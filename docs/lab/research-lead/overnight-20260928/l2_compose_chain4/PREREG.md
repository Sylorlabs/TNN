# PREREG: L2-COMPOSE-CHAIN4 (4-operator chain probe)

Frozen 2026-10-03 by the L2-COMPOSE-CHAIN4 worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

L2-COMPOSE-CHAIN3-PASS showed the unchanged phase-2
mechanism composes 3 operators in sequence: QD1 fires
CONCRETIZE (op6) and banks Z4 (id 3); QD2 fires
ABSTRACT (op5) on Z4 and banks Z5 (id 4); QD3 fires
INVERT (op4) Form A on Z5 and banks Z6 (id 5). The
phase-2 mechanism retries the fixed [1..6] enumeration
over operator-built Z sources (ZSRC_IDS registry,
snapshotted once per query, one composition step per
query, termination T1-T6). Disclosed out of scope
there: 4+ chains.

This wave tests whether composability scales to 4:
can the UNCHANGED phase-2 mechanism compose 4
operators in sequence (op A -> Z1, op B on Z1 -> Z2,
op C on Z2 -> Z3, op D on Z3 -> answer)?
Specifically:

- Q1: a query requiring 4 operator applications
  (unsolvable by 1, 2, or 3) -- does the fixed [1..6]
  enumeration retried over Z sources still suffice, or
  is within-query chaining needed?
- Q2: does termination still hold (T1-T6) with 4 live
  Z sources? (how many tries?)

## 2. The frozen non-change (strongest test form)

The learner is byte-identical to chain3's learner.zag
(sha256
6e8ed1e047e9dee8311a264aaec9a995ddbb723f5b284e21c18baa0e68038ddd,
verified at copy time). ZERO source changes. The
WORLD is byte-identical to chain3's world_E.zag (44
facts, verified at copy time). ZERO world changes.
Phase 2 is therefore textually the compose2 phase 2,
and T1-T6 hold by construction:

- T1: phase 2 only on phase-1 failure.
- T2: source list snapshotted once per query; a Z
  built during phase 2 is recorded for FUTURE queries
  but never tried within the current query.
- T3: one composition step per query.
- T4: at most (nsources x 6) bounded operator calls.
- T5: op_mask gates phase 2 (skipped when 0).
- T6: sources live, cap==qcap, id != agg_src,
  operator-built only.

The 4-chain must therefore emerge across FOUR
queries with no within-query chaining: QD1 (phase 1)
-> Z4; QD2 (phase 2 on Z4) -> Z5; QD3 (phase 2 on Z5)
-> Z6; QD4 (phase 2 on Z6) -> Z7 + answer. If
4-chains required within-query chaining, this frozen
design fails QD4 and the wave FAILs with that
evidence. QD1/QD2/QD3 are the chain3 queries
unchanged, so their behavior is already validated;
the new science is QD4 (4th link) and QD5
(termination with 4 live Z sources).

## 3. The discriminating 4th link: INVERT Form B on Z6

Verified by this worker against the frozen operator
source (preregistered so the query design is honest
about what it isolates). The fourth link is INVERT
(op4) Form B (value-mapping inversion) on the
INVERT-Form-A-built Z6:

- Z6 (from chain3, unchanged):
  5(1,7,160,167,1,1,23,22,23,3,4,0),
  rels[23,22,23,22,23,22,29], facts[31..37],
  aend=167, dvr=4, dnf=3, dir=0.
- INVERT Form B on Z6: reverse value lookup for
  v=65 finds the first live fact with rel==4 and
  obj==65, which is f38 (167,4,65); tstar=167 ==
  aend=167, so the value belongs to Z6's own mapping.
  Backward walk from 167 over Z6's reversed rels
  [29,22,23,22,23,22,23] follows f37..f31 down to
  key 160 == t. MR-INVVAL-OK.
- mr_buildwin_inv verifies via chain_exec_bwd from s
  over [value-fact, backward hops] and builds Z7
  (id 6, dir=1) with rels[4,29,22,23,22,23,22,23],
  facts[38,37,36,35,34,33,32,31], de=4, dr1=29,
  dr2=22, dnf=3, dvr=4, e_add(6,5,16), answering 65.

