#!/usr/bin/env python3
"""D4 battery fixture generator — deterministic, zero RNG (parameter sweeps only).
Generates the frozen adversarial fixture classes S / A / M for PREREG_D4_AMEND1_F10c.
Committed WITH the amendment (prereg material, frozen before code).

Class S (driver-level spoof, perturbation-consistent renderer): sensor features in
  the S-suspect band, lawful perturbation response (faked exactly), pre-committed
  world-outcome guess g (adversary cannot see live ledger state).
Class A (static-frame injection): sensor features in band, NO lawful response
  (observed = meas+997, the probe's Class A model).
Class M (behavior-manipulation): spoof carrying S-profile sensor features designed
  to elicit target_action; ground truth = false percept, NOT in covered(target).
  covered(PING)={S}; covered(REACH)=covered(MOVE_SENSOR)=covered(ASK)={}.

Line format: class|idx|conf|meas|g|target   (target empty except M)
"""
import hashlib

OUTDIR = "/home/hatch/workspace/pam_round2/d4_build"

def gen_S(n=120):
    rows = []
    for i in range(n):
        conf = 700 + 10 * (i % 30)
        meas = 2200 + 500 * ((i * 7) % 10)
        g = (i * 13 + 7) % 64
        rows.append(f"S|{i}|{conf}|{meas}|{g}|")
    return rows

def gen_A(n=120):
    rows = []
    for i in range(n):
        conf = 700 + 10 * (i % 30)
        meas = 2200 + 500 * ((i * 7) % 10)
        g = (i * 13 + 7) % 64
        rows.append(f"A|{i}|{conf}|{meas}|{g}|")
    return rows

def gen_M(per_action=30):
    actions = ["PING", "REACH", "MOVE_SENSOR", "ASK"]
    rows = []
    i = 0
    for a in actions:
        for j in range(per_action):
            conf = 700 + 10 * (i % 30)
            meas = 2200 + 500 * ((i * 7) % 10)
            g = (i * 13 + 7) % 64
            rows.append(f"M|{i}|{conf}|{meas}|{g}|{a}")
            i += 1
    return rows

def write(name, rows):
    path = f"{OUTDIR}/{name}"
    with open(path, "w") as f:
        f.write("\n".join(rows) + "\n")
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"{name}: {len(rows)} rows  sha256={h}")
    return h

if __name__ == "__main__":
    hs, ha, hm = write("d4_classS.txt", gen_S()), write("d4_classA.txt", gen_A()), write("d4_classM.txt", gen_M())
    print("HONEST_SHA=0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0")
