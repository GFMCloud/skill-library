# Comparison: "Why your Claude Code routine reported success and did nothing" vs the installed set

Candidate: `candidate/article.md` (an article, claimed pin `8b1cd795…`). I have no shell here, so I could not recompute the hash. I read the file in full, and it matches the clean-room review's description.

## 0. Ancestry

**None.** I found no shared history.
- The article has no frontmatter, no skill structure and no CHANGELOG. It is a blog post from `runbook.scosovan.com`.
- No incumbent names it. A grep of `incumbents/` for `scosovan`, `runbook`, `9:07`, `x-deny` and `idempot` found nothing. The `403` hits were unrelated.
- The only text overlap is conceptual. The incumbents say "Unreachable is reported as unreachable, never as empty", and the article says "A source that could not be read must never render as a source with nothing in it." The two were written independently and arrive at the same rule.

So the question is not "what did the fork learn". It is "what does an outside article add to a mature local set".

**Lane mismatch.** The article is about cloud Routines. `schedule-harness` covers local Desktop scheduled tasks, and its description carves Routines out: "not for cloud-triggered work with no local file access (that is a Routine)". No incumbent skill says how to write a Routine prompt. That is the one real gap the article touches.

## Clean-room review: spot-checks

- **Agent-directed text.** It says there is none. Confirmed by reading the whole file. The only imperative text is the prompt block in Check 5, which is addressed to the reader.
- **Missing coverage.** It says the article does not cover prompt injection, secrets, cost or concurrency. Confirmed by grep: no match for `inject`, `secret`, `spend` or `concurren`.
- **Provenance.** It cites the `manus_admin` slug and four posts all dated 5 Oct 2026. Confirmed at article lines 15 and 132-143.
- **Quotations.** The Check 5 block, the "9:07" line, the "every connector … included by default" line and the "72-hour GitHub expiry" line all match the file (lines 43, 100, 118).
- **Path.** Its Flags section lists `pins/scosovan/article.md`, not `candidate/article.md`. I could not confirm they are the same file, and I could not check the hash.
- **Platform claims.** I did not check these against live docs. This agent has no fetch tool, so every platform claim (Trusted network, `x-deny-reason`, 9:07, connector defaults) stays unverified.

I agree with the review's ratings: evidence 2/5, actionability 5/5, high currency risk.

## 1. Classification of every technique

The clean-room review lists nine techniques. Each gets one class.

### T1. Two-outcome source accounting (`read: <count> … / unavailable: <exact error>`) → INGESTIBLE FRAGMENTS

The incumbent already has the rule, at harness level:
- `incumbents/CLAUDE.md` Working conventions: "Per source, record reachable or unreachable, items returned, items new versus already in the seen-index. Unreachable is reported as unreachable, never as empty."
- `incumbents/phase-0-scan.md` step 6: "A call cut off twice is reported as unreachable for this cycle, never as empty."
- `evidence-report` handles the same case for checks: "`UNVERIFIED` with the reason".

On coverage the incumbent is as good or better: it has a three-way count and a retry-then-escalate rule. Two phrases in the article are sharper:

| Fragment | Incumbent text it improves | What it adds |
|---|---|---|
| `unavailable: <the exact error or refusal text>` | `CLAUDE.md`, "Working conventions", `unreachable` bullet, and `phase-0-scan.md` step 6 "Record per source: reachable or unreachable" | Verbatim error text. The incumbent records only the state, not why. |
| `read: <count> items for <explicit window>` | the same bullets | The window is recorded next to the count. The incumbent has `items returned` but no window. |
| "If a source is unavailable, the section it feeds says `unavailable: <reason>`" | `phase-0-scan.md` "Output" (candidate list and Anomalies) | The unreachable state is carried into the downstream section, so a report cannot silently shrink. |

Landing note: `CLAUDE.md` says "Nothing that changes this harness itself is auto-applied. Findings about CONFIG.md, CLAUDE.md, prompts/ … are Tier 3." So these edits must be queued as Tier 3. Use the library's words, not the article's: "unreachable" and `UNVERIFIED`, not "unavailable" (see §2).

### T2. A verification step that can fail → REDUNDANT

