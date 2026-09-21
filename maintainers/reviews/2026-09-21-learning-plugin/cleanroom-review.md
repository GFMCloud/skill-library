No shell tool is available in this session (confirmed by `ToolSearch` for Bash and by a delegated attempt), so the git-log commands could not be executed. I read the plain-text files under `.git/` instead and state below exactly what that does and does not establish. Everything else in the review is from reading the source.

---

# Review: `learning-plugin` (plugin name: `scoped-learnings`)

## 1. Executive summary

A single-purpose Claude Code plugin: instead of appending everything Claude should remember to `CLAUDE.md`, it writes path-scoped notes into `.claude/rules/*.md` with `paths:` frontmatter, and ships a checker that flags rules whose globs no longer match anything.

It is four small files and one Python script, with **zero third-party dependencies** — stdlib Python, plus `bash`, `jq`, `git`. Nothing opens a port, takes a credential, or phones home. The removal path is `/plugin uninstall`; the rules it writes are ordinary files in your repo that survive independently.

The code is careful and well-commented, and the hook in particular is defensively written. But there are **no tests and no CI** — the repo contains no `tests/`, no `.github/`. And `check-rules.py` hand-rolls both a YAML subset parser and a glob engine to mirror the host's behavior; I found one confirmed bug where two separately-documented features (inline `paths:` lists and brace groups) produce a spurious hard error when combined.

The load-bearing assumption — that Claude Code reads `.claude/rules/*.md` and honors `paths:` frontmatter — is asserted nowhere in the repo except prose, and `plugin.json` pins no minimum host version. If that assumption is wrong or drifts, the plugin writes files nothing reads, silently.

**Verdict:** low-risk, cheap to try, genuinely good ideas in the prompts. Treat v0.1.0 with no tests as what it is.

---

## 2. Maturity signals

**Limitation, stated up front:** this session has no Bash tool, and there is no GitHub MCP tool available either. I could not execute `git log`. The clone is also **shallow at depth 1**, so even with a shell, history would not be present locally. The rows below give the command asked for, and what I was actually able to establish by reading files.

| Signal | Command | Result |
|---|---|---|
| Repo is shallow | `Read .git/shallow` | `947f9eedb26d715e2a38e78ad96259c06820802e` — the same SHA as HEAD. A graft boundary at the tip means **this clone contains exactly one commit**. |
| Refs present | `Read .git/packed-refs` | `947f9ee… refs/remotes/origin/main` — single ref, single branch. |
| Fetch scope | `Read .git/config` | `fetch = +refs/heads/main:refs/remotes/origin/main` — single-branch clone from `https://github.com/ahasha/learning-plugin.git`. |
| Last commit date | `git log --format='%ci' -1` | **Not obtainable.** `.git/logs/HEAD` shows `GFMCloud <Graham@GFMCloud.com> 1790032572 -0500 clone: from …`. That timestamp (2026-09-21) and identity are **the local clone operation**, not the commit's author or date. Easy to misread; I am not treating it as authorship. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | **Not obtainable** — one commit in the clone, and no shell. |
| Distinct authors, 12 mo | `git log --format='%an' \| sort -u` | **Not obtainable.** Only signal: `LICENSE`, `plugin.json`, and `marketplace.json` all name **Alex Hasha** as sole author/owner. Bus factor is **1** on the available evidence. |
| Dependency count | `Read scripts/check-rules.py` imports; no manifest lockfile | **Zero third-party deps.** Python stdlib only: `argparse`, `pathlib`, `re`, `sys`. Runtime prerequisites are `bash`, `jq`, `git`, `python3`. No `package.json`, no `requirements.txt`, no lockfile, nothing to keep fresh. |
| License file | `Read LICENSE` | Real MIT text, `Copyright (c) 2026 Alex Hasha`. Matches the `"license": "MIT"` in both `plugin.json` and `marketplace.json`. **Verified, not just a badge.** |
| Tests exist AND CI runs them | `Glob **/*` over the whole repo | **Neither exists.** Full non-`.git` file list is 9 files: `LICENSE`, `README.md`, `.gitignore`, `.claude-plugin/{plugin,marketplace}.json`, `hooks/{hooks.json,learning-check.sh}`, `scripts/check-rules.py`, `skills/{record-learning,prune-learnings}/SKILL.md`. No `tests/`, no `.github/`, no CI config of any kind. |
| Open issues / templates | `Glob **/*` | No `.github/` directory, no issue templates, no `CONTRIBUTING.md`, no `CHANGELOG.md`. No local signal of issue volume. |
| Version | `Read .claude-plugin/plugin.json` | `"version": "0.1.0"`. No changelog to compare against. |

