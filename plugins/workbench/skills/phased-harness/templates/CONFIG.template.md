# Project configuration

Parameters for `<PROJECT-NAME>`. Sessions **must stop and ask** if any value is `TBD`.
This is the only setup interruption.

| Key | Value | Notes |
|-----|-------|-------|
| `<param_1>` | `<value or TBD>` | `<what it controls; where it is consumed>` |
| `<param_2>` | `<value or TBD>` | |
| `<param_3>` | `<value or TBD>` | |

<!-- Typical parameters: target repo/org, local paths, visibility, whether CI is used,
     thresholds, target environment, deadline. One row per thing a runbook interpolates.
     If a runbook references a key, it must exist here. -->

## Standing authorizations (for continuous runs)

These grant `/phase` permission up front so the run does not stop to ask. Set a value
to `no` to force a pause at that step instead.

| Key | Value | Covers |
|-----|-------|--------|
| `auth_<area_1>` | `yes` | `<the concrete actions this covers - commands, writes, installs>` |
| `auth_<area_2>` | `yes` | |
| `auth_<area_3>` | `no` | `<set to no → the run pauses and asks before this>` |

Read these with `turn-reduction:standing-authorization` if it is installed: resolve
each question against this table before asking the user anything.

**Never pre-authorizable:**

- `<IRREVERSIBLE-STEP>` - always requires explicit confirmation of the enumerated
  list at Gate B. It is a designed stop point; the full set is enumerated in the
  `/phase` skill's interruption policy.
- `<any other never-pre-authorized action; one line each, including any gate beyond
  A and B this project defines>`

Actions taken under a standing authorization are still **logged** in `STATE.md` -
authorization removes the question, not the record.
