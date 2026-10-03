# PREREG: GEN-STRESS -- Mapping the True Generality Boundary of GEN

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-1) strictly precedes all
implementation. Worker: gen-stress. Date: 2026-10-03.

## 1. Question

GEN-GENERALITY (C402) proved GEN (the frozen C380 value-graph extension of U:
rounds over a value pool plus observed-kind checking, d6_gen.zag at
82732a9e8, UNMODIFIED) handles fan-in, DAG-4, chain-3, and partial
applicability with no new mechanism. The proven envelope is therefore:
up to 4 structures, up to 3 levels, 1- and 2-input shapes, within 6 rounds
and 64 pool values, with honest decline (ANS=-2) on unsatisfiable graphs.

This battery pushes beyond that envelope on four axes and maps exactly
where GEN breaks:

- S1 SCALE-5: five structures in a 5-deep chain (beyond chain-3).
- S2 SCALE-6-DAG: six structures, four levels, 3-way fan-out feeding two
  sequential 2-input combiners (the dual-combiner DAG shape the C402 prereg
  rejected as a world design over sum collisions; built here with
  collision-free value engineering).
- S3 NEAR-MISS: the expected answer is reachable ONLY through a
  kind-violating application (one slot kind off). A quiet round fires
  WIDEN. Does GEN decline cleanly or emit a contract-violating success?
- S4 ROUND-CAP: a valid 7-structure chain needing 7 rounds, one more than
  the frozen cap of 6. Clean decline or wrong answer?
- S5 POOL-CAP: a (NUM,NUM) combiner over a quadratically growing pool,
  driving the value pool past 64 entries and the tried2 table past 64
  entries under real load. What do the two caps do?

## 2. The mechanism under test (frozen, unmodified)

GEN is d6_gen.zag at commit 82732a9e8, unchanged (digests in NAMECHECK.md
Step 1). Recap of the frozen rules, plus the boundary-relevant mechanics
this battery exercises (all read directly from the frozen source):

- Value pool seeded with the query subject; each pool value carries its
  observed kind (pkind: 1 = NODE iff the value is a fact subject, else
  2 = NUM) and provenance.
- Rounds (cap 6, all six execute): per round, every MAP in id order
  (1-input MAPs, then 2-input MAPs) is applied to every pool value present
  at round start (pool order; 2-input MAPs over all (i,j) pairs in lex
  order), skipping already-tried applications.
- Admission (compatibility, empty = compatible): 1-input (m,v) admitted
  iff kind(v) in m.inmask; 2-input (m,v1,v2) iff kind(v1) in m.inmask1 and
  kind(v2) in m.inmask2. Rejected applications are NOT marked tried and
  are re-examined each round until widening.
- Each tried application prints one line (INTER= / INTER2=) and increments
  TRIES. Result == expected ends the query with success. Result >= 0 and
  != expected joins the pool (deduplicated by value). Result -2 joins
  nothing.
- Quiet round (no new tried application AND no new pool value) triggers ONE
  admission-off phase (WIDEN=1 printed once); a second quiet round ends
  the query with ANS=-2 (decline). The round cap (6) also ends the query.
- POOL CAP (frozen source, gen_addval): the pool holds at most 64 values.
  When full, a new value is SILENTLY DROPPED (returns -1, no print, no
  decline, no error). The round continues.
- TRIED2 CAP (frozen source, tried2_add): the 2-input tried table holds at
  most 64 entries. When full, new pairs are SILENTLY NOT RECORDED, so
  tried2_has returns 0 for them next round and they are RE-TRIED every
  subsequent round (INTER2 reprints, TRIES inflates). No crash, no decline.

No new behavior classes, no new opcodes, no new admission/trial/recording
rules are authorized in this battery. The only new code is world setups
and the driver (gs_new.zag). GEN stays FROZEN; this battery characterizes
its boundary, never repairs it.

## 3. Clean failure vs wrong answer (frozen definitions)

Because GEN's end-to-end check only ever emits a value it computed,
"value mismatch" wrong answers are impossible by construction. The live
distinction for this battery is contractual:

- CLEAN FAILURE: the query ends with ANS=-2 (honest decline). The value
  graph provably contained no licensed path to the target within the
  resource bounds, and GEN said so.
- WRONG ANSWER (contract sense): the query ends with ANS=exp where the
  producing application VIOLATED the learned kind contracts, i.e. it was
  admitted only because WIDEN suspended admission. The value matches the
  target, but no contract-licensed composition derives it.

