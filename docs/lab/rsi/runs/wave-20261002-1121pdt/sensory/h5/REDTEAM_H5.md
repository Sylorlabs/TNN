# RED TEAM H5: penumbra-dilated cirrus shadow field

Frozen prereg: PREREG_H5.md (committed alone c9da6ec2e). Mechanism: PDSH.
Status: 1024 battery running; this doc holds completed analyses, rest on done.

## T1: diff contract vs r11_baseline (machine-checked)
`diff r11_baseline.zag h5_terrain.zag`: only ADDED lines (3 new functions
b_cirrus_d, b_cirrus_dp, b_cshadow5) plus 4 changed lines (b_tshade call site:
`let csh:f64 = b_cshadow5(px, py, pz, camx, camz);` replacing the H3/H4 inline
or absent shadow; three direct-sun lines multiplied by csh). No other
renderer math touched. b_cirrus_d byte-identical field math to H4 (seeds
601/602, same warp, same gates). PASS.

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
H5-KB7 (variant <= 1.5x baseline median at 1024) PENDING on battery timings.

## T5: sky / moon / acutance non-regression
PENDING (h5_verify H5-KB2/KB3/KB8 on 1024 pair). The mechanism only touches
b_tshade's direct-sun term on terrain; sky and moon paths are untouched
by construction (T1), but the verifier measures it.

## Verifier self-check
h5_verify.zag white-box recompute mirrors the frozen block verbatim,
INCLUDING tap renormalization (caught and fixed pre-battery: dd0a8c388).
v_cshfield5 = b_cshadow5 math; v_csh_center = H4 center-tap math for KB9.
Output via single-buffer emit idiom (no _zag_print dynamics). Compiles clean.
