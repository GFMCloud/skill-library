---
name: work-board
description: >-
  Stands up and runs a project's work board: a private claude.ai page with a decision
  inbox ("Needs you"), five fixed columns and a card database, generated from one
  template, plus the session protocol that keeps it current (read the inbox at pickup
  and close-out, act only on answers to the current question, continue to the next Ready
  card, higher-tier review before done). Use when starting a project ("set up a board",
  "work board init"), adopting an existing one ("adopt a board for this repo", "put this
  project on a board"), regenerating the page after a template change, or whenever a
  session in a project with `.claude/board.json` needs to ask Graham something or finish
  a card. Not for one-off folders that never go through a starter, and not a reconciler
  across boards. Costs one Artifact publish and a few ArtifactData writes at setup; its
  Stop hook reads the session transcript at every stop in a project that has a board.
metadata:
  maturity: incubator
---

# Work board

One board per project: the place open work and Graham's pending decisions live, so the
chat carries neither. A project holds only `.claude/board.json` and a generated page; the
page is generated from `templates/work-board.html`, never hand-edited.

## What a board is

A private claude.ai artifact with the `db` and `comments` capabilities; its cards are documents in one
collection (default `cards`). Columns are fixed so every board reads the same:

| id | label | meaning |
|---|---|---|
| `inbox` | Needs you | a question, sign-off or action only Graham can take |
| `ready` | Ready | decided and unblocked; a session may pull it |
| `doing` | In progress | a session or agent is on it, or it is scheduled |
| `review` | In review | built, waiting on the higher-tier reviewer |
| `done` | Done | reviewer green light plus evidence |

Lanes are per-project deadline or milestone groups ("This week", "Before launch"),
default one. Card fields, the write shapes and the three page rules are in
[references/cards.md](references/cards.md). Read it before the first card write.

The page opens on **Needs you** with a count badge of unanswered questions; the other tabs
are Board (columns by lane) and Done (collapsed). An inbox card shows the question, the
recommended default (labelled), one line of why and the evidence link, then Accept,
Amend (the default as editable text), Discuss and one comment box; one save writes
`answer {choice, text, at, ask_rev}`; an Amend whose text equals the default is refused.
A command card (`ask.command`) is marked "You run this", shows the command in a monospace
block with a Copy button and what to expect, and answers **I ran it** (`choice: "ran"`) or
Discuss.
The page refuses a move to Done without evidence and a green review. A **Tell Claude**
button in the header posts a comment on the board and sends it to Claude (the `comments`
capability's `sendToClaude`), pre-filled with the inbox cards Graham has answered. When no
Claude Code session is watching the board, claude.ai may answer the send with its own chat
Claude, which cannot reach this machine, rather than the page saying no session is watching
(seen 2026-09-28); his answers are on the cards either way, and a session's pickup reads
them. It is one self-contained file, light and dark, usable at phone width. Its one external call
is Google Fonts, for the mood board's type pairing; offline it falls back to system fonts.

## Stand one up: `init` (new project) or `adopt` (existing project)

Two parts, because Bash cannot publish an artifact. `<skill>` below is this skill's
directory; read `installPath` for `turn-reduction` out of
`~/.claude/plugins/installed_plugins.json` when you need it absolute.

1. **Render the page.** Lanes are `ID:NAME[:WHEN]`, repeatable.

   ```bash
   python3 <skill>/scripts/work_board.py render --name <project> \
     --lane now:"This week" --lane later:"Later" --out <project>/.claude/work-board.html
   ```

2. **Publish it** with the Artifact tool: `file_path` the rendered page,
   `capabilities: {"db": {}, "comments": {}}`, `icon: "board"`. Keep the URL it returns.
   The publish starts a watch on the board. Before relying on Tell Claude, confirm with
   ArtifactComments `watch` (no URL) that the board's row says "auto-replies armed".
3. **Write the config** from that URL. `init` for a project `new-project` just scaffolded;
   `adopt` for an existing project (it keeps an existing `authorization.json`, and takes
   `--trigger NAME=REGEX` for the project's own state-changing scripts).

   ```bash
   python3 <skill>/scripts/work_board.py init --project-dir <project> --url <artifact url> \
     --name <project> --lane now:"This week" --lane later:"Later"
   ```

   It writes `.claude/board.json` and a starter `authorization.json` (from
   `templates/authorization.json`: the G4 tiers and the push procedure, validated with
   `standing-authorization`'s `authz.py` before writing), re-renders the page, and refuses
   to overwrite either file. If it says the page differs, republish it to the same URL.
4. **Seed the cards** with ArtifactData (`batch`): a `ready` card per deliverable in
   scope (from SPEC.md, or the project's open-work list when adopting), an `inbox` card
   per open question, each with a recommended default.
5. **Link it**: the board URL goes in README.md and CLAUDE.md, and CLAUDE.md gets one
   line: "Asks go to the work board inbox, not chat."
6. Trim `authorization.json`'s granted list to what is true for the project. A project
   whose own spec or ADR requires Graham's review for merges removes the merge grant.

## The session protocol

In a project with `.claude/board.json`:

- **Pickup:** query the board (ArtifactData `query`, collection from board.json) for
  `inbox`, `doing` and `review`. Act on every inbox card whose `answer.ask_rev` equals
  `ask.ask_rev`: Accept means do the default, Amend means do the amended text, Discuss
  means raise it first thing, and I ran it (`ran`) means Graham ran the card's command:
  read the result back and close. Ignore an answer whose rev does not match.
- **Watch every board you write to**, at pickup and before your first write to it, so
  Graham's Tell Claude reaches this session and not a chat Claude: ArtifactComments `watch`
  with the board URL, then `watch` with no URL to confirm its row says "auto-replies armed".
  A session working across two projects watches both boards; publishing one board arms
  only that one. Arming needs comment auto-replies on for the session, and happens
  only when this session publishes the board or Graham pasted the board link in his own
  message; if the row is not armed, republish the same page to the board's URL (no
  re-render needed) or ask for the link. Only a main session holds a watch: a subagent,
  teammate or print session cannot receive a Tell Claude. A Tell Claude comment that wakes the session is
  read with ArtifactComments `read`, handled like a pickup, answered in its thread with
  what was done, and resolved.
- **Release the watch when you hand off.** With two sessions watching one board, a Tell
  Claude wakes only one of them, and not necessarily the one doing the work (2026-09-28:
  an Accept for the resuming session went to the session that wrote the handoff, which
  still held its watch). A session that writes a handoff, or hears that another session
  is taking over, stops its watch on every board before its final message: ArtifactComments
  `watch` with the board URL and `on: false`, then `watch` with no URL to confirm no board
  row is left. The session that picks up arms its own watch at pickup, as above.
- **Asks go to the inbox, not chat.** Anything that needs Graham becomes an inbox card
  with a recommended default, and the session keeps working on what it can. Check
  `authorization.json` first (`authz.py check`): an ask it already grants is not asked.
  Intent questions ("what is this for?") are exempt and still go in chat.
- **An Accept does not reach the auto-mode classifier.** The classifier reads chat and
  commands, never the board, so shape each accepted action so it can pass:
  - **Merges go through a pull request**: `gh pr create`, CI green, the reviewer's green
    verdict on the card, then `gh pr merge`. Never a local `git merge` into the default
    branch: the autoMode allow entry names pull-request merges on GFMCloud repos, and a local
    merge is refused (SCL, 2026-09-28).
  - **Graham-tier actions** (deletes, prod or cloud writes outside staging, billing) are a
    command card: the exact command in `ask.command`, built from a read-only lookup made
    first, and what it prints on success in `ask.expect` (shape in
    [references/cards.md](references/cards.md)). Never put the command in the question's
    prose. His `ran` answer means he ran it; the session then reads each result back and
    closes the card. Do not run these yourself after any answer (2026-09-28: an Accept on a
    command written into the question was read as permission, and the classifier blocked
    the session's run).
  - **Hook, settings and permission-text edits** are named on the card as a paste from the
    start, with the paste in the card's notes; do not attempt them.
- **Continue by default.** When a card is done, take the next Ready card in lane then
  due-date order. Skip cards with an unfinished `blocked_by` and anything on the run's
  "Not this time" list. Stop only when Ready is empty or everything left waits on Graham.
- **Higher-tier review before done.** Builder work goes to `review`; a reviewer of a
  higher tier (Fable 5.1 > Opus > Sonnet > Haiku; top-tier work gets a fresh same-tier
  session; nobody reviews their own work) checks it against `done_when` and writes the
  `review` record. Only then does the card move to `done`, with an `evidence` line.
  Three exemptions, each said in the review record: docs-only commits that deploy nothing;
  a decision card closed by recording Graham's answer, with nothing built; and an action
  Graham ran himself, closed on the session's read-back of the result
  ([references/cards.md](references/cards.md)).
- **Every state change is logged on the board** before the turn ends: commit, merge,
  push, deploy, cloud write. A change in another repo that has its own board is logged on
  that board; a repo without one logs on the project's. If no card is affected, end with a
  line `BOARD: no card affected: <reason>`.
- **Close-out:** re-read the inbox; the closing message says only "N new items in your
  inbox" plus the board link. If the turn would otherwise end on a should-I question with
  no inbox card, either write the card or add a line `INBOX: none needed: <reason>`.
- **Pushes** of the session's own commits follow `authorization.json`'s `push_procedure`:
  record each SHA you create, run
  `bash <skill>/scripts/push_check.sh --repo <repo> --branch <branch> --sha <sha>...`,
  and push as a separate command only after it prints `PUSH CHECK: PASS`. It checks the
  gh account is GFMCloud, origin is under `github.com/GFMCloud/`, gitleaks is clean, and
  the outgoing commits are exactly the recorded SHAs. It never pushes. On a branch's
  first push there is no `origin/<branch>`, so it measures from origin's default branch
  and prints the base it used; for a branch stacked on another, add `--base origin/<that
  branch>`. `--base` accepts only a ref under `refs/remotes/origin/`; a SHA, `HEAD~N` or a
  local branch stops, because it could hide a foreign commit from the range.

The Stop hook `turn-reduction/hooks/board_gate.py` enforces the logging rule and the
inbox rule. It blocks once per stop and lets the next stop through.

## Regenerate after a template change

```bash
python3 <skill>/scripts/work_board.py render --board <project>/.claude/board.json
python3 <skill>/scripts/work_board.py validate <project>/.claude/board.json
```

Then republish the page to the board's `url` with the Artifact tool (omit `capabilities`
so the grants carry forward). A board first published with `db` only has its Tell Claude
button hidden: republish it once with `capabilities: {"db": {}, "comments": {}}`. Cards live in the database and survive a republish.
`validate` fails when the page on disk differs from a fresh render: that is a hand edit or
a stale page, and the fix is always render plus republish. Lanes change in board.json,
then regenerate.

## Kill switches

- Rename `authorization.json` to `authorization.json.superseded`: the hook's chat-ask
  block turns off; the state-change block stays on.
- Rename `.claude/board.json` to `board.json.superseded`: both blocks turn off and the
  project returns to asking in chat.

## Known weaknesses

- The hook matches command text and phrases. A state change behind an alias or an
  unlisted script, or an ask phrased as "Thoughts?", is not caught; add project scripts to
  `triggers[]` in board.json.
- The page enforces its rules only for writes made through the page. A session writing
  with ArtifactData can still write `column: done` without a review; the rule in
  references/cards.md and the reviewer are the control there.
- Fixture mode (a local preview with no artifact runtime, or `#fixture` on the URL) shows
  labelled demo cards and keeps saves in the tab. It is for checking the page, never data.

## Inputs

The project directory, its name and lanes, and for adoption its list of open work. At
session time: `.claude/board.json` and `authorization.json` in the project.

## Verify

`work_board.py validate <project>/.claude/board.json` prints `VALID`; `authz.py validate
<project>/authorization.json` prints `VALID`; an ArtifactData `list` of the collection
returns the seeded cards. The hook is proven by `plugins/turn-reduction/tests/prove-board-gate.sh`
and the push check by `plugins/turn-reduction/tests/prove-push-check.sh`.

## Done when

The board URL is in README.md and CLAUDE.md, both validators pass, and the inbox holds a
card for every open question with a recommended default.

## Stop when

`init` or `adopt` refuses because a board or authorization file already exists: read what
is there, never overwrite it. The Artifact publish fails or returns no URL. `push_check.sh`
prints `STOP`: file an inbox card with its output instead of pushing. A question is
stop-listed in `authorization.json`: it goes to the inbox and the work on that card waits.
