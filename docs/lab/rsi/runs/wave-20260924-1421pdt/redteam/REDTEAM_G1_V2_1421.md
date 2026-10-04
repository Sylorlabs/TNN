# REDTEAM_G1_V2_1421.md - independent red-team review, G1 SUNSHAFTS re-freeze

Reviewer: independent red-team agent (did not implement the candidate).
Method: shell, grep, sha256sum, od/awk byte reads of the committed BMPs.
No Python used anywhere in this review. The worker's numbers were not
trusted; every killing claim was recomputed from committed artifacts.

Overall verdict: CONFIRM the DISCARD.

## Independent verification of the evidence

Commit order (frozen prereg strictly first):
- 1d8d40013 "freeze G1 sunshafts re-freeze prereg": contains only
  preregs/PREREG_G1_SHAFTS_1421.md (182 lines, single file).
- 782dbb228 "G1 sunshafts re-freeze implementation and evidence (DISCARD)":
  34 files, all under candidates/g1_v2/. No LOOP_STATE.md, no judge
  files, no other wave paths.
- 1d8d40013 is an ancestor of 782dbb228 (git merge-base check passed).
- git log --all on the candidates/g1_v2/ path shows exactly one commit
  (782dbb228): no g1_v2 file was committed before the prereg.

Baseline rebuild (recomputed, not trusted):
- sha256 of evidence/base.bmp =
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  byte-identical to the frozen S14-record hash in the prereg. Gate PASSED.
- Toolchain src/tools/toolchain/znc_linux_x86_64_abed8aa1 recomputed sha
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  matches the frozen pin.
- Vendored sub/R33_NATIVE_IO_V1.zag recomputed sha
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8,
  matches the frozen pin.

Geometric validator (not self-certifying, checked three ways):
- evidence_validator.txt: V1..V6 all PASS, VALIDATOR_SUN_MARGIN,76,
  WEDGE_KEPT,39 OFFWEDGE_KEPT,48 TERRAIN_KEPT,64 RADCUT_KEPT,24,
  VALIDATOR_OVERALL,PASS. Margin 76 >= 40 required by V1.
- Runner cross-check is real: evidence_verify_n12.txt prints the identical
  four *_KEPT lines (39/48/64/24), so validator and verifier evaluated
  the same frozen point sets.
- Independent recompute: I re-derived the wedge set in awk from the frozen
  formula (rays r=0..5 dir (r-1,-1), step 36, t=1..8) with frame and disc
  filters ((700,250) r150 giant, (170,120) r26 moon): 39 kept, drop
  accounting exactly as the prereg's pre-freeze validation stated (5 out
  of frame left, 2 out of frame right, 2 inside the giant disc: (686,156)
  and (650,120)). The validator is not certifying itself; its geometry
  checks V3/V4/V5 use the world-model functions against the same
  point coordinates, and my from-scratch recompute agrees.

T-gate recalibration (frozen procedure followed):
- evidence_n12_run1.txt stdout order: pass1..pass3, "g1 sunshafts",
  "G1 shafts: N=12 sky_px=325786 gate=707", then pass4/pass5. The field
  measurement ran on the rebuilt baseline run before any lift was applied.
- var_n12_trace_1.md G1.8: mean_T=569 std_T=92 gate=707 lifted_px=3651
  per_mille=11. Gate arithmetic checks: 569 + 92 + 46 = 707, matching the
  frozen G = mean_T + std_T + std_T/2 (1.5 sigma). 3651/325786 = 1.12
  percent lifted, per-mille 11, consistent with a thin upper tail; the
  97.14 percent wash at hardcoded gate 400 is the inherited 1121pdt
  figure (context, not re-verified this wave). No hardcoded gate remains.

KB2/KB3 killing evidence (recomputed from the BMP bytes):
- All three variant reruns are byte-identical:
  8076028d9031618544c6986dc6c4ddd12408add53afdf82dac7801c14b8c3bea x3
  (KB1 PASS).
- Per-pixel luma L=(299R+587G+114B)/1000 over base.bmp vs var_n12_1.bmp:
  all 39 kept wedge points have dL = 0. Verifier INFO lines agree:
  INFO_KB2_RATIO_X10000,10000 (ratio 1.0000, bar >= 1.12) and
  INFO_KB3_VAR_X100,0 (var 0.00, bar >= 60.0). KB2 FAIL, KB3 FAIL.
- Sun point (110,300): dL = 0 (L=95 both).
- Characterization cross-check: 2238 sky pixels with nonzero dL,
  max dL = 9, bbox x 888..1023 y 254..305, centroid (984.5,278.3),
  matching the worker's (984,278) and ~870px-from-sun figures
  (actual distance sqrt(874^2+22^2) ~ 874). Blob pixels are a strict
  subset of the 3651 above-gate pixels: 3651 - 2238 = 1413 quantize to
  L=0 under integer math, as the worker stated.
