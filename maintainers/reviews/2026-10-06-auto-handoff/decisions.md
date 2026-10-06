# Decisions: auto-handoff

contract: v1
source: https://github.com/obie/auto-handoff
type: code-repo
pin: 19405aa47bcb31ef775a427a7118f9519ea21734 (2026-10-04 08:53 -0600, "Add auto-handoff plugin for Claude Code"; shallow clone; MIT; 46 stars, created 2026-10-04, 10 files)
reviewed: 2026-10-06
verdict: HARVEST
recheck: -
evidence: maintainers/reviews/2026-10-06-auto-handoff/cleanroom-review.md, maintainers/reviews/2026-10-06-auto-handoff/comparison.md

## Verdict reasoning

A 145-line Claude Code plugin (function hooks, the Mods surface that shipped in 2.1.287)
that arms a timer when a main-loop turn ends and, after 50 idle minutes, runs a handoff
command while the one-hour prompt cache is still warm; seven behavioral tests on a mocked
clock, no dependencies, one commit, one author. The clean room verified every README claim
against the code except one: the one-handoff-per-absence latch rests on an untested
assumption about the origin the plugin's own `$.command.run` reports. Not ADOPT: its bundled
skill is named `handoff`, the same bare name as the installed skill with a different body
(the worst routing case), it writes conversation contents into `docs/handoffs/` with no
redaction step and no typed claims, and the hooks API it uses is early access. HARVEST: the
idle-before-the-cache-expires trigger is a real gap (nothing installed acts on idle; the only
incumbent guidance is the manual "/compact before stepping away" habit), and three fragments
close gaps in `handoff` and `cache-economics.md`. Two independent implementations of the
same idea appeared the same week (alexknowshtml/claude-auto-handoff, a context-threshold
trigger; a Pi extension that cancels its jump when the notes read fails), so the trigger is
not one person's notion. What would change the verdict: a second maintainer and a test for
the origin assumption, or the trigger landing here as our own mod pointed at our own skill.

## Ancestry

