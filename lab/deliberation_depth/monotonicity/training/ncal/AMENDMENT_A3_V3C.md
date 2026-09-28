# AMENDMENT A3 (pre-implementation) — correct S8 predicted-kill cells

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN. Amends the v3c prereg (commit
  `567b399f`) BEFORE any implementation or scored run. The hierarchy (§3.1) is
  unchanged; only the §3.3 prediction text is corrected.

## Correction

Prereg §3.3 predicted S8's kill as "(O,1) backs off from n=2 exact cells to mixed
(f1,d1) cells → G ≈ −0.494". That described the wrong backoff level: the frozen
§3.1 hierarchy is L1=(f1,f5,depth) → L2=(f1,f5) → L3=(depth) → L4=global, so
min_n=8 backs off to L2=(f1,f5), not (f1,d).

White-box simulation of S8 under the FROZEN hierarchy on the s1 matrix:
**B13 = 11 violations** — (admit,d) at all five depths (G ≈ −0.166) and (O,d) at all
six depths (G ≈ −0.198). Mechanism reason (unchanged): the sufficiency threshold
forces backoff from pure exact cells into mixed coarser cells, reintroducing the
cross-family dilution the exact classes solved. The kill prediction "B13 ≥ 1" stands;
the predicted count is refined 1 → 11.

(A favorable note for the record: the same simulation gives Design S B3 gviol = 0,
not the 2/2/2 redteam artifacts carried over from m20 in §3.2's prediction text —
the exact-cell schema calibrates the redteam family too. The frozen kill criterion
remains B3 > 2; 0 is not a regression.)
