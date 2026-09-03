# hstack vs. installed set — Stage 3 comparison

Candidate: `github.com/howardchan2008/hstack`, pinned at
`b1abe1ae2659920d9e2452309e97074628eacfd3` (single commit, single author, 2026-09-03).
Read in full: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `LICENSE`, `hooks.manifest.json`,
`install.sh`, `doctor.sh`, all of `docs/*.md`, all of `rules/common/*.md` (15 files),
all three files in `tests/`, and 15 of the 37 hook files in full (the rest sampled by
header, self-test block, and the clean-room review's account, cross-checked against the
manifest and the code that was read).

## Ancestry

**No shared history.** `git log` on the candidate shows one commit, one author
(`chakhanghowardchan2008@gmail.com`, "Chak Hang (Howard) Chan"), remote
`github.com/howardchan2008/hstack`. `grep -ril` across the entire candidate tree for
`skill-library`, `gfmcloud`, `turn-reduction`, `foundry-core`, `verification-kit`,
`capability-preflight`, `standing-authorization`, `pre-delivery-verifier`, and
`validate-skills` returned zero hits. No merge note, no byte-identical or near-identical
file, no matching section structure, no CHANGELOG entry naming the other side. The
commit message ("mirror of claude-hooks") refers to the author's own private source
repo, not to anything on this machine.

This is two independent operators who converged on the same diagnosis — "prose rules
regress, a hook is a wall" — and built structurally similar machinery (a manifest as
single source of truth, a doctor/health-check script, negative controls, evidence-based
verification) with no contact between them. Where the two agree, that is convergent
validation, not derivation. Where they disagree, it is a genuine difference in judgment,
not drift from a shared ancestor. Every classification below treats it that way.

