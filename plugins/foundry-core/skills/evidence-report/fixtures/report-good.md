FIXTURE: a synthetic evidence report that must PASS scripts/check-report.py. Not real data.

CLAIM:   the skill lands in the plugin cache with real content
CHECK:   wc -c ~/.claude/plugins/cache/x/skills/y/SKILL.md
OUTPUT:  1636 /Users/x/.claude/plugins/cache/x/skills/y/SKILL.md
VERDICT: VERIFIED, rules out an empty cache directory reported as success

CLAIM:   the validator exits 0 on the tree at 4f80ce9
CHECK:   bash scripts/validate-skills.sh
OUTPUT:  63 skills checked: 0 failures, 41 warnings
VERDICT: VERIFIED, rules out a structural failure in any skill

CLAIM:   the deploy answers at its real endpoint
CHECK:   curl -sS https://example.invalid/health
OUTPUT:
VERDICT: UNVERIFIED, no network from this container

NOT VERIFIED
- install over the GitHub source: the container has no gh auth
