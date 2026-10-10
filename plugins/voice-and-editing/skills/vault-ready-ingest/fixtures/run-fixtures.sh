#!/usr/bin/env bash
# Run the ingest fixtures with the readwise-links venv (PyYAML, markdown-it-py, pytest). No model is called.
set -euo pipefail
REPO=${READWISE_REPO:-$HOME/work/readwise-links}
cd "$(dirname "$0")"
READWISE_REPO="$REPO" "$REPO/.venv/bin/python" -m pytest -q -p no:cacheprovider test_ingest.py