S3 is designed so these two outcomes are mutually exclusive and jointly
exhaustive: exp=207 is unreachable under admission (both 207-yielding
pairs are kind-rejected), a quiet round is forced, and WIDEN fires. If GEN
then emits ANS=207, that is a WRONG ANSWER in the contract sense above;
if it declines, that is CLEAN FAILURE past the widening hatch. Either
outcome maps the exact boundary of GEN's soundness guarantee.

## 4. Opaque naming scheme (frozen; kill bar K8)

Per Micah's critical constraint, no structure, relation, or entity
identifier may carry human domain semantics. The scheme (same as C402):

- Structures: m0..m7 (indices only). Arity is a class property
  (class 4 = 2-input, the frozen generic ADD2; classes 0/1/3 = 1-input).
- Relations: bare integers 91..98.
- Entities: bare integers. Subjects 201..206; objects 211+; small integers
  are computed values (never subjects of any fact, hence kind 2 = NUM).
- Queries: S1, S2, S3, S4, S5.
- Composition shapes are written abstractly, e.g. Z(s) =
  m5(m3(m0(m4(s)), m1(m4(s))), m2(m4(s))). Shape words (chain, fan-out,
  fan-in, DAG) describe composition topology, not domains, and are
  permitted per the C402 precedent.

Forbidden in gs_new.zag, this PREREG, and the REPORT: any noun, verb, or
adjective denoting a human domain or task (the banned class enumerated in
the C402 prereg Section 3). A reader of the frozen worlds must be unable
to tell what "domain" any structure belongs to.

## 5. Frozen worlds (all facts fixed here)

Notation: (s, r, o) facts. m_i = (class, rel). Teaching calls use the base
teach/teach2 (observe/observe2 on success only). Each query runs on a FRESH
world (world_new + setup), so no cross-query contract contamination.

### setup_s1 (S1 SCALE-5): Z(s) = m4(m3(m2(m1(m0(s))))) -- 5-chain

Facts:
  (201,91,211),
  (211,92,212),
  (212,93,213),
  (213,94,214),
  (214,95,215),(214,95,216),
  (231,96,232)
MAPs: m0 = class 0 rel 91; m1 = class 0 rel 92; m2 = class 0 rel 93;
      m3 = class 0 rel 94; m4 = class 1 rel 95; m5 = class 3 (distractor).
Teaching:
  teach(m0,201,211); teach(m1,211,212); teach(m2,212,213);
  teach(m3,213,214); teach(m4,214,2); teach(m5,231,231)
Contracts after teaching:
  m0..m3 in{1} out{1}; m4 in{1} out{2}; m5 in{1} out{1}
Query: s=201, exp=2, nm=6.
Check: m0(201)=211, m1(211)=212, m2(212)=213, m3(213)=214, m4(214)=2.
Five structures, five levels; each round adds exactly one link value.

### setup_s2 (S2 SCALE-6-DAG): Z(s) = m3(m5(m0(m4(s)), m1(m4(s))), m2(m4(s)))

Six structures, four levels, 3-way fan-out at level 2, two sequential
2-input combiners (m5 intermediate with (NUM,NUM) contract, m3 final with
(NUM,NODE) contract; the id order tries the final combiner first, which
bounds the R4 pair explosion). The (214,95,241) fact exists only to make
214 a fact subject (kind 1 = NODE), which the m3 contract requires; it is
never walked or counted on any query path.
Facts:
  (202,91,211),
  (211,92,221),(211,92,222),(211,92,223),
  (211,93,231),(211,93,232),
  (211,94,214),
  (214,95,241)
MAPs: m0 = class 1 rel 92; m1 = class 1 rel 93; m2 = class 0 rel 94;
      m3 = class 4 (2-input, final); m4 = class 0 rel 91 (stem);
      m5 = class 4 (2-input, intermediate).
Teaching:
  teach(m4,202,211); teach(m0,211,3); teach(m1,211,2); teach(m2,211,214);
  teach2(m5,3,2,5); teach2(m3,5,214,219)
Contracts after teaching:
  m4 in{1} out{1}; m0 in{1} out{2}; m1 in{1} out{2}; m2 in{1} out{1};
  m5 in1{2} in2{2} out{2}; m3 in1{2} in2{1} out{2}