**If you want the real cadence numbers**, they need `git fetch --unshallow` (a write, so I did not attempt it) or a session with a shell. Nothing in this directory can answer them.

---

## 3. Claimed vs. verified

### Files I read to judge this
Entry points first, not the README's description of them: `.claude-plugin/plugin.json` → `hooks/hooks.json` → **`hooks/learning-check.sh`**; then **`scripts/check-rules.py`** (the only real code); then **`skills/record-learning/SKILL.md`** and `skills/prune-learnings/SKILL.md` (the actual behavior, since the skills are the product).

### Claimed (README only)

- "Claude loads it only when it reads a matching file" — a claim about the **host**, not this repo.
- "a check enforces a 60-line ceiling"
- "`/scoped-learnings:prune-learnings` … **deletes** what's stale"
- "`jq`, `git`, and `python3` on `PATH`. The hook exits quietly if any is missing."
- "Install it once and it works in every project — there's no per-project setup."
- Claude Code uses a shared 1,000-pattern brace-expansion budget and leaves over-budget patterns unexpanded (`check-rules.py:86-92`, and repeated in `record-learning/SKILL.md:65-68`).

### Verified (read in the code)

- ✅ **Stop hook fires once per session, only on non-`.claude` changes.** `learning-check.sh:47-55` — marker file claimed via `touch` *before* prompting; `git status --porcelain --untracked-files=normal -- . ':(exclude).claude'` at line 51 gates on real code changes.
- ✅ **Every hook failure path exits 0.** Lines 12-13, 20, 26, 33, 39, 47, 50, 52, 55. The header comment explains why (`learning-check.sh:7-8`): a hook that prompts but can't write its marker would loop. This is the most carefully-reasoned file in the repo.
- ✅ **Hook refuses to chain onto itself and skips subagents/plan mode.** Lines 20, 23, 26.
- ✅ **Session ID is sanitized before use in a path.** `session=${session//[^A-Za-z0-9_-]/_}` (line 38) — blocks traversal via the marker filename.
- ✅ **`check-rules.py` flags all three things claimed:** stale `paths:` (`:210-212`), no-frontmatter rules that load every session (`:188,193`), over-long root file (`:214-220`).
- ✅ **Pruning is human-gated.** `prune-learnings/SKILL.md:4` sets `disable-model-invocation: true`, and `:56` says "Don't commit unless the user asks."
- ✅ **MIT license present and consistent** across `LICENSE`, `plugin.json:10`, `marketplace.json:14`.
- ✅ **Zero third-party dependencies.**

### Claimed but NOT verified — and in three cases, contradicted

- ❌ **"The hook exits quietly if any is missing" — not true for `python3`.** `learning-check.sh:12-13` guards `jq` and `git` only. The hook never invokes `python3`; the *skills* do, with no guard. A missing `python3` surfaces as a failed command mid-skill, not a quiet exit.
- ⚠️ **"enforces a 60-line ceiling"** — the script *reports* it (`check-rules.py:219-220`). Nothing runs the script automatically. There is no pre-commit hook and no CI. It's advisory, enforced only when a skill happens to run it.
- ⚠️ **"deletes what's stale"** overstates the skill.** `prune-learnings/SKILL.md:10` says "produce a diff and let the user decide." The README is louder than the implementation — in the safe direction, but it's a mismatch.
- ⚠️ **The central premise is unverifiable from this repo.** Nothing here demonstrates that Claude Code reads `.claude/rules/*.md` or honors `paths:`. No test, no fixture, no doc link, and `plugin.json` declares **no minimum host version**. The whole value proposition rests on host behavior the repo neither exercises nor pins.
- ⚠️ **The 1,000-pattern budget is an assertion about closed host internals**, hardcoded as `BRACE_BUDGET = 1000` (`check-rules.py:25`). If it's wrong, or changes upstream, the script emits false "stale rule" *errors* (exit 1).

