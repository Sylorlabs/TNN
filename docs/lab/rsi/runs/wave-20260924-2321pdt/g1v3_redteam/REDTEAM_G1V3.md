# REDTEAM_G1V3.md - Independent red-team review of G1 SUNSHAFTS v3
## Wave wave-20260924-1721pdt (provisional verdict DISCARD, not previously red-teamed)
## Reviewer: Worker 2 (G1 v3 red-team), wave-20260924-2321pdt

Independent recomputation from committed records only. The implementation
was not modified, no pipeline was re-run, no new renders were created.

## 1. Commit order: PASS

- Prereg: acf7cedce, committed 2026-09-25 00:57:43 UTC, adds only
  docs/lab/rsi/runs/wave-20260924-1721pdt/preregs/PREREG_G1_SHAFTS_1721.md
  (329 insertions, 2 files including NOVELTY_ARGUMENT_1721.md).
- Addendum: 1da140387, committed 2026-09-25 01:17:00 UTC, adds only
  docs/lab/rsi/runs/wave-20260924-1721pdt/preregs/PREREG_G1_SHAFTS_1721_ADDENDUM_SIGN.md
  (66 insertions, single file, committed alone). The addendum is dated
  2026-09-24 and self-describes as pre-implementation; it quotes the
  coordinator decision verbatim adopting the prose-intended clarity-gate
  reading with s'(P) = (T(P) - BMEAN_T[b])*1024/BSTD_T[b], SGATE = 1152.
- Implementation: 39707e077, committed 2026-09-25 01:24:34 UTC.
- Both acf7cedce and 1da140387 are ancestors of 39707e077
  (git merge-base --is-ancestor confirms). Timestamps are strictly
  increasing: prereg < addendum < implementation.
- Result: PASS. S10 commit-order discipline satisfied; the addendum is
  dated pre-implementation and committed alone.

## 2. Frozen-bar recomputation from committed BMPs and logs

All hashes recomputed with sha256sum on the committed files.

- KB1 determinism: CONFIRMED. All three variant BMPs recompute to
  96f3a899ee45155b5272536a25f71614a43ef6bca213a2ab6a4b7fc212ec3cd4,
  identical across var_v3_1/2/3.bmp, and matching the committed runner
  record evidence_v3_sha.txt (commit 39707e077). The three run logs each
  print the identical line "G1v3 shafts: N=12 K=7 gated_px=323997
  clarity_pass=28476 delta_pass=2805 lifted_px=2805".
- KB2 shaft ratio: CONFIRMED FAIL. Committed verifier output
  evidence_verify_v3.txt records INFO_KB2_RATIO_X10000,10000 = 1.0000
  against the frozen bar >= 1.12 (prereg lines 166-167, confirmed in the
  committed prereg at acf7cedce). KB2,FAIL in the record.
- KB3 var(dL): CONFIRMED FAIL. INFO_KB3_VAR_X100,0 = 0.00 against the
  frozen bar >= 60.0 (prereg line 168). KB3,FAIL in the record.
- KB4: CONFIRMED PASS. INFO_KB4_MEANABS_X100,0 = 0.00 <= 1.0.
- KB5: CONFIRMED PASS. INFO_KB5_MEANABS_X100,0 = 0.00 <= 6.0.
- KB6: CONFIRMED PASS. Acutance base 472 / variant 472, ratio x10000
  10000 = 1.0000 <= 1.10.
- KB7: CONFIRMED PASS. INFO_KB7_MAXSECONDDIFF,0 = 0 <= 25.
- KB8 cost: CONFIRMED PASS. evidence_walltime.txt records
  baseline=934ms, v3_avg=1964ms, ratio 2.10x <= 3.0x frozen bar.
- Validator V1-V6: CONFIRMED PASS. evidence_validator.txt records
  V1_SUN_ABOVE_HORIZON PASS (margin 76 px), V2/V3/V4/V5 PASS, V6
  keep asserts PASS, kept counts 39/48/64/24, VALIDATOR_OVERALL PASS.
  Cross-check: the verifier record evidence_verify_v3.txt carries the
  identical kept counts (39/48/64/24), consistent with the prereg's
  runner cross-check requirement.
