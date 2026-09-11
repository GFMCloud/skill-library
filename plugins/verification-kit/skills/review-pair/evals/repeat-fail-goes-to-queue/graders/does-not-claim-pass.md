---
type: regex
pattern: "\\bapply(?:ing)?\\s+(?:the\\s+)?change\\b(?!.{0,60}(hold|queue|do not|don't|should not))"
target: last_message
flags: i
match: not_contains
---
