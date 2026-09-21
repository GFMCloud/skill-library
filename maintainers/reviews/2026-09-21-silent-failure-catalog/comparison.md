# Comparison: `silent-failure-catalog` (candidate) vs the installed verification set

Scope and limits: I had only Read, Glob and Grep. Nothing was executed, so every "confirmed" below means confirmed by reading source. Facts I recall from outside the files (pytest exit codes, `-q` output) are labelled as such.

I read in full:
- All of `incumbents/` (proof-of-work, evidence-report, smoke-gate with references, scripts and fixtures; `evidence-guard.py`, `prove-hooks.sh`, `validate-skills.sh`).
- `cleanroom-review.md` and `inventory.md`.
- From the candidate: README, AGENTS, CHANGELOG, llms.txt, CONTRIBUTING, all 14 `failures/` entries, all four `docs/*.md` pages, `failures/README.md`, all three tools and the pre-commit hook.

I did not open `tools/samples/*`, LICENSE, SECURITY body text beyond one grep line, SUPPORT, CoC, CITATION, `.zenodo.json`, or the issue templates.

Not read, judged from `inventory.md` descriptions only: `eval-harness`, `output-lint`, `skill-discovery`, `toolkit-review`, `fact-currency-check`, `sweep-harness`, `bounded-loop`.

## 0. Ancestry: none found

