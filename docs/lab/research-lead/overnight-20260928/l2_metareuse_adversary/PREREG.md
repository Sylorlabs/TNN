# PREREG: L2-METAREUSE-ADVERSARY (sealed-world generality probe)

Frozen 2026-10-03 by the L2-METAREUSE-ADVERSARY worker,
BEFORE any implementation exists. This file plus
NAMECHECK.md will be committed ALONE.

## 1. Mandate and scope

The L2 meta-reuse arc reached L2-INVERT-VALUE-PASS
(K1-K8) on ONE builder-designed world family, with the
honest non-claim: "one builder-designed world family, no
sealed-adversary generality". This wave supplies the
sealed-adversary generality test for the 6-operator
meta-reuse harness (ops 1=COMBINE, 2=SUBSTITUTE,
3=TRUNCATE, 4=INVERT with Form A structural reversal and
Form B value-mapping inversion, 5=ABSTRACT,
6=CONCRETIZE; fixed order [1..6], first verifying
operator wins).

Seven sealed builds. Each build = the builder's frozen
`learner.zag` (reused BYTE-IDENTICAL, never edited) +
one adversary-designed `world_*.zag` + one
adversary-designed `driver_*.zag`, concatenated and
compiled with the pinned znc. The driver never names an
operator, a source pair, a binding, a pattern, or a
form; queries are issued as (start,terminal,value,cap,
dom) with one arm-level OP_MASK, exactly as in the
builder lanes.

## 2. Relation/node id conventions (all builds)

All ids fit u8. Fresh ids, disjoint from the builder's
family (builder used rels 2,5,6,7,8,9,11,12,15,16,17,
18,19,38):

- V=4 (value relation), E=21 (source entry),
  F1=22, F2=23 (source fold pair), P1=24 (partner and
  distractor rel), SE=25 (substitute entry),
  G1=26, G2=27 (query-region fold pair),
  ED=28 (dead entry), EN=29 (new entry),
  D1=31 (decoy fold), C1=32, C2=33 (cycle pair),
  PF1=34, PF2=35 (pattern folds), PE1=36, PE2=37
  (second-pattern folds), hole rel 0.
- Taught MAPs per build: mD' id 0 (distractor, dom 2,
  cap 2=ROUTE, rels [P1]); mA' id 1 (AGG source, dom 1,
  cap 1=AGG); mB' id 2 (partner, dom 2, cap 2, rels
  [P1,P1]); mP' id 3 (pattern, dom 1, cap 1, hole
  entry 0) where needed.
- Caps: AGG=1, ROUTE=2. Doms: A=1, B=2 (equality only).

## 3. World design rationale

Each world isolates exactly one operator (core builds)
or attacks one mechanism decision point
(falsification builds). Fact ids (fid) are teach order;
first-match scans (entry scan, fold discovery,
value lookup, source/pattern search) resolve ties by
lowest fid, which the designs below exploit or respect
deliberately.

### Build A (core: COMBINE, SUBSTITUTE, TRUNCATE)

Fresh family: rels 21/22/23/24/25/26/27/4, source
mA' nf=2 (rels [21,22,23,22,23]), partner mB' rels
[24,24]. Tests whether ops 1-3 fire on a topology the
builder never drew: different ids, nf=2 source, and a
TRUNCATE query that reuses the source's own start node
(a genuine prefix-reuse shape, not a fresh region).

- Q1 (40,47,53,AGG,B): COMBINE. Partner head [24,24]
  from 40 reaches 42, then the AGG tail [21,22,23,22,
  23] is discovered at runtime from 42 to 47 with
  value 53. Op 1 must win; the distractor mD' ([24])
  must fail both bindings first (route too short).
- Q2 (50,55,54,AGG,A): SUBSTITUTE. Fresh entry
  rel 25 with runtime-discovered folds (26,27) to 55,
  value 54. Ops 1 must fail (no partner route from 50
  or from the AGG-head midpoint 55).
