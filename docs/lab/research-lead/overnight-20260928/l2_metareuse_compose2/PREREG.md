# PREREG: L2-METAREUSE-COMPOSE-2 (operator composition probe)

Frozen 2026-10-03 by the L2-METAREUSE-COMPOSE-2 worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE. Any pre-verdict
correction goes in a PREREG_AMENDMENT file, transparent,
never silent.

## 1. Mandate and scope

The L2 meta-reuse arc reached L2-METAREUSE-ADVERSARY-PASS:
six operators (1=COMBINE, 2=SUBSTITUTE, 3=TRUNCATE,
4=INVERT with Form A structural reversal and Form B
value-mapping inversion, 5=ABSTRACT, 6=CONCRETIZE) fire
on sealed worlds under a fixed [1..6] enumeration where
each operator is tried independently on one AGG source
and the first verifying operator wins. The OUTPUT of one
operator never feeds as INPUT to another: `ex_query`
selects `agg_src` as the first live MAP with cap==qcap
(a taught MAP), so a Z MAP built by an earlier operator
firing can never become a later operator's source. This
was confirmed by this worker's own code inspection of
the frozen `l2_metareuse_adversary/learner.zag`
(`mr_adapt`, `ex_query`): no path exists from a built Z
row back into an operator's `agg_src` argument.

This wave tests whether the operators are COMPOSABLE:
can a Z-structure produced by one operator serve as the
source for another operator, so that a query unsolvable
by any single operator on the taught source becomes
solvable by an operator sequence (here CONCRETIZE then
ABSTRACT)? And what are the termination conditions for
such composition?

## 2. The composition mechanism (frozen design)

The extended learner keeps the frozen phase 1 EXACTLY:
ops 1..6 tried in fixed order on `agg_src`, first
verifying operator wins, identical traces
(MR-OP-TRY/OK/FAIL/SKIP), identical tries counting.

Phase 2 (new, runs only if phase 1 produced no verified
operator): build a source list = the operator-built Z
MAP ids recorded in state (see 2a), in build order,
filtered to live MAPs with cap==qcap and id != agg_src.
For each Z source in order, retry the fixed [1..6]
enumeration (same mask discipline, distinct trace tags
MR-COP-TRY/OK/FAIL/SKIP, same tries counting). The first
verifying (operator, Z-source) pair wins and builds its
Z via the unchanged mr_buildwin / mr_buildwin_inv
(including execution verification, t16 provenance edge
to the Z source actually used, and delivery).

Composition therefore happens ACROSS queries: query N
fires op i and banks Z_i as a first-class MAP; query
N+1, unsolvable from the taught source, fires op j with
Z_i as its source. No within-query operator chaining.

### 2a. Operator-built Z registry (frozen)

State additions (1392+ is free scratch per the frozen
layout comment; never cleared by ex_query, zeroed per
arm by z_alloc):

- 1392 ZSRC_COUNT i32: number of recorded Z ids.
- 1396..1411 ZSRC_IDS: up to 16 u8 Z MAP ids, build order.

mr_buildwin and mr_buildwin_inv, after a successful
map_create (zid >= 0), append zid to ZSRC_IDS
(guarded by count < 16). These two functions are called
only on the operator paths, so the registry is exactly
the set of operator outputs. No other code writes
1392+. The registry does not change phase-1 behavior:
no phase-1 code reads 1392+.

### 2b. Termination conditions (frozen)

- T1: Phase 2 executes only if phase 1 failed
  (ans < 0). A query solved by a single operator never
  enters composition.
- T2: The phase-2 source list is snapshotted ONCE per
  query, before any phase-2 operator runs. A Z MAP built
  during phase 2 is recorded for FUTURE queries but is
  not added to the current query's list: no intra-query
  chaining, no same-query feedback loop.
- T3: Composition depth per query is exactly one step
  (taught source -> Z_i -> Z_j). Longer chains arise
  only across successive verified queries, each step
  independently gated by full execution verification.
- T4: Every operator invocation remains bounded by the
  frozen loop bounds (fold counts, rel lengths, fact and
  MAP table sizes). Phase 2 adds at most
  (nsources x 6) bounded operator calls per query.
- T5: op_mask gates phase-2 operator tries identically
  to phase 1; phase 2 is skipped entirely when
  op_mask == 0 (reuse disabled).
- T6: A phase-2 source must be live, cap == qcap,
  id != agg_src, and present in ZSRC_IDS (operator
  output, never a taught MAP).

