# EVAL_DECOY: sealed evaluation on the decoy world family

Lane H5R2-DECOY, wave-20261001-2321pdt. Evaluator: the lane worker.
Implements the frozen protocol in PREREG_DECOY.md (freeze commit
51a4fe8e1, 2026-10-02 07:00:11 UTC). Pure Zag; safebin PATH;
`which python3` printed nothing at lane startup and at every check
(NAMECHECK.md Step 0); zero forbidden-executable invocations.

## Compared arms

- H5R2 (t2_prov_ok provenance gate): substrate extracted from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
- (a) REVERT-TO-LATEST, (b) NO-GATE, (c) RANDOM-ANCHOR: substrates
  extracted from 1203b865d352ae8ba380f57350218edd4d637b3a, SHA-256
  d929d50c3b3499b4c1b17bcd9e1319eecf4044f9fb96125e01de35ad1d520220,
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
  c03b4575993ecbdb3a851c75972f4281e210340f90d0c7c6622b8160cf1a0ee1.
  No working-tree file was used as a build input.

## World files (assembled post-implementation, per prereg 7.1)

Byte-copy of each arm substrate with the single main line changed
(diff-verified: exactly one line differs), plus the frozen
DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af),
plus DECOY_FRAG.zag from the implementation commit 4511f5c64
(SHA-256 6acc0965bc456e17229c24c6e7859b0a0dc5533c74e3b81f5708848014f99a6f),
plus the world alias line. Pre-run SHA-256:

- h5r2_d1.zag e45e60aa8d8a9456073e1af9473e948689604dda889189a387cb2e55d0a7e9d5
- h5r2_d2.zag a4c13c65d6ae8b0e7c2d9ae8dd548ef7e4ff3dc75b3fb59c288e8593c38f2621
- bl_latest_d1.zag b2fb045a9651d63002fd1e8d0f61264ff9b36e40b3c2b5a632afb8fc0f4c6d92
- bl_latest_d2.zag 48c1d55ea47b2f3c1cefc94dacf91e47467433358369ad17c64ecdfc4c831877
- bl_nogate_d1.zag 173939b405bfd02a00a8602e6db34ce0bf9d3c12f4446e61f26ba0f22d461aa8
- bl_nogate_d2.zag 89cc00fc7a66864bc753ac25fe98fef1188f5eb693eccbb73d2c6d989c05663f
- bl_random_d1.zag 33ba092a15fa3b9b44387b3f778304e27bfc8d0c9155b0693a71b6e12432e944
- bl_random_d2.zag 51de612859731995eb06427e842b073c7679f7c02033c6f9289e2da6cb45a86c

Each world compiled separately with the pinned znc; 3/3 runs;
full-stdout SHA-256 (identical across the 3 runs in every world):

- h5r2_d1 4f5be4d5010ab76083a51a6f4efe71a74202ba30893419fbc8626302db894508
- h5r2_d2 7169d86bbe4013dd57380c0208219ef0eeccb84bb429897bb775a56616217b2a
- bl_latest_d1 0a52481b48906a768d28efb549a60a71bceb674c74dcbb44125790951f3b5db4
- bl_latest_d2 d0d08ac7c8f3425b46271e5a8410eb211a0a2d0822d76667417c11068bf1bde8
- bl_nogate_d1 9b8b01182aa09cd6cf4813b0b2738f974970ac950dd70a2d34b70f38eb218ba5
- bl_nogate_d2 070a3787699c7b7ec4004c596c016e40bdd5a6223d677d3643d44fd54dad8873
- bl_random_d1 06a9a9de75a4c6356b9d37f106719cde7b9a3a3b84ca130a485a4e932a820b48
- bl_random_d2 793d3b19773f71ba2b1e426548b4bffafa9e496cb2fc77c8605fbcadc59deccb

Exit codes: h5r2_* exited 1 (all checks passed; the driver's ok
polarity), all baselines exited 0 (D-check failures, see below). Every
run completed and dumped.

## DB-4 (determinism): PASS for all arms

3/3 byte-identical full-stdout runs per arm per world (table above).
No nondeterminism anywhere.

## Marker scores (run 1; runs 2-3 byte-identical)

Per world: "D ok" / "D-ANS ok" / D-DECOY-FAIL / D-DEP-FAIL / D-KEY-FAIL /
other D-*-FAIL / VAL-FAIL / DONE:

- h5r2_d1: 4 / 4 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- h5r2_d2: 4 / 4 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- bl_latest_d1: 0 / 4 / 4 / 0 / 4 / 0 / 0 / DONE-FAIL
- bl_latest_d2: 0 / 4 / 4 / 0 / 4 / 0 / 0 / DONE-FAIL
- bl_nogate_d1: 0 / 4 / 0 / 4 / 4 / 0 / 0 / DONE-FAIL
- bl_nogate_d2: 0 / 4 / 0 / 4 / 4 / 0 / 0 / DONE-FAIL
- bl_random_d1: 1 / 4 / 1 / 2 / 3 / 0 / 0 / DONE-FAIL
- bl_random_d2: 1 / 4 / 1 / 2 / 3 / 0 / 0 / DONE-FAIL

Bar totals (8 decoy probes: 4 per world):

| bar | H5R2 | (a) REVERT-TO-LATEST | (b) NO-GATE | (c) RANDOM-ANCHOR |
|---|---|---|---|---|
| D ok (target 8) | 8/8 | 0/8 | 0/8 | 2/8 |
| D-ANS ok (target 8) | 8/8 | 8/8 | 8/8 | 8/8 |
| D-DECOY-FAIL | 0 | 8 | 0 | 2 |
| D-DEP-FAIL (stale) | 0 | 0 | 8 | 4 |
| VAL-FAIL | 0 | 0 | 0 | 0 |

## What each arm shows (white-box samples, d1 P1)

- H5R2: `D sup=2 liveid=65 decoyid=37 klive=36`,
  `D dep->36 tag=1 s=87301 r=8702 o=87406 sup=0`: the revert MAP
  anchors to the live reverted fact on K=(b,8702) (node 36, klive);
  the decoy fact (node 37) is untouched. D ok on all 8 probes.
- REVERT-TO-LATEST: `D sup=2 liveid=38 decoyid=28 klive=27`,
  `D dep->28 tag=1 s=87301 r=8704 o=87406 sup=0`: the revert MAP
  anchors to the decoy fact (r=8704, the unrelated key K2).
  D-DECOY-FAIL on all 8 probes, the exact pre-registered failure
  signature. Value answers are all correct (VAL-FAIL 0): the failure
  is provenance-only, exactly as NO-GATE's was in the baseline lane.
- NO-GATE: `D sup=2 liveid=47 decoyid=37 klive=36`,
  `D dep->3 tag=1 s=87301 r=8702 o=87406 sup=1`: anchors to the
  superseded original fact (node 3, sup=1). D-DEP-FAIL on all 8
  probes: its baseline-lane failure mode, unchanged.
- RANDOM-ANCHOR: 2/8 D ok; the 6 failures split 2 decoy-anchored and
  4 stale-anchored, chance-level as pre-registered (one of three
  verifying candidates is the correct one).

## Frozen kill bars

- DB-1 (H5R2 8/8 D ok): PASS. Every revert MAP anchors DEP edges to
  live tag-1 non-superseded facts on the K lineage, never the decoy.
- DB-2 (recency D-DECOY-FAIL on >=5/8): PASS with 8/8. The predicted
  failure mode materialized on every probe.
- DB-3 (controls as in the baseline lane): PASS. NO-GATE 0/8 via
  D-DEP-FAIL to the superseded original fact; RANDOM-ANCHOR 2/8 < 8/8.
- DB-4 (3/3 byte-identical): PASS for all 8 worlds.
- DB-5 (D-ANS ok 8/8 on all 4 arms): PASS. The K2 decoy fact is a
  genuine live fact on every arm; no world is adversarial-by-brokenness.

## Verdict: DECOY-DISCRIMINATES

All five frozen kill bars hold. The t2_prov_ok provenance gate is
shown necessary against the recency heuristic: on worlds where the
newest fact is not the live one, H5R2 anchors every revert MAP to the
live (older) fact while REVERT-TO-LATEST anchors to the decoy on 8/8
probes. The BASELINE-MATCHES result is thereby resolved: recency
explained the four-world battery only because, on those worlds, the
newest fact happened to be the live one.

## Negative controls

NC-D0: no world was VOID; all 8 assemblies verified per the frozen
rule. NC-D1: no forbidden-executable invocation (PROCESS-FAIL not
triggered). NC-D2: prereg freeze commit 51a4fe8e1 (2026-10-02
07:00:11 UTC) strictly precedes implementation commit 4511f5c64
(07:02:57 UTC) strictly precedes this eval; ordering clean.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-DECOY/sealed/
  (8 assembled world files + 8 compiled world binaries)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-DECOY/DECOY_FRAG.zag
  (decoy probe implementation, SHA-256
  6acc0965bc456e17229c24c6e7859b0a0dc5533c74e3b81f5708848014f99a6f)
- stdout hashes in the table above (run 1 = run 2 = run 3 per world)