One coincidental parallel worth flagging so it is not mistaken for ancestry:
`hooks/burn-context.sh` injects a `[FABLE-SESSION]` block naming Fable 5.1's context
window, thinking mode, and effort levels, and Graham's own
`/Users/gfm/.claude/CLAUDE.md` has a "Working on Claude Fable 5.1" section covering the
same facts. Both are independent responses to the same model release landing the same
week (`hstack`'s CLAUDE.md is dated 2026-09-02, Graham's section reads "added
2026-09-02"). No text overlaps.

## Classification

### The clean-room review's "ideas worth taking" (section 5)

**1. Mutation-test your regexes, and self-test the mutation tester** (`tests/dead-branch-sweep.py`) — **COMPLEMENT**, bordering **SUPERIOR SUBSTITUTE** for one specific incumbent procedure.

No incumbent skill mutation-tests anything. The closest analog is
`/Users/gfm/work/claude-improvements-weekly/prompts/phase-0-survey.md` step 5, which
instantiates the global rule "a gate or validator is trusted only after being proven by
deliberate failure; a check that has never failed a fixture is untested"
(`/Users/gfm/.claude/CLAUDE.md`, "Evidence over assertion") for exactly one validator
(`scripts/validate-skills.sh`), by hand, once per weekly cycle: strip one field, confirm
the printed FAIL line, restore byte-identical, confirm green again.

`dead-branch-sweep.py` generalizes the same idea into something that runs on every
regex in every hook, automatically, on every test run, and — this is the part
phase-0-survey.md's manual procedure does not have — **proves the sweep itself can find
a planted defect**, via its own `self_test()`:

> "Builds a throwaway hook with one covered regex and one uncovered one, and asserts the
> sweep flags exactly the uncovered one. Without this, a sweep that silently matched
> nothing would print a clean bill of health forever, which is the exact failure the
> tool exists to detect." (`tests/dead-branch-sweep.py:134-139`)

That is meta-verification the phase-0 procedure lacks: nothing today proves the
break-and-restore step would catch a *real* regression versus one it happens to be
looking at. I ran the self-test logic by reading it, not by executing the candidate's
scripts (guardrail: never run the candidate's scripts). The mechanism is sound on
inspection: `corrupt()` uses AST line spans to replace exactly one `NAME = re.compile(...)`
assignment, re-runs that file's own `--self-test`, and reports the regex as dead if the
self-test still passes.

**What would have to change before this substitutes for anything here**: the library's
validators (`validate-skills.sh`) do not check compiled regexes at all — they check
frontmatter fields and links via plain string/AST matching, not regex libraries the
sweep's `regex_names()` pattern (`NAME = re.compile(...)`) would find. The one place on
this machine with a regex a sweep like this could exercise is the single installed
PreToolUse hook's `grep -q '—'` (not a compiled regex, a grep invocation) — the sweep
would need retargeting from "corrupt a Python `re.compile` assignment" to "corrupt a
shell grep pattern," which is a different corruption strategy, not a port.

**2. Direction decides the test arm** (`tests/dead-branch-sweep.py:21`) — **COMPLEMENT**.

> "A dead DETECTOR under-blocks: the rule silently stops firing. A dead EXEMPTION
> over-blocks, which is worse, because an over-blocking guard gets bypassed or deleted
> rather than obeyed."

No incumbent states this distinction. `proof-of-work` says "verify at the level the
failure lives" but does not distinguish a detector's failure mode from an exemption's.
Worth folding into `foundry-core:proof-of-work` or `verification-kit:pre-delivery-verifier`
as a one-paragraph addition on how to design a negative control for a rule that has both
a "catches X" half and a "except when Y" half.

**3. A checker must not be able to match its own documentation** (`tests/parity.py:192`) — **INGESTIBLE FRAGMENT** of `proof-of-work` / `pre-delivery-verifier`.

The principle is already stated at a higher level of generality in
`foundry-core:proof-of-work`: "A check that structurally cannot see the defect is not a
check, however green it comes back," and `pre-delivery-verifier` repeats it almost
verbatim from the `claude plugin validate` incident. That principle is **REDUNDANT**
with the candidate's framing. What is not redundant is the concrete technique
`parity.py` uses to hold itself to that standard:

> "The first version grepped raw text and could not fail: deleting the real
> `"decision"` object from a hook left the WORD in the comment above it, and the check
> stayed green against the exact bug it was written for. A checker that matches prose is
> measuring documentation." (`tests/parity.py:196-199`)

The fix — parse with `ast` and require the string to appear as a **dict literal key**
being built (`isinstance(node, ast.Dict)` with a matching `ast.Constant` key), not a
`.get()` call reading one (`tests/parity.py:227-239`) — is a specific, generalizable
technique neither incumbent skill gives: *how* to build a checker immune to prose
matches, not just the instruction to do so. Worth quoting as a technique inside
`proof-of-work`'s "What counts, by artifact class -> Config and manifests" section.

**4. Negative controls for capability probes** (`docs/TESTING.md:48`) — **REDUNDANT**, near-exact match with `capability-preflight`.

> "A credential probe reported 51 slots live. Re-running each probe with a deliberately
> corrupted key showed 5 of them still passing, so for those, 'live' carried no
> information: the probe was reading a status endpoint that answers before it looks at
> credentials." (`docs/TESTING.md:48-52`)

Matching directive, `capability-preflight` SKILL.md:

> "The target must be capable of failing. An auth probe once returned `200` naming the
> right league from a *public* endpoint — the identical response comes back with no
> credential at all. So every capability carries a negative control: the same access,
> deliberately deprived of the thing being proven, which must fail. If it succeeds the
> capability is `NOT PROVEN` no matter how green the read and write were."
> (`capability-preflight/SKILL.md:80-86`)

Same incident shape (a probe that answers before checking the thing it claims to prove),
same fix (a negative control that must fail), same verdict name pattern (`NOT PROVEN` /
"live carried no information"). `capability-preflight` is equal or superior here: it
turns the insight into a runnable manifest format (`preflight.py`) with a required
`negative_control` block and a machine-checked `expect`, where the candidate's version is
a documented anecdote with no corresponding enforcement in the repo (no test file
requires every probe-like hook to carry a negative control — `negative-control.py`
covers *hooks*, not general-purpose probes).

**5. Config keys that silently disable an entire subsystem** (`doctor.sh:73`) — **COMPLEMENT**.

> "Some settings keys make Claude Code drop the ENTIRE hooks block of the file that
> contains them. The file still parses, nothing warns, and checks 1 to 4 above all pass,
> because every one of them is true of a hook that never runs. … `fallbackModel` and
> `workflowSizeGuideline` each did it." (`doctor.sh:73-80`, confirmed in the actual
> `POISON = ("fallbackModel", "workflowSizeGuideline")` check I read at `doctor.sh:81-87`)

No incumbent addresses this failure class: a settings key that makes an entire
gated subsystem inert while every existing check stays green because each one only
verifies a symptom, not the precondition. This is a genuine gap. It would consume
directly into a `capability-preflight`-style probe for `/Users/gfm/.claude/settings.json`
("the hooks block is live," proven by a real hook execution, not by the file parsing),
which does not currently exist on this machine — the one installed hook has never been
probed this way.

**6. State a heuristic's ceiling in the file that implements it** (`hooks/item-coverage.py:213-224`) — **INGESTIBLE FRAGMENT** of `evidence-report` / `proof-of-work`.

> "MIN_TERMS items judged / turns blocked — 3: 59.8% / 39.3% — 4: 47.9% / 28.5% —
> 5: 36.5% / 20.6% — 6: 24.8% / 12.4%. Five is chosen and the ceiling that comes with
> it is real: this guard sees about a third of what he asks for. … so it is a floor
> under the worst omissions, never a proof that a turn was complete."

`foundry-core:proof-of-work` requires "the not-verified list," which is the artifact-level
version of the same discipline (say what was not checked). `item-coverage.py` extends
that one level deeper: **a detector should state, in the file, the tradeoff curve it
chose and what fraction of true positives it accepts missing at that setting.** That is
a sharper, more specific requirement than anything in `evidence-report`, worth adding as
a line: "a heuristic detector states its own measured miss rate at the threshold it
ships with, not just that it has one."

**7. Publishing a redaction tool publishes the redaction list** (`README.md:113`) — **COMPLEMENT**, narrow.

> "a scrubber's rules are a list of every private string it knows about, so including it
> for transparency would have published exactly the thing it removes."

No incumbent skill touches redaction/scrubbing at all. This is real and correct, and it
is exactly the kind of thing the `source-intake` pipeline itself (per Graham's memory
notes) or any future publish-a-repo workflow should carry, but nothing installed
consumes it today. Filed as a complement with no current consumer.

**8. One fact, one place, and generate the copies** (`docs/ARCHITECTURE.md`, `hooks.manifest.json`) — **REDUNDANT**, exact match with the global working agreement.

Matching directive, `/Users/gfm/.claude/CLAUDE.md`, "Edit the generator, never the
output":

> "Generated artifacts … are changed only through their generator: the template,
> script, or manifest (add to `flake.nix`, not an ad-hoc install). Hand-edits to
> generated output are lost on the next regeneration and drift from source. This was
> the single most-repeated rule in the corpus, written independently in four projects."

`hooks.manifest.json`'s own comment: "install.sh merges this into settings.json,
doctor.sh checks the live settings against it, tests/negative-control.py iterates it, and
settings.example.json is generated from it. They drifted apart once when each held its
own copy of the list." Same principle, same failure mode named, independently arrived
at. `skill-library`'s own `scripts/generate-inventory.sh` + `validate-skills.sh` F13
check ("docs/inventory.md missing or stale; run: generate-inventory.sh") is the
incumbent's working instance of the identical pattern. Neither side is superior; they are
the same rule implemented twice, and the candidate's own residual drift (the stale
word-form hook counts documented below) is the argument *for* the rule, not against it —
exactly as the clean-room review notes.

