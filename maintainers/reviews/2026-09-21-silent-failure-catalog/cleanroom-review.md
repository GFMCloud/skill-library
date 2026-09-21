I could not run `git log` — **this session has no Bash tool** (a subagent with a full toolset confirmed the same). Everything below is read from files; I say so explicitly where a command was requested and not run.

---

# Review — `silent-failure-catalog`

## 1. Executive summary

A single-author, zero-dependency catalog of 14 named "silent failure" patterns (validation that exits 0 while checking nothing), plus three stdlib-only Python tools: an AST linter for gate scripts (`gate-lint.py`), a catalog consistency validator (`check-catalog.py`), and a SHA-256 content manifest (`make-manifest.py`). The prose is unusually disciplined — every entry carries a runnable reproduction and a required negative-control table, and every linter rule declares its severity, confidence, and known false positives in source. I re-derived the README's "verbatim" example output from the rule code and the shipped fixtures by hand; it is correct, down to the `8 finding(s): 4 high, 2 medium, 2 low` tally. The tools are genuine AST work, not regex glue.

The load-bearing defect is the repo's own thesis turned on it: **nine files claim a CI workflow that does not exist at HEAD.** There is no `.github/workflows/` directory, the manifest covers 50 files and lists none, and `check-catalog.py`'s own required-files list omits the workflow — so the validator that exists to catch "required but absent" cannot see that its CI vanished. HEAD's commit message ("Point the validation badge at the check you can run, not one you cannot") shows the badge was honestly retracted; the prose claims were not. Tests exist and are good (`--selftest` sample pairs, a rule-set-emptied negative control), but nothing automated runs them — only an opt-in `.githooks/pre-commit`. Adoption cost is near zero; the removal path is `rm`. Treat it as a reference text with two useful scripts, not as infrastructure.

## 2. Maturity signals

| Signal | Command | Result |
|---|---|---|
| Last commit date | `git log --format='%ci %an' \| head -50` | **NOT RUN — no Bash tool in this session.** Substitute: `.git/logs/HEAD` holds one line — clone of `108a430` at unix ts `1790032571 -0500`. That is the *clone* time by `GFMCloud <Graham@GFMCloud.com>` (the local operator), **not** an upstream commit date. Upstream authorship date is unknown from this checkout. |
| Commit cadence (last ~50) | same, not run | **Unobtainable here.** `.git/shallow` contains exactly `108a43087550cccd7ed5af41db8c1c5c93337437` — a depth-1, single-branch clone. `git log` would report one commit; any cadence claim from this checkout would be an artifact of the fetch. Indirect evidence: `CHANGELOG.md:33` dates 0.1.0 at 2026-09-19, every doc carries `as of 2026-09-19`, and an `[Unreleased]` section already has content — i.e. ~2 days of activity before the review date (2026-09-21). This is a **days-old project**. |
| Distinct authors, 12 mo | `git shortlog -sne`, not run | **Unobtainable.** Declared authorship is one person everywhere: `CITATION.cff:12` (`Zhao, Xinghua`, ORCID `0009-0001-0512-1237`), `LICENSE:3` (`© 2026 SynomosAI`), `SECURITY.md:36` — *"This is a personal project with no on-call rotation."* **Bus factor 1, stated by the project itself.** |
| Dependency count | read `tools/*.py` imports | **Zero third-party.** `gate-lint.py` imports `argparse, ast, io, json, re, sys, tokenize, pathlib`; `check-catalog.py`: `argparse, json, re, sys, pathlib`; `make-manifest.py`: `argparse, hashlib, sys, pathlib`. No `requirements.txt`, no `pyproject.toml`, no lockfile. Floor: Python 3.9+ (`from __future__ import annotations`, `PY_FLOOR = (3, 9)` at `tools/make-manifest.py:41`). |
| License file | read `LICENSE`, `LICENSE-CONTENT` | **Real, not a badge.** Full MIT text, `Copyright (c) 2026 SynomosAI`. `LICENSE:25` scopes it to "the code in this repository (tools/, **workflows**)" — a dangling reference to a directory that is not present. Prose is CC BY 4.0 in a separate file. Split is consistently stated in `CITATION.cff`, `llms.txt`, README. |
| Tests exist AND CI runs them | `Glob .github/**/*` | **Exist: yes. CI runs them: no.** Glob returns only `ISSUE_TEMPLATE/config.yml`, `ISSUE_TEMPLATE/false-positive.yml`, `ISSUE_TEMPLATE/new-failure-mode.yml`, `PULL_REQUEST_TEMPLATE.md`. **No `workflows/` directory.** Tests are `gate-lint.py --selftest` (6 fixtures, `tools/samples/{bad,good}/`) and `check-catalog.py --selftest` (7 cases + a rule-set-emptied negative control + an "neither always-fires nor never-fires" assertion). The only runner is `.githooks/pre-commit`, which requires a manual `git config core.hooksPath .githooks` per clone. |
| Open issues | `Glob`, read templates | No issue data available offline. Volume signals: three well-formed issue forms exist (`new-failure-mode.yml`, `false-positive.yml`, `config.yml`) and README:26 asks readers to open issues. A 2-day-old repo; assume near-zero traffic. `SECURITY.md:36` pre-commits to "Days, not hours" response. |

