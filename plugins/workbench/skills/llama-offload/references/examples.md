# Calibration examples

Five worked cases. Each names the boundary where the intern stops and Claude takes over. Use these to
judge borderline tasks: if the new task resembles one of these on both volume and boundary, it
delegates.

## 1. Transaction log parsing

Input: 500+ free-text transaction entries from league history, inconsistent formats, such as
"Mike drops Ohtani picks up Skenes 4/12".

Per-item job: extract `{manager, action, player, date}` as JSON.

Why it delegates: bounded extraction, locked output format, errors obvious on inspection.

Boundary: extraction only. Anything computing keeper cost or contract implications from the parsed
data escalates to Claude plus scl-keeper-logic-validator. The intern parses the sentence; it never
touches the rulebook.

## 2. Name normalization across data sources

Input: player names from ESPN exports, Google Sheets, and draft tools: "J. Rodriguez",
"Julio Rodriguez", "Rodriguez, Julio".

Per-item job: map each variant to a canonical name from a provided roster list.

Why it delegates: pure string matching against a closed list, high volume every season.

Boundary: UNSURE catches genuinely ambiguous collisions, such as two J. Rodriguezes, for Claude to
resolve. This is an expected-ambiguity class, so do not count these against the 10% escalation
tripwire.

## 3. Activity note classification

Input: a quarter of raw CRM activity notes and call logs.

Per-item job: tag each with `{stage, product_interest, next_action_needed: y/n}` from a fixed
taxonomy.

Why it delegates: fixed taxonomy, per-note independence, and the data stays local so customer info
never hits a cloud API.

Boundary: anything drafted FOR a customer from these notes is Claude plus graham-voice, never the
intern.

## 4. Job posting extraction

Input: dozens of scraped job postings per scraper run.

Per-item job: extract `{title, company, salary_range, location, remote_policy, top_5_requirements}`
to JSON.

Why it delegates: repetitive extraction feeding a downstream resume-tailoring step.

Boundary: the tailoring itself, matching a person's experience to requirements, is judgment work and
stays with Claude.

## 5. Collection inventory normalization

Input: freeform collection notes and purchase records: "2011 Topps Update Trout RC PSA 9",
"trout rookie graded nine".

Per-item job: structure into `{year, set, player, card_type, grade, grader}`.

Why it delegates: bounded vocabulary, closed schema, mistakes visually obvious against source text.

Boundary: valuation or sell/hold calls are Claude, with current market data.
