I read the repository without executing anything. Note up front: **this session has no shell tool**, so I could not run `git log`, `wc`, or the test suite. Where the rubric asks for command output, I read the equivalent artifacts directly (`.git/logs/HEAD`, `.git/shallow`, `.git/packed-refs`, `CHANGELOG.md`) and say so rather than inventing output.

Files read in full: `README.md`, `DOCS.md` (1152 lines), `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `.claude-plugin/marketplace.json`, `plugin/claude-code/.claude-plugin/plugin.json`, `plugin/claude-code/hooks/hooks.json`, `plugin/claude-code/scripts/tripwire.py` (1184 lines), `tools/mine.py` (774 lines), `plugin/opencode/precedent.ts`, `.github/workflows/ci.yml`, `tests/test_tripwire.py` (1714 lines), `tests/test_mine.py`, `examples/a-retry-that-never-retries.md`.

---

# Review: `precedent`

## 1. Executive summary

A `PreToolUse` hook that reads a corpus of hand-written markdown "failure class" pages and injects any page whose declared path/command globs match the `Edit`/`Write`/`Bash` call about to run. One stdlib-only Python file (1184 lines) plus an offline SQLite miner; zero runtime dependencies, no server, no build step. The engineering is unusually careful for its size: a fail-open contract (always `sys.exit(0)`, because exit 2 from `PreToolUse` denies the tool call), a bounded path-glob matcher with memoised failure pairs, word-boundary command redaction instead of length truncation, and forward/backward-compatible telemetry that counts unknown fields apart rather than folding them to zero. ~2300 lines of tests run on six Python versions in CI.

Against that: the project is **one day old**. Every release in the CHANGELOG, 0.3.0 "First release" through 0.6.0, is dated 2026-09-19, one author, no issues, no external users. The headline empirical claim (7–29% of defect commits re-derive a known lesson across five repos) has no artifact in the repo. And `DOCS.md`'s "What is injected" section documents a rule the code does not implement — it tells page authors their post-Evidence checklist is *not* injected when the code, the CHANGELOG and a passing test all say it is.

## 2. Maturity signals

No shell available; these are file reads, stated as such.

| Signal | How I checked | What it returned |
|---|---|---|
| Last commit | `Read .git/logs/HEAD` | One entry: `0000…000 f5141c34… GFMCloud <…> 1789867464 -0500 clone: from https://github.com/FullFran/precedent`. Epoch 1789867464 ≈ 2026-09-19/20 — the clone, not the commit. |
| Commit cadence (last ~50) | `Read .git/shallow`, `.git/packed-refs` | **Unavailable.** `.git/shallow` contains exactly `f5141c34…` — a depth-1 clone. There is no history to read; `git log` here would return one commit. |
| Substitute for cadence | `Read CHANGELOG.md` | Four releases — 0.3.0, 0.4.0, 0.5.0, 0.6.0 — **all dated 2026-09-19**. 0.3.0 is labelled "First release". Entire project history is one day. |
| Distinct authors, 12 months | `Read .git/logs/HEAD`, `LICENSE`, both manifests | One name everywhere: `FullFran` (`marketplace.json` owner/author, `plugin.json` author, `LICENSE` "Copyright (c) 2026 FullFran"). Bus factor 1. |
| Tags | `Read .git/refs/tags/v0.6.0` (present in tree listing) | Single tag `v0.6.0`, matching `plugin.json` and `marketplace.json` version `0.6.0`. Three declarations of the version; `--version` reads the manifest rather than a constant, so only the two JSON files can drift. |
| Dependency count | `Read` all manifests + imports | **Zero runtime dependencies.** `tripwire.py` imports `json, os, re, sys, datetime, pathlib`. `mine.py` adds `argparse, itertools, sqlite3, collections`. `precedent.ts` uses `node:child_process`, `node:fs`, `node:path`, `node:url` and one **type-only** import (`import type { Plugin } from "@opencode-ai/plugin"`) — erased at runtime. No `package.json` anywhere. CI pins `actions/checkout@v4`, `actions/setup-python@v5`. |
| License file (not a badge) | `Read LICENSE` | Real MIT text, 21 lines, copyright 2026 FullFran. Not just a badge. |
| Tests exist AND CI runs them | `Read tests/*`, `.github/workflows/ci.yml` | Both. `test_tripwire.py` 1714 lines, `test_mine.py` 553 lines; CI runs `python -m py_compile …` then `python -m unittest discover tests` on `push` to main, `tags: v*`, and every PR, across Python 3.8–3.13, `fail-fast: false`. Whether it is *green* is claimed by the README badge only and cannot be verified from the clone. |
| Open issues / templates | Directory listing | No `.github/ISSUE_TEMPLATE`, no `PULL_REQUEST_TEMPLATE`, no `CODEOWNERS`. `.github/` contains only `workflows/ci.yml`. Nothing hints at issue volume; consistent with a repo published today. |

