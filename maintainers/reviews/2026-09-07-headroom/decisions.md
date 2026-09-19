# Decisions: headroom

contract: v1
source: https://github.com/headroomlabs-ai/headroom
type: code-repo
pin: e67b3c8a29443a60d6b0018fb22f525c5cd7e709
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
evidence: cleanroom-review.md, comparison.md (both in this directory; archived under ~/skill-library/docs/reviews/2026-09-07-headroom/ at Step 6)

## Verdict reasoning

Headroom is a real, active, well-tested product (v0.37.0, weekly releases, CI runs 810 Python test files across four shards), but it solves a bottleneck this machine does not have: per-request provider cache economics at API-key scale. Installing it means a standing local proxy in the credential path, about 1,182 resolved Python packages, an upload beacon that is on by default, and writes to `~/.claude/settings.json` and `~/.claude.json`. Nothing in it is a substitute for an incumbent. One design technique fills a gap `retro` names as unbuilt, and three one-line principles are candidates for the global CLAUDE.md. The verdict would change to ADOPT only if Graham starts running high-volume API-key agent workloads where cache invalidation is a measured cost.

## Ancestry

none. Checked: grep for skill-library, gfmcloud, graham across the clone (zero hits), CHANGELOG cross-references, and SKILL.md files in the candidate (there are none).

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour, one sitting | `M` an afternoon, one PR | `L`
multi-session, or a merge under the 500-line body cap with more than a handful
of edits; L always goes through `phased-harness`.
Adoption cost is mandatory and never "none": what this adds to the maintenance
surface and how it gets backed out.

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Marker-block merge-and-carry-forward for accumulated learnings: current run's sections replace same-named prior sections, prior sections not re-emitted are carried forward, full rebuild only by deleting the block | INGESTIBLE FRAGMENT | Add one design-note bullet to retro section 6 naming this as the reference technique for the unbuilt `/retro-review`, with its known limit: it promotes idempotently but never demotes, so a demotion pass still needs its own mechanism (the section 6 concern) | headroom/learn/writer.py:151-170 (`_merge_recommendations` docstring) | plugins/workbench/skills/retro/SKILL.md, section 6 | S | About six lines in an incubator skill body (150 lines, cap 500); backed out by deleting the bullet | ratified | this session |
| 2 | Legacy-block migration: move accumulated content out of a team-shared file into a personal one with a warning and a gitignore hint | INGESTIBLE FRAGMENT | Do not land. retro never writes to shared files, and the `.superseded` convention already governs content moves | headroom/learn/writer.py:287-336 (`_migrate_legacy_block`) | none | S | n/a | out | |
| 3 | Telemetry two-switch: local collection and upload are separate switches; turning on local stats is not consent to upload, and an upgrade must not start uploading | INGESTIBLE FRAGMENT | One bullet under Credentials and secrets in the global CLAUDE.md | headroom/telemetry/beacon.py:18-20 | /Users/gfm/.claude/CLAUDE.md, Credentials and secrets | S | One more line loaded into every session; zero corrections on record, so it fails the economy rule today; backed out by deleting the line | out: Graham ruled 2026-09-07, hold; listed as candidates in the review record | Graham |
| 4 | Refuse to silently ignore a user-supplied override: when a caller passes a parameter the code path cannot honor, raise rather than drop it | INGESTIBLE FRAGMENT | One bullet under Surgical edits in the global CLAUDE.md, phrased generically | headroom/transforms/smart_crusher.py:36-40 | /Users/gfm/.claude/CLAUDE.md, Surgical edits | S | Same as row 3 | out: Graham ruled 2026-09-07, hold; listed as candidates in the review record | Graham |
| 5 | A default policy is one named constant, so it is one line to audit and one line to reverse | INGESTIBLE FRAGMENT | One bullet under Boundaries are declared and enforced, as a sibling of the tool-layer rule | headroom/telemetry/beacon.py:52-55 | /Users/gfm/.claude/CLAUDE.md, Boundaries are declared and enforced | S | Same as row 3 | out: Graham ruled 2026-09-07, hold; listed as candidates in the review record | Graham |
| 6 | Freeze what the provider already cached; compress only the delta | COMPLEMENT | Nothing on this machine sits between agent and provider, so no consumer. Record as re-review trigger | headroom/cache/prefix_tracker.py:6-14 | none | n/a | n/a | out | |
| 7 | A comparison key is never a source for rebuilt bytes | COMPLEMENT | No consumer; note in the review record only | headroom/cache/prefix_tracker.py:146-149 | none | n/a | n/a | out | |
| 8 | An unreproducible landing-page number is a liability, not evidence | REDUNDANT | proof-of-work and evidence-report already state this more operationally (CLAIM / CHECK / OUTPUT / VERDICT plus a NOT VERIFIED list) | benchmarks/index_proof_table.py:8-10 | none | n/a | n/a | out | |
| 9 | Truncate telemetry labels at the format boundary so a label built for A/B analysis does not ship model tier and size bucket | COMPLEMENT | No telemetry emitter on this machine; note only | headroom/telemetry/session.py:668-674 | none | n/a | n/a | out | |
| 10 | `headroom learn` as a mechanism (single LLM call over a digest, direct write on `--apply`, two-way routing) | INGESTIBLE FRAGMENTS | Not a substitute for retro plus transcript-scanner: it gives up path:line provenance and per-lesson human routing, which retro rejects by design. Fragments covered by rows 1 and 2 | headroom/learn/analyzer.py, writer.py, cli/learn.py | none as a whole | n/a | n/a | out | |
| 11 | Headroom as an installed tool (`headroom wrap claude`, hooks plugin, proxy) | DISCARD | Do not install. Adoption cost 2/5, failure modes 2/5 in the clean-room review; beacon on by default; OAuth token written to disk despite SECURITY.md saying no credential storage; writes `~/.claude/settings.json`, `~/.claude.json`, project `.claude/settings.local.json`; PreToolUse hook shells out on every Bash call. Incumbent approach to cost is llama-offload, model-effort-advisor, handoff | README.md, headroom/cli/wrap.py:1020-1070, 1589-1789 | none | n/a | Standing proxy, ~1,182 packages, Rust toolchain on sdist path; removal is per-tool `headroom unwrap`, untested here | out: Graham ruled 2026-09-07, do not install | Graham |

