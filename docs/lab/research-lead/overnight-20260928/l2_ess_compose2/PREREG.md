# PREREG: L2-ESS-COMPOSE2 (operator standing x [6,2,4] composition)

Frozen 2026-10-03 by the L2-ESS-COMPOSE2 worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

L2-ESS-COMPOSE-PASS showed operator standing transfers
to the [6,5,4] composition learner (57 -> 33 tries,
zero wrong skips), with the refinement that the
standing cell key must be per-(op, *src*, sig), not
per-(op,sig). L2-COMPOSE-CHAIN3B-PASS showed [6,2,4]
(CONCRETIZE -> SUBSTITUTE -> INVERT Form B) composes
on the frozen mechanism: [6,5,4] is not special.

This wave tests whether the standing mechanism
generalizes to the DIFFERENT triple [6,2,4]. The
standing learner is reused BYTE-IDENTICAL from
l2_ess_compose (zero source changes); only the world
(world_H.zag, the [6,2,4] world) and the driver are
new. If standing improves efficiency with correctness
preserved and zero wrong skips on [6,2,4], the
per-(op,src,sig) design generalizes beyond [6,5,4].
If it fails, the wave reports which discriminator
pattern breaks it, not a bare negative.

## 2. The standing mechanism under test (unchanged)

From the l2_ess_compose REPORT (mechanism reused
byte-identical, not re-derived):

- Cell table: 6 ops x 16 MAP ids x 32 sigs x 4B
  [SUC,FAIL,STRK,QTOUCH] at
  1412+(((op-1)*16+src)*32+sig)*4. Source id is part
  of the key.
- Gate (st_standing_eval): mode 0 = immediate try;
  mode 1 = (op,src,sig) cells; mode 2 = (op,0,0)
  global cells. struck = (STRK>=3) OR (SUC*2<FAIL);
  probation at QTOUCH>=8.
- Context signature st_sig = em*16+nf*2+pat
  (em = entry-match flag, nf = d_nf clamped 0..7,
  pat = d_entry==0).
- Updates (st_standing_upd, learner-side only):
  after phase 1 keyed (s,agg_src); after each Z
  source keyed (s,zsrc). Commit -> SUC+8/STRK=0/
  FAIL/=2; tried-not-committed -> FAIL+4/STRK+1.
- Gating at all 12 enumeration blocks with
  TRIEDMASK_P1/P2 and phase-appropriate tags.

## 3. Why [6,2,4] is a discriminating test

[6,2,4]'s middle link is SUBSTITUTE with the
de-MISMATCH discriminator (entry rel != de(src)),
dual to ABSTRACT's de-match. The standing key must
separate op2's QD2-phase-1 failure on taught
(src=1, sig=4) from op2's QD2-phase-2 success on Z1
(src=3, sig=6), and must let op2 be tried (not
skipped) on Z1 again in QD3 where it correctly
fails.

The load-bearing per-(op,src,sig) moment: in QD3,
phase 2 visits Z1 then Z2 under the SAME signature
(sig=6: s=68, em=0, nf=3 on both). op4 (INVERT)
fails on Z1 and must still fire on Z2. With a
per-(op,sig) key, QD3's op4 failure on Z1 would
strike the shared (4,6) cell and op4 on Z2 would be
wrongly skipped, breaking the chain. With
per-(op,src,sig), (4,3,6) is struck but (4,4,6) is
fresh, so op4 fires on Z2. This wave's KB-NOSKIP
directly tests that the src in the key carries the
[6,2,4] chain.

## 4. Hand-derived predicted standing trace (world_H)

Signatures on world_H (agg mA' id 1: de=21, dnf=2;
Z1 id 3: de=29, dnf=3; Z2 id 4: de=23, dnf=3;
Z3 id 5: de=4, dnf=3):

- Phase 1 (src=1): QD1..QD4 all sig=4
  (em=0: no live (s,21,*) fact; nf=2).
- Phase 2 Z1 (src=3): sig=6 (em=0, nf=3).
- Phase 2 Z2 (src=4): QD3 sig=6 (em=0);
  QD4 sig=22 (em=1: f32=(190,23,191)).
- Phase 2 Z3 (src=5): QD4 sig=6 (em=0).

QA (20,25,51): pipeline hit, via=1, val=51. No
standing activity (unchanged from ESS).

