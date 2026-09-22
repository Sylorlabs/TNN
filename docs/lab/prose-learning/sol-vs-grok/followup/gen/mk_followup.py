#!/usr/bin/env python3
"""Make the FOLLOWUP sealed battery (after build freeze).

Usage: mk_followup.py [outdir]
Writes teach_sg.txt, probe_sg.txt, expected_sg.json into outdir.
Builders must not read the output before scoring (one shot).
"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from battery import build
from cfg_followup import CONFIG
n_t, n_p = build(CONFIG, sys.argv[1] if len(sys.argv) > 1 else "followup")
print(f"followup: teach={n_t} probes={n_p}")
