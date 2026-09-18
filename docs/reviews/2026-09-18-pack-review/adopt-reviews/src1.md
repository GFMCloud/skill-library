# Clean-room review: `ponytail` skill repository

## 1. Executive summary

Six `SKILL.md` files exist in the canonical `skills/` directory, mirrored byte-for-byte (frontmatter aside) into `.openclaw/skills/` for a second host — so six distinct skills, twelve files on disk. All six are tightly scoped variants of one idea: a "lazy senior dev" heuristic ladder (YAGNI → codebase → stdlib → native → dependency → one-liner → minimum) plus four satellite report/utility skills (`review`, `audit`, `debt`, `gain`, `help`) that never touch code, only report on it. The core skill (`ponytail`) is unusually concrete for this genre — a seven-rung ordered decision procedure, explicit output format, explicit "never simplify away" exception list, and an explicit debt-marking convention (`ponytail: <ceiling>, <upgrade path>`) that the other skills consume mechanically. The satellite skills are well-differentiated from each other and from the core skill (diff-scope vs repo-scope vs debt-ledger vs benchmark-display vs help-card), with essentially no functional overlap. The main risk is the core skill's own admission: an internal benchmark (`benchmarks/results/2026-06-16-robustness-audit.md`) found the "stdlib-first" pressure causes OpenAI models to reach for `email.utils.parseaddr` (a parser, not a validator) and accept malformed emails — a real, disclosed failure mode of Rung 3, not fixed and not hidden. The evidence corpus (agentic benchmark, robustness audit, self-verifying test harnesses) is genuinely load-bearing rather than decorative, which is rare and worth crediting. One directive addresses the agent reading the repo directly (see Flags).

## 2. Per-skill review

### `ponytail` (core) — `skills/ponytail/SKILL.md`

