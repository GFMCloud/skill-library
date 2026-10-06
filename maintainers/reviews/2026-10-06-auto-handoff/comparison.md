# Comparison: obie/auto-handoff (`19405aa`) against the installed handoff stack

## 0. Ancestry

**No shared history.** I checked three things:

- **Named references.** A grep of `incumbents/` for `obie`, `auto-handoff`, `alexknowshtml`, `forked`, `merged from` and `CHANGELOG` found nothing. The one exception is `context-alexknowshtml.md`, which is excluded as context.
- **Files and structure.** No file is byte-identical or near-identical. The candidate `skills/handoff/SKILL.md` is 36 lines and the incumbent is 322. The section structures differ.
- **Convergence.** The incumbent is v0.6.3, reviewed 2026-10-01. The candidate is v0.1.0 and was cloned about 2026-10-04. The two arrived at similar narrative sections independently: goal, status, decisions, dead ends, files, verification, next steps. So the question is what each side has that the other lacks, not what the other side learned since a fork.

The two cover mostly different ground. The candidate is a trigger, an idle timer. The incumbent is a content and verification protocol. The only direct overlap is the narrative template.

**Context-file oddity.** `context-alexknowshtml.md` is headed "fetched 2026-10-06" but today is 2026-10-05. Treat its provenance dates as loose.

## 0.1 Spot-checks of the clean-room review

Checked and confirmed:
- **Code line cites.** In `hooks/register.ts`, `PERSON` is at lines 21-27, the done-latch at 54-56, the late-skip at 60-64, `session.end` at 138-144 and the main-loop gate at 126-136.
- **Skill cites.** `allowed-tools` is at `SKILL.md:4` and "Skip any other investigation" at `SKILL.md:17`.
- **Tests.** There are exactly 7 tests.
- **Manifest and CI.** No `package.json` and no `.github/`. `plugin.json` defaults are 50 minutes and `auto-handoff:handoff`.
- **Untested assumption (risk a).** In `tests/auto-handoff.test.ts`, no test dispatches `command.run` with an origin for the plugin's own run. The `engine` stub (lines 27-31) swallows `command.run` without calling `next`. The "hands off once" test simulates the handoff's own turn only with `turn.start` and `turn.complete`. So the clean-room review is right that the one-handoff-per-absence guarantee rests on an unproven assumption.

Could not check:
- **Git signals.** The candidate directory has no `.git`, so the reflog and shallow-clone claims are unverifiable here.
- **Host behavior.** I have no way to test the function-hooks API, or whether the permission matcher accepts the compound `date …; git status …` under two separate `Bash(...)` grants.

## 1. Classification of the ideas worth taking

| # | Idea | Class |
|---|---|---|
| 1 | Act on idle just before the cache expires | **COMPLEMENT** |
| 2 | Late-timer means the machine slept, so skip | **COMPLEMENT** (travels with 1) |
| 3 | Person origin vs automated origin resets the latch | **COMPLEMENT** (travels with 1) |
| 4 | Set the done-latch before the action runs | **DISCARD** as a standalone idea |
| 5 | Unattended skill design | **INGESTIBLE FRAGMENTS** |
| 6 | Fixed handoff template | **INGESTIBLE FRAGMENTS** (one fragment) |
| 7 | Test timer logic by shifting stored state | **COMPLEMENT** (travels with 1) |

### 1. Idle timer before cache expiry: COMPLEMENT

- **The gap.** No incumbent acts on idle. The only incumbent guidance is a manual habit in `incumbents/cache-economics.md`: "Run `/compact` before stepping away from a long session." `incumbents/handoff/SKILL.md` only fires on a user phrase or "proactively suggest". Nothing runs unattended.
- **Who would consume it.** Nothing on this machine does today. The incumbent hooks are a SessionStart reader and a PreCompact snapshotter.
- **Candidate hook.** `hooks/register.ts:126-136`: "isMainLoop && !(await read($, isDone))" arms `plan.wait`.
- **Cost.** It reuses the 1-hour cache that `cache-economics.md` describes. The README concedes "The handoff is a turn like any other… keeps the cache warm for another hour" (`README.md:54`). That is a deliberate cached read of a long context, so it is not free.

### 2. Late-fire skip: COMPLEMENT (travels with 1)

> "A machine that slept through the wait wakes with the cache already cold, and a handoff then rereads the whole conversation at full price" (`register.ts:14-16`)

`cache-economics.md` has no mention of sleep or cold-cache avoidance. It is only useful inside the hook, so it is not a prose fragment. It also doubles as the correct handling of a quit-and-resume: `session.start` re-arms with `Math.max(0, …)` (`register.ts:96-105`), so a stale `idleSince` fires immediately and gets skipped.

### 3. Person vs automation origin: COMPLEMENT (travels with 1)

> "A background task's notification or a scheduled trigger starts a turn too, and neither says anyone is here." (`register.ts:19-20`)

