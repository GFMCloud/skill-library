# Review: "Why your Claude Code routine reported success and did nothing"

Source: `article.md` (from runbook.scosovan.com, Guides category; author byline "The Routines Runbook", slug `manus_admin`)

## 1. Executive summary

- The core idea is sound and useful: in unattended agent runs, a green "run succeeded" status only means the session ran without an infrastructure error. It says nothing about whether the task got done.
- The best idea is Check 5, "Honest when blind". It comes with a short prompt block you can paste that makes the routine report either "read" or "unavailable" for each source, so a failed read never looks like an empty result.
- Most of the "eight-point pass" is standard reliability practice (idempotency, least privilege, fail loudly, verify outputs), applied to LLM routines with clear prose.
- The platform claims are cited to Anthropic docs "checked 5 October 2026", but nothing is quoted or linked to a specific section. They are asserted with a date, not shown. They include the Trusted network default, the `403` / `x-deny-reason` signature, all connectors attached by default, and the 9:07 advice.
- The article is a sales funnel for a paid product (32 routines, "fourteen guardrail patterns"). The advice still stands on its own. The page says it is not affiliated with Anthropic.
- The author slug `manus_admin` suggests the site may be agent-generated. That doesn't make it wrong, but it is a reason to re-check the platform specifics.
- Biggest risk: it describes research-preview behaviour, which changes over time. Re-verify the platform claims before relying on them.

## 2. Claims list

| # | Claim | Status |
|---|---|---|
| 1 | Anthropic's routines docs say a green status means the session started and exited without infrastructure error, not that the task succeeded | asserted (paraphrase of docs, docs linked only in footer, no quote or anchor) |
| 2 | The run list is the only thing most people look at | asserted |
| 3 | A connector that times out can produce "no urgent messages" output that can't be told apart from a real empty result | asserted (illustrative scenario, no demo) |
| 4 | "Source could not be read" is the most expensive failure mode in unattended work | asserted |
| 5 | A failed calendar connector renders an empty schedule | asserted / anecdotal |
| 6 | Silence defaults to "fine" in the reader's head | asserted |
| 7 | On the default cloud environment, network access is "Trusted", which allows only Anthropic's default allowlist | asserted (doc-derived, not quoted) |
| 8 | Requests to hosts not on the list fail with `403` and the header `x-deny-reason: host_not_allowed` | asserted (specific and checkable, but not shown) |
| 9 | Routines scheduled exactly on the hour can start several minutes late | asserted |
| 10 | Anthropic recommends 9:07 rather than 9:00 | asserted (attributed to Anthropic, not quoted) |
| 11 | Local Desktop tasks missed while the machine was asleep can run as catch-up on wake (e.g. 11pm) | asserted (doc-derived) |
| 12 | None of the three failures produce an error; all three show green | asserted (follows from claim 1 if that holds) |
| 13 | A routine session has no memory of your conversations and can't ask follow-up questions | asserted |
| 14 | A GitHub trigger fires on every push to an open PR | asserted |
| 15 | Claude Code does not reuse sessions across events, so five pushes means five independent runs | asserted |
| 16 | Keying state on the head commit SHA (not the PR number) prevents duplicate writes | asserted (logically sound, no procedure shown) |
| 17 | Check 5 is "the one almost every prompt fails" | asserted, unsupported generalization |
| 18 | The read/unavailable block is "the single highest-value edit" you can make | asserted |
| 19 | When you create a routine, every connector attached to your account is included by default | asserted (doc-derived, high-stakes) |
| 20 | During a run, Claude can use every tool from an included connector, including writes, without asking permission | asserted (doc-derived, high-stakes) |
| 21 | Templates accepted unedited arrive with your full connector list, write scopes included | asserted (follows from 19) |
| 22 | There are hourly caps, dropped GitHub events, and a "72-hour GitHub expiry that switches a routine off entirely" | asserted (deferred to another article) |
| 23 | There are "three scheduling options" | asserted (deferred) |
| 24 | Anthropic offers eight free templates | asserted |
| 25 | Routines are a research preview | asserted (dated footer) |
| 26 | Platform behaviour was checked against the docs on 5 Oct 2026 | asserted (a date stamp is good practice, but not evidence) |

Nothing is strictly **evidenced**: there are no quotes, screenshots, logs or reproducible tests. The closest are the specific, falsifiable details (claims 8, 10, 19, 20), which a reader could check against the linked docs.

## 3. Techniques worth taking

1. **Two-outcome source accounting (the main takeaway):**
   ```
   For each source, record exactly one of two outcomes:
     read: <count> items for <explicit window>
     unavailable: <the exact error or refusal text>

   Never infer absence from a failure. If a source is unavailable, the
   section it feeds says "unavailable: <reason>". An empty section and
   an unreadable section must never look the same.
   ```
