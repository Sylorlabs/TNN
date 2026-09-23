#!/usr/bin/env python3
"""mk_lists.py -- R2-14 battery lists from the FROZEN R2-7 gen_ledger.jsonl.

B-adv : all r2a+r2a2 fixtures with family>=1 (10,425), sorted by
        (split, task_name, index), first 10,000.
B-ctrl: all r2n fixtures (5,100, family 0), sorted by (split, task_name,
        index), first 2,000.
B-cp  : all family-4 fixtures in fixtures_cp/, sorted by (task, slot).

Writes <name>.list (absolute paths, one per line) and <name>.manifest
(sha256 of each fixture). Deterministic; no RNG.
"""
import json, os, hashlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORK = os.path.normpath(os.path.join(HERE, ".."))
R27 = os.path.normpath(os.path.join(FORK, "..", "R2-7"))
EV = os.path.join(FORK, "evidence")
os.makedirs(EV, exist_ok=True)

def ledger_rows():
    rows = []
    for line in open(os.path.join(R27, "evidence", "gen_ledger.jsonl")):
        d = json.loads(line)
        idx = int(d["id"].rsplit("_", 1)[-1])
        p = os.path.join(R27, "fixtures_R2A", d["split"],
                         "%s_%s_%d.r2fx" % (d["split"], d["task"], idx))
        rows.append((d["split"], d["task"], idx, d["family"], d["truth"],
                     os.path.abspath(p)))
    return rows

def write_list(name, paths):
    lp = os.path.join(EV, name + ".list")
    mp = os.path.join(EV, name + ".manifest")
    with open(lp, "w") as f:
        f.write("\n".join(paths) + "\n")
    with open(mp, "w") as f:
        for p in paths:
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            f.write("%s  %s\n" % (h, p))
    print("%s: %d fixtures" % (name, len(paths)))

def main():
    rows = ledger_rows()
    adv = [r for r in rows if r[0] in ("r2a", "r2a2") and r[3] >= 1]
    adv.sort(key=lambda r: (r[0], r[1], r[2]))
    assert len(adv) == 10425, len(adv)
    write_list("b_adv", [r[5] for r in adv[:10000]])
    ctrl = [r for r in rows if r[0] == "r2n"]
    ctrl.sort(key=lambda r: (r[0], r[1], r[2]))
    assert len(ctrl) == 5100, len(ctrl)
    write_list("b_ctrl", [r[5] for r in ctrl[:2000]])
    # B-cp: family-4 fixtures produced by gen_cp.py
    cpdir = os.path.join(FORK, "fixtures_cp")
    cp = []
    if os.path.isdir(cpdir):
        import glob
        for f in glob.glob(os.path.join(cpdir, "cp_*.r2fx")):
            base = os.path.basename(f)[:-5]
            _, task, slot = base.split("_")
            cp.append((task, int(slot), os.path.abspath(f)))
    cp.sort()
    write_list("b_cp", [p for _, _, p in cp])

if __name__ == "__main__":
    main()
