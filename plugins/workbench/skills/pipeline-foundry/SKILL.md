---
name: "pipeline-foundry"
description: "Turn a project idea into a complete handoff scaffold a fresh Claude Code session can execute from with minimal human intervention. Use when starting a new project, preparing work for delegation, writing a project brief or handoff, or when a project needs scoping before execution. Runs a conversational intake, establishes decision authority and standing constants, maps needs against installed marketplaces, and emits a repo scaffold as a zip. Refuses to emit a handoff until every readiness check passes; recommending that a project be tabled is a legitimate outcome."
metadata:
  maturity: incubator
---

# pipeline-foundry

Turn a project idea into a **handoff scaffold** — the complete contents of a project repo
that a brand-new Claude Code session, with zero conversation context, can execute from.

**This skill does not execute the project.** It is a routing and packaging skill. Three
jobs, in order of how often they get skipped:

1. **Definition** — pressure-test intent, outcome and scope until concrete.
2. **Delegation** — establish decision authority, ceilings and escalation rules so the
   executor does not route every fork back to a human.
3. **Gatekeeping** — refuse to emit a handoff until every readiness check is green.

**The intake is a commitment filter, not overhead.** A project that cannot survive an hour
of definition will not survive three weeks of execution. Do not apologise for the depth,
and do not inflate a small project to justify it — the milestone-1 test in §6 exposes
inflation in both directions.

---

## The problem this exists to solve

Read this before running an intake. Every section below is aimed at it.

Nine prior projects were mined. They did not die from bad decisions or from waiting on
approvals. **They died from turn volume** — the cumulative cost of check-ins. Where
intervention density is computable it runs **3+ per hour sustained**, and every source
report states its own count is a floor.

The turn mix says which turns to attack. Of 133 located interventions, the largest slice
by far is the human supplying an external fact, a scope call, or domain judgment the
executor could not derive. The smallest slice is the executor having a recommendation and
the human agreeing. **Widening decision authority attacks the smallest slice.** So the
intake's highest-value output is not permissions — it is the constants block (§3) and
execution ownership (§4).

**Secondary cause, 9 of 9 projects: nothing noticed when the human stopped.** Silences of
11–21 days on work correctly self-assessed as nearly done, with unblocked queues sitting
untouched. §8 exists for this.

---

## 1. Intake — conversational, not a form

Take whatever is offered — a sentence or a page. Infer what you can. **Ask only what
blocks routing.** Depth scales with complexity: a small project with good specialist
coverage gets a fast intake; a novel or fuzzy one gets a deep session and possibly a
follow-up.

Do not walk a checklist at the person. The list below is what must be *established*, in
whatever order the conversation naturally goes:

- **Intent and outcome** — what is being built, why, and what "done" looks like in
  verifiable terms
- **Classification** — build / research / content / creative / hybrid
- **Constraints** — platform, stack, budget, timeline, hard boundaries
- **Standing constants** (§3)
- **Decision authority** (§4)
- **Asset mapping** (§5)
- **Gap disposition** (§6)
- **Milestone plan** (§7)

**Ask about hard boundaries explicitly.** Pre-declared boundaries held across the entire
corpus; undeclared ones drifted. One project that declared "confirm before applying a
public-access change" got an executor that hit exactly that line, refused, reverted its own
partial change and escalated. Another that never declared sandbox-versus-production ran
every write against live production under an admin principal. **The difference was whether
anyone said it out loud.**

---

## 2. Scale the intake to the project

| Signal | Intake shape |
| --- | --- |
| Small scope, existing specialist coverage, clear outcome | Fast — confirm, map, emit |
| Novel domain, or outcome stated as an activity rather than a result | Deep — expect to push back on scope |
| Cannot articulate what done looks like | **Do not emit.** Say so, and offer to help define it |
| Person is describing three projects | Split them, then run the smallest first |

---

## 3. Standing constants — the highest-value thing you produce

**This is the single largest category of avoidable human turn.** Not the whole of the
largest slice — much of that is genuinely novel input only a human can supply — but the
**re-asked** subset: the executor asking for something already written down.

