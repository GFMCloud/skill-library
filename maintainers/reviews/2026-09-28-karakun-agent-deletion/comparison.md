# Comparison: Karakun "coding agent deleted every file" article vs. installed skill library

## 0. Spot-checks of the clean-room review

Before using the clean-room review's judgments, I re-read `candidate.md` directly and checked six of its claims:

- **"raccoon" stray first line** (review §intro, Flag D) — confirmed: `candidate.md` line 1 is literally `raccoon`, unrelated to the article.
- **Rule block quoted at lines 354–371** (review Flag A) — confirmed verbatim against `candidate.md` lines 356–371; the five bullets under `## Git` match character-for-character, including the `AGENT_GUARD_APPROVE` override line.
- **Env var claim #16** (`CLAUDECODE=1`; `CODEX_THREAD_ID`/`CODEX_SESSION_ID`) — confirmed against `candidate.md` lines 247–248.
- **"6 of 6" and "2 of 7" experiment results** (claims #21, #25) — confirmed against the prose at `candidate.md` lines 329–331 and line 394.
- **Claim #27, flagged "asserted / over-extended"** — re-checked the actual table text at `candidate.md` lines 440–449: it prints "refused in 5 of 7 runs" for **both** the direct-push and inside-a-script columns, but the narrative (lines 388–398) only ever describes testing the direct `git push` case under pressure. No script-mediated push test is described anywhere in the article. The review's flag is correct: the script-push column looks filled in by analogy, not measured.

All six checks confirmed the review's readings. I found no misquotes or unsupported leaps beyond what the review itself already flagged, so I treat its claim table and technique list as reliable groundwork below.

## 1. Ancestry

No shared history. `candidate.md` is a third-party blog post from Karakun AG's developer hub (author François Martin, published 2026-08-28, pinned by hash), describing a real incident on the author's own personal repos and pointing at his own external tool, `martinfrancois/agent-git-guard`. The incumbent files (`deny-destructive.py`, `evidence-guard.py`, `hooks-registry.md`, `global-push-rules.md`, `inc-proof-of-work/`) are Graham's personal skill library, with its own internal ruling IDs (`Q-2026-09-03-15`, `Q-2026-08-15-5`), its own incident log (2026-09-02, 2026-09-03, 2026-09-07 reviews), and its own vendoring practice (explicit "Vendored unmodified from X, see SOURCE.md" style credit elsewhere in the library, e.g. `security-audit`). Nothing in either file set names the other: no merge note, no byte-overlap, no matching section structure beyond the generic fact that both are about "stop an agent from pushing something destructive." This is convergent, not derived — two independent parties hit the same Claude-Code-shaped problem (an agent that can run `git push` from inside a Bash tool call) and built different-shaped defenses. That reframes the comparison correctly: this is "what did each side learn independently," not "who forked from whom."

## 2. Classification of every technique

Numbering follows the clean-room review's §3 list, which I re-verified against the article text.

### 1. Inspect the staged diff before every commit
> `candidate.md`: "Running `git diff --cached --stat` in each repository would have shown 151 files about to disappear from one and 723 from the other."

**COMPLEMENT.** The nearest incumbent text is `inc-proof-of-work/references/code-checklist.md` phase 6:
> "**Diff** | `git diff --stat`, then read each changed file | ... | look for unintended changes, missing error handling, unhandled edge cases"

But that check fires at *proof-of-work completion time* — when an artifact is about to be declared done — not at *every git commit*. The Karakun incident happened entirely inside a "test" that committed and pushed without ever reaching a "declare done" step, so proof-of-work's own trigger would never have fired. `global-push-rules.md` has a diff-style check too, but it's scoped to push time and compares commit SHAs, not file content: "Immediately before pushing, run `git log --oneline origin/<branch>..HEAD` and read the list." Nothing in the required incumbent set puts a check *between `git commit` and the commit actually happening*. Gap: no incumbent rule reads `git diff --cached` before a commit is made. Nothing on this machine currently consumes this.

### 2. Don't revert in a shallow clone
> `candidate.md`: "Claude eventually switched to full clones and restored both repositories" (implied rule, not stated as one).

**COMPLEMENT.** No mention of `--depth`, shallow clones, or `git revert` anywhere in `deny-destructive.py`, `evidence-guard.py`, `hooks-registry.md`, or the `global-push-rules.md` excerpt. This is also structurally invisible to `deny-destructive.py`'s design: its `RULES` list is a deny-list of command *text* (`git reset --hard`, `git branch -D`, etc.), but the Karakun incident's dangerous command was an ordinary `git revert --no-commit HEAD` — nothing about that string is abnormal. The danger was entirely in repository *state* (shallow vs. full), which text-pattern matching cannot see. That's a real, not cosmetic, blind spot in the deny-list design as it stands.

### 3. Protect branches on personal repos once an agent can reach them
> `candidate.md`: "the personal repositories where you skipped it are worth revisiting the moment an agent can reach them."

**COMPLEMENT.** This is server-side GitHub branch protection. Nothing in the read incumbent set operates at that layer — `deny-destructive.py` and `evidence-guard.py` are both Claude-Code-side PreToolUse hooks (client-side, defeated the moment a script bypasses the harness), and `global-push-rules.md`'s carve-out is an agent-instruction-level policy, not a remote-enforced one. The library has no analogue to "the push is refused at GitHub before it lands, on every machine, regardless of what any local hook does."

### 4. Give the agent its own identity (separate machine account / app installation)
> `candidate.md`: "giving the agent a separate identity, a machine account or app installation whose credentials have no bypass rights."

**COMPLEMENT**, thinly touched. `global-push-rules.md`'s push carve-out gates on `gh auth status shows GFMCloud active` and separately excludes `gmorris1221` from ever being pre-authorizable, which implies *some* identity separation already exists between a personal account and an org identity the agent uses — but the excerpt never states the agent has its own credentials distinct from any human-usable account, nor that those credentials lack bypass rights on branch protection. The candidate's version is more explicit and goes further (no bypass rights specifically).

### 5. Detect the agent through an inherited environment variable
> `candidate.md`: "For any other tool, run `env | sort` inside an agent session and look for a variable that is not in your own shell." (`CLAUDECODE=1` for Claude Code.)

**COMPLEMENT.** Neither `deny-destructive.py` nor `evidence-guard.py` reads any environment variable to distinguish an agent-initiated command from a human one — both key entirely off `tool_input.command` text and `tool_name`. This is a genuinely new detection primitive for this library.

### 6. A `pre-push` git hook keyed on that env-var marker
> `candidate.md`: "the guard is a `pre-push` hook that refuses when it sees one of those variables and does nothing when it does not."

**SUPERIOR SUBSTITUTE**, for the specific job "stop a dangerous `git push`." Compare directly:

> `deny-destructive.py`: `("git push --force", re.compile(r"\bgit\s+push\b[^|;&]*\s(--force|-f)(\s|$)"))`

This regex requires `--force` to be followed immediately by whitespace or end-of-string. I traced it against `git push origin main --force-with-lease --force-if-includes`: the substring after `--force` is `-with-lease`, not whitespace, so the rule **does not fire**. `deny-destructive.py` blocks bare `--force`/`-f` but silently allows `--force-with-lease`, the exact flag the article shows is insufficient on its own. Worse, `deny-destructive.py`'s docstring itself states its blind spot: it only matches `tool_input.command` text on the `Bash` tool — a script the agent writes and runs (`python3 cleanup.py`) is invisible to it, which is *exactly* the mechanism of the Karakun incident (a "unit test" that ran `main()` on import and pushed from inside Python, not from a visible `git push` Bash call). A real git-level `pre-push` hook, which git invokes "no matter what process started it" (candidate.md line 239), closes that specific hole. What would need to be edited before it could actually replace/patch `deny-destructive.py`'s coverage here: (a) drop the personal, first-person framing and the `AGENT_GUARD_APPROVE=1` self-override bullet — it directly contradicts `global-push-rules.md`'s stated policy that "force pushes... stay never-pre-authorizable," so an agent-settable bypass variable cannot be adopted as-is; (b) confirm `CLAUDECODE=1` is actually set in this environment (plausible but unverified here — I have no Bash); (c) install it as an actual `.git/hooks/pre-push` (or via `core.hooksPath`) rather than a Claude-Code `PreToolUse` hook, since the whole point is to sit outside the harness; (d) register it in `hooks-registry.md`'s table, following the precedent already set there for hooks that sit outside the parsed table (`readonly-agent-guard.py` is documented as exactly this kind of exception).

### 7. `--force-with-lease --force-if-includes`, and the background-fetch correction
> `candidate.md`: "Fetching that remote quietly updates what your clone last saw... I tested it: the push went through and discarded two of them." / "Adding `--force-if-includes` to `--force-with-lease` closes that gap."

**INGESTIBLE FRAGMENT** of technique #8's rule block. `global-push-rules.md` already forbids agent-initiated force pushes outright ("force pushes... stay never-pre-authorizable"), which is a *stricter* net position than the candidate's "approve, then use the safer flags." So the headline policy is REDUNDANT — the incumbent's blanket ban subsumes the candidate's conditional allowance. But the specific technical correction (`--force-with-lease` alone is defeated by an incidental background fetch) is new, concrete, and not stated anywhere in the read incumbent set; it's worth keeping as a footnote wherever this library documents what happens on the rare occasion a human explicitly does approve a force push.

### 8. The short `## Git` rule block for `CLAUDE.md`/`AGENTS.md`
Treated as a bundle of five bullets; see the philosophy-conflict section below for the one that actually contradicts. Net classification: **INGESTIBLE FRAGMENTS**.

- Bullet 1 (diff before commit) → new, see item 1 above.
- Bullet 2 (PR always) → **conflicts** with `global-push-rules.md`'s carve-out; do not adopt as written (see §4).
- Bullet 3 (rejected push = stop signal, fetch and look) → largely REDUNDANT: `global-push-rules.md` already has "A push sends exactly the commits named in the request and nothing else... if any commit on it is not yours or not named, stop and ask," which is the same "verify before you push, stop on mismatch" instinct, arguably more specific (it also catches another session's silent commit, a scenario the candidate never considers).
- Bullet 4 ("tell me before you repair it. Repair by adding a commit.") → COMPLEMENT. Nothing in the read incumbent set states this. It's a direct, well-targeted lesson from this exact incident (Claude's revert-of-a-revert made things worse) and is missing from `global-push-rules.md`.
- Bullet 5 (pre-push hook + override discipline) → depends on #6 actually being built here; as written it's a **factual error if pasted verbatim now** (see §4).

### 9. Test your rules against the agent instead of assuming they work
> `candidate.md`: replaying the task with and without each rule, including a "production is down" pressure variant, and cutting rules the agent follows anyway unprompted.

**COMPLEMENT**, relative to the five required incumbents — none of them describes empirically testing a *CLAUDE.md instruction* against a live agent before trusting it. Something on this machine would plausibly consume it: the broader inventory (not one of the five required files, so not read in full here) lists `foundry-core:eval-harness` — "capability evals and regression evals... pass@k / pass^k reliability numbers... before a skill/hook is trusted" — which is the same methodological instinct, generalized to skills and hooks rather than specifically to git-safety instruction lines. It isn't wired to test `global-push-rules.md`'s carve-out today.

### The article's closing thesis
> `candidate.md`: "Git returned exit code zero... The result was nonsense... What was missing was one basic question: *Does this result make any sense?*"

**REDUNDANT.** `inc-proof-of-work/SKILL.md` already states this, more generally and with more evidence:
> "Where a tool reports its own outcome, confirm the outcome independently by inspecting what it claims to have produced... The check passed *because* it was run at the wrong level, and a passing check at the wrong level is more dangerous than no check at all: it converts an unknown into a false known."

The incumbent version generalizes beyond git (three logged real bugs: a plugin install, a marketplace update, a validator), whereas the candidate's version is one anecdote. Nothing to take here.

## 3. Routing collisions

The candidate isn't a skill package with a name/description to collide on, so the closest analogue is: if its `## Git` rule block were pasted into `global-push-rules.md`'s `CLAUDE.md` under the same `## Git` heading the incumbent already implies, the two bodies would sit under **one name with contradictory content** — precisely the "worst case, because nothing looks wrong" pattern the task warns about. A session reading a merged `## Git` section containing both "push your own commits without asking, under these conditions" (carve-out) and "land changes through a pull request... unless a standing rule allows self-merge" (candidate bullet 2) has no way to know which clause wins for an ordinary same-repo commit; whichever bullet the model attends to last, or reads as more specific, decides behavior. For a routine GFMCloud push under carve-out conditions, the *existing* rule would plausibly win (it's more specific: named org, named preconditions), but a model under time pressure — exactly the failure mode the candidate's own 2-of-7 experiment demonstrates — has a written PR-bullet sitting right next to it to point to as justification for *not* pushing, or conversely could read "self-merge allowed" loosely and push directly anyway, satisfying neither rule cleanly. That ambiguity itself is the hazard, not a specific misfire.

## 4. Philosophy conflicts

**Direct-push vs. PR-only**, and it's a real contradiction, not a difference of emphasis:

> `global-push-rules.md`: "**Autonomy tiers.** Just do it and log: commit, move cards, push own commits (below)." and "**Push carve-out.** A session may push without asking only its own commits, to a repo whose `git remote get-url origin` is under `github.com/GFMCloud/`, after [preconditions]... the push run as a separate command."

> `candidate.md` (rule block): "Land changes on the default branch through a pull request, and ask before merging unless a standing rule allows self-merge."

The incumbent's default posture is autonomous direct push under met preconditions, no PR required. The candidate's rule — written *by the person who was just burned by a direct push* — insists on a PR gate as the baseline, precisely because PR + required CI would have stopped both incidents in the article ("neither the invalid YAML nor the deletion commits would have passed CI"). These are not compatible defaults for the same repo class; adopting the candidate's bullet verbatim would silently override the carve-out (or vice versa), and nothing resolves the precedence.

## 5. Corrections needed at ingest

- **The rule block's last bullet is a factual claim about this environment that is currently false.** "A `pre-push` hook refuses these pushes, including ones a script makes" — no such hook exists here. `deny-destructive.py` is a Claude-Code `PreToolUse` hook, not a git `pre-push` hook, and as shown in §2.6 it doesn't even catch `--force-with-lease`. Pasting this bullet into `CLAUDE.md` without first building the hook would give the agent false confidence exactly where the article warns against it.
- **`AGENT_GUARD_APPROVE`-style self-override cannot be adopted as a real mechanism here** without contradicting `global-push-rules.md`'s "force pushes... stay never-pre-authorizable." If the pre-push-hook idea (§2.6) is built, its override path should route through the existing "Graham via inbox" autonomy tier, not a new agent-settable env var.
- **Don't cite the article's "5 of 7 either way" figure** for script-mediated pushes if writing this up internally — confirmed above that the script-push column is unmeasured, only the direct-push column was tested.
- **Drop the stray "raccoon" first line** if any part of `candidate.md` is archived or excerpted elsewhere — it's a scraping artifact, not content.
- **Style mismatch**: the candidate's rule block is first-person, owner-voiced ("tell me," "my overrides, never yours"). This library's convention, visible throughout `deny-destructive.py`, `evidence-guard.py`, and `hooks-registry.md`, is third-person/imperative with dated rulings and review citations (e.g., "ruled Q-2026-09-03-15 row 1," "oops-i-did-it-again review 2026-09-07, rows 2, 4, 5"). Any fragment taken from the candidate should be rewritten into that citation style, with this comparison document as its cited source, rather than pasted as first-person prose.

## 6. Net assessment

If only three things could be taken:

1. **The pre-push-hook-keyed-on-an-environment-marker design (§2.5–2.6)**, as a new git-level `pre-push` hook (not a `PreToolUse` hook), because it's the one idea here that closes a demonstrated, structural blind spot in `deny-destructive.py` — script-mediated pushes are invisible to command-text matching by construction, and the incident that produced this article happened exactly that way. Target: a new file alongside `deny-destructive.py`'s home (its own docstring implies `~/.claude/hooks/`), installed as an actual git hook via `core.hooksPath`, with a new row added to `hooks-registry.md` in the style already used for hooks that sit outside the parsed table (the `readonly-agent-guard.py` precedent), and its override path reconciled with `global-push-rules.md`'s "never-pre-authorizable" force-push policy rather than a new self-settable variable.
2. **The pre-commit diff-accountability rule (§2.1)** — "read `git diff --cached --stat` before every commit and account for every file it lists" — because it's a checkpoint at a moment (commit time) this library currently has no check for at all; its nearest neighbors fire either at push time (SHA comparison only) or at proof-of-work completion time (too late for a commit that's already landed). Target: a new bullet in `global-push-rules.md`'s `CLAUDE.md` excerpt, in that file's existing citation style, distinct from and not replacing the existing pre-push SHA check.
3. **The shallow-clone revert hazard (§2.2)**, because it's a class of danger — a normally-safe command made dangerous by invisible repository state — that `deny-destructive.py`'s deny-list design cannot catch by construction, and nothing else in the read set names it either. Target: a "Known weaknesses" addendum in `deny-destructive.py`'s docstring naming the gap explicitly (matching the file's existing practice of stating its own blind spots), plus a short instruction bullet in `global-push-rules.md` ("before `git revert` in any clone, confirm it isn't shallow — `git rev-parse --is-shallow-repository` — or unshallow first").

Everything else in the candidate is either already covered as well or better by the incumbent set (the "success message is not evidence" thesis, by `inc-proof-of-work/SKILL.md`; the general "stop on a rejected push" instinct, by `global-push-rules.md`'s commit-mismatch check), or is a genuine complement whose absence isn't urgent enough to make the top three (branch protection, separate agent identity, the empirical rule-testing methodology).