- Q3 (20,23,55,AGG,A): TRUNCATE. Start = mA's own
  start; 1-fold prefix to 23 with a dedicated value
  fact (23,4,55). Ops 1-2 must fail (no partner
  route; no non-entry candidate from 20).

### Build B (core: INVERT Form A + Form B)

Fresh family for both INVERT forms in one world.

- Q4A (60,65,56,AGG,A): Form A only. The reversed
  source relseq [23,22,23,22,21] is walked strictly
  forward from 60 to 65, value 56. Form B must fail:
  the value 56 lives at 65, not at the source end 25
  (strict source-terminal check). Ops 1-3 must fail
  (SUBSTITUTE's foldwalk shape-fails on the reversed
  chain; TRUNCATE's 1-fold prefix misses 65).
- Q4B (57,20,57,AGG,A): Form B only. Reverse value
  lookup finds (25,4,57); 25 equals the source end;
  backward obj-match walk over [23,22,23,22,21]
  reaches key 20. Form A is never attempted (Form B
  tried first and verifies). Ops 1-3 must fail (the
  value node 57 has no outgoing facts at all).

### Build C (core: ABSTRACT, CONCRETIZE)

Fresh family; pattern mP' has nf=3 (not the builder's
2) to prove the fold count is read from the pattern,
not hardcoded.

