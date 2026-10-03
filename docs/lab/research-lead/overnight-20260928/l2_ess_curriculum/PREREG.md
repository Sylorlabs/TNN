# PREREG: L2-ESS-CURRICULUM (two-family test of H-OP-ESS)

Status: PREREG-FROZEN. No implementation exists at this commit and none
is built in this lane until after the freeze commit. This file holds the
frozen experimental design: the two families, the four arms, the standing
algebra with exact constants, the context-signature function, the
preregistered kill bars (KB-*), the falsifiers, and the T1-T8 compliance
statement. A later REPORT.md records the verdict against these bars.
Non-ledger task (claim minting paused).
Scope: `docs/lab/research-lead/overnight-20260928/l2_ess_curriculum/`
Worker: L2-ESS-CURRICULUM-RETRY subagent (depth 2/2), 2026-10-03.
Parent hypothesis: `../l2_ess_hypothesis/HYPOTHESIS.md` (H1: operator
standing IS ESS, instance #5, second-order procedure-level; H0 preserved:
operators should NOT have ESS; H0 falsified iff P2+P3+P5 jointly
observed). This prereg is the "future experiment lane" its section 10
calls for, with its own frozen bars per T1-T8.

## 1. Question

Does the learner-written per-(operator, context-signature) standing
record (SUC/FAIL/STRK cells, gating via MR-OP-STANDING-SKIP, probation
recovery) (a) diverge from the ungated baseline with behavioral
consequence (P2), (b) recover by graded probation dynamics after a
strike-latch retirement (P3), and (c) beat a global per-operator cell
that over-retires (P5), on a SECOND world family genuinely different
from L2-INVERT-VALUE? Joint P2+P3+P5 falsifies H0.

## 2. Families

Family A (existing evidence, reused unchanged in structure): the seven
L2-INVERT-VALUE queries against sources mD/mA/mB0/mP, all six operators
each necessary for their query class (K5 ablation stands):
q0 QCOMB (90,86,42,cap1,dom2) op1; q1 QSUB (200,43,11,cap1,dom1) op2;
q2 QTRUNC (100,42,32,cap1,dom1) op3; q3 QINV (120,127,60,cap1,dom1) op4;
q4 QABS (150,166,77,cap1,dom1) op5; q5 QCONC (210,234,91,cap1,dom1) op6;
q6 QINVVAL (11,100,11,cap1,dom1) op4. Expected vals:
42/11/32/60/77/91/11.

Family B (NEW, genuinely different structure and operator-viability
profile): a new source region with disjoint relations, a new source MAP
mX, and queries solvable by a different operator mix while op 2
(SUBSTITUTE) is the systematic failure (the stale specialist).

New world facts (appended after the 44 frozen facts; fact region grows
44 -> 56; see section 6):
- 44:(300,51,310) 45:(310,52,311) 46:(311,53,312) 47:(312,54,71)
- mX: rs=[51,52,53], fs=[44,45,46], start=300, end=312, dom=3, cap=3.
  Descriptor (generic m_teach derivation, extended to cap 3 per
  section 6): d_entry=51, d_r1=52, d_r2=53, d_nf=1, d_valrel=54.
- Family-B queries (cap=3, dom=3, agg_src=mX by the frozen first-live
  MAP rule):
  - q7 QABS2 (300,312,71): op 5 ABSTRACT solves (entry (300,51,310),
    1-fold walk 310->311->312, valof(312,54)=71). Ops 1-4 fail.
    op 2 fails: zero entry candidates (only fact with sub==300 is
    (300,51,310), rel == d_entry).
  - q8 QINVB (71,300,71): op 4 Form B solves (reverse lookup v=71 ->
    fact 47 (312,54,71), tstar=312 == mX end, backward walk
    312->311->310->300, key 300 == t). Ops 1-3 fail (no sub==71
    facts; truncate dnf=1 never tries). op 2 fails: no candidates.
  - q9..q14 QX3..QX8 (300,999,71),(300,998,71),(300,997,71),
    (300,996,71),(300,995,71),(300,994,71): UNSOLVABLE by design
    (terminals unreachable; value 71 belongs to mX's terminal 312,
    not to these terminals). All six operators fail in the ungated
    baseline. op 2 fails on each (no candidates). These queries exist
    to drive the strike latch and then exhibit the skip.