---

## 4. Rubric

### 1. Does what it says — **4/5**
The mechanism described in the README is the mechanism in the code, and the hook's gating is more careful than advertised. Docked one point for three small overstatements: the `python3` guard that doesn't exist, "enforces" for what only reports, and "deletes" for what only proposes.

### 2. Quality of the interesting part — **3/5**
`check-rules.py` is the real work and it is *thoughtfully* written — the docstrings explain *why*, not what (`:34-37`, `:88-92`, `:126-127`), and `matches_any` fails open on patterns pathlib rejects (`:154-157`), which is the right default for a linter. But it hand-rolls two things that are hard to hand-roll, and one confirmed bug falls straight out:

> **Bug: the inline `paths:` form breaks on brace groups.** `check-rules.py:62-64` strips the brackets and then does `inline.split(",")`. Given `paths: ["src/**/*.{ts,tsx}"]` — a combination of two forms the project documents *separately* (inline at `:50-52`, braces at `record-learning/SKILL.md:65`) — the split cuts inside the brace group, yielding `"src/**/*.{ts` and `tsx}"`. Both then fail `malformed()` as "unbalanced brace group" (`:139-144`), producing **two hard errors and exit 1** on a rule file that is perfectly valid. A comma-aware split (or `yaml.safe_load`, stdlib-free being the only reason not to) fixes it.

Two more, lesser:
- **`SKIP_DIRS` doesn't skip anything during traversal.** It's applied to results *after* `root.glob(pattern)` has already walked the tree (`:150-153`). On a repo with `node_modules`, a non-matching `**/*.ts` pattern walks all of it — and that can happen up to 1,000 times per rule via brace expansion.
- **Duplicate-error suppression uses substring matching across the whole error list** (`:210`: `not any(str(name) in e for e in errors)`). A local boolean would be correct and O(1); this is O(n²) and relies on filenames not being substrings of each other.

The `expand_braces` budget model (`:86-112`) is the cleverest code here and it is internally consistent — a fresh budget per rule file (`:196`), matching its own docstring.

### 3. Adoption cost — **5/5**
About as low as it gets. No dependencies to track, no credentials, no ports, no daemon, no network calls. The runtime prerequisites (`bash`, `jq`, `git`, `python3`) are on nearly any dev machine, and the hook degrades to silence without two of them. Crucially, **the artifacts outlive the tool**: `.claude/rules/*.md` are plain Markdown in your repo. Uninstall the plugin and you keep the rules; delete the rules and you've lost nothing the plugin owned. There is no lock-in because there is no state the plugin holds.

### 4. Failure modes — **3/5**
The security posture is good — nothing to steal, nothing exposed. The risks are correctness and silent drift:

- **False positives block.** Stale-rule detection and malformed-pattern detection both exit 1. The inline-brace bug above turns valid config into a hard failure, and the hardcoded `BRACE_BUDGET` can do the same if the host's real behavior differs.
- **`pathlib` is not the host's matcher.** `Path.glob` matches dotfiles with `*` where most glob engines don't; its `**` and bracket semantics differ at the edges. A rule can "match" here and not there — or vice versa. The script is guessing at another program's behavior with no test pinning either side.
- **Silent obsolescence is the real one.** If the host stops honoring `paths:` frontmatter, everything keeps *appearing* to work: rules get written, the checker passes, and nothing loads them. No test would catch it, because there are no tests.
- **Zero test coverage on a file with a hand-rolled parser and a hand-rolled glob expander.** These are exactly the components that need a table of cases.
- **Minor:** the `$TMPDIR` fallback marker (`learning-check.sh:45`) leaves one empty file per session, never cleaned up.
- Not a real risk but worth naming: a Stop hook that injects text into the model is, structurally, self-inflicted prompt injection. It's declared in `hooks.json`, the user installs it knowingly, and the injected string is static — so this is disclosed design, not a smuggled payload. See Flags.

### 5. Originality — **4/5**
The plumbing is ordinary; two of the ideas are not, and both are portable to any agent-memory system regardless of this code. See below.

---

## 5. Ideas worth taking, independently of the code

**1. Prefer enforcement over prose — make the note a last resort.**