- Q5 (80,86,58,AGG,A): ABSTRACT. TWO entry
  candidates share the interface rel 21: the lower-fid
  candidate (80,21,81) is a dead end (tests candidate
  backtracking: the learner must skip it and use
  (80,21,82)), then runtime folds (26,27) to 86,
  value 58. Ops 1-4 must fail (COMBINE/TRUNCATE take
  the dead first entry; SUBSTITUTE has no non-entry
  candidate; INVERT's value lives at 86 not 25).
- Q6 (90,98,59,AGG,A): CONCRETIZE. Dead entry
  (90,28,91) first, live entry (90,29,92) second;
  3-fold region with novel folds (26,27) vs the
  source's (22,23); pattern mP' (nf=3) supplies the
  skeleton. Ops 1-5 must fail (SUBSTITUTE's dnf=2
  foldwalk cannot span 3 folds; ABSTRACT has no
  rel-21 entry; INVERT's value is at 98 not 25).

### Build X1 (falsify: greedy first-match fold discovery)

SUBSTITUTE-shaped query (100,106,61) where the fold
node 101 has TWO outgoing non-value facts: decoy
(101,31,102) at LOWER fid (dead end) and the live
(101,26,103). ex_foldwalk takes the first fid match
with no backtracking, so it commits to the decoy and
shape-fails. PREDICTED: all 6 ops fail, ANS -2. This
tests the implied claim "fold relations are
discovered at runtime": discovery is greedy
first-match, and this world makes the greediness
observable. Predicted graceful failure with trace
MR-SUB-CAND r=25 u=101 then FAIL-SHAPE.

### Build X2 (falsify: first-match reverse value lookup)

INVERT-Form-B-shaped query (57,20,57) where the value
57 is carried by TWO facts: decoy (110,4,57) at LOWER
fid and the genuine (25,4,57) at the source end.
mr_invert_val keeps the FIRST (rel==dvr,obj==v)
match, so tstar=110 != source end 25 and the strict
terminal check fires. Form A cannot apply (no
rel-23 hop from 57). PREDICTED: all 6 ops fail,
ANS -2, trace MR-INVVAL-LOOKUP t*=110 srcend=25 then
MR-INVVAL-FAIL then MR-INV-FAIL. Tests whether the
"reverse value lookup" is robust to value aliasing.

### Build X3 (falsify: first-match pattern selection /
operator interference)

CONCRETIZE-shaped query (90,96,59) with TWO live
pattern MAPs: mP1' (id 3, nf=3) and mP2' (id 4,
nf=2). The query region has 2 folds, fitting mP2'
but not mP1'. Pattern search takes the FIRST
(cap==qcap, entry==0) MAP in id order, so it commits
to mP1' and fails. PREDICTED: ANS -2, trace
MR-PATTERN-SRC id=3. Tests whether pattern selection
is positional rather than best-fit (two patterns
interfere).

### Build X4 (falsify: greedy discovery trapped by a cycle)

SUBSTITUTE-shaped query (120,126,62) where fold node
121 offers a 2-cycle (121,32,122),(122,33,121) at
LOWER fid than the live continuation (121,26,123).
ex_foldwalk commits to the cycle, walks it k times
(it is bounded, so it terminates), and lands on 121
instead of 126: VERIFY-FAIL. PREDICTED: all 6 ops
fail, ANS -2, trace SHAPE-OK term=121 then
VERIFY-FAIL. Tests termination + correctness of
discovery under cyclic ambiguity (no hang is
predicted; a hang would be a wave-level FAIL).

## 4. Frozen world specifications

Notation fid:(sub,rel,obj). Teach order = fid order.

### 4a. Build A (world_A.zag): 24 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(40,24,41) f10:(41,24,42) f11:(42,21,43)
  f12:(43,22,44) f13:(44,23,45) f14:(45,22,46)
  f15:(46,23,47) f16:(47,4,53)
- f17:(50,25,51) f18:(51,26,52) f19:(52,27,53)
  f20:(53,26,54) f21:(54,27,55) f22:(55,4,54)
- f23:(23,4,55)

MAPs: mD' id0 rs[24] fs[0] 10->11 dom2 cap2;
mA' id1 rs[21,22,23,22,23] fs[1,2,3,4,5] 20->25
dom1 cap1 (de=21,dr1=22,dr2=23,dnf=2,dvr=4);
mB' id2 rs[24,24] fs[7,8] 30->32 dom2 cap2.

Queries (FULL mask 63): QA(20,25,51,1,1),
QB(30,32,-1,2,2), Q1(40,47,53,1,2),
Q2(50,55,54,1,1), Q3(20,23,55,1,1);
re-asks Q1-B, Q2-B, Q3-B.

### 4b. Build B (world_B.zag): 16 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(60,23,61) f10:(61,22,62) f11:(62,23,63)
  f12:(63,22,64) f13:(64,21,65) f14:(65,4,56)
- f15:(25,4,57)

MAPs: same three as build A (ids 0,1,2).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
Q4A(60,65,56,1,1), Q4B(57,20,57,1,1);
re-asks Q4A-B, Q4B-B.

### 4c. Build C (world_C.zag): 33 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(70,0,71) f10:(71,34,72) f11:(72,35,73)
  f12:(73,34,74) f13:(74,35,75) f14:(75,34,76)
  f15:(76,35,77) f16:(77,4,52)
- f17:(80,21,81) f18:(80,21,82) f19:(82,26,83)
  f20:(83,27,84) f21:(84,26,85) f22:(85,27,86)
  f23:(86,4,58)
- f24:(90,28,91) f25:(90,29,92) f26:(92,26,93)
  f27:(93,27,94) f28:(94,26,95) f29:(95,27,96)
  f30:(96,26,97) f31:(97,27,98) f32:(98,4,59)

MAPs: mD' id0, mA' id1, mB' id2 (as build A);
mP' id3 rs[0,34,35,34,35,34,35] fs[9,10,11,12,
13,14,15] 70->77 dom1 cap1
(de=0,dr1=34,dr2=35,dnf=3,dvr=4).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
Q5(80,86,58,1,1), Q6(90,98,59,1,1);
re-asks Q5-B, Q6-B.

### 4d. Build X1 (world_X1.zag): 22 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(70,0,71) f10:(71,34,72) f11:(72,35,73)
  f12:(73,34,74) f13:(74,35,75) f14:(75,4,52)
- f15:(100,25,101) f16:(101,31,102)
  f17:(101,26,103) f18:(103,27,104)
  f19:(104,26,105) f20:(105,27,106)
  f21:(106,4,61)

