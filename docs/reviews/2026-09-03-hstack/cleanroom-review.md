I have what I need. Full review below.

---

# Review: `hstack`

## 1. Executive summary

A single-author collection of 37 Claude Code lifecycle hooks that refuse agent actions, extracted from a private working config on 2026-09-03. The repo has exactly one commit, so there is no cadence, no second author, and no history to read.

The engineering around the hooks is unusually good and the hooks themselves are unusually specific. `hooks.manifest.json` is a real single source of truth, `tests/parity.py` enforces it, and `tests/dead-branch-sweep.py` is regex-scoped mutation testing with a self-test that proves the sweep can find a planted dead branch. CI runs on Ubuntu and macOS, shellchecks, and smoke-tests install → re-install → uninstall.

The gap is between the framing and the artifact. The README says "every guard is tested twice"; 26 of 37 hooks have no test case at all, including all six blocking `Stop` hooks. Six hooks are registered as bare `python`, which does not exist on a stock Mac, and `doctor.sh` silently substitutes `python3` and reports them armed — the exact "present, registered, never fires" failure the repo was built to detect. Twelve helper binaries the guards call are not shipped, so several guards no-op on a fresh install. Numbers in the README, CHANGELOG, SECURITY.md and ARCHITECTURE.md are stale wherever they are spelled as words, because the parity check only matches digits.

Worth reading for the ideas. Adopt selectively, hook by hook, not via `install.sh`.

## 2. Maturity signals

| Signal | Command | Output | Read |
|---|---|---|---|
| Last commit | `git log --format='%ci %an'` | `2026-09-03 11:52:33 +0900 Chak Hang (Howard) Chan` | Same day as review. Fresh. |
| Commit cadence | `git log --oneline \| wc -l` | `1` | No cadence exists. Squashed snapshot export; `git log --format='%ci %an' \| head -50` returns one line. |
| Distinct authors, 12mo | same | 1 (`chakhanghowardchan2008@gmail.com`) | Bus factor 1, and the code is written around one operator's workflow. |
| Remote / branches | `git remote -v`; `git branch -a` | `github.com/howardchan2008/hstack`; `main` only, no tags | No release tags despite `VERSION`=0.2.0 and a CHANGELOG. |
| Dependency count | manifest read; `grep` for imports | zero third-party | Python stdlib and bash only. Genuinely no inherited dependency surface. |
| License file | `cat LICENSE`; `wc -c LICENSE` | 290 bytes, `Copyright (c) 2026` | **Present but abridged and unnamed** — see rubric 3. |
| Tests exist | `ls tests/` | `run.sh`, `parity.py`, `negative-control.py`, `dead-branch-sweep.py` | Five-stage suite, real. |
| CI runs them | `cat .github/workflows/ci.yml` | `bash tests/run.sh` on `[ubuntu-latest, macos-latest]` + shellcheck + install-smoke | Verified: CI genuinely runs the suite, both platforms, plus idempotency and uninstall assertions. |
| Issue volume | `ls .github/ISSUE_TEMPLATE/` | `false-positive.md`, `guard-failed-open.md` | Two templates, both well-chosen. No issue history available offline. |
| Hook count | `ls hooks/*.sh \| wc -l` → 27; `ls hooks/*.py \| wc -l` → 10 | 37 total; manifest has 37 | Files and manifest agree. Prose does not. |

## 3. Claimed vs verified

### Verified (read it in the code or the log)

- **37 hooks, manifest and disk agree.** `parity.py` check 1 enforces both directions. The README table's per-event breakdown (17 PreToolUse / 2 PostToolUse / 4 SessionStart / 6 UserPromptSubmit / 8 Stop) is correct against the manifest.
- **`settings.example.json` is generated, not maintained.** `parity.py:43 build_settings()` and `install.sh:141 command_for()` produce the same shape; check 2 asserts equality.
- **No network calls, no telemetry.** Grepped `curl|wget|urllib|requests\.|http.client|socket` across `hooks/`: every hit is a detection pattern or a self-test fixture (`written-call-guard.py:145`, `capability-claim-gate.py:186`). SECURITY.md's claim holds.
- **Zero dependencies.** Stdlib Python, bash. Confirmed by reading every import.
- **CI actually runs the suite on both platforms**, and the install-smoke job asserts no duplicate registrations on second install and an empty settings file after uninstall. Those assertions are real code, not a badge.
- **The `--self-test` / `--dead-branch` layering works as described.** `dead-branch-sweep.py:133 self_test()` builds a fake hook with one covered and one uncovered regex and asserts the sweep flags exactly the uncovered one.
- **Scrubber damage survived into shipped files.** `docs/CORRECTIONS.md:35` contains the path `~/.the local proxy/events.jsonl`; `state-verify-inject.sh:113` and `linkedin-browser-ban.sh:61,235` read "the the local proxy"; `item-coverage.py:229` reads "the a venture evolution instance"; four places use "the owner 2026-07-11" as a sentence subject. The README's account of placeholder substitution producing nonsense is accurate, and some of it shipped.

