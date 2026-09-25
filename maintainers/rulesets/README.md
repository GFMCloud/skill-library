# Rulesets

`main.json` protects the default branch. Import it in GitHub under Settings > Rules >
Rulesets > New ruleset > Import a ruleset.

What it does:

- Blocks deleting `main` and force-pushing to it.
- Requires a pull request into `main`, with no approving review needed, since the
  repository has one maintainer.
- Requires the `validate` and `brand-gate` checks to pass before a merge.
- Lets the repository admin role bypass all of it (`actor_id` 5). That keeps the
  owner's existing direct pushes working, such as the weekly maintainer's publish
  step and incubator edits made straight on `main`. It also means the local hooks
  are the only check on those pushes. Remove the bypass entry to put every change
  through a pull request.

Private repositories on a free personal account can't enforce rulesets, so the work
and SCL skill repositories follow the same rule by instruction until they move to an
organization plan.