### The three test mechanisms

**`tests/parity.py`** — **INGESTIBLE FRAGMENT** of `scripts/validate-skills.sh`, plus one clean miss.

Both are "does the repo agree with itself" checkers generated against one manifest
(`hooks.manifest.json` vs. the SKILL.md frontmatter tree), and both check bidirectional
membership (files on disk vs. files declared) and cross-file consistency
(`settings.example.json` regenerated vs. `docs/inventory.md` regenerated — check 2 in
`parity.py` and F13 in `validate-skills.sh` are the same check on different data).
`validate-skills.sh` has no equivalent of `parity.py` check 7 (does the file's `block`
column match its actual refusal mechanism, verified by AST for Python and a stricter
`exit 2` regex for shell) — nothing in `validate-skills.sh` verifies that a skill's
described *behavior* is real, only its declared *shape* (frontmatter fields, links,
body length). That is check 7's fragment, already covered under item 3 above.

I verified check 5 personally by re-deriving the manifest count: I counted every
`"file":` entry in `hooks.manifest.json` by hand — 37 — matching both the manifest's own
implicit count and `README.md`'s table ("37 hooks: 17 PreToolUse, 2 PostToolUse, 4
SessionStart, 6 UserPromptSubmit, 8 Stop"), while the README's *title* still says
"Thirty-one." Check 5 exists precisely to catch this and structurally cannot: its regex
`\b(\w+)\s+hooks\b` on "Thirty-one Claude Code hooks" captures the word "Code," and its
word-to-number table (`twelve, sixteen, twenty, twentyfive, eighteen, fifteen`) has no
entry for "thirty-one" regardless. I confirmed this is a real, live bug in the shipped
checker, not a review artifact — read `tests/parity.py:112-118` myself.

**`tests/dead-branch-sweep.py`** — see item 1 above. **COMPLEMENT**, arguably the single
best individual mechanism in the repo.

**`tests/negative-control.py`** — **COMPLEMENT**, no incumbent equivalent for hook/guard
behavior specifically.

`capability-preflight` proves *access to a system*; nothing installed proves *a guard
refuses what it claims to refuse and stays out of the way of ordinary work*. This
four-verdict design (block / allow / warn / nudge) is more refined than a simple
pass/fail: it separately handles a reporter that must print something (`warn`, so a
silenced reporter still fails the suite) and a guard that refuses once and yields on
retry (`nudge`, asserted twice so a nudge that never clears reads as a plain block). I
read all 20 cases in full and traced several of the comments to real, dated incidents in
the code they test (e.g. the `probe-dedupe/allow-first` case explicitly documents that
an earlier version of itself tripped the wrong half of the same guard). This is the
mechanism that would directly answer the question below about turning "a check that has
never failed a fixture is untested" into something executable on this machine, for the
one hook that exists here today.