- Context signatures (section 5): q7 sig=(em=1,nf=1,pat=0)=18;
  q8 sig=(em=0,nf=1,pat=0)=2; q9..q14 sig=18. Family A sigs are
  (em,nf=3,pat=0) in {2+16=18? no: (0,3,0)=6, (1,3,0)=22}; in packed
  form family A uses sig 6 and 22, family B uses sig 18 and 2.
  Disjoint cell sets: no family-A query touches a family-B cell.

Family B-prime (world change, then recovery): between q14 and q15 the
driver teaches 8 more facts (world change, driver-side teaching, not
learner state):
- 48:(300,61,320) 49:(320,52,321) 50:(321,53,322) 51:(322,54,72)
- 52:(300,62,330) 53:(330,52,331) 54:(331,53,332) 55:(332,54,73)
- q15 B1 (300,322,72,cap3,dom3): op 2 now viable via candidate
  (300,61,320) (rel 61 != 51): foldwalk 320->321->322, terminal 322,
  valof(322,54)=72. Solvable ONLY by op 2 (op 3: dnf=1 never tries;
  op 4B: v=72 -> fact 51, tstar=322 != mX end 312, FAIL; op 4A:
  reversed rels [53,52,51] from 300, no (300,53,?) fact, FAIL;
  op 5: foldwalk terminal 312 != 322, FAIL; op 6 must fail, verified
  at runtime by KB-FAM-B).
- q16 B2 (300,332,73,cap3,dom3): op 2 via candidate (300,62,330)
  (candidate (300,61,320) tried first, verifies to 322 != 332, then
  (300,62,330) verifies to 332, valof=73). Solvable ONLY by op 2.

## 3. Arms (one binary, four sequential arms, fresh state each)

- ARM UNGATED (mode 0): standing machinery disabled. Baseline.
- ARM STANDING (mode 1): per-(operator, sig) cells (the H1 record).
- ARM GLOBAL (mode 2): ablation, single global per-operator cell
  (sig forced 0). Tests P5.
- ARM RIVAL (mode 3): F-A stateless pre-check arm. Before trying op 2
  only, scan live facts for sub==s AND rel != d_entry(agg_src); if none,
  print MR-RIVAL-SKIP 2 and skip the trial (no persistent state, no
  updates, no strike lag, no probation). All other operators tried
  normally. This is the explicit rival HYPOTHESIS.md section 8 F-A
  names.

Mode is an arm-level causal-control flag set by the driver through the
learner-side setter mr_standing_arm(st, mode), analogous to OP_MASK
(per ARM, never per query). The driver never reads or writes standing
cells, thresholds, or signatures (T2/T3; audited by KB-P4).

Each arm runs: Phase A (q0..q6), Phase B (q7..q14), teach facts 48..55,
Phase B-prime (q15..q16). OP_MASK=63 throughout.

## 4. Standing algebra (frozen constants)

Per cell (op in 1..6, sig in 0..31): SUC u8, FAIL u8, STRK u8,
QTOUCH u8 (queries touching the cell). 6*32*4 = 768 bytes at
state offset 1488 (see section 6). Cold start (0,0,0,0) is always
tried.

- Gating (mr_adapt, after mask-bit check, before MR-OP-TRY N):
  compute sig (mode 1) or 0 (mode 2); QTOUCH=min(255,QTOUCH+1);
  struck = (STRK>=3) OR (SUC*2 < FAIL). If not struck: try normally.
  If struck and QTOUCH>=8: probation, print MR-OP-PROBATION N,
  QTOUCH=0, try the operator. If struck and QTOUCH<8: print
  MR-OP-STANDING-SKIP N, skip (no trial, no ticks, no update).
