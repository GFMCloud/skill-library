---
name: write-control-omits-required-field-first
runs: 1
max_turns: 16
timeout_seconds: 300
allowed_tools: [Read, Write, Bash, Skill]
---
Use the capability-preflight skill. Below is a draft manifest for a write to an API.
Before it ever runs against the real service, check it against the skill and fix
anything the skill says is wrong. Save the fixed manifest as `capability-manifest.json`
in the current directory and check it with this skill's `preflight.py --validate-only`.
There is no network here, so do not run the probes for real. Tell me what you changed,
why, and in what order the probes will run.

FIXTURE API reference (invented for this exercise; the service is not real):

    POST $API_BASE/v1/triggers creates a trigger and returns {"id": ...}.
      name       required string
      hook_type  required string; a request without it is refused with 422
                 before anything is created
      filter     optional object, free-form, stored exactly as given
    GET $API_BASE/v1/triggers lists triggers as {"triggers": [...]}.
    Triggers created through the API cannot be deleted or edited through it.

Draft manifest:

```json
{
  "milestone": "eval: trigger API write access",
  "capabilities": [
    {
      "name": "triggers API",
      "population": "triggers in the workspace at $API_BASE",
      "excludes": "every other workspace; editing or deleting triggers",
      "remedy": "issue a token with the triggers write scope and export it as API_TOKEN",
      "read": {
        "cmd": "curl -sf -H \"Authorization: Bearer $API_TOKEN\" \"$API_BASE/v1/triggers\"",
        "evidence": "contains:\"triggers\""
      },
      "write": {
        "cmd": "curl -sf -X POST -H \"Authorization: Bearer $API_TOKEN\" -H 'Content-Type: application/json' -d '{\"name\":\"preflight-probe\",\"hook_type\":\"webhook\",\"filter\":{\"repo\":\"probe\"}}' \"$API_BASE/v1/triggers\"",
        "evidence": "contains:\"id\""
      },
      "negative_control": {
        "cmd": "curl -sf -X POST -H \"Authorization: Bearer $API_TOKEN\" -H 'Content-Type: application/json' -d '{\"name\":\"preflight-probe\",\"hook_type\":\"webhook\",\"filter\":{\"probe\":1}}' \"$API_BASE/v1/triggers\"",
        "expect": "nonzero_exit",
        "why": "a deliberately invalid filter, so the server rejects it and nothing is created"
      }
    }
  ]
}
```