Evidenced repeatedly in the corpus: an intake route asked twice in two documents an hour
apart; a nickname-to-owner mapping "supplied explicitly, per file, repeatedly"; a
trust-tier assignment asked per-run **despite already being written into that project's
CLAUDE.md.**

Elicit, and write into the constants skill:

- named people and channels, with **names, not roles**
- account structure and identifiers — never credentials
- **environment topology** (below)
- naming and label taxonomies, allowed values for categorical fields
- terminology the project uses differently from its common meaning
- do-not-say and do-not-do lists
- the project's fixed answers to anything an executor would otherwise ask twice

### Environment topology earns its own prompt

Ask directly: *"What surprises people about how this environment is put together?"*

Cross-account boundaries, split DNS, required auth profiles, propagation delays, and steps
that cannot be automated are all constants. In the corpus a DNS zone living in a different
account from its application cost 30–60 minutes **every time it was rediscovered** — because
it was rediscovered rather than recorded. **A surprise that recurs is a missing constant,
not bad luck.**

### Constants ship as a skill, not as CLAUDE.md prose

Write them to `.claude/skills/project-constants/SKILL.md`. CLAUDE.md carries the standing
rule and a pointer.

**Why:** verified on Claude Code 2.1.220 — the `Explore` and `Plan` subagents **do not
receive CLAUDE.md**, and no frontmatter field or setting changes that. They are also the
subagents an executor reaches for when orienting in an unfamiliar repo, which is exactly
when constants matter. A skill can be preloaded into any agent with
`skills: ["project-constants"]`, and the full content is injected, not just the description.

**Bound on this:** the `skills` field is **not** applied when a subagent definition runs as
an agent-team teammate. Teammates read CLAUDE.md normally — which is why the pointer stays
in CLAUDE.md rather than that section being deleted. The two paths cover each other.

**The standing rule for the executor:** if it is in the constants skill, use it and do not
ask. If a constant is missing, ask once and write the answer in.

---

## 4. Execution and verification authority

The clearest executor-side gap in the corpus: **verification absent or failed in 7 of 9
projects**, and the human repeatedly acting as the transport layer between the executor and
the target system — roughly 15 upload cycles on one app, called "the estate's dominant cost
sink" in that project's own retrospective.

Establish, and write into CLAUDE.md:

- **The executor owns the deploy–verify–fix loop end to end.** It does not hand over an
  artifact and then ask whether it worked.
- **Proof of work, not assertion.** Nothing is done without executed evidence. Grep, lint
  and self-review do not count where the failure mode can hide from them.
- **A success message is not evidence.** Four separate instances in this marketplace's own
  construction, every one found by testing rather than reading.
- **Verify at the level the failure lives, and scope the check to the live artifact.** A
  check scoped to a directory tree rather than the active version is equally blind.
- **The executor runs the check itself.** Before routing a verification step to a human,
  establish that it genuinely cannot be run by the executor.
- **Bulk triage is pre-filtered.** Reduce the set, then present the residue with a
  recommendation per item — never a raw list.

### Enforce at the tool layer where you can

A rule in prose can be reasoned around; a tool the agent does not have cannot be. Where a
recommended specialist's job is to check or verify, it carries
`disallowedTools: ["Write", "Edit", "NotebookEdit"]`. This is **verified as enforced, not
merely parsed.**

Apply it with judgment. An agent that must write does not get the restriction, and says
inline why — "copy, never destroy" is not a line the tool layer can draw.

---

## 5. Decision authority — the remaining slice

Establish:

- **Defaults** for unspecified choices (boring over novel, ship over polish, and so on —
  set per project)
- **Ceilings** — scope, dependency-addition tolerance, spend
- **The standing rule:** clear recommended action within ceilings → take it, log it in
  PROGRESS.md, continue. Do not ask.
- **The escalation stop-list**, which is derived from the corpus rather than invented:
  - **Irreversible actions**, specifically **state changes of a different authority class
    than the work in flight**. A "close" pulled out of an approved bulk-update run and
    handled manually — updates are correctable, closes are visible to other people.
  - **Classification and categorization fields.** Never adjusted to make a narrative fit.
  - **Anything beyond ceilings, touching credentials, or touching production.**
  - **Anything that changes project intent.**
  - Everything else is decide → log → continue.

