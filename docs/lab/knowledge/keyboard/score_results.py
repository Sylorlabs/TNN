#!/usr/bin/env python3
"""Glue: score a results file from run_battery.zag into the metrics table.

Results lines: typed \\t truth \\t kind \\t kb_rank \\t bl_rank \\t char_rank
(char_rank = 0 for non-S1 items.)
"""
import sys

def main():
    path = sys.argv[1]
    kinds = ["S1", "S2", "RW"]
    tot = {k: 0 for k in kinds}
    kb1 = {k: 0 for k in kinds}
    kb3 = {k: 0 for k in kinds}
    bl1 = {k: 0 for k in kinds}
    bl3 = {k: 0 for k in kinds}
    char_n = 0
    char1 = 0
    char3 = 0
    n = 0
    for line in open(path):
        line = line.rstrip("\n")
        if not line:
            continue
        typed, truth, kind, kbr, blr, chr_ = line.split("\t")
        kbr, blr, chr_ = int(kbr), int(blr), int(chr_)
        assert kind in kinds, kind
        tot[kind] += 1
        n += 1
        kb1[kind] += (kbr == 1)
        kb3[kind] += (kbr <= 3)
        bl1[kind] += (blr == 1)
        bl3[kind] += (blr <= 3)
        if kind == "S1":
            char_n += 1
            char1 += (chr_ == 1)
            char3 += (chr_ <= 3)

    def pct(x, d):
        return 100.0 * x / d if d else 0.0

    print(f"ITEMS {n}")
    print(f"{'kind':<4} {'n':>6} {'KB top1':>8} {'BL top1':>8} {'delta_pp':>8} {'KB top3':>8} {'BL top3':>8}")
    allk = kb1s = bl1s = 0
    for k in kinds + ["ALL"]:
        if k == "ALL":
            d = n
            a1 = sum(kb1.values()); b1 = sum(bl1.values())
            a3 = sum(kb3.values()); b3 = sum(bl3.values())
        else:
            d = tot[k]
            a1, b1, a3, b3 = kb1[k], bl1[k], kb3[k], bl3[k]
        print(f"{k:<4} {d:>6} {pct(a1,d):>7.2f}% {pct(b1,d):>7.2f}% {pct(a1,d)-pct(b1,d):>+7.2f}pp {pct(a3,d):>7.2f}% {pct(b3,d):>7.2f}%")
    print(f"CHAR n={char_n} top1={pct(char1,char_n):.2f}% top3={pct(char3,char_n):.2f}%")
    # raw counts for the verdict doc
    print(f"RAW kb1={sum(kb1.values())} bl1={sum(bl1.values())} kb3={sum(kb3.values())} bl3={sum(bl3.values())} n={n}")

if __name__ == "__main__":
    main()
