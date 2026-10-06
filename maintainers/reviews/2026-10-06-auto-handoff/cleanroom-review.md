# auto-handoff: standalone review

**Files read:** `README.md`, `LICENSE`, `.gitignore`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `hooks/hooks.json` (entry point, which loads only `./register.ts`), `hooks/register.ts`, `types/index.d.ts`, `skills/handoff/SKILL.md`, `tests/auto-handoff.test.ts`, `.git/config`, `.git/shallow`, `.git/logs/HEAD`.

**Limit on this review:** I had no shell, so I could not run `git log` or any other command. The git signals below come from reading `.git/` files directly, and I mark where that falls short.

## 1. Executive summary

- **What it is:** a Claude Code plugin of about 145 lines of TypeScript. After a main-loop turn ends, it waits 50 minutes, then runs a slash command (by default a bundled `handoff` skill). The skill writes `docs/handoffs/<timestamp>-<slug>.md` while the one-hour prompt cache is still warm.
- **Main logic:** the timer code is careful. It rearms after a reload and avoids a race when a turn starts as the timer fires. It hands off once per absence and skips the handoff if the timer fires late (the machine slept). It treats only some prompt origins as "the person is back".
- **Tests:** seven behavioural tests run against a mocked clock. There is no CI config, so the tests are claimed, not verified to run.
- **Dependencies:** none. No `package.json`; the only import is the host-provided `'claude-code'` module. The README says the API it uses is early access, so the real maintenance risk is churn in the host API.
- **History:** a shallow clone with one commit (`19405aa`) by a single author named in the manifest. Cadence and bus factor can't be assessed beyond that.
- **Main risks:**
  - An unproven assumption about the origin of the plugin's own `$.command.run`. If it is a "person" origin, the plugin would hand off every 50 minutes for as long as you're away.
  - Handoff files hold conversation contents, are written into the repo tree, and are not gitignored.
- **Verdict:** small, readable and easy to remove. Worth adopting or copying from, as long as you accept that the plugin API is early access.

## 2. Maturity signals

| Signal | Command / method | Result |
|---|---|---|
| Last commit date | `git log -1 --format=%ci` (**not run, no shell**). Read `.git/logs/HEAD` instead | The reflog only shows the local clone at Unix time `1791267301` (about 2026-10-04). The commit's own date is in a compressed pack and I couldn't read it. Session context lists one commit, `19405aa Add auto-handoff plugin for Claude Code`. |
| Commit cadence (last ~50) | `git log --format='%ci %an' \| head -50` (**not run**). Read `.git/shallow` | `.git/shallow` contains `19405aa…`, so this is a depth-1 shallow clone. Only one commit is visible and cadence can't be judged. |
| Distinct authors, 12 months | same (**not run**) | Unknown from git. The manifests name a single author, "Obie Fernandez" (`plugin.json`, `marketplace.json`, `LICENSE`). Treat it as a one-person project. |
| Dependencies | Glob for manifests | No `package.json`, lockfile or `node_modules`. The only import is `'claude-code'` / `'claude-code/testing'`, which the host provides. `.gitignore` excludes `node_modules/` and `tsconfig.json`. |
| License file | Read `LICENSE` | MIT, "Copyright (c) 2026 Obie Fernandez". Present and standard. |
| Tests exist / CI runs them | Glob `**/*`, `.*/**/*` | `tests/auto-handoff.test.ts` exists with 7 tests. There is **no `.github/` directory or any other CI config**, so the tests are claimed, not verified. |
| Open issues | n/a | No `.github/` or issue templates, and I made no network access. Not assessed. |
| Version | `plugin.json` | `0.1.0` |

## 3. Claimed vs verified

