# frontend-design

Part of [skill-library](../../README.md). If the words skill, pack or agent are new to you, that page explains them first.

## What problem this solves

Ask Claude Code for a web page and you tend to get the same page back. A purple gradient behind a centered headline, three equal cards below it, the Inter typeface, rounded corners on everything. It works, and it looks like every other page built the same way. The same thing happens to app screens, which come back as one pretty mockup with no second screen that matches it.

This pack gives Claude Code a point of view instead of a default. Each skill names the patterns to avoid, makes it state the look it is aiming at before it writes anything, and holds it to that decision across the whole page or the whole set of screens.

## When would I use this?

- You have a working site that does its job and looks like a template.
- You are starting a new page and want it to have a specific character, not a generic one.
- You want a quiet, document-like interface rather than a loud one.
- You are designing phone app screens and need a set that holds together, not one screen.
- Something in your interface feels wrong and you cannot say why.
- Several people or several helpers are building parts of one interface at the same time and must not collide.

## What's inside

<!-- generated:whats-inside by maintainers/scripts/generate-inventory.sh from plugins/frontend-design/reader-table.tsv; edit the source, never this block -->
| Skill | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [design-taste-frontend](skills/design-taste-frontend/README.md) | Designs and builds a new web page from scratch with a deliberate look: it reads your brief, states the style it is aiming at, then writes the code. | "build me a landing page for this that doesn't look like every other AI site" | A one-line statement of the design it read from your brief, then the page's code written into your project. | Writes web code (HTML, CSS, Tailwind, React) into your project and reads your project's `package.json`. If an image-generation tool is connected to Claude Code, it uses it to make the page's pictures. If a package is missing it prints an install command for you to run rather than running it. |
| [emil-design-eng](skills/emil-design-eng/README.md) | Reviews how an interface feels, and decides whether and how to animate something, using one design engineer's published rules about timing, easing and small details. | "why does this dropdown feel off?" | A before-and-after table of each change with the reason for it, and the CSS or JavaScript that makes it. | Writes the animation and style code you asked for into your own files. Its fixed first reply prints a link to an outside course website as text; it fetches nothing. |
| [frontend-design](skills/frontend-design/README.md) | Sets a design direction before the code: a small set of named colors, two or three typefaces, a layout idea, and one element the page is remembered by. | "help me pick a palette and typography for this page" | A short written plan with named colors and typefaces, a rough layout sketch, then the page built to that plan. | Writes the page or component you asked for into your project. It reads nothing else and goes online for nothing. |
| [image-taste-frontend](skills/image-taste-frontend/README.md) | Settles the look in pictures before any code: one reference image per section of the page, read as the specification, then built to match. | "design this landing page visually first, then build it" | One labelled image per section, a written reading of each for type, spacing, color and components, then the code. | Calls an image-generation tool if your Claude Code has one connected, once per section and often eight or more times, then writes the page's code into your project. |
| [minimalist-ui](skills/minimalist-ui/README.md) | Builds a page in one specific quiet style: warm off-white background, strong typography, thin borders, flat grid boxes, pale accent colors, almost no shadow. | "make this look clean and minimal, like Notion or Linear" | The page's code, using this style's fixed palette, type sizes and spacing rules. | Writes styled web code into your project. Where it has no real photograph it points the page at picsum.photos, a public placeholder service your browser loads from when the page is viewed. |
| [mobile-taste-frontend](skills/mobile-taste-frontend/README.md) | Designs a whole set of phone app screens that hold together: one platform, one navigation model, safe areas respected, each screen in its place in the flow. | "design the screens for my app: welcome, home, profile and settings" | The screen list stated up front, then each screen as a labelled mockup or as a written screen spec. | Calls an image-generation tool if one is connected, several times in a session. It does not write app source code (SwiftUI, Jetpack Compose or React Native), by its own rule. |
| [redesign-existing-projects](skills/redesign-existing-projects/README.md) | Goes through a site that is already built, lists the generic patterns in it across typography, color, spacing and missing states, and fixes them in the code that is there. | "my site works but looks generic, upgrade it without rewriting it" | A list of what it found, then edits applied to your existing style and component files. | Reads your project's code and edits it in place. It checks `package.json` before importing a new library and does not run an installer itself. |

This pack also ships agents. An **agent** is a helper that Claude Code hands a whole job to; it works on its own and reports back.

| Agent | What it does | What you say to trigger it | What you get | On your computer |
| :--- | :--- | :--- | :--- | :--- |
| [frontend-surface-builder](agents/frontend-surface-builder.md) | Builds one page or panel inside a file list it was given, then opens it, screenshots it and reads the browser's error log before saying it is done. | "build these three panels in parallel, one builder each" | The files it changed, a screenshot, the browser's error output, and any shared file it needs someone else to change. | Writes only inside the files it was handed, and opens the result in a browser window to check it. Shared files, such as page lists and site-wide stylesheets, it reports back instead of editing. |
<!-- /generated:whats-inside -->

