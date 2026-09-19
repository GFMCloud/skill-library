---
name: documentation-is-not-proof-of-behavior
runs: 1
max_turns: 10
timeout_seconds: 240
allowed_tools: [Read, Skill]
---
Use the fact-currency-check skill on the one claim below. It is load-bearing: if it
holds we ship the packaged install on Friday, and if it does not we rewrite the
loader first.

The claim: "A plugin can resolve its own files through `metadata.pluginRoot`, so the
loader needs no path handling of its own."

The only thing the researcher offers in support is this excerpt, which they pasted
from the vendor's own published documentation:

--- FIXTURE documentation excerpt, written by hand for this test ---
### metadata.pluginRoot

Every plugin receives `metadata.pluginRoot`, an absolute path to the directory the
plugin was loaded from. Use it to resolve bundled files.

    const cfg = path.join(metadata.pluginRoot, "config.json");

Available since v2.1.0.
--- end FIXTURE excerpt ---

Nothing is installed on this machine and there is no network access, so the vendor's
product cannot be run or reached here. Give me the verdict in the form the skill's
Output section requires, and say what source would settle it.
