#!/usr/bin/env python3
"""R2-5 evaluator: runs full battery, computes prereg metrics."""
import os, sys, glob, re, subprocess, hashlib

FORK = os.path.dirname(os.path.abspath(__file__))
SENSE = os.path.join(FORK, "src", "sense")
FIXDIR = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures"
TASKS = ["colordisc","colorconst","shapetrans","pitchdisc","timbredisc","motiondir"]
EXT = {"colordisc":"img","colorconst":"img","shapetrans":"img",
       "pitchdisc":"pcm","timbredisc":"pcm","motiondir":"vid"}

def parse_output(out):
    """Parse sense output into dict."""
    d = {}
    m = re.search(r'judgment=([A-Z_0-9]+)', out); d['judgment'] = m.group(1) if m else None
    m = re.search(r'confidence=([0-9]+)', out); d['confidence'] = int(m.group(1)) if m else 0
    m = re.search(r'state=([A-Z]+)', out); d['state'] = m.group(1) if m else None
    m = re.search(r'promotion_path=([a-z\-]+)', out); d['path'] = m.group(1) if m else None
    m = re.search(r'warrant=([^;]+)', out); d['warrant'] = m.group(1) if m else None
    m = re.search(r'ops=([0-9]+)', out); d['ops'] = int(m.group(1)) if m else 0
    m = re.search(r'ledger=([^\n]+)', out); d['ledger'] = m.group(1).strip() if m else None
    return d

def run_sense(task, fixture, mode="full", prev_hash="0"*64, idx=0):
    """Run sense binary, return parsed output."""
    args = [SENSE, task, fixture]
    if mode == "ablate":
        args.append("ablate")
    else:
        args.append("full")
    args.extend([prev_hash, str(idx)])
    out = subprocess.run(args, capture_output=True, text=True, timeout=30).stdout
    return parse_output(out)

def get_truth(fixture):
    with open(fixture + ".truth") as f:
        return f.read().strip().split("=")[-1]

def main():
    # For now, run on a subset to test
    # Full battery will be run separately
    print("R2-5 evaluator - test mode")
    print("Use run_full.py for the complete battery")

if __name__ == "__main__":
    main()
