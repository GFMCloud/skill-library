# Scrollback components

Fourteen patterns. Markup is copy-paste ready against
[scrollback.css](scrollback.css). Use a listed pattern before inventing one.

## The frame (the signature element)

Every block of content sits in one. It carries all the personality; the content
inside stays flat.

```html
<section class="frame">
  <span class="c tl">+</span><span class="c tr">+</span>
  <span class="c bl">+</span><span class="c br">+</span>
  <span class="ttl">04 · Color</span>
  ...content...
</section>
```

```
+ - - - - - - - -  [ TITLE ]  - - - - - - - - +
|                                             |
|            content sits here                |
|                                             |
+ - - - - - - - - - - - - - - - - - - - - - - +
```

| | |
|---|---|
| Corner glyph | `+` at 15px in `--rule` |
| Horizontal run | 8px dash / 10px gap, 1px |
| Vertical run | 14px tick / 30px gap, 1px |
| Title | centred, knocks out the top rule, wrapped in `[ ]` with a space inside each bracket |
| Padding desktop | 48 top / 48 sides / 40 bottom |
| Padding mobile | 40 / 24 / 32 |
| Radius | 0 |

Verticals are deliberately sparser than horizontals so they read as intermittent
pipe characters rather than a dotted border. The rules are CSS gradients, not
borders, so the dash phase is identical at every frame width. The corners are
real `+` characters in the type, so they inherit the face.

**Frames do not nest.** A frame inside a frame means the content was two ideas;
split it. The only rectangles permitted inside a frame are the `--surface` panel
(document, command block) and the corner-bracket spec box, and neither uses the
dashed treatment.

Frames stack in a single 880px column with 80px between them.

---

## 1. Data table

```html
<div class="scroll">
<table>
  <thead>
    <tr><th>Agent</th><th class="r">Tokens</th><th class="r">Time</th></tr>
    <tr class="rule"><td colspan="3"><span></span></td></tr>
  </thead>
  <tbody>
    <tr><td>Inks and paper</td><td class="r">115,207</td><td class="r">16m</td></tr>
    <tr><td>Overprint and drift</td><td class="r">135,218</td><td class="r">16m</td></tr>
    <tr class="rule"><td colspan="3"><span></span></td></tr>
  </tbody>
  <tfoot>
    <tr><td>Total</td><td class="r">437,141</td><td class="r">~50m</td></tr>
  </tfoot>
</table>
</div>
```

- Header row in `--text`. Not muted, not accent. Muting the header is the most
  common mistake.
- Dashed separator beneath the header and above the total. Total row `--bright`.
- No zebra striping, no vertical rules, no cell borders, no hover highlight.
- Units live with the number, never doing double duty in the column header.
- Approximation is marked: `~50m` is honest, `50m` would not be.
- Always inside `.scroll`. The table scrolls, never the page.

## 2. Flow

```html
<div class="flow">
  <div class="node">
    <div class="bars" role="img" aria-label="Small input, seven short bars">
      <i style="height:5px"></i><i style="height:9px"></i><i style="height:13px"></i>
    </div>
    <span class="cap">your taste</span>
  </div>
  <div class="leader"></div>
  <span class="glyph">▸</span>
  <span class="glyph" style="color:var(--text)">AI</span>
  <div class="leader"></div>
  <span class="glyph">▸</span>
  <div class="node">
    <div class="bars" role="img" aria-label="Amplified output, eight taller bars">
      <i style="height:14px"></i><i style="height:34px"></i><i style="height:40px"></i>
    </div>
    <span class="cap">amplified</span>
  </div>
</div>
```

- The shape is `state ── ▸ ── transform ── ▸ ── state`. Connectors are dashed
  leaders in `--rule` with `▸` in `--muted` at each junction.
- Both end states must be the same kind of object at different magnitudes. The
  delta is the point, so the two sides have to be visually comparable.
- The transform label sits in `--text`, unboxed. It is a step, not a node.
- Below 640px the leaders and glyphs hide and the flow stacks; order carries the
  sequence.

## 3. Spec diagram

