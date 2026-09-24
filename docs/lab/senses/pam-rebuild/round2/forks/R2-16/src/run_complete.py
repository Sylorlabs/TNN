#!/usr/bin/env python3
"""run_complete.py -- R2-16 completion battery driver.

For each (battery, mode): runs the r216 binary's runlist TWICE into
evidence/, byte-compares the two runs (ledger + stdout via SHA256),
and verifies the hash chain. Any mismatch or chain failure aborts
with nonzero status.

Usage: run_complete.py [batt:mode ...]   (default: all JOBS)
Output: evidence/batt_<b>_<mode>_r{1,2}.{ledger,stdout}

Deterministic; no RNG. Pure glue around the frozen binary.
"""
import subprocess, os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
BIN = os.path.join(FORK, "build", "r216")
EV = os.path.join(FORK, "evidence")
JOBS = [
    ("b_adv", "union"), ("b_ctrl", "union"), ("b_holdout", "union"),
]

def run(cmd, outpath):
    with open(outpath, "w") as out:
        r = subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT)
    if r.returncode != 0:
        raise SystemExit("FAILED: %s (rc=%d)" % (" ".join(cmd), r.returncode))

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    only = sys.argv[1:]
    for batt, mode in JOBS:
        if only and batt not in only and "%s:%s" % (batt, mode) not in only:
            continue
        lst = os.path.join(EV, batt + ".list")
        n = sum(1 for _ in open(lst))
        if n == 0:
            print("SKIP %s %s (empty list)" % (batt, mode), flush=True)
            continue
        print("RUN %s %s n=%d" % (batt, mode, n), flush=True)
        outs = []
        for rep in (1, 2):
            led = os.path.join(EV, "batt_%s_%s_r%d.ledger" % (batt, mode, rep))
            so = os.path.join(EV, "batt_%s_%s_r%d.stdout" % (batt, mode, rep))
            run([BIN, "runlist", lst, led, mode], so)
            outs.append((led, so))
            print("  r%d ledger_sha=%s stdout_sha=%s" % (rep, sha(led), sha(so)), flush=True)
        for kind, kname in ((0, "ledger"), (1, "stdout")):
            a, b = outs[0][kind], outs[1][kind]
            if sha(a) != sha(b):
                raise SystemExit("MISMATCH: %s vs %s" % (a, b))
            print("  cmp %s: IDENTICAL" % kname, flush=True)
        # chain verify (same formula as verify_chain.py / builder's driver)
        led = outs[0][0]
        prev = b"0" * 64
        ln = 0
        with open(led, "rb") as f:
            for raw in f:
                line = raw.rstrip(b"\n")
                if not line:
                    continue
                i = line.rfind(b" hash=")
                assert i > 0, "no hash tag at line %d" % ln
                content, h = line[:i], line[i + 6:]
                calc = hashlib.sha256(bytes.fromhex(prev.decode()) + content).hexdigest()
                assert calc.encode() == h, "chain break at line %d" % ln
                prev = h
                ln += 1
        assert ln == n, (ln, n)
        print("  chain: OK lines=%d" % ln, flush=True)
    print("BATTERY-COMPLETE")

if __name__ == "__main__":
    main()
