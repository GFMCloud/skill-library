# Comparison: "The Guard I Installed Was Enabled, Running, and Doing Nothing" against the installed hook tooling

Candidate: `candidate/article.md`, a blog post dated 2026-09-17. I could not check the sha256 pin (`ba29e50b`) here, so I take it as given.

Incumbents, all read in full:
- `incumbents/2026-09-03-hooks-and-permissions.result.md`
- `incumbents/hooks-registry.md`
- `incumbents/prove-hooks.sh`
- `incumbents/replay-hooks.py`
- `inventory.md`, read in full for the collision analysis.

Limits:
- None of the four incumbents is a skill. They are a result log, a wiring table and two maintainer scripts, so there is no incumbent description or `SKILL.md` to compare.
- `deny-destructive.py`, `route-large-read.py` and `evidence-guard.py` are not in the incumbent set. I know them only through the registry rows and the result log.
- I did not verify anything about the function-hooks API. Nothing on disk documents it.

## Flags

Nothing in `candidate/` addresses a reader or agent, so there was nothing to act on. Three passages touch agent configuration, and I did not act on any of them:
- `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` in a fenced block (article lines 27-29).
- "It's in settings now, user scope, so every session gets it." (line 39).
- "The harness is mirrored public at [claude-harness](https://github.com/ucsandman/claude-harness), swept of secrets and memory." (line 205).

The rest of the file is site chrome and a marketing call to action ("Take the AI Audit").

## Ancestry

There is no shared history.
- Grepping the incumbents for `Sander`, `ucsandman`, `claude-harness`, `practical systems`, `heartbeat`, `function hook`, `FUNCTION_HOOKS`, `canary` and `shadow` finds nothing outside `cleanroom-review.md`.
- There are no merge notes and no CHANGELOG. No incumbent file resembles a candidate file, because the candidate is prose and the incumbents are code, a result log and a table, so there was nothing to diff.
- The incumbents cite other sources: "hstack review 2026-09-03" (`prove-hooks.sh:11`, `:56`, `:62`), "ECC evaluation" (`hooks-registry.md:40`) and "the oops-i-did-it-again review" (`replay-hooks.py:6`).
- Both sides do state "prove it by deliberate failure". The candidate says "a check that came back green has been run, not verified. Make it fail on purpose first." (line 35). The incumbent says "a gate or validator is trusted only after being proven by deliberate failure" (`prove-hooks.sh:10-11`). The wording differs, so I read this as convergence, not lineage.

So the question is "is it better", not "what did the other side learn since the fork".

## Cleanroom spot-checks

I treated the clean-room review as a second opinion. Against the actual file I checked:
- **27 versus 19 hooks.** Confirmed. Line 43 says 27, the promo at line 223 says 19.
- **Table arithmetic.** All five rows are consistent, and "Reserve error" is measured minus reserved. There is no `# EST:` column, so claim 25 ("1,500 to 2,300 tokens high", line 119) has no support in the post.
- **The 15,000 to 436,000 tokens promo.** Line 227.
- **The `find` false positive.** The pattern `\bfind\b` and the command are quoted at lines 169-172.
- **Section 3 quotes.** Items 1, 2, 3, 6, 8 and 9 match lines 97, 95, 99, 178, 154 and 200.
- **Not checkable.** The API claims, the 266-denial log, the nine-capability probe and the GitHub mirror.

The review's verdicts hold. Two things it could not know:
- **A local check on the probe risk.** It warns that a probe of "nine capabilities" misses semantic drift. The incumbent record supports that: `prove-hooks.sh:68-70` says version 2.1.260 alone "fixed four ways a permission rule silently failed to apply".
- **Release cadence.** The incumbent ran on 2.1.263 on 2026-09-07 (`result.md:3`). The article reports 2.1.273 to 2.1.274 on 2026-09-17. That is roughly eleven patch versions in ten days, faster than the "most weeks" the article claims (line 150).

I also found one item the review missed, in the "command position" rule (see A7).

## Classification

