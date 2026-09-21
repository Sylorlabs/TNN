#!/usr/bin/env python3
"""Build the four scripted decision histories for arm-3 varB verification.

Reads turn-1 proposals (empty history -> 8 INTRODUCE WORD_SPANs, seqs 0-7)
and writes:
  hist_adopt4.bin : seqs 0-3 ADOPT            -> expect CORROBORATE
  hist_adopt8.bin : seqs 0-7 ADOPT            -> expect RELATE
  hist_reject.bin : seqs 0-7 REJECT R1        -> expect INTRODUCE (fresh region)
  hist_consol.bin : seqs 0-5 ADOPT; 6,7 = seq6-span REJECT R1 x2;
                    8 = seq7-span ADOPT; 9,10 = seq7-span REJECT R1 x2
                    -> expect CONSOLIDATE with 2 RETRACTs

Usage: gen_hist.py <turn1_proposals.bin> <outdir>
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from props import parse_stream, write_history

ADOPT, REVISE, REJECT, DEFER = 0, 1, 2, 3
R1 = 1

def main():
    t1_path, outdir = sys.argv[1], sys.argv[2]
    stim = open(os.path.join(outdir, "stimulus.txt"), "rb").read()
    with open(t1_path, "rb") as f:
        t1 = parse_stream(f.read(), len(stim), expect_sess=1001, expect_seq0=0)
    assert len(t1) == 8 and all(p["kind"] == 1 for p in t1), \
        f"turn1 must be 8 WORD_SPANs, got {len(t1)}"
    spans = [(p["ss"], p["se"]) for p in t1]

    def rec(seq, kind, verdict, reason, ss, se):
        return (seq, kind, verdict, reason, ss, se)

    # adopt4: 4 adoptions -> CORROBORATE (adopt10=4>=3, adopted=4<5)
    h_adopt4 = [rec(i, 1, ADOPT, 0, *spans[i]) for i in range(4)]
    # adopt8: 8 adoptions -> RELATE (adopted=8>=5)
    h_adopt8 = [rec(i, 1, ADOPT, 0, *spans[i]) for i in range(8)]
    # reject: 8 consecutive R1 -> INTRODUCE fresh (consec_rej=8>=3)
    h_reject = [rec(i, 1, REJECT, R1, *spans[i]) for i in range(8)]
    # consol: 6 adopts -> RELATE path, then 2x reject (CONSOLIDATE),
    # an adopt (break), then 2x reject on another span (stays CONSOLIDATE)
    s6, s7 = spans[6], spans[7]
    h_consol = ([rec(i, 1, ADOPT, 0, *spans[i]) for i in range(6)]
                + [rec(6, 1, REJECT, R1, *s6),
                   rec(7, 1, REJECT, R1, *s6),
                   rec(8, 1, ADOPT, 0, *s7),
                   rec(9, 1, REJECT, R1, *s7),
                   rec(10, 1, REJECT, R1, *s7)])
    for name, recs in [("hist_adopt4", h_adopt4), ("hist_adopt8", h_adopt8),
                       ("hist_reject", h_reject), ("hist_consol", h_consol)]:
        p = os.path.join(outdir, name + ".bin")
        write_history(p, recs)
        print(f"wrote {p} ({len(recs)} records)")

if __name__ == "__main__":
    main()
