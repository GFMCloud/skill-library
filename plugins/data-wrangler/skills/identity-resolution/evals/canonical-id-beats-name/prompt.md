---
name: canonical-id-beats-name
runs: 1
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Skill]
---
Use the identity-resolution skill to match these two record sources. Email is the
canonical identifier where present. Produce the mapping table and say which rule
resolved each pair.

Source A:
- A1, name "Bob Smith", email bob.smith@example.com
- A2, name "Bob Smith", email bsmith@other.example
- A3, name "Dana Ruiz", email (none)

Source B:
- B7, name "Robert Smith", email bob.smith@example.com
- B8, name "Bob Smith", email bsmith@other.example
- B9, name "Dana Ruiz-Ortega", email (none)

Do not run any commands; the data is complete as given.
