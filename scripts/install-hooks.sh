#!/usr/bin/env bash
# Point this clone's git hooks at .githooks/ (the employer-term and secret gate), and
# install gitleaks at the version CI pins when it is missing. Safe to re-run; the
# project SessionStart hook (.claude/settings.json) runs it at every session start.
# Check with: git config core.hooksPath   (prints .githooks)
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
git config core.hooksPath .githooks

GL_VERSION=8.28.0
BIN="$HOME/.local/bin"   # the hooks put this on PATH
if ! command -v gitleaks >/dev/null 2>&1 && [ ! -x "$BIN/gitleaks" ]; then
  case "$(uname -s)_$(uname -m)" in
    Linux_x86_64)  asset=linux_x64;    sum=a65b5253807a68ac0cafa4414031fd740aeb55f54fb7e55f386acb52e6a840eb ;;
    Linux_aarch64) asset=linux_arm64;  sum=eff65261156100e5d94a6b3dec313d532fddfe19ae1590bf7a2b4f2699128356 ;;
    Darwin_arm64)  asset=darwin_arm64; sum=d942f3ad147250c9edbaab3fed9e482f98d3b59ba10ae97b8d75647e3ade492c ;;
    Darwin_x86_64) asset=darwin_x64;   sum=edf5a507008b0d2ef4959575772772770586409c1f6f74dabf19cbe7ec341ced ;;
    *) asset= ;;
  esac
  if [ -n "$asset" ]; then
    tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
    if curl -sSfL -o "$tmp/gl.tgz" \
        "https://github.com/gitleaks/gitleaks/releases/download/v$GL_VERSION/gitleaks_${GL_VERSION}_$asset.tar.gz" \
      && echo "$sum  $tmp/gl.tgz" | shasum -a 256 -c - >/dev/null; then
      tar xzf "$tmp/gl.tgz" -C "$tmp" gitleaks
      mkdir -p "$BIN" && install -m 0755 "$tmp/gitleaks" "$BIN/gitleaks"
      echo "installed gitleaks $GL_VERSION to $BIN (checksum verified)"
    else
      echo "note: could not fetch and verify gitleaks $GL_VERSION; the hooks will refuse to commit until it is installed." >&2
    fi
  else
    echo "note: no pinned gitleaks build for this platform; install gitleaks $GL_VERSION yourself." >&2
  fi
fi
echo "hooks installed: $(git config core.hooksPath)"
