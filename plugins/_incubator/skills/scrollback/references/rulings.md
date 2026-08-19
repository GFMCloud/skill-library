# Scrollback rulings

Every number here was computed, not eyeballed. Ratios use the WCAG 2.x
relative-luminance formula; regenerate them with
[../templates/verify.py](../templates/verify.py).

## Palette, measured

### Core: seven tokens, and it stays seven

| Token | Hex | On `--canvas` | On `--surface` | Role |
|---|---|---|---|---|
| `--canvas` | `#11110F` | ground | | Page background. Warm near-black: R=G, B two points lower. |
| `--surface` | `#171715` | 1.05:1 | | Raised panels only. |
| `--rule` | `#494844` | 2.06:1 | 1.96:1 | Frames, separators, leaders. Never text. |
| `--muted` | `#8A8781` | 5.28:1 | 5.01:1 | Captions, sub-descriptions, label halves. |
| `--text` | `#B7B4AD` | 9.13:1 | 8.67:1 | Body and data. Warm bone, not white. |
| `--bright` | `#E9E7E1` | 15.29:1 | 14.52:1 | Emphasis only. |
| `--accent` | `#2E8EFF` | 5.79:1 | 5.50:1 | Frame titles, data marks, focus. |

### Extension A: rule on surface

`--rule-dim` `#2B2B29` · 1.33:1 on canvas, 1.27:1 on surface. Decorative only.
Separators drawn inside a `--surface` panel, where the full rule is too strong.

### Extension B: signal (system-state surfaces only)

| Token | Hex | On canvas | Permitted use |
|---|---|---|---|
| `--signal-warn` | `#E5A13A` | 8.54:1 | Degraded state, threshold breach, warning line in a log. |
| `--signal-fail` | `#F26A5A` | 6.29:1 | Failed state, destructive confirmation, validation error. |

Hard scope: logs, validation, alerts, product state. **Never** on a document, an
invoice, a marketing page, or a chart.

**There is no success colour.** Success gets `--bright`. A green would be a
fourth hue earning nothing: in a system whose default state is fine, "OK" is the
absence of a signal. It also keeps the palette legible to readers with a
red-green deficiency, since amber and red are separated by more than hue (the
severity word carries the meaning first).

### Extension C: paper (print only)

Invoked by `@media print` and nothing else. **There is no light theme for
screen** and the system does not respond to `prefers-color-scheme`.

| Token | Screen | Paper | On paper |
|---|---|---|---|
| `--canvas` | `#11110F` | `#F2F1EC` | ground |
| `--surface` | `#171715` | `#E8E6E0` | 1.10:1 |
| `--rule` | `#494844` | `#B5B2AA` | 1.87:1 |
| `--muted` | `#8A8781` | `#6E6B65` | 4.70:1 |
| `--text` | `#B7B4AD` | `#3A3833` | 10.35:1 |
| `--bright` | `#E9E7E1` | `#1B1B18` | 15.26:1 |
| `--accent` | `#2E8EFF` | `#1660C8` | 5.24:1 |

The accent darkens because it has to: `#2E8EFF` on `#F2F1EC` measures **2.89:1**
and fails at any size. `#1660C8` restores it to 5.24:1.

Consequence for marks: any SVG inside a printable surface must take its colours
from `var()`, never a literal, or it renders light-on-light on paper.

## Accent discipline and amendment SB-01/A1

Three uses: the bracketed frame title, data marks, the focus indicator.

**SB-01/A1.** The source system named two permitted uses and defined no focus
style at all. Focus is added as a third because it is a transient machine state
rather than decoration, and because the obvious alternative fails: `--rule`
measures 2.06:1 against the canvas and WCAG 1.4.11 requires 3:1 for a non-text
indicator. `--accent` measures 5.79:1 and passes. There was no compliant way to
keep the rule at two.

Interaction otherwise runs on the brightness ramp, not on hue: `--rule` →
`--muted` → `--text` → `--bright`, one step per state change.

## Accessibility floors that follow from the numbers

- `--muted` is the floor. Never below 13px, and never on `--surface` below 13px,
  where it drops to 5.01:1.
- `--rule` never carries meaning. A border conveying state must be `--muted` or
  brighter.
- Status is a word before it is a colour. Every signal use pairs the hue with a
  lowercase severity word or a bracketed pill.
- Decorative glyphs take `aria-hidden="true"`: frame corners, flow arrows, leader
  lines. The tree's box-drawing characters are content and stay readable.
- Every chart, sparkline and mark takes `role="img"` and an `aria-label` stating
  shape, range and endpoint.
- Prose measure is set in `ch` (72, hard ceiling 80). The 880px column holds
  about 97 characters at 15px, so the leftover column is left empty on purpose.
- Known limitation: one monospace face at 15px has a smaller effective x-height
  than a 15px grotesque. Readers who need larger text will zoom, so every layout
  must survive 200% zoom with no horizontal page scroll.

## Precedence