- Update (op_standing_update, learner post-query path, after mr_adapt
  returns, only if the meta phase ran with agg_src>=0; modes 1-2 only):
  for each op whose TRIEDMASK bit is set (tried via TRY or PROBATION):
  on commit (op == MR_OP and MR_OP_DECIDED): SUC=min(255,SUC+8),
  STRK=0, FAIL=FAIL/2. On trial failure (tried, not committed):
  FAIL=min(255,FAIL+4), STRK=min(255,STRK+1). Untried ops (masked off
  or standing-skipped): no update; the record learns only from trials.
  Prints MR-STANDING-UPD op= sig= suc= fail= strk= per updated cell.
- TRIEDMASK: learner i32 bitmask (offset 2260), bit N-1 set when op N
  is tried; reset at mr_adapt entry.
- STANDING_MODE: learner i32 (offset 2256), written only by
  mr_standing_arm (driver-called per arm).

Predicted cell trajectory for (op2, sig=18) in ARM STANDING:
q7 tried/fail -> (0,4,1); q9 tried/fail -> (0,8,2);
q10 tried/fail -> (0,12,3) STRIKE; q11..q14 skipped (no update);
q15 probation tried/OK -> (8,6,0); q16 tried/OK -> (16,3,0).
Graded recovery, not a binary flip.

Predicted ARM GLOBAL trajectory for op 2 (global cell): q1 OK ->
(8,0,0); q2 fail -> (8,4,1); q3 fail -> (8,8,2); q4 fail ->
(8,12,3) STRIKE; q5..q8 skipped; q8 is the 8th touch -> probation
tried/fail -> re-strike; q9..q14 skipped; q15 skipped (WRONG: op 2
would verify; query lost, val=-2); q16 8th touch -> probation
tried/OK (late recovery).

## 5. Context signature (frozen)

st_sig(st, s, agg_src): em = 1 if any live fact has sub==s AND
rel==d_entry(agg_src) else 0; nf = d_nf(agg_src) clamped to 0..7;
pat = 1 if d_entry==0 else 0. sig = em*16 + nf*2 + pat
(SIGMAX=32). Generic function over (query start, source descriptor);
no world/answer literals, no family labels, no researcher-enumerated
property lists (T7; audited by KB-P4).

## 6. Implementation notes (frozen)

- Base: the L2-INVERT-VALUE harness (learner/world/driver), extended.
- Fact region grows 44 -> 56 facts: state layout shifts +96 bytes
  (facts 16..463; MAPs 464..1103; edges 1104..1359; answers
  1360..1423; i32 fields 1424..1487; standing cells 1488..2255;
  STANDING_MODE 2256; TRIEDMASK 2260). f_teach cap 44 -> 56;
  candidate buffers z_alloc(44) -> z_alloc(64).
- m_teach descriptor derivation extended from (cap==1) to
  (cap==1 OR cap==3): generic (d_entry=rels[0], alternating fold
  pair, d_valrel=rel of first live fact with sub==end); no relation
  or world literals. Needed so mX (cap=3) gets a real descriptor;
  family-A behavior (cap=1) unchanged.
- No new modes, bridges, handlers, edge types, opcodes, or semantic
  cases (T6). New learner state: the 768-byte cell table + 2 i32s.
  New trace tags (HYPOTHESIS.md section 5): MR-OP-STANDING-SKIP N,
  MR-OP-PROBATION N, MR-STANDING-UPD. Rival tag: MR-RIVAL-SKIP 2.
- Pure Zag, safebin, pinned znc (T5). Determinism: 3/3 byte-identical
  (T4, KB-DET).

## 7. Frozen kill bars

- KB-FAM-A (harness sanity): ARM UNGATED q0..q6 commit ops
  1,2,3,4,5,6,4 with vals 42,11,32,60,77,91,11. (Guards against
  breakage from the layout shift and m_teach extension.)
- KB-FAM-B (new-family sanity): ARM UNGATED q7 op==5 val==71;
  q8 op==4 val==71; q9..q14 val==-2 (all six operators fail);
  q15 op==2 val==72; q16 op==2 val==73.