QD1 (90,97,59): phase-1 sig=4, all cells fresh:
op1..op5 FAIL, op6 OK. tries=6, op=6, dec=1,
via=3, val=59. Z1 built. Update: (1..5,1,4) =
FAIL4/STRK1; (6,1,4) = SUC8.

QD2 (180,187,67): phase-1 sig=4: ops 1-5 SKIP
(struck (0,4,1)); op6 TRY (SUC8) -> FAIL
(OLD-FOLDS). tries=1. Update: (6,1,4) = (8,4,1).
Phase-2 Z1 sig=6, fresh: op1 FAIL, op2 OK.
tries=3, op=2, dec=1, via=4, val=67. Z2 built.
Update: (2,3,6) = SUC8; (1,3,6) = FAIL4/STRK1.

QD3 (68,180,68): phase-1 sig=4: ops 1-5 SKIP;
op6 TRY (16<4 false) -> FAIL. tries=1. Update:
(6,1,4) = (8,8,2). Phase-2 Z1 sig=6: op1 SKIP
(struck); op2 TRY (SUC8) -> FAIL; op3..op6 TRY
(fresh) -> FAIL. tries=6. Update: (2,3,6) =
(8,4,1); (3..6,3,6) = FAIL4/STRK1. Phase-2 Z2
sig=6, fresh: op1..op3 FAIL, op4 OK Form B.
tries=10, op=4, dec=1, via=5, val=68. Z3 built.
Update: (4,4,6) = SUC8; (1..3,4,6) = FAIL4/STRK1.

QD4 (190,194,69): phase-1 sig=4: ops 1-5 SKIP;
op6 TRY (16<8 false) -> FAIL. tries=1. Update:
(6,1,4) = (8,12,3). Phase-2 Z1 sig=6: op1 SKIP;
op2 TRY (16<4 false) -> FAIL; op3..op6 SKIP
(struck). tries=2. Update: (2,3,6) = (8,8,2).
Phase-2 Z2 sig=22, fresh: 6 tried, all FAIL.
tries=8. Phase-2 Z3 sig=6, fresh: 6 tried, all
FAIL. tries=14, op=-1, dec=0, val=-2.

Re-asks QD1-B/QD2-B/QD3-B: pipeline hits, via=3/4/5,
val=59/67/68, entered=0. No standing activity.

Predicted totals: UNGATED 6+8+16+24=54; STANDING
6+3+10+14=33; savings 21. Standing skips: QD2 5
(phase-1 ops 1-5), QD3 6 (phase-1 ops 1-5, Z1 op1),
QD4 10 (phase-1 ops 1-5, Z1 ops 1,3,4,5,6) = 21,
matching 54-33.

## 5. Frozen predicted outcomes (build H2)

### 5a. UNGATED arm (mode 0, mask 63)

Identical to chain3b build H FULL (frozen
predictions, H-K3/H-K4): QA via=1 val=51;
QD1 op=6 tries=6 dec=1 via=3 val=59 Z1-exact=1;
QD2 op=2 tries=8 dec=1 via=4 val=67 Z2-exact=1;
QD3 op=4 tries=16 dec=1 via=5 val=68 Z3-exact=1;
QD4 op=-1 tries=24 dec=0 val=-2; re-asks via=3/4/5
val=59/67/68 entered=0; u_sum=54.

### 5b. STANDING arm (mode 1, mask 63)

QA via=1 val=51; QD1 op=6 tries=6 via=3 val=59
Z1-exact=1; QD2 op=2 tries=3 via=4 val=67
Z2-exact=1; QD3 op=4 tries=10 via=5 val=68
Z3-exact=1; QD4 op=-1 tries=14 val=-2 dec=0;
re-asks via=3/4/5 val=59/67/68 entered=0;
s_sum=33. Z1/Z2/Z3 rows field-identical to UNGATED.

### 5c. GLOBAL arm (mode 2, mask 63; informational)

