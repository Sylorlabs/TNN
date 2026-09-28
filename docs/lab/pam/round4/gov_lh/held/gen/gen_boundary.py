#!/usr/bin/env python3
"""gen_boundary.py — MG6 adversarial boundary variants (mode 2, explicit spans).

Grid: mrgF in {399,400,401} x |dseq| in {19,20,21} x spans
{overlap-by-1, touching, disjoint-by-1} = 27 cells. All wrong
(truth != challenger jcode), conf >= 700, within tol.

Stream shape (4 trials, tcode=4):
  A: correct PASS establishing perm (j=7, truth=7)        -> disp 0
  B: correct PASS corroborating                            -> disp 1
  C: wrong PASS conflicting (j=9, truth=7), mrgF=V        -> disp 8 (store)
  D: wrong PASS same jcode, |dmeas|=50<=120, seq=1000+Dlt -> disp 8 (veto) or 9 (allow)

conf/meas (900/910, 4000/4050) are far from all F5 exemplars, so the F5
precondition never fires here: the grid probes MG6 alone.
Preregistered expectation (not a bar): allow iff V>=400 AND Dlt>=20 AND
spans disjoint (touching counts as disjoint) -> 8 allow cells.

Also emits the decoy stream: verbatim CC1-V9 cell x100 (mode 2).
Zero RNG. Deterministic.
"""
import os

W = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held")
OUT = os.path.join(W, "gen/boundary")
os.makedirs(OUT, exist_ok=True)

def line(seq, tcode, prog, conf, mrgF, jc, pred, meas, correct, truth, sa, sb):
    return "|".join(map(str, [seq, tcode, prog, prog, 1, 1, conf, mrgF,
                              jc, pred, meas, correct, truth, sa, sb]))

SPANS = {
    # (stored_sa, stored_sb, incoming_sa, incoming_sb)
    "overlap":    (0, 100, 99, 200),    # [0,100) vs [99,200): overlap by 1
    "touching":   (0, 100, 100, 200),   # touch at 100 -> disjoint
    "disjoint":   (0, 100, 101, 201),   # gap of 1 -> disjoint
}

cells = []
for V in (399, 400, 401):
    for D in (19, 20, 21):
        for sname, (ssa, ssb, isa, isb) in SPANS.items():
            trials = [
                line(500, 4, 0, 800, 500, 7, 1, 1000, 1, 7, 0, 2000),
                line(600, 4, 0, 810, 510, 7, 1, 1010, 1, 7, 100, 2100),
                line(1000, 4, 0, 900, V, 9, 1, 4000, 0, 7, ssa, ssb),
                line(1000 + D, 4, 0, 910, V, 9, 1, 4050, 0, 7, isa, isb),
            ]
            name = "b_mrg%d_dseq%d_%s" % (V, D, sname)
            p = os.path.join(OUT, name + ".txt")
            open(p, "w").write("\n".join(trials) + "\n")
            expect_allow = (V >= 400) and (D >= 20) and (sname != "overlap")
            cells.append((name, expect_allow))
            print(name, "expect", "ALLOW" if expect_allow else "veto")

print(len(cells), "boundary cells")

# decoy: verbatim CC1-V9 cell x100 (mode 2, explicit spans)
v9 = [ln for ln in open(os.path.join(W, "gen/cc1_cells/mode2/cc1_cc1_v9_m2.txt")).read().strip().split("\n")]
dp = os.path.join(OUT, "decoy_v9_x100.txt")
open(dp, "w").write("\n".join(v9 * 100) + "\n")
print("decoy:", dp, len(v9) * 100, "trials")