- Article: "Make that step able to *fail* the run, a verification section that always passes is decoration."
- Incumbent, `evidence-report/SKILL.md`: "A verdict that does not say what failure mode it eliminates is decoration." Its `## Stop when` reads: "never substitute reasoning about why it probably works."

The incumbent also has a mechanical checker (`scripts/check-report.py`, with a fixture that passes and one that fails). Spec §3 requires an independent reviewer: "The reviewer runs on a model that differs from the builder's, with no parent history." The article's version is a self-check by the same session, which is weaker.

### T3. Explicit OK/PARTIAL status plus one log line per run → INGESTIBLE FRAGMENTS

Covered in spirit. `schedule-harness/SKILL.md` Done when: "each run's own summary names its actual outcome … rather than reporting a bare green status". The run-log fixture shows a summary like "Graded 11 of 14 … 1 game queued to Tier 3". Run logs live at `runs/YYYY-MM-DD.md`.

What the incumbent lacks is a closed status token that a script can check.

| Fragment | Target | Adds |
|---|---|---|
| "make PARTIAL the result whenever a source was unavailable or a verification check failed" | `schedule-harness/SKILL.md` `## Done when`, and the first line of the run-log format in `FIXTURE-run-log-excerpt.md` | A status of OK or PARTIAL on the first line, with a forcing rule. A grep can then count PARTIAL runs. |

The article's "append one line per run to a log file" adds nothing. The incumbents already write per-phase run logs on disk.

### T4. Idempotency key (head SHA, not PR number) → REDUNDANT

- Article: "Key your state on something stable … so a repeat run writes nothing instead of writing a duplicate."
- Incumbent, `toolkit-interface-spec.md` §6 (Seen-index entry v1): "A re-fire in the same state updates `last_seen` and produces no report. A flapping sequence A→B→A produces one report per transition."

The incumbent handles flapping and defines the transition predicate. The article's SHA example is specific to GitHub-trigger Routines, and nothing here uses those. The article is also incomplete, as the clean-room review notes: each new push still yields a new result.

### T5. Time-awareness (read the clock, compare to the slot, say so first, report the intended window) → INGESTIBLE FRAGMENTS

The incumbent covers it with a primary source. `schedule-harness/SKILL.md` "Overlap skip and the time guard": "state in the instructions what the run should do if it is firing late (skip stale work, only act on what changed since the last successful run, or name a cutoff)". `references/platform-facts.md` quotes the Desktop doc: "A task scheduled for 9am might run at 11pm if your computer was asleep all day."

Two things in the article are more concrete:

| Fragment | Target | Adds |
|---|---|---|
| "If it is hours late, say so in the first line of the output" | `schedule-harness/SKILL.md` "Overlap skip and the time guard" | A required visible disclosure. The incumbent's list of options (skip, act on what changed, cutoff) does not require telling the reader. |
| "report on the window the slot intended, not the last 24 hours from now" | same section | Names the wrong default window explicitly. |

Both need the §3 correction below.

**Incumbent defect found while reading.** `schedule-harness/SKILL.md` says "Do write a time guard into the pointer's prompt". But `toolkit-interface-spec.md` §7 says the body is "the harness directory …; the phase skill …; the mode …; the absolute-limits block; nothing else". `templates/pointer.md` repeats "nothing else". The template and the fixtures contain no time-guard line. The run-log fixture says "Time guard in the prompt held", which implies a guard that the template cannot render. `check-pointer.py` does not forbid extra lines, so a guard would pass the check, but the spec contradicts it. The incumbent should settle where the time guard lives, either in the harness `/phase` skill or in an allowed pointer line. This is a defect in the incumbent, found in passing.

### T6. Off-the-hour scheduling (9:07, not 9:00) → COMPLEMENT (small, unverified)

- **Gap:** no incumbent mentions start jitter.
- **Consumer:** none directly. `change-watch` "registers a scheduled task or Routine", so it is the only plausible consumer.
- **Limit:** the platform-facts file covers only the Desktop-tasks doc. The 9:07 advice is attributed to the Routines doc and I could not verify it.
- **Action:** run `fact-currency-check` before use. `phase-0-scan.md` step 4 offers a watch list (`state/watch.md`) for items that need a recheck. A one-line watch entry is the right form for now.