---

## 6. Asset mapping

Map what the project needs against what is actually installed.

```bash
claude plugin marketplace list
claude plugin list
```

**Read every installed marketplace, not just `gfm-foundry`.** It is the source of truth for
execution specialists and scaffold templates; it is not the only marketplace on the machine.

**Qualify every name as `<plugin>@<marketplace>`.** Plugin names are not unique across
marketplaces, and `claude plugin details <bare-name>` will silently resolve to the wrong
one — observed with a plugin that existed in two installed marketplaces.

**Where an overlap decision is load-bearing — build it or don't — read the body.** A
plugin's own description is not a primary source for what it does. In this marketplace's
construction, reading two candidate bodies in full changed the finding: one solved a
different problem than its description implied, and surfaced a gap that the
description-level assessment had missed entirely.

**Do rough mapping only.** The executor does the authoritative pass at bootstrap, because
"present in a marketplace" is not "installed and working."

### Defer model and effort routing

**Do not build model/effort/subagent-routing logic into the handoff.** If
`workbench:model-effort-advisor` is available, recommend it — it scores a task and returns
model, reasoning effort, and inline-vs-subagent.

Make it a **soft** reference with a stated fallback. A cross-marketplace reference by
namespaced name is an undeclared runtime coupling that breaks silently if that marketplace
is disabled. Recommend, name the fallback, do not depend.

`pipeline-foundry` keeps only the **project-shape** recommendation: which work modes suit
this project and why.

---

## 7. Gap disposition and milestone slicing

### Every unknown gets one label, a named owner, and a date

- **Claude-executable** — a factual or technical lookup; becomes an executor task
- **Human homework** — judgment- or research-heavy; marked blocking-milestone-1 or not
- **Human decision** — taste, priorities, direction; asked now if blocking, else queued
- **Deferred** — parked, **with the condition that revives it**

**A role is not an owner.** And an owner alone is insufficient: one corpus item had a named
owner *and* a due date and lapsed silently, because nothing was watching. That is why §8
exists.

**Originating failure:** nine of nine projects carried unknowns that were named,
acknowledged, documented, and then routed around permanently. **An unknown that blocks gets
fixed; an unknown you can work around outlives the project.**

**Returned research is verified before it is acted on.** Treat "no evidence found" as "did
not look hard." Watch specifically for an open issue being read as an unmet need — one
research pass returned a claim that was stale in a way that reversed its own conclusion,
because a feature request whose ask had shipped was never closed.

### Milestone 1 must reach something demonstrable before any human input is needed

With written acceptance criteria.

**Inability to slice milestone 1 that way is diagnostic.** The project is vaguer or bigger
than admitted. Say so. Do not emit a handoff and hope.

Multi-session execution is expected and fine — slicing exists for resumability and
demonstrability, not because a session ending is failure.

---

## 8. Re-entry — how the project notices when the human stops

Set a cadence at intake. **Default: weekly.**

Implemented as a **cloud Routine** (`/schedule` in the CLI, or claude.ai/code/routines),
pointed at the project repo. On fire it reads PROGRESS.md, CONTINUATION.md and
OPEN-ITEMS.md, works the Ready queue, surfaces overdue items, and reports.

**Why a cloud Routine specifically:** it needs neither the machine on nor a session open.
The failure being detected is a person walking away, so any detector requiring their laptop
to be running assumes away the thing that broke. It also runs with **no permission
prompts**, which is what makes the continuation queue real rather than aspirational.

**Do not implement this as a session-scoped `/loop` or cron task.** Those expire seven days
after creation, and the silences this catches run 11–21 days. A detector that deletes
itself before the failure it detects is worse than none, because it looks handled.

**Weekly** is set from the detection requirement, not from evidence about optimal cadence —
there is none. Weekly fires ~3× inside a 21-day silence. Daily is noise for a legitimately
idle project and burns the run cap.

