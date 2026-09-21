# Comparison: `precedent` (candidate, pinned `f5141c3`) against the installed set

## Ancestry

**No shared history found.** I checked the following:

- **Text overlap.** I grepped `candidate/` for `retro`, `evidence-guard`, `skill-library`, `long-projects`, `Graham`, `jit`, `just-in-time` and `CLAUDE.md`. The only hit is the unrelated word "retrospective" at `candidate/README.md:48`. There is also no hit for `onsetter`, the source the incumbent runbook cites.
- **Changelog.** `candidate/CHANGELOG.md` has four releases (0.3.0 to 0.6.0), all dated 2026-09-19. None names any incumbent.
- **File overlap.** Nothing in the candidate resembles an incumbent file. `evidence-guard.py` is a table of code regexes over Bash commands, and `tripwire.py` is a corpus-driven glob matcher. I compared them by reading, so there was no diff to run.

**Direction:** none. This is independent convergence on one mechanism: a `PreToolUse` hook that emits `additionalContext` keyed on the tool call. The shared field name comes from the Claude Code hook API, not from a fork. The incumbent `incumbents/2026-09-03-jit-rules-prototype.md` (Q-12) predates the candidate's whole life by 16 days. So every classification below asks "is it better", not "what did the other side learn since the fork".

## Spot-checks of the clean-room review

I read these myself and they held:
- **`DOCS.md:95-102` documents a rule the code does not implement.** The manual says "Everything below `## Evidence` stays on disk too, including any section written after it." `CHANGELOG.md` says "Cutting from the heading to the end of the file was the first rule and it was wrong." `split_evidence()` (`tripwire.py:141-188`) re-appends the tail, and `test_a_section_after_evidence_is_still_injected` (`tests/test_tripwire.py:1212`) asserts it.
- **The `#`-inside-evidence bug is real.** `tripwire.py:177-182` does `stripped = lines[j].lstrip()` and treats any leading `#` as a heading. The evidence convention is indented quotes, so `    # comment` reads as depth 1 and ends the section early. The tests at 1222-1236 cover only `###` headings, never this case. I confirmed this by reading the code, not by running it.
- **Dead line at `tripwire.py:169-170`.** `level` is computed and then overwritten.
- **Stale sample at `DOCS.md:551` and `559`.** It prints `(from script location)`, but `tripwire.py:892` prints `(from {source})`.
- **OpenCode adapter reads `input.args?.path`** (`plugin/opencode/precedent.ts:121`), as the review says. I cannot confirm OpenCode's real argument key from this repo.
- **Redaction, three-state corpus and stats quotes** match the review at `tripwire.py:477-503`, `283-297` and `1040-1046`. The ledger and honesty-note quotes match at `mine.py:60-70` and `502-526`.
- **The 55% figure looks wrong.** By hand count the example page's Evidence section is roughly 400 of roughly 1700 characters, about 23%. The 55% only fits the abandoned heading-to-EOF rule. This is an estimate, since I had no shell.

**Not verified:** test results, CI status, "28ms", the 7-29% recurrence study, the 24-48% measurement (private corpus), and OpenCode behaviour. The review and I both lacked a shell.

## Classification

Items 1 to 6 are the review's "ideas worth taking". Items 7 to 10 are additions of mine, marked as such.

### 1. Push not pull, and no MCP server: **REDUNDANT**
The principle is already held by `incumbents/global-claude-md-boundaries-section.md`: "a rule in prose can be reasoned around, a tool the agent does not have cannot." It is also built into `incumbents/evidence-guard.py` ("Mechanizes the evidence rules the global working agreements state in prose"). Candidate side, `DOCS.md:905-909`: "An MCP tool only fires when the model decides to call it." Nothing here proposes an MCP lesson store, so the extra argument has no use.

