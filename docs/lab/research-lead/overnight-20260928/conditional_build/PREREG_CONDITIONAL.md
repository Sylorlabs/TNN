# Preregistration: Conditional-First Program Search Build

Date: 2026-09-30. Worker: Conditional-First Builder.
Status: FROZEN. Committed before any mechanism implementation is written.

## 0. Standing-rules name-check

1. Pure Zag only. No Python at any stage: authoring, building with znc,
   running, verification, byte checks. Shell tools only: sha256sum,
   md5sum, cmp, grep, wc, git, diff. Byte checks via
   worker_snippets/check_no_dash.sh. Zero Python invoked from task start.
2. No em dashes in loop documentation. This document uses hyphens only
   and is shell-checked before commit.
3. This prereg commit strictly precedes the implementation commit
   (commit-order self-check; K1).
4. Frozen base sources are never edited. Work happens on copies under
   docs/lab/research-lead/overnight-20260928/conditional_build/.
5. The contaminated research paper is not touched.
6. Commits local, owned pathspec only
   (docs/lab/research-lead/overnight-20260928/conditional_build/).
7. Other workers' files are not touched. If a git lock is encountered,
   wait; never remove a live lock.

## 1. Design adopted

CONDITIONAL-DESIGN-COMPLETE (commit e7ca7d83a), the primary
recommendation of the beam architecture review (BEAM-REVIEW-COMPLETE,
commit 2135396ce).

Base machinery: the frozen R3 baseline, file q4_r3/q4_r3.zag at commit
023b4f84a (sha256
da830caf4263a6bbccf24b24eea935be98f795d37e3a19ee7ce8c9c9ad92ac73).
NOT the failed Design 1, unified, or G2 variants. The R1 control base
is q4_r1/r1.zag (sha256
26ed9643ebfd90c05bcb2c723f7109ca09a3c8ba722c1e77302e7e188c63c571).
The FREC control base is q4_adv2_clean/frecfold_clean.zag (sha256
659e0ca53f5c7b17077328d0a798324af294d57c8aac6968a79841d8cbde7450).

Everything not named in design sections 4 and 5 stays frozen: 24
rounds, beam size 32, top-32 selection by (score desc, opc asc, node
asc), tax 200 per opc, IV selection, retention, phase1/phase2
structure, determinism requirements, pure-Zag red line.

## 2. Scope and files

Owned directory:
docs/lab/research-lead/overnight-20260928/conditional_build/

Files:

- PREREG_CONDITIONAL.md (this file).
- r3_base.zag: measurement-only baseline. Frozen q4_r3.zag plus a
  read-only DROUND scan in phase1 and a phase1 driver call in main
  (fam 5, nterms 8, seed 42). Already built and run BEFORE this prereg
  was written; it contains no new mechanism. Its outputs are the
  frozen baseline numbers in section 6.
- r3c.zag: r3_base.zag plus Change A and Change B (section 3).
  Written only after this prereg commits.
- r1c.zag: q4_r1/r1.zag plus Change A and Change B, hitbuf dummy.
  Written only after this prereg commits.
- frcc.zag: q4_adv2_clean/frecfold_clean.zag plus Change A and
  Change B, hitbuf dummy. Written only after this prereg commits.
- Binaries r3_base_bin, r3c_bin, r1c_bin, frcc_bin (znc-built).
- Raw outputs: BASE_1/2/3.txt, COND_R3_1/2/3.txt, COND_R1_1/2/3.txt,
  COND_FRC_1/2/3.txt (plus .err files, expected empty).
- RESULT_CONDITIONAL.md: verdict.

## 3. Changes (design sections 4 and 5, operationalized)

### Change A: COND primitive (op 4)

- Semantics: COND(c, a, b) = (c AND a) OR ((NOT c) AND b), computed
  from the three child 64-bit signatures:
  lo = (lo_c AND lo_a) OR ((NOT lo_c) AND lo_b), hi likewise.
  Generic multiplexer; no branch on child identity.
- node_new_op gains a c2:i32 parameter. Existing call sites pass -1.
  op==4 reads children c0 (condition), c1 (a-branch), c2 (b-branch).
- opc follows the uniform rule: 1 + opc(c0) + opc(c1) + opc(c2).
  Tax unchanged at 200 per opc. No COND-specific adjustment.
- Node layout grows 28 to 32 bytes. Offsets 0..24 unchanged; third
  child c2 stored at offset 28. node_new_term and node_new_libterm
  store c2 = -1. The trace record grows 20 to 24 bytes to carry c2.
  sig_lookup, sig_hash, node_pred, score_node, beam selection are
  byte-untouched apart from the node-stride constant.
