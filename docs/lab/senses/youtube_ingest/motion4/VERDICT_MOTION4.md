# VERDICT_MOTION4 — multi-scale coherence-field motion kill battery

2026-09-24. Rendered MECHANICALLY from the frozen prereg bars (PREREG_MOTION4.md §7).
No editorializing; each bar is PASS/FAIL with the numbers.

- Frozen prereg: PREREG_MOTION4.md (commit f69f5653)
- Frozen source: motion4.zag (blob sha 98d4aab5b0e5dce36d2ffb6d6738c75748f2f180;
  local working copy byte-identical to committed blob)
- Binary: built from the committed source with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  sha256 `d0de7df75a3762deb512125af0a1fa0f4ef0c08cb1188ae8c4a6fef06ee67b3f`,
  identical to BUILD_NOTES.md. No source change at any point during the battery.
- Run order: B1 → B2 → B3a → RM1 → RM2 → B4 (B4 run once, last, on the frozen binary+source).
- Scoring convention (frozen throughout): "false CANDIDATE" = decision=CANDIDATE with
  judgment ≠ frozen truth; "correct" = CANDIDATE with judgment = truth; WITHHOLD is
  never an error. AMBIG labels are excluded from scoring, distribution reported.

## Per-battery results

| Battery | n | correct | false | withhold | ops/clip |
|---|---|---|---|---|---|
| B1 (M3 synthetic primary) | 60 | 57 | 0 | 3 | 973,568 |
| B2 (M3 synthetic adversarial) | 30 | 11 | 1 | 18 | 973,568 |
| B3a (real-footage labeled windows) | 13 | 13 | 0 | 0 | 973,568 |
| RM1 (fast translated real textures) | 252 | 232 | 0 | 20 | 973,568 |
| RM2 (genuine real motion) | 52 | 16 (17 labeled: 16/0/1) | 0 | 36 (35 AMBIG excluded) | 973,568 |
| B4 (YT1 held-out) | 13 | 8 | 0 | 5 | 973,568 |

Detail:

- **B1:** 57/60. The 3 withholds (p017 SE, p026 SW, p056 S) are all
  `scale_disagree` — distinct direction bins across scales on diagonal/south
  synthetic motion. 0 false. (M3 was 60/60; M4 regresses 3 into honest withhold.)
- **B2:** 26 moving + 4 STILL. Moving-catch 7/26, all 4 STILL caught (exact_still,
  conf 1000). 18 moving withheld with reason `still_dir_conflict` (1px/frame:
  S2 claims STILL at 0.25 scale-px while S0/S1 claim coherent direction, frozen
  P5 forces WITHHOLD). **1 false:** p006 (truth SW) → STILL CANDIDATE
  `subnoise_still` conf 414. Mechanism: S0's evidence fell below E_FLOOR
  (ebar=57 < 64), so S0 WITHHOLDs rather than claiming direction; with no
  DirCands, S2's STILL claim passes unchallenged through the frozen §4.4
  resolution (StillCands ≠ ∅ → STILL CANDIDATE). This is frozen-mechanism
  behavior, not a scoring artifact.
- **B3a:** 12 STILL + 1 MOTION-E (OQSNhk5ICTI_w065, sub-perceptual E drift) —
  all 13 correct, 0 false, 0 withhold. The single genuine real-motion direction
  test is caught.
