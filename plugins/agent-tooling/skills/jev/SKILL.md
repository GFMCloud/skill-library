---
name: jev
description: >-
  Find where TypeSafe's Jev model fits in the current project, then fold it in the way
  Graham's lessons showed: scan for per-item judgments, run the fit check (can code
  assemble the evidence?), draft the decision and its definitions from the project's own
  data for Graham to edit, then build a reviewed questions.py with a pinned model,
  fail-closed validation and a review band, measured against past decisions. Use when
  Graham says "use Jev", "add a Jev check", "TypeSafe", "System One", "where could Jev
  help here", or asks whether a cheap typed judgment could replace an LLM call or a
  manual review step. Loads first; for the API, SDK and question-type reference read
  typesafe:typesafe-ai, which this skill does not restate. Not for bulk text rewriting or
  extraction that produces text (llama-offload), not for private data while the data
  decision says public only. Costs a project scan, one short interview, and API spend
  printed on every run.
metadata:
  maturity: incubator
---

# Jev

Decide whether Jev fits a project, and if it does, build the narrowest useful Jev step
into it and measure it against decisions already made.

**The one thing to hold onto:** Jev is the cheap last step of a pipeline. It returns
probabilities about evidence you hand it, and the answer is capped by that evidence. In
Graham's lessons the questions barely moved the results; the evidence packet did (title
only: confidence 0.24; one-line rule text: confidently wrong; the real records in full:
twice the agreement). Most of the work is building the packet.

## Step 0: preflight (every time, before anything else)

1. Key present, never printed: `test -n "$TYPESAFE_API_KEY" && echo "key present"`. If
   absent, stop and hand Graham the storing command in
   [references/setup.md](references/setup.md); never ask for the key in chat, never
   write it anywhere, never register an MCP server with the key as an `-e` literal.
2. Read `~/work/jev-lab/DATA-DECISION.md`. While it says public only, no private data
   (email, transcripts, personal or customer records, private repo contents) goes to
   TypeSafe. Ask Graham once per project whether the data is public if it is not obvious,
   record the answer in the project's `DONE.md`, and do not raise it again.
3. Official plugin present: `claude plugin list 2>&1 | grep -c typesafe` returns 1. Read
   `typesafe:typesafe-ai` before writing code; it points at the live docs, which change
   weekly.

## Step 1: find the decision points

Scan the project for places where a per-item judgment over text is made today:

- an LLM call that classifies, filters, matches, routes or checks (look for
  `anthropic`, `openai`, `claude -p` with a prompt that asks for a label or yes/no);
- a heuristic standing in for judgment (keyword lists, regex classifiers, fuzzy string
  matching such as `rapidfuzz` or `token_sort_ratio`, hand-tuned scores);
- a manual review queue or a log of human verdicts (columns named disposition, verdict,
  status, label, reviewed, SKIP, keep or drop);
- a pipeline stage that reads free text and branches.

List each with its file and line, the judgment it makes, and roughly how many items pass
through it. Then match each to a shape in
[references/use-cases.md](references/use-cases.md); that catalogue covers a dozen shapes
from the TypeSafe docs, cookbooks and the repos reviewed, with fit signals for each. Do
not stop at the first candidate: two or three candidates with a ranked verdict beat one.

## Step 2: the fit check (a gate, not a formality)

For each candidate answer these, in order. The first is decisive.

1. **Can code assemble the evidence the decision is really made against, in full?**
   The item itself (not a summary another model shortened) plus every reference record a
   careful human would check (the rule text, not its title; the candidate record, not
   its id). If assembling it takes research (fetching docs, reading code, multi-step
   reasoning), Jev adds little: whatever does the research can usually make the call.
   Say so and stop for that candidate.
2. Is the judgment narrow and typed, with the options known in advance?
3. Is there volume, latency or cost pressure that makes an LLM call wasteful?
4. Do known answers exist (past verdicts, a labelled log), or can Graham label 20 to 30
   items in a few minutes?
5. Is the data allowed under Step 0?
6. Is a wrong answer bounded, or can a review band catch the unsure middle?