### A1. Heartbeat handoff between a classic layer and a function-hook layer: COMPLEMENT
- **The gap.** No incumbent runs two layers that could own one decision, and none checks that a hook was loaded in a real session. The registry admits this for plugin hooks: "`prove-hooks.sh` does not cover plugin hooks; that gap is a residue" (`hooks-registry.md:33-34`).
- **Consumer today.** None. The machine has no function-hook layer, so the mechanism is unconsumed. The principle behind it is taken as a fragment under A4.

### A2. Per-guard ownership modes `classic`, `mod`, `shadow_mod`: REDUNDANT
- **Incumbent.** `replay-hooks.py`.
- **Candidate:** "`shadow_mod` means both run, the new one's verdict is recorded and thrown away, and the old one still decides." (line 95)
- **Incumbent:** "measure a hook's fire rate on real command history before wiring it" (`replay-hooks.py:1`), with a born-date before/after split.
- **Why equal or better.** Replay needs no live second layer and no risk of double blocking, and the machine has no second layer to shadow.

### A3. Fail toward the old behaviour: DISCARD
- It only means something with two layers.
- The incumbents already record each hook's failure direction per row, for example "Fails closed on unparseable hook input" (`hooks-registry.md:21`).
- The article's own claim 20 has no failure test behind it.

### A4. Check the artifact a component produces, not its presence in a list: INGESTIBLE FRAGMENTS
The whole item is partly redundant. One fragment exposes a real gap.
- **Fragment.** "Check for the artifact it produces when it runs, not for its presence in a list." (line 202)
- **Incumbent claim it corrects.** `prove-hooks.sh:63-66`: "This script verifies hooks by side effect (the command ran and answered), never by the presence of a config key."
  - The command runs under `prove-hooks.sh`, not under Claude Code. It proves the script is correct on fixtures. It does not prove a normal session invokes it, which is the article's failure 1 for command hooks.
  - The only session-level proof is the manual headless run in `result.md:76-95`. Its cost was USD 0.97 for three calls (`result.md:102`), which is the price of a standing version.
- **Where it lands.**
  - Reword the `prove-hooks.sh` header sentence to say what it proves.
  - Add a live-session step to the runbook's Step 6 ("standing re-proof after every CLI update", `result.md:20`).
  - Cover the plugin hook `readonly-agent-guard.py`, whose `prove-guard.sh` has the same gap (`hooks-registry.md:28-34`).

### A5. Verify by deliberate failure: REDUNDANT, incumbent superior
- **Candidate:** "a check that came back green has been run, not verified. Make it fail on purpose first." (line 35)
- **Incumbent:** the mutated-settings run shows `RED  PreToolUse matcher=Bash #0  positive #0 was allow (dead detector under-blocks)` and `exit=1` (`result.md:44-46`).
- **Why superior.** The incumbent has the rule mechanised and executed. The article says its own count is 3 of 27.

### A6. Test the denials as well as the allows: REDUNDANT, incumbent superior
- **Candidate:** "cases in both directions: the false positives that must pass, and every genuinely slow root-scoped search that must still be denied." (line 178)
- **Incumbent:** "Every positive must deny and every negative must allow" (`prove-hooks.sh:22-23`), run as `23 positive=deny, 17 negative=allow` on the Bash hook.
- **Why superior.** The incumbent's failures are named `dead detector under-blocks` and `dead exemption over-blocks` (`prove-hooks.sh:297`, `:303`). This already catches the article's `\b` to backspace bug, because that guard "matched nothing".

### A7. Anchor the tool name to a command position, and do not build patterns by string concatenation: INGESTIBLE FRAGMENTS
- **Fragment:** "the tool name now has to sit at a command position, meaning the start of the line or right after a pipe, semicolon, `&&` or a subshell opener." (line 174)
- **Incumbent weakness it targets.** The Bash denier once blocked an orchestrator command only because its prompt text contained the force-push string: "Both are the accepted cost; both are now stated in the script header as known weaknesses." (`result.md:67-74`)
- **Target.** `deny-destructive.py`, which I have not read. Read it first.
- **Preconditions.**
  - The article's list omits `||`, `&`, newlines, backticks, and wrappers such as `sudo`, `env X=1`, `xargs`, `time`, `bash -c "..."`.
  - It also still false-positives on a quoted `; find`, for example `node -e "x; find ~"`.
  - For a slow-search guard a false negative costs minutes. For a destructive-command guard it costs data, so anchoring must not lower the existing positives.
  - Add wrapper-aware positives and one quoted-text negative to `PreToolUse__Bash__0.json` before changing the pattern. Then run `prove-hooks.sh` and `replay-hooks.py` on copied transcripts to see whether the fire rate drops.
