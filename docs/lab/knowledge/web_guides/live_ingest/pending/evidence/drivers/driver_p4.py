#!/usr/bin/env python3
"""P4 driver: 4/4 TESTC resolve with frozen provenance.
PASS -> RESOLVE|<seq>|KB|TESTED|<proto>; FAIL -> REJ|TEST-FAILED|<proto>.
Expects exactly 2 TESTED and 2 test failures (tst-03, tst-04 per battery).
Also runs the check programs to confirm exit codes."""
import os, sys, subprocess
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

TST = {
    "tst-01": ("PRIME-IDX", "check_prime_idx.py", 0),
    "tst-02": ("POW2", "check_pow2.py", 0),
    "tst-03": ("FIB-IDX", "check_fib_idx.py", 1),
    "tst-04": ("DIGSUM", "check_digsum.py", 1),
}

def main():
    log("=== P4: test provenance ===")
    # confirm check programs' exit codes first
    for cid, (proto, script, exp_rc) in TST.items():
        d = f"{BAT}/tst/{cid}"
        r = subprocess.run([sys.executable, f"{BAT}/tst/checks/{script}",
                            f"{d}/fixture_input.txt"],
                           capture_output=True, text=True)
        check(f"p4-{cid}-check", r.returncode == exp_rc,
              f"{script} rc={r.returncode} expect={exp_rc}")

    sd = init_state("p4", hold=False)
    for i, cid in enumerate(["tst-01", "tst-02", "tst-03", "tst-04"], 1):
        rc, out, err = run("kbpend", f"{BAT}/tst/{cid}/claim.txt", sd)
        assert rc == 0 and f"PENDING|HELD|{i}" in out, (cid, rc, out, err)
    # kbtest: tst-01 PASS, tst-02 PASS, tst-03 FAIL, tst-04 FAIL
    plan = [("tst-01", "PASS"), ("tst-02", "PASS"), ("tst-03", "FAIL"), ("tst-04", "FAIL")]
    for idx, (cid, result) in enumerate(plan, 1):
        proto = TST[cid][0]
        rc, out, err = run("kbtest", sd, str(idx), result, proto)
        assert rc == 0, (cid, rc, out, err)
        log(f"  {cid} {result}: {out.strip().split(chr(10))[0]}")
    res = open(os.path.join(sd, "resolutions.txt")).read()
    ntested = res.count("|KB|TESTED|")
    check("p4-tested-count", ntested == 2, f"TESTED lines={ntested}")
    rej = open(os.path.join(sd, "rejections.txt")).read()
    nfail = rej.count("TEST-FAILED")
    check("p4-fail-count", nfail == 2, f"TEST-FAILED lines={nfail}")
    # TESTED byte-distinguishable from CORROBORATED (kind field differs)
    tested_lines = [l for l in res.split("\n") if "|KB|TESTED|" in l]
    corr_lines = [l for l in res.split("\n") if "|KB|CORROBORATED|" in l]
    check("p4-kind-distinct", len(tested_lines) == 2 and len(corr_lines) == 0,
          f"tested={len(tested_lines)} corroborated={len(corr_lines)}")
    # installed claims for the two PASS
    kb = open(os.path.join(sd, "knowledge.txt")).read()
    nkb = len([l for l in kb.split("\n") if l.startswith("KB|")])
    check("p4-kb-count", nkb == 14, f"KB lines={nkb} (12+2)")
    save_checks("p4-")

if __name__ == "__main__":
    main()