### Claimed, and contradicted by the code

1. **"Thirty-one Claude Code hooks"** (`README.md:5`) — there are 37. `parity.py` check 5 exists precisely to catch this and cannot: its regex `\b(\w+)\s+hooks\b` captures `Code` from "Thirty-one Claude Code hooks", and its word list (`twelve, sixteen, twenty, twentyfive, eighteen, fifteen`) has no entry for thirty-one regardless.
2. **"every guard is tested twice: against the payload it must refuse, and against an ordinary payload it must let through"** (`README.md:88`) — `negative-control.py` has 20 cases covering 11 of 37 hooks. Only 6 hooks have both arms (dash-gate, grep-portability, ls-before-write, pipestatus-guard, risk-checkpoint, lane-guard). Five have an allow arm only. **26 hooks have no case at all**, including every one of the six blocking `Stop` hooks (`stop-justify`, `closeout-shape`, `item-coverage`, `capability-claim-gate`, `handoff-gate`, `person-claim-balance`) and both `block: "deny"` PreToolUse hooks. `docs/TESTING.md:79` discloses only the `agent-budget` gap.
3. **"`python3` for the four python hooks"** (`README.md:106`, echoed at `doctor.sh:37`) — there are 10 python hooks.
4. **Six hooks are registered to run under bare `python`.** `hooks.manifest.json` gives `"runner": "python"` for `item-coverage.py`, `capability-claim-gate.py`, `handoff-gate.py`, `written-call-guard.py`, `owner-facts.py`, `person-claim-balance.py`, so `install.sh:142` writes `python $HOME/.claude/hooks/item-coverage.py` into `settings.json` (confirmed in `settings.example.json:55,190,212,216,220,224`). Stock macOS has no `python` on PATH. **`doctor.sh` masks this in both places it could catch it** — `doctor.sh:114` accepts `shutil.which(runner) or shutil.which(runner + "3")`, and the liveness probe at `doctor.sh:129-131` re-resolves through the same fallback — so it executes the hook with `python3` and prints `armed`. CI passes because `actions/setup-python` puts `python` on PATH. This is the repo's own thesis failing on the repo: registered, documented, reported healthy, never runs.
5. **The same six files carry `#!$HOME/.venvs/agent-libs/bin/python`** as their shebang — an unexpanded variable pointing at the author's private venv. They are the newest hooks and were never normalized to the repo's `#!/usr/bin/env python3` convention. `parity.py` checks manifest, roster, docs and counts; it does not check that a `runner` resolves or that a shebang is valid.
6. **"State is written under `~/.claude/state/`"** (`SECURITY.md:20`, repeated in `ARCHITECTURE.md`) — hooks write to at least twelve distinct locations: `state/`, `carryover/`, `tasks/`, `logs/`, `context/`, `last-context/`, `stop-justify/`, `stop-justify-ignore`, `agent-dispatch/`, `agent-budget-audit/`, `closeout-advisory`, and `.burn-statusline-cache`. `--uninstall` removes none of them.
7. **"Twenty-five files of shell and python"** (`SECURITY.md:12`) and CHANGELOG's "Sixteen to twenty-five" — 41 files ship under `hooks/`. Twelve hooks appear in no changelog entry.
8. **`docs/ARCHITECTURE.md` prose is stale where the diagram is correct.** The ASCII diagram (6 / 17 of which 15 refuse / 8 of which 6 refuse / 4) is right, because `parity.py` check 6 validates digit-form numbers. Twenty lines later: "All five `UserPromptSubmit` hooks" (6) and "Nine of the twelve `PreToolUse` hooks and both blocking `Stop` hooks" (15 of 17; six blocking Stop hooks). Word-form numerals are unchecked, and `parity.py` check 5 only reads the README anyway.
9. **Twelve referenced helpers do not ship.** `~/.claude/bin/{claims-audit, websearch, exa, click-credits, pointer-check, guard-verdict, cc-whatsnew, gen-sot-digest.sh, verify-live.sh}` and `~/.claude/reference/{capability-routes.json, click-routing.md, keychain-use-cases.md}`. `ARCHITECTURE.md` discloses that ten private files are held back, which is honest, but does not say that guards depend on them. `curl-router.sh:44` is `[ -f "$ROUTES" ] || exit 0` — on a fresh install it is a permanent no-op. `websearch-router.sh` and `click-credit-guard.sh` are in the same position.
10. **`--uninstall` does not reverse the install.** `install.sh:220` prints "rules/ left in place: they are yours to keep or delete by hand". `README.md:99` says "`--uninstall` reverses it."
11. **A BSD-ism in a blocking path that CI cannot reach.** `curl-router.sh:48` uses `stat -f %m`, which is BSD-only. On Linux the `|| echo 0` fallback makes `age` enormous, so the override file is deleted *and* the block still applies — the documented escape hatch (`touch /tmp/curl-router-approved && re-run`) fails on Linux. CI never sees it because the guard exits at line 44 first, having no routes file.