I independently verified the review's central quantitative finding by reading
`negative-control.py`'s `cases()` function myself and counting: cases exist only for
`dash-gate`, `grep-portability`, `ls-before-write`, `pipestatus-guard`, `risk-checkpoint`,
`lane-guard`, `agent-budget`, `curl-router`, `fetch-guard`, `probe-dedupe`, and
`websearch-router` — 11 of 37 hooks, 20 cases total (matching the README's claimed
"20/20"), with only 6 of those 11 carrying both a block and an allow arm. The six
Stop hooks I read in full — `item-coverage.py`, `capability-claim-gate.py`,
`handoff-gate.py`, `person-claim-balance.py`, `stop-justify.sh`, `closeout-shape.py` —
each carry their own `--self-test`, but none appear in `negative-control.py`'s external
suite, confirming the review's claim that all six blocking Stop hooks have zero coverage
in the one file whose header says "every guard is tested twice."

### `doctor.sh`

**COMPLEMENT.** No incumbent checks the specific four-stage failure chain doctor.sh
targets: file present -> executable with resolvable interpreter -> registered in
`settings.json` under the right event/matcher -> survives a live payload without
crashing. `capability-preflight` proves access to *external* systems; nothing proves a
*locally installed hook* is armed versus merely present. Given Graham's machine has
exactly one installed hook (the em-dash `PreToolUse` guard on `Artifact` publish, per
`/Users/gfm/.claude/settings.json`), this has never been checked this way — there is no
script on this machine today that would catch the exact failure doctor.sh is built
around ("present, registered, never fires" — I confirmed this class of bug is real by
reading `doctor.sh:104-115`, where the tool's own fallback `shutil.which(runner) or
shutil.which(runner + "3")` masks the very failure the file exists to catch: six hooks
registered under bare `python`, which the tool silently resolves to `python3` and
reports armed. I read this section directly, not from the review's paraphrase, and it
is accurate).

### Hook families

**PreToolUse guards (17, 15 refuse)** — mixed, with one standout.

`dash-gate.sh` is a **SUPERIOR SUBSTITUTE** for the one hook Graham has installed. The
installed hook (`/Users/gfm/.claude/settings.json`, extracted via the `hooks` key only,
per this task's guardrail) is:

```
matcher: "Artifact"
jq -r '... .tool_input.file_path ...' | { read -r f; if [ -n "$f" ] && [ -f "$f" ] &&
  /usr/bin/grep -q '—' "$f"; then echo '{"...permissionDecision":"deny"...}'; fi; }
```

It fires only on `Artifact` publish, checks only the literal em dash byte, has no
allow-list for legitimate uses, and offers no override. `dash-gate.sh` (`hooks/dash-gate.sh`,
91 lines, read in full) fires on `Write|Edit` generally, covers em dash, en dash, and
horizontal bar by Unicode codepoint (`chr(0x2014)`, `chr(0x2013)`, `chr(0x2015)` —
deliberately not written literally, so the file cannot self-block), scopes to authored
extensions only (`.md .sh .py .js .jsx .ts .tsx .txt`, explicitly excluding data-capture
formats so a scraped page or transcript is not corrupted to enforce a style rule),
carries an `EXEMPT` list (`CLAUDE.original`, `.prev.`, `node_modules/`, `.git/`,
`queue|transcripts|inbox` directories), and a documented one-shot escape hatch
(`DASH_GATE_OFF=1`) for a deliberate verbatim quote. Both hooks encode the same policy
(no em dashes; Graham's own global rule says exactly this: "No em dashes in any written
content you produce or edit"), and `dash-gate.sh` is measurably more complete on every
axis: scope of trigger, scope of character class, false-positive handling, and override
ergonomics.

**What would have to change before it replaces the installed hook**: the trigger
would broaden from "Artifact publish only" to "every Write/Edit to an authored
extension," which is a real behavior change Graham has not asked for and should decide
deliberately, not inherit by import; the exemption list references paths specific to
Howard's setup (`node_modules`, `.git`, `queue|transcripts|inbox`) that would need
re-scoping to Graham's own scratch/data conventions; and the `EXEMPT` regex `\.original\.`
etc. would need auditing against Graham's actual file-naming habits (`.superseded` is
Graham's convention for retiring files, not `.original` or `.prev.`, so the exemption
list as shipped would not protect the files it needs to on this machine).

The remaining PreToolUse guards (`risk-checkpoint.sh`, `pipestatus-guard.sh`,
`grep-portability.sh`, `ls-before-write.sh`, `lane-guard.sh`, `agent-budget.sh`,
`click-credit-guard.sh`, `paid-inference-guard.sh`, `written-call-guard.py`,
`curl-router.sh`, `linkedin-path-guard.sh`, `linkedin-browser-ban.sh`,
`outbound-copy-gate.py`) are **COMPLEMENT**: Graham has zero mechanical enforcement in
any of these areas (destructive-command interception, pipe-swallowed exit codes, PCRE
portability, clobbering finished work, expensive fan-out routing, per-tool spend
metering, outbound-message linting). The closest incumbent is prose: the global rule
"Before any command that could discard uncommitted work … run `git status` first," which
is auto-mode session guidance, not a `PreToolUse` hook, and has no negative control
proving it actually stops anything. `fetch-guard.sh` and `websearch-router.sh`
(`block: none`, reporters) are also **COMPLEMENT** — nothing warns Graham when a fetch
target moved underneath an edit, or names a cheaper lane before a paid search.

**Stop hooks (8, 6 refuse)** — **COMPLEMENT**, and the largest structural gap this
review surfaces.

Graham's `settings.json` `hooks` key has **no `Stop` entry at all** — verified directly
from the extracted `hooks` key, which contains only `PreToolUse`. Every one of
Graham's close-out conventions (the "Done" claims are made from the artifact's
user-facing behavior" rule, the ADHD skill's "restate state every turn," the
"turn-reduction" philosophy of not asking should-I questions, the standing-authorization
skill's granted/stop-list check) is enforced today by **prose alone**: CLAUDE.md text,
skill descriptions, and the model's own discipline. That is precisely the failure mode
the candidate's whole thesis, and Graham's own global rule, both name: "Prose in a rules
file is advice. A PreToolUse hook is a wall" (`hstack` README) versus "No artifact is
presented as done without executed evidence… grep, lint, and self-review do not count as
verification" (`/Users/gfm/.claude/CLAUDE.md`). Graham's rule states the standard;
`hstack`'s Stop hooks are one worked example of mechanizing an adjacent standard
(closeout shape, item coverage, handoff appropriateness) that nothing on this machine
currently does.

Within that group: `item-coverage.py` (refuses a close-out that silently drops a request
item, verified by term-overlap fingerprinting) and `handoff-gate.py` (refuses a
`YOUR MOVE` item that is actually doable by the agent, measured at 91% of a sampled
1,520-item corpus) are each genuine complements with no incumbent equivalent — nothing
here mechanically checks either property, though both restate philosophy Graham's own
memory notes already hold (`ask-intent-before-executing.md`; "decide, do not ask" appears
verbatim in `claude-improvements-weekly`'s CLAUDE.md). `capability-claim-gate.py` is the
closest structural cousin to `capability-preflight` and the global "Evidence over
assertion" rule, but works at the opposite end of the pipeline: `capability-preflight`
proves access *before* a milestone starts; `capability-claim-gate.py` catches an
unverified "X is dead" claim *after* it is already written, by checking whether the
turn's own tool calls mention the subject. These are complementary positions in the same
pipeline, not duplicates — see Philosophy conflicts below for why they should not be
merged. `person-claim-balance.py` (refuses a one-directional deficit-only reading of a
person) is a **COMPLEMENT with no current consumer**: it exists to catch a specific
failure from Howard's own relationship-analysis workflows, which is not a task type
Graham's installed skills currently perform; the underlying principle (a detector whose
errors are 100% one-directional is expressing a prior, not measuring noise) is sound and
portable, but nothing on this machine would exercise the hook as shipped.

`stop-justify.sh` and `auto-push.sh` are **COMPLEMENT**: nothing checks for a dirty
working tree or an unpushed branch at Stop. `closeout-shape.py` is **COMPLEMENT**: it
mechanizes exactly the shape Graham's global rule states in prose ("Any message that
needs a fact or decision from Graham puts that ask in its first line") but for a
different literal format (`DONE` / `YOUR MOVE` vs. whatever heading convention Graham's
sessions actually use) — porting it verbatim would require rewriting every regex against
Graham's own close-out format, not merely re-pointing a path.

**UserPromptSubmit injectors (6)** — **COMPLEMENT**, with one adoptable pattern.

None of these have an incumbent analog — Graham's session-start behavior relies entirely
on CLAUDE.md being loaded once, with no per-turn injection mechanism at all. The
adoptable pattern, independent of any specific hook, is the **"LAYER CHECK"** convention
used by `state-verify-inject.sh` and `closeout-preflight.sh`: before injecting a rule
into every turn's context, check whether an always-loaded file already verifiably
carries it, and injectors fall back to a full block only when that check fails (file
moved, heading renamed, session started somewhere the file does not reach). Quote:

> "One fact, one always-loaded layer: emit the pointer whenever that section is
> verifiably present, and fall through to the full block when it is not." (`hooks/state-verify-inject.sh:76-77`)

This is a mechanism, not a rule the library already has: it is a *checked* deduplication
between a per-turn injector and a session-start file, whereas the closest incumbent
concept (the global "Duplication and reversibility" rule: "a general rule reappearing in
a project file is drift") is enforced by human sweep, not by a hook reading the file at
runtime. Worth filing as a complement for any future Graham hook that injects text
per-turn.

**SessionStart (4)** — **COMPLEMENT**. `wiring-verify.sh` is a lightweight, automatic,
every-session version of what `phase-0-survey.md` step 5 does manually and weekly
(prove the guards are armed). `session-collide.sh` (who else is live in this tree) is a
mechanized version of the global Concurrency rule ("check who else is on it: list live
sessions on the same repo or path") — Graham's version is a standing instruction to run
a check; the candidate's version runs it automatically at every session start with no
recall required. `session-identity.sh` and `context-restore.sh` have no incumbent
analog.

### A mechanism the review's section 5 did not list

The **"LAYER CHECK" convention** described above (state-verify-inject.sh /
closeout-preflight.sh) is real, generalizable, and absent from the clean-room review's
"ideas worth taking" list, which focused on the testing machinery. It is the one idea in
the injector family worth carrying forward on its own.

## Routing collisions

If `rules/` and the hooks were installed alongside the library and the global CLAUDE.md:

- **`rules/common/git-workflow.md`** mandates a strict conventional-commit type prefix
  (`feat, fix, refactor, docs, test, chore, perf, ci`) with no exceptions stated. Graham's
  `claude-improvements-weekly` project prefixes commits `[weekly YYYY-MM-DD]` and names a
  finding id — a different, incompatible convention for the same slot in the message.
  Installing `rules/` globally would put two contradictory commit-message formats into
  context at once, and whichever loads last wins by accident — the exact failure
  `rules/common/performance.md` itself documents happening to this same author twice
  ("Two loaded rule files disagreeing about which model does the work is worse than
  either one alone, because whichever is read second wins by accident").
- **`hooks/dash-gate.sh`** would run alongside Graham's installed em-dash
  `PreToolUse` hook, enforcing the identical policy at two different scopes
  (`Write|Edit` broadly vs. `Artifact` publish only) with two different mechanisms. Not a
  contradiction — both block the same character — but a duplicate firing on any
  `Artifact` publish that is also a `Write`, and a silent behavior gap on every other
  `Write`/`Edit` that only `dash-gate.sh` would catch. Installing it without retiring or
  scoping around the existing hook creates exactly the "one fact stored twice" failure
  the candidate's own `hooks.manifest.json` exists to prevent.
- **`hooks/agent-budget.sh`** would impose hard per-session (8/24h), box-wide (40/24h),
  and weekly (200/7d) caps on `Agent` tool dispatches. Nothing in Graham's setup expects
  this. `claude-improvements-weekly`'s Phase 0 fans out `workbench:transcript-scanner`
  subagents in batches of up to 7 files each, and the global Concurrency rule
  contemplates "5 to 7 sessions run concurrently... every working day" each dispatching
  subagents — a box-wide cap of 40/24h, sized around Howard's own measured usage, would
  silently start blocking Graham's own scheduled weekly maintainer mid-run with no
  advance warning, the first time it happened.
- **`hooks/lane-guard.sh`** would block any `Workflow` tool call fanning out over 20
  items, or any `resumeFromRunId` call, pending a stated-in-chat lane justification and a
  `touch /tmp/lane-check-approved`. This directly collides with the global rule
  "Parallel write-capable subagents get disjoint file subtrees" — a pattern of
  legitimate, sanctioned wide fan-out — by inserting an unfamiliar manual approval
  ritual in front of it, tuned to a different tool (Claude's own `Workflow` primitive,
  which is not the same surface as the `Agent` tool Graham's fan-outs use, but the
  collision risk is real if Graham's environment ever exposes the same tool).
- **`rules/common/coding-style.md`**'s file-size guidance ("200-400 lines typical, 800
  max") is inconsistent with the candidate's own shipped hooks (`risk-checkpoint.sh`
  1,568 lines, `stop-justify.sh` 1,297, `closeout-shape.py` 1,293, `session-collide.sh`
  1,077) — an internal collision, not one with Graham's setup, but worth naming since
  `validate-skills.sh` enforces an actual hard cap (500 lines) on skill bodies (F7) that
  the candidate's own rule would also fail if it were a skill.

## Philosophy conflicts

**Fail-open vs. "a red validator is a bug in the content."** The global rule states: "A
red validator is a bug in the content, never in the validator. Fix the content, or
deliberately change the rule." That frames a validator's refusal as authoritative once
it fires — the content is wrong until proven otherwise. The candidate's stated default is
the opposite for the *majority* of its own guards:

> "Fail open unless the downside is money. Missing helper, unreadable payload, strange
> environment: exit 0. A guard that breaks the session when its own dependency is absent
> is worse than the risk it covers." (`docs/WRITING-A-GUARD.md`, rule 3)

> "Most hooks here fail open. … A guard that breaks the session when its own dependency
> is missing is worse than the risk it covers, and it gets deleted within a week."
> (`docs/ARCHITECTURE.md`, "Fail-open against fail-closed")

These are not the same claim measured differently — they are opposite defaults for what
"a check I cannot currently satisfy" should do. Graham's rule assumes the check is
right and blocks until the content changes. The candidate assumes the check is often
wrong or malfunctioning (`risk-checkpoint.sh`'s own header: "A guard malfunction, not a
risky command") and defaults to letting the *operator's underlying work* through rather
than the *validator's verdict*, reserving fail-closed for the two guards where the
downside is money (`lane-guard.sh`, `click-credit-guard.sh`). Both are defensible
positions for their respective contexts — Graham's rule governs a small number of
deliberately-installed, human-reviewed validators (`validate-skills.sh`); the
candidate's rule governs 37 hooks running unattended on every tool call, where an
unmaintained one that fails closed silently jams a session. Adopting `hstack` hooks
wholesale under Graham's current rule would mean either rewriting every fail-open guard
to fail closed (defeating their own stated design and likely producing the exact "gets
deleted within a week" failure they were built to avoid) or explicitly carving out an
exception to the global rule for imported hooks, which the rule as written does not
contemplate.

**The candidate's own CLAUDE.md contradicts the candidate's own rules/ directory.**
`hstack/CLAUDE.md` states: "State the goal and the constraints, not the steps.
Over-prescriptive prompts and skills reduce output quality on this model." The
candidate's own `rules/common/` (903 lines across 15 files) is almost entirely the
opposite: numbered, step-by-step runbooks (`development-workflow.md`'s five-step Feature
Implementation Workflow, `testing.md`'s six-step TDD cycle, `security.md`'s eight-item
pre-commit checklist). This is an internal contradiction, not a candidate-vs-incumbent
one, but it matters for ingest: Graham's own skill-library runbooks
(`prompts/phase-N-*.md`) are *also* numbered, step-by-step, and highly prescriptive, and
they demonstrably work in this environment (`phase-0-survey.md` is nine explicit steps).
So the candidate's stated philosophy ("state goals, not steps") should not be imported as
a general principle on the strength of this repo — the repo's own best-engineered
artifacts (the hooks, `dead-branch-sweep.py`, `parity.py`) are the product of extremely
specific, incident-cited, step-level prose, not generic goal statements. The CLAUDE.md
line reads as advice for one particular model's raw prompting style, not as a verdict
on runbook-style engineering, and conflating the two would be a mistake at ingest.

**"Decide, do not ask" — same philosophy, different mechanism, not redundant.**
`handoff-gate.py`'s thesis ("91% of items handed to the owner did not need him") restates
Graham's own memory note `ask-intent-before-executing.md` and the verbatim rule in
`claude-improvements-weekly`'s CLAUDE.md ("Never ask… Anything you would have asked
becomes a Tier 3 queue entry"). These agree in substance. They differ in mechanism and
therefore should not be merged into one: `standing-authorization` intervenes **before**
a question is asked (a manifest of pre-approved actions, checked against the phrasing of
the question itself); `handoff-gate.py` intervenes **after** a close-out is already
written, by pattern-matching the `YOUR MOVE` section for phrasings that hand back a
decision the agent could make. A system with both would catch different failure
instances: `standing-authorization` catches the mid-turn "should I…" question before it
interrupts the user; `handoff-gate.py` catches an already-composed close-out that quietly
parks work under a differently-worded ask that never triggered a `should-I` phrasing at
all. Complementary, not duplicative.

## Corrections needed at ingest

Factual errors independently verified by reading the primary files (not taken on the
review's word alone):

- **Hook count.** README title says "Thirty-one," README table and `hooks.manifest.json`
  both say 37 (confirmed by counting `"file":` entries in the manifest myself: 37).
- **Python hook count**, stale in three separate files, all read directly: `README.md:106`
  ("python3 for the four python hooks"), `docs/INSTALL.md:82` ("python3 (four hooks are
  python…)"), `docs/TROUBLESHOOTING.md:11` ("Four hooks are python"). Actual count from
  the manifest: 10 (`prompt-items.py, carryover-queue.py, closeout-shape.py,
  outbound-copy-gate.py, item-coverage.py, capability-claim-gate.py, handoff-gate.py,
  written-call-guard.py, owner-facts.py, person-claim-balance.py`).
- **License.** `LICENSE` is 290 bytes and stops mid-sentence after "to deal in the
  Software without restriction." — verified by reading the file directly. It is missing
  the grant of rights to copy/modify/distribute/sublicense, the attribution condition,
  and the liability limitation. It is not a valid MIT license as shipped. This is the
  single highest-priority fix before anything else here, per the repo's own stated
  standard ("no license means no adoption," `README.md`).
- **`docs/ARCHITECTURE.md` prose numbers**, verified directly against the manifest count
  I performed myself (17 PreToolUse hooks, 15 of which have `block != "none"`; 8 Stop
  hooks, 6 of which have `block != "none"`): the prose twenty lines below the (correct)
  ASCII diagram reads "Nine of the twelve `PreToolUse` hooks and both blocking `Stop`
  hooks" — both numbers stale (12 should be 17, "both" should be "six").
- **CHANGELOG stale wording**, verified directly: "Sixteen to twenty-five" under the
  0.2.0 entry, when the repo now ships 37.
- **Scrubber damage that shipped**, verified directly in `docs/CORRECTIONS.md`: the
  "context measurement confounds" entry reads `~/.the local proxy/events.jsonl`, a
  redaction artifact (a product name replaced mid-word by "the local proxy" without
  checking the result reads as English).
- **Six hooks with an unresolvable runner and an unexpanded shebang**, verified directly:
  `hooks.manifest.json` gives `"runner": "python"` (not `python3`) for exactly
  `item-coverage.py, capability-claim-gate.py, handoff-gate.py, written-call-guard.py,
  owner-facts.py, person-claim-balance.py`, and I opened all six files myself — every one
  opens with the literal shebang `#!$HOME/.venvs/agent-libs/bin/python`, an unexpanded
  environment variable pointing at the author's private virtualenv. `doctor.sh`'s own
  fallback (`shutil.which(runner) or shutil.which(runner + "3")`, read directly at lines
  113-115 and 129-131) silently substitutes `python3` and reports these six **armed**,
  which is the exact "present, registered, never fires" failure the tool exists to
  catch, on the tool itself.
- **A stateless model cannot honor** the routing tables `curl-router.sh`,
  `websearch-router.sh`, and `click-credit-guard.sh` depend on
  (`~/.claude/reference/capability-routes.json`, `click-routing.md`) — all three fall
  silent (not wrong, just inert) on a fresh install with no routes file, which is
  documented behavior (`curl-router.sh:44`, `[ -f "$ROUTES" ] || exit 0`) but means the
  guards ship as no-ops until a new owner writes their own routing table by hand; nothing
  in the repo prompts for this at install time.
- **Style violations against the library's own conventions**: no `.superseded` renaming
  convention exists in the candidate (superseded routing tables or dead hooks are simply
  deleted or left commented, per `CHANGELOG.md`); several `rules/common/*.md` files use
  em dashes nowhere I found (consistent with Graham's own no-em-dash rule, so no
  violation there), but `rules/common/writing-style.md` itself documents the em-dash ban
  as a **rule to enforce in output to a third party**, not a repo-wide style guide for
  markdown documentation — the distinction matters if any of this prose is copied
  verbatim into Graham's own rule files, which do not currently separate "how Claude
  should write to Graham" from "how documentation should read."

## Net assessment

If only three things could be taken:

**1. Port `tests/negative-control.py`'s methodology to prove Graham's own installed
em-dash `PreToolUse` hook by deliberate failure.** Effort: **S** (under an hour). Target:
a new small test file, e.g. `/Users/gfm/.claude/hooks/tests/em-dash-negative-control.sh`
or a script under `/Users/gfm/skill-library/scripts/`. This is the direct, concrete
answer to whether any candidate mechanism turns the global rule's own sentence — "a
check that has never failed a fixture is untested" — into something executable here: the
one hook on this machine has never been fed the exact payload it exists to refuse, nor an
ordinary payload it must let through. `negative-control.py`'s block/allow verdict pair is
the right shape for exactly this, ported as a concept (feed the hook a file containing an
em dash via stdin in the hook's own JSON shape, assert `permissionDecision: deny`; feed it
an ordinary file, assert allow), not as code (the candidate's harness is built around its
own 37-hook manifest and would need stripping to the one hook, not extending).

**2. Take `dash-gate.sh` as a fragment, not a hook.** Effort: **S-M** (under an hour to
port the codepoint-based detection and the `EXEMPT` pattern; the M side is the
deliberate scope decision named above — whether to broaden from Artifact-publish-only to
all Write/Edit). Target: rewrite the installed hook in
`/Users/gfm/.claude/settings.json`'s `PreToolUse` block, replacing the single-purpose
`grep -q '—'` with a small script carrying the three real improvements: codepoints
instead of literal characters (so the hook file cannot self-block), en-dash and
horizontal-bar coverage alongside em dash, and an exemption list re-scoped to Graham's
own conventions (`.superseded` files, `/private/tmp/claude-501/**` scratch paths) rather
than Howard's (`node_modules`, `.git`, `queue|transcripts|inbox`). Do not broaden the
trigger scope from `Artifact` without deciding that deliberately — that is a real
behavior change, not a drop-in improvement.

**3. Treat the Stop-hook gap as a phased-harness candidate, not a quick port.** Effort:
**L** (multi-session). This repo's single biggest finding for Graham's setup is
structural, not any one file: zero mechanical enforcement exists today for close-out
shape, item coverage, or handoff appropriateness, despite prose rules on this machine
already stating all three (the ADHD skill, `ask-intent-before-executing.md`,
`claude-improvements-weekly`'s "Never ask"). `item-coverage.py` and `handoff-gate.py` are
the concrete templates, but neither ports directly: both are built against Howard's
specific close-out format (`DONE` / `YOUR MOVE` headings) and both carry a documented,
hard-won tuning history (MIN_TERMS backtested against a week of real turns; the `PASTED`
and `INFORMAL` filters added only after measured false-positive runs). Reproducing that
tuning against Graham's actual close-out conventions and actual turn corpus is real work,
not a file copy, and belongs in `workbench:phased-harness` rather than being applied as a
same-session edit. Target: a new phased-harness project scoped to "mechanize close-out
verification," informed by these two files as reference implementations, not as source
to import.
