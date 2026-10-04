#!/usr/bin/env python3
"""Finalize the r2a_r29 fixture set: validate trials.tsv, (re)write a correct
MANIFEST.sha256 covering all generated fixtures+truths, validate counts.
The generator's built-in manifest filter hardcodes the default OUT path, so
for r2a_r29 it would emit an empty manifest; this script writes the correct one
in the same format. Pure glue.
Usage: finalize_r2a_manifest.py <r2a_r29 dir>   (cwd must be ~/workspace/tnn-lab)
"""
import hashlib, json, os, sys

LAB = os.getcwd()

def main():
    out = sys.argv[1]
    trials_p = os.path.join(out, "trials.tsv")
    trials = []
    with open(trials_p) as f:
        f.readline()
        for line in f:
            q = line.rstrip("\n").split("\t")
            trials.append(q)
    print(f"trials.tsv: {len(trials)} rows")
    assert len(trials) == 10000, f"expected 10000, got {len(trials)}"

    missing, bad_truth = [], []
    n_gen = 0
    for q in trials:
        tid, task, split, fam, rel, truth = q[0], q[1], q[2], q[3], q[4], q[5]
        p = os.path.join(LAB, rel)
        if rel.startswith("senses/pam-rebuild/round2/fixtures/r2a_r29/"):
            n_gen += 1
            if not os.path.exists(p):
                missing.append(rel)
            tp = p + ".truth"
            if not os.path.exists(tp):
                bad_truth.append(rel)
            else:
                t = open(tp).read().strip().split("=", 1)[1].strip()
                if t != truth:
                    bad_truth.append(rel + " (truth mismatch)")
    print(f"generated fixtures referenced: {n_gen}")
    print(f"missing fixture files: {len(missing)}")
    print(f"truth problems: {len(bad_truth)}")
    for m in missing[:5]: print("  MISSING", m)
    for m in bad_truth[:5]: print("  BADTRUTH", m)
    if missing or bad_truth:
        sys.exit(1)

    # per-task / per-family counts
    from collections import Counter
    cs, cf = Counter(), Counter()
    for q in trials:
        if q[2] == "normal": cs[q[1]] += 1
        elif q[2] == "adversarial": cf[q[3]] += 1
    print("normal per task:", dict(cs))
    print("adversarial per family:", dict(cf))

    # manifest over generated files (fixtures + truths), same format as generator
    man_path = os.path.join(out, "MANIFEST.sha256")
    with open(man_path, "w") as mf:
        mf.write("# R2A generated fixtures (r2a_r29 isolated set). Frozen harness fixtures\n")
        mf.write("# are covered by senses/rebuild/harness/fixtures/MANIFEST.sha256.\n")
        for q in sorted(trials, key=lambda r: r[0]):
            rel = q[4]
            if not rel.startswith("senses/pam-rebuild/round2/fixtures/r2a_r29/"):
                continue
            for suffix in ("", ".truth"):
                p = os.path.join(LAB, rel + suffix)
                h = hashlib.sha256()
                with open(p, "rb") as fh:
                    h.update(fh.read())
                mf.write("%s  %s\n" % (h.hexdigest(), rel + suffix))
    print("wrote", man_path)

    # ledger sanity
    led = json.load(open(os.path.join(out, "generator_ledger.json")))
    print("ledger trial_total:", led.get("trial_total"))
    assert led.get("trial_total") == 10000

if __name__ == "__main__":
    main()
