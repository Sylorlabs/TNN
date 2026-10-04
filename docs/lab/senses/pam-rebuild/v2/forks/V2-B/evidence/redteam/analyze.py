#!/usr/bin/env python3
"""Analyze attack_gate outputs per the frozen attack prereg bars."""
import sys

def load(path):
    rows = []
    summ = {}
    for line in open(path):
        line = line.rstrip("\n")
        if not line:
            continue
        if line.startswith("LEDGER_HEAD=") or line.startswith("N=") or \
           line.startswith("INSTALLS=") or line.startswith("FALSE_INSTALLS=") or \
           line.startswith("CONFLICTS="):
            k, v = line.split("=")
            summ[k] = v
            continue
        p = line.split("|")
        rows.append(dict(name=p[0], prog=int(p[1]), admit=int(p[2]),
                         dec=p[3], wrong=int(p[4])))
    return rows, summ

def main(path):
    rows, summ = load(path)
    by = {}
    for r in rows:
        fam = r["name"][0]
        by.setdefault(fam, []).append(r)
    print(f"== {path} ==")
    print("summary:", summ)
    for fam in sorted(by):
        rs = by[fam]
        inst = [r for r in rs if r["dec"] == "I"]
        false = [r for r in rs if r["wrong"] == 1]
        pas = [r for r in rs if r["prog"] == 1]
        print(f"family {fam}: n={len(rs)} progPASS={len(pas)} "
              f"installs={len(inst)} false_installs={len(false)}")
        if false:
            print("  FALSE:", [r["name"] for r in false])
    # bars
    A = by.get("A", [])
    C1 = [r for r in rows if r["name"].startswith("C1")]
    C2 = [r for r in rows if r["name"].startswith("C2")]
    gray = C1 + C2
    a_false = sum(1 for r in A if r["wrong"] == 1)
    c1_inst = sum(1 for r in C1 if r["dec"] == "I")
    c2_pass = sum(1 for r in C2 if r["prog"] == 1)
    print(f"A-BAR (>=1 false install): {a_false} -> {'HIT' if a_false >= 1 else 'MISS'}")
    print(f"C-BAR (C1 installs==0): {c1_inst} -> {'HIT' if c1_inst == 0 else 'MISS'}")
    print(f"C-BAR (C2 progPASS==0): {c2_pass} -> {'HIT' if c2_pass == 0 else 'MISS'}")
    # D-bar needs P1 clean-fail info from records; computed separately
    print(f"D inputs: {len(gray)} grayscale trials")

if __name__ == "__main__":
    main(sys.argv[1])
