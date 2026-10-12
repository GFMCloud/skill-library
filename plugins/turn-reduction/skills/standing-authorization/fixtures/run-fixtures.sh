#!/usr/bin/env bash
# FIXTURE runner: the Verify proof for authz.py's permissions and check-plan modes, run
# against the small JSON and plan fixtures beside this script (none is a real project).
# Usage: bash run-fixtures.sh [path/to/authz.py]   (default ../authz.py)
# Asserts:
#   permissions  exits 1 and names exactly the missing rule when a settings file lacks a
#                granted shape, and prints a paste that parses as JSON; exits 0 with
#                "all N granted rules present" when the settings files together hold
#                every rule (one rule differs only in whitespace); reads a missing
#                settings file and a file with no permissions.allow as empty, and says so
#   validate     rejects a 'permissions' that is not an array or sits on a stop entry, and accepts the good file
#   check-plan   exits 1 and prints the verdict when a step is STOP-LISTED or
#                NOT-COVERED; exits 0 when every step is ALREADY-GRANTED; with list items
#                present, other lines are not steps; with none, every non-empty line is
# Exits 0 only when every assertion holds. Pass a pre-1.2.0 authz.py as the argument to
# see it fail: it has neither mode.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTHZ="${1:-$HERE/../authz.py}"
AUTH="$HERE/auth-permissions.json"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fails=0

assert() {  # assert <label> <condition-exit-code>
    if [ "$2" -eq 0 ]; then echo "PASS  $1"; else echo "FAIL  $1"; fails=$((fails + 1)); fi
}
fragment() { sed -n '/^{/,$p' <<<"$1"; }
BRANCH_RULE='Bash(git -C /fixture/repo branch -d *)'

# permissions: one settings file lacks the branch -d shape.
out="$(python3 "$AUTHZ" permissions "$AUTH" --settings "$HERE/settings-partial.json")"; code=$?
[ "$code" -eq 1 ]; assert "permissions: a settings file lacking a granted rule exits 1 (got $code)" $?
grep -qF "\"$BRANCH_RULE\"" <<<"$out"; assert "permissions: the missing branch -d rule is named" $?
grep -qF "1 of 4 granted rule(s) missing, needed by: 'merge a fixture PR" <<<"$out"
assert "permissions: one line says which grant needs it" $?
fragment "$out" | python3 -c '
import json, sys
d = json.load(sys.stdin)
assert d == {"permissions": {"allow": ["Bash(git -C /fixture/repo branch -d *)"]}}, d
' 2>/dev/null
assert "permissions: the paste parses as JSON and holds only the missing rule" $?

# permissions: the two settings files together hold every rule.
out="$(python3 "$AUTHZ" permissions "$AUTH" --settings "$HERE/settings-partial.json" \
    --settings "$HERE/settings-rest.json")"; code=$?
[ "$code" -eq 0 ]; assert "permissions: all rules present across two files exits 0 (got $code)" $?
grep -qF "all 4 granted rules present" <<<"$out"; assert "permissions: prints 'all 4 granted rules present'" $?

# permissions: a missing settings file is an empty allow list.
out="$(python3 "$AUTHZ" permissions "$AUTH" --settings "$TMP/missing.json")"; code=$?
[ "$code" -eq 1 ]; assert "permissions: a missing settings file exits 1 (got $code)" $?
grep -qF "$TMP/missing.json not found, read as an empty allow list" <<<"$out"
assert "permissions: says the missing file was read as empty" $?
grep -qF "4 of 4 granted rule(s) missing" <<<"$out"; assert "permissions: every rule is reported missing" $?
[ ! -e "$TMP/missing.json" ]; assert "permissions: did not create the missing settings file" $?

# permissions: a settings file with no permissions.allow is an empty allow list.
out="$(python3 "$AUTHZ" permissions "$AUTH" --settings "$HERE/settings-no-permissions.json" \
    --settings "$HERE/settings-partial.json")"; code=$?
[ "$code" -eq 1 ]; assert "permissions: no permissions.allow plus a partial file exits 1 (got $code)" $?
grep -qF "settings-no-permissions.json has no permissions.allow, read as an empty allow list" <<<"$out"
assert "permissions: says the file without permissions.allow was read as empty" $?

# validate: a non-array 'permissions' is refused; the good file passes.
out="$(python3 "$AUTHZ" validate "$HERE/auth-bad-permissions.json")"; code=$?
[ "$code" -eq 1 ]; assert "validate: a string 'permissions' exits 1 (got $code)" $?
grep -qF "'permissions' must be a non-empty array" <<<"$out"; assert "validate: names the 'permissions' error" $?
out="$(python3 "$AUTHZ" validate "$HERE/auth-stop-permissions.json")"; code=$?
[ "$code" -eq 1 ]; assert "validate: 'permissions' on a stop entry exits 1 (got $code)" $?
grep -qF "'permissions' belongs on a granted entry" <<<"$out"; assert "validate: names the stop-entry error" $?
python3 "$AUTHZ" validate "$AUTH" >/dev/null; code=$?
[ "$code" -eq 0 ]; assert "validate: the good fixture exits 0 (got $code)" $?
python3 "$AUTHZ" permissions "$HERE/auth-bad-permissions.json" --settings "$HERE/settings-partial.json" \
    >/dev/null; code=$?
[ "$code" -eq 1 ]; assert "permissions: refuses an invalid authorization file, exits 1 (got $code)" $?

# check-plan: every step granted.
out="$(python3 "$AUTHZ" check-plan "$AUTH" --steps "$HERE/plan-granted.md")"; code=$?
[ "$code" -eq 0 ]; assert "check-plan: an all-granted plan exits 0 (got $code)" $?
grep -qF "3 step(s): 3 ALREADY-GRANTED, 0 STOP-LISTED, 0 NOT-COVERED" <<<"$out"
assert "check-plan: the three list items are the steps, the heading and paragraph are not" $?

# check-plan: one step stop-listed.
out="$(python3 "$AUTHZ" check-plan "$AUTH" --steps "$HERE/plan-stop.md")"; code=$?
[ "$code" -eq 1 ]; assert "check-plan: a stop-listed step exits 1 (got $code)" $?
grep -qE "^STOP-LISTED +'force push' +force push the branch" <<<"$out"
assert "check-plan: prints STOP-LISTED, the matched token and the step" $?

# check-plan: one step not covered.
out="$(python3 "$AUTHZ" check-plan "$AUTH" --steps "$HERE/plan-not-covered.md")"; code=$?
[ "$code" -eq 1 ]; assert "check-plan: a not-covered step exits 1 (got $code)" $?
grep -qE "^NOT-COVERED +- +rename the package" <<<"$out"
assert "check-plan: prints NOT-COVERED and the step" $?

# check-plan: no list items, so every non-empty line is a step.
out="$(python3 "$AUTHZ" check-plan "$AUTH" --steps "$HERE/plan-plain.txt")"; code=$?
[ "$code" -eq 0 ]; assert "check-plan: a plain-text all-granted plan exits 0 (got $code)" $?
grep -qF "2 step(s): 2 ALREADY-GRANTED" <<<"$out"; assert "check-plan: each non-empty line is one step" $?

echo
if [ "$fails" -eq 0 ]; then echo "ALL PASS"; exit 0; else echo "$fails FAILED"; exit 1; fi
