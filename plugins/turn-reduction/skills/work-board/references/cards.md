# Card schema and writes

One document per card in the board's collection (default `cards`), written with the
ArtifactData tool against the board's `url` from `.claude/board.json`. The page reads the
same documents live.

## Fields

| field | type | meaning |
|---|---|---|
| `id` | string | the document id; short and stable (`c12`, `b7-merge`) |
| `title` | string | one line, what the card is |
| `column` | `inbox` `ready` `doing` `review` `done` | where it stands |
| `lane` | string | a lane id from board.json; unknown or missing lanes show in the last lane |
| `kind` | `build` `decision` `run` `merge` `milestone` | the chip on the card |
| `due` | `YYYY-MM-DD` | optional |
| `blocked_by` | list of card ids | a session skips a card while any of these is not done |
| `done_when` | string | a link to the DONE.md section this card is verified against |
| `notes` | string | free text |
| `links` | list of `{label, url}` | https only; the page ignores anything else |
| `evidence` | string | what was run or checked and what it showed; required for done |
| `review` | object | `{verdict, builder_model, reviewer_model, agent_id, at}`; written by the reviewer session, never the builder; a read-only reviewer that cannot write the board has the builder transcribe its verdict, naming the reviewer and "transcribed" in `agent_id`; for an exempt card (see Rules), by the session that verified it |
| `ask` | object | `{question, default, why, evidence_link, ask_rev}`, plus `command` and `expect` on a command card (below); only on inbox cards |
| `answer` | object | `{choice: accept or amend or discuss, text, at, ask_rev}`, or `choice: ran` on a command card; written by the page when Graham answers |
| `updated_at` | ISO time, UTC | every write sets it |
| `updated_by` | string | who wrote, and why in a few words (`session 2026-09-28: merged e5c0766`) |

`why` inside `ask` is an addition to PROPOSAL section 2's field list: section 3 puts "one
line of why" on the inbox card, and it needs a field to live in.

**Command cards.** When the ask is for Graham to run a command, the command goes in
`ask.command` and never inside `question` prose. `question` says what the command does and
why it is his to run; `expect` says what he should see and in which window. The page marks
the card "You run this", shows the command in a monospace block with a Copy button (on the
Needs you list and in the card), and offers only **I ran it** (`choice: "ran"`, with any
output he pasted in `text`) and Discuss. The command follows the global rule for handed-over
commands: one self-contained paste from any directory, printing its own result.

## Rules

- **Done needs evidence and a green review.** `review.verdict` is green when it is `green`,
  `pass`, `passed` or `approved` (any case); write `green`. The page refuses the move; a session must not write
  `column: done` without both either. Three kinds of card are exempt from the reviewer and
  say so in `evidence`; the session that verified the result writes the record:
  - docs-only commits that deploy nothing (PROPOSAL V8): `reviewer_model: "exempt: docs-only"`;
  - a decision card closed by recording Graham's answer, nothing built:
    `reviewer_model: "exempt: decision recorded"`;
  - an action Graham ran himself (a delete, a console or billing change), closed on the
    session's read-back of every result: `reviewer_model: "exempt: Graham-run, read back"`.
  Anything a session built, merged or deployed is not exempt. A card that mixes an exempt
  item with anything the session built goes to review. The Graham-run exemption covers the
  command Graham ran and its read-back; a script, template, scheduled task or config the
  session wrote is built work and is reviewed (before Graham runs it, where he runs it).
- **Editing an ask bumps `ask_rev` and clears `answer`.** Write both in one update:
  `{"ask": {..., "ask_rev": <old + 1>}, "answer": null}`.
- **Act on an answer only when `answer.ask_rev == ask.ask_rev`.** A mismatch means Graham
  answered an older question; leave the card in the inbox.

## Writes that come up every session

Open an inbox card (a question for Graham):

```json
{"action": "set", "url": "<board url>", "collection": "cards", "doc_id": "c14",
 "data": {"title": "Pick the backup target", "column": "inbox", "lane": "now", "kind": "decision",
          "ask": {"question": "Back up to S3 Glacier or B2?", "default": "S3 Glacier Deep Archive",
                  "why": "Same account as the rest; cheapest at our size.",
                  "evidence_link": "https://github.com/GFMCloud/x/blob/main/docs/backup.md", "ask_rev": 1},
          "answer": null, "updated_at": "2026-09-28T14:00:00Z", "updated_by": "session: backup design"}}
```

Act on an Accept or Amend (revs match): do the work, then move the card on:

```json
{"action": "update", "url": "<board url>", "collection": "cards", "doc_id": "c14",
 "data": {"column": "ready", "notes": "Graham amended: B2. Acting on ask_rev 1.",
          "updated_at": "...", "updated_by": "session: acted on answer"}}
```

A Discuss answer stays in the inbox; raise it at the top of the next message to Graham.

Open a command card (Graham runs it; the session never runs it after his answer):

```json
{"action": "set", "url": "<board url>", "collection": "cards", "doc_id": "q-rm-wt",
 "data": {"title": "Remove the merged worktree", "column": "inbox", "lane": "now", "kind": "run",
          "ask": {"question": "Remove the merged worktree (a deletion, so yours to run)",
                  "command": "git -C /Users/gfm/repo worktree remove /Users/gfm/repo/wt && echo \"worktree removed\"",
                  "expect": "The line: worktree removed, in any terminal window.",
                  "why": "Clean, merged into main and even with origin; the branch stays.",
                  "evidence_link": "", "ask_rev": 1},
          "answer": null, "updated_at": "...", "updated_by": "session: worktree cleanup"}}
```

Act on a `ran` answer (revs match): read every result back, then close the card with the
Graham-run exemption (`reviewer_model: "exempt: Graham-run, read back"`). If the read-back
does not show the expected result, say so on the card and leave it open.

Record a review (the reviewer session writes this, then the builder may move to done):

```json
{"action": "update", "url": "<board url>", "collection": "cards", "doc_id": "c9",
 "data": {"review": {"verdict": "green", "builder_model": "Opus", "reviewer_model": "Fable 5.1",
                     "agent_id": "a1b2c3", "at": "2026-09-28T15:10:00Z"}}}
```

Several cards at once: `"action": "batch"` with `writes: [{op, collection, doc_id, data}]`.
The Stop hook recognizes an inbox write by `"column": "inbox"` or an `ask` object anywhere
in the call.