### 2. Redaction by token boundary, not length: **COMPLEMENT**
- **The gap:** no incumbent I read logs command lines. `evidence-guard`'s "secret exposure" rule warns before a command runs. It does not say how to log one safely. The candidate says: "Truncating to a character count is NOT redaction ... `TOKEN=sk-abc gh issue comment` puts the token in the first word."
- **Consumer:** none today. It applies only if a command-logging hook is built, including precedent's own telemetry.
- **Adjacent observation:** the candidate's counterexample shows a gap in `evidence-guard.py`'s secret rule. That rule requires `\bexport\s+` and 16 or more characters, so `TOKEN=sk-abc gh ...` passes silently.

### 3. Retired is not broken ("a decision is not a typo"): **COMPLEMENT**
- **The gap:** `incumbents/retro/SKILL.md` §6 admits: "Its limit is the next bullet: it promotes idempotently but never demotes." It also says "No tracking of 'this rule hasn't been referenced in N sessions.'" The retro template's Status field allows only `proposed | acted-on | rejected`.
- **What the candidate adds:** a `**Retired:** <reason>` state that keeps the evidence, drops the triggers and prints the reason. The candidate's rationale: "conflating them is how a typo hides as a decision."
- **Consumer:** the unbuilt `/retro-review`. Nothing consumes it today.
- **Caveat:** `--stats` counts fires per page (`pattern_freq`). Fired is not the same as followed.

### 4. Suppression list keyed on stable ids, printed every run: **COMPLEMENT**
- **The gap:** retro's "Not promoted" section records rejections, but nothing consults it as a suppressor. Retro is scoped to one session, so it does not have the miner's "same group proposed every run" problem.
- **Consumer:** plausibly `skill-discovery`, which ranks candidates from up to 50 sessions and would re-propose rejected ones. I read only its inventory line, so this is unverified. It is outside the assigned incumbents.

### 5. Count unknown history apart rather than as zero: **REDUNDANT**
This holds at the principle level, against the inventory description of `evidence-report` (not read in full): "states what was checked, what the check returned, and what was not checked". The candidate's version: "counted apart instead of being folded in at 0". The mechanism, log-schema evolution, has no log here to apply to.

### 6. Honesty note the miner always prints: **DISCARD**
It is miner-specific, and the miner has no consumer. `evidence-guard.py`'s docstring already states its "Known weaknesses", and its output ends with "WARN only; the command ran."

### 7. (mine) Core mechanism: path and command triggered injection from a corpus: **SUPERIOR SUBSTITUTE, for step 2 of the jit runbook only**
The two sides, quoted:
- **Incumbent, `2026-09-03-jit-rules-prototype.md` step 2:** "PreToolUse hook on Write and Edit: read `tool_input.file_path`, match the globs, emit `additionalContext` with the matching rule text."
- **Candidate, `README.md:60-63`:** "A `PreToolUse` hook matches the file path or the command of an about-to-run `Edit`, `Write` or `Bash` call against each page's declared triggers, and puts every matching page into the model's context as `additionalContext`."

The incumbent is a plan for a hook that does not exist yet. The candidate is a built hook with a bounded matcher, an always-exit-0 contract, telemetry and a large test suite. It extends the mechanism to Bash commands, which the runbook does not need.

**Edits required before it could replace step 2:**
- **Scope.** Runbook Boundaries say "`.claude/settings.json` and `.claude/hooks/` in this project only." The candidate installs as a user-level plugin, with a global corpus at `~/.precedent`. The install must be project-local instead: vendor the one file into `.claude/hooks/` and set `PRECEDENT_PATTERNS` to a project directory.
- **Format.** Step 1 specifies `.claude/rules/*.md` "with a `paths:` glob each". The candidate parses `**Trigger paths:**` bold lines and reports anything else as "skipped as broken" (`README.md:176-178`). Either convert the rule files or change `parse_page`.
- **Bugs.** Fix the `#` split bug and the dead line, both listed under corrections below.

**Unknown:** I have no `2026-09-03-jit-rules-prototype.result.md`. If Q-12 has already resolved to "drop", this item is moot.

