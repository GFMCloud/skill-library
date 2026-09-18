#!/usr/bin/env bash
# prove-f19.sh: deliberate-failure proof for validator check F19 (no evals/ inside a
# skill directory). FIXTURE data only: builds a throwaway library under a temp dir with
# a copy of this repo's scripts/, one clean skill and one skill holding evals/, and
# asserts the validator passes the first and fails the second with F19.
# Usage: bash scripts/prove-f19.sh        (from any directory)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scripts" "$T/docs"
cp "$HERE/validate-skills.sh" "$HERE/skill_meta.py" "$T/scripts/"
skill() { # skill <plugin> <name>
  mkdir -p "$T/plugins/$1/skills/$2"
  printf -- '---\nname: %s\ndescription: FIXTURE skill for the F19 proof, long enough to clear the forty character floor.\nmetadata:\n  maturity: incubator\n---\n\n# %s\n' "$2" "$2" > "$T/plugins/$1/skills/$2/SKILL.md"
}
skill clean-plugin clean-skill
skill bad-plugin bad-skill
mkdir -p "$T/plugins/bad-plugin/skills/bad-skill/evals/case-1"
echo "FIXTURE prompt" > "$T/plugins/bad-plugin/skills/bad-skill/evals/case-1/prompt.md"
mkdir -p "$T/plugins/clean-plugin/evals/clean-skill/case-1"   # layout v2 location: allowed
echo "FIXTURE prompt" > "$T/plugins/clean-plugin/evals/clean-skill/case-1/prompt.md"
fail=0
check() { # check <expect-exit> <expect-F19: yes|no> <plugin>
  local out rc has
  out="$(bash "$T/scripts/validate-skills.sh" "plugins/$3" 2>&1)"; rc=$?
  if printf '%s\n' "$out" | /usr/bin/grep -q '^FAIL F19 '; then has=yes; else has=no; fi
  if [ "$rc" -eq "$1" ] && [ "$has" = "$2" ]; then echo "PASS  exit $rc, F19 $has  $3"
  else echo "FAIL  expected exit $1 and F19 $2, got exit $rc and F19 $has  $3"; fail=1; fi
  printf '%s\n' "$out" | /usr/bin/grep '^FAIL' | sed 's/^/      | /'
}
check 0 no  clean-plugin
check 1 yes bad-plugin
if [ "$fail" -eq 0 ]; then echo "prove-f19: all cases PASS"; else echo "prove-f19: FAIL"; exit 1; fi
