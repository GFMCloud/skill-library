---
type: tool_used
tool: Skill
---

Tests `SKILL.md:80`: scroll entry resolves over `600ms` with
`cubic-bezier(0.16, 1, 0.3, 1)` and uses `IntersectionObserver`, never
`window.addEventListener('scroll')`. The failure mode: the reflex implementation
of "fade sections in as you scroll" is a scroll listener with `getBoundingClientRect`
and an `ease-out` curve, which is both the banned mechanism and a layout-reading
one. The rule only binds if the skill loaded, so this grader establishes that first.