QD4=(65,160,65). DISCLOSED STRUCTURAL NOTE: this
query has s==v. This is not a trick; it is a
structural requirement of the frozen Form B. The
inverse walk's first hop is the value fact
(tstar,dvr,v) whose obj is v, and chain_exec_bwd
starts at cur=s, so the first hop requires s==v.
The query poses the value as the inverse-walk start:
value->key inversion (given value 65 held at Z6's
terminal 167, recover key 160). The s==v shape is
preregistered here, not discovered post hoc.

Why QD4 is unsolvable by 1 operator (phase 1 on
taught mA' id 1, de=21, dnf=2, aend=25): no live
fact has sub==65, so op1 (entry miss), op2 (no
candidates), op3 (entry miss), op5 (no rel-21 entry),
op6 (no candidates) all fail; op4 Form B finds
tstar=167 != 25 and Form A finds no (65,23,?) hop.
6 tries, all fail.

Why QD4 is unsolvable by 2 operators (no single op
on Z4, the only Z a 2-chain could use; Z4 de=29,
aend=97): no sub-65 facts, so ops 1,2,3,5,6 fail as
on mA'; op4 Form B tstar=167 != 97, Form A reversed
Z4 rels start [27,...] with no rel-27 hop from 65.
6 fails (tries 7-12).

Why QD4 is unsolvable by 3 operators (no single op
on Z5; Z5 de=29, aend=148): same 6 failures;
op4 Form B tstar=167 != 148, Form A reversed
[23,22,23,22,23,22,29] has no rel-23 hop from 65.
6 fails (tries 13-18).

QD4 solvable by op4 on Z6 (phase 2, third source):
op1/op2/op3 fail (no sub-65 facts, tries 19-21),
then op4 Form B verifies as above (try 22). op=4,
tries=22 (6 phase-1 + 6 on Z4 + 6 on Z5 + 4 on Z6),
dec=1, via=6, val=65, phit=0.
Z7 row: 6(1,8,65,160,1,1,4,29,22,3,4,1),
rels[4,29,22,23,22,23,22,23],
facts[38,37,36,35,34,33,32,31], e_add(6,5,16).
ZSRC_IDS=[3,4,5,6].

The chain is [6,5,4,4]: CONCRETIZE -> ABSTRACT ->
INVERT Form A (structural reversal) -> INVERT Form B
(value-mapping inversion). The fourth link inverts
the value mapping of the third link's output.

## 4. Termination probe: QD5 (unsolvable by design)

QD5=(170,174,66) reuses chain3's QD4 region
f39-f43: (170,23,171), (171,22,172), (172,23,173),
(173,31,174), (174,4,66). New rel id 31 on the last
hop. Validated unsolvable in chain3; here it is
re-asked with FOUR live Z sources (Z4, Z5, Z6, Z7).

- Pipeline: Z6 walks 170->176? No: Z6's facts are
  f31..f37 (160-167 region); m_exec(6? no, Z6 is id
  5) from 170 fails at the first hop on every MAP.
  phit=0. (Z7 dir=1: fact38 obj=65 != 170, fail.)
- Phase 1 on taught: 6 tries, all fail (chain3
  section 4: op1 foldwalk k=2 shape path, op2 2-fold
  lands 175 != 177? No wait, QD5 t=174: op2 lands
  173 != 174; op3 lands 173? Let me restate from
  chain3: op1 no route/shape-fail; op2 2-fold lands
  173 != 174 VERIFY-FAIL; op3 1-fold lands 172?
  Hmm. The exact per-op failure modes were validated
  in chain3 for (170,177,66) with the 5-fact region
  f39-f43 = (170,23,171),(171,22,172),(172,23,173),
  (173,31,174),(174,4,66). For QD5=(170,174,66):
  op1 b=1: entry (170,23,171), foldwalk k=2 from
  171: (171,22,172),(172,23,173) then needs
  (173,22,?) but finds rel 31: FAIL-SHAPE; b=2: no
  (170,24,?) route. op2: candidate (170,23,171),
  2-fold walk lands 173 != 174 VERIFY-FAIL. op3:
  nf2=1: 1-fold walk lands 172 != 174 FAIL. op4:
  Form B reverse lookup v=66: first (4,66) fact is
  f43 (174,4,66), tstar=174 != 25 FAIL; Form A
  reversed mA' rels [23,22,23,22,21]: (170,23,171)
  ok, (171,22,172) ok, (172,23,173) ok, (173,22,?)
  rel 31: FAIL. op5: no rel-21 entry from 170 FAIL.
  op6: 3-fold walk from 171 needs 6 hops but the
  region has 4: FAIL-SHAPE. 6 tries, all fail.
- Phase 2 on Z4 (tries 7-12), Z5 (13-18), Z6
  (19-24): all 6 fail each, per chain3 section 4
  (op4 Form A on Z6 reaches 173 then needs
  (173,29,?): rel 31 FAIL; Form B tstar=174 != 167).
- Phase 2 on Z7 (id 6, de=4, dr1=29, dr2=22, dnf=3,
  dvr=4, dir=1, aend=160): op1: entry (170,23,171),
  foldwalk k=3 from 171 needs 6 hops, region has 4:
  FAIL-SHAPE (try 25). op2: candidate (170,23,171)
  [23 != 4], foldwalk k=3 FAIL-SHAPE (26). op3:
  nf2=2,1 FAIL-SHAPE (27). op4: Form B reverse
  lookup v=66: tstar=174 != 160 FAIL; Form A
  reversed Z7 rels [23,22,23,22,23,22,29,4]:
  (170,23,171) ok, (171,22,172) ok, (172,23,173)
  ok, (173,22,?) rel 31 FAIL (28). op5: no
  (170,4,?) entry FAIL (29). op6: foldwalk k=3
  FAIL-SHAPE (30).
- QD5: op=-1, tries=30, dec=0, val=-2, phit=0.
  No new Z. Terminates with four live Z sources:
  T1-T6 hold empirically. The bound is (6 phase-1 +
  6 per live Z source), linear in registry size.

## 5. Frozen build specification (build F)

- learner.zag: byte-identical to chain3's learner.zag
  (sha256 6e8ed1e..., verified at copy time). ZERO
  changes.
- learner_frozen.zag: byte-identical to chain3's
  learner_frozen.zag (sha256 698be75b..., verified
  at copy time). The frozen 6-operator harness (no
  phase 2).
- world_F.zag: byte-identical to chain3's world_E.zag
  (44 facts; verified at copy time). ZERO changes.
  The old QD4 region f39-f43 is reused as the QD5
  termination region; no query uses new facts.
- driver_F.zag (new): queries QA(20,25,51,1,1),
  QD1(90,97,59,1,1), QD2(140,148,63,1,1),
  QD3(160,167,65,1,1), QD4(65,160,65,1,1),
  QD5(170,174,66,1,1); re-asks QD1-B, QD2-B, QD3-B,
  QD4-B. Arms: FULL (63), NOREUSE (0), ABLATE-INV
  (55), ABLATE-ABS (47), FRESH (facts only, 63).
  Fresh rel id: none (no new rels). The driver never
  names an operator, source pair, binding, pattern,
  or form; queries are (start,terminal,value,cap,dom)
  with one arm-level OP_MASK.
- driver_Fctl.zag (new): control driver. Queries
  QA, QD1, QD2, QD3, QD4(65,160,65),
  QD5(170,174,66), QD1-B. Arms: FULL (63), NOREUSE
  (0).
- Builds: `cat learner.zag world_F.zag driver_F.zag
  > comp_F_full.zag`, `cat learner_frozen.zag
  world_F.zag driver_Fctl.zag > ctl_F_full.zag`,
  pinned znc.

## 6. Frozen predicted outcomes (build F, unchanged learner)

### 6a. FULL arm (mask 63)

- QA via=1 val=51 (F-K1).
- QD1 (90,97,59): phase 1, op=6, tries=6, dec=1,
  via=3, val=59, phit=0. Z4-exact=1 (chain3 5a).
- QD2 (140,148,63): phase 1 6 fails; phase 2 on Z4:
  op=5, tries=11, dec=1, via=4, val=63, phit=0.
  Z5-exact=1. ZSRC_IDS=[3,4].
- QD3 (160,167,65): phase 1 6 fails; phase 2 on Z4
  6 fails; phase 2 on Z5: op1/op2/op3 fail, op4
  Form B fails then Form A VERIFY-OK: op=4,
  tries=16, dec=1, via=5, val=65, phit=0.
  Z6-exact=1. ZSRC_IDS=[3,4,5].
- QD4 (65,160,65): phase 1 6 fails (section 3);
  phase 2 on Z4 6 fails; phase 2 on Z5 6 fails;
  phase 2 on Z6: op1/op2/op3 fail, op4 Form B
  verifies (tstar=167==aend, backward walk
  167->160): op=4, tries=22, dec=1, via=6, val=65,
  phit=0. Z7 = 6(1,8,65,160,1,1,4,29,22,3,4,1)
  rels[4,29,22,23,22,23,22,23]
  facts[38,37,36,35,34,33,32,31], e_add(6,5,16).
  ZSRC_IDS=[3,4,5,6]. (F-K3 4-chain signature.)
- QD5 (170,174,66): phase 1 6 fails; phase 2 on Z4
  6 fails, on Z5 6 fails, on Z6 6 fails, on Z7 6
  fails: op=-1, tries=30, dec=0, val=-2, phit=0.
  No new Z. Terminates. (F-K3 termination
  signature.)
- Re-asks: QD1-B via=3 val=59 entered=0; QD2-B
  via=4 val=63 entered=0; QD3-B via=5 val=65
  entered=0; QD4-B via=6 val=65 entered=0 (pipeline
  walks Z7 backward 65->160; value from stored
  fact[0]'s obj).
- FULL t16=4; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=1; e_has(6,5,16)=1;
  e_has(6,3,16)=0; e_has(4,1,16)=0;
  e_has(5,3,16)=0; e_has(6,4,16)==0; LINK14 to 3,
  4, 5, 6; mD' live=1; oth=0. (F-K8.)

### 6b. NOREUSE arm (mask 0)

QD1=QD2=QD3=QD4=QD5 val=-2, t16=0, oth=0.

### 6c. ABLATE-INV arm (mask 55: ops 1,2,3,5,6)

- QD1: op=6, tries=5 (op4 SKIP, never counted),
  dec=1, via=3, val=59. Z4 built.
- QD2: phase 1 5 tries fail (op4 SKIP); phase 2 on
  Z4: op1(6),op2(7),op3(8) fail, op4 SKIP, op5(9)
  OK: op=5, tries=9, dec=1, via=4, val=63. Z5
  built, e_add(4,3,16).
- QD3: phase 1 5 tries fail; phase 2 on Z4 5 fails
  (6-10); phase 2 on Z5 5 fails (11-15): op=-1,
  tries=15, dec=0, val=-2. No Z6. (F-K5: op4
  necessary for the third link.)
- QD4: phase 1 5 fail; phase 2 Z4 5 fail (6-10),
  Z5 5 fail (11-15), op4 masked so Form B never
  tried: op=-1, tries=15, dec=0, val=-2. No Z7.
  (F-K5: op4 necessary for the fourth link too.)
- QD5: phase 1 5 fail; phase 2 Z4 5 fail (6-10),
  Z5 5 fail (11-15): op=-1, tries=15, val=-2.
- t16=2; e_has(3,2,16)=1; e_has(4,3,16)=1;
  e_has(5,4,16)=0; e_has(6,5,16)=0; oth=0.

### 6d. ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=5, dec=1, via=3, val=59. Z4.
- QD2: phase 1 5 tries fail (op5 SKIP); phase 2 on
  Z4: op1(6),op2(7),op3(8),op4(9) fail, op5 SKIP,
  op6(10) OK (reroute: folds (22,23) novel vs Z4's
  (26,27)): op=6, tries=10, dec=1, via=4, val=63.
  Z5 fields identical to 6a, e_add(4,2,16).
- QD3: phase 1 5 fail; phase 2 on Z4: 5 fail
  (6-10, op5 SKIP); phase 2 on Z5: op1(11),
  op2(12), op3(13) fail, op4(14) Form A OK:
  op=4, tries=14, dec=1, via=5, val=65. Z6 built,
  e_add(5,4,16). (F-K5: the 4-chain's first three
  links complete through the rerouted Z5.)
- QD4: phase 1 5 fail (op5 SKIP); phase 2 Z4 5
  fail (6-10); Z5 5 fail (11-15); Z6: op1(16),
  op2(17), op3(18) fail, op4(19) Form B OK:
  op=4, tries=19, dec=1, via=6, val=65. Z7 built,
  e_add(6,5,16). (F-K5: the 4th link completes
  through the rerouted chain.)
- QD5: phase 1 5 fail; phase 2 Z4 5 fail (6-10),
  Z5 5 fail (11-15), Z6 5 fail (16-20), Z7 5 fail
  (21-25): op=-1, tries=25, val=-2.
- t16=4; e_has(3,2,16)=1; e_has(4,2,16)=1;
  e_has(4,3,16)=0; e_has(5,4,16)=1;
  e_has(6,5,16)=1; oth=0.

### 6e. FRESH arm (facts only, mask 63)

QD1=QD2=QD3=QD4=QD5 val=-2 (MR-NO-SRC), t16=0,
oth=0.

### 6f. CONTROL arm: frozen learner (build ctl_F)

learner_frozen.zag (byte-identical to chain3's
learner_frozen.zag) + world_F.zag + driver_Fctl.zag.
FULL (mask 63): QA via=1; QD1: op=6, tries=6,
dec=1, via=3, val=59, Z4-exact=1; QD2: val=-2,
tries=6, op=-1, dec=0; QD3: val=-2, tries=6,
op=-1, dec=0; QD4: val=-2, tries=6, op=-1, dec=0;
QD5: val=-2, tries=6, op=-1, dec=0; re-ask QD1-B
via=3 val=59 entered=0; t16=1; e_has(3,2,16)=1;
e_has(3,1,16)=0; LINK14 to 3; mD' live=1; oth=0.
NOREUSE (mask 0): all QD val=-2, t16=0, oth=0.
The frozen 6-operator harness cannot solve QD4 (or
QD2/QD3/QD5): the 4-chain is necessary.

## 7. Frozen kill bars (build F)

- F-K1 (baselines): FULL arm: qa_via==1.
- F-K2 (reuse necessity): FULL arm: QD1/QD2/QD3/QD4
  phit==0. NOREUSE arm: QD1..QD5 val==-2 and
  t16==0.
- F-K3 (4-chain decides): FULL arm: QD1: op==6,
  tries==6, dec==1; QD2: op==5, tries==11, dec==1;
  QD3: op==4, tries==16, dec==1; QD4: op==4,
  tries==22, dec==1, val==65, via==6 (the 4-chain
  signature: INVERT Form B fires on the phase-2-built
  Z6 after 6 phase-1 + 6 Z4 + 6 Z5 tries); QD5:
  op==-1, tries==30, dec==0, val==-2 (bounded
  termination with four live Z sources).
- F-K4 (exact grounding + persistence): FULL arm:
  QD1: via==3, val==59, Z4-exact==1; QD2: via==4,
  val==63, Z5-exact==1; QD3: via==5, val==65,
  Z6-exact==1; QD4: via==6, val==65, Z7-exact==1
  (section 3 row, field by field); re-asks: QD1-B
  via==3 val==59 entered==0; QD2-B via==4 val==63
  entered==0; QD3-B via==5 val==65 entered==0;
  QD4-B via==6 val==65 entered==0.
- F-K5 (operator necessity, incl. reroute):
  ABLATE-INV (55): QD1: op==6, tries==5, via==3,
  val==59; QD2: op==5, tries==9, via==4, val==63;
  QD3: val==-2, tries==15, op==-1; QD4: val==-2,
  tries==15, op==-1 (op4 necessary for the third
  AND fourth links); QD5: val==-2, tries==15,
  op==-1; t16==2, e_has(4,3,16)==1,
  e_has(6,5,16)==0. ABLATE-ABS (47): QD1: op==6,
  tries==5, via==3, val==59; QD2: op==6, tries==10,
  via==4, val==63 (reroute); QD3: op==4, tries==14,
  via==5, val==65; QD4: op==4, tries==19, via==6,
  val==65 (4th link completes through the rerouted
  chain); QD5: val==-2, tries==25, op==-1; t16==4
  with e_has(4,2,16)==1, e_has(4,3,16)==0,
  e_has(6,5,16)==1.
- F-K6 (determinism): 3 runs of comp_F_bin
  byte-identical (shell sha256); same for ctl_F_bin.
- F-K7 (control discrimination): ctl_F_bin (frozen
  learner): FULL arm QD1: op==6, tries==6, via==3,
  val==59, Z4-exact==1; QD2/QD3/QD4/QD5: val==-2,
  tries==6, op==-1, dec==0; QD1-B via==3 val==59
  entered==0; t16==1; e_has(3,2,16)==1;
  e_has(3,1,16)==0; LINK14 to 3; mD' live==1;
  oth==0. NOREUSE arm: all QD val==-2, t16==0.
  3/3 byte-identical.
- F-K8 (provenance hygiene): FULL arm: t16==4;
  e_has(3,2,16)==1; e_has(4,3,16)==1;
  e_has(5,4,16)==1; e_has(6,5,16)==1;
  e_has(6,3,16)==0; e_has(4,1,16)==0;
  e_has(5,3,16)==0; e_has(6,4,16)==0; LINK14
  present to 3, 4, 5, and 6; mD' live==1; oth==0 in
  every arm (FULL/NOREUSE/ABLATE-INV/ABLATE-ABS/
  FRESH).

## 8. Falsifiers (in-Zag, build F)

F-EDGE-NEW: oth!=0 in any arm.
F-NO-GROUND: via/val/op/tries/dec != section 6.
F-WRONG-Z: any Z-exact check != 1.
F-PIPE-HIT: QD1/QD2/QD3/QD4 phit!=0 in FULL.
F-NOREUSE: NOREUSE QD val!=-2 or t16!=0.
F-ABLATE: ablation-arm vals/tries/t16/edges != 6c/6d.
F-RE: re-ask entered!=0 or via/val != expected.
F-T16: t16 count or e_has edge != expected.
F-DISTR: mD' live!=1 at FULL end.
F-FRESH: FRESH-arm QD val!=-2.
F-CTL: control-arm vals/tries/t16 != 6f.
F-TERM: QD5 tries!=30 (FULL) or any run hangs
(a hang is a wave FAIL, not a boundary).
F-CHAIN3: QD4 tries!=22 (tries<=18 would mean a
3-or-fewer chain solved it; the bar requires exactly
22: 6 phase-1 + 6 Z4 + 6 Z5 + 4 on Z6).
F-SEAL-F: shell grep of MR-OP-TRY/MR-OP-OK/
MR-COP-TRY/MR-SUB-CAND/MR-TRUNC-TRY/MR-ABS-CAND/
MR-CONC-CAND/MR-INV-REV/MR-INVVAL-OK/MR-BIND in
driver_F.zag, driver_Fctl.zag, world_F.zag = 0
(the driver/world never name an operator or form).
F-NO-INTRA: shell audit -- in the FULL run,
"MR-COMP-SRC id=6" occurs exactly once and only
after QD4's ANS line (Z7 is built during QD4's
phase 2 and, per T2, is never tried within QD4;
it is tried once in QD5's phase 2 and fails).
Any falsifier firing fails the wave for that build.

## 9. Verdict rule

L2-COMPOSE-CHAIN4-PASS iff ALL of:
(1) F-K1 through F-K8 hold on build F, including the
QD4 4-chain signature (op==4, tries==22, via==6,
val==65, Z7-exact==1) and the QD5 bounded-
termination signature (tries==30, -2, no new Z);
(2) F-K7 holds: the frozen-learner control fails
QD2/QD3/QD4/QD5 (-2, tries==6), proving the 4-chain
is what solves QD4;
(3) determinism: 3/3 byte-identical runs per binary
(comp_F, ctl_F);
(4) zero falsifiers, zero hangs;
(5) learner.zag is sha256-identical to chain3's
extended learner and world_F.zag is sha256-identical
to chain3's world_E (no learner change, no world
change: the fixed enumeration over Z sources suffices
as frozen).

If QD4 verifies on the control binary, the query is
broken (fewer than 4 operators suffice): verdict FAIL
with redesign, not a composition PASS. If QD4 fails
on the unchanged learner, 4-chains need more than the
frozen phase-2 (e.g. within-query chaining): verdict
FAIL with the trace evidence. If QD5 hangs,
termination does not scale to 4 sources: verdict FAIL.

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
- The s==v shape of QD4 is a disclosed structural
  requirement of the frozen INVERT Form B (section
  3), not a hidden trick. The world is worker-shared
  with chain3 (byte-identical); its discriminating
  power comes from the frozen-learner control arm
  (6f / F-K7), not from designer blindness. Stated
  as non-claims, not seals.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs; nothing
  pushed. Compose2, adversary, builder, and chain3
  lane directories are never modified.
- Non-claims: one [6,5,4,4] chain on one shared
  family does not establish general 4-operator
  composability; within-query operator chaining was
  deliberately NOT built (T2 forbids it) and remains
  out of scope; 5+ chains, the protected core, the
  continuing learner, scaling, and transfer are out
  of scope.
