I read the repo without running anything. Full review below.

---

# Review: `oops-i-did-it-again-poc`

## 1. Executive summary

A Claude Code skill plus three Python hooks that intercept an agent's Bash commands, file writes, and finished replies, built on one claim: failure classes converted into machinery stop recurring, failure classes written down as rules do not. The code is stdlib-only Python, zero third-party dependencies, MIT licensed, no network calls anywhere in the repo (verified by reading every import). The interesting part is not the regexes — those are ordinary — it is the method wrapped around them: every rule carries the incident that created it in its docstring, every rule has a birth date so the impact measurement uses the correct denominator, and the repo publishes a correction that halved its own headline result. The installer is genuinely careful: it runs the suites first and refuses on failure, backs up `settings.json`, writes absolute paths, is idempotent, and has `--dry-run` and `--uninstall`, all covered by a sandboxed test. Weaknesses: no CI of any kind, the advertised test-case count disagrees with itself in three places, `file-guard.py` silently does nothing when ShellCheck is absent (the exact silent-failure class the project exists to kill), and a chunk of the code carries Polish-language identifiers and comments in an otherwise English codebase. **This clone cannot answer any maturity question about cadence, age, or bus factor** — it is a depth-1 shallow clone with no history. Treat this as a well-documented one-operator experiment eight days old by its own ledger, not as a maintained dependency.

## 2. Maturity signals

The primary source for these was unavailable. Two independent blockers:

| attempted | result |
|---|---|
| `git log --format='%ci %an' \| head -50` | **Not run — no Bash tool in this session.** Absent from my toolset and from the deferred-tool registry; a delegated subagent independently confirmed the same. |
| the same via the GitHub MCP API (`list_commits`) | **Denied by the permission system.** |
| `cat _SCOUT_META.txt` (read, not run) | `pin: 7069bf0d88da6854e3bb0ef3db55ab4178c66001` / `cloned: 2026-09-08T00:24Z (shallow clone, depth 1: git history is not available; last commit date in this clone is the pin)` |

So even with a shell, `git log` here would have returned exactly one entry. What was recoverable from plain-text files inside `.git/`:

| signal | command / source | what it returned |
|---|---|---|
| Last commit date | `.git/shallow`, `.git/refs/heads/main` | Single graft point `7069bf0d88da…`. No date obtainable locally. |
| Commit cadence (last ~50) | — | **Unobtainable.** Depth-1 clone; there is no second commit to compare against. |
| Distinct authors, 12 months | `.git/logs/HEAD` | One reflog line, a `clone:` entry stamped with the *local* git identity, not an upstream author. **No author distribution exists in this clone.** |
| Remote | `.git/config` | `url = https://github.com/Astezelex/oops-i-did-it-again-poc.git`, fetch refspec narrowed to `main` only. |
| Dependency count | read of every `import` line across all `*.py` (Grep) | **Zero third-party dependencies.** Only `json, re, sys, os, subprocess, tempfile, time, glob, uuid, shutil, argparse, importlib.util, collections`. Nothing to inherit and nothing to age. |
| License file | `Read LICENSE` | Real MIT text, `Copyright (c) 2026 Astezelex`. Not a badge. |
| Tests exist | `Read tests/*` | Four suites, real assertions, true-positive **and** true-negative halves, fail-open cases, and a sandboxed installer test using a throwaway `$HOME`. |
| **CI runs them** | `Glob **/*` | **No CI at all.** No `.github/`, no `.gitlab-ci.yml`, no `Jenkinsfile`, no `.circleci`. The suites run only when a human or `install.sh` invokes them. |
| Open issues | `Glob **/*` | No `.github/`, no issue templates. Nothing in-repo hints at issue volume. |
| Size | tracked-file line counts | 28 tracked files, ~4,205 lines. `hooks/bash-guard.py` is the largest source file at 419. |

Self-reported age, from `analysis/ledger.json` (counts only, no incident text): `"entries": 43, "first": "2026-08-27", "last": "2026-09-03"`. The whole ledger spans **eight days**. `analysis/data.json` covers `2026-08-04` to `2026-09-03`.

