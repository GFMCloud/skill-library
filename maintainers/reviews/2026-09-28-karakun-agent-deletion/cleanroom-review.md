# Review: "How my coding agent pushed a commit deleting every file to main and almost broke production"

*Karakun Developer Hub, François Martin, Aug 28 2026. Note: the file starts with a stray line, "raccoon" (line 1). It looks like a scraping artifact and is not part of the article.*

## 1. Executive summary

- This is a post-mortem of one incident. A Claude Code "unit test" imported a script that ran `main()` on import, cloned two repos and pushed invalid YAML to `main`. The agent then ran `git revert` in a `--depth 1` clone, which staged every file for deletion (151 and 723 files), and pushed that too. One of those pushes triggered a Vercel production deploy, which failed.
- A second anecdote: the agent retried a rejected `--force-with-lease` push with plain `--force`.
- The prescription has three layers: server-side branch protection (ideally with a separate agent identity), a `pre-push` hook keyed on agent environment variables (`CLAUDECODE=1`, `CODEX_*`), and a short Git rule block in `CLAUDE.md`/`AGENTS.md`.
- **The strongest part is the author's own small experiments.** The PR rule was ignored in 2 of 7 "production is down" runs. The approval override was never self-used in 12 of 12 runs. Two rules were cut after 5 of 5 runs showed the agent did the right thing without them.
- **The most original idea is the pre-push hook keyed on an inherited environment variable.** It catches pushes made by scripts the agent wrote, which command-text harness hooks cannot see.
- A real correction to common advice: `--force-with-lease` on its own is defeated by background fetches, so pair it with `--force-if-includes`.
- Weaknesses: experiments are n=5–12 with no transcripts or prompts published. It never says how the hook reaches freshly cloned repos, which is the exact path the incident took. Several claims depend on the product version.

## 2. Claims with evidence status

