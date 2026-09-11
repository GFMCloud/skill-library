#!/usr/bin/env python3
"""score-table.py -- the site-review gate.

Reads a Lighthouse JSON report and a linkinator JSON report, prints the
scored table (with the two mandatory labels), and exits 1 if any category
scores below 90 or any link is broken, 0 otherwise. This is the check the
skill's /goal condition points at (see templates/goal-condition.md).

Field paths this script relies on (cite by path, never redefine elsewhere):
  Lighthouse JSON: categories.<id>.score            float 0..1, id in
                   {performance, accessibility, best-practices, seo}
  linkinator JSON: links[].state, links[].status     state in
                   {"BROKEN", "OK", "SKIPPED"}

Usage (absolute or relative paths, runnable from any directory):
  score-table.py <lighthouse-report.json> <linkinator-report.json>

Exit codes:
  0  all four categories >= 90 and zero broken links
  1  at least one category < 90, at least one broken link, or malformed input
"""
import json
import sys

THRESHOLD = 90

CATEGORIES = [
    ("performance", "Performance"),
    ("accessibility", "Accessibility"),
    ("best-practices", "Best Practices"),
    ("seo", "SEO"),
]

LABELS = [
    "The performance score is a lab proxy and does not certify Core Web "
    "Vitals or INP.",
    "The accessibility score is an automatable-issue floor, not WCAG "
    "compliance.",
]

# Canonical wording lives in templates/goal-condition.md (the roadmap-verbatim
# fix-phase condition); this string must match it exactly.
GOAL_CONDITION = (
    "all four scores at or above 90 and linkinator reports zero broken, "
    "stop after 5 tries"
)


def load_json(path, what):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"FAIL: could not read {what} JSON at {path}: {e}", file=sys.stderr)
        sys.exit(1)


def score_lighthouse(lh):
    categories = lh.get("categories")
    if categories is None:
        print("FAIL: lighthouse report has no top-level 'categories' object", file=sys.stderr)
        sys.exit(1)
    rows = []
    ok = True
    for cat_id, label in CATEGORIES:
        cat = categories.get(cat_id)
        if cat is None or cat.get("score") is None:
            print(f"FAIL: lighthouse report missing categories.{cat_id}.score", file=sys.stderr)
            sys.exit(1)
        score100 = round(cat["score"] * 100)
        status = "PASS" if score100 >= THRESHOLD else "FAIL"
        if status == "FAIL":
            ok = False
        rows.append((label, score100, status))
    return rows, ok


def score_linkinator(li):
    links = li.get("links")
    if links is None:
        print("FAIL: linkinator report has no top-level 'links' array", file=sys.stderr)
        sys.exit(1)
    broken = [l for l in links if l.get("state") == "BROKEN"]
    return broken, len(links)


def main():
    if len(sys.argv) != 3:
        print("usage: score-table.py <lighthouse.json> <linkinator.json>", file=sys.stderr)
        sys.exit(1)

    lh_path, li_path = sys.argv[1], sys.argv[2]
    lh = load_json(lh_path, "Lighthouse")
    li = load_json(li_path, "linkinator")

    rows, categories_ok = score_lighthouse(lh)
    broken, total_links = score_linkinator(li)
    links_ok = len(broken) == 0

    print("| Category | Score | Status |")
    print("|---|---|---|")
    for label, score100, status in rows:
        print(f"| {label} | {score100} | {status} |")
    link_status = "PASS" if links_ok else "FAIL"
    print(f"| Broken links (linkinator, {total_links} checked) | {len(broken)} | {link_status} |")

    print()
    for label in LABELS:
        print(f"Label: {label}")

    if broken:
        print()
        print("Broken links:")
        for l in broken:
            print(f"  - {l.get('url')} (status {l.get('status')})")

    all_ok = categories_ok and links_ok

    print()
    verdict = "MET" if all_ok else "NOT MET"
    print(f"goal_condition: {GOAL_CONDITION} -- {verdict}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
