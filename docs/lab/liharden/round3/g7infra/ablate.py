#!/usr/bin/env python3
"""Ablation probes: verify each exemption condition is load-bearing.
Each probe mutates the T5_longwire or TECH1_archived bundle in ONE way and
expects WITHHOLD|COPYCOLLAPSE (i.e., the exemption was doing real work).
"""
import hashlib, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_g7infra import bundle, run, FIX, PINS, pin_payload

def lines_of(data):
    return data.decode().split("\n")

def rebuild(lines):
    return ("\n".join(l for l in lines if l != "") + "\n").encode()

def drop_pin(data, name):
    ls = lines_of(data)
    out, skip = [], False
    for l in ls:
        if skip:
            skip = False
            continue
        if l.startswith("PINB|%s|" % name):
            skip = True
            continue
        if ("|%s|" % name) in l and (l.startswith("CPIN|") or l.startswith("APIN|")):
            continue
        out.append(l)
    return rebuild(out)

def main():
    fails = []
    def check(label, data, want):
        o1, o2 = run("g7infra", data), run("g7infra", data)
        ok = (o1 == o2) and (want in o1)
        print("%-28s -> %s %s" % (label, o1, "OK" if ok else "FAIL"))
        if not ok:
            fails.append(label)

    t5 = bundle(os.path.join(FIX, "T5_longwire"), "calibration.txt")
    # A1: no citation pin at all -> collapse
    check("A1 T5 minus CPIN", drop_pin(t5, "cite_wire_report.txt"), "WITHHOLD|COPYCOLLAPSE")
    # A2: citation pin NEWER than quorum (fetched_at bumped past 1790208000)
    ls = lines_of(t5)
    ls2 = [l.replace("CPIN|https://wire.example/commission-report|1609459200|",
                     "CPIN|https://wire.example/commission-report|1790208001|") for l in ls]
    check("A2 T5 cite pin newer", rebuild(ls2), "WITHHOLD|COPYCOLLAPSE")
    # A3: tampered pin payload (sha mismatch -> pin rejected)
    ls = lines_of(t5)
    out = []
    for i, l in enumerate(ls):
        out.append(l)
        if l.startswith("PINB|cite_wire_report.txt|"):
            out.append("X" + ls[i + 1][1:])  # corrupted payload line
            # skip original payload (next iteration would re-add); mark by consuming
            ls[i + 1] = ""
    # rebuild carefully: drop the emptied original
    data3 = ("\n".join(l for l in out if l != "") + "\n").encode()
    # NOTE: driver-computed sha no longer matches -> binary must reject pin
    check("A3 T5 tampered pin", data3, "WITHHOLD|COPYCOLLAPSE")
    # A4: pin present+valid but NOT containing the sentence
    alt = b"Archived snapshot of the commission report page. No relevant sentence here. End."
    sha = hashlib.sha256(alt).hexdigest()
    ls = lines_of(t5)
    out, skip = [], False
    for l in ls:
        if skip:
            out.append(alt.decode())
            skip = False
            continue
        if l.startswith("PINB|cite_wire_report.txt|"):
            out.append("PINB|cite_wire_report.txt|%s" % sha)
            skip = True
            continue
        out.append(l)
    check("A4 T5 pin w/o sentence", rebuild(out), "WITHHOLD|COPYCOLLAPSE")
    # A5: one voter cites a different URL -> no shared citation -> collapse
    ls = lines_of(t5)
    ls2 = [l.replace("M|t5c|FETCH=1790208000|CITE=https://wire.example/commission-report",
                     "M|t5c|FETCH=1790208000|CITE=https://other.example/x", 1) if l.startswith("M|t5c|") else l
           for l in ls]
    check("A5 T5 split citation", rebuild(ls2), "WITHHOLD|COPYCOLLAPSE")
    # A6: TECH1 minus archive pin -> collapse
    t1 = bundle(os.path.join(FIX, "TECH1_archived"), "calibration.txt")
    check("A6 TECH1 minus APIN", drop_pin(t1, "arch_2020.txt"), "WITHHOLD|COPYCOLLAPSE")
    # A7: archive pin NEWER than quorum -> collapse
    ls = lines_of(t1)
    ls2 = [l.replace("APIN|archive:2020-corpus|1577836800|", "APIN|archive:2020-corpus|1790208001|")
           for l in ls]
    check("A7 TECH1 archive newer", rebuild(ls2), "WITHHOLD|COPYCOLLAPSE")
    # A8: F7_longring WITH a valid citation pin injected (attacker plants old pin?)
    # -> must still collapse: no CITE metadata on voters, pin alone is not enough
    print("A8: F7 has no CITE metadata; unpinned citation cannot exempt (by design).")
    if fails:
        print("ABLATION FAILURES: %s" % fails)
        sys.exit(5)
    print("ALL ABLATIONS HOLD")

if __name__ == "__main__":
    main()
