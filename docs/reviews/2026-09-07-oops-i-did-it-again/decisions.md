# Decisions: oops-i-did-it-again

contract: v1
source: https://github.com/Astezelex/oops-i-did-it-again-poc
type: code-repo
pin: 7069bf0d88da6854e3bb0ef3db55ab4178c66001 (cloned 2026-09-08T00:24:38Z)
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-07-oops-i-did-it-again/cleanroom-review.md, docs/reviews/2026-09-07-oops-i-did-it-again/comparison.md

## Verdict reasoning

Installing is out: the installer merges hooks into `~/.claude/settings.json` by script (this
machine wires hooks by a ruled runbook), the skill's Step 3 writes new hook code without a
confirmation gate, and style-guard would reopen the closed em-dash scoping ruling. The method
is the deliverable, and it is unusually well measured for an eight-day, one-operator
experiment: the headline 9.15 to 4.29 per 100 commands recomputes from shipped data, every
rule carries its incident and its birth date, and the repo publishes the correction that
halved its own result. Three things fill real gaps: replay a rule against real history before
wiring it (the noise-rate half that prove-hooks.sh lacks), five evidence-class Bash guards
that mechanize rules this machine states only in prose, and the recurrence-escalation rule.
What would change the verdict: nothing toward ADOPT; the pieces are meant to be taken apart.

## Ancestry

none. Independent invention of adjacent territory; the prove-hooks.sh lineage is the hstack
review, a different candidate the same week.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session (phased-harness).
Adoption cost is mandatory and never "none".

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Replay a candidate rule against real command history before wiring it; a WARN above about 5 percent of commands is too noisy | COMPLEMENT (prove-hooks.sh proves correctness on fixtures; nothing measures noise on real traffic) | `scripts/replay-hooks.py` in skill-library: run a hook command over the Bash commands in a COPY of `~/.claude/projects/*/*.jsonl` and report fire rate per rule; one line in prove-hooks.sh's header naming it as the second proof | `hooks/replay.py:20-30`, `README.md:185-187` | new `~/skill-library/scripts/replay-hooks.py` plus one header line in `scripts/prove-hooks.sh` | M | a script to keep in step with the hook contract; it reads transcripts, so it runs on a copy and prints nothing but rates | ratified 2026-09-07; one-session runbook claude-scout-weekly `docs/runbooks/2026-09-07-replay-hooks.md` | Graham |
| 2 | Evidence-class Bash guards with no installed analogue: pipe masks exit code, stderr discarded, measurement silenced, empty grep read as absence, arbitrary row from a listing, guessed unit candidates | COMPLEMENT (mechanizes "a tool's output is proof of what you checked, not of what exists") | A second PreToolUse Bash hook (`~/.claude/hooks/evidence-guard.sh`), WARN only (additionalContext, no permissionDecision), each rule with a fixture in `scripts/prove-hooks.d/` and a replay (row 1) before wiring | `hooks/bash-guard.py` rules `r_pipe_masks_exit_code`, `r_stderr_discarded`, `r_measurement_silenced`, `r_empty_grep_as_absence`, `r_arbitrary_row_from_listing`, `r_guessed_unit_candidates` | `~/.claude/settings.json` plus a hook script | M | one more process per Bash call; warn fatigue if noisy (the replay is the guard against that); removal is deleting the entry | ratified 2026-09-07 into the hooks-and-permissions runbook (Step 5), gated on row 1 existing | Graham |
| 3 | Catastrophic-command patterns absent from the runbook's derived list: download piped to a shell, fork bomb, `dd` to a raw device, `mkfs` on a device, `chmod 777 /` | COMPLEMENT | Add the five patterns to the destructive-command hook's list in the runbook, each with a fixture | `hooks/bash-guard.py` `r_catastrophic` | `claude-scout-weekly/docs/runbooks/2026-09-03-hooks-and-permissions.md` Step 1 | S | five more patterns to prove | ratified 2026-09-07 with Q-2026-09-07-3; applied 2026-09-07 (runbook Step 1) | scout |
| 4 | Bash-level secret detector: literal secret in an export, `sshpass -p`, a credential file printed or piped to the network | COMPLEMENT (the secrets rule is pre-commit, not pre-execution) | One WARN rule in the row 2 hook or the runbook's hook | `hooks/bash-guard.py` `r_secret_exposure` (note its any-pipe-is-a-capture choice, justified by six false denials in replay) | same as row 2 | S | false positives on legitimate pipes until replayed | ratified 2026-09-07 with Q-2026-09-07-3; applied 2026-09-07 (runbook Step 5) | scout |
| 5 | WARN on edits to `.claude/settings*`, `.claude/hooks/`, or the guard scripts themselves | COMPLEMENT (the auto-mode classifier blocks only edits that grant standing autonomy) | One WARN rule in the row 2 hook | `hooks/bash-guard.py` `r_config_guard` | same as row 2 | S | noise when hooks are legitimately edited | ratified 2026-09-07 with Q-2026-09-07-3; applied 2026-09-07 (runbook Step 5) | scout |
| 6 | Rule-birth dating: a rule cannot have influenced a command written before it existed, so every before/after comparison uses the rule's own start date | COMPLEMENT (an S-effort interim answer to the tabled ablation question, config-drift-checker row 4) | Record the birth date in each fixture file and have replay-hooks.py (row 1) split its rate at that date | `analysis/measure.py:47-67` | `scripts/prove-hooks.d/*.json` (a `born` field) and row 1's script | S | none beyond row 1 | ratified 2026-09-07 with row 1 (replay-hooks runbook) | Graham |
| 7 | Recurrence escalation: on the third occurrence of a failure class, stop and say the mechanism is failing; do not add a fourth rule on top of three that are not firing | INGESTIBLE FRAGMENT | One sentence in the global Evidence over assertion section, or the authoring standard; must first resolve the trigger-surface collision with `retro` (both fire on "a mistake just happened" with contradictory write authority) | `skills/oops-i-did-it-again/SKILL.md:94-97` | `~/.claude/CLAUDE.md` (Tier 3) or `docs/authoring-standard.md` | S | one more always-loaded sentence if global | ratified 2026-09-07 (Q-2026-09-07-9: `retro` owns the trigger); applied 2026-09-07 as a recurrence-check paragraph in retro section 3, not in global CLAUDE.md | scout |
| 8 | Stop-hook loop brake: `stop_hook_active` plus a session-scoped counter that gives up after two blocks | COMPLEMENT (no Stop hook exists here; hstack row 7 is tabled) | Reference for whoever builds the first Stop hook; attach the pin to hstack row 7 | `hooks/style-guard.py:20-28,109-139`, `tests/test_style_guard.py:88-90` | `docs/reviews/2026-09-03-hstack/decisions.md` row 7 (a pointer) | S | none until a Stop hook exists | ratified 2026-09-07; applied 2026-09-07 (hstack decisions row 7) | scout |
| 9 | Write-time check for unverified vendor-behavior claims in notes and handoffs | COMPLEMENT (fact-currency-check checks old facts, not fresh assertions) | Watch; a Write/Edit hook rule if the handoff skill grows a lint step | `hooks/file-guard.py:46-51` | none today | M | false positives on ordinary prose | out (no consumer today; noted for handoff) | Graham |
| 10 | ShellCheck on write | COMPLEMENT, do not port as-is | Silent pass when ShellCheck is absent is the failure class the repo exists to kill; any port makes absence a visible WARN | `hooks/file-guard.py:106-138` | none | M | ShellCheck dependency | out | scout |
| 11 | style-guard Stop hook (em dash, a phrase tic) on every turn | DISCARD (reopens a closed ruling) | The installed dash gate is scoped to Artifact publish by ruling; widening is a separate ruling, not an ingest | `hooks/style-guard.py` | none | n/a | n/a | out | scout |
| 12 | install.sh, guard.py, PORTING.md | DISCARD | Wrong paradigm for how this machine wires hooks; portability problem this machine does not have. Keep the `canon()` order-insensitive JSON fingerprint in mind if a hook installer is ever built | `install.sh:116-125` | none | n/a | n/a | out | scout |

