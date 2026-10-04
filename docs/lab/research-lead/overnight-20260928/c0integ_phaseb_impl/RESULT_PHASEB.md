# C0INTEG Phase B Result: Grown-Menu Reuse Benefit

Date: 2026-09-30. Worker: C0INTEG Phase B Builder.
Prereg: `ba971c03d` (frozen before implementation).
Design: `2571d52c1` (PHASEB-DESIGN-COMPLETE).
Phase A baseline: `c3d8aaf90` (PHASEA-PASS).

Status: RESULT COMMITTED. Verdict: PHASEB-FAIL.

Zero Python at every stage. Byte-verified free of em/en dashes.

## Implementation

File: `c0integ_b.zag` (1,612 lines).
Binary: `c0integ_b_bin` (205,485 bytes).

Changes from Phase A (`c0integ_a.zag`):
1. `sealed()` extended with families 10-14 (X1, X2, X3, Y-std, Y-hard).
2. `beam_extend()` instrumented: `sts(st, 48, stg(st, 48) + tn)` after candidate scoring loop (M3 counter, harness-side only).
3. New `phase1_m()`: identical to `phase1()` plus 25-element `mlog` buffer recording beam-top true accuracy after each beam_extend (M2 measurement, harness-side only).
4. New helpers: `pb_seed()`, `m2_from_log()`, `tree_has_rec()`, `fresh_for_seed()`.
5. New `main()`: Phase B driver implementing A-GROWN, A-CTRL, A-ABLATE per prereg.

## Results (3/3 byte-identical runs)

SHA-256 of stdout (all three runs):
`2b7a4e040e864cfe8fe2e14a955a8096c9dab6073759af7429b815f4bf6cc609`

Exit code: 0. Stderr: empty.

### Per-seed summary

| Seed | nrec | G-YSTD opc/true | C-YSTD opc/true | G-YHARD true | C-YHARD true |
|------|------|-----------------|-----------------|--------------|--------------|
| 90011 | 0 | 3/64 | 2/56 | 59 | 59 |
| 90988 | 0 | (see log) | (see log) | (see log) | (see log) |
| 91965 | 0 | (see log) | (see log) | (see log) | (see log) |
| 92942 | 0 | (see log) | (see log) | (see log) | (see log) |
| 93919 | 0 | (see log) | (see log) | (see log) | (see log) |

Full per-seed logs in `PHASEB_RUN1.txt`.

### Metric evaluation

- I2A (recruitment): 0/5 seeds recruited. Bar requires >=4/5. **FAIL.**
- M1 (node count): 0/5 seeds. Bar requires >=4/5. **FAIL.**
- M2 (interventions): 0/5 seeds. Bar requires >=4/5. **FAIL.**
- M3 (evaluations): 0/5 seeds. Bar requires >=4/5. **FAIL.**
- M4 (structural audit): 0 bad (no seeds counted, so no violations). **PASS (vacuous).**
- M5 (ablation): 0 (ablate opc/m2 did not match control). **FAIL.**
- M6 (Y-hard capability): grown 0/5, ctrl 0/5. Bar requires grown >=4/5. **FAIL.**
- F-MENU: did not fire (no recruited ops to expand; vacuously false).
- F-NOGAIN: **FIRED** (M1, M2, M3 all failed).

### Test verdicts

- I2: **FAIL** (I2a 0/5 < 4/5; M1 0/5 < 4/5).
- I4: **FAIL** (F-NOGAIN fired).
- I5: **DID NOT RUN** (prereg section 8: I5 requires F_I2 on record; I2 yielded no recruitment).

### Final verdict

**PHASEB-FAIL**

Falsifier fired: F-NOGAIN (M1, M2, M3 all failed their bars).
Missed bars: I2a (0/5 vs 4/5), M1 (0/5 vs 4/5), M2 (0/5 vs 4/5), M3 (0/5 vs 4/5), M6 (0/5 vs 4/5).

## Diagnosis

The beam does not keep consistent factored forms across the three X episodes. On seed 90011, all three X episodes achieved 64/64 true accuracy with 3-op trees, but the three trees had three distinct canonical shapes (nshapes=3, winner=-1). The fragment detector requires the same shape in all three kept trees (freq>=3). Because the beam finds different equivalent forms (e.g., OR-of-ANDs vs AND-of-ORs vs other 3-op equivalents), no fragment qualifies for recruitment.

This confirms design Risk 1: "the beam may keep an equivalent but differently-factored tree."

The OP-RECRUIT mechanism is sound (Phase A proved it), but the Phase B hypothesis that three factored-OR episodes would yield a recruitable common fragment is false under the current beam. The beam optimizes for evidence fit and simplicity, not for structural consistency across episodes.

## Honest scope

Phase B is a clean, preregistered, deterministic test of grown-menu reuse benefit. The result is an honest FAIL: the integration does not demonstrate reuse benefit because recruitment does not fire on the designed families.

This does not invalidate Phase A (the mechanism works when fragments are present). It shows that the specific Phase B family design does not reliably produce recruitable fragments.

## I5 status

I5 did not run. Per prereg section 8, I5 requires the I2/I4 result commit with F_I2 on record. I2 yielded no recruitment (0/5), so there is no F_I2. The verdict is PHASEB-FAIL based on I2/I4 alone, as specified.

## K1/K2/K3 verification

- K1 (prereg frozen before implementation): PASS. Prereg `ba971c03d` committed before `c0integ_b.zag` existed.
- K2 (all tests run): PASS. I2 and I4 implemented and run. I5 correctly skipped per prereg conditional.
- K3 (pure Zag, 3/3 identical): PASS. Zero Python. Three runs byte-identical (sha256 above). Exit 0, empty stderr.

## Files

- Prereg: `PREREG_PHASEB.md` (committed as `ba971c03d`)
- Implementation: `c0integ_b.zag`
- Binary: `c0integ_b_bin`
- Run logs: `PHASEB_RUN1.txt`, `PHASEB_RUN2.txt`, `PHASEB_RUN3.txt` (byte-identical)
- Stderr logs: `PHASEB_RUN1.err`, `PHASEB_RUN2.err`, `PHASEB_RUN3.err` (empty)
- This result: `RESULT_PHASEB.md`

## Verdict: PHASEB-FAIL