### 8. (mine) Head/evidence split and `injected_chars`: **INGESTIBLE FRAGMENTS**
The item as a whole is weak: the docs contradict the code and the split has a bug. Two fragments are worth taking.

- **Fragment A.**
  - *Quote (`tripwire.py:144-146`):* "Only the `## Evidence` section is removed: from that heading down to the next heading of the same or a higher level, or the end of the page."
  - *Target:* `2026-09-03-jit-rules-prototype.md`, step 1.
  - *Adds:* a rule file may carry an `## Evidence` section that stays on disk while the hook injects the rest. This fits the incumbent economy rule "Write a project fact down only once it has cost a correction twice", because the two corrections can be quoted without being paid for on every match.
  - *Condition:* fix the `#` bug first.
- **Fragment B.**
  - *Quote (`CHANGELOG.md`, 0.6.0):* "**`injected_chars`** on every telemetry line: what the invocation really put in front of the model".
  - *Target:* runbook step 3, "the context tokens at the first write".
  - *Adds:* a logged number for the hook arm instead of a hand comparison.
  - *Limit:* it counts characters, not tokens. It cannot replace the CLAUDE.md-arm baseline.

### 9. (mine) Not-wired-up detection (`--check`, `--session-start`, blind-run counting): **REDUNDANT**
- **Incumbent, jit runbook step 4:** "a Write to `runs/x.md` shows the injected text in the transcript; a Write to `README.md` shows none."
- **Candidate, `--check`:** reports the resolved corpus and `NOT WIRED UP` when nothing loaded.

These are equal for a one-shot proof. The candidate's ongoing `--stats` warning is better, but only if item 7 is adopted.

### 10. (mine) Fail-open contract: **REDUNDANT**
- **Incumbent, `evidence-guard.py`:** "Fails open on any error", implemented as `except Exception: return  # fail open`.
- **Candidate, `CONTRIBUTING.md`:** "Never make a path that can exit non-zero or block a tool call."

They are equal.

### Remaining items
- **Admission rule** ("Two independent occurrences", "No evidence, no page"): **REDUNDANT** against the economy section ("only once it has cost a correction twice") and the retro template's mandatory `Evidence` field.
- **OpenCode adapter and `tools/mine.py` as tools:** **DISCARD.** Nothing I read mentions OpenCode or `engram`, and the adapter has no tests.

## Routing collisions

- **Skill descriptions:** none. The candidate ships no `SKILL.md`, and the inventory has no `precedent` or `tripwire` name. There are no identical names with different bodies.
- **Hook layer, the real collision.**
  - Both `evidence-guard.py` (Bash) and the candidate (`Edit|Write|Bash`, 5s timeout per call) would fire `PreToolUse` on the same Bash call and each inject `additionalContext`.
  - The `--init` starter page tells the model "Check the exit status survives the whole pipeline. A pipe, a `tail`..." That duplicates `evidence-guard`'s "pipe masks exit code" rule, delivered at a different moment.
  - A user-authored page with `**Trigger command:** make *`, as in the README example, would fire alongside `evidence-guard`'s `make(?:\s+\S+)?` tool list.
  - Globs cannot express `evidence-guard`'s conditional rules, such as `lambda c: "pipefail" not in c`. So `evidence-guard` should keep the Bash lane.
- **Retro routing:** the retro routing table has no destination for path-scoped recurring lessons. "Log a retro" goes to retro. Retro output would never reach precedent unless a new row is added.

## Philosophy conflicts

1. **A second store of lessons.**
   - Retro: "Do not create a `learnings/` directory or any other second store ... A parallel store of the same kind of content rots because nothing ever reads it consistently."
   - Candidate: a corpus at `~/.precedent/patterns`. Its answer to "rots" is that a hook reads it deterministically.
   - Real contradiction as written. It needs a ruling before ingest, and the retro text would need an explicit exemption.
