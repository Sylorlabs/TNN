# PREREG: PROXY-HEURISTIC-GATE

## Question

PROXY-CLOSEDLOOP reached REDUN3-CLOSEDLOOP-DISCRIMINATES (C9 PASS)
with a disclosed caveat: the MA4b band-pairing heuristic
(`advpair`/`advpair2`) fires ADVKILL=1 on the T2/T3/T4 closed-loop
E795 reseeds, while the structural (D) dormancy gate held for those
victims (DG2=125, dormant). K=3's T4 ADVKILL2=1 was the true
adversarial kill (victim active, DG2=3). The heuristic does not
condition on dormancy; the gate does. This lane resolves the
disagreement experimentally.

## Hypothesis under test

The MA4b heuristic is not fundamentally flawed; it is missing the
dormancy condition. Conditioning the detector on dormancy -- it
fires only when the victim is ACTIVE (e-lastwin[v] <= 60, i.e. the
victim FAILS redun3's (D) gate) -- eliminates the false positive
while preserving the true positive. The structural gate (dormancy)
is the right authority: by the interventional criterion a kill is
the destruction of a current functional role, which is exactly what
the (D) gate operationalizes ("a dormant cell cannot be killed; an
active cell can"). Minimal change to align them: add the (D)
condition to the heuristic detector.

## Design (frozen)

Build on PROXY-CLOSEDLOOP; do not redesign. Do NOT modify the
redun3 proxy. Additive harness-side change only:

1. New functions `advpaird` / `advpair2d`: byte-identical bodies to
   `advpair` / `advpair2`, plus one leading dormancy check --
   `if(e - lastwin[v] > 60){ return 0; }` -- using the same `e`
   (episode) and the same lastwin arena (3688972) as redun3's (D)
   gate. Signature gains only the `e:i32` parameter.
2. New write-only tallies `advkilld` (3687364) and `advkill2d`
   (3687368), carved from the documented-unused 64-byte region at
   3687364. No other arena address moves.
3. At the W-trigger proxy-reseed call sites (cond==2, vkind==1),
   after the existing advpair/advpair2 loops, run the conditioned
   detectors over the same candidates and increment the new
   tallies. Existing loops, tallies, and reseeding logic untouched.
4. Print `ADVKILLD=` / `ADVKILL2D=` after `ADVKILL2=`. Banner PROXY
   tag gains `-HG` suffix (`redun3-HG`, `redun2a-K3-HG`).

## Streams (frozen)

- `hg_t2`, `hg_t3`, `hg_t4`: copies of `cl_t2/t3/t4.zag`
  (redun3 closed loop) + conditioned detectors. False-positive
  cases: parent runs show ADVKILL=1 ADVKILL2=1 with E795 victim
  cell 2 dormant (DG2=125, LW2=669).
- `hg_k3t4`: copy of `pr_t4.zag` (PROXY-REDESIGN, K=3-driven loop)
  + conditioned detectors. True-positive control: parent run shows
  ADVKILL=0 ADVKILL2=1 with E795 victim cell 2 active (DG2=3,
  LW2=791). This is the only available true adversarial kill; the
  redun3 closed loop never kills an active cell (BADRED=0).

Parent reference values (run1 files, frozen before this prereg):
- cl_t2/t3/t4: `TRIGW n=4 E14:3U F=1 E675:D F=13 E735:0R F=15
  E795:2R F=15`; `REDSEEDW n=2 BADRED=0 ADVKILL=1 ADVKILL2=1`;
  `PROTDEST=0`; `B5A..B5G=1 B8=1 B9=1 B10=1 B10B=1 GENFAIL=0`.
- pr_t4: `TRIGW n=4 E14:3U F=1 E675:D E735:2R F=15 E795:2R F=15`;
  `REDSEEDW n=2 BADRED=0 ADVKILL=0 ADVKILL2=1`; `PROTDEST=0`;
  `B5A..B5G=1 B8=1 B9=1 B10=0 B10B=1 GENFAIL=0`.

## Frozen kill bars

- H1 COMMIT-ORDER: this PREREG.md committed strictly before any
  `hg_*.zag` implementation file exists in the lane.
- H2 TOOLCHAIN: safebin-only PATH for the whole lane; `which
  python3`/`python`/`perl`/`ruby`/`node` return nothing at build
  and run time; zero forbidden-executable invocations; 3/3 runs
  byte-identical per stream (sha256 recorded).
- H3 FALSE-POSITIVE ELIMINATION (primary, must discriminate):
  on hg_t2, hg_t3, hg_t4 -- raw `ADVKILL=1` AND `ADVKILL2=1`
  (unconditioned heuristic still fires, matching parent) AND
  `ADVKILLD=0` AND `ADVKILL2D=0` (conditioned detectors silent),
  on all 3 runs of all 3 streams.
- H4 TRUE-POSITIVE PRESERVATION (primary, must discriminate):
  on hg_k3t4 -- raw `ADVKILL=0` AND `ADVKILL2=1` (matching parent)
  AND `ADVKILL2D=1` (conditioned detector still fires on the
  active-victim kill) AND `ADVKILLD=0`, on all 3 runs.
- H5 CORRECTNESS PRESERVED: on every run, TRIGW, REDSEEDX/Y/W,
  BADRED, PROTDEST, B5A..B5G, B8, B9, GENFAIL identical to the
  parent run1 values above (hg_t2/t3/t4 vs cl_t2/t3/t4;
  hg_k3t4 vs pr_t4). The new fields ADVKILLD=/ADVKILL2D= are the
  only permitted output differences.
- H6 MINIMAL DIFF / PROXY UNTOUCHED: `diff` of each hg_*.zag vs
  its parent shows ONLY: (a) arena comment for advkilld/advkill2d,
  (b) new fns advpaird/advpair2d, (c) conditioned call sites +
  tallies, (d) ADVKILLD=/ADVKILL2D= print fields, (e) banner `-HG`
  tag. `redun3`, `advpair`, `advpair2`, and all reseeding/tally
  logic byte-identical to parent (verified by extracting and
  comparing those regions).

## Verdict mapping (frozen)

- H3 PASS + H4 PASS: HEURISTIC-GATE-ALIGNED. The heuristic was
  missing the dormancy condition, not fundamentally flawed; the
  structural (dormancy) gate is the right authority; the minimal
  aligning change is adding the (D) condition to the detector.
- H3 FAIL: HEURISTIC-FLAWED. Conditioning on dormancy does not
  eliminate the false positive; the band-pairing heuristic has a
  deeper defect (report the residual firing pattern).
- H4 FAIL: GATE-OVERFITS. Dormancy conditioning destroys true
  discrimination; the gate and heuristic cannot be aligned this
  way (report which true pattern was lost).
- Any of H1/H2/H5/H6 FAIL: PROCESS-FAIL for this wave; re-freeze
  cleanly before any verdict use.

## What this does NOT test

- Generality to new tile designs or new adversarial patterns.
- Whether the 60-episode dormancy window is principled (unchanged,
  still the thin-margin window from PROXY-REDESIGN).
- Whether the conditioned detector should REPLACE the raw one in
  future harnesses (a governance decision for the research lead).
