#!/usr/bin/env python3
"""A board gate that never blocks. prove-board-gate.sh run against this file must FAIL;
if it passes, the prover is not checking anything."""
import sys

sys.stdin.read()
sys.exit(0)
