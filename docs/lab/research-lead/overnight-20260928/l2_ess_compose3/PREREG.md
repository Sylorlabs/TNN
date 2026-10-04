# PREREG: L2-ESS-COMPOSE3 (operator standing x [6,5,4,4] composition)

Frozen 2026-10-03 by the L2-ESS-COMPOSE3 worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

L2-ESS-COMPOSE-PASS showed operator standing transfers
to the [6,5,4] composition learner (57 -> 33 tries,
zero wrong skips), with the refinement that the
standing cell key must be per-(op, *src*, sig), not
per-(op,sig). L2-ESS-COMPOSE2-PASS showed the
byte-identical frozen mechanism transfers to the
different triple [6,2,4] (54 -> 33 tries, zero wrong
skips, probation recovery), proving the
per-(op,src,sig) key carries SUBSTITUTE's de-mismatch
lifecycle. L2-COMPOSE-CHAIN4-PASS showed [6,5,4,4]
(CONCRETIZE -> ABSTRACT -> INVERT Form A ->
INVERT Form B) composes on the frozen mechanism, with
QD4=(65,160,65) solved via INVERT Form B on Z6.

This wave tests whether the standing mechanism
scales to the LONGER 4-operator chain. The standing
learner is reused BYTE-IDENTICAL from
l2_ess_compose2 (zero source changes); only the world
(world_F.zag, the [6,5,4,4] world) and the driver are
new. If standing improves efficiency with correctness
preserved and zero wrong skips on [6,5,4,4], the
per-(op,src,sig) design scales beyond 3-operator
chains. If it fails, the wave reports which
discriminator pattern breaks it, not a bare negative.

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
  probation-try at QTOUCH>=8 (QTOUCH reset to 0).
- Context signature st_sig = em*16+nf*2+pat
  (em = live (s,de(src)) fact flag, nf = dnf(src)
  clamped 0..7, pat = de(src)==0).
- Updates (st_standing_upd, learner-side only):
  after phase 1 keyed (s,agg_src); after each Z
  source keyed (s,zsrc). Commit -> SUC+8/STRK=0/
  FAIL/=2; tried-not-committed -> FAIL+4/STRK+1.
- Gating at all 12 enumeration blocks with
  TRIEDMASK_P1/P2 and phase-appropriate tags.
- Tries counted at st+1380 on every non-skipped
  enumeration (TRY and PROBATION both count).

## 3. Why [6,5,4,4] is a discriminating test

The 4-chain forces the SAME operator (op4 INVERT) to
fire twice, under the SAME context signature
(sig=6, em=0, nf=3), on TWO DIFFERENT Z sources
(Z5 in QD3 via Form A, Z6 in QD4 via Form B). The
per-(op,src,sig) key must keep these in separate
cells: (4,4,6) for Form A on Z5, (4,5,6) for Form B
on Z6. Concretely:

(a) QD3's op4 success on Z5 must not let QD4 skip
    op4 on Z6 (different src, fresh cell).
(b) QD4's op4 failure on Z5 (phase-2 Z5 visit)
    must not strike op4 on Z6 (different src).
(c) QD5's op4 try on Z5 must not be skipped: the
    (4,4,6) cell carries SUC=8 from QD3, so the
    operator is tried and correctly fails.
(d) The two INVERT forms share one operator id, so
    a per-(op,sig) key would conflate Form A and
    Form B histories; the src in the key is what
    separates them.

Additionally the 4-chain adds a fourth live Z
source (Z7) in QD5's termination probe, testing
that standing scales with source count: QD5 visits
four Z sources under three signatures.

## 4. Hand-derived predicted standing trace (world_F)