## Conflicts for the user to rule on

- `git reset --hard`: the runbook's hook BLOCKs it; the candidate WARNs ("BLOCK is only for
  traps that are never legitimate"). Proposal: keep BLOCK here (the runbook was ruled).
  Alternative: adopt the candidate's WARN tier for this one command.
- Who adds a standing restriction: the candidate's skill writes new hook code as an ordinary
  step; here a hook goes through a gated runbook with recorded proofs. Proposal: row 7's
  fragment only, never the skill's Step 3. Alternative: none recommended.
- Style enforcement scope (row 11): Artifact publish only (ruled) versus every Stop event.
  Proposal: leave the ruling. Alternative: reopen via a runbook.
- A permissive verdict must be silent, not an explicit allow: the candidate's rule
  (`bash-guard.py:13-16`, an "allow" bypasses the normal prompt) agrees with how the installed
  em-dash hook already behaves (empty output on the negative control). No ruling needed;
  recorded so prove-hooks.sh keeps treating empty output as the allow verdict.

## Corrections at ingest

- Test counts stated as 95, 83, and 96 in three places; do not quote any of them.
- `file-guard.py` ShellCheck path passes silently when the binary is absent (row 10).
- Polish identifiers in `bash-guard.py:356-369` and `measure.py:125-129`; rewrite, never copy.
- `replay.py` reads `~/.claude/projects/*/*.jsonl` directly; run any port on a copy.
- A few README lines lean toward mannered prose; restyle any quoted sentence.

## Flags

Disclosed, not injection: `AGENTS.md` is addressed to an installing agent ("Run these in
order ... `./install.sh`") and tells the agent to read the user's real shell history aloud
via replay.py; `install.sh:84-170` pipes an inline Python heredoc into python3 to rewrite
`~/.claude/settings.json`. No credential solicitation; test secrets are assembled from
fragments. None acted on.

## Rulings log

2026-09-07: proposed by the scout cycle (cycle 2); nothing ratified. Rows 3 to 5 amend the
hooks-and-permissions runbook and ride Q-2026-09-07-3. Recorded in claude-scout-weekly
STATE.md as Q-2026-09-07-8.
2026-09-07: ratified in claude-scout-weekly `/phase ratify` (Graham, interactive). Rows 1 and 6 to the replay-hooks runbook; row 2 to the hooks runbook after row 1; rows 3, 4, 5 applied to the hooks runbook with Q-2026-09-07-3; row 7 waits on the retro arbiter; row 8 applied. Recorded as Q-2026-09-07-8 ruling.
2026-09-07 (later): Q-2026-09-07-9 ruled by Graham, `retro` owns "a mistake just happened"; row 7 applied to retro section 3 (workbench 0.9.3).
