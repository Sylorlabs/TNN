# FS-E4 Feasibility Analysis — R2-15 naive formation on R2A fixtures

Date: 2026-09-24. Analysis only (no prereg committed, no battery built).

## Method

Wrapped raw R2FX F/G spans into the payload formats of R2-15's frozen
naive front-ends (`r2p_front.zag`) and judged every fixture in
`round2/forks/R2-7/fixtures_R2A/` (r2n/r2a/r2a2) with a Python mirror of the
naive judges. Mirror validated: 200/200 F-fooled and 200/200 G-clean on the
generator-verified R2P pitchdisc pairs.

Wrapping:
- colordisc: 6144B F/G as 64x32 RGB frame (patch A left, patch B right),
  threshold d2<400 -> SAME(0) else DIFFERENT(1). Matches front_colordisc.
- shapetrans: F 96x96 u8 -> 12x12 downsample vs P96 protos; G 48x48 u8 ->
  12x12 vs P48 protos. Matches nf_shapetrans.
- pitchdisc: F/G 32000 int16 @16kHz -> zero-crossing freq on
  [0.10,0.80)/[1.10,1.90)s windows, per-mille<5 -> SAME. Matches nf_pitchdisc.

## Results: naive-judgment shapes per (task, split)

Format: n / F_ok% / G_ok% / both_ok (fj==gj==tc) / F_fooled with G_ok / F_fooled with G_same_lie

colordisc:
  r2n : n=1080 F_ok=33.3% G_ok=33.3% both=360  fooled: G_ok=0    G_samelie=720
  r2a : n=1150 F_ok=30.4% G_ok=30.4% both=350  fooled: G_ok=0    G_samelie=800
  r2a2: n=1180 F_ok=30.5% G_ok=30.5% both=360  fooled: G_ok=0    G_samelie=820
  -> both_ok ALL truth=SAME (r2n sub=0 normals; r2a/r2a2 COL-2 illuminant-drift).
     COL-1/COL-3 metamers fool the naive RGB judge on BOTH F and G (G is a
     re-render of metameric spectra; the naive judge cannot use the spectra).

shapetrans:
  r2n : n=1296 both=499  fooled: G_ok=265 G_samelie=106
  r2a : n=1150 both=411  fooled: G_ok=280 G_samelie=132
  r2a2: n=1195 both=397  fooled: G_ok=330 G_samelie=138

pitchdisc:
  r2n : n=720  both=295  fooled: G_ok=92  G_samelie=146
  r2a : n=1150 both=322  fooled: G_ok=239 G_samelie=241
  r2a2: n=1180 both=327  fooled: G_ok=248 G_samelie=255

## Required vs available (per parent-brief family shapes)

E4-N (recall, fj==gj==tc): need 1000 + E4-WA 300 = 1300 per task.
  colordisc: 1070 available (all SAME-truth). SHORT by 230, and 100% SAME bias.
  shapetrans: 1307 available. OK (margin 7).
  pitchdisc: 944 available. SHORT by 356.

E4-U (F fooled L, G clean) 700 + E4-C (same + booster-F fooled) 650 = 1350 per task.
  colordisc: 0 available. FUNDAMENTAL BLOCKER (G never clean when F fooled).
  shapetrans: 610 available. SHORT by 740.
  pitchdisc: 487 available. SHORT by 863.

E4-W (F fooled L, second F fooled L): needs pairs; bounded above by F_fooled
  counts (colordisc 2340, shapetrans 1219+527, pitchdisc 1284+350) — feasible
  in count but the E4-U/E4-C blocker already kills the battery.

## Conclusion

The specified battery cannot be assembled. R2-15's naive front-ends do not
produce the FSC family shapes on R2A fixtures at the required rates:
- colordisc: the R2A G-span (re-render of metameric spectra) fools the naive
  RGB judge exactly when F is fooled -> zero E4-U/E4-C trials exist.
- shapetrans/pitchdisc: E4-U-shaped trials exist but at <45% of the required
  1350 per task; E4-N controls are short for pitchdisc (944 < 1300).
- colordisc E4-N would be 100% SAME-truth (no DIFFERENT controls exist with
  correct naive formation).

Root cause: R2A G-spans are "clean" for R2-7's formation front-ends (which use
spectra/second-presentations), NOT for R2-15's naive r2p judges. The debate's
"tasks with the best formation" assumption does not hold for the naive
mechanism on these fixtures.

No prereg was committed (nothing feasible to preregister). No battery built.
Awaiting parent decision: amend spec, change tasks/mechanism, or stand down.
