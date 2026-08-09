---
name: skill-discovery
description: >
  Mine recent Claude sessions to discover workflows Graham runs repeatedly from
  scratch that should be codified as skills. Trigger when Graham says "what should
  I turn into a skill", "find new skills", "what am I doing repeatedly", "skill
  discovery", or "mine my sessions for workflows". Scans up to 50 sessions using
  a fan-out pattern - batch scanners run in parallel, a compression pass handles
  large outputs, then a synthesis agent clusters by structural similarity and ranks
  candidates by frequency x friction. Outputs a ranked list of skill candidates with
  trigger phrases, workflow outlines, and evidence.
metadata:
  maturity: incubator
---

# Skill Discovery Workflow

Mines recent Claude sessions to find workflows Graham runs repeatedly from scratch
that should be codified into skills. The core signal is re-setup cost - tasks where
Graham had to re-explain context, re-establish a sequence, or start from zero that
he'd done before.

---

## Confirm before starting

"I'll scan your recent sessions for workflows you keep running from scratch. Takes
a few minutes - I'll run batch scanners in parallel. Ready?"

---

## Phase 0 - Verify tools, then list sessions and batch

Before anything else, confirm the session-mining tools are actually available in
this environment: `mcp__ccd_session_mgmt__list_sessions`,
`mcp__ccd_session_mgmt__get_session`, `mcp__ccd_session_mgmt__search_session_transcripts`,
and `mcp__ccd_session_mgmt__list_events`. If any of them are missing, or a call fails
with a "tool not found" style error rather than a normal empty result, stop and tell
Graham plainly that session-mining tools aren't available here, so the skill can't run
in its normal form. Offer a fallback instead of failing quietly - for example, ask him
to paste a few recent session summaries or transcript excerpts directly, and run the
Phase 1 extraction logic against that pasted text instead of live tool output.

Once tools are confirmed, use `mcp__ccd_session_mgmt__list_sessions` with `limit: 50`.
This tool already excludes the current session from its results, so no manual
filtering is needed there.

Split the returned sessions into batches of 10. Up to 5 batches.

---

## Phase 1 - Fan-out batch scanners

Spin up one agent per batch simultaneously (all in a single message, multiple Agent
tool calls). Each agent uses the Phase 1 prompt below with its batch of session IDs.

### Phase 1 agent prompt

---

You are a workflow extraction agent. Scan each session transcript and extract
structured information about what workflow was performed. Your job is pure extraction -
no assessment of whether something should be a skill. That happens later.

**Sessions to scan:**
[SESSION_ID_LIST_FOR_THIS_BATCH]

**For each session:**

There is no single call that returns a whole transcript, so reconstruct enough of
each session from three tools:

1. Call `mcp__ccd_session_mgmt__get_session` for orientation - title, creation time,
   model, and branch/worktree info. This is metadata only, no conversation content.
2. Call `mcp__ccd_session_mgmt__list_events` with a limit of around 40 and no
   `before_uuid` to get the most recent slice of the transcript (it returns events
   most-recent-last).
3. If that slice isn't enough to identify the workflow or judge re-setup cost, page
   backward: call `list_events` again with `before_uuid` set to the earliest event's
   uuid from the previous call. Repeat up to two more times (roughly 150 events total,
   mirroring the old "first 150 turns" budget) or stop earlier once a call returns
   fewer events than the limit - that means you've reached the start of the session.
   Read the batches in chronological order (oldest batch first) once you're done
   paging, since each new page you fetch is further in the past than the last.
4. If it's clearly a single-action task within the first slice (roughly the "20 turns"
   equivalent), stop paging and move on - no need to page backward on a short session.
5. If CONTINUATION status is still unclear after reading the events you gathered, use
   `mcp__ccd_session_mgmt__search_session_transcripts` with a query like "continuing
   from" or "picking up where we left off" and check whether this session's title
   shows up among the hits.

This reconstruction is an approximation, not a guaranteed full transcript - if you hit
the paging budget before reaching a clear task boundary, note that in RE_SETUP_DETAIL
(e.g., "partial context only, paging budget exhausted") so Phase 2 can weight it
appropriately.

**Extract this structure for every session:**

```
SESSION: [title]
CONTINUATION: [yes / no] - was this explicitly picking up from a previous session?
  (look for: handoff references, "continuing from", "picking up where we left off")
TASK: [one sentence - what was the actual goal?]
STEPS: [numbered sequence - what happened in what order, at a high level]
INPUT_TYPE: [document | conversation/notes | raw data | URL/web | code | verbal brief | other]
OUTPUT_TYPE: [document | analysis | communication | automation | code | research | planning | other]
RE_SETUP: [high / medium / low / none]
  high   = Graham pasted substantial background context, re-explained something
            he'd clearly explained before, or said "like we did before" then
            had to re-setup anyway
  medium = some context establishment but not excessive
  low    = minimal - Claude had context or task was self-contained
  none   = no re-setup needed at all
RE_SETUP_DETAIL: [what specifically did Graham have to re-establish? one sentence, or "n/a"]
FRICTION: [what slowed it down, required rework, or caused repeated clarification?
           or "none observed"]
DURATION: [single-turn | short (2-10 turns) | medium (10-40 turns) | long (40+ turns)]
```

