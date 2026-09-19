# Getting the plan before the change

Part of the [turn-reduction](../../README.md) pack.

Some changes cannot be taken back. A setting that deletes old files. A permission opened wider than it should be. A rename in cloud settings that quietly destroys the thing it renames. This skill puts a stop before that kind of work. Claude Code reads your project first, then looks at the systems the change would actually touch, using commands that only look and never alter. Then it hands you four things: what it thinks you asked for, at most three questions it genuinely cannot answer for itself, a numbered list of the assumptions it is making, and the plan itself, naming the files it would change and the order it would work in. Then it stops and waits for you.

The point of the assumptions is that you can disagree with them. Each one is written to be specific enough to be wrong, which is cheaper to discover now than afterwards.

## Say this to use it

Any of these will do:

- "plan this first, don't write any code yet"
- "what's your approach before you touch it?"
- "this touches the database, give me a plan"

Or, to be certain this skill and no other one runs:

```
/turn-reduction:plan-gate
```

It asks you nothing before it starts investigating. It asks only after, and only for things a wrong answer would mean throwing work away, each with the answer it recommends so you can agree to all of them in one line. If it cannot reach a live system, it will not ask you for a key or a password. It writes down what it could not check as an assumption and hands the plan back anyway.

## What you'll get

A plan in four parts, with nothing on your computer or in your live systems changed.

EXAMPLE-PENDING-REAL-RUN

## Good to know

- **It writes nothing and changes nothing.** Producing a plan and stopping is the whole point of the skill. Implementation happens afterwards, once you approve it.
- **It reads your live systems, not only your project files.** For infrastructure work it runs look-only commands such as `terraform state list` and `terraform plan -refresh-only`, AWS `describe`, `get` and `list` calls, `kubectl get` and `describe`, and `docker compose ps`. This is further than the other three skills in the pack go: it reaches what is actually running, including production, in read-only form.
- **Those commands go over the internet.** Cloud and cluster commands talk to remote services. Nothing is sent anywhere else.
- **It uses the sign-ins already on your computer.** It is told never to ask you for a key or token, and to flag it as a design problem if the plan itself would need one written out in plain text.
- **It names the account or workspace it looked at.** A plan written against one environment should not be used on another, so the plan says which one it read.
- **It skips itself on small work.** A typo, a rename, a comment or a change of about twenty lines with one obvious correct form does not get the ceremony.
- **If an assumption turns out to be wrong later, it stops and tells you.** It is instructed not to quietly switch to a different design once you have approved a specific one.
- **What it needs first.** Nothing ships with it. To look at live systems it uses whichever of `terraform`, the AWS command-line tool, `kubectl` or `docker` you already use and are already signed in to. Without those it still plans from your project files and records what it could not check.
- **It is newer than the rest of the pack.** It is the only skill here marked `incubator`, which in this library means less proven than one marked `stable`, and the only one carrying no version or review date.

## What next

- Before the plan, [capability-preflight](../capability-preflight/) proves Claude Code can actually reach the systems the plan assumes.
- After approval, [proof-of-work](../../../foundry-core/skills/proof-of-work/) in the `foundry-core` pack is how the finished change gets checked rather than declared done.
- For a change with no real blast radius, [orch-pipeline](../../../long-projects/skills/orch-pipeline/) in the `long-projects` pack is the lighter routine.
- Back to the [turn-reduction pack](../../README.md), or to [skill-library](../../../../README.md).
