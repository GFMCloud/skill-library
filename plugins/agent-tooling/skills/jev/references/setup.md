# Jev on this machine

Facts a fresh session needs, dated 2026-09-27. API details (endpoint, question types,
limits, pricing) are not here: read `typesafe:typesafe-ai` and the live docs it points at.

## The key

Stored in the macOS Keychain as a generic password named `TYPESAFE_API_KEY`, exported
from `~/.zshenv` with the same pattern as `ODDS_API_KEY`. Check it without printing it:

```bash
test -n "$TYPESAFE_API_KEY" && echo "key present"
```

If it is missing (a new machine, or a rotated key), Graham runs this one line in his own
Terminal. `-w` with no value makes `security` prompt for the key without echoing it; he
should see two prompts and then the confirmation line. Check `~/.zshenv` first so the
export is not added twice.

```bash
security add-generic-password -a "$USER" -s TYPESAFE_API_KEY -w && printf '%s\n' 'export TYPESAFE_API_KEY="$(security find-generic-password -a "$USER" -s TYPESAFE_API_KEY -w 2>/dev/null)"' >> ~/.zshenv && echo "Key stored in Keychain as TYPESAFE_API_KEY and export added to ~/.zshenv"
```

Never: ask for the key in chat, print it, write it to a file, or run
`claude mcp add -e TYPESAFE_API_KEY=...` (that writes the value into `~/.claude.json`).

## The official plugin

`typesafe@typesafe-ai` from the `typesafe-ai/skills` marketplace, one `SKILL.md`, no hooks
or MCP servers. Invoked as `typesafe:typesafe-ai`. Install if missing:

```bash
claude plugin marketplace add typesafe-ai/skills && claude plugin install typesafe@typesafe-ai && claude plugin list 2>&1 | grep -A3 typesafe
```

## The SDK

Python: `uv add typesafe-sdk` (0.7.2 on 2026-09-27; Python 3.10 or later). It reads
`TYPESAFE_API_KEY` from the environment. Class names: `TypeSafeClient`, `Choice`, `Score`,
`Noul`, `NoulCriteria`. Answers are under `result.answers[id]`, with `.choice`,
`.probabilities`, `.confidence` (Choice, Score) and `.noul` (Noul; no confidence).
`result.usage.input_tokens` is the billable count; `result.model` is the model that
actually answered. At debug log level the SDK logs request and response bodies (not the key).

## The model

`jev-1.13.0` on 2026-09-27; the alias `jev-latest` pointed to it. Before pinning in a new
project, list the current models with `client.models.list()` and read the changelog if the
version moved: thresholds set on one version do not carry to another.

## Measured here (2026-09-27, native API, this network)

| Request size | Median latency | Source |
|---|---|---|
| about 780 input tokens | 145 ms | `~/work/jev-lab/lab/lesson2-results.json` |
| about 28,000 input tokens | 295 ms | `~/work/jev-lab/lab/lesson5-results.json` |

Cost at the docs' $0.042 per million input tokens (output free): about $0.00004 per small
call, about $0.0012 per call checking one item against 47 records. Every lesson run and
re-run together cost about $0.14, most of it two 51-item runs against 47 records each.

## Where the work lives

- `~/work/jev-lab/REPORT.md`: pre-lesson research (sources, setup, conflicts).
- `~/work/jev-lab/lab/LESSONS.md`: what each lesson ran and showed, with numbers.
- `~/work/jev-lab/lab/questions.py`, `test_questions.py`, `lesson5.py`: the scout build,
  the worked example the templates were generalized from.
- `~/work/jev-lab/DATA-DECISION.md`: what data may go to TypeSafe.
