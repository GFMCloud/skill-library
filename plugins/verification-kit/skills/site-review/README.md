# Scoring a live website and fixing what is wrong

Part of the [verification-kit](../../README.md) pack.

You have a site up and you want to know whether it is in good shape. This skill measures the live site: speed, accessibility, standard good practice and search visibility, each scored out of a hundred, plus every link on the site followed to find the broken ones. It takes screenshots at phone width and in dark mode, and works through a written checklist for the parts no measuring tool can score, such as whether the first screen says what the site is for. Then it fixes what it can on a separate copy of your files, re-measures after each fix, and shows you a before and after table. Nothing is published until you say so.

## Say this to use it

Any of these will do:

- "review my site at https://example.com"
- "check my site's Lighthouse scores and find the broken links"
- "is this site ready?"

Or, to be certain this skill and no other one runs:

```
/verification-kit:site-review
```

It will ask for the address of the live site. It needs a real, deployed address: it refuses a folder of files on your computer, because the tools it uses have to fetch real pages. It will ask whether you want extra rows on the content checklist, and, if you want the fixes made, which branch to work on. A branch is a separate copy of the work kept by git, the tool programmers use to track changes, so your live site stays as it is until you accept the fixes.

## What you'll get

A scored table before and after, the list of broken links, the phone-width and dark-mode screenshots, and a prioritized list of fixes with a status on each.

*This example is illustrative. It was written by hand to show the shape of the output, not copied from a real run.*

```
site-review: https://example.com

                 before   after
Performance         62      91
Accessibility       78      96
Best practices      83      100
SEO                 90      100
Broken links         4       0

Broken links found: /about/team (404), /blog/old-post (404),
  two links to a supplier's site that has moved.

Fixes: images resized and served in a modern format (done), missing alt
  text on 11 images (done), two dead internal links repointed (done),
  the supplier links need a new address from you (waiting on you).

The performance score is a lab proxy and does not certify Core Web Vitals or INP.
The accessibility score is an automatable-issue floor, not WCAG compliance.
```

## Good to know

- **It downloads two tools the first time you use it.** Lighthouse, which scores a page, and linkinator, which follows links. They come from npm, the public download site for Node tools, and they are not on your computer until that first run. That run needs internet access.
- **It needs Node and `npx`.** Without them, neither tool runs. The score table it prints afterwards is a small Python script that comes with the skill and only reads the two report files.
- **It runs a hidden Chrome window against your live site,** twice per pass: once at normal size, once at phone width with dark mode forced on.
- **It crawls your whole site.** Link checking follows every link it finds, so a large site receives a lot of requests in a short time.
- **It writes report files and screenshots** into a folder you choose. The fix phase then edits your site's own files, on the separate branch you named.
- **Nothing is deployed without you saying so.** Publishing a fix to the live site is a point where it stops and asks, every time.
- **The fix phase starts a second Claude reviewer for each attempt,** which costs model usage. A fix is applied only if that reviewer passes it. Two failed reviews with nothing new in the second, and it holds the change for you.
- **It gives up after five attempts** rather than grinding on, and reports exactly which rows are still red.
- **The two score labels above are printed with every table, and they matter.** The speed score is measured in controlled conditions on one machine, not from real visitors. The accessibility score covers only the problems a tool can detect automatically, which is somewhere between a third and a half of the published accessibility standard. A full score is a floor, not a pass.
- **The dark mode check is a best-effort setting, not a real feature of the scoring tool.** Treat the dark mode screenshot as the evidence, not that run's scores.
- **It uses no account, key or password.**
- **Part of its output description points at a file that is not inside the pack,** kept in this repository's `maintainers/` folder and not shipped when you install.

## What next

- Want a quick automatic check that a deploy is up, to run every time? [smoke-gate](../smoke-gate/).
- Deploy failing and you want it diagnosed and retried? [deploy-verify-fix](../../../deploy-ops/skills/deploy-verify-fix/).
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