**CONTINUATION.md is pre-authorized work**, not a wish list. It executes unattended, so
nothing on the §5 stop-list belongs in it, and every item names a done condition something
in the transcript can demonstrate.

---

## 9. Green-check gate

**No handoff until all eight pass.** Any red → the output is the named blocker, not a
bigger brief.

1. Intent and verifiable success criteria defined
2. Constants block populated, including environment topology
3. Decision authority set — defaults, ceilings, escalation stop-list
4. Tools and specialists mapped against **all** installed marketplaces; creation needs identified
5. Every gap dispositioned, each with a named owner and a date
6. Milestone 1 sliced with acceptance criteria, reachable with no human input
7. Re-entry cadence and continuation queue defined
8. Blocking homework and decisions resolved, or explicitly accepted as milestone-blockers

**"Table this project" is a legitimate and expected output.** So is "this is three
projects." So is "come back when you can say what done looks like."

---

## 10. Emit the scaffold

Generate from `templates/` in `gfm-foundry`, filling every `{{PLACEHOLDER}}`:

| File | Role |
| --- | --- |
| `CLAUDE.md` | The persistent law — read every session |
| `HANDOFF.md` | The one-time briefing — read once |
| `PROGRESS.md` | Running log; the only record of delegated decisions |
| `CONTINUATION.md` | Pre-authorized queue for unattended runs |
| `OPEN-ITEMS.md` | Custodian ledger, checked on every re-entry |
| `.claude/skills/project-constants/SKILL.md` | The constants |
| `.gitignore` | From `templates/scaffold.gitignore` |

Plus basic file structure appropriate to the project type.

**Deliver as a zip.** Repo creation happens outside this session — no GitHub write access
here, and no credential handling.

### Author every rule with its originating failure inline

This is not a style preference. In the corpus, written rules bound the **executor**
reliably — one project honored 6 of 7 written defaults without exception, another's locked
decision blocks held across six session boundaries. They did **not** reliably bind the
human: a "do not rebuild from scratch" instruction was written at 12:48 and violated at
14:09 by its own author.

**The corrections that stuck shared one property: each was written after a concrete defect,
with the defect attached.** Where a rule is a structural fact rather than a correction, say
so rather than inventing a failure for it.

*External validation:* a skill written independently for one of these projects states every
one of its hard gates with the failure that produced it attached, in exactly this form.

---

## 11. Guardrails

- Does not execute the project.
- Does not invent missing context. Ask, or disposition it as a gap.
- Minimum necessary specialists. Prefer existing assets over new ones.
- Does not emit a handoff past a red check.
- Permitted and expected to recommend tabling.
- **Never handles raw credentials.** Assume CLI-native auth exists.
- Recommends only mechanisms the executor can actually invoke — no abstract patterns.

---

## 12. Work modes available to the executor

Recommend from this list, with the constraint attached. Defer model and effort choice to
`workbench:model-effort-advisor` (§6).

| Primitive | Use for | Constraint |
| --- | --- | --- |
| Main session inline | Sequential work, tight dependencies | Default |
| Subagents | Focused side tasks where only the result matters | Background by default (v2.1.198+). **`Explore` and `Plan` do not see CLAUDE.md** |
| Custom subagents | Repeated roles | Plugin agents namespaced `<plugin>:<agent>` |
| Skills | Packaged procedure | Preload with `skills:`; injects full content |
| Plan mode / `opusplan` | Design before execution | Strong model plans, cheap model executes |
| Worktrees | Independent parallel workstreams | Branches from the **default branch**, not parent HEAD |
| `/goal` | Keep working until a condition holds | Evaluator reads the transcript only; bound it with a turn clause |
| Monitors | React to a stream instead of polling | Interactive CLI only |
| Advisor tool | Executor stuck, would otherwise ask | Escalates to a **model**, not a human — not a stop-list substitute |
| Agent teams | Parallel exploration needing debate | Experimental, off by default, high token cost |
| Routines | Unattended scheduled work | Cloud; no local files; 1-hour minimum |
