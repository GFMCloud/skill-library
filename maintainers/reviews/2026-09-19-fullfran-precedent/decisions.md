# Decisions: fullfran-precedent

contract: v1
source: https://github.com/FullFran/precedent
type: code-repo
pin: f5141c341f60e1510d413e48a2095bb358b0463b (v0.6.0; shallow clone 2026-09-19)
reviewed: 2026-09-19
verdict: HARVEST
recheck:
evidence: docs/proposals/2026-09-19-fullfran-precedent/cleanroom-review.md, docs/proposals/2026-09-19-fullfran-precedent/comparison.md (claude-scout-weekly; held here because of A-11)

## Verdict reasoning

A careful, stdlib-only `PreToolUse` hook that injects a hand-written lesson page when an
Edit, Write, or Bash call matches the page's path or command globs. It is the third
independent implementation of just-in-time rule loading this project has seen (onsetter,
cycle 1; jev-rules, cycle 4 C-16), and the first with tests and a fail-open contract. It is
also one day old: four releases all dated 2026-09-19, one author, 0 stars, 0 issues (gh api,
2026-09-19), its manual contradicts its code on what gets injected, and its evidence splitter
has a real bug. So the plugin is not installed and not adopted. The rows are: a built
reference for step 2 of the ratified JIT-rules prototype runbook (Q-2026-09-03-12, not yet
run: no result file exists), two fragments for that runbook, a vocabulary for retro's
unsolved demotion, and one gap it exposed in the installed evidence-guard. The verdict would
move to WATCH if Graham drops the JIT prototype.

## Ancestry

