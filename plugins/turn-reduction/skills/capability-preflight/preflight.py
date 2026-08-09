#!/usr/bin/env python3
"""capability-preflight — prove access to every system a milestone must touch, before it starts.

Reads a manifest of capabilities. For each one it exercises a real read, a real write, and a
negative control that must fail. Anything unproven comes back in a single batch at the end.

Exit codes:
  0  every capability proven (non-blocking verified-unreachable entries allowed)
  1  at least one capability not proven — see BLOCKERS
  2  manifest rejected before anything ran

Stdlib only. Runs on Python 3.9+.
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_TIMEOUT = 30
EXCERPT_CHARS = 400

# Constructs that let a probe report success without examining anything.
# `grep ... || echo "OK"` once printed a green tick for a directory that did not exist.
MASKING_CONSTRUCTS = [
    ("||", "`||` can substitute a success for a failure"),
    ("; true", "`; true` discards the real exit code"),
    ("&& true", "`&& true` obscures which command's status is reported"),
    ("set +e", "`set +e` disables exit-code propagation"),
    ("; exit 0", "`; exit 0` forces success"),
]

SECRET_PATTERNS = [
    re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}"),
    re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"),
    re.compile(r"\bxox[abposr]-[A-Za-z0-9\-]{10,}"),
    re.compile(r"(?i)\b(?:bearer|token|api[_-]?key|password|secret)\b\s*[:=]?\s*\S{8,}"),
    re.compile(r"\b[A-Za-z0-9_\-]{40,}\b"),
]

# Commit SHAs and content hashes are evidence, not credentials — the length rule would eat them.
HASH_SHAPED = re.compile(r"^[0-9a-f]{40}$|^[0-9a-f]{64}$")


def _mask(match):
    return match.group(0) if HASH_SHAPED.match(match.group(0)) else "[redacted]"


def redact(text):
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(_mask, text)
    return text


def excerpt(text):
    flat = " ".join(redact(text).split())
    if len(flat) > EXCERPT_CHARS:
        flat = flat[:EXCERPT_CHARS] + "…"
    return flat


# --------------------------------------------------------------------------------------
# evidence rules
# --------------------------------------------------------------------------------------

def parse_evidence(rule):
    """Return (kind, argument) or raise ValueError. Rules are required, never defaulted."""
    if not isinstance(rule, str) or not rule.strip():
        raise ValueError("evidence rule must be a non-empty string")
    rule = rule.strip()
    if rule == "nonempty":
        return ("nonempty", None)
    m = re.match(r"^count>(\d+)$", rule)
    if m:
        return ("count", int(m.group(1)))
    m = re.match(r"^lines>=(\d+)$", rule)
    if m:
        return ("lines", int(m.group(1)))
    if rule.startswith("contains:"):
        return ("contains", rule[len("contains:"):])
    raise ValueError(
        "unknown evidence rule %r — use nonempty, count>N, lines>=N, or contains:TEXT" % rule
    )


def check_evidence(rule, stdout):
    """Did this probe actually examine something? Returns (satisfied, human explanation)."""
    kind, arg = parse_evidence(rule)
    body = stdout.strip()
    if kind == "nonempty":
        return (bool(body), "stdout %s" % ("carried output" if body else "was empty"))
    if kind == "count":
        token = body.split()[-1] if body.split() else ""
        try:
            value = int(token)
        except ValueError:
            return (False, "stdout %r does not end in an integer to compare against %d" % (excerpt(body), arg))
        return (value > arg, "counted %d, needed >%d" % (value, arg))
    if kind == "lines":
        n = len([ln for ln in body.splitlines() if ln.strip()])
        return (n >= arg, "%d non-blank lines, needed >=%d" % (n, arg))
    if kind == "contains":
        return (arg in stdout, "stdout %s %r" % ("contains" if arg in stdout else "does not contain", arg))
    return (False, "unreachable")


def parse_expect(rule):
    if rule is None:
        return ("nonzero_exit", None)
    if not isinstance(rule, str) or not rule.strip():
        raise ValueError("expect must be a non-empty string")
    rule = rule.strip()
    if rule == "nonzero_exit":
        return ("nonzero_exit", None)
    if rule.startswith("not_contains:"):
        return ("not_contains", rule[len("not_contains:"):])
    if rule.startswith("contains:"):
        return ("contains", rule[len("contains:"):])
    raise ValueError(
        "unknown expect rule %r — use nonzero_exit, contains:TEXT, or not_contains:TEXT" % rule
    )


def check_expect(rule, result):
    kind, arg = parse_expect(rule)
    if kind == "nonzero_exit":
        return (result["exit"] != 0, "exited %d, needed non-zero" % result["exit"])
    if kind == "contains":
        got = arg in result["stdout"]
        return (got, "stdout %s %r" % ("contains" if got else "does not contain", arg))
    if kind == "not_contains":
        got = arg not in result["stdout"]
        return (got, "stdout %s %r" % ("does not contain" if got else "contains", arg))
    return (False, "unreachable")


# --------------------------------------------------------------------------------------
# manifest validation — everything below runs before a single probe does
# --------------------------------------------------------------------------------------

def _require_text(obj, key, where, errors):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append("%s: %r must be a non-empty string" % (where, key))
        return None
    return value


def _validate_cmd(cmd, where, errors):
    if not isinstance(cmd, str) or not cmd.strip():
        errors.append("%s: 'cmd' must be a non-empty string" % where)
        return
    for construct, why in MASKING_CONSTRUCTS:
        if construct in cmd:
            errors.append(
                "%s: command contains %s — %s. A probe must be able to report failure."
                % (where, construct, why)
            )


def _validate_probe(probe, where, errors, needs_evidence=True):
    if not isinstance(probe, dict):
        errors.append("%s: must be an object with 'cmd'" % where)
        return
    _validate_cmd(probe.get("cmd"), where, errors)
    if needs_evidence:
        try:
            parse_evidence(probe.get("evidence"))
        except ValueError as exc:
            errors.append("%s: %s" % (where, exc))
    timeout = probe.get("timeout", DEFAULT_TIMEOUT)
    if not isinstance(timeout, int) or timeout <= 0:
        errors.append("%s: 'timeout' must be a positive integer number of seconds" % where)


def validate(manifest):
    errors = []
    if not isinstance(manifest, dict):
        return ["manifest root must be a JSON object"]
    _require_text(manifest, "milestone", "manifest", errors)

    caps = manifest.get("capabilities")
    if not isinstance(caps, list) or not caps:
        errors.append("manifest: 'capabilities' must be a non-empty array")
        return errors

    seen = set()
    for i, cap in enumerate(caps):
        where = "capabilities[%d]" % i
        if not isinstance(cap, dict):
            errors.append("%s: must be an object" % where)
            continue
        name = _require_text(cap, "name", where, errors)
        if name:
            where = "capability %r" % name
            if name in seen:
                errors.append("%s: duplicate capability name" % where)
            seen.add(name)
        # Scope travels with the result, always. A diagnostic that ran only against records
        # holding a prior-season slot passed for two sessions without ever seeing the cases
        # it existed to catch.
        _require_text(cap, "population", where, errors)
        _require_text(cap, "excludes", where, errors)
        _require_text(cap, "remedy", where, errors)

        if "declared_unreachable" in cap:
            du = cap["declared_unreachable"]
            if not isinstance(du, dict):
                errors.append("%s: 'declared_unreachable' must be an object" % where)
                continue
            _require_text(du, "why", "%s.declared_unreachable" % where, errors)
            if "probe" not in du:
                errors.append(
                    "%s: 'declared_unreachable' needs a 'probe' that is run and must fail. "
                    "A tooling limit is a claim until the running system refutes it." % where
                )
            else:
                _validate_probe(du["probe"], "%s.declared_unreachable.probe" % where, errors,
                                needs_evidence=False)
            continue

        for key in ("read", "write"):
            if key not in cap:
                errors.append("%s: missing %r probe — access is proven by exercising it, "
                              "both directions" % (where, key))
            else:
                _validate_probe(cap[key], "%s.%s" % (where, key), errors)

        if "negative_control" not in cap:
            errors.append(
                "%s: missing 'negative_control'. A probe that cannot fail proves nothing — "
                "an auth check once returned 200 from an endpoint that answers the same with "
                "no credential at all." % where
            )
        else:
            nc = cap["negative_control"]
            if not isinstance(nc, dict):
                errors.append("%s.negative_control: must be an object" % where)
            else:
                _validate_probe(nc, "%s.negative_control" % where, errors, needs_evidence=False)
                _require_text(nc, "why", "%s.negative_control" % where, errors)
                try:
                    parse_expect(nc.get("expect"))
                except ValueError as exc:
                    errors.append("%s.negative_control: %s" % (where, exc))
    return errors


# --------------------------------------------------------------------------------------
# running
# --------------------------------------------------------------------------------------

def run_probe(probe, cwd):
    cmd = probe["cmd"]
    timeout = probe.get("timeout", DEFAULT_TIMEOUT)
    env = dict(os.environ)
    for key, value in (probe.get("env") or {}).items():
        env[str(key)] = str(value)
    try:
        completed = subprocess.run(
            ["bash", "-c", cmd],
            cwd=cwd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return {
            "cmd": cmd,
            "exit": completed.returncode,
            "stdout": completed.stdout.decode("utf-8", "replace"),
            "stderr": completed.stderr.decode("utf-8", "replace"),
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {"cmd": cmd, "exit": 124, "stdout": "", "stderr": "timed out after %ds" % timeout,
                "timed_out": True}


def assess_probe(probe, result):
    """A probe passes only when it exited clean AND is shown to have examined something."""
    if result["timed_out"]:
        return ("TIMED OUT", "no result after %ds" % probe.get("timeout", DEFAULT_TIMEOUT))
    if result["exit"] != 0:
        detail = excerpt(result["stderr"] or result["stdout"]) or "no output"
        return ("FAILED", "exit %d — %s" % (result["exit"], detail))
    satisfied, why = check_evidence(probe["evidence"], result["stdout"])
    if not satisfied:
        # Exit 0 with nothing examined is the false green this whole script exists for.
        return ("INCONCLUSIVE", "exit 0 but examined nothing provable: %s" % why)
    return ("PROVEN", why)


def assess_capability(cap, cwd):
    """Returns a result record. Never raises; never stops the batch."""
    record = {
        "name": cap["name"],
        "population": cap["population"],
        "excludes": cap["excludes"],
        "remedy": cap["remedy"],
        "probes": [],
        "reasons": [],
    }

    if "declared_unreachable" in cap:
        du = cap["declared_unreachable"]
        result = run_probe(du["probe"], cwd)
        blocking = du.get("blocking", True)
        record["kind"] = "declared_unreachable"
        record["why"] = du["why"]
        record["blocking"] = bool(blocking)
        record["probes"].append({"role": "unreachability probe", "result": result,
                                 "verdict": "ran"})
        if result["exit"] == 0 and not result["timed_out"]:
            # The device bridge existed and no folder had been connected. A setup step nobody
            # took, filed as a tooling limit.
            record["verdict"] = "FALSE-ARCHITECTURAL-CLAIM"
            record["blocking"] = True
            record["reasons"].append(
                "declared unreachable, but the probe succeeded (exit 0). This is a setup step "
                "nobody took, not a tooling limit. Output: %s" % (excerpt(result["stdout"]) or "none")
            )
        else:
            record["verdict"] = "UNREACHABLE (verified)"
            record["reasons"].append(
                "probe failed as claimed (exit %d), so the limit is real" % result["exit"]
            )
        return record

    record["kind"] = "capability"
    record["blocking"] = True
    ok = True

    for role in ("read", "write"):
        probe = cap[role]
        result = run_probe(probe, cwd)
        verdict, why = assess_probe(probe, result)
        record["probes"].append({"role": role, "result": result, "verdict": verdict, "why": why})
        if verdict != "PROVEN":
            ok = False
            record["reasons"].append("%s %s — %s" % (role, verdict.lower(), why))

    nc = cap["negative_control"]
    nc_result = run_probe(nc, cwd)
    discriminating, why = check_expect(nc.get("expect"), nc_result)
    record["probes"].append({
        "role": "negative control",
        "result": nc_result,
        "verdict": "DISCRIMINATING" if discriminating else "NOT DISCRIMINATING",
        "why": why,
        "control_why": nc["why"],
    })
    if not discriminating:
        ok = False
        record["reasons"].append(
            "negative control did not fail (%s) — the probe would return the same answer with "
            "no access at all, so it proves nothing" % why
        )

    record["verdict"] = "PROVEN" if ok else "NOT PROVEN"
    return record


# --------------------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------------------

def report(manifest, records, stream):
    write = stream.write
    write("capability pre-flight — %s\n" % manifest["milestone"])
    write("=" * 78 + "\n\n")

    for rec in records:
        write("CAPABILITY  %s\n" % rec["name"])
        write("  population  %s\n" % rec["population"])
        write("  excludes    %s\n" % rec["excludes"])
        for probe in rec["probes"]:
            write("  %-18s %s\n" % (probe["role"], probe["verdict"]))
            write("      $ %s\n" % probe["result"]["cmd"])
            if probe.get("why"):
                write("      %s\n" % probe["why"])
            if probe["role"] == "negative control":
                write("      control asserts: %s\n" % probe["control_why"])
            out = excerpt(probe["result"]["stdout"])
            if out:
                write("      stdout: %s\n" % out)
        write("  => %s\n\n" % rec["verdict"])

    blockers = [r for r in records if r["verdict"] != "PROVEN" and r["blocking"]]
    routed = [r for r in records if r["verdict"] == "UNREACHABLE (verified)" and not r["blocking"]]

    if routed:
        write("ROUTED AROUND — verified unreachable, the plan does not depend on it\n")
        write("-" * 78 + "\n")
        for rec in routed:
            write("  %s: %s\n" % (rec["name"], rec["why"]))
        write("\n")

    write("SCOPE OF THIS RESULT\n")
    write("-" * 78 + "\n")
    write("  %d capabilities declared in the manifest and all %d were exercised.\n"
          % (len(records), len(records)))
    write("  This says nothing about any system the manifest does not name. Each capability's\n")
    write("  population and excludes are printed above and bound its result only.\n\n")

    if not blockers:
        write("PRE-FLIGHT PASSED — every declared capability proven by exercise. Work may start.\n")
        return 0

    write("BLOCKERS — %d, all of them, before work starts\n" % len(blockers))
    write("-" * 78 + "\n")
    for i, rec in enumerate(blockers, 1):
        write("%d. %s — %s\n" % (i, rec["name"], rec["verdict"]))
        for reason in rec["reasons"]:
            write("     why:    %s\n" % reason)
        write("     needed: %s\n" % rec["remedy"])
    write("\nNothing in this milestone starts until every item above is cleared.\n")
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="preflight.py",
        description="Prove access to every system a milestone must touch, before it starts.",
    )
    parser.add_argument("manifest", help="path to the capability manifest (JSON)")
    parser.add_argument("--cwd", default=None,
                        help="working directory probes run in (default: the manifest's directory)")
    parser.add_argument("--json", dest="json_out", default=None,
                        help="also write the full record to this path")
    parser.add_argument("--validate-only", action="store_true",
                        help="check the manifest and exit without running any probe")
    args = parser.parse_args(argv)

    try:
        with open(args.manifest, "r") as handle:
            manifest = json.load(handle)
    except (IOError, OSError) as exc:
        sys.stderr.write("cannot read manifest: %s\n" % exc)
        return 2
    except ValueError as exc:
        sys.stderr.write("manifest is not valid JSON: %s\n" % exc)
        return 2

    errors = validate(manifest)
    if errors:
        sys.stderr.write("MANIFEST REJECTED — nothing was run.\n")
        for err in errors:
            sys.stderr.write("  - %s\n" % err)
        return 2
    if args.validate_only:
        sys.stdout.write("manifest accepted: %d capabilities, no probe run (--validate-only)\n"
                         % len(manifest["capabilities"]))
        return 0

    cwd = args.cwd or os.path.dirname(os.path.abspath(args.manifest)) or os.getcwd()
    records = [assess_capability(cap, cwd) for cap in manifest["capabilities"]]
    code = report(manifest, records, sys.stdout)

    if args.json_out:
        payload = {"milestone": manifest["milestone"], "exit_code": code, "capabilities": records}
        with open(args.json_out, "w") as handle:
            json.dump(payload, handle, indent=2)
            handle.write("\n")
    return code


if __name__ == "__main__":
    sys.exit(main())
