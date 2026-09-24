#!/usr/bin/env python3
"""gen_budget.py — W12 frozen priced streams (PREREG_W12.md, frozen).

Deterministic (zero RNG).
w12_stream.txt: 1102 C rows in tape order + 30 wrong-set rows (W+P) flagged:
  idx|conf|mrgF|strong|agree|wrong
  (wrong=1 for the 30; the K1 end-to-end check runs bar+W12 over all rows.)
w12_attack.txt: junk-flood stream: 500 junk + 1 high-price true target
  (a real C row with idx%10==0, i.e. stake=1) + 127 surrounding trues:
  idx|conf|mrgF|strong|agree|wrong|junk
Price inputs are computed IN the instrument from these fields + ledger
position (see PREREG_W12 §2); the fixture carries no prices.
"""
import hashlib, os

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"

def main():
    c_rows, wrong_rows = [], []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        k = f[0]
        if k == "C":
            c_rows.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
        elif k == "W":
            wrong_rows.append((int(f[1]), int(f[2]), 1, 1))
        elif k == "P":
            wrong_rows.append((int(f[2]), int(f[3]), 1, 1))
    assert len(c_rows) == 1102 and len(wrong_rows) == 30
    lines = []
    for i, (cf, mg, s, a) in enumerate(c_rows):
        lines.append(f"{i}|{cf}|{mg}|{s}|{a}|0")
    for j, (cf, mg, s, a) in enumerate(wrong_rows):
        lines.append(f"{1102 + j}|{cf}|{mg}|{s}|{a}|1")
    p = os.path.join(HERE, "w12_stream.txt")
    open(p, "w").write("\n".join(lines) + "\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"w12_stream.txt: {len(lines)} rows sha256={h}")
    # attack stream: 500 junk, then target true + 127 trues (one episode)
    target = None
    for i, (cf, mg, s, a) in enumerate(c_rows):
        if i % 10 == 0 and cf >= 705 and mg >= 3588 and s == 1 and a == 1:
            target = (i, cf, mg, s, a)
            break
    assert target is not None
    alines = []
    for j in range(500):
        cf = 700 + (j % 51); mg = 3600 + (j % 401)
        alines.append(f"{j}|{cf}|{mg}|1|1|0|1")
    ti, tcf, tmg, ts, ta = target
    alines.append(f"500|{tcf}|{tmg}|{ts}|{ta}|0|0")
    n = 0
    for i, (cf, mg, s, a) in enumerate(c_rows):
        if i == ti:
            continue
        alines.append(f"{501 + n}|{cf}|{mg}|{s}|{a}|0|0")
        n += 1
        if n == 127:
            break
    ap = os.path.join(HERE, "w12_attack.txt")
    open(ap, "w").write("\n".join(alines) + "\n")
    ah = hashlib.sha256(open(ap, "rb").read()).hexdigest()
    print(f"w12_attack.txt: {len(alines)} rows (target idx {ti}) sha256={ah}")

if __name__ == "__main__":
    main()