For sessions with no workflow (pure Q&A, single-turn factual questions, trivial
one-liners):

```
SESSION: [title]
SKIP: [one sentence - e.g., "single-turn factual question, no workflow to extract"]
```

**Output:** All session extractions in order, then a blank line, then this line:
`EXTRACTED: [N] sessions | SKIPPED: [N] sessions | CONTINUATIONS: [N] flagged`

---

## Phase 1.5 - Compression pass (conditional)

After all Phase 1 agents return, count the total word count of their combined output.

**If total output exceeds 12,000 words:** Run a compression agent before Phase 2.

### Compression agent prompt

---

You are compressing workflow extraction summaries for clustering. For each session
extraction, reduce it to this compact format. Preserve all factual content - just
cut narrative and compress language.

[PASTE ALL PHASE 1 OUTPUT]

**Output format for each session:**

```
[SESSION TITLE] | CONT:[Y/N] | TASK:[10 words max] | STEPS:[count] |
IN:[input type] | OUT:[output type] | SETUP:[H/M/L/none] | FRICTION:[brief or none]
```

Skipped sessions: one line each - `[TITLE] | SKIP`

---

**If total output is under 12,000 words:** Skip this phase and pass Phase 1 output
directly to Phase 2.

---

## Phase 2 - Synthesis

Pass all Phase 1 output (or compressed output from Phase 1.5) to a single synthesis
agent using the prompt below.

### Phase 2 synthesis agent prompt

---

You are a skill synthesis agent. Your job is to cluster workflows by structural
similarity and produce a ranked list of skill candidates. Follow the steps in order.

**Input:**
[PHASE 1 OUTPUT OR COMPRESSED OUTPUT]

---

**STEP 0 - Quality check (do this first)**

Scan the extractions. Flag any that are too sparse to cluster (missing TASK, missing
STEPS, or clearly misextracted). List them at the top of your output as:
`EXCLUDED (poor extraction): [session title] - [reason]`

Exclude all sessions flagged CONTINUATION: yes from frequency counts. They can inform
workflow shape but don't count as independent instances.

---

**STEP 1 - Check against installed skills**

Before clustering, eliminate any workflows already covered by these installed skills.
If an extracted workflow maps cleanly to an existing skill, exclude it from candidates.
Note exclusions briefly.

Installed skills to check against.

This list must match the marketplace. If it drifts, this skill will propose skills that
already exist. Regenerate it from the repo rather than editing it from memory:

    python scripts/list-skills.py

