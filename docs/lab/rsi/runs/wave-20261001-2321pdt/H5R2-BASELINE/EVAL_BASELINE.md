# EVAL_BASELINE: sealed evaluation of the three simple baselines

Lane H5R2-BASELINE, wave-20261001-2321pdt. Evaluator: the lane worker.
Implements the frozen comparative protocol in PREREG_BASELINE.md
(freeze commit 28cbe5877). Pure Zag; safebin PATH; `which python3`
printed nothing at lane startup and at every check (NAMECHECK.md
Step 0); zero forbidden-executable invocations.

## Compared artifact

TNN3H5R H5R2 BUILD-PASS + H5R2-REPRO REPRO-PASS (frozen reference:
KB-W0 36/36, KB-W2R 12/12, KB-B2R 24/24, KB-W3 8/8, KB-B3 24/24,
KB-D1 3/3 x4 worlds; frozen binary SHA-256
19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287).

## World files (assembled post-implementation, per prereg 5.2)

Byte-copy of each baseline substrate with the single main line changed
(diff-verified: exactly one line differs), plus the frozen
DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af),
plus the world alias line. Pre-run SHA-256:

- bl_nogate_c1.zag  f4920c6d8c142ab2fcb2dc2030abf63b96ecf4d91661fe07555a0c11ef9f9041
- bl_nogate_c2.zag  4cb5ead3e64b34c1361ae0a9ba09171c40be02e5c7696051d0bd445c58388b27
- bl_nogate_w3a.zag 4b21cdb51f3cea23acebc9018b027c6ba83aa3f731c77419804367b54e1556bd
- bl_nogate_w3b.zag 5cf65b22985a620a9c396a93d3b9f7711122dc0a706f26b3063b8528d3668b7b
- bl_latest_c1.zag  8dd58b59d893f0cd7c11bacb02d96610a63e5251ae26faed3e2758b17df4b6cc
- bl_latest_c2.zag  4d737b4d1bf28277ce0aeaeb5384237cb0c3367656cc873bae906218310fddbc
- bl_latest_w3a.zag 4b7ce982ba7aaed292681ac250c4c13c7a462f790065c1496f3e5e4e65752b04
- bl_latest_w3b.zag aa00e42f99d41b9bc17539bc77dfc45e70f1290893db0219e7c227dd65d5419e
- bl_random_c1.zag  5d025c3e98ddbee4f028031a631d2719398ce55ea45eccda0f13ff1ed8ec7d0f
- bl_random_c2.zag  76715f040a8d8cabec3f4b1a991c928bd0fc4143600509f93933e9afa7f0c239
- bl_random_w3a.zag fa3abb6d858981868fb703372870a16f3d95296cf36718f06383d5d79dc43f25
- bl_random_w3b.zag ccc27d08a036a703983602164154ae3bbac2f430e82cdcf4128336d166ecb341

Each world compiled separately with the pinned znc; 3/3 runs;
full-stdout SHA-256 (identical across the 3 runs in every world):

- bl_nogate_c1  f71e319fce803e4ed0e99bc596baa8ba6ba6f439fe45c0d8e1f62f5759ffb980
- bl_nogate_c2  aa84a6ba518681bdb56c660e98a7a82b1037810e424414d8415f61e3e7b1693b
- bl_nogate_w3a 7456fe6a9018b4058615b2632f27b183ab1946379280242fd54529b2b2d83055
- bl_nogate_w3b 19aa516e7d9a312625421fac7a7693b2f5741c8024aaeff255363a291c682c65
- bl_latest_c1  0b15b2e572983d4a1366611c0f8c3544deab233d150c405220b556105e9610cb
- bl_latest_c2  2e3d520196f51cc0e69af77f45f09e1deb0b18474446f6b6220bef8b374ebc79
- bl_latest_w3a 5a0ff037db6d9eb576be02d4749e27fd0b112a9fa6fcee0a896a5dc4ef34d314
- bl_latest_w3b b53953518b55bc26724c79d3a52fa47ca1d1cd18d1b16755945fe146e48c0de7
- bl_random_c1  c102f4e7b8390a2f514b50858300c1fc6713ee05dc04b80bb0cfdd9e97b0a714
- bl_random_c2  0499e591bf1cb9b85cc575a82d637a71efda55e88306b4a035fe57786b853e4f
- bl_random_w3a f39b08852393ffa8ed6dc9a1c684e7b60741e223c15cd15f56464b13e335e579
- bl_random_w3b 0013b8bb140c462635c9626e017819e800ff6fa9532242a52b37e10e6fe6a624

