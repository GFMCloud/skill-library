# Stage 3 prompt: comparison against incumbents

Fill in the angle-bracket fields and give this to one subagent. State the model
in the spawn. The subagent reads everything named here in full; it does not
skim.

---

# Task: compare an external source against the installed set

Two inputs, both on disk.

**A. Candidate:** `<PINNED-PATH>` (`<source type>`, pinned at `<commit or hash>`).
An independent clean-room review of it, written by a reviewer who had no
knowledge of the installed set, is at `<CLEANROOM-REVIEW-PATH>`. Read that
first and treat its judgments as a second opinion, not gospel: spot-check its
claims against the actual files, and say which you checked.

**B. Incumbents:** the installed skill library is inventoried at
`~/skill-library/docs/inventory.md`. The incumbents relevant to this candidate
are:

- `<path to incumbent SKILL.md>` (and its `references/`)
- `<...>`

Read ALL of these in full, including references.

## First: ancestry

Before classifying anything, check whether the incumbent and the candidate share
history: a merge note naming the other, byte-identical or near-identical files
(diff them), matching section structure, a CHANGELOG entry. If they do, say so
at the top and state the direction (which forked from which, and when). This
reframes every classification below from "is it better" to "what did the other
side learn since the fork".

## Classify every item in the candidate

For a skill collection, every skill; for a code repo, every idea the clean-room
review listed as worth taking; for an article, every technique. Exactly one of:

1. **REDUNDANT**: the incumbent already covers this as well or better. Name the
   incumbent and quote one pair of matching directives showing it is equal or
   superior.
2. **SUPERIOR SUBSTITUTE**: does what an incumbent does, measurably better.
   Quote the pair showing why. Say what would have to be edited before it
   could replace the incumbent (length cap, style rules, factual errors).
3. **COMPLEMENT**: covers ground no incumbent touches. State exactly what the
   gap is and whether anything on this machine would consume it.
4. **INGESTIBLE FRAGMENTS**: the item as a whole is redundant or weak, but
   specific sections are better than the incumbent's treatment. List each
   fragment: quote it, name the incumbent file and section it improves, and say
   what it replaces or adds.
5. **DISCARD**: adds nothing; one line.

## Then answer

- **Routing collisions**: if both were installed together, which descriptions
  or names would collide or misroute? Be concrete about which would win for
  typical prompts, and whether identical names have different bodies (the
  worst case, because nothing looks wrong).
- **Philosophy conflicts**: where do the two give CONTRADICTORY advice, not
  just different emphasis? Quote both sides.
- **Corrections needed at ingest**: factual errors, rules a stateless model
  cannot honor, style violations against the library's conventions.
- **Net assessment**: if only three things could be taken, which, and in what
  form (whole item vs fragment, and the target file for each).

Quote verbatim and cite file paths throughout. Write the full analysis as
markdown, save a copy to `<OUTPUT-PATH>`, and return it as your final message.