## 3. Claimed vs verified

**Verified (I saw it in the code or the config)**

- Stdlib-only, Python 3.8+, no packages to install, no build step. ✔
- `PreToolUse` hook matching `Edit|Write|Bash`, emitting `{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":…}}`; nothing on a miss (`tripwire.py:619-664`, asserted byte-exact in `test_tripwire.py:539-558`).
- Always exits 0. `main()` wraps every mode in `try/except Exception: pass` then unconditional `sys.exit(0)` (`tripwire.py:1159-1179`), with a dedicated `TestSafetyMatrix` covering malformed JSON, empty stdin, missing fields, a 5 MB payload, a 5 MB command string, and an unwritable home.
- Two independent matchers with the documented semantics, including `**` matching zero segments, `*` never crossing `/`, and no `**` special case in the command matcher — every row of the DOCS worked-example tables has a corresponding assertion.
- Path-glob blowup is bounded: `collapse_double_star()` plus a per-call `failed` memo set (`tripwire.py:383-418`), with `TestPathologicalGlob` asserting 8 `**` runs against a 40-segment non-matching path completes in under 1s.
- Command redaction by token boundary, not character count — stops at the first token starting with `-` or containing `=` (`tripwire.py:477-503`). Tests assert `TOKEN=sk-LEAKED gh issue comment` logs `(redacted)` and that neither `TOKEN` nor `sk-LEAKED` appears anywhere in the log file.
- Three distinct corpus states — loaded / retired-on-purpose / skipped-as-broken — kept apart through `load_corpus()`, `--check`, `--stats` and `--session-start` (`tripwire.py:283-339`, `TestRetiredPages`).
- Corpus resolution never relative to the script; `PRECEDENT_PATTERNS` > `PRECEDENT_HOME/patterns` > `~/.precedent/patterns`, with `TestDefaultCorpusResolution` covering the unset case.
- Miner opens the store read-only (`file:…?mode=ro` + `PRAGMA query_only = ON`), verifies required columns before trusting them, and never writes to the ledger.
- Evidence stays on disk after a match (`test_evidence_is_still_on_disk_after_a_match`), and `--match --full` returns it.

**Claimed, not verifiable from this repository**

- "Between 7% and 29% of genuine defect commits re-derived a lesson already learned somewhere else" across five repositories, and "fifteen architecture decision records … every one written in the same commit or session as the fix." No data, script, or citation ships. This is the entire justification for the tool and it is unfalsifiable from here.
- "Costs ~0 tokens and runs in about 28ms." No benchmark in the repo or CI. The ~0-token claim is structurally plausible for a miss (a hook that prints nothing), but 28ms is an assertion.
- "Claude Code reports it as `harness-only — no model context cost`" — a claim about the host UI.
- CI is green (README badge). The badge is an image URL; the clone carries no run data.
- OpenCode support is listed as **supported**. There is no TypeScript toolchain, no `package.json`, no typecheck or lint step in CI, and **not one test** touching `precedent.ts`. "Supported" here means "written and reasoned about carefully", not "verified".
- "Measured on real pages, this removes 24-48% of what a match costs." The real corpus is private by design, so the measurement cannot be reproduced — and see the next item, which suggests the measurement rule and the shipped rule are not the same.

**Claimed and contradicted by the code**

- **`DOCS.md:95-102` documents the wrong injection rule.** It says: *"**The cut is at the heading, not around the section.** Everything below `## Evidence` stays on disk too, including any section written after it … both put their `## Check before you trust it` checklist below the evidence, so that checklist is on disk and is not injected. Move it above `## Evidence` in your own pages if you want the model to read it."* That is the heading-to-EOF rule the CHANGELOG explicitly calls wrong and replaced: *"Cutting from the heading to the end of the file was the first rule and it was wrong."* `split_evidence()` (`tripwire.py:141-188`) removes only the Evidence section and re-appends the tail, README:186-188 says so, and `test_a_section_after_evidence_is_still_injected` asserts it. The reference manual is telling page authors to restructure pages around a rule that no longer exists.
- **The 55% figure is computed under that abandoned rule.** README:69-70 and `DOCS.md:87-88` say the evidence is "55% of the example page shipped here". By my count of `examples/a-retry-that-never-retries.md` (~1717 chars total): the Evidence section alone is ~402 chars ≈ **23%**; Evidence *plus* the checklist below it is ~952 chars ≈ **55.4%**. The 55% is the old heading-to-EOF cut. What the shipped code actually strips from that page is less than half the advertised saving — and ~23% sits just below the separately claimed "24-48%" range.
- **`DOCS.md:551` shows output the code cannot produce.** `run_check()` prints exactly one of `PRECEDENT_PATTERNS`, `PRECEDENT_HOME`, or `default` (`tripwire.py:884-892`). The sample shows `corpus: .precedent/patterns (from script location)`, and DOCS:558-562 then writes a whole paragraph explaining what that label means. It is a stale string from an earlier design.

