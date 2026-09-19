# Turning an idea into a brief someone else can run

Part of the [project-starters](../../README.md) pack.

Projects rarely fail on one bad decision. They fail on the steady cost of check-ins: the person running the work stopping every twenty minutes to ask for a fact, a scope call or a yes. This skill runs a conversation that pressure-tests what you are building, then writes down the things that would otherwise be asked twice: the fixed facts of the project, who is allowed to decide what, where the line is that nobody crosses, and what the first demonstrable milestone is. It packages the result as a set of documents a brand-new Claude Code session, with none of your conversation, can work from. It does not build the project.

## Say this to use it

Any of these will do:

- "turn this idea into a handoff a fresh session can run"
- "scope this project before I start it"
- "write me a project brief I can hand over"

Or, to be certain this skill and no other one runs:

```
/project-starters:pipeline-foundry
```

It will ask what is being built and what done looks like in terms you could check, what the constraints are, what surprises people about how the environment is put together, and what must never happen. It asks only what it needs to route the work, and a small clear project gets a short conversation.

## What you'll get

A readiness check, then either a zip of project documents or a named blocker.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Readiness check

  1. Intent and checkable success criteria        pass
  2. Fixed facts written down, including the
     unobvious parts of the environment           pass
  3. Decision authority: defaults, ceilings,
     the escalation stop-list                     pass
  4. Tools and specialists mapped                 pass
  5. Every unknown has an owner and a date        FAIL
  6. Milestone 1 reachable with no human input    pass
  7. Re-entry cadence and queue defined           pass
  8. Blocking homework resolved                   pass

Check 5 is red, so there is no handoff yet. Two unknowns have no
owner: which account holds the DNS zone, and who signs off the
data retention rule. Both are yours to answer. Tell me and I will
finish the scaffold.
```

## Good to know

- **It can tell you not to start.** Recommending that a project be shelved is one of its answers, as is "this is three projects" and "come back when you can say what done looks like". It will not hand over a brief while a readiness check is failing.
- **It recommends a scheduled job that runs with nobody watching.** The default is weekly. It reopens the project files in the cloud, works through a queue of tasks you approved in advance, and reports. It runs with no permission prompts, which is what makes the queue real. The skill also defines a list of things that must never go in that queue, including anything that cannot be undone, anything touching credentials or a live system, and anything that changes what the project is for. Read both parts before you set one up.
- **It needs a local copy of a separate project for its templates.** The templates live in `github.com/GFMCloud/gfm-foundry`. If that copy is not on your computer the skill stops and asks for it, rather than writing the files from memory.
- **It hands you a zip, and creates nothing online.** Making the repository is left to you, deliberately. It states that it never handles credentials.
- **It writes a small skill inside your project.** The project's fixed facts go to `.claude/skills/project-constants/SKILL.md` rather than into `CLAUDE.md` prose, because two of Claude Code's built-in helpers do not receive `CLAUDE.md` and are exactly the ones used when finding your way around an unfamiliar project.
- **It points you at a skill in another pack.** For choosing which model and effort level to use, it refers to [model-effort-advisor](../../../agent-tooling/skills/model-effort-advisor/), which is in the `agent-tooling` pack. Install that pack too if you want that advice.
- **It reads what is installed on your machine.** It runs `claude plugin marketplace list` and `claude plugin list` to see which packs are there, so it can point the brief at things that actually exist.
- **The conversation is the product, and it takes a while.** A novel or fuzzy project gets a deep session and possibly a second one. That length is the filter, not overhead.

## What next

- Ready to create the folder and the git setup? [new-project](../new-project/) does that part.
- Want to work backwards from the outcome before scoping? [systems-design](../systems-design/) comes first.
- For work that will span many sessions and end in something irreversible, [phased-harness](../../../long-projects/skills/phased-harness/) builds a project that pauses at gates.
- Back to the [project-starters pack](../../README.md), or to [skill-library](../../../../README.md).
