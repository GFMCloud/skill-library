# Rulesets

`main.json` protects the default branch. Import it in GitHub under Settings > Rules >
Rulesets > New ruleset > Import a ruleset.

What it does:

- Blocks deleting `main` and force-pushing to it.
- Requires a pull request into `main`, with no approving review needed, since the
  repository has one maintainer.
- Requires the `validate` and `brand-gate` checks to pass before a merge, and pins
  both to GitHub Actions (`integration_id` 15368), so no other app can satisfy them by
  posting a status with the same name.
- Allows merge commits only. Consolidation PRs keep one commit per skill so a bad
  skill is one revert; a squash would lose that.
- Has no bypass. Claude sessions act as the owner's account, so an admin bypass would
  let every session push straight to `main` or merge with a red check. Every change,
  the weekly maintainer's included, goes through a pull request.

Private repositories on a free personal account can't enforce rulesets, so the work
and SCL skill repositories follow the same rule by instruction until they move to an
organization plan.