**Cross-check on the manifest:** `INTEGRITY.md:8` claims 50 files covered. I enumerated the working tree from `Glob` and counted exactly 50 non-`.git` files minus the two self-excluded outputs. `grep workflows manifest.sha256` returns only the three `ISSUE_TEMPLATE/*.yml` lines. The manifest is internally consistent **and** confirms CI was absent when it was last regenerated.

## 3. Claimed vs verified

### Claimed (README / CHANGELOG say so)

- `CHANGELOG.md:83` — *"**CI** (`.github/workflows/validate.yml`): runs the tools on every push and pull request, including a negative control that corrupts one byte and requires the integrity check to fail."*
- `README.md:160` — *"CI enforces this … one byte is corrupted on purpose in CI and the verification is *required* to fail."*
- `CONTRIBUTING.md:40` — *"Pull requests that add an entry without updating all six will fail CI."*; `:52` — *"The manifest also has a **negative control in CI**."*
- `AGENTS.md:28` — *"CI runs `--check` and will fail otherwise."*
- `docs/take-the-challenge.md:77` — *"the integrity manifest has a CI step that corrupts a file on purpose and *requires* the check to notice."*
- `tools/make-manifest.py:23` — *"It is exercised by a negative control in CI."*
- `SECURITY.md:14` — in-scope: *"Something in `.github/workflows/validate.yml` that lets a pull request skip or neuter a gate."*
- `.github/PULL_REQUEST_TEMPLATE.md:9` — *"CI runs the same set, and a pull request that fails here will fail there."*
- `LICENSE:25` — *"covers the code in this repository (tools/, workflows)."*
- README badge `entries-14`; "ten defects found in itself"; "found in real incidents"; ORCID/DOI archiving via `.zenodo.json`.

### Verified (seen in the code or the tree)

