# Comparison: `learning-plugin` (`scoped-learnings`) vs the installed set

Quoted lines that contain an em dash are shown as `[em dash]` in place of the dash, because this output may not contain any.

## Ancestry

**None found.**
- **No merge note or changelog:** `candidate/` has no CHANGELOG. A grep of `incumbents/` for `ahasha`, `scoped-learnings`, `learning-plugin`, `record-learning` and `prune-learnings` returns zero hits.
- **No shared text:** the section structures do not match. `incumbents/retro/SKILL.md` runs gate, transcript, classify, where it lands, schema, and what it does not do. `candidate/skills/record-learning/SKILL.md` runs worth-it, enforcement, destination, entry, paths, verify, diff.
- **Independent convergence:** both sides attack CLAUDE.md bloat and both apply a "write only what earns it" bar. `retro` has an anti-`learnings/` sentence, but it does not cite the candidate.
- **Direction:** there is none, so this is a "is it better" comparison. I cannot date the candidate. The `.git` claims in the clean-room review (shallow, one commit) are unchecked by me, because the copy I was given has no `.git`.
- **The candidate is the fourth JIT-adjacent design seen here.** Unlike the three in `incumbents/precedent-decisions-2026-09-19.md`, it uses no hook to load rules. It relies on the native `paths:` frontmatter mechanism.

## Spot-checks of `cleanroom-review.md`

**Confirmed by reading the files**
- **Inline-brace bug at `check-rules.py:62-64`.** I traced it. `paths: ["src/**/*.{ts,tsx}"]` becomes `"src/**/*.{ts` and `tsx}"` after `split(",")`. `malformed()` then reports "unbalanced brace group" twice, giving two errors and exit 1 on a valid rule.
- **`python3` guard.** The hook guards `jq` and `git` only (`hooks/learning-check.sh:12-13`), so the README line "The hook exits quietly if any is missing" is wrong for `python3`.
- **Static hook string** and the "do not mention this check" clause (`learning-check.sh:57-62`).
- **Marker claimed before prompting** (`:54-55`).
- **`prune-learnings` is manual-only:** `disable-model-invocation: true` at `:4`, and "Don't commit unless the user asks" at `:56`.
- **`SKIP_DIRS` applied after the glob walk** (`check-rules.py:150-153`).
- **Substring error-dedup at `:210`.**
- **File inventory:** nine files, no tests, no CI.
- **License:** MIT text is standard (`Copyright (c) 2026 Alex Hasha`).

**Resolved by the first-party docs, which the review lacked**
- **The central premise** was "unverifiable from this repo". `incumbents/claude-code-docs-memory-rules-section-fetched-2026-09-21.md` confirms it: "Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use."
- **`BRACE_BUDGET = 1000`** was called an "assertion about closed host internals". The docs state the 1,000-pattern budget, the unexpanded fallback and the `[` behaviour.

**New from the docs (candidate diverges)**
- Brace-free patterns "don't count against" the budget. The candidate decrements the budget for every pattern (`check-rules.py:111`, `budget[0] -= len(results)`). The 4 MiB cap is not modelled.

**Not verified by anyone**
- Whether `hookSpecificOutput.additionalContext` under `hookEventName: "Stop"` is valid and actually makes Claude continue.
- Whether `scratchpad_dir` and `agent_id` are real hook input fields. The fetched docs cover rules only.

## Direct answer: does the runbook's step 2 duplicate the native mechanism?

**Yes in purpose and effect, and no in trigger.**

The runbook step 2 says: "PreToolUse hook on Write and Edit: read `tool_input.file_path`, match the globs, emit `additionalContext` with the matching rule text."

The native docs say: "Rules load into context every session or when matching files are opened", and rules without `paths` "are loaded at launch".

Step 1 of the runbook already writes `.claude/rules/*.md` with a `paths:` glob each. That is exactly the native input format. So on any recent build, step 1 alone may already deliver glob-matched, on-demand loading. Step 2 then re-implements the loader.

