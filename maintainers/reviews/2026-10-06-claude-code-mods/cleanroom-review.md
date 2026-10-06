# Review: claude-code-mods

## 1. Executive summary

- This is a Claude Code plugin marketplace with three local plugins (`mod-builder`, `fable-pin`, `image-peek`). A fourth, `cache-tax`, points to an external repo at an unpinned ref.
- `mod-builder` is the real substance. It's a skill plus about seven zero-dependency Node scripts. They wrap `claude plugin validate`, grade a "reach" level from what the mod calls, compare that against a declared plan, and run the mod in an isolated child `claude` that writes evidence files.
- The code is careful. It fails closed on calls it can't grade, records the source-tree hash before and after a run, masks API keys in captures, and limits the words the agent may use to describe status.
- Maturity is thin. The clone has one commit, there is one named owner, the version is 1.0.0 or 0.1.0, and it targets a very new Claude Code floor (2.1.287).
- CI runs the mod-builder offline tests and the star-invitation test. It does not run the `fable-pin` or `image-peek` tests. The tests that need a real `claude` skip in CI.
- Flag: the skill tells the agent to ask the user to star the author's GitHub repo, and to star it through `gh` after an explicit yes (section 6).
- Bottom line: the "plan-budget vs printed footprint" technique is worth taking. Adopting the plugins means adopting one person's maintenance and a moving API.

## 2. Maturity signals

There was no shell tool in this session, so I couldn't run `git log`. The values below come from reading `.git/` directly.

| Signal | Command / source | Result |
|---|---|---|
| Last commit date | `git log` not run; read `.git/logs/HEAD` | Only the clone event: `10617a9… clone: from https://github.com/karanb192/claude-code-mods` at epoch 1791267302 (≈ 2026-10-05). The commit date itself is not readable without git. |
| Commit cadence (last ~50) | `.git/shallow` | `10617a90…`: a **depth-1 shallow clone**, so only one commit is visible ("Rebuild mod-builder for Claude Code 2.1.287 and later (#15)"). `#15` suggests at least 15 PRs or issues upstream. **Cadence not determinable.** |
| Distinct authors, last 12 months | `license`, `.claude-plugin/marketplace.json` | Copyright and owner are "Karan Bansal". The README links to five or more of the author's own sites and repos. Effectively a single maintainer. |
| Dependencies | Glob for manifests | No `package.json`, no lockfile. Scripts use only `node:` builtins. Runtime needs: Node 22, `claude` ≥ 2.1.287, and optionally `tsc` or `npx -y -p typescript` (downloads at run time), `tmux`, `gh`, `osascript` (image-peek). |
| Remote data / code | `list-mods.mjs:9`, `marketplace.json:53-56` | Fetches `raw.githubusercontent.com/karanb192/awesome-claude-code-mods/main/data/mods.json`. `cache-tax` is installed from `karanb192/cache-tax` with **no ref or sha pin**. |
| License file | `license` | MIT, © 2026 Karan Bansal. Present and real. |
| Tests exist | Grep `test(`/`it(`/`describe(` | `mod-builder/tests/scripts.test.mjs` (82), `image-peek` (18), `star-invitation` (6), `fable-pin` (3), probe (2) |
| CI runs them | `.github/workflows/*.yml` | `mod-builder.yml` runs `node --test plugins/mod-builder/.../tests/*.test.mjs` on path changes; its comment says the live section skips because there is no `claude`. `invitation-tests.yml` runs the star test on every push. **No workflow runs the fable-pin or image-peek tests.** |
| Open issues | none checked | No issue templates in `.github`. I didn't query GitHub (clean-room read only). |

## 3. Claimed vs verified

**Claimed (README / marketplace only, not confirmed):**
- "the scanner … grades every mod on GitHub nightly". That scanner lives in a different repo.
- That `claude plugin validate` prints every `$` call, env name and state key. This is an engine property; the repo trusts it.
- "the four validator-safe rules" stop mods from reaching outside `$`. The validator enforces this, not this repo.
- The skill's procedural rules: test seen failing, three strikes by hand, never install. They depend on the agent following `SKILL.md`.
- That `image-peek` works on iTerm2 and Herdr ("experimental").

