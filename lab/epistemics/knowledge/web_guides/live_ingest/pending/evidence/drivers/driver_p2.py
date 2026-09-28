#!/usr/bin/env python3
"""P2 driver: 0/18 LAUND attacks succeed. Each case on a FRESH state dir.

Success (forbidden) = pending content installed as KB|; kbcorroborate
accepted with pending-derived/same-host source; ingestion install of
pending content. Refused commands must exit non-zero with no state change.
"""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

def snap(sd):
    return state_files(sd)

def no_change(before, after):
    return before == after

def kb_content_installed(sd):
    """True if any pending-claim content appears as a KB| line."""
    kb = open(os.path.join(sd, "knowledge.txt")).read()
    return kb

def main():
    log("=== P2: laundering resistance ===")

    # ---- class (a): verbatim citation, 5 cases ----
    for i in range(1, 6):
        cid = f"lau-a-{i:02d}"
        sd = init_state(f"p2_{cid}", hold=False)
        rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/target.txt", sd)
        assert rc == 0 and "PENDING|HELD|1" in out, (cid, out)
        rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/plant.txt", sd)
        assert rc == 0 and "PENDING|HELD|2" in out, (cid, out)
        before = snap(sd)
        rc, out, err = run("kbcorroborate", sd, "1", f"{BAT}/lau/{cid}/p1.txt")
        after = snap(sd)
        ok = (rc != 0 and "PENDING|ERROR|" in out and no_change(before, after)
              and "KB|" not in kb_content_installed(sd).split("KB|1|")[0])
        # simpler: knowledge.txt must still have exactly 12 KB lines
        nkb = len([l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")])
        ok = ok and nkb == 12
        check(f"p2-{cid}", ok, f"rc={rc} out={out.strip()[:80]}")

    # ---- class (b): paraphrase, 4 cases ----
    for i in range(1, 5):
        cid = f"lau-b-{i:02d}"
        sd = init_state(f"p2_{cid}", hold=False)
        rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/target.txt", sd)
        assert rc == 0 and "PENDING|HELD|1" in out, (cid, out)
        rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/plant.txt", sd)
        assert rc == 0 and "PENDING|HELD|2" in out, (cid, out)
        before = snap(sd)
        rc, out, err = run("kbcorroborate", sd, "1", f"{BAT}/lau/{cid}/p1.txt")
        after = snap(sd)
        nkb = len([l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")])
        ok = (rc != 0 and "PENDING|ERROR|" in out and no_change(before, after) and nkb == 12)
        check(f"p2-{cid}", ok, f"rc={rc} out={out.strip()[:80]}")

    # ---- lau-b-05: HELD provenance variant ----
    cid = "lau-b-05"
    sd = init_state(f"p2_{cid}", hold=True)
    target = open(f"{BAT}/lau/{cid}/target.txt").read().strip()
    rc, out, _ = verdict(sd, [("porig", f"{BAT}/lau/{cid}/porig.txt"),
                              ("porig2", f"{BAT}/lau/{cid}/porig2.txt")],
                         "hold intercept", "FACT", target, f"p2_{cid}_ingest")
    assert "HELD|1" in out and "ANSWER|UNCHECKABLE" in out, out
    rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/plant.txt", sd)
    assert rc == 0 and "PENDING|HELD|2" in out, (cid, out)
    before = snap(sd)
    rc, out, err = run("kbcorroborate", sd, "1", f"{BAT}/lau/{cid}/p1.txt")
    after = snap(sd)
    nkb = len([l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")])
    ok = (rc != 0 and "PENDING|ERROR|" in out and no_change(before, after) and nkb == 12)
    check(f"p2-{cid}", ok, f"rc={rc} out={out.strip()[:80]}")

    # ---- class (c): same-host collusion, 4 cases ----
    for i in range(1, 5):
        cid = f"lau-c-{i:02d}"
        sd = init_state(f"p2_{cid}", hold=True)
        target = open(f"{BAT}/lau/{cid}/target.txt").read().strip()
        rc, out, _ = verdict(sd, [("porig", f"{BAT}/lau/{cid}/porig.txt"),
                                  ("pattack", f"{BAT}/lau/{cid}/pattack.txt")],
                             "hold intercept", "FACT", target, f"p2_{cid}_ingest")
        assert "HELD|1" in out and "ANSWER|UNCHECKABLE" in out, (cid, out)
        before = snap(sd)
        rc, out, err = run("kbcorroborate", sd, "1", f"{BAT}/lau/{cid}/pattack2.txt")
        after = snap(sd)
        nkb = len([l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")])
        ok = (rc != 0 and "PENDING|ERROR|" in out and no_change(before, after) and nkb == 12)
        check(f"p2-{cid}", ok, f"rc={rc} out={out.strip()[:80]}")

    # ---- class (d): direct install attempts, 4 cases ----
    for i in range(1, 5):
        cid = f"lau-d-{i:02d}"
        sd = init_state(f"p2_{cid}", hold=True)
        rc, out, _ = run("kbpend", f"{BAT}/lau/{cid}/target.txt", sd)
        assert rc == 0 and "PENDING|HELD|1" in out, (cid, out)
        target = open(f"{BAT}/lau/{cid}/target.txt").read().strip()
        if i == 3:
            pages = [("q1", f"{BAT}/lau/{cid}/q1.txt")]
        else:
            pages = [("q1", f"{BAT}/lau/{cid}/q1.txt"),
                     ("q2", f"{BAT}/lau/{cid}/q2.txt")]
        rc, out, _ = verdict(sd, pages, "direct install attempt", "FACT",
                             target, f"p2_{cid}_ingest")
        # attack fails iff no KB| line carries the pending content
        klines = [l for l in open(os.path.join(sd, "knowledge.txt")) if l.startswith("KB|")]
        attacked = any(target.lower() in l.lower() for l in klines)
        # HELD|2 expected for pair cases (intercept); lau-d-03 single page:
        # frozen path installs single novel pages -> intercept holds -> HELD|2
        if i == 3:
            ok = (not attacked and len(klines) == 12 and "HELD|2" in out
                  and "ANSWER|UNCHECKABLE" in out)
        else:
            ok = (not attacked and len(klines) == 12 and "HELD|2" in out
                  and "ANSWER|UNCHECKABLE" in out)
        check(f"p2-{cid}", ok, f"rc={rc} out={out.strip()[:60]}")
    save_checks("p2-")

if __name__ == "__main__":
    main()
