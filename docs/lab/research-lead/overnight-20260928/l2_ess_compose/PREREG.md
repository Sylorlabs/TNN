# PREREG: L2-ESS-COMPOSE (operator standing in the composition learner)

Status: PREREG-FROZEN. No implementation exists at this commit and none
is built in this lane until after the freeze commit. This file holds the
frozen experimental design: the question, the standing integration, the
five arms, the predicted trajectories, the frozen kill bars (KB-*), the
falsifiers, and the T1-T8 compliance statement. A later REPORT.md records
the verdict against these bars. Non-ledger task (claim minting paused).
Scope: `docs/lab/research-lead/overnight-20260928/l2_ess_compose/`
Worker: L2-ESS-COMPOSE subagent (depth 2/2), 2026-10-03.

## 1. Question

L2-ESS-CURRICULUM showed operator standing (per-(op, context) SUC/FAIL/
STRK cells, MR-OP-STANDING-SKIP gating, probation recovery) saves trials
on single-operator meta-reuse queries (H1 SURVIVES, H0 FALSIFIED).
L2-COMPOSE-CHAIN3 showed the frozen phase-2 (fixed [1..6] enumeration
retried over Z sources) composes the [6,5,4] chain with zero learner
changes. This lane asks: does the composition learner benefit from
operator standing? (a) efficiency: fewer tries on the [6,5,4] chain;
(b) correctness: no wrong skips (every skipped operator would have
failed); (c) probation: recovery when a retired operator becomes viable
after a context change.

## 2. Standing integration (frozen design)

Base: `../l2_compose_chain3/learner.zag`, zero operator-semantic
changes. Only additions: standing records + gating.

### 2.1 Cell table

Per (operator, source, signature): 6 ops x 16 MAP ids x 32 sigs x 4
bytes [SUC,FAIL,STRK,QTOUCH] at
`1412 + (((op-1)*16 + src)*32 + sig)*4`, i.e. 1412..13699 (12288 bytes).
The source id is part of the key: composition tries the same operator
against DIFFERENT sources (taught source, Z4, Z5, Z6) within one query,
and a naive per-(op,sig) key would let phase-2 failures on Z4 strike the
cell that phase-2 on Z5 needs (predicted: op 4 struck on Z4/sig6, then
wrongly skipped on Z5/sig6, breaking the QD3 [6,5,4] third link). The
(src) key is the composition-setting analogue of ESS P5 context
sensitivity. Mode 2 (GLOBAL ablation): src forced 0, sig forced 0, i.e.
pure per-operator cells (the over-retirement rival).

Control i32s: 13700 STANDING_MODE, 13704 TRIEDMASK_P1, 13708
TRIEDMASK_P2. No existing state offset moves; driver buffers 8192 ->
16384 bytes.

### 2.2 Gate (st_standing_eval, frozen algebra from ESS)

Mode 0 (UNGATED): return 0 immediately (no touch, no print delta).
Mode 1: sig = st_sig(st, s, src); mode 2: src=0, sig=0.
QTOUCH = min(255, QTOUCH+1) on every consult.
struck = (STRK>=3) OR (SUC*2 < FAIL).
Not struck -> 0 (try). Struck and QTOUCH>=8 -> probation: QTOUCH=0,
return 2 (try, caller prints MR-OP-PROBATION / MR-COP-PROBATION).
Struck and QTOUCH<8 -> return 1 (skip, caller prints
MR-OP-STANDING-SKIP / MR-COP-STANDING-SKIP).

### 2.3 Context signature (st_sig, ESS formula, chain3 MAP base)

em = 1 iff any live fact has sub==s AND rel==d_entry(src); nf =
d_nf(src) clamped 0..7; pat = 1 iff d_entry==0.
sig = em*16 + nf*2 + pat (0..31). Generic over (query start, source
descriptor); no world/answer literals.

### 2.4 Updates (st_standing_upd, learner write path only)

Called (a) after phase 1 keyed (s, agg_src) with TRIEDMASK_P1, and
(b) after each Z source's phase-2 enumeration keyed (s, zsrc) with
TRIEDMASK_P2 (reset per Z source). For each tried op: committed ->
SUC=min(255,SUC+8), STRK=0, FAIL=FAIL/2; tried-not-committed ->
FAIL=min(255,FAIL+4), STRK=min(255,STRK+1). Untried (masked or
skipped): no update. Prints MR-STANDING-UPD ph=1/2 op= src= sig=
suc= fail= strk=. Modes 1-2 only.

### 2.5 Gating points