- has_d_subexpr additionally walks c2 (offset 28) with the same
  c2 >= 0 guard. (r3c only; r1c and frcc have no has_d_subexpr.)
- Deduplication via the existing sig_lookup is automatic.

### Change B: Branch-Accuracy Profile and conditional combiner

- New function beam_cond_combine, called from beam_extend after the
  frozen pair-combination phase and before scoring, in every
  beam_extend invocation (phase1 and phase2, all three batteries).
- Condition set: every current beam member node, in beam order. No
  terminal gating, no identity filter, no skip.
- BAP is computed over the current observed evidence set only
  (en rows from ev_x/ev_y). This is the non-cheating reading of the
  design: the learner cannot see unobserved targets. For condition
  index ci and member index j:
  rows1[ci] = count of evidence rows with pred(c)==1,
  rows0[ci] = count with pred(c)==0,
  agree1[ci][j] = count of rows with pred(c)==1 AND pred(m)==ev_y,
  agree0[ci][j] = count of rows with pred(c)==0 AND pred(m)==ev_y.
- TAU = 1.0 frozen (design section 9). Implemented as exact integer
  checks: agree1[ci][ai]==rows1[ci] and agree0[ci][bi]==rows0[ci].
- Proposal rule: for c, A, B in beam order, if rows1>0 and rows0>0
  and both branch agreements are exact, propose COND(c, A, B) via
  node_new_op(op=4). No blind ternary enumeration.
- CAP_COND = 256 frozen (design default). At most 256 licensed
  (c,A,B) triples per combiner invocation, taken in enumeration
  order; the combiner then stops. The cap counts licensed triples.
- Determinism: fixed enumeration orders, no RNG. Proposals dedupe
  via sig_lookup; the frozen seen[] guard prevents duplicate tmp
  entries.
- Buffer growth (mechanical): tmp 3136*4 to 3392*4, tsc 3136*12 to
  3392*12, picked 3136 to 3392. All other capacities unchanged
  (8192 node cap, 4096 trace records, beam 32, evidence 32).

### Instrumentation (reporting only, not mechanism)

- CONDHIT (r3c only): hitbuf is 12 bytes (+0 first-hit-round init
  -1, +4/+8 target E signature lo/hi). The driver computes the E
  signature from sealed(8, x) over x=0..63 (same method as d_sig).
  Inside the combiner, after node_new_op(op=4), if hitbuf[0]<0 and
  the proposed node signature equals the E signature, hitbuf[0] is
  set to the current combiner round. Combiner rounds are numbered:
  phase2 first beam_extend = 0, loop iteration r = r+1; phase1 loop
  iteration r = r, final extend = 24. hitbuf[0] is reset to -1
  immediately before the A2-REUSE phase2 call; main emits
  "CONDHIT round=<v>" after A2-REUSE. r1c and frcc allocate a dummy
  hitbuf that is never read or emitted.
- DROUND (r3_base and r3c): phase1 takes dlo/dhi params; after each
  beam_extend a read-only beam_sig_hit scan records the first round
  whose post-selection beam holds the D signature (final extend = 24,
  -1 if never). Emitted as "DROUND <n>". Cannot affect search.

## 4. Frozen predictions and bars

- P1 (mechanism check): the first COND proposal whose signature
  equals the target E signature occurs within at most 2 combiner
  rounds of D entering the phase-2 beam. D enters as a library term
  at beam init (combiner round 0). Bar: CONDHIT round <= 2.
- P2 (primary): A2-PASS == 1 under the frozen definition
  (true==64/64 AND reuse_iv*2<=scratch_iv AND HAS_D==1).
- P3 (generality): phase-1 rounds-to-D improves on the frozen
  baseline. Frozen baseline DROUND = 4 (section 6). Bar:
  DROUND(r3c) < 4, where a DROUND of -1 (not found) maps to 25.
- P4 (no regression on frozen controls):
  (a) A1-PASS stays 1;
  (b) R1 battery: PASS_SEEDS >= 0/5 (frozen outcome 0/5, R1-FAIL);
      the full per-seed table is reported; an improvement is
      generality evidence, not a regression;
  (c) FREC battery: per-instance best true-correct across 5 seeds is
      at least the frozen best: I1 >= 46/64, I2 >= 63/64,
      I3 >= 40/64.

## 5. F-CASE (design section 7)

F-CASE fires, killing the mechanism regardless of scores, if any of
the following holds:

