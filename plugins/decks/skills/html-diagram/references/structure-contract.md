# Structure Contract

The exact rules for filling the four content slots in `assets/template.html`. Read this before drawing. The `<style>` block and the `<script>` engine are frozen - you only ever touch four things: the SVG zones, the SVG nodes, the SVG edges (+ labels), and the two JS objects `DETAIL` and `FLOWS`.

The canvas is a fixed SVG `viewBox="0 0 1560 980"`. It scales to fit any screen, so coordinates are abstract units, not pixels. Origin is top-left, x grows right, y grows down.

---

## The mental model

A diagram is four layers stacked on one SVG stage:

- **Zones** - dashed-outline columns that group components. Visual only, no interactivity. Lay them left-to-right in the direction data flows.
- **Nodes** - the clickable component boxes, placed inside zones.
- **Edges** - the arrows between nodes, each with a small text label.
- **Two data objects** - `DETAIL` (what shows when a node is clicked) and `FLOWS` (what lights up when a chip is clicked).

The engine wires it together: clicking a node looks up its `data-k` in `DETAIL`; clicking a chip looks up its `data-flow` in `FLOWS`, dims everything, then re-lights the listed edges and nodes and animates the arrows.

---

## SLOT 1 - Zones

One `<g class="zone">` per grouping. Lay them as columns across the 1560-wide canvas in flow order.

```
<g class="zone" id="z-aws">
  <rect x="690" y="120" width="390" height="720"/>
  <text class="ztitle" x="710" y="150">AWS Integration</text>
  <text class="zsub"   x="710" y="168">the glue we own</text>
</g>
```

- `ztitle` is the group name (uppercased by CSS). `zsub` is an optional one-line caption.
- Title text sits at `zone_x + 20`, `zone_y + 30`; subtitle 18 below that.
- Leave a gutter of ~40-60 units between zone columns for edges and labels to breathe.
- A typical 4-column layout: zones starting near x=40, 330, 690, 1120. Widen a zone if its nodes are wide (a node with long text lines needs ~350 width).

## SLOT 2 - Nodes

One `<g class="node ...">` per component, placed inside a zone's rect.

```
<g class="node hero" data-k="lambda">
  <rect x="710" y="330" width="350" height="120"/>
  <text class="t" x="730" y="360">Offer Lambda</text>
  <text class="k" x="730" y="380">the one integration point</text>
  <text class="m" x="730" y="402">Python · boto3</text>
  <text class="m" x="730" y="420">builds the ChangeSet request</text>
</g>
```

Rules:
- **`data-k` is the join key.** It must be unique and must have a matching `DETAIL[data-k]` entry. The validator enforces this.
- Text x-offset is `rect_x + 20`. First line (`t`) at `rect_y + 30`; each following line +18 to +22.
- Keep to a title plus 2-4 short lines. If you need more, it belongs in the click-through `DETAIL`, not on the box.
- Text classes: `t` = title (bold, ink), `m` = muted mono detail line, `k` = a small gold "kicker" tag for the one thing you want to flag on a node (use sparingly, ~once).

### Node classes (pick one by role)

| Class | Look | Use for |
|---|---|---|
| (none) | plain surface box | the default - most components |
| `hero` | gold-tinted fill, gold border | the single most important node - the one integration point, the core service. **Use once per diagram.** |
| `store` | grey-blue fill | datastores, secrets, anything that holds state |
| `entity` | teal-tinted fill | a created artifact / the thing the system produces |
| `ext` | dashed border | external / third-party / not-owned-by-us components |

Classes combine: `class="node store ext"` = an external datastore.

## SLOT 3 - Edges (and labels)

Draw edges **after** nodes exist, so you know the connect points. One `<path class="edge">` per connection, with a matching label.

```
<path class="edge" id="e-lambdacat" d="M1060,372 C 1102,372 1112,232 1140,232"/>
<text class="elbl" data-e="e-lambdacat" x="1090" y="300" text-anchor="middle">StartChangeSet</text>
```

