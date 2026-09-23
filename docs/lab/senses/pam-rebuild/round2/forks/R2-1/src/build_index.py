#!/usr/bin/env python3
"""Build trial_index.csv and MANIFEST.sha256 for the 10,000-trial R2-1 suite.

Trial index: trial_idx, fixture_id, fixture_path, task, truth, stratum, family.
Manifest: SHA-256 of every scored .r2a and .truth file (explicit index only).
"""
import os, sys, csv, hashlib

FORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SUITE = os.path.join(FORK, "suite")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
ADV_FAMS = [
    [("R2A-COL-1", 331), ("R2A-COL-2", 290), ("R2A-COL-3", 331)],
    [("R2A-CCN-1", 282), ("R2A-CCN-2", 282)],
    [("R2A-SHP-1", 331), ("R2A-SHP-2", 373), ("R2A-SHP-3", 248)],
    [("R2A-PTC-1", 290), ("R2A-PTC-2", 331), ("R2A-PTC-3", 331)],
    [("R2A-TMB-1", 207), ("R2A-TMB-2", 207), ("R2A-TMB-3", 157)],
    [("R2A-MOT-1", 290), ("R2A-MOT-2", 290), ("R2A-MOT-3", 244)],
]

def fam_of(taskidx, idx):
    acc = 0
    for fam, cnt in ADV_FAMS[taskidx]:
        if idx < acc + cnt:
            return fam
        acc += cnt
    raise ValueError("adv index out of range")

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def main():
    # Enumerate scored fixtures: r21n_ (gen normal), r21a_ (gen adv), r21f_ (frozen)
    trials = []
    for fn in sorted(os.listdir(SUITE)):
        if not fn.endswith(".r2a"):
            continue
        fid = fn[:-4]
        if fid.startswith("r21n_"):
            stratum = "gen_normal"
        elif fid.startswith("r21a_"):
            stratum = "gen_adv"
        elif fid.startswith("r21f_"):
            # r21f_<task>_<idx>; idx<740 normal, >=740 adversarial
            stratum = None  # determined below
        else:
            continue
        # task is the middle component
        parts = fid.split("_")
        # r21n_colordisc_0 -> ['r21n','colordisc','0']
        task = parts[1]
        ti = TASKS.index(task)
        num = int(parts[2])
        if fid.startswith("r21f_"):
            stratum = "frozen_normal" if num < 740 else "frozen_adv"
        family = ""
        if stratum in ("gen_adv",):
            family = fam_of(ti, num)
        truth_p = os.path.join(SUITE, fn + ".truth")
        truth = open(truth_p).read().strip()
        assert truth.startswith("truth=")
        truth = truth[6:]
        trials.append({
            "fixture_id": fid,
            "fixture_path": os.path.join(SUITE, fn),
            "task": task,
            "truth": truth,
            "stratum": stratum,
            "family": family,
        })
    # Deterministic order: sort by fixture_id
    trials.sort(key=lambda t: t["fixture_id"])
    for i, t in enumerate(trials):
        t["trial_idx"] = i
    # Validate counts
    from collections import Counter
    c = Counter(t["stratum"] for t in trials)
    print("stratum counts:", dict(c), flush=True)
    assert c["gen_normal"] == 4260, c
    assert c["gen_adv"] == 4815, c
    assert c["frozen_normal"] == 740, c
    assert c["frozen_adv"] == 185, c
    assert len(trials) == 10000, len(trials)
    # Write trial index
    idx_path = os.path.join(FORK, "evidence", "trial_index.csv")
    with open(idx_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["trial_idx", "fixture_id", "fixture_path",
                                           "task", "truth", "stratum", "family"])
        w.writeheader()
        w.writerows(trials)
    print("wrote %s (%d trials)" % (idx_path, len(trials)), flush=True)
    # Write MANIFEST.sha256 from explicit index only
    man_path = os.path.join(SUITE, "MANIFEST.sha256")
    lines = []
    for t in trials:
        for suffix in ["", ".truth"]:
            p = t["fixture_path"] + suffix
            h = sha256_file(p)
            # repo-relative path for the manifest
            rel = os.path.relpath(p, os.path.expanduser("~/workspace/tnn-lab"))
            lines.append("%s  %s\n" % (h, rel))
    lines.sort(key=lambda l: l[65:])
    with open(man_path, "w") as fh:
        fh.writelines(lines)
    print("wrote %s (%d entries)" % (man_path, len(lines)), flush=True)

if __name__ == "__main__":
    main()
