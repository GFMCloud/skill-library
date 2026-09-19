# Getting second opinions on a decision

Part of the [long-projects](../../README.md) pack.

By the time a hard decision comes up, the conversation has usually talked itself into an answer. Everything said so far pulls the next thing said in the same direction, and asking the same conversation to argue against itself does not undo that. This skill makes Claude Code write down its own position first, then asks three separate helpers the same question. Each one starts fresh, sees only the question and the few facts it needs, and takes a different angle: one challenges whether the question is even the right one, one cares about what actually happens day to day, one looks for how the plan fails. You see all four answers, and the strongest disagreement is printed whether or not it won.

## Say this to use it

Any of these will do:

- "give me second opinions on this, I think I'm anchored"
- "argue the other side of this decision"
- "should we ship this now or hold it, get some dissent first"

Or, to be certain this skill and no other one runs:

```
/long-projects:council
```

It will ask one clarifying question if the decision cannot be stated as a single question. Otherwise it asks nothing and starts.

## What you'll get

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
## Council: ship the rewrite Friday, or hold two weeks

**Architect:** Hold. The old import path is still live and nothing tests it.
**Skeptic:** Wrong question. Nobody has asked whether the rewrite is needed at all.
**Pragmatist:** Ship Friday behind a switch. Two weeks of waiting teaches you nothing.
**Critic:** Ship and the failure is silent: bad rows land and look fine until month end.

### Verdict
- **Consensus:** the untested import path is the real risk, not the date.
- **Strongest dissent:** the Pragmatist's, that holding buys no information.
- **Premise check:** the Skeptic challenged the question; the rewrite's value was assumed.
- **Recommendation:** test the import path first, then ship behind a switch.
  This moved from the opening position, which was to hold outright.
```

## Good to know

- **It costs three extra Claude helpers each time you run it.** That is tokens and some waiting. There is one round by default, and a second round is your choice.
- **It changes nothing on your computer.** No file is written, nothing is run, nothing goes online. If the decision belongs in a record your project already keeps, it tells you to put it there rather than starting a notes file of its own.
- **The helpers see only what you give them.** They never see the conversation, which is the whole point, so a decision that depends on context you have not stated will get thin answers.
- **The opening position is written before the helpers reply.** That is deliberate, so the final recommendation cannot quietly become a summary of the other three, and so you can see whether it moved.
- **A helper that does not come back is reported, not invented.** If one fails to return, you get the ones that did and a note saying which is missing.
- **It will not convene over a fact.** If the answer can be looked up, it answers instead.
- **It was adapted from someone else's project.** The original is an MIT-licensed skill from the ECC project, and the skill says so in its own text.

## What next

- Checking whether finished work is right, rather than deciding what to do? That is [santa-method](../santa-method/).
- Want the decision written down so it can be re-checked later instead of just trusted? [rulings-harness](../rulings-harness/) does that.
- Deciding on a risky change before making it? [plan-gate](../../../turn-reduction/skills/plan-gate/) is the pause before the work, not the argument about the direction.
- Back to the [long-projects pack](../../README.md), or to [skill-library](../../../../README.md).
