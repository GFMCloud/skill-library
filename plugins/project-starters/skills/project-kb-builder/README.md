# Turning a long document into knowledge files

Part of the [project-starters](../../README.md) pack.

A hundred-page handbook is the wrong shape for Claude to answer questions from. Retrieval works better on topic-sized files with predictable headings. This skill reads one long source document and rewrites it as a numbered set of markdown files: an index at the front, the rules that apply to everything next, then one file per topic, then reference material. Each topic file uses the same headings, so an answer about one topic is found the same way as an answer about any other. It flags contradictions and duplicates in the source rather than smoothing them over.

## Say this to use it

Any of these will do:

- "turn this 100-page PDF into knowledge files for a project"
- "break this handbook down into a KB"
- "make this into markdown I can upload as project knowledge"

Or, to be certain this skill and no other one runs:

```
/project-starters:project-kb-builder
```

It asks once whether you want a set of project instructions drafted alongside the files, or are handling that separately. Then it proposes the file list and waits for a yes. That is the only checkpoint. After it, it builds through without asking you to confirm interpretations.

## What you'll get

A proposed file list to approve, then the files themselves.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Proposed structure:

  00-funding-programs-index.md        router across all programs
  01-policies-and-key-dates.md        rules that apply to everything
  10-training-and-certification.md
  11-partner-fee-credits.md
  12-innovation-sandbox.md
  20-public-sector-considerations.md  vertical-specific overrides
  21-glossary.md

Confirm and I'll extract, or flag changes.

Two things found in the source, which I will note in the files
rather than quietly fix:
  - Sections 1.10 and 1.11 are identical. Treating 1.10 as the one
    that counts.
  - Section 4 says the cap is $50k; the appendix says $75k. Which
    applies?
```

## Good to know

- **The numbers in the filenames are doing work.** Lower numbers signal higher priority when several files match a question. The index is the entry point, the cross-cutting rules apply broadly, the topic files are narrow. If you want a different naming scheme it will honour it, and it will tell you what is lost.
- **It rewrites rather than copies.** Prose gets distilled and restructured for lookup. Amounts, dates, percentages and rule wording are kept exact.
- **It flags problems in the source in the file that carries them.** Duplicate sections, contradictions, references to sections that do not exist, and items listed as current that were discontinued.
- **It reads the one document you give it, in full, and nothing else.** It goes online for nothing, uses no account, and deletes or moves nothing.
- **It was written for the Claude website, not for Claude Code.** The last step writes the files to `/mnt/user-data/outputs/<kb-name>/` and then shows them with a tool called `present_files`. Neither the folder nor the tool exists when you run Claude Code on your own computer. To use it here, tell it where to put the files, for example a folder inside the project you are working in, and open them yourself. Everything before that last step works as written.
- **It will tell you when it is the wrong tool.** For a source under about thirty pages, or one that is pure narrative with no separable topics, it says so and suggests something simpler.
- **The finished files go somewhere you set up.** They are written for uploading into a Claude Project's knowledge, which you create and upload to yourself.

## What next

- Setting up the Claude Project that these files go into? [project-setup-wizard](../project-setup-wizard/) writes the description and the instructions for it.
- Back to the [project-starters pack](../../README.md), or to [skill-library](../../../../README.md).