Predicted: QD1 op=6 val=59 tries=6; QD2 reroutes
via op6 on Z1 (op=6, val=67, tries=2; global cells
do not distinguish sources, so op2 is globally
struck but op6's global SUC lets it fire); QD3
val=-2 (op4 globally retired after QD1/QD2
failures, the INVERT link never fires, chain
broken); QD4 val=-2. Informational only: the
load-bearing prediction is QD3 val=-2 under GLOBAL
while STANDING solves QD3 (val=68), confirming the
(src,sig) key is load-bearing for [6,2,4] too.

### 5d. Probation arms (ESS probation world, reused)

PROB-UNG (mode 0): PQ1..PQ7 val=-2; PQR op=2
val=62. PROB (mode 1): PQ1..PQ7 val=-2; PQR op=2
val=62; PQR trace shows MR-OP-PROBATION then
MR-OP-OK 2 (strike -> skip -> QTOUCH=8 ->
probation -> verify -> commit).

## 6. Frozen kill bars (build H2)

- KB-EFF (efficiency): s_sum < u_sum AND
  (u_sum - s_sum) >= 10. Predicted: 33 < 54,
  savings 21.
- KB-CORR (correctness): for QA/QD1/QD2/QD3/QD4
  and the three re-asks, via/val/op identical
  between UNGATED and STANDING; Z1/Z2/Z3 exact
  checks = 1 in both arms; d_check rows equal
  field by field.
- KB-NOSKIP (no wrong skips): every
  MR-OP-STANDING-SKIP / MR-COP-STANDING-SKIP in the
  STANDING arm is paired with a same-query
  same-phase FAIL of the same op in the UNGATED
  arm; zero OK-withheld (F-D does not fire). The
  verifying operators (op2 on Z1 in QD2, op4 on Z2
  in QD3) are never skipped: their phase-2 cells
  are fresh per (src,sig).
- KB-PROB (probation recovery): (a) PROB-UNG:
  PQ1..PQ7 val=-2, PQR op=2 val=62 (solver
  exists); (b) PROB: PQ1..PQ7 val=-2, PQR op=2
  val=62; (c) PROB PQR trace: MR-OP-PROBATION then
  MR-OP-OK 2 (the retired operator recovers when
  the world changes).
- KB-SEAL: driver_H2.zag: zero operator/form
  names, zero standing offsets, zero trace
  tags/threshold/signature literals (shell grep
  audit, 0 hits).
- KB-DET: 3/3 byte-identical runs (shell sha256).

## 7. Falsifiers

F-D (wrong skip): any STANDING-SKIP in the STANDING
arm for an (op, query, phase) where the UNGATED arm
shows the same op OK (succeeded) in the same query
and phase. Fires -> wave FAIL.
F-EFF: s_sum >= u_sum, or (u_sum - s_sum) < 10.
F-CORR: any via/val/op/Z-exact mismatch UNGATED vs
STANDING.
F-PROB: probation predictions in 5d not met.
F-SEAL: any grep hit in driver_H2.zag.
F-DET: the three run outputs differ.
Any falsifier firing fails the wave.

## 8. Verdict rule

L2-ESS-COMPOSE2-PASS iff ALL of:
(1) KB-EFF, KB-CORR, KB-NOSKIP, KB-PROB, KB-SEAL,
KB-DET hold on build H2 with the section 5
signatures (QD2 op=2 tries=3, QD3 op=4 tries=10,
QD4 tries=14 in STANDING; UNGATED reproduces the
chain3b H signatures 6/8/16/24);
(2) zero falsifiers, zero hangs;
(3) learner.zag is sha256-identical to
l2_ess_compose's learner.zag (no learner change:
the standing mechanism generalizes as frozen);
(4) world_H.zag is sha256-identical to the
l2_compose_chain3b lane's world_H.zag.

If STANDING changes any via/val/op vs UNGATED, or
any skip withholds a success, the per-(op,src,sig)
design does NOT generalize as frozen: verdict FAIL
with the trace evidence identifying which
discriminator pattern broke it.

## 9. Standing rules for this wave

- Prereg frozen BEFORE implementation; this file +
  NAMECHECK.md committed ALONE. Any pre-verdict
  correction goes in a PREREG_AMENDMENT file,
  transparent, never silent.
- Pure Zag for all scientific computation; safebin
  PATH; no python3/python (Step 0).
- as/ae tick counts are INFORMATIONAL ONLY: printed
  per query per arm, never bars. Determinism is
  established by 3/3 byte-identical runs.
- The claim under test is L2 (operator standing
  records reused across queries), not L3: the
  operator menu, the phase-2 rule, and the standing
  update/gate formulas are researcher-supplied.
  This wave cannot promote anything to L3.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs; nothing
  pushed. The compose, chain3b, ess_compose, and
  builder lane directories are never modified.
- Non-claims: one [6,2,4] chain on one fresh family
  does not establish general standing
  composability; 4+ chains, the protected core, the
  continuing learner, scaling, and transfer are out
  of scope.