Query: s=202, exp=219, nm=6.
Check: m4(202)=211, m0(211)=3, m1(211)=2, m2(211)=214,
  m5(3,2)=5, m3(5,214)=219.
Collision audit (required for path attribution): pool NUMs are
{3,2,6,5,4,205,217,204,213,216,208,220,207}; m5 (NUM,NUM) sums stay below
12 and never equal 219; m3 (NUM,NODE) sums: the only pair yielding 219
is (5,214) (next-nearest: (6,214)=220, (5,213)=218... 213 is NUM, not
admitted in slot 2; (4,214)=218). 219 is produced exactly once, by the
intended final application, in R4.

### setup_s3 (S3 NEAR-MISS): exp reachable only via a kind-violating pair

Facts:
  (205,91,211),(205,91,212),
  (231,94,232)
MAPs: m0 = class 1 rel 91; m1 = class 4 (2-input); m2 = class 3 (distractor).
Teaching:
  teach(m0,205,2); teach2(m1,205,205,410); teach(m2,231,231)
Contracts after teaching:
  m0 in{1} out{2}; m1 in1{1} in2{1} out{2}; m2 in{1} out{1}
Query: s=205, exp=207, nm=3.
The only pairs yielding 207 from the reachable pool {205, 2, 410} are
(205,2) [kinds (1,2): slot 2 violates in2{1}] and (2,205) [kinds (2,1):
slot 1 violates in1{1}]. Under admission 207 is unreachable. R2 is
provably quiet (all candidate applications either already tried or
kind-rejected; no new pool values), so WIDEN=1 fires. R3 runs with
admission suspended. Predicted per the frozen rules: m1(205,2)=207 is
tried in R3 and ends the query with ANS=207, a contract-violating
success (WRONG ANSWER in the Section 3 contract sense).

### setup_s4 (S4 ROUND-CAP): Z(s) = m6(m5(m4(m3(m2(m1(m0(s))))))) -- 7-chain

Seven structures, seven levels; the value path needs 7 rounds, one more
than the frozen cap of 6.
Facts:
  (201,91,211),
  (211,92,212),
  (212,93,213),
  (213,94,214),
  (214,95,215),
  (215,96,216),
  (216,97,221),(216,97,222),
  (231,98,232)
MAPs: m0 = class 0 rel 91; m1 = class 0 rel 92; m2 = class 0 rel 93;
      m3 = class 0 rel 94; m4 = class 0 rel 95; m5 = class 0 rel 96;
      m6 = class 1 rel 97; m7 = class 3 (distractor).
Teaching:
  teach(m0,201,211); teach(m1,211,212); teach(m2,212,213);
  teach(m3,213,214); teach(m4,214,215); teach(m5,215,216);
  teach(m6,216,2); teach(m7,231,231)
Contracts after teaching:
  m0..m5 in{1} out{1}; m6 in{1} out{2}; m7 in{1} out{1}
Query: s=201, exp=2, nm=8.
Check: the full path m6(m5(...m0(201)...)) = m6(216) = 2 is valid, but 216
is produced in R6 and m6 never gets a round to consume it. Every round is
productive (8 new tried applications and one new pool value per round),
so no quiet round and no WIDEN. Predicted: clean decline ANS=-2 at the
round cap.

### setup_s5 (S5 POOL-CAP): (NUM,NUM) combiner over a quadratically growing pool

Facts:
  (201,91,211),(201,91,212),
  (201,92,221),(201,92,222),(201,92,223),
  (231,93,232)
MAPs: m0 = class 1 rel 91; m1 = class 1 rel 92; m2 = class 4 (2-input);
      m3 = class 3 (distractor).
Teaching:
  teach(m0,201,2); teach(m1,201,3); teach2(m2,2,3,5); teach(m3,231,231)
Contracts after teaching:
  m0 in{1} out{2}; m1 in{1} out{2}; m2 in1{2} in2{2} out{2}; m3 in{1} out{1}
Query: s=201, exp=999999 (unattainable by construction: the maximum
reachable pair sum within 6 rounds is 192), nm=4.
Growth accounting (frozen rules): R1 pool {201,2,3} (3 tries); R2 adds
{4,5,6} (4 tries, tried2=4); R3 adds {7..12} (21 new tries, tried2=25,
pool=12); R4 adds {13..24} (96 new tries; tried2 records 39 more then
caps at 64, 57 pairs unrecorded; pool=24); R5 adds {25..48} (465 new
tries, all unrecorded; pool=48); R6: 2145 new tries (2209 pairs minus 64
recorded); new sums {49..96} but the pool caps at 64, so exactly 16 are
added and the rest are silently dropped. No round is quiet (tries and
pool growth every round), so WIDEN never fires. Predicted: ANS=-2,
TRIES=2734, honest decline with the pool cap and the tried2 retry leak
both exercised.

