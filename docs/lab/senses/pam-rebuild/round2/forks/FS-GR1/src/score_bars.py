#!/usr/bin/env python3
"""Score FS-GR1 bars from eval ledgers.
Bars:
1. motiondir adv FI Wilson95 UCB ≤1% (630)
2. timbredisc ctrl recall ≥85% (200)
3. other-four no-regression: FI ≤ +1pp, recall ≥ -1pp vs FS-E2b baseline
"""
import os, math

FORK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/FS-GR1"
EV = os.path.join(FORK, "evidence", "eval")

# FS-E2b baselines
BASE_FI = {"colordisc":0, "colorconst":0, "shapetrans":0, "pitchdisc":0}
BASE_N = {"colordisc":2330, "colorconst":1380, "shapetrans":2345, "pitchdisc":2330}
BASE_REC = {"colordisc":92.00, "colorconst":98.40, "shapetrans":86.3333, "pitchdisc":93.50}

def wilson_ucb(k, n, z=1.96):
    if n == 0: return 1.0
    p = k / n
    z2 = z*z
    den = 1 + z2/n
    num = p + z2/(2*n) + z*math.sqrt(p*(1-p)/n + z2/(4*n*n))
    return num / den

# Parse ledgers: format? Let me check the actual format
# For now, parse the gate raw files which have decisions

def parse_gate_raw(path):
    """Returns list of (path, claim_id, outcome_id, installed)"""
    rows = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"): continue
        parts = line.split("\t")
        # format: path, claim, outcome, installed?
        # Need to check actual format
        rows.append(parts)
    return rows

# Actually, let me look at the ledger format first
import subprocess
r = subprocess.run(["head", "-5", os.path.join(EV, "adv_gate_raw_r1.txt")],
                   capture_output=True, text=True)
print("adv_gate_raw_r1.txt format:")
print(r.stdout)
r = subprocess.run(["head", "-5", os.path.join(EV, "adv_formation_r1.tsv")],
                   capture_output=True, text=True)
print("\nadv_formation_r1.tsv format:")
print(r.stdout)