```html
<div class="box">
  <span class="k2 tl"></span><span class="k2 tr"></span>
  <span class="k2 bl"></span><span class="k2 br"></span>
  <div>outer&nbsp;&nbsp;16px</div>
  <div class="box" style="margin-top:16px;max-width:60%">
    <span class="k2 tl"></span><span class="k2 tr"></span>
    <span class="k2 bl"></span><span class="k2 br"></span>
    <div>inner&nbsp;&nbsp;12px</div>
  </div>
  <div style="margin-top:16px">inset&nbsp;&nbsp;4px</div>
</div>
<div class="formula">
  inner = outer &minus; inset<br>
  <span class="dim">12px&nbsp;&nbsp;=&nbsp;&nbsp;16px&nbsp;&minus;&nbsp;&nbsp;4px</span>
</div>
```

- Four L-shaped corner brackets in `--accent`, 14px arms, 1px stroke. Never a
  closed border.
- Each box carries a `name  value` label with exactly two spaces between.
- Close with the relationship as an equation, then the same equation with numbers
  substituted in `--muted`. The formula line is the payoff; do not bury it.
- This is a sanctioned accent use: the brackets are data, not decoration.

## 4. Document (invoice, receipt, statement)

```html
<div class="doc">
  <div class="meta">
    <span class="mark"><svg width="16" height="16" ...></svg> Well</span>
    <dl>
      <dt>Ref</dt><dd>WELL-2026-0417</dd>
      <dt>Due</dt><dd>26 Jun 2026 · Net 14</dd>
    </dl>
  </div>
  <div class="drule"></div>
  <div class="cols">
    <div>
      <div class="eyebrow">From</div>
      <div class="br">Wellapp SAS</div>
      <div class="sub">15 Rue Raynouard<br>75016 Paris</div>
    </div>
    <div>
      <div class="eyebrow">Bill to</div>
      <div class="br">Ferrari S.p.A.</div>
      <div class="sub">Via Abetone Inferiore 4<br>41053 Maranello</div>
    </div>
  </div>
  <div class="drule"></div>
  <div class="scroll"><table>...line items...</table></div>
  <div class="drule"></div>
  <div class="totals">
    <div class="row"><span class="sub">Subtotal excl. VAT</span><span>&euro;3,975.18</span></div>
    <div class="drule" style="margin:12px 0"></div>
    <div class="row total"><span>Total due</span><span>&euro;4,770.22</span></div>
  </div>
</div>
```

- A `--surface` panel inside the frame, 56px padding. This is the only place
  `--surface` appears.
- Separators inside the panel use `--rule-dim`, not `--rule`. On a raised panel
  the full rule is too strong.
- Mark top-left; label/value metadata top-right with values right-aligned in
  `--bright`.
- Line items are `--text` with a `--muted` sub-description directly beneath.
- Totals right-aligned in a column no wider than 340px.
- Signal tokens are **not** permitted here. An invoice has no severity.
- Prints through the paper palette with no layout change. Any SVG mark must use
  `fill="var(--bright)"`, never a literal, or it vanishes on paper.

## 5. Chart

```html
<div style="display:flex;align-items:flex-end;gap:32px">
  <div class="bars" style="height:88px" role="img"
       aria-label="Runs per week, eight bars rising from 22 to 88, latest 1,204">
    <i style="height:22px"></i><i style="height:47px"></i><i style="height:88px"></i>
  </div>
  <div class="rows tight" style="padding-bottom:4px">
    <div class="cap">runs per week</div>
    <div class="br">1,204 <span class="sub">latest</span></div>
  </div>
</div>
```

- Flat bars in `--accent`, square corners, 16px wide, 3px gaps. No axes, no
  gridlines, no tooltips as decoration.
- **No second series colour.** If a chart needs a legend it is doing too much for
  this system; split it.
- The value that matters is stated in `--bright` next to the chart, not read off
  an axis. Bars carry shape, the number carries fact.
- `role="img"` plus an `aria-label` stating trend and range. A bar chart with no
  text alternative is a decorative rectangle.

## 6. Status pill

```html
<span class="pill ok">OK</span>
<span class="pill live">RUNNING</span>
<span class="pill">IDLE</span>
<span class="pill warn">DEGRADED</span>
<span class="pill fail">FAILED</span>
```