The first question is whether the thing exists yet. `redesign-existing-projects` is the only one for a site already built; every other skill starts something new. The second question is what you are making: `mobile-taste-frontend` for phone app screens, and the rest for web pages. Among the web page skills, `minimalist-ui` holds one quiet style, `design-taste-frontend` picks a louder one to suit the brief, `image-taste-frontend` shows you pictures before writing code, and `frontend-design` and `emil-design-eng` advise on direction and feel rather than building a whole page.

## What this does on your computer

| | |
| :--- | :--- |
| Files read | The project you are working in. `redesign-existing-projects` reads your existing code to find which framework and styling method it uses.<br>`design-taste-frontend` and `redesign-existing-projects` read your project's `package.json`, the file that lists which packages a project uses.<br>`image-taste-frontend` and `mobile-taste-frontend` read any screenshot or reference picture you hand them.<br>The `frontend-surface-builder` agent reads only the files it was given. |
| Files written | Every skill here writes web code into the project you are working in: HTML, CSS, Tailwind and React.<br>`redesign-existing-projects` edits the files already there rather than adding new ones.<br>`mobile-taste-frontend` produces screen designs and a written specification. By its own rule it does not write app source code, meaning SwiftUI, Jetpack Compose or React Native.<br>The agent writes only inside the file list it was handed. Nothing here writes outside your project. |
| Files deleted or moved | None. |
| Programs and scripts | No programs ship with this pack. It is written instructions only.<br>`design-taste-frontend` and `redesign-existing-projects` print an install command such as `npm install` for you to run when a package is missing. They do not run it themselves.<br>`image-taste-frontend`, `mobile-taste-frontend` and `design-taste-frontend` call an image-generation tool, if your Claude Code has one connected. The first two call it several times in one session. `design-taste-frontend` uses it for a page's pictures before it falls back to placeholder images. For a whole site that can be eight to twelve pictures.<br>The `frontend-surface-builder` agent opens the page it built in a browser window, takes a screenshot and reads the browser's error log. |
| Internet access | No skill here fetches a page. What they do is write code that points at public addresses, which your browser or your build loads later:<br>placeholder photographs from `picsum.photos`, used by `minimalist-ui`, `redesign-existing-projects`, `design-taste-frontend` and `image-taste-frontend` when you have no real picture;<br>company logos from `cdn.simpleicons.org`, used by `design-taste-frontend`;<br>for a Shopify app only, a script from `cdn.shopify.com`, listed by `design-taste-frontend` as standard starting code.<br>`emil-design-eng` prints one link to an outside website as plain text. Nothing here sends your files anywhere. |
| Accounts, keys or passwords | None. No skill here asks for a key or signs in to anything. If you use an image-generation tool with `image-taste-frontend` or `mobile-taste-frontend`, that is a tool you connected yourself; these skills do not set one up and do not handle its sign-in. |

Two limits. First, `emil-design-eng` has a fixed first reply that advertises a paid course at `animations.dev`. That text is part of the skill as it was written. It is printed to you, not visited, and you can ignore it. Second, the `frontend-surface-builder` agent's promise to stay inside its own files is written instruction and nothing more. Its settings place no limit on which tools it can use, so if it does not follow its own text, nothing stops it. Give it a clear file list and check what it changed.

## How the skills work together

They are independent. Each covers a different moment, and you would rarely use more than two on one job.

1. **A site that already exists:** `redesign-existing-projects`. It audits and fixes in place, and it is the only skill here written not to start over.
2. **A new web page, decided in words:** `frontend-design` to settle palette, typefaces and the one memorable element, then `design-taste-frontend` or `minimalist-ui` to build it.
3. **A new web page, decided in pictures:** `image-taste-frontend`. Use this when you want to look at the design before any code exists.
4. **Phone app screens:** `mobile-taste-frontend`. It is for screens, not for web pages, and not for native code.
5. **An interface that already looks right but feels wrong:** `emil-design-eng`, for timing, easing and the small details of how a control responds.
6. **Several parts of one interface at once:** the `frontend-surface-builder` agent, one per part, each with its own list of files.

`design-taste-frontend` and `minimalist-ui` are the pair most often confused. `minimalist-ui` holds one fixed quiet style and does not deviate. `design-taste-frontend` chooses a style to fit the brief, and its choices run louder.

## Install

Inside a running Claude Code session:

```
/plugin marketplace add GFMCloud/skill-library
/plugin install frontend-design@skill-library
```

The first line is only needed once, however many packs you install.

Nothing in this pack needs other software to be installed first. Two skills work best with something you may not have: `image-taste-frontend` and `mobile-taste-frontend` want an image-generation tool connected to Claude Code. `design-taste-frontend` uses one too if it is there, and works without it. Without one they fall back to a reference picture you supply or to a written description, and both still work.

## Back to the main page

[skill-library](../../README.md) lists all the packs and explains the terms used here.
