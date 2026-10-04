# Preregistration: Conditional Threshold Calibration

Date: 2026-09-30. Worker: Conditional Threshold Calibrator.
Status: FROZEN. Committed before any threshold implementation is written.

## 0. Standing-rules name-check

1. Pure Zag only. No Python at any stage: authoring, building with znc,
   running, verification, byte checks. Shell tools only: sha256sum,
   md5sum, cmp, grep, wc, git, diff. Byte checks via the shell-only
   snippet docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
   Zero Python invoked from task start. LOOP_STATE.md name-checked
   (standing rules 1, 2; shell-only byte checks; commit-order self-check).
2. No em dashes in loop documentation. This document uses hyphens only
   and is shell-checked before commit.
3. This prereg commit strictly precedes the implementation commit
   (commit-order self-check; K1).
4. Base sources are the committed v2 implementation files (see section 1).
   Work happens on copies under
   docs/lab/research-lead/overnight-20260928/conditional_threshold/.
5. The contaminated research paper is not touched.
6. Commits local, owned pathspec only
   (docs/lab/research-lead/overnight-20260928/conditional_threshold/).
7. Other workers' files are not touched. If a git lock is encountered,
   wait; never remove a live lock.

## 1. Design adopted

Threshold calibration of the v2 conditional-first mechanism, addressing
the CONDITIONAL-TAX-FAIL (commit b0d1749f2) P1'/P2' failure.

Diagnosis (committed in RESULT_CONDITIONAL_TAX.md, b0d1749f2):
- The v2 Tier-1 minimum slice of 4 rows is miscalibrated for the R3
  phase-2 target: the genuine structural condition D has fewer than 4
  rows in at least one branch of the observed evidence, so the Tier-1
  license never fires (CONDHIT round=-1, A2-PASS 0).
- With min slice 1 (uncommitted debug build, worker-reported data),
  the full v2 mechanism (T1+T2) achieves CONDHIT round=0 and A2-PASS=1
  while retaining the FREC-I3 repair. This is a threshold calibration
  failure, not a mechanism failure.
- The v2 design correctly repaired the FREC-I3 evidence-overfitting
  (v1: 32/64 to v2: 40/64, meeting the frozen bar). T1+T2 are validated;
  only the Tier-1 threshold is recalibrated.

Base implementation: the v2 conditional-tax files from commit b0d1749f2,
directory
docs/lab/research-lead/overnight-20260928/conditional_tax_build/:
- r3t.zag (R3 battery with T1 and T2)
- r1t.zag (R1 battery with T1 and T2)
- frct.zag (FREC battery with T1 and T2)

The threshold files are copies with exactly the single change specified
in section 3. Nothing else changes.

Everything not named in section 3 stays as in v2: COND op 4 with generic
multiplexer semantics, 32-byte node layout, 24-byte trace records,
200/opc tax rate, T1 license-cost tax (B=2 Tier-1, B=4 Tier-2), T2
stability-gated license (Tier-1 exact agreement no persistence cap 64;
Tier-2 exact agreement min slice max(4,en/8) plus persistence cap 64),
total cap 128, score formula, top-32 selection, 24 rounds, IV machinery,
phase structure, TAU=1.0, determinism, CONDHIT and DROUND
instrumentation.

## 2. Scope and files

Owned directory:
docs/lab/research-lead/overnight-20260928/conditional_threshold/

Files:

- PREREG_CONDITIONAL_THRESHOLD.md (this file).
- r3h.zag: copy of v2 r3t.zag plus the section-3 change.
  Written only after this prereg commits.
- r1h.zag: copy of v2 r1t.zag plus the section-3 change.
  Written only after this prereg commits.
- frch.zag: copy of v2 frct.zag plus the section-3 change.
  Written only after this prereg commits.
- Binaries r3h_bin, r1h_bin, frch_bin (znc-built, not committed).
- Raw outputs: THR_R3_1/2/3.txt, THR_R1_1/2/3.txt, THR_FRC_1/2/3.txt
  (plus .err files, expected empty).
- RESULT_CONDITIONAL_THRESHOLD.md: verdict.

## 3. Change (single, operationalized)

### Tier-1 minimum slice: min(4, en/8)