Note on exit codes: the sealed driver returns ok (1 = all checks
passed, 0 = some check failed). bl_latest_* exited 1 (all pass);
bl_nogate_* and bl_random_* exited 0 (provenance checks failed, see
below). This polarity is the driver's, not a crash: every run
completed and dumped.

## CB-3 (determinism): PASS for all baselines

3/3 byte-identical full-stdout runs per baseline per world (table
above). No nondeterminism anywhere, including the fixed-seed LCG in
baseline (c).

## Bar-by-bar results (driver markers, run 1; runs 2-3 byte-identical)

Marker counts per world (W0/W2R/B2R/B3R from the C worlds; W3/B3 from
the W3 worlds; FAIL = any FAIL marker line):

- bl_nogate_c1: W0=18 W2R=4 B2R=8 B3R=2 FAIL=3
  (C1R1 W2R-DEP-FAIL, C1R2 W2R-DEP-FAIL, C1 DONE-FAIL)
- bl_nogate_c2: W0=18 W2R=4 B2R=8 B3R=2 FAIL=3
  (C2R1 W2R-DEP-FAIL, C2R2 W2R-DEP-FAIL, C2 DONE-FAIL)
- bl_nogate_w3a: W0=16 W3=0 B3=12 FAIL=5
  (W3A1..W3A4 W3-DEP-FAIL, W3A DONE-FAIL)
- bl_nogate_w3b: W0=16 W3=0 B3=12 FAIL=5
  (W3B1..W3B4 W3-DEP-FAIL, W3B DONE-FAIL)
- bl_latest_c1: W0=18 W2R=6 B2R=8 B3R=2 FAIL=0
- bl_latest_c2: W0=18 W2R=6 B2R=8 B3R=2 FAIL=0
- bl_latest_w3a: W0=16 W3=4 B3=12 FAIL=0
- bl_latest_w3b: W0=16 W3=4 B3=12 FAIL=0
- bl_random_c1: W0=18 W2R=4 B2R=8 B3R=2 FAIL=3
  (C1R1 W2R-DEP-FAIL, C1R2 W2R-DEP-FAIL, C1 DONE-FAIL)
- bl_random_c2: W0=18 W2R=4 B2R=8 B3R=2 FAIL=3
  (C2R1 W2R-DEP-FAIL, C2R2 W2R-DEP-FAIL, C2 DONE-FAIL)
- bl_random_w3a: W0=16 W3=2 B3=12 FAIL=3
  (W3A2 W3-DEP-FAIL, W3A4 W3-DEP-FAIL, W3A DONE-FAIL)
- bl_random_w3b: W0=16 W3=2 B3=12 FAIL=3
  (W3B2 W3-DEP-FAIL, W3B4 W3-DEP-FAIL, W3B DONE-FAIL)

Bar scores (C worlds w_c1+w_c2 for W0/W2R/B2R; W3 worlds w_w3a+w_w3b
for W3/B3):

| bar | H5R2 ref | (b) NO-GATE | (a) REVERT-TO-LATEST | (c) RANDOM-ANCHOR |
|---|---|---|---|---|
| KB-W0 | 36/36 | 36/36 | 36/36 | 36/36 |
| KB-W2R | 12/12 | 8/12 | 12/12 | 8/12 |
| KB-B2R | 24/24 | 24/24 | 24/24 | 24/24 |
| KB-W3 | 8/8 | 0/8 | 8/8 | 4/8 |
| KB-B3 | 24/24 | 24/24 | 24/24 | 24/24 |

