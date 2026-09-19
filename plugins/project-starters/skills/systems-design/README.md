# Working backwards from the outcome

Part of the [project-starters](../../README.md) pack.

Plans usually get written forwards, from what you would do first. That hides the assumptions, because nothing forces you to say what has to be true for the end result to exist. This skill runs a guided conversation of 20 to 30 minutes that goes the other way. It makes you define success in terms someone could measure, works backwards asking what must be true immediately before each stage, then holds a premortem: it is six months later, this failed, what happened. The output is a plan whose steps have evidence attached, a ranked list of ways it could fail, and blocks of work small enough to do one at a time.

## Say this to use it

Any of these will do:

- "help me work backwards from this goal"
- "validate this idea before I commit to it"
- "help me think through how this would actually work"

Or, to be certain this skill and no other one runs:

```
/project-starters:systems-design
```

It confirms before it starts, because the conversation is long. Then it asks what success looks like in observable terms, what evidence would prove you got there, what the timeline is, and which constraints cannot move. It pushes back on vague answers: "successful launch" gets sent back, "500 paid users at under $3 each" does not.

## What you'll get

A summary document and a diagram of the system, after the conversation.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
End state
  500 paid users, 40% weekly active, under $3 to acquire one, by 30 June.
  Evidence: the billing export and the analytics dashboard, both dated.

Working backwards, what must be true
  <- 500 paid    people convert from trial at 8% or better
  <- 8% convert  the first-run experience answers "what is this for" in 30s
  <- that exists you know the top three reasons trials stall

Ranked failure modes
  1. Spend on acquisition before the retention number is real.
     Early warning: cost per user falls while week-4 retention drifts.
  2. The 8% figure is borrowed from a different market.
     Cheap test: 20 manual trial calls before building anything.

Sprint-ready blocks
  A. Trial-stall interviews        no dependencies, start now
  B. First-run rebuild            needs A
  C. Paid acquisition             needs B and the retention number
```

## Good to know

- **It was written for the Claude website, not for Claude Code.** Three things it names are website features: the folder `/mnt/user-data/outputs/` it saves the summary to, the `present_files` tool it shows the document with, and `ask_user_input_v0`, the question tool it uses for multiple-choice and ranking questions. None of them exist when you run Claude Code on your own computer. The conversation works here as written. For the last step, tell it to save the document into the project folder you are working in, and expect the questions as plain text rather than as a list you tick.
- **It draws the diagram through another pack.** The diagram step calls the `visualize` pack's drawing tool. Without that pack installed you get the document and no picture.
- **It reads no files.** Everything it works from is what you say in the conversation. It uses no account and goes online for nothing of its own. A diagram may load drawing libraries from the internet when you open it, depending on what the drawing tool produces.
- **It writes one document and changes nothing else.** It deletes and moves nothing, and runs no commands.
- **It will tell you an idea is not ready.** If you cannot say what success looks like in measurable terms, it says the definition is too loose and stops there rather than producing a plan on top of it.
- **The premortem is the part people skip and the part that pays.** It asks for specific failures, not "ran out of money", and it asks which failures you cannot mitigate at all, up to and including whether to stop now.
- **It switches between two modes and says which one it is in.** One gathers and builds with you. The other challenges what you said, directly and without softening. The second is the point of the exercise.
- **Two files in its folder are test material.** `manual-test-walkthrough.md` and `test-prompts.json` describe how the skill is checked. They are not part of what it does.

## What next

- Have a plan and want it packaged so a fresh session can execute it? [pipeline-foundry](../pipeline-foundry/) does that next.
- Ready to create the folder and the git setup? [new-project](../new-project/).
- Want a second opinion on a decision the plan turns on? [council](../../../long-projects/skills/council/) argues the other side.
- Back to the [project-starters pack](../../README.md), or to [skill-library](../../../../README.md).
