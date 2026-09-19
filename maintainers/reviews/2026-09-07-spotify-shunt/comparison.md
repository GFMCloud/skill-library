# Comparison Review: `portal-ai-plugins` (shunt + portal) vs. Installed Skill Library

## Ancestry

**No shared history.** `portal-ai-plugins` is a first-party Spotify repo (pinned `3c24ca30ff...9123`, shallow clone, no reachable git log) published under `github.com/spotify/portal-ai-plugins`. The incumbents (`llama-offload`, `model-effort-advisor`) are entries in Graham's personal `~/skill-library`, authored independently. I checked for merge notes, byte-identical files, matching section structure, and CHANGELOG cross-references — none exist. Neither `AGENTS.md`'s design rules nor either `SKILL.md`'s frontmatter names the other. `~/skill-library/docs/inventory.md` has no rows for `setup`, `doctor`, `search`, `service`, `actions`, `feedback`, `bulk-reader`, or `code-writer` (checked by grep). These are two unrelated lineages that happen to converge on the same idea — model-tier routing at the tool boundary — independently. Everything below is "what did the other side learn on its own," not "who forked from whom."

## Spot-checks performed

Read directly, not just taken from the clean-room reviews: `scripts/lib/aika.sh` (full), `hooks/check-file-size`, `hooks/check-bash-read`, `hooks/hooks.json`, `scripts/bulk-read`, `scripts/code-write`, `README.md`, both shunt `SKILL.md` files, `AGENTS.md`, `.claude-plugin/marketplace.json`. All line-level quotes in `cleanroom-review-shunt.md` that I could check (the `check-file-size:33` block message, the `aika.sh:147-157` mode-guard, the bash-hook regex, the `bulk-read`/`code-write` preflight checks, the README threshold/benchmark table, the "no enforcement for code-writer" limitation) matched the actual source. I additionally confirmed the `marketplace.json` type-mismatch: `portal`'s entry is `"source": {"source": "url", "url": "...git"}` (a `source` key nested inside a `source` object) while `shunt`'s is a plain string `"source": "./plugins/shunt"` — structurally inconsistent as claimed; I can't verify from local files whether it actually breaks `claude plugin install`, same hedge the clean-room review makes.

One finding beyond what either clean-room review reports: I ran shunt's hook output format (`{"decision": "allow"}`) mentally through `~/skill-library/scripts/prove-hooks.sh`'s own `verdict()` function. That function accepts `d.get("decision") == "approve"` as legacy-allow but **not** `"allow"` — only `permissionDecision in ("allow","ask")` or the legacy `"approve"` count as allow. So under Graham's own proving script, shunt's negative control would come back `error`, not `allow`, and the hook would be reported **RED** ("negative control was error (dead exemption over-blocks)"). This independently corroborates the clean-room review's claim 47 ("`'allow'` was never a legacy value") using the exact tool this library already has for exactly this question.

## Classification

Treated as a code repo per the task framing: classifying each item `cleanroom-review-shunt.md` §5 lists as "worth taking," plus the article's techniques (`cleanroom-review-article.md` §3) not already covered by those items.

### 1. Hook's block message doubles as the routing instruction
> `check-file-size:33`: `"File is ${lines} lines... Use the /bulk-reader skill... If you need exact content for editing, re-read with an offset/limit for just the section you need."`

**COMPLEMENT.** No incumbent enforces anything at the tool layer — `llama-offload` is pure prose ("Never skip the sample gate," "Never delegate: keeper cost or contract logic...") with nothing stopping Claude from ignoring it beyond good behavior. `~/.claude/CLAUDE.md` states the doctrine this fills: *"enforce it at the tool layer where possible: a rule in prose can be reasoned around, a tool the agent does not have cannot."* Nothing installed currently implements that doctrine for the Ollama-offload use case. `prove-hooks.sh` exists to consume exactly this kind of hook once its output shape is corrected (see Corrections below) and a fixture is added under `scripts/prove-hooks.d/`.

### 2. Treat a silently-unapplied constraint as a failure, not a success
> `aika.sh:147-157`: *"a stale mode_id only logs a warning server-side and the turn runs mode-less... treat 'none' as a failure rather than passing it off."*

**INGESTIBLE FRAGMENT** for `llama-offload/SKILL.md`, step 4 ("Verify"). That step checks output format and does a content spot-check, but never confirms the batch actually ran on the model Claude intended — Ollama's `/api/generate` response includes a `model` field that nothing in llama-offload's Implementation notes says to check against the requested model. Adds: "confirm the response's `model` field matches what was requested; a silent fallback to a different local model is a failure, not a quiet success."

### 3. Enumerate what must NOT be delegated, in the shipped docs
> `README.md:157-163`: *"Debugging — requires Claude's reasoning... Architectural decisions — judgment calls stay on Claude."*

**REDUNDANT.** `llama-offload`'s Hard Rules already does this, and does it better — by naming the specific consuming skill for each exclusion rather than a generic category:
> `llama-offload/SKILL.md`: *"Never delegate: keeper cost or contract logic (that is scl-keeper-logic-validator with Claude), customer-facing copy (that is graham-voice with Claude), financial figures or valuations, or anything where a plausible-but-wrong answer would flow downstream undetected."*