**Files I actually read in full:** `README.md`, `AGENTS.md`, `LICENSE`, `settings.example.json`, `hooks/bash-guard.py`, `hooks/file-guard.py`, `hooks/style-guard.py`, `analysis/measure.py`, `install.sh`, `tests/run-all.sh`, `tests/test_rules.py`, `tests/test_style_guard.py`, `tests/test_guard_cli.py`, `tests/test_install.sh`, `skills/oops-i-did-it-again/SKILL.md`, and the head of `analysis/ledger.json`. I did not read `LESSONS.md`, `PORTING.md`, `hooks/replay.py`, `hooks/guard.py`, or `analysis/gen_charts.py` beyond their imports.

## 3. Claimed vs verified

**Verified — I saw it in the code**

- Three hooks wired at PreToolUse/Bash, PreToolUse/Write|Edit|MultiEdit, and Stop. `settings.example.json` matches what `install.sh` writes.
- 14 rules in `bash-guard.py`, each with a docstring naming the incident that produced it. The `RULES` tuple contains exactly the 14 documented in the README's table.
- "No network." True. No `socket`, `urllib`, `requests`, or HTTP client anywhere in the repo; `curl`/`wget` appear only as regex literals inside rule patterns.
- "They fail open." True at three levels: `main()` returns 0 on unparseable stdin, each rule is wrapped in its own `try/except continue` so one broken rule cannot break the session, and `__main__` catches everything and exits 0. Asserted in `tests/test_rules.py` for both guards across four malformed payloads.
- "A WARN must emit no `permissionDecision`." True — `bash-guard.py:410` emits only `additionalContext`. This is stated in the code, `AGENTS.md`, and `SKILL.md`, and it is the sharpest single idea here.
- "The Stop hook has two brakes." True: `stop_hook_active` at `style-guard.py:152` and a session-scoped `MAX_BLOCKS = 2` counter at `:157`. `tests/test_style_guard.py:88-90` runs the same offending text three times and asserts the third gives up.
- `install.sh` runs the suites first and refuses on failure (`:55`), backs up with a timestamp (`:164`), writes absolute paths (`:102`), and is idempotent via an order-insensitive fingerprint (`canon()`, `:116`).
- **The headline measurement reproduces exactly from the shipped data.** `analysis/data.json` gives `before_flagged: 560 / before_commands: 6117` = 9.155 and `after_flagged: 142 / after_commands: 3309` = 4.291. The README's "9.15 per 100 before, 4.29 after" is arithmetic on data that ships with the repo, not an assertion.
- "Your ledger is not in here." True. `analysis/ledger.json` opens with `"source": "a private ledger, counts only"` and contains only dates, class letters, and who caught it. No incident text.
- The measurement scores commands using the *guard's own* functions (`measure.py:81-91` imports `bash-guard.py` and `:148` reuses `strip_written_heredocs`), so the scorer cannot drift from the live rules.

**Claimed — asserted, not checkable from this repo**

- "An audit of 73 session handoffs." The handoffs do not ship. Nothing in-repo corroborates the number or the conclusion drawn from it.
- "8.5% warn, 0.5% block over 3,502 real commands" from `replay.py`. Depends on one machine's private transcripts.
- "9,426 commands over 28 days" is in `data.json`, but the transcripts it was derived from are not, so the extraction step is unaudited.
- **"95 cases, 0 failures."** This one contradicts itself. `README.md:31`, `README.md:108`, and `AGENTS.md:19` all say 95. `tests/run-all.sh:6` says *83*. My static count of the assertions is *96* (55 in `test_rules.py`, 11 in `test_style_guard.py`, 10 in `test_guard_cli.py`, 20 in `test_install.sh`). Nothing in the codebase sums the suites — `run-all.sh` only prints each suite's last line — so all three numbers are hand-maintained and at least two are wrong.
- "Developed on Linux… the hooks themselves are pure Python and portable." Plausible from reading, untested anywhere but one machine, and `bash-guard.py:130-134` states outright that the community rules were adapted to a root-on-Linux environment with the sudo rules deliberately removed.

