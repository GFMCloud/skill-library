General working agreements live in `~/.claude/CLAUDE.md`. The repo's authoring rules live in
`../../CLAUDE.md`. This file adds only what is specific to the 2026-10 two-laptop migration.

# migration-2026-10: session instructions

This directory is the harness for making `GFMCloud/skill-library` the one editable home of
every generic skill on both laptops. You are here to execute one phase of it, on one machine.

## Orientation (do this first, every session)

1. Run the machine detection step at the top of every runbook before anything else. Home
   runbooks require `gh api user --jq .login` to print `GFMCloud`; work runbooks require
   `gmorris1221`. Any other result stops the run.
2. Read this machine's state file (`STATE-home.md` or `STATE-work.md`): phase reached, commit
   SHA the machine was brought to, decision log, evidence, anomalies.
3. Read `CONFIG.md`. **If any value is `TBD`, stop and ask before doing anything else.**
4. Load the runbook for the next phase from `prompts/` and execute it. A phase's prerequisite
   phase must be marked complete in the relevant state file; if it is not, say so and stop.
5. `docs/end-state.md` defines the invariant. When an instruction here or in a runbook is
   ambiguous, that document is the tiebreaker.

## Hard guardrails

- **Nothing in a work-side runbook is executed from the home laptop, and nothing in a
  home-side runbook from the work laptop.** The machine detection step enforces it; a session
  that finds itself on the wrong machine stops at that step.
- **No write to GitHub as gmorris1221 from the home laptop, and no GFMCloud credential on the
  work laptop.** The home laptop may read gmorris1221 repositories (and switches `gh` back to
  GFMCloud afterwards); it never writes as that account.
- **Phase -1 is read-only.** Its two stated exceptions (the throwaway branch push and pausing
  the weekly maintainer) are the only state changes, each recorded with its undo.
- **Phase 0 disables nothing.** No company pack is disabled or dropped until it is empty, in
  Phase 1, under its own gate.
- **This directory is public.** No company, customer, person, account ID, internal hostname or
  work-laptop user name appears in any file here, including pasted survey output. Redact
  before pasting (`<brand>`, `~`, counts instead of logins). The denylist scan is the
  mechanical check; the denylist itself never enters the repo.
- **A collision with an invariant is a stop, not a tiebreak.** If a phase's plan collides with
  the invariant in `docs/end-state.md`, a guardrail here, or the never-pre-authorizable list
  in `CONFIG.md`, the phase bends and the invariant does not. Record the collision in the
  state file and stop for a ruling.
- **Move, never copy.** A skill that moves into skill-library leaves its old location as a
  `.superseded` rename (the machine-wide convention), never as a second editable copy.
- **Nothing is deleted until Phase 3 verification passes and Gate B is confirmed.**
- **Decisions are proposed by Claude and ruled by Graham in one batch at Gate A.** Execution
  phases run only ruled rows; unruled rows are skipped and reported, never guessed at.
- **Every gate is proven by deliberate failure before it is trusted.** Each runbook names the
  negative control for any gate it introduces; the control's output goes in the state file.
- **Every PR this harness produces is reviewed by a fresh session at or above the author's
  model tier before merge.** Merging is never pre-authorized.

## Working conventions

- The two state files are the resume points, one per machine. Keep them current as you work.
  Files are the source of truth; conversation memory is not.
- Record executed evidence (the command and its actual output) per
  `foundry-core:evidence-report`. A green CI run is necessary, not sufficient.
- Anomalies go in the state file under Anomalies with a one-line recommendation and are
  reviewed at the next gate, not raised one by one.
- Commits in `~/skill-library`: one PR per deliverable, validator exit 0, a `CHANGELOG.md`
  line for any behavior change, secret scan (`gitleaks`) and denylist scan clean before each
  commit, pushed only under the global push carve-out (own commits, GFMCloud origin, `gh auth
  status` shows the machine's account, `git log --oneline origin/main..HEAD` equals the SHAs
  recorded in the state file).
- Commits in the company marketplace and in the config repos happen on the work laptop only,
  as gmorris1221, and are recorded in `STATE-work.md` by SHA.
