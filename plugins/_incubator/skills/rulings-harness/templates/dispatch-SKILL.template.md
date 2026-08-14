---
name: rulings
description: >-
  Record a new ruling (`/rulings new`) or check whether any existing ruling's
  falsifier has fired (`/rulings check`) for `<LOCATION-NAME>`. Use when a measured
  decision needs to be written down with evidence, or when it's time to verify the
  register is still current.
metadata:
  maturity: stable
  version: 1.0.0
  reviewed: <YYYY-MM-DD>
---

# Run the `<LOCATION-NAME>` rulings register

`rulings/INDEX.md` is the enumeration. `rulings/<slug>.md` files are the individual
decisions. Two modes, chosen by argument.

## `/rulings new`: record a decision

1. Ask what was decided and what was measured, if not already given.
2. Classify against the boundary: *it cost something to determine, and a future
   session would otherwise re-derive or violate it.*
   - No evidence could falsify it → this is a **preference**. Say so and stop; it
     belongs in CLAUDE.md, not here.
   - Measured, falsifiable, has a natural expiry → **ruling**.
   - Learned from a real incident, does not expire but needs the incident linked →
     **burn-derived**.
3. Write `rulings/<slug>.md` following the schema every sibling file in this
   directory already uses (frontmatter: `slug`, `category`, `revisit-by`, `status`;
   body: the ruling as one line, then Evidence, Falsifier, Re-test), filling all
   fields. A burn-derived ruling gets `Falsifier: none, burn-derived` and the
   incident cited in Evidence; every other ruling gets a real, checkable falsifier
   and a runnable re-test.
4. Add one row to `INDEX.md`.
5. If the source material was existing CLAUDE.md content, do **not** edit CLAUDE.md.
   Instead, write a short proposal (what line(s) would be removed and why) and hand
   it to the user to apply themselves.

## `/rulings check`: verify the register

1. Read `INDEX.md`. For every row with `status: active` and a real falsifier
   (skip burn-derived rows, whose falsifier is `none`):
   - Evaluate the **Falsifier** condition against the world: check an installed
     version, re-run the **Re-test** fixture, compare the result to what the ruling
     asserts.
   - If the falsifier has fired, or `revisit-by` has passed, mark the row
     `needs-redecision` in `INDEX.md`.
2. Report the list of rulings needing redecision, each with what fired and the fresh
   evidence gathered. Do not rewrite the ruling file itself: redeciding is a human
   call; this pass only detects and reports.
3. If nothing fired, report the clean count and stop.

## Guardrails

Only this skill's session edits `INDEX.md` and ruling files; do not delegate either
write to a subagent that could run concurrently with another writer. CLAUDE.md is
never edited by either mode: migration proposals are handed to the user, not
applied.
