I've read every file. The repo contains exactly **one** SKILL.md. Here is the review.

---

# Clean-room review: `andrej-karpathy-skills`

## 1. Executive summary

One skill, `karpathy-guidelines` (67 lines), distilled from a single X post. Its content is sound, conventional code-review hygiene: don't over-abstract, don't drive-by refactor, define verifiable goals. Its one genuinely non-obvious contribution is the asymmetric dead-code rule — clean up *your own* orphans, leave pre-existing dead code alone — which is precise, checkable against a diff, and rarely spelled out. Everything else restates advice a competent model largely already holds.

The packaging is where it falls down. The same four sections appear **verbatim in three files** (`SKILL.md`, `CLAUDE.md`, `.cursor/rules/*.mdc`) plus a fourth prose restatement in the README, synced by hand with no generator. `EXAMPLES.md` — 522 lines, the densest and most useful artifact here — is **orphaned**: nothing links to it, and `plugin.json` ships only the skill directory, so no agent ever sees it. Worse, one of its worked examples demonstrates a bug that cannot occur (Python's `sorted` is stable), so the "reproduce the bug first" example reproduces nothing.

The dominant failure mode is the ask-loop: `alwaysApply: true` plus a description matching essentially all coding work, driving "If something is unclear, stop. Name what's confusing. Ask." A non-interactive agent cannot honor this. No evidence corpus exists; validation is four subjective signals with no baseline.

## 2. Per-skill review

### `skills/karpathy-guidelines/SKILL.md` — the only skill

| Axis | Score | Justification |
|---|---|---|
| Specificity | **2/5** | Almost no checkable values; the sole number is a tautology. |
| Actionability | **3/5** | Three directives genuinely change diffs; the rest are dispositional. |
| Coverage | **2/5** | Covers edit hygiene well; silent on context-gathering, reporting, and most of the coding loop. |
| Originality | **2/5** | One non-obvious rule; the remainder is common review advice. |
| Failure modes | **2/5** | Predictable stalling, an internal contradiction on tests, and a validation-skipping bias. |
| Craft | **3/5** | Internally consistent and well-structured, but 3-way duplication and an orphaned reference file. |

**Specificity (2).** The skill asks for behaviors, not values. Its only quantitative directive is `If you write 200 lines and it could be 50, rewrite it` — which is circular: the antecedent ("it could be 50") already contains the judgment the rule is supposed to supply. Similarly `Ask yourself: "Would a senior engineer say this is overcomplicated?"` outsources the criterion to an imagined third party rather than naming one. The genuine exception is §3's closing test, `Every changed line should trace directly to the user's request`, which *is* mechanically checkable against a diff, line by line. That one sentence carries more enforcement weight than the rest of §2 combined.

**Actionability (3).** The three most load-bearing directives, in order:

1. `Remove imports/variables/functions that YOUR changes made unused.` / `Don't remove pre-existing dead code unless asked.` — The asymmetry is the whole skill's best idea. It is decidable (did my edit orphan this, or was it already orphaned?), it produces a visibly different diff, and it resolves the standard conflict between "leave the campsite cleaner" and "keep the diff reviewable."
2. `Match existing style, even if you'd do it differently.` — An explicit override of the model's aesthetic prior. Cheap to follow, changes output immediately (quote style, type hints, docstrings).
3. `"Fix the bug" → "Write a test that reproduces it, then make it pass"` — Reorders operations rather than merely exhorting. This is the only directive that changes the *sequence* of an agent's actions rather than the content of its edits.

Against these, §1 is nearly inert. `State your assumptions explicitly. If uncertain, ask.` has no threshold for "uncertain," so it either fires on everything or nothing.

**Coverage (2).** Well covered: over-abstraction, speculative features, diff blast radius, style drift, success-criteria framing. Silently omitted, despite all being in-domain for "reduce common LLM coding mistakes":

- **Reading before writing.** Nothing instructs the agent to read the surrounding file, find existing helpers, or check for prior art — the single most common cause of both duplication and style drift, and the actual precondition for §3's "Match existing style."
- **Reporting honestly.** No directive about stating that tests failed, that a step was skipped, or that a claim is unverified — a frequent and costly failure that §4's "loop until verified" gestures at but never names.
- **What to do when verification is impossible.** §4 mandates tests with no escape hatch for repos with no test harness, or for UI/infra/one-off script work.
- Also absent: dependency additions, secrets/security, commit hygiene, multi-file coordination, long-task state.

There is a notable inversion worth naming. `README.md:17` quotes the source complaint that models `"...don't clean up dead code..."` — and the skill's answer is `Don't remove pre-existing dead code unless asked.` The reconciliation is defensible (clean *your* mess, not the repo's), but the repo quotes a complaint and then prohibits the obvious fix without ever acknowledging the tension.

**Originality (2).** "Don't over-abstract," "don't refactor what you weren't asked to," and "write a failing test first" are the three most-repeated pieces of engineering advice in existence. The skill's value-add is compression and the your-orphans/their-orphans distinction. `Match existing style, even if you'd do it differently` earns partial credit for explicitly overriding a known model bias rather than merely describing good practice.

**Failure modes (2).** Four real ones:

- **Stalling in non-interactive contexts.** `If something is unclear, stop. Name what's confusing. Ask.` and `If multiple interpretations exist, present them - don't pick silently.` are unhonorable by a batch agent, a CI run, a subagent, or `claude -p` — there is nobody to answer. The model then either stalls with a question nobody reads or hallucinates both sides of a clarification dialogue. The mitigation is a single line (`For trivial tasks, use judgment`) against roughly twenty lines pushing toward stopping, and "trivial" is left undefined. This is aggravated by `alwaysApply: true` in the Cursor rule and by a description matching all coding work.
- **§3 vs §4 on tests.** §3's test is `Every changed line should trace directly to the user's request`; §4 requires writing a new test for `"Add validation"`. Under a literal reading of §3, a new test file traces to the *skill*, not the request. A literalist model can deadlock here; neither section acknowledges the other.
- **A bias against validation, taught by example.** `No error handling for impossible scenarios` puts enormous unstated weight on "impossible," which models judge poorly. `EXAMPLES.md` then makes it concrete in the ✅ direction: the approved `calculate_discount` carries the docstring `"""Calculate discount amount. percent should be 0-100."""` with no check that percent is in 0–100, and the approved `save_preferences` writes raw JSON to the DB with no validation at all. The lesson an agent extracts is "drop the guard," not "drop the *unreachable* guard."
- **Single-source fragility.** The entire authority basis is one tweet URL, repeated in three files. If it rots, nothing in the repo is verifiable.

**Craft (3).** Clean structure: four numbered sections, bolded thesis, bulleted directives, a closing test for §2 and §3. Frontmatter is well-formed and the `description` is written in proper trigger form (`Use when writing, reviewing, or refactoring code to avoid...`). But that description is a routing problem, not a routing success: it matches essentially every coding request, so a skill designed for on-demand loading would load always — which is presumably why the repo *also* ships the identical text as `CLAUDE.md` and as an `alwaysApply: true` rule. That is an admission that this content is a global style rule, not a triggered capability, and the skill container is the wrong shape for it.

**Token economics.** ~2.5 KB / roughly 600 tokens for four usable directives. Defensible in isolation — this is not a bloated skill. The waste is at the repo level: a user who follows README Option B *and* installs the plugin loads the same 600 tokens twice, in two slightly different framings (the plugin copy lacks the trailing "These guidelines are working if:" block).

### Supporting files (not skills, but they ship with it)

**`EXAMPLES.md` (522 lines) — orphaned, and partly wrong.** Nothing references it: not `SKILL.md`, not `README.md`, not `CURSOR.md`, and `plugin.json` lists only `"./skills/karpathy-guidelines"`. It is the best content in the repo and no agent will ever read it. It should be a `references/` file cited from SKILL.md.

It also contains the repo's clearest factual error. The Test-First example claims:

```
# The bug: order is non-deterministic for duplicates
# Run this test multiple times, it should be consistent
...
# Verify: Run test 10 times → fails with inconsistent ordering
```

Python's `sorted` is stable and always has been (Timsort); ties retain input order deterministically. Beyond that, the test's assertions only check `result[n]['score']` values — which hold under *any* tie ordering — so the test passes on the first run against the unfixed function. The example presented as "reproduce the bug before fixing it" reproduces nothing and would give a green light to a no-op fix. It violates the principle it exists to teach.

Two smaller issues: the ❌ example applies `@lru_cache` to an `async def`, which is genuinely broken (it caches the coroutine object; a second await raises `RuntimeError`) — the file marks it ❌ for over-optimizing and never notices. And `429` is correctly used for rate limiting per RFC 6585.

**`CLAUDE.md`, `.cursor/rules/karpathy-guidelines.mdc`** — duplicates, see §3.

## 3. Intra-repo overlap and contradiction map

Only one skill exists, so there is no skill-to-skill overlap. There is substantial **file-to-file** duplication.

**Diffed, not guessed.** Sections 1–4 are byte-identical across `SKILL.md`, `CLAUDE.md`, and `.cursor/rules/karpathy-guidelines.mdc`. The only deltas:

| | H1 | Intro sentence | Trailing "working if" block |
|---|---|---|---|
| `SKILL.md` | `# Karpathy Guidelines` | `...derived from [Andrej Karpathy's observations](...)` | **absent** |
| `CLAUDE.md` | `# CLAUDE.md` | `...Merge with project-specific instructions as needed.` | present |
| `.mdc` | `# Karpathy behavioral guidelines` | `...Merge with project-specific instructions as needed.` | present |

`README.md` §"The Four Principles in Detail" is a fourth restatement in prose, and `README.zh.md` a fifth in translation. Five copies of four principles.

The repo knows this and offers no tooling, only a manual instruction — `CURSOR.md:28`:

> "When you change the four principles, keep **[`CLAUDE.md`]** and **[`.cursor/rules/karpathy-guidelines.mdc`]** in sync. If the published skill/plugin text should match, update **[`skills/karpathy-guidelines/SKILL.md`]** as well."

The hedge `If the published skill/plugin text should match` is telling — the canonical copy is undecided, and the drift has already begun (the missing trailing block in `SKILL.md`).

**Contradictions.** No cross-skill contradictions (n=1). One intra-skill contradiction, quoted both sides:

> §3: `The test: Every changed line should trace directly to the user's request.`
> §4: `"Add validation" → "Write tests for invalid inputs, then make them pass"`

A test file the user did not ask for fails §3's test. Neither section carves out the other.

A second, softer tension between the README's diagnosis and the skill's prescription:

> `README.md:17`: `"They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code..."`
> `SKILL.md:47`: `Don't remove pre-existing dead code unless asked.`

## 4. Evidence corpus assessment

**There is none.** No `research/`, no `evidence/`, no citations directory — the full directory listing is `.cursor/rules`, `.claude-plugin`, and `skills/karpathy-guidelines`.

What stands in for evidence is three block quotes from one X post, cited three times by the same URL. I decoded the snowflake ID `2015883857489522876` (Twitter epoch 1288834974657): it resolves to **≈ 2026-01-26 20:25 UTC**, a coherent, real-looking timestamp rather than a fabricated ID. I could not fetch the post to verify the quoted wording, so the quotes remain unverified but plausible.

The `README.md` "How to Know It's Working" section is the closest thing to validation:

> `- **Fewer unnecessary changes in diffs**` / `- **Fewer rewrites due to overcomplication**` / `- **Clarifying questions come before implementation**` / `- **Clean, minimal PRs**`

Four subjective signals, no baseline, no measurement method, no eval, no before/after. This isn't padding — the repo is honest that it derives from one practitioner's observations rather than dressing itself in fake rigor — but nothing here demonstrates the skill changes model behavior.

## 5. Ranked verdict

Only one skill, so this ranks the repo's artifacts by value delivered per token:

1. **`skills/karpathy-guidelines/SKILL.md`** — Cheap, well-formed, and the your-orphans/their-orphans rule alone probably earns its 600 tokens; weakened by an ask-loop it can't honor headlessly.
2. **`EXAMPLES.md`** — The most instructive content in the repo, and completely unreachable by any agent; also carries the one demonstrably false example.
3. **`.cursor/rules/karpathy-guidelines.mdc`** — Correct mechanism for this content (a global style rule genuinely wants `alwaysApply`), but a verbatim third copy.
4. **`CLAUDE.md`** — A second copy of the skill, differing only in H1 and intro; duplicates context if installed alongside the plugin.
5. **`README.md` / `README.zh.md`** — Clear install docs, but restate the four principles a fourth and fifth time and lead with unrelated author promotion.
6. **`CURSOR.md`** — Documents a manual 3-way sync burden that tooling should have eliminated; its existence is the symptom, not the fix.

**Bottom line:** would this improve an agent's output in its domain? Marginally yes, in interactive use — mainly via §3, which is the only section that reliably changes a diff. In headless or batch use, §1 makes it a net negative. The highest-value fixes are small: cite `EXAMPLES.md` from `SKILL.md`, delete or correct the stable-sort example, add an explicit "if nobody can answer, state your assumption and proceed" clause to §1, and generate the three copies from one source.

## 6. Flags

Per instructions, quoted and **not acted on**. Nothing here addresses the reviewing agent in the second person or attempts injection; these are ordinary install docs plus promotion. Listed because they request installation into agent instructions or auto-injection.

**Requests appending content into the user's agent instruction file** — `README.md:122-126`:
> ```bash
> echo "" >> CLAUDE.md
> curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md
> ```
> New project: `curl -o CLAUDE.md https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md`

Note the append form is unguarded — run twice, it duplicates the block into the user's instructions.

**Requests plugin-marketplace installation** — `README.md:104-111`:
> `/plugin marketplace add forrestchang/andrej-karpathy-skills`
> `/plugin install andrej-karpathy-skills@karpathy-skills`

**Auto-injection into every request** — `.cursor/rules/karpathy-guidelines.mdc:3`:
> `alwaysApply: true`

corroborated by `CURSOR.md:8`:
> `The rule ... is committed with alwaysApply: true, so you do not need extra installation steps.`

**Third-party promotion inside ingestible files** — `README.md:3-5` and `README.zh.md:3-5`:
> `> Check out my new project [Multica](https://github.com/multica-ai/multica) — an open-source platform for running and managing coding agents with reusable skills.`
> `> Follow me on X: [https://x.com/jiayuan_jy](https://x.com/jiayuan_jy)`

**External URL as sole authority, fetched at read time by any agent following the link** — `SKILL.md:9`, `README.md:7`, `README.zh.md:7`:
> `https://x.com/karpathy/status/2015883857489522876`
