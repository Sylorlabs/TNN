#!/usr/bin/env python3
"""R2-11 frozen list builder (deterministic, seed 20260923). See STRATIFICATION.md."""
import os

LAB = os.path.expanduser("~/workspace/tnn-lab")
WORK = os.path.join(LAB, "senses/pam-rebuild/round2/work/r2-11")
GEN = os.path.join(WORK, "fixtures")
FROZ = os.path.join(LAB, "senses/rebuild/harness/fixtures")
OUT = os.path.join(WORK, "lists")
SEED = 20260923

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TDIR = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
        "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
        "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
TEXT = {"colordisc": "img", "colorconst": "img", "shapetrans": "img",
        "pitchdisc": "pcm", "timbredisc": "pcm", "motiondir": "vid"}
QUOTA = {"colordisc": 822, "colorconst": 548, "shapetrans": 1011,
         "pitchdisc": 575, "timbredisc": 575, "motiondir": 469}

def rel(p):
    return os.path.relpath(p, LAB)

def gen_files(task, split):
    d = os.path.join(GEN, split, task)
    fs = sorted(f for f in os.listdir(d) if f.endswith("." + TEXT[task]))
    return [rel(os.path.join(d, f)) for f in fs]

def frozen_files(task, split):
    d = os.path.join(FROZ, TDIR[task], split)
    fs = sorted(f for f in os.listdir(d) if f.endswith("." + TEXT[task]))
    return [rel(os.path.join(d, f)) for f in fs]

def stride(pool, quota):
    n = len(pool)
    return [pool[(j * n) // quota] for j in range(quota)]

scoring = []
for t in TASKS:
    adv = gen_files(t, "adversarial") + frozen_files(t, "adversarial")
    scoring += [(t, p) for p in adv]
    pool = gen_files(t, "normal") + frozen_files(t, "primary") + frozen_files(t, "noise")
    scoring += [(t, p) for p in stride(pool, QUOTA[t])]

assert len(scoring) == 10000, len(scoring)
with open(os.path.join(OUT, "scoring_10000.txt"), "w") as f:
    for t, p in scoring:
        f.write("%s %s\n" % (t, p))

FAM_LAYOUT = {
    "colordisc": [("COL-1", 400), ("COL-2", 350), ("COL-3", 400)],
    "colorconst": [("CCN-1", 380), ("CCN-2", 300)],
    "shapetrans": [("SHP-1", 400), ("SHP-2", 350), ("SHP-3", 400)],
    "pitchdisc": [("PTC-1", 400), ("PTC-2", 350), ("PTC-3", 400)],
    "timbredisc": [("TMB-1", 250), ("TMB-2", 220), ("TMB-3", 220)],
    "motiondir": [("MOT-1", 345), ("MOT-2", 330), ("MOT-3", 320)],
}
for t, lays in FAM_LAYOUT.items():
    assert sum(c for _, c in lays) == len(gen_files(t, "adversarial")), t

fam_items = {}
for t, lays in FAM_LAYOUT.items():
    files = gen_files(t, "adversarial")
    i = 0
    for fam, c in lays:
        fam_items[(t, fam)] = files[i:i+c]
        i += c

fams = sorted(fam_items.keys(), key=lambda k: (-len(fam_items[k]), k[0], k[1]))
adv_quota = {k: 5 for k in fam_items}
for k in fams[:15]:
    adv_quota[k] += 1
assert sum(adv_quota.values()) == 100

human_adv = []
for k in sorted(fam_items.keys()):
    human_adv += [(k[0], p, k[1]) for p in stride(fam_items[k], adv_quota[k])]

clean_pool = {}
for t in TASKS:
    clean_pool[t] = gen_files(t, "normal") + frozen_files(t, "primary") + frozen_files(t, "noise")
t_sorted = sorted(TASKS, key=lambda t: -len(clean_pool[t]))
clean_quota = {t: 16 for t in TASKS}
for t in t_sorted[:4]:
    clean_quota[t] += 1
assert sum(clean_quota.values()) == 100
human_clean = []
for t in TASKS:
    human_clean += [(t, p, "CLEAN") for p in stride(clean_pool[t], clean_quota[t])]

human = human_adv + human_clean
assert len(human) == 200

def splitmix64(x):
    x = (x + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
    z = x
    z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
    return z ^ (z >> 31)

rng = SEED
order = list(range(200))
for i in range(199, 0, -1):
    rng = splitmix64(rng)
    j = rng % (i + 1)
    order[i], order[j] = order[j], order[i]
human = [human[i] for i in order]

with open(os.path.join(OUT, "human_200.txt"), "w") as f:
    for i, (t, p, kind) in enumerate(human):
        f.write("H%03d %s %s %s\n" % (i + 1, t, p, kind))

os.makedirs(os.path.join(WORK, "sealed"), exist_ok=True)
with open(os.path.join(WORK, "sealed", "human_200_key.txt"), "w") as f:
    f.write("# SEALED - do not include in the human package\n")
    for i, (t, p, kind) in enumerate(human):
        f.write("H%03d %s %s %s\n" % (i + 1, t, p, kind))

with open(os.path.join(OUT, "STRATIFICATION.md"), "w") as f:
    f.write("# R2-11 frozen list stratification (seed 20260923)\n\n")
    f.write("## scoring_10000.txt\n\n")
    f.write("Task-major order (colordisc, colorconst, shapetrans, pitchdisc,\n"
            "timbredisc, motiondir); within a task: all adversarial first\n"
            "(generated index order, then frozen name order), then the\n"
            "stride-selected normal quota from [generated, frozen primary,\n"
            "frozen noise]. Stride: index j -> (j*count)//quota.\n\n")
    f.write("| task | adv (gen+frozen) | normal quota (pool) |\n"
            "|---|---|---|\n")
    for t in TASKS:
        na = len(gen_files(t, "adversarial")) + len(frozen_files(t, "adversarial"))
        npool = len(gen_files(t, "normal")) + len(frozen_files(t, "primary")) + len(frozen_files(t, "noise"))
        f.write("| %s | %d | %d (%d) |\n" % (t, na, QUOTA[t], npool))
    f.write("\nTotal: 6000 adversarial + 4000 normal = 10000.\n\n")
    f.write("## human_200.txt\n\n")
    f.write("100 adversarial: 5 per each of 17 R2A families + 1 extra to the\n"
            "15 largest families (stride-selected within family).\n"
            "100 clean: stride-selected from the per-task normal pool; 17 each\n"
            "for the 4 largest task pools, 16 each for the other two.\n"
            "Blind order: Fisher-Yates with splitmix64(SEED=20260923).\n"
            "Format: `HNNN task lab/relative/path KIND` (KIND = family or CLEAN).\n\n")
    f.write("### adversarial quotas\n\n")
    for k in sorted(fam_items.keys()):
        f.write("- %s %s: %d of %d\n" % (k[0], k[1], adv_quota[k], len(fam_items[k])))
    f.write("\n### clean quotas\n\n")
    for t in TASKS:
        f.write("- %s: %d of %d\n" % (t, clean_quota[t], len(clean_pool[t])))

print("scoring_10000:", len(scoring))
print("human_200:", len(human))
missing = [p for _, p in scoring if not os.path.exists(os.path.join(LAB, p))]
missing += [p for _, p, _ in human if not os.path.exists(os.path.join(LAB, p))]
print("missing:", len(missing))
for m in missing[:5]:
    print("  ", m)
