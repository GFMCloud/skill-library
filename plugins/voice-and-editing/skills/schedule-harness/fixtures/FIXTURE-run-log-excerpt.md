FIXTURE: illustrative run log excerpt. This is not a real scheduled-task run, no task
named `cfb-picks-sunday-grade` exists yet, nothing here was executed, and no timestamp
below corresponds to an actual event. It exists only to show, per the roadmap's
Validation line for T7, what "the run log shows the limits honored and a queued item
where a question would have been asked" and "a second run started during the first is
skipped with the built-in reason" should look like once a real task is registered and
run. Do not cite this file as evidence that a run happened.

---

## Run 1, 2026-09-14T18:07:00-05:00 (Sunday, scheduled)

Task: cfb-picks-sunday-grade
Mode: grade
Permission mode: acceptEdits (saved from the attended "Run now")
Worktree: none (this phase commits picks results to the harness's own tree)

- Read `/Users/gfm/work/cfb-picks-harness/.claude/skills/phase/SKILL.md`, dispatched
  phase `grade`.
- Time guard in the prompt held: "only grade games completed before this run's start
  time": 3 games still in progress were skipped, not graded as losses.
- Step "fetch final scores" failed once (rate-limited, HTTP 429), retried, succeeded on
  attempt 2 of the consecutive-retry cap of 2. Logged, not escalated.
- Step "flag any pick whose grading is ambiguous" found one ambiguous case (a game
  ruled a no-contest after weather cancellation). Per the Absolute-limits block v1 line
  "anything the run would have asked becomes a queued Tier 3 item", this was not asked
  as a question, it was written to the Tier 3 queue:

  ```
  Tier 3 queue entry, 2026-09-14T18:11:42-05:00
  source: cfb-picks-sunday-grade, run 1
  question: "Auburn @ Georgia was ruled a no-contest after a weather cancellation,
             does the harness's grading spec treat a no-contest pick as a push, a
             loss, or excluded from the week's record?"
  status: pending
  ```

- Hook timeout (120s) never triggered; longest hook ran 34s.
- No git push attempted. No deletion. No credentials touched. No edit under
  `~/.claude/plugins/`. No edit to the harness's own CONFIG.md, CLAUDE.md, or prompts/.

**Summary written by the run:** "Graded 11 of 14 completed games; 3 in-progress games
deferred to next run; 1 game queued to Tier 3 for a grading-rule question; 1 transient
rate limit retried and recovered within cap." This summary names the queued item and
the retry, matching the run's actual outcome, not just a green status line.

## Run 2, 2026-09-14T18:09:00-05:00 (manual "Run now", started while Run 1 was active)

- Skipped. Run history reason (platform-native, not re-implemented by this skill):
  "the previous run was still in progress." See
  [references/platform-facts.md](../references/platform-facts.md), "Review history"
  bullet.
- No session was started, no tokens spent, no files touched.
