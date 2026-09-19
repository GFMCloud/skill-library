# Headroom vs. installed skill library — comparison

Candidate: `/private/tmp/claude-501/-Users-gfm-work/c88c0612-6d03-448d-b8c2-c8bf34bf9507/scratchpad/headroom`, pinned `e67b3c8a29443a60d6b0018fb22f525c5cd7e709` (HEAD; latest commit `feat(vertex): add Gemini 3.8 Flash agent benchmark suite (#3371)`, 2026-09-05).
Second opinion: `/private/tmp/claude-501/-Users-gfm-work/c88c0612-6d03-448d-b8c2-c8bf34bf9507/scratchpad/cleanroom-review.md`.

## Ancestry

**None found.** Checked:

- `grep -ril "skill-library\|gfmcloud\|graham" .` (all `.py`/`.md`/`.json` in the headroom clone) — zero hits.
- `.changelog.md` / `CHANGELOG.md` for `skill-library` or `gfmcloud` — zero hits.
- No `SKILL.md` file anywhere in the candidate (`find . -iname "SKILL.md"` — empty), so there is no candidate file that could be byte-identical to an incumbent SKILL.md.
- No shared filenames, section structure, or CHANGELOG cross-reference between headroom and any of the seven incumbents. Headroom is a Python/Rust package (library + proxy + MCP server + CLI); the incumbents are markdown skill definitions. Independent projects, independent structure.

## The cleanroom review's evidence, spot-checked

I re-verified every quote the cleanroom review attributes to section 5, plus the maturity/claimed-vs-verified claims that bear on classification, by opening the cited files directly:

