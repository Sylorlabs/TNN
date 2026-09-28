#!/usr/bin/env python3
"""Make the CALIBRATION battery (visible to crews)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from battery import build
from cfg_calib import CONFIG
n_t, n_p = build(CONFIG, sys.argv[1] if len(sys.argv) > 1 else "calib")
print(f"calib: teach={n_t} probes={n_p}")