## 6. Frozen predictions (exact stdout, 3/3 byte-identical)

Driver order: S1, S2, S3, S4, S5, one o_flush at end. Derivations follow
the frozen GEN rules of Section 2 (admission per observed kind; id order;
lex pair order; round snapshots; rejected-not-tried; pool cap 64 silent;
tried2 cap 64 with retry leak).

### S1 (s=201, exp=2, nm=6) -- predicted PASS (GEN scales to 5-chain)

R1: pool=[201]. m0: 211. m1..m4: -2. m5: 201 dup.
R2: pool=[201,211]. m0 on 211: -2. m1: 212. m2..m4: -2. m5: 211 dup.
R3: pool=[201,211,212]. m2: 213. rest -2/dup.
R4: pool=[201,211,212,213]. m3: 214. rest -2/dup.
R5: pool=[201,211,212,213,214]. m0..m3 on 214: -2. m4 on 214: 2 = exp
SUCCESS (m5 never reached in R5).
```
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=201
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=2
ARM=GEN PROB=S1 ANS=2 TRIES=29
```

### S2 (s=202, exp=219, nm=6) -- predicted PASS (GEN scales to 6-structure DAG)

R1: pool=[202]. m0: -2. m1: -2. m2: -2. m4: 211. m3/m5: (0,0) rejected.
R2: pool=[202,211]. m0: 3. m1: 2. m2: 214. m4 on 211: -2. m3/m5 pairs
all rejected.
R3: pool=[202,211,3,2,214]. m0 on 214: -2. m1 on 214: -2. m2 on
3,2,214: -2,-2,-2. m4 on 3,2,214: -2,-2,-2. m3 (final, in1{2} in2{1}):
(2,0): 205 add; (2,1): 214 dup; (2,4): 217 add; (3,0): 204 add;
(3,1): 213 add; (3,4): 216 add. m5 (inter, NUM,NUM): (2,2): 6 add;
(2,3): 5 add; (3,2): 5 dup; (3,3): 4 add.
R4: pool=[202,211,3,2,214,6,5,4,205,217,204,213,216]. 1-input MAPs: m2/m4
on the 8 new NUMs: -2 each (16 tries); m0/m1: all rejected. m3: (5,0):
208 add; (5,1): 217 dup; (5,4): 220 add; (6,0): 207 dup; (6,1): 216 dup;
(6,4): 219 = exp SUCCESS (m5 never reached in R4).
```
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=3
INTER=2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER2=205
INTER2=214
INTER2=217
INTER2=204
INTER2=213
INTER2=216
INTER2=6
INTER2=5
INTER2=5
INTER2=4
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER2=208
INTER2=217
INTER2=220
INTER2=207
INTER2=216
INTER2=219
ARM=GEN PROB=S2 ANS=219 TRIES=48
```

### S3 (s=205, exp=207, nm=3) -- predicted BOUNDARY (contract-violating success)

R1: pool=[205]. m0: 2 add. m2: 205 dup. m1: (0,0) admitted (1,1): 410 add.
R2: pool=[205,2,410]. m0/m2: new indices kind-rejected. m1: (0,0) tried;
all 8 other pairs kind-rejected. nt and nv unchanged: QUIET round 1 ->
WIDEN=1 printed (admission suspended from here on).
R3: admission off. m0 on 2, 410: -2, -2. m2 on 2, 410: 2 dup, 410 dup.
m1: (0,1) now admitted: 205+2=207 = exp SUCCESS.
```
INTER=2
INTER=205
INTER2=410
WIDEN=1
INTER=-2
INTER=-2
INTER=2
INTER=410
INTER2=207
ARM=GEN PROB=S3 ANS=207 TRIES=8
```
Interpretation (frozen before results): this is the WRONG ANSWER outcome
in the Section 3 contract sense. m1's learned contract is in1{1}
in2{1}; the success path m1(205,2) feeds a NUM into slot 2. GEN does not
fail cleanly on this near-miss: the widening hatch suspends kind
checking and a value coincidence (205+2=207) is accepted as the answer.
The boundary mapped: GEN's decline-soundness holds only while admission
is active.