- `headroom/cache/prefix_tracker.py:6-14` — quote matches verbatim (read lines 1-160).
- `headroom/telemetry/beacon.py:18-20, 52-55` — quote matches verbatim; also confirmed `BEACON_DEFAULT_ON = True` (line 56 in the review's citation; actual line in the file I read is the `BEACON_DEFAULT_ON = True` assignment following the docstring) and the fail-open language.
- `headroom/transforms/smart_crusher.py:36-40` — quote matches verbatim (read lines 1-60).
- `benchmarks/index_proof_table.py:8-10` — quote matches verbatim (read lines 1-40).
- `headroom/telemetry/session.py:668-674` — quote matches verbatim (read lines 590-680); the transform-name truncation and its stated rationale ("would put the model tier and a request-size bucket on the wire") are exactly as claimed.
- `llms.txt:67` ("off by default (opt-in)") vs `README.md:592` ("on by default") vs `beacon.py`'s `BEACON_DEFAULT_ON = True` — all three read exactly as the cleanroom review states; the contradiction is real, not a misreading.
- `SECURITY.md:7,60` — "0.27.x (latest)" and "No credential storage" both read as quoted.
- `headroom/copilot_auth.py` — `save_headroom_copilot_oauth_token()` exists and writes an OAuth refresh token to disk (confirmed at the function definition around line 626 in the review's numbering; I read the surrounding block and confirmed the write path and shape, though I did not independently re-verify the exact `chmod 0o600` claim byte-for-byte).
- Git log: unlike the reviewer (who reported `git log` blocked in their sandbox), I had a working `git` in this session and confirmed HEAD is the pinned commit and the ~30-commit visible history (`fix(compression)`, `fix(proxy)`, `feat(cache)`, `docs(readme)` etc.) is consistent with the reviewer's file-based inference (shallow clone, active project, recent commits days before the snapshot date).

I did not re-run the benchmark script, re-derive the 810/1012 test counts, or re-verify the 21-release CHANGELOG count; I take those on the reviewer's word as lower-stakes claims not load-bearing for the classification below.

Additionally, for the "installable tool" and "routing collisions" analysis I read parts the cleanroom review did not quote:

- `headroom/learn/writer.py` (full, 441 lines) — the `ClaudeCodeWriter`, its default target (`CLAUDE.local.md`, not `CLAUDE.md`), and its `_migrate_legacy_block` logic.
- `headroom/learn/analyzer.py` (full, 951 lines) — the single-LLM-call pipeline, digest builder, CLI-backend fallback (including shelling out to `claude -p` itself), and system prompt.
- `headroom/cli/wrap.py` (targeted greps + reads around lines 860-930, 1020-1070, 1180-1220, 1580-1670, 1780-1870, 1950-2130, 2550-2560, 4670-4680, 5170-5590) — confirmed it reads/writes `~/.claude/settings.json`, `~/.claude.json`, `.claude/settings.local.json`, `~/.serena/serena_config.yml`, `~/.codex`, `~/.config/opencode`.
- `.claude-plugin/marketplace.json` and `plugins/headroom-agent-hooks/hooks/hooks.json` / `.claude-plugin/plugin.json` — confirms Headroom ships an installable Claude Code plugin with `SessionStart` and `PreToolUse` hooks that shell out to `headroom init hook ensure`.
- `headroom/cli/learn.py` (targeted greps) — confirmed `headroom learn` defaults to dry-run and only writes with an explicit `--apply` flag.

## Classification

### (a) The seven ideas from cleanroom review §5

**1. "Freeze what the provider already cached; compress only the delta"** (`headroom/cache/prefix_tracker.py:6-14`)

**COMPLEMENT.** No incumbent skill does prompt-cache-aware compression, or touches provider cache economics at all. `workbench:handoff` is the nearest neighbor (context getting long → summarize into a new session) but it is a full-context reset, not incremental cache-preserving compression — a categorically different response to the same underlying problem (context growth). Nothing installed on this machine would consume this idea: it requires a proxy sitting between the agent and the provider API, and none of the incumbents run in that position. Gap: an installed skill library has no mechanism at all for cache-aware token economics; it only has "restart with a fresh session" (`handoff`) and "route bulk work off-model" (`llama-offload`), neither of which addresses live single-session cache economics.

**2. "Separate 'collect locally' from 'upload' as two switches, and say why"** (`headroom/telemetry/beacon.py:18-20`)

**INGESTIBLE FRAGMENT.** No incumbent states this rule. The global `/Users/gfm/.claude/CLAUDE.md` has adjacent material — "Secrets live in `.env` or a keychain… secret-scan before every commit" and "Standing escalation triggers… touching credentials or production" — but nothing about telemetry/data-egress switch design specifically. Fragment to take: the design principle "an operator who turned on local stats has not thereby agreed to upload anything, and must not start doing so on upgrade" — worth a one-line addition to the global CLAUDE.md's "Credentials and secrets" section, since this machine already runs several tools with local-state-vs-network-egress distinctions (the beacon in `source-intake`, `claude-scout-weekly`'s "propose-only until ruled" status). Target file: `/Users/gfm/.claude/CLAUDE.md`, "Credentials and secrets" section — a new short bullet, not a whole new section (per "CLAUDE.md economy": "Write a project fact down only once it has cost a correction twice" — this has not yet cost a correction on this machine, so it is a candidate, not an automatic add).

**3. "Make a default policy one auditable line"** (`headroom/telemetry/beacon.py:52-55`)

**INGESTIBLE FRAGMENT**, adjacent to but not redundant with an existing rule. Compare:
> Headroom: *"This single constant is the whole policy — deliberately, so the decision is one line to audit and one line to reverse."*
> `/Users/gfm/.claude/CLAUDE.md`, "Boundaries are declared and enforced": *"Name the boundary before the work starts, and enforce it at the tool layer where possible: a rule in prose can be reasoned around, a tool the agent does not have cannot."*

These are siblings, not duplicates — the CLAUDE.md rule is about *where* a boundary is enforced (tool layer vs. prose); Headroom's is about *how a default is expressed in code* (a single named constant, not a scattered set of conditionals) so it can be audited and reversed in one place. Worth taking as a fragment appended to the same "Boundaries are declared and enforced" section, not a new section.

**4. "A comparison key must never become a source for rebuilt bytes"** (`headroom/cache/prefix_tracker.py:146-149`)

**COMPLEMENT**, narrow. No incumbent addresses this; it is a specific safety property for systems that compare a normalized/stripped view of data for equality while forwarding the original bytes elsewhere. Nothing installed currently builds or maintains such a system, so nothing here would consume it today — flagged as a good idea to remember rather than something to file anywhere right now.

**5. "Refuse to silently ignore a user-supplied override"** (`headroom/transforms/smart_crusher.py:36-40`)

**INGESTIBLE FRAGMENT.** No incumbent states this as a rule, though it rhymes with two existing ones: `/Users/gfm/.claude/CLAUDE.md`'s "A red validator is a bug in the content, never in the validator" (fail loud, don't quietly work around) and the `rulings-harness` doctrine of falsifiability. But neither says "when a caller supplies a parameter your current code path can't honor, raise, don't drop." Fragment worth taking: *"Silently dropping a user-supplied [X] is a silent-fallback bug we explicitly refuse to ship"* as a general coding-discipline addition, e.g. under "Surgical edits" in the global CLAUDE.md, phrased generically (not tied to "scorer").

