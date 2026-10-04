# Judging a website's design like an award jury

Part of the [verification-kit](../../README.md) pack.

You have built a site and want an honest answer to "is the design actually good?", not a compliment. This skill takes screenshots of the page at desktop and phone width, scrolling the way a visitor would, and hands them to three separate Claude reviewers who have never seen how or why the site was made. Each scores it on the four things the Awwwards jury scores (design, usability, creativity and content, each out of 10) and must point at what it saw for every score. The middle score of the three counts, and the site is approved only when every category reaches its minimum. You get the scores, the evidence, and specific changes to make in each category.

## Say this to use it

- "judge the design of https://example.com"
- "would this site win an Awwwards?"
- "is this landing page good enough to ship? score it like a design jury"

Or, to be certain this skill and no other one runs:

```
/verification-kit:design-jury
```

It will ask whether the page is a showcase (a portfolio, launch or brand site, the kind you would enter for an award) or a product page (a tool, dashboard or docs page). A product page has a lower bar for creativity. If you do not say, it asks once.

## What you'll get

A score table, the evidence behind each score, and fixes per category. This one is copied from a real run, shortened, on the skill's own deliberately weak test page (a FIXTURE, not a real site):

```
# design-jury: NOT APPROVED

| Category   | Weight | Passes  | Median | Spread | Floor | Result      |
| design     | 40%    | 4, 4, 4 | 4      | 0      | 7     | below floor |
| usability  | 30%    | 5, 5, 4 | 5      | 1      | 7     | below floor |
| creativity | 20%    | 3, 3, 3 | 3      | 0      | 7     | below floor |
| content    | 10%    | 3, 3, 3 | 3      | 0      | 7     | below floor |

## Design
Evidence:
- desktop/frame-00.png: centered H1 with gradient text over a purple-to-blue
  gradient, white pill button with a purple glow
- manifest.json fonts: everything is Arial; weight is the only scale lever
To improve:
- Drop the gradient fill on the H1 and set it solid white.
- Load one display face for headings, keep Arial for body, and declare a scale.
- Replace the emoji in all nine cards with one drawn icon set.
```

## Good to know

- **The scale is the Awwwards scale, which is tight.** Real jurors almost always give 7 or 8, and a Site of the Day averages about 7.3. A typical well-made business site scores 5 or 6 here. That is a correct score, not a harsh one.
- **The minimums for a showcase page are 7 for design, creativity and content, and 6 for usability,** where the reviewers measured about half a point harsher than the real jury. 7 is the score a typical juror gives a Site of the Day. For a product page the minimums are design 6, usability 7, creativity 5 and content 6; those are a judgment call, because no jury scores exist for tools and dashboards to measure them against.
- **It cannot see everything.** It works from screenshots and the page's text, so hover effects, sound, page transitions and how smooth the scrolling feels are listed as "not observed" and never scored. On a site that leans on motion, the creativity score is the least reliable number it gives.
- **Its accuracy is measured, and the numbers are in the skill.** It was tested against the published jury scores of real Sites of the Day, and against sites that won lesser awards or none. See [calibration-web.md](references/calibration-web.md).
- **It starts three extra Claude reviewers for every review,** each reading 15 to 30 screenshots, which costs model usage and takes several minutes.
- **It runs a hidden Chrome window against the page** and saves screenshots and page text into a folder you choose. It presses an obvious "Start" or "Enter" button once if the site has one. It needs Node 22 or later, Python 3, and Google Chrome installed in the standard place (`/Applications/Google Chrome.app` on a Mac, or `google-chrome` or `chromium` in `/usr/bin` on Linux). The page must be reachable from your computer, including one running on `localhost`. A page behind a sign-in is captured as its sign-in screen, so the skill stops rather than judging it.
- **The fix list repeats itself.** Each of the three reviewers writes its own fixes, and they are merged only when the wording matches exactly, so the same fix can appear two or three times in different words. Read the repeats as votes: a fix every reviewer named is the strongest.
- **It does not measure speed, accessibility or broken links.** That is [site-review](../site-review/).
- **Websites only, for now.** Slide decks, PDFs and diagrams are planned as separate modules; asked to judge one today, it says so and stops.
- **It uses no account, key or password.**

## What next

- Need the site's speed, accessibility score and broken links too? [site-review](../site-review/).
- Want a second, separate reviewer to check a change against its goal? [review-pair](../review-pair/).
- Back to the [verification-kit pack](../../README.md), or to [skill-library](../../../../README.md).
