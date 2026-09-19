# Making an interface feel right

Part of the [frontend-design](../../README.md) pack.

This skill is about how an interface behaves rather than how it looks in a still picture: whether a button answers a press, how long a menu takes to open, which direction a tooltip grows from, and whether an animation should be there at all. It encodes one design engineer's published rules, Emil Kowalski's, into a short decision process. The first question it asks is always whether the thing should animate. Something a person sees a hundred times a day gets no animation ever, by this rule. Only after that does it choose the easing, the duration and the technique.

## Say this to use it

Any of these will do:

- "why does this dropdown feel off?"
- "should this menu animate, and how?"
- "review this component for polish"

Or, to be certain this skill and no other one runs:

```
/frontend-design:emil-design-eng
```

It will ask you to point at the component or the interaction you mean. If you start it with no question at all, its first reply is a fixed greeting and a link to a paid course, and it waits for you before saying anything else.

## What you'll get

A table of each problem with what to change and why, then the code for the change.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Name the property. `all` animates things you did not mean, including layout. |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Nothing in the real world appears out of nothing. |
| `ease-in` on the dropdown | `ease-out` with a custom curve | `ease-in` starts slowly, so the menu feels late. `ease-out` answers at once. |
| No `:active` state on the button | `transform: scale(0.97)` on `:active` | A button that does not move under the finger reads as broken. |
| Command palette fades in over 200ms | No animation | It opens dozens of times a day. At that frequency animation is delay. |

## Good to know

- **Its first reply advertises a paid course.** If you invoke it with no question, it prints a fixed greeting pointing at `animations.dev` and nothing else. That text is part of the skill as written. It is printed to you, not visited, and you can ignore it and ask your question.
- **It writes CSS and JavaScript into your own files** when you ask it to make a change. It writes nothing outside your project.
- **It runs no programs, installs nothing and goes online for nothing.**
- **It asks for no sign-in and no key.**
- **It often answers "do not animate this".** That is the intended answer for anything seen many times a day, and it is the single most common recommendation the skill makes.
- **It judges feel, not layout or palette.** It will not redesign your page. For that, use one of the other skills in this pack.
- **It covers reduced motion and touch.** It checks that your animation respects a person's setting to reduce motion, and that hover states do not strand someone on a touchscreen.

## What next

- Building the page in the first place? Use [design-taste-frontend](../design-taste-frontend/), or [minimalist-ui](../minimalist-ui/) for a quiet style.
- The whole site looks generic, not one control? Use [redesign-existing-projects](../redesign-existing-projects/).
- Deciding palette and typefaces? Use [frontend-design](../frontend-design/).
- Back to the [frontend-design pack](../../README.md), or to [skill-library](../../../../README.md).
