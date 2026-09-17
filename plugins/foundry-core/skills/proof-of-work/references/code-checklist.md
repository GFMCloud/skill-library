# Code artifact class: a concrete check sequence

`proof-of-work` says code is proven by running it against representative input. This is
the ordered list of what to run for an ordinary JavaScript, TypeScript or Python repo when
the project names no sequence of its own. The project's own commands win where they exist.

Adapted from the ECC project's `verification-loop` skill (MIT, v2.2.1), reviewed
2026-09-17. Record: `docs/reviews/2026-09-17-ecc/`. Two changes from the source: its
commands piped output through `head` and `tail`, which hides the tool's exit code, so the
pipes are gone; and its "verify every 15 minutes" cadence was left out, because an
unattended cadence belongs to `workbench:schedule-harness`, not to an evidence standard.

Run in this order. Send long output to a file and read the file; never pipe a check
through `head`, `tail` or `grep`, because the exit code reported is then the pipe's.

| # | Phase | JS / TS | Python | Rule |
|---|---|---|---|---|
| 1 | Build | `npm run build` | the package's build or import check | **Stop** on failure: nothing after this means anything |
| 2 | Types | `npx --no-install tsc --noEmit` | `pyright .` | report every error with its count |
| 3 | Lint | `npm run lint` | `ruff check .` | warnings reported, not silently fixed |
| 4 | Tests | `npm test -- --coverage` | `python3 -m pytest` or `python3 -m unittest discover` | **Stop** on failure; report total, passed, failed, and coverage if the repo measures it |
| 5 | Secrets and leftovers | the project's secret scanner; failing that `grep -rn` for key-shaped strings and stray debug logging in the changed files | same | a secret hit is a hard stop, not a warning |
| 6 | Diff | `git diff --stat`, then read each changed file | same | look for unintended changes, missing error handling, unhandled edge cases |

Do not invent a coverage threshold. If the repo sets one, report against it; if it does
not, report the number.

Phases 1 to 5 are pre-filters plus the test run. They do not replace the standard's first
rule: the changed behavior itself is executed against representative input and the output
is inspected. A green sequence with no run of the new behavior is not evidence for it.

Report in the `evidence-report` format. One line per phase with the command, the exit
code and the count that matters, then the not-verified list. A phase that could not run
(no build script, tool absent) is listed as not run, never as passed.
