# REPORT: PROXY-HEURISTIC-GATE -- aligning the MA4b heuristic with the dormancy gate

## Headline verdict: HEURISTIC-GATE-ALIGNED

H3 PASS + H4 PASS. Conditioning the MA4b band-pairing heuristic on
dormancy eliminates the false positive while preserving the true
positive. The heuristic was not fundamentally flawed; it was
missing the dormancy condition. The structural (dormancy) gate is
the right authority. The minimal aligning change is one leading
check in the detector: `if(e - lastwin[v] > 60){ return 0; }`,
using the same episode `e` and the same lastwin arena (3688972) as
redun3's (D) gate.

## The disagreement, resolved

PROXY-CLOSEDLOOP disclosed that the MA4b heuristic (`advpair` /
`advpair2`) fires ADVKILL=1 on the T2/T3/T4 closed-loop E795
reseeds, where the victim (cell 2) was dormant (DG2=125): a false
positive, since nothing with a current functional role was
destroyed. K=3's T4 ADVKILL2=1 was the true adversarial kill
(victim active, DG2=3). The heuristic did not condition on
dormancy; redun3's (D) gate does.

This lane built dormancy-conditioned twins of both detectors
(`advpaird` / `advpair2d`: byte-identical bodies to `advpair` /
`advpair2`, plus the (D) check on the victim) and ran them
alongside the untouched originals:

| Stream | Raw ADVKILL / ADVKILL2 | Conditioned ADVKILLD / ADVKILL2D | Victim state |
|--------|------------------------|---------------------------------|--------------|
| hg_t2 (x3) | 1 / 1 | 0 / 0 | dormant, DG2=125 |
| hg_t3 (x3) | 1 / 1 | 0 / 0 | dormant, DG2=125 |
| hg_t4 (x3) | 1 / 1 | 0 / 0 | dormant, DG2=125 |
| hg_k3t4 (x3) | 0 / 1 | 0 / 1 | active, DG2=3 |

The raw detectors reproduce the parent values exactly (the
heuristic still sees the same band-pairing pattern), and the
conditioned detectors split them perfectly along the dormancy
line: silent on all 9 dormant-victim runs, firing on all 3
active-victim runs. The PAIR2 audit confirms the mechanism: on
hg_t4 the raw advpair2 logged `PAIR2 E795:2R VC=1 A0=4` (victim
cell 2, anchor cell 0) while ADVKILL2D stayed 0, because the
victim's DG2=125 > 60 tripped the leading dormancy check.

## Answers to the four questions

1. **Does conditioning the heuristic on dormancy eliminate the
   false positive?** Yes. H3 PASS: 9/9 runs, ADVKILLD=0 and
   ADVKILL2D=0, with the raw detectors still firing (1/1).
2. **Or is the heuristic fundamentally flawed?** No. H4 PASS:
   the conditioned detector still fires (ADVKILL2D=1, 3/3 runs)
   on the genuine adversarial kill. The band-pairing signature
   carries real signal; it was only missing the dormancy
   condition.
3. **Is the structural gate (dormancy) the right authority?**
   Yes. By the interventional criterion a kill is the
   destruction of a current functional role, which is exactly
   what the (D) gate operationalizes ("a dormant cell cannot be
   killed; an active cell can"). Conditioning the heuristic on
   the identical condition aligns the two with no residual
   disagreement on any tested stream.
4. **What is the minimal change to align them?** Add the (D)
   condition to the detector: evaluate `e - lastwin[v] > 60`
   first and suppress the fire. One leading check, same `e`,
   same arena, no other logic touched.

## Frozen bars

- H1 COMMIT-ORDER: PASS. PREREG.md (22b557bdd) committed with
  only NAMECHECK.md; all hg_*.zag files were created after and
  remain untracked until the implementation commit.
- H2 TOOLCHAIN: PASS. Safebin-only PATH throughout; `which
  python3`/`python`/`perl`/`ruby`/`node` return nothing at build
  and run time; zero forbidden-executable invocations. 3/3 runs
  byte-identical per stream (1 unique sha256 each):
  - t2: e4c3dcd3af70acd1b78a736e2ca8a1ef2bd54afbf16a82b19d10fab78273ba0c
  - t3: e44833639d5c12f099b5451a38e636b2ae483ada5041660f9d53a2efd7aa4c53
  - t4: 5ee12c86fef92f109376cf7ca67114c11c9e25c7b70ec7635e0f48fcef20ec2f
  - k3t4: 521f8590db15056c0a8f7045f59addce0548200ef6889ef9070a2ab8f3c3b659
  Only compiler warning is the pre-existing A0101 off-by-one in
  `etc_ep` (untouched code, identical in parents).
- H3 FALSE-POSITIVE ELIMINATION: PASS. hg_t2/t3/t4: raw
  ADVKILL=1 ADVKILL2=1 AND ADVKILLD=0 ADVKILL2D=0, 9/9 runs.
- H4 TRUE-POSITIVE PRESERVATION: PASS. hg_k3t4: raw ADVKILL=0
  ADVKILL2=1 AND ADVKILLD=0 ADVKILL2D=1, 3/3 runs.
- H5 CORRECTNESS PRESERVED: PASS. TRIGW, REDSEEDX/Y/W, BADRED,
  PROTDEST, B5A..B5G, B8, B9, GENFAIL identical to parent run1
  values on all 4 streams (hg_t2/t3/t4 vs cl_t2/t3/t4;
  hg_k3t4 vs pr_t4). New fields ADVKILLD=/ADVKILL2D= are the only
  output differences.
- H6 MINIMAL DIFF / PROXY UNTOUCHED: PASS. Per-file diff vs
  parent shows only: (a) arena comment for advkilld/advkill2d at
  3687364/3687368 (carved from the documented-unused 64-byte
  region), (b) new fns advpaird/advpair2d, (c) conditioned call
  sites + tallies, (d) ADVKILLD=/ADVKILL2D= print fields,
  (e) banner `-HG` tag. Zero unintended deletions. `redun3`,
  `advpair`, `advpair2` extracted and sha256-compared
  byte-identical to parents (11/11). All reseeding and tally
  logic untouched.

## Design

Additive harness-side change only, on top of PROXY-CLOSEDLOOP
(hg_t2/t3/t4 from cl_t2/t3/t4) and PROXY-REDESIGN (hg_k3t4 from
pr_t4, the K=3-driven loop that contains the only available true
adversarial kill). The redun3 proxy was not modified, per the
task constraint; the original heuristic detectors were not
modified either -- the conditioned twins run alongside them so
the disagreement is measured, not assumed away.

## Honest boundaries

- The conditioned detector inherits the 60-episode dormancy
  window verbatim; this lane does not test whether 60 is
  principled (still the thin-margin window from PROXY-REDESIGN).
- Discrimination is demonstrated on exactly one true-positive
  pattern (K=3 T4 E795) and three false-positive instances
  (T2/T3/T4 E795). Generality to new adversarial patterns is not
  tested.
- Whether future harnesses should REPLACE the raw detectors
  with the conditioned ones is a governance decision for the
  research lead, not taken here; this lane only establishes that
  conditioning aligns them.
- What is measured are cell-mean tallies, band pairings, and win
  recency, as MA1-4. Not strategy invention, not L3.
