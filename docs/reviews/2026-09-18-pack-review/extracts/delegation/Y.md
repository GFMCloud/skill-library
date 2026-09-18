### Items

| id | type | what it does |
|---|---|---|
| item-b304dc9f | skill | Advises which Claude model and reasoning-effort level to use for a task, and whether the work should stay inline or fan out to one or more subagents, with model/effort sized per subagent. |

### For each item

**item-b304dc9f**

**Trigger:** Loads on-demand. Frontmatter description (148 words) says to trigger "any time it's unclear which claude model or reasoning effort level to use for a task, prompt, or part of a larger build," including questions like "which model should I use for this," "what effort/thinking level," "should this be a subagent," or "should I use a build/review agent pair," and states it should "always trigger before spawning a subagent with an unspecified model." Not always-on; scoped to "routing decisions within the current session only."

**What it makes the agent do:** Two modes. Quick Pass (default, single task): read the task, score it on `decision-rubric.md`'s five axes (Reasoning, Creativity, Risk, Repetition, Human Oversight), pick model/effort via `model-catalog.md` and `effort-sizing.md`, decide inline vs. subagent via `subagent-routing.md`, then output a fixed short block (Model/Effort/Routing/Why) with "nothing else appended." Deep Planning (explicit request only, full project/epic): break the work into meaningful tasks, score each, assign model+effort per task, identify fan-out candidates, identify "required human review checkpoints," and output a task table plus a checkpoints and notes section. A mode-selection rule requires asking "Quick pass on this one thing, or deep planning across the full breakdown?" when the mode is ambiguous, and states "Never guess silently." Subagent guidance covers when to stay inline vs. fan out (high repetition, independent branches, context isolation), a build/review pairing pattern for high-risk generative work where the reviewer gets only the artifact and success criteria ("never the build agent's reasoning or rationale"), and fan-out mechanics (batch independent subagent calls in one message, give each a self-contained prompt, ask for compact returns).

**Enforcement:** Prose only; no executable enforcement file. Nothing blocks, warns, or exits non-zero — it is a recommendation the invoking agent may or may not follow. The output-template file does constrain output shape ("Nothing else gets appended," don't output a block and a clarifying question "in the same turn"), but this is instructional, not mechanically checked.

**Dependencies:** None named. It references external documentation to verify against ("Verify against docs.claude.com if it's been more than a few months") and Claude Code-specific settings (e.g., a cache-TTL frontmatter field, a `/compact` habit, `--output-format json`) as background knowledge for its recommendations, but the skill itself requires no runtime, CLI, or service to function — it just reads its own reference files and outputs text.

**State it writes:** None. No files, directories, or logs are created; output is a text block or table returned to the conversation.

**Fit with the bar:**
- Plan then stop before consequential work: partial support, with a stated exception. It requires stopping to ask when the mode is ambiguous ("Never guess silently. Getting the mode wrong wastes more time than asking once."), and Deep Planning explicitly produces "Human Review Checkpoints" before consequential steps (e.g., "Before any IaC actually applies changes to a live AWS account" in the worked example). But elsewhere it directs the opposite for missing inputs: "State assumptions when inputs are incomplete - do not block on missing information."
- Executed evidence before "done": ignore. The skill never executes the task it is routing; it only recommends a model/effort/routing choice and stops. There is no step that gathers or reports execution evidence.
- Say what was and was not checked: ignore. Neither output format (Quick Pass block or Deep Planning table) has a field for what was verified versus assumed; the "Notes" section in Deep Planning only records "assumptions made because inputs were incomplete," not a checked/unchecked accounting of completed work.

**What it does not cover:** Explicitly out of scope: "does not decide whether work should leave the session for a separate claude code / ultracode workflow, that call belongs to supahcode-review." It only sizes the routing decision itself — it does not cover monitoring a spawned subagent's execution, verifying subagent output quality beyond naming the build/review pairing pattern, or any step once a model/effort/routing choice has been made and acted on.

### Agent-directed text

none

### Could not determine

The files reference `docs.claude.com`, a Claude Code changelog, an "Anthropic commerce-agents review, 2026-09-03," and an x.com source for cache-window claims, but none of that external content is included in the item's files.