**6. "An unreproducible number on your landing page is a liability, not evidence"** (`benchmarks/index_proof_table.py:8-10`)

**REDUNDANT.** `foundry-core:proof-of-work` and `foundry-core:evidence-report` already cover this, and arguably state it more operationally:
> Headroom: *"A number on the front page of the docs that nobody can regenerate is a liability, not evidence."*
> `proof-of-work` SKILL.md: *"State what was run, against what input, and what came back. All three. A result with no input named is not reproducible."*
> `evidence-report` SKILL.md: *"CHECK — the command or action, verbatim and re-runnable. Not 'validated the manifest.'"*

The incumbents go further than Headroom's one-line principle: they specify the exact fields a reproducible claim must carry (CLAIM/CHECK/OUTPUT/VERDICT) and mandate a NOT VERIFIED list, which Headroom's benchmark script doesn't formalize as a general practice — it just fixed one specific script. Nothing to take; the principle is already installed and more thoroughly operationalized.

**7. "Truncate telemetry labels at the format boundary, not the value"** (`headroom/telemetry/session.py:668-674`)

**COMPLEMENT**, narrow and low-priority. No incumbent touches telemetry field design. Nothing installed currently emits telemetry labels in a format this technique would apply to, so it is a fact worth knowing, not an action item.

### (b) `headroom learn` as a mechanism

**INGESTIBLE FRAGMENTS**, not a wholesale substitute. `headroom learn` (via `headroom/learn/{scanner,analyzer,writer}.py`) and the installed trio of `workbench:retro` + `workbench:skill-discovery` + `workbench:transcript-scanner` both mine session history for durable lessons, but they differ enough in philosophy that neither replaces the other:

| Dimension | `headroom learn` | Installed (`retro`) |
|---|---|---|
| Extraction | One LLM call over a text digest of tool calls/failures/loops (`analyzer.py:_build_digest`, `_call_llm`) | Dedicated `transcript-scanner` subagent, bounded-slice discipline, `path:line` provenance mandatory |
| Write path | Direct write to CLAUDE.local.md/MEMORY.md/AGENTS.md/GEMINI.md/GROK.md on `--apply` (dry-run is the default; confirmed in `headroom/cli/learn.py:75,322,341-342`) | **Never writes** to CLAUDE.md/memory itself — "This skill proposes destinations… the session (or user) acts on the proposal" |
| Routing granularity | 2 buckets: CONTEXT_FILE (stable project facts) vs MEMORY_FILE (evolving preferences) | 6-way table: memory (feedback) / project CLAUDE.md / decisions/ ADR / hook-or-CI / eval case / one-off-discard |
| Update semantics | Marker-delimited section, LLM told to re-emit a section wholesale to replace it, unlisted prior sections auto-carried-forward (`writer.py:_merge_recommendations`) | One file per session (`.claude/retros/YYYY-MM-DD-<slug>.md`); retro explicitly says no cross-session synthesis/promotion exists yet ("only `/retro` is built") |
| Cross-agent support | Codex/Gemini/Grok/opencode writers exist | Claude Code only |

Fragment worth taking, quoted and cited:

