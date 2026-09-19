# Review: fast-jev-compaction

## 1. Executive summary

- **What it is:** a TypeScript library plus a Claude Code function-hook plugin. When a session compacts, it doesn't write a summary. It asks TypeSafe's hosted "Jev" model two keep-probability questions about every older tool call, then deletes or truncates tool calls and results. All user and assistant text stays word for word.
- **The code does what the README says.** Nearly every mechanism the README describes is in `src/`. The code is small, careful and dependency-free at runtime, with a clean seam for swapping the transport (`JevAsker`).
- **Tests are good but never run automatically.** There's no CI config at all, so the passing tests are claimed, not verified.
- **I could not measure how mature it is.** The checkout is a depth-1 shallow clone, and I had no shell to run `git log`. There is one visible commit, merging PR #17 from a `devin/…` branch around 2026-09-17. That suggests an AI agent wrote at least some of the code and the project is young.
- **Adoption cost is the main problem:**
  - Every compaction sends your whole conversation to a third-party endpoint (`api.typesafe.ai`): prompts, assistant text, and tool inputs such as Bash commands and Write contents up to 1000 characters.
  - It needs a TypeSafe key.
  - It depends on a Claude Code feature that is early-access and gated behind an env flag.
- **Worth taking:** the prune-instead-of-summarize idea, the three-way keep / truncate / drop decision, and the staged state-fitting ladder. You can take those without the vendor dependency.

## 2. Maturity signals

I had no Bash tool in this session, so I read the `.git` files directly with Read, Glob and Grep.

