#!/bin/bash
# toolkit-review: deliberate-failure proofs for every script, no model called.
# Usage: prove-scripts.sh [proof-dir]      default: a fresh directory under $TMPDIR
# Builds a throwaway run directory, a stub claude and a fake ~/.claude tree, then checks
# that every gate passes what it must pass and fails what it must fail. Exit 1 on any FAIL.
# Run this before the first wave of any run; a check that has never failed is untested.
S="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SK="$(dirname "$S")"
F="$SK/templates/fixtures"
P="${1:-${TMPDIR:-/tmp}/tr-proof-$$}"
rm -rf "$P"; mkdir -p "$P"
export TR_RUN="$P/run"
fails=0
t() { # t <expected: zero|nonzero|N> <label> <cmd...>
  exp="$1"; label="$2"; shift 2
  out="$("$@" 2>&1)"; rc=$?
  case "$exp" in
    zero)    [ "$rc" -eq 0 ] && v=PASS || v=FAIL ;;
    nonzero) [ "$rc" -ne 0 ] && v=PASS || v=FAIL ;;
    *)       [ "$rc" -eq "$exp" ] && v=PASS || v=FAIL ;;
  esac
  [ "$v" = FAIL ] && fails=$((fails + 1))
  printf '%s  expected %-7s got exit %-3s  %s\n' "$v" "$exp" "$rc" "$label"
  printf '%s\n' "$out" | sed -n '1,3p' | sed 's/^/      | /'
}
# 1. A run directory, from the real init script.
t zero "init-run creates a run directory" bash "$S/init-run.sh" "$TR_RUN" spot self proof-run
printf 'Graham\nGFMCloud\ninstalled\nincumbent\n' > "$TR_RUN/name-list.txt"
printf 'turn-reduction\nworkbench\n' > "$TR_RUN/context-names.txt"
t nonzero "init-run refuses an existing run" bash "$S/init-run.sh" "$TR_RUN" spot self
# 2. Extraction checks.
mkdir -p "$P/src-cites"; echo "requires the turn-reduction plugin" > "$P/src-cites/SKILL.md"
t zero    "check-extract passes the clean fixture"                     bash "$S/check-extract.sh" "$F/extract-clean.md"
t nonzero "check-extract fails the fixture with owner names"           bash "$S/check-extract.sh" "$F/extract-with-names.md"
t nonzero "check-extract fails a context name the source does not cite" bash "$S/check-extract.sh" "$F/extract-cites-source.md"
t zero    "check-extract allows a context name the source cites"       bash "$S/check-extract.sh" "$F/extract-cites-source.md" "$P/src-cites"
# A rejected report under extracts/ is archived and gets a rejection note, with the side
# found through the map, not given by the caller.
mkdir -p "$TR_RUN/extracts/proofslot" "$TR_RUN/slots/proofslot/installed" "$TR_RUN/private"
printf '{"proofslot": {"X": "installed", "Y": "cand"}}\n' > "$TR_RUN/private/map.json"
cp "$F/extract-with-names.md" "$TR_RUN/extracts/proofslot/X.md"
t nonzero "check-extract rejects a report under extracts/ and archives it" bash "$S/check-extract.sh" "$TR_RUN/extracts/proofslot/X.md"
[ -s "$TR_RUN/extracts-raw/proofslot/X.attempt-1.md" ] && [ -s "$TR_RUN/extracts-raw/proofslot/X.rejection.txt" ] && [ ! -e "$TR_RUN/extracts/proofslot/X.md" ] \
  && echo "PASS  archive and rejection note exist, report removed from extracts/" \
  || { echo "FAIL  archive or rejection note missing"; fails=$((fails + 1)); }
