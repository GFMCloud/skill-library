#!/usr/bin/env python3
"""Combine k blind judge passes into one design-jury result and apply the floor gate.

Usage:
    python3 aggregate.py <floors.json> <purpose> <out-dir> <judge-1.json> [<judge-2.json> ...]

    floors.json  per-medium floors file, e.g. references/floors-web.json
    purpose      a key of floors.json["purposes"], e.g. showcase or product
    out-dir      where report.md and verdict.yaml are written

Each judge file is one pass in the shape `design-jury-judge/v1` (see
references/judge-prompt.md): integer 1-10 scores for the medium's categories, evidence,
improvements, not_observed.

Per category: the median of the passes is the score and max minus min is the spread. A
spread above SPREAD_LIMIT marks the category unstable. APPROVED requires every category's
median at or above its floor and no unstable category. The weighted overall is reported
for information and never gates.

Exit codes: 0 APPROVED, 1 NOT APPROVED, 2 bad input.
"""

import json
import statistics
import sys
from pathlib import Path

SPREAD_LIMIT = 2


def fail_input(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(2)


def load_judge(path, categories):
    try:
        data = json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail_input(f"{path}: {exc}")
    if data.get("judge") != "design-jury-judge/v1":
        fail_input(f"{path}: judge field is {data.get('judge')!r}, expected 'design-jury-judge/v1'")
    for cat in categories:
        score = data.get("scores", {}).get(cat)
        if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 10:
            fail_input(f"{path}: scores.{cat} is {score!r}, expected an integer 1-10")
        evidence = data.get("evidence", {}).get(cat)
        if not evidence or not isinstance(evidence, list):
            fail_input(f"{path}: evidence.{cat} is empty or not a list; a score without evidence is not accepted")
        for i, e in enumerate(evidence):
            if not isinstance(e, dict) or not isinstance(e.get("where"), str) or not isinstance(e.get("observed"), str):
                fail_input(f"{path}: evidence.{cat}[{i}] needs string fields where and observed")
            if e.get("effect") not in ("+", "-", "0"):
                fail_input(f"{path}: evidence.{cat}[{i}].effect is {e.get('effect')!r}, expected +, - or 0")
    return data


def main(argv):
    if len(argv) < 5:
        fail_input(__doc__.split("\n\n")[1])
    floors_path, purpose, out_dir, judge_paths = argv[1], argv[2], Path(argv[3]), argv[4:]
    try:
        floors = json.loads(Path(floors_path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail_input(f"{floors_path}: {exc}")
    if purpose not in floors["purposes"]:
        fail_input(f"purpose {purpose!r} not in {sorted(floors['purposes'])}")
    categories = list(floors["weights"])
    floor = floors["purposes"][purpose]
    judges = [load_judge(p, categories) for p in judge_paths]
    targets = {j.get("target") for j in judges}
    if len(targets) != 1:
        fail_input(f"judge files name different targets: {sorted(map(str, targets))}")
    target = targets.pop()

    rows, issues = [], []
    for cat in categories:
        scores = [j["scores"][cat] for j in judges]
        med = statistics.median(scores)
        spread = max(scores) - min(scores)
        unstable = len(scores) > 1 and spread > SPREAD_LIMIT
        passed = med >= floor[cat] and not unstable
        rows.append((cat, scores, med, spread, floor[cat], unstable, passed))
        if not passed:
            gap = floor[cat] - med
            why = (f"judges disagree by {spread} points (limit {SPREAD_LIMIT})" if unstable
                   else f"median {med:g} is {gap:g} below the floor of {floor[cat]:g}")
            first_fix = next((imp for j in judges for imp in j.get("improvements", {}).get(cat, [])), "none given")
            issues.append({
                "id": len(issues) + 1,
                "where": f"{cat} ({', '.join(e['where'] for e in judges[0]['evidence'][cat][:2])})",
                "what": f"{cat}: {why}. First fix: {first_fix}",
                "evidence": f"{len(judges)} blind judge passes Read the render set → {cat} scores {scores}",
                "gap": gap if not unstable else 0,
            })

    weighted = sum(floors["weights"][c] * r[2] for c, r in zip(categories, rows))
    approved = not issues
    max_spread = max(r[3] for r in rows)
    worst_gap = max((i["gap"] for i in issues), default=0)
    severity = "none" if approved else "high" if worst_gap >= 2 else "medium" if worst_gap >= 1 else "low"
    confidence = round(max(0.1, 1 - max_spread / 10), 2)

    out_dir.mkdir(parents=True, exist_ok=True)
    verdict = ["verdict: v1", f"target: {target}", f"result: {'pass' if approved else 'fail'}",
               f"severity: {severity}", f"confidence: {confidence}"]
    if approved:
        verdict.append("issues: []")
    else:
        verdict.append("issues:")
        for i in issues:
            verdict += [f"  - id: {i['id']}"] + [
                f"    {k}: {json.dumps(i[k], ensure_ascii=False)}" for k in ("where", "what", "evidence")]
    verdict.append("new_information: false")
    (out_dir / "verdict.yaml").write_text("\n".join(verdict) + "\n")

    status = floors.get("status", "PROPOSED")
    lines = [
        f"# design-jury: {'APPROVED' if approved else 'NOT APPROVED'}",
        "",
        f"Target: {target}  ",
        f"Medium: {floors['medium']}. Purpose: {purpose}. Judge passes: {len(judges)}.  ",
        f"Floors: {status}" + (f" ({floors['approved']})" if floors.get("approved") else "") + ".",
        "",
        "| Category | Weight | Passes | Median | Spread | Floor | Result |",
        "|---|---|---|---|---|---|---|",
    ]
    for cat, scores, med, spread, fl, unstable, passed in rows:
        result = "pass" if passed else ("UNSTABLE" if unstable else "below floor")
        lines.append(f"| {cat} | {floors['weights'][cat]:.0%} | {', '.join(map(str, scores))} | {med:g} "
                     f"| {spread} | {fl:g} | {result} |")
    lines += ["", f"Weighted overall (information only, never gates): {weighted:.2f}", ""]
    for cat in categories:
        lines.append(f"## {cat.capitalize()}")
        lines.append("")
        lines.append("Evidence (pass 1):")
        for e in judges[0]["evidence"][cat]:
            lines.append(f"- `{e['where']}` ({e.get('effect', '?')}) {e['observed']}")
        imps = [imp for j in judges for imp in j.get("improvements", {}).get(cat, [])]
        if imps:
            lines.append("")
            lines.append("To improve (all passes, deduplicated):")
            for imp in dict.fromkeys(imps):
                lines.append(f"- {imp}")
        lines.append("")
    not_obs = sorted({n for j in judges for n in j.get("not_observed", [])})
    lines += ["## Not observed", "", *[f"- {n}" for n in not_obs], ""]
    lines += ["## Labels", "", *[f"- {label}" for label in floors.get("labels", [])], ""]
    (out_dir / "report.md").write_text("\n".join(lines))

    print("\n".join(lines[:len(categories) + 9]))
    print(f"wrote {out_dir / 'report.md'} and {out_dir / 'verdict.yaml'}")
    return 0 if approved else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