| Signal | How I checked | What it returned |
|---|---|---|
| Last commit date | Read `.git/logs/HEAD` and `.git/shallow` | One entry: `clone: from https://github.com/tamaratran/fast-jev-compaction` at epoch 1789795787 (about 2026-09-19). `.git/shallow` holds a single SHA (`e3f262a`), so this is a depth-1 clone. The HEAD message is `Merge pull request #17 from tamaratran/devin/1789683249-readme-tagline`; the branch-name epoch works out to about 2026-09-17. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` | **Not measured.** I couldn't run it (no shell), and the shallow clone would only return one commit anyway. PR number #17 means at least 17 PRs so far. |
| Distinct authors, last 12 months | same | **Not measured.** Visible: owner `tamaratran` (`.claude-plugin/marketplace.json`) and a `devin/` branch prefix (an AI agent). Treat it as a single-maintainer project until shown otherwise. |
| Dependency count / freshness | Read `package.json`; Grep count of `"node_modules/…": {` in `package-lock.json` | **0 runtime dependencies.** 4 devDependencies (`@types/node ^22`, `tsx ^4.19`, `typescript ^5.7`, `vitest ^2.1.8`), 122 packages in the lockfile. I didn't check freshness because I had no network or npm. `vitest ^2` looks at least a major version old for late 2026. |
| License file | Read `LICENSE` | MIT, but it reads `Copyright (c) 2025` with **no holder named**. `package.json` and `plugin.json` both say MIT. |
| Tests exist AND CI runs them | Glob `**/*` (it listed dot-directories like `.claude-plugin`) | Tests exist: `tests/fast-jev-compaction.test.ts` (about 30 cases) and `tests/hook.test.ts`. **There is no `.github/` and no CI config of any kind.** So the tests exist but nothing runs them automatically. |
| Open issues | No `.github` or issue templates; no network | Not assessed. |
| Changelog / versioning | Glob | No CHANGELOG. `package.json` is at 0.2.0 but `plugin.json` and `marketplace.json` are at 0.3.0, so the version numbers have drifted apart. |

## 3. Claimed vs verified

**Verified in code:**
- **Calls are paired with results and some are pinned.** `collectToolCalls` pairs by `tool_use_id`. A call is pinned if the call *or* its result sits in the first message or the last N messages (`src/state.ts:62-93`).
- **Jev never sees tool output.** Each result is replaced with `ok|error, N chars (omitted)` (`src/state.ts:105`).
- **The state-fitting ladder matches the README exactly** (`src/state.ts:195-304`):
  - tool inputs capped at 1000, then 200, then 60 characters;
  - long texts abridged, oldest first, pinned messages last;
  - old messages collapsed to a note;
  - old calls reduced to one line each;
  - old messages with no calls left out;
  - runs of call-only messages merged;
  - then it throws.
- **Two `noul` questions per call** (`src/compact.ts:56`).
- **Batching keeps each request under the token cap.** The full state goes with every batch and the batches run concurrently via `Promise.all` (`src/compact.ts:73-99, 275`).
- **The three-way decision matches the README.** Keep if `keepResult` passes the threshold; else truncate the result if `keepCall` passes; else drop the call and its result (`src/compact.ts:101-115`).
- **The rebuild keeps untouched objects and never leaves a result without its call.** Unchanged messages come back as the same objects; a message left empty is removed. A dropped call's result goes with it, because both filters use the same `tool_use_id` action map (`src/compact.ts:149-225`).
- **Failures throw.** A missing key, a non-2xx response, bad JSON or a missing or non-finite answer all throw (`src/request.ts`, `src/client.ts:30`).
- **The hook falls back to Claude Code's built-in summary** when anything throws or the reduction is under `minReductionRatio` (`hooks/fast-jev.ts:263-290`).
- **The hook also triggers compaction itself** once context reaches `compactAtPercent` (60 by default) (`hooks/fast-jev.ts:292-307`). The README only mentions this in `hooks/README.md`.
- **The key lookup order is:** plugin option, then the `TYPESAFE_API_KEY` env var, then `settings.env` (`hooks/fast-jev.ts:227-244`).

**Claimed only (not verifiable from the repo):**
- That the token estimator "lands 2–18% above the true count" of Jev's reported usage (`src/state.ts:23-26`). No calibration data or script is included.
- That Jev's request limit is 32k and its probabilities are "calibrated". This is external to the repo.
- That `npm test`, `typecheck` and `validate:plugin` pass. Nothing runs them (see above).
- That it works with Claude Code 2.1.274 function hooks. The checked-in `types/claude-code.d.ts` says `// Written by Claude Code 2.1.274.`, but I couldn't verify runtime compatibility.
- Whatever reduction you get in practice. The only live check is `examples/demo.ts`, which needs a key and the network.

## 4. Rubric scores

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **5** | Every mechanism in the README maps to specific code, including the exact truncation caps, stage names and fallback conditions. |
| 2 | Quality of the interesting part | **4** | The fitting ladder and the rebuild are careful: they track tokens incrementally, reuse objects so Claude Code keeps its message handles, and keep the call/result pairing intact. There is no timeout, retry or concurrency limit on requests, and one design choice needs caveats (see "Failure modes" below). |
| 3 | Adoption cost | **2** | You add a proprietary vendor, an API key, conversation data leaving your machine, and an early-access Claude Code feature behind a flag. Removal is easy: uninstall the plugin and you're back to built-in compaction. |
| 4 | Failure modes | **2** | Errors are conservative: any failure falls back to the built-in summary. The bigger concerns are data leaving the machine, repeated compaction, requests with no timeout, lock-in to one vendor, and possible churn in the early-access API. |
| 5 | Originality | **4** | Pruning tool traffic instead of summarizing, with a separate "keep the call, drop the output" middle option, is a strong idea that transfers to other setups. |

**Failure modes in detail (why #4 scores 2):**
- **Data leaving the machine.** Every compaction sends the whole conversation text and tool inputs to `https://api.typesafe.ai/v1/systemone` (`src/request.ts:3`). That can include Bash commands with inline secrets and file contents from Write/Edit inputs (up to 1000 characters). Nothing is redacted.
- **Jev judges results it never saw.** It decides whether to keep a result without seeing any of it, only the tool name, the input and the character count. So an important detail inside an old result, such as an exact error message, can be truncated on the model's guess. The README is candid about this ("a probability is not a proof").
- **Repeated compaction.** If a compaction reduces enough to pass the 25% bar but context is still at or above 60%, the next `turn.complete` triggers another compaction. That can mean one full-conversation upload per turn. The `compacting` flag only prevents overlapping runs.
- **No timeout on requests.** `fetch` gets no `AbortSignal`, and `Promise.all` sends every batch at once with no limit. A slow endpoint stalls `/compact`, unless Claude Code's own hook time limit (mentioned in the type file) cuts it off.
- **Lock-in.** The `JevAsker` seam can be swapped, but the questions assume Jev's `noul` answer format.
- **Early-access API.** The plugin relies on typings generated from one Claude Code build and says to "regenerate and review that file after a Claude Code upgrade".

**Minor issues:**
- The "old messages collapsed" stage also rewrites short texts, such as `"go ahead"`, into a longer `[… 8 chars omitted …]` note. This wastes tokens but causes no wrong results, since tokens are recounted after each change.
- The LICENSE names no copyright holder.
- The version numbers differ between files (0.2.0 vs 0.3.0).

## 5. Ideas worth taking independently of the code

1. **Prune, don't summarize; never rewrite text.** "This library never rewrites anything. It only deletes tool calls and tool results… User and assistant text stays verbatim and in order." (`README.md:12-15`)
2. **A middle option between keep and drop: keep the call, truncate the result to its first N characters plus a note telling the model to re-run.**
   - "`keepCall ≥ threshold` → keep the call, truncate the result to its first `truncateHeadChars` characters plus a one-line note" (`README.md:49-50`)
   - The note text: `re-run the tool if needed` (`src/compact.ts:138-140`)
3. **Two separate questions per call.** One asks whether knowing the call happened still matters; the other asks whether its output is still needed and couldn't simply be re-fetched. (`src/compact.ts:60, 64`)
4. **An ordered state-fitting ladder that records which stage it needed.** "tool inputs truncated to 1000, then 200, then 60 characters; long texts abridged… old tool calls reduced to one line each (`t12 Read file_path=src/a.ts → ok 480ch`)" (`README.md:30-35`). The stage name is returned in `stats.stateStage`, which is useful for diagnosing why a compaction behaved as it did.
5. **Return untouched inputs as the same objects.** This lets the host keep its handles on unchanged messages and only take edited content from rebuilt ones. "Whatever came back unchanged… is the engine's own object, handle included; anything rebuilt is a fresh message without a handle" (`hooks/fast-jev.ts:124-129`)
6. **Only replace the built-in behaviour when the result is clearly better.** Falling back when the reduction is below 25% (`hooks/fast-jev.ts:271-277`) is a cheap safety bar for any replacement of built-in behaviour.
7. **A token estimator with no tokenizer dependency**, split into words, digits and symbols. It's aimed at JSON-heavy payloads, where a flat characters-per-token ratio undercounts (`src/state.ts:21-38`). The calibration claim is unverified, but the approach is reusable.

## 6. Flags

- **Nothing in the repo addresses a reviewing agent, asks to be added to CLAUDE.md or AGENTS.md, or asks the reader for credentials.** I searched for phrases like "you are", "reviewer", "ignore previous", "CLAUDE.md", "AGENTS.md" and "add this to". The only hits were:
  - the `noul` question text sent to Jev (`src/compact.ts:60,64`);
  - Claude Code API doc comments in the generated `types/claude-code.d.ts`.

  None of them were directed at a reviewer.
- **Credential handling, for information:**
  - The plugin asks users to put a third-party key in `~/.claude/settings.json`: `{ "env": { "CLAUDE_CODE_ENABLE_FUNCTION_HOOKS": "1", "TYPESAFE_API_KEY": "<your key>" } }` (`README.md:142`).
  - The hook reads that key back from settings (`hooks/fast-jev.ts:237-241`).
  - The generated type file documents a `$.session.authorize()` handle mechanism where "the secret never reaches the plugin" (`types/claude-code.d.ts:2357`). The plugin reads the raw key instead.
- **Build script side effects:** `demo/JevDemo/build.sh` compiles, ad-hoc code-signs and `open`s a macOS app. It's opt-in and not part of `npm` scripts. I did not run it.
