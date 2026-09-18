All files read. Now I'll compose the report.

### Items

| id | type | one line |
|---|---|---|
| item-979f7ecc | skill | A meta-skill that interviews the user and scaffolds a hypothesis-register/run-log project directory (`experiment-<name>/`), including two dispatch sub-skills (`/hypothesis`, `/run`) that later enforce predict-before-look discipline in that project. |

### For each item

**item-979f7ecc**

**Trigger:** Loads on-demand (skill frontmatter `description`), triggered by phrases like "I keep re-deriving the same finding for my model", "track hypotheses for this analysis", "experiment harness", or "stop me from rationalizing results after I see them"; explicitly declines for terminal/irreversible-finish work (routes to a sibling skill) or one-off single-session analysis. Not always on.

**What it makes the agent do:** Runs a three-step scaffolding process: (1) a "Fit test" requiring both a no-terminal-gate condition and a real risk of re-running/rationalizing ideas to hold, else "decline, and say why"; (2) a one-batch interview extracting what is being modeled, the holdout definition/freeze method, project directory location, naming convention, and confirmation that only the orchestrator commits; (3) scaffold a fixed tree (`CLAUDE.md`, `REGISTER.md`, `HOLDOUT.md`, `dead-ideas.md`, `runs/run-0001-<slug>.md`, two dispatch skills) from templates, with rules: "Freeze the holdout before any run happens", `REGISTER.md` is append-only, replace every `<PLACEHOLDER>`, and "Do not run any experiment here, scaffolding only." Verification step at the end checks files exist with headers only (no fabricated example rows), dispatch skills exist and name the right files, links resolve, and reports the tree with line counts. The two generated sub-skills (`/hypothesis`, `/run`) themselves make a *later* agent, in the scaffolded project: check `dead-ideas.md` before registering a hypothesis and stop to confirm with the user if it resembles a killed idea; write Hypothesis/Prediction/Config to a run file and explicitly not execute in that same step ("Do not execute the run in this step, even if it would be convenient"); on `/run`, gate-check that Prediction was saved before now via a `created` timestamp, refuse to proceed if Prediction is empty ("Do not fill in a prediction now and then immediately run"), execute using Config "exactly as written," fill Result/Verdict only after, update the register status, and log refuted/abandoned ideas to `dead-ideas.md`.

**Enforcement:** Entirely prose/procedural — there is no executable script, hook, or CI check in the files. The "gate" is a file-authoring convention: `/run`'s instructions tell the agent to check a `created` timestamp and an empty-Prediction condition and refuse to continue, but nothing outside the agent's own compliance enforces this (no linter, no hook). Fails open in the sense that everything depends on the acting agent choosing to follow the written steps; the doctrine file itself calls this "a file-existence check, not a promise," but confirms no separate mechanism verifies it.

**Dependencies:** None named — no runtimes, CLIs, or services are referenced. It depends only on the agent itself following the templates and on `~/.claude/CLAUDE.md` existing as a pointer target (referenced but not shown). The generated `/hypothesis` and `/run` skills depend on each other's outputs (register, run files) and on the scaffold this skill produces.

**State it writes:** During scaffolding: `experiment-<name>/CLAUDE.md`, `REGISTER.md`, `HOLDOUT.md`, `dead-ideas.md`, `runs/run-0001-<slug>.md`, and `.claude/skills/hypothesis/SKILL.md` and `.claude/skills/run/SKILL.md`. Later, within the scaffolded project (via the generated sub-skills, not this skill itself): new rows in `REGISTER.md` and `dead-ideas.md`, and new files `runs/run-<NNNN>-<slug>.md` per run.

**Fit with the bar:**
- Plan then stop before consequential work: supports this strongly. Step 1's fit test is itself a stop-and-decide gate before scaffolding, and the produced `/hypothesis` skill explicitly separates writing a prediction from executing a run: "Do not execute the run in this step, even if it would be convenient... the gate is exactly this separation."
- Executed evidence before "done": supports this. `/run`'s Result section demands "raw output, not an interpretation," Config must reproduce the run, and the "Done when" checklist requires the tree fully substituted with no stray placeholders and both dispatch skills verified to exist.
- Say what was and was not checked: supports this. The Verdict section requires stating "confirmed / refuted / inconclusive... state the sample size or interval the verdict rests on," and the doctrine file distinguishes recovered intent from invented design explicitly, itself a was/was-not-checked disclosure at the meta level.
No conflicting lines found.

**What it does not cover:** Does not itself run or score any experiment — it only scaffolds; actual predict-before-look enforcement lives in generated sub-skills, not in this skill's own execution. No mechanism forces a subagent or a different session to respect the "only orchestrator writes REGISTER.md" rule beyond stated guardrail text. No handling of concurrent runs beyond a one-line delegation note. No terminal/exit condition for the harness itself since, by design, "there is no 'done' for the harness itself; individual runs finish, the project does not."

### Agent-directed text

- item-979f7ecc (SKILL.md): "This skill **interviews and scaffolds**. It does not run experiments." / "Do not run any experiment here, scaffolding only." / "Replace every `<PLACEHOLDER>`. Grep the generated tree for `<` before finishing." / "After writing, verify: `REGISTER.md`, `HOLDOUT.md`, and `dead-ideas.md` all exist with only their headers filled in (no fabricated example rows)..."
- item-979f7ecc (hypothesis-dispatch.template.md, becomes `.claude/skills/hypothesis/SKILL.md` in the scaffolded project): "Read [dead-ideas.md]... If the proposed hypothesis matches or closely resembles a killed one, stop and confirm with the user explicitly..." / "Do not execute the run in this step, even if it would be convenient."
- item-979f7ecc (run-dispatch.template.md, becomes `.claude/skills/run/SKILL.md`): "If Prediction is empty, stop: this run was not registered through `/hypothesis`... Do not fill in a prediction now and then immediately run: that is the exact rationalization failure this harness exists to prevent." / "Do not silently change parameters mid-run; if the config needs to change, that is a new run file."
- item-979f7ecc (CLAUDE.template.md, becomes the scaffolded project's `CLAUDE.md`): "Do not work around it by writing Prediction and Result in the same pass." / "Do not fit, tune, or adjust anything against the holdout after it is frozen."

### Could not determine

- The content of `~/.claude/CLAUDE.md`, referenced by CLAUDE.template.md as holding "general working agreements," is not included in these files.
- The sibling skills `phased-harness`, `sweep-harness`, and `rulings-harness`, referenced repeatedly for contrast and shared design lineage, are not included in these files.
- The "SCL (Sloshball Champions League) fantasy player model" cited in doctrine.md as the motivating project is referenced only by name; its actual materials are not present.
