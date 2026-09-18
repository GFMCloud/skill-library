FIXTURE: a synthetic evidence report that must FAIL scripts/check-report.py on four counts: a VERIFIED block with an empty OUTPUT, a block with no identifier, a verdict token outside the three, and no NOT VERIFIED section. Not real data.

CLAIM:   the skill lands in the plugin cache with real content
CHECK:   wc -c the cache file
OUTPUT:
VERDICT: VERIFIED, rules out an empty directory

CLAIM:   the manifest looks right
CHECK:   read the manifest
OUTPUT:  looked fine
VERDICT: VERIFIED, rules out nothing in particular

CLAIM:   the deploy is probably fine
CHECK:   thought about it
OUTPUT:  should work
VERDICT: LOOKS GOOD
