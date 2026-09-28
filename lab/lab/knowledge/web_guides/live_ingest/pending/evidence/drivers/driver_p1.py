#!/usr/bin/env python3
"""P1 driver: 0/24 RECALL probes return installed-fact."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

def main():
    log("=== P1: pending-recall separation ===")
    sd = init_state("p1", hold=False)
    for i in range(1, 9):
        cid = f"hon-{i:02d}"
        rc, out, err = run("kbpend", f"{BAT}/hon/{cid}/claim.txt", sd)
        assert rc == 0 and f"PENDING|HELD|{i}" in out, (cid, rc, out, err)
    log("8 HON claims pended")
    for i in range(1, 25):
        cid = f"rec-{i:02d}"
        title, host, sents = battery_page(f"{BAT}/rec/{cid}/p1.txt")
        probe = sents[0]
        rc, out, err = verdict(sd, [("p1", f"{BAT}/rec/{cid}/p1.txt")],
                               "recall probe", "FACT", probe, f"p1_{cid}")
        kblines = [l for l in out.split("\n") if l.startswith("KB|")]
        installed_fact = bool(kblines)
        low = out.lower()
        for c in KB:
            if f"answer|{c.lower()}" in low:
                installed_fact = True
        if installed_fact:
            log(f"  {cid} LEAK: {out[:200]}")
        check(f"p1-{cid}", not installed_fact, f"rc={rc}")
    save_checks("p1-")

if __name__ == "__main__":
    main()