rm -f "$TR_RUN/private/map.json"
# 3. Judgment checks, rubric v2.
t zero    "check-judgment passes the good comparison fixture"          bash "$S/check-judgment.sh" "$F/judgment-good.md"
t nonzero "check-judgment fails the missing-steelman fixture"          bash "$S/check-judgment.sh" "$F/judgment-missing-steelman.md"
t nonzero "check-judgment fails a mutual SUPERSEDES pair"              bash "$S/check-judgment.sh" "$F/judgment-mutual-supersedes.md"
t nonzero "check-judgment fails a class with a missing id"             bash "$S/check-judgment.sh" "$F/judgment-missing-id.md"
t zero    "check-judgment passes the good self-review fixture"         bash "$S/check-judgment.sh" "$F/self-judgment-good.md" self
t nonzero "check-judgment self mode fails the comparison fixture"      bash "$S/check-judgment.sh" "$F/judgment-good.md" self
# 4. The ~/.claude check on a fake tree.
fake="$P/dot-claude"; mkdir -p "$fake/backups" "$fake/projects/x" "$fake/plugins/cache/x/.in_use" "$fake/skills/synced/y" "$fake/hooks"
touch "$TR_RUN/.marker"; sleep 1
touch "$fake/backups/b.json" "$fake/projects/x/s.jsonl" "$fake/plugins/cache/x/.in_use/123" "$fake/plugins/.last_inuse_sweep" "$fake/skills/synced/y/m.json"
t zero "check-dot-claude passes a bookkeeping-only tree"              bash "$S/check-dot-claude.sh" "$fake"
touch "$fake/hooks/planted.sh"
t 9    "check-dot-claude exits 9 on a planted hook"                   bash "$S/check-dot-claude.sh" "$fake"
rm "$fake/hooks/planted.sh"; touch "$fake/plugins/cache/x/plugin.json"
t 9    "check-dot-claude exits 9 on a plugin file beside an exempt marker" bash "$S/check-dot-claude.sh" "$fake"
t 2    "check-dot-claude exits 2 on a missing root"                   bash "$S/check-dot-claude.sh" "$P/no-such-dir"
# 5. The headless runner with a stub claude.
stub="$P/stub-claude"
cat > "$stub" <<'EOF'
#!/bin/bash
case "${STUB_MODE:-ok}" in
  ok)    printf '{"result":"OK","is_error":false,"usage":{"input_tokens":10,"output_tokens":2}}' ;;
  talks) printf '{"result":"This report discusses rate limit handling.","is_error":false,"usage":{"input_tokens":10,"output_tokens":9}}' ;;
  429)   printf '{"is_error":true,"result":"API Error: 429 rate limit exceeded, resets at 12:00"}'; exit 1 ;;
  empty) printf '{"result":"","is_error":false,"usage":{"input_tokens":1,"output_tokens":0}}' ;;
  hang)  sleep 30 ;;