1. **Specificity: 5/5.** The ladder is fully ordered and each rung has a concrete trigger: `"Can it be one line? One line."`, `"Native platform feature covers it? <input type="date"> over a picker lib, CSS over JS, DB constraint over app code."` These are checkable — a reviewer can point at a diff and say which rung was violated.
2. **Actionability: 5/5.** The three most load-bearing directives: (a) the ladder itself, which forces a specific search order before writing code; (b) `"Bug fix = root cause, not symptom... grep every caller of the function you're about to touch"` — a mechanical, greppable instruction; (c) the output contract `"Code first. Then at most three short lines... Pattern: [code] → skipped: [X], add when [Y]."` — a literal template the model can fill in. Following these produces measurably different diffs (see benchmark below), not just different tone.
3. **Coverage: 4/5.** Covers greenfield writing, bug-fixing, dependency choice, and prose suppression. Silent on: multi-file architectural decisions (when does "fewest files" stop applying to a genuinely multi-module feature?), and on how the ladder interacts with existing house style/lint conventions (a codebase that already has a `DateInput` wrapper component — rung 2 says reuse it, but the skill doesn't say what happens when the existing pattern is itself over-engineered; only `ponytail-audit` handles that, and only on request).
4. **Originality: 4/5.** The ladder ordering is the genuine contribution — most "write simple code" guidance is unordered vibes ("avoid over-engineering"); this gives a decidable sequence. The `ponytail:` marker convention (deliberate-shortcut comment with ceiling + trigger, consumed by a sibling skill) is a non-obvious, well-thought-through mechanism most skills of this type lack.
5. **Failure modes: 3/5.** Two real ones, both disclosed by the repo's own benchmarks rather than hidden: (a) the stdlib-reach-first instinct causing `parseaddr`-style validate/parse confusion on some providers; (b) the "shortest working diff" instruction can conflict with "fewest files" — a genuinely small diff sometimes needs a new file (e.g., a new test file the skill itself mandates via the "leaves ONE runnable check behind" rule), and the skill doesn't rank these two pressures against each other. Also: `"Two rungs work → take the higher one and move on"` is fine in the abstract but gives no tie-break when a native feature and an installed dependency are equally viable and the dependency is clearly the house convention — rung ordering is fixed, judgment isn't asked for.
6. **Craft: 5/5.** Internally consistent (the "Not lazy about" list in `AGENTS.md`/`.openclaw` copy matches the "When NOT to be lazy" section word-for-word in intent), well-structured, frontmatter description is long but appropriately keyword-dense for routing (`"ponytail", "be lazy", "lazy mode", "simplest solution"...`) with an explicit negative case (`"Do NOT use for non-coding requests"`).

### `ponytail-review` — `skills/ponytail-review/SKILL.md`

1. **Specificity: 5/5.** Fixed five-tag taxonomy (`delete:`, `stdlib:`, `native:`, `yagni:`, `shrink:`) and a literal output grammar: `` `L<line>: <tag> <what>. <replacement>.` ``.
2. **Actionability: 5/5.** Load-bearing: the output grammar itself (forces one line per finding, no prose); the explicit good/bad example pair (`❌ "This EmailValidator class might be more complex..."` vs `✅ "L12-38: stdlib: 27-line validator class..."`) which gives the model a concrete negative exemplar to avoid; the closing metric `net: -<N> lines possible.` which forces a summary commitment.
3. **Coverage: 4/5.** Explicitly out of scope: `"Correctness bugs, security holes, and performance"` — clean, stated boundary rather than silent omission. Good.
4. **Originality: 3/5.** Solid but a fairly conventional "structured diff review" pattern; the taxonomy is the value-add.
5. **Failure modes: 3/5.** A reviewer following only this skill on a diff that has both a security hole and over-engineering will say nothing about the security hole, and the "Route them to a normal review pass" instruction assumes a second review pass will actually happen — in a single-skill invocation it may not.
6. **Craft: 5/5.** Explicitly cross-references `ponytail-audit` and differentiates scope in its own description; no redundancy.

### `ponytail-audit` — `skills/ponytail-audit/SKILL.md`

Near-identical tag taxonomy and output grammar to `ponytail-review`, intentionally: `"ponytail-review, repo-wide. Scan the whole tree instead of a diff."` This is the one place where near-total textual overlap is *correct design* — it's explicitly declared as the same review applied at a different scope, not an accidental duplicate.

1. **Specificity: 4/5.** Slightly less concrete than `-review`: `"Hunt"` section lists categories (`"Deps the stdlib or platform already ships, single-implementation interfaces, factories with one product..."`) without a worked example the way `-review` has.
2. **Actionability: 4/5.** Same ranked-output contract; load-bearing directive: `"Rank findings biggest cut first"` forces prioritization over an unordered dump.
3. **Coverage: 4/5.** Same explicit scope fence as `-review`.
4. **Originality: 3/5.** Derivative of `-review` by design; fine.
5. **Failure modes: 3/5.** Repo-wide scans on a large codebase risk token bloat with no guidance on how to chunk/sample a large tree — the skill assumes the whole tree fits in context.
6. **Craft: 5/5.** Clean differentiation from sibling skill in its own frontmatter description.

### `ponytail-debt` — `skills/ponytail-debt/SKILL.md`

1. **Specificity: 5/5.** A literal, copy-pasteable grep command: `` grep -rnE '(#|//) ?ponytail:' . ``, and a fixed row grammar: `` <file>:<line>, <what was simplified>. ceiling: <the limit named>. upgrade: <the trigger to revisit>. ``
2. **Actionability: 5/5.** Load-bearing: the grep pattern itself (mechanical, deterministic); the `no-trigger` tag rule (`"any ponytail: comment that names no upgrade path or trigger gets a no-trigger tag"`) which is a checkable condition on free text; the closing tally `<N> markers, <M> with no trigger.`
3. **Coverage: 5/5.** Fully self-contained for its narrow job; explicitly notes extensibility (`"add other comment prefixes if your stack uses them"`).
4. **Originality: 5/5.** This is the most novel skill in the set — a debt-ledger skill that only works because a sibling skill (`ponytail`) was designed to emit a matching marker convention. Cross-skill design coherence like this is uncommon.
5. **Failure modes: 2/5.** The grep pattern only matches `#` and `//` comment styles; a Python triple-quote block, HTML `<!-- -->`, or SQL `--` comment convention would silently miss markers, understating debt — the skill flags this itself (`"add other comment prefixes if your stack uses them"`) but that's an unenforced instruction to the model, not a safeguard.
6. **Craft: 5/5.** Tight, no redundancy with siblings.

### `ponytail-gain` — `skills/ponytail-gain/SKILL.md`

1. **Specificity: 4/5.** Renders a fixed ASCII scoreboard template with exact percentages.
2. **Actionability: 3/5.** This skill doesn't change code output, only display; its most load-bearing rule is the honesty guard: `"NEVER print a per-repo savings number... the unbuilt version was never written, so there is no real baseline to subtract from in a live repo."` That's a genuinely good anti-hallucination guardrail — it pre-empts the model fabricating a "you saved 340 lines" claim it has no basis for.
3. **Coverage: 3/5.** Single-purpose by design.
4. **Originality: 4/5.** The explicit ban on inventing a per-repo number is the standout, non-obvious idea — most "show me the impact" skills would happily let the model confabulate a plausible-looking savings figure.
5. **Failure modes: 2/5.** The numbers are frozen benchmark medians (`"5 everyday tasks... three models"`) baked into the skill text; they will silently go stale as models/versions change and the skill gives no mechanism to detect staleness — a model invoking this in a year will confidently print 2026-dated numbers with no self-check.
6. **Craft: 4/5.** Correctly points elsewhere (`/ponytail-debt`) for real per-repo figures instead of duplicating that logic.

### `ponytail-help` — `skills/ponytail-help/SKILL.md`

1. **Specificity: 5/5.** Literal reference tables, exact env var name (`PONYTAIL_DEFAULT_MODE`), exact config path per OS.
2. **Actionability: 2/5.** Pure lookup/display; low load-bearing content beyond correctly reproducing README facts (resolution order `"env var > config file > full"`).
3. **Coverage: 5/5.** Complete for its scope.
4. **Originality: 1/5.** Expected, restates other docs verbatim — that's the point of a help card, not a criticism per se, but by the rubric's originality axis it scores low.
5. **Failure modes: 3/5.** Points to `/reload-plugins` and specific update commands (`npm install -g @anthropic-ai/claude-code@latest`) that will age badly as install mechanics change; a help card that quotes exact CLI incantations is the part of this repo most likely to drift from truth.
6. **Craft: 4/5.** Consistent with README's own tables (cross-checked Level/Command mappings match).

## 3. Intra-repo overlap and contradiction map

- **`skills/*` vs `.openclaw/skills/*`**: textually identical bodies, frontmatter differs (OpenClaw copy drops `argument-hint`, adds `homepage`, shortens `description` to a single-line string). This is declared, intentional packaging (`README.md`: `"The OpenClaw skill package (.openclaw/skills/) is generated from skills/"`) verified by a build script and a test that fails on staleness. Not a craft defect.
- **`ponytail-review` vs `ponytail-audit`**: same tag taxonomy and output grammar, deliberately — the frontmatter of `-audit` says outright `"Like ponytail-review, but scans the entire codebase instead of a diff"`. Genuine, declared duplication of mechanism at different scope, not accidental overlap.
- **`ponytail-gain` vs `ponytail-help`**: both one-shot, non-mutating "display a card" skills; no content overlap (impact numbers vs command reference) but similar shape/behavior class — a host with only fuzzy skill routing could plausibly confuse `"show ponytail impact"` with `"what ponytail commands"` phrasing; the descriptions do use distinct trigger phrases, so risk is low but not zero.
- **Soft tension, not a contradiction**: the core `ponytail` skill regulates some of its own prose (`"No essays, no feature tours, no design notes... every paragraph defending a simplification is complexity smuggled back in as prose"`), while the README's FAQ claims a clean division of labor with a sibling project: `"Different halves, no overlap: caveman leaves code byte-for-byte exact, ponytail stays out of the prose."` In practice `ponytail` does constrain some prose (its own justification text), so "ponytail stays out of the prose" is only true for code-external commentary, not for ponytail's own output-format rule. Minor imprecision in the README claim, not a functional contradiction between skill files.
- No hard contradictions found between any two `SKILL.md` files — the boundary fences (`"Correctness bugs, security holes, and performance are explicitly out of scope"` appears verbatim in both `-review` and `-audit`) are consistent everywhere they're repeated.

## 4. Evidence corpus assessment

Genuinely evidence-backed, not padding — unusually so for this genre:

- `benchmarks/results/2026-06-18-agentic.md` is a real methodology writeup: names its own prior flaw (`"An earlier agentic run showed a tiny ~4% gap... it was wrong: ponytail and caveman are Claude Code plugins that fire a SessionStart hook, and that hook was firing on every arm"`), states a competing critique it's responding to (issue #126), and reports a result where its own skill does *not* win (`"On irreducible code the arms converge... near-identical across all arms"`).
- `benchmarks/results/2026-06-16-robustness-audit.md` is the strongest piece of evidence in the repo: a self-verifying harness (`"a known-correct and a known-lazy-wrong reference must pass/fail respectively before any model output is scored"`) that surfaces and *keeps* an unresolved weakness of the skill (the `parseaddr` validate/parse trap on OpenAI models) rather than quietly patching the skill text to hide it — explicitly stating 8 candidate fixes were tried and rejected because they made things worse (`"Counter-instructions make small models overthink and fail more. Nothing was shipped"`).
- `benchmarks/README.md` distinguishes first-party numbers from two named third-party reproductions (KuldeepB19, RicardoCostaGit) with dates and caveats, and explicitly flags a methodological weakness of its own older number (`"The 80-94% single-shot numbers were inflated by a chatty baseline, Colin was right"`).
- Checkable arithmetic: README's `"ponytail is lowest on every metric (LOC 46%, tokens 78%, cost 80%, time 73%)"` correctly derives from the agentic writeup's `-54%/-22%/-20%/-27%` (100 minus each) — no discrepancy found.
- One unverifiable-but-plausible technical claim: `"Node.js ≥ 22.22.0 (promptfoo's engine constraint)"` — cannot confirm against promptfoo's actual `engines` field from this repo alone; flagged as unverified, not as an error.

## 5. Ranked verdict

1. **`ponytail`** — the ordered ladder plus explicit exception list is the rare skill with genuinely mechanical, checkable directives and its own disclosed failure mode.
2. **`ponytail-debt`** — smallest and most novel: a deterministic grep-and-ledger skill that only works because of a cross-skill marker convention designed on purpose.
3. **`ponytail-review`** — tight tag taxonomy with a concrete good/bad example pair; clean scope fence.
4. **`ponytail-audit`** — same mechanism as `-review` at repo scope; slightly less concrete ("Hunt" list lacks a worked example) and has no guard against token bloat on large trees.
5. **`ponytail-gain`** — good anti-hallucination honesty rule (`"NEVER print a per-repo savings number"`), but low actionability (display-only) and frozen numbers that will age.
6. **`ponytail-help`** — necessary but the least original by design, and the piece most likely to drift (hardcoded update commands, exact paths) as the underlying product evolves.

## 6. Flags

- `skills/ponytail/SKILL.md:32` (and identically in `AGENTS.md:32`): `"(Yes, this file also applies to agents working on the ponytail repo itself. Especially to them.)"` — addresses the agent reading the file directly and asserts self-application. Benign self-referential scoping (the skill governing its own repo's contributors), not a prompt-injection attempt against a reviewer; not acted on.
- No other content in any `SKILL.md`, `AGENTS.md`, or adapter rule file attempts to instruct a reviewing/grading agent, request installation into another agent's persistent instructions on the reviewer's behalf, or contains hidden/obfuscated directives. Grep for common injection phrasing (`ignore previous`, `disregard`, `you are reviewing`, etc.) returned no matches outside benign code comments about system-prompt construction in the benchmark harness itself.
