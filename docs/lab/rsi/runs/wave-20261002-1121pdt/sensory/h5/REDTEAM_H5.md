# RED TEAM H5: penumbra-dilated cirrus shadow field

Frozen prereg: PREREG_H5.md (committed alone c9da6ec2e). Mechanism: PDSH.
Recovery worker (wave-20261002-1121pdt): rebuilt all three binaries from
frozen committed source with safebin znc; r11_baseline and h5_terrain
bit-identical to prior worker's binaries; h5_verify bit-identical to the
post-fix (dd0a8c388) binary. Full battery re-run in progress.

## T1: diff contract vs r11_baseline (machine-checked)
`diff r11_baseline.zag h5_terrain.zag`: only ADDED lines (3 new functions
b_cirrus_d, b_cirrus_dp, b_cshadow5) plus 4 changed lines (b_tshade call site:
`let csh:f64 = b_cshadow5(px, py, pz, camx, camz);` replacing the H3/H4 inline
or absent shadow; three direct-sun lines multiplied by csh). No other
renderer math touched. b_cirrus_d byte-identical field math to H4 (seeds
601/602, same warp, same gates). Frozen func block (h5_funcs_block.txt)
matches the source verbatim modulo whitespace (68 lines). PASS.

## T1b: verifier-vs-prereg gate discrepancy (dated addendum, process bug)
The verifier's KB4 gate is `fail if frac < 0.05 or frac > 0.80`, but the
frozen prereg H5-KB4 bar is the fraction in [0.03, 0.60]. The gate was
inherited from the H4 verifier template; the H5 prereg tightened the
window and the gate was not updated. The verifier's RAW reported value
(H5KB4_SHADOWFRAC_x10000) is correct; only its PASS/FAIL line for KB4 is
untrustworthy. Verdict on KB4 is therefore computed by hand from the raw
value against the frozen [0.03, 0.60] window; the prereg governs. This is
a verifier process bug, not a mechanism defect; the frozen mechanism
math is unchanged. All other verifier gates match the prereg exactly
(KB2/KB3 <= 1.0, KB5 >= 0.60, KB6 mean in [-25.0,-0.5] and blowfrac 0,
KB8 <= 1.15, KB9 > 0.50).
CORRECTION: the earlier draft of this doc quoted KB7 as 1.5x; the frozen
prereg H5-KB7 is median variant wall <= 2.0x median baseline wall. The
prereg value governs.

## T2: banding / grid / kernel artifacts (needs 1024 renders)
PENDING. Plan: difference map base-vs-var at 1024; inspect shadow-boundary
regions for concentric ringing (5-tap max kernel), axis-aligned banding
(perpendicular-frame quantization), and grid imprint (fbm lattice alignment).
The 256 smoke showed 6924/196608 pixels differ (3.5%), all-darkening;
no sky/moon pixels changed at 256.

## T3: KB9 re-tune kill
PENDING (needs h5_verify on 1024 pair). If KB9 fails but KB4 passes, the
prereg mandates a re-tune kill (mechanism becomes a coverage knob, not a
penumbra model). If KB9 passes, the penumbra claim is white-box supported.

## T4: cost blowup
256 smoke: H5 175 s vs baseline 181 s (ratio 0.97x). The 5-tap kernel costs
5x on the shadow march only; shadow march is a small fraction of total.
H5-KB7 (median variant 1024 wall <= 2.0x median baseline 1024 wall, same
machine) PENDING on battery timings.

## T6: knowledge vs architecture (authorship of the penumbra kernel)
The penumbra kernel is RESEARCHER-AUTHORED, not learner-created: R_P = 0.03,
5 taps, max-rule, and the 0.45 attenuation are all frozen constants in the
prereg, written by the researcher before any render existed. No learning
claim is made for H5 and none is supported: the NEW_KNOWLEDGE_CLAIM, if
the bars pass, is strictly "the extended-source penumbra model measurably
improves the alien-terrain render under the frozen bars," a human-authored
hypothesis under test, not a learned structure. The JUDGE_BRIEF must state
this authorship plainly so the render is never mistaken for L2/L3 evidence.
Nothing about H5 touches learner state, memory, or adaptation; it is a
mechanism candidate for the imagery pipeline, judged by Micah's eyes.

## T7: metric gaming
Could the mechanism game the frozen bars? By construction, no post-hoc
tuning occurred: all constants (R_P, tap count, attenuation, heights,
point sets, bar thresholds) were frozen in PREREG_H5.md before
implementation, and the diff contract forbids any other source change.
Specific gaming vectors examined and closed:
- KB6 (mean dL in [-25,-0.5], zero blowout): the csh clamp [0,1] and the
  0.45 max attenuation bound darkening by construction; a blowout would
  require violating the frozen math, which the diff contract forbids.
- KB4 (shadow fraction window): the max-kernel can only widen coverage
  relative to H4's point sample; the window's upper bound (0.60) is the
  anti-blanket check, measured, not tunable post hoc.
- KB9 (penumbra-specificity > 0.50): the threshold is a frozen judgment
  call; the measurement recomputes both the 5-tap and center-tap fields
  white-box per kept pixel, so it cannot be gamed without changing the
  frozen field math.
- KB5 (correlation > 0.60): decorrelated darkening fails by design; the
  correlation is computed against the verifier's independent recompute
  of the frozen math, not against the renderer's internal state.
No parameter was touched after any number was seen. The one process
deviation found (T1b KB4 gate) is documented and decided in favor of the
prereg, against the looser verifier gate.

## T8: render determinism
Covered by the battery itself: H5-KB1 (3 variant renders sha256-identical),
the 2x baseline gate (sha256-identical), and the rebuild check (fresh
znc build from frozen source bit-identical to the prior worker's binaries
for r11_baseline and h5_terrain; h5_verify bit-identical to the post-fix
binary). Zero-RNG design: the only noise source is the integer-hash
value noise with frozen seeds. Zero stderr required on every run.

## T5: sky / moon / acutance non-regression
PENDING (h5_verify H5-KB2/KB3/KB8 on 1024 pair). The mechanism only touches
b_tshade's direct-sun term on terrain; sky and moon paths are untouched
by construction (T1), but the verifier measures it.

## Verifier self-check
h5_verify.zag white-box recompute mirrors the frozen block verbatim,
INCLUDING tap renormalization (caught and fixed pre-battery: dd0a8c388).
v_cshfield5 = b_cshadow5 math; v_csh_center = H4 center-tap math for KB9.
Output via single-buffer emit idiom (no _zag_print dynamics). Compiles clean.
