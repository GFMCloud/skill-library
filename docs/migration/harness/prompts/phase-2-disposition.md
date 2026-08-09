# Phase 2 — Gate A: present proposals, collect rulings in one batch

**Nature: the first of the two designed user interruptions.** Everything the user
must rule on is presented at once — never row-by-row.

## Present

From the `MIGRATION.md` produced in Phase 1, present one consolidated decision
package in chat:

1. **Summary counts** — how many skills, proposed split across
   `library:<plugin>` / `project` / `deprecate` / `archive`, and the plugin list
   the proposals imply.
2. **Rulings actually required** — the short list of rows where the call is
   genuinely the user's: drifted duplicates (which copy wins), skills whose purpose
   is unclear, anything with an `archive` proposal (content leaves active use), and
   any anomaly logged in Phase 1. For each: the proposal, the alternative, one line
   of reasoning.
3. **Everything else** — the remaining rows as a compact table, proposal shown,
   ratified by default unless the user objects ("the rest go where proposed —
   object to any of these?").

Use AskUserQuestion where the choices are enumerable; free-form review of the table
is fine too. **One batch. Wait for the rulings.**

## Record

- Write the user's rulings into the Ruling column of `MIGRATION.md` (including
  "as proposed" ratifications) and commit. Rulings that change a proposal get the
  user's stated reason logged in `STATE.md`'s decision log.
- Sanity-check the ratified table: every row ruled; every drifted row has a winner;
  no two `library:*` rows share a skill name; plugin groupings are sensible install
  units per `docs/end-state.md`.
- `STATE.md`: Phase 2 checked; decision log updated with the final plugin list;
  session log line added.

Then proceed directly to Phase 3 — no further confirmation.
