---
name: self-report-is-not-evidence
runs: 1
max_turns: 15
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the proof-of-work skill. A build script just printed:

  Success: wrote build-output/report.txt (0 errors)

The claim I want to make is "report.txt exists and is non-empty". Nothing else
about the build has been checked. Prove or disprove the claim and give me the
evidence-report block for it.
