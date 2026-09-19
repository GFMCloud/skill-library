# Deploy, check, fix, repeat

Part of the [deploy-ops](../../README.md) pack.

This skill stops Claude Code from calling a deploy finished because the deploy tool said so. It has Claude Code send the change to the running site or service, then go and look at the thing a visitor actually meets, at its real address. If that is wrong, it reads the real error output, works out the cause, fixes it, and deploys again, without handing the work back to you between rounds. It also makes Claude Code settle a few things before the first deploy, including the exact command to roll back, so nobody is inventing one while a site is down.

## Say this to use it

Any of these will do:

- "deploy this and keep going until it actually works"
- "push this to staging and verify it properly"
- "the deploy says it worked but the page is still wrong, sort it out"

Or, to be certain this skill and no other one runs:

```
/deploy-ops:deploy-verify-fix
```

It will ask for five things it cannot guess: the exact deploy command for each place you deploy to, the address or endpoint that counts as proof it worked, anything unusual about your setup, the rollback command, and how many failed rounds should be too many before it comes back to you.

## What you'll get

Each round reported in one line, then the verification that actually settled it.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
Standing constants agreed:
  deploy (staging): ./scripts/deploy.sh staging
  verification:     https://staging.example.com/orders/1042
  rollback:         ./scripts/deploy.sh staging --to 1f9c2ab
  reject after:     3 failed rounds with nothing new learned

Round 1  deploy.sh staging -> ok.  Page loads, order total shows 0.00.  Not verified.
Round 2  read app log: currency field arrives as string, parser returns 0.
         Fixed the parser, committed, redeployed.  Total shows 48.60.  Correct.
         Checked four more orders, including a refunded one: all correct.

Verified at https://staging.example.com/orders/1042 and three others.
Not done yet: this is staging. Say the word and it goes to production,
then gets checked there again to the same standard.
```

## Good to know

- **It runs your commands, not its own.** No program ships with this skill. Whatever your deploy, verification and rollback commands do is what happens, so it is worth reading them before you point this at something that matters.
- **It changes your project's files.** Fixing is part of the loop, and its instructions say nothing gets deployed that has not been committed first.
- **It goes online every round.** Verifying means loading the real address rather than trusting a tool's report, so it reaches whatever host you are deploying to.
- **It writes one line per round into the log your project already keeps.** It creates no log of its own.
- **It stops rather than touch a credential.** A fix that needs a password, a key, or a write to the real site beyond what you agreed is listed as a reason to come back to you.
- **It stops on its own when it stops learning.** Three failed rounds in a row where the last one told it nothing new counts as spinning, and it escalates with a diagnosis and a recommendation instead of the file.
- **It will say when rolling back is the better move,** rather than carrying on because the loop had been going well.
- **The test copy comes first, always,** and going from there to the real site waits for you to say so. "Looks mostly fine" and silence do not count.
- **The stops are written instructions, not something your computer enforces.** They hold because Claude Code follows them, not because a tool is switched off.
- **It costs rounds.** Each one is a real deploy and a real check, so a stubborn failure can take time and tokens before it either works or comes back to you.

## What next

- Moving a site to Cloudflare Pages is its own sequence: [cloudflare-pages-migration](../cloudflare-pages-migration/).
- To hand the whole job to a separate helper that keeps going on its own, ask for the [deploy-loop-owner](../../agents/deploy-loop-owner.md) agent in this pack.
- For what counts as proof in general, not only for deploys: [proof-of-work](../../../foundry-core/skills/proof-of-work/).
- For a small automatic check that your deploy is up, run again and again: [smoke-gate](../../../verification-kit/skills/smoke-gate/).
- Back to the [deploy-ops pack](../../README.md), or to [skill-library](../../../../README.md).