esac
EOF
chmod +x "$stub"
export TR_CLAUDE="$stub"
echo "prompt" > "$P/prompt.txt"
t zero "headless exits 0 on a stub reply"                          bash "$S/headless.sh" clean "$P" sonnet "$P/prompt.txt" "$P/out-ok.md" proof-ok
t zero "headless does not read a reply that talks about limits as a 429" env STUB_MODE=talks bash "$S/headless.sh" clean "$P" sonnet "$P/prompt.txt" "$P/out-talks.md" proof-talks
t 4    "headless exits 4 on a real 429"                            env STUB_MODE=429 bash "$S/headless.sh" clean "$P" sonnet "$P/prompt.txt" "$P/out-429.md" proof-429
t 5    "headless exits 5 on an empty reply"                        env STUB_MODE=empty bash "$S/headless.sh" clean "$P" sonnet "$P/prompt.txt" "$P/out-empty.md" proof-empty
t 3    "headless exits 3 on a stall (1 second timeout)"            env STUB_MODE=hang HEADLESS_TIMEOUT_S=1 bash "$S/headless.sh" clean "$P" sonnet "$P/prompt.txt" "$P/out-hang.md" proof-hang
t 2    "headless exits 2 on a missing prompt file"                 bash "$S/headless.sh" clean "$P" sonnet "$P/no-prompt.txt" "$P/out-x.md" proof-missing
t 2    "headless exits 2 on an unknown profile"                    bash "$S/headless.sh" nope "$P" sonnet "$P/prompt.txt" "$P/out-y.md" proof-profile
echo "--- budget file after the stub runs"
cat "$TR_RUN/budget/usage.tsv" | sed 's/^/      | /'
t zero "sum-budget reads the file"                                 bash "$S/sum-budget.sh"
# 6. Runners refuse missing targets; run-wave refuses a non-runner and stops on a 429.
t 2 "run-extractor refuses a slot that does not exist"             bash "$S/run-extractor.sh" no-such-slot installed
t 2 "run-judge refuses a slot with no extracts"                    bash "$S/run-judge.sh" no-such-slot XY
t 2 "run-reader refuses a chunk that does not exist"               bash "$S/run-reader.sh" 999
t 2 "run-fixture-arm refuses when the fixture repo is absent"      bash "$S/run-fixture-arm.sh" bare 1
t 7 "run-hook-bench refuses a candidate side before Gate A"        bash "$S/run-hook-bench.sh" some-source
printf 'rm -rf /\n' > "$P/bad.jobs"
t 2 "run-wave refuses a job that is not a runner"                  bash "$S/run-wave.sh" "$P/bad.jobs" "$P/bad.log"
# A wave whose first job hits a 429 must not launch the second. The judge runner needs a
# slot; give it one whose extracts exist, and let the stub return 429.
mkdir -p "$TR_RUN/extracts/proof" "$TR_RUN/slots/proof"; echo "a proof slot" > "$TR_RUN/slots/proof/purpose.txt"
cp "$F/extract-clean.md" "$TR_RUN/extracts/proof/X.md"; cp "$F/extract-clean.md" "$TR_RUN/extracts/proof/Y.md"
printf 'run-judge.sh proof XY\nrun-judge.sh proof YX\n' > "$P/wave.jobs"
t 4 "run-wave stops on the first 429"                              env STUB_MODE=429 bash "$S/run-wave.sh" "$P/wave.jobs" "$P/wave.log"
echo "      | wave log lines: $(wc -l < "$P/wave.log" | tr -d ' ') (expect 1: the second job never launched)"
[ "$(wc -l < "$P/wave.log" | tr -d ' ')" = "1" ] || { echo "FAIL  second job launched after a 429"; fails=$((fails + 1)); }
rm -f "$TR_RUN/judgments/proof/"*
t zero "run-wave runs two stub judges to completion"               bash "$S/run-wave.sh" "$P/wave.jobs" "$P/wave2.log"
# 7. Generators on a two-item, two-side slot.
mkdir -p "$P/items/a" "$P/items/b"; printf -- '---\nname: a\ndescription: does one thing well\n---\n# a\nbody\n' > "$P/items/a/SKILL.md"; printf 'print(1)\n' > "$P/items/b/hook.py"
printf 'slot\tpurpose\tevidence\nproof2\tproof slot\tstatic\n' > "$TR_RUN/slot-map.tsv"
printf 'id\tside\tsource\tslot\ttype\tpath\n-\tinstalled\tlib\tproof2\tskill\t%s\n-\tcand\tsrc1\tproof2\thook\t%s\n' "$P/items/a" "$P/items/b/hook.py" > "$TR_RUN/items.tsv"
t zero "bin-slots places two items and maps the slot"              python3 "$S/bin-slots.py"
t zero "make-facts writes facts for the slot"                      python3 "$S/make-facts.py"
echo "      | ids: $(cut -f1 "$TR_RUN/items.tsv" | tail -n +2 | tr '\n' ' ')"
ids=($(cut -f1 "$TR_RUN/items.tsv" | tail -n +2))
mkdir -p "$TR_RUN/judgments/proof2"
sed -e "s/item-aaaaaaaa/${ids[0]}/g" -e "s/item-bbbbbbbb/${ids[1]}/g" "$F/judgment-good.md" > "$TR_RUN/judgments/proof2/judge-XY.md"
cp "$TR_RUN/judgments/proof2/judge-XY.md" "$TR_RUN/judgments/proof2/judge-YX.md"
t zero "make-ledger derives a verdict from the rows"               python3 "$S/make-ledger.py"
/usr/bin/grep -E '^\| proof2' "$TR_RUN/LEDGER.md" | sed 's/^/      | /'
t zero "make-patches lists the named candidate item"               python3 "$S/make-patches.py"
echo "--- result"
if [ "$fails" -eq 0 ]; then echo "prove-scripts: all proofs PASS (proof dir $P)"; else echo "prove-scripts: $fails FAIL (proof dir $P)"; exit 1; fi