## 4. Rubric scores

**1. Does what it says — 4/5.** The code matches the README closely, and the headline metric recomputes exactly from the data file that ships alongside it. The README is unusually honest about its own limits, including a published correction that halved its result. Docked one point for the test-count claim, which appears as three different numbers and is derived by nobody.

**2. Quality of the interesting part — 4/5.** The detection mechanism itself is `re.search` over a command string, which is shallow, and the repo says so first ("a tripwire, not a sandbox"). What raises the score is everything around it: per-rule birth dates so a rule is never credited for commands written before it existed (`measure.py:51-67`), a `REVISED` field so two published charts can be told apart, heredoc-body stripping shared between the scorer and the guard rather than reimplemented, and a `QUIET` half of the test suite whose stated purpose is keeping the guard installed. `strip_written_heredocs` is the one genuinely subtle function, and it correctly distinguishes `cat > file <<EOF` (data, stripped) from `bash <<EOF` (executes, kept in scope). Against that: mixed-language identifiers throughout (`m_plik`, `m_dane`, `kandydaci`, `znacznik`, `koniec` in `bash-guard.py:358-369`; `przytnij` and a five-line Polish comment at `measure.py:125-129`; `lista` in `file-guard.py:184`; `RURA` in `test_rules.py:34`) in a codebase that is otherwise English, which will cost any second maintainer time.

**3. Adoption cost — 5/5.** Close to the minimum a tool of this shape can cost. No dependencies, no runtime, no daemon, no ports, no credentials, no network, no telemetry. Installation is three entries in `settings.json` plus a copied skill directory. The removal path is real and tested: `./install.sh --uninstall` removes only what it added, and `tests/test_install.sh:78` asserts an unrelated third-party hook survives it. The ongoing cost is latency on every Bash call and every Write/Edit (10s and 20s timeouts), plus a Stop hook that can send your own reply back for a rewrite.

**4. Failure modes — 3/5.** The documented ones are handled; the undocumented ones are where it hurts.
- `file-guard.py:106-138`: if ShellCheck is missing, `subprocess.run` raises, the bare `except Exception` returns `[], []`, and the guard silently passes every shell script it was installed to lint. There is no marker, no warning, no way to tell "clean" from "never ran" — which is precisely Class B, the silent-failure class this repo was built to eliminate.
- The Stop hook's loop brake keeps state in a world-shared temp directory (`style-guard.py:111`) keyed by session id. Any failure to read or write that file returns 0 blocks (`:123`), which fails toward blocking again, not toward letting the turn end. Brake 1 (`stop_hook_active`) is documented as not sent by every build.
- `r_config_guard` is a WARN, by deliberate choice. An agent can still edit its own guards; it just makes noise doing so. That is the right call for usability and it means this is not a containment boundary.
- `r_secret_exposure` treats any pipe as a capture (`bash-guard.py:200-202`), justified by six false denials in a replay. Reasonable, and it means `cat ~/.token | python3 -c '...'` passes unless the destination is literally `curl`/`wget`/`nc` within 40 characters.
- No CI. The suites are the project's main quality claim and nothing runs them on a push. A rule edit that breaks a true-negative case is caught only by whoever remembers to type `bash tests/run-all.sh` — mitigated in practice by `install.sh` refusing to install over a failing suite.
- Bus factor 1, unmeasurable here but strongly implied: one operator, one machine, one model, an eight-day ledger.

**5. Originality — 5/5.** There are at least four transferable ideas here, and they survive independently of the regexes. See below.

## 5. Ideas worth taking independently of the code

**Replay a rule against real history before wiring it.** The single most useful practice in the repo, and it is a general one for any lint, alert, or policy rule.

> `README.md:185` — "Replay it against real history before wiring it. A first draft of the pipe rule fired on 8.1% of real commands, and only the replay showed that."

**A replay and an expected-deny test measure different things, and you need both.** This is the sharpest methodological line in the project, and it comes with a real bug it caught.