## 4. Rubric scores

**1. Does what it says — 4/5.** The mechanism is exactly what the README describes, and the README is unusually disciplined about what the tool is *not* (not a memory system, not a linter, not a search index) and about OpenCode being weaker rather than equivalent. The deduction is for the reference manual contradicting the code on the single rule that decides what reaches the model, plus a headline percentage measured under the superseded rule.

**2. Quality of the interesting part — 4/5.** This is not glue. The interesting parts are the bounded segment matcher, the fail-open contract enforced as a stated invariant with a test class named after it, the head/evidence split, and the log-schema evolution rules (a missing `kind` defaults to `"path"` because every pre-command line *was* a path match; missing `injected_chars` is counted apart rather than as zero). Three concrete deductions:

- **The evidence splitter is fooled by a `#` inside quoted evidence.** The end-of-section scan does `stripped = lines[j].lstrip()` then treats any leading `#` as a heading (`tripwire.py:177-182`). Evidence is quoted as indented blocks — that is the shipped convention, and `mine.py:render_draft` indents every quoted lesson by four spaces. A quoted commit message, log line or issue body whose line begins with `#` (a shell comment, a markdown heading) ends the Evidence section early at depth 1, and everything after it is re-appended to the head and injected. The section start is anchored with `^#{2,6}`; the end is not anchored the same way.
- **The command matcher never got the care the path matcher got.** `_command_regex` joins escaped literals with `.*` under `re.DOTALL`, anchored (`tripwire.py:447-449`). A glob with several `*` against a multi-megabyte command string is polynomial backtracking. `TestSafetyMatrix` exercises a 5 MB command, but only against `gh * --body*` (two wildcards). The 5s hook timeout caps the damage; the asymmetry is still notable in a file that documents its other matcher's complexity bound in a comment block.
- `split_evidence` line 169 computes `level` and line 170 immediately overwrites it — dead code in a file where nearly every other line is justified by a comment.

**3. Adoption cost — 4/5 (low).** Zero dependencies, no server, no port, no credentials, no build. Removal is `/plugin uninstall` plus `rm -rf ~/.precedent`; nothing else on the machine is touched and the corpus is your own files. The real costs: a Python subprocess on **every** `Edit`, `Write` and `Bash` call (5s timeout each, per `hooks.json`); an append-only `~/.precedent/tripwire.jsonl` that gains a line per tool call with **no rotation, no cap and no documented opt-out**, recording every edited file path in full and forever (local only, never transmitted — but `--stats` reads the whole file each run); and the corpus itself, which is the actual price — the maintenance is the writing, and CONTRIBUTING's two-occurrence admission rule makes that deliberately expensive. Note also that installing this is a harness-configuration change: two hooks that run on essentially every tool call.

**4. Failure modes — 3/5.** The blast radius is deliberately small and genuinely well handled: fail-open by construction, no network anywhere, the miner physically cannot write, and the project's signature failure — installed-but-pointed-at-nothing, which looks identical to an honest miss — is attacked from three directions (`--session-start` notice, `--check`'s `NOT WIRED UP`, and `--stats`' blind-run warning that refuses to count corpus-less runs as misses). Where depending on it hurts:

- Silent under-stripping via the `#`-in-evidence split, above: quoted commit messages reach the model without anyone noticing, since nothing surfaces the diff between page and head except `--stats`' `injected_chars`.
- The OpenCode adapter reads `input.args?.path` for `edit`/`write` (`precedent.ts:121`). The module docstring documents verifying tool *ids* two ways — against the type definitions and against literal registrations in the compiled binary — but says nothing about verifying the *argument key*. OpenCode's edit/write tool schemas use `filePath`, not `path`, as far as I know; I cannot confirm that from this repo. If it is `filePath`, the adapter silently never matches an edit, and every failure path in that file resolves to `""` — indistinguishable from a miss. That is precisely the failure class the project exists to document, sitting in the one file with no tests.
- **The project's own CI violates its own shipped checklist.** The starter page `--init` writes says: *"Count what ran. A runner that discovers work can discover nothing and still exit 0; assert the count is non-zero."* CI runs `python -m unittest discover tests` and asserts nothing about the count. Rename or move `tests/`, and the gate goes green having run zero tests.
- Python 3.8 is in the CI matrix and is end-of-life upstream (security fixes ended October 2024). Keeping the floor honest is admirable; the floor itself is now unsupported, and `setup-python`'s 3.8 availability on `ubuntu-latest` is a maintenance tripwire of its own.
- Bus factor 1, four releases in a single day, zero external usage. Nothing here has survived contact with a second user.

