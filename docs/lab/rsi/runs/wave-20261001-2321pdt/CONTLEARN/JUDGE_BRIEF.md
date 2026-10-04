# JUDGE_BRIEF: CONTLEARN learner-ownership probe

RENDER_SHA: 408ffdcdc
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: CONTLEARN INTEGRATION-DEMONSTRATED with red-team QUALIFY
NEW_KNOWLEDGE_CLAIM: With the per-query supervisor disconnected (every query
masked: expected=-2, flags=1), the frozen TNN-2 core still stores 13/13 chain
structures, retrieves 20/20 stored values across 3 task families, and shows
reuse that causally depends on the stored structures (in-arena deletion drops
original-value reuse to 0/20), with no regression on the prior 30/30 battery.

## Verdict

BUILD-PASS: LEARNOWN-DEMONSTRATED. All frozen kill bars K0 through K6 pass.

## Numbers vs frozen kill bars

- K3 (no regression): 2021pdt `cl_driver` re-run read-only, 3/3
  byte-identical, stdout SHA-256
  `53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44`
  (matches the 2021pdt recorded value), REUSE_COUNT 30/30 with R1C 6, R2C 3,
  R3C 3, R4C 12, R5C 6. PASS.
- K4a (unsupervised store): STORE_OK 13/13 (7 family-B MAPs + 6 family-C
  MAPs promoted under masked queries, alive DEP edges to licensing facts).
  PASS.
- K4b (unsupervised reuse): REUSE_OK 20/20 masked probes return stored
  values across 3 task families (7 one-hop, 7 concept-chain, 6
  distinct-relation chain), serving nodes verified white-box. PASS.
- K4c (ablation): REUSE2_ORIG 0/20 (bar <= 2), REUSE2_NEWV 20/20
  (bar >= 18). Deleting the serving structures via contradiction dropped
  original-value reuse to zero while the machinery still retrieved the 20
  successor values. PASS.
- K4d (nostore control): 20/20 true misses, 20 UNCERT nodes. PASS.
- K5 (machinery sanity): TREAT UNCERT count 0. PASS.
- K6 (determinism): 3/3 byte-identical per mode; TREAT
  `1ff527fa97b36da25fd8163299773680e53ae47fba521fc2227b0bf7c39394d9`,
  NOSTORE
  `839e66149ffc1f455d661452d860981adb1f846ade28b4638469b8c0e949a920`;
  zero stderr; exit 0. PASS.
- K0/K1/K2 (governance): prereg frozen alone at 408ffdcdc, strict descendant
  implementation, one process per run, one logged znc build, frozen core
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified three times, driver audit clean (0 cognition functions, 0
  structural writes, 0 new tags/edges/opcodes/modes/bridges), pure Zag.
  PASS.

## What this does not claim

No learner agency in the causal sense (H2-v2/H3 stand); no procedure
execution at query time (reuse is exact-hit retrieval of machinery-taught
facts, Attack 6 carried forward); no L3; no generality; the script is
disclosed, not a sealed adversarial world.

## Evidence paths (lane directory)

- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/PREREG_LEARNOWN.md`
  (frozen prereg, commit 408ffdcdc)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/DRIVER.md` (build
  record; binary `lo_driver`
  `35f78f8c3eb6fce9dec2262875f8cb1cb0efef1f7cffa824bdfaebb9a7a0ac4a`)
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/RUN_LOG.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/VERDICT_LEARNOWN.md`
- `docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN/transcript_TREAT_r{1,2,3}.txt`,
  `transcript_NOSTORE_r{1,2,3}.txt`, `harness.log`, `znc_invocations.log`

## Architecture accounting

Cognition source delta 0/0/0. New modes/bridges/handlers/semantic cases 0.
The single persistent workspace is the frozen arena; all structures in
frozen formats. One-system rule satisfied by construction.
