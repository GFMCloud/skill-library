---
name: plan-gate
description: Pre-implementation gate for work with real blast radius. Investigate the repo AND the live state it deploys against, then produce a restated goal, at most three blocking questions (each with a recommended default), numbered falsifiable assumptions, and a file-level plan. Then stop and wait for approval. Use this whenever the user asks to plan before building, wants an approach or proposal before code, says "don't write code yet", "plan this first", "think before you touch it", or names plan-gate directly. Also use it when the user is about to change infrastructure with real consequences (Terraform or other IaC, IAM, networking, database migrations, deletion or retention policies, auth, or anything touching money) even if they didn't ask for a plan. Skip it for typos, renames, and throwaway scripts.
metadata:
  maturity: incubator
---

# Plan gate

Work like a contractor who bills for rework: the cost of a wrong assumption is yours to avoid, and the cost of an unnecessary question is the user's to pay. Both are real costs. The whole design of this gate is to spend cheap tokens on investigation and restatement so nobody spends expensive time on rework, or on an outage.

The output of this skill is a plan, not an implementation. You stop at the end. That is the point.

## Inputs

The user's request and read access to the repo it concerns. For a change that touches
live infrastructure, read-only access to that system through CLI auth already present in
the environment. Nothing is asked of the user before investigation starts, and a
credential is never an input: live state that cannot be reached becomes a stated
assumption (section 1).

## Verify

The delivered plan has all four parts from section 2: a Goal with acceptance criteria;
zero to three blocking questions, each with a recommended default; numbered assumptions
that a reader could check and disagree with; a Plan naming files or resource addresses,
the working order, and each rejected alternative. Every command run during investigation
was read-only, and for infrastructure the account, workspace, or context the plan was
written against is named. Pass means a reader can point at each part and nothing in the
repo or the live system changed.

## Done when

The four-part plan is delivered and the turn has ended without implementing anything.
After approval: the implementation matches the approved plan, and any assumption that
proved wrong was reported with options, not improvised around (section 4).

## Stop when

Live state cannot be reached (no credentials, no network, wrong account): say what could
not be verified, record it as an explicit assumption, and hand back; never guess and never
ask for a secret. An investigation step would mutate anything: do not run it. The plan
would need a credential handled in plaintext: flag it as a design problem before going
further. Mid-implementation, an assumption fails or the plan does not survive contact
with the code: stop and report what was found and the options. The change is a typo, a
rename, a comment, or under roughly 20 lines with one obvious correct form: do not run
the gate at all (section 3).

## 1. Investigate before you ask

Anything discoverable in under a minute of searching is not a question: it's research you owe the user. Read the relevant code, tests, configs, and dependency manifests first. Never ask about test framework, language version, lint rules, error handling conventions, directory layout, or existing abstractions that already exist in the repo. If the codebase contradicts itself, *that* is worth raising.

**Then check what the repo can't tell you.** A repo is a claim about the world; the running system is the world. Infrastructure code drifts, resources get clicked into existence in a console, and a policy in `main` is not necessarily the policy in prod. Reading only the checked-in files is how a plan that looks correct destroys something that wasn't in the plan.

So when the change touches live infrastructure, verify against actual state before you write assumptions about it, strictly read-only:

- Terraform/OpenTofu: `terraform state list`, `terraform show`, `terraform plan -refresh-only` to surface drift, and check which workspace and backend you're actually pointed at
- AWS: `aws <service> describe-*` / `get-*` / `list-*` for the specific resources in scope, and `aws sts get-caller-identity` so you know which account and role you're reasoning about: a plan written against the wrong account is worse than no plan
- Kubernetes: `kubectl get`/`describe` for the objects in scope, plus the current context
- Containers/homelab: `docker compose ps`, `docker compose config`, systemd unit status: whatever shows what's *running* rather than what's declared

Nothing in this phase may mutate anything. No `apply`, no `destroy`, no `kubectl edit`, no writes. The user has not approved anything yet, and an investigation step that changes state has already violated the gate it exists to serve.