1. String audit: any ADDED OR MODIFIED line (git diff of each new
   .zag against its frozen base blob) contains any of the literals
   Y4, Y5, y4, y5, 710202, fam8, F-PARCOND, or the strings 710101
   through 710299, in code or comments. Frozen lines are
   grandfathered: the frozen sources already contain Y4, Y5, 710202,
   and F-PARCOND in sealed()/driver comments (verified by grep
   before this prereg), so the audit is scoped to added/modified
   lines only, verified by diff.
2. Gate audit: no proposal, scoring, or selection rule branches on a
   terminal index constant or on node identity. Terminal indices
   appear only inside generic loops over the beam.
3. Enumeration audit: the COND proposal loop iterates the condition
   set and the A/B sets over all beam members in beam order, with no
   skip and no identity filter; the TAU check applies uniformly.
4. Semantics audit: the COND evaluator implements the generic
   multiplexer from child truth tables, with no branch on child
   identity.
5. Tax audit: the tax constant is unchanged at 200 per opc, and COND
   opc follows the uniform rule. No COND-specific adjustment.
6. Generality requirement: satisfied by P3 (phase-1 D measurement,
   a second compositional target). A mechanism passing P2 but
   failing P3 is recorded as a one-target trick, not a
   search-architecture result.

## 6. Pre-prereg baseline measurement (frozen machinery only)

Measured 2026-09-30 with r3_base.zag (frozen q4_r3.zag plus
read-only DROUND reporting; no mechanism change):

- 3/3 byte-identical runs, md5 8864bdf74f0d2a41d1baa0b93f3241bd,
  zero stderr.
- P1-BASE DROUND 4, kept node 1105 (matches the frozen kept-D node
  id 1105 from commit 5f56cc491).
- With the new P1-BASE reporting lines removed, output is
  byte-identical to frozen Q4R3_RAW_1.txt (diff clean).
- Frozen battery values: A1 REUSE_IV 0 true=64/64, A1-PASS 1;
  A2 REUSE_IV 24 true=53/64 HAS_D=1, A2-PASS 0; R3-PASS 0.

Frozen control outcomes (for P4):

- R1: 3/3 byte-identical, md5 6f15d782940abdf824be99721dcc2d36.
  PASS_SEEDS 0/5 (R1-FAIL, F-R1 fired). Per-seed table in
  q4_r1/R1_RESULT.md.
- FREC: 3/3 byte-identical, md5 60e3dc5ee70bd3672c08a6a7082d521c.
  Per-instance best true-correct: I1 46/64, I2 63/64, I3 40/64.

## 7. Execution protocol (frozen)

Build: znc <file>.zag -o <file>_bin (pinned znc
/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc,
version 2026.07.0-dev).

Runs (each battery 3 times, stdout to .txt, stderr to .err):

- ./r3c_bin > COND_R3_1.txt 2> COND_R3_1.err (etc. for _2, _3)
- ./r1c_bin > COND_R1_1.txt 2> COND_R1_1.err (etc.)
- ./frcc_bin > COND_FRC_1.txt 2> COND_FRC_1.err (etc.)

Verification: md5sum triple equality per battery; cmp of stderr
(expected empty); extraction of verdict lines via grep.

F-CASE audit: for each of r3c.zag, r1c.zag, frcc.zag, run
git diff --no-index <frozen-base> <new-file>, take added/modified
lines, grep for the section-5.1 literal set; also manual review of
the combiner and COND evaluator against audits 2-5.

## 8. Verdict rule

CONDITIONAL-PASS iff ALL of the following hold:

- K1: this prereg commit strictly precedes the implementation commit
  (commit-order self-check).
- K2: all runs complete (R3, R1, FREC batteries, 3 runs each).
- K3: pure Zag at every stage (zero Python), 3/3 byte-identical per
  battery, zero stderr.
- P1: CONDHIT round <= 2.
- P2: A2-PASS == 1.
- P3: DROUND(r3c) < 4 (with -1 mapped to 25).
- P4: A1-PASS == 1, R1 PASS_SEEDS >= 0/5, FREC I1 >= 46/64,
  I2 >= 63/64, I3 >= 40/64.
- F-CASE: none of the six audits fires.

Otherwise CONDITIONAL-FAIL, with the failing bar named. Partial
passes are reported as diagnostics, never as a pass.

## 9. Honest scope

Bounded-L2 search-architecture experiment only. No L3 claim, no
Criterion 0 claim. COND is researcher-supplied, exactly like AND, OR,
XOR, NOT. The novelty claim is limited to: a conditional-first
search representation (BAP plus combiner) repairs the measured
compositional-generation bottleneck on R3 Arm 2. The mechanism does
not invent conditionals, does not choose its own representation, and
does not revise its alphabet.

CONDITIONAL-PREREG-FROZEN.
