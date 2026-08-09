---
name: llama-offload
description: Route bulk repetitive text transforms through a local Ollama model instead of processing items directly. Use when a task involves many similar, bounded, mechanical operations across 20+ items - per-row classification, extraction, normalization, reformatting, or summarization. Trigger on "for each row", "normalize these", "classify all", "extract from every", "tag all of these", "offload this locally", "run this through Ollama", or any CSV/JSON batch transform. Also trigger when the data is sensitive and should stay off a cloud API. Delegable work looks like parsing transaction logs, normalizing names against a roster, tagging activity notes, extracting fields from scraped job postings, structuring inventory records. Do NOT use for tasks needing domain judgment, contextual reasoning, or rule interpretation - keeper logic goes to scl-keeper-logic-validator, customer-facing copy goes to graham-voice, and valuations or financial figures stay with Claude regardless of volume. For choosing between Claude models or subagent lanes rather than offloading off-model entirely, use model-effort-advisor.
metadata:
  maturity: incubator
---

# Llama Offload

## Purpose

Claude architects and reviews; the local model grinds. Saves Claude usage on high-volume mechanical
work and keeps sensitive data local. The mental model: Claude is the senior consultant, Ollama is the
intern. The intern handles bounded, repetitive tasks with clear success criteria. The consultant
designs the task, checks the first few, and handles anything the intern escalates.

## Preconditions

Check all three before delegating.

1. Ollama is running: `curl -s localhost:11434/api/tags` succeeds
2. A suitable model is pulled. Prefer the largest available, fall back gracefully: 8b > 3b > 1.5b.
   Check with the tags endpoint above.
3. The task passes the delegation test below.

If Ollama is not running or no model is available, say so and ask whether to start it, pull a model,
or have Claude do the work directly. Do not silently fall back to doing bulk work directly. That
defeats the point of the skill.

## Delegation test

All four must be true.

- [ ] 20+ similar items
- [ ] Each item is bounded: clear input, clear output format, no external context needed beyond what
      fits in the per-item prompt
- [ ] A wrong answer is detectable by inspection, not silently plausible
- [ ] No domain rules or judgment required per item

If any check fails, Claude does the work directly. When borderline, do not delegate. The review cost
of a bad batch exceeds the generation savings.

## Workflow

1. **Design.** Claude writes the per-item prompt. Constraints:
   - Output format locked, JSON or single-line
   - "Output ONLY the answer, no preamble or commentary"
   - Preserve all specifics verbatim: names, numbers, dates, paths
   - Explicit escape hatch: "If the item is ambiguous or you cannot determine the answer, respond
     with exactly UNSURE"
2. **Sample.** Run 5 to 10 representative items, including known-messy ones rather than only clean
   ones. Show the input/output pairs to the user. HARD STOP, wait for approval before the full batch.
3. **Batch.** Process the full set via the localhost:11434 API, not `ollama run` per item. The API
   keeps the model loaded; per-item CLI calls pay reload overhead. Write results to a file as you go,
   never stdout-only.
4. **Verify.** Format compliance check on 100% of output, which is cheap and scriptable. Content
   spot-check a random 5%, minimum 10 items, against source.
5. **Escalate.** Collect all UNSURE responses and format failures. Claude handles those items
   individually. The intern escalates; it never guesses.
6. **Report.** Counts: processed, escalated, spot-check pass rate. Flag if the escalation rate
   exceeds 10%, excluding item classes where ambiguity is expected and UNSURE is the correct answer,
   such as genuinely colliding names. A high unexpected-escalation rate means the task was not
   actually intern-grade. Stop and reconsider the split rather than grinding through.

## Hard rules

- Never delegate: keeper cost or contract logic (that is scl-keeper-logic-validator with Claude),
  customer-facing copy (that is graham-voice with Claude), financial figures or valuations, or
  anything where a plausible-but-wrong answer would flow downstream undetected.
- Never skip the sample gate.
- Batch output is always written to disk before verification.
- Sensitive data such as customer info or financial records is a reason TO delegate locally rather
  than process via a cloud API, but the same judgment boundaries still apply.

## Implementation notes

- API endpoint: POST http://localhost:11434/api/generate with
  `{"model": "...", "prompt": "...", "stream": false}`
- Portable across Mac and Windows. The API contract is identical, only the wrapper script language
  differs, bash versus PowerShell.
- Batch scripts live alongside the task, not in this skill. Each batch job is disposable; the
  workflow is what persists.

## Calibration

See [references/examples.md](references/examples.md) for five worked examples with their delegation
boundaries. Read it when deciding whether a borderline task qualifies.