Nothing installed distinguishes these. The `PERSON` set is a judgment call. It includes `'sdk'` and `'auto-continuation'`, which the clean-room review flags as debatable. The origin names are host API facts I cannot check here.

### 4. Latch before action: DISCARD

This is a standard idempotency idiom with no content to transplant. If idea 1 is taken, it arrives with the code. The real issue is the untested origin assumption above, not the latch.

### 5. Unattended skill design: INGESTIBLE FRAGMENTS

The incumbent has no unattended mode. Its frontmatter has no `allowed-tools`, and its procedure assumes a human: "Present the file to the user for download", "ask: 'Looks like we're mid-session…'".

- **Fragment A.** Replaces nothing and adds a new "Unattended runs" section to `incumbents/handoff/SKILL.md`:
  > "This skill often runs unattended, after the session has sat idle with nobody at the keyboard. Ask no questions and wait for no confirmation. Write the file from what you already know."
  > "The steps below are pre-approved. Any other command or file write may raise a permission prompt that nobody is there to answer, and the handoff would never be written. Stay inside the steps."
- **Fragment B.** Adds the cost reason, with one amendment (see section 4):
  > "Skip any other investigation, because every extra tool call rereads the whole conversation."
- **Fragment C.** Not a fragment to take. The `allowed-tools` line is too narrow for the incumbent's procedure and writes to the wrong path.

### 6. Fixed template: INGESTIBLE FRAGMENTS (one fragment)

Most of the template is **redundant**, and the incumbent is superior:

> Candidate: "**Dead ends**: what was tried and failed, so the next session skips it."
> Incumbent: "TRIED AND REJECTED - [Approach that was attempted or considered and killed] - WHY REJECTED: [brief reason]" and "A rejection with no reason invites a re-litigation."

The same applies to Verification versus VERIFICATION STATE and the typed claims block. The incumbent is stricter: "Confirmed working: [what was actually tested or verified, and how]".

**One real fragment.** Add to `incumbents/handoff/SKILL.md`, Behavior Notes:

> "Record any standing instructions the person gave about how to work, since the next session will not have heard them." (`candidate SKILL.md:36`)

The incumbent has no standing-instructions field. Its only comparable field is type-specific ("Voice / tone notes") and applies only to writing. This also helps the incumbent's own "Preserve rationale" principle.

### 7. Timer test technique: COMPLEMENT (travels with 1)

> "The mocked clock fires a timer the moment it is due, so the sleep is told the other way round: the idle clock is recorded three hours back." (`tests/auto-handoff.test.ts:110-111`)

Useful only if the hook is adopted. Take the whole test file with it. The incumbent's `fixtures/run-fixtures.sh` covers the claim checker, not timers.

## 2. Routing collisions

If both are installed, the **same bare name `handoff` has two different bodies**: `long-projects:handoff` and `auto-handoff:handoff`. That is the worst case, because nothing looks wrong.

- **Description overlap.** The candidate's description is "Write a handoff document so a fresh session can pick up this work. Use when a session is about to end or go cold, before switching tasks, or when the user asks for a handoff." For prompts like "handoff", "fresh session" and "wrap this up" it matches the incumbent's triggers.
- **Which wins for typical prompts.** The incumbent carries an explicit tiebreaker in its description ("when both are installed, always use this one"). The candidate does not. So for a typed "handoff" the incumbent is likely to win. This is a model-routing judgment I cannot test here. A bare `/handoff` could resolve ambiguously. Plugin skills are namespaced, but I am not certain how bare names resolve.
- **The unattended path always hits the candidate.** The hook runs `auto-handoff:handoff` by name. So the same machine would produce two handoff styles in two places:
  - **Interactive.** `handoff-<topic>-<date>.md` with typed claims, per the incumbent.
  - **Idle-triggered.** `docs/handoffs/<timestamp>-<slug>.md` with no claims.
- **Downstream effect.** `incumbents/session-carryover.py:37` only matches `^handoff-.+\.md$` and `:46` only scans the project root and `docs/`, not `docs/handoffs/`. Candidate files are therefore invisible to the SessionStart hook. If one is passed to a new session, Resume Mode finds no `## Typed Claims` and falls back to "pre-T5 format… manual spot-checks".

## 3. Philosophy conflicts

These are contradictions, not differences in emphasis.

1. **Verification at write time.**
   - Candidate: "Run this one command, exactly as written… Skip any other investigation" (`SKILL.md:17`).
   - Incumbent: "every `checkable` entry's `check` command was actually run at write time and its output is what appears in `expected` - not recalled, not inferred" (`incumbents/handoff/SKILL.md`, Verify).
   - Both cannot hold. Running checks is more tool calls, which are not pre-approved by the candidate's `allowed-tools`.
2. **Delivery.**
   - Candidate: "Reply with the file's path and one sentence on what it covers." (`SKILL.md:19`)
   - Incumbent: "Every message that delivers or updates the handoff carries this block in full… Never write 'the prompt from earlier still works'."
