# Rulings-harness doctrine: why each rule exists

Recovered from a design session (2026-08-12) that named `CLAUDE.md` itself as the
problem: it is "full of measured rulings" that were true when written and silently
rot afterward, indistinguishable from the preferences sitting next to them.

## The three decay modes this harness fixes

- **Version rot.** A ruling like "anydoc is 25–55x faster than markitdown" is true
  against specific installed versions on a specific date. Nothing re-checks that as
  the tools update, so the number quietly stops being true while the rule keeps
  firing.
- **Provenance collapse.** A rule surviving several rounds of CLAUDE.md editing loses
  the "why" first: what was measured, when, how. Once the method is gone, nobody can
  tell whether the rule still applies or whether it was ever really general.
- **Silent re-litigation.** Without a stated falsifier, every future session either
  blindly trusts an aging rule or re-derives it from scratch because there is no way
  to check whether it still holds. Both are waste; the second is worse, because it
  produces a second, possibly conflicting answer that nobody reconciles.

## Why the classification boundary is the load-bearing part

Not every line in a CLAUDE.md is a ruling, and treating them all the same is exactly
what leads to CLAUDE.md bloat in one direction (never demoting anything) or
under-provenance in the other (moving preferences out of the file that legitimately
owns them). The test (*it cost something to determine, and a future session would
otherwise re-derive or violate it*) is deliberately narrow. Applying it:

- "Don't auto-run `open <file>.html`" has no evidence that could overturn it; it is a
  standing choice about behavior, not a measurement. It stays a preference, in
  CLAUDE.md, forever.
- "anydoc is 25–55x faster; fall back to markitdown on error" was measured, with
  numbers, on a date, against specific tool versions. It is falsifiable (a version
  bump could close the gap) and it will eventually need re-checking. It is a ruling.
- "Two agents appending to one tracker only worked by luck" came from watching a real
  collision happen during the 2026-08-09 migration. It is not going to stop being true
  the way a benchmark number can drift, so it does not expire. But its authority comes
  entirely from the incident, and a rule with no incident attached is one a confident
  future session will talk itself out of the first time it looks inconvenient. It is
  burn-derived: no falsifier, but the incident must be linked in Evidence.

Getting this test wrong in either direction breaks the harness: promote preferences
into "rulings" and every register fills with unfalsifiable noise the check pass can
never resolve; leave real rulings in CLAUDE.md and the rot this harness exists to stop
keeps happening exactly as before.

## Why the per-ruling schema has exactly these five fields

- **The ruling, one imperative line.** If it cannot be stated as an instruction, it is
  not actionable yet. Write the instruction, not a description of a finding.
- **Evidence**: what, when, how. This is provenance. Losing this field is what
  "provenance collapse" means; a ruling without it degrades into an assertion nobody
  can check.
- **Revisit-by**: a date, not "eventually". Without a forced date, "someday" never
  arrives and the ruling ages silently exactly like the CLAUDE.md line it replaced.
- **Falsifier**: the one field a plain description never has. Stating the specific
  condition that would overturn a ruling ("markitdown ships RTF parsing", "a re-run
  shows the gap under 2x") is what makes `/rulings check` possible at all: without a
  falsifier, "check whether this still holds" has no test to run.
- **Re-test**: the fixture or command, not a description of one. A falsifier nobody
  can actually evaluate is theater. This field is what turns the check pass from
  "read and guess" into "run and know."

## Why migration is a proposal, never an in-place edit

The original design explicitly declined to migrate CLAUDE.md content as part of
building the harness: "a proposal for you to review rather than editing CLAUDE.md
directly." The reasoning generalizes past the one instance it was said about: a tool
that edits a user's standing instructions as a side effect of a different task (here,
scaffolding) is exactly the kind of unreviewed change the rest of this project's
guardrails exist to prevent. Build the harness; let migration be its own reviewed
step, every time it is run.

## Why `/rulings check` never edits a ruling file

Detecting that a falsifier fired is mechanical: check a version, run a fixture,
compare numbers. Deciding what the ruling becomes next is not: it might be replaced,
narrowed, or reaffirmed with fresh evidence. Collapsing detection and re-decision into
one automatic pass would silently overwrite a decision a human should make, which is
the same failure `phased-harness`'s Gate A exists to prevent for a different kind of
decision. The check pass hands back a list; a human, in a later step, writes the new
version.

## What this is not

- Not a general-purpose knowledge base. It holds decisions with a shelf life, not
  documentation, and not preferences no evidence could touch.
- Not a replacement for CLAUDE.md. Preferences stay there; only measured, falsifiable,
  or burn-derived findings move out.
- Not an auto-migrator. It never bulk-edits an existing CLAUDE.md; every migration is
  a reviewed proposal.