- A bracketed uppercase word at 13px, 0.08em tracking. No background, no border,
  no radius, because there is no pill.
- State is carried by the **word first and the colour second**, so meaning
  survives greyscale, colour deficiency and a plain-text log.
- OK is `--bright`, idle `--muted`, running `--accent`, degraded
  `--signal-warn`, failed `--signal-fail`.
- Running counts against the accent budget. If a screen has many concurrent live
  states, drop them all to `--bright`.

## 7. Log stream

```html
<div class="log">
  <div class="ln"><span class="t">09:41:02</span><span class="s">info</span>
    <span class="m">connector.sync started · 48,200 records queued</span></div>
  <div class="ln warn"><span class="t">09:41:44</span><span class="s">warn</span>
    <span class="m">rate limit at 82% · backing off 2s</span></div>
  <div class="ln fail"><span class="t">09:42:38</span><span class="s">fail</span>
    <span class="m">batch 6/8 rejected · schema drift on `issued_at`</span></div>
</div>
```

- Three columns on a fixed grid: timestamp `--rule`, severity `--muted`, message
  `--text`. The timestamp is chrome, so it recedes furthest.
- Severity words are lowercase and padded to a fixed width so the message column
  stays flush. This is the one place lowercase labels are correct.
- Only the failing line brightens its message to `--bright`. Everything else
  stays at `--text` so the failure is findable by scanning.
- No row backgrounds, no left border stripes, no icons.
- Below 640px the grid collapses to one column and the three parts run inline.

## 8. Command block

```html
<div class="cmd"><span class="p">$ </span><span class="in">scrollback verify --tokens</span>
<span class="out">  7 core tokens             ok
  contrast floor 4.50:1     ok · lowest 4.70:1 (--muted on paper)</span>
<span class="p">$ </span><span class="in">_</span></div>
```

- A `--surface` panel at 13px. Prompt sigil `--muted`, typed command `--bright`,
  output `--text`.
- `white-space:pre` is load-bearing. Without it the newlines collapse and the
  block renders as one line. This bug ships regularly.
- Output is never re-typeset. Reproduce it as the program emitted it, including
  the alignment.
- Never syntax-highlight the command.
- The trailing cursor is a **static** underscore. It does not blink.

## 9. Spec sheet

```html
<div class="spec">
  <dt>Family</dt><span class="lead-dots"></span><dd>Berkeley Mono TX-02</dd>
  <dt>Advance width</dt><span class="lead-dots"></span><dd>0.60em</dd>
  <dt>Licence</dt><span class="lead-dots"></span><dd>per seat</dd>
</div>
```

- Label `--muted` left, value `--bright` right, dotted leader between. The
  datasheet pattern, for short flat facts only.
- Fewer than about ten pairs and no second dimension. More than that, or any
  comparison across rows, is a data table.
- The leader is **dotted** `--rule`, not dashed. Dashes belong to the frame and
  the separators; the leader is a different job and reads as one.
- Values never wrap. A value long enough to wrap is a table cell.
- Below 640px the leader drops and the pair stacks, label over value. A dotted
  leader shorter than about 8 characters reads as damage, not structure.

## 10. Meter

```html
<div class="meter"><span class="label">tokens</span>
  <span class="track"><span class="fill" style="width:34%"></span></span>
  <span class="val">34%</span></div>
<div class="meter"><span class="label">rate limit</span>
  <span class="track"><span class="fill fail" style="width:100%"></span></span>
  <span class="val">100%</span></div>
```

- Track `--rule-dim`, fill `--accent`, both 8px tall and square. The track is
  always full width so bars are comparable down the column.
- `.track` and `.fill` **must be `display:block`**. As inline spans a percentage
  width silently computes to 0 and the meter renders empty.
- The numeric value is always printed in `--bright` at the end. A bar without its
  number is a decoration.
- Fill switches to `--signal-warn` above a declared threshold and
  `--signal-fail` at breach. Declare thresholds in the product, not per screen.
- No animation on fill width, no gradient, no rounded cap, no percentage inside
  the bar.

## 11. Sparkline

