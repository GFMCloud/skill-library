# Hooks registry

Every hook wired in `~/.claude/settings.json`, with its event, its matcher, and whether
it can block the tool call or only warn. The hook scripts live in `~/.claude/hooks/`,
their one editable home; there is no source copy in this repo. This file records the
wiring, not the code.

`scripts/prove-hooks.sh` reads the table below and goes RED when `settings.json` wires
a hook that has no row here (matched on event, matcher and script file name). A row
with no matching wiring is printed as a NOTE and does not fail the run. Adding,
removing or re-wiring a hook means editing this table in the same change, next to the
hook's fixture in `scripts/prove-hooks.d/`.

The check parses the table: keep the first four columns in this order, and write the
fourth as exactly `blocks` or `warns`.

| Event | Matcher | Hook | Blocks or warns | Fixture | What it does |
|---|---|---|---|---|---|
| PreToolUse | Artifact | `dash-gate.sh` | blocks | `PreToolUse__Artifact.json` | Denies an Artifact publish whose file contains an em dash, en dash or horizontal bar. Fails open on unreadable input. |
| PreToolUse | Bash | `deny-destructive.py` | blocks | `PreToolUse__Bash__0.json` | Denies listed destructive, catastrophic and credential-reading commands, and `rm -rf` outside the scratchpad. Fails closed on unparseable hook input; an unmatched command is allowed. |
| PreToolUse | Bash | `evidence-guard.py` | warns | `PreToolUse__Bash__1.json` | Adds context when a command shape hides evidence (a pipe masking an exit code, and similar). Never denies. Fails open. |
| PreToolUse | Read | `route-large-read.py` | blocks | `PreToolUse__Read.json` | While the llama-offload marker exists, denies a Read over 200 KB with no offset or limit. Silent otherwise. Fails open. |
| PreToolUse | Read | `deny-destructive.py` | blocks | `PreToolUse__Read__1.json` | Denies a Read of a credential path (`.env` and variants, `.pem`, SSH private keys, `.aws/credentials`, `.netrc`, `.npmrc`, `.pypirc`). Second hook on the Read matcher; the fixture index depends on that order. |

Two hooks answer PreToolUse:Bash and two answer PreToolUse:Read. How Claude Code
arbitrates two answers to one event is not recorded here: the arbitration warning from
plan H2 item 3 was left out of this change.

Source of the registry idea: ECC evaluation, plan-gate output H2
(`docs/reviews/2026-09-17-ecc.md`). No ECC code was adopted.