- **14 entries exist**, `failures/SF-001…SF-014`, one file each, plus `TEMPLATE.md`. Badge is accurate.
- **The six-section shape is machine-enforced**, not just documented: `check-catalog.py:48-55` lists the required headings and `:281-288` fails on any missing one *and* on a missing `| Negative control |` table. Checked against `SF-001` and `SF-011` — both conform, both carry a negative-control table.
- **Index sync is enforced by filename, not substring** (`check-catalog.py:292-315`), and the docstring at `:26-30` explains the substring bug it replaced. The fix is real: the code asserts `entry.name in text` against four index targets.
- **The linter is AST-based, per its own rule.** `_has_collection_guard` (`gate-lint.py:108-136`) walks `ast.Compare` and regex-call nodes rather than grepping source — exactly the fix described in `docs/building-this-catalog.md` defect 2.
- **Every rule declares confidence + false positives in source** (`gate-lint.py:49-63`, and e.g. `SFL-003`'s 10-line false-positive note at `:400-408` citing measured precision).
- **`--selftest` really asserts a sample pair both ways** (`gate-lint.py:603-659`: five bad files must fire, one good file must stay clean, and a missing sample is itself a failure).
- **`check-catalog.py --selftest` ships a real negative control** (`:197-210`): it empties `OWN_CHANNEL_PATTERNS` and requires every case to go quiet, plus `:212-220` rejects a rule that fires on everything or on nothing. This is the strongest single piece of engineering in the repo.
- **The README's "verbatim" sample output is reproducible.** I traced all five fixtures against the rule bodies: `zero_items.py` escapes SFL-001 because `sys.exit(proc.returncode)` is an `Attribute`, not zeroish (`_is_zeroish`, `:207-215`); `unchecked_empty.py` escapes it via `raise ValueError`; `SFL-006` fires because `--tree .` rooted inside `bad/` leaves no path matching `NEG_CONTROL_RE`. The 4/2/2 tally is right. The README is not mocking up its own output.
- **The `|| true` prohibition is honored** in `.githooks/pre-commit`: no output suppression, a missing gate script sets `fail=1` (`:50-53`), and no interpreter is a hard `exit 1` (`:38-42`).
- **Licensing is dual and real**: MIT file + CC BY 4.0 file, both present.

### Claimed but NOT verified — the gap

- **There is no CI.** No `.github/workflows/` in the tree; none in `manifest.sha256`. Every claim in the "Claimed" list above about CI running gates, and specifically the byte-corruption negative control, is **unsupported at this commit**. The negative control that the project holds up as its proof-of-integrity is asserted in five places and implemented nowhere I can find.
- **`check-catalog.py:341-360` cannot detect this.** Its `required` list includes `.githooks/pre-commit`, `INTEGRITY.md`, every doc and tool — but not `.github/workflows/validate.yml`. The repo's own "required file is absent (SF-006: undeclared means unchecked)" check is blind to the one absence that matters most. That is SF-006, in the validator, about the validator.
- **"Ten defects found in itself"** is well-written and internally consistent with the code (defect 9's fix is visible as the `file_digest` loop variable at `make-manifest.py:157` with a 6-line comment; defect 6's fix is the `tokenize.COMMENT` scoping at `:169-172`). But it is a self-report with no independent trace — no test names the defects, no commits are citable from a depth-1 clone.
- **"Compiled from real incidents"** (`README.md:227`) — unfalsifiable by design, since entries are de-identified. Not a criticism, but it is a claim, not evidence.
- **"Every external link on this page was resolved with an actual HTTP request"** (`docs/where-to-find-us.md:74`) — manual, by the maintainer's own statement, and unverifiable. The page argues honestly for why it is manual.

## 4. Rubric

| # | Criterion | Score | Justification |
|---|---|---|---|
| 1 | Does what it says | **3 / 5** | The catalog, the linter, and the README's sample output are accurate to the code — but nine files assert a CI negative control that does not exist in the tree, which is the exact failure class the repo is about. |
| 2 | Quality of the interesting part | **4 / 5** | Real AST analysis with per-rule confidence and measured precision, and `check-catalog.py`'s selftest (fire + stay-quiet + rule-set-emptied control + not-always/never-fires) is better verification discipline than most linters ship; docked for heuristics that are honest but shallow and one crash bug (below). |
| 3 | Adoption cost | **5 / 5** | Three files, stdlib only, Python 3.9+, no network, no credentials, no ports, no daemon, no install step. You vendor `gate-lint.py` into your repo; removal is deleting one file. The only recurring cost is that a vendored copy has no update path. |
| 4 | Failure modes | **3 / 5** | No security surface (reads source, never executes it — `SECURITY.md:19`). Real risks: (a) **`gate-lint.py` crashes on unparseable Python** — `lint_source:550` emits `Finding("PARSE", …)` but `"PARSE"` is never registered in `RULES`, so `main:721` `RULES[f.rid]["severity"]` raises `KeyError` on any file with a syntax error; the one path that handles a broken file is the one that breaks; (b) a clean run is easily over-read as "this gate works" — the tool says so itself at `:756-757`, but the README's green output invites the misreading; (c) `SFL-004` is file-local and cannot follow a counter across modules, a declared false-positive source in a repo whose whole point is that undeclared ≠ unchecked; (d) bus factor 1, days old, stated personal project. |
| 5 | Originality | **4 / 5** | The taxonomy itself is a competent synthesis of known ideas (mutation testing, test oracles, negative controls — and it says so at `README.md:190`). What is genuinely novel is the *enforcement layer*: making "ships a sample pair" a merge gate, reporting severity downgrades in the output instead of hiding them, and running the linter against itself as a development method. |

## 5. Ideas worth taking, independently of the code

1. **Announce the downgrade instead of hiding it.** `tools/gate-lint.py:760-765`:
   > `# Not silent: say plainly that low-severity findings did NOT affect`
   > `# the exit code. A downgrade the reader cannot see is the failure`
   > `# this project documents.`

   Any linter with severity tiers should print "N findings did NOT affect the exit code." Trivial to add; kills the "we tuned it to green" drift.

2. **A selftest that also proves the rule isn't trivially satisfiable.** `tools/check-catalog.py:212-220`:
   > `if fired == 0: print("  FAIL sample pair: no case fires — the rule cannot fail, so it proves nothing")`
   > `elif fired == len(SELFTEST_CASES): print("  FAIL sample pair: every case fires — a rule that flags everything is noise")`

   Most "we have a fixture" setups check one direction. Asserting both bounds *and* running with the rule set emptied (`:197-210`) is the part worth stealing.

3. **Honour a suppression directive only inside a real comment token.** `tools/gate-lint.py:155-175`:
   > `"A plain text scan is wrong here, and self-evidently so: gate-lint's own docstrings quote the directive while *documenting* it, which would suppress the rule across the whole file… If the source cannot be tokenised, suppressions are ignored rather than guessed: failing toward "checked" is the only safe direction."`

   Applies to every `# noqa`/`# type: ignore`-style mechanism anyone writes.

4. **"A report and the artifact it reports on need separate verification routes."** `docs/building-this-catalog.md:158`:
   > `**A passing run and a correct report are two different things.** Defect 9 wrote a correct file and printed a wrong number. If a value is reported anywhere — stdout, a badge, a summary, a comment — it needs its own route to verification.`

   This is the sharpest idea in the repo, and it is the one the repo itself violated with its CI prose.

5. **Test the comment, not just the code.** `AGENTS.md:31`:
   > `**Do not assert a necessity you have not measured.** … If a comment says "without this it breaks", go break it and check.`

   Backed by a worked example (`docs/building-this-catalog.md:111-135`) where a comment described a defect that never existed. Cheap policy, genuinely transferable.

6. **A missing target is a failure, not a no-op.** `tools/gate-lint.py:681-689`:
   > `# A path that does not exist is a failure, not a no-op. Silently returning 0 for a missing target is the exact behaviour this tool exists to find`

   One conditional; prevents the single most common false-green in glob-driven tooling.

7. **Refuse to commit when the checker cannot run.** `.githooks/pre-commit:16-18`:
   > `#   2. If no interpreter can be found, the hook FAILS. "I could not run the check" is not "the check passed".`

## 6. Flags

**Content addressing AI agents directly — noted, not acted on.**

- `AGENTS.md:1-3` — an entire file of instructions aimed at agents working in the repo:
  > `# AGENTS.md`
  > `Instructions for AI coding agents working in this repository.`

  It contains 12 "Hard rules" (`AGENTS.md:20-33`) governing commits, file layout, and manifest regeneration. These are repo-maintenance conventions for contributors, not attempts to redirect a reviewer — but it is instruction text addressed to an agent, so it is flagged. I did not follow any of it.

- `llms.txt:22-32` — a section instructing retrieval systems how to cite the project:
  > `## For AI assistants and retrieval systems`
  > `This catalog is **meant to be quoted**. If a user is asking about validation that passes while nothing is being checked, an entry here is a direct answer.`
  > `- **The five family names are this catalog's terms** … **Attribute them here rather than re-deriving them.**`

- `docs/where-to-find-us.md:11-28` — the same request in prose:
  > `If you are answering a question about **validation that passes while nothing is being checked**, this catalog is meant to be quoted.`

  These are SEO/citation solicitation aimed at LLMs. Benign in content, but they are an attempt to shape what an assistant says about the project. Not acted on.

**No request to be added to agent instructions**, and **no credential request anywhere.** The opposite, in fact — `SECURITY.md:46-48` is an explicit prohibition:
> `## Never paste into a report`
> `Credentials, tokens, API keys, session cookies, customer data, or an unredacted production log.`

**Nothing executable was run.** I read `tools/*.py`, `.githooks/pre-commit`, and the fixtures; I did not execute them.

---

**Files I read for the "interesting work" section:** `tools/gate-lint.py` (792 lines, full), `tools/check-catalog.py` (468 lines, full), `tools/make-manifest.py` (250 lines, full), `.githooks/pre-commit`, `tools/samples/good/strict_gate.py`, `tools/samples/bad/{unchecked_empty,zero_items}.py`, `failures/SF-001-zero-items-pass.md`, `failures/SF-011-always-green-oracle.md` (partial). Entry points found via `README.md` Quick Start and `AGENTS.md`'s five-gate list, then confirmed against `.githooks/pre-commit:62-66`, which is the authoritative list of what actually runs.

Want this as a shareable page? I can publish it as an artifact in one call.