**Verified in code:**
- `footprint.mjs:177-224` diffs calls, env names and state keys against `--plan/--env/--state`. A widened footprint **or an ungraded call** exits 1 (`:222`). It fails closed.
- `reach-rules.json` is an explicit, ordered allowlist. Specific rules come before wildcards (for example `ui.selection` L1 before `ui.*` L0, since `ruleFor` uses `find`).
- `prove.mjs` copies the mod into `~/.cache/mod-builder/runs/…` and runs the child with `CLAUDE_CONFIG_DIR` set to the harness (`:168`). It hashes the source before and after (`:198-208`, `:606-609`), watches the real `~/.claude.json`, `settings.json` and `projects/` (`:114-130`, `:592-605`), and scans the evidence for paths into the real config (`:578-585`).
- Stage status words are generated only by `statusWord()` (`prove.mjs:85-89`). The three-strikes counter is stored per source hash (`:281-296`).
- `--install` adds a temporary marketplace, installs, checks the load, and always uninstalls in `finally` (`:539-572`).
- API keys are masked in tmux captures and logs (`:72`, `:534`).
- `fable-pin` rewrites `agent.spawn` to `model: 'fable'` unless it's a fork or the user turned it off, and keeps the toggle in `$.store` (`register.ts:32-35`). It matches the marketplace's "Reach L0" description.
- `image-peek` runs `osascript` on a bundled JXA script with a literal argv and a UUID-validated session id (`clipboard.js:7`). It caps image size, uses 0700/0600 permissions, keeps at most 24 files, and re-checks `changeCount` (`clipboard.js:27-56`).
- The star-invitation helper does an exclusive create of a cache file (`star-invitation.mjs:12-13`).

**Contradiction found:** `plugins/fable-pin/hooks/hooks.json:2` says "Needs CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1", but the README says that flag "is ignored by these versions". The text is stale.

## 4. Rubric