- **The marker-block merge-and-carry-forward mechanism** (`headroom/learn/writer.py:89-193`, `_MARKER_START`/`_MARKER_END`, `_merge_recommendations`): *"Sections produced by the current run take precedence over same-named prior sections… Prior sections whose headings do not reappear in the new run are carried forward so a re-run doesn't silently drop accumulated learnings."* This is exactly the gap `retro` names as unbuilt in its own §6: *"No weekly review, no cross-session synthesis, no promotion automation… Run this against real sessions first, build the review once a corpus of retros exists to review."* Headroom's idempotent-merge technique (not the LLM call, not the direct-write default) is a usable pattern for the eventual `/retro-review` retro's own design defers to later. Target: `~/skill-library/plugins/workbench/skills/retro/SKILL.md` §6, as a design note for the future weekly-review piece — not code to import, since it would need to be re-implemented against retro's file-per-session model rather than a single merged block.
- **The legacy-block auto-migration technique** (`headroom/learn/writer.py:287-336`, `_migrate_legacy_block`): moving accumulated content out of a team-shared file into a personal one, with a warning and a `.gitignore` hint, rather than either leaving stale content in the shared file or silently dropping it. This is a genuinely well-thought-out migration pattern (`"CLAUDE.md is team-shared, so personal learnings now live in {target_path.name}"`) that has no analog in `retro`'s design and is worth remembering if the skill library ever needs to migrate accumulated content between files.

The mechanism as a whole is not a **superior substitute** for `retro`+`transcript-scanner` because it trades away exactly what this machine's working agreements insist on: "Own the loop… run the check yourself" and evidence-per-claim (`path:line` provenance in `transcript-scanner`'s output contract) for a single opaque LLM call whose reasoning is not inspectable, and it can write directly to CLAUDE.md-equivalents on `--apply` with no per-lesson human routing decision — retro's core design choice ("this skill proposes… it does not edit memory, CLAUDE.md, or a decisions folder itself") is a direct rejection of that automation model, not an oversight.

### (c) Headroom as an installable tool (`headroom wrap claude`) for this Claude Code / macOS setup

**DISCARD**, for this user, at this time. Headroom's core value proposition (compress tokens sent to the provider, save on cache-invalidation costs) targets a different bottleneck than the ones this machine's incumbents optimize for. The installed approach to token/cost economy is: `llama-offload` (route bulk mechanical work off-model entirely), `model-effort-advisor` (route work to the cheapest sufficient Claude model/effort), and `handoff` (reset context rather than compress it). None of these need a standing local proxy, a Rust toolchain, ~1,182 resolved Python packages (`[all]` extras), or a beacon-on-by-default background service. Headroom would add: cache-aware compression and cross-agent memory writers, real capabilities, but at an adoption cost the cleanroom review itself scores 2/5, and for a single-operator dev machine (not a team running many agents burning real API-key budget) the savings Headroom targets (per-request cache economics at scale) are not the bottleneck this user's working agreements are optimizing for — those agreements are about *evidence and auditability of agent behavior*, not raw token cost. If Graham later runs high-volume, high-cost agent workloads where cache economics matter, this verdict should be revisited; it is not evaluated as permanently irrelevant, only irrelevant to the current, evidenced use pattern.

## Routing collisions

If `headroom wrap claude` / its hooks / `headroom learn --apply` were installed alongside the incumbents, concretely:

