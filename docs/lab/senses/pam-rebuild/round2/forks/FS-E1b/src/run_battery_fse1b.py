#!/usr/bin/env python3
"""run_battery_fse1b.py -- FS-E1b full battery driver.

For each (battery, mode): runs the fse1 binary's runlist TWICE into
evidence/, byte-compares the two runs (ledger + stdout), and verifies the
hash chain. Any mismatch or chain failure aborts with nonzero status.

NOTE: the runlist "union" mode exercises the FS-E1 mechanism (run_challenge
dispatches to the modified cc_chal/mo_chal and the pure-agreement
chal_supports); the mode label is inherited from R2-16. Verified identical
to `full` mode on sample fixtures.

Batteries: b_adv (10k R2A adversarial), b_ctrl (2k R2A controls), from
R2-16's evidence/*.list (frozen).

Output: evidence/batt_<b>_<mode>_r{1,2}.{ledger,stdout}
"""
import subprocess, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
R16EV = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-16/evidence"
BIN = os.path.join(FORK, "build", "fse1b")
EV = os.path.join(FORK, "evidence")
JOBS = [
    ("b_adv", "union"),
    ("b_ctrl", "union"),
]

def run(cmd, outpath):
    with open(outpath, "w") as out:
        r = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit("FAILED: %s (rc=%d)" % (" ".join(cmd), r.returncode))

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def main():
    only = sys.argv[1:]
    os.makedirs(EV, exist_ok=True)
    for batt, mode in JOBS:
        if only and batt not in only and "%s:%s" % (batt, mode) not in only:
            continue
        lst = os.path.join(R16EV, batt + ".list")
        n = sum(1 for _ in open(lst))
        if n == 0:
            print("SKIP %s %s (empty list)" % (batt, mode))
            continue
        print("RUN %s %s n=%d" % (batt, mode, n), flush=True)
        outs = []
        for rep in (1, 2):
            led = os.path.join(EV, "batt_%s_%s_r%d.ledger" % (batt, mode, rep))
            so = os.path.join(EV, "batt_%s_%s_r%d.stdout" % (batt, mode, rep))
            run([BIN, "runlist", lst, led, mode], so)
            outs.append((led, so))
        for kind in (0, 1):
            a, b = outs[0][kind], outs[1][kind]
            if sha(a) != sha(b):
                raise SystemExit("MISMATCH: %s vs %s" % (a, b))
            print("  cmp %s: IDENTICAL" % ("ledger" if kind == 0 else "stdout"))
        # chain verify (inline, same formula as R2-16 verify_chain.py)
        led = outs[0][0]
        prev = b"0" * 64
        ln = 0
        for raw in open(led, "rb"):
            line = raw.rstrip(b"\n")
            if not line:
                continue
            i = line.rfind(b" hash=")
            assert i > 0
            content, h = line[:i], line[i + 6:]
            calc = hashlib.sha256(bytes.fromhex(prev.decode()) + content).hexdigest()
            assert calc.encode() == h, "chain break at line %d" % ln
            prev = h
            ln += 1
        assert ln == n, (ln, n)
        print("  chain: OK lines=%d" % ln)
    print("BATTERY-COMPLETE")

if __name__ == "__main__":
    main()
