# PREREG: L2-COMPOSE-CHAIN3 (3-operator chain probe)

Frozen 2026-10-03 by the L2-COMPOSE-CHAIN3 worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

L2-METAREUSE-COMPOSE-2-PASS showed operators compose
across queries: QD1 fires CONCRETIZE (op6) and banks
Z4 (dnf=3, de=29); QD2, unsolvable by any single
operator on the taught source, fires ABSTRACT (op5) on
Z4 and banks Z5. The phase-2 mechanism retries the
fixed [1..6] enumeration over operator-built Z sources
(ZSRC_IDS registry, snapshotted once per query, one
composition step per query, termination T1-T6).
Disclosed out of scope there: within-query chaining,
longer chains, scaling, transfer.

This wave tests whether composability scales beyond
pairs: can the UNCHANGED phase-2 mechanism compose
3 operators in sequence (op A -> Z1, op B on Z1 -> Z2,
op C on Z2 -> answer)? Specifically:

- Q1: a world requiring 3 operators (unsolvable by 1
  or 2) — does the fixed [1..6] enumeration retried
  over Z sources still suffice, or is within-query
  chaining needed?
- Q2: does termination still hold (T1-T6) with 3 live
  Z sources?

## 2. The frozen non-change (strongest test form)

The learner is byte-identical to compose2's extended
learner.zag (sha256
6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd,
verified at copy time). ZERO source changes. Phase 2
is therefore textually the compose2 phase 2, and T1-T6
hold by construction:

- T1: phase 2 only on phase-1 failure.
- T2: source list snapshotted once per query; a Z
  built during phase 2 is recorded for FUTURE queries
  but never tried within the current query.
- T3: one composition step per query.
- T4: at most (nsources x 6) bounded operator calls.
- T5: op_mask gates phase 2 (skipped when 0).
- T6: sources live, cap==qcap, id != agg_src,
  operator-built only.

The 3-chain must therefore emerge across THREE
queries with no within-query chaining: QD1 (phase 1)
-> Z4; QD2 (phase 2 on Z4) -> Z5; QD3 (phase 2 on Z5)
-> answer. If 3-chains required within-query
chaining, this frozen design fails QD3 and the wave
FAILs with that evidence.

## 3. The discriminating chain: [6,5,4]

Verified by this worker against the frozen operator
source (preregistered so the world design is honest
about what it isolates). The third link is INVERT
(op4) Form A on the ABSTRACT-built Z5:

