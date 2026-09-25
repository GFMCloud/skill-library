#!/usr/bin/env bash
# Point this clone's git hooks at .githooks/ (the employer-term and secret gate).
# Run once per clone. Check with: git config core.hooksPath   (prints .githooks)
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
git config core.hooksPath .githooks
command -v gitleaks >/dev/null 2>&1 || echo "note: gitleaks is not installed; the hooks will refuse to commit until it is (brew install gitleaks)."
echo "hooks installed: $(git config core.hooksPath)"