2. **Where cross-project lessons live.**
   - Retro: a cross-project lesson "belongs in `~/.claude/CLAUDE.md` instead".
   - Candidate (`README.md:51-55`): "they are per-repository, while the recurrence is cross-repository."
   - Its global corpus is a second home for the same lessons, and it avoids the economy rule's "every line loads into every session" cost.
3. **Escalation on recurrence.**
   - Retro: on the third occurrence, "stop and state that the mechanism already holding two rules for it is failing".
   - Candidate: pages only accumulate, and a page can be manually retired. It has no rule for a page that fires and the failure recurs anyway.
   - Tension, not a contradiction.

**Not conflicts:** the candidate and `evidence-guard` are both advisory and fail open, so they sit at the same tier. The boundaries section wants enforcement "at the tool layer where possible", and precedent never claims to enforce.

## Corrections needed at ingest

- **Docs and code disagree.** Fix `DOCS.md:95-102`, the 55% figure (`README.md:68-70`, `DOCS.md:86-88`, and "routinely more") and the stale label at `DOCS.md:551`, `559`.
- **Code.** Fix the `#`-in-evidence split, for example by anchoring the end-of-section scan to `^#{1,6}\s` on unindented lines, and add a test. Remove the dead line at `tripwire.py:169`.
- **Unverified numbers.** "28ms", "7-29%" and "24-48%" have no artifact. Do not carry them into library text.
- **Rules a stateless model cannot honor.** "Two independent occurrences" cannot be counted without a store across sessions. Tie it to retro's recurrence check over `.claude/retros/`, or to the ledger.
- **Missing discipline.** `evidence-guard.py` requires replay against four weeks of history and "a rule above 5 fires per 100 commands was narrowed or dropped". The candidate has no fire-rate gate, so any Bash trigger page needs replay through `replay-hooks.py` first.
- **Trust boundary.** Whatever is writable at `~/.precedent/patterns` becomes model-facing instruction text. Keep the corpus in a reviewed repo.
- **Telemetry.** The log is append-only with full edited paths and no rotation. Add a cap or an opt-out.
- **Install path.** Do not `/plugin install`. It edits harness settings, which the boundaries section treats as a declared boundary (paste-only files, and a chat override must be recorded first). Vendor the file project-locally and prove it with `prove-hooks.sh`.
- **Style.** The candidate's prose is dense with em dashes (README, DOCS headings, the `hooks.json` description). If any of it is ingested, strip them. I am inferring this from the `humanizer` inventory line ("dashes everywhere").

## Net assessment: three things

1. **Use `tripwire.py` as the hook for Q-12 step 2.** Take it as a vendored file, not the plugin, and only after the fixes above. Edit `2026-09-03-jit-rules-prototype.md` step 2 and put the file in the project's `.claude/hooks/`. First check whether the Q-12 result file already says "drop".
2. **Fragments A and B (evidence split and `injected_chars`).** Add them to the jit runbook's steps 1 and 3. Fix the `#` bug first, and remember the number counts characters, not tokens.
3. **Retirement-with-reason as the vocabulary for retro's unsolved demotion.** Add it to `incumbents/retro/SKILL.md` §6 as a design requirement for the future `/retro-review`, and possibly `retired` to the template's Status enum. Add a caveat that fires-per-page does not prove the page was followed. It is text only, no code. Ruling 1 above must be settled first.

Leave everything else (matcher, MCP argument, OpenCode, miner) alone.

## Flags

Nothing in the files I read addresses a reviewing agent. The clean-room review reports the same. The candidate does carry model-directed text as its product:
- The starter page: "Make it fail on purpose, once, and watch it go red."
- The OpenCode header: "Read it before your next action."

I did nothing with either.

I read `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, the example page and `hooks.json` in full. I read excerpts of `DOCS.md`, `tripwire.py`, `mine.py`, `precedent.ts` and `test_tripwire.py`. I read all seven incumbent files in full.