- **Merge note:** none.
- **Shared files:** none. Candidate files are README/AGENTS/CHANGELOG/docs/failures/tools. Incumbents are SKILL.md/README/scripts/fixtures. There is nothing to diff.
- **References in either direction:** a grep of `candidate/` for `proof-of-work|evidence-report|smoke-gate|foundry|skill-library|NOT VERIFIED|Graham|gfm` returned no hits. The only match to my query set was `assayance` (candidate's sibling repo).
- **Fork dates:** incumbents were reviewed 2026-09-11 to 2026-09-18 (`reviewed:` frontmatter, `SKILL.md:7`). The candidate is dated 2026-09-19.
- **Convergent evolution, not a fork.** Both sides independently reached "a check must be seen failing":
  - Candidate: `taxonomy.md`, "No negative control means no evidence".
  - Incumbents: `smoke-gate/SKILL.md`, "prove each assertion category by poisoning it".
  - Incumbents: `prove-hooks.sh:12-13`, "a gate or validator is trusted only after being proven by deliberate failure".
- So the question is not "what did the other side learn since the fork". It is "where do two independent implementations differ". The answer is in section 6.
- I could not verify the pinned commit. My Glob of `candidate/.git/**` returned nothing.

## 1. Spot-check of the clean-room review

**Confirmed by reading:**
- **No CI exists.** No `.github/workflows/` in the Glob. CI is claimed at:
  - `CHANGELOG.md:83`: "**CI** (`.github/workflows/validate.yml`): runs the tools on every push and pull request,"
  - `README.md:160`, `CONTRIBUTING.md:40` and `:52`, `AGENTS.md:28`
  - `take-the-challenge.md:77`, `make-manifest.py:23`
  - `SECURITY.md:14`, `PULL_REQUEST_TEMPLATE.md:9`, `LICENSE:25`
  - The reviewer's list holds.
- **The validator cannot see it.** `check-catalog.py:341-360` `required` omits the workflow.
- **`PARSE` crash.** `gate-lint.py:550` returns `Finding("PARSE", ...)`. `PARSE` is never in `RULES`. `:721` does `RULES[f.rid]["severity"]`, so any unparseable target raises `KeyError`.
- **Selftest structure.** `gate-lint.py:603-659` and `check-catalog.py:177-227` match the description.
- **README tally.** I recounted the README sample output: 4 high, 2 medium, 2 low. It matches. I did not re-derive the rules against the fixtures.
- **Pre-commit fails closed.** Honoured as described (`pre-commit:38-42`, `:50-53`).

**Missed by the reviewer:**
- **`SFL-006` is never proven to fire.** `gate-lint.py:608-615` `expect` lists SFL-001 to 005 only. This breaks the candidate's own rule "A rule without a sample pair is not merged" (`AGENTS.md:76`).
- **Docs disagree on SFL-003's measurement.** `gate-lint.py:401-403` says "three findings and no true positives". `building-this-catalog.md:87` says "four findings and zero true positives".
- **The "reverse-control suite" is not shipped.** `building-this-catalog.md` calls it a control, but `tools/` holds only three scripts plus samples.
- **Negative controls are asserted by substring, not by execution.** `check-catalog.py:286`: `if "| Negative control |" not in text:` with the message "Fix section has no negative-control table". It checks only for the string anywhere in the file. Nothing runs the snippets, and section 5 shows two are broken.

## 2. Classification

### Ideas the clean-room review listed (R1 to R7), then the merged scout items (S1 to S3)

| # | Item | Class | Basis |
|---|---|---|---|
| R1 | Announce the severity downgrade | **REDUNDANT** | Candidate `gate-lint.py:764`: `"%d low-severity finding(s) did NOT affect the exit code. "`. Incumbent `evidence-guard.py:86`: `" WARN only; the command ran."`. `smoke-stop-hook.sh:33` also prints its release. Equal. |
| R2 | Selftest proves a rule is not trivially satisfiable, including a run with the rule set emptied | **INGESTIBLE FRAGMENTS** | See F1 below. |
| R3 | Honour a suppression only inside a real comment token | **REDUNDANT** | Candidate `gate-lint.py:158`: "A plain text scan is wrong here... gate-lint's own docstrings quote the directive while *documenting* it". Incumbent `validate-skills.sh:15-17`: "a grep would match the key inside prose or inside this validator's own documentation and call a broken skill green". Same lesson. The library has no suppression directive, so nothing would consume the mechanism. |
| R4 | A report and its artifact need separate verification routes | **REDUNDANT** (incumbent superior) | Candidate `building-this-catalog.md:158`: "**A passing run and a correct report are two different things.**" Incumbent `run-checks.sh:74`: "The table is read back from the files, so a phase with no recorded exit code cannot show as ran." That is mechanised, plus a tamper fixture (`run-fixture-proof.sh:28`). Also `proof-of-work/SKILL.md:62`. |
| R5 | Do not assert a necessity you have not measured | **INGESTIBLE FRAGMENTS** | See F2 below. |
| R6 | A missing target is a failure, not a no-op | **REDUNDANT** (incumbent superior) | Candidate `gate-lint.py:681`: "A path that does not exist is a failure, not a no-op." Incumbent `validate-skills.sh:233`: `"F0: zero skills found; a green run that checked nothing is a false green"`, plus `:22` (root from script location, from a real incident A-11). |
| R7 | Refuse to commit when the checker cannot run | **REDUNDANT** (incumbent superior), but see conflict C1 | Candidate `pre-commit:17-18`: `"I could not run the check" is not "the check passed".` Incumbent `run-checks.sh:14-16`: "a phase whose tool is absent is `not-run`... 3 if any phase could not run". Also `prove-hooks.sh:9-10`. The incumbent gives a distinct exit code. |
| S1 | Six-class taxonomy of defective checks (asyncdot.com) | **INGESTIBLE FRAGMENTS** | See F3. The article is not on disk, so I cannot quote its classes. My mapping to the candidate is by name only and unverified: vacuous assertion is SF-001/002, swallowed error is SF-003/004, wrong reference is SF-008/009. Stale premise is likely already covered by installed `fact-currency-check` (inventory text only). Scope mismatch is SF-006/010. |
| S2 | Five-case must-fail set for agent evals | **REDUNDANT** (provisional) | I have neither the five cases nor `eval-harness`. The mechanism is already present: `smoke-gate/SKILL.md`, "Five categories, five recorded exit-1 runs, captured verbatim." The candidate also ships five bad samples (`gate-lint.py:608-614`). Re-check against `eval-harness` before discarding. |
| S3 | "Put the value you read back into the report" | **REDUNDANT** (incumbent superior) | Candidate `SF-011`: "Report the measured value on PASS." Incumbent `evidence-report/SKILL.md`: "**Attach the identifier.** A commit SHA, a byte count, a row count, a timestamp." `check-report.py:74-75` enforces it. |

### The 14 entries and the tooling (beyond the reviewer's list)

| Item | Class | Basis |
|---|---|---|
| SF-001 zero items | **INGESTIBLE FRAGMENTS** | F4 below, which needs correction. |
| SF-002 early return, SF-003 swallowed exception, SF-004 sentinel | **COMPLEMENT** | Python test and validator authoring anti-patterns. Incumbents only have shell-level analogues (`evidence-guard.py` "stderr discarded"). Likely consumers are the reviewers spawned by `orch-review` and `orch-pipeline` (inventory text only). |
| SF-005 neutral marker | **REDUNDANT** (incumbent superior) | `run-checks.sh` `not-run` and `skipped` exit 3, and `check-poison-coverage.py:46`: "never report this category as passed". The diagnostic in F3 is separate. |
| SF-006 undeclared means unchecked | **INGESTIBLE FRAGMENTS** | Exposes a real hole in `smoke-gate` (F5). |
| SF-007 empty value | **REDUNDANT** | `check-report.py:72-73` (empty OUTPUT on VERIFIED fails), `validate-skills.sh` F3/F4. |
| SF-008 loading as use, SF-009 exposure as usage | **COMPLEMENT** | No incumbent touches proxy metrics. A plausible consumer on this machine is `skill-discovery` (ranks by "frequency x friction", so counting skill names in transcripts is exactly SF-009) and `toolkit-review`. Both are inventory text only. |
| SF-010 local green is not remote green | **REDUNDANT** | `proof-of-work/SKILL.md:91`: "A green pipeline is a claim about the pipeline." Also `deploy-verify-fix` and `smoke-gate`. |
| SF-011 always-green oracle | **REDUNDANT** (incumbent superior) | Per-category poison runs with recorded exit 1, and `prove-hooks.sh` two-sided controls. |
| SF-012 misattributed failure | **COMPLEMENT** (small) | "Do not use `in` for identity" is stated in no incumbent SKILL.md. Two local instances exist: the smoke identity check `grep -qF -- "$IDENTITY_EXPECT"` matches anywhere in the page, and `check-report.py:76` accepts a verdict containing any of `shows\|confirm`. |
| SF-013 stale copy | **INGESTIBLE FRAGMENTS** | F6. |
| SF-014 zombie process | **COMPLEMENT**, but the code is broken (section 5) | Watchdog and progress-signal advice has no incumbent home. Possible consumers are `bounded-loop` and `schedule-harness` (inventory text only). |
| `gate-lint.py` | **COMPLEMENT**, weak consumer | The library's Python gates are `check-report.py`, `check-poison-coverage.py`, `generate-smoke-script.py` and `evidence-guard.py`. Most gates are bash or embedded Python that gate-lint cannot see. Not worth vendoring (crash bug, unproven SFL-006). |
| `check-catalog.py`, `make-manifest.py` | **DISCARD** | Repo-specific plumbing. The manifest "does **not** attest authorship" (README). |
| README, AGENTS, llms.txt, where-to-find-us, take-the-challenge, question-map, community files | **DISCARD** | Promotion and retrieval-shaping. See Flags. |

### Fragments in detail

**F1. Emptied-rule mutation arm.**
- Candidate `check-catalog.py:197-198`: "# Negative control. With the rule set emptied, every case must go quiet." It clears `OWN_CHANNEL_PATTERNS` and requires every case to go quiet.
- Incumbent `prove-hooks.sh:56-60` lists exactly this as unbuilt: "a mutation arm that corrupts each hook's pattern and expects the positive control to start passing would prove the fixtures themselves. Do that when a second hook exists."
- The trigger is already met. `evidence-guard.py:64` names `deny-destructive.py`, `dash-gate.sh` and `route-large-read.py`. The fixtures also cover session-memory hooks.
- **Adds to:** `prove-hooks.sh` header plus a mutation pass.
- **Do not take** the candidate's "N of M cases fire" bound (`check-catalog.py:213-220`). The incumbent's labelled positive and negative controls are stronger.

**F2. "Necessity claims are claims."**
- Candidate `AGENTS.md:31`: "If a comment says "without this it breaks", go break it and check."
- Incumbent `proof-of-work/SKILL.md:131` says "Do not substitute reasoning about why it probably works" but has no code-comment case.
- **Adds:** one bullet to `proof-of-work/SKILL.md`, "What counts", Code. Worked example: `building-this-catalog.md` defect 10.

**F3. Three probes** (a new short `proof-of-work/references/false-green-probes.md`, linked from "A success message is not evidence").
- State-count probe. `taxonomy.md:55`: "count the check's possible outputs. If there are N states and only N-1 of them can produce a non-zero exit, the missing one is your bug."
- Proxy question. `taxonomy.md:69`: "state the claim, then ask *"could this evidence be true while the claim is false?"*" This sharpens `proof-of-work/SKILL.md:53-54`: "A check that structurally cannot see the defect is not a check, however green it comes back."
- Exposure rule of thumb. `SF-009`: "if a metric's value is close to your request count, it is measuring exposure, not usage."
- The evidence-versus-claim table in `SF-008` is worth carrying too.

**F4. Zero-collected guard** (`proof-of-work/references/code-checklist.md` row 4, and `run-checks.sh`).
- Incumbent row 4 says "report total, passed, failed". `run-checks.sh:39` records `python3 -m unittest discover` as `ran` on any exit 0, with no count check.
- Recall, not run: I believe unittest exits 0 on empty discovery before Python 3.12.
- **Adds:** "a total of 0 is a failure", implemented as a grep of the captured `$out` file.
- Do not use the candidate's snippet as written (section 5).

**F5. `smoke-gate` zero-category and unreachable-target holes** (by reading, not executed).
- `check-poison-coverage.py:42` iterates `for category in assertions:`. `generate-smoke-script.py:107` uses `if "identity" in a:`.
- A manifest with `assertions: {}` generates a script whose only output is `SMOKE PASS: all categories green` and exits 0. Coverage prints `RESULT: every assertion category has a poison entry` and exits 0.
- An empty `routes: []` or `connections: []` loops zero times. `SKILL.md` says five categories, but nothing enforces five.
- SF-006's remedy (`SF-006`): "compare the declared set against the discovered set, and treat the difference as failure in **both** directions." Fix: require all five categories and non-empty lists, with a missing category reported UNPROVEN and exiting 3.
- The console check is `BODY_CONSOLE="$(curl -sS "$TARGET" || true)"`. An unreachable target yields an empty body, so it prints `PASS console: no error marker found`. In a console-only manifest that is a `SMOKE PASS`.
- The marker defaults to the poison string (`generate-smoke-script.py:182`). `PASS` therefore means "the poison string is absent", not "no console errors". The disclosure in `SKILL.md` understates this.
- `SF-005` corollary: "Rename the outcome if the scope is narrower than it sounds (`CONSISTENT` vs `PASS`), or widen the check."
- **Adds to:** `generate-smoke-script.py:180-205` and `check-poison-coverage.py`.

**F6. Self-contamination of `run-checks.sh`'s secrets phase.**
- The secrets phase greps `.` and writes matches into the log folder (`README.md`: "copies what it finds into that log").
- If the log directory is inside the tree, the next run rescans the previous run's matches. This is SF-013's shape.
- SF-013's remedy: use `git ls-files`, not a tree walk.
- I have not reproduced this.

## 3. Routing collisions

The candidate has no SKILL.md, so it cannot collide today. If it were vendored as a skill:

- **"Tests passed but I think nothing ran" / "why does my validator always pass?"** No incumbent description matches these, so a candidate skill would win by default. That is a genuine routing gap, and F3 and F4 would fill it inside `proof-of-work` without a new skill.
- **"Verify this before you say it's done" and "an agent says tests passed, can I trust it"** (`question-map.md` L1). `proof-of-work` (stable, "whenever a tool reports its own success") should win, and the candidate's answer ("require an **artifact**, not a statement") is the same advice. A candidate skill with that trigger would be a redundant router competitor.
- **"Prove each category can fail" / "make a smoke test."** `smoke-gate` must keep these.
- **Terminology collision, the worst kind because nothing looks wrong.**
  - Candidate `README.md:86`: "*Every negative result needs a positive control.*" Its own tables and `taxonomy.md:110` use "negative control" for the input that must make the check fail.
  - Incumbent `prove-hooks.sh:6-8`: "a POSITIVE control (the payload the hook exists to refuse; it must answer with a deny or block) and a NEGATIVE control (a payload it must let through...)".
  - The candidate's "negative control" is the incumbent's "positive control". Add "poison" in `smoke-gate` and `sweep-harness`, and "manifest" (Smoke manifest yaml, sweep frozen manifest, `manifest.sha256`), and one vocabulary carries three or four meanings.
- **Identical names with different bodies:** none found.

## 4. Philosophy conflicts

**C1. Fail closed vs fail open when the check cannot run.**
- Candidate `AGENTS.md:33`: "If an interpreter, a dependency or a required file is missing, the gate exits non-zero. Never `|| true`, never an unreadable file treated as an empty one, never a skip."
- Incumbent `smoke-stop-hook.sh:23-25`: `echo "smoke-stop-hook: smoke script missing: '${smoke}'; the gate did not run" >&2` then `exit 0`.
- Incumbent `evidence-guard.py:9`: "Fails open on any error." Generated smoke scripts also emit `|| true`.
- The incumbents' reason is defensible: a blocking Stop hook that cannot run would wedge every turn. The candidate's SF-005 would still call a stderr line beside `exit 0` a "neutral marker".
- The incumbents' "never silent" claim (README: "Either way you see the message") rests on `stop-hook.md:26-29`, which quotes only stdout for exit 0, not stderr. I have not verified that exit-0 stderr is shown.
- **Resolution:** keep fail-open for hooks, but say why and prove the message is visible. Fail-closed for commit gates is correct.

**C2. Piping a check.**
- Candidate `SF-001` fix: `pytest --strict-markers -q | tee out.txt`, then `grep -qE "collected [1-9]" out.txt`.
- Incumbent `code-checklist.md:13-14`: "never pipe a check through `head`, `tail` or `grep`, because the exit code reported is then the pipe's."
- Related, in the incumbents' own guard: `evidence-guard.py:34` lists `tail|head|grep|wc|sed|awk|cut|sort|less` but not `tee`, so it would not warn on the candidate's own snippet. Add `tee`.

**C3. Visible placeholders.**
- Candidate `AGENTS.md:32` (rule 11) wants `[NEEDS CLARIFICATION: <the specific question>]` left visible.
- Installed `output-lint` "catches unsubstituted placeholders" (inventory text only), so it would flag this. Either exempt the marker or use the incumbents' closing NOT VERIFIED list instead.

## 5. Corrections needed at ingest

**Factual or logic errors in fix snippets:**
- **SF-001.**
  - The `tee` pipe masks the runner's exit code, and the pipe is itself a mechanism that produces "exit 0".
  - As I recall (not run), `pytest` exits 5 on an empty collection, which conflicts with the symptom block (`SF-001`) and `question-map.md:58` ("`pytest` reports success on an empty collection in many configurations").
  - As I recall, `-q` drops the "collected N items" line, so `grep "collected [1-9]"` may fail on healthy runs.
- **SF-014.** The deadline check is dead:
  ```
  last_progress = time.monotonic()             # positive progress signal
  if time.monotonic() - last_progress > DEADLINE:
  ```
  `last_progress` is reset on the line before the comparison, so the condition is never true. The `for line in p.stdout` loop also blocks with no line arriving, so silence cannot trigger it. The catalog's own fix is an always-green oracle (SF-011). Rewrite with a reader thread or `select`, and run the negative control before publishing.
- **Unfounded CI claims:** the nine files listed in section 1. Delete them or add the workflow. Also `LICENSE:25` ("tools/, workflows").
- **`gate-lint.py` `PARSE` `KeyError`.** Register the rule or handle it in `main`.
- **`SFL-006`** needs a sample pair and selftest coverage. Its `NEG_CONTROL_RE` matches `bad` or `broken` anywhere in a relative path, so almost any real tree silences it.
- **Terminology:** rename to "must-fail control", or match `prove-hooks.sh`'s polarity.

**Style violations against library conventions:**
- **Missing contract sections.** `validate-skills.sh` requires Inputs, Verify, Done when and Stop when, in order (F14 to F16). It also requires `name` equal to the directory (F5), `metadata.maturity` (F9), description of at least 40 characters (F4), and a plugin version bump (F17).
- **Body length.** SKILL.md bodies are capped at 500 lines (F7).
- **Inventory.** The generated inventory must be regenerated (F13).
- **Em dashes.** The candidate uses them throughout. The library appears to gate them (`dash-gate.sh` in `evidence-guard.py:64`; `{{TMP_EMDASH}}` fixtures in `prove-hooks.sh`), though the scope is unknown from these files.
- **Prose register.** Strip `中文要点` blocks, "as of" citation ceremony, emoji output and the retrieval-solicitation prose.

**Rules a stateless model cannot honour:**
- "Quote the entry id and its `as of` date" (nothing to check a regression against).
- "Every external link... resolved with an actual HTTP request" (manual).
- "Never a skip" when the tool is not installed. A session can only report `not-run`, which is the incumbents' form.

**Incumbent defect exposed by this review:** `generate-smoke-script.py:14` cites `scripts/run-poison-proof.sh`, which does not exist in `smoke-gate/scripts/` (three files, per my Glob). `validate-skills.sh` F18 scans only SKILL.md text, not script docstrings.

## 6. Net assessment: the three things to take

1. **Fragment: SF-006 and SF-005 applied to `smoke-gate`** (F5). Target files:
   - `smoke-gate/scripts/check-poison-coverage.py`
   - `smoke-gate/scripts/generate-smoke-script.py`
   - `smoke-gate/SKILL.md`, "Verify" and "Done when"
   
   This is the highest-value item: a proven gate that can print PASS with zero checks, or with the target down.
2. **Fragment: zero-collected guard** (F4). Targets: `proof-of-work/references/code-checklist.md` row 4 and `proof-of-work/scripts/run-checks.sh:39`, then add a fixture `checks-zero.tsv` to `run-fixture-proof.sh`. Written fresh, not copied from SF-001.
3. **Fragment: the three probes plus the necessity bullet** (F3 and F2). Targets: a new `proof-of-work/references/false-green-probes.md` (about 40 lines, linked from "A success message is not evidence"), plus one bullet under "What counts", Code.

Runner-up: the emptied-rule mutation arm for `prove-hooks.sh` (F1), which the file itself calls overdue in effect. Do not install the catalog, gate-lint or the docs wholesale.

## Flags: text in `candidate/` addressing the reader (not followed)

- `AGENTS.md:1-3`: "# AGENTS.md" / "Instructions for AI coding agents working in this repository." plus 12 "Hard rules".
- `llms.txt:24`: "This catalog is **meant to be quoted**. If a user is asking about validation that passes while nothing is being checked, an entry here is a direct answer."
- `llms.txt:29`: "Attribute them here rather than re-deriving them."
- `docs/where-to-find-us.md:13`: "If you are answering a question about **validation that passes while nothing is being checked**, this catalog is meant to be quoted."
- `docs/question-map.md:7`: "An AI retrieval system does not know who wrote this catalog."
- `docs/take-the-challenge.md:60`: "Entry is designed to cost one API call, from a human with `curl` or from an agent over MCP." This points an agent at an external scored event.
- `README.md:26`: "**If this saved you a debugging session, open an issue naming the pattern you hit.**"
- `README.md:231`: `<!-- drift probe -->`. This is unexplained and inert, and I did not act on it.
