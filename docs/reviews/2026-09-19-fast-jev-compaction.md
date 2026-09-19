---
contract: v1
source: https://github.com/tamaratran/fast-jev-compaction
type: code-repo
pin: e3f262a7f4d42bd8dd32ced30d26176f7cb545b0
reviewed: 2026-09-19
verdict: SKIP
recheck:
applied: none
evidence: docs/reviews/2026-09-19-fast-jev-compaction/cleanroom-review.md
---

# fast-jev-compaction

**Verdict:** SKIP. The plugin works by sending the whole conversation (user and
assistant text plus tool inputs up to 1000 characters) to a third-party endpoint,
`api.typesafe.ai`, on every compaction, and that is its design, not a maturity gap.
It also asks for a raw vendor key in `~/.claude/settings.json`, which the credentials
rule forbids.

**Ancestry:** none. Nothing installed replaces compaction. The nearest incumbents are
the `pre-compact-state` PreCompact hook (snapshots STATE.md, no network) and the
`handoff` skill; neither overlaps, and neither shares code or text with this source.

## What landed

Nothing.

## What was declined, and why

- The plugin itself: data egress and credential handling above. Also, at this pin,
  open issue #56 reports that `keepResult` and `keepCall` come back on different
  scales against one shared `keepThreshold`, so `keep` is unreachable for non-pinned
  calls (reported with a repro, not reproduced here: no key, and none was requested).
  Issue #52 reports that late state-fitting stages remove the messages being scored
  on a 1084-message replay.
- The transferable ideas (prune tool traffic instead of summarizing, the
  keep / truncate-with-re-run-note / drop decision, fall back to the built-in when
  reduction is under 25%): no target file. They only matter to someone writing a
  compaction hook, and no such project exists here. Recorded so a later local build
  can start from the clean-room review, section 5.
- Comparison was done inline, not by subagent: one item, no incumbent in the slot.

## Facts checked on 2026-09-19

- Function hooks are real in the installed Claude Code 2.1.276: the binary contains
  `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` (5 hits) and `session.compact` (18 hits).
  Early access, behind an env flag; the repo pins typings from 2.1.274.
- Repo created 2026-09-17, 3496 stars and 181 forks two days later, 45 open issues
  and PRs, one maintainer plus a `devin/` agent branch prefix. No CI. Zero runtime
  dependencies. `package.json` 0.2.0 against `plugin.json` 0.3.0.
- Key issuance was undocumented (issue #54); a commenter points at
  `console.typesafe.ai/keys`. Pricing and quota not stated anywhere in the repo.

## Flags

- No text in the repo addresses a reviewing agent.
- `README.md:142` instructs users to put the key in settings:
  `{ "env": { "CLAUDE_CODE_ENABLE_FUNCTION_HOOKS": "1", "TYPESAFE_API_KEY": "<your key>" } }`.
  `hooks/fast-jev.ts:237-241` reads it back from settings, although the generated
  type file documents a `$.session.authorize()` path where the secret never reaches
  the plugin.
- `demo/JevDemo/build.sh` compiles, ad-hoc signs and opens a macOS app. Not run.
- Nothing from the repo was installed, built or executed.

## Re-review trigger

A transport that keeps the conversation on this machine (a local model behind the
`JevAsker` seam, shipped by the project), or Graham deciding to build a local
compaction hook on the function-hooks surface once it leaves early access.
