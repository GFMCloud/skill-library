# Archetype: infra (AWS / Terraform)

Layout: `envs/{dev,prod}/` compose modules from `modules/`. Resources are not declared
directly in an env — that keeps dev and prod structurally identical so they differ only
in tfvars, which is the only way "it worked in dev" means anything.

## What SPEC.md needs

- **§2 Decisions** — region(s), account layout (single account or Organizations), state
  backend and where it lives, how auth is obtained (SSO profile, assumed role — name the
  mechanism, never a key), naming/tagging convention.
- **§3 Scope** — which resources this repo owns. Infra repos rot when ownership is
  ambiguous and two things manage the same resource.
- **§5 Dependencies and access** — what already exists that this depends on and does not
  create: VPCs, hosted zones, the state bucket itself, ACM certs.
- **§6 Verification** — the real commands:

  ```bash
  terraform fmt -check -recursive
  terraform -chdir=envs/dev init -backend=false && terraform -chdir=envs/dev validate
  terraform -chdir=envs/dev plan          # expected: no changes on a clean tree
  ```

  "Plan is empty against a clean tree" is the strongest signal an infra repo has. Say so.

## Traps worth a hard rule

- **Bootstrapping the backend.** The state bucket cannot be managed by the state it
  stores. Either it is created out of band, or there is a separate `bootstrap/` with
  local state. Decide which and write it down, or the first `terraform init` on a new
  machine is a mystery.
- **`terraform destroy` in a shared account.** Needs explicit sign-off, always.
- **Secrets in state.** Terraform state holds resource attributes in plaintext, including
  generated passwords and some data-source reads. State is not in git; the backend is
  encrypted; nobody pastes state into a chat.
- **Provider version drift.** `.terraform.lock.hcl` **is** committed — it pins provider
  hashes. `.gitignore` deliberately does not exclude it.
- **`-auto-approve` outside CI.** The plan is the review step. Skipping it is skipping
  the review.

## Hand-off to plan-gate

If the first real session will touch IAM, networking, state, deletion/retention policy,
or anything that spends money, say so in `KICKOFF.md`: that session should run
`plan-gate` before writing Terraform. This scaffolding session is not the place to do it —
there is nothing deployed yet to plan against.