2. **A verification step that can fail:** "Add a step where the routine re-opens its own output and checks it against what it read… Make that step able to *fail* the run, a verification section that always passes is decoration."
3. **An explicit status per run, plus a log:** "Give every run an explicit status, OK or PARTIAL, and make PARTIAL the result whenever a source was unavailable or a verification check failed. Append one line per run to a log file."
4. **Idempotency key:** "Key your state on something stable (the head commit SHA, not the PR number) so a repeat run writes nothing instead of writing a duplicate."
5. **Time-awareness:** "Have the prompt read the clock first and compare it to the slot it was meant to run in. If it is hours late, say so in the first line of the output and report on the window the slot intended."
6. **Off-the-hour scheduling:** "pick 9:07 rather than 9:00."
7. **Connector pruning:** "Strip that list down to what the routine actually needs before the first run, not after the first incident."
8. **Catching network denials:** watch for "`403` and the header `x-deny-reason: host_not_allowed`" and report it as unavailable rather than carrying on.
9. **The 8-row checklist table** works as a pre-scheduling review.

## 4. Rubric scores

| Criterion | Score | Note |
|---|---|---|
| Evidence quality | **2/5** | The key platform facts are specific and attributed to dated docs, but none are quoted, linked to a section, or demonstrated. Behavioural claims ("almost every prompt fails") have no support. |
| Novelty | **3/5** | Mostly classic ops hygiene, reframed for LLM routines. "Unreadable must not render as empty", turned into a prompt contract, is the one sharp, non-obvious idea. The point that green means infra health is useful framing. |
| Actionability | **5/5** | Concrete prompt text, a checklist and specific config moves (prune connectors, offset the minute, SHA keys). A reader can apply these tomorrow. |
| Currency risk | **High (2/5 for durability)** | It describes a research-preview product. Defaults, header names, scheduling jitter and connector scoping are exactly the details that change. |
| Failure modes | see below | |

**Failure modes for a reader who follows it uncritically:**
- **Trusting prompt-level verification too much.** The model that wrote the output also "verifies" it. Self-checking cuts errors but doesn't guarantee correctness, and a model can still write "OK" when it should write "PARTIAL". An out-of-band check (a log scraper or alert on missing log lines) is still needed. The article implies the prompt alone is enough.
- **The log file may not persist.** "Append one line per run to a log file" assumes the cloud session's filesystem outlives the run. If it is ephemeral, the log disappears. The article doesn't say where to write it (a repo commit, an external store).
- **Relying on the exact `x-deny-reason` string.** If the header or status code changes, a prompt that matches on that exact string stops catching the failure. The general rule ("any fetch error → unavailable") is more robust.
- **Treating the 8 checks as complete.** Not covered: prompt injection from the content a routine reads (important given the connector write-scope warning), secrets handling, cost/rate limits, and concurrent overlapping runs (race conditions beyond simple idempotency).
- **SHA keying is incomplete.** Keying on the head SHA dedupes repeat events for the same commit, but each new push still produces a new result. Readers may expect "one result per PR".
- **Upsell bias.** Claims of universal failure ("almost every prompt fails") help sell the product. Discount them accordingly.

## 5. Currency-risk list (re-verify before acting)

1. Green status means infra-only success (routines docs wording).
2. Default cloud network mode is "Trusted", with an Anthropic allowlist.
3. Blocked hosts return `403` with `x-deny-reason: host_not_allowed`.
4. On-the-hour schedules start several minutes late, and the "9:07" recommendation.
5. Desktop scheduled tasks run catch-up on wake, and how late they can be.
6. **All account connectors are attached to new routines by default.** This one carries the most security weight, so verify it first.
7. **Included connector tools, including writes, run without permission prompts.**
8. GitHub triggers fire on every push to an open PR, with no session reuse across events.
9. Hourly caps, dropped GitHub events, and the "72-hour GitHub expiry" that disables a routine (claimed in the linked article).
10. "Eight free templates" and "three scheduling options".
11. Research-preview status in general. The page was verified 5 Oct 2026, the same day as this review, but it will go stale.

## 6. Flags

- **Path reviewed:** `/private/tmp/claude-501/-Users-gfm-work/b4d0962e-1222-4c70-8020-40a28facede2/scratchpad/pins/scosovan/article.md`
- **Text addressed to agents:** none. No hidden instructions or text aimed at an AI reader.
- **Installation into agent configuration:** no instruction to install anything into agent config files (CLAUDE.md, settings, MCP, hooks). The only paste-in content is the prompt block in Check 5, which the article frames as text for the reader's own routine prompt. It is benign: it only restricts how outputs are reported. The linked companion article offers a "complete hardened prompt you can paste in". That prompt was not reviewed here and should be read in full before use.
- **Commercial:** the page funnels to a paid product and a "free starter" checkout link (`/checkout/?add-to-cart=28`). It states it is not affiliated with Anthropic.
- **Provenance note:** the author URL slug is `manus_admin`, so the content may be agent-generated. All four posts on the site are dated the same day, 5 Oct 2026.