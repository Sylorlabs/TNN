#!/usr/bin/env python3
"""PAM fork H2 — B6 determinism protocol (test harness only, NOT architecture).

60-fixture sample (10/task from frozen primary), 3 byte-identical runs each
of sense_h2; 3 runs of memgate over the 60-record stream with byte-identical
ledgers; independent Python recompute of the ledger; 3 byte-identical runs of
the rebuilt Approach-A binary on the same 60.
"""
import hashlib
import os
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
H2 = os.path.join(LAB, "senses/pam-rebuild/forks/H2")
HARN = os.path.join(LAB, "senses/rebuild/harness/fixtures")
SENSE_H2 = os.path.join(H2, "src/sense_h2")
SENSE_A = os.path.join(LAB, "senses/rebuild/a_raw/sense")
MEMGATE = os.path.join(H2, "src/memgate")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
TSUB = ["t1_colordisc", "t2_colorconst", "t3_shapetrans",
        "t4_pitchdisc", "t5_timbredisc", "motiondir".replace("motiondir", "t6_motiondir")]
WORK = os.path.join(H2, "evidence", "_evalwork")
os.makedirs(WORK, exist_ok=True)

fails = []


def run3(binary, task, path):
    outs = []
    for _ in range(3):
        r = subprocess.run([binary, task, path], capture_output=True, timeout=300)
        outs.append((r.returncode, r.stdout))
    return outs


def main():
    # 60 fixtures: first 10 sorted of each task's frozen primary
    fixtures = []
    for ti, task in enumerate(TASKS):
        d = os.path.join(HARN, TSUB[ti], "primary")
        fs = sorted(f for f in os.listdir(d) if not f.endswith(".truth"))[:10]
        for f in fs:
            fixtures.append((task, os.path.join(d, f), f))
    assert len(fixtures) == 60, len(fixtures)

    # 1. sense_h2 x3 byte-identical on each
    h2_recs = []
    for task, path, f in fixtures:
        outs = run3(SENSE_H2, task, path)
        if not all(o == outs[0] for o in outs) or outs[0][0] != 0:
            fails.append(("sense_h2", f))
        kv = {}
        for line in outs[0][1].decode().splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                kv[k.strip()] = v.strip()
        progline = kv.get("program", "")
        phash = hashlib.sha256(progline.encode()).hexdigest()
        truth = open(path + ".truth").read().strip().split("=", 1)[1]
        progmap = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
        jcode = {"SAME": 0, "DIFFERENT": 1, "SAME_SURFACE": 2, "LIGHT_CHANGED": 3,
                 "CIRCLE": 4, "SQUARE": 5, "TRIANGLE": 6, "HIGHER": 7, "LOWER": 8,
                 "PURE": 9, "BRIGHT": 10, "DULL": 11, "LEFT": 12, "RIGHT": 13,
                 "STILL": 14, "UNKNOWN": 15}.get(kv.get("judgment"), 99)
        h2_recs.append("%d|%d|%s|%d|%d|%s|%s|%s|%s|%s|%s" % (
            len(h2_recs), TASKS.index(task), f, progmap.get(kv.get("prog"), 2),
            jcode, kv.get("judgment"), kv.get("confidence"), kv.get("pred"),
            kv.get("measure"), phash, truth))
    print("sense_h2 3x byte-identical: %d/60 ok" % (60 - len(fails)), flush=True)

    # 2. A x3 byte-identical on each
    a_fails = 0
    for task, path, f in fixtures:
        outs = run3(SENSE_A, task, path)
        if not all(o == outs[0] for o in outs) or outs[0][0] != 0:
            a_fails += 1
            fails.append(("approachA", f))
    print("approach-A 3x byte-identical: %d/60 ok" % (60 - a_fails), flush=True)

    # 3. memgate x3 on the 60-record stream, ledger byte-identical
    rec_path = os.path.join(WORK, "det_records.txt")
    with open(rec_path, "w") as fh:
        fh.write("\n".join(h2_recs) + "\n")
    ledgers = []
    for i in range(3):
        lp = os.path.join(WORK, "det_ledger_%d.txt" % i)
        r = subprocess.run([MEMGATE, rec_path, lp], capture_output=True, timeout=120)
        assert r.returncode == 0, r.stderr.decode()[:300]
        ledgers.append(open(lp, "rb").read())
    lg_ok = ledgers[0] == ledgers[1] == ledgers[2]
    if not lg_ok:
        fails.append(("memgate-ledger", "byte-mismatch"))
    print("memgate ledger 3x byte-identical: %s" % lg_ok, flush=True)

    # 4. independent ledger recompute
    prev = "0" * 64
    n = 0
    indep_ok = True
    for line in ledgers[0].decode().splitlines():
        p, h, canon = line.split("|", 2)
        if p != prev:
            indep_ok = False
            break
        if hashlib.sha256(bytes.fromhex(p) + canon.encode()).hexdigest() != h:
            indep_ok = False
            break
        prev = h
        n += 1
    if not indep_ok:
        fails.append(("ledger-recompute", "mismatch"))
    print("independent ledger recompute: %s (%d links)" % (indep_ok, n), flush=True)

    print("B6 determinism protocol: %s" % ("PASS" if not fails else "FAIL %r" % fails), flush=True)
    return 1 if fails else 0


sys.exit(main())