### S4 (s=201, exp=2, nm=8) -- predicted CLEAN DECLINE at the round cap

R1: pool=[201]. m0: 211; m1..m6: -2; m7: 201 dup. (8 tries)
R2: pool=[201,211]. m1: 212; rest -2/dup. (8 tries)
R3: m2: 213. (8 tries)
R4: m3: 214. (8 tries)
R5: m4: 215. (8 tries)
R6: m5: 216. (8 tries)
The round loop ends after R6; m6 never consumes 216. Every round added 8
tried applications and one pool value, so no quiet round and no WIDEN.
```
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=201
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=211
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=213
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=215
INTER=-2
INTER=-2
INTER=214
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=216
INTER=-2
INTER=215
ARM=GEN PROB=S4 ANS=-2 TRIES=48
```

### S5 (s=201, exp=999999, nm=4) -- predicted CLEAN DECLINE under cap load

R1: INTER=2, INTER=3, INTER=201 (3 tries). m2: (0,0) rejected.
R2: m2: INTER2=4,5,5,6 (4 tries). tried2=4. pool=6.
R3: m2: 21 new tries. tried2=25. pool=12.
R4: m2: 96 new tries (121 pairs minus 25 recorded); tried2 records 39
more then caps at 64 (57 pairs unrecorded). pool=24.
R5: m2: 465 new tries (529 pairs minus 64 recorded; all unrecorded).
pool=48.
R6: m2: 2145 new tries (2209 pairs minus 64 recorded). New sums
{49..96}: the pool caps at 64, so exactly 16 are added and the rest are
silently dropped. Round ends by the round cap.
The 2731 INTER2= lines are not hand-enumerated (combinatorial volume);
the exact TRIES count below plus 3/3 byte-identical determinism is the
checkable bar. Predicted tail:
```
ARM=GEN PROB=S5 ANS=-2 TRIES=2734
```
with exactly 3 INTER= lines (2, 3, 201), exactly 2731 INTER2= lines,
and zero WIDEN=1 lines in the S5 section.

## 7. Frozen kill bars

- K1 UNMODIFIED-MECHANISM: PASS iff (a) ref_gs_base.zag sha256-matches
  d6_base.zag at commit 82732a9e8 (digest in NAMECHECK.md Step 1);
  (b) ref_gs_gen.zag sha256-matches d6_gen.zag at commit 82732a9e8;
  (c) gs_full.zag region diffs are EMPTY (base whole; gen minus main;
  new driver); (d) grep audit: gs_new.zag defines only setup_s1..setup_s5
  + main, uses only pre-existing classes 0/1/3/4, zero new opcodes, zero
  relation-conditional branches outside the setup functions.
- K2 SCALE-5: PASS iff the S1 section prints EXACTLY the Section 6 block
  (ANS=2, TRIES=29, no WIDEN).
- K3 SCALE-6-DAG: PASS iff the S2 section prints EXACTLY the Section 6
  block (ANS=219, TRIES=48, no WIDEN).
- K4 NEAR-MISS: PASS iff the S3 section prints EXACTLY the Section 6
  block (WIDEN=1 present, ANS=207, TRIES=8).
- K5 ROUND-CAP: PASS iff the S4 section prints EXACTLY the Section 6
  block (ANS=-2, TRIES=48, no WIDEN=1 line).
- K6 POOL-CAP: PASS iff the S5 section ends with EXACTLY
  `ARM=GEN PROB=S5 ANS=-2 TRIES=2734`, contains exactly 3 INTER= lines,
  exactly 2731 INTER2= lines, and zero WIDEN=1 lines.
- K7 DETERMINISM: PASS iff 3/3 runs produce byte-identical stdout
  (pairwise cmp); sha256 digests recorded for binary and outputs;
  stderr empty.
- K8 OPAQUE-NAMING: PASS iff the grep audit finds zero banned-vocabulary
  tokens (Section 4) in gs_new.zag, PREREG.md, and REPORT.md, and all
  structures/relations/entities are referenced by index/integer only.

## 8. Verdict mapping (frozen)

- K1 FAIL: BUILD-FAIL (the mechanism was modified to pass; per Micah's
  constraint, no structure-specific handlers and no new mechanism).
