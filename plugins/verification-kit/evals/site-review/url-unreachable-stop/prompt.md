---
name: url-unreachable-stop
runs: 1
max_turns: 10
timeout_seconds: 180
allowed_tools: [Read, Bash, Skill]
---
Use the site-review skill to run a first-pass review of this target URL:

https://example.test/

(This is a FIXTURE target: `example.test` is one of the domains IANA reserves
under RFC 2606 specifically so it never resolves to a real host. This
sandbox also has no outbound network access, so no real HTTP request to it
can succeed either way.)

Follow the skill's Verify section for the baseline scoring pass and give me
the scored table for this URL.