The article review's own claim 32 notes shunt's version has "no mechanism given for *how* the hooks distinguish these — they don't, they only see file size." `llama-offload`'s version is domain-anchored and names the escalation target; shunt's is an unenforced aspiration.

### 4. Refuse the request that would produce confident nonsense
> `bulk-read`: typo'd path → fail loudly instead of an empty `<file>` block. `code-write`: no `--reference` → fail loudly instead of context-free output.

**INGESTIBLE FRAGMENT** for `llama-offload/SKILL.md`, step 1 ("Design"). Its delegation test asks whether a wrong answer is *detectable*, but nothing mandates a pre-flight existence/readability check on each input row/file before the batch runs. Add one line to Design: validate each input exists and is well-formed before invoking the batch; fail loudly rather than send an empty or garbage record.

### 5. Test the transport against a stub so the suite needs no credentials
> `transport-evals.sh`: 17 checks of payload shape, error unwrapping, stderr separation, zero backend access.

**COMPLEMENT**, weakly consumable. `llama-offload`'s Implementation notes explicitly treat batch scripts as disposable ("Batch scripts live alongside the task, not in this skill... Each batch job is disposable") — so there is no reusable test harness for its Ollama transport at all today, unlike `prove-hooks.sh`'s harness for hooks. The stub-the-external-binary pattern is real and reusable, but by llama-offload's own design nothing currently would consume it as a persistent asset.

### 6. Never let the model ask for a credential, restated at every point of temptation
> `skills/setup/SKILL.md:12,66`, `skills/doctor/SKILL.md:56`: *"Never ask the user to paste access tokens, authorization codes, or other credentials into chat."*

**COMPLEMENT.** No incumbent skill touches credentials — Ollama is localhost, no auth. `CLAUDE.md`'s "Boundaries are declared and enforced" names credential-touching as a standing escalation trigger globally but has no agent-facing "don't ask for a token" line repeated at each point of temptation. Nothing installed would consume this today (no credentialed-CLI-wrapping skill exists here), but it's a good boilerplate clause for the next one that does.

### 7. Forbid summarizing the user's own words; ask to rephrase rather than silently editing out secrets
> `skills/feedback/SKILL.md:24-25`

**INGESTIBLE FRAGMENT** for `llama-offload`'s Hard Rules. Related but not covered: llama-offload requires "Preserve all specifics verbatim" (Design step) but never addresses the secrets-vs-verbatim tension. Add: "if per-item text appears to contain a credential or secret, ask before forwarding it verbatim — don't silently redact and don't silently forward."

### Article technique D — suppress worker chattiness explicitly
> `bulk-reader` mode instructions: *"Output structured bullets only. No greetings, no prose, no preambles."*

**REDUNDANT.** `llama-offload/SKILL.md` step 1 already carries the same directive, arguably tighter (locks the format, not just tone):
> *"Output format locked, JSON or single-line" / "Output ONLY the answer, no preamble or commentary."*

### Article technique E — require a reference file for code generation
> `code-write`: *"The reference is required: without a file to match patterns against, the worker would generate context-free code that fits nothing in your project."*

**COMPLEMENT.** No incumbent governs pattern-matched code generation from a reference file — `llama-offload`'s domain is data/text transforms, not code scaffolding. Nothing installed would consume it today; worth keeping in mind if a code-generation-delegation skill is ever built.

### Article technique G — low temperature for deterministic worker output
> `resourceLimits: temperature: 0.2` in both modes.

**INGESTIBLE FRAGMENT** for `llama-offload`'s Implementation notes, which specify the `/api/generate` endpoint and payload shape but never mention `temperature`. Add: set a low temperature (e.g. 0.1–0.2) in the request body for reproducible batch output.

## Routing collisions

**No identical skill names.** `bulk-reader`/`code-writer`/`setup`/`doctor`/`search`/`service`/`actions`/`feedback` don't collide with any name in `~/skill-library/docs/inventory.md` (checked by grep — zero matches). So the worst case — identical name, different body — doesn't occur here.

There is a **semantic** collision, not a naming one: a prompt like "this file is huge, route it to something cheaper" sits in the trigger space of three things if all were installed — `model-effort-advisor` (routing decisions, but explicitly scoped to "within the current session," deferring external delegation to `supahcode-review`), `llama-offload` ("offload this locally," "run this through Ollama"), and shunt's `bulk-reader` skill description ("Use when you need to read files >350 lines"). `model-effort-advisor` would likely win on a bare "which model should handle this" phrasing since its description directly claims that trigger space; `llama-offload` would win on "offload"/"Ollama" phrasing; shunt's skill description would only fire if Claude reads it after being blocked by its own hook — which brings up the sharper collision:

