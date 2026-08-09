---
name: project-kb-builder
description: "Turns a large source document (PDF, DOCX, PPTX, or similar reference material) into a structured set of markdown knowledge base files ready to upload to a Claude Project. Use when the user wants to break down a big doc into usable KB files, create knowledge files for a Claude Project, or build a reference system from source material. Triggers on phrases like \"turn this into a KB,\" \"break this down for a project,\" \"make this into knowledge files,\" \"extract this into markdown for a project,\" or when a user uploads a large reference doc and asks how to feed it to Claude as a project knowledge base."
metadata:
  maturity: incubator
---

# Project KB Builder

Turn a large source doc into a structured set of markdown knowledge files for a Claude Project.

## When to use this skill

Use when the user wants to:
- Convert a large reference doc (PDF, DOCX, PPTX) into knowledge files for a Claude Project
- Build a structured KB that Claude can retrieve from accurately
- Break down dense source material into topic-scoped, retrievable chunks
- Create a project where Claude acts as an SME on the source content

Do NOT use this skill for:
- Single short documents that fit in one file (just extract directly)
- Documents that are pure narrative with no discrete topics (a memoir, a single article)
- Tasks where the user just wants a summary, not a retrievable KB

## The 7-step process

Follow these steps in order. Confirm structure ONCE with the user (Step 4), then build through to completion without further check-ins unless a true blocker appears.

### Step 1: Split persona from content

Before any extraction, decide what goes where:

- **Project Instructions (system prompt):** persona, behavior, voice, role-specific context about the user (e.g., "the user is a Services Partner, not an ISV"), how Claude should respond, what to prioritize.
- **Knowledge files:** retrievable factual content from the source - programs, policies, procedures, definitions.

Persona/behavior content does NOT go in knowledge files. It loads every chat via Project Instructions and shouldn't compete with retrieval.

If the user hasn't thought about the system prompt yet, flag it: "Want me to draft a Project Instructions block alongside the KB files, or are you handling that separately?"

### Step 2: Read the source and inventory content domains

Read the full source doc. Identify:

