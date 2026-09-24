#!/usr/bin/env python3
"""gen_m1.py — M1 fixture generator (derives from PREREG_M1_BAR.md, never the instrument).

Deterministic (zero RNG). Reads the three frozen sources, writes m1_cases.txt:
  C|conf|mrgF|strong|agree   (1,102 RK-3 denominator rows)
  W|conf|mrgF|1|1            (12 TMB-5 wrongs)
  P|pairid|conf|mrgF|1|1     (18 rows: 9 CC1 wrong pairs)
  B|conf|mrgF|strong|agree   (1,109 diagnostic broad wrongs)
"""
import json, os, hashlib, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SWEEP = "/home/hatch/workspace/pam_round2/o1_delivery/sweep.jsonl"
INSTALL = "/home/hatch/workspace/pam_round2/d1_stack/rec_install.records"
GUARD = "/home/hatch/workspace/pam_round2/cc1_guard/prereg/gen_guard.py"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    rows = []
    # D: correct & conf>=700
    nd = 0
    for line in open(SWEEP):
        r = json.loads(line)
        if r["judgment"] == r["truth"] and r["conf"] >= 700:
            rows.append(("C", r["conf"], r["mrgF"], r["strong"], r["agree"]))
            nd += 1
    # B: wrong & conf>=700 (diagnostic only)
    nb = 0
    for line in open(SWEEP):
        r = json.loads(line)
        if r["judgment"] != r["truth"] and r["conf"] >= 700:
            rows.append(("B", r["conf"], r["mrgF"], r["strong"], r["agree"]))
            nb += 1
    # W: rec_install.records seq 24..35 (12 TMB-5 wrongs)
    nw = 0
    for line in open(INSTALL):
        f = line.rstrip("\n").split("|")
        seq = int(f[0])
        if 24 <= seq <= 35:
            assert f[5] == "RICH" and f[10] in ("DARK", "BRIGHT"), f
            rows.append(("W", int(f[6]), int(f[8]), 1, 1))  # conf, meas->mrgF
            nw += 1
    # P: CC1 wrong pairs from gen_guard.py literals (trials idx 2,3 of cells)
    # P: CC1 wrong pairs from gen_guard.py literals (trials idx 2,3 of cells).
    # Parsed line-by-line: cell header ("NAME", [ ... ]), then tuple rows.
    cells = {}
    cur = None
    for ln in open(GUARD):
        s = ln.strip()
        mh = re.match(r'\("((?:CC1(?:-V\d+)?))", \[', s)
        if mh:
            cur = mh.group(1)
            cells[cur] = []
            continue
        if cur is not None:
            mt = re.match(r'\((-?\d+(?:,-?\d+){12})\),?\s*$', s)
            if mt:
                cells[cur].append(tuple(int(x) for x in mt.group(1).split(",")))
            elif s.startswith("],"):
                cur = None
    order = ["CC1"] + ["CC1-V%d" % i for i in range(1, 9)]
    np = 0
    for pi, name in enumerate(order):
        tr = cells[name]
        assert len(tr) == 4, (name, len(tr))
        for ti in (2, 3):
            t = tr[ti]
            assert t[2] == 2 and t[7] == 3, (name, ti, t)  # jcode=2 wrong, truth=3
            rows.append(("P", pi, t[3], t[6], 1, 1))  # pairid, conf, mrgF
            np += 1
    assert nd == 1102, nd
    assert nw == 12, nw
    assert np == 18, np
    assert nb == 1109, nb
    out = os.path.join(HERE, "m1_cases.txt")
    with open(out, "w") as f:
        for r in rows:
            if r[0] == "P":
                f.write("P|%d|%d|%d|1|1\n" % (r[1], r[2], r[3]))
            else:
                f.write("%s|%d|%d|%d|%d\n" % r)
    print("wrote %s rows=%d (C=%d W=%d P=%d B=%d) sha=%s" % (out, len(rows), nd, nw, np, nb, sha(out)))

if __name__ == "__main__":
    main()