## Conflicts for the user to rule on

1. Rows 3, 4, 5 versus the global CLAUDE.md economy rule. The file says "Write a project fact down only once it has cost a correction twice." None of the three principles has cost a correction on this machine. Proposal: hold all three out and list them in the review record as candidates, so a future correction can pull the exact wording. Alternative: land any subset now because they are general coding discipline rather than project facts. One line of reasoning: every line loads into every session, and three unforced additions set a precedent the rule exists to stop.
2. Row 11, Headroom as a tool. Headroom's stance: "An anonymous beacon is on by default" (README.md:592, `BEACON_DEFAULT_ON = True` in beacon.py). This machine's stance on outward data flow is propose-only until ruled (claude-scout-weekly ruling Q-2026-09-03-1) and "Secrets live in .env or a keychain, never in ... state files." Proposal: do not install. Alternative: install with `HEADROOM_BEACON=0` and test `headroom unwrap claude` first. Reasoning: the token-cost bottleneck it targets is not one this machine has evidenced.

## Corrections at ingest

- Row 1 note is paraphrased, not quoted, so the em dashes in writer.py docstrings do not carry over.
- Any reference to Headroom's telemetry default must cite README.md or beacon.py, never llms.txt, whose line 67 states the opposite of the code.
- The clean-room reviewer's Bash was blocked for git, so its cadence signal came from CHANGELOG release dates (21 releases 2026-05-26 to 2026-08-27). The comparison agent ran git log and confirmed the shape. No factual correction needed; recording the substitution.

## Flags

- README.md:27-29 addresses AI agents directly: "AI agents / LLMs: read /llms.txt here, or fetch the live index ... full docs blob." Points at a live remote URL and at an in-repo file whose telemetry claim is wrong. Not followed.
- .github/copilot-instructions.md prescribes a reviewing agent's verdicts: "Treat .github/PULL_REQUEST_TEMPLATE.md and CONTRIBUTING.md as required policy, not optional guidance ... prefer blocking feedback over optional suggestions." Conventional location, stricter not laxer. Not acted on.
- llms.txt:67 "Anonymous telemetry is off by default (opt-in)" contradicts beacon.py `BEACON_DEFAULT_ON = True` and README.md:592.
- SECURITY.md:60 "No credential storage: We never store or log API keys" contradicts copilot_auth.py `save_headroom_copilot_oauth_token()`, which writes an OAuth token to disk (mode 0600 per the clean-room review).
- No install, build, or test script from the source was run.

## Rulings log

- 2026-09-07, this session: table drafted; row 1 ratified by default, rows 2, 6 to 10 out by default, rows 3, 4, 5, 11 put to Graham as questions.
- 2026-09-07, Graham: "1 hold, 2 no". Rows 3, 4, 5 out (held as candidates in the review record); row 11 out (do not install). Row 1 ratified. No side effects carried by the overridden proposals: nothing had been written.
