# GSAP and Motion skeletons for scroll work

Derived from upstream `Leonxlnx/taste-skill` v2, `skills/taste-skill/SKILL.md` §5.A to §5.D, at
commit `ccbc15639c97057cbfcf32ecebc38ef716e4bb37`. Restyled to the pack's conventions. The flagship
body (`../SKILL.md`, section 7) decides *when* a pattern is used; this file holds the canonical
code and the failure diagnoses.

Library choice: Motion (`motion/react`) for UI, bento, and state-change motion. GSAP plus
ScrollTrigger for full-page scrolltelling and scroll hijacks, isolated in dedicated leaf components
with `useEffect` cleanup. Never mix GSAP or Three.js with Motion in the same component tree; they
fight over the same frames.

## When each pattern applies

- **Sticky-stack** (cards pin and stack on scroll): a "card stack on scroll" must be a real
  sticky-stack, not a sequential reveal list. Common failure: the trigger fires halfway through the
  scroll instead of pinning at the viewport top. Fix: `start: "top top"`, not `start: "top center"`
  or `"top 80%"`.
- **Horizontal pan** (vertical scroll drives a horizontal track): common failure: the animation
  starts before the section is pinned, so the user sees half a slide. Same fix: `start: "top top"`,
  pin the wrapper, scrub the inner track.
- **Scroll-reveal stagger** (items appear as they enter the viewport, no pinning): prefer Motion's
  `whileInView` over GSAP. Lighter, no ScrollTrigger needed. Use it for feature lists, testimonial
  grids, logo walls, anything that only needs "enter on scroll". Save GSAP for real pin and scrub
  work.

Every skeleton below checks `useReducedMotion()` first and renders static when it is set. That is
the pack's reduced-motion rule (body section 8), not an optional nicety.

## A. Sticky-stack, canonical skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function StickyStack({ cards }: { cards: React.ReactNode[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !ref.current) return;
    const ctx = gsap.context(() => {
      const cardEls = gsap.utils.toArray<HTMLElement>(".stack-card");
      cardEls.forEach((card, i) => {
        if (i === cardEls.length - 1) return;
        ScrollTrigger.create({
          trigger: card,
          start: "top top",                              // pin at viewport top
          endTrigger: cardEls[cardEls.length - 1],
          end: "top top",
          pin: true,
          pinSpacing: false,
        });
        gsap.to(card, {
          scale: 0.92,
          opacity: 0.55,
          ease: "none",
          scrollTrigger: {
            trigger: cardEls[i + 1],
            start: "top bottom",
            end: "top top",
            scrub: true,
          },
        });
      });
    }, ref);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <div ref={ref} className="relative">
      {cards.map((card, i) => (
        <div
          key={i}
          className="stack-card sticky top-0 min-h-[100dvh] flex items-center justify-center"
        >
          {card}
        </div>
      ))}
    </div>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, every card except the last is pinned, and the
scale and opacity transform is driven by the *next* card's scroll trigger, so the previous card
shrinks as the next one arrives.

## B. Horizontal pan, canonical skeleton

```tsx
"use client";
import { useRef, useEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useReducedMotion } from "motion/react";

gsap.registerPlugin(ScrollTrigger);

export function HorizontalPan({ children }: { children: React.ReactNode }) {
  const wrap = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const reduce = useReducedMotion();

  useEffect(() => {
    if (reduce || !wrap.current || !track.current) return;
    const ctx = gsap.context(() => {
      const distance = track.current!.scrollWidth - window.innerWidth;
      gsap.to(track.current, {
        x: -distance,
        ease: "none",
        scrollTrigger: {
          trigger: wrap.current,
          start: "top top",                              // pin starts when section top hits viewport top
          end: () => `+=${distance}`,                    // scroll distance = track width minus viewport
          pin: true,
          scrub: 1,
          invalidateOnRefresh: true,
        },
      });
    }, wrap);
    return () => ctx.revert();
  }, [reduce]);

  return (
    <section ref={wrap} className="relative overflow-hidden">
      <div ref={track} className="flex h-[100dvh] items-center">
        {children}
      </div>
    </section>
  );
}
```

Critical points: `start: "top top"`, `pin: true`, `end: "+=${distance}"` (scroll length equals the
horizontal travel needed), `scrub: 1`. The wrapper is pinned; the inner track slides horizontally
as the user scrolls vertically.

## C. Scroll-reveal stagger, the lighter alternative

```tsx
"use client";
import { motion, useReducedMotion } from "motion/react";

export function RevealStagger({ items }: { items: string[] }) {
  const reduce = useReducedMotion();
  return (
    <ul className="grid gap-6">
      {items.map((item, i) => (
        <motion.li
          key={item}
          initial={reduce ? false : { opacity: 0, y: 24 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{
            duration: 0.6,
            delay: i * 0.06,
            ease: [0.16, 1, 0.3, 1],
          }}
        >
          {item}
        </motion.li>
      ))}
    </ul>
  );
}
```

## D. Forbidden animation patterns

- `window.addEventListener("scroll", ...)` is banned. It runs on every scroll frame, is jank-prone,
  and has no batching. Use Motion's `useScroll()`, GSAP's ScrollTrigger, `IntersectionObserver`, or
  CSS scroll-driven animations (`animation-timeline: view()`).
- Custom scroll-progress calculations using `window.scrollY` in React state. Same reason: a
  re-render on every frame.
- `requestAnimationFrame` loops that touch React state. Use motion values (`useMotionValue` plus
  `useTransform`) instead.
- Wrapping static content in `layout` props "for safety". `layout` and `layoutId` are for visible
  state changes (re-ordering lists, expanding modals, shared elements between routes); on static
  content they only cost measurement work.
- `staggerChildren` with the parent `variants` and the children in different Client Component
  trees. They must share one tree; if data is async, pass it as props into a centralized parent
  motion wrapper.
