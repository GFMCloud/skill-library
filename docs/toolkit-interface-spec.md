<!--
Moved into the library 2026-09-11 (toolkit-build branch, Gate B ruling A14) from
/Users/gfm/work/toolkit-build-harness/docs/interface-spec.md, where it was authored
in Phase 1 and ratified at Gate A. This file is the one editable home of every shape
below; the harness copy is renamed .superseded. References below to "this harness",
Phase 4, STATE.md, CONFIG.md, roadmap_path, and research_path are to the
toolkit-build-harness that produced the eight toolkit skills; section 10 (Builder
report v1) is that harness's own shape and is kept for the record.
-->
# Interface spec v1

Status: Ratified 2026-09-11 (Gate A, all ten shapes as proposed). Binding on every builder.

Every shape one toolkit skill produces and another consumes is defined here, once.
Builders reference a shape by name and version ("emits a Goal block v1 as defined in
`docs/toolkit-interface-spec.md`"); they never redefine it in a SKILL.md. A field change after
ratification is a breaking change: bump the shape's version here, note the migration in
the library CHANGELOG, and treat the amendment as its own gated act.

Sources: the toolkit entries in `ROADMAP.md` (`roadmap_path`) and the verified claims in
`research-2026-09-11.md` (`research_path`), cited by row number as R-n.

Conventions shared by every shape:

- Serialized as YAML in a fenced block, or as the equivalent Markdown table where a
  skill's report is prose. The field names are the contract, not the container.
- The first field is always the shape name with its version (`goal_block: v1`).
- Timestamps are ISO 8601 with offset. Paths are absolute or repo-relative and say which.
- Text quoted from a command's output is verbatim, never paraphrased.
- Anything produced from a fixture carries the word FIXTURE in the field or file that
  holds it.

## 1. Goal block v1

Produced by goal-spec. Consumed by bounded-loop, site-review, review-pair, and `/goal`
(R-1, R-2).

```yaml
goal_block: v1
ask: <the ask in the user's words, unedited>
kind: measurable | judgment
end_state: <one measurable end state, or for judgment the rubric's pass line>
check: <a command, or an observable Claude can surface verbatim in the transcript>
expected: <exit code or value that means met>
baseline: <the check's output before any work, verbatim, with the timestamp it was run>
constraints: [<things that must not change, one per item>]
budget: <turn or time clause in /goal wording, e.g. "stop after 3 attempts">
human_gate: <the one action that needs Graham, or "none">
rubric: <repo-relative path; present only when kind is judgment>
goal_condition: <the single-line /goal form derived from end_state, check, expected, budget>
```

Rules: no execution starts until every field except `rubric` is filled; `baseline` is
recorded by running `check` once, never by recall; for `kind: judgment` the rubric file
is criterion-separated and each criterion is scored independently, never one holistic
number (research, secondary findings, T1).

Example:

```yaml
goal_block: v1
ask: "get the homepage lighthouse scores up"
kind: measurable
end_state: all four Lighthouse category scores at or above 90 on https://gfmcloud.com/
check: npx lhci collect --url=https://gfmcloud.com/ && node scripts/lh-scores.js
expected: "perf>=90 a11y>=90 bp>=90 seo>=90"
baseline: "perf=71 a11y=88 bp=92 seo=100  (2026-09-11T14:02:11-05:00)"
constraints: [no content changes to the hero copy, no new third-party scripts]
budget: stop after 5 tries
human_gate: deploying the fix branch to production
goal_condition: "all four Lighthouse scores at or above 90 on gfmcloud.com per scripts/lh-scores.js, stop after 5 tries"
```

## 2. Escalation report v1

Produced by bounded-loop. Consumed by humans, `STATE.md` files, and site-review's
failure path (R-3, R-11).

```yaml
escalation: v1
goal_block: <path to the goal block, or inline goal_condition>
attempts: <n> of <budget>
last_failing_output: |
  <verbatim, the check's full output on the final attempt>
tried:
  - {attempt: 1, diff_hash: <sha of the attempt's diff>, summary: <one line>}
cause_class: ambiguous_check_feedback | unreachable_condition | test_file_modified | no_progress
likely_causes: [<exactly two, one line each>]
question: <the one question for Graham>
```

Rules: `attempts` counts distinct `diff_hash` values only; a repeated hash is not a new
attempt. `cause_class: test_file_modified` is set whenever the verifier or any test file
changed between attempts, regardless of the check's exit code. `cause_class: no_progress`
is set on a `/goal` "impossible" verdict or on two consecutive identical hashes.

Example:

```yaml
escalation: v1
goal_block: runs/goal-2026-09-11.yaml
attempts: 3 of 3
last_failing_output: |
  FAIL tests/test_parse.py::test_empty_header - AssertionError: expected 0 got 1
tried:
  - {attempt: 1, diff_hash: 4f1c2a9, summary: strip header before count}
  - {attempt: 2, diff_hash: 88be013, summary: guard on zero-length input}
  - {attempt: 3, diff_hash: c0ffee1, summary: move guard above the split}
cause_class: ambiguous_check_feedback
likely_causes: [the test expects the header row excluded from the count, the fixture has a trailing newline the parser counts]
question: should an empty header row count as a record?
```

## 3. Verdict object v1

Produced by review-pair's reviewer, and by every Phase 4 reviewer in this harness.
Consumed by the orchestrator, which applies only on `pass` (R-4).

```yaml
verdict: v1
target: <path or change id reviewed>
result: pass | fail
severity: none | low | medium | high
confidence: <0..1>
issues:
  - id: <n>
    where: <file:line or section heading>
    what: <one sentence>
    evidence: <command → its output, or "not-checked: <reason>">
new_information: true | false
```

Rules: `issues` is empty on `pass`. `evidence` names an executed check and what it
returned, written `<command> → <output>`; an issue the reviewer could not run a check
for says `not-checked: <reason>` instead. A quote from the change is not evidence on
its own (tightened 2026-09-18 from "or a quote under 15 words": the validator could
not tell a reviewer who ran a check from one who read a line). `new_information` is `false` on a first review and
answers, on a second review, "does this verdict cite anything the first did not". A
second `fail` with `new_information: false` is a repeat fail and holds the target. The
reviewer runs on a model that differs from the builder's, with no parent history, and
receives the goal and the change only. Rubric line every reviewer receives verbatim:
**explanation length is not a quality signal.**

Example:

```yaml
verdict: v1
target: plugins/foundry-core/skills/goal-spec
result: fail
severity: medium
confidence: 0.8
issues:
  - id: 1
    where: SKILL.md "## Verify"
    what: the section names no command, so the baseline cannot be recorded.
    evidence: /usr/bin/grep -c 'baseline' SKILL.md → 0
new_information: false
```

## 4. Typed claim v1

Produced by the handoff writer (handoff skill, write side). Consumed by handoff resume
mode and `consistency-checker:spec-artifact-diff` (research, secondary findings, T5).

```yaml
claims: v1
written_at: <timestamp>
checkable:
  - type: branch | count | file_hash | deploy_status | test_result | state_file_field
    claim: <one sentence>
    check: <command that re-fetches the live value>
    expected: <the value at write time, from running check, never from memory>
not_checkable:
  - kind: rationale | warning | decision
    text: <one sentence>
```

Rules: every `checkable.expected` is written from the output of `check` at write time.
Resume output, in this order: status in three sentences; a table of checkable claims with
columns claim, command, actual output, match or mismatch; the `not_checkable` list under
the heading "unverified by design"; then either one question (a claim is ambiguous or
mismatched) or "proceeding". Zero typed claims are accepted from the document alone.

Example:

```yaml
claims: v1
written_at: 2026-09-11T16:20:00-05:00
checkable:
  - type: branch
    claim: work is on the toolkit-build branch of the skill library
    check: git -C /Users/gfm/skill-library branch --show-current
    expected: toolkit-build
  - type: count
    claim: the validator sees 49 skills
    check: bash /Users/gfm/skill-library/scripts/validate-skills.sh | tail -1
    expected: "49 skills checked: 7 failures, 42 warnings"
not_checkable:
  - kind: decision
    text: the stable backfill was deferred to Gate A rather than done in Phase 1.
```

## 5. Smoke manifest v1

Consumed by smoke-gate, which generates the smoke script from it (R-3; research,
secondary findings, T3).

```yaml
smoke: v1
target: <url, or the launch command that yields one>
assertions:
  identity:    {expect: <who the tool should think the user is>}
  freshness:   {field: <date or count the page shows>, must_advance_from: <value>}
  connections: [{name: <socket or api or relay>, expect: open}]
  routes:      [{path: <path>, status: 200}]
  console:     {errors: 0}
poison:
  identity:    <a wrong value that must make the script exit 1>
  freshness:   <a stale value that must make the script exit 1>
  connections: <a dead endpoint that must make the script exit 1>
  routes:      <a path that must 404>
  console:     <an injected error>
```

Rules: one recorded exit 1 per assertion category before the live run counts; a category
with no poison entry is not proven and the gate reports it as unproven, never as passed.
The live run attaches the script's full output and one screenshot.

Example:

```yaml
smoke: v1
target: https://staging.sloshball.example/
assertions:
  identity:    {expect: "Graham (commissioner)"}
  freshness:   {field: "Rosters updated", must_advance_from: "2026-09-07"}
  connections: [{name: live-scores-socket, expect: open}]
  routes:      [{path: /standings, status: 200}, {path: /teams/1, status: 200}]
  console:     {errors: 0}
poison:
  identity:    "Guest"
  freshness:   "2026-09-01"
  connections: wss://127.0.0.1:1/dead
  routes:      /standings-old
  console:     "throw new Error('FIXTURE poison')"
```

## 6. Seen-index entry v1

Consumed by change-watch (R-8, R-9; research, secondary findings, T8).

```yaml
seen: v1
source: <alarm name, PR number, metric name, marker path>
last_state: <the value last observed>
last_seen: <timestamp of the last observation, any state>
last_reported: <timestamp of the last report, or never>
```

Rules: the report predicate is a transition, `current_state != last_state`. A re-fire in
the same state updates `last_seen` and produces no report. A flapping sequence A→B→A
produces one report per transition, so two, never one per poll. The classification of
the resulting action as safe or approval-only runs as a separate step before any
diagnostic call.

Example:

```yaml
seen: v1
source: cloudwatch:scl-roster-refresh-errors
last_state: ALARM
last_seen: 2026-09-11T03:10:00-05:00
last_reported: 2026-09-11T03:10:00-05:00
```

## 7. Scheduled-task pointer v1

Produced by schedule-harness (R-6, R-7, R-10).

A thin pointer file at `~/.claude/scheduled-tasks/<name>/SKILL.md`. Frontmatter: `name`
and `description` only. Body, in order: the harness directory (absolute); the phase skill
to read, by absolute path; the mode (`continuous` or a named phase); the absolute-limits
block; nothing else. The dispatch logic has one editable home in the harness.

Absolute-limits block v1, every line present:

```text
- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: <seconds>
- consecutive-retry cap on a failed or rate-limited step: <n>
- anything the run would have asked becomes a queued Tier 3 item
```

Rules: the task's permission mode is set explicitly at registration and its saved
approvals are seeded by one attended "Run now"; headless runs use `--permission-prompts
none`; the prompt carries a time guard because a missed run is caught up once at wake
time; overlap skip is the platform's, observed in the run history, not re-implemented.

Example pointer body:

```text
Harness: /Users/gfm/work/cfb-picks-harness
Phase skill: /Users/gfm/work/cfb-picks-harness/.claude/skills/phase/SKILL.md
Mode: grade
Absolute limits:
- no git push
- no deletion (rename to .superseded)
- no credentials
- no edits under ~/.claude/plugins/
- no edits to the harness's own CONFIG.md, CLAUDE.md, or prompts/
- no edits in a repo with uncommitted changes this run did not make
- hook timeout: 120
- consecutive-retry cap on a failed or rate-limited step: 2
- anything the run would have asked becomes a queued Tier 3 item
```

## 8. Contract sections v1 (T0, binding on every skill)

Four H2 sections in SKILL.md, in this order, after the title and any introduction and
before `## Output contract`: `## Inputs`, `## Verify`, `## Done when`, `## Stop when`.
Enforced by `scripts/validate-skills.sh` as committed in Phase 1 (d0356db): stable skills
fail (F14 missing, F15 out of order, F16 vacuous Stop when); incubator skills warn (W4,
W5, W6). `## Stop when` must contain at least one line that is not "done". Full wording
in the library's `docs/authoring-standard.md`, "Contract sections", which is the one
editable home; this section points at it.

## 9. Eval suite layout v2 (binding on every new skill)

Per-skill, in the plugin's top-level `evals/` directory, one subdirectory per skill. The
CLI refuses an eval dir inside `skills/` ("--eval-dir must not be inside the plugin's
skills/ directory (a loaded component directory)"), which is why v1's
`plugins/<plugin>/skills/<skill>/evals/` was retired on 2026-09-18:

```text
plugins/<plugin>/evals/<skill>/
└── <case-name>/
    ├── prompt.md          # frontmatter: name, runs: 1, max_turns, timeout_seconds, allowed_tools; body: the prompt
    └── graders/
        └── <grader>.md    # frontmatter: type: regex | tool_used | tool_order | file_exists, plus that type's fields
```

Rules: at least two cases per skill; graders limited to `regex`, `tool_used`,
`tool_order`, `file_exists` (no `llm`, no `baseline`); `runs: 1` in the file so an
execution is cheap by default; no `results/` directory is ever committed (`.gitignore`
covers the CLI's default results path, and the run command writes outside the library
anyway). `max_turns` is a runaway guard, not an assertion: set it to about twice the
turns a passing run takes. A case that loads a skill, runs Bash and reports took 5 to 9
turns across 12 trials on 2026-09-18, so 6 cut passing runs off before their report.

The run command, from the repo root, one skill's suite at a time:

```bash
claude plugin eval plugins/<plugin> --eval-dir evals/<skill> --ablation none --no-publish --max-cost-usd 2 --threshold 0.8 --runs 3 --allow-tools Bash --trust-plugin --output-dir <dir outside the library> --report <dir outside the library>/report.html --json <dir outside the library>/result.json
```

Notes: without `--eval-dir` the CLI runs every case under `plugins/<plugin>/evals/`;
`--case <glob>` filters by case name and does not support character classes; a case
whose `allowed_tools` includes `Bash`, `Write` or `Edit` needs the matching
`--allow-tools` grant or the tool is denied; `--runs 3` overrides the file's `runs: 1`.
Two cases at three trials cost about $1.40 to $1.60. Execution status: first executed
2026-09-18 on Claude Code 2.1.274; the command is no longer gated on this account.

Example `prompt.md`:

```markdown
---
name: refuses-without-check
runs: 1
max_turns: 4
timeout_seconds: 120
allowed_tools: [Read, Skill]
---
Improve the homepage. Do not ask me anything, just start.
```

Example `graders/names-a-check.md`:

```markdown
---
type: regex
pattern: "check:"
match: contains
---
```

## 10. Builder report v1 (this harness; consumed by the orchestrator)

Written by every Phase 3 builder to `<harness>/runs/phase-3/<skill>.md`:

```markdown
# <skill> build report

## Files created
<one path per line, repo-relative>

## Deliberate failure (FIXTURE)
<the command run against the fixture and its verbatim failing output>

## Passing run
<the command run against a passing input and its verbatim output>

## Shared-file requests
<one line each: file, change, why; or "none">

## Open questions
<one line each; or "none">

## Self-check against the roadmap entry
| Roadmap line (Validation or Success) | Evidence in the directory |
```

## 11. Persisted-state safety invariants v1

Added 2026-09-17 (ECC evaluation, plan-gate output H1, ledger `memory` item-10 fragments).
An addition, not a field change: no shape above changes version. Binding on anything that
persists state between sessions or reads it back: a handoff file, a state file, a
seen-index, a snapshot, and any hook or skill that injects stored text into a session.

1. **Create-only writes.** A memory or snapshot write creates a new file and fails if
   the target exists. It never truncates, replaces or appends to an earlier record. A
   state file that is edited in place by design (`STATE.md`) is edited by the session
   that owns it, never by a hook.
2. **Secret-shaped strings are rejected before the write.** The text is checked before
   anything is written or injected, and a hit means nothing is written: no partial file,
   no redacted copy. The refusal names the shape, never the string.
3. **Symlinks are never followed on read.** A stored file that is a symlink is skipped
   or refused; it is not read through.
4. **No automatic promotion.** Nothing moves stored text into a standing tier (a memory
   directory, a CLAUDE.md, a settings file, a skill) without Graham's accept. Text read
   back from storage enters a session labelled unverified, and a Typed claim v1 block
   is accepted only through the resume procedure in section 4.

Each invariant has a fixture that fails when it is violated: `scripts/prove-hooks.d/`
`SessionStart__startup_clear.json` and `PreCompact__manual_auto.json` (their
`_invariants` lines map controls to invariants), enforced for the hooks by
`~/.claude/hooks/memory_safety.py`.

## Composition map

| Skill | Wraps (first-party primitive) | Research row | Produces | Consumes |
|---|---|---|---|---|
| T1 goal-spec | `/goal` condition syntax | R-1, R-2 | Goal block v1 | nothing |
| T2 bounded-loop | blocking Stop hook (exit 2, `additionalContext`) | R-3, R-11 | Escalation report v1 | Goal block v1 |
| T3 smoke-gate | Stop hook (optional); Anthropic `webapp-testing` scripts | R-3, R-12 | smoke script, run log, screenshot | Smoke manifest v1; Escalation report v1 on red (via bounded-loop) |
| T4 review-pair | read-only subagent (`permissionMode: plan`, `maxTurns`, different `model`) | R-4 | Verdict object v1 | Goal block v1; the change |
| T5 handoff resume | none new (existing skill) | secondary T5 | Typed claim v1 (write side); resume status | Typed claim v1 (read side) |
| T6 site-review | `/goal` template; Lighthouse CLI; linkinator | R-1, R-2 | scored table, fix list | Goal block v1; Verdict object v1 (re-score) |
| T7 schedule-harness | desktop scheduled task (permission mode, saved approvals, overlap skip, catch-up) | R-6, R-7, R-10 | Scheduled-task pointer v1 | nothing (an existing harness's `/phase`) |
| T8 change-watch | desktop scheduled task poll, Routine API trigger, Channel webhook (preview) | R-7, R-8, R-9 | exception reports | Seen-index entry v1; Smoke manifest v1 (staging check); Scheduled-task pointer v1 |

Dependency by interface only: wave 2 skills read wave 1 SKILL.md files for the shape
names, never for code.