Phase 1 (mr_adapt over agg_src): each of the 6 MR-OP blocks consults
the gate keyed (s, agg_src); TRY/PROBATION sets the TRIEDMASK_P1 bit
and MR_OP_TRIES++; SKIP prints MR-OP-STANDING-SKIP.
Phase 2 (per-Z-source enumeration): each of the 6 MR-COP blocks
consults the gate keyed (s, zsrc); TRY/PROBATION sets the
TRIEDMASK_P2 bit and MR_OP_TRIES++; SKIP prints
MR-COP-STANDING-SKIP. In mode 0 the trace is byte-identical to the
chain3 baseline (no new tags; triedmask writes are state-only).

### 2.6 Driver

`mr_standing_arm(st, mode)` per arm (arm-level causal-control flag,
analogous to OP_MASK; the driver never reads/writes cells,
thresholds, or signatures). Queries are (start,terminal,value,cap,dom)
with arm-level mode + OP_MASK only.

## 3. Arms (one binary, five sequential arms, fresh state each)

- ARM UNGATED (mode 0): E-world FULL sequence, mask 63: QA(20,25,51),
  QD1(90,97,59), QD2(140,148,63), QD3(160,167,65), QD4(170,174,66),
  QD1-B, QD2-B, QD3-B. Baseline; must reproduce chain3 build-E
  signatures (QD1 op=6 tries=6; QD2 op=5 tries=11; QD3 op=4 tries=16;
  QD4 tries=24 val=-2).
- ARM STANDING (mode 1): identical sequence.
- ARM GLOBAL (mode 2): identical sequence (informational ablation).
- ARM PROB-UNG (mode 0): small probation world (section 4):
  PQ1..PQ7 = (10,990-k,61) k=0..6; driver teaches 6 recovery facts;
  PQR = (10,24,62).
- ARM PROB (mode 1): identical to PROB-UNG.

## 4. Probation world (driver-taught, 12 facts total, cap 44 untouched)

Initial: F0 (10,21,11) F1 (11,22,12) F2 (12,23,13) F3 (13,22,14)
F4 (14,23,15) F5 (15,4,61); MAP mP0 id 0: rels [21,22,23,22,23],
facts [0..4], start=10, end=15, dom=1, cap=1 ->
d_entry=21, d_r1=22, d_r2=23, d_nf=2, d_valrel=4.
sig(10, src=0) = 1*16+2*2+0 = 20 (F0 gives em=1; unchanged by the
recovery facts).
PQ1..PQ7 (10,990-k,61): unsolvable by design (terminal unreachable);
direct execution fails (mP0 walks 10->15); no route source exists for
op 1 (single MAP); op 6 has no pattern MAP (d_entry=21 != 0); phase 2
has no Z sources (nothing builds). All six ops fail in UNGATED.
Recovery facts (driver-taught after PQ7): (10,23,20) (20,22,21)
(21,23,22) (22,22,23) (23,23,24) (24,4,62).
PQR (10,24,62): op 2 verifies via candidate (10,23,20): foldwalk
20 -22-> 21 -23-> 22 -22-> 23 -23-> 24, term=24==t,
valof(24,4)=62==v. op 1 cannot verify (no cross-cap route source in
this world, by construction). Direct execution still fails
(mP0 10->15 != 24); no inverse Z exists (pipeline clear).
Predicted (op2, src=0, sig=20) trajectory in ARM PROB: PQ1
tried/fail -> (0,4,1); PQ2..PQ7 skipped (QTOUCH 2..7); PQR QTOUCH=8
-> MR-OP-PROBATION 2, tried/verify -> commit op=2 val=62 ->
(8,4,0).

## 5. Predicted main-sequence trajectories (STANDING arm)

