#!/usr/bin/env python3
"""Run the frozen driver against battery_blind (no driver changes)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_kb
run_kb.BAT = os.path.join(run_kb.HERE, 'battery_blind')
run_kb.main()
