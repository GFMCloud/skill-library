# Find the work you keep repeating from scratch

Part of the [voice-and-editing](../../README.md) pack.

If you use Claude Code a lot, some jobs come back again and again, and each time you explain the same background and walk through the same sequence. This skill reads your recent Claude conversations, looks for those repeats, and gives you a ranked list of the ones worth writing down as a skill. It ranks by how often a job came back and how much re-explaining it cost you each time. It also checks each candidate against what you already have installed, so it does not suggest building something that exists.

## Say this to use it

Any of these will do:

- "what should I turn into a skill?"
- "what am I doing over and over?"
- "mine my recent sessions for workflows"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:skill-discovery
```

It will tell you it is about to read your recent sessions and that this takes a few minutes, and wait for you to say go. Nothing is read before you agree.

## What you'll get

A short list of candidates, strongest first, each with the phrases you would say to start it and the conversations it was found in.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```text
Scanned 47 sessions.  6 clusters found.  2 already covered by installed skills.

P1  Invoice PDF -> expense rows -> monthly summary
    Seen in 7 sessions.  You re-explained the category rules every time.
    You would say: "do the expenses for March", "turn these invoices into rows"
    Steps it would encode: read the PDFs, pull out date, supplier, amount,
      apply your category rules, flag anything unmatched, write the summary.
    Found in: "March invoices", "Q1 expenses tidy-up", and 5 more.
    Build this now, or add to the backlog?

P2  Draft reply to a customer complaint, then check the tone
    Seen in 4 sessions.  Medium re-setup cost.

Watch list (not enough evidence yet): 2 items.
Save the rest as a backlog file?
```

## Good to know

- **It reads whole past conversations of yours.** That is the material it works from, so anything you have discussed with Claude may pass through it. It goes to the Claude model and nowhere else.
- **It writes one file, and only if you say yes.** At the end it offers to save the lower-priority candidates as a backlog file. Decline and nothing is written. It deletes and moves nothing.
- **It starts up to five helper agents at once, then one more to group the results.** Those are extra Claude sessions, so a run costs real time and tokens on top of your own conversation.
- **No program ships with it.** It works through the session-reading tools your Claude app provides.
- **It stops if those tools are missing.** Rather than quietly returning nothing, it says the session-reading tools are not available here and offers to work from transcripts you paste in instead.
- **It needs no account, key or password of its own.**
- **It reads one file from the author's own setup if it is there.** A list of installed skills at `~/skill-library/docs/inventory.md` helps it avoid suggesting something that already exists. If you do not keep a skill library at that path, the file is absent and the run says so, and the candidates may overlap with skills it could not see.
- **The skill's own wording is written for its author.** Some of it speaks to one person by name and assumes his habits. The steps work for anyone, but expect to read past that.
- **It offers to run itself again later.** At the end it asks whether to re-run every thirty sessions. Setting that up is a separate step you would do yourself.

## What next

- To see what is installed and what each thing covers: [capability-index](../capability-index/).
- Once you have decided what to build, the review pipeline for material coming in from elsewhere is [source-intake](../source-intake/).
- To judge whether the skills you already have are earning their place: [toolkit-review](../toolkit-review/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