## 4. Rubric

**1. Does what it says — 3/5.**
The mechanism is real and the hooks do refuse; the *inventory* claims are wrong in six places, and the testing claim ("every guard is tested twice") is true of 6 of 37 hooks. A repo whose stated purpose is catching confident-and-wrong claims ships several.

**2. Quality of the interesting part — 4/5.**
Not glue. `parity.py`, `dead-branch-sweep.py` and `doctor.sh` are the interesting files and each contains a mechanism I have not seen assembled this way. The hooks themselves are dense and heavily reasoned — `item-coverage.py` documents a backtest over a week of real turns with a threshold table (`MIN_TERMS` 3/4/5/6 against turns blocked) and states its own ceiling: "this guard sees about a third of what he asks for." That is the right way to ship a heuristic. Marked down because size is uncontrolled — `risk-checkpoint.sh` is 1,568 lines of bash and `stop-justify.sh` 1,297, both in the blocking path of every relevant call, both far past where shell is a reasonable medium.

**3. Adoption cost — 2/5.**
`install.sh` copies `rules/` (15 files, 903 lines of standing instructions) into `~/.claude/rules/`, where they load into every session in every project on the machine, and `--uninstall` deliberately leaves them. It registers 37 programs that execute before every matching tool call with your shell's privileges — correctly disclosed in `SECURITY.md`. Nine of the ten guards' worth of routing behaviour depends on helper binaries you do not have. Removal path: settings registrations and `hooks/` come out cleanly and idempotently (CI proves it); `rules/` and twelve state directories do not. The license is the sharper problem: `LICENSE` is 290 bytes, headed "MIT License", holding an unnamed `Copyright (c) 2026`, and it stops after "to deal in the Software without restriction." The grant of rights to copy/modify/distribute/sublicense, the attribution condition, and the liability limitation are all absent. It is not the MIT license and it is not obviously a valid grant. For a repo whose own README says "no license means no adoption," that is worth fixing before anything else here.