- K2 and K3 PASS (with K1): GEN-SCALES. GEN's frozen mechanism covers
  5-structure chains and 6-structure 4-level DAGs with 3-way fan-out and
  sequential 2-input combiners: the C402 generality result extends past
  the 4-structure envelope with no new machinery.
- K2 or K3 FAIL: BOUNDARY-FOUND (SCALE). The verdict names the failing
  shape and the mechanism-level cause; INFORMATIVE, not a battery
  failure. No weakening of bars, no post-hoc world edits.
- K4 PASS: BOUNDARY-FOUND (WIDEN). This is the predicted INFORMATIVE
  outcome either way: if the block matches, GEN's decline-soundness is
  shown to hold only while admission is active; the widening hatch
  suspends kind contracts and a near-miss yields a contract-violating
  success. If the block does NOT match (e.g. GEN declines despite WIDEN),
  the verdict is BOUNDARY-FOUND with the opposite sign and the mechanism
  rule responsible is named.
- K5 PASS: BOUNDARY-FOUND (ROUNDS). GEN is complete only for value paths
  needing at most 6 rounds; a valid 7-round path declines cleanly
  (ANS=-2, no wrong answer, no WIDEN). The round cap is a completeness
  bound, not a soundness hole.
- K6 PASS: BOUNDARY-FOUND (POOL). Both caps characterized under load:
  the 64-value pool cap drops overflow silently (no error, no decline);
  the 64-entry tried2 cap causes unbounded retry inflation (R6 alone
  burns 2145 tries re-attempting unrecorded pairs) with no crash and no
  wrong answer. Wasted work, not unsoundness.
- K7 FAIL (nondeterminism): UNDECIDED; decisive rerun named.
- K8 FAIL: BUILD-FAIL (naming discipline broken).

Overall verdict GEN-STRESS-CHARACTERIZED requires K1, K7, K8 PASS; K2/K3
extend the generality claim; K4/K5/K6 map the boundary whether the
mechanism holds or breaks, exactly as preregistered.

## 9. Honest boundaries (pre-declared)

- Behaviors installed as previously-learned MAPs (canonical standing);
  expected-answer verification of acceptance (canonical boundary).
- GEN is researcher-implemented (C380 boundary B3 holds): the claim is
  only that a GENERAL extension of U's principles exists and where its
  boundary lies, not that a learner invented it.
- Exactly one generic 2-input class (ADD2, ISA-level addition) is used,
  as authorized in C402 boundary B1. No other new classes or opcodes.
- S5's exact INTER2 listing is not hand-enumerated; the bar is the exact
  TRIES count (2734), exact line counts, absence of WIDEN, and 3/3
  byte-identical determinism.
- S2's (214,95,241) fact exists solely to fix 214's observed kind to NODE
  (the m3 contract requires in2{1}); it is never on any query path.
- The dual-2-input-combiner DAG (S2) answers the C402 Section 8 open
  item: it is testable with the single ADD2 class once sum collisions
  are engineered away via a (NUM,NODE) final contract.

## 10. Implementation plan (frozen order)

1. ref_gs_base.zag, ref_gs_gen.zag: byte-copies of the C402
   ref_gg_base.zag / ref_gg_gen.zag (themselves verified copies of
   d6_base.zag / d6_gen.zag at commit 82732a9e8); sha256 must match
   NAMECHECK.md Step 1.
2. gs_new.zag: setup_s1..setup_s5, main() running S1..S5 in that order
   on fresh worlds, single o_flush at end.
3. Assemble: gs_full.zag = ref_gs_base.zag +
   (ref_gs_gen.zag minus main(), stripped via
   sed '/^fn main()i32 {/,$d') + gs_new.zag. Diff each region against
   its reference (must be EMPTY).
4. Compile with the pinned safebin znc; run 3x; sha256; pairwise
   byte-compare; verify each kill bar.
5. REPORT.md with verdict per the Section 8 mapping.

Zag pitfalls (standing, from AGENTS.md): setups are straight-line
fact_add/map_new/teach/teach2 calls (no loops, no nesting); single
preallocated output buffer with cursor helpers and one raw-syscall
flush (in base); no _zag_print for dynamic content; no !(A && B) in
while conditions; no `as *i32` + slice construction. Git via
/usr/bin/git directly (safebin git symlink has the EPERM defect);
explicit pathspec commits only; never git reset on the shared branch;
this lane works on its own branch lane-genstress-20261003.
