#!/usr/bin/env python3
"""P6 driver: hold-intercept end-to-end.
HOLD ON:  3 shapes -> HELD|1 + ANSWER|UNCHECKABLE, pending provenance HELD:<host>
HOLD OFF: 3 shapes -> frozen factual answers, no pending claim written.
Shapes: same-host collusion, distinct-host verbatim pair, distinct-host Storebaelt pair."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/pending-run"))
from harness import *

set_passdir(sys.argv[1])

def pages_for(shape):
    if shape == "same-host":
        # lau-c-01 porig + pattack (same host)
        return [("porig", f"{BAT}/lau/lau-c-01/porig.txt"),
                ("pattack", f"{BAT}/lau/lau-c-01/pattack.txt")], \
               "The Akashi Kaikyo Bridge central span is 1991 meters."
    if shape == "verbatim":
        # hon-01 p1 + p2 (distinct hosts, verbatim claim)
        return [("p1", f"{BAT}/hon/hon-01/p1.txt"),
                ("p2", f"{BAT}/hon/hon-01/p2.txt")], \
               "The Golden Gate Bridge has a main span of 1280 meters."
    if shape == "storebaelt":
        # lau-b-05 porig + porig2 (distinct hosts)
        return [("porig", f"{BAT}/lau/lau-b-05/porig.txt"),
                ("porig2", f"{BAT}/lau/lau-b-05/porig2.txt")], \
               "The Storebaelt Bridge east span reaches 1624 meters in total."
    raise ValueError(shape)

def main():
    log("=== P6: hold intercept ===")
    for shape in ["same-host", "verbatim", "storebaelt"]:
        pages, query = pages_for(shape)
        # HOLD ON
        sd = init_state(f"p6_on_{shape}", hold=True)
        rc, out, err = verdict(sd, pages, "hold intercept", "FACT", query, f"p6_on_{shape}")
        held = "HELD|1" in out
        unchk = "ANSWER|UNCHECKABLE" in out
        pend = [l for l in open(os.path.join(sd, "pending.txt")) if l.startswith("PENDING|")]
        prov_ok = len(pend) == 1 and ":HELD:" in pend[0] or "HELD:" in pend[0]
        ok = held and unchk and len(pend) == 1 and "HELD:" in pend[0]
        if not ok:
            log(f"  ON {shape}: out={out[:120]} pend={pend}")
        check(f"p6-on-{shape}", ok and rc == 0, f"rc={rc}")
        # HOLD OFF: frozen factual answer, no pending
        sd2 = init_state(f"p6_off_{shape}", hold=False)
        rc, out, err = verdict(sd2, pages, "hold intercept", "FACT", query, f"p6_off_{shape}")
        # Frozen factual answer: should contain ANSWER| with the fact (not UNCHECKABLE)
        has_answer = "ANSWER|" in out and "UNCHECKABLE" not in out
        pend2 = []
        pp = os.path.join(sd2, "pending.txt")
        if os.path.exists(pp):
            pend2 = [l for l in open(pp) if l.startswith("PENDING|")]
        ok2 = has_answer and len(pend2) == 0
        if not ok2:
            log(f"  OFF {shape}: out={out[:200]} pend={len(pend2)}")
        check(f"p6-off-{shape}", ok2, f"rc={rc}")
    save_checks("p6-")

if __name__ == "__main__":
    main()