- KB-P1 (gating saves): for each of q11..q14,
  as(UNGATED)-as(STANDING) >= 48 (48 = the fact count during phase B;
  each skipped op-2 trial saves at least the full 48-tick candidate
  scan); and q7,q8 committed op/via/val identical across
  UNGATED and STANDING.
- KB-P2 (divergence): at least one phase-B query where ARM UNGATED
  prints MR-OP-TRY 2 followed by MR-OP-FAIL 2 and ARM STANDING prints
  MR-OP-STANDING-SKIP 2 with no MR-OP-TRY 2 (shell grep on the trace;
  expected on q11..q14, four instances).
- KB-P3 (reversibility): (a) ARM STANDING q15 prints
  MR-OP-PROBATION 2 and commits op==2 val==72 (in-Zag);
  (b) the MR-STANDING-UPD trace shows cell (op=2,sig=18) moving
  (0,12,3) -> (8,6,0) -> (16,3,0) across q15,q16 (graded recovery,
  shell grep); (c) trials restored on the FIRST B-prime exposure,
  i.e. within K=8 touching queries (in-Zag: q15 op==2).
- KB-P5 (learned context beats global): ARM GLOBAL q15 prints
  MR-OP-STANDING-SKIP 2 and commits val==-2 (query lost to
  over-retirement), while ARM STANDING q15 commits val==72 via op 2
  (in-Zag: val[q15] GLOBAL==-2 AND val[q15] STANDING==72).
- KB-P4 (learner-written, T2/T3): grep of driver.zag yields zero hits
  for operator names, form names, trace tags, standing offsets,
  thresholds, signature literals (K3/K7-style audit).
- KB-F-A (rival): ARM RIVAL's op-2 skip/trial decisions differ from
  ARM STANDING's on at least one query (expected: q2 QTRUNC, q7, q9,
  q10: RIVAL prints MR-RIVAL-SKIP 2 where STANDING prints MR-OP-TRY 2).
  If the rival reproduced every decision, F-A would fire; a single
  difference keeps F-A unfired.
- KB-F-D (wrong-skip bound, T8): bound is ZERO. For every
  MR-OP-STANDING-SKIP N in ARM STANDING, ARM UNGATED's trial of op N
  on the same query must show MR-OP-FAIL N (never MR-OP-OK N).
  Shell-paired per query. If any skip withholds an operator that the
  ungated baseline verifies, F-D fires and the verdict is H0
  (operators should NOT have ESS), per HYPOTHESIS.md section 8.
- KB-DET (T4): 3/3 byte-identical runs (sha256).

## 8. Verdict rule

- H1 SURVIVES iff KB-FAM-A, KB-FAM-B, KB-P1, KB-P4, KB-DET pass and
  no falsifier (F-A, F-D) fires.
- H0 FALSIFIED iff KB-P2 AND KB-P3 AND KB-P5 jointly pass
  (HYPOTHESIS.md section 9: divergence + endorsement-like
  strike/probation dynamics + context-sensitive distrust a stateless
  pre-check cannot reproduce).
- F-D firing -> verdict H0 (this E algebra is wrong; retry only as a
  new algebra under a new prereg).
- F-A firing -> ESS category claim dies (record may survive as an
  optimization); verdict "learned policy", H1 fails as ESS.

## 9. T1-T8 compliance

T1: this frozen prereg, kill bars KB-* above, committed before
implementation. T2/T3: KB-P4 audit; write path learner-side only
(section 4). T4: KB-DET. T5: pure Zag, safebin, pinned znc (Step 0).
T6: no new modes/bridges/handlers/edge types/opcodes/semantic cases;
only learner state + the hypothesis-named trace tags. T7: section 5
generic signature; KB-P4 audits for literals. T8: KB-F-D states the
zero bound and the verdict on exceeding it.

## 10. Commit-order self-check

PREREG.md + NAMECHECK.md committed alone at the freeze commit; no
implementation existed. Implementation and REPORT.md follow only after.
