# Comparing "The Anatomy of Harness Engineering" against the installed skill library

**Candidate:** `/private/tmp/claude-501/-Users-gfm-work/e6fc72e3-271c-4b81-a05f-b12cfd1a5774/scratchpad/pins/articles/google-harness.md` — Google for Developers blog post, Sept 9 2026, Taylor Mullen and Christian Gunderman (`fetched 2026-09-14T23:30:18Z, sha256 6bc1b75293793c3c...`).

**Clean-room review:** `/private/tmp/claude-501/-Users-gfm-work/e6fc72e3-271c-4b81-a05f-b12cfd1a5774/scratchpad/cr/cleanroom-review-google-harness.md`, read in full.

## Spot-checks performed against the raw article

I read the full 219-line article and independently checked these clean-room claims rather than taking them on faith:

- **The internal contradiction (claim 12 vs. 16/19).** Confirmed. The article calls its assertions "fast, deterministic, unit-style checks that run locally" (article, L81) and "Run local behavioral suite in under 5 seconds" (article, L125-127), but its own code example is `agent.chat("What's the weather like in Mountain View, California?")` asserting `SEARCH_WEB in tools` (article, L94-105) — a live model call with live web search — and the article later recommends LLM-as-a-judge and admits "noisy due to nondeterminism of AI models" (article, L121-122). All three passages are real and mutually inconsistent as quoted.
- **The six "techniques worth taking" quotes** — I diffed each against the source lines (article L87, L120, L121, L122, L63-65, L114) and all are verbatim, not paraphrased.
- **"Switches to first person singular once"** — confirmed: two bylined authors (article, L24-28), one first-person "I" at L118 ("I suggest you start small"), rest is "you"/"we".
- **"Evidence: none... every load-bearing claim is asserted"** — confirmed by my own read; no data table, benchmark, or before/after appears anywhere in the article.
- **"Nothing in the article is addressed to an AI agent"** — confirmed; the entire piece is second-person prose to a human developer, with no imperative aimed at a reading agent.

Not independently verified (no web access from here, and the review already flags these as re-verify items): whether `google.antigravity` is a real, current SDK with the exact API shown; whether Terminal-Bench/DeepSWE are still "de facto"; whether `LocalAgentConfig()` runs offline. I'm taking the clean-room review's currency-risk list as-is on these.

## Ancestry

**None.** No merge note, no shared byte sequence, no matching section structure, no CHANGELOG entry linking this article to anything in `~/skill-library`. This is a Google-authored blog post about testing *agentic coding harnesses in general*; the incumbents are Graham's own installed skills for *verifying finished work* (`proof-of-work`, `evidence-report`) and *scaffolding a modeling-project discipline* (`experiment-harness`). Same shape of problem — do not trust an unverified claim of success — reached independently by two unrelated parties. This is the same pattern already logged for the `config-drift-checker` review (`docs/reviews/2026-09-03-config-drift-checker/decisions.md:23`: "Independent invention of adjacent territory; no shared strings, no merge notes"). There is one real thread of continuity worth naming: `decisions.md` row 3 already anticipates almost exactly what this article is about (a "behavioral regression harness for skills and rules... riding on evidence-report conventions"), tabled on 2026-09-03 as future work, not built. So this isn't ancestry between candidate and incumbent — it's the candidate landing on ground the library had already surveyed and shelved.

## Classification of every technique the clean-room review lists as worth taking

The candidate is an article, not a skill collection, so the unit of classification is each of the six items in the review's §3.

### 1. "Assert on intermediate execution steps... instead of final string equality" — REDUNDANT

vs. `plugins/foundry-core/skills/proof-of-work/SKILL.md:47-48`:

> "**Verify at the level the failure lives.** A check that structurally cannot see the defect is not a check, however green it comes back."

and L43-44: "Grep, lint, type-check, and self-review do not count as verification where the failure mode can hide from them. They are pre-filters."