### T7. Connector pruning / least privilege → COMPLEMENT

- **Gap:** the Absolute-limits block v1 covers git push, deletion, credentials, plugin edits, harness-doc edits, dirty trees, hook timeout, retry cap, and Tier 3 queueing. None of those limits addresses which tools or connectors a scheduled session holds.
- **Partial overlap:** the scout harness restricts scanner tools (`--allowedTools <the source's fetch tools only>`), but that is for subagents.
- **Consumers:** `change-watch` (Routine registration) and the registration hand-off step of `schedule-harness` (cadence, folder, model, worktree).
- **Tension:** the incumbent says to select "always allow" on every permission prompt to seed approvals. The article's point is that the starting tool list should be trimmed before the first run. These two pieces of advice apply to different platforms, but a Desktop-task user gets only the first.
- **Verification:** "every connector … included by default" and "writes … without … permission" are the highest-stakes claims, and they are unverified.

### T8. Catching the network denial signature (`403` + `x-deny-reason: host_not_allowed`) → DISCARD

The general rule ("any fetch error becomes unreachable") is already redundant (T1). The specific string is unverified and brittle: the clean-room review notes that matching it exactly fails if Anthropic changes the header. No scheduled run here is a cloud Routine on the Trusted network, so nothing would consume it. If kept at all, it belongs as a `state/watch.md` entry (recheck, then maybe re-fetch), not as skill text.

### T9. The eight-row checklist → REDUNDANT for local harnesses, COMPLEMENT for Routines

Row by row, the incumbents are stronger wherever they overlap:

| Article check | Incumbent |
|---|---|
| 1 Self-contained | `CLAUDE.md`: "Files are the source of truth; conversation memory is not." |
| 2 Sources named | `phase-0-scan.md` item schema ("a block missing a field is dropped") and `evidence-report`: "Attach the identifier." |
| 3 Verified | `evidence-report` and spec §3 |
| 4 Idempotent | spec §6 |
| 5 Honest when blind | `CLAUDE.md` |
| 6 Least privilege | partial (T7) |
| 7 Fails loudly | Tier 3 queue, "Never ask", "The report is the deliverable" |
| 8 Time-aware | `schedule-harness` time guard |

As a pre-scheduling review for cloud Routines it is a genuine complement. Nothing local covers that lane. Still, it is a table in a blog post, not a gated check, so adopting it would be a reference note, not a skill.

### Whole-article verdict

**COMPLEMENT** (small) for the Routine lane, plus the fragments above. It is not a superior substitute for anything, because nothing in it beats an incumbent as a whole.

## 2. Routing collisions

The article has no `name` or `description`, so nothing collides today. If it were wrapped as a skill, for example "routine-hardening":

- **`schedule-harness`.** It triggers on "schedule this phase", "turn this into a scheduled task", "unattended on a cadence". A new Routine skill would trigger on "routine", "unattended", "scheduled". For "turn this into a scheduled task", `schedule-harness` would win, because it names the exact phrase. For "my routine reported success and did nothing", nothing local fires. The new skill would need a "Not for" line mirroring `schedule-harness`'s own carve-out: harness phases on a local desktop go to `schedule-harness`, cloud Routines go to the new one.
- **`change-watch`.** Its description already says "a scheduled task or Routine gets registered", so a prompt about watching something on a Routine could route to either.
- **`evidence-report`.** Its trigger is "any claim that work is done". The article's "reported success" language overlaps, and `evidence-report` would win because it is stable.
- **Same name, different body.** None. The article carries no name.
- **Vocabulary collision.** This is the quiet one. Three words now name one concept: the article's "unavailable", `CLAUDE.md`'s "unreachable", and `evidence-report`'s "UNVERIFIED". A reader grepping run logs for "unreachable" would miss a section that says "unavailable". Ingest should use the library's words.

## 3. Philosophy conflicts (contradictory, not just different)

