# Hooks registry

Every hook wired in `~/.claude/settings.json`, with its event, its matcher, and whether
it can block the tool call or only warn. The hook scripts live in `~/.claude/hooks/`,
their one editable home; there is no source copy in this repo. This file records the
wiring, not the code.

`maintainers/scripts/prove-hooks.sh` reads the table below and goes RED when `settings.json` wires
a hook that has no row here (matched on event, matcher and script file name). A row
with no matching wiring is printed as a NOTE and does not fail the run. Adding,
removing or re-wiring a hook means editing this table in the same change, next to the
hook's fixture in `maintainers/scripts/prove-hooks.d/`.

The check parses the table: keep the first four columns in this order, and write the
fourth as exactly `blocks` or `warns`. A matcher that contains a pipe is written with
the pipe escaped (`startup\|clear`).

| Event | Matcher | Hook | Blocks or warns | Fixture | What it does |
|---|---|---|---|---|---|
| PreToolUse | Artifact | `dash-gate.sh` | blocks | `PreToolUse__Artifact.json` | Denies an Artifact publish whose file contains an em dash, en dash or horizontal bar. Fails open on unreadable input. |
| PreToolUse | Bash | `deny-destructive.py` | blocks | `PreToolUse__Bash__0.json` | Denies listed destructive, catastrophic and credential-reading commands, and `rm -rf` outside the scratchpad. Fails closed on unparseable hook input; an unmatched command is allowed. |
| PreToolUse | Bash | `evidence-guard.py` | warns | `PreToolUse__Bash__1.json` | Adds context when a command shape hides evidence (a pipe masking an exit code, and similar). Never denies. Fails open. |
| PreToolUse | Read | `route-large-read.py` | blocks | `PreToolUse__Read.json` | While the llama-offload marker exists, denies a Read over 200 KB with no offset or limit. Silent otherwise. Fails open. |
| PreToolUse | Read | `deny-destructive.py` | blocks | `PreToolUse__Read__1.json` | Denies a Read of a credential path (`.env` and variants, `.pem`, SSH private keys, `.aws/credentials`, `.netrc`, `.npmrc`, `.pypirc`). Second hook on the Read matcher; the fixture index depends on that order. |
| SessionStart | startup\|clear | `session-carryover.py` | warns | `SessionStart__startup_clear.json` | Injects only the typed claims block of the project's newest handoff, with its path and age, when the claims are 7 days old or less; names a stale, claims-less or secret-bearing handoff in one line instead. Writes nothing. Fails open with a stderr line. Imports `memory_safety.py` from the same directory. |
| PreCompact | manual\|auto | `pre-compact-state.py` | warns | `PreCompact__manual_auto.json` | Copies the project's `STATE.md` to `STATE-precompact-<stamp>.md` beside it, create-only; refuses on a name collision, a secret-shaped string or a symlink. Does nothing in a project with no `STATE.md`. Never blocks compaction ("warns" here means only that). Imports `memory_safety.py`. |

One more PreToolUse:Bash hook is not wired in `settings.json` and so is outside the
table the check parses: `readonly-agent-guard.py`, shipped by the `verification-kit`
plugin in its `hooks/hooks.json` (its one editable home is the repo; it installs with the
plugin). It denies write-shaped Bash commands only when the hook input's `agent_type`
names a read-only agent, and decides nothing otherwise. Proof:
`plugins/verification-kit/hooks/prove-guard.sh`. `prove-hooks.sh` does not cover plugin
hooks; that gap is a residue, stated here rather than hidden.

One Stop hook is also plugin-shipped and outside the parsed table: `board_gate.py`,
shipped by the `turn-reduction` plugin in its `hooks/hooks.json` (its one editable home is
the repo; it installs with the plugin). Event `Stop`, no matcher, **blocks** (exit 2, once
per stop; `stop_hook_active` lets the next stop through). It does nothing unless the
project has `.claude/board.json`; with one, it blocks a turn that changed state (commit,
merge, push, deploy, mutating aws, board.json `triggers[]`) with no work-board write after
it, and, while `authorization.json` exists, a turn that ends on a should-I ask in chat with
no inbox card written. Fails open on any error. Proof:
`plugins/turn-reduction/tests/prove-board-gate.sh`, plus the same prover run against
`tests/fixtures/board-gate/stub-never-blocks.py`, which must fail. SCL V2 still wires its
own `scripts/hooks/board-gate.py` in its project settings until its conversion retires it.

The fixtures cover the cases someone thought of. Replay mode covers what sessions really
ran: `python3 plugins/turn-reduction/tests/replay-board-gate.py --n 60` feeds the shell
commands and turn-ending assistant messages of the 60 most recent main-session
transcripts (`~/.claude/projects/*/*.jsonl`) through the hook's matching functions and
prints every (a) and (b) hit with the firing shell segment or the matching sentence, then
the counts. A person judges each hit; a false one becomes a fixture and a fix. It opens
transcripts read-only and prints short excerpts only. It is opt-in and never runs in CI,
because transcripts exist only on this machine; `run-tests.sh` proves the tool itself on a
synthetic, read-only transcript. Run it after any change to the trigger list or the lexer.

Two hooks answer PreToolUse:Bash in `settings.json` (three with the plugin hook) and two answer PreToolUse:Read. How Claude Code
arbitrates two answers to one event is not recorded here: the arbitration warning from
plan H2 item 3 was left out of this change.

Source of the registry idea: ECC evaluation, plan-gate output H2
(`maintainers/reviews/2026-09-17-ecc.md`). No ECC code was adopted.