Phase-1 cells are (op, src=1, sig=4) for all QD queries (s in
{90,140,160,170} never has a live (s,21,?) fact; d_nf(mA')=2).
- QD1: all fresh; ops 1-5 fail -> (0,4,1); op 6 verifies -> (8,0,0).
  tries=6. Z4 (id 3) built.
- QD2 phase 1: ops 1-5 struck, QTOUCH=2 -> skipped; op 6 (8,0,0)
  tried -> fail -> (8,4,1). tries=1. Phase 2 on Z4 (src=3,
  sig=22: em=1 via (140,29,142)): ops 1-4 fail -> (0,4,1); op 5
  verifies -> (8,0,0). tries=1+5=6. Z5 (id 4) built.
- QD3 phase 1: ops 1-5 skipped (QTOUCH=3); op 6 tried -> (8,8,2).
  tries=1. Phase 2 on Z4 (src=3, sig=6: em=0): all 6 fail ->
  (0,4,1). tries=7. Phase 2 on Z5 (src=4, sig=6): ops 1-3 fail ->
  (0,4,1); op 4 Form A verifies -> (8,0,0), commit. tries=11.
  Z6 (id 5) built.
- QD4 phase 1: ops 1-5 skipped (QTOUCH=4); op 6 tried -> (8,12,3)
  struck. tries=1. Phase 2 on Z4 (src=3, sig=6): all skipped
  (QTOUCH=2). Phase 2 on Z5 (src=4, sig=6): ops 1-3 skipped; op 4
  (8,0,0) tried -> fail -> (8,4,1); ops 5,6 fresh tried -> fail ->
  (0,4,1). tries=4. Phase 2 on Z6 (src=5, sig=22: em=1 via
  (170,23,171), d_entry(Z6)=23): all fresh, all fail -> (0,4,1).
  tries=10. QD4 val=-2.
Predicted tries QD1..QD4: UNGATED 6+11+16+24=57; STANDING
6+6+11+10=33 (saving 24).

GLOBAL arm (informational) predicted: QD1 ok (tries=6); QD2 phase-2
op 5 globally struck after its QD1 phase-1 failure -> skipped ->
QD2 val=-2 (Z5 never built); QD3/QD4 val=-2. Demonstrates the
(src,sig) key is load-bearing vs per-operator retirement.

## 6. Frozen kill bars

- KB-EFF (efficiency): in-Zag. sum(tries QD1..QD4) STANDING <
  UNGATED, and (UNGATED - STANDING) >= 10.
- KB-CORR (correctness): in-Zag. QA/QD1/QD2/QD3: via, val, op equal
  STANDING vs UNGATED; QD4: val==-2 and op==-1 in both;
  d_check_z4/z5/z6 == 1 in both; QD1-B/QD2-B/QD3-B: via and val
  equal.
- KB-NOSKIP (no wrong skips): shell-paired. Every
  MR-OP-STANDING-SKIP N / MR-COP-STANDING-SKIP N in ARM STANDING
  on query Q pairs with MR-OP-FAIL N / MR-COP-FAIL N in ARM
  UNGATED on Q. Bound is ZERO OK-withheld; any violation fires
  F-D.
- KB-PROB (probation recovery): (a) in-Zag: PROB-UNG PQR op==2
  val==62 and PQ1..PQ7 val==-2 (world-change sanity: the solver
  exists); (b) in-Zag: PROB PQR op==2 val==62 and PQ1..PQ7
  val==-2; (c) shell: PROB trace shows MR-OP-PROBATION 2 in the
  PQR section, and MR-STANDING-UPD shows (op=2,src=0,sig=20)
  struck before PQR.
- KB-SEAL: shell grep of driver.zag: zero hits for operator names,
  form names, trace tags, standing offsets (1412/13700/13704/
  13708), threshold literals, signature literals.
- KB-DET: 3/3 byte-identical runs per binary (sha256).

## 7. Verdict rule

- PASS iff KB-EFF, KB-CORR, KB-NOSKIP, KB-PROB, KB-SEAL, KB-DET
  all hold and no falsifier fires.
- F-D (wrong skip): any standing skip withholding an operator that
  verifies in UNGATED on the same query -> verdict FAIL (this
  standing algebra is wrong for composition; retry only as a new
  algebra under a new prereg).
- F-EFF: KB-EFF fails -> standing does not improve composition
  efficiency -> verdict FAIL on the efficiency question.
- F-PROB: KB-PROB fails -> probation does not recover in the
  composition setting -> verdict FAIL on the recovery question.
- The GLOBAL arm is informational (predicted over-retirement);
  its outcome is reported, not a bar.

## 8. T1-T8 compliance

T1: this frozen prereg, committed before implementation. T2/T3:
driver only sets arm mode and teaches world facts/MAPs; write path
learner-side only (KB-SEAL audit). T4: KB-DET. T5: pure Zag,
safebin, pinned znc (NAMECHECK Step 0). T6: no new modes/bridges/
handlers/edge types/opcodes/semantic cases; only learner state
(the cell table + 3 i32s) and hypothesis-named trace tags.
T7: st_sig is generic over (query start, source descriptor);
KB-SEAL audits for literals. T8: KB-NOSKIP states the zero bound
and F-D states the verdict on exceeding it.

## 9. Commit-order self-check

PREREG.md + NAMECHECK.md committed alone at the freeze commit; no
implementation exists. Implementation and REPORT.md follow only
after.