none. Independent convergence on the hook API's `additionalContext` field; the incumbent
runbook predates the candidate by 16 days.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Path and command triggered injection from a corpus, built and tested | SUPERIOR SUBSTITUTE for step 2 of the JIT runbook only | When the JIT prototype is run, vendor `tripwire.py` project-locally into `.claude/hooks/` with `PRECEDENT_PATTERNS` pointing at a project directory, never `/plugin install`; fix the `#`-in-evidence split and the dead line first; prove with `prove-hooks.sh`; replay any Bash trigger page through `replay-hooks.py` | `plugin/claude-code/scripts/tripwire.py`; `README.md:60-63` | `docs/runbooks/2026-09-03-jit-rules-prototype.md` step 2 (claude-scout-weekly; a harness file, Graham's edit) | M | A subprocess on every Edit, Write, and Bash call (5 s timeout); an append-only log of every edited path with no rotation; a vendored file from a one-day-old, single-author repo that must be read in full at the pin; backs out by removing the hook entry and the file | proposed | Graham |
| 2 | An `## Evidence` section stays on disk while the hook injects the rest | INGESTIBLE FRAGMENT | One sentence in runbook step 1: a rule file may carry its two quoted corrections under `## Evidence`, not injected. Fits "write a fact down only once it has cost a correction twice" without paying for the quotes on every match | `tripwire.py:144-146` | same runbook, step 1 | S | One sentence; depends on row 1's splitter fix | proposed | Graham |
| 3 | `injected_chars` logged per invocation | INGESTIBLE FRAGMENT | Runbook step 3 measures the hook arm from the log instead of by hand; note it counts characters, not tokens | `CHANGELOG.md` 0.6.0 | same runbook, step 3 | S | One sentence | proposed | Graham |
| 4 | "Retired is a decision, skipped is a typo": retirement with a stated reason keeps the evidence and drops the triggers | COMPLEMENT | One design requirement in retro section 6 for the future `/retro-review` (retro "promotes idempotently but never demotes"), with the caveat that fires per page do not prove the page was followed; possibly `retired` in the template's Status enum. Blocked on conflict 1 below | `tripwire.py:288-295` | `plugins/long-projects/skills/retro/SKILL.md` | S | Text only; none beyond upkeep | proposed | Graham (S-16: retro owns this surface) |
| 5 | (exposed by the candidate's redaction counterexample) evidence-guard's secret rule needs `export` and 16+ characters, so `TOKEN=sk-abc gh ...` passes silently | COMPLEMENT | Add an inline-assignment arm (`\b\w*(KEY|TOKEN|SECRET|PASSWORD)\w*=\S+\s+\S`) as WARN, with positive and negative fixtures, replayed on four weeks of history against the 5-per-100 bar before wiring. Verified 2026-09-19: `evidence-guard.py:58` requires `\bexport\s+` | `tripwire.py:483-490` | `~/.claude/hooks/evidence-guard.py` (settings-wired hook) | S | One regex and two fixtures; replay first because inline env assignment is common | proposed | Graham (settings hook: always Tier 3) |
| 6 | Redaction by token boundary, not length | COMPLEMENT, no consumer | Park until a hook here logs command lines | `tripwire.py:477-503` | none | - | - | out | - |
| 7 | Suppression list keyed on stable ids, printed every run | COMPLEMENT, consumer unverified | Park; plausible for `skill-discovery`, not read in this comparison | `tools/mine.py:60-70, 521-525` | none | - | - | out | - |
| 8 | Push not pull; fail-open contract; not-wired-up detection; two-occurrence admission rule; count unknown history apart | REDUNDANT | Boundaries rule, evidence-guard, runbook step 4, the economy rule, evidence-report | comparison.md items 1, 5, 9, 10 | none | - | - | out | - |
| 9 | OpenCode adapter; `tools/mine.py`; the plugin install itself | DISCARD | No OpenCode here; the miner reads a third-party memory database; installs are Tier 3 and this repo is one day old | - | none | - | - | out | - |

## Conflicts for the user to rule on

1. Retro: "Do not create a `learnings/` directory or any other second store ... A parallel
   store of the same kind of content rots because nothing ever reads it consistently." vs the
   candidate: a lesson corpus read deterministically by a hook on every matching tool call.
   Proposal: no second store; if the JIT prototype succeeds, its rule files are the project's
   rules moved out of CLAUDE.md (a move, not a copy), which is what Q-2026-09-03-12 already
   tests. Alternative: exempt a hook-read corpus in retro's text. Reasoning: the retro
   sentence's premise is "nothing ever reads it", which a hook falsifies, but one editable
   home still binds.
2. Economy rule: "every line loads into every session" vs three implementations that load a
   rule only when a matching tool call happens. This is Q-2026-09-03-12 again, now with a
   credible implementation. Proposal: run the ratified prototype runbook with row 1 as its
   hook before changing any rule text. Alternative: keep the prototype hand-built as written.

## Corrections at ingest

- `DOCS.md:95-102` documents the abandoned heading-to-EOF cut; the code re-appends the tail.
  The "55%" figure fits only the abandoned rule (about 23% by count at this pin).
- `tripwire.py:177-182` treats any indented line starting with `#` as a heading, so a quoted
  shell comment ends the Evidence section early and the rest is injected. Anchor the scan to
  unindented `^#{1,6}\s` and add a test. Dead line at `tripwire.py:169`.
- "28ms", "7-29%", "24-48%" have no artifact in the repo; do not carry them.
- CI asserts no test count: `unittest discover` on a moved `tests/` goes green on zero tests,
  against the project's own starter page.
- The corpus directory becomes model-facing text; keep it in a reviewed repo.
- The candidate's prose is dense with em dashes; strip them from anything ingested.

## Flags

Nothing addresses a reviewing agent. The product itself is model-directed text, quoted in
cleanroom-review.md section 6 ("Read it before your next action."; "Make it fail on purpose,
once, and watch it go red."). README install steps (`/plugin marketplace add`, plugin
install) were not followed. No script from the repo was run; the reviewers had no shell.

## Rulings log

2026-09-19, scout cycle 4 (unattended): all rows proposed, none applied. Queue entry
Q-2026-09-19-8.