1. **Self-verification.**
   - Article, Check 3: "Add a step where the routine re-opens its own output and checks it against what it read."
   - `toolkit-interface-spec.md` §3: "The reviewer runs on a model that differs from the builder's, with no parent history." And `evidence-report`: "never substitute reasoning about why it probably works."
   - The article's check is the same session re-reading its own output, with no executed command. That is exactly the check the incumbents do not count as evidence. Treat T2's check as a cheap first filter, never as the verdict.
2. **Thin pointer vs self-contained prompt.**
   - Article, Check 1: "Write it as instructions to a competent stranger … name the files, name the windows, name the thresholds."
   - Spec §7: "The dispatch logic has one editable home in the harness." The pointer body is "nothing else".
   - A local harness can rely on files. A cloud Routine has no local harness, so the article's rule is correct there and wrong for `schedule-harness`. Do not merge the two. Keep the lanes separate.
3. **Permissions posture.**
   - Incumbent: "select 'always allow' for each one" (`references/platform-facts.md`, saved approvals).
   - Article, Check 6: "Strip that list down to what the routine actually needs before the first run, not after the first incident."
   - These are not strictly contradictory because they address different platforms. But a reader who follows both gets blanket approval first, trimming later. The incumbent should add a review of the "Always allowed" panel (the platform doc already mentions it).

## 4. Corrections needed at ingest

- **Em dashes and AI tells.** `CLAUDE.md` says "No em dashes in authored text." The article uses them throughout ("it does not mean the task in your prompt succeeded"). It also has not-X-but-Y constructions ("It is not good news. It is *no* news"), staged one-line closers ("Two outcomes, never one. That is the entire trick.") and bold labels. Run `humanizer` over any fragment before it lands.
- **A stateless model cannot compare to a slot it was never told.** Check 8 says to "compare it to the slot it was meant to run in". A Routine session receives no slot. The prompt must hardcode the intended time (for example "this run is meant for 07:00 local"), and the model needs a clock source such as `date`. Without this the rule cannot be honored.
- **"Append one line per run to a log file."** No destination is given. A cloud session's filesystem may not persist (the clean-room review flags this). Locally this works (`runs/`). For a Routine, name an external store or a repo commit.
- **PARTIAL cannot be self-enforced.** The model that fails to read a source may also fail to write PARTIAL. Pair it with an out-of-band check. `CLAUDE.md` already has one shape of this: "A cycle that ends without republishing the report page to `report_artifact_url` is not done." Staleness of that report is detectable without the model's cooperation.
- **Platform facts need dated primary-source quotes.** The article is dated 5 Oct 2026, the same day as this comparison, and quotes nothing. The incumbent standard (`references/platform-facts.md`) is the quoted doc line plus fetch date. Re-fetch the Routines doc and quote the lines for the Trusted network, `x-deny-reason`, 9:07, and connector defaults. Until then, treat all four as unverified. The 5 Oct date stamp is not evidence.
- **Upsell claims.** "The one almost every prompt fails" and "the single highest-value edit" are unsupported. Drop them.
- **Terminology.** Use the library's terms (harness, Tier 3, unreachable) and not "routine" generically. "Routine" capitalised means the cloud product in `schedule-harness`'s description.
- **Do not ingest the companion articles or product links.** The "hardened prompt you can paste in" was not read, and the funnel to a paid product is a commercial pitch.

## 5. Net assessment: the three things to take

1. **Verbatim error text and explicit window in the unreachable record** (T1 fragments). Add them to `incumbents/CLAUDE.md` "Working conventions" and `phase-0-scan.md` step 6 coverage record. Use "unreachable" and "UNVERIFIED". This is a Tier 3 proposal under the scout harness's own rule, not an auto-apply.
2. **Late-run disclosure plus intended-window rule** (T5 fragments). Add them to `schedule-harness/SKILL.md` "Overlap skip and the time guard". Resolve first the contradiction that the pointer template has no place for a time guard.
3. **PARTIAL forced by an unreachable source or a failed check** (T3 fragment). Put it in `schedule-harness/SKILL.md` `## Done when` and on the first line of the run-log fixture, so a script can count PARTIAL runs.

Everything else: do not ingest. Park the platform-specific Routine claims (9:07, connector defaults, `x-deny-reason`) as `state/watch.md` recheck entries until a dated primary-source quote exists. No whole item is worth installing as a skill.