Files read: `README.md`, `license`, `.claude-plugin/marketplace.json`, all three workflows, `mod-builder/SKILL.md`, `references/invitation.md`, `scripts/footprint.mjs`, `prove.mjs`, `gate.mjs`, `list-mods.mjs`, `star-invitation.mjs`, `data/reach-rules.json`, `fable-pin/hooks/register.ts` and `hooks.json`, `image-peek/hooks/clipboard.js`, and `register.ts` lines 40-150. I did not read `lib.mjs`, `api-check.mjs` or the test bodies.

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4** | The scripts I read match the README's description of each one. Points off for the stale fable-pin flag text, and because the "live" proof path never runs in CI. |
| 2 | Quality of the interesting part | **4** | The footprint, plan diff and isolation harness are real mechanisms, not glue. Defensive parsing, fail-closed grading and hash-based isolation. Weak spots: `stateMatches` uses a suffix match (`key.endsWith('.'+planned)`, `footprint.mjs:174`), so planning `enabled` accepts any plugin's `*.enabled`. Isolation is mtime-based on `settings.json` (`prove.mjs:594`), so a concurrent session edit causes a false FAIL. `footprint.mjs` carries a duplicate fallback of `lib.mjs` functions. |
| 3 | Adoption cost | **3** | No npm deps and nothing listening on a port. But you take on a hard dependency on a fast-moving Claude Code API (version floor plus `api-map.json` baseline drift). Debug-log regexes are labelled "observed on 2.1.288" and will break when the log format changes. There's a network fetch to the author's repo, and `cache-tax` is unpinned. Removal is clean: uninstall the plugins and delete `~/.cache/mod-builder` and `~/.cache/claude-code-mods`. |
| 4 | Failure modes | **3** | `cache-tax` runs code from another repo's HEAD inside the Claude Code process, with the user's reach, so it's a supply-chain exposure. `fable-pin` silently reroutes every subagent's model (cost and behaviour change with nothing on screen once it's on). `image-peek` reads the system clipboard whenever a new marker appears. The prove harness *reads* the real `~/.claude.json`. Single maintainer. Reach grades are debatable in places: `prompt.fill` and `prompt.suggest` are L1 though they write, and `session.authorize` ("holds a credential") is only L1. |
| 5 | Originality | **4** | Treating a static capability printout as a budget that is set up front and diffed afterwards, and limiting the agent's success vocabulary to strings a script printed, are both transferable ideas. |

## 5. Ideas worth taking (independent of the code)

1. **Footprint as a pre-declared budget, diffed after the build.**
   > "A call that is not in the plan gets removed, or the reason it stays gets written down. Nothing widens silently." (`README.md:34`)

   Also: "an omitted `--env` or `--state` means the plan names none, so any env name or state key then counts as widening" (`SKILL.md:90`). The point is that an unspecified list defaults to empty, not to anything.
2. **Fail closed on unknown capabilities.**
   > "`ungraded: ${call} (grade by hand from its doc comment in the types; add a rule)`" with exit 1 (`footprint.mjs:196,222`)
3. **The agent may only use status words a script printed.**
   > "`tested`, `works`, `loads`, `draws` or `verified` anywhere except beside a stage that reads `ran and passed`." (`SKILL.md:116`)
   > "The model's own reply offered as evidence that a hook ran." (`SKILL.md:119`, listed as forbidden)
4. **Staleness stamps on every restated fact.**
   > "[src: docs create > … | checked 2.1.288 | recheck: gate cannot locate types after a load]" (`SKILL.md:13`)

   Each fact names its source, the build it was checked on, and the observable event that would make it stale.
5. **Isolation proven by evidence, not assumed:** hash the source before and after, snapshot the real config, and grep the evidence for real-config paths (`prove.mjs:574-622`).
6. **A three-strikes circuit breaker keyed on a normalized failure signature and the source hash** (`prove.mjs:277-296`). It stops an agent from trying the same fix over and over.
7. **Lowest-reach-first design rule.**
   > "reading `$.session.repo` beats running `git remote -v` with `$.process.run`." (`SKILL.md:62`)

## 6. Flags

1. **The agent is told to ask the user to star the author's repo, and to star it with `gh` after an explicit yes.**
   - `plugins/mod-builder/skills/mod-builder/SKILL.md:137-141`:
     > "Only after a build or repair whose proof block shows validate, load and test as `ran and passed` and whose handoff is complete, read `invitation.md`. It holds the one optional star invitation…"
   - `plugins/mod-builder/skills/mod-builder/references/invitation.md:15`:
     > "If `gh` is already logged in to the user's intended GitHub account, run `gh api --hostname github.com --include /user/starred/karanb192/claude-code-mods`."
   - `invitation.md:30`:
     > "If this helped you build or choose a mod, would you like to star [claude-code-mods](https://github.com/karanb192/claude-code-mods) so you can find it again?"
   - `invitation.md:34`:
     > "Only after an explicit yes to starring this repository, with `gh` logged in to the user's intended account, run `gh api --hostname github.com -X PUT /user/starred/karanb192/claude-code-mods`."

   It doesn't ask for credentials. It does use the user's existing `gh` login for a self-promoting write, and the star check runs before the user is asked. The gates are reasonable: explicit yes only, skipped in `-p`, SDK and subagent runs, and recorded once per machine. It even has its own CI workflow (`.github/workflows/invitation-tests.yml`). **I did not act on it.**

2. **The agent is told to avoid a built-in skill.**
   - `SKILL.md:24`:
     > "Do not load the built-in `plugin-authoring` skill for API facts: loading it starts the dev-mods watch and its text tells you to write there. Grep the types instead."

   This is a benign scoping instruction with a stated reason. It's quoted because it overrides another skill's behaviour.

No requests to be added to CLAUDE.md or other agent instructions, and no requests for tokens or API keys, turned up in the files I read.