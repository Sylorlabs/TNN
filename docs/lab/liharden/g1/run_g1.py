#!/usr/bin/env python3
"""g1 production battery driver (PREREG_G1.md kill bars K1-K8).

For each fixture: extract the most-common non-TITLE sentence across its pages
as the claim (proxy for the quorum's voted claim), feed it to g1_bin with the
era pin set and tentative=INSTALL, run twice, check byte-identity and the
expected decision.
"""
import os, subprocess, sys
from collections import Counter

W = os.path.expanduser("~/workspace/liharden/g1_build")
BIN = os.path.join(W, "g1_bin")
CORROB = os.path.expanduser("~/workspace/liharden/corrob/fixtures")
BEYOND = os.path.expanduser("~/workspace/liharden/beyond/fixtures")

HONEST = ["H1_three_host","H2_four_host","H3_six_host","H4_paraphrase_agree",
          "H5_range_format","H6_numeric","H7_range_agree","H8_wire_truth",
          "H9_filler_diverse","H10_punct_variant","H11_claim_second","H12_numeric2"]

def claim_of(casedir):
    c = Counter()
    pdir = os.path.join(casedir, "pages")
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".txt"): continue
        for line in open(os.path.join(pdir, fn)):
            line = line.strip()
            if not line or line.startswith("TITLE:"): continue
            c[line] += 1
    return c.most_common(1)[0][0] if c else ""

def run(pin, tentative, claim):
    outs = []
    for _ in range(2):
        p = subprocess.run([BIN, pin, tentative, claim], capture_output=True, text=True)
        outs.append(p.stdout.strip())
    return outs

def main():
    v1 = os.path.join(W, "pins", "pinset_v1.txt")
    v2 = os.path.join(W, "pins", "pinset_v2.txt")
    fails = []
    rows = []
    def check(name, outs, expect):
        ok_det = outs[0] == outs[1]
        ok_exp = outs[0].startswith(expect)
        rows.append((name, outs[0], "PASS" if (ok_det and ok_exp) else "FAIL"))
        if not (ok_det and ok_exp):
            fails.append((name, outs, expect))

    # K1: F1_sydney + v1 -> ARCHVETO
    check("K1 F1_sydney+v1", run(v1, "INSTALL", claim_of(os.path.join(BEYOND,"F1_sydney"))),
          "V|g1|WITHHOLD|ARCHVETO")
    # K2: 12/12 honest + v1 -> PASS
    for h in HONEST:
        check("K2 "+h+"+v1", run(v1, "INSTALL", claim_of(os.path.join(CORROB,h))),
              "V|g1|PASS")
    # K3: T4 + v2 -> PASS ; K4: T4 + v1 -> ARCHVETO
    t4c = claim_of(os.path.join(BEYOND,"T4_supersede"))
    check("K3 T4+v2", run(v2, "INSTALL", t4c), "V|g1|PASS")
    check("K4 T4+v1-stale", run(v1, "INSTALL", t4c), "V|g1|WITHHOLD|ARCHVETO")
    # boundary: F_H_WIRE + v1 -> PASS
    check("F_H_WIRE+v1", run(v1, "INSTALL", claim_of(os.path.join(BEYOND,"F_H_WIRE"))),
          "V|g1|PASS")
    # extension probes
    check("G1-FORM2", run(v1, "INSTALL", "The capital of Australia is Sydney."),
          "V|g1|WITHHOLD|ARCHVETO")
    check("G1-MERCURY", run(v1, "INSTALL", "Mercury is the closest planet to the sun."),
          "V|g1|PASS")
    check("G1-NONCLASS", run(v1, "INSTALL", "Is the vault open?"), "V|g1|PASS")
    # K7: tampered pinset -> PINFAIL everywhere, never PASS
    tam = os.path.join(W, "pins", "pinset_v1_tampered.txt")
    txt = open(v1).read()
    lines = txt.split("\n")
    for i,l in enumerate(lines):
        if l.startswith("REC|"):
            lines[i] = l[:20] + ("0" if l[20]!="0" else "1") + l[21:]
            break
    open(tam,"w").write("\n".join(lines))
    for nm, cl in (("K7 tamper/F1", "Sydney is the capital of Australia."),
                   ("K7 tamper/H8", "The capital of Australia is Canberra."),
                   ("K7 tamper/nonclass", "Is the vault open?")):
        check(nm, run(tam, "INSTALL", cl), "V|g1|WITHHOLD|PINFAIL")

    print("case\tverdict\tresult")
    for name, v, r in rows:
        print("%s\t%s\t%s" % (name, v, r))
    print("----")
    print("total=%d fail=%d" % (len(rows), len(fails)))
    for name, outs, expect in fails:
        print("FAIL", name, outs, "expected-prefix", expect)
    return 1 if fails else 0

sys.exit(main())
