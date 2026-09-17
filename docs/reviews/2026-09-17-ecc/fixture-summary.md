# Review fixture summary (FIXTURE-derived)

**Everything here comes from a synthetic repo with planted conditions (`planted.tsv`, 10 rows). Nothing in this file is a finding about real code or about how any candidate behaves on real work.** Model: Sonnet for all nine runs and for the scorer. Tools for all arms: `Read,Glob,Grep,Skill,Agent` (Gate A row A4). Task: "Review this repo for issues."

## Per run

Scored by one restricted, blinded scorer run (`scorer/scores.md`; reports renamed R1 to R9 in random order, map in the harness `private/` directory).

| run | found (scorer) | missed | other real | false positives | evidence | asserted | turns | subagents by type | tokens in+out |
|---|---|---|---|---|---|---|---|---|---|
| bare-1 | 8 of 10 | P3, P5 | 0 | 0 none | 7 | 0 | 18 | {} | 94,454 |
| bare-2 | 10 of 10 | none | 1 | 0 none | 8 | 0 | 17 | {} | 101,563 |
| bare-3 | 9 of 10 | P7 | 0 | 0 none | 7 | 0 | 18 | {} | 72,030 |
| current-1 | 9 of 10 | P3 | 2 | 0 none | 7 | 0 | 19 | {"general-purpose": 4} | 568,394 |
| current-2 | 9 of 10 | P7 | 0 | 0 none | 9 | 0 | 19 | {"general-purpose": 4} | 561,409 |
| current-3 | 9 of 10 | P3 | 1 | 0 none | 10 | 0 | 20 | {"general-purpose": 3, "claude": 1} | 672,001 |
| current-plus-ecc-1 | 9 of 10 | P3 | 0 | 0 none | 8 | 0 | 19 | {"general-purpose": 3, "review-arm:code-reviewer": 1} | 660,013 |
| current-plus-ecc-2 | 10 of 10 | none | 1 | 0 none | 11 | 0 | 17 | {} | 444,815 |
| current-plus-ecc-3 | 9 of 10 | P7 | 1 | 0 none | 8 | 1 | 18 | {} | 451,111 |

## Per condition, by arm (restricted scorer)

| condition | bare | current | current-plus-ecc |
|---|---|---|---|
| P1 | 3 of 3 | 3 of 3 | 3 of 3 |
| P2 | 3 of 3 | 3 of 3 | 3 of 3 |
| P3 | 2 of 3 | 1 of 3 | 2 of 3 |
| P4 | 3 of 3 | 3 of 3 | 3 of 3 |
| P5 | 2 of 3 | 3 of 3 | 3 of 3 |
| P6 | 3 of 3 | 3 of 3 | 3 of 3 |
| P7 | 2 of 3 | 2 of 3 | 2 of 3 |
| P8 | 3 of 3 | 3 of 3 | 3 of 3 |
| P9 | 3 of 3 | 3 of 3 | 3 of 3 |
| P10 | 3 of 3 | 3 of 3 | 3 of 3 |

## Consistency statement

**No difference between arms holds in every run of an arm, so the fixture shows no difference in planted conditions found.** Seven conditions, including the three cross-file ones added under row A4 (P8, P9, P10), were found by every run of every arm. P3, P5 and P7 vary inside arms: P5 was missed by one bare run and by no other run, which is a one-run difference and does not count; P3 and P7 were each missed by at least one run in every arm. False positives: 0 in all nine runs. Findings asserted without a file, line or quote: 1 (in `current-plus-ecc-3`), 0 elsewhere.

What does differ in every run is cost: bare runs used 72,030 to 101,563 tokens; the six default-settings runs used 444,815 to 672,001.

## Was a candidate exercised at all

- **Review skills: not observable, so not tested.** `--output-format json` with `--no-session-persistence` records no tool calls, and the result JSON has no field for Skill use. No report text says a skill was used. The `current` arm's review skills are therefore recorded as never shown to trigger, not as scored.
- **Agents: observable through `subagent_stats`.** All three `current` runs spawned 4 subagents (`general-purpose`, one `claude`), nesting to depth 3, and their reports say the purpose was to look for a way to execute tests, which no run had. Of the `current-plus-ecc` runs, one spawned 4 (three `general-purpose` and one `review-arm:code-reviewer`, the only invocation of an ECC item in the fixture) and two spawned none. No bare run spawned any. So two of three `current-plus-ecc` runs did not exercise any ECC item, and the ECC `security-review` skill and two of its three agents were never shown to run.

## Limits

- Headroom: after the A4 conditions were added the bare arm still scored 8, 10 and 9 of 10, so the fixture could have shown a difference on three conditions at most.
- P3 is weakened by its own label: the config file's FIXTURE comment calls the key a fake test string, and all four reports that missed P3 (`bare-1`, `current-1`, `current-3`, `current-plus-ecc-1`) cite that label as the reason not to flag it.
- The pattern scorer (`notes/score-fixture.py`) over-counts: its P3 pattern matches P9 text (same file name plus the word secret elsewhere) and its P7 pattern matches a report that names both versions while declining to assess them. Its totals (bare 9, 10, 10; current 10, 9, 10; current-plus-ecc 10, 10, 9) are kept in `STATE.md` as run, and the restricted scorer's are the ones used here. The restricted scorer is a single Sonnet run and was not itself double-checked beyond the P3 and P7 spot checks.
- With `Skill` in the tool list even the bare arm sees Claude Code's bundled skills, including `code-review` and `security-review` (`proofs/agent-tool/reply-list-with-agent.md`), so bare is not "no review skill available".
- No run could execute anything; every run says so.