**4. Failure modes — 2/5.**
The dominant one is verified above: six hooks registered to a `python` that will not exist on the target platform, with the diagnostic tool substituting `python3` and reporting them armed. `doctor.sh` is the only thing standing between a user and that failure, and it is the thing that hides it. Beyond that: several guards no-op silently when their helper is missing (fail-open, deliberate and documented at `ARCHITECTURE.md`, but indistinguishable from a working guard with nothing to say — the exact rot the repo's own `warn` verdict was invented to catch, and the `warn` verdict is defined in `negative-control.py:251` and used by zero cases). Two hooks fail *closed* on an unparseable payload (`click-credit-guard.sh:48`, `lane-guard.sh`), which means a missing `/usr/bin/python3` blocks every matching call. No lock-in: hooks are independent files, deletable one at a time. No unmaintained transitive deps, because there are none.

**5. Originality — 4/5.**
`dead-branch-sweep.py` alone justifies reading the repo. The framing that a dead *detector* under-blocks while a dead *exemption* over-blocks — and that these need different test arms — is a real distinction I have not seen stated. `doctor.sh`'s POISON list is a genuine field observation. The negative-control discipline is not novel in testing generally, but its application to agent guards, with the two-arm requirement enforced in the suite, is the right idea.

## 5. Ideas worth taking independently of the code

**Mutation-test your regexes, and self-test the mutation tester.** `tests/dead-branch-sweep.py:1`

> "corrupt one regex at a time so it can never match, re-run that hook's own self-test, and report every regex the test did not miss. […] Run against the private tree this was built from, the first sweep found 31 dead regexes across the hooks and the surrounding CLI. […] Three were not merely untested but unreachable: an exemption applied only to sentences another regex had already matched, where the two word lists were disjoint, so it could never exempt anything."

The paired insight is that the sweep needs its own positive control (`dead-branch-sweep.py:133`), or "no dead branches found" is unfalsifiable.

**Direction decides the test arm.** `tests/dead-branch-sweep.py:21`

> "A dead DETECTOR under-blocks: the rule silently stops firing. A dead EXEMPTION over-blocks, which is worse, because an over-blocking guard gets bypassed or deleted rather than obeyed."

**A checker must not be able to match its own documentation.** `tests/parity.py:192`

> "The first version grepped raw text and could not fail: deleting the real `"decision"` object from a hook left the WORD in the comment above it, and the check stayed green against the exact bug it was written for. A checker that matches prose is measuring documentation."

The fix — parse with `ast` and distinguish a dict *literal* key from a `.get()` read (`parity.py:230`) — is the generalizable part: a text match cannot tell emitting from referencing.

**Negative controls for capability probes.** `docs/TESTING.md:48`

> "A credential probe reported 51 slots live. Re-running each probe with a deliberately corrupted key showed 5 of them still passing, so for those, 'live' carried no information: the probe was reading a status endpoint that answers before it looks at credentials."

Applies to any health check anywhere. Feed it a broken world; if it still says healthy, it measures nothing.

**Config keys that silently disable an entire subsystem.** `doctor.sh:73`

> "Some settings keys make Claude Code drop the ENTIRE hooks block of the file that contains them. The file still parses, nothing warns, and checks 1 to 4 above all pass, because every one of them is true of a hook that never runs. […] `fallbackModel` and `workflowSizeGuideline` each did it."

Verify by side effect, not by configuration state. (The note correctly adds "Re-verify against your own version before trusting this list either way.")

**State a heuristic's ceiling in the file that implements it.** `hooks/item-coverage.py:213`

> "MIN_TERMS items judged turns blocked / 3 59.8% 39.3% / 4 47.9% 28.5% / 5 36.5% 20.6% / 6 24.8% 12.4% — Five is chosen and the ceiling that comes with it is real: this guard sees about a third of what he asks for. […] so it is a floor under the worst omissions, never a proof that a turn was complete."

**Publishing a redaction tool publishes the redaction list.** `README.md:113`

> "a scrubber's rules are a list of every private string it knows about, so including it for transparency would have published exactly the thing it removes. Transparency about a redaction cannot be the redaction list."

**One fact, one place, and generate the copies.** `docs/ARCHITECTURE.md` — `hooks.manifest.json` is read by the installer, the doctor, the parity check and the generated example settings. The idea is sound; the repo's own residual drift (six stale counts, all in word-form numerals) is the argument for making the generator cover prose too, not against the pattern.

## 6. Flags

Nothing in this repo asks for credentials, asks to be added to agent instructions covertly, or attempts to redirect a reviewing agent. The items below are disclosed behaviour, reported because they address an agent directly and because installing this repo modifies a machine's global agent context.

**`CLAUDE.md`** — auto-loaded by any Claude Code session opened in this directory, and it instructs the reading agent:

> "- Long single turns are normal (15 minutes on a hard task). Background anything over ~30s and let the completion notification bring you back. Never poll.
> - State the goal and the constraints, not the steps. Over-prescriptive prompts and skills reduce output quality on this model.
> - Delegate independent subtrees to sub-agents asynchronously and keep working."

Ordinary project configuration, not an injection attempt. I did not act on it.

**`install.sh:226`** — `copy_tree rules` installs 15 files / 903 lines of standing instructions into `~/.claude/rules/`, which load into every session on the machine, in every project. Disclosed in the README ("`rules/common/` | the always-loaded rules the guards enforce") and in `docs/INSTALL.md`. Flagged because it is the widest-reaching effect of running the installer and because `--uninstall` does not undo it (`install.sh:220`).

**`hooks/burn-context.sh:197`** — a `UserPromptSubmit` hook that injects steering text into the model's context each turn, including model-selection direction:

> "`[FABLE-SESSION] This session is on Fable 5.1. […] Mechanical work belongs elsewhere: /model claude-opus-5.`"

This is the hook's documented purpose ("Injects current burn stats into Claude's context so the model SEES the cost"), and it is scoped to the installing user's own sessions. Worth knowing before installing: six `UserPromptSubmit` hooks prepend text to every prompt you send.

**`.gitignore:7`** — names a private file the hooks read from the repo root:

> "`# Howard's private working backlog. The carryover hook reads it from the repo root; it must never be published from this public repo.` `OPEN-ITEMS.md`"

Not present in the tree. Noted because it confirms hooks read paths outside what the repo ships, and the protection is a `.gitignore` entry rather than a check.

No secrets, tokens, or keys found. The `keychain` references throughout (`websearch-router.sh:155`, `item-coverage.py:229`) are the author's own routing notes referring to their machine, not requests directed at the reader.
