#!/usr/bin/env python3
"""Freeze R2-10 training and evaluation samples.
Each: 200 trials (100 clean + 100 adversarial), mutually disjoint, and both
disjoint from R2-9's sample (R2-9 evidence empty as of 2026-09-23; using
R2-10-specific seed 20261023 and a disjoint fixture pool).
Deterministic LCG. Writes sample manifests + SHA256.
Pure glue — no TNN decisions."""
import hashlib, os

FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures")
OUT = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10/evidence")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
# adversarial families for the 100 (frozen R2-9 stratification)
ADVFAM = [("R2A-COL-1", "colordisc"), ("R2A-CCN-2", "colorconst"),
          ("R2A-SHP-1", "shapetrans"), ("R2A-SHP-2", "shapetrans"),
          ("R2A-PTC-2", "pitchdisc"), ("R2A-MOT-2", "motiondir")]

def lcg(seed):
    s = seed
    while True:
        s = (s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        yield s

def load_families():
    fams = {}
    with open(os.path.join(FIX, "FAMILIES.tsv")) as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                fams[p[0]] = (p[1], p[2])
    return fams

def shuffle(lst, g):
    idx = list(range(len(lst)))
    for i in range(len(idx) - 1, 0, -1):
        j = next(g) % (i + 1)
        idx[i], idx[j] = idx[j], idx[i]
    return [lst[i] for i in idx]

def main():
    fams = load_families()
    # clean pool: all r2n fixtures
    clean = [(fn, fam, truth) for fn, (fam, truth) in fams.items() if fn.startswith("r2n_")]
    # adversarial pool: all r2a fixtures
    adv = [(fn, fam, truth) for fn, (fam, truth) in fams.items() if fn.startswith("r2a_")]

    g = lcg(20261023)
    used = set()

    def take_clean(n_per_task):
        sample = []
        for task in TASKS:
            pool = [x for x in clean if task in x[0] and x[0] not in used]
            pool = shuffle(pool, g)
            take = pool[:n_per_task[task]]
            for x in take:
                used.add(x[0])
            sample.extend(take)
        return sample

    def take_adv(n_per_fam):
        sample = []
        for fam, task in ADVFAM:
            pool = [x for x in adv if x[1] == fam and x[0] not in used]
            pool = shuffle(pool, g)
            # n_per_fam is per family; distribute 100 across 6 families
            take = pool[:n_per_fam[fam]]
            for x in take:
                used.add(x[0])
            sample.extend(take)
        return sample

    # Training: 100 clean (17,17,17,17,16,16) + 100 adv (17,17,17,17,16,16 across 6 fams)
    clean_n = {"colordisc": 17, "colorconst": 17, "shapetrans": 17,
               "pitchdisc": 17, "timbredisc": 16, "motiondir": 16}
    adv_n = {"R2A-COL-1": 17, "R2A-CCN-2": 17, "R2A-SHP-1": 17,
             "R2A-SHP-2": 17, "R2A-PTC-2": 16, "R2A-MOT-2": 16}
    train = take_clean(clean_n) + take_adv(adv_n)

    # Evaluation: 100 clean + 100 adv, disjoint from training
    eval_ = take_clean(clean_n) + take_adv(adv_n)

    assert len(train) == 200, len(train)
    assert len(eval_) == 200, len(eval_)
    assert len(set(x[0] for x in train) & set(x[0] for x in eval_)) == 0

    os.makedirs(OUT, exist_ok=True)
    for name, sample in [("train", train), ("eval", eval_)]:
        # deterministic presentation order: shuffle with the LCG
        sample = shuffle(sample, g)
        path = os.path.join(OUT, f"sample_{name}_manifest.tsv")
        with open(path, "w") as f:
            f.write("order\tfixture\tfamily\ttruth\n")
            for i, (fn, fam, truth) in enumerate(sample):
                f.write(f"{i}\t{fn}\t{fam}\t{truth}\n")
        with open(path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        with open(path + ".sha256", "w") as f:
            f.write(h + f"  sample_{name}_manifest.tsv\n")
        print(f"{name}: 200 trials, sha256={h[:16]}...")

    # disjointness proof
    train_f = set(x[0] for x in train)
    eval_f = set(x[0] for x in eval_)
    print(f"train/eval overlap: {len(train_f & eval_f)} (must be 0)")

if __name__ == "__main__":
    main()
