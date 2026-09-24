#!/usr/bin/env python3
"""gen_govlh.py — PAM GOV-LH CREW 1 fixtures (PREREG_GOVLH_W12.md, frozen).

Deterministic: zero RNG, zero wall clock. All generation is closed-form
integer arithmetic on indices, grounded in the frozen M1 tape
(pam/round3/m1/m1_cases.txt) and the frozen W12 generation logic.

Streams (idx|conf|mrgF|strong|agree|wrong|cat):
  glh_honest_10x.txt   11320 rows: 10x C copies + 300 wrongs (120 W-dense + 180 P-canon)
  glh_honest_100x.txt 113200 rows: 100x C copies + 3000 wrongs (1200 + 1800)
  glh_attack_10x.txt    6271 rows: 5000 junk + 1 target + 1270 trues
  glh_attack_100x.txt  62701 rows: 50000 junk + 1 target + 12700 trues
  glh_adv_10x.txt      12620 rows: honest_10x + 1040 ADV + 260 BND
  glh_adv_100x.txt    126200 rows: honest_100x + 10400 ADV + 2600 BND

Wrong families:
  W-dense: conf = 764 + ((j*37) mod 69) in [764,832],
           mrgF = 1888 + ((j*113) mod 486) in [1888,2373], s=a=1.
           Bounds = the tape's observed W min/max (asserted).
  P-canon: the tape's 18 P (conf,mrgF) cells in tape order, cycled.
  ADV:     conf in {706..730 step 2} x mrgF in {3600..7000} (104 cells), s=a=1.
  BND:     conf in {706..730 step 2} x mrgF in {358,382} (26 cells), s=a=1.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TAPE = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
CT, MT = 705, 3588  # frozen bar (as implemented)

P_CONF = [706 + 2 * k for k in range(13)]          # 706..730
ADV_MRG = [3600, 4000, 4500, 5000, 5500, 6000, 6500, 7000]
BND_MRG = [358, 382]


def load_tape():
    c_rows, w_rows, p_cells = [], [], []
    for ln in open(TAPE):
        f = ln.strip().split("|")
        if f[0] == "C":
            c_rows.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
        elif f[0] == "W":
            w_rows.append((int(f[1]), int(f[2])))
        elif f[0] == "P":
            p_cells.append((int(f[2]), int(f[3])))
    assert len(c_rows) == 1102 and len(w_rows) == 12 and len(p_cells) == 18
    wcf = [c for c, _ in w_rows]
    wmg = [m for _, m in w_rows]
    assert (min(wcf), max(wcf)) == (764, 832)
    assert (min(wmg), max(wmg)) == (1888, 2373)
    return c_rows, p_cells


def w_dense(j):
    conf = 764 + ((j * 37) % 69)
    mrg = 1888 + ((j * 113) % 486)
    assert 764 <= conf <= 832 and 1888 <= mrg <= 2373
    return conf, mrg


def adv_cell(k):
    c = k % 104
    return P_CONF[c % 13], ADV_MRG[(c // 13) % 8]


def bnd_cell(k):
    return P_CONF[k % 13], BND_MRG[((k // 13) % 2)]


def write_stream(name, rows):
    p = os.path.join(HERE, name)
    with open(p, "w") as f:
        for (i, cf, mg, s, a, w, cat) in rows:
            f.write(f"{i}|{cf}|{mg}|{s}|{a}|{w}|{cat}\n")
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    print(f"{name}: {len(rows)} rows sha256={h}")
    return h


def honest_wrong_battery(c_rows, p_cells, copies_w, copies_p):
    """Leg-1 battery: W-dense + P-canon. Returns list of (conf,mrg,cat)."""
    wrongs = []
    for j in range(copies_w):
        cf, mg = w_dense(j)
        wrongs.append((cf, mg, "W"))
    for j in range(copies_p):
        cf, mg = p_cells[j % 18]
        wrongs.append((cf, mg, "P"))
    return wrongs


def main():
    c_rows, p_cells = load_tape()
    shas = {}

    # ---- Leg 1 + Leg 2 honest streams ----
    for scale, tag in ((10, "10x"), (100, "100x")):
        rows = []
        idx = 0
        for _ in range(scale):
            for (cf, mg, s, a) in c_rows:
                rows.append((idx, cf, mg, s, a, 0, "C"))
                idx += 1
        wrongs = honest_wrong_battery(c_rows, p_cells, 120 * scale // 10,
                                      180 * scale // 10)
        for (cf, mg, cat) in wrongs:
            rows.append((idx, cf, mg, 1, 1, 1, cat))
            idx += 1
        name = f"glh_honest_{tag}.txt"
        shas[name] = write_stream(name, rows)
        # bar-level sanity counts (not a run — pure arithmetic on the fixture)
        nwrong = len(wrongs)
        nadm = sum(1 for (cf, mg, _) in wrongs if cf >= CT and mg >= MT)
        print(f"  leg1 battery: {nwrong} wrongs, bar-admits {nadm} "
              f"({100.0 * nadm / nwrong:.2f}%)")

    # ---- Leg 2 attack streams ----
    target = None
    for i, (cf, mg, s, a) in enumerate(c_rows):
        if i % 10 == 0 and cf >= CT and mg >= MT and s == 1 and a == 1:
            target = (i, cf, mg, s, a)
            break
    assert target is not None
    ti, tcf, tmg, ts, ta = target
    print(f"attack target: tape C idx {ti} conf={tcf} mrgF={tmg}")
    for scale, tag, njunk, ntrue in ((10, "10x", 5000, 1270),
                                    (100, "100x", 50000, 12700)):
        rows = []
        for j in range(njunk):
            cf = 700 + (j % 51)
            mg = 3600 + (j % 401)
            rows.append((j, cf, mg, 1, 1, 0, "J"))
        rows.append((njunk, tcf, tmg, ts, ta, 0, "T"))
        # Surrounding trues: the 1101 non-target C rows in tape order,
        # cycled deterministically (1101 < 1270/12700 needed at scale).
        avail = [(i, cf, mg, s, a) for i, (cf, mg, s, a) in enumerate(c_rows)
                 if i != ti]
        assert len(avail) == 1101
        for n in range(ntrue):  # trues cycle the 1101 avail rows
            i, cf, mg, s, a = avail[n % 1101]
            rows.append((njunk + 1 + n, cf, mg, s, a, 0, "C"))
        name = f"glh_attack_{tag}.txt"
        shas[name] = write_stream(name, rows)
        print(f"  target ledger idx {njunk}")

    # ---- Leg 3 adversarial streams ----
    for scale, tag in ((10, "10x"), (100, "100x")):
        base = f"glh_honest_{tag}.txt"
        rows = []
        for ln in open(os.path.join(HERE, base)):
            f = ln.rstrip("\n").split("|")
            rows.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]),
                         int(f[4]), int(f[5]), f[6]))
        idx = len(rows)
        for k in range(104 * scale):
            cf, mg = adv_cell(k)
            rows.append((idx, cf, mg, 1, 1, 1, "ADV"))
            idx += 1
        for k in range(26 * scale):
            cf, mg = bnd_cell(k)
            rows.append((idx, cf, mg, 1, 1, 1, "BND"))
            idx += 1
        name = f"glh_adv_{tag}.txt"
        shas[name] = write_stream(name, rows)

    print("done.")


if __name__ == "__main__":
    main()