MAPs: mD' id0, mA' id1, mB' id2;
mP' id3 rs[0,34,35,34,35] fs[9,10,11,12,13]
70->75 dom1 cap1 (de=0,dr1=34,dr2=35,dnf=2,
dvr=4).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QX1(100,106,61,1,1).

### 4e. Build X2 (world_X2.zag): 11 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(110,4,57)
- f10:(25,4,57)

MAPs: mD' id0, mA' id1, mB' id2 (no pattern).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QX2(57,20,57,1,1).

### 4f. Build X3 (world_X3.zag): 32 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,22,26)
  f7:(26,23,27) f8:(27,4,51)
- f9:(30,24,31) f10:(31,24,32)
- f11:(70,0,71) f12:(71,34,72) f13:(72,35,73)
  f14:(73,34,74) f15:(74,35,75) f16:(75,34,76)
  f17:(76,35,77) f18:(77,4,52)
- f19:(80,0,81) f20:(81,36,82) f21:(82,37,83)
  f22:(83,36,84) f23:(84,37,85) f24:(85,4,53)
- f25:(90,28,91) f26:(90,29,92) f27:(92,26,93)
  f28:(93,27,94) f29:(94,26,95) f30:(95,27,96)
  f31:(96,4,59)

MAPs: mD' id0; mA' id1 rs[21,22,23,22,23,22,23]
fs[1,2,3,4,5,6,7] 20->27 dom1 cap1
(de=21,dr1=22,dr2=23,dnf=3,dvr=4); mB' id2;
mP1' id3 rs[0,34,35,34,35,34,35]
fs[11,12,13,14,15,16,17] 70->77 dom1 cap1
(de=0,dnf=3); mP2' id4 rs[0,36,37,36,37]
fs[19,20,21,22,23] 80->85 dom1 cap1
(de=0,dnf=2).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QX3(90,96,59,1,1).

### 4g. Build X4 (world_X4.zag): 23 facts

- f0:(10,24,11)
- f1:(20,21,21) f2:(21,22,22) f3:(22,23,23)
  f4:(23,22,24) f5:(24,23,25) f6:(25,4,51)
- f7:(30,24,31) f8:(31,24,32)
- f9:(70,0,71) f10:(71,34,72) f11:(72,35,73)
  f12:(73,34,74) f13:(74,35,75) f14:(75,4,52)
- f15:(120,25,121) f16:(121,32,122)
  f17:(122,33,121) f18:(121,26,123)
  f19:(123,27,124) f20:(124,26,125)
  f21:(125,27,126) f22:(126,4,62)

MAPs: mD' id0, mA' id1, mB' id2;
mP' id3 rs[0,34,35,34,35] fs[9,10,11,12,13]
70->75 dom1 cap1 (de=0,dnf=2).

Queries: QA(20,25,51,1,1), QB(30,32,-1,2,2),
QX4(120,126,62,1,1).

## 5. Frozen predicted outcomes

Z-row notation: id(live,rl,start,end,dom,cap,
de,dr1,dr2,dnf,dvr,dir) rels[...] facts[...].
All derivations were hand-simulated against the
frozen learner; section 7 records the bar
consequences. as/ae tick counts are INFORMATIONAL
only (printed, not barred).

### 5a. Build A

