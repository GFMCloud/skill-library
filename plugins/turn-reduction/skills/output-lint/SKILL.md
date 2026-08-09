---
name: "output-lint"
description: "Check a message or document before sending it, whenever it carries a command to run or an ask to act on — catches unsubstituted placeholders, commands that cannot run as written, writes announced before they are made, and counts with no enumeration behind them. Use before any hand-off, instruction, or status report."
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: 2026-08-09
---

# output-lint

The second-largest avoidable category in the audit was a human correcting the agent's
*process*, not its facts: 21 turns, 14.2%. Verbatim: *"this is dumb I'm not just going to
paste cmd line shit"*, *"give me a simplified overview, come on"*, *"a context dump you had
to convert into a decision yourself"*, *"I didn't put it in because you should know that"*.

Six of those defects are mechanically checkable. Two are not. This checks the six and
prints the two next to the result, rather than letting a clean run imply the message was
good.

## Run it

```bash
# from anywhere
python3 <this-skill-dir>/output_lint.py draft.md
printf '%s' "$MESSAGE" | python3 <this-skill-dir>/output_lint.py -
```

Absolute path when you need one: read `installPath` for `turn-reduction@gfm-foundry` out
of `~/.claude/plugins/installed_plugins.json`. Never construct it.

Exit `0` clean, `1` errors present, `2` input unreadable. `--strict` promotes warnings to
errors.

## The six that are checked

**placeholder** — `YOUR_…`, `{{…}}`, `<slot>`, the literal word PLACEHOLDER. A shipped
`YOUR_LEAGUE_ID` produced a `400` that tested nothing and cost a round trip to discover.
Inside a code fence or an inline command this is an error; in bare prose it is a warning,
because prose slots are usually deliberate. Known HTML tags are not flagged.

**interpreter** — the fence tag has to match what is in the block. Python was once
presented as a shell command; pasted, it fails at the first line. A block tagged `bash`
containing `import`, `def`, `print(`, or a colon-terminated block header is an error. A
block tagged `python` holding shell is a warning. An untagged block holding commands is a
warning.

**cwd** — a command whose meaning depends on where it runs (`./script`, bare `git`,
`npm`, `make`, `pytest`, and similar) must have its directory stated: a `cd` line inside
the block, or the directory named in the prose immediately above it. `git -C` and `git
clone` are exempt because they carry their own location.

**glob** — unquoted `**` in a shell block with no `shopt -s globstar` expands as a single
`*` and silently matches the wrong set. Quoted `"**/*.sql"` is fine: the tool expands it,
not the shell. Brace expansion in a block tagged `sh` is an error — it is not POSIX.

**announced-write** — *"I'll create the config and push it"*. Proof-of-work was violated
one message after being written down. Make the write, then report it with its result. The
check fires on first-person future and present-progressive write verbs.

**uncited-count** — any bare *"N files"*, *"N turns"*, *"N errors"* has to arrive with the
enumeration that produced it: the command in backticks, the list itself, or the word
counted or enumerated nearby. Recall said 128 turns; enumeration said 148. One session
self-reported "nine" and enumerated to 39. Markdown table rows are exempt — a table is its
own enumeration.

## The two that are not checked

The script prints both of these under `NOT CHECKED` on every run, pass or fail. They are
the weaker half and they are stated as rules, not claimed as checks.

**Lead with the ask.** If the reader has to act, the action is the first line — not the
conclusion that follows the analysis. The recorded correction was *"give me a simplified
overview, come on"* against a message whose ask was in the last paragraph.

**One decision per message where possible.** Three consecutive turns in one session were a
single decision: an over-broad ask, then *"which question is real?"*, then approval of what
should have been decided without asking. Splitting or narrowing the ask collapses that to
one turn — or, better, to none (`turn-reduction:standing-authorization`).

## Scope

It reads one input, checks six rules, and says so in the output. A clean result means
those six rules found nothing in that text. It is not a judgment that the message is good,
and it does not transfer to the next message — a check correctly scoped to one thing had
its conclusion inherited by six, and that inference is what this footer exists to block.

It is aimed at outgoing messages, hand-offs, and instructions. Running it over reference
documentation will produce noise: docs legitimately quote placeholders and counts.

## Pairs with

- `foundry-core:proof-of-work` — the standard `announced-write` enforces the tail of.
- `turn-reduction:standing-authorization` — removes the ask instead of improving it.
