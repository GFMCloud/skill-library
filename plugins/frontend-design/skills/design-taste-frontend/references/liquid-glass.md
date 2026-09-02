# Apple Liquid Glass: honest web approximation

Derived from upstream `Leonxlnx/taste-skill` v2, `skills/taste-skill/SKILL.md` Appendix C and the
§5 glassmorphism note, at commit `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`. Restyled to the pack's
conventions. The flagship body (`../SKILL.md`, section 6) has the two-line refraction directive;
this file is the full skeleton and the honesty note.

Do not treat random CSS snippets as official Apple Liquid Glass.

## When glass is appropriate

Premium consumer, Apple-adjacent, luxury brand, or media-overlay vibes. Inappropriate for
dashboards, public-sector, or "boring B2B" briefs. When used, go beyond `backdrop-blur`: add a 1px
inner border and a subtle inner shadow for physical edge refraction, and provide a solid-fill
fallback under `prefers-reduced-transparency`.

## What is official

Apple documents Liquid Glass inside the Human Interface Guidelines and the Developer Documentation
for Apple platforms. It is a dynamic material used across Apple platform UI. The native
implementation belongs to Apple platform APIs and system components, not to a public web CSS
package. Relevant official docs: Human Interface Guidelines, Materials; Developer Documentation,
Liquid Glass and Adopting Liquid Glass; SwiftUI, Material.

## What is not official

There is no `liquid-glass.css` from Apple for normal websites. A web approximation can use
`backdrop-filter`, transparent backgrounds, layered borders, highlight overlays, gradients, motion,
and strong contrast fallbacks. That is web glassmorphism, a frosted-glass approximation, not
official Apple Liquid Glass. Label it as such in comments.

## Safer web approximation skeleton

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

.liquid-glass-web-approx::before {
  content: "";
  position: absolute;
  inset: 0;
  z-index: -1;
  border-radius: inherit;
  background:
    radial-gradient(circle at 20% 0%, rgb(255 255 255 / .55), transparent 34%),
    linear-gradient(90deg, rgb(255 255 255 / .18), transparent 42%, rgb(255 255 255 / .14));
  pointer-events: none;
}

.liquid-glass-web-approx::after {
  content: "";
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  border: 1px solid rgb(255 255 255 / .14);
  pointer-events: none;
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
    box-shadow:
      inset 0 1px 0 rgb(255 255 255 / .22),
      0 18px 60px rgb(0 0 0 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

`prefers-reduced-transparency` has uneven browser support; test it. Always provide enough contrast
even without the blur. The `backdrop-blur` performance rule in the flagship body still applies:
fixed and sticky elements only, never scrolling containers.
