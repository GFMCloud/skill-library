#!/usr/bin/env python3
"""Measure a design-jury judge against human jury scores.

Usage:
    python3 calibrate.py <ground-truth.json> <runs-dir> [--held-out slug,slug,...]

    ground-truth.json  array of records with `slug` and `scores` {category: mean jury score}
                       and optionally `juror_sd` {category: sd}; for the web medium this is
                       the calibration set behind references/calibration-web.md
    runs-dir           one subdirectory per slug holding judge-*.json files
                       (design-jury-judge/v1); the median of a slug's passes is its score

Records may instead carry only a `tier` (an ordinal label such as an award level) with no
`scores`; with a top-level `tier_order` list (best first), the report adds the judge's
weighted overall per tier and the share of cross-tier site pairs it orders correctly.

Prints, per category and for the weighted overall where weights are given in the ground
truth file's top level (`{"weights": {...}, "tier_order": [...], "records": [...]}`) or as
a bare array without weights: mean absolute error (MAE), mean signed error (bias: positive means the judge
scores higher than the jury), Spearman rank correlation, and the mean juror SD as the human
baseline. Held-out slugs are reported as their own block and are excluded from the tuning
block, so a rubric tuned on the tuning block is tested on sites it never saw.

Exit codes: 0 report printed, 2 bad input. The numbers are a measurement, not a gate.
"""

import json
import statistics
import sys
from pathlib import Path


def fail_input(msg):
    print(f"STOP: {msg}", file=sys.stderr)
    sys.exit(2)


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    r = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs, ys):
    if len(xs) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
        return None
    rx, ry = ranks(xs), ranks(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den


def block(name, pairs, categories, weights):
    print(f"\n## {name}: {len(pairs)} sites")
    if not pairs:
        print("(none)")
        return
    print("| Category | MAE | MAE of always-7 | Bias | Spearman | Mean juror SD |")
    print("|---|---|---|---|---|---|")
    cols = list(categories) + (["overall"] if weights else [])
    for cat in cols:
        if cat == "overall":
            jy = [sum(weights[c] * p["judge"][c] for c in categories) for p in pairs]
            hy = [sum(weights[c] * p["jury"][c] for c in categories) for p in pairs]
            sd = None
        else:
            jy = [p["judge"][cat] for p in pairs]
            hy = [p["jury"][cat] for p in pairs]
            sds = [p["sd"][cat] for p in pairs if p["sd"].get(cat) is not None]
            sd = statistics.mean(sds) if sds else None
        mae = statistics.mean(abs(a - b) for a, b in zip(jy, hy))
        # A judge that answers 7 for everything: the score to beat on a top-tier-only set.
        base = statistics.mean(abs(7 - b) for b in hy)
        bias = statistics.mean(a - b for a, b in zip(jy, hy))
        rho = spearman(jy, hy)
        print(f"| {cat} | {mae:.2f} | {base:.2f} | {bias:+.2f} | {'n/a' if rho is None else f'{rho:.2f}'} "
              f"| {'n/a' if sd is None else f'{sd:.2f}'} |")


def main(argv):
    if len(argv) < 3:
        fail_input(__doc__.split("\n\n")[1])
    truth_path, runs_dir = Path(argv[1]), Path(argv[2])
    held_out = set()
    if "--held-out" in argv:
        held_out = set(argv[argv.index("--held-out") + 1].split(","))
    try:
        truth = json.loads(truth_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail_input(f"{truth_path}: {exc}")
    weights = truth.get("weights") if isinstance(truth, dict) else None
    tier_order = truth.get("tier_order") if isinstance(truth, dict) else None
    records = truth["records"] if isinstance(truth, dict) else truth
    scored = [r for r in records if r.get("scores")]
    categories = list(weights) if weights else list(scored[0]["scores"])

    tuning, held, missing, tiered = [], [], [], []
    for rec in records:
        files = sorted((runs_dir / rec["slug"]).glob("judge-*.json"))
        if not files:
            missing.append(rec["slug"])
            continue
        passes = [json.loads(f.read_text())["scores"] for f in files]
        judge = {c: statistics.median(p[c] for p in passes) for c in categories}
        if rec.get("tier"):
            overall = sum(weights[c] * judge[c] for c in categories) if weights else statistics.mean(judge.values())
            tiered.append((rec["slug"], rec["tier"], overall))
        if not rec.get("scores"):
            continue
        pair = {"slug": rec["slug"], "judge": judge, "jury": rec["scores"],
                "sd": rec.get("juror_sd") or {}, "passes": len(passes)}
        (held if rec["slug"] in held_out else tuning).append(pair)

    unknown = held_out - {r["slug"] for r in records}
    if unknown:
        fail_input(f"held-out slugs not in ground truth: {sorted(unknown)}")
    print(f"# Calibration: {truth_path.name} vs {runs_dir}")
    print(f"Judged: {len(records) - len(missing)} of {len(records)}. Not judged: {', '.join(missing) or 'none'}.")
    block("Tuning set", tuning, categories, weights)
    block("Held-out set", held, categories, weights)
    if tier_order and tiered:
        print(f"\n## Ordinal tiers ({' > '.join(tier_order)}): judge weighted overall")
        print("| Tier | Sites | Mean | Min | Max |")
        print("|---|---|---|---|---|")
        for t in tier_order:
            xs = [o for _, tier, o in tiered if tier == t]
            if xs:
                print(f"| {t} | {len(xs)} | {statistics.mean(xs):.2f} | {min(xs):.2f} | {max(xs):.2f} |")
        rank = {t: i for i, t in enumerate(tier_order)}
        right = ties = total = 0
        for i, (_, ta, oa) in enumerate(tiered):
            for _, tb, ob in tiered[i + 1:]:
                if ta == tb:
                    continue
                total += 1
                hi, lo = (oa, ob) if rank[ta] < rank[tb] else (ob, oa)
                right += hi > lo
                ties += hi == lo
        print(f"\nCross-tier pairs ordered correctly: {right} of {total} ({right / total:.0%}); "
              f"tied: {ties}; chance level: 50%.")
    print("\n## Per site (judge median vs jury mean)")
    for p in tuning + held:
        tag = " (held out)" if p in held else ""
        cells = ", ".join(f"{c[:3]} {p['judge'][c]:g}/{p['jury'][c]:.2f}" for c in categories)
        print(f"- {p['slug']}{tag}, {p['passes']} pass(es): {cells}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
