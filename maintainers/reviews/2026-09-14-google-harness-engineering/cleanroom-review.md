# Review: "The Anatomy of Harness Engineering: How to Evaluate, Iterate, and Guard AI Coding Agents"

*Google for Developers blog, Sept 9, 2026. Taylor Mullen and Christian Gunderman.*

## 1. Executive summary

- **Main argument:** end-to-end benchmarks like Terminal-Bench and DeepSWE tell you *that* an agent got worse, not *why*. The authors say you should add "behavioral evals": tests that check what the agent did along the way (which tools it called, which files it changed) rather than its final output.
- **Order of work:** build by dogfooding first, and add evals later, once you need to catch regressions.
- **What you get:** one Antigravity SDK pytest example, a three-step starter loop, and a sketch of letting an LLM rewrite its own system prompt until the tests pass.
- **Evidence:** none. There's no data, no case study, no before/after, and no failure rates. Every load-bearing claim is asserted.
- **Contradictions:** it calls the checks "fast, deterministic, unit-style" and "under 5 seconds". Its own example calls a live model with web search, it recommends LLM-as-a-judge, and it later admits single runs are "noisy due to nondeterminism".
- **Novelty:** low to moderate. Testing the path an agent takes rather than its output, and watching pass rates over many runs rather than one, are both sound and already well known. The self-tuning prompt loop is the least common idea here and gets one sentence.
- **Actionability:** moderate. The three-step loop can be done tomorrow. The code depends on an SDK whose API you'd need to check first.
- **Main risk:** following the advice uncritically could leave you with slow, flaky "unit" tests and prompts tuned to pass the eval suite rather than to work well.

## 2. Claims and evidence status