- Z5 (from compose2's world_D, unchanged here):
  5(1,7,140,148,1,1,29,22,23,3,4,0),
  rels[29,22,23,22,23,22,23], aend=148, dvr=4.
- INVERT Form A on Z5 reverses its rels to
  [23,22,23,22,23,22,29] and walks strictly forward
  from the query start. Form B is tried first and
  fails (tstar=167 != aend=148), so Form A is the
  firing form (honest note: the chain's third link is
  structural reversal, not value inversion).
- QD3=(160,167,65) region: (160,23,161),
  (161,22,162), (162,23,163), (163,22,164),
  (164,23,165), (165,22,166), (166,29,167),
  (167,4,65). Form A walk 160->167, valof(167,4)=65.

Why QD3 is unsolvable by 1 operator (phase 1 on
taught mA' id 1, de=21, dnf=2, aend=25):

- op1: b=1 foldwalk k=2 from 161 lands 165, no
  rel-24 hop from 165 on mD'/mB'; b=2 no rel-24 hop
  from 160. FAIL.
- op2: candidate (160,23,161), 2-fold walk lands
  165 != 167. VERIFY-FAIL.
- op3: nf2=1, 1-fold walk lands 163 != 167. FAIL.
- op4: Form B tstar=167 != 25 FAIL; Form A reversed
  mA' rels [23,22,23,22,21]: dead at (164,21,?).
  FAIL.
- op5: no rel-21 entry from 160. FAIL.
- op6: pattern mP' (nf=3): 3-fold walk from 161
  needs (166,23,?) but the last hop is rel 29.
  FAIL-SHAPE.

Why QD3 is unsolvable by 2 operators (no single op
on Z4, the only Z a 2-chain could use; Z4 de=29,
dr=(26,27), dnf=3, aend=98):

- op1: foldwalk k=3 from 161 FAIL-SHAPE; b=2 no
  route from 160. FAIL.
- op2: candidate (160,23,161) rel 23 != 29,
  3-fold walk FAIL-SHAPE. FAIL.
- op3: nf2=2 walk lands 165, nf2=1 lands 163.
  FAIL.
- op4: Form B tstar=167 != 98 FAIL; Form A reversed
  Z4 rels start [27,...]: no rel-27 hop from 160.
  FAIL.
- op5: no rel-29 entry from 160. FAIL.
- op6: 3-fold walk from 161 FAIL-SHAPE. FAIL.

QD3 solvable by op4 on Z5 (phase 2, second source):
ops 1,2,3 fail as on Z4 (foldwalk k=3 shape-fails;
op3 lands 165/163), then op4 Form B fails
(167 != 148), Form A verifies 160->167 with
valof=65. op=4, tries=16 (6 phase-1 + 6 on Z4 +
op1/op2/op3 on Z5 + op4), dec=1, via=6, val=65.

Z6 row: mr_buildwin with src1=5 (agg_src), de=23,
dr1=22, dr2=23, dnf=3, dvr=4, dir=0:
6(1,7,160,167,1,1,23,22,23,3,4,0),
rels[23,22,23,22,23,22,29], facts[42,43,44,45,46,47,48],
e_add(6,5,16). ZSRC_IDS=[4,5,6].

## 4. Termination probe: QD4 (unsolvable by design)

QD4=(170,177,66): (170,23,171), (171,22,172),
(172,23,173), (173,22,174), (174,23,175),
(175,22,176), (176,31,177), (177,4,66). New rel
id 31 on the last hop.

- Pipeline: Z6 walks 170->176 then needs
  (176,29,?) but finds rel 31: fail. All others
  fail at the first hop. phit=0.
- Phase 1 on taught: op1 no route; op2 2-fold lands
  175 != 177; op3 1-fold lands 173; op4 Form B
  tstar=177 != 25, Form A dead at (174,21,?);
  op5 no rel-21; op6 3-fold needs (176,23,?) but
  finds rel 31: FAIL-SHAPE. 6 tries, all fail.
- Phase 2 on Z4: op1/op2 foldwalk k=3 shape-fail;
  op3 lands 175/173; op4 Form B 177 != 98, Form A
  no rel-27 hop; op5 no rel-29 entry; op6
  shape-fail. 6 fails (tries 7-12).
- Phase 2 on Z5: op1/op2/op3 as on Z4; op4 Form B
  177 != 148, Form A reversed walk reaches 176 then
  needs (176,29,?): rel 31: FAIL; op5 no rel-29
  entry; op6 shape-fail. 6 fails (tries 13-18).
- Phase 2 on Z6 (de=23, dnf=3, aend=167): op1
  shape-fail; op2 no candidate (only rel-23 entry
  from 170, equals de); op3 lands 175/173; op4 Form B
  177 != 167, Form A reversed [29,...]: no rel-29
  hop from 170; op5 entry (170,23,171) 3-fold
  shape-fail; op6 shape-fail. 6 fails (19-24).
- QD4: op=-1, tries=24, dec=0, val=-2, no new Z.
  Terminates with three live Z sources: T1-T6 hold
  empirically, not just by construction.

## 5. Frozen world specification (world_E.zag)

world_D's 42 facts (f0-f41) unchanged, plus 16:

- QD3 region f42:(160,23,161) f43:(161,22,162)
  f44:(162,23,163) f45:(163,22,164)
  f46:(164,23,165) f47:(165,22,166)
  f48:(166,29,167) f49:(167,4,65)
- QD4 region f50:(170,23,171) f51:(171,22,172)
  f52:(172,23,173) f53:(173,22,174)
  f54:(174,23,175) f55:(175,22,176)
  f56:(176,31,177) f57:(177,4,66)

New rel id: 31 (fresh, disjoint from builder /
adversary / compose2 families). MAPs: the same 4
taught MAPs as world_D (mD' id 0, mA' id 1, mB' id 2,
mP' id 3). Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QD1(90,98,59,1,1), QD2(140,148,63,1,1),
QD3(160,167,65,1,1), QD4(170,177,66,1,1);
re-asks QD1-B, QD2-B, QD3-B.

## 6. Frozen predicted outcomes (build E, unchanged learner)

### 6a. FULL arm (mask 63)

- QA via=1 val=51; QB via=2 val=-1 (E-K1).
- QD1 (90,98,59): phase 1, op=6, tries=6, dec=1,
  via=4, val=59, phit=0. Z4 as in compose2 5a.
- QD2 (140,148,63): phase 1 6 fails; phase 2 on Z4:
  op=5, tries=11, dec=1, via=5, val=63, phit=0.
  Z5 as in compose2 5a. ZSRC_IDS=[4,5].
- QD3 (160,167,65): phase 1 6 fails (section 3);
  phase 2 on Z4 6 fails; phase 2 on Z5: op1/op2/op3
  fail, op4 Form B fails then Form A VERIFY-OK:
  op=4, tries=16, dec=1, via=6, val=65, phit=0.
  Z6 = 6(1,7,160,167,1,1,23,22,23,3,4,0)
  rels[23,22,23,22,23,22,29]
  facts[42,43,44,45,46,47,48]. e_add(6,5,16).
  ZSRC_IDS=[4,5,6]. (E-K3 3-chain signature.)
- QD4 (170,177,66): phase 1 6 fails; phase 2 on Z4
  6 fails, on Z5 6 fails, on Z6 6 fails: op=-1,
  tries=24, dec=0, val=-2, phit=0. No new Z.
  Terminates. (E-K3 termination signature.)
- Re-asks: QD1-B via=4 val=59 entered=0; QD2-B
  via=5 val=63 entered=0; QD3-B via=6 val=65
  entered=0 (pipeline walks Z6 forward 160->167).
- FULL t16=3; e_has(4,3,16)=1; e_has(5,4,16)=1;
  e_has(6,5,16)=1; e_has(6,3,16)=0;
  e_has(4,1,16)=0; e_has(5,3,16)=0; LINK14 to 4, 5,
  6; mD' live=1; oth=0. (E-K8.)

### 6b. NOREUSE arm (mask 0)

QD1=QD2=QD3=QD4 val=-2, t16=0, oth=0.

### 6c. ABLATE-INV arm (mask 55: ops 1,2,3,5,6)

- QD1: op=6, tries=5 (op4 SKIP, never counted),
  dec=1, via=4, val=59. Z4 built.
- QD2: phase 1 5 tries fail (op4 SKIP); phase 2 on
  Z4: op1(6),op2(7),op3(8) fail, op4 SKIP, op5(9)
  OK: op=5, tries=9, dec=1, via=5, val=63. Z5
  built, e_add(5,4,16).
- QD3: phase 1 5 tries fail; phase 2 on Z4 5 fails
  (6-10); phase 2 on Z5 5 fails (11-15): op=-1,
  tries=15, dec=0, val=-2. No Z6. (E-K5: op4
  necessary for the third link.)
- QD4: phase 1 5 fail; phase 2 Z4 5 fail (6-10),
  Z5 5 fail (11-15): op=-1, tries=15, val=-2.
- t16=2; e_has(4,3,16)=1; e_has(5,4,16)=1;
  e_has(6,5,16)=0; oth=0.

### 6d. ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=5, dec=1, via=4, val=59. Z4.
- QD2: phase 1 5 tries fail (op5 SKIP); phase 2 on
  Z4: op1(6),op2(7),op3(8),op4(9) fail, op5 SKIP,
  op6(10) OK (reroute: folds (22,23) novel vs Z4's
  (26,27)): op=6, tries=10, dec=1, via=5, val=63.
  Z5 fields identical to 6a, e_add(5,3,16).
- QD3: phase 1 5 fail; phase 2 on Z4: 5 fail
  (6-10, op5 SKIP); phase 2 on Z5: op1(11),
  op2(12), op3(13) fail, op4(14) Form A OK:
  op=4, tries=14, dec=1, via=6, val=65. Z6 built,
  e_add(6,5,16). (E-K5: the 3-chain completes
  through the rerouted Z5.)
- QD4: phase 1 5 fail; phase 2 Z4 5 fail (6-10),
  Z5 5 fail (11-15), Z6 5 fail (16-20): op=-1,
  tries=20, val=-2.
- t16=2; e_has(4,3,16)=1; e_has(5,3,16)=1;
  e_has(5,4,16)=0; e_has(6,5,16)=1; oth=0.

### 6e. FRESH arm (facts only, mask 63)

QD1=QD2=QD3=QD4 val=-2 (MR-NO-SRC), t16=0, oth=0.

### 6f. CONTROL arm: frozen learner (build ctl_E)

learner_frozen.zag (byte-identical to the adversary's
frozen learner, sha256
698be75b19e3d9a85b3b308aa4d1e645cbb4e386169bcb47d8b20dfb93877731)
+ world_E.zag + driver_Ectl.zag. FULL (mask 63):
QA via=1, QB via=2; QD1: op=6, tries=6, dec=1,
via=4, val=59, Z4-exact=1; QD2: val=-2, tries=6,
op=-1, dec=0; QD3: val=-2, tries=6, op=-1, dec=0;
QD4: val=-2, tries=6, op=-1, dec=0; re-ask QD1-B
via=4 val=59 entered=0; t16=1; e_has(4,3,16)=1;
e_has(4,1,16)=0; LINK14 to 4; mD' live=1; oth=0.
NOREUSE (mask 0): all QD val=-2, t16=0, oth=0.
The frozen 6-operator harness cannot solve QD3 (or
QD2/QD4): the 3-chain is necessary.

## 7. Frozen kill bars (build E)

- E-K1 (baselines): FULL arm: qa_via==1, qb_via==2.
- E-K2 (reuse necessity): FULL arm: QD1/QD2/QD3
  phit==0. NOREUSE arm: QD1=QD2=QD3=QD4 val==-2 and
  t16==0.
- E-K3 (3-chain decides): FULL arm: QD1: op==6,
  tries==6, dec==1; QD2: op==5, tries==11, dec==1;
  QD3: op==4, tries==16, dec==1, val==65, via==6
  (the 3-chain signature: INVERT fires on the
  phase-2-built Z5 after 6 phase-1 + 6 Z4 tries);
  QD4: op==-1, tries==24, dec==0, val==-2
  (bounded termination with three live Z sources).
- E-K4 (exact grounding + persistence): FULL arm:
  QD1: via==4, val==59, Z4-exact==1; QD2: via==5,
  val==63, Z5-exact==1; QD3: via==6, val==65,
  Z6-exact==1 (section 3 row, field by field);
  re-asks: QD1-B via==4 val==59 entered==0; QD2-B
  via==5 val==63 entered==0; QD3-B via==6 val==65
  entered==0.
- E-K5 (operator necessity, incl. 3-chain reroute):
  ABLATE-INV (55): QD1: op==6, tries==5, via==4,
  val==59; QD2: op==5, tries==9, via==5, val==63;
  QD3: val==-2, tries==15, op==-1 (op4 necessary
  for the third link); t16==2,
  e_has(5,4,16)==1. ABLATE-ABS (47): QD1: op==6,
  tries==5, via==4, val==59; QD2: op==6, tries==10,
  via==5, val==63 (reroute); QD3: op==4, tries==14,
  via==6, val==65 (3-chain completes through the
  rerouted Z5); QD4: val==-2, tries==20, op==-1;
  t16==2 with e_has(5,3,16)==1,
  e_has(5,4,16)==0, e_has(6,5,16)==1.
- E-K6 (determinism): 3 runs of comp_E_bin
  byte-identical (shell sha256); same for ctl_E_bin.
- E-K7 (control discrimination): ctl_E_bin (frozen
  learner): FULL arm QD1: op==6, tries==6, via==4,
  val==59, Z4-exact==1; QD2/QD3/QD4: val==-2,
  tries==6, op==-1, dec==0; t16==1;
  e_has(4,3,16)==1; e_has(4,1,16)==0; LINK14 to 4;
  mD' live==1; oth==0. NOREUSE arm: all QD val==-2,
  t16==0. 3/3 byte-identical.
- E-K8 (provenance hygiene): FULL arm: t16==3;
  e_has(4,3,16)==1; e_has(5,4,16)==1;
  e_has(6,5,16)==1; e_has(6,3,16)==0;
  e_has(4,1,16)==0; e_has(5,3,16)==0; LINK14
  present to 4, 5, and 6; mD' live==1; oth==0 in
  every arm (FULL/NOREUSE/ABLATE-INV/ABLATE-ABS/
  FRESH).

## 8. Falsifiers (in-Zag, build E)

F-EDGE-NEW: oth!=0 in any arm.
F-NO-GROUND: via/val/op/tries/dec != section 6.
F-WRONG-Z: any Z-exact check != 1.
F-PIPE-HIT: QD1/QD2/QD3 phit!=0 in FULL.
F-NOREUSE: NOREUSE QD val!=-2 or t16!=0.
F-ABLATE: ablation-arm vals/tries/t16/edges != 6c/6d.
F-RE: re-ask entered!=0 or via/val != expected.
F-T16: t16 count or e_has edge != expected.
F-DISTR: mD' live!=1 at FULL end.
F-FRESH: FRESH-arm QD val!=-2.
F-CTL: control-arm vals/tries/t16 != 6f.
F-TERM: QD4 tries!=24 (FULL) or any run hangs
(a hang is a wave FAIL, not a boundary).
F-CHAIN2: QD3 tries<=12 would mean a 2-or-fewer
chain solved it (bar requires exactly 16).
F-SEAL-E: shell grep of MR-OP-TRY/MR-OP-OK/
MR-COP-TRY/MR-SUB-CAND/MR-TRUNC-TRY/MR-ABS-CAND/
MR-CONC-CAND/MR-INV-REV/MR-INVVAL-OK/MR-BIND in
driver_E.zag, driver_Ectl.zag, world_E.zag = 0
(the driver/world never name an operator or form).
F-NO-INTRA: shell audit — in the FULL run,
"MR-COMP-SRC id=6" occurs exactly once and only
after QD3's ANS line (Z6 is built during QD3's
phase 2 and, per T2, is never tried within QD3;
it is tried once in QD4's phase 2 and fails).
Any falsifier firing fails the wave for that build.

## 9. Verdict rule

L2-COMPOSE-CHAIN3-PASS iff ALL of:
(1) E-K1 through E-K8 hold on build E, including the
QD3 3-chain signature (op==4, tries==16, via==6,
val==65, Z6-exact==1) and the QD4 bounded-
termination signature (tries==24, -2, no new Z);
(2) E-K7 holds: the frozen-learner control fails
QD2/QD3/QD4 (-2, tries==6), proving the 3-chain is
what solves QD3;
(3) determinism: 3/3 byte-identical runs per binary
(comp_E, ctl_E);
(4) zero falsifiers, zero hangs;
(5) learner.zag is sha256-identical to compose2's
extended learner (no learner change: the fixed
enumeration over Z sources suffices as frozen).

If QD3 verifies on the control binary, the world is
broken (fewer than 3 operators suffice): verdict FAIL
with redesign, not a composition PASS. If QD3 fails
on the unchanged learner, 3-chains need more than the
frozen phase-2 (e.g. within-query chaining): verdict
FAIL with the trace evidence. If QD4 hangs,
termination does not scale: verdict FAIL.

## 10. Standing rules for this wave

- Prereg frozen BEFORE implementation; this file +
  NAMECHECK.md committed ALONE. Any pre-verdict
  correction goes in a PREREG_AMENDMENT file,
  transparent, never silent.
- Pure Zag for all scientific computation; safebin
  PATH; no python3/python (Step 0).
- as/ae tick counts are INFORMATIONAL ONLY: printed
  per query per arm, never bars. Determinism is
  established by 3/3 byte-identical runs.
- The claim under test is L2 (operator output reused
  as operator input across queries by a fixed,
  researcher-supplied two-phase enumeration), not L3:
  the operator menu, the phase-2 rule, and the
  termination conditions are researcher-supplied.
  This wave cannot promote anything to L3.
- Build E's world is worker-designed (this worker
  verified every prediction against the frozen
  operator source itself); its discriminating power
  comes from the frozen-learner control arm (6f /
  E-K7), not from designer blindness. Stated as a
  non-claim, not a seal.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs; nothing
  pushed. Compose2, adversary, and builder lane
  directories are never modified.
- Non-claims: one [6,5,4] chain on one fresh family
  does not establish general 3-operator
  composability; within-query operator chaining was
  deliberately NOT built (T2 forbids it) and remains
  out of scope; longer chains (4+), the protected
  core, the continuing learner, scaling, and transfer
  are out of scope.
