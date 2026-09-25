#!/usr/bin/env python3
"""P3 driver: 8/8 HON promote (KB install + RESOLVE|KB|CORROBORATED),
4/4 REFUTE demote (REJ|CONTRADICTED + RESOLVE|REJ)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

def main():
    log("=== P3: honest resolution ===")
    sd = init_state("p3", hold=False)
    # kbpend the 8 HON claims
    for i in range(1, 9):
        cid = f"hon-{i:02d}"
        rc, out, err = run("kbpend", f"{BAT}/hon/{cid}/claim.txt", sd)
        assert rc == 0 and f"PENDING|HELD|{i}" in out, (cid, rc, out, err)
    # kbcorroborate each with p2
    for i in range(1, 9):
        cid = f"hon-{i:02d}"
        rc, out, err = run("kbcorroborate", sd, str(i), f"{BAT}/hon/{cid}/p2.txt")
        ok = (rc == 0 and f"PENDING|PROMOTED|{i}|" in out)
        if not ok:
            log(f"  {cid} corroborate failed: rc={rc} out={out.strip()[:120]}")
        check(f"p3-{cid}", ok, f"rc={rc}")
    # verify knowledge.txt has the 8 installed + resolutions
    kb = open(os.path.join(sd, "knowledge.txt")).read()
    nkb = len([l for l in kb.split("\n") if l.startswith("KB|")])
    check("p3-kb-count", nkb == 20, f"knowledge.txt KB lines={nkb} (12+8)")
    res = open(os.path.join(sd, "resolutions.txt")).read()
    ncorr = res.count("|KB|CORROBORATED|")
    check("p3-corroborated", ncorr == 8, f"CORROBORATED lines={ncorr}")

    # REFUTE: fresh state
    sd2 = init_state("p3r", hold=False)
    for i in range(1, 5):
        cid = f"ref-{i:02d}"
        rc, out, err = run("kbpend", f"{BAT}/ref/{cid}/claim.txt", sd2)
        assert rc == 0 and f"PENDING|HELD|{i}" in out, (cid, rc, out, err)
    expected = [
        "CONTRADICTED:measure-review.example:Millau Viaduct height check",
        "CONTRADICTED:height-audit.example:Tokyo Skytree height audit",
        "CONTRADICTED:hull-survey.example:Ever Given length survey",
        "CONTRADICTED:capacity-check.example:Rungrado capacity check",
    ]
    for i in range(1, 5):
        cid = f"ref-{i:02d}"
        rc, out, err = run("kbrefute", sd2, str(i), f"{BAT}/ref/{cid}/p3.txt")
        ok = (rc == 0 and f"PENDING|DEMOTED|{i}|" in out)
        if not ok:
            log(f"  {cid} refute failed: rc={rc} out={out.strip()[:150]}")
        check(f"p3-{cid}", ok, f"rc={rc}")
    rej = open(os.path.join(sd2, "rejections.txt")).read()
    for i, exp in enumerate(expected, 1):
        check(f"p3-ref-reason-{i}", exp in rej, exp[:50])
    nrej = len([l for l in rej.split("\n") if l.startswith("REJ|")])
    check("p3-rej-count", nrej == 4, f"REJ lines={nrej}")
    # refuted claims never installed
    kb2 = open(os.path.join(sd2, "knowledge.txt")).read()
    nkb2 = len([l for l in kb2.split("\n") if l.startswith("KB|")])
    check("p3-no-install", nkb2 == 12, f"knowledge.txt KB lines={nkb2}")
    save_checks("p3-")

if __name__ == "__main__":
    main()