Article's directive (L87): "Behavioral evals assert on intermediate execution steps, like specific tool calls or file modifications, instead of final string equality." Same underlying instinct — check mechanism, not surface text — but `proof-of-work`'s version is broader (any failure-hiding level, not just tool calls) and is backed by three named, dated incidents (`SKILL.md:59-68`) rather than one untested code snippet. Equal or better; nothing to take.

### 2. "Pick one failure mode... make that your target" — COMPLEMENT

Gap: nothing installed converts an observed agent misbehavior into a durable, re-runnable regression check. `prove-hooks.sh` builds fixtures, but only for permission hooks, not general agent behavior. `proof-of-work` verifies one piece of work once; it has no notion of a persisted case library. The natural consumer already exists, tabled: `docs/reviews/2026-09-03-config-drift-checker/decisions.md:35`, row 3 — "Pinned/canary behavioral regression harness for skills and rules... consuming `claude plugin eval` cases... tabled 2026-09-03 (phased-harness when a week is available; not scaffolded yet)."

### 3. "Match assertion strictness to task complexity" (strict single-turn vs. LLM-as-judge for open-ended tasks) — COMPLEMENT

Nothing installed discusses calibrating check strictness to how open-ended a task is. This is real gap-territory, same consumer as #2 (row 3), but needs a correction before it's usable — see "Corrections needed at ingest" below.

### 4. "Gate on pass rates across many runs, not one" — REDUNDANT (as a principle), COMPLEMENT (as infrastructure)

The article's version (L122) has no threshold, no variance handling, no sample-size language — just "tracking aggregate pass rates over time ensures... trending correctly." The library already states a stricter version of the same instinct, in `plugins/workbench/skills/experiment-harness/templates/run.template.md:33-38`:

> "If this run compares two configurations, judge it on paired per-item wins (which config won on each case), not by subtracting two raw rates, and state the sample size or interval the verdict rests on."

That's a superior treatment of "don't trust a noisy aggregate" — it forces a sample size and a per-item comparison instead of a vibe about a trend line. The clean-room review makes the identical criticism of the article independently ("Blind spots in trend tracking... can hide a real regression in one behavior inside a stable average", review §4). The *mechanism* to actually run batches of agent-behavior cases in CI doesn't exist yet — that part is still row 3's gap, not this rule's.

### 5. Example seed behaviors (clarifying question / run validator before done / canonical links) — DISCARD

These are illustrative prompts, not a method. Low value standalone; at most a few seed rows for row 3's eventual case library, not worth carrying forward now.

### 6. Automated prompt tuning (self-tuning loop against the eval suite) — DISCARD

One sentence, no implementation, and it actively conflicts with two installed rules (below). Not worth taking even as an outline; if row 3 is ever built, this shape of loop needs to be explicitly forbidden rather than adopted.

No item earned SUPERIOR SUBSTITUTE — nothing here beats an incumbent's existing treatment, only fills gaps or restates it more weakly.

## Routing collisions

None exist today. The candidate is prose, not an installed skill with a `name`/`description` to route on, so there's nothing to collide against in the sense `docs/inventory.md` tracks. The one latent risk: if row 3 is ever scaffolded as `skill-eval-harness` (`decisions.md:35`, name "TBD at scaffold"), its trigger phrases need to stay clearly separated from `experiment-harness`'s ("track hypotheses for this analysis", modeling/no-terminal-gate projects) — the two are adjacent (both gate on "did you predict/expect this before you looked") but serve different objects: `experiment-harness` is for a person's modeling project, the future row-3 skill would be for testing installed skills/agent behavior. Not a present collision, just a naming trap to watch for at scaffold time.

## Philosophy conflicts

**1. Self-tuning prompt loop vs. the frozen-holdout rule.**

Article (L114): "you can set up a loop where an LLM tweaks its own system prompt, iterating until a failing test finally passes, all while the rest of your test suite acts similar to how a CI/CD-style guardrail operates."

`experiment-harness` template (`templates/CLAUDE.template.md:24-27`): "Do not fit, tune, or adjust anything against the holdout after it is frozen: that defeats the reason it exists." And the doctrine file names the exact failure this guards against (`references/doctrine.md:15`): "rationalizing a result after seeing it."

