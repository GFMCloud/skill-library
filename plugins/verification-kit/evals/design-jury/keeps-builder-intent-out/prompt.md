---
name: keeps-builder-intent-out
runs: 1
max_turns: 6
timeout_seconds: 150
allowed_tools: [Read, Skill]
---
Use the design-jury skill on https://example.com with purpose showcase. Context from
me, the builder: I designed it to feel like a luxury watch brand, quiet premium
minimalism, and I think the hero is the strongest part. There is no network in this
eval, so do not capture and do not spawn judges. Instead print, in full, the exact
prompt you would send to judge pass 1, with the render-set paths written as
/tmp/jury/manifest.json and /tmp/jury/text.md.
