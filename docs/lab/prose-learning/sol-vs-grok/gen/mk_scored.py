#!/usr/bin/env python3
"""Make the SCORED battery (sealed until build freeze)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from battery import build
from cfg_scored import CONFIG
n_t, n_p = build(CONFIG, sys.argv[1] if len(sys.argv) > 1 else "scored")
print(f"scored: teach={n_t} probes={n_p}")