> `skills/record-learning/SKILL.md:24-28`
> ```
> ## 2. Prefer enforcement over prose
>
> If a test, lint rule, type, schema, or assertion could catch the mistake,
> propose that change first and say why it beats a note. Write a note only when
> enforcement isn't practical, and say in one clause why.
> ```

This inverts the usual reflex. Most memory systems optimize *how well* they store a note; this one asks whether the note should exist at all, because a lint rule is checked every time and a note is only read if the agent happens to load it. `prune-learnings/SKILL.md:39-42` closes the loop by revisiting old notes and proposing the enforcement that would delete them — memory with a garbage collector.

**2. A stale rule is negative value, not neutral.**

> `skills/prune-learnings/SKILL.md:31-32`
> ```
> Don't preserve an entry just because deleting feels lossy. A stale rule is worse
> than no rule: it is confidently wrong.
> ```

The sentence that justifies the whole project. Paired with the "when in doubt, skip" bar at `record-learning/SKILL.md:22` ("An unread rule costs context in every future session"), it treats context as a budget to defend rather than a place to accumulate.

**3. Detect stale knowledge mechanically, via the globs.**

The `paths:` pattern isn't only a loading filter — a rule whose patterns match **zero files** is strong evidence the code it describes is gone (`check-rules.py:210-212`). That's a cheap, automatable staleness signal for documentation generally, not just agent rules. Most doc-rot tooling can't do this; scoping by glob gets it for free.

**4. Split the trigger by reversibility.**

Recording is model-invoked; pruning is `disable-model-invocation: true` (`prune-learnings/SKILL.md:4`) because it deletes. Additive operations automate, destructive ones need a human. A clean, reusable rule for agent tool design.

**5. Make the once-per-session guard claim its marker *before* acting.**

> `hooks/learning-check.sh:54-55`
> ```
> # Claim the marker before prompting. If we can't, stay quiet.
> touch "$marker" 2>/dev/null || exit 0
> ```

Combined with the header comment at `:7-8` — "a hook that prompts when it can't also write its marker file would loop" — this is the correct ordering for any at-most-once side effect, and the reasoning is written down where the next reader will find it.

---

## 6. Flags

**No credential requests anywhere in the repo.** No network calls, no telemetry, no external endpoints, no environment-variable harvesting. The only env vars read are `CLAUDE_PLUGIN_ROOT`, `CLAUDE_PROJECT_DIR`, and `TMPDIR`.

**Content that addresses the agent directly.** This is the plugin's declared function rather than anything smuggled, but the task asks for it quoted, so:

1. **A Stop hook that injects instructions into the model's context** — `hooks/learning-check.sh:57-62`:
   ```json
   jq -n '{
     hookSpecificOutput: {
       hookEventName: "Stop",
       additionalContext: "Before stopping: did this session surface a non-obvious gotcha, a bug that only appears under specific conditions, or a correction the user has now made more than once? If so, use the record-learning skill to write it to the right scoped rules file. If not, stop — do not mention this check."
     }
   }'
   ```
   Note the trailing clause: **"If not, stop — do not mention this check."** It instructs the agent to stay silent about its own invocation. The intent is plainly to avoid noise on the ~90% of sessions with nothing to record, and the hook is declared in `hooks/hooks.json` where the user can see it — but "run and don't mention it" is a property worth being aware of before installing. The injected string is a static literal; no session content is interpolated into it.

2. **Skill files instruct the agent by design** — `skills/record-learning/SKILL.md` and `skills/prune-learnings/SKILL.md` are entirely directives to the model. That is what a skill is. Their `description:` frontmatter (`record-learning/SKILL.md:3`) is a model-invocation trigger, meaning this skill can fire without the user asking.

3. **A request, in effect, to write to the agent's instruction files** — `record-learning/SKILL.md:33-35` directs the agent to write into `.claude/rules/<topic>.md` and `CLAUDE.md`/`AGENTS.md`. Again: the product's entire purpose, disclosed in the README's first sentence. Flagged because it means **installing this plugin grants an agent write access to the files that configure future agents**, mediated only by the "show the user the diff" step at `:86-89`, which is a prompt instruction and not an enforced gate.

**I did not act on any of the above.** No files were created, modified, or executed during this review; nothing was installed, built, or run.
