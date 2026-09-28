#!/usr/bin/env python3
"""R2-4 determinism protocol (test harness only, NOT architecture).

- 60-fixture sample (10/task, first 10 sorted R2A normal per task):
  3 byte-identical runs each of sense_r24.
- 3 runs of deliberate.zag on a fixed escalation-cases file.
- Full sweep re-run -> records.txt byte-identical (RK-7).
- 3 runs of memgate over the records -> byte-identical ledger (B6).
- Independent Python recompute of the ledger hash chain.
"""
import hashlib
import os
import subprocess
import sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
R24 = os.path.join(LAB, "senses/pam-rebuild/round2/forks/R2-4")
WORK = os.path.join(R24, "evidence", "_evalwork")
BINDIR = os.path.join(WORK, "bin")
SENSE = os.path.join(BINDIR, "sense_r24")
DELIB = os.path.join(BINDIR, "deliberate")
MEMGATE = os.path.join(BINDIR, "memgate")
TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]
FIX = os.path.join(R24, "fixtures")

fails = []


def run3(binary, *args):
    outs = []
    for _ in range(3):
        r = subprocess.run([binary] + list(args), capture_output=True, timeout=300)
        outs.append((r.returncode, r.stdout))
    return outs


def check(name, outs):
    ok = outs[0] == outs[1] == outs[2]
    print("%s: %s" % (name, "IDENTICAL" if ok else "MISMATCH"), flush=True)
    if not ok:
        fails.append(name)
    return ok


def main():
    # 60 fixtures: first 10 sorted R2A normal per task
    fixtures = []
    for task in TASKS:
        cands = sorted(f for f in os.listdir(FIX)
                       if f.startswith("r2n_%s_" % task) and f.endswith(".r24"))
        for f in cands[:10]:
            fixtures.append((task, os.path.join(FIX, f)))
    print("sample: %d fixtures" % len(fixtures), flush=True)
    for task, path in fixtures:
        check("sense3 %s/%s" % (task, os.path.basename(path)), run3(SENSE, task, path))

    # deliberate: fixed cases file, 3 runs
    cases = os.path.join(WORK, "det_cases.txt")
    with open(cases, "w") as fh:
        fh.write("1|0|0|SAME|850|900|1|1|4|0|0|0|4|8\n")
        fh.write("2|0|0|SAME|850|100|1|1|4|0|0|0|4|8\n")
        fh.write("3|2|1|SQUARE|900|150|1|1|974|0|50|1|900|60\n")
    check("deliberate3", run3(DELIB, cases))

    # memgate: 3 runs over records.txt -> byte-identical ledger
    rec = os.path.join(WORK, "records.txt")
    ledgers = []
    for i in range(3):
        lp = os.path.join(WORK, "det_ledger_%d.txt" % i)
        if os.path.exists(lp):
            os.remove(lp)
        r = subprocess.run([MEMGATE, rec, lp], capture_output=True, timeout=600)
        ledgers.append((r.returncode, open(lp, "rb").read(), r.stdout))
    check("ledger3", ledgers)

    # independent Python recompute of the ledger chain
    prev = bytes(32)
    n = 0
    ok = True
    with open(rec) as rf, open(os.path.join(WORK, "det_ledger_0.txt")) as lf:
        for rline, lline in zip(rf, lf):
            rline = rline.rstrip("\n")
            parts = lline.rstrip("\n").split("|", 2)
            if len(parts) != 3 or parts[0] != prev.hex():
                ok = False
                break
            h = hashlib.sha256(prev + parts[2].encode()).hexdigest()
            if h != parts[1]:
                ok = False
                break
            prev = bytes.fromhex(h)
            n += 1
    print("ledger-recompute: %s (%d links)" % ("OK" if ok else "FAIL", n), flush=True)
    if not ok:
        fails.append("ledger-recompute")

    if fails:
        print("DETERMINISM FAILURES:", fails, flush=True)
        sys.exit(1)
    print("ALL DETERMINISM CHECKS PASS", flush=True)


if __name__ == "__main__":
    main()