- Supporting bars independently confirmed: 0/48 OFFWEDGE points nonzero
  dL (KB5 PASS, mean|dL| = 0.00); RADCUT all dL = 0 with max |second
  difference| = 0 (KB7 PASS); the global nonzero-dL bbox is sky-only
  (x 888..1023, y 254..305), so no terrain pixel moved (KB4 PASS at 0.00).
  KB6 acutance 472/472 ratio 1.0000 and KB8 1948ms avg vs 957ms baseline
  (2.04x <= 3x, budget 2871ms) taken from committed logs; not
  re-derived, but the INFO lines are internally consistent.

## Ruling 1: CONFIRM the DISCARD

The killing evidence is real: KB2 = 1.0000 (bar >= 1.12) and
KB3 = 0.00 (bar >= 60.0), recomputed from the committed BMPs. This is a
genuine mechanism miss, not a freeze defect and not an unpassable-by-
construction bar:

- Not a freeze defect: both 1121pdt defects were repaired and the repair
  held. The geometric validator passes every frozen check (margin 76,
  tier_at == 0 everywhere required, keep counts 39/48/64/24 against
  36/36/56/16), the validator/verifier cross-check is byte-real, and the
  T-gate recalibration followed the frozen procedure on the rebuilt
  baseline (measured 569/92, gate 707, wash down to ~1.1 percent). The
  bars were fully evaluable this wave.
- Not unpassable by construction: the wedge fan radiates from the sun
  along six rays, all kept points verified in sky. A mechanism that
  actually lifted fan-shaped shafts would register on these points; the
  bars were genuinely at risk. This mechanism's march-mean transmittance
  instead rewards long line-of-sight alignments through low-density
  corridors far from the sun, so the lift lands in a compact blob at the
  frame edge (136x51 px, max +9 luma) that intersects no wedge ray: the
  shallowest wedge ray (slope -1/4) passes through y ~ 72..106 at the
  blob's x-range, while the blob sits at y 254..305. The frozen shaft
  detector correctly reports nothing. The worker's mechanism reading is
  consistent with the committed artifacts.

Observation (not a verdict-changer): all six wedge rays have dy = -1,
i.e. the frozen fan samples only upward-going rays from the sun (angles
135 degrees up-left through 14 degrees above horizontal-right). No ray
samples near-horizontal rightward or downward directions, so a future
prereg that wants full-fan coverage may widen the sampling. Under the
frozen prereg this is a design choice, not a defect, and it does not
rescue this candidate.

## Ruling 2: the structural observation is appropriate as a queued-next item

The worker's note (a minimum-D line-of-sight formulation would
concentrate signal near the sun; a mechanism redesign) was not
implemented, not tested, and not used to adjust any constant, bar, or
verdict this wave. Nothing in it weakens the frozen bars or re-opens
this prereg. A min-D formulation is a different mechanism, and any
future shaft work must go under a fresh prereg with its own frozen bars
and its own geometric validation. As a queued-next hypothesis for the
coordinator, the note is legitimate and does not smuggle anything into
this wave.

## Ruling 3: no gaming, no confounds, no weakened bars, no Python contact

- Bar thresholds in the verdict table match the prereg freeze exactly
  (KB2 >= 1.12, KB3 >= 60.0, KB4 <= 1.0, KB5 <= 6.0, KB6 <= 1.10,
  KB7 <= 25, KB8 <= 3x). Nothing was weakened, narrowed, or
  re-interpreted. The two FAILs were taken as DISCARD per the frozen
  verdict mapping.
- No sealed pair, no JUDGE_BRIEF.md, nothing for the judge queue: correct
  under the frozen mapping (no g1_v2 judge artifacts exist; the sealed
  files found in this wave belong to the separate cv1_cite candidate).
- No Python contact: no .py files under candidates/g1_v2/; the only
  "python" string hits are benign (a "No Python" comment in the vendored
  IO copy, the runner's own static-check grep lines, and the verdict
  doc). No rand/time/clock calls in authored .zag sources (only "No RNG,
  no clock" comments). Determinism holds across 3 reruns with identical
  shas.
- One confound check: the 1413 above-gate pixels that quantize to L=0 are
  real integer-math behavior, disclosed by the worker, and consistent
  with my recompute (3651 above gate, 2238 nonzero dL). No hidden wash:
  every nonzero-dL pixel sits inside the reported blob bbox.

New evidence contributed by this review: independent awk recompute of
the wedge keep set (39, with per-point drop accounting), per-pixel dL
verification (0/39 wedge, 0/48 offwedge, sun point 0), blob bbox and
centroid from BMP bytes, and confirmation that no wedge ray intersects
the lifted blob.

Nothing in this review was written to LOOP_STATE.md. Nothing was pushed
to GitHub. No em-dashes appear in this document.
