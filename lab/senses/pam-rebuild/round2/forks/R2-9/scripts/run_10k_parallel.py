#!/usr/bin/env python3
"""Run the 10k battery in parallel (N workers).
Each worker runs: sense batch <chunk_trials.tsv> <chunk_outdir> <emit|noemit>
Merges percepts (sorted by trial_id) and concatenates ledgers.
Usage: run_10k_parallel.py <emit|noemit> <run_id> [nworkers=10]
cwd must be ~/workspace/tnn-lab (fixture paths are lab-relative).
Output: work/battery10k_<mode>_<run_id>/percepts.tsv, LEDGER.jsonl (merged)
Pure glue.
"""
import os, sys, subprocess, shutil

LAB = os.path.expanduser("~/workspace/tnn-lab")
FORK = os.path.join(LAB, "senses", "pam-rebuild", "round2", "forks", "R2-9")
R2A = os.path.join(LAB, "senses", "pam-rebuild", "round2", "fixtures", "r2a_r29")
BIN = os.path.join(FORK, "work", "sense")

def main():
    mode = sys.argv[1]
    run_id = sys.argv[2]
    nw = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    with open(os.path.join(R2A, "trials.tsv")) as f:
        header = f.readline()
        rows = f.readlines()
    assert len(rows) == 10000, len(rows)

    chunk_size = (len(rows) + nw - 1) // nw
    workdir = os.path.join(FORK, "work", "battery10k_%s_%s" % (mode, run_id))
    os.makedirs(workdir, exist_ok=True)

    # launch workers
    procs = []
    for w in range(nw):
        chunk = rows[w*chunk_size:(w+1)*chunk_size]
        if not chunk:
            continue
        cdir = os.path.join(workdir, "w%02d" % w)
        os.makedirs(cdir, exist_ok=True)
        ctrials = os.path.join(cdir, "trials.tsv")
        with open(ctrials, "w") as f:
            f.write(header)
            f.writelines(chunk)
        cout = os.path.join(cdir, "out")
        log = open(os.path.join(cdir, "run.log"), "w")
        p = subprocess.Popen([BIN, "batch", ctrials, cout, mode],
                             stdout=log, stderr=subprocess.STDOUT, cwd=LAB)
        procs.append((w, p, cdir, cout, log))
        print("launched worker %d (%d trials)" % (w, len(chunk)), flush=True)

    # wait
    failed = []
    for w, p, cdir, cout, log in procs:
        rc = p.wait()
        log.close()
        with open(os.path.join(cdir, "run.log")) as f:
            last = f.read().strip().splitlines()
            last = last[-1] if last else "(no output)"
        print("worker %d done rc=%d: %s" % (w, rc, last), flush=True)
        if rc != 0:
            failed.append(w)
    if failed:
        print("FAILED workers: %s" % failed, flush=True)
        return 1

    # merge percepts (sort by trial_id for determinism)
    all_rows = []
    for w, p, cdir, cout, log in procs:
        pp = os.path.join(cout, "percepts.tsv")
        with open(pp) as f:
            h = f.readline()
            for line in f:
                all_rows.append(line)
    # sort by trial_id (first column)
    all_rows.sort(key=lambda l: l.split("\t", 1)[0])
    with open(os.path.join(workdir, "percepts.tsv"), "w") as f:
        f.write(h)
        f.writelines(all_rows)
    print("merged percepts: %d rows" % len(all_rows), flush=True)

    # merge ledgers (concatenate; each worker's chain is intact)
    with open(os.path.join(workdir, "LEDGER.jsonl"), "w") as out:
        for w, p, cdir, cout, log in procs:
            lp = os.path.join(cout, "LEDGER.jsonl")
            if os.path.exists(lp):
                with open(lp) as f:
                    shutil.copyfileobj(f, out)
    print("merged ledgers", flush=True)
    print("ALL DONE", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