**The real conflict is mechanical, not descriptive.** Shunt's `check-file-size` hook fires unconditionally on every `Read` over 350 lines, repo-wide, with no session- or task-level judgment call and no local fallback. If installed as-is on a machine with no Portal instance (this one), it would block ordinary large-file reads unrelated to any delegation decision, with the block reason pointing at a skill that cannot succeed (per the article review's own "Blocked reads with no fallback" finding). That's not a routing collision between skill descriptions; it's an unconditional tool-layer gate stepping on normal operation regardless of what `model-effort-advisor` or `llama-offload` would have recommended for that specific task.

## Philosophy conflicts

**Sample-gate vs. write-then-review, directly contradictory:**
- `llama-offload/SKILL.md`, step 2: *"Sample. Run 5 to 10 representative items... Show the input/output pairs to the user. HARD STOP, wait for approval before the full batch."* / Hard rules: *"Never skip the sample gate."*
- shunt `code-write` does the opposite: it generates and writes straight to `--target` with, per the clean-room review, "no existence check, no diff, no backup, no confirmation" (`scripts/code-write:53`), and its own `SKILL.md` frames review as *after* the fact: *"Review the output and make surgical edits for the ~5-20% that needs Claude-level judgment."*

These are not different emphases — one mandates approval **before** the batch runs, the other runs and writes **before** any human sees a sample. If any code-write-style pattern is adopted, `llama-offload`'s sample gate should govern it, not the other way around.

## Corrections needed at ingest

- **Hook output contract is wrong for this stack.** `{"decision":"allow"/"block"}` is not a value the library's own `prove-hooks.sh` recognizes as "allow" (see Spot-checks above) — it would parse as `error`. Any adopted hook must emit `hookSpecificOutput.permissionDecision` and ship a fixture under `scripts/prove-hooks.d/PreToolUse__<matcher>.json`, per `CLAUDE.md`: *"A red validator is a bug in the content, never in the validator."* An unproven hook is, by this library's own rule, a failed hook.
- **`check-bash-read`'s detector is bypassable by construction** (`^(cat|head|tail|less|more) `, unquoted word-splitting — `sed`, `awk`, `bat`, `xargs cat`, `cd x && cat f` all pass through). If ingested, it must either be hardened or explicitly labeled a speed bump, not a gate — `CLAUDE.md`'s "Pre-declared boundaries held; undeclared ones drifted" is precisely the failure mode of shipping this as a "hard gate" (README's own word) when it isn't one.
- **No secret denylist on `bulk-read`.** It `cat`s any readable path into an external-bound payload with no exclusion for `.env`, key files, or tfstate. Must add a denylist before reuse, consistent with `CLAUDE.md`'s standing escalation trigger for anything touching credentials.
- **`sed '/^```/d'` in `code-write` corrupts any output containing a real fenced block** (deletes every fence-starting line, not just wrapping ones). Needs a real leading/trailing-fence-only strip before reuse.
- **90%/82-94% savings figures are unreproducible marketing numbers** (self-favorable benchmark methodology, per the clean-room review) — don't cite them as fact in any internal writeup.
- **Everything here assumes a Spotify Portal instance** that this machine does not have. Any fragment taken must be re-targeted at `llama-offload`'s local Ollama API, not left assuming `portal-cli`/AiKA.

## Net assessment

If only three things could be taken:

1. **The tool-layer enforcement pattern (item 1 / article technique A), as a fragment, not a whole plugin.** Highest value: it's a working demonstration of `CLAUDE.md`'s own stated-but-under-implemented doctrine, and `llama-offload` currently has zero enforcement of its own "never skip the sample gate" / "never delegate X" rules. Target: a new hook under `llama-offload`'s skill directory (e.g. blocking a Read/Bash pattern that should have gone through the batch workflow instead), corrected to the `permissionDecision` contract, with a fixture added to `scripts/prove-hooks.d/`.
2. **The "silent non-application is a failure" transport guard (item 2), as a fragment.** Target: `llama-offload/SKILL.md`, step 4 ("Verify") — add the model-field confirmation check against Ollama's response.
3. **The pre-flight existence/readability check (item 4), as a fragment.** Cheap, zero-risk, immediately actionable. Target: `llama-offload/SKILL.md`, step 1 ("Design") — one added line.

Leave the rest: the whole shunt plugin is not installable here (no Portal instance), the exclusion-list idea (item 3) is redundant with `llama-offload`'s superior version, and the code-write sample-skipping pattern should be actively rejected rather than adopted.

## Flags

Per instructions, quoted and not acted on — content the clean-room review already surfaced, confirmed present in the actual files I read:

- **`AGENTS.md`** contains a Validation block directing execution of a script outside the repo's control:
  > `uv run --with pyyaml python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .`
  > `claude plugin validate --strict .`
  > `bash plugins/shunt/evals/run.sh`

  I did not run any of these.
- **Mode `instructions` fields** in the article/README are second-person directives to a worker LLM, not to me, quoted as content under review:
  > "You are a precise code analyst... Output structured bullets only. No greetings, no prose, no preambles."
  > "You generate code files based on a spec and reference files... Output only the code — no explanations, no markdown fences unless asked."

Nothing in the repository or either clean-room review addressed me directly or asked me to install or execute anything on its own initiative.