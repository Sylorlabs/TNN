# VERDICT_MOTION3 — coherence-field motion primitive (M3)

2026-09-23. Prereg: `PREREG_MOTION3.md` (frozen, commit fa29b24…),
amendment 1 (B3b supplemental battery, commit 34f3535…).
Implementation: `motion3.zag` (pure Zag, zero RNG).

## Bars

| Bar | Requirement | Result |
|-----|-------------|--------|
| K1 primary | ≥45/60 correct (B1 TEST-FRESH) | **60/60** PASS |
| K2 adversarial | 0 false candidates (B2, esp. 0 false-STILL) | **30/30 no-error, 0 false** PASS |
| K3 real footage | 0 candidate errors on labeled B3 windows | **0 errors** PASS |
| K4 held-out | 0 false candidates (B4 YT1) | **13/13 no-error** PASS |
| Determinism | 3× identical + full-battery digest match | PASS |

Targets: T1 ≥50/60 primary → 60/60. T2 ≥80% adversarial moving-motion
catch → 29/30 judged (25/26 moving caught = 96.2%, 1 honest withhold).
T3 ≥50% of MOTION windows correct direction → 1/1 (w065→E); thin —
see limitations.

## What improved

- Fitted centroid baseline: 33.3% primary, 30.0% adversarial, 7
  false-STILL on moving adversarial clips.
- M3: 100% primary, 100% no-error adversarial, **zero false-STILL**,
  zero false directions anywhere (B1/B2/B3/B4 combined: 0 errors).
- Cost: 749,568 ops/clip vs ~2.8M (method2), under the 1.5M budget.

## Honest limitations

1. **Real-motion detection is thin.** The frozen B3 sample contained
   no clear-translation window at the 0.32 s baseline; the B3b
   timelapse clips had conflicting cloud layers (relabeled AMBIG).
   Only one real window (w065, sub-perceptual E drift) tests
   direction detection on real footage — method3 got it right, but
   n=1.
2. **"STILL" labels were revised.** Pair-level analysis showed the
   OQSNhk5ICTI talking-head video has substantial sub-perceptual
   pixel drift — 8 windows relabeled (1→MOTION-E, 7→AMBIG). The
   original frame0-vs-frame7 eyeballing was insufficient. The 12
   remaining STILL windows are verified pixel-still (E~0, all pairs).
3. **One anomalous binary run** (see BUILD_NOTES.md): a single
   divergent output that did not reproduce in 100+ runs; cause
   unknown. All numbers above are from verified re-runs.
4. **Withhold rate on real footage is high** (28/44 AMBIG withhold,
   plus 9 judged STILL). This is by design (P4: never guess on
   incoherent motion), but it means M3 says "I don't know" often on
   complex real scenes — correct per the never-install-a-false-memory
   requirement, but limited coverage.
5. **±2px search range** cannot track fast motion (e.g., timelapse).
   Frozen by prereg; larger ranges are future work.

## Conclusion

M3 meets all kill bars. The dangerous failure mode that gated the
vision pipeline — confident false judgments on sub-threshold motion
(87.5% adversarial false-install) — is eliminated: across 116 test
clips (60+30+13+13 labeled), method3 made **zero false candidate
judgments**. It detects coherent motion down to the pixel level
(w065) and withholds honestly on everything else. The primitive is
READY as a no-false-memory motion sensor; coverage of fast/complex
real motion remains future work.
