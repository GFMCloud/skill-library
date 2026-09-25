# Brand kit contract v1

Status: proposed 2026-09-25 with the consolidation hardening PR. Binding on every
skill that styles output from a brand (decks, diagrams, frontend, charts) once it
merges.

## Why this exists

Deck, diagram and frontend skills in this library never define a brand. They take one
from a folder the user points at, which the skills already call the "design system
folder" or "brand kit". Until now that folder had no defined shape, so each skill
guessed at it. Skills coming in from a private work library also expect to run a drift
check against the brand's own asset script. This contract gives the folder one shape
that any brand (a personal one, an employer's, a client's) can fill, and says how a
skill uses it.

## The folder

```
<kit>/
├── colors_and_type.css    required: the tokens below, declared on :root
├── fonts/                 optional: font files the CSS names (.ttf, .otf, .woff2)
├── assets/logos/          optional: logo files (.svg preferred, .png accepted)
├── brand-assets.py        optional: the brand's own asset tool (see Drift check)
└── .brand-provenance      optional: written by brand-assets.py when it installs a kit
```

A kit is found in this order: the path the user gives, then `./brand-kit/` in the
project, then the neutral default kit in this repo at `templates/brand-kit/`. A skill
that falls back to the default says so in its output.

## Tokens in colors_and_type.css

Type scale: the `--t-*` names `cd-to-pptx` already reads (see its
`references/wireframe-baseline-rules.md`). Pixel values are for a 1920x1080 slide;
a skill scaling to another surface keeps the ratios.

| Token | Role |
|---|---|
| `--t-hero` | hero number or cover title |
| `--t-title` | slide or page title |
| `--t-subtitle` | subtitle |
| `--t-body` | body text |
| `--t-small` | small text and labels |
| `--t-micro` | captions |
| `--t-eyebrow` | eyebrow above a title |

Fonts and color, by role:

| Token | Role |
|---|---|
| `--font-display` | headings; a full font stack ending in a generic family |
| `--font-body` | running text; a full stack |
| `--font-mono` | code and data; a full stack |
| `--c-bg` | page or slide background |
| `--c-surface` | cards and panels on the background |
| `--c-fg` | primary text |
| `--c-fg-muted` | secondary text |
| `--c-line` | rules, borders, gridlines |
| `--c-accent` | the one emphasis color (chart hero series, links, highlights) |
| `--c-accent-soft` | accent at low strength (fills, hover) |
| `--c-good`, `--c-warn`, `--c-bad` | status colors, separate from the accent |

A kit may declare more tokens. A skill uses only the ones above unless its own
SKILL.md names an extra token and says what happens when a kit lacks it.

## How a skill uses a kit

1. **Resolve the kit** by the order above, and name the one in use in its output.
2. **Read tokens by name** from `colors_and_type.css`. When a token is missing, use
   the default kit's value for it and say which tokens were defaulted. Never invent a
   brand value.
3. **Drift check, when the kit supports it.** If `<kit>/brand-assets.py` exists, run
   `python3 <kit>/brand-assets.py check <output folder>` before calling the output
   finished. Exit 0 means the assets in the output match the kit. Any other exit is a
   stop: report the script's output verbatim and don't ship. When the script is
   absent, skip the check and say it was skipped. The contract fixes only the `check`
   subcommand and its exit code; a brand's script may do more.
4. **Assets are copied, never linked.** Fonts and logos used by an output are copied
   into it from the kit, so the output stands alone.

## Precedence

For a rebuilt artifact (an export converted to another format), the existing rule in
`cd-to-pptx` holds: the export is the truth for what is on the page and where; the kit
is the truth for asset files and for any token the export uses but does not define.
When the two disagree on a value, the skill flags it instead of picking one.

## Versioning

A change to a required file, a token's name or role, or the drift-check call is a
breaking change: bump this document to v2, note the migration in CHANGELOG.md, and
update every skill that reads a kit in the same PR.
