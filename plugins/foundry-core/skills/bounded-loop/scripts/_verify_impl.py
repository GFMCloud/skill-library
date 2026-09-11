#!/usr/bin/env python3
"""Implementation for stop-hook-verify.sh. Not called directly.

Reads its configuration from environment variables set by the wrapper
(CHECK, BUDGET, REPO, STATE, ESCALATION_OUT, GOAL_TEXT, HOOK_STDIN) plus
guard paths as argv. See stop-hook-verify.sh for the contract and
references/stop-hook-contract.md for the hook doc lines this implements.

Attempt-fingerprint design decision: this treats "the attempt's diff" as a
content snapshot hash of the repo tree (path, size, sha256 of every tracked
file, excluding .git and the hook's own state/escalation output) rather than
a literal `git diff`. That works whether or not --repo is a git checkout,
which is what lets the deliberate-failure fixtures be plain directories
instead of nested git repos inside the library. Known limitation: a snapshot
hash cannot distinguish "reverted then reapplied" from "never touched" the
way a true diff against a fixed baseline can; for the bounded, small-task
scope this skill is for (see SKILL.md "Scope note"), that gap has not
mattered in practice testing this script.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

CAUSE_TEST_FILE = "test_file_modified"
CAUSE_NO_PROGRESS = "no_progress"
CAUSE_UNREACHABLE = "unreachable_condition"
CAUSE_AMBIGUOUS = "ambiguous_check_feedback"


def eprint(*a):
    print(*a, file=sys.stderr)


def snapshot_hash(root, subpaths=None, exclude_abs=()):
    """Hash (relpath, size, content) of every file under root, or only under
    subpaths when given. Deterministic regardless of mtime or file order."""
    h = hashlib.sha256()
    exclude_abs = {os.path.realpath(p) for p in exclude_abs}
    roots = [os.path.join(root, p) for p in subpaths] if subpaths else [root]
    files = []
    for r in roots:
        if os.path.isfile(r):
            files.append(r)
            continue
        for base, dirs, names in os.walk(r):
            dirs[:] = [d for d in dirs if d != ".git"]
            for n in names:
                files.append(os.path.join(base, n))
    files = sorted(set(os.path.realpath(f) for f in files))
    for f in files:
        if f in exclude_abs or not os.path.isfile(f):
            continue
        rel = os.path.relpath(f, os.path.realpath(root))
        try:
            with open(f, "rb") as fh:
                data = fh.read()
        except OSError:
            continue
        h.update(rel.encode())
        h.update(str(len(data)).encode())
        h.update(data)
    return h.hexdigest()[:12]


def load_state(path):
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {
        "attempts": [],
        "last_diff_hash": None,
        "last_guard_hash": None,
        "repeat_count": 0,
        "status": "in_progress",
    }


def save_state(path, state):
    os.makedirs(os.path.dirname(os.path.realpath(path)) or ".", exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, path)


def yaml_block_scalar(text, indent="  "):
    lines = text.splitlines() or [""]
    return "\n".join(indent + l for l in lines)


def write_escalation(path, goal_text, attempts, budget, last_output, cause, causes, question):
    lines = []
    lines.append("escalation: v1")
    lines.append(f"goal_block: {goal_text}")
    lines.append(f"attempts: {len(attempts)} of {budget}")
    lines.append("last_failing_output: |")
    lines.append(yaml_block_scalar(last_output))
    lines.append("tried:")
    for a in attempts:
        lines.append(
            f"  - {{attempt: {a['n']}, diff_hash: {a['diff_hash']}, "
            f"summary: {a['summary']}}}"
        )
    lines.append(f"cause_class: {cause}")
    lines.append("likely_causes: [" + ", ".join(causes) + "]")
    lines.append(f"question: {question}")
    content = "\n".join(lines) + "\n"
    os.makedirs(os.path.dirname(os.path.realpath(path)) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return content


def summarize(output, n=1):
    first = next((l for l in output.splitlines() if l.strip()), "").strip()
    return (first[:77] + "...") if len(first) > 80 else (first or f"attempt {n}")


def main():
    guard_paths = sys.argv[1:]
    check = os.environ["CHECK"]
    budget = int(os.environ.get("BUDGET") or "3")
    goal_text = os.environ.get("GOAL_TEXT") or "not provided"

    hook_stdin = os.environ.get("HOOK_STDIN") or ""
    stdin_cwd = None
    if hook_stdin.strip():
        try:
            stdin_cwd = json.loads(hook_stdin).get("cwd")
        except (json.JSONDecodeError, AttributeError):
            pass

    repo = os.environ.get("REPO") or stdin_cwd or os.getcwd()
    repo = os.path.realpath(repo)
    state_path = os.environ.get("STATE") or os.path.join(repo, ".bounded-loop", "state.json")
    escalation_out = os.environ.get("ESCALATION_OUT") or os.path.join(
        os.path.dirname(os.path.realpath(state_path)), "escalation.yaml"
    )

    state = load_state(state_path)

    if state.get("status") == "escalated":
        # Already handed back; a further Stop event finds nothing new to gate.
        eprint("bounded-loop: already escalated; see", escalation_out)
        sys.exit(0)
    if state.get("status") == "passed":
        eprint("bounded-loop: target already met; nothing to gate")
        sys.exit(0)

    exclude = {state_path, escalation_out}
    diff_hash = snapshot_hash(repo, exclude_abs=exclude)
    guard_hash = snapshot_hash(repo, subpaths=guard_paths, exclude_abs=exclude) if guard_paths else None

    # Run the check unconditionally: even the guard-fail path needs its
    # verbatim output for last_failing_output, and the escalation.yaml is
    # cause_class: test_file_modified regardless of what the check returned.
    proc = subprocess.run(["bash", "-c", check], cwd=repo,
                           capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    passed = proc.returncode == 0

    guard_fired = (
        guard_paths
        and state.get("last_guard_hash") is not None
        and guard_hash != state["last_guard_hash"]
    )
    if guard_paths:
        state["last_guard_hash"] = guard_hash

    if guard_fired:
        state["status"] = "escalated"
        save_state(state_path, state)
        report = write_escalation(
            escalation_out, goal_text, state["attempts"], budget, output,
            CAUSE_TEST_FILE,
            [
                "a guarded verifier or test file changed between attempts",
                "the check's real result cannot be trusted while that file is in question",
            ],
            "the guarded files changed between attempts; should this attempt's "
            "changes to them be reviewed and reverted, or was the update intended?",
        )
        print(report)
        eprint("bounded-loop: guarded file changed; automatic fail, escalation written to", escalation_out)
        sys.exit(0)

    is_repeat = diff_hash == state.get("last_diff_hash")
    if is_repeat:
        state["repeat_count"] = state.get("repeat_count", 0) + 1
    else:
        state["repeat_count"] = 0
        state["last_diff_hash"] = diff_hash

    if passed:
        state["status"] = "passed"
        if not is_repeat:
            n = len(state["attempts"]) + 1
            state["attempts"].append({"n": n,
                                       "diff_hash": diff_hash,
                                       "summary": summarize(output, n)})
        save_state(state_path, state)
        print(f"bounded-loop: target met at attempt {len(state['attempts'])}")
        print("check output:")
        print(output)
        sys.exit(0)

    if not is_repeat:
        n = len(state["attempts"]) + 1
        state["attempts"].append({"n": n,
                                   "diff_hash": diff_hash,
                                   "summary": summarize(output, n)})
        state["attempts"][-1]["check_output"] = output
    save_state(state_path, state)

    attempts = state["attempts"]

    if state["repeat_count"] >= 1:
        state["status"] = "escalated"
        save_state(state_path, state)
        report = write_escalation(
            escalation_out, goal_text, attempts, budget, output,
            CAUSE_NO_PROGRESS,
            [
                "two consecutive attempts produced no change to the workspace",
                "the agent may be stuck re-proposing the same fix",
            ],
            "no code changed between the last two attempts while the check "
            "still fails; is there a different approach worth trying, or is "
            "this one blocked on something outside the repo?",
        )
        print(report)
        eprint("bounded-loop: two consecutive identical attempts; escalation written to", escalation_out)
        sys.exit(0)

    if len(attempts) >= budget:
        outputs = {a.get("check_output", "") for a in attempts}
        cause = CAUSE_UNREACHABLE if len(outputs) == 1 else CAUSE_AMBIGUOUS
        if cause == CAUSE_UNREACHABLE:
            causes = [
                "the check's failing output never changed across attempts despite different diffs",
                "the condition the check enforces may not be satisfiable as written",
            ]
            question = ("the check output was identical on every attempt; is the "
                         "check itself wrong, or is the target genuinely unreachable "
                         "from here?")
        else:
            causes = [
                "the check's feedback changed each attempt without converging",
                "the check may be asserting something the ask did not actually require",
            ]
            question = "which of the check's failures is the one that must pass?"
        state["status"] = "escalated"
        save_state(state_path, state)
        report = write_escalation(escalation_out, goal_text, attempts, budget,
                                   output, cause, causes, question)
        print(report)
        eprint(f"bounded-loop: budget exhausted ({len(attempts)} of {budget}); "
               f"escalation written to {escalation_out}")
        sys.exit(0)

    # Fail, budget remains: block the turn. Per the hooks doc, exit 2's
    # blocking message is "your stderr text" when no JSON blocking decision
    # is printed (references/stop-hook-contract.md quotes this exactly), so
    # the check's verbatim output on stderr is what reaches Claude to keep
    # working.
    eprint(f"bounded-loop: attempt {len(attempts)} of {budget} failed, check output follows")
    eprint(output)
    sys.exit(2)


if __name__ == "__main__":
    main()
