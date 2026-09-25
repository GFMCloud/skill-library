#!/usr/bin/env bash
# prove-f20.sh: deliberate-failure proof for validator check F20 (a skill with
# metadata.source has a row in its plugin's NOTICE.md, and every row names such a
# skill). FIXTURE data only: builds a throwaway library under a temp dir with a copy of
# this repo's scripts/ and three plugins, and asserts the validator passes the
# attributed one and fails the other two with F20.
# Usage: bash maintainers/scripts/prove-f20.sh        (from any directory)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scripts" "$T/docs"
cp "$HERE/../../scripts/validate-skills.sh" "$HERE/../../scripts/skill_meta.py" "$T/scripts/"
skill() { # skill <plugin> <name> [source]
  mkdir -p "$T/plugins/$1/skills/$2"
  printf -- '---\nname: %s\ndescription: FIXTURE skill for the F20 proof, long enough to clear the forty character floor.\nmetadata:\n  maturity: incubator\n%s---\n\n# %s\n' \
    "$2" "${3:+  source: $3
}" "$2" > "$T/plugins/$1/skills/$2/SKILL.md"
}
notice() { # notice <plugin> <row-name>
  printf '# NOTICE\n\n## Derived skills\n\n| skill | source key |\n|---|---|\n| %s | fixture/upstream@0000000 |\n' "$2" > "$T/plugins/$1/NOTICE.md"
}
skill good-plugin derived fixture/upstream@0000000; notice good-plugin derived
skill unlisted-plugin derived fixture/upstream@0000000          # source, no NOTICE row
skill stray-plugin plain; notice stray-plugin ghost             # row, no such sourced skill
fail=0
check() { # check <expect-exit> <expect-F20: yes|no> <plugin>
  local out rc has
  out="$(cd "$T" && bash scripts/validate-skills.sh "plugins/$3" 2>&1)"; rc=$?
  if printf '%s\n' "$out" | grep -q '^FAIL F20 '; then has=yes; else has=no; fi
  if [ "$rc" -eq "$1" ] && [ "$has" = "$2" ]; then echo "PASS  exit $rc, F20 $has  $3"
  else echo "FAIL  expected exit $1 and F20 $2, got exit $rc and F20 $has  $3"; fail=1; fi
  printf '%s\n' "$out" | grep '^FAIL' | sed 's/^/      | /'
}
check 0 no  good-plugin
check 1 yes unlisted-plugin
check 1 yes stray-plugin
if [ "$fail" -eq 0 ]; then echo "prove-f20: all cases PASS"; else echo "prove-f20: FAIL"; exit 1; fi