none. No shared files, names or prose; convergent narrative sections (goal, status, dead
ends, verification, next steps) arrived at independently. The candidate is v0.1.0 (2026-10-04);
the incumbent handoff is 0.6.4 (2026-10-06).

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Idle-triggered handoff before the cache window closes: a mod that arms on `turn.complete` for the main loop only, skips a late fire (the machine slept, the cache is cold), resets only on a person origin, and runs one handoff command per absence | COMPLEMENT | Take the hook as a pattern, not the plugin: write our own mod (or vendor `hooks/register.ts`, `hooks.json`, `types/index.d.ts` and the seven tests after reading all 146 lines) whose `command` is an unattended variant of the installed `handoff` skill (row 2), after `claude plugin validate` confirms the API on the installed CLI and after adding the missing test that the plugin's own `$.command.run` does not reset the latch | `hooks/register.ts:14-27, 48-64, 96-105, 126-136`; `tests/auto-handoff.test.ts` | a new plugin under `plugins/long-projects/` (a mod beside the handoff skill) | M | a function-hooks plugin on an early-access API to keep in step with CLI releases; every idle session pays one cached read per absence; backed out by disabling the plugin | proposed (Tier 3: a new plugin and an install; joins the hooks-hardening question of which hook layer this machine adopts) | Graham |
| 2 | Unattended-runs mode for the installed handoff skill: ask no questions, stay inside a short pre-approved tool list, write the file from what is already known, with the cost reason stated ("every extra tool call rereads the whole conversation") | INGESTIBLE FRAGMENTS | A new `## Unattended runs` section in handoff SKILL.md with the candidate's two sentences corrected at ingest: the output path stays `handoff-<topic>-<date>.md` in the project root so `session-carryover.py` finds it; the Redaction section applies; typed claims are limited to pre-approved read-only checks (`git branch --show-current`, `git rev-parse HEAD`, `shasum`) or written as `not_checkable` with that said; the copy-paste prompt block goes inside the file since nobody reads the message | `skills/handoff/SKILL.md:11-17` | `plugins/long-projects/skills/handoff/SKILL.md` | S | one more section in an already long skill; backed out by deleting it. Would fit the widened Tier 2 (incubator body, S, decisions row); flag off, so Tier 3 | proposed | Graham |
| 3 | Standing instructions travel with the handoff ("Record any standing instructions the person gave about how to work, since the next session will not have heard them") | INGESTIBLE FRAGMENT | Landed this cycle inside the ratified relayready row 1 (INVARIANTS field) as the Behavior Note "Standing instructions travel"; no further edit | `skills/handoff/SKILL.md:36` | `plugins/long-projects/skills/handoff/SKILL.md` | S | none beyond the note already made | ratified (covered by Q-2026-09-21-4 row 1, applied 2026-10-06) | scout |
| 4 | Cold-cache facts the routing reference lacks: the 5-minute cache applies in usage overage (verified against this session's own ScheduleWakeup tool text, which says exactly that), so a fixed 50-minute idle threshold is wrong there and nothing in the CLI tells a plugin which TTL a session has; a machine that slept wakes to a cold cache, so idle-triggered work is skipped rather than paid for at full price; an idle-triggered handoff turn is itself a cached read that re-warms the cache for another hour | INGESTIBLE FRAGMENT | Three sentences under "Habits that keep the cache warm" in `cache-economics.md`, written from the first-party facts, not the README | `README.md:7, 53-54`; `hooks/register.ts:14-17` | `plugins/agent-tooling/skills/model-effort-advisor/references/cache-economics.md` | S | three sentences to keep true; backed out by deleting them. **Fits Tier 2 as written** (S, INGESTIBLE FRAGMENT, a references/ file of an incubator skill, from a decisions row); flag off, so Tier 3 | proposed | Graham |
| 5 | Late-timer sleep detection (`LATE_SHARE = 0.1`), person-vs-automation origin set, latch-before-action, and the shift-the-stored-clock test technique | COMPLEMENT, travel with row 1 | Arrive with the code if row 1 is taken; none is a prose fragment | `hooks/register.ts:14-27, 54-64`; `tests/auto-handoff.test.ts:110-111` | with row 1 | - | with row 1 | out unless row 1 is ratified | - |
| 6 | The bundled `handoff` skill and its template (goal, status, dead ends, verification, next steps) and `plugin.json`'s default command | REDUNDANT, and a bare-name collision | The incumbent's TRIED AND REJECTED with reasons, VERIFICATION STATE and typed claims are stricter; the candidate skill shares the bare name `handoff` with a different body, and its files are invisible to `session-carryover.py` (`^handoff-.+\.md$`, project root or `docs/`) | `skills/handoff/SKILL.md`, `.claude-plugin/plugin.json` | none | - | - | out | - |

## Conflicts for the user to rule on

1. **Write-time verification against "run one command, skip other investigation".** The
   candidate's unattended skill pre-approves four read-only commands and says "Skip any
   other investigation, because every extra tool call rereads the whole conversation"
   (`SKILL.md:17`). The incumbent's Verify: "every `checkable` entry's `check` command was
   actually run at write time". Both cannot hold in an unattended run with the candidate's
   tool list. Proposal (row 2): the unattended section allows a short list of pre-approved
   read-only claim checks, and anything else is `not_checkable` and says so. Alternative:
   no typed claims in unattended handoffs, and a stated "pre-T5" fallback on resume.
2. **The 1-hour window is not universal.** `cache-economics.md` says "Claude Code runs a
   1-hour prompt-cache window"; in usage overage later requests drop to the 5-minute TTL
   (this session's own tool text). Proposal (row 4): say so, and say a plugin cannot detect
   which TTL applies. Alternative: leave the file and rely on the "re-verify" line.

## Corrections at ingest

- Output location and name: `docs/handoffs/<timestamp>-<slug>.md` becomes
  `handoff-<slug>-<YYYY-MM-DD>.md` in the project root, or `session-carryover.py:37,46`
  never sees it.
- The Redaction section applies to the unattended path; the candidate has none and its
  files are not gitignored, so `git add -A` would commit conversation contents.
- The compound `date ...; git status ...` under two `Bash(...)` grants is claimed to run in
  the default permission mode and was not verified; test before relying on it.
- Library style: the candidate description has no "Not for" clause, no cost line and no
  `metadata`; its skill must be renamed or namespaced before anything of it is installed.
- `register.ts` was read in full by the clean room (146 lines: timers, state, one command
  run); nothing in it addresses a reading agent or asks for a credential. Re-read before any
  vendoring; the pin is one commit old.
- The comparison's context file (alexknowshtml README) was fetched 2026-10-06 UTC, which the
  Sonnet reviewer read as "tomorrow" from its Pacific clock; a date, not a defect.

## Flags

- `skills/handoff/SKILL.md:11`: "Ask no questions and wait for no confirmation." and `:4`
  `allowed-tools: Write(docs/handoffs/**), Edit(docs/handoffs/**), Bash(date *), Bash(git status *), Bash(mkdir -p docs/handoffs*)`.
  Instructions to the model that runs the bundled skill, by design; narrow and read-only
  apart from the two write paths. Not acted on.
- `README.md:49` tells users who swap in their own `command` to grant their own
  `allowed-tools`: widens what runs with nobody present. Noted.
- Nothing addresses the reviewing agent, asks to be added to agent instructions, or asks for
  credentials.

## Rulings log

- 2026-10-06, scout cycle 7 (unattended): rows 1, 2, 4 proposed, queued as Q-2026-10-06-9 in
  claude-scout-weekly `STATE.md`; row 3 ratified by overlap with Q-2026-09-21-4 row 1 and
  landed in handoff 0.6.4; rows 5 and 6 out. Row 4 is the fourth row in seven cycles that
  fits Tier 2 as written (flag off, H12 open).