If you can't reach the live state (no credentials, no network, wrong account), don't guess and don't ask for a secret. Say plainly what you couldn't verify, and record it as an explicit assumption in the next section so the user can confirm or correct it. Assume CLI-native auth already exists in the environment; never ask the user to paste a credential, key, or token, and flag it as a design problem if the plan would require handling one in plaintext.

## 2. Then produce this, and stop

**Goal.** One paragraph restating what the user asked for, in your own words, including the acceptance criteria you'll hold yourself to. If your restatement is wrong, this is the cheapest possible place to find out: which is why it goes first and why it should be specific enough to actually be wrong.

**Blocking questions (0–3).** Only ask when a wrong answer means throwing work away, not adjusting it. Give each question your recommended default so the user can reply "yes to all". Never ask an open question where a proposed answer would do. If nothing is genuinely blocking, say so and list zero; padding this section to look thorough trains the user to stop reading it.

**Assumptions.** Numbered, specific, falsifiable. "Inputs are under 10k rows and fit in memory" is an assumption. "The code should be maintainable" is not: nobody can check it and nobody can disagree with it. Cover whichever of these the task actually touches, and skip the ones it doesn't:

- **Data**: shape, volume, trust level, encoding, what a malformed input looks like
- **Failure**: what should happen on timeout, partial write, or downstream 500: retry, fail loud, or degrade
- **Boundaries**: who calls this, what's public API vs. internal, backwards-compat obligations
- **State**: concurrency, idempotency, transactionality, ordering guarantees
- **Environment**: runtime version, where it deploys, what it's allowed to reach, which account/region/workspace, what auth it runs as
- **Scope**: what you're deliberately *not* doing, and what you're leaving as a TODO
- **Testing**: what you'll write tests for and what you'll leave uncovered

For infrastructure changes, these three are usually where the damage lives, so state them explicitly rather than letting them hide inside "Environment":

- **Blast radius**: what gets replaced vs. updated in place, and what a replacement takes down with it. Name the resources that will be destroyed and recreated, by address.
- **Reversibility**: can this be rolled back, and how? A change with no rollback path is a different kind of change, and the user should get to know that before approving it, not after.
- **Drift**: what you found that the repo didn't predict, and whether the plan absorbs it or trips over it.

**Plan.** Files you'll create or modify, the key function/type signatures or resource addresses, and the order you'll work in. Where you chose between real alternatives, name the alternative and say why you rejected it in one clause. A plan with no rejected alternatives usually means you didn't look for any.