- Tripwire: bar definition lives in run_g1v3.sh lines 118-130 (clarity
  pass fraction within 50..150 per mille), not in the frozen prereg;
  it is a runner sanity check. Measured 28476/323997 = 87.89 per mille,
  recomputed independently; recorded value 87 per mille is inside the
  bar. No bar definition was weakened: the runner file is byte-stable
  within the implementation commit, and 87 was never outside [50,150].

## 3. Killing evidence: CONFIRMED by independent byte-level diff

The worker's central claim is that no lifted pixel overlaps the WEDGE
set. I verified this independently by diffing the committed BMPs
(base.bmp vs var_v3_1.bmp) at byte level and mapping differing pixels
to image coordinates (1024x1024 24-bit BMP, bottom-up, row stride 3072):

- 2622 pixels have at least one changed channel byte (worker probe
  reported 2609 with nonzero luma dL; the small delta is consistent
  with a few channel changes that cancel to zero luma; not material).
- Lifted-pixel bbox recomputed: x 125..1023, y 308..458. Zero lifted
  pixels with y < 300.
- The verifier source (g1_verify_v3.zag, commit 39707e077, lines
  107-108, 193-197) generates wedge points as
  x = 110 + t*(r-1)*36, y = 300 - t*36 for t in 1..8, r in 0..5, so
  every wedge point has y <= 264 < 300 (the kept set passed the tier-0
  filter and validator V3 WEDGE_KEPT_ALL_SKY).
- The lifted band (y >= 308) is disjoint from the wedge set
  (y <= 264) by construction. Zero overlap is a geometric certainty
  given the committed deterministic generator; 0 of 39 kept wedge
  points can carry lift.
- Verifier record is consistent: KB2 ratio exactly 1.0000 and KB3
  variance exactly 0 require dL = 0 at all 39 kept wedge points.
- The sun-anchoring characterization (77% of lifted pixels within 200
  px of sun S=(110,300)) was not re-derived independently; it is a
  descriptive post-run probe result (probe_lift_v3.zag output), not a
  frozen bar, and is consistent with the recomputed bbox centroid
  region just below and right of the sun. No verdict depends on it.

## 4. Baseline-first invariant: CONFIRMED

- The runner (run_g1v3.sh, committed in 39707e077) enforces baseline
  first: baseline renders and the byte-identity gate must pass (the
  runner exits 1 on gate failure) before the three variant renders.
  The evidence logs show the baseline run completing before the v3
  runs in each recorded execution.
- Byte identity: the rebuilt base.bmp recomputes to
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  byte-identical to the S14-record baseline BMP in the wave-20260923-2021pdt
  sealed pair commit a4a42758
  (docs/lab/rsi/runs/wave-20260923-2021pdt/sensory-levers/r8c_baseline_1024.bmp
  and s14_blind/pair_39ca6681.bmp both recompute to that hash).
- Baseline gate PASS per the frozen S14 record.

## 5. Static purity check: PASS (no Python contact)

- No .py files anywhere under g1/ or preregs/ (find -iname '*.py'
  returns nothing).
- grep -rilE 'python' over the run's .zag/.sh/.md/.txt sources finds
  only self-referential purity statements and the runner's own static
  check lines (run_g1v3.sh strips // and # comments before grepping;
  R33_NATIVE_IO_V1.zag line 17 says "No Python, shell execution, libc
  implementation or hidden language runtime"; T_DISTRIBUTION_1721.md
  says "pure Zag, no Python"). No python invocation, no python import,
  no python token in executable code.
- The worker's claim "Python contact: none" is CONFIRMED.

## Bottom line

CONFIRM DISCARD [NEW]. Every killing number recomputed from the
committed BMPs and logs: KB2 1.0000 (< 1.12), KB3 0.00 (< 60.0), KB1
byte-identical x3 at 96f3a899..., validator V1-V6 all pass, baseline
gate byte-identical to the S14 record e4f65557..., cost 2.10x within
3.0x. The lifted band (recomputed y 308..458) is disjoint from the
frozen upward wedge fan (all kept wedge points y <= 264), so 0 of 39
wedge points carry lift. Commit order PASS, S10 satisfied, no Python
contact, no bar weakened. The mechanism-miss reading in the verdict
file (sector-agnostic angular-minimum predicate) is consistent with
the recomputed evidence.

No CANNOT-CONFIRM items: all needed records are present in the
committed evidence. Review artifacts produced by this worker: none
except this report; no renders, no re-runs, no implementation changes.