| # | Claim | Status |
|---|---|---|
| 1 | Developers new to harness engineering often run Terminal-Bench or DeepSWE, see the score move a few points, and can't tell why. | asserted |
| 2 | End-to-end benchmarks are the standard way to evaluate model performance. | asserted |
| 3 | The investigations those benchmarks trigger are expensive. | asserted |
| 4 | Behavioral evals are "often a better measure of confidence" about whether expected behaviors happen and whether you're regressing. | asserted |
| 5 | Behavioral evals help explain why a change moves results. | asserted |
| 6 | "Most teams" evaluate agents like a student taking an exam (a codebase, a time limit, tests passing). | asserted |
| 7 | End-to-end benchmarks don't usually tell you directly what caused a drop. | asserted, though widely accepted |
| 8 | Behavioral evals work like integration tests. With a rich enough set, you have a baseline and can keep improving the prompt against it. | asserted |
| 9 | Early on, rely on instinct and dogfooding rather than an eval harness. | anecdotal (the authors' own build experience, generalized) |
| 10 | Evals don't make sense until the agent can dogfood its own codebase, write its own markdown renderer, and so on. | anecdotal, and stated as an absolute rule |
| 11 | The main purpose of an eval suite is catching regressions, not measuring gains. | asserted (a values claim) |
| 12 | A robust framework splits behavioral checks into fast, deterministic, unit-style checks that run locally. | asserted, and **contradicted** by claims 16 and 19 and by the code example |
| 13 | Checking small observable actions makes a reliable safety net, so you'll know "immediately" when a core behavior breaks. | asserted |
| 14 | Behavioral evals check intermediate steps (tool calls, file changes) rather than exact final strings. | partly evidenced: a code example shows the pattern, but not that it works |
| 15 | With a rich suite you can automate prompt engineering: an LLM rewrites its own system prompt until a failing test passes, while the rest of the suite guards against breakage. | asserted, with no implementation or results |
| 16 | For complex tasks, the agent may find an unexpected but correct path, so use fuzzier outcome checks such as LLM-as-a-judge. | asserted |
| 17 | Single eval runs are noisy because models are nondeterministic. | asserted, though widely accepted |
| 18 | Tracking pass rates across batches over time shows whether behavior is heading the right way, and lets you change prompts and models without stopping development. | asserted |
| 19 | The local behavioral suite runs in under 5 seconds. | asserted, and implausible for tests that call a live model |
| 20 | Behavioral evals complement end-to-end suites rather than replacing them. | asserted |
| 21 | Using both gives more confidence when changing prompts, adding features, or switching models. | asserted |
| 22 | The SDK exposes `google.antigravity.Agent`, `LocalAgentConfig`, `types.BuiltinTools.SEARCH_WEB`, and `response.tool_calls` as an async iterable. | evidenced only by the snippet and a repo link; not shown running |

**Tally:** 0 claims evidenced by data, about 2 partly evidenced by example code, 2 anecdotal, and the rest asserted.

## 3. Techniques worth taking (quoted)

1. **Assert on tool calls, not on the text of the answer.**
   > "Behavioral evals assert on intermediate execution steps, like specific tool calls or file modifications, instead of final string equality"

   The example collects `[call.name async for call in response.tool_calls]` and asserts that `SEARCH_WEB` is in the list.

2. **Turn a real failure into a test.**
   > "Pick one failure mode: Find a recent mistake your agent made, like forgetting to run unit tests before marking a task as done. Find a single, obvious action that slipped, and make that your target."

3. **Match how strict the test is to how open-ended the task is.**
   > "For simple tasks with one optimal solution, build a strict single-turn assertion checking if the agent hit a specific milestone (e.g., verifying it called the test-runner)... for more complex tasks... avoid enforcing a rigid tool sequence. Instead, use fuzzier, outcome-based checks, such as an LLM-as-a-judge"

4. **Gate on pass rates across many runs, not on a single run.**
   > "Rather than blocking PRs on single eval runs that can be noisy due to nondeterminism of AI models, automate batch evaluations to pull a larger volume of data. Tracking aggregate pass rates over time ensures the model's behavior is trending correctly."

5. **Example behaviors to target** (useful as seed test ideas):
   > "When given an underspecified prompt, does the agent ask a clarifying question instead of guessing?"
   > "When modifying a build file, does it run the local validator before declaring it complete?"
   > "When generating documentation, does it provide canonical repository links?"

6. **Automated prompt tuning** (only an outline, no details):
   > "you can set up a loop where an LLM tweaks its own system prompt, iterating until a failing test finally passes, all while the rest of your test suite acts similar to how a CI/CD-style guardrail operates."

## 4. Rubric scores

| Criterion | Score | Note |
|---|---|---|
| Evidence quality | **1/5** | No load-bearing claim has data. The one code example shows the syntax, not that the approach works. |
| Novelty | **2/5** | Testing the agent's path, using LLM-as-a-judge for open-ended tasks, and gating on aggregate pass rates are already common. The self-tuning prompt loop and "evals come after dogfooding" are the only less obvious points, and neither is developed. |
| Actionability | **3/5** | The three-step loop and the assertion pattern are specific enough to start tomorrow. It gives no guidance on batch size, pass-rate thresholds, judge design, or stopping the self-tuning loop from overfitting. |
| Currency risk | **2/5** (high risk) | The code depends on a specific Antigravity SDK API, and the benchmark names and "de facto" framing reflect the field as of Sept 2026. |
| Failure modes | **2/5** (many unaddressed) | See below. The article raises nondeterminism but none of the other risks. |

**What goes wrong for a reader who follows it uncritically:**

- **Flaky "unit" tests.** They'd build tests they think are fast and deterministic, like the weather example, which actually depend on a live model and the network. They'd get flaky CI and waste time on false alarms. The "under 5 seconds" figure sets the wrong expectation.
- **Overfitting.** The self-tuning prompt loop without a held-out set or human review would tune the prompt to pass the tests, not to behave well generally. The system prompt would slowly fill with special cases.
- **Brittle strict checks.** Tests that require a specific tool call would fail good alternative paths, such as reading a cached file instead of searching the web. Worse, they'd reward agents that make the call and then ignore the result, because "called the tool" isn't the same as "used it correctly".
- **An unvalidated judge.** Using LLM-as-a-judge without checking it against human labels just adds a second nondeterministic model with its own biases.
- **Blind spots in trend tracking.** Watching only aggregate pass rates, with no threshold or variance tracking, can hide a real regression in one behavior inside a stable average.
- **Evals added too late.** Waiting until the agent can "dogfood its own codebase" means early design decisions get no regression coverage.
- **Unverified API.** Copying the code as-is could fail if the SDK's API differs from the snippet.

## 5. Currency-risk list (re-verify before acting)

1. **Antigravity SDK API surface:** `from google.antigravity import Agent, LocalAgentConfig, types`, `Agent(config)` as an async context manager, `agent.chat()`, `response.tool_calls` as an async iterable, and `types.BuiltinTools.SEARCH_WEB`. Check against the current release of `github.com/google-antigravity/antigravity-sdk-python`, including whether the repo is public and what the package is called.
2. **Whether `LocalAgentConfig()` with no arguments runs offline or still calls a hosted model.** This decides whether the "fast, deterministic, local" claim can hold at all.
3. **The Terminal-Bench and DeepSWE references**, and the claim that end-to-end benchmarks are "the de facto" standard. Benchmark versions and which ones teams actually use change quickly.
4. **"Run local behavioral suite in under 5 seconds."** Time this on your own suite; it depends on model latency and how many tests you have.
5. **The idea that single runs are too noisy to gate PRs.** This depends on the model's sampling settings and whether its outputs are reproducible, which varies by model and version.

## 6. Flags

- **Nothing in the article is addressed to an AI agent, and it contains no instructions to install anything into agent configuration.** It is written for human readers throughout.
- **Code a reader might run:** `import pytest` / `from google.antigravity import ...` and `pytest evals/behavioral/ -v`. These are examples for humans to run in their own project. There's no install command, and nothing was run during this review.
- **Leftover page text:** "Python", "Shell" and "Copied" after the code blocks, plus navigation and footer links, are from the web page, not the article. The screenshot at line 67 ("Screenshot 2026-09-09 at 9.34.40 AM") couldn't be viewed, so anything it shows wasn't reviewed.
- **Minor inconsistency:** the post has two authors but switches to first person singular once ("I suggest you start small").
