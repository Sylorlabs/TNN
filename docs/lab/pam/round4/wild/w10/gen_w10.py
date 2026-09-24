#!/usr/bin/env python3
"""gen_w10.py — W10 frozen candidate bundles (PREREG_W10.md, frozen).

Deterministic (zero RNG). Reads the canonical tape; emits one bundle per
C/W/P/B row plus 50 forged-attack bundles (F):
  id|kind|conf|mrgF|strong|agree|origin|prov_label|content_sig
kind: C/W/P/B from tape; F = forged-attack (every 22nd C row, attacked).
origin (0=GEN,1=EXT): (conf + mrgF) mod 2.
prov_label: C/B: = origin (consistent). W/P: = 1-origin (GEN->EXT relabeled).
  F: = 1-origin AND conf := min(1000, conf+150) (relabel + authority forgery).
content_sig: base = conf*1000003 XOR mrgF*9176 XOR idx*31 (u64);
  sig = base*1000 + (base mod 500)  -> (sig mod 1000) < 500 (intact marker).
"""
import hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
M64 = (1 << 64) - 1

def bundle(idx, kind, conf, mrg, strong, agree, forged=False):
    origin = (conf + mrg) & 1
    if kind in ("C", "B"):
        prov = origin
    else:
        prov = 1 - origin
    if forged:
        prov = 1 - origin
        conf = min(1000, conf + 150)
    base = ((conf * 1000003) ^ (mrg * 9176) ^ (idx * 31)) & M64
    sig = base * 1000 + (base % 500)
    assert (sig % 1000) < 500
    return (idx, kind, conf, mrg, strong, agree, origin, prov, sig)

def main():
    rows = []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        k = f[0]
        if k == "P":
            rows.append((k, int(f[2]), int(f[3]), 1, 1))
        else:
            rows.append((k, int(f[1]), int(f[2]), int(f[3]), int(f[4])))
    c_rows = [(i, r) for i, r in enumerate(rows) if r[0] == "C"]
    assert len(c_rows) == 1102
    out = []
    for i, (k, conf, mrg, s, a) in enumerate(rows):
        b = bundle(i, k, conf, mrg, s, a, forged=False)
        out.append("%d|%s|%d|%d|%d|%d|%d|%d|%d" % b)
    # 50 forged-attack bundles: copies of every 22nd C row, attacked, fresh ids
    fid = len(rows)
    fidxs = list(range(0, len(c_rows), 22))[:50]
    assert len(fidxs) == 50
    for j in fidxs:
        i, (k, conf, mrg, s, a) = c_rows[j]
        b = bundle(fid, "F", conf, mrg, s, a, forged=True)
        out.append("%d|%s|%d|%d|%d|%d|%d|%d|%d" % b)
        fid += 1
    final = out
    p = os.path.join(HERE, "w10_bundles.txt")
    open(p, "w").write("\n".join(final) + "\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    kinds = {}
    for line in final:
        kinds[line.split("|")[1]] = kinds.get(line.split("|")[1], 0) + 1
    print(f"w10_bundles.txt: {len(final)} rows kinds={kinds} sha256={h}")

if __name__ == "__main__":
    main()
