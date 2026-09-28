#!/usr/bin/env python3
"""Fast finalize: builds trials.tsv, MANIFEST.sha256, generator_ledger.json
without recomputing annotations (those are deterministic; computed separately).
Usage: finalize_r2a_fast.py <outdir>
"""
import os, sys, json, hashlib

LAB = os.path.expanduser("~/workspace/tnn-lab")
sys.path.insert(0, os.path.join(LAB, "senses", "pam-rebuild", "round2", "fixtures"))
sys.path.insert(0, os.path.join(LAB, "senses", "rebuild", "harness"))
import r2a_gen as G

def read_truth(path):
    with open(path + ".truth") as f:
        return f.read().strip()

def main():
    OUT = sys.argv[1]
    NORM_D = os.path.join(OUT, "normal")
    ADV_D = os.path.join(OUT, "adversarial")
    FROZEN_HARNESS = os.path.join(LAB, "senses", "rebuild", "harness", "fixtures")

    print("verifying frozen harness manifest...", flush=True)
    total, bad = G.verify_harness_manifest()
    print("harness fixtures verified: %d, mismatches: %d" % (total, len(bad)), flush=True)
    assert not bad

    trials = []
    # normal
    for ti, task in enumerate(G.TASKS):
        d = os.path.join(NORM_D, task)
        ext = G.EXTS[ti]
        for idx in range(G.N_NORM[ti]):
            fid = "r2n_%s_%04d" % (task, idx)
            path = os.path.join(d, fid + ext)
            truth = read_truth(path)
            rel = os.path.relpath(path, LAB)
            trials.append((fid, task, "normal", "-", rel, truth))
        print("normal %s: %d" % (task, G.N_NORM[ti]), flush=True)
    # adversarial
    fam_counters = {}
    for ti, fam, count in G.ADV_PLAN:
        task = G.TASKS[ti]
        d = os.path.join(ADV_D, fam)
        ext = G.EXTS[ti]
        for j in range(count):
            idx = fam_counters.get(ti, 0)
            fam_counters[ti] = idx + 1
            fid = "r2a_%s_%04d" % (task, idx)
            path = os.path.join(d, fid + ext)
            truth = read_truth(path)
            rel = os.path.relpath(path, LAB)
            trials.append((fid, task, "adversarial", fam, rel, truth))
        print("adversarial %s: %d" % (fam, count), flush=True)
    # harness
    tdir_map = {"colordisc": "t1_colordisc", "colorconst": "t2_colorconst",
                "shapetrans": "t3_shapetrans", "pitchdisc": "t4_pitchdisc",
                "timbredisc": "t5_timbredisc", "motiondir": "t6_motiondir"}
    for ti, task in enumerate(G.TASKS):
        td = tdir_map[task]
        ext = G.EXTS[ti]
        for variant, split in (("primary", "normal"), ("noise", "normal"),
                               ("adversarial", "adversarial")):
            vd = os.path.join(FROZEN_HARNESS, td, variant)
            for fn in sorted(os.listdir(vd)):
                if not fn.endswith(ext):
                    continue
                fid = "h_%s_%s_%s" % (task, variant, fn[:-len(ext)])
                rel = os.path.relpath(os.path.join(vd, fn), LAB)
                with open(os.path.join(vd, fn + ".truth")) as f:
                    truth = f.read().strip().split("=", 1)[1]
                trials.append((fid, task, split, "harness-" + variant, rel, truth))
    print("total trials (incl. harness): %d" % len(trials), flush=True)
    assert len(trials) == 10000, len(trials)

    trials.sort(key=lambda r: r[0])
    with open(os.path.join(OUT, "trials.tsv"), "w") as f:
        f.write("trial_id\ttask\tsplit\tfamily\tfixture\ttruth\n")
        for r in trials:
            f.write("\t".join(r) + "\n")
    print("trials.tsv written", flush=True)

    # manifest
    man_path = os.path.join(OUT, "MANIFEST.sha256")
    with open(man_path, "w") as mf:
        mf.write("# R2A generated fixtures. Frozen harness fixtures are covered by\n")
        mf.write("# senses/rebuild/harness/fixtures/MANIFEST.sha256 (verified %d files).\n" % total)
        for r in trials:
            if r[4].startswith("senses/pam-rebuild/round2/fixtures/r2a_r29/"):
                for suffix in ("", ".truth"):
                    p = os.path.join(LAB, r[4] + suffix)
                    h = hashlib.sha256()
                    with open(p, "rb") as fh:
                        h.update(fh.read())
                    mf.write("%s  %s\n" % (h.hexdigest(), r[4] + suffix))
    print("MANIFEST.sha256 written", flush=True)

    # ledger
    ledger = {"master_seed": G.MASTER, "streams": {"normal_ext": "400+taskidx",
              "adversarial": "500+taskidx"},
              "reconciliation": "per-task distribution rows treated as shares; "
              "scaled to fill 4260/4815 remainders after frozen harness fixtures",
              "normal_counts": dict(zip(G.TASKS, G.N_NORM)),
              "adv_counts": {fam: c for _, fam, c in G.ADV_PLAN},
              "trial_total": len(trials),
              "families": {
        "R2A-COL-1": "metamer-pairs: truth DIFFERENT (dE2000 2.6-5.0), RGB Euclid<15",
        "R2A-COL-2": "illuminant-drift: truth SAME surface, illuminant shifts mid-item",
        "R2A-COL-3": "CARRYOVER gray-trap: truth DIFFERENT (dE2000 2.6-5.0), RGB Euclid<25",
        "R2A-CCN-1": "extreme illuminants (xblue/xred + 0.55 exposure)",
        "R2A-CCN-2": "mixed-illuminant: half-frame warm / half-frame cool",
        "R2A-SHP-1": "CARRYOVER occlusion-bar; truth = underlying shape",
        "R2A-SHP-2": "distractor-blob: second same-color blob beside target",
        "R2A-SHP-3": "low-contrast gray + full clutter",
        "R2A-PTC-1": "CARRYOVER near-threshold dF/F bands",
        "R2A-PTC-2": "glide-through-threshold; truth from endpoint ratio",
        "R2A-PTC-3": "CARRYOVER harmonic-distractor on tone B",
        "R2A-TMB-1": "CARRYOVER boundary-straddling (inter-profile midpoints)",
        "R2A-TMB-2": "harmonic-boost x1.15 on 2nd harmonic",
        "R2A-TMB-3": "CARRYOVER distractor harmonic profiles",
        "R2A-MOT-1": "reversed-video: frames 0-3 translate D, 4-7 mirror; truth = D",
        "R2A-MOT-2": "flicker (frames 2,5 perpendicular jitter) + superimposed ghost motion",
        "R2A-MOT-3": "CARRYOVER camouflaged: 25% contrast, 1px/frame",
    }, "notes": [
        "TMB-1: the frozen spec's 1075/1400/3000 Hz boundary figures cannot be "
        "realized as stated (harness base-profile true centroids are 440/509/747/"
        "1214 Hz, all below the lowest figure); realized as straddling the "
        "nearest-profile decision midpoints. Recorded here, not changed silently.",
        "Per-task distribution rows in R2_FIXTURE_SET.md sum to 5100 (normal) / "
        "5815 (adversarial) vs frozen totals 5000/5000; treated as shares and "
        "scaled to 4260/4815 generated. Trial total is exactly 10000.",
        "Adversarial fixtures generated by 6 parallel per-task workers "
        "(scripts/gen_adv_task.py) replicating r2a_gen.py's adversarial loop "
        "exactly (same seeds 500+taskidx, same per-task idx).",
        "Annotations (deterministic fixture metadata) computed separately in "
        "annotations.json; not required for trial execution.",
    ]}
    with open(os.path.join(OUT, "generator_ledger.json"), "w") as f:
        json.dump(ledger, f, indent=1, sort_keys=True)
    print("generator_ledger.json written", flush=True)
    print("DONE. trials=%d" % len(trials), flush=True)

if __name__ == "__main__":
    main()
