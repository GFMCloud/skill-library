# Ready-queue run: a builder-reviewer lane over Ready cards

How a session works several Ready cards in one sitting with subagents. Four sessions in the
week of 2026-09-28 rebuilt this lane by hand from a prior run's DONE.md; this file is the
shape they converged on. It starts from Ready cards and
ends with card updates, so it lives with the board. For one change with no board, use
`long-projects:orch-pipeline` instead.

## 1. Pick and plan

- Query the board for `ready` cards in the current lane, in lane then due-date order. Skip a
  card with an unfinished `blocked_by` and anything on the run's "Not this time" list.
- Write the plan before any spawn: per card, the builder model (state it; never inherit
  silently), the files it may touch, and the check that proves it (`done_when`). Cards that
  touch the same files go in different waves or the same builder.
- For more than three cards, or any card that touches prod or a shared schema, have a
  higher-tier advisor read the plan against the repo first. In one run it caught stale line
  anchors, a second crash site, a dependency trap and partial-card rules before any builder
  started.
- Move each picked card to `doing` (pinned write, [cards.md](cards.md)).

## 2. Build, in waves

- One builder subagent per card, each in its own git worktree on its own branch
  (`<card-id>-<slug>`), with the card's `done_when`, its file list, and a do-not-touch list
  naming the other builders' files. Git commands that move shared refs, the board and the
  run log stay with the orchestrator.
- Two waves is the usual size; a wave starts when the previous wave's reviews are back.
- Check that `.claude/worktrees/` is ignored in the repo before the first worktree; if it
  is not, say so on the run's card rather than committing worktree clutter.

## 3. Review, fix loop capped at two

- Per card, a fresh reviewer that did not build it, of a higher tier than the builder
  (the board's tier rule; a Fable-built card gets a fresh Fable reviewer), checks the
  branch against `done_when` and runs the card's check itself. Its verdict goes on the card's `review` record.
- On a red verdict, the builder (or a fresh fixer) makes one fix pass and the reviewer
  re-runs. Two rounds at most. Still red after two: move the card back to `ready` with the
  reviewer's findings in `notes`, or file an inbox card if the blocker is a decision, and
  go on to the next card.
- This loop gates a subagent's fix, not the session's own turn, so `/goal` with
  `bounded-loop` does not apply to it; the cap of two is the bound.

## 4. Land each card

- After a green review the orchestrator re-runs the suite itself on the branch. A reviewer's
  green is not the orchestrator's evidence.
- Commit on the card's branch (one branch per card), record the SHA, remove the worktree,
  and update the card: `review` record, `evidence` (what ran and what it printed), and
  `column: review` or `done` per the board's rules.
- Merges go through a pull request (SKILL.md, "An Accept does not reach the auto-mode
  classifier"). Pushes follow `push_check.sh` per branch, each push its own command.

## 5. Close the run

Re-read the inbox, take the next Ready card if any remain (continue by default), and end
with the inbox count and the board link. Every commit, push and merge is logged on its card
before the turn ends.
