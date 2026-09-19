# Designing a set of phone app screens

Part of the [frontend-design](../../README.md) pack.

This skill designs app screens for a phone, as a set that holds together rather than one attractive mockup. It picks a platform first, iPhone or Android or a neutral middle, and says which, because that choice decides the navigation, the bars at the top and bottom, and the spacing. It then commits out loud to how many screens it is making, keeps one palette and one navigation model across all of them, and leaves room for the parts of the screen the phone itself owns: the status bar, the notch, the tab bar and the home indicator. It designs screens. It does not write app code.

## Say this to use it

Any of these will do:

- "design the screens for my app: welcome, home, profile and settings"
- "I need an onboarding flow for an iOS app, four or five screens"
- "here's a screenshot of my app, design the rest of the screens to match"

Or, to be certain this skill and no other one runs:

```
/frontend-design:mobile-taste-frontend
```

It will name the platform it is committing to and list the screens it is about to make, before it makes any of them, so you can change either while it is still cheap. It will also say plainly if it has no image-generation tool and which fallback it is taking.

## What you'll get

The screen list stated first, then each screen, either as a labelled mockup in a phone frame or as a written screen specification.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Platform: iOS native. Tab bar for the four top-level sections, sheets for
secondary tasks, large titles on the list screens.

Six screens: welcome, permissions, home, browse, detail, profile.

[Screen 1 of 6: welcome]  (mockup in a phone frame)
[Screen 2 of 6: permissions]  (mockup in a phone frame)
...

Held across the set:
  Palette    bone, ink, one clay accent
  Type       one display face, one text face, nothing below 15pt
  Safe area  44pt reserved at the top, 34pt at the home indicator
  Nav        tab bar on home, browse, saved, profile; detail pushes, never tabs
```

## Good to know

- **It calls an image-generation tool repeatedly** if your Claude Code has one connected: one call per screen, and again for any screen it judges too weak to ship. Each call costs whatever that tool costs you.
- **It works without an image tool,** from a screenshot you supply or from a written screen specification it agrees with you first.
- **The image tool is yours, not the skill's.** If one is connected, you connected it. This skill sets nothing up and handles no key.
- **It does not write app source code.** No SwiftUI, no Jetpack Compose, no React Native. That is its own stated boundary, so expect designs and a specification, not something you can build and run.
- **It is not for websites.** A web page, a hero or a marketing page goes to a different skill.
- **It runs no programs, fetches nothing itself, and asks for no sign-in.**
- **It will not hand back one screen instead of the set,** by its own rule, so expect the whole list you agreed to.

## What next

- Building a web page rather than app screens? Use [image-taste-frontend](../image-taste-frontend/), which works the same way for pages.
- Want a page built straight into code? Use [design-taste-frontend](../design-taste-frontend/), or [minimalist-ui](../minimalist-ui/) for a quiet style.
- Deciding how a control should move and respond? Use [emil-design-eng](../emil-design-eng/).
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
