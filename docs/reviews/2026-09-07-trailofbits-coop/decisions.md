# Decisions: trailofbits-coop

contract: v1
source: https://github.com/trailofbits/coop
type: code-repo
pin: cbfe0273ac68585f381bcd9edf22384cac2cefce (cloned 2026-09-08T00:24:38Z, depth 1)
reviewed: 2026-09-07
verdict: HARVEST
recheck: n/a
evidence: docs/reviews/2026-09-07-trailofbits-coop/cleanroom-review.md, docs/reviews/2026-09-07-trailofbits-coop/comparison.md

## Verdict reasoning

The tool itself is an install (a VM runtime, a guest image, host processes holding live API
keys, about 216 crates), so adopting it is Tier 3 whatever the review says; it is also the
first concrete candidate for the OS-sandbox alternative that Q-2026-09-03-4 left as "a later
decision", and the review found nothing that rules it out (Apache-2.0, CI with cargo-deny and
SHA-pinned actions, a credential proxy that is default-deny by operation, clean removal).
The rows are the deliverable today: two sentences for the hooks runbook, one for the
authoring standard, a pointer for the Q-4 row. What would change the verdict to ADOPT:
Graham naming a week for the sandbox decision, and the VM integration suite running in CI.

## Ancestry

none. Grepped the tree for skill-library, GFMCloud, scout-weekly, improvements-weekly:
zero matches. One independent convergence: coop's `.claude/skills/closeout-review/SKILL.md`
is a pointer shim to a single shared skill, the same one-editable-home convention as the
global working agreements.

## Rows

Legend for Ruling: `proposed` | `ratified` | `overridden: <text>` | `out`.
Effort: `S` under an hour | `M` an afternoon, one PR | `L` multi-session (phased-harness).
Adoption cost is mandatory and never "none".

| # | Item | Class | Proposal | Source (path, lines) | Target (one library file) | Effort | Adoption cost | Ruling | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | coop as the OS sandbox for the two unattended weekly maintainers (Lima microVM on macOS; agent runs inside with full tools; host API key never enters the guest) | COMPLEMENT (the Q-2026-09-03-4 alternative, now with a candidate) | Evaluate in a phased-harness when Graham names a week: run one scheduled cycle inside `coop claude` from a clone of the harness, compare the run log to a host run, decide. Not an install by this run | `README.md`, `docs/trust-model.md`, `coop-proxy/src/proxy.rs:243-262` | new phased-harness project (decision record in `claude-scout-weekly/docs/`) | L | Lima plus Virtualization.framework, a built guest image, a long-lived host proxy per VM holding a live credential, writes to `~/.ssh/config`, a self-updating binary that degrades to checksum-only without `gh`; removal is `coop uninstall --purge` and `coop destroy --all` | proposed | Graham |
| 2 | Tiered enforcement that reports which tier held (`apply() -> bool`, warn vs info) | COMPLEMENT | Attach the pin as a worked example to the Q-2026-09-03-4 row so the sandbox decision starts from it | `coop-proxy/src/jail.rs:120-202` | `claude-scout-weekly/STATE.md`, Q-2026-09-03-4 status cell (Tier 1: this project's state) | S | one pointer to keep current if the pin moves | applied 2026-09-07 (STATE.md) | scout |
| 3 | Fail-open process gates, stated as a principle: a gate that cannot positively identify its target case allows, so it never wedges unrelated work | INGESTIBLE FRAGMENT | One sentence in the hooks-and-permissions runbook Step 1 rationale | `.claude/hooks/closeout-review-gate.sh:17-18` | `claude-scout-weekly/docs/runbooks/2026-09-03-hooks-and-permissions.md` | S | none beyond one line; the runbook is a ruled document, so the edit rides Q-2026-09-07-3 | proposed (with Q-2026-09-07-3) | Graham |
| 4 | Allow-list by operation versus deny-list by pattern: the runbook's destructive-command hook chose deny-list without saying why an allow-list was not viable (arbitrary shell cannot be enumerated; a fixed API surface can) | INGESTIBLE FRAGMENT (philosophy note) | One sentence in the same runbook Step 1 acknowledging the choice | `coop-proxy/src/proxy.rs:243-248` | same runbook | S | none beyond one line | proposed (with Q-2026-09-07-3) | Graham |
| 5 | Limitations stated at the same altitude as the design: a module or skill that enforces something lists its known weaknesses next to its rationale, not in an appendix | INGESTIBLE FRAGMENT | One bullet in the authoring standard's Body section, beside the heuristic-ceiling bullet landed 2026-09-07 | `coop-proxy/src/jail.rs:41` | `~/skill-library/docs/authoring-standard.md` | S | none beyond one bullet | proposed | Graham |
| 6 | A per-project trust model with a merge-blocking stop-and-confirm checklist anchored to exact code idioms | SUPERIOR SUBSTITUTE (as a pattern for security-sensitive projects; the global escalation list stays abstract) | Guidance in phased-harness for projects that touch credentials, network, or production: scaffold a trust-model doc with concrete triggers | `docs/trust-model.md:340-354` | `plugins/workbench/skills/phased-harness/` references | M | a template to maintain; only projects that opt in pay | proposed | Graham |
| 7 | Test that the sandbox self-test can fail (`probe_fails_when_unconfined`) | REDUNDANT | Already the global rule ("proven by deliberate failure") and now `scripts/prove-hooks.sh` | `coop-proxy/src/jail.rs:280-286` | none | n/a | n/a | out | scout |
| 8 | Self-restrict after startup rather than before exec; concurrency permit attached to the response body | DISCARD (reference only, no consumer) | Read when row 1 is built; nothing to land | `coop-proxy/src/jail.rs:30-34`, `proxy.rs:59-88` | none | n/a | n/a | out | scout |

## Conflicts for the user to rule on

- Allow-list versus deny-list (row 4): coop's proxy is default-deny by operation; the
  runbook's destructive-command hook is default-allow with a deny pattern list, justified as
  "a wrong pattern blocks real work until edited; that is the accepted cost". Different
  domains (fixed HTTP surface versus arbitrary shell), so no reversal is proposed; the
  runbook should say the alternative was considered. Alternative: leave the runbook silent.

## Corrections at ingest

- Em dashes in coop's module docs and trust model; restyle any quoted sentence.
- The escalation-trigger list in the global CLAUDE.md is restated in project files; row 6
  must not touch it, only add project-level guidance.
- The clean-room review labels one quote `CLAUDE.md:1-5`; the line is `CLAUDE.md` line 1.

## Flags

Disclosed, not injection: `AGENTS.md` and `CLAUDE.md` are project instructions for agents
working on coop; `.claude/settings.json` pre-approves about 80 Bash patterns and registers
three hooks that run repo-authored shell (`no-pipe-test-output.sh`, `closeout-review-gate.sh`
on PreToolUse Bash; `cargo-fmt.sh` on Write and Edit). Anyone opening this clone as a
Claude Code working directory runs that shell on their tool calls. Not acted on; the clone
was read from outside with `--restricted`.

## Rulings log

2026-09-07: proposed by the scout cycle (cycle 2). Row 2 applied as a Tier 1 STATE.md
annotation. Rows 3 and 4 ride Q-2026-09-07-3 (the runbook amendment already queued). Rows
1, 5, 6 await `/phase ratify`.