- **RM1:** 204 kill + 48 exploratory. 3px/frame: 94/96 correct; 6px/frame:
  78/96 correct, 18 withhold, **0 false**; STILL 12/12; exploratory 8px/frame
  48/48 correct (reported only). The 18 six-px misses are WITHHOLD with
  reason `incoherent` (S0's code), concentrated on diagonal directions
  (NE 9, NW 3, SE 2, SW 2, N 1).
- **RM2:** 52 clips (11 MOTION-D, 6 STILL, 35 AMBIG). Labeled: 16/17 correct,
  0 false, 1 withhold (rm2_uKNQCPXDNdc_b2_t3630, truth E → `still_dir_conflict`;
  forest pan at b2 baseline). All 6 STILL correct. All 10 other MOTION-D caught.
  AMBIG distribution (35, excluded): clouds/deformation 6, cloud-no-coherence 1,
  ocean waves 6, atmospheric shimmer 6, pedestrians/multi-motion 9, deer
  walking 1, FPV drone 6.
- **B4:** 8/13 correct, 0 false, 5 withhold (all `still_dir_conflict` on
  adversarial 1px/frame clips adv_E/N/S/SW/W). All 4 primary-like caught
  (N/NE/NW/S/SE/SW/W incl. adv_NE, adv_NW, adv_SE, exact_still on adv_STILL).

## Kill bars K1–K7

| Bar | Requirement | Measured | Verdict |
|-----|-------------|----------|---------|
| K1 (B1) | correct ≥ 45/60 AND zero false CANDIDATE | 57/60, 0 false | **PASS** |
| K2 (B2) | zero false CANDIDATE AND moving-catch ≥ 25/26 | 1 false (p006 false-STILL), moving-catch 7/26 | **FAIL** |
| K3 (RM1) | zero false on all 204 AND 6px correct-direction ≥ 40% | 0 false; 78/96 = 81.3% | **PASS** |
| K4 (B3a + RM2 labeled) | zero false CANDIDATE | 0 false (30 labeled windows: 29 correct, 1 withhold) | **PASS** |
| K5 (B4) | zero false CANDIDATE | 0 false on 13 | **PASS** |
| K6 (determinism) | 3× identical stdout on one RM1 fixture; full B1+B2+RM1 rerun → identical digest; zero RNG in source; rebuild → byte-identical binary | 3× sha `1dc64fe7…` identical; combined B1+B2+RM1 digest `46c9eaed…` == `46c9eaed…` (two passes, TSVs byte-identical); `grep -ciE "rand\|random\|time\|clock\|seed"` = 0; rebuild sha `d0de7df7…` byte-identical | **PASS** |
| K7 (cost) | ops ≤ 1,500,000 per 8-frame window | 973,568 on every clip (all batteries) | **PASS** |

Targets (reported, not kill):

| Target | Bar | Measured |
|---|---|---|
| T1 | RM1 6px correct-direction ≥ 60% | 78/96 = 81.3% — MET |
| T2 | RM2 MOTION-D catch ≥ 50% | 10/11 = 90.9% — MET |
| T3 | RM1 withhold ≤ 30%; B1 withhold ≤ 10% | RM1 20/204 = 9.8%; B1 3/60 = 5.0% — MET |

## Verdict

**MOTION4 FAILS its kill battery on K2 only.** Six of seven bars pass.

K2 fails on BOTH clauses:
- zero false CANDIDATE: 1 false — p006 (1px/frame SW synthetic) judged STILL
  CANDIDATE (conf 414). A false-STILL on moving footage is the exact failure
  mode the K-bars exist to forbid; M3 scored 0 on this clip by withholding.
- moving-catch ≥ 25/26: 7/26. Frozen P5 forces `still_dir_conflict` WITHHOLD
  on 18/26 (the S2-still vs S0/S1-direction contradiction at 1px/frame).

Both failures are frozen-mechanism consequences, recorded in BUILD_NOTES.md
as an anticipated mechanism-vs-bar tension — not scorer error, not tuning,
not a build defect. Per prereg §7, K2's bar is the repair round's problem:

**Repair-round proposal (not an action — no source was touched):**
the repair round, with Micah's sign-off, would need to change one or both of:
1. The 1px/frame contradiction rule: a scale that claims STILL while another
   claims coherent direction at ≥G_MIN_PM scale displacement currently forces
   `still_dir_conflict` (or, when S0's evidence is sub-E_FLOOR, lets the STILL
   claim through). A revised P5 could make a blind-to-d scale's STILL claim
   ineligible as StillCands when it cannot resolve d — "a scale that cannot
   see d may not claim stillness at d."
2. K2's moving-catch bar itself: if 1px/frame detection is declared out of
   M4's scope, the bar must be rewritten (not the mechanism).

Either path requires a new prereg version; nothing was tuned here.

## Determinism artifacts

- 3× single-fixture runs (rm1_t00_E3.vid): sha256
  `1dc64fe7146cd5b9bb884265168da90f6c8fedf758355b732ec76e94b995c2e9` ×3.
- Combined B1+B2+RM1 digest, pass 1: `46c9eaed690606b105b072375aaa41e7b41cce8d6fdfa97949300b5111e99c94`;
  pass 2 (re-run): `46c9eaed690606b105b072375aaa41e7b41cce8d6fdfa97949300b5111e99c94` (identical).
  Per-battery TSVs byte-identical across both passes and vs the scoring passes.
- Rebuilt binary sha256: `d0de7df75a3762deb512125af0a1fa0f4ef0c08cb1188ae8c4a6fef06ee67b3f`
  (BUILD_NOTES match).
- RNG grep over motion4.zag: 0 matches.