Rules:
- **`id` on the edge, `data-e` on the label must match.** The validator enforces this.
- Use a cubic Bézier (`C`) for anything that isn't a straight horizontal/vertical hop - it routes cleanly around boxes. `M startX,startY C c1x,c1y c2x,c2y endX,endY`.
- Start/end on the **edge** of a node's rect, not its center, so the arrowhead lands on the border. Horizontal hop: start at `(node_right, node_mid_y)`, end at `(next_left, next_mid_y)`.
- Add `class="edge dash"` for dependencies, credential reads, "built on top of" relationships - anything that isn't the main request flow.
- Arrowheads are automatic (`marker-end`). Direction follows the path direction, so draw from source to target.
- **Route around nodes, never through them.** If a straight line would cross a box, bend the Bézier.
- Labels: 1-3 words, placed near the midpoint, nudged off the line so they don't sit on it. If an edge passes close to a node, push the label away from that node's text - label/text collision is the most common layout bug.

## SLOT 4 - DETAIL and FLOWS (in the `<script>`)

### DETAIL - one entry per node

```
const DETAIL = {
  lambda: { t:"Offer Lambda", m:"the ONE integration point",
            b:"Assembles the <code>StartChangeSet</code> request... <b>the only in-house code that talks to Marketplace</b>." },
};
```

- Key = the node's `data-k`. `t` = title, `m` = a meta/subtitle line, `b` = 1-3 sentence body.
- `b` allows inline HTML: `<b>` for the key takeaway, `<code>` for API calls / identifiers. Keep it to the "why this matters," not a spec dump.
- Every node needs one. Extra entries with no node are allowed but flagged.

### FLOWS - one entry per chip

```
const FLOWS = {
  create: {
    name: "Create offer - the Catalog API path",
    edges: ["e-flowapi","e-apilambda","e-lambdacat","e-catoffer"],
    nodes: ["flow","apigw","lambda","catalog","offer"],
    steps: ["Power Automate calls API Gateway...", "Lambda submits <code>StartChangeSet</code>...", "..."]
  }
};
```

- Key = the chip's `data-flow`. Add a matching `<button class="chip" data-flow="create">` in the top bar.
- `edges` / `nodes` = the ids and data-ks that light up on this path. List them in flow order (cosmetic, but reads better).
- `steps` = ordered caption lines shown bottom-left when the flow is active. Inline HTML ok. Aim for 3-5.
- **Do not add an `all` entry** - "Everything" is built into the engine and just clears the highlight.
- Pick flows that tell distinct stories. 2-5 is the sweet spot. One per major request path ("create", "read", "notify", "login"), not one per edge.

---

## Layout method that works

1. Decide zones and their left-to-right order first. Assign each an x-column and a width.
2. Stack nodes vertically inside each zone. Give the hero node a bit more height.
3. Only now draw edges - you can read the connect coordinates off the placed rects.
4. Add labels last, nudging each off its line and away from nearby node text.
5. Run `scripts/validate.py`, then screenshot (`--shots`) and eyeball.

## Gotchas (carried from real builds)

- **`hero` fill can go muddy on a dark navy ground** (gold-on-navy can read olive depending on the exact hues in play). It's acceptable; the lit state recolors it during a flow anyway. Don't put two hero nodes in one diagram.
- **Label/node-text collision** is the #1 layout bug. A label sitting on a node's bottom line looks broken. Nudge it.
- **Don't edit the theme pre-paint script or the `diagram-theme` localStorage key** - they're in the template head for a reason (no flash of wrong theme on load).
- **Fonts:** the default web font (Inter, currently) loads from Google Fonts at view time - a deliberate choice, not an oversight, so the file stays self-contained without needing local TTFs. Sandbox screenshots fall back to system-ui if the fetch is blocked - fine for checking layout, the real font renders in the browser. Swap `--diagram-font` and the `<link>` together if the project has its own brand font.
- **Wordmark, not logo:** the bar uses a text lockup (a placeholder org name) because brand PNGs aren't always available. If the user provides a logo path, base64-embed it with a light/dark swap and replace the `.wordmark` span - don't invent a brand mark.