**Plan self-check.** Before presenting, read the plan against these and fix what fails. They are checks on the plan, not on the code (adapted from the ECC project's `planner` agent, MIT, v2.2.1; review record `maintainers/reviews/2026-09-17-ecc/`):

- Every step names the file or resource address it touches. A step with no path is a wish.
- The plan says how each step will be verified, and what is tested versus left uncovered. A plan with no testing strategy fails this check.
- Each phase can be delivered and rolled back on its own. If phase 2 only works once phase 4 exists, the phases are wrong.
- No value is hardcoded that the repo or the environment already defines (account IDs, regions, paths, limits).
- The unhappy path is in the plan: what each step does on timeout, partial write or a failed apply.

A worked example of the level of detail expected, for "add a 30-day expiration rule to the logs bucket":

> **Goal.** Objects under `logs/` in `app-logs-prod` expire after 30 days; nothing outside `logs/` changes; verified by reading the live lifecycle configuration after apply.
> **Blocking questions (1).** Versioning is on, so expiration leaves noncurrent versions behind. Also expire noncurrent versions after 30 days? Default: yes.
> **Assumptions.** 1. The bucket is managed by `infra/s3.tf` (`aws_s3_bucket.logs`), confirmed with `terraform state list`. 2. No lifecycle rule exists today, confirmed with `aws s3api get-bucket-lifecycle-configuration` (returned NoSuchLifecycleConfiguration). 3. Nothing reads `logs/` objects older than 30 days; not verifiable from here, please confirm. Blast radius: deletes data by design, in place, no replacement. Reversibility: the rule can be removed, deleted objects cannot be restored. Drift: none found.
> **Plan.** 1. `infra/s3.tf`: add `aws_s3_bucket_lifecycle_configuration.logs` with one rule, prefix `logs/`, 30 days current and noncurrent. Verify: `terraform plan` shows 1 to add, 0 to change, 0 to destroy. 2. Apply. Verify: `get-bucket-lifecycle-configuration` returns the rule. Rejected: a bucket-wide rule, because `exports/` shares the bucket.

Then wait. Do not begin implementing.

## 3. Proportionality

This ceremony scales with blast radius, and the failure mode runs in both directions: full treatment on a rename wastes the user's attention, and skipping it on an IAM edit is how buckets end up public.

Just do it, no ceremony: a typo fix, a rename, a comment, a change under roughly 20 lines with one obvious correct form, or a throwaway script whose whole output you're going to read anyway.

Full treatment, and be more suspicious than usual of your own assumptions:

**IaC and state.** Any file under `terraform/`, `infra/`, or any `.tf`/`.tfvars`. `terraform state mv|rm|import|taint`. Backend or workspace config. Provider and module version bumps. Any `lifecycle` block, `force_destroy`, or `prevent_destroy`. Any change to `count` or `for_each` on resources that already exist: reindexing silently destroys and recreates, and the diff rarely looks like it.

**Identity and access.** Any IAM policy document, trust policy, or `assume_role` config. Permission boundaries and SCPs. Any wildcard appearing in an `Action` or `Resource`. Security group and NACL rules, especially anything opening to `0.0.0.0/0`. S3 bucket policies and public access block settings. KMS key policies. OIDC provider and federation config.

**Data and schema.** Database migrations, particularly non-additive ones: `DROP`, `ALTER TYPE`, adding `NOT NULL` to a populated column. Any `DELETE`/`UPDATE`/`TRUNCATE` whose `WHERE` clause you had to think about. RDS engine upgrades and parameter groups. DynamoDB key schema or index changes.

**Deletion and retention.** S3 lifecycle and expiration rules, versioning toggles, CloudWatch log retention. Snapshot and backup schedules. `restic forget` / `borg prune` policies and any homelab rotation or cleanup script. Anything whose success condition is "files are gone."

**Networking and DNS.** VPC, subnet, route table, NAT, peering, transit gateway. Route 53 changes: apex, `NS`, and `MX` records especially, since the blast radius is "mail stops" or "the domain stops," not "one service degrades." Reverse proxy config (Traefik/Caddy/nginx) and anything touching ACME or cert state.

**Secrets.** Anything reading or writing Secrets Manager, SSM Parameter Store, SOPS, age, or Vault. Rotation logic. Anything that could land a secret in state, logs, or a shell history.

**Homelab.** Docker Compose volume and bind-mount path changes: a changed path silently starts an empty service rather than failing. systemd units for always-on services. ZFS/LVM/mdadm operations on pools, datasets, or snapshots. Proxmox VM/LXC config and disk resizes. Anything on the host that runs DNS, the reverse proxy, or backups, because those take everything else with them.

Treat this list as illustrative rather than exhaustive. The underlying question it's approximating: *if this goes wrong, do I find out from a test, or from an alert?* If the honest answer is an alert (or a bill), run the gate whether or not the change matches a bullet above.

Line count is a bad proxy on the way up. A one-line diff can be the most dangerous change in the repo: `force_destroy = true`, a wildcard in a policy statement, a dropped `WHERE` clause. When the line count says "small" and the trigger list says "dangerous," believe the trigger list.

When you're genuinely unsure which side of the line something falls on, run the gate. An unnecessary plan costs the user thirty seconds of reading; a skipped one can cost an afternoon or a database.

## 4. After approval

Implement the plan as approved.

If you discover mid-implementation that an assumption was wrong or the plan doesn't survive contact with the code, stop and say so. Don't quietly improvise a different design, and don't press on with an approach you now believe is wrong: the user approved a specific plan, and silently substituting another one converts their approval into something they never actually gave. A short "assumption 3 was wrong, here's what I found, here are the two options" is always cheaper than discovering it in review.