- **Redundant part.** The string-concatenation warning is covered by A6.

### A8. A version pin defers to a capability probe: REDUNDANT, incumbent superior (with a philosophy conflict, below)
- **Candidate:** "A patch change defers to the probe: if every capability still answers true on the installed build, the API is intact and the pin is merely stale." (line 154)
- **Incumbent:** "Re-run after every Claude Code update: 2.1.260 alone fixed four ways a permission rule silently failed to apply ... a hook or rule that was green last week is unproven today." (`prove-hooks.sh:68-70`)
- **Why superior.** The incumbent's probe is the behavioural fixture run, not a list of booleans. It has no exact-match pin to go stale.
- **One residue.** Its trigger is prose plus the Thursday cadence. Printing `claude --version` in the `prove-hooks.sh` summary would tie each green line to a build, a one-line optional edit.

### A9. Rewrite beats deny; correct the model onto the valid path and say why: INGESTIBLE FRAGMENTS
Only the message half transfers. The rewrite half is not taken (see conflicts).
- **Fragment:** "Correct it onto the valid path and explain why, on the result it's already reading." (line 200)
- **Incumbent text it improves:** `Blocked by deny-destructive (git push --force); hooks-and-permissions runbook, ruled Q-2026-09-03-15 row 1. Not a prompt: choose a different command.` (`result.md:70`)
- **What changes.** Keep the decision as deny. Append one clause naming the safe sibling where one exists. The fixtures already list them: `--force-with-lease`, `git branch -d`, `git reset --soft`, and `rm -rf` under the scratchpad root (`result.md:62-65`).
- **Convention.** Keep the rule name in parentheses right after the hook name, because `replay-hooks.py:86` parses that shape.
- **Fixture.** Add a `stdout_contains` assertion for the hint.

### A10. Tag rows by writer when two producers share a history: DISCARD
The incumbents have no two-writer ledger. This is a passing tip.

### A11. "A guard that false-positives is a guard you'll disable": REDUNDANT, incumbent superior
- **Candidate:** "Every wrong denial spends some of the trust that makes the right ones work." (line 203)
- **Incumbent:** "a rule above 5 fires per 100 commands overall is too noisy to wire as a WARN" (`replay-hooks.py:154`), a measured threshold on real history.

### A12. Function-hook API: `tool.call` result rewriting, `$.session.usage()`, store and bus: COMPLEMENT
- **The gap.** The incumbents are all `type: command` hooks. `prove-hooks.sh:257-259` marks any other hook type RED with "not a command hook; nothing to prove", so adopting function hooks would need a new proof arm.
- **Consumer today.** None.
- **Status.** Unverified and experimental. Hold it, and run `fact-currency-check` against the docs before any use.

### A13. Secret redaction of every tool result: COMPLEMENT
- **The gap.** The incumbents deny reads of credential paths (`hooks-registry.md:24`) and refuse secret-shaped strings in handoff and state files. Nothing scrubs secrets in a result the model receives (`env` output, MCP output).
- **Consumer.** None, and it is blocked on the A12 mechanism.
- **Caveat.** The article describes no test that redaction fires on known-bad input, which is the shape it warns against.

### A14. Read cache and context nudge: DISCARD
- The evidence is bare assertion.
- Both need `$.session` or function hooks.
- The cache adds stale-read risk.
- The `handoff` skill already proactively suggests a fresh session when context is long.

### A15. Subagent cost accounting and the "17,000 token" startup tax: COMPLEMENT
- **The gap.** No incumbent measures reserved versus measured spawn cost.
- **Consumer.** Only `model-effort-advisor`, which I know from `inventory.md` alone.
- **What not to take.** The number is n=5 from one install, and the article's own related post reports 15,000 to 436,000. Do not ingest the number. The method is only useful if measured on this machine.

### A16. Runtime adapter, bus, DashClaw, CostClaw integration: DISCARD
This is author-specific plumbing with no consumer here.

## Routing collisions