| Case | Native `paths:` rule | Step 2 hook |
|---|---|---|
| Trigger | Read of a matching file | PreToolUse on Write or Edit of a matching path |
| Edit of an existing file (the step 3 task: append a row to `state/seen.md`) | Loads at the Read that precedes the Edit, before the edit is composed | Injects at the Edit call. Whether the model sees it before or after composing that call is unverified. |
| Write of a brand-new file never read (e.g. `runs/x.md`, step 4's proof) | No Read occurs, so no documented trigger. The docs are silent, so this needs a test. | Fires. This is the one case the hook clearly adds. |
| Read-only session over `reports/**` | Loads | Silent, which is cheaper |
| Bash append (`echo >> state/seen.md`) | Not covered | Not covered, since the matcher is Write and Edit only |

The Bash gap is real on this machine. `incumbents/global-claude-md-boundaries-section.md` records that on 2026-09-18 a paste-only `settings.json` edit was applied "through Bash one turn after the Edit tool was classifier-blocked for it".

**Consequences for the runbook (my inference, not documented behaviour)**
- **Step 3 cannot isolate the hook.** After step 1, both arms have native-format rule files. The "without hook" arm is no longer a no-JIT baseline. It needs three arms: rules in CLAUDE.md, native only, and native plus hook.
- **Double-loading risk.** A rule can arrive once at Read and again at Edit.
- **Step 3 only measures "context tokens at the first write".** A hook that re-injects on every matching Write is not measured.
- **Internal contradictions in the runbook.** Step 1 says "Leave the originals in CLAUDE.md for this test" but step 3 says "CLAUDE.md trimmed". The Boundaries section lists edits only to `.claude/settings.json` and `.claude/hooks/`, but step 1 writes `.claude/rules/`.
- **Precedent row 1 needs re-ruling.** It calls `tripwire.py` a "SUPERIOR SUBSTITUTE for step 2 of the JIT runbook only". Its remaining unique value is new-file Write and Bash triggers, if the native test shows a gap.
- **Suggested fix.** Add a native-only arm first. Keep step 2 only if a fresh-session Write to a new `runs/**` file, with nothing read, shows no rule text.

## Classification of the clean-room's five ideas

### 1. Prefer enforcement over prose: REDUNDANT

Incumbent: `incumbents/retro/SKILL.md` section 3, which is superior.
- **Candidate** (`record-learning/SKILL.md:26-28`): "If a test, lint rule, type, schema, or assertion could catch the mistake, propose that change first".
- **Retro** (routing table): "Deterministic check (something a script could catch every time) | A hook or CI, not prose", plus "Behavioral regression ... | An eval case in the owning skill".
- Retro adds the eval row and the third-occurrence "mechanism is failing" rule.
- Boundaries adds the same principle: "a rule in prose can be reasoned around, a tool the agent does not have cannot."

**One leftover piece** (`prune-learnings/SKILL.md:39-42`): "delete the note in the same diff if the user accepts". Retro never retires notes. See fragment F2.

### 2. A stale rule is negative value: INGESTIBLE FRAGMENT

The candidate's line is `prune-learnings/SKILL.md:31-32`: "A stale rule is worse than no rule: it is confidently wrong."
- **The incumbent's argument is cost only.** The economy rule says "every line loads into every session."
- **Retro names a blocker.** Retro section 6 says demotion needs tracking of "this rule hasn't been referenced in N sessions", and that "No mechanism for it exists yet".
- **`prune-learnings` step 2 needs no usage tracking.** It tests each entry against the current code: gone means delete, changed means rewrite, unsure means list under "couldn't verify".
- **Limit:** this works for code-fact rules. It does not work for process preferences held in memory `feedback`.
- **Target:** `incumbents/retro/SKILL.md` section 6, second bullet. Add the code-test staleness route as an alternative to reference counting, and the "confidently wrong" sentence as the reason.

### 3. Detect staleness mechanically via globs (`check-rules.py`): COMPLEMENT

- **The gap.** Nothing in `inventory.md` lints `.claude/rules/*.md`. `spec-artifact-diff` checks document claims against a tree, not rule globs.
- **Consumer.** None on this machine yet. The only prospective consumer is the three rule files that runbook step 1 would create.
- **Caveats.** A glob such as `runs/**` matches nothing before the first run, giving a false "stale" error. The parser bug and the budget divergence must be fixed first.

### 4. Split the trigger by reversibility: REDUNDANT

- **Candidate:** `disable-model-invocation: true` (`prune-learnings/SKILL.md:4`) for the destructive skill.
- **Retro:** "never touches CLAUDE.md, memory, or a decisions/ ADR directly, it proposes destinations". It never writes to these at all, so it is stricter.
- **Boundaries:** "enforce it at the tool layer where possible".

**A check worth doing:** `adhd` says "Only apply when Graham explicitly invokes /adhd. Do not auto-trigger". I cannot see its frontmatter. If it enforces that in prose only, the flag would move it to the tool layer.

### 5. Claim the marker before acting: INGESTIBLE FRAGMENT

The quote is `learning-check.sh:54-55`: "Claim the marker before prompting. If we can't, stay quiet."
- **Incumbent gap.** Runbook step 2 emits rule text on every matching Write with no once-per-session guard.
- **Target:** runbook step 2, if step 2 survives. Emit each rule once per session, claiming the marker first, and measure total injected characters over the session, not only at the first write.
- **Fail-open** itself is already covered per precedent row 8.

### The four shipped components

- **`record-learning` skill: INGESTIBLE FRAGMENTS.** See F1 and F3 below. As a whole it conflicts with `retro` (see Philosophy conflicts).
- **`prune-learnings` skill: COMPLEMENT.** Nothing installed prunes rules files or root CLAUDE.md by staleness. Rulings-harness is for measured findings only. Fragments F2 and F4 are the useful parts.
- **Stop hook: DISCARD.** Its gate contradicts retro's (see Philosophy conflicts), and its Stop-event output format is unverified.
- **Plugin packaging (`plugin.json`, `marketplace.json`):** DISCARD. It would give the plugin's skills and Stop hook a way in.

## Ingestible fragments

**F1. Entry format: rule, then reason.**
- **Quote:** `record-learning/SKILL.md:47-48`: "One bullet per learning: **the rule, then the reason.** The reason is what stops a future reader from deleting a rule they don't understand."
- **Adds to:** `incumbents/retro/SKILL.md` section 3. Retro routes lessons but gives no format for the entry that lands in CLAUDE.md or a rules file.
- **Precedent row 2** adds an `## Evidence` section. The two combine: one reason line, with the quotes kept on disk.

**F2. Route path-scoped lessons to a rules file, and retire the note when enforcement lands.**
- **Quote:** the destination table row "Specific files or directories | `.claude/rules/<topic>.md` with `paths:` frontmatter", plus `:42-44` "If adding a line would push it over, that's a signal the learning is really path-scoped [em dash] move it."
- **Adds to:** `incumbents/retro/SKILL.md` section 3 routing table. It currently has no `.claude/rules/` row. The docs confirm this is a first-party auto-loading mechanism, which weakens the "second store" objection.
- **The docs suggest a better cross-project row.** Retro's cross-project special case sends everything to `~/.claude/CLAUDE.md`, which loads every session. The docs offer `~/.claude/rules/` for personal rules, and that path is scopable by `paths:`. Retro should propose that for file-type-scoped lessons.
- **Retire on enforcement:** add "delete the note once the check exists" to the future `/retro-review` requirements, next to precedent row 4.
- **Gated on precedent conflict 1.** `retro` owns this surface, so do not edit before that ruling.

**F3. Split criteria for the runbook's step 1.**
- **Quote:** `prune-learnings/SKILL.md:47-48`: "A root-file line that only applies to certain paths → move it into `.claude/rules/<topic>.md` with `paths:`."
- **Adds to:** `incumbents/2026-09-03-jit-rules-prototype.md` step 1. The runbook picks three rules by example only, and step 1 is exactly this operation.
- **Fits precedent conflict 1's proposal** ("a move, not a copy") and contradicts the runbook's "Leave the originals in CLAUDE.md".

**F4. Merge duplicates by topic.**
- **Quote:** `prune-learnings/SKILL.md:36-38`: "Prefer one file per topic with a wider `paths:` list over several files with near-identical patterns."
- **Adds to:** nothing yet. It is a rule for future rule-file upkeep, to attach if the prototype is adopted.

## Routing collisions if both were installed

There are no identical names. Neither `record-learning` nor `prune-learnings` appears in `inventory.md`, so the worst case, the same name with different bodies, is absent.

1. **`record-learning` against `retro`.**
   - **Trigger overlap:** record-learning fires "at the end of any task where something surprising was discovered, a bug had a subtle cause, or the user corrected your output". Retro's automatic triggers are "something broke and got fixed" and "a decision got made". Both claim the end of a task where a bug was fixed.
   - **Who wins:** record-learning has no "Not for" clause and no gate. It is the broader description and would fire on more prompts. Retro wins only on the literal words "retro" and "/retro".
2. **"remember this" or "add this to the rules".** Record-learning wins by name. It writes to `.claude/rules/` or root CLAUDE.md. Retro routes standing preferences ("How I want you to work") to memory `feedback`. A bare "remember that I prefer X" would land in project CLAUDE.md instead. That is a silent misroute.
3. **The Stop hook against `retro`.** Two session-end mechanisms would run, one self-assessed and one evidence-gated. If `bounded-loop`'s Stop hook is active, `learning-check.sh` consumes its once-per-session marker on the first Stop, which may be a failing turn.
4. **`prune-learnings` against `rulings-harness`.** The description "a CLAUDE.md or notes file is accumulating measured findings ... that could go stale" overlaps in intent. `prune-learnings` is manual-only, so it only collides if the user types the slash command.

## Philosophy conflicts (contradictory advice)

- **C1. Propose against write.**
  - **Retro:** "This skill **proposes** destinations. It does not edit memory, CLAUDE.md, or a decisions folder itself".
  - **Candidate:** "Before creating a file, run `ls .claude/rules` ... Create `.claude/rules/` if it doesn't exist", then "## 7. Show the diff". `prune-learnings` says "**delete the entry**". Both write first and show the diff after. `prune-learnings:10` says "let the user decide", but the deletion is already applied.
- **C2. Evidence gate against self-assessment.**
  - **Retro:** "**Determine the gate from evidence, not self-assessment.**" and "You are not a reliable narrator of your own session".
  - **Hook:** "Before stopping: did this session surface a non-obvious gotcha ...? If so, use the record-learning skill". That asks the same narrator.
  - **Gates diverge:** the hook fires on uncommitted changes outside `.claude`, while retro's git leg counts commits. A fully committed session fires retro but not the hook. A dirty tree with no failure fires the hook but not retro.
- **C3. Admission threshold.**
  - **Economy:** "Write a project fact down only once it has cost a correction twice."
  - **Candidate:** "Record it only if it is **non-obvious**: a gotcha someone would hit again, a bug that only appears under specific conditions, or a correction the user has now made more than once." The first two admit a first-occurrence note.
  - **Retro:** a one-off "correctly dies" in the retro file.
- **C4. Second store.**
  - **Retro:** "Do not create a `learnings/` directory or any other second store. ... A parallel store of the same kind of content rots because nothing ever reads it consistently".
  - **README:** "A gotcha about API handlers goes in `.claude/rules/api.md` with `paths: ["src/api/**/*.ts"]`."
  - **Resolution:** the docs make `.claude/rules/` part of the same memory-file mechanism, and native path scoping does read it. The "nothing ever reads it" premise fails for it. So it is not a `learnings/`-style store. Retro's table still needs the row (F2). This supports the "move, not copy" answer to precedent conflict 1.
- **Different emphasis, not contradiction:** "do not mention this check" (hook) against retro's one-line "No retro: gate not met". Retro's line is for a user-invoked run.

## Corrections needed at ingest

1. **Fix `check-rules.py:62-64`.** Use a comma-aware split, or parse the block list only. The docs show only the block-list form. Add a fixture.
2. **Fix the budget model.** Brace-free patterns do not consume budget (`:111`), and the 4 MiB cap is unmodelled. `plugin.json` pins no minimum host version, but the docs tie the `paths` fixes to v2.1.207 and v2.1.217.
3. **README "exits quietly if any is missing"** is false for `python3`. Skills call `python3` unguarded.
4. **A rule a stateless model cannot honor.** "a correction the user has now made more than once" (`record-learning:12-14` and the hook string) cannot be counted across sessions or after compaction. Replace it with retro's recurrence check over earlier `.claude/retros/` files or a scanner result.
5. **Em dashes.** There are 12 across four files. The library convention is to strip them from anything ingested.
6. **Style against the library's conventions.**
   - **Descriptions:** `record-learning` has no "Not for" line and is overbroad. Library descriptions carry trigger phrases, exclusions and cost lines.
   - **Frontmatter:** neither skill has `metadata: maturity`.
   - **Cost note:** `prune-learnings` step 2 ("find the code it describes" for every bullet) is an unbounded read with no cost note.
7. **Root-line cap.** `ROOT_LINE_LIMIT = 60` is arbitrary and applies only to project `CLAUDE.md`, `AGENTS.md` and `.claude/CLAUDE.md`. It ignores `~/.claude/rules/` and symlinked shared rules.
8. **If vendored:** apply the `SKIP_DIRS` and error-dedup fixes from the review (`:150-153`, `:210`).
9. **Do not ingest the Stop hook.** Its output format is unverified, and it contradicts retro (C2).

## Flags (text addressing the reader or model)

Nothing in `candidate/` addresses a reviewing agent or comparison. The product itself is model-directed text.

- **Hook injection** (`hooks/learning-check.sh:60`), which instructs the model to stay silent about its own invocation: "Before stopping: did this session surface a non-obvious gotcha, a bug that only appears under specific conditions, or a correction the user has now made more than once? If so, use the record-learning skill to write it to the right scoped rules file. If not, stop [em dash] do not mention this check."
- **Skill directives**, by design: `record-learning/SKILL.md:87-89`, "Show the user the diff for the files you touched", and both skills' `description:` fields, which are model-invocation triggers.
- **Write access to instruction files.** Installing the plugin lets an agent write the files that configure future agents. The only gate is the prose diff step.

## Net assessment: the three things to take

1. **Native-first re-scoping of the JIT runbook (a change to `incumbents/2026-09-03-jit-rules-prototype.md`, not candidate text).**
   - Add a native-only arm.
   - Make step 2 conditional on a fresh-session new-file Write showing no rule text.
   - Reconcile the step 1 and step 3 contradiction and the boundaries list.
   - Re-rule precedent row 1 accordingly.
   - This is the highest-value result, and it comes from the docs file, not the candidate.
2. **F2 as a fragment into `incumbents/retro/SKILL.md` section 3.** Add a routing row for path-scoped lessons to `.claude/rules/<topic>.md` with `paths:`, and for cross-project file-type lessons to `~/.claude/rules/`. Pair it with F1 (rule, then reason). Wait for the ruling on precedent conflict 1.
3. **The code-test staleness route, in the "unsolved demotion" bullet of `retro` section 6.** From `prune-learnings` step 2 and the "confidently wrong" line, as a design requirement for the future `/retro-review`. Add `check-rules.py` as a project-local, bug-fixed vendored linter only if the prototype adopts rules files.

**Do not install the plugin.** Its Stop hook and its writing skill contradict retro's evidence gate and its proposal-only rule.