1. **The user's own words** win over everything here.
2. **A project's existing system** wins, unless the project is Scrollback.
3. **Scrollback owns charts and data marks inside a Scrollback surface.**

Point 3 is a deliberate exception to the account-level rule that `dataviz` owns
every chart in every medium. The reasoning: `dataviz` allocates a categorical
series palette, and Scrollback's entire proposition is seven tokens with one
accent. A multi-series palette dropped into a Scrollback surface adds a second,
third and fourth hue and the system stops reading as instrumentation on the first
chart. Scrollback's answer to multi-series is not a palette, it is a split: if a
chart needs a legend it becomes two charts.

What still applies from `dataviz` and is not overridden: the accessibility of the
encoding (contrast floors, never colour alone, redundant encoding), and the
discipline of choosing the mark form to fit the question. What is overridden:
series colours, legend conventions, and any palette allocation.

`artifact-design` fundamentals apply, with one exception: its instruction to
design both themes does not, because Scrollback is a deliberate single-theme
system with a print-only inversion. Paint background and every colour explicitly
so the page holds on either host ground.

## Source-set errata

The source declared `specimen.html` normative where the written guidelines and
the code disagreed. Four disagreements were found. In each case the code won.

| # | Guideline said | Code did | Resolution |
|---|---|---|---|
| E1 | Mobile frame padding 24 / 16 | 40 top, 24 sides, 32 bottom | Code wins; 40 / 24 / 32. |
| E2 | Seven tokens, no others | Ships an untokenized `#2B2B29` inside the document panel | Promoted to `--rule-dim`, extension A. |
| E3 | One separator pattern | `.rule` meant two things (table row and document divider), forcing a `.rule2` class with no matching CSS | Split into `tr.rule` and `.drule`. Dead class removed. |
| E4 | Accent has exactly two uses | No focus style defined at all | Amendment SB-01/A1. |

## Implementation bugs this system produces

Recorded because each shipped at least once and none is visible in code review.

- A `%` width on an inline `<span>` computes to 0. `.track` and `.fill` need
  `display:block`.
- A multi-line block that is not a `<pre>` collapses its newlines. The command
  block needs `white-space:pre`.
- A `white-space:nowrap` value overflows the viewport on mobile. Stack the pair
  instead of letting the page scroll sideways.
- Token names break after the leading `--`. Apply `.nw` to cells holding them.
- SVG colour literals survive screen and break on paper. Use `var()`.

## Where the CSS lives

[scrollback.css](scrollback.css) in this skill is the **single editable home** of
the system's CSS. Every Scrollback page inlines or links a copy, and those copies
are generated output: fix here first, then propagate. The published SB-01 brand
guide is a specimen that inlines such a copy plus its own document-only rules.

## Amending

- Extensions are declared with a scope, never added to core. Core stays at seven.
- A new accent use requires an amendment with a stated reason and a measured
  alternative that was rejected. SB-01/A1 is the format.
- A new component answers three questions before it ships: which brightness step
  carries its emphasis, what it does at 375px, what a screen reader gets.
- Revision numbering is `SB-01 rev N.M`. A change that breaks an existing surface
  increments N.
- Renaming or removing an exported token is a breaking change: bump the major and
  sweep every consumer.

## Revision history

| Rev | Date | Change |
|---|---|---|
| 1.0 | 2026-08-18 | Named Scrollback. Lineage, mark, interaction, motion, accessibility, applications, nine new components, three extensions, four errata added to the Terminal Spec source. |
| 0.1 | source | Terminal Spec design guidelines, extracted from four reference artifacts. |

## Lineage

Where the system comes from, and what it refuses.

| Reference | Taken | Left |
|---|---|---|
| Bloomberg Terminal (1982, custom mono by Matthew Carter) | Density as respect; a palette consistent enough to identify the room | The amber; the training cost |
| [Berkeley Mono TX-02](https://usgraphics.com/products/berkeley-mono), U.S. Graphics Company | The technical-drawing posture; the datasheet designator (`SB-01`, not `v1`) | The hardware nostalgia |
| [The Monospace Web](https://owickstrom.github.io/the-monospace-web/), Oskar Wickström | The character grid as a real layout constraint | The full character-cell lock; Scrollback snaps to 8px |
| man pages and RFCs | Citable numbered sections; the 80-column ceiling; no ornament that is not structure | Little; this is the closest ancestor |
| [Charm Lip Gloss](https://github.com/charmbracelet/lipgloss) | That a terminal surface deserves real layout discipline | 256-colour palettes |

Neighbours: [Geist Mono](https://vercel.com/font), Linear, Raycast, Resend use
mono as a brand accent. Scrollback uses it as the whole system.

Refused by name, because they are standard practice in the published
terminal-aesthetic genre ([terminal.css](https://terminalcss.xyz/), hacker.css,
the CRT-revival references) and a contributor will otherwise add them as a
helpful improvement: phosphor green, CRT scanlines and curvature, text glow,
blinking cursors, typewriter reveals, ASCII-art wordmarks, inverse-video
emphasis in running text, a hard 80-column page width.
