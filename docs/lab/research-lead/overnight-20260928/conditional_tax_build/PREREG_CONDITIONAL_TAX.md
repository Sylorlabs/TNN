# Preregistration: Conditional Tax v2 Build

Date: 2026-09-30. Worker: Conditional Tax Builder.
Status: FROZEN. Committed before any v2 mechanism implementation is written.

## 0. Standing-rules name-check

1. Pure Zag only. No Python at any stage: authoring, building with znc,
   running, verification, byte checks. Shell tools only: sha256sum,
   md5sum, cmp, grep, wc, git, diff. Byte checks via
   worker_snippets/check_no_dash.sh. Zero Python invoked from task start.
2. No em dashes in loop documentation. This document uses hyphens only
   and is shell-checked before commit.
3. This prereg commit strictly precedes the implementation commit
   (commit-order self-check; K1).
4. Base sources are the committed v1 implementation files (see section 1).
   Work happens on copies under
   docs/lab/research-lead/overnight-20260928/conditional_tax_build/.
5. The contaminated research paper is not touched.
6. Commits local, owned pathspec only
   (docs/lab/research-lead/overnight-20260928/conditional_tax_build/).
7. Other workers' files are not touched. If a git lock is encountered,
   wait; never remove a live lock.

## 1. Design adopted

CONDITIONAL-TAX-DESIGN-COMPLETE (commit 18e0c12a6), addressing the
CONDITIONAL-FAIL (commit c6f6d6787) P4(c) FREC-I3 regression.

Base implementation: the v1 conditional-first files from commit
c6f6d6787, directory
docs/lab/research-lead/overnight-20260928/conditional_build/:
- r3c.zag (R3 battery with Change A and Change B v1)
- r1c.zag (R1 battery with Change A and Change B v1)
- frcc.zag (FREC battery with Change A and Change B v1)

The v2 files are copies with exactly the T1 and T2 modifications
specified in section 3. Nothing else changes.

Everything not named in section 3 stays as in v1: COND op 4 with
generic multiplexer semantics, 32-byte node layout, 24-byte trace
records, 200/opc tax rate, score formula, top-32 selection, 24 rounds,
IV machinery, phase structure, TAU=1.0, determinism, CONDHIT and
DROUND instrumentation.

## 2. Scope and files

Owned directory:
docs/lab/research-lead/overnight-20260928/conditional_tax_build/

Files:

- PREREG_CONDITIONAL_TAX.md (this file).
- r3t.zag: copy of v1 r3c.zag plus T1 and T2 (section 3).
  Written only after this prereg commits.
- r1t.zag: copy of v1 r1c.zag plus T1 and T2 (section 3).
  Written only after this prereg commits.
- frct.zag: copy of v1 frcc.zag plus T1 and T2 (section 3).
  Written only after this prereg commits.
- Binaries r3t_bin, r1t_bin, frct_bin (znc-built).
- Raw outputs: TAX_R3_1/2/3.txt, TAX_R1_1/2/3.txt, TAX_FRC_1/2/3.txt
  (plus .err files, expected empty).
- RESULT_CONDITIONAL_TAX.md: verdict.

## 3. Changes (design sections 3 and 4, operationalized)

### Change T1: license-cost tax

In node_new_op, op==4 case:

v1 rule:
  oc=1 + opc(c0) + opc(c1) + opc(c2)

v2 rule:
  oc=B + opc(c0) + opc(c1) + opc(c2)
where B depends on the condition node's provenance tier:
  B=2 if c0 is Tier-1 (terminal or library term)
  B=4 if c0 is Tier-2 (round-built node)

Tier classification (structural, by node kind at offset 0):
  Tier-1: ndg(nodes, c0, 0)==0 (terminal or library term)
  Tier-2: ndg(nodes, c0, 0)==1 (round-built op node)

The 200/opc tax rate is unchanged. No COND-specific rate. The base
differentiation is by provenance tier only, never by node identity,
terminal index, family, or target literals.

R3 preservation: COND(D,Y4,Y5) has D as library term (kind 0),
Tier-1, B=2, opc=2, tax 400, score 9600 at 64/64. Still beats the
4-op tree (9200) and 3-op overfitter (9400).

### Change T2: stability-gated license

The beam_cond_combine function is revised:

1. New parameter pbeam:[]u8, a 32-entry buffer of node ids from the
   previous round's input beam (S_{r-2} semantics; see driver
   plumbing below). Used only for the Tier-2 persistence gate.

2. Condition tier split (structural, by node kind):
   Tier-1 conditions: beam members with ndg(nodes, cn, 0)==0.
   Tier-2 conditions: beam members with ndg(nodes, cn, 0)==1.

3. Tier-1 license (enumerated first):
   - Exact slice agreement at TAU=1.0 (agree1==rows1, agree0==rows0).
   - Minimum slice size 4: rows1>=4 and rows0>=4.
   - No persistence requirement.
   - Cap 64 proposals per invocation.

4. Tier-2 license (enumerated after Tier-1):
   - Exact slice agreement at TAU=1.0.
   - Minimum slice size max(4, en/8) where en is current evidence
     row count.
   - Persistence: c, A, and B must all be present in pbeam
     (membership check by node id).
   - Cap 64 proposals per invocation.

5. Total cap 128 per invocation (down from v1 256).

6. Enumeration order: Tier-1 conditions in beam order first (with
   their A,B pairs in beam order), then Tier-2 conditions in beam
   order (with their A,B pairs in beam order). Deterministic, no RNG.
   Deduplication via sig_lookup and the frozen seen[] guard unchanged.

