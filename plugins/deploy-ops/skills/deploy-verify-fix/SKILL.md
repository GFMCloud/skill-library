---
name: "deploy-verify-fix"
description: "The deploy iteration loop — push a change to a running environment, verify it at the level a user meets it, diagnose failures from real output, and redeploy without handing the artifact to a human between cycles. Use for every deploy, staging or production."
metadata:
  maturity: incubator
---

# deploy-verify-fix

The mechanics of iterating on a live environment without a human in the
transport path.

## Before the first deploy

Establish these once and write them into the project's standing constants
(spec §4a). Each is something that otherwise gets rediscovered on every cycle:

- **The deploy command**, verbatim, for each environment. Not "run the deploy
  script."
- **The verification target** — the URL, endpoint, or artifact a user actually
  meets, distinct from whatever the deploy tool reports on.
- **Environment topology surprises.** Split DNS, cross-account boundaries,
  required auth profiles, propagation delay, anything manual. The logged case
  cost 30–60 minutes *per occurrence* because it lived in nobody's notes.
- **The rollback command**, tested. A rollback first attempted during an
  incident is not a rollback plan.
- **The reject threshold** — how many failed cycles before escalating. Agree it
  now, not while failing.

## The loop

**1. Deploy.** One change at a time where possible. A cycle that changes three
things cannot tell you which one worked.

**2. Verify at the level the failure lives.** This is the step that gets
skipped, and skipping it is why deploys "succeed" and stay broken.

| Not verification | Verification |
| --- | --- |
| The deploy tool printed success | The thing responds at its real address |
| `curl -I` returns 200 | The page renders and its content is right |
| A green pipeline | The deployed build is the one that was tested |
| One record looks right | Several representative records look right, including an edge case |

Wait out propagation before concluding a failure. A DNS record that has not
propagated looks identical to a broken deploy for the first few minutes.

**3. Diagnose from real output.** Logs, response bodies, actual errors. Not
from reasoning about what probably went wrong. If the output does not exist,
getting it is the next cycle — instrumenting is progress.

**4. Fix and redeploy.** Do not return to the human. This is the whole point.

**5. Record the cycle.** One line: what changed, what the verification
returned. The log is what makes cycle three smarter than cycle one, and it is
what the escalation report is built from if the loop does not converge.

## Stop conditions

Escalate rather than continue when **any** of these fires:

- **Three consecutive cycles fail and the last produced no new information.**
  The information test is the real one — ten cycles each revealing something
  are fine; two identical ones are a loop, not iteration.
- The fix requires a credential, a production write outside the agreed scope,
  or anything on the standing stop-list.
- The cause is outside the project's boundary — an upstream dependency, an
  entitlement, another system's behavior.
- **Rollback is now cheaper than rolling forward.** Say so and recommend it;
  do not keep pushing because the loop was going well.

Escalate with the diagnosis, the cycle log, and a recommendation. Never with
the artifact and a request to try it.

## Staging to production

- Staging first, always. Originating failure: a project that tested in
  production because no staging environment existed — its own logged
  number-one failure mode.
- **Promote the tested build; do not rebuild.** What was approved must be what
  ships.
- Re-verify in production. Staging passing is evidence about staging.
- Production verification is the same standard, not a lighter one — a real
  load and several representative records, not a health check.

## Prior art worth reading

`scl:scl-module-deploy-checklist` is a mature, project-specific instance of
this loop, with its hard gates written the way spec §4d prescribes: each one
names the failure that produced it. It is not reusable as-is — it is bound to
specific modules, accounts, and scripts — but its gate structure is the model
this skill generalises, and it is the closest thing in the corpus to a working
proof that this pattern holds.