3. **Redaction.**
   - Incumbent: "Before writing the handoff file, strip secrets, API keys, credentials, tokens, account IDs…".
   - Candidate: no redaction step at all. It tells the model to use "exact paths, command lines, identifiers and error text" (`SKILL.md:36`) and writes into the project tree with no ignore rule.
4. **Asking.**
   - Incumbent: "ask: 'Looks like we're mid-session - do you want to handoff now or keep going?'".
   - Candidate: "Ask no questions".
   - This is resolvable by mode (attended versus unattended), not a real disagreement.
5. **Resume.**
   - Incumbent: a whole mode that re-runs checks and stops on mismatch.
   - Candidate: no resume story. This is a gap, not a contradiction.

## 4. Corrections needed at ingest

1. **Output location and name.** Change `docs/handoffs/<timestamp>-<slug>.md` to `handoff-<slug>-<YYYY-MM-DD>.md` so `session-carryover.py:37,46` can see it.
2. **Add the redaction rule** ("Redaction" section of the incumbent) to the unattended path. Handoff files land in the working tree and are not ignored. The clean-room review flags that `git add -A` would commit them.
3. **Typed claims in unattended mode.** The `allowed-tools` grant stops the model from running checks, so any claim written there would have an unrun `expected`. That is exactly the failure the incumbent forbids. Either:
   - widen `allowed-tools` to a short list of read-only checks (e.g. `git branch --show-current`, `git rev-parse HEAD`), accepting more reread cost; or
   - write `not_checkable` only and say so in the file.
4. **Delivery contradiction.** In unattended mode, put the copy-paste prompt block inside the file itself, since nobody reads the message. Resolve fragment B's "skip other investigation" to "except the pre-approved claim checks".
5. **Compound command risk.** `date +%Y-%m-%d-%H%M; git status --short --branch` is one Bash call joined by `;` under two separate `Bash(...)` grants (README line 34 claims it completes in default mode). I can't verify the matcher accepts that. Test it before relying on "completes in the default permission mode".
6. **Library style.** The candidate skill description has no "Not for…" clause, no cost line and no `metadata` (maturity, version, reviewed). The inventory shows the convention (e.g. `metadata: maturity / version / reviewed`). Rename or namespace the skill to avoid the bare `handoff` collision.
7. **cache-economics.md is incomplete.** It says flatly "Claude Code runs a 1-hour prompt-cache window". The candidate notes the 5-minute cache applies in usage overage, which the current session's own scheduling tooling also describes. A fixed `minutes: 50` is wrong there and the plugin "cannot tell which cache a session has" (`README.md:53`). The cache-economics numbers are dated 2026-09-07, so re-verify before quoting.
8. **Hook API risk.** The README says the API is early access and was tested on Claude Code 2.1.289. Run `claude plugin validate` on this machine before depending on it.
9. **Third-party code.** Review `register.ts` fully before installing. I read all 146 lines. They do only timers, state and a command run, and nothing in the repo addresses a reading agent or asks for credentials.

## 5. Net assessment: the three things to take

1. **The idle hook, as a whole item (COMPLEMENT).**
   - **What:** `hooks/register.ts`, `hooks/hooks.json`, `types/index.d.ts` and `tests/auto-handoff.test.ts`, as a standalone plugin.
   - **Config:** point its `command` option at the unattended handoff variant from item 2, not the candidate skill.
   - **Before enabling:**
     - Run `claude plugin validate .` to confirm the hooks API.
     - Add a test that `$.command.run` from the plugin itself does not reset the latch.
2. **Unattended-runs fragments plus the standing-instructions line (INGESTIBLE FRAGMENTS).**
   - **Target:** `incumbents/handoff/SKILL.md`, as a new `## Unattended runs` section.
   - **Contents:** fragments A and B, plus the line "Record any standing instructions…" in Behavior Notes.
   - **Required edits:** applying the section 4 corrections (path/name, redaction, claims limited to pre-approved read-only checks, prompt block written into the file).
3. **The cold-cache fragment (INGESTIBLE FRAGMENTS).**
   - **Target:** `incumbents/cache-economics.md`, under "Habits that keep the cache warm".
   - **Adds:**
     - the 5-minute cache in overage and why a fixed idle threshold is wrong there;
     - that a machine that slept wakes to a cold cache, so skip idle-triggered work;
     - that an idle-triggered handoff turn costs a cached read and re-warms the cache for an hour.

**Not taken:** the candidate `SKILL.md` as a whole and `plugin.json`'s default command. Taking the skill whole would create the bare-name collision and the redaction and claims regressions above. The alexknowshtml implementation (a context-size trigger that replaces auto-compact) is context only. Its idea of sourcing files and commits "from the transcript in code" is a possible later improvement to the typed claims block, but I have not evaluated it as a candidate.