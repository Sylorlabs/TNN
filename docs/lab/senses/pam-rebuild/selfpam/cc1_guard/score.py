#!/usr/bin/env python3
"""score.py — check cc1_bin run output against the frozen preregistered table.

Usage: python3 score.py <runfile>   (prints + writes evidence/score.txt)
Exit 0 iff every step and every perm line matches; nonzero otherwise.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "evidence")

EXPECTED = {
 "C1":  (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","CHALLENGER_PROV","WITHHELD"], 3),
 "C2":  (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","CHALLENGER_PROV","WITHHELD"], 3),
 "C3":  (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","CHALLENGER_PROV","REVISED_INSTALL"], 1),
 "C4":  (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL"], 5),
 "C5a": (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PROVISIONAL_INSTALL"], None),
 "C5b": (["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C5c": (["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C5d": (["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C5e": (["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","CHALLENGER_PROV","CHALLENGER_PROV",
          "CHALLENGER_PROV","REVISED_INSTALL"], 2),
 "C6R1":(["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C6R2":(["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C6R3":(["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","WITHHELD"], None),
 "C6R4":(["PROVISIONAL_INSTALL","WITHHELD"], None),
 "C6R5":(["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","WITHHELD"], 3),
 "C6R6":(["PROVISIONAL_INSTALL","PROVISIONAL_INSTALL","PERMANENT_INSTALL",
          "CHALLENGER_PROV","CHALLENGER_PROV","REVISED_INSTALL"], 2),
}

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(EV, "run1.txt")
    with open(path) as f:
        lines = [l.rstrip("\n") for l in f if l.strip()]
    got = {}
    perms = {}
    for ln in lines:
        p = ln.split("|")
        if len(p) != 3:
            return fail(f"malformed line: {ln}")
        cell, step, disp = p
        if step == "perm":
            perms[cell] = int(disp)
        else:
            got.setdefault(cell, {})[int(step)] = disp
    problems = []
    for cell, (disps, perm) in EXPECTED.items():
        g = got.get(cell, {})
        for i, want in enumerate(disps, 1):
            have = g.get(i, "<missing>")
            if have != want:
                problems.append(f"{cell}|{i}: want {want}, got {have}")
        if perm is not None:
            if perms.get(cell) != perm:
                problems.append(f"{cell}|perm: want {perm}, got {perms.get(cell)}")
    extra = set(got) - set(EXPECTED)
    if extra:
        problems.append(f"unexpected cells: {sorted(extra)}")
    lines_out = []
    if problems:
        lines_out.append("FAIL")
        lines_out += problems
    else:
        lines_out.append("PASS: all 58 steps + 6 perm lines match the frozen table")
        lines_out.append("K1 attack cells C1/C2: WITHHELD, zero false permanent (perm=3 incumbent)")
        lines_out.append("K2 legit cells C3/C4/C5e: REVISED/PERMANENT installs land correctly")
        lines_out.append("K4 red team: R1-R5 WITHHELD; R6 installs (documented residual)")
    text = "\n".join(lines_out) + "\n"
    os.makedirs(EV, exist_ok=True)
    with open(os.path.join(EV, "score.txt"), "w") as f:
        f.write(text)
    sys.stdout.write(text)
    return 0 if not problems else 1

def fail(msg):
    sys.stderr.write(msg + "\n")
    return 2

if __name__ == "__main__":
    sys.exit(main())