## What each baseline shows

(b) NO-GATE: reproduces the killed H5R failure mode exactly on the new
sealed worlds. All failures are provenance-only: W2R-DEP-FAIL on all 4
revert probes (sample C1R1: `dep->254 tag=1 sup=0`,
`dep->255 tag=1 sup=1`, the post-revert MAP anchors a DEP edge to the
superseded original fact) and W3-DEP-FAIL on all 8 chained probes.
Behavioral bars are untouched (24/24, 24/24): the stale MAP still
returns the right value. The fix matters for provenance, not for
answers.

(a) REVERT-TO-LATEST: matches the H5R2 reference on all five bars.
Zero FAIL lines on any world. White-box samples: C1R1
`W2R sup=2 liveid=181`, `dep->146 tag=1 sup=0`,
`dep->171 tag=1 sup=0` (node 171 is the live reverted fact); W3A1
`W3 sup=3 liveid=49`, `dep->2 tag=1 sup=0`, `dep->39 tag=1 sup=0`.
On these sealed worlds, preferring the most recently created facts
anchors every revert MAP to the live fact, with no liveness or
supersession checks anywhere in the trial loop.

(c) RANDOM-ANCHOR: chance-level provenance. W2R-DEP-FAIL on 4/12
revert probes, W3-DEP-FAIL on 4/8 chained probes, varying across
probes; behavioral bars intact. Arbitrary anchoring does not suffice;
the anchoring discipline must be systematic.

## Comparative verdict (frozen CB-1/CB-2/CB-3)

- CB-1 (H5R2 must exceed each baseline by >= 2 on W2R or W3):
  (b) max(12-8, 8-0)=8 PASS; (c) max(12-8, 8-4)=4 PASS;
  (a) max(12-12, 8-8)=0 FAIL.
- CB-2 (no baseline matches the full five-bar reference vector):
  VIOLATED by (a) REVERT-TO-LATEST (36/36, 12/12, 24/24, 8/8, 24/24).
- CB-3: PASS for all baselines.

## Verdict: BASELINE-MATCHES (via baseline (a) REVERT-TO-LATEST)

The recency heuristic explains the sealed results as well as the
t2_prov_ok provenance gate: on this battery the two mechanisms are
indistinguishable on every bar. The gate is not shown necessary by
these four sealed worlds. What the battery cannot discriminate: a
world where the most recently created fact is NOT the live one (e.g.
a decoy OBSERVE on another key after the revert, making a dead fact
the newest while the correct live fact is older). In such a world the
gate anchors correctly and recency anchors to the decoy; that is the
discriminating experiment for the next adversarial battery.

Honest costs of the alternatives, for the record: (a) regresses the
substrate's built-in battery to 45/46 (F2 FAIL: masked-query
disambiguation now prefers the most recently taught 2-hop chain,
breaking the pinned BFS-first composition preference), while H5R2
holds 46/46. (b) is the killed mechanism and fails provenance bars as
killed. (c) fails provenance at chance level.

## Negative controls

NC-B0: no baseline world was VOID; all 12 assemblies verified per the
frozen rule. NC-B1: no forbidden-executable invocation (PROCESS-FAIL
not triggered). NC-B2: prereg freeze commit 28cbe5877 (2026-10-02
06:44:42 UTC) strictly precedes all implementation artifacts; ordering
clean.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-BASELINE/sealed/
  (12 assembled world files + 12 compiled world binaries)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-BASELINE/bl_nogate.zag,
  bl_latest.zag, bl_random.zag (baseline sources + .bin builds)
- stdout hashes in the table above (run 1 = run 2 = run 3 per world)
