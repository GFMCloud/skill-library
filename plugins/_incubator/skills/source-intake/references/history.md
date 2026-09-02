# Why source-intake is shaped this way

Three attempts at the same problem on this account. The first two were retired;
the third shipped a real change on its first run. The differences are the rules.

## Attempt 1: source-triage harness (retired 2026-08)

A launchd collector pulling feeds twice daily, Ollama scoring, a daily digest,
and GitHub issues for phone triage. It deliberately built no worker: after
fourteen days of live operation, label activity was to decide whether anything
would ever be applied. Archived at
`~/work/archive/source-triage-harness.superseded`. Lesson: intake without an
execution path measures interest, not value.

## Attempt 2: source-review + source-harvest (retired 2026-08-30)

A two-skill pipeline: a review note committed to a private notes repo under a
versioned contract, and a harvest skill that would apply the note weeks later
from Claude Code. Four days of operation: three notes, zero applied changes;
`source-harvest` never ran once.

The judgment layer worked. The notes were contract-compliant, the untrusted
content rule fired correctly, and a blind incumbent comparison (step 3b) caught
a real bias. **The transport layer never worked.** The skill declared "designed
to run anywhere: mobile chat or Claude Code, assume only web fetch plus the
GitHub connector", but the runtime actually used was a cloud session holding a
token scoped to `claude/*` branches that could not write `main`. Two of three
notes stranded on unmerged branches, invisible to the very INDEX.md meant to
prevent duplicate reviews. Three consecutive diagnoses proposed fixing the write
instruction while the environment went unchecked.

Two rules fall out of this, both now in `SKILL.md`:

- **Step 0 is an environment gate, not a preference.** The skill runs in Claude
  Code on the laptop or it does not run. There is no degraded mode, because the
  degraded mode is where the work went to die.
- **No index file.** A hand-maintained INDEX.md beside the files it indexes is a
  denormalized cache: it drifts, and it becomes the only merge-conflict surface
  between concurrent runs. `ls docs/reviews/` is the index.

Kept from attempt 2 because they were right: the ADOPT / HARVEST / WATCH / SKIP
vocabulary with SKIP expected to be common, the mandatory adoption cost, the
untrusted-content and clone-and-run rules, the effort scale, and the insight
behind the blind comparison.

## Attempt 3: the taste-skill run (2026-09-01)

`Leonxlnx/taste-skill`, a 13-skill design-taste collection, reviewed and merged
into the installed `frontend-design` plugin in one day. Record:
`~/work/archive/taste-skill-merge-closed-2026-09-01/STATE.md`. What was different:

- **A clean room that is actually empty.** `claude -p --setting-sources ""`
  with read-only tools loads no CLAUDE.md, no skill listing, no memory. The
  reviewer could not anchor on the incumbent because it had never heard of it.
  Attempt 2's step 3b tried to get the same effect by stripping labels and
  spawning per-candidate subagents inside a session that still had everything
  loaded; the headless run is simpler and honest.
- **The comparison stage found shared ancestry.** The installed pack turned out
  to be a curated fork of an earlier generation of the source, written in its
  own merge note. That reframed "install or not" into "pull upstream's
  post-fork corrections", which no single-pass review would have found. The
  comparison prompt now asks for ancestry explicitly.
- **The decisions table was the seam, and it lived inside the thing that
  executed it.** Attempt 2's note contract was the same idea in a repo waiting
  for a harvest that never came. Here the table was pre-seeded into a
  `phased-harness` Gate A and ruled in one batch (36 rows, four questions).
- **Everything ran on the laptop** with a local clone and `gh`, and the run
  itself pushed, opened the PR, merged on green CI, and refreshed the plugin
  caches under a single Gate B confirmation.

Weak spots recorded there, so they are not repeated: harness runbooks carried
five small errors the run had to route around as anomalies (a changelog file
that did not exist, a Tailwind-only proxy on a vanilla-CSS page, a control
plugin built from one file instead of the directory, a `.superseded` check
phrased as `grep` instead of `find`, inventory regeneration in the wrong phase);
and the behavior test discriminated on eyebrows and serif but not on reduced
motion, because the old body never mentioned it and the model emitted it
anyway. Pick discriminators the old artifact provably lacked in output.

## The label-blind judge (from attempt 2, kept as a bias check)

Use when Step 3's comparison returns "keep ours" on every row and you want to
know whether that is the incumbent defending itself:

1. Extract both artifacts into neutral form, stripped of adoption status. No
   "installed", "ours", "current", "new"; Candidate A and Candidate B only.
2. Spawn one subagent per candidate with an identical rubric (what it does,
   strengths, weaknesses, failure modes, maintenance surface). Each sees only
   its own candidate and never learns an alternative exists.
3. A third subagent, the judge, sees only the two structured reports and never
   the labels, and rules: adopt B and retire A, amend A with named items from B,
   keep A, or replace both. Replacement and retire-both are first-class
   outcomes, not concessions.
4. Record which agent saw what.
