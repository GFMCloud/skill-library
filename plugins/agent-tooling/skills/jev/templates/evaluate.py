# evaluate.py: run questions.judge over items with known answers and report agreement.
#
#   python evaluate.py tuning          # iterate on this set
#   python evaluate.py heldout         # run once, after the questions are settled
#   python evaluate.py tuning 3        # three trials, to see run-to-run noise
#
# Known answers are past decisions (someone's calls), so this reports AGREEMENT, not
# accuracy. Replace load_items() with the project's own source; keep the fixed split.
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

from typesafe_sdk import TypeSafeClient

from questions import judge

PRICE_PER_M_INPUT = 0.042  # docs pricing on 2026-09-27; confirm on the live pricing page
HELDOUT_SHARE = 0.4
SEED = 7  # fixed, so the split never moves between runs


def load_items():
    """Return [{"id", "expected", "candidate", "reference"}]. Build the evidence here, in
    full, as it stood when each past decision was made. Replace this fixture loader."""
    return json.loads(Path("<LABELLED_ITEMS>.json").read_text())


def split(items):
    shuffled = sorted(items, key=lambda i: str(i["id"]))
    random.Random(SEED).shuffle(shuffled)
    cut = int(len(shuffled) * (1 - HELDOUT_SHARE))
    return {"tuning": shuffled[:cut], "heldout": shuffled[cut:]}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "tuning"
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    items = split(load_items())[which]
    print(f"{which}: {len(items)} items, {trials} trial(s)")
    results, tokens, latencies = [], 0, []
    with TypeSafeClient() as client:
        for t in range(trials):
            for it in items:
                t0 = time.perf_counter()
                out = judge(client, it["candidate"], it["reference"])
                latencies.append((time.perf_counter() - t0) * 1000)
                tokens += out["input_tokens"]
                results.append({"trial": t, "id": it["id"], "expected": it["expected"], "got": out["route"]})
    Path(f"evaluate-{which}.json").write_text(json.dumps(results, indent=2))

    for t in range(trials):
        rows = [r for r in results if r["trial"] == t]
        decided = [r for r in rows if r["got"] != "review"]
        agree = sum(r["got"] == r["expected"] for r in rows)
        agree_decided = sum(r["got"] == r["expected"] for r in decided)
        print(f"trial {t}: agreement {agree}/{len(rows)}; sent to review {len(rows) - len(decided)}; "
              f"of the rest {agree_decided}/{len(decided)} agree")
    by_class = Counter((r["expected"], r["got"]) for r in results if r["trial"] == 0)
    for (exp, got), n in sorted(by_class.items()):
        print(f"  expected {exp:20} got {got:20} {n}")
    if trials > 1:
        flips = {r["id"] for r in results} - {i for i in {r["id"] for r in results}
                                              if len({r["got"] for r in results if r["id"] == i}) == 1}
        print(f"label changed between trials on {len(flips)} items: {sorted(flips)}")
    latencies.sort()
    print(f"median latency {latencies[len(latencies) // 2]:.0f} ms; input tokens {tokens}; "
          f"spend ${tokens / 1e6 * PRICE_PER_M_INPUT:.5f}")


if __name__ == "__main__":
    main()