**5. Originality — 4/5.** There are at least five ideas worth taking whether or not you take the code. Listed below.

## 5. Ideas worth taking independently of the code

**Push, not pull — and the explicit refusal to ship an MCP server.**
> "**It would turn surfacing into a *pull* the agent has to remember to perform.** An MCP tool only fires when the model decides to call it. That's exactly the failure class this tool exists to prevent" — `DOCS.md:905-911`

The generalisable point: retrieval the model must remember to perform is retrieval that fails exactly when it matters. Declaring the trigger next to the content, and having the harness fire it, removes the model's judgment from the step where its judgment is worst.

**Redaction by token boundary, not by length.**
> "Truncating to a character count is NOT redaction, and treating it as such is how a secret ends up on disk: it protects only by accident of position. `gh issue comment --body "..." && curl -H "Authorization: Bearer sk-..."` keeps the Authorization header inside the first 80 characters, while `TOKEN=sk-abc gh issue comment` puts the token in the first word. Both were written in full by a length limit." — `plugin/claude-code/scripts/tripwire.py:483-490`

Two lines, two opposite counterexamples, and a rule that handles both (stop at the first `-`-prefixed or `=`-containing token). Directly liftable into any tool that logs command lines.

**A decision is not a typo — give them different words.**
> "pages    loaded, and able to fire … retired  a decision … skipped  broken … three distinct states that must stay distinct: conflating them is how a typo hides as a decision." — `plugin/claude-code/scripts/tripwire.py:288-295`

Retirement as a first-class state that keeps the evidence, drops the triggers, and prints under its own heading with its stated reason.

**Key a suppression list on ids that do not move, and say out loud what it suppressed.**
> "The key is the set of OBSERVATION IDS in a group, never a group id. Group ids here are assigned by rank within one run … so 'group 3' means a different group tomorrow" — `tools/mine.py:65-69`
> "Printed whether or not anything was suppressed: a run that silently dropped candidates would be indistinguishable from a run that found fewer of them, and a ledger that is read but never mentioned is only marginally better than one nothing reads at all." — `tools/mine.py:521-525`

**Count unknown history apart rather than folding it to zero.**
> "There is no honest number to substitute for them, so they are counted apart instead of being folded in at 0 (which would understate what the corpus used to cost) or at their page size (which is not recorded anywhere in the log)." — `plugin/claude-code/scripts/tripwire.py:1041-1046`

A clean rule for evolving an append-only log format without silently corrupting the aggregate.

**Honourable mention — the honesty note the miner always prints** (`tools/mine.py:502-516`), which states in the tool's own output that lexical grouping is not class identification and that a high-ranked group may be a coincidence. A tool that ships its own limitations in every report is rare.

## 6. Flags

**No prompt injection against a reviewing agent. No request for credentials. Nothing asks to be added to agent instructions or a CLAUDE.md.** I did not act on anything below.

The repository does contain text written to be read by a model — that is the product, not an attack. Quoted for completeness:

1. `plugin/opencode/precedent.ts:59-64` — text prepended to a tool result, addressed to the model:
> `"precedent match (plugin/opencode/precedent.ts) -- this page matched AFTER the tool call already ran: OpenCode's tool.execute.after fires post-hoc, unlike Claude Code's PreToolUse. It is not part of the tool's own output. Read it before your next action."`

2. `plugin/claude-code/scripts/tripwire.py:770-778` (`STARTER_PAGE`, injected as `additionalContext` on a match) — imperative guidance directed at whoever is about to edit:
> `"- Make it fail on purpose, once, and watch it go red. A gate never observed failing is not yet a gate."`

3. `examples/a-retry-that-never-retries.md:33-41` — same shape, in the shipped example page.

Two things a human should weigh before installing, neither of them hidden by the project:

- **Installation is a harness-configuration change.** `README.md:79-84` instructs the user to add the repo as a plugin marketplace source and install a plugin that registers a `PreToolUse` hook on `Edit|Write|Bash` and a `SessionStart` hook. Every matching edit and command thereafter spawns a subprocess and can inject arbitrary text from `~/.precedent/patterns/*.md` into the model's context. The corpus is whatever is at that path — which is the design, and is why `--check` naming the resolved directory matters.
- **`tools/mine.py` reads a third-party local database**, `~/.engram/engram.db` by default (`tools/mine.py:38`), containing personal memory records. It is read-only by two mechanisms and runs offline, on demand, never from a hook — but it is the one part of this repo that touches data outside its own directory.