**voice**
- graham-voice (drafting and editing anything outbound in the user's voice)

**deck-build** (installed, disabled by default)
- deck-scaffolding-builder (planning a deck: blueprint, design spec, layout map, wireframe)
- cd-to-pptx (Claude Design HTML deck export into native editable PowerPoint)
- chart-discipline (chart type selection, data encoding, annotation on numeric charts)
- html-diagram (standalone interactive architecture, system, and flow diagrams)

**deck-critique** (installed, disabled by default)
- layout-critique (does a slide READ: visual hierarchy and legibility pass)
- sales-lens-review (does an asset SELL: sales-leader gut check)

**frontend-design**
- design-taste-frontend (premium greenfield frontend builds)
- redesign-existing-projects (upgrading an existing codebase in place)
- minimalist-ui (minimal, editorial, document-style aesthetic specifically)
- image-taste-frontend (settling the design visually first, then implementing to match)

**workbench**
- skill-discovery (this skill)
- capability-index (points at packs that are installed but disabled)
- supahcode-review (code review workflow)
- model-effort-advisor (which model and effort level for a given task)
- folder-to-repo (turning a loose folder into a proper git repo)
- project-kb-builder (source document into Claude Project knowledge files)
- project-setup-wizard (setting up a new Claude Project)
- systems-design (backwards design methodology, planning)
- fable-project-review (deep project review producing an executable improvement plan)
- adhd (shaping response output for an ADHD reader, on explicit /adhd invocation)
- llama-offload (offloading bulk mechanical text transforms to a local Ollama model)
- handoff (packaging a session into a summary a fresh session can pick up from)

**scl**
- scl-keeper-logic-validator (SCL keeper cost, contract length, placement rules)
- scl-session-startup-enforcer (SCL session startup sequence and guardrails)
- scl-module-deploy-checklist (SCL staging to production deploy sequence)

Also assume Claude's stock skills are present and do not propose rebuilding them:
docx, pptx, pdf, xlsx, canvas-design, brand-guidelines, mcp-builder, frontend-slides,
web-artifacts-builder, skill-creator, consolidate-memory, doc-coauthoring,
learn, schedule.

`handoff` is the exception. A customized fork of it lives in `workbench` above, so treat it as a
marketplace skill, not a stock one.

---

**STEP 2 - Cluster by structural similarity**

Group remaining sessions into clusters. Two sessions belong in the same cluster
if they score 4/5 or higher on this checklist:

1. TRIGGER: Would Graham use a similar phrase to start both? (same intent)
2. INPUT: Same input type going in?
3. OUTPUT: Same output type coming out?
4. SEQUENCE LENGTH: Similar number of steps (within 2-3 steps)?
5. DECISION POINTS: Same intermediate decisions or judgment calls required?

Score 4-5: same cluster
Score 3: flag as "possible overlap" - keep separate but note it
Score 0-2: different clusters

**Threshold rules:**
- 4+ sessions in a cluster = High priority candidate (build now)
- 2-3 sessions = Watch list (flag, don't build yet)
- 1 session = exclude from candidates (note if friction was extreme)

---

**STEP 3 - Score and rank**

Score each qualifying cluster (4+ sessions):

FREQUENCY: count of non-continuation sessions in the cluster
FRICTION: highest re-setup level across sessions in the cluster
  (one "high" in the cluster makes the cluster high friction)

PRIORITY = Frequency x Friction:
- High x High = P1 (build immediately)
- High x Medium = P2
- Medium x High = P2
- High x Low = P3
- Medium x Medium = P3
- anything x Low = P4

---

**STEP 4 - Write candidate cards**

For each cluster scoring P1 or P2, write a full candidate card.
For P3 and P4, write a short card (name, triggers, evidence only).

**Full candidate card format:**

---
## [Candidate name - describe the workflow, not the topic]
## e.g., "Call notes → structured CRM log + follow-up email" not "Salesforce work"

PRIORITY: P[1/2] | Frequency: [N sessions] | Friction: [H/M]

TRIGGER PHRASES (what Graham would actually say):
- "[phrase]"
- "[phrase]"
- "[phrase]"

WORKFLOW THIS SKILL WOULD ENCODE:
1. [step - outcome-oriented, not activity]
2. [step]
3. [step]
[5-8 steps max - the skeleton, not full instructions]

RE-SETUP COST ELIMINATED:
[What Graham would no longer have to re-explain or re-setup each time - be specific]

EVIDENCE:
- [session title]: [one sentence on what happened]
- [session title]: [one sentence on what happened]

DRAFT SKILL DESCRIPTION (for SKILL.md frontmatter, 2-3 sentences):
[What it does, when to trigger, what it outputs - match the style of existing
skill descriptions]

---

**Short card format (P3/P4):**

[Candidate name] | P[3/4] | [N] sessions | Triggers: "[phrase]", "[phrase]"

---

**STEP 5 - Watch list and exclusions**

Watch list (2-3 session clusters):
[Name] | [N] sessions | Friction: [H/M/L] | Sessions: [titles]

Explicitly not candidates:
[Thing that came up frequently but shouldn't be a skill] - [one sentence why]

---

## Phase 3 - Present to Graham

After synthesis returns:

1. Show Priority P1 candidates first in chat. Don't bury Graham in the full list.
2. For each P1 candidate, ask: "Build this now or add to backlog?"
3. After P1 decisions, show P2 candidates.
4. Offer to save P3/P4 and the watch list as a backlog file.

Don't show everything at once. Work P1 → P2 → offer to save the rest.

---

## Post-run offer

After presenting results:
"Want me to schedule this to run automatically every 30 sessions?"

---

## What makes a strong skill candidate vs. a weak one

**Strong:**
- Multi-step sequence with a clear input type and clear output type
- The sequence is repeatable - same steps work across different instances of the task
- Graham has domain knowledge baked into the steps (not just "do research")
- There's a real starting point that can be templated (context Graham keeps re-establishing)
- The output type is consistent (always a doc, always an email, always a plan)

**Weak:**
- Tasks that happened to be complex but won't recur in the same form
- Tasks where Graham's judgment IS the whole workflow (nothing to encode)
- Tasks that are one-liners once you know what you're doing
- Tasks already covered by an installed skill
- Tasks so varied that "same skill prompt" would mean a blank page

When in doubt, put it on the watch list. Better to catch it again next run with
more evidence than to build a skill that encodes one instance.
