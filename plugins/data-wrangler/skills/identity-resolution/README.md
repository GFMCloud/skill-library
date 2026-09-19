# Matching records that mean the same thing

Part of the [data-wrangler](../../README.md) pack.

Two files can describe the same customer and still not agree on the name. One says "Acme Corp.", one says "acme co", one says "ACME" and means a different company entirely. This skill decides which records refer to the same real thing. It works down a fixed order: an account number or email wins outright, then the same name once case and spacing are tidied up, then a table of known nicknames and old names, then a close-enough match you have agreed the rules for beforehand. Anything left over stays unmatched with a reason written next to it. It never fills in a plausible answer to make the result look complete. The list of decisions it makes is written out as a file, so the same cleanup does not have to be worked out again next month.

## Say this to use it

Any of these will do:

- "do these two customer lists refer to the same companies?"
- "match the names in this export against our account IDs"
- "these supplier names nearly line up, work out which are the same supplier"

Or, to be certain this skill and no other one runs:

```
/data-wrangler:identity-resolution
```

It will ask which field is the reliable identifier, if there is one. If names have to be compared by similarity, it will ask you to set two limits first: how close is close enough to accept, and how far apart is far enough to reject. If you do not set them, it stops and asks rather than choosing for you.

## What you'll get

A mapping table of every name and what it was matched to, a list of what did not match, and the counts.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Mapping table (suppliers-mapping.tsv)

alias             canonical     rule      score  added
"Acme Corp."      ACME_CORP     exact-id         2026-09-19
"acme co"         ACME_CORP     normalised       2026-09-19
"Acme Corporation" ACME_CORP    known-alias      2026-09-19
"Acme Holdings"   ACME_HOLD     fuzzy     0.91   2026-09-19
"ACME"            UNRESOLVED    -                2026-09-19

Unmatched (2 of 412)

"ACME"          ambiguous: matches ACME_CORP and ACME_HOLD equally
"Northwind (old)" no candidate above the reject limit of 0.70

Counts: 412 records in. 410 resolved into 137 groups. 2 unresolved.
Fuzzy matches were judged against accept 0.90, reject 0.70, as agreed.
```

## Good to know

- **It writes two files every time it runs.** The mapping table and the list of unmatched records, both new files in the folder you are working in.
- **It reads only what you hand it.** The record files you name, and any mapping table you already have for the same things. It does not go looking for other data on your computer.
- **It never deletes or moves anything.** Your original files are left exactly as they were.
- **It does not go online and does not sign in to anything.** No account, no key, no password, and nothing is sent anywhere.
- **No programs ship with it.** It is written instructions that Claude Code follows, so there is nothing to install and nothing extra needed to run it.
- **It will stop and ask before matching by similarity.** Without an agreed accept limit and reject limit, a close-enough match is a number somebody invented, so it asks for both first.
- **Anything it cannot decide stays undecided.** An unmatched record is reported with its reason, never replaced by the most likely answer.
- **It reports the leftovers as a list, not a percentage.** The few records that do not match are usually the renamed, merged or genuinely ambiguous ones, which is exactly where the interesting cases are.

## What next

- For a whole data job rather than the matching step alone, use the [data-pipeline-owner agent](../../agents/data-pipeline-owner.md) in this pack. It does the reading, cleaning and reshaping around this step and reports the counts at every stage.
- To have the counts and the leftovers actually checked rather than summarised, install the `foundry-core` pack and use [proof-of-work](../../../foundry-core/skills/proof-of-work/).
- Back to the [data-wrangler pack](../../README.md), or to [skill-library](../../../../README.md).