There are none as things stand. The candidate is an article with no name or description, and the incumbents are files, so nothing on either side routes. No identical names exist.

If a skill were written from this article, three existing skills would collide on typical prompts, and the new skill would lose to all of them:
- **`proof-of-work`, `capability-preflight` and `eval-harness`.** They already fire on "prove a hook works", "negative control" and "before it is trusted".
- **`toolkit-review`.** It fires on "hook bench".
- **The vocabulary.** "Hook" in the registry means classic command hook. The article's "hook" and "Mod" mean function hooks, and its "27 hooks" would sit beside the registry's six wired rows plus one plugin row. Mixed into one file this would misdescribe the machine without looking wrong.

## Philosophy conflicts

**1. Rewrite versus deny.**
- **Candidate:** "**Rewrite beats deny.** ... Deny is reserved for what no rewrite can fix." (lines 73, 200)
- **Incumbent:** the force-push rule is a ruled deny (`result.md:70`, Q-2026-09-03-15 row 1): "Not a prompt: choose a different command."
- **Which wins.** Silently rewriting `--force` to `--force-with-lease` leaves the model believing it force-pushed. Keep deny for the destructive class and take only the message shape (A9).

**2. False-positive tolerance.**
- **Candidate:** "A guard that false-positives is a guard you'll disable."
- **Incumbent:** the force-push text match and the unexpanded-variable `rm -rf` denial are "the accepted cost" (`result.md:72-74`).
- **Reconciliation.** The incumbent accepts false positives on the destructive class only, and measures noise elsewhere with `replay-hooks.py`.

**3. What a patch release means.**
- **Candidate:** "A patch change defers to the probe" (line 154).
- **Incumbent:** a patch release invalidates last week's green (`prove-hooks.sh:68-70`).
- **Which wins.** The incumbent, and its evidence is the four silent failures fixed in 2.1.260. The two sides reconcile only if the "probe" is the behavioural fixture run.

## Corrections needed at ingest

- **Do not cite either hook count.** The article says 27 in the body and 19 in a promo, with no reconciliation.
- **Drop claim 25** (the 1,500 to 2,300 token overestimation). The table shows reserve error of -301 to +679 and no `# EST:` column. "Reserve error" is measured minus reserved, so "+" means under-reserved.
- **Fix the command-position rule** before use. The article omits `||`, `&`, newlines, backticks and wrapper commands (A7).
- **Windows paths.** `%TEMP%` and `C:\Projects` are not portable to this macOS machine.
- **Rules a stateless model cannot honour.**
  - The "learned median per agent type" needs a persistent store.
  - The heartbeat "rewritten every main turn" needs a live plugin.
  - The 266-denial log is not on disk.
- **Style.** The prose is full of the patterns `humanizer` targets: "not X but Y" contrasts and one-line closers such as "I had the instrument. I read the wrong dial." Rewrite any ingested text in library voice. It has no em dashes in its own prose. The only one is inside the quoted canary output at line 144, which `dash-gate.sh` would deny on an Artifact publish.
- **Compatibility with `prove-hooks.sh`.**
  - The candidate's contract is "Exit 2 means block" (line 43).
  - `prove-hooks.sh` maps empty stdout to "allow" (`:221`), so an exit-2-only hook would read as a dead detector.
  - Any imported classic hook must emit a JSON deny.

## Net assessment

If only three things could be taken:
1. **A4 as a fragment.** Add a live-session proof to `incumbents/prove-hooks.sh` (correct the header at `:63-66`) and to the runbook's Step 6. Extend it to the plugin hook noted in `incumbents/hooks-registry.md:28-34`. This is the only real gap the article exposes. The cost is about USD 0.30 per live call, per the recorded runs.
2. **A7 as a fragment.** Apply command-position anchoring to `deny-destructive.py` to fix the documented accepted false positive. Do it test-first, with wrapper-aware positives added to `PreToolUse__Bash__0.json`.
3. **A9 as a fragment.** Add a "safe sibling" hint to the deny reasons in `deny-destructive.py`, keeping the decision as deny and keeping the rule-name-in-parentheses convention.

Hold A1, A12, A13 and A15 until function hooks are verified against the docs and this machine has a consumer for them.