Report the verdict first, in one line per candidate: strong fit, weak fit, or no fit,
with the reason. Measured examples: the weekly scout's novelty triage was a weak fit
(its deciding facts come from verification the orchestrator does); fantasy player ID
matching is a strong candidate (code already holds both records). Recommend one.

## Step 3: review the data, then draft, then ask

Before asking Graham anything, read what the project already holds:

- the known answers: where past decisions live, how many, what vocabulary they use, and
  whether that vocabulary was ever defined (the scout's four novelty labels never were);
- the reference records the decision is checked against, and whether they can be pulled
  in full as of the date each past decision was made (git history is the usual source;
  a record added later leaks the answer);
- a tuning set and a held-out set, split before the first question is written.

Then draft, in Graham's own terms, for him to edit rather than answer from blank:

- the decision and what code does with each answer;
- each option's definition as what / not_for / examples, drawn from real past cases,
  with the examples held out of the test sets;
- the boundary calls the data could not settle (usually one or two), each with a
  recommended answer.

Ask at most four questions, all at once, only for facts the files cannot supply: where a
boundary sits, what a wrong answer costs, which past decisions to trust. If he says "go
with your recommendation", do. Propose a Done when for the Jev step with a spend ceiling
(every lesson run together cost about $0.14; a ceiling of $1 leaves room).

## Step 4: build

Copy [templates/questions.py](templates/questions.py), [templates/test_questions.py](templates/test_questions.py)
and [templates/evaluate.py](templates/evaluate.py) into the project and adapt them. The
contract, proven in the lessons:

- every question and threshold in `questions.py`, one file a person can review;
- `MODEL` pinned to a versioned id (not `jev-latest`) once thresholds are set, with the
  reason in a comment; the response's `model` field checked on every call;
- a missing answer or a different model raises; nothing defaults to a safe-looking value;
- routes in code, with a middle band that goes to review, never a guess;
- thresholds labelled provisional until a held-out run supports them;
- `test_questions.py` proves the gate by deliberate failure with a fake client, no API
  call, before any real run.

Question design rules and the evidence behind each are in
[references/question-design.md](references/question-design.md). Read it before writing
the first question. The short form: state holds the evidence and anything to compare
against; instructions ask one narrow thing and point at state fields with backticks;
criteria are the yardstick, and Jev judges only against what they say.

## Step 5: measure, revise once, hold out

Run `evaluate.py` on the tuning set, read the misses by class, revise, then run the
held-out set once. Report:

- agreement with past decisions, per class, never "accuracy" (the labels are someone's
  past calls, not ground truth);
- how many answers cleared the confidence or margin gate, and how many of those were right;
- spend from `usage.input_tokens`, printed at the end of every run;
- for any difference under about 3 items in 25, a rerun before believing it (identical
  inputs moved by 3 items across runs in the lessons).

Label any fixture or fake data as such wherever it appears. A result derived from a
fixture is never reported as a finding about real data.

## Known weaknesses of this method

- Measured on one project (the scout) with a held-out run that was used once for a
  revision; every threshold number in the references is dated and provisional.
- Jev catches a contradiction an item states, not one that needs outside evidence or an
  inference step; rules phrased as prohibitions draw false disputes.
- "Give every Choice a way out" is the docs' advice, not something the lessons measured.
- Jev reads English best; other languages are accepted at lower accuracy.

## Inputs

The current project directory and its data; the key in the environment; the official
`typesafe` plugin; `~/work/jev-lab/DATA-DECISION.md`; Graham for at most one round of
up to four questions.

## Verify

`python test_questions.py` passes (the gate raises on a missing answer and on a
different model); `python evaluate.py` prints agreement on the tuning and held-out sets,
the gated count, and total spend; the key never appears in any output or file.

## Done when

Either the project holds a `questions.py`, a passing `test_questions.py`, and a held-out
run with agreement and spend reported and recorded in the project's `DONE.md`; or
Graham has a one-line "not a fit" verdict per candidate with the reason.

## Stop when

- The key is missing: hand over the storing command and stop.
- The only candidates need research to assemble their evidence: report "no fit" and stop.
- The data is private and the data decision says public only.
- No known answers exist and Graham cannot label 20 items: stop and say what labelling
  would take.
- The spend ceiling in the Done when is reached.
