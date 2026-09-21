# Decisions: learning-plugin (scoped-learnings)

contract: v1
source: https://github.com/ahasha/learning-plugin
type: code-repo
pin: 947f9eedb26d715e2a38e78ad96259c06820802e (v0.1.0; shallow clone 2026-09-21; repo created 2026-09-19, 0 stars, MIT, 9 files, no tests, no CI)
reviewed: 2026-09-21
verdict: HARVEST
recheck:
evidence: maintainers/reviews/2026-09-21-learning-plugin/cleanroom-review.md, maintainers/reviews/2026-09-21-learning-plugin/comparison.md, maintainers/reviews/2026-09-21-learning-plugin/claude-code-docs-memory-rules-section.md (first-party docs excerpt, fetched 2026-09-21)

## Verdict reasoning

A small plugin that writes learnings into `.claude/rules/*.md` files with `paths:`
frontmatter, plus a stdlib checker that flags rule files whose globs match nothing. The plugin
is not installed: its Stop hook asks the model to self-assess ("did this session surface a
non-obvious gotcha ...? ... If not, stop [and] do not mention this check"), which contradicts
retro's "Determine the gate from evidence, not self-assessment", and its recording skill
writes first and shows the diff after, where retro only proposes. Its checker has a confirmed
parser bug (an inline `paths: ["src/**/*.{ts,tsx}"]` splits inside the brace group and exits
1 on a valid rule) and no tests.

The review's value is what the candidate stands on. It is the fourth just-in-time rule loader
this project has seen (onsetter, jev-rules, FullFran/precedent) and the first that uses no
hook, because **Claude Code documents path-scoped rules as a native feature**
(code.claude.com/docs/en/memory, fetched 2026-09-21): "Rules without a `paths` field are
loaded unconditionally and apply to all files. Path-scoped rules trigger when Claude reads
files matching the pattern, not on every tool use." and "Personal rules in `~/.claude/rules/`
apply to every project on your machine." Four cycles of scouting never recorded this
(`grep -c` for `.claude/rules` or `path-scoped` over the seen-index, STATE.md, and the
precedent decisions: 0, 0, 0), and the ratified JIT-rules prototype runbook
(`claude-scout-weekly/docs/runbooks/2026-09-03-jit-rules-prototype.md`) already writes native
rule files in step 1 and then builds a hook in step 2 to load them a second time. The verdict
would be SKIP if the native mechanism were already in use here (`ls ~/.claude/rules`: no such
directory; no project under `~/work` has `.claude/rules/`).

## Ancestry

none.

## Rows

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Native-first re-scoping of the JIT-rules prototype | (from the first-party docs, surfaced by the candidate) | Amend the runbook before it is run: three arms (rules in CLAUDE.md; native `paths:` rules only; native plus hook); keep the step 2 hook only if a fresh-session Write to a new `runs/**` file, with nothing read first, shows no rule text (the one case the docs leave open, since native rules trigger on Read); resolve the runbook's own contradiction (step 1 "Leave the originals in CLAUDE.md" vs step 3 "CLAUDE.md trimmed") and add `.claude/rules/` to its Boundaries list; re-rule precedent row 1 (`tripwire.py`), whose remaining unique value is new-file Write and Bash triggers | docs excerpt; `README.md` | `claude-scout-weekly/docs/runbooks/2026-09-03-jit-rules-prototype.md` (not a library file; Graham's runbook) | S to amend, M to run | The prototype gets one more arm; if native-only works, no hook is built and nothing new needs proving after each CLI update | proposed | Graham |
| 2 | Route path-scoped lessons to a rules file | INGESTIBLE FRAGMENT | retro section 3 routing table gains two rows: a lesson that only applies to certain paths goes to `.claude/rules/<topic>.md` with `paths:`; a cross-project lesson scoped to a file type goes to `~/.claude/rules/` instead of `~/.claude/CLAUDE.md`, which loads every session. The docs make `.claude/rules/` part of the same memory mechanism that is always read, so it is not the "second store" retro forbids ("A parallel store of the same kind of content rots because nothing ever reads it consistently"). Gated on precedent conflict 1 (Q-2026-09-19-8 row 4): rule files moved out of CLAUDE.md are a move, not a copy | `skills/record-learning/SKILL.md` destination table, `:42-44` | `plugins/long-projects/skills/retro/SKILL.md` | S | Two table rows; retro proposes to a location nothing here uses yet, so the first use needs the row 1 result | proposed | Graham |
| 3 | Entry format: the rule, then the reason | INGESTIBLE FRAGMENT | One sentence in retro section 3: an entry that lands in CLAUDE.md or a rules file is "the rule, then the reason", because "The reason is what stops a future reader from deleting a rule they don't understand." Combines with precedent row 2 (`## Evidence` kept on disk) | `skills/record-learning/SKILL.md:47-48` | same retro SKILL.md | S | One sentence | proposed | Graham |
| 4 | Staleness tested against the code, not by reference counting | INGESTIBLE FRAGMENT | retro section 6 says demotion needs "this rule hasn't been referenced in N sessions" tracking and that "No mechanism for it exists yet". Add the alternative route for code-fact rules: test each entry against the current code (gone: delete; changed: rewrite; unsure: list as could-not-verify), and the reason: "A stale rule is worse than no rule: it is confidently wrong." Does not work for process preferences. Also: delete the note once the enforcing check exists | `skills/prune-learnings/SKILL.md:31-32`, `:39-42` | same retro SKILL.md, section 6 | S | A design requirement for the future `/retro-review`; no behavior change today | proposed | Graham |
| 5 | Glob-staleness linter for rule files (`check-rules.py`) | COMPLEMENT, no consumer yet | Only if the row 1 prototype adopts rule files: vendor project-locally after fixing the inline-brace split (`:62-64`), the budget model (brace-free patterns do not consume the 1,000-pattern budget per the docs; `:111` decrements for every pattern), `SKIP_DIRS` applied after the walk (`:150-153`), and the substring error dedup (`:210`); add fixtures. A glob such as `runs/**` matches nothing before the first run, so an empty match needs a first-run exemption | `scripts/check-rules.py` | none yet | M | A hand-rolled YAML subset and glob expander to maintain; mirrors host behavior that can drift | proposed | Graham |
| 6 | Once-per-session marker claimed before acting | INGESTIBLE FRAGMENT | If the row 1 hook survives: emit each rule once per session, claim the marker first ("a hook that prompts when it can't also write its marker file would loop"), and measure total injected characters over the session, not only at the first write | `hooks/learning-check.sh:7-8`, `:54-55` | the same runbook, step 2 | S | One sentence | proposed | Graham |
| 7 | "Prefer enforcement over prose"; destructive skill marked `disable-model-invocation: true` | REDUNDANT | retro routing table ("Deterministic check ... A hook or CI, not prose") and the Boundaries rule are equal or stricter. One check worth doing: whether `adhd` ("Only apply when Graham explicitly invokes /adhd") enforces that in frontmatter or only in prose | `skills/record-learning/SKILL.md:24-28`; `skills/prune-learnings/SKILL.md:4` | none | - | - | out | - |
| 8 | The Stop hook, the `record-learning` and `prune-learnings` skills as shipped, plugin packaging | DISCARD | Collides with retro on the end-of-task trigger surface (S-16: retro owns it); a bare "remember that I prefer X" would land in project CLAUDE.md instead of memory `feedback`; the Stop-event `additionalContext` output format is unverified | - | none | - | - | out | - |

