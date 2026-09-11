---
name: "identity-resolution"
description: "Match records that refer to the same real-world entity across sources with different names, spellings, and identifiers. Use when joining data whose keys do not line up exactly, and before assuming two similarly-named things are the same thing."
metadata:
  maturity: stable
  version: 1.0.1
  reviewed: 2026-09-11
---

# identity-resolution

Deciding whether two records are the same entity. The part of data wrangling
that cannot be done by a join, and the part that gets reimplemented every time
because the rules live in code instead of in an artifact.

## Inputs

Two or more record sources to be matched; the canonical identifier where one exists;
the accept and reject thresholds for fuzzy matching, agreed before any match is
applied; any existing mapping table for the same entities.

## Verify

Counts reconcile: records in equals resolved plus unresolved, and every cluster is
listed. The whole procedure re-run from the original source produces the same output.
Every fuzzy match carries its score and the threshold it was judged against.

## Done when

The mapping table is emitted as a keyed, commented data artifact; the reject ledger
lists every unresolved record with its reason; the scale the resolution was validated
at is stated.

## Stop when

No canonical identifier exists and no threshold has been agreed: ask for the threshold
before applying any fuzzy match. A cluster above two members cannot be inspected. The
counts do not reconcile after a re-run; a resolution that is not reproducible is not
handed over.

## Order of operations

Work down this list and stop at the first rule that resolves. Later rules are
weaker and must never override an earlier one.

**1. Exact match on a canonical identifier.** Account ID, primary key, email.
If one exists, it wins outright. Everything below is a fallback for records
that do not have one.

**2. Exact match after normalisation.** Case-fold, trim, collapse internal
whitespace, strip known punctuation and honorifics, normalise unicode. Record
every normalisation applied — this list *is* part of the ruleset and the next
project needs it. Case alone is a logged failure here: a table-name casing
mismatch shipped in this corpus.

**3. Explicit mapping table.** Nicknames, abbreviations, legal-vs-trading
names, historical names. This table is an **artifact**, not a code block, and
it is the single most valuable output of the whole procedure.

**4. Fuzzy match — proposed, never applied silently.** Produce candidates with
scores, apply a threshold agreed in advance, and route everything between the
accept and reject thresholds to review rather than resolving it. A fuzzy match
applied without a recorded threshold is an invented value.

**5. Unresolved.** A null with a recorded reason. **Never a guess.** The
strongest rule in this corpus is *never invent a value* — asserted five times
in a single project. An entity that cannot be resolved stays unresolved and
appears in the reject ledger.

## The mapping table is the deliverable

Four projects independently rebuilt this work. What each of them failed to
leave behind was the table — the accumulated knowledge of which strings mean
the same thing. Emit it as data, keyed and commented:

```
alias            canonical        rule    added
"acme co"        ACME_CORP        manual  2026-07-27
"Acme Corp."     ACME_CORP        norm-2
"ACME"           UNRESOLVED       —       ambiguous: 2 candidates
```

Where an entry encodes a standing project fact rather than a one-off cleanup,
promote it into the project's standing constants block (spec §4a). The corpus
records the same nickname→owner mapping being supplied by hand, per file,
repeatedly — a table that existed in someone's head and nowhere durable.

## Two traps

**Transitive collapse.** A matches B, B matches C, therefore A matches C — and
now three distinct entities are one. Fuzzy matching is not transitive. Cluster
explicitly and inspect any cluster above two members before accepting it.

**The tail is where the entities are.** Resolution rates look excellent
because most records are easy. The 5% that do not resolve are usually not
noise — they are the acquisitions, the renames, the joint accounts, the
genuinely ambiguous. Report the tail as a list, not as a percentage.

## Before you finish

- Reconcile counts: records in, resolved, unresolved, and clusters formed. They
  must add up.
- Re-run the whole procedure from the original source and confirm the same
  output. A resolution that is not reproducible is not a resolution.
- State the scale it was validated at. *"The 16-file assumptions broke at 130
  files"* is a logged failure of exactly this omission.