**Claimed only (README or manifest says it; I couldn't confirm):**
- It was developed and tested on Claude Code 2.1.289.
- `claude plugin test .` runs the tests and they pass. Nothing shows they have ever run.
- The host fills `options` from `userConfig` defaults. The code relies on this for `command`: `String(undefined)` would yield `"undefined"`.
- A reload "drops the timer and keeps the state" (host behaviour).
- The skill completes in the default permission mode because of `allowed-tools`. This depends on the host's permission matcher accepting the compound command `date …; git status …` under `Bash(date *)` and `Bash(git status *)`.
- The plugin's own `$.command.run` does not fire `command.run` with a "person" origin. Nothing states this, but the "one handoff per absence" claim depends on it.

**Verified in the code:**
- **Idle clock:** armed at `turn.complete` only when `e.agentId === undefined` (`hooks/register.ts:126-136`). Disarmed at every `turn.start` (`:119-124`). Subagents are excluded.
- **One handoff per absence:** `isDone` is set before the command runs (`:54-56`). It is reset only for origins in `PERSON` (`:21-27`, `:81-85`).
- **`/clear` cancels:** `session.end` disarms and clears state (`:138-144`). It does this for every end reason, not just clear.
- **Late-fire skip:** skipped if `idle - wait > wait * 0.1` (`:17`, `:60-64`). With the 50-minute default that means more than 5 minutes late.
- **Reload resume:** `session.start` rearms from the stored `idleSince` with the remaining time (`:96-105`).
- **Race guard:** if `idleSince` is null when the timer fires, a turn has started, so it doesn't hand off (`:48-51`).
- **Options:** `minutes` falls back to 50 when it isn't positive. A leading `/` is stripped from `command` (`:88-92`).
- **Skill:** pre-approves only `Write`/`Edit` under `docs/handoffs/**`, `date`, `git status` and `mkdir -p docs/handoffs` (`skills/handoff/SKILL.md:4`). It tells the model to commit nothing.
- **Tests:** they cover the 50-minute firing, reset on a new turn, once per absence (including that a task notification doesn't reset it), subagent exclusion, `/clear`, sleep skip, and options (`tests/auto-handoff.test.ts`).

## 4. Rubric

| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Does what it says | **4** | Every README behaviour has matching code and a test. One gap: the claim that the plugin stays quiet during the handoff's own command rests on an untested assumption about the origin `$.command.run` reports. The test's stub handler for `command.run` may intercept it before the plugin sees it. |
| 2 | Quality of the core | **4** | It's a small but real state machine, not glue around another tool. The comments explain *why*, and the edge cases (race, reload, sleep) are handled. Weak points: `'auto-continuation'` and `'sdk'` count as "person is back" origins (debatable), and a failed or skipped handoff is never retried. |
| 3 | Adoption cost | **5** | No deps, ports, credentials or runtime beyond Claude Code. Removal is `/plugin uninstall` plus deleting `docs/handoffs/`. The ongoing cost is tracking an early-access hooks API. |
| 4 | Failure modes | **3** | (a) If the plugin's own command counts as a person origin, it would hand off every 50 minutes while you're away, costing a cached read each time and growing the files. (b) Handoff files land in the project tree, are not gitignored, and may contain secrets or details from the conversation, so a `git add -A` would commit them. (c) The 50-minute default is wrong for sessions on the 5-minute cache, and the README says the plugin can't detect this. (d) The skill runs with no one present. If the model reaches for a tool that isn't pre-approved, the turn waits at a permission prompt and nothing is written (README states this). (e) A one-person project on early-access APIs. |
| 5 | Originality | **4** | Timing an automatic action to the prompt cache TTL is a new and specific idea. The late-timer sleep detection and the person-vs-automation origin split are clean techniques. |

## 5. Ideas worth taking

1. **Act just before the prompt cache expires, not after.** The plugin times the action to when cached re-reading is still cheap.
   > "When a session has sat idle for 50 minutes it runs a handoff command while the cache is still warm" (`README.md:7`)

2. **Use a late timer to detect that the machine slept,** and skip work that would now be expensive.
   > "A machine that slept through the wait wakes with the cache already cold, and a handoff then rereads the whole conversation at full price with nobody there to want it." `const LATE_SHARE = 0.1` (`hooks/register.ts:14-17`)

3. **Tell human input apart from automated input** before resetting "user is back" state.
   > "The origins that mean the person is back. A background task's notification or a scheduled trigger starts a turn too, and neither says anyone is here." (`hooks/register.ts:19-20`)

4. **Set the "done" latch before the action runs,** so the action's own side effects can't trigger it again.
   > "Set before the command runs, so its own turn does not arm the timer again and hand off every `wait` for as long as the person is away." (`hooks/register.ts:54-55`)

5. **Write skills for unattended runs with a tight set of pre-approved tools and few tool calls,** and explain the cost reason to the model.
   > "Skip any other investigation, because every extra tool call rereads the whole conversation." (`skills/handoff/SKILL.md:17`)
   > "The steps below are pre-approved. Any other command or file write may raise a permission prompt that nobody is there to answer…" (`skills/handoff/SKILL.md:13`)

6. **A fixed handoff template** that covers dead ends and standing instructions, not just status.
   > "**Dead ends**: what was tried and failed, so the next session skips it." … "Record any standing instructions the person gave about how to work, since the next session will not have heard them." (`skills/handoff/SKILL.md:30,36`)

7. **Test timer logic by shifting stored state instead of moving the clock,** when the mocked clock fires timers exactly on time.
   > "The mocked clock fires a timer the moment it is due, so the sleep is told the other way round: the idle clock is recorded three hours back." (`tests/auto-handoff.test.ts:110-111`)

## 6. Flags

**Nothing in the repo addresses the reviewing agent, asks to be added to agent instructions, or asks for credentials.**

One item to note, though it falls short of a flag: `skills/handoff/SKILL.md` gives instructions to the model that will run the skill. That is the skill's intended purpose. It includes:

> "Ask no questions and wait for no confirmation." (`skills/handoff/SKILL.md:11`)

> `allowed-tools: Write(docs/handoffs/**), Edit(docs/handoffs/**), Bash(date *), Bash(git status *), Bash(mkdir -p docs/handoffs*)` (`skills/handoff/SKILL.md:4`)

The pre-approval is narrow: writes only under `docs/handoffs/`, and only read-only shell commands. Users who swap in their own `command` are told to grant their own `allowed-tools` (`README.md:49`). That widens what runs with no one present, so review any replacement command with that in mind.