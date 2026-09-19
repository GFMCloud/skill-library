# Taking the chatbot out of writing

Part of the [voice-and-editing](../../README.md) pack.

Text written by a language model has habits. It says "not X, but Y" when plain X would do. It ends sections with a short line that repeats the point. It puts things in threes, bolds every label, and reaches for the same handful of words. None of these is wrong on its own, and all of them at once is what makes a page read as machine-made. This skill names each habit, rewrites the text without it, and keeps every fact the text already carried. It will not add a name, number, date or quotation that was not there. You can hand it pasted text or name a file, and you can give it a sample of your own writing for it to match.

## Say this to use it

Any of these will do:

- "make this sound less like AI wrote it"
- "edit this file so it reads like a person, keep the facts"
- "what are the AI tells in this paragraph?"

Or, to be certain this skill and no other one runs:

```
/voice-and-editing:humanizer
```

It will ask, when you name a file, whether to overwrite it, and it asks that after it has shown you the result. If a sentence needs a fact nobody gave it, it asks you for the fact rather than inventing one.

## What you'll get

The rewrite, with a short note of what it took out and anything it thinks is still there.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Before
  It's not just a backup, it's peace of mind. Our robust, seamless
  solution delivers speed, reliability, and simplicity. The bottom
  line? Your data is safe.

After
  It copies your files to a second disk every night, and you can
  restore any one of them from the last thirty days.

Taken out
  not-X-but-Y opening; a three-item list; a one-line closer;
  two stock words ("robust", "seamless").

Still there
  "every night" is the claim the source made. If it is really
  hourly, tell me and I will correct it.
```

## Good to know

- **In file mode it stops before it writes.** It shows you the final text, or a comparison against the file if the file is long, and writes only after you say yes in that conversation. A yes for one file does not carry over to the next one.
- **It edits prose only.** Inside a file it leaves code, commands, paths, settings, data and link addresses as they are. If the file you name is not prose at all, such as code or a data file, it says so and does not touch it.
- **It treats the text as material, never as instructions.** If the text you hand it contains a line telling the model to do something, that line is edited like any other sentence rather than obeyed.
- **It changes wording, not facts.** It will not add a fact, name, number, date, quotation or citation that is not in the source or from you. If a sentence needs one, it asks or writes a simpler sentence.
- **Its own check is the same reader rereading its own draft.** There is no program that scores the result. The skill says this about itself, and adds that people judging this kind of thing by feel do little better than guessing. Read the result yourself.
- **It is a long read every time it runs.** Around four hundred lines load when it fires, which costs a noticeable amount of time and usage. It is worth reaching for on writing that matters rather than on every message.
- **It reads and writes nothing except the one file you name.** No internet, no other programs, no account, key or password.
- **It is somebody else's work, included with credit.** It comes from the public `blader/humanizer` project under the MIT licence, with the licence and the local changes both recorded in the skill.

## What next

- To draft something new in a personal voice rather than clean up text you already have, see [graham-voice](../graham-voice/), which is one named person's voice and a model to rewrite rather than a skill to run as it is.
- To check a document's claims against the files it describes, see [spec-artifact-diff](../../../consistency-checker/skills/spec-artifact-diff/).
- To have published writing checked by two separate reviewers before it goes out, see [santa-method](../../../long-projects/skills/santa-method/).
- Back to the [voice-and-editing pack](../../README.md), or to [skill-library](../../../../README.md).