### 2c. Why the discriminating pair is [6,5], not [4,5]

Verified by this worker against the frozen operator
source (preregistered here so the world design is
honest about what it isolates):

- ABSTRACT (op5) on source S needs entry facts with
  rel == S.de, then a S.dnf-fold walk. SUBSTITUTE (op2)
  on the taught source accepts ANY entry rel != 21 with
  the same (u, dnf=2, dvr=4) foldwalk. Hence for any
  query region where ABSTRACT-on-Z verifies,
  SUBSTITUTE-on-mA' verifies too, UNLESS the fold count
  differs: op2 always uses the taught source's dnf=2.
- Only CONCRETIZE (op6) can mint a Z with dnf=3 from
  the taught source alone: from a pattern with nf=3 it
  builds Z with dnf=3. INVERT-A, SUBSTITUTE, TRUNCATE,
  COMBINE all produce dnf in {0,1,2} when run on the
  taught mA' (rl=5). TRUNCATE only reduces dnf.
- Therefore the discriminating composition is
  [6 then 5]: QD1 fires CONCRETIZE and banks Z_conc
  with dnf=3 and de=29; QD2 is a 3-fold region with
  entry rel 29 and source folds (22,23). On the taught
  source: op5 fails (no rel-21 entries), op2 fails
  (2-fold walk lands mid-region), op6 fails (folds are
  not novel against mA's (22,23): OLD-FOLDS), op1/op3/
  op4 fail (no partner route, dead first entry,
  value/terminal mismatch). On Z_conc (de=29, dnf=3):
  op5 verifies.
- The task's example pair [4,5] (INVERT then ABSTRACT)
  CANNOT discriminate in this harness: INVERT-A's Z on
  the taught source has dnf=2, so any region ABSTRACT
  solves on it, SUBSTITUTE solves on the taught source.
  This negative result is preregistered as mechanism
  analysis, not tested with a build.

### 2d. Correction to the prior attempt's predictions

An independent trace of mr_concretize against the
frozen source shows the t16 provenance edge of a
CONCRETIZE-built Z goes to the PATTERN MAP (src1=pat),
not to agg_src: mr_buildwin is called with
src1=pat, and mr_buildwin does e_add(zid,src1,16).
Hence for the FULL arm: e_has(4,3,16)==1 (Z4 was built
by op6 from pattern mP' id 3) and e_has(4,1,16)==0.
The prior lane's prereg wrote (4,1,16)==1, which is
wrong against the frozen code. The adversary's own
build C confirms the rule: its op6-built Z6 has edge
(5,3), i.e. to the pattern. This prereg's bars use the
corrected edges.

## 3. Relation/node id conventions (build D)

Fresh ids, disjoint from builder/adversary families where
it matters (builder used 2,5,6,7,8,9,11,12,15,16,17,18,
19,38; adversary used 4,21-29,31-37):

- V=4 (value relation), E=21 (taught entry),
  F1=22, F2=23 (taught fold pair), P1=24 (partner),
  SE=25 (unused here), G1=26, G2=27 (QD1 novel folds),
  ED=28 (dead entry), EN=29 (new entry, becomes
  Z_conc.de and QD2/QD3 interface), PF1=34, PF2=35
  (pattern folds).
- Taught MAPs: mD' id 0 (dom 2, cap 2=ROUTE, rels [24]);
  mA' id 1 (dom 1, cap 1=AGG, rels [21,22,23,22,23],
  20->25, de=21,dr1=22,dr2=23,dnf=2,dvr=4);
  mB' id 2 (dom 2, cap 2, rels [24,24], 30->32);
  mP' id 3 (dom 1, cap 1, hole entry 0, rels
  [0,34,35,34,35,34,35], 70->77, dnf=3).
- Caps: AGG=1, ROUTE=2. Doms: A=1, B=2 (equality only).

## 4. Frozen world specification (world_D.zag)

42 facts, fid = teach order. All ids fit u8.

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(70,0,71) f10:(71,34,72) f11:(72,35,73)
  f12:(73,34,74) f13:(74,35,75) f14:(75,34,76)
  f15:(76,35,77) f16:(77,4,52)
- QD1 region f17:(90,28,91) f18:(90,29,92)
  f19:(92,26,93) f20:(93,27,94) f21:(94,26,95)
  f22:(95,27,96) f23:(96,26,97) f24:(97,27,98)
  f25:(98,4,59)