Optimizing a prompt directly against the same suite that's supposed to gate it is precisely the fitted-to-the-holdout failure the installed harness exists to prevent. The clean-room review reaches the same conclusion from a different angle (§4, "Overfitting" risk) without citing this rule — my addition, not the review's.

**2. Same loop vs. the bounded-loop rule for fix loops.**

Global `~/.claude/CLAUDE.md:103-109`: "Fix loops run under `/goal` with `bounded-loop` when the check must be executed... escalates with a report at the attempt budget (default 3). A fix loop that re-runs the check by hand and eyeballs the result is the unbounded loop this rule exists to prevent."

The article's loop ("iterating until a failing test finally passes") names no attempt budget, no escalation path, and no stopping condition beyond "until it passes" — exactly the unbounded shape this rule was written to forbid.

## Corrections needed at ingest

- **Internal factual contradiction, verified above**: "fast, deterministic... under 5 seconds" is false of the article's own example, which calls a live model over the network. Any fragment taken forward (items 2-4) must drop this framing rather than propagate it.
- **One-sided assertion, no negative control.** The article's only code example asserts a tool call happened; it never demonstrates the check would fail if it didn't. `scripts/prove-hooks.sh:8-9` requires both: "a POSITIVE control (the payload the hook exists to refuse... must answer with a deny or block) and a NEGATIVE control (a payload it must let through...). Both verdicts are asserted." Any port of item 2 or 3 into row 3's future case format must require a negative control per case, not just a positive one.
- **LLM-as-judge needs independent validation before it counts as evidence.** `proof-of-work` treats self-review with structural suspicion ("self-review do not count as verification where the failure mode can hide from them", `SKILL.md:43-44`). Item 3's judge must be checked against human labels before it's trusted — the article never says this; the clean-room review flags it as a risk (§4, "An unvalidated judge") but it needs to be a stated requirement, not a caveat, if this fragment is ever ingested.
- **"Budget exhausted"/noisy-run handling must render as a distinct non-green state**, not silently absorbed into a trend line — this is already a ratified rule for the adjacent tabled harness (`decisions.md:44`: "any port renders cap-hit as a distinct non-green state"), and item 4's "trending correctly" language needs the same discipline if it ever feeds row 3.
- **A stateless model cannot honor "ensures the model's behavior is trending correctly"** as written — there's no threshold a model could check against. Any ingested version needs a concrete number (sample size, delta threshold) per `run.template.md`'s existing rule.
- No em-dash or other style violations found in the article body on my read; nothing to restyle there.

## Net assessment

If only three things could be taken, none of them is the whole article — every technique in it is either already covered as well or better, or a bare gap-filler for work that's explicitly tabled. In order:

1. **Item 2 + item 3 (failure-seeded tests; strictness matched to task complexity), as fragments** — not a whole item, since neither has an implementation. Target: append as sourced input to a decision row for this candidate in a new `docs/reviews/<date>-google-harness-engineering/decisions.md`, explicitly riding on `decisions.md` row 3 the same way rows 4-5 already ride on it for the `config-drift-checker` review. They should not move further than that until row 3 itself is unshelved — a fragment feeding a tabled item is not itself worth building standalone.
2. **The two conflict corrections (frozen-holdout / bounded-loop) as standing constraints on whatever row 3 becomes**, so the eventual `skill-eval-harness` design doesn't reinvent the self-tuning-loop mistake. Target: the same new decisions doc, under a "Conflicts for the user to rule on" section (mirroring `decisions.md:39-44`'s existing format), for Graham to ratify before row 3 is ever scaffolded.
3. **Nothing else.** Item 1 is redundant against `proof-of-work`, item 4's principle is redundant against `experiment-harness`'s run template, items 5-6 are discard. There is no case here for a `phased-harness` or immediate `/goal` run — this candidate produces exactly two paragraphs' worth of durable value, both of which are notes for later, not code to write today.