In beam_cond_combine, the Tier-1 pass currently requires fixed
minimum slice 4:

  if(r1c>=4){
    if(r0c>=4){

The calibrated rule replaces the fixed 4 with minsl1 = min(4, en/8),
where en is the current evidence row count (stg(st, 12)):

  // Threshold calibration: Tier-1 min slice = min(4, en/8).
  let minsl1:i32=en/8;
  if(minsl1>4){ minsl1=4; }

  if(r1c>=minsl1){
    if(r0c>=minsl1){

Calibration facts (verified against committed v2 sources):
- passive() sets en=8 in all three batteries before the first combiner
  call; do_iv increments en by 1. So en>=8 whenever beam_cond_combine
  runs, and minsl1 is in [1,4], never 0.
- R3 phase-2 round 0: en=8, minsl1=1. This exactly reproduces the
  debug-build regime (min slice 1) that achieved CONDHIT round=0 and
  A2-PASS=1 in worker-reported v2 data. The preregistered mechanistic
  prediction is that the committed implementation reproduces it.
- en>=32: minsl1=4, identical to v2. The FREC-I3 repair (validated at
  en=32 with threshold 4) is preserved by construction in the regime
  where it was measured; any deviation is caught by the frozen P4''
  bars.
- Tier-2 is unchanged: min slice max(4, en/8) plus the persistence
  gate. At en>=32 both tiers use 4; below en=32 Tier-1 is strictly
  more lenient than Tier-2, matching the design rationale (Tier-1
  conditions are terminals/library terms, stable by construction).

No other line changes. Comments describing the Tier-1 pass are updated
to state min slice min(4,en/8). The Tier-1/Tier-2 split, caps, exact
agreement at TAU=1.0, enumeration order, and dedup are unchanged.

## 4. Frozen predictions and bars

- P1'' (mechanism check): CONDHIT round <= 2. At R3 phase-2 round 0,
  en=8 gives minsl1=1, reproducing the debug regime that hit round 0.
- P2'' (primary): A2-PASS == 1 (true==64/64 AND reuse_iv*2<=scratch_iv
  AND HAS_D==1).
- P3'' (generality): DROUND(r3h) < 4 (frozen baseline 4; v2 achieved 1).
- P4'' (no regression on frozen controls):
  (a) A1-PASS == 1;
  (b) R1 PASS_SEEDS >= 0/5 (frozen 0/5; v2 achieved 2/5);
  (c) FREC I1 >= 46/64, I2 >= 63/64, I3 >= 40/64.
      (v2 repaired I3 to 40/64; the recalibration must not regress it.
      The more lenient early-round Tier-1 threshold is the honest
      residual risk; the frozen bar falsifies either way.)
- P5'' (diagnostic, not a bar): per-round fraction of beam members
  that are COND nodes on FREC I3, reported as crowding diagnostic.

## 5. F-CASE (eight audits, carried over from v2)

F-CASE fires, killing the mechanism regardless of scores, if any of
the following holds:

1. String audit: any ADDED OR MODIFIED line (git diff of each new
   .zag against its v2 base) contains Y4, Y5, y4, y5, 710202, fam8,
   F-PARCOND, or 710101 through 710299, in code or comments.
2. Gate audit: no proposal, scoring, or selection rule branches on a
   terminal index constant or on node identity. Terminal indices
   appear only inside generic loops.
3. Enumeration audit: Tier-1 enumerates all terminal/library beam
   members in beam order with no skip and no identity filter;
   Tier-2 enumerates all round-built beam members in beam order with
   no skip and no identity filter. TAU applies uniformly.
4. Semantics audit: the COND evaluator implements the generic
   multiplexer from child truth tables, with no branch on child
   identity.
5. Tax-rate audit: the rate is unchanged at 200 per opc. No
   COND-specific rate.
6. Generality requirement: satisfied by P3'' (phase-1 D measurement,
   a second compositional target).
7. Tier audit: the Tier-1/Tier-2 classification branches only on node
   provenance (ndg(nodes, n, 0)==0 vs ==1), never on node identity,
   terminal index, family, or target literals.
8. Tax-base audit: COND base B=2 for Tier-1 and B=4 for Tier-2,
   uniform 200/opc, no other base or rate adjustments.
9. Threshold audit (new): minsl1 is computed purely from en
   (evidence row count, structural) as min(4, en/8); no branch on
   node identity, terminal index, family, or target literals in the
   threshold computation.

## 6. Execution protocol (frozen)

Build: znc <file>.zag -o <file>_bin (pinned znc
/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc,
version 2026.07.0-dev).

Runs (each battery 3 times, stdout to .txt, stderr to .err):

- ./r3h_bin > THR_R3_1.txt 2> THR_R3_1.err (etc. for _2, _3)
- ./r1h_bin > THR_R1_1.txt 2> THR_R1_1.err (etc.)
- ./frch_bin > THR_FRC_1.txt 2> THR_FRC_1.err (etc.)

Verification: md5sum triple equality per battery; cmp of stderr
(expected empty); extraction of verdict lines via grep.

F-CASE audit: for each of r3h.zag, r1h.zag, frch.zag, run
git diff of the new file against its v2 base, take added/modified
lines, grep for the section-5.1 literal set; manual review of the
threshold computation and combiner against audits 2, 3, 4, 5, 7, 8, 9.

## 7. Verdict rule

THRESHOLD-PASS iff ALL of the following hold:

- K1: this prereg commit strictly precedes the implementation commit
  (commit-order self-check).
- K2: all runs complete (R3, R1, FREC batteries, 3 runs each).
- K3: pure Zag at every stage (zero Python), 3/3 byte-identical per
  battery, zero stderr.
- P1'': CONDHIT round <= 2.
- P2'': A2-PASS == 1.
- P3'': DROUND(r3h) < 4 (with -1 mapped to 25).
- P4'': A1-PASS == 1, R1 PASS_SEEDS >= 0/5, FREC I1 >= 46/64,
  I2 >= 63/64, I3 >= 40/64.
- F-CASE: none of the nine audits fires.

Otherwise THRESHOLD-FAIL, with the failing bar named. Partial passes
are reported as diagnostics, never as a pass.

## 8. Honest scope

Bounded-L2 search-architecture experiment only. No L3 claim, no
Criterion 0 claim. COND remains researcher-supplied. The novelty claim
is limited to: calibrating the Tier-1 minimum slice to min(4, en/8)
repairs the P1'/P2' calibration failure while preserving the v2
FREC-I3 overfitting repair. Residual risks: the more lenient
early-round Tier-1 threshold may reintroduce spurious COND licenses
on FREC (caught by P4''(c)); the persistence gate may still block
genuine Tier-2 discoveries; B=4 may prove too weak or strong. The
frozen bars falsify either way; nothing is adjusted post-hoc.

CONDITIONAL-THRESHOLD-PREREG-FROZEN.