- QD2 region f26:(140,29,141) f27:(140,29,142)
  f28:(142,22,143) f29:(143,23,144)
  f30:(144,22,145) f31:(145,23,146)
  f32:(146,22,147) f33:(147,23,148)
  f34:(148,4,63)
- QD3 region f35:(150,29,151) f36:(151,22,152)
  f37:(152,23,153) f38:(153,22,154)
  f39:(154,23,155) f40:(155,22,156)
  f41:(156,23,157)
  (deliberately NO value fact at 157)

MAPs: mD' id0 rs[24] fs[0] 10->11 dom2 cap2;
mA' id1 rs[21,22,23,22,23] fs[1,2,3,4,5] 20->25
dom1 cap1; mB' id2 rs[24,24] fs[7,8] 30->32 dom2
cap2; mP' id3 rs[0,34,35,34,35,34,35]
fs[9,10,11,12,13,14,15] 70->77 dom1 cap1
(de=0,dr1=34,dr2=35,dnf=3,dvr=4).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QD1(90,98,59,1,1), QD2(140,148,63,1,1),
QD3(150,157,64,1,1); re-asks QD1-B(90,98,59,1,1),
QD2-B(140,148,63,1,1).

## 5. Frozen predicted outcomes (build D, extended learner)

Z-row notation: id(live,rl,start,end,dom,cap,
de,dr1,dr2,dnf,dvr,dir) rels[...] facts[...].
Hand-simulated by this worker against the frozen
phase-2 design and the frozen operator source;
section 6 records the bar consequences. as/ae tick
counts are INFORMATIONAL only (printed, not barred).

### 5a. FULL arm (mask 63)