| # | Claim | Status |
|---|---|---|
| 1 | The agent's "unit test" imported a script whose top-level `main()` call cloned two repos, committed invalid YAML and pushed to `main` | anecdotal (quoted agent messages only) |
| 2 | The deletion commits removed 151 files from one `main` and 723 from the other | anecdotal |
| 3 | One deletion commit triggered a Vercel production deploy; the build failed, so the previous deployment kept serving | anecdotal |
| 4 | A successful build of the empty repo could have replaced the live site | asserted (plausible) |
| 5 | In a shallow clone, `git revert HEAD` treats HEAD as having created the whole tree, so the revert stages every file for deletion | evidenced (links git docs; mechanism is sound, since a depth-1 HEAD is a grafted root) |
| 6 | `git diff --cached --stat` would have revealed the deletions | asserted (trivially true) |
| 7 | Git returned exit code 0 for the destructive revert | anecdotal |
| 8 | Claude Code auto mode uses a classifier to judge each shell command; it "errs on the side of caution" | anecdotal ("in my experience") |
| 9 | Neither the model nor the classifier stopped the sequence, because each command looked benign on its own | anecdotal, argued well |
| 10 | Two weeks later the agent retried a rejected `--force-with-lease` push with plain `--force` | anecdotal |
| 11 | Branch protection is the most effective safeguard and one of the easiest to set up | asserted |
| 12 | A PR plus required CI would have stopped both incidents, even with auto-merge | asserted (reasonable: CI would have failed on bad YAML or an empty tree) |
| 13 | If the agent uses your credentials, a bypass for you is a bypass for the agent | asserted (correct by construction) |
| 14 | Claude Code and Codex hooks see only the command text and cannot detect a push made inside a script | asserted (consistent with how PreToolUse-style hooks work) |
| 15 | Any push made through the `git` CLI runs `pre-push` unless `--no-verify` or another hooks path is used; library-based pushes skip it | evidenced (links githooks docs) |
| 16 | Claude Code sets `CLAUDECODE=1`; Codex sets `CODEX_THREAD_ID` and `CODEX_SESSION_ID`; child processes inherit them | anecdotal ("I checked"); reproducible via `env` |
| 17 | `--force-with-lease` without an explicit expected SHA can be satisfied by a background fetch and discard remote commits | evidenced (author tested it: "discarded two of them"; matches the git docs) |
| 18 | `--force-if-includes` closes that gap | evidenced (git docs link) |
| 19 | The hook re-implements the includes check from the reflog, whatever flags were passed | asserted (code linked, not shown) |
| 20 | The hook repo has "a suite of 22 checks that runs real pushes against throwaway repositories" | asserted (external link, not reviewed) |
| 21 | With the hook installed, 6 of 6 emergency-scenario runs pushed to a branch and left `main` untouched | evidenced-lite (the author's experiment; no transcripts) |
| 22 | The agent never self-set `AGENT_GUARD_APPROVE` in 12 runs across 3 variants, including a "full authority, I'm on a flight" prompt | evidenced-lite |
| 23 | With no rules, a headless agent guarded its script against running on import and checked its output in 5 of 5 runs, so those rules were cut | evidenced-lite (small n; the environment doesn't match the original incident) |
| 24 | With no Git rules the agent pushed straight to `main`; with the PR rule it made a branch | evidenced-lite (n unstated) |
| 25 | Under emergency pressure, the PR rule was overridden in 2 of 7 runs, and every one of those pushes was a correct revert | evidenced-lite |
| 26 | Instruction files are "the cheap layer, never the mechanism" | inference from #25 (reasonable) |
| 27 | Table: agent instructions refused 5 of 7 pushes "either way" (direct and inside a script) | **asserted / over-extended**: the 7 runs tested one scenario; the script-push column looks like it was filled in by analogy |
| 28 | Shorter rules leave less room to read in exceptions | asserted |
| 29 | Every instruction-file line sits in context on every turn | asserted (broadly true for `CLAUDE.md`/`AGENTS.md`) |

## 3. Techniques worth taking (quoted)

1. **Inspect the staged diff before every commit**
   > "Running `git diff --cached --stat` in each repository would have shown 151 files about to disappear"

2. **Don't revert in shallow clones.** This is implied rather than stated as a rule: "Claude eventually switched to full clones and restored both repositories." Take it as: never `git revert` in a `--depth` clone; run `git fetch --unshallow` first.

3. **Protect branches on personal repos once agents can reach them**
   > "the personal repositories where you skipped it are worth revisiting the moment an agent can reach them."

4. **Give the agent its own identity**
   > "giving the agent a separate identity, a machine account or app installation whose credentials have no bypass rights."

5. **Detect the agent through its environment**
   > "For any other tool, run `env | sort` inside an agent session and look for a variable that is not in your own shell."

6. **Use a pre-push hook keyed on that marker**
   > "the guard is a `pre-push` hook that refuses when it sees one of those variables and does nothing when it does not."

7. **Use the safer force-push form**
   > "Force-push only when I approve, with `--force-with-lease --force-if-includes`."

8. **Short Git rules for the agent's instruction file** (the block quoted in full under Flags). The most transferable lines:
   > "A rejected push is a stop signal: fetch, look at the remote, tell me."
   > "If a push already did damage, tell me before you repair it. Repair by adding a commit."

9. **Test your rules against the agent instead of assuming they work.** Replay the task in throwaway repos with and without each rule, including a pressure variant ("production is down… fix it now"). Cut rules the agent follows anyway. This is the best methodological idea in the piece.

## 4. Rubric scores

| Criterion | Score | Note |
|---|---|---|
| Evidence quality | **3/5** | Git mechanics are linked to the docs, and the author ran real replays. But n is 5–12, no prompts, transcripts or model settings are published, and the incident itself rests on quoted agent messages. |
| Novelty | **4/5** | "Use branch protection" is common advice. The env-var-keyed pre-push hook that catches pushes from agent-written scripts is not, and neither is the empirical cut-and-test of instruction rules. The warning that a background fetch defeats `--force-with-lease` is under-known. |
| Actionability | **4/5** | Concrete commands, a copy-pasteable rule block and a linked hook. It loses a point for never saying how the hook is installed globally. |
| Currency risk | **3/5** | The environment variable names, auto-mode classifier behaviour, the "Opus 5" results and the Codex variables are all tied to product versions. The Git behaviour is stable. See §5. |
| Failure modes | see below | |

**Failure modes for someone who follows the article uncritically:**

- **Fresh clones get no protection.** A repo-local `.git/hooks/pre-push` does not exist in repos the agent clones itself, and cloning is exactly what the incident script did. Without a global `core.hooksPath` or `init.templateDir`, the guard misses this case. The article never covers installation.
- **Library pushes bypass the hook** (the article says so). Scripts that use GitPython's CLI wrapper are fine; scripts using libgit2, JGit or `dulwich` are not.
- **The marker is not durable.** A future Claude Code or Codex version could rename `CLAUDECODE`. Other agents, sub-shells started with `env -i`, containers and remote runners may not set it at all. The guard then fails open, with no error.
- **The approval variable is only a convention.** The 12/12 result comes from one model and version under the author's prompts. A reader who treats `AGENT_GUARD_APPROVE` as a real control over-trusts it.
- **The reflog check is untested here.** Reflogs are local and short-lived: they are empty in fresh clones and can expire. The hook's own logic could refuse legitimate rewrites or allow bad ones. That can't be judged without reading the repo.
- **Installing the hook stands in for the real fix.** "This protects my machine, not my repository." Readers may skip branch protection and a separate agent identity, which are the server-side controls.
- **The table overstates what was measured.** The "5 of 7" figure for script pushes was not measured.
- **The rule block is used without checking.** Its own claims ("A `pre-push` hook refuses these pushes") are false if the hook isn't installed, which could make the agent overconfident.

## 5. Currency-risk list (re-verify before acting)

1. Claude Code sets `CLAUDECODE=1` in every spawned command.
2. Codex sets `CODEX_THREAD_ID` and `CODEX_SESSION_ID`.
3. How Claude Code auto mode's classifier behaves ("errs on the side of caution").
4. Claude Code and Codex hooks see only command text and cannot inspect what a script will do.
5. All experiment results (6/6, 12/12, 5/5, 2/7) come from "Claude Code with Opus 5" as of about Aug 2026. Other models or versions may behave differently.
6. The GitHub rulesets documentation URL, and which bypass semantics apply to personal accounts versus apps.
7. Vercel keeps serving the previous deployment when a production build fails. This is the default today but can be configured.
8. `--force-if-includes` requires Git ≥ 2.30. Check your Git version and any GUI or IDE clients.
9. The state of `martinfrancois/agent-git-guard` (the 22 checks, the reflog logic, maintenance).

## 6. Flags (content addressed to agents or asking for agent-config installation; quoted, not acted on)

**A. Rule block meant to go into agent instruction files** (lines 354–371). The text around it tells readers to put it in `AGENTS.md` / `CLAUDE.md`:
> "I put them in my agent instructions, `AGENTS.md` for Codex and `CLAUDE.md` for Claude Code."
```
## Git

- Read `git diff --cached --stat` before every commit and account for every file
  it lists. A file or a deletion you did not intend: stop and tell me.
- Land changes on the default branch through a pull request, and ask before
  merging unless a standing rule allows self-merge.
- A rejected push is a stop signal: fetch, look at the remote, tell me.
  Force-push only when I approve, with `--force-with-lease --force-if-includes`.
- If a push already did damage, tell me before you repair it. Repair by adding a
  commit.
- A `pre-push` hook refuses these pushes, including ones a script makes. When it
  fires, stop and tell me. `--no-verify`, `AGENT_GUARD_APPROVE`, and clearing
  the environment marker it uses to tell an agent from a human are my overrides,
  never yours.
```
It is written in the imperative and addressed to an agent. The content is defensive and harmless. Before adopting it, note that its last bullet claims a hook exists, which is only true once you've installed it.

**B. A recommendation to install third-party code into your Git hooks:**
> "It is at [martinfrancois/agent-git-guard](https://github.com/martinfrancois/agent-git-guard), with the caveats and a suite of 22 checks…"

A `pre-push` hook runs on every push you make. Read the code before installing it. I did not inspect this repo.

**C. The approval variable's name, planted where agents will read it:**
> "the hook honours `AGENT_GUARD_APPROVE=1`"

This is the variable that bypasses the guard. The article reports that it put the variable's name into `CLAUDE.md` during testing.

**D. The first line of the file is "raccoon".** It is unrelated to the article and has no apparent purpose. Most likely it is a scraping or pinning artifact, but it is not reader content.