### Driver plumbing for pbeam

A helper beam_extend_round wraps beam_extend:

- Inputs: all beam_extend params plus pbeam:[]u8 and psave:[]u8
  (both 32*4 byte buffers).
- Steps:
  a. Copy current beam node ids to psave (with -1 padding beyond bn).
  b. Call beam_extend with pbeam as the persistence reference.
  c. Copy psave to pbeam (pbeam now holds S_{r-1} for next round).
- Initialization: before the round loop, copy initial beam node
  ids to pbeam (with -1 padding). Tier-2 is thus blocked in round 0
  (pbeam holds only terminals, kind 0; Tier-2 requires kind 1).

All beam_extend call sites in the drivers are replaced with
beam_extend_round. The beam_extend and beam_cond_combine signatures
gain the pbeam parameter.

Helper functions (new, generic):
- copy_beam_ids(beam, dst, bn): copy bn node ids, pad rest with -1.
- pbeam_has(pbeam, n): return 1 if n found in 32 pbeam entries.

### Instrumentation (unchanged from v1)

CONDHIT (r3t only) and DROUND (r3t) carried over verbatim. r1t and
frct allocate dummy hitbuf as in v1.

## 4. Frozen predictions and bars

- P1' (mechanism check): CONDHIT round <= 2. D enters phase-2 beam
  as library term (Tier-1); COND(D,Y4,Y5) proposed in first Tier-1
  pass.
- P2' (primary): A2-PASS == 1 (true==64/64 AND reuse_iv*2<=scratch_iv
  AND HAS_D==1).
- P3' (generality): DROUND(r3t) < 4 (frozen baseline 4; v1 achieved 1
  via COND(X1,XOR,AND) through Tier-1 terminal X1).
- P4' (no regression on frozen controls):
  (a) A1-PASS == 1;
  (b) R1 PASS_SEEDS >= 0/5 (frozen 0/5; v1 achieved 1/5);
  (c) FREC I1 >= 46/64, I2 >= 63/64, I3 >= 40/64.
      (v1 failed I3 at 32/64; this is the bar T1+T2 must repair.)
- P5' (diagnostic, not a bar): per-round fraction of beam members
  that are COND nodes on FREC I3, reported as crowding diagnostic.

## 5. F-CASE (design section 8, eight audits)

F-CASE fires, killing the mechanism regardless of scores, if any of
the following holds:

1. String audit: any ADDED OR MODIFIED line (git diff of each new
   .zag against its v1 base) contains Y4, Y5, y4, y5, 710202, fam8,
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
6. Generality requirement: satisfied by P3' (phase-1 D measurement,
   a second compositional target).
7. Tier audit (new): the Tier-1/Tier-2 classification branches only
   on node provenance (ndg(nodes, n, 0)==0 vs ==1), never on node
   identity, terminal index, family, or target literals.
8. Tax-base audit (new): COND base B=2 for Tier-1 and B=4 for
   Tier-2, uniform 200/opc, no other base or rate adjustments.

## 6. Execution protocol (frozen)

Build: znc <file>.zag -o <file>_bin (pinned znc
/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc,
version 2026.07.0-dev).

Runs (each battery 3 times, stdout to .txt, stderr to .err):

- ./r3t_bin > TAX_R3_1.txt 2> TAX_R3_1.err (etc. for _2, _3)
- ./r1t_bin > TAX_R1_1.txt 2> TAX_R1_1.err (etc.)
- ./frct_bin > TAX_FRC_1.txt 2> TAX_FRC_1.err (etc.)

Verification: md5sum triple equality per battery; cmp of stderr
(expected empty); extraction of verdict lines via grep.

F-CASE audit: for each of r3t.zag, r1t.zag, frct.zag, run
git diff --no-index <v1-base> <new-file>, take added/modified
lines, grep for the section-5.1 literal set; manual review of the
combiner, tier classification, and tax computation against audits
2, 3, 4, 5, 7, 8.

## 7. Verdict rule

CONDITIONAL-TAX-PASS iff ALL of the following hold:

- K1: this prereg commit strictly precedes the implementation commit
  (commit-order self-check).
- K2: all runs complete (R3, R1, FREC batteries, 3 runs each).
- K3: pure Zag at every stage (zero Python), 3/3 byte-identical per
  battery, zero stderr.
- P1': CONDHIT round <= 2.
- P2': A2-PASS == 1.
- P3': DROUND(r3t) < 4 (with -1 mapped to 25).
- P4': A1-PASS == 1, R1 PASS_SEEDS >= 0/5, FREC I1 >= 46/64,
  I2 >= 63/64, I3 >= 40/64.
- F-CASE: none of the eight audits fires.

Otherwise CONDITIONAL-TAX-FAIL, with the failing bar named. Partial
passes are reported as diagnostics, never as a pass.

## 8. Honest scope

Bounded-L2 search-architecture experiment only. No L3 claim, no
Criterion 0 claim. COND remains researcher-supplied. The novelty
claim is limited to: a stability-gated license plus a license-cost
tax repairs the measured FREC-I3 evidence-overfitting regression
while preserving the R3 Arm 2 compositional repair. Residual risks
from the design (Tier-1 terminals may suffice for spurious licenses;
persistence gate may block genuine Tier-2 discoveries; B=4 may prove
too weak or strong) are measurable under the frozen bars; none is
adjusted post-hoc.

CONDITIONAL-TAX-PREREG-FROZEN.