```html
<svg width="180" height="24" viewBox="0 0 180 24" role="img"
     aria-label="Sync latency over 14 days, flat near 8 then rising to 21 on the final day">
  <polyline fill="none" stroke="var(--muted)" stroke-width="1"
            points="0,16 42,14 84,15 126,10 166,9 178,3"/>
  <rect x="176" y="1" width="4" height="4" fill="var(--accent)"/>
</svg>
```

- 1px polyline in `--muted`, no fill, no axis, no grid. A 4px square in
  `--accent` marks the latest point and nothing else does.
- Fixed 180 × 24 box so lines stack comparably in a column. Never stretch one to
  fill available width.
- Current value `--bright` and window `--muted` sit to the right, always.
- Colours as `var()`, not literals, or the mark breaks under the print palette.
- The `aria-label` states shape, range and endpoint in words. It is the only
  accessible reading of the mark.

## 12. Note

```html
<div class="note warn">
  <div class="h">Caution</div>
  <p>The left rule and the heading take --signal-warn. The body stays --text.</p>
</div>
```

- A 1px left rule with 24px indent. No background, no icon, no rounded card.
- Heading word uppercase 13px, 0.12em tracking, matching the eyebrow role.
- Coloured notes are a signal-token use and inherit that scope: system state, not
  editorial emphasis.
- Never use a note to make ordinary prose feel important. Three on a page is
  already too many.

## 13. Tree

```html
<pre class="tree"><span class="d">scrollback/</span>
<span class="g">├─</span> <span class="d">tokens/</span>
<span class="g">│  └─</span> core.css        <span class="k">7 tokens</span>
<span class="g">└─</span> specimen.html     <span class="k">normative</span></pre>
```

- Box-drawing characters `├ │ └ ─` in `--rule`. The one sanctioned extension to
  the glyph set, because a tree drawn any other way is worse.
- Directories `--bright` with a trailing slash, files `--text`, annotations
  `--muted` at the right.
- Set in a `<pre>` so the alignment is the alignment. Never rebuild a tree out of
  nested lists and indents.
- The glyphs are content here, not decoration, so they are announced. Keep names
  meaningful.

## 14. Field and button

```html
<div class="field">
  <label for="ref">Reference</label>
  <input id="ref" type="text" placeholder="WELL-2026-0417">
</div>
<button class="btn" type="button">Issue</button>
<button class="btn" type="button" disabled>Void</button>
```

- Inputs are a `--surface` well with a single `--rule` underline. No box, no
  radius, no inner shadow. The underline is the field.
- Placeholders are `--rule`, deliberately near-invisible: a placeholder is not a
  label, and this system always ships the label.
- Buttons are a 1px `--rule` outline with uppercase 13px `--text`. Hover lifts
  text to `--bright` and border to `--muted`. Nothing fills.
- **No primary button fill.** A filled accent button is a fourth accent use.
  Primacy comes from order and from wording.
- Destructive actions are not red buttons. They are ordinary buttons behind a
  confirmation that states the consequence in `--signal-fail`.
- Disabled drops to `--rule` on `--rule-dim`, failing contrast on purpose: it is
  not readable because it is not available.

---

## Interaction states

| State | Treatment |
|---|---|
| Link, rest | `--bright`, dashed `--rule` underline, 4px offset |
| Link, hover | underline goes solid and `--bright` |
| Focus | 1px `--accent` outline, 2px offset, radius 0 |
| Hover, controls | `--text` → `--bright`, border `--rule` → `--muted` |
| Active | no additional treatment; the result is the feedback |
| Disabled | `--rule` on `--rule-dim`, no pointer |
| Selection | `--accent` ground, `--canvas` text |
| Loading | the word, in `--muted`. No spinner, no skeleton, no shimmer |

## Utility classes

`.scroll` overflow container · `.rows` / `.rows.tight` / `.rows.wide` vertical
stacks · `.cols` equal columns · `.hr` / `.hr.dim` dashed separators ·
`.panel` / `.pad` surface panels · `.eyebrow` bracketed label · `.cap` caption ·
`.sub` `.br` `.dim` `.acc` brightness ramp · `.r` right-align · `.nw` nowrap ·
`.mast` masthead · `.pill` status · `.note` callout