1. **`~/.claude/settings.json`** — `headroom wrap claude` writes `ANTHROPIC_BASE_URL` and `ENABLE_TOOL_SEARCH` env keys and a `PreToolUse`/`SessionStart` hook entry marked by the string `headroom-init-claude` (`headroom/cli/wrap.py:1020-1070`, `_remove_claude_managed_hooks`, `_HEADROOM_HOOK_MARKERS`, `_HEADROOM_ENV_KEYS`). This is the same file the `update-config` skill and any user-authored hooks live in. Headroom claims to only touch entries matching its own marker on `unwrap`, and says "unrelated settings and user-authored hooks are left untouched" — but this is Headroom's own claim about its own code, not independently verified here; a collision risk exists if the marker-matching logic has edge cases (e.g., a hook that legitimately contains the substring `headroom-init-claude` for unrelated reasons, however unlikely).
2. **`~/.claude.json`** — `wrap.py` explicitly documents a race: rewriting this file "would race Claude Code's own writer," and Headroom special-cases its `selfheal` subcommand to skip a cleanup step specifically for this reason (`wrap.py`, `_should_purge_context_tools` docstring). Any Claude Code session actively running while `headroom wrap`/`unwrap` touches this file is a collision surface Headroom itself acknowledges but does not fully solve — it dodges the race in one code path, not universally.
3. **`.claude/settings.local.json`** (project-local, not global) — Headroom writes `ANTHROPIC_BASE_URL` here per-project and installs a project-scoped self-heal `SessionStart` hook marked `headroom-wrap-selfheal` (`wrap.py:1589-1789`). This is the file the global CLAUDE.md's "Standing defaults" (build/verify without asking) and any project's own settings coexist in. A project that also uses `update-config`-managed hooks would need Headroom's marker-based removal to correctly distinguish its own entries — again, unverified beyond reading Headroom's own code.
4. **`CLAUDE.local.md`** — this is exactly where `ClaudeCodeWriter` in `headroom/learn/writer.py` writes by default (not `CLAUDE.md`), specifically to avoid polluting the team-shared file (issue #1072 cited in the docstring). This file is not currently used by any incumbent skill inventoried here (`retro` writes to `.claude/retros/`, not `CLAUDE.local.md`), so there is no direct file collision today — but if `retro` or a future promotion mechanism ever starts writing to `CLAUDE.local.md`, the two would silently interleave content under the same `<!-- headroom:learn:start -->`/`<!-- headroom:learn:end -->` markers Headroom owns, and a non-Headroom writer touching the same markers would corrupt Headroom's merge logic (and vice versa if Headroom ever ran against a file another tool marker-manages).
5. **`~/.claude/CLAUDE.md`** (global) — `ClaudeCodeWriter._resolve_context_path` writes here specifically when `project.project_path == Path.home()`, i.e., when `headroom learn` is run with the home directory as the "project." This is the exact same file this task treats as an incumbent. A `headroom learn --apply` run against `~` would insert a `<!-- headroom:learn:start -->` marker block directly into the global working-agreements file this user has spent real effort consolidating from every project CLAUDE.md ("Consolidated 2026-08-12 from every project CLAUDE.md on this machine"). Given that file's own rule — "Every rule, skill, and document has exactly one editable home… an editable duplicate is drift" — an LLM-authored, auto-merged block living inside that file would itself become a second, machine-written editable surface inside the single-home file, which the file's own governing principle argues against.
6. **Skill/plugin descriptions that would misroute** — Headroom ships **no `SKILL.md` files** (confirmed: empty `find . -iname SKILL.md`), so there is no direct skill-description collision with any incumbent's `description:` frontmatter. It does ship a Claude Code **plugin** (`.claude-plugin/marketplace.json`, `plugins/headroom-agent-hooks/`) with `SessionStart`/`PreToolUse` hooks that shell out to `headroom init hook ensure` on every Bash/PowerShell tool call — a standing per-call overhead that would run alongside every other installed hook, unconditionally, for every tool call matching `Bash|PowerShell`, regardless of whether Headroom's proxy is in use that session.

## Philosophy conflicts

These are contradictions, not differences of emphasis:

1. **Telemetry / data egress.** Global CLAUDE.md, "Credentials and secrets": *"Secrets live in `.env` or a keychain, never in a committed file, never in state files, notes, or logs."* This is about secrets specifically, but the broader working-agreement culture (see `claude-scout-weekly`'s memory note: *"propose-only until Q-2026-09-03-1 ruled"*, and `source-intake`'s repeated emphasis on clean-room isolation) treats any outbound data flow as something to gate explicitly before it happens by default. Headroom's own beacon: *"An anonymous beacon is on by default"* (`README.md:592`) with `BEACON_DEFAULT_ON = True` as the literal code default. Headroom's position — opt-out telemetry is fine because the payload is content-free — is a direct, stated disagreement with a default-off-until-decided posture. Neither side is "wrong" in the abstract (Headroom's payload genuinely appears content-free per my read of `session.py`), but installing `headroom wrap` means accepting an upload-by-default tool on a machine whose explicit working culture is "propose-only until ruled" for outward data flow. This needs a decision, not a silent install.

2. **Credentials, "we never store."** Global CLAUDE.md: *"Never handle raw credentials: not reading them, not writing them, not echoing them back."* `headroom/copilot_auth.py`'s `save_headroom_copilot_oauth_token()` writes a GitHub Copilot OAuth refresh token to disk on the user's behalf as part of normal operation (this is Headroom managing its *own* auth flow for a provider it proxies to, not Claude/this session handling credentials — a materially different situation from this session handling Graham's credentials directly). Still, if `headroom wrap` is installed, the tool now holds a standing credential store outside `.env`/keychain, on the local filesystem, which is exactly the storage location the global CLAUDE.md's rule is written to prevent ("Secrets live in `.env` or a keychain, never in a committed file, never in state files"). `Copilot_auth`'s file is a state file storing a secret. Headroom's own `SECURITY.md` claims "No credential storage," which the code contradicts — a second-order problem: adopting Headroom would mean trusting a security doc that is already wrong about its own product on this exact point.

3. **"Edit the generator, never the output."** Global CLAUDE.md: *"Generated artifacts… are changed only through their generator… Hand-edits to generated output are lost on the next regeneration and drift from source."* `headroom learn`'s writer treats `CLAUDE.md`/`CLAUDE.local.md` as its own generated output (marker-delimited, machine-owned block, human edits inside the markers presumably get clobbered on the next `--apply` run, though I did not find explicit code guarding against a human having hand-edited inside the markers between runs). This is actually **consistent** with the "edit the generator" principle in one direction (the LLM digest+prompt is the generator; the CLAUDE.md block is the generated output) but creates a **new** generator this user did not choose and cannot inspect the reasoning of before it writes — the underlying LLM call is not auditable in the way `transcript-scanner`'s `path:line`-cited findings are. This is a contradiction with the machine's evidence culture even where it's consistent with the generator/output split.

## Corrections needed at ingest

- **Factual error to note if any fragment cites Headroom's own docs:** `llms.txt:67` states telemetry is "off by default (opt-in)," which is false per the code (`BEACON_DEFAULT_ON = True`). Any ingested note referencing Headroom's telemetry stance must cite the README/code, not `llms.txt`.
- **Stateless-model-unfriendly content:** none of the ingestible fragments require session memory or ongoing state to honor — they are single, self-contained principles (a comment/docstring convention, a routing default). No correction needed on that axis.
- **Style violations against library conventions** (would need fixing before any fragment lands in a SKILL.md or CLAUDE.md): the Headroom source quotes use standard prose without em dashes in the specific lines quoted above (checked: none of the seven §5 quotes contain an em dash), so no changes needed there. Headroom's own docstrings do use em dashes elsewhere in the codebase (e.g., `writer.py:36-38`, `analyzer.py` docstrings) — if a fragment is lifted verbatim rather than paraphrased, re-punctuate any em dash to match the "no em dashes" style rule before it lands in an incumbent file. None of the fragments recommended above need verbatim insertion; all are recommended as short paraphrased bullets, which sidesteps this.

## Net assessment

If only three things could be taken:

1. **The marker-block merge-and-carry-forward mechanism** (`headroom/learn/writer.py:89-193`), as a design note, not code — target `~/skill-library/plugins/workbench/skills/retro/SKILL.md` §6, appended as a concrete technique to reference when the deferred `/retro-review` weekly-synthesis piece finally gets built. This directly fills a gap `retro` names as its own known-missing piece.
2. **Two fragments into `/Users/gfm/.claude/CLAUDE.md`**: (a) the telemetry two-switch separation principle, appended to "Credentials and secrets," and (b) the "refuse to silently drop a user-supplied override" principle, appended to "Surgical edits." Both are short, general, and match the file's own "write it down once it has cost a correction twice" bar only loosely — recommend holding both as noted-but-not-yet-added candidates rather than inserting immediately, per the file's own economy rule, unless Graham wants them in now.
3. **Nothing else, as a whole item.** `headroom wrap claude` itself is a DISCARD for current use (adoption cost and philosophy conflicts outweigh the token-economy benefit for a single-operator setup not currently bottlenecked on provider cache costs), and the remaining four §5 ideas are either REDUNDANT (idea 6, already covered by `proof-of-work`/`evidence-report`, better) or narrow COMPLEMENTs with nothing on this machine to consume them yet (ideas 1, 4, 7).

No code, plugin, or hook from the candidate should be installed. The three items above are documentation-only additions, and two of the three are explicitly flagged as "candidate, not yet justified" under this machine's own CLAUDE.md-economy rule.
