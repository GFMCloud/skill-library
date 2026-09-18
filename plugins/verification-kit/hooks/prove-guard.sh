#!/usr/bin/env bash
# prove-guard.sh: deliberate-failure proof for readonly-agent-guard.py, no session needed.
# Usage: bash plugins/verification-kit/hooks/prove-guard.sh        (from any directory)
# Feeds the hook the stdin JSON Claude Code sends a PreToolUse Bash hook, once per case,
# and asserts deny or allow. Exit 1 on the first disagreement.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
H="$HERE/readonly-agent-guard.py"
fail=0
run() { # run <expect: deny|allow> <label> <json>
  local exp="$1" label="$2" json="$3" out rc v
  out="$(printf '%s' "$json" | python3 "$H" 2>/dev/null)"; rc=$?
  if printf '%s' "$out" | /usr/bin/grep -q '"permissionDecision": *"deny"'; then v=deny; else v=allow; fi
  if [ "$v" = "$exp" ] && [ "$rc" -eq 0 ]; then echo "PASS  $exp  $label"; else echo "FAIL  expected $exp got $v (exit $rc)  $label"; printf '%s\n' "$out" | sed 's/^/      | /'; fail=1; fi
}
v() { printf '{"hook_event_name":"PreToolUse","tool_name":"Bash","agent_type":"%s","agent_id":"a1","scratchpad_dir":"/private/tmp/scratch-x","cwd":"/Users/x/proj","tool_input":{"command":%s}}' "$1" "$2"; }
# Positives: inside a read-only agent, writes are denied.
run deny  "heredoc redirect to a project file"      "$(v verification-kit:pre-delivery-verifier '"cat <<EOF > src/app.py\nprint(1)\nEOF"')"
run deny  "append redirect"                          "$(v pre-delivery-verifier '"echo x >> notes.md"')"
run deny  "sed -i"                                   "$(v cross-document-checker '"sed -i \"s/a/b/\" README.md"')"
run deny  "tee"                                      "$(v silent-failure-hunter '"ls | tee out.txt"')"
run deny  "git commit"                               "$(v transcript-scanner '"git commit -am wip"')"
run deny  "mv into the tree"                         "$(v Explore '"mv a.md b.md"')"
run deny  "python inline write"                      "$(v pre-delivery-verifier '"python3 -c \"open(\\\"x.txt\\\",\\\"w\\\").write(\\\"hi\\\")\""')"
# 2026-09-18: a pre-delivery-verifier run got `> /tmp/co.txt` through. /tmp was an allowed
# root; only the scratchpad is now. The fd-prefixed and clobber forms were never matched.
run deny  "redirect to /tmp, outside the scratchpad" "$(v verification-kit:pre-delivery-verifier '"ls -la > /tmp/co.txt"')"
run deny  "redirect to a /private/tmp sibling"       "$(v pre-delivery-verifier '"ls > /private/tmp/other/out.txt"')"
run deny  "dot-dot path out of the scratchpad"       "$(v pre-delivery-verifier '"ls > /private/tmp/scratch-x/../other/out.txt"')"
run deny  "&> redirect to a file"                    "$(v pre-delivery-verifier '"pytest -q &> out.txt"')"
run deny  "numbered fd redirect to a file"           "$(v pre-delivery-verifier '"pytest -q 2> err.log"')"
run deny  ">| clobber redirect"                      "$(v pre-delivery-verifier '"ls >| out.txt"')"
run deny  ">& redirect to a file"                    "$(v pre-delivery-verifier '"ls >& out.txt"')"
run deny  "cp into /tmp"                             "$(v pre-delivery-verifier '"cp README.md /tmp/copy.md"')"
# Negatives: reads, scratchpad writes, other agents, and the main session all pass.
run allow "fd duplication to stderr is not a write"  "$(v pre-delivery-verifier '"echo warn >&2"')"
run allow "stderr to /dev/null"                      "$(v pre-delivery-verifier '"ls missing 2>/dev/null"')"
run allow "&> into the scratchpad"                   "$(v pre-delivery-verifier '"pytest -q &> /private/tmp/scratch-x/out.txt"')"
run allow "read-only command in a verifier"          "$(v pre-delivery-verifier '"git status --short && wc -l README.md"')"
run allow "stderr redirect is not a write"           "$(v pre-delivery-verifier '"bash scripts/validate.sh 2>&1"')"
run allow "redirect to /dev/null"                    "$(v pre-delivery-verifier '"pytest -q > /dev/null 2>&1"')"
run allow "redirect into the scratchpad"             "$(v pre-delivery-verifier '"pytest -q > /private/tmp/scratch-x/out.txt 2>&1"')"
run allow "mkdir inside the scratchpad"              "$(v pre-delivery-verifier '"mkdir -p /private/tmp/scratch-x/work"')"
run allow "a write in a general-purpose agent"       "$(v general-purpose '"echo x > file.txt"')"
run allow "a write in the main session (no agent_type)" '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"echo x > file.txt"}}'
run allow "a Read tool call in a verifier is not Bash" '{"hook_event_name":"PreToolUse","tool_name":"Read","agent_type":"pre-delivery-verifier","tool_input":{"file_path":"/x"}}'
run allow "unparseable input fails open"             'not json'
if [ "$fail" -eq 0 ]; then echo "prove-guard: all cases PASS"; else echo "prove-guard: FAIL"; exit 1; fi
