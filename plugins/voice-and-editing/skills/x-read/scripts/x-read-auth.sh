#!/bin/bash
# Store your X session cookies in the macOS keychain for x-read.
# Run this yourself in a terminal; values are read with no echo and never leave this machine.
#
#   x-read-auth.sh            prompt for auth_token and ct0, store as x-read-AUTH_TOKEN / x-read-CT0
#   x-read-auth.sh --status   report which items exist (no values)
#   x-read-auth.sh --delete   remove both items
#
# Where to find the values: x.com, signed in -> DevTools -> Application -> Cookies -> https://x.com
# -> copy the Value of `auth_token` and of `ct0`. They expire when you sign out of x.com.
set -euo pipefail
PREFIX="x-read-"
[[ "${OSTYPE:-}" == darwin* ]] || { echo "macOS only (uses the security command)" >&2; exit 1; }

case "${1:-}" in
  --status)
    for key in AUTH_TOKEN CT0; do
      if security find-generic-password -a "$USER" -s "${PREFIX}${key}" -w >/dev/null 2>&1; then
        echo "$key: set"
      else
        echo "$key: missing"
      fi
    done
    exit 0 ;;
  --delete)
    for key in AUTH_TOKEN CT0; do
      security delete-generic-password -a "$USER" -s "${PREFIX}${key}" >/dev/null 2>&1 && echo "$key: removed" || echo "$key: not present"
    done
    exit 0 ;;
  "") ;;
  *) echo "unknown argument: $1" >&2; exit 2 ;;
esac

# Shape checks only; values are never echoed. auth_token is 40 hex chars, ct0 is 160.
for key in AUTH_TOKEN CT0; do
  read -rs -p "Paste ${key} (input hidden): " value; echo
  value="${value//[[:space:]]/}"
  if [[ -z "$value" ]]; then echo "$key: skipped (empty)"; continue; fi
  if [[ ! "$value" =~ ^[0-9a-f]+$ ]]; then echo "$key: rejected, expected hex only (got ${#value} chars)" >&2; exit 1; fi
  if [[ "$key" == AUTH_TOKEN && ${#value} -ne 40 ]]; then echo "AUTH_TOKEN: rejected, expected 40 hex chars (got ${#value})" >&2; exit 1; fi
  if [[ "$key" == CT0 && ${#value} -lt 64 ]]; then echo "CT0: rejected, expected a long hex string of about 160 chars (got ${#value}); this looks like auth_token" >&2; exit 1; fi
  security add-generic-password -a "$USER" -s "${PREFIX}${key}" -w "$value" -U >/dev/null
  echo "$key: stored as ${PREFIX}${key} (${#value} chars)"
done
echo "Done. Verify with: node \"$(cd "$(dirname "$0")" && pwd)/x-read.mjs\" auth-check"
