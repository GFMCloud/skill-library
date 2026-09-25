#!/usr/bin/env bash
# prove-brand-gate.sh: deliberate-failure proof for scripts/brand-gate.py. FIXTURE data
# only: copies the gate into a temp dir with a denylist holding the hash of one fixture
# word, then asserts which lines it fails and which it lets through. The real denylist
# is never read, so no denied word appears in this file or its output.
# Usage: bash maintainers/scripts/prove-brand-gate.sh   (from any directory)
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
mkdir -p "$T/scripts" "$T/maintainers/brand-gate"
cp "$HERE/../../scripts/brand-gate.py" "$T/scripts/"
printf '%s\n' "$(printf '%s' fixturecorp | sha256sum | cut -d' ' -f1)" \
  "$(printf '%s' fixture-voice | sha256sum | cut -d' ' -f1)" \
  > "$T/maintainers/brand-gate/denylist.sha256"
printf 'reviewword\n' > "$T/maintainers/brand-gate/review-flags.txt"
fail=0
check() { # check <expect-exit> <label> <text>
  local rc
  printf '%s\n' "$3" | python3 "$T/scripts/brand-gate.py" --text >/dev/null 2>&1; rc=$?
  if [ "$rc" -eq "$1" ]; then echo "PASS  exit $rc  $2"
  else echo "FAIL  expected exit $1, got $rc  $2"; fail=1; fi
}
check 1 "denied word, other case"            "Built for FixtureCorp"
check 1 "denied word inside a CSS token"     "--fixturecorp-accent: red;"
check 1 "denied word split across two words" "a Fixture Corp deck"
check 1 "denied hyphenated term"             "see fixture-voice first"
check 1 "camelCase identifier"               "const fixturecorpBlue = 1"
check 1 "PascalCase file name"               "FixtureCorpLogo.svg"
check 1 "fullwidth letters (NFKC)"           "$(python3 -c 'print("\uff26ixture\uff23orp deck")')"
check 0 "glued lowercase token only warns"   "fixturecorporation"
warns() { # warns <label> <text>: exit 0 but a WARN line
  if printf '%s\n' "$2" | python3 "$T/scripts/brand-gate.py" --text 2>&1 | grep -q '^WARN'; then
    echo "PASS  warned  $1"; else echo "FAIL  no warning  $1"; fail=1; fi
}
warns "glued lowercase token is flagged"     "fixturecorporation"
check 1 "AWS account id in an ARN"           "arn:aws:iam::$(printf %s%s 123456 789012):role/x"
check 1 "account id in a CDK bucket name"    "cdk-hnb659fds-assets-$(printf %s%s 123456 789012)-us-east-1"
check 1 "console dashed account id"          "account $(printf %s-%s-%s 1234 5678 9012)"
check 0 "UUID last group"                    "550e8400-e29b-41d4-a716-446655440000"
check 0 "touch -t timestamp"                 "touch -t 202609010000 a.txt"
check 0 "review flag only warns"             "one reviewword here"
check 0 "clean text"                         "nothing to see"

# The gate's own list fails closed.
list="$T/maintainers/brand-gate/denylist.sha256"; cp "$list" "$T/list.bak"
printf 'fixturecorp\n' >> "$list"
check 2 "plaintext line in the denylist"     "nothing to see"
printf '# only a comment\n' > "$list"
check 2 "empty denylist"                     "nothing to see"
cp "$T/list.bak" "$list"

# Staged content: comments in the list, Office XML, and strings in a binary.
git -C "$T" init -q && git -C "$T" config user.email p@example.invalid && git -C "$T" config user.name p
staged() { # staged <expect-exit> <label> <path>; the file is already written
  local rc
  git -C "$T" add -f "$3"
  (cd "$T" && python3 scripts/brand-gate.py --staged >/dev/null 2>&1); rc=$?
  git -C "$T" rm -q --cached "$3"
  if [ "$rc" -eq "$1" ]; then echo "PASS  exit $rc  $2"
  else echo "FAIL  expected exit $1, got $rc  $2"; fail=1; fi
}
printf '# old term: FixtureCorp\n' >> "$list"
staged 1 "denied word in a denylist comment" maintainers/brand-gate/denylist.sha256
cp "$T/list.bak" "$list"
python3 - "$T/deck.pptx" <<'PY'
import sys, zipfile
with zipfile.ZipFile(sys.argv[1], "w") as z:
    z.writestr("ppt/slides/slide1.xml", "<p:sld><a:t>Fixture</a:t><a:t>Corp</a:t></p:sld>")
PY
staged 1 "denied word in pptx slide XML" deck.pptx
printf '\x89PNG\r\n\x1a\n\0\0\0tEXtComment\0made by FixtureCorp\0' > "$T/logo.png"
staged 1 "denied word in PNG text chunk" logo.png
printf '\x89PNG\r\n\x1a\n\0\0\0\0' > "$T/plain.png"
staged 0 "clean binary passes (with a warning)" plain.png

if [ "$fail" -eq 0 ]; then echo "prove-brand-gate: all cases PASS"; else echo "prove-brand-gate: FAIL"; exit 1; fi