## Conflicts for the user to rule on

1. **The economy rule's premise.** Global CLAUDE.md: "Keep CLAUDE.md files short; every line
   loads into every session." First-party docs: "use path-scoped rules so instructions load
   only when Claude works with matching files", and rules in `~/.claude/rules/` with a `paths`
   field load only on a matching Read. The premise holds for CLAUDE.md itself and for rules
   without `paths`; it does not hold for the whole instruction surface. Proposal: no wording
   change until the row 1 prototype reports; then, if native-only works, add one sentence to
   the economy section naming `~/.claude/rules/` with `paths:` as the home for rules that only
   matter for certain files. Alternative: try it now by moving one file-type-scoped global
   rule (for example the visualize and dataviz precedence block, which matters only when
   building pages and charts) into `~/.claude/rules/` and watching one week of sessions.
2. **Admission threshold.** Economy rule: "Write a project fact down only once it has cost a
   correction twice." Candidate: record anything "non-obvious", including a first-occurrence
   gotcha. Proposal: keep the incumbent's threshold; a path-scoped rule is cheaper to carry but
   a stale one is still "confidently wrong".

## Corrections at ingest

- "a correction the user has now made more than once" cannot be counted by a stateless model
  across sessions; use retro's recurrence check over earlier `.claude/retros/` files.
- README: "The hook exits quietly if any is missing" is false for `python3` (only `jq` and
  `git` are guarded).
- `plugin.json` pins no minimum host version; the docs tie `paths` fixes to specific releases
  (v2.1.198 symlinked checkouts, v2.1.211 `--setting-sources` behavior).
- 12 em dashes across four files; strip at ingest.

## Flags

- `hooks/learning-check.sh:60` injects: "Before stopping: did this session surface a non-obvious gotcha ... If so, use the record-learning skill to write it to the right scoped rules file. If not, stop [em dash] do not mention this check." An instruction to stay silent about its own invocation. Not installed, not followed.
- `skills/record-learning/SKILL.md:33-35` directs the agent to write into `.claude/rules/<topic>.md` and `CLAUDE.md` or `AGENTS.md`: installing the plugin grants an agent write access to the files that configure future agents, gated only by a prose "show the diff" step.
- No credential request, no network call, no telemetry.

## Rulings log

- 2026-09-21, scout cycle 5 (unattended): all rows `proposed`; rows 1 and conflict 1 queued as Q-2026-09-21-1, rows 2 to 6 as Q-2026-09-21-5, in claude-scout-weekly `STATE.md`. Nothing applied; every target is an incubator skill body, a runbook, or the global CLAUDE.md.
