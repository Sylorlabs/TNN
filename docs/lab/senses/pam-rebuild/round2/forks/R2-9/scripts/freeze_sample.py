#!/usr/bin/env python3
"""Freeze the 200-trial human sample for R2-9 KB-E3/E4.
100 clean (stratified across 6 tasks) + 100 adversarial (stratified across
the 6 frozen families: COL-1, CCN-2, SHP-1, SHP-2, PTC-2, MOT-2).
Deterministic seed-20260923 permutation. Writes sample_manifest.tsv + SHA256.
Pure glue — no TNN decisions.
"""
import hashlib, os, sys

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures/r2a_r29")
OUT = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-9/evidence")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
# adversarial families for the 100: (family, task)
ADVFAM = [("COL-1", "colordisc"), ("CCN-2", "colorconst"), ("SHP-1", "shapetrans"),
          ("SHP-2", "shapetrans"), ("PTC-2", "pitchdisc"), ("MOT-2", "motiondir")]

def lcg(seed):
    s = seed
    while True:
        s = (s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        yield s

def main():
    trials = []
    with open(os.path.join(FIX, "trials.tsv")) as f:
        header = f.readline()
        for line in f:
            # trial_id, task, split, family, fixture, truth
            p = line.rstrip("\n").split("\t")
            if len(p) >= 6:
                trials.append({"id": p[0], "task": p[1], "kind": p[2],
                               "family": p[3], "fixture": p[4], "truth": p[5]})
    clean = [t for t in trials if t["kind"] == "normal"]
    adv = [t for t in trials if t["kind"] == "adversarial"]

    # 100 clean: stratified across 6 tasks (17,17,17,17,16,16)
    per_task = {"colordisc": 17, "colorconst": 17, "shapetrans": 17,
                "pitchdisc": 17, "timbredisc": 16, "motiondir": 16}
    g = lcg(20260923)
    sample = []
    for task in TASKS:
        pool = [t for t in clean if t["task"] == task]
        # deterministic shuffle
        idx = list(range(len(pool)))
        for i in range(len(idx) - 1, 0, -1):
            j = next(g) % (i + 1)
            idx[i], idx[j] = idx[j], idx[i]
        n = per_task[task]
        for k in range(n):
            sample.append(pool[idx[k]])

    # 100 adversarial: stratified across 6 families (17,17,17,17,16,16)
    per_fam = {"COL-1": 17, "CCN-2": 17, "SHP-1": 17, "SHP-2": 17, "PTC-2": 16, "MOT-2": 16}
    for fam, task in ADVFAM:
        pool = [t for t in adv if t["family"] == fam and t["task"] == task]
        if len(pool) < per_fam[fam]:
            print(f"WARNING: family {fam} has only {len(pool)} fixtures", file=sys.stderr)
        idx = list(range(len(pool)))
        for i in range(len(idx) - 1, 0, -1):
            j = next(g) % (i + 1)
            idx[i], idx[j] = idx[j], idx[i]
        n = min(per_fam[fam], len(pool))
        for k in range(n):
            sample.append(pool[idx[k]])

    # deterministic global permutation (presentation order)
    idx = list(range(len(sample)))
    for i in range(len(idx) - 1, 0, -1):
        j = next(g) % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    sample = [sample[i] for i in idx]

    os.makedirs(OUT, exist_ok=True)
    mp = os.path.join(OUT, "human_sample_manifest.tsv")
    with open(mp, "w") as f:
        f.write("sample_idx\ttrial_id\ttask\tfixture\ttruth\tkind\tfamily\n")
        for i, t in enumerate(sample):
            f.write(f"{i}\t{t['id']}\t{t['task']}\t{t['fixture']}\t{t['truth']}\t{t['kind']}\t{t['family']}\n")
    h = hashlib.sha256(open(mp, "rb").read()).hexdigest()
    with open(os.path.join(OUT, "human_sample.sha256"), "w") as f:
        f.write(h + "  human_sample_manifest.tsv\n")
    print(f"sample: {len(sample)} trials, sha256={h}")

main()