- Natural topic boundaries (programs, sections, modules, chapters)
- Cross-cutting content that applies to everything (policies, definitions, key dates, glossary terms)
- Index/router content (table of contents, decision trees, "which program for which scenario")
- Discontinued or deprecated content (note it, don't give it its own file)
- Source bugs (duplicates, contradictions, broken references) - flag these, don't paper over them

Output of this step is an internal inventory, not a deliverable yet.

### Step 3: Propose file structure using the tier-prefix convention

Default structure (the "opinionated" pattern):

```
00-{topic}-index.md           Router / index / decision tree
01-{topic}-policies.md        Cross-cutting policies, compliance, key dates
10-{first-program}.md         Individual topic 1
11-{second-program}.md        Individual topic 2
...
19-{nth-program}.md           Individual topic N (up to 9 programs at this tier)
20-{appendix-1}.md            Special-case rules, edge cases, vertical-specific content
21-{glossary}.md              Glossary / definitions
```

Why tier prefixes: filename ordering signals retrieval priority to Claude when multiple files match a query. Lower numbers = higher priority / more general. The index file (00) is the entry point; cross-cutting policies (01) apply broadly; individual topics (10-19) are scoped; appendix content (20+) is reference.

If the source doesn't fit this exactly, adapt:
- More than 9 individual topics: use 10-19 for primary, 20-29 for secondary topics, push appendix to 30+
- No cross-cutting policies: skip the 01 file
- No appendix content: skip the 20+ files
- Single-domain doc with no sub-topics: this skill is overkill, just extract to one file

### Step 4: Confirm structure with the user (one checkpoint)

Before extracting, present the proposed file list and get a yes/no. Format:

```
Proposed structure:

00-{name}-index.md
01-{name}-policies.md
10-{topic-1}.md
11-{topic-2}.md
...

Confirm and I'll extract, or flag changes.
```

This is the ONLY mandatory checkpoint. Do not ask for interpretation confirmations during extraction. If something is genuinely ambiguous (not just "I'd like to double-check"), surface it as a blocker. Otherwise make the call and move.

### Step 5: Extract using the standard per-file template

Each individual topic file (10-19 tier) uses this template:

```markdown
# {Topic Name}

## TL;DR

2-4 sentences. What it is, who it's for, the headline rule.

## Eligibility / Scope

Who qualifies, what qualifies, what doesn't.

## Mechanics

How it works - funding amounts, percentages, caps, timelines, key parameters.

## Required Inputs

Documents, approvals, prerequisites needed to use this.

## Process

Step-by-step submission, approval, or execution flow.

## Key Dates

Deadlines, cutoffs, fiscal year boundaries, expiration windows.

## External Resources

Links, portals, contact paths, official references.

## Common Issues

Pitfalls, edge cases, things that get rejected, audit risks.
```

Adapt section names if the source content demands it (e.g., "Funding Mechanics" instead of "Mechanics" for funding programs, "Compliance Notes" instead of "Common Issues" for policy files). Keep the template consistent across all program-tier files in the same KB.

The 00-index, 01-policies, and 20+ appendix files use their own structure - they're not constrained to the per-topic template.

### Step 6: Flag source bugs and contradictions explicitly

If the source has:
- Duplicate sections (e.g., Section 1.10 and 1.11 are identical)
- Contradictory rules across sections
- Broken cross-references ("see Section X" where X doesn't exist)
- Discontinued items still listed as active

Call them out in the relevant file with a clear note. Example:

```markdown
> Note: The source PDF lists Section 1.11 as a duplicate of Section 1.10 (likely a doc bug). Treating Section 1.10 as authoritative.
```

Do not silently smooth these over. The user needs to know the source is imperfect.

### Step 7: Output to a downloadable folder and present

Write all files to `/mnt/user-data/outputs/{kb-name}/`. Use a kebab-case folder name based on the source content (e.g., `aws-funding-kb`, `vendor-onboarding-kb`).

Use the `present_files` tool to show all files at once. Lead with the index file (00) since it's the entry point.

After presenting, give the user a short next-steps block:

```
Next steps:
- Upload these files to your Claude Project's knowledge
- Add the Project Instructions block (if drafted) to the project's instructions field
- Test with a real query and iterate per-file based on gaps
```

## Anti-patterns - don't do these

- **Per-file "Internal Notes [Placeholder]" sections.** If the user has personal/role-specific context, it goes in Project Instructions, not in every knowledge file. Placeholders bloat the KB and rarely get filled in.
- **Splitting tightly cross-referenced content.** If two sections constantly reference each other, they belong in the same file. Splitting creates retrieval gaps.
- **Giving discontinued items their own file.** Fold them into the index with a clear "discontinued as of X" note. Don't create forward-looking files for deprecated content.
- **Verbatim extraction.** This is a reference-doc rewrite, not a copy. Distill, tighten, restructure for retrieval. Keep dollar amounts, dates, percentages, and rule-language exact - rewrite the surrounding prose.
- **Asking for interpretation confirmation.** "Should I include this section?" / "Is this the right framing?" - no. Make the call. Surface only true blockers (e.g., "the source contradicts itself on the cap amount, which version applies?").
- **Skipping the system prompt question.** Always ask about Project Instructions in Step 1, even if just to confirm the user is handling it separately.

## Escape hatches - when to deviate

- **Source is short (< 30 pages):** This skill is overkill. Suggest a single markdown file or a 2-3 file split.
- **Source is pure narrative:** No discrete topics to extract. Suggest a different approach - summary, outline, or chapter-by-chapter notes.
- **Source has > 15 distinct topics:** Use multi-tier expansion (10-19 primary, 20-29 secondary) or suggest splitting into multiple Projects.
- **Source has no cross-cutting policies:** Skip the 01 file.
- **User wants a different file naming convention:** Honor it, but explain that tier-prefixing is what signals retrieval priority. If they override, drop the prefixes consistently.

## Reference example

The skill's reference build is the AWS Partner Funding KB:

```
00-funding-programs-index.md          Router across all programs, includes discontinued (CEI)
01-policies-compliance-and-key-dates.md   Cross-cutting rules (pre-approval, no stacking, cutoffs)
10-training-and-certification.md
11-apn-fee-credits.md
12-innovation-sandbox.md
13-marketing-development-funds.md
14-proof-of-concept.md
16-migration-acceleration-program.md  (skipped 15 - left room for adjacent program)
17-isv-workload-migration-program.md
18-marketplace-private-offer-promotion.md
20-public-sector-considerations.md    Vertical-specific overrides
21-glossary.md
```

Source was a 110-page PDF. Output was ~2,900 lines of markdown across 12 files. System prompt lived separately in Project Instructions.

## Interaction style

- One structure checkpoint (Step 4). Otherwise build through.
- No "is this okay?" between steps. Make calls and move.
- Surface only true blockers - genuine ambiguity in the source, not preference checks.
- Reference-doc tone in the output. Tight prose, plain text dollar amounts and dates, tables for comparison data.
- TL;DR at the top of each topic file. Common Issues at the bottom.
- Follow the user's voice/formatting preferences for any conversational responses, but the KB files themselves use neutral reference-doc tone unless the user specifies otherwise.