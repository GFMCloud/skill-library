---
name: no-inter-no-lucide-in-the-type-stack
runs: 1
max_turns: 12
timeout_seconds: 240
allowed_tools: [Read, Write, Skill]
---
Use the minimalist-ui skill. Build the type layer for the marketing page of
Ledgerlane, a FIXTURE invoicing tool for freelance translators. Do not ask me
anything, just build it.

Write a single stylesheet `type.css` in the current directory that defines, as CSS
custom properties on `:root` and then applies them:

1. the body and UI sans-serif stack
2. the hero heading serif stack, with its tracking and line-height
3. the monospace stack for keyboard shortcuts and metadata
4. the body text color and the secondary text color

Then in your reply, paste the four font-family declarations and the two text
colors exactly as they appear in the file, and name the icon set you would use
for the nav icons.
