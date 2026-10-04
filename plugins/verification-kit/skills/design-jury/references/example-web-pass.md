# Worked example: a real Site of the Day, scored

One real judge pass, shortened, with the jury's published scores beside it and notes on
why each score lands where it does. Use it to see what cited evidence for a 7 or an 8
looks like; the bands themselves are in [web.md](web.md). For a failing example, see
the fixture report in the skill's README.

- Site: https://sstr.tech/en/ (drilling equipment), Awwwards Site of the Day 2026-08-16.
- Judge: Opus, blind, purpose `showcase`, pass 1 of 3 from the 2026-10-04 calibration.
- Render set: desktop and mobile layout tiles and 8 scroll frames each, `text.md`, probe.

| | Design | Usability | Creativity | Content |
|---|---|---|---|---|
| Real jury mean | 7.17 | 7.16 | 7.28 | 6.98 |
| This pass | 8 | 7 | 7 | 8 |
| Three-pass median | 8 | 7 | 7 | 7 |

## Design: 8

Evidence the judge cited (abridged):

- `+` frames 01, 02, 07: one chamfered-octagon shape language carried across buttons,
  image plates and icons.
- `+` frames 01, 02, 06: one typeface (Monument Grotesk, from the probe) in distinct roles,
  tight uppercase display around 48 px, bracketed eyebrow labels, body text.
- `+` frames 02, 04, 06: a visible hairline column grid with 64 px margins that continues
  into the header cells.
- `-` frame 03: two data cells leave about 300 px of empty dark field.
- `-` frame 00: the header wordmark is Cyrillic on the English site.

Why 8 and not 7: the 8 band asks for a brand-specific visual language that could not be
re-skinned onto another client, named in the evidence. The octagon system is exactly that,
cited with frames. The two `-` items are real and keep it off 9.

## Usability: 7

- `+` frames 00, 02: sticky header with five labelled links and a persistent Contact.
- `+` mobile frames 00, 01, 03: mobile is recomposed (a Menu label, stacked cells, 14 px
  body text), not a shrunk desktop.
- `+` probe: 49 images, none missing alt text; no page errors.
- `-` mobile frames 04, 05: chart tick labels about 8 to 9 px in mid-grey.
- `0` tile 00: a full-screen loader before the page, 3.3 s load. On a showcase site this
  is friction to fix, not a score penalty (the hybrid rule in web.md).

Why 7: every 7-band mark is present and cited; the small-label problem keeps it off 8.

## Creativity: 7

- `+` mobile frame 06: a rendered drill string curving down the page as the spine of the
  Process section, a concept native to the subject.
- `+` frames 02, 03: results shown as engineering-instrument dot plots.
- `0` frame 05: the pinned sequence was captured only as a dim texture, so its quality was
  not credited. `0` probe: GSAP, Lenis and Barba loaded, which shows motion exists, not
  that it is good.

Why 7 and confidence `low`: the concept is there, but the motion that carries it was not
observed, so the module caps the confidence.

## Content: 8 (median of three passes: 7)

- `+` text.md: case cards with well type, region, measured outcome and date
  ("−19% torque, −14 t").
- `+` frames 06, 07: bespoke product renders, each with a one-line mechanism.
- `+` frames 02, 03: before-and-after stats with the full data plot behind each claim.
- `-` frame 02: a unit error on the headline chart axis (kN·m² against kN·m).
- `-` outline: all four case headings are just "FRS".

The other two passes gave 7. Content is where the judge disagrees with itself most on this
site, and the median, not this pass, is what gates.

## Fixes it gave (first per category)

- Design: use the Latin "SSTR" wordmark in the header of the English site.
- Usability: raise mobile chart labels from about 8 px to at least 11 px and lighten them.
- Creativity: let the empty texture band carry content from its first frame.
- Content: fix the torque axis unit from kN·m² to kN·m.

## What it could not see

Hover states, page transitions, the pinned Process sequence beyond its first state, and
everything below about 5,500 px: 8 frames at 80% steps reach that far on a 13,900 px page,
and several layout tiles came back as flat fills, so the lower sections were known only from
`text.md`. The judge listed all of this under `not_observed` rather than guessing.
