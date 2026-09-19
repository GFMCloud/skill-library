#!/usr/bin/env bash
# FIXTURE: builds the scratch git repo the three FIXTURE handoff files check against.
# Never run this against skill-library or any real repo - it creates a throwaway repo
# under /tmp and is safe to re-run (it deletes and recreates the target directory).
set -euo pipefail

REPO_DIR="/tmp/handoff-fixture-repo"

rm -rf "$REPO_DIR"
mkdir -p "$REPO_DIR"
git -C "$REPO_DIR" init -q
git -C "$REPO_DIR" config user.email "fixture@example.com"
git -C "$REPO_DIR" config user.name "Fixture Builder"
git -C "$REPO_DIR" checkout -q -b feature-typed-claims
echo "one" > "$REPO_DIR/a.txt"
echo "two" > "$REPO_DIR/b.txt"
# Backdate both files to before the fixtures' written_at (2026-09-11), so the staleness
# check reports nothing until run-fixtures.sh touches one of them.
touch -t 202609010000 "$REPO_DIR/a.txt" "$REPO_DIR/b.txt"
git -C "$REPO_DIR" add a.txt b.txt
git -C "$REPO_DIR" commit -q -m "FIXTURE: initial commit"

echo "Fixture repo ready at $REPO_DIR"
echo "Branch: $(git -C "$REPO_DIR" branch --show-current)"
echo "Tracked file count: $(git -C "$REPO_DIR" ls-files | wc -l | tr -d ' ')"
