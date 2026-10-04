# Calibration: web module

The measured ceiling of the web judge, from one calibration run on 2026-10-03. Read this
before trusting a score. Re-run it after any change to `web.md` or `judge-prompt.md`:
capture with `scripts/capture.mjs`, judge each site with the prompt, then
`scripts/calibrate.py`.

## Contents

- [Bottom line](#bottom-line)
- [Method](#method)
- [Error against the jury](#error-against-the-jury)
- [Tier ordering and gate pass rates](#tier-ordering-and-gate-pass-rates)
- [Deliberate-failure proof and spread](#deliberate-failure-proof-and-spread)
- [Limits of this run](#limits-of-this-run)
- [The sites](#the-sites)

## Bottom line

- **It reliably fails weak work.** Both labelled fixtures were NOT APPROVED on every
  category, with three blind passes agreeing to within one point.
- **It cannot rank award-grade sites against each other.** On Sites of the Day its error
  against the jury is no better than always answering 7, and rank correlation within that
  tier is noise. Jury means sit in a 7.0 to 8.2 band that an integer judge cannot resolve.
- **It separates award tiers weakly.** Mean judge overall: Site of the Day 7.11, Honorable
  Mention 6.78, unawarded nominee 6.72. Cross-tier pairs ordered correctly: 59% (chance
  50%).
- **It is harsh on Usability for sites it was not tuned on** (held-out bias −0.63). The
  showcase Usability floor is 6, not 7, to offset that; with it, 13 of 15 real Sites of
  the Day pass, and so do 4 of 6 unawarded nominees.

## Method

- **Ground truth.** Awwwards publishes per-category jury means and a per-juror table only
  for Sites of the Day; Honorable Mention and nominee pages show no scores (checked on 10
  HM pages and awwwards.com/sites/palmo). So 15 Sites of the Day (2026-07-03 to
  2026-10-03, spread across the score range, 5 held out) give numeric truth, and 6
  Honorable Mentions (5 judged; see Capture) and 6 nominees still unawarded three weeks after nomination give
  ordinal truth: Site of the Day above Honorable Mention (jury 6.5 or more) above nominee
  (below 6.5).
- **Judge.** Opus, one blind non-fork pass per site (k=1) with purpose `showcase`, except
  two Sites of the Day judged three times for spread. Production runs use three passes, so
  these single-pass numbers are the conservative case.
- **Rubric versions.** Rubric v1 scored Usability 1.24 and Content 1.40 below the jury on
  Sites of the Day, because it penalised entry gates and sparse copy that the jury
  rewards. Graham ruled the hybrid fix (2026-10-03): showcase follows the jury, product
  stays strict. Every number below is rubric v2. Held-out sites were judged once, after
  v2 was frozen; produx-design had also been judged under v1 before that rule was in
  place, and its v1 score was seen during tuning.
- **Capture.** Live sites, headless Chrome, 2026-10-03, 27 sampled and 26 judged.
  tbwa-hakuhodo-corporate-site produced no frames in 480 s and is excluded as a capture
  failure. illoca reached the 480 s deadline after all 8 frames at both widths; its
  manifest is marked partial and it was judged, which `SKILL.md` step 2 allows when both
  widths have frames.

## Error against the jury

### Tuning set: 10 sites
| Category | MAE | MAE of always-7 | Bias | Spearman | Mean juror SD |
|---|---|---|---|---|---|
| design | 0.51 | 0.38 | -0.08 | -0.50 | 0.76 |
| usability | 0.31 | 0.21 | -0.31 | -0.17 | 0.67 |
| creativity | 0.52 | 0.54 | -0.24 | 0.11 | 0.77 |
| content | 0.53 | 0.35 | -0.15 | 0.10 | 0.81 |
| overall | 0.39 | 0.36 | -0.19 | -0.44 | n/a |

### Held-out set: 5 sites
| Category | MAE | MAE of always-7 | Bias | Spearman | Mean juror SD |
|---|---|---|---|---|---|
| design | 0.48 | 0.31 | -0.11 | -0.71 | 0.70 |
| usability | 0.63 | 0.23 | -0.63 | 0.00 | 0.69 |
| creativity | 0.70 | 0.58 | -0.38 | 0.32 | 0.77 |
| content | 0.41 | 0.41 | -0.41 | n/a | 0.77 |
| overall | 0.50 | 0.35 | -0.35 | 0.30 | n/a |

MAE is mean absolute error of the judge's integer score against the jury mean. "MAE of
always-7" is a judge that answers 7 for everything; on a set where every jury mean is near
7.3, that is the number to beat, and this judge does not beat it. Bias is judge minus
jury. Mean juror SD is how much the human jurors disagree with each other.

## Tier ordering and gate pass rates

### Ordinal tiers (A > B > C): judge weighted overall
| Tier | Sites | Mean | Min | Max |
|---|---|---|---|---|
| A | 15 | 7.11 | 6.70 | 7.70 |
| B | 5 | 6.78 | 6.40 | 7.00 |
| C | 6 | 6.72 | 5.50 | 7.00 |

Cross-tier pairs ordered correctly: 116 of 195 (59%); tied: 29; chance level: 50%.

Showcase gate with the approved floors (Design 7, Usability 6, Creativity 7, Content 7),
each site's judge median:

- Tier A: 13 of 15 pass showcase; fails: likova ['creativity']; haoqi-design ['content']
- Tier B: 2 of 5 pass showcase; fails: beige-force ['usability']; signal-a-studio ['creativity', 'content']; vakantiehuis-coquelicots ['creativity']
- Tier C: 4 of 6 pass showcase; fails: studio-nikita ['design', 'creativity', 'content']; creativeans ['creativity']

At the first proposal (Usability 7) the rates were 10 of 15, 2 of 5 and 3 of 6. Graham
lowered showcase Usability to 6 to offset the measured bias: three more Sites of the Day
pass, and one more nominee.

## Deliberate-failure proof and spread

Fable judges (Opus built the fixtures), three blind passes each, final capture script:

| Fixture | Design | Usability | Creativity | Content | Verdict |
|---|---|---|---|---|---|
| `generic-template.FIXTURE.html` | 4, 4, 4 | 5, 5, 4 | 3, 3, 3 | 3, 3, 3 | NOT APPROVED (exit 1) |
| `unusable-polish.FIXTURE.html` | 6, 6, 6 | 4, 4, 4 | 5, 5, 5 | 4, 4, 4 | NOT APPROVED (exit 1) |

Spread on two Sites of the Day, Opus, three passes: sstr-friction-reduction 8/7/8/8,
8/7/8/8, 7/7/8/8 (passes); sharplink 7/6/7/7, 7/6/7/7, 7/7/7/7 (Usability median 6
against a jury 7.25; passes at the approved floor of 6). Largest spread seen in any category: 1.

## Limits of this run

- One run, one day, 26 sites. Sites change after their award; scores here are against
  the site as captured on 2026-10-03.
- Nothing below 6.5 overall has public jury scores, so the low end is proven only by the
  two fixtures, not calibrated against humans.
- Single-pass judging for most sites; three-pass medians may move a borderline 6 to 7.
- The judge sees screenshots, a text extract and a probe. Motion quality, hover,
  sound and smoothness were never observed, for any site.

## The sites

| Site | Tier | Awarded | Jury means D / U / C / Ct | Juror SD | Judge D/U/C/Ct |
|---|---|---|---|---|---|
| [sstr-friction-reduction](https://sstr.tech/en/) | Site of the Day | 2026-08-16 | 7.17 / 7.16 / 7.28 / 6.98 | 0.71 / 0.59 / 0.72 / 0.88 | 8/7/8/8 (k=3) |
| [produx-design (held out)](https://www.produx.design) | Site of the Day | 2026-08-09 | 7.10 / 7.10 / 7.52 / 7.10 | 0.85 / 0.50 / 0.96 / 0.60 | 7/6/7/7 |
| [vero-new-york](https://verostudio.com/) | Site of the Day | 2026-08-08 | 7.38 / 7.09 / 7.13 / 7.06 | 0.77 / 0.56 / 0.75 / 0.71 | 7/7/7/7 |
| [milledollars](https://milledollars.fr/) | Site of the Day | 2026-10-02 | 7.25 / 7.15 / 7.23 / 7.39 | 0.73 / 0.52 / 0.80 / 0.84 | 7/7/7/8 |
| [hiroto-sato (held out)](https://www.hirotos.com) | Site of the Day | 2026-07-17 | 7.08 / 7.25 / 7.48 / 7.33 | 0.48 / 0.81 / 0.89 / 0.96 | 8/7/8/7 |
| [united-carriers](https://unitedcarriers.com/) | Site of the Day | 2026-09-06 | 7.35 / 7.00 / 7.61 / 7.16 | 0.62 / 0.46 / 0.75 / 0.68 | 8/7/8/7 |
| [white-desert](https://white-desert.com/) | Site of the Day | 2026-09-11 | 7.28 / 7.27 / 7.21 / 7.74 | 0.65 / 0.62 / 0.65 / 0.75 | 7/7/7/8 |
| [likova (held out)](https://likova.space) | Site of the Day | 2026-08-19 | 7.49 / 7.13 / 7.28 / 7.44 | 0.89 / 0.69 / 0.73 / 0.77 | 7/7/6/7 |
| [haoqi-design](https://haoqi.design) | Site of the Day | 2026-08-14 | 7.44 / 7.10 / 7.69 / 7.17 | 0.67 / 0.50 / 0.68 / 0.54 | 7/7/7/6 |
| [sharplink](https://www.sharplink.com/) | Site of the Day | 2026-08-27 | 7.44 / 7.25 / 7.50 / 7.25 | 0.69 / 0.73 / 0.70 / 0.87 | 7/6/7/7 (k=3) |
| [zeroz-brand-site (held out)](https://otsuka-air.jp/) | Site of the Day | 2026-08-24 | 7.38 / 7.19 / 7.90 / 7.29 | 0.67 / 0.71 / 0.72 / 0.70 | 7/7/7/7 |
| [illoca](https://illoca.unseen.co/) | Site of the Day | 2026-09-04 | 7.33 / 7.43 / 7.70 / 7.36 | 0.84 / 0.75 / 0.77 / 0.81 | 8/7/8/7 |
| [l-i-s-a](https://lisa.locomotive.ca/en) | Site of the Day | 2026-09-16 | 7.45 / 7.22 / 7.89 / 7.61 | 0.84 / 0.92 / 0.68 / 0.88 | 7/7/7/7 |
| [the-watch (held out)](https://thewatch.60fps.fr/) | Site of the Day | 2026-08-17 | 7.51 / 7.48 / 7.74 / 7.90 | 0.63 / 0.74 / 0.55 / 0.82 | 7/6/8/7 |
| [why-zero](https://why.zero.university/) | Site of the Day | 2026-09-07 | 7.70 / 7.46 / 8.16 / 7.75 | 1.09 / 1.05 / 1.16 / 1.16 | 7/7/7/7 |
| [filmbot](https://filmbot.com/) | Honorable Mention | 2026-09-09 | not published |  | 7/7/7/7 |
| [base-power-company-base-core](https://www.basepowercompany.com/core) | Honorable Mention | 2026-09-07 | not published |  | 7/7/7/7 |
| [beige-force](https://beigeforce.com/) | Honorable Mention | 2026-09-04 | not published |  | 7/5/7/7 |
| [signal-a-studio](https://signal-a.studio) | Honorable Mention | 2026-09-01 | not published |  | 7/7/6/6 |
| [tbwa-hakuhodo-corporate-site](https://www.tbwahakuhodo.co.jp/) | Honorable Mention | 2026-08-29 | not published |  | capture failed |
| [vakantiehuis-coquelicots](https://coquelicots.nl) | Honorable Mention | 2026-08-26 | not published |  | 7/7/6/7 |
| [studio-loop](https://studioloop.com.br) | Nominee, no award | 2026-09-11 | not published |  | 7/7/7/7 |
| [brand-packaging-portfolio](https://marina-zakharova.netlify.app/) | Nominee, no award | 2026-09-11 | not published |  | 7/7/7/7 |
| [charmling](https://charmling.app) | Nominee, no award | 2026-09-11 | not published |  | 7/6/8/8 |
| [kavieng-creative](https://www.kaviengcreative.com/) | Nominee, no award | 2026-09-10 | not published |  | 7/7/7/7 |
| [studio-nikita](https://www.studio-nikita.com/) | Nominee, no award | 2026-09-10 | not published |  | 5/6/6/5 |
| [creativeans](https://www.creativeans.com/) | Nominee, no award | 2026-09-09 | not published |  | 7/7/6/7 |

Ground truth fetched from each site's Awwwards page (https://www.awwwards.com/sites/<slug>)
on 2026-10-03; only URLs, dates and the numbers are kept.