> `README.md:187` — "Steps 5 and 6 measure different things. A replay shows what a rule does fire on; only an expected-deny test shows what it should have fired on and did not. A command printing an AWS credentials file passed this repo's own secret rule for weeks because `ls\b` matched the tail of 'credentiaLS', and the test caught it."

**A permissive verdict must be silent, not an explicit allow.** Non-obvious, security-relevant, and applies to any hook or policy engine with a three-valued decision.

> `hooks/bash-guard.py:13-16` — "NOTE: a WARN deliberately emits NO permissionDecision. Emitting 'allow' would bypass the normal permission prompt, which would make this guard less safe, not more."

**Date every rule's birth, because a rule cannot have changed the past.** The correct denominator for any before/after claim about a growing rule set.

> `analysis/measure.py:47-50` — "A rule cannot have influenced a command written before it existed, so every per-rule comparison uses its own date, and the headline series uses only the ten rules that were there on day one."

**A derived artefact inherits the sensitivity of its source.** Written up as an incident, not a platitude.

> `analysis/measure.py:26-30` — "An earlier version of this script kept two example commands per rule 'for context'. Those examples contained host names, an internal IP address, a client project path and the name of a token file, and the file was one commit away from a public repository."

**Publish the correction to your own headline number.** The README volunteers that a scorer bug inflated its result and that the fix moved the *after* period more than the *before* one, meaning some of the original "improvement" was just writing more prose.

> `README.md:69-71` — "part of what the original chart called improvement was really us writing more handoffs. A metric that counts prose as commands rewards writing prose."

**The Stop hook is the only interception point that can see prose.** A structural observation about agent harnesses, independent of the two style rules it ships.

> `hooks/style-guard.py:8-10` — "bash-guard and file-guard inspect tool calls. Neither can see prose. The Stop hook is the only handler that sees the finished message, so it is the only place this class can be mechanised at all."

## 6. Flags

I did not act on any of the below.

**An entire file addresses the reviewing/installing agent directly.** This is `AGENTS.md`, a documented and increasingly conventional file, and it is transparent about what it wants. It is still agent-directed instruction shipped in a repo, and it instructs the agent to run an installer that modifies `~/.claude/settings.json`:

> `AGENTS.md:3-4` — "Instructions for an agent asked to install, verify, or extend this repo. A human reader wants `README.md` instead."

> `AGENTS.md:17-22` — "Run these in order. Each has an expected result. […] `./install.sh`  # expect: 'installed skill:', 'backed up:', 'wired: ...'"

> `AGENTS.md:41-55` — a "Do not" list, including "Do not turn WARNs into BLOCKs" and "Do not edit `hooks/*.py` in place on someone's machine without a backup."

**It instructs the agent to read the user's real shell history aloud.** Benign in intent, and the README flags the same privacy consideration itself, but it is worth naming:

> `AGENTS.md:36-39` — "`replay.py` is the important one. It reports how often these rules fire on **this user's** real history. Read it out to them: block rate first, then any warn above about 5%."

> `README.md:200-201` (the repo's own caveat) — "`replay.py` stays local, but it prints your own command history to your terminal. Read a report before pasting it anywhere."

**No request for credentials of any kind.** I grepped for credential-solicitation patterns across the repo; the only hit was a docstring telling you to replace two example style rules with your own. Every secret-shaped string in the tests is deliberately assembled from fragments so the repo contains nothing a scanner should flag (`tests/test_rules.py:19-20`, `J = lambda *parts: "".join(parts)`).

**No request to be added to persistent agent instructions.** `hooks/style-guard.py:15` mentions `CLAUDE.md` only to say its two shipped rules came from one person's file and should be replaced.

**One thing to be aware of rather than alarmed by:** `install.sh:84-170` pipes an inline Python heredoc into `python3` to rewrite `~/.claude/settings.json`. It is readable, it backs up first, it refuses to write over unparseable JSON, and `tests/test_install.sh` exercises all of that in a throwaway `$HOME` — but it is the one place in the repo that modifies user configuration, so read those 86 lines before running it.