- QA: via=1 (pipeline mA'), val=51.
- QB: via=2 (pipeline mB'), val=-1.
- QD1 (90,98,59): phase 1 on mA' (id 1).
  op1: b=1 dead first entry (90,28,91) FAIL-SHAPE;
  b=2 no partner head from 90: FAIL (try 1).
  op2: (90,28,91) FAIL-SHAPE; (90,29,92) 2-fold
  walk lands on 96 != 98: VERIFY-FAIL (try 2).
  op3: nf2=1, dead first entry: FAIL-SHAPE (try 3).
  op4: Form B lookup finds (98,4,59), tstar=98 !=
  srcend 25: MR-INVVAL-FAIL; Form A no rel-23 hop
  from 90: MR-INV-FAIL (try 4). op5: no rel-21
  entry from 90 (try 5). op6: pattern mP' (nf=3);
  (90,28,91) FAIL-SHAPE; (90,29,92) 3-fold walk to
  98, valof=59, folds (26,27) novel vs (22,23):
  VERIFY-OK (try 6).
  op=6, tries=6, dec=1, via=4, val=59, phit=0.
  Z4 = 4(1,7,90,98,1,1,29,26,27,3,4,0)
  rels[29,26,27,26,27,26,27]
  facts[18,19,20,21,22,23,24].
  e_add(4,3,16) (src1=pattern). ZSRC_IDS=[4].
- QD2 (140,148,63): pipeline fails. Phase 1 on mA':
  op1 FAIL (try 1); op2: (140,29,141) FAIL-SHAPE,
  (140,29,142) 2-fold walk lands on 146 != 148:
  VERIFY-FAIL (try 2); op3 FAIL-SHAPE (try 3);
  op4: Form B tstar=148 != 25, Form A no rel-23
  hop (try 4); op5: no rel-21 entry (try 5);
  op6: pattern mP'; (140,29,141) FAIL-SHAPE;
  (140,29,142) 3-fold walk to 148, valof=63,
  folds (22,23) NOT novel vs mA's (22,23):
  OLD-FOLDS, VERIFY-FAIL (try 6).
  Phase 1: 6 tries, all fail.
  Phase 2: ZSRC_IDS=[4]; Z4 live, cap=1, !=
  agg_src: MR-COMP-SRC id=4.
  op1 on Z4 FAIL (try 7); op2 on Z4: no non-29
  entry from 140: FAIL (try 8); op3 on Z4:
  FAIL-SHAPE (try 9); op4 on Z4: Form B
  tstar=148 != aend 98, Form A reversed
  [27,26,27,26,27,26,29] no rel-27 hop from 140
  (try 10); op5 on Z4 (de=29,dnf=3):
  (140,29,141) FAIL-SHAPE; (140,29,142) 3-fold
  walk to 148, valof=63: VERIFY-OK (try 11).
  op=5, tries=11, dec=1, via=5, val=63, phit=0.
  Z5 = 5(1,7,140,148,1,1,29,22,23,3,4,0)
  rels[29,22,23,22,23,22,23]
  facts[27,28,29,30,31,32,33].
  e_add(5,4,16). ZSRC_IDS=[4,5].
- QD3 (150,157,64): pipeline fails. Phase 1 on
  mA': 6 tries, all fail (op1 no partner tail;
  op2 2-fold to 155 != 157; op3 nf2=1 to 153 !=
  157; op4 Form B no (rel==4,obj==64) fact, Form A
  no rel-23 hop; op5 no rel-21 entry; op6 pattern
  mP' 3-fold walk to 157, valof(157,4)=-1 != 64:
  VERIFY-FAIL).
  Phase 2 on Z4: op1 FAIL (7); op2 no candidate
  (8); op3 miss (9); op4 Form B no value fact,
  Form A no rel-27 hop (10); op5 (150,29,151)
  3-fold walk to 157, valof=-1 != 64: VERIFY-FAIL
  (11); op6 folds (22,23) novel vs Z4's (26,27)
  but valof=-1: FAIL (12).
  Phase 2 on Z5 (de=29,dr=(22,23),dnf=3): op1
  FAIL (13); op2 no candidate (14); op3 miss
  (15); op4 Form B no value fact, Form A reversed
  [23,22,23,22,23,22,29] no rel-23 hop (16);
  op5 to 157, valof=-1: VERIFY-FAIL (17); op6
  folds (22,23) OLD-FOLDS vs Z5's (22,23) (18).
  QD3: val=-2, op=-1, tries=18, dec=0, via=-1,
  phit=0. No new Z. Terminates.
- Re-asks: QD1-B via=4 val=59 entered=0;
  QD2-B via=5 val=63 entered=0 (pipeline walks
  Z5's relseq 140->148).
- FULL t16=2; e_has(4,3,16)=1; e_has(5,4,16)=1;
  e_has(4,1,16)=0; e_has(5,3,16)=0; LINK14 to 4
  and 5; mD' live=1; oth=0.

### 5b. NOREUSE arm (mask 0)

QD1=QD2=QD3=-2, t16=0, oth=0. Phase 2 skipped
(op_mask==0); phase 1 all MR-OP-SKIP.

### 5c. ABLATE-ABS arm (mask 47: ops 1,2,3,4,6)

- QD1: op=6, tries=6, dec=1, via=4, val=59
  (phase 1; op5 masked, never reached).
  Z4 as in 5a. ZSRC_IDS=[4].
- QD2: phase 1: ops 1,2,3,4 fail, op5 SKIP, op6
  OLD-FOLDS fail: 5 tries. Phase 2 on Z4: ops
  1,2,3,4 fail (tries 6,7,8,9), op5 SKIP, op6:
  pattern mP', folds (22,23) novel vs Z4's
  (26,27), 3-fold walk to 148, valof=63:
  VERIFY-OK (try 10). REROUTE: op=6, tries=10,
  dec=1, via=5, val=63. Z5 row identical fields
  to 5a: 5(1,7,140,148,1,1,29,22,23,3,4,0)
  rels[29,22,23,22,23,22,23]
  facts[27,28,29,30,31,32,33],
  but e_add(5,3,16) (src1=pattern, per
  mr_concretize). ZSRC_IDS=[4,5].
- QD3: phase 1: 5 tries (op5 skipped), all fail.
  Phase 2 on Z4: ops 1-4 fail (6,7,8,9), op5
  SKIP, op6 novel folds but valof=-1: FAIL (10).
  Phase 2 on Z5: ops 1-4 fail (11,12,13,14),
  op5 SKIP, op6 OLD-FOLDS (15).
  QD3: val=-2, op=-1, tries=15, dec=0.
- t16=2; e_has(4,3,16)=1; e_has(5,3,16)=1;
  e_has(5,4,16)=0; e_has(4,1,16)=0; oth=0.

### 5d. ABLATE-CONC arm (mask 31: ops 1-5)

- QD1: phase 1 ops 1-5 fail (5 tries), op6 SKIP;
  phase 2: ZSRC empty: MR-COMP-NONE: val=-2,
  op=-1, tries=5.
- QD2: phase 1 ops 1-5 fail (5 tries); phase 2
  empty: val=-2, tries=5.
- QD3: val=-2, tries=5.
- t16=0, oth=0.

### 5e. FRESH arm (facts only, mask 63)

QD1=QD2=QD3=-2 (MR-NO-SRC: no taught MAPs),
t16=0, oth=0.

### 5f. CONTROL arm: frozen learner (build ctl_D)

driver_Dctl.zag on learner_frozen.zag (byte-identical
to l2_metareuse_adversary/learner.zag) + world_D.zag.
FULL (mask 63): QA via=1, QB via=2;
QD1: op=6, tries=6, dec=1, via=4, val=59,
Z4-exact=1 (same row as 5a; the frozen learner
builds it identically);
QD2: phase 1 all 6 fail (same as 5a phase 1),
NO phase 2 exists: val=-2, op=-1, tries=6,
dec=0;
QD3: val=-2, op=-1, tries=6, dec=0;
re-ask QD1-B via=4 val=59 entered=0
(QD2-B is not re-asked in the control arm: no Z5
exists, so pipeline fails and meta-reuse fails
with val=-2);
t16=1; e_has(4,3,16)=1; e_has(4,1,16)=0;
LINK14 to 4; mD' live=1; oth=0.
NOREUSE (mask 0): QD1=QD2=QD3 val=-2, t16=0, oth=0.

The control proves the composition step is
NECESSARY: the frozen 6-operator harness, on the
identical world, cannot solve QD2 (or QD3).

## 6. Frozen kill bars (build D, extended learner)

- D-K1 (baselines): FULL arm: qa_via==1, qb_via==2.
- D-K2 (reuse necessity): FULL arm: QD1/QD2 phit==0.
  NOREUSE arm: QD1=QD2=QD3 val==-2 and t16==0.
- D-K3 (composition decides): FULL arm: QD1:
  op==6, tries==6, dec==1; QD2: op==5, tries==11,
  dec==1 (the composition signature: op 5 fired on
  a Z source after 6 failed phase-1 tries);
  QD3: op==-1, tries==18, dec==0, val==-2
  (bounded termination with two Z sources live).
- D-K4 (exact grounding + persistence): FULL arm:
  QD1: via==4, val==59, Z4-exact==1 (section 5a
  row, checked field by field); QD2: via==5,
  val==63, Z5-exact==1; re-asks: QD1-B via==4
  val==59 entered==0; QD2-B via==5 val==63
  entered==0.
- D-K5 (operator necessity, incl. composition
  reroute): ABLATE-CONC (31): QD1=QD2=QD3 val==-2,
  tries==5 each, t16==0 (op6 necessary for the
  whole chain: without it no Z_conc exists, so
  QD2 cannot compose). ABLATE-ABS (47): QD1:
  op==6, tries==6, via==4, val==59; QD2: op==6,
  tries==10, via==5, val==63 (composition still
  fires through the phase-2 CONCRETIZE path on
  Z_conc: the reroute is preregistered, not a
  surprise); QD3: val==-2, tries==15, op==-1;
  t16==2 with e_has(5,3,16)==1 and
  e_has(5,4,16)==0.
- D-K6 (determinism): 3 runs of comp_D_bin
  byte-identical (shell sha256).
- D-K7 (control discrimination): ctl_D_bin (frozen
  learner): FULL arm QD1: op==6, tries==6,
  via==4, val==59, Z4-exact==1; QD2: val==-2,
  tries==6, op==-1, dec==0; QD3: val==-2,
  tries==6, op==-1, dec==0; t16==1;
  e_has(4,3,16)==1; e_has(4,1,16)==0; LINK14 to 4;
  mD' live==1; oth==0. NOREUSE arm: QD1=QD2=QD3
  val==-2, t16==0. 3/3 byte-identical.
- D-K8 (provenance hygiene): FULL arm: t16==2;
  e_has(4,3,16)==1; e_has(5,4,16)==1;
  e_has(4,1,16)==0; e_has(5,3,16)==0; LINK14
  present to 4 and 5; mD' live==1; oth==0 in
  every arm (FULL/NOREUSE/ABLATE-ABS/ABLATE-CONC/
  FRESH).

## 7. Regression: the seven sealed adversary builds

Builds reg_A, reg_B, reg_C, reg_X1, reg_X2, reg_X3,
reg_X4: the EXTENDED learner.zag + byte-identical
copies of the adversary's world_*.zag and driver_*.zag
(sha256-verified against
l2_metareuse_adversary/{world,driver}_*.zag at build
time). The extended learner's phase 1 is textually
identical to the frozen mr_adapt; the only additions
are the ZSRC registry writes in mr_buildwin /
mr_buildwin_inv (no checked field changes) and the
phase-2 block, which runs only when phase 1 fails.

Frozen bar R-REG: every predicted outcome in the
adversary PREREG sections 5a-5g reproduces EXACTLY on
the extended learner: same op/tries/dec/via/val/phit
per query, same Z rows, same ablation vals and t16
counts, same re-ask behavior, same K1'-K5',K8' bar
values, XK1' boundaries (val=-2, tries=6, op=-1,
t16=0, oth=0) on X1-X4, XK2' NOREUSE, XK3' trace
greps (the one new trace line MR-COMP-NONE emitted
when phase 2 finds no Z source does not disturb any
XK3' pattern), XK4' 3/3 byte-identical runs,
termination on X4. Rationale per build: A/B/C reuse
queries all verify in phase 1 (tries 1,2,3 / 4,4 /
5,6), so phase 2 never runs; X1-X4 reach phase 2 with
an empty ZSRC registry, so behavior is identical
apart from the single MR-COMP-NONE line.

R-K7' (change audit): diff of extended learner.zag
against the frozen learner.zag shows ONLY: (a) header
comment paragraph describing phase 2, (b) state
layout comment lines for 1392/1396, (c) ZSRC append
in mr_buildwin and mr_buildwin_inv, (d) the phase-2
block in mr_adapt. No other line differs.

## 8. Falsifiers (in-Zag, build D)

F-EDGE-NEW: oth!=0 in any arm.
F-NO-GROUND: via/val/op/tries/dec != section 5.
F-WRONG-Z: any Z-exact check != 1.
F-PIPE-HIT: QD1/QD2 phit!=0 in FULL.
F-NOREUSE: NOREUSE QD val!=-2 or t16!=0.
F-ABLATE: ablation-arm vals/tries/t16/edges != 5c/5d.
F-RE: re-ask entered!=0 or via/val != expected.
F-T16: t16 count or e_has edge != expected.
F-DISTR: mD' live!=1 at FULL end.
F-FRESH: FRESH-arm QD val!=-2.
F-CTL: control-arm vals/tries/t16 != 5f.
F-TERM: QD3 tries!=18 (FULL) or any run hangs
(a hang is a wave FAIL, not a boundary).
F-SEAL-D: shell grep of MR-OP-TRY/MR-OP-OK/
MR-COP-TRY/MR-SUB-CAND/MR-TRUNC-TRY/MR-ABS-CAND/
MR-CONC-CAND/MR-INV-REV/MR-INVVAL-OK/MR-BIND in
driver_D.zag, driver_Dctl.zag, world_D.zag = 0
(the driver/world never name an operator or form).
F-REG: any R-REG mismatch on the seven sealed builds.
Any falsifier firing fails the wave for that build.

## 9. Verdict rule

L2-METAREUSE-COMPOSE-2-PASS iff ALL of:
(1) R-REG holds on all seven sealed builds (the
existing 6-operator behavior is unbroken);
(2) D-K1 through D-K8 hold on build D, including the
QD2 composition signature (op=5, tries=11, via=5)
and the QD3 bounded-termination signature (tries=18,
-2, no new Z);
(3) D-K7 holds: the frozen-learner control fails QD2
and QD3 (-2, tries=6), proving composition is what
solves QD2;
(4) determinism: 3/3 byte-identical runs per binary
(comp_D, ctl_D, reg_A/B/C/X1/X2/X3/X4);
(5) zero falsifiers, zero hangs.

If QD2 verifies on the control binary, the world is
broken (single operators suffice): verdict FAIL with
redesign, not a composition PASS. If QD2 fails on the
extended learner, composition as designed does not
work: verdict FAIL with the trace evidence.

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
- Build D's world is worker-designed (this worker
  audited the prior lane's design and re-verified
  every prediction against the frozen source itself);
  its discriminating power comes from the frozen-
  learner control arm (5f/6-D-K7), not from designer
  blindness. Stated as a non-claim, not a seal.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs; nothing
  pushed. Adversary and builder lane directories are
  never modified.
- Non-claims: one composition pair [6,5] on one fresh
  family does not establish general operator
  composability; within-query operator chaining,
  longer chains, the protected core, the continuing
  learner, scaling, and transfer are out of scope.