Source descriptors (from driver_F.zag d_check_*,
offsets o+34=de, o+37=dnf; taught mA' id 1 from the
ESS design): src=1 (mA'): de=21, dnf=2, pat=0;
src=3 (Z4): de=29, dnf=3; src=4 (Z5): de=29,
dnf=3; src=5 (Z6): de=23, dnf=3; src=6 (Z7):
de=4, dnf=3. Phase-1 sig base is 4 (nf=2);
phase-2 sig base is 6 (nf=3); em adds 16 when a
live (s,de) fact exists.

Taught entry facts: (90,29,91), (140,29,142),
(160,23,161), (170,23,171). No taught fact has
subj 65. Z-builds reference existing facts only.

QA (20,25,51): pipeline hit, via=1, val=51. No
standing activity (as in ESS/COMPOSE2).

QD1 (90,97,59): phase-1 src=1 sig=4 (em=0: no
live (90,21,*)), all cells fresh: ops 1-5 FAIL,
op6 OK. tries=6, op=6, dec=1, via=3, val=59.
Z4 built. Update: (1..5,1,4)=(0,4,1);
(6,1,4)=(8,0,0).

QD2 (140,148,63): phase-1 src=1 sig=4 (em=0):
ops 1-5 SKIP (struck (0,4,1)); op6 TRY (8,0,0)
-> FAIL. tries=1. Update: (6,1,4)=(8,4,1).
Phase-2 Z4 src=3 sig=22 (em=1: f23=(140,29,142)
is live), fresh: ops 1-4 FAIL, op5 OK. tries=6,
op=5, dec=1, via=4, val=63. Z5 built. Update:
(1..4,3,22)=(0,4,1); (5,3,22)=(8,0,0).

QD3 (160,167,65): phase-1 src=1 sig=4 (em=0):
ops 1-5 SKIP; op6 TRY (8,4,1; 16<4 false) ->
FAIL. tries=1. Update: (6,1,4)=(8,8,2).
Phase-2 Z4 src=3 sig=6 (em=0: no live
(160,29,*)), fresh: 6 tried, all FAIL. tries=7.
Update: (1..6,3,6)=(0,4,1). Phase-2 Z5 src=4
sig=6 (em=0), fresh: ops 1-3 FAIL, op4 OK
Form A. tries=11, op=4, dec=1, via=5, val=65.
Z6 built. Update: (1..3,4,6)=(0,4,1);
(4,4,6)=(8,0,0).

QD4 (65,160,65): phase-1 src=1 sig=4 (em=0: no
subj-65 facts): ops 1-5 SKIP; op6 TRY (8,8,2;
16<8 false, 2<3) -> FAIL. tries=1. Update:
(6,1,4)=(8,12,3). Phase-2 Z4 src=3 sig=6
(em=0): (op,3,6)=(0,4,1) all SKIP. tries=1.
Phase-2 Z5 src=4 sig=6 (em=0): ops 1-3 SKIP
((0,4,1)); op4 TRY ((8,0,0)) -> FAIL; ops 5-6
TRY (fresh) -> FAIL. tries=4. Update:
(4,4,6)=(8,4,1); (5,4,6)=(0,4,1);
(6,4,6)=(0,4,1). Phase-2 Z6 src=5 sig=6
(em=0: no live (65,23,*)), fresh: ops 1-3 FAIL,
op4 OK Form B. tries=8, op=4, dec=1, via=6,
val=65. Z7 built. Update: (1..3,5,6)=(0,4,1);
(4,5,6)=(8,0,0). The src key separates the two
INVERT firings: (4,4,6) vs (4,5,6).

QD5 (170,174,66): phase-1 src=1 sig=4 (em=0):
ops 1-5 SKIP; op6 SKIP ((8,12,3): STRK=3>=3).
tries=0. Phase-2 Z4 src=3 sig=6 (em=0): all
SKIP ((0,4,1)). tries=0. Phase-2 Z5 src=4
sig=6 (em=0): ops 1-3,5,6 SKIP; op4 TRY
((8,4,1): 16<4 false) -> FAIL. tries=1.
Update: (4,4,6)=(8,8,2). Phase-2 Z6 src=5
sig=22 (em=1: f39=(170,23,171) live), fresh: 6
tried, all FAIL. tries=7. Update:
(1..6,5,22)=(0,4,1). Phase-2 Z7 src=6 sig=6
(em=0: no live (170,4,*)), fresh: 6 tried, all
FAIL. tries=13, op=-1, dec=0, val=-2.

Re-asks QD1-B/QD2-B/QD3-B/QD4-B: pipeline hits,
via=3/4/5/6, val=59/63/65/65, entered=0. No
standing activity.

Probation: no QTOUCH reaches 8 on the F-world
sequence (max is 5 on (1..5,1,4) and (6,1,4));
no MR-OP-PROBATION / MR-COP-PROBATION fires in
the UNGATED/STANDING/GLOBAL arms.

Predicted totals: UNGATED 6+11+16+22+30=85;
STANDING 6+6+11+8+13=44; savings 41.
Standing skips: QD2 5 (phase-1 ops 1-5), QD3 5
(phase-1 ops 1-5), QD4 14 (phase-1 ops 1-5, Z4
ops 1-6, Z5 ops 1-3), QD5 17 (phase-1 ops 1-6,
Z4 ops 1-6, Z5 ops 1,2,3,5,6) = 41, matching
85-44.

## 5. Frozen predicted outcomes (build F3)

### 5a. UNGATED arm (mode 0, mask 63)

Reproduces the chain4 build-F FULL signatures
(frozen predictions, F-K3/F-K4): QA via=1
val=51; QD1 op=6 tries=6 dec=1 via=3 val=59
Z4-exact=1; QD2 op=5 tries=11 dec=1 via=4
val=63 Z5-exact=1; QD3 op=4 tries=16 dec=1
via=5 val=65 Z6-exact=1; QD4 op=4 tries=22
dec=1 via=6 val=65 Z7-exact=1; QD5 op=-1
tries=30 dec=0 val=-2; re-asks via=3/4/5/6
val=59/63/65/65 entered=0; u_sum=85. Mode 0 is
the byte-identical-trace path; the standing
integration is purely additive and gated.

### 5b. STANDING arm (mode 1, mask 63)

QA via=1 val=51; QD1 op=6 tries=6 via=3 val=59
Z4-exact=1; QD2 op=5 tries=6 via=4 val=63
Z5-exact=1; QD3 op=4 tries=11 via=5 val=65
Z6-exact=1; QD4 op=4 tries=8 via=6 val=65
Z7-exact=1; QD5 op=-1 tries=13 val=-2 dec=0;
re-asks via=3/4/5/6 val=59/63/65/65 entered=0;
s_sum=44. Z4/Z5/Z6/Z7 rows field-identical to
UNGATED.

### 5c. GLOBAL arm (mode 2, mask 63; informational)

Predicted qualitative outcome (same world and
same QD1/QD2 as the ESS [6,5,4] GLOBAL arm):
QD1 op=6 val=59 tries=6; QD2 reroutes via op6
on Z4 (op=6, val=63; global cells do not
distinguish sources); QD3 val=-2 (op4 globally
retired after QD1, the INVERT link never fires,
chain broken at the third link); QD4 val=-2;
QD5 val=-2. Informational only: the load-bearing
prediction is QD3 val=-2 under GLOBAL while
STANDING solves QD3 (val=65), confirming the
(src,sig) key is load-bearing for the 4-chain
too.

### 5d. Probation arms (ESS probation world, reused)

PROB-UNG (mode 0): PQ1..PQ7 val=-2; PQR op=2
val=62. PROB (mode 1): PQ1..PQ7 val=-2; PQR op=2
val=62; PQR trace shows MR-OP-PROBATION then
MR-OP-OK 2 (strike -> skip -> QTOUCH=8 ->
probation -> verify -> commit).

## 6. Frozen kill bars (build F3)

- KB-EFF (efficiency): s_sum < u_sum AND
  (u_sum - s_sum) >= 10. Predicted: 44 < 85,
  savings 41.
- KB-CORR (correctness): for QA/QD1..QD5 and the
  four re-asks, via/val/op identical between
  UNGATED and STANDING; Z4/Z5/Z6/Z7 exact checks
  = 1 in both arms; d_check rows equal field by
  field.
- KB-NOSKIP (no wrong skips): every
  MR-OP-STANDING-SKIP / MR-COP-STANDING-SKIP in the
  STANDING arm is paired with a same-query
  same-phase FAIL of the same op in the UNGATED
  arm; zero OK-withheld (F-D does not fire). The
  verifying operators (op6 QD1 phase-1, op5 QD2
  Z4, op4 QD3 Z5, op4 QD4 Z6) are never skipped:
  their phase-2 cells are fresh per (src,sig).
  Predicted skip multiset: QD2 5, QD3 5, QD4 14,
  QD5 17 = 41.
- KB-PROB (probation recovery): (a) PROB-UNG:
  PQ1..PQ7 val=-2, PQR op=2 val=62 (solver
  exists); (b) PROB: PQ1..PQ7 val=-2, PQR op=2
  val=62; (c) PROB PQR trace: MR-OP-PROBATION then
  MR-OP-OK 2 (the retired operator recovers when
  the world changes).
- KB-SEAL: driver_F3.zag: zero operator/form
  names, zero standing offsets, zero trace
  tags/threshold/signature literals (shell grep
  audit, 0 hits).
- KB-DET: 3/3 byte-identical runs (shell sha256).

## 7. Falsifiers

F-D (wrong skip): any STANDING-SKIP in the
STANDING arm for an (op, query, phase, source)
where the UNGATED arm shows the same op OK
(succeeded) in the same query, phase, and source.
Fires -> wave FAIL.
F-EFF: s_sum >= u_sum, or (u_sum - s_sum) < 10.
F-CORR: any via/val/op/Z-exact mismatch UNGATED
vs STANDING.
F-PROB: probation predictions in 5d not met.
F-SEAL: any grep hit in driver_F3.zag.
F-DET: the three run outputs differ.
Any falsifier firing fails the wave.

## 8. Verdict rule

L2-ESS-COMPOSE3-PASS iff ALL of:
(1) KB-EFF, KB-CORR, KB-NOSKIP, KB-PROB, KB-SEAL,
KB-DET hold on build F3 with the section 5
signatures (QD2 op=5 tries=6, QD3 op=4 tries=11,
QD4 op=4 tries=8, QD5 tries=13 in STANDING;
UNGATED reproduces the chain4 F signatures
6/11/16/22/30);
(2) zero falsifiers, zero hangs;
(3) learner.zag is sha256-identical to
l2_ess_compose2's learner.zag (no learner change:
the standing mechanism scales as frozen);
(4) world_F.zag is sha256-identical to the
l2_compose_chain4 lane's world_F.zag.

If STANDING changes any via/val/op vs UNGATED, or
any skip withholds a success, or the two INVERT
firings are conflated (e.g. op4 skipped on Z6 in
QD4, or QD4 failing), the per-(op,src,sig) design
does NOT scale as frozen: verdict FAIL with the
trace evidence identifying which pattern broke it.

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
  pushed. The compose, chain3b, chain4, ess_compose,
  ess_compose2, and builder lane directories are
  never modified.
- Non-claims: one [6,5,4,4] chain on one shared
  family does not establish general standing
  composability at arbitrary depth; 5+ chains, the
  protected core, the continuing learner, scaling,
  and transfer are out of scope.
