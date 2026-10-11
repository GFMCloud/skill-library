#!/usr/bin/env bash
# test-update-installed-plugins.sh: proves update-installed-plugins.sh refuses a plugin
# whose hook surface changed and still updates the rest. Everything lives under one temp
# dir (the only thing deleted): a fake plugins root (install cache + marketplace clone)
# and a stub `claude` that logs each call and prints `plugin list` in the real format.
# Nothing here touches ~/.claude, the network, or the real `claude`.
# Usage: bash scripts/test-update-installed-plugins.sh [path to an updater script]
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
UPDATER="${1:-$HERE/update-installed-plugins.sh}"
T="$(mktemp -d "${TMPDIR:-/tmp}/uip-test.XXXXXX")" || exit 2
trap 'rm -rf "$T"' EXIT
CACHE="$T/plugins/cache/skill-library"
CLONE="$T/plugins/marketplaces/skill-library/plugins"
mkdir -p "$T/bin" "$CACHE" "$CLONE"
export STUB_LOG="$T/claude.log" STUB_LIST="$T/list.txt"

cat > "$T/bin/claude" <<'STUB'
#!/bin/bash
echo "$*" >> "$STUB_LOG"
[[ "$1 $2" == "plugin list" ]] && cat "$STUB_LIST"
exit 0
STUB
chmod +x "$T/bin/claude"

# mk <dir> <name> <version> <skill text>: a plugin with a manifest and one skill, no hooks.
mk() {
  mkdir -p "$1/.claude-plugin" "$1/skills/s"
  printf '{"name":"%s","version":"%s"}\n' "$2" "$3" > "$1/.claude-plugin/plugin.json"
  echo "$4" > "$1/skills/s/SKILL.md"
}
# hooks <dir> <guard text>: hooks/hooks.json (command runs hooks/guard.sh) and hooks/guard.sh.
hooks() {
  mkdir -p "$1/hooks"
  cat > "$1/hooks/hooks.json" <<'JSON'
{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"bash \"${CLAUDE_PLUGIN_ROOT}/hooks/guard.sh\""}]}]}}
JSON
  echo "$2" > "$1/hooks/guard.sh"
}
# inline <dir> <version> <script text>: hooks declared inline in plugin.json, calling scripts/run.sh.
inline() {
  mkdir -p "$1/scripts"
  cat > "$1/.claude-plugin/plugin.json" <<JSON
{"name":"x","version":"$2","hooks":{"Stop":[{"hooks":[{"type":"command","command":"bash \${CLAUDE_PLUGIN_ROOT}/scripts/run.sh"}]}]}}
JSON
  echo "$3" > "$1/scripts/run.sh"
}
# pair <name> <old skill> <new skill>: installed copy 1.0.0 in the cache, incoming 1.1.0 in the clone.
pair() {
  mk "$CACHE/$1/1.0.0" "$1" 1.0.0 "$2"
  mk "$CLONE/$1" "$1" 1.1.0 "$3"
}

pair hookchanged skill skill
hooks "$CACHE/hookchanged/1.0.0" "echo guard v1"; hooks "$CLONE/hookchanged" "echo guard v2"
pair hookadded skill skill
hooks "$CLONE/hookadded" "echo guard v1"
pair hooksremoved skill skill
hooks "$CACHE/hooksremoved/1.0.0" "echo guard v1"
pair inlinechanged skill skill
inline "$CACHE/inlinechanged/1.0.0" 1.0.0 "echo run v1"; inline "$CLONE/inlinechanged" 1.1.0 "echo run v2"
pair modechanged skill skill
hooks "$CACHE/modechanged/1.0.0" "echo guard v1"; hooks "$CLONE/modechanged" "echo guard v1"; chmod +x "$CLONE/modechanged/hooks/guard.sh"
pair nohooks "skill text old" "skill text new"
pair samehooks "skill text old" "skill text new"
hooks "$CACHE/samehooks/1.0.0" "echo guard v1"; hooks "$CLONE/samehooks" "echo guard v1"
pair nocache skill skill
rm -rf "$CACHE/nocache"
pair nomarket skill skill
rm -rf "$CLONE/nomarket"

list() { # real `claude plugin list` shape; the updater reads field 2 and the Version line
  echo "Installed plugins:"
  for p in "$@"; do
    printf '\n  ❯ %s@skill-library\n    Version: 1.0.0\n    Scope: user\n    Status: ✔ enabled\n' "$p"
  done
  printf '\n  ❯ other@claude-plugins-official\n    Version: 9.9.9\n    Scope: user\n    Status: ✔ enabled\n'
}

run() { # run the updater against the fixture; sets OUT and RC
  : > "$STUB_LOG"
  OUT="$(PLUGINS_ROOT="$T/plugins" UPDATER_PATH_PREFIX="$T/bin" UPDATER_SKIP_RECONCILE=1 zsh "$UPDATER" 2>&1)"
  RC=$?
}
updated() { grep -qx "plugin update $1@skill-library" "$STUB_LOG"; }
refused() { grep -q "^REFUSED $1@skill-library: $2" <<< "$OUT"; }
shown() { grep -qx -- "$1" <<< "$OUT"; }
logged() { grep -qx -- "$1" "$STUB_LOG"; }
not() { ! "$@"; }

fails=0
check() { # check <label> <command...>
  local label=$1; shift
  if "$@"; then echo "PASS $label"; else echo "FAIL $label"; fails=$((fails + 1)); fi
}

list hookchanged hookadded hooksremoved inlinechanged modechanged nohooks samehooks nocache nomarket > "$STUB_LIST"
run
echo "--- updater output (all cases)"; echo "$OUT"; echo "--- stub claude calls"; cat "$STUB_LOG"; echo "---"
check "stub claude was reached" logged "plugin marketplace update skill-library"
check "hookchanged: REFUSED line" refused hookchanged "hooks changed between 1.0.0 and 1.1.0"
check "hookchanged: diff shown" shown "+echo guard v2"
check "hookchanged: not updated" not updated hookchanged
check "hookadded: REFUSED line" refused hookadded "hooks changed between 1.0.0 and 1.1.0"
check "hookadded: not updated" not updated hookadded
check "hooksremoved: REFUSED line" refused hooksremoved "hooks changed between 1.0.0 and 1.1.0"
check "hooksremoved: not updated" not updated hooksremoved
check "inlinechanged (script outside hooks/): REFUSED line" refused inlinechanged "hooks changed"
check "inlinechanged: not updated" not updated inlinechanged
check "modechanged (exec bit only): REFUSED line" refused modechanged "hooks changed"
check "modechanged: not updated" not updated modechanged
check "nocache: REFUSED, fail closed" refused nocache "installed copy not found"
check "nocache: not updated" not updated nocache
check "nomarket: REFUSED, fail closed" refused nomarket "marketplace copy not found"
check "nomarket: not updated" not updated nomarket
check "nohooks: updated" updated nohooks
check "samehooks: updated" updated samehooks
check "non-skill-library plugin never updated" not logged "plugin update other@claude-plugins-official"
check "exit non-zero when any plugin refused" test "$RC" -ne 0

list nohooks samehooks > "$STUB_LIST"
run
check "clean set: nohooks updated" updated nohooks
check "clean set: samehooks updated" updated samehooks
check "clean set: no REFUSED line" not grep -q "^REFUSED" <<< "$OUT"
check "clean set: exit 0" test "$RC" -eq 0

echo
if [[ $fails -eq 0 ]]; then echo "ALL PASS"; else echo "$fails FAILED"; exit 1; fi
