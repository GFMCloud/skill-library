### Items

| id | type | one-line description |
|---|---|---|
| item-ed2aee87 | skill | An on-demand checklist reference for reviewing application and cloud infrastructure security, producing PASS/FAIL/NOT VERIFIABLE findings with a stop-gate on remediation. |

### For each item

**item-ed2aee87**

**Trigger:** Loads on demand, not always on. The frontmatter description lists the load conditions: a change touching authentication, user input, database queries, file paths, external APIs, secrets, or infrastructure; the user saying "security pass," "security checklist," or "is this safe to deploy"; or being invoked as the security dimension of a named orchestrated-review flow (cited in the output contract as `workbench:orch-review`).

**What it makes the agent do:** Pick which of ten listed areas (secrets, input validation, injection, authn/authz, XSS, CSRF, rate limiting, data exposure, dependencies, cloud) apply, and say which were skipped and why. Load only the reference file(s) needed. For each area, search for FAIL patterns "before concluding PASS," and require that every PASS "names what was searched." Every finding must carry file, line, quoted code, severity, and the checklist row it fails. Rows that can't be settled by reading code (e.g., whether MFA is on, whether backups actually restore) must be reported as "not verifiable from the code," with the read-only command or console page that would show it — "never marked PASS by assumption." A hard stop-gate governs remediation: the skill "finds and reports" but does not remediate; any action that changes something is listed under "Proposed actions" and withheld until the user confirms that specific action; anything touching a credential or account setting (rotation, MFA, IAM, a secrets manager) is "never performed by the agent" and handed to the user instead; a suspected live secret is a hard stop — report location, not value, and halt the review until the user says how to proceed. Output must follow a fixed template ending in a "Not checked" line.

**Enforcement:** Prose only — per the supplied facts, enforcement files: none. Nothing in the file is an executable check; compliance depends entirely on the invoking agent following the written checklist and stop-gate. There is no described fallback for a non-compliant agent, so as written it fails open (no external mechanism blocks a skipped step or a PASS given without a search).

**Dependencies:** None named at the runtime level (no CLI, service, or install step is required by the skill itself). Internally it depends on its own two reference files (`references/application-security.md`, `references/cloud-security.md`) and it names, but does not include, two other identifiers it interoperates with: `workbench:orch-review` (consumes its output) and `turn-reduction:plan-gate` (said to run first for infrastructure with "real blast radius").

**State it writes:** None. "Done when" is defined as delivering the report with "nothing has been changed." No log, file, or directory is created by the skill's own operation. (A path, `docs/reviews/2026-09-17-ecc/`, is mentioned as where the skill's own adaptation from a prior source was recorded — that is documentation of the skill's provenance, not an output the skill produces when run.)

**Fit with the bar:**
- Plan then stop before consequential work: supports. Every state-changing action is placed under a proposed-actions list requiring per-action confirmation, credential/account actions are barred to the agent outright, and a live secret forces a hard stop before continuing.
- Executed evidence before "done": supports. Findings require quoted code at a cited line; PASS requires naming what was searched; "Done when" requires the full report with every applicable area resolved to PASS/FAIL/NOT VERIFIABLE, explicitly with "nothing has been changed."
- Say what was and was not checked: supports. The output template has a mandatory "Not checked: <areas skipped and why>" line, and the "not verifiable from the code" category is required wherever the agent lacks the access to check (e.g., cloud console state), rather than being assumed.

**What it does not cover:** States its own limit directly: "it does not find logic flaws, and a clean result is not a statement that the system is secure." Most cloud/account-level rows (MFA status, rotation configuration, whether a backup restore has actually been tested, branch protection settings) are expected to come out NOT VERIFIABLE since they require access the agent doesn't have. It provides no automated scanning, dependency-audit execution, or secret-scanning tool of its own — only names read-only commands (e.g., `npm audit`, `grep` searches) the reviewer may choose to run.

### Agent-directed text

none

### Could not determine

The files reference, but do not include, the orchestrated-review flow that consumes this skill's output (`workbench:orch-review`), the plan-gate flow it says infrastructure changes should go through first (`turn-reduction:plan-gate`), and a separate built-in security-review command it says it is distinct from. The adaptation record it points to (`docs/reviews/2026-09-17-ecc/`) is likewise not among the files reviewed.
