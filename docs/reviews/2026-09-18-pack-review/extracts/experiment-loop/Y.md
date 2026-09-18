### Items

| id | type | one line |
|---|---|---|
| item-5d659876 | skill | Instructs an agent on how to plan, branch, launch, monitor, and record a tree of experiment runs against a fixed baseline and run command. |

### For each item

**item-5d659876**
**Trigger:** Loads on-demand, per its frontmatter description: "Use before creating or changing experiments, launching a first run, deciding what to try next, handling a completed run, or reporting experiment progress." It is not always-on.

**What it makes the agent do:** Treat a project as a tree of experiment nodes descending from a root "baseline" that holds the run command; never edit a node once a run has "answered" it (frozen), and never change the run command/env across children. Before a first launch, resolve the train/eval command and ask only if unclear. If a run dies without producing a result, repair that same node in place rather than branching; a "repair cap" of "two runs in a row that answer nothing on one node" triggers asking the user, and the same failure recurring on a second node also triggers asking. Shape the tree as "stacked bushes": fan siblings for co-equal options of one decision, then descend a new round onto the previous round's confirmed winner rather than fanning everything off the root or chaining unrelated nodes. The core "auto-research loop" has seven steps: read the baseline code, form one round's co-equal hypotheses, create the round's nodes with a deliberately chosen parent, implement each change on its own git branch, launch the round's children, run a per-completion loop using `orx exp wait --project` as a "sleep-until-change signal, not the source of truth" (re-reading `orx runs` each wake to catch every newly-terminal run), and analyze each finish with one of four moves — Repair, Refill, Promote, Stop. It instructs stopping "when the goal is met, or after ~3 consecutive failed or regressed runs," writing up the tree as an artifact, and closing any turn that ran/changed experiments with a one-line-per-node summary of what was tested, status, and headline result. It also documents a `orx exp desc` notes field that is fully overwritten (not appended) on write.

**Enforcement:** Prose only. There is no script, hook, or exit-code check inside the file; compliance depends entirely on the agent following the written procedure. The named external CLI commands (`orx create-experiment`, `orx exp run`, `orx exp wait`, `orx runs`, `orx logs`, `orx exp desc`) are outside this file and not shown to fail closed or open here.

**Dependencies:** No runtime dependency is formally declared in the file. It assumes and references an external `orx` command-line tool and its subcommands, a private Git worktree of the project repository, and several sibling skills/documents it defers to by name (a "session playbook," and skills for git, evidence, compute backend selection, and report-writing) plus a "session playbook's Python policy." None of these referenced items are included in this file set.

**State it writes:** The file itself writes nothing locally. It describes state maintained by the external `orx` system: experiment nodes and their branches, run logs, a per-node free-form description field (`orx exp desc`, fully overwritten on each write), and a project-level write-up artifact produced at stop time.

**Fit with the bar:**
- *Plan then stop before consequential work* — partially supported: it requires asking the user only after a "repair cap" of two unproductive runs on one node, or when project setup is unclear before the first launch; otherwise the loop is designed to launch rounds, wait, and refill/promote autonomously without a stated checkpoint before each new launch.
- *Executed evidence before "done"* — supported: "actually read its results with `orx logs <runId>` ... Don't infer from status alone," and it requires that "the committed code emits enough run evidence to judge the node" before launching.
- *Say what was and was not checked* — partially supported: it mandates a turn-end summary of "what it tested, its status, and the headline result" for each relevant node, but does not itself instruct stating what was *not* checked.

**What it does not cover:** How to choose or configure a compute backend (defers to a separate compute skill), how to read/diff git branches (defers to a separate git skill), what counts as adequate run evidence (defers to a separate evidence skill), report naming/folder conventions (defers to a separate reports skill), and the Python/environment policy for the first launch (defers to a "session playbook").

### Agent-directed text
none

### Could not determine
The file references an `orx` CLI tool and its subcommands, a "session playbook," and separate skills/documents for git operations, run evidence, compute-backend selection, and report writing — none of these are present in this file set, so their actual contents and enforcement (if any) cannot be determined from what was provided.