- QA: via=1 (pipeline mA'), val=51.
- QB: via=2 (pipeline mB'), val=-1.
- Q1: op=1, tries=1, dec=1, via=4, val=53,
  phit=0. Z1 = 4(1,7,40,47,2,1,0,0,0,0,4,0)
  rels[24,24,21,22,23,22,23]
  facts[9,10,11,12,13,14,15].
  (op1: rsrc mD' b=1 shape-fail, b=2 fail;
  rsrc mB' b=1 shape-fail, b=2 VERIFY-OK.)
- Q2: op=2, tries=2, dec=1, via=5, val=54,
  phit=0. Z2 = 5(1,5,50,55,1,1,25,26,27,2,4,0)
  rels[25,26,27,26,27] facts[17,18,19,20,21].
  (op1: AGG head reaches 55, partner tails from 55
  fail; b=2 partner heads from 50 fail.)
- Q3: op=3, tries=3, dec=1, via=6, val=55,
  phit=0. Z3 = 6(1,3,20,23,1,1,21,22,23,1,4,0)
  rels[21,22,23] facts[1,2,3].
  (op1: AGG head reaches 25, partner tails fail;
  b=2 fail. op2: no non-entry candidate from 20.
  op3: nf2=1 verifies to 23 with (23,4,55).)
- Re-asks: Q1-B via=4 val=53 entered=0;
  Q2-B via=5 val=54 entered=0;
  Q3-B via=6 val=55 entered=0.
- FULL t16=4; e_has (4,1,16),(4,2,16),
  (5,1,16),(6,1,16); LINK14 to 4,5,6; mD' live.
- Arms: FULL mask 63; ABLATE-COMBINE mask 62:
  Q1=-2, Q2=54, Q3=55, t16=2;
  ABLATE-SUBST mask 61: Q1=53, Q2=-2, Q3=55,
  t16=3; ABLATE-TRUNC mask 59: Q1=53, Q2=54,
  Q3=-2, t16=3; NOREUSE mask 0: Q1=Q2=Q3=-2,
  t16=0; FRESH: Q1=Q2=Q3=-2, t16=0.

### 5b. Build B

- QA: via=1, val=51. QB: via=2, val=-1.
- Q4A: op=4, tries=4, dec=1, via=4, val=56,
  phit=0. Z4a = 4(1,5,60,65,1,1,23,22,23,2,4,0)
  rels[23,22,23,22,21] facts[9,10,11,12,13].
  (op1: b=1 shape-fail, b=2 fail. op2: foldwalk
  shape-fail on the reversed chain. op3: 1-fold
  prefix reaches 63 not 65. op4: Form B lookup
  finds (65,4,56), tstar=65 != 25, MR-INVVAL-FAIL;
  Form A strict walk 60->65, MR-INV-OK.)
- Q4B: op=4, tries=4, dec=1, via=5, val=57,
  phit=0. Z4b = 5(1,6,57,20,1,1,4,23,22,2,4,1)
  rels[4,23,22,23,22,21] facts[15,5,4,3,2,1].
  (ops 1-3: value node 57 has no outgoing facts.
  op4: Form B lookup finds (25,4,57), tstar=25
  == source end, backward walk 25->20,
  MR-INVVAL-OK; Form A never attempted.)
- Re-asks: Q4A-B via=4 val=56 entered=0;
  Q4B-B via=5 val=57 entered=0 (backward
  pipeline execution of the dir=1 MAP).
- FULL t16=2; e_has (4,1,16),(5,1,16);
  LINK14 to 4,5; mD' live.
- Arms: FULL 63; ABLATE-INV 55: Q4A=-2, Q4B=-2,
  t16=0; NOREUSE 0: -2s, t16=0; FRESH: -2s.

### 5c. Build C

- QA: via=1, val=51. QB: via=2, val=-1.
- Q5: op=5, tries=5, dec=1, via=4, val=58,
  phit=0. Z5 = 4(1,5,80,86,1,1,21,26,27,2,4,0)
  rels[21,26,27,26,27] facts[18,19,20,21,22].
  (op1: b=1 takes dead first entry (80,21,81),
  shape-fail; b=2 fail. op2: no non-entry
  candidate. op3: dead first entry, fail. op4:
  Form B tstar=86 != 25; Form A no rel-23 hop
  from 80. op5: candidate 1 (u=81) FAIL-SHAPE,
  candidate 2 (u=82) VERIFY-OK with folds
  (26,27).)
- Q6: op=6, tries=6, dec=1, via=5, val=59,
  phit=0. Z6 = 5(1,7,90,98,1,1,29,26,27,3,4,0)
  rels[29,26,27,26,27,26,27]
  facts[25,26,27,28,29,30,31].
  (op1: dead first entry. op2: dnf=2 foldwalk
  cannot span the 3-fold region (term 96 !=
  98). op3: dead first entry. op4: tstar=98
  != 25; no rel-23 hop. op5: no rel-21 entry.
  op6: pattern mP' (nf=3) matched; candidate 1
  dead; candidate 2 verifies with novel folds
  (26,27) vs source (22,23).)
- Re-asks: Q5-B via=4 val=58 entered=0;
  Q6-B via=5 val=59 entered=0.
- FULL t16=2; e_has (4,1,16),(5,3,16);
  LINK14 to 4,5; mD' live.
- Arms: FULL 63; ABLATE-ABS 47: Q5=-2, Q6=59,
  t16=1; ABLATE-CONC 31: Q5=58, Q6=-2, t16=1;
  NOREUSE 0: -2s, t16=0; FRESH: -2s.

### 5d. Build X1

- QA: via=1, val=51. QB: via=2, val=-1.
- QX1: PREDICTED val=-2, tries=6, op=-1,
  t16=0, oth=0. All 6 ops attempted and failed:
  op2 trace MR-SUB-CAND r=25 u=101 then
  FAIL-SHAPE (greedy fold pick commits to decoy
  f16). op6 reaches pattern mP' but its
  candidate shape-fails on the same decoy.
- Arms: FULL 63; NOREUSE 0 (val -2, t16 0).

### 5e. Build X2

- QA: via=1, val=51. QB: via=2, val=-1.
- QX2: PREDICTED val=-2, tries=6, op=-1,
  t16=0, oth=0. op4 trace MR-INVVAL-LOOKUP
  t*=110 srcend=25, MR-INVVAL-FAIL, then
  MR-INV-FAIL (no rel-23 hop from 57). op6:
  MR-NO-PATTERN.
- Arms: FULL 63; NOREUSE 0.

### 5f. Build X3

- QA: via=1, val=51. QB: via=2, val=-1.
- QX3: PREDICTED val=-2, tries=6, op=-1,
  t16=0, oth=0. op6 trace MR-PATTERN-SRC id=3
  (commits to mP1', nf=3, which cannot span the
  2-fold region); mP2' (id 4, nf=2, fitting) is
  never considered.
- Arms: FULL 63; NOREUSE 0.

### 5g. Build X4

- QA: via=1, val=51. QB: via=2, val=-1.
- QX4: PREDICTED val=-2, tries=6, op=-1,
  t16=0, oth=0. op2 trace MR-SUB-CAND r=25
  u=121, SHAPE-OK term=121, VERIFY-FAIL (cycle
  walked, terminates, lands on 121 not 126).
  Run must TERMINATE (all discovery loops are
  fold-count bounded); a hang is a wave FAIL.
- Arms: FULL 63; NOREUSE 0.

## 6. Frozen kill bars

### 6a. Core builds (A, B, C)

- K1' (baselines): FULL arm: qa_via==1,
  qb_via==2.
- K2' (reuse necessity): FULL arm: every reuse
  query phit==0. NOREUSE arm: every reuse query
  val==-2 and t16==0.
- K3' (verification decides): FULL arm, per
  reuse query: op==intended (A:1,2,3; B:4,4;
  C:5,6), tries==op index, dec==1.
- K4' (exact grounding + persistence): FULL
  arm, per reuse query: via==expected Z id,
  val==expected value, Z-exact==1 (section 5
  rows, checked field by field); re-ask:
  via==Z id, val==expected, entered==0.
- K5' (operator necessity): ablation arms per
  section 5: ablating the intended op kills
  exactly its query (-2); all other queries
  keep FULL-arm values; t16 counts per
  section 5.
- K6' (determinism): 3 runs per build
  byte-identical (shell sha256).
- K7' (seal): this lane's learner.zag
  sha256-identical to the builder's frozen
  `l2_invert_value/learner.zag`; shell grep of
  MR-OP-TRY/MR-OP-OK/MR-SUB-CAND/MR-TRUNC-TRY/
  MR-ABS-CAND/MR-CONC-CAND/MR-INV-REV/
  MR-INVVAL-OK/MR-BIND in each driver_*.zag = 0
  (the driver never names an operator or form).
- K8' (provenance hygiene): FULL arm:
  t16==expected count; e_has==1 for each
  expected (Z,source,16) edge; LINK14 present
  to each built Z; mD' live==1 at end;
  oth (ex_eoth)==0 in every arm.

Verdict rule (core): ALL of K1'-K8' PASS on all
three builds -> the operators generalize to the
fresh families. Any K-bar FAIL on a clean
isolated world is a genuine generality failure
and fails the wave for that family (reported
per-build, not averaged away).

### 6b. Falsification builds (X1-X4)

- XK1' (predicted boundary): FULL arm:
  val==-2, tries==6, op==-1, t16==0, oth==0.
  If instead val!=-2 (a correct-by-verification
  answer), the prediction is FALSIFIED in the
  positive direction: report HARNESS-SOLVED
  (generality stronger than the adversary
  modeled), not a defect.
- XK2': NOREUSE arm: val==-2, t16==0.
- XK3' (mechanism trace evidence, shell grep on
  run output): X1: `MR-SUB-CAND r=25 u=101`
  followed by `FAIL-SHAPE`, and `MR-OP-FAIL 6`;
  X2: `MR-INVVAL-LOOKUP t*=110 srcend=25`,
  `MR-INVVAL-FAIL`, `MR-INV-FAIL`;
  X3: `MR-PATTERN-SRC id=3`;
  X4: `SHAPE-OK term=121` followed by
  `VERIFY-FAIL`.
- XK4' (determinism + termination): 3 runs
  byte-identical; every run terminates (a hang
  is a wave FAIL, not a boundary).
- XK5' (seal): same as K7'.

Verdict rule (X): XK2'-XK5' must PASS. XK1'
distinguishes "predicted boundary confirmed"
(val==-2) from "harness solved" (val!=-2);
both are reported honestly. Crash, hang,
non-determinism, or oth!=0 fails the wave.

## 7. Falsifiers (in-Zag, per build)

F-EDGE-NEW: oth!=0 in any arm.
F-NO-GROUND: via/val/op/tries/dec != section 5.
F-WRONG-Z: any Z-exact check != 1.
F-PIPE-HIT: reuse query phit!=0 in FULL.
F-NOREUSE: NOREUSE reuse val!=-2 or t16!=0.
F-ABLATE: ablation-arm vals/t16 != section 5.
F-RE: re-ask entered!=0 or via/val != expected.
F-T16: t16 count or e_has edge != expected.
F-DISTR: mD' live!=1 at FULL end.
F-FRESH: FRESH-arm reuse val!=-2.
F-SEAL: learner.zag sha256 != builder's (shell).
Any falsifier firing fails the wave for that
build (XK1'-positive case excepted per 6b).

## 8. Standing rules for this wave

- Prereg frozen BEFORE implementation; this
  file + NAMECHECK.md committed ALONE. Any
  pre-verdict correction goes in a
  PREREG_AMENDMENT file, transparent, never
  silent; no counting-rule or learner-code
  change is possible (learner is frozen
  and reused byte-identical).
- Pure Zag for all scientific computation;
  safebin PATH; no python3/python (Step 0).
- as/ae tick counts are INFORMATIONAL ONLY:
  printed per query per arm for the record,
  never bars. Determinism is established by
  3/3 byte-identical runs (K6'/XK4').
- The harness claim under test is L2
  (learner-driven structural adaptation with
  operator choice), not L3: the operator menu
  and INVERT forms are researcher-supplied.
  This wave cannot promote anything to L3.
- No em/en dashes in loop documentation.
- Commits local with explicit pathspecs;
  nothing pushed. Builder lane directories
  are never modified.
- Non-claims: 3 fresh core families + 4
  adversarial probes do not establish
  universal generality; the protected core,
  the continuing learner, scaling, and
  transfer are out of scope. A PASS here
  retires the "single builder-designed
  family" non-claim for these operators; it
  does not certify them against all worlds.
