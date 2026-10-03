# PREREG: GEN-GENERALITY -- Is GEN General Beyond the Diamond?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.
Worker: gen-generality. Date: 2026-10-03.

## 1. Question

C380 established: U (unified behavior-contract operation, pipeline-only trial
space {singles, ordered pairs}) is defeated by diamond/fan-out, and GEN
(value-graph generalization: rounds over a value pool + observed-kind
checking, frozen design in the C380 prereg Section 4) solves the diamond with
no new mechanism. Verdict: GENERAL-EXTENSION-EXISTS.

Micah's ruling on that result: "The diamond/fan-out failure must trigger
competing GENERAL composition hypotheses, NOT a DIAMOND handler."

This battery tests whether GEN is genuinely general or a diamond-shaped
patch in disguise. Four probes, each a composition shape GEN has never been
tested on:

- Q1 FAN-IN: two structures' outputs converge into one downstream structure
  (convergent; the dual of the diamond's divergence).
- Q2 DAG-4: a 4-structure DAG (stem feeding a diamond: neither a linear
  pipeline nor a single diamond).
- Q3 CHAIN-3: three 1-input structures chained (pool reuse across 3 rounds).
- Q4a/Q4b PARTIAL: a 2-input structure whose needs are only partially
  satisfied by an upstream structure's output (one slot from the upstream
  output, the other from the query subject itself); Q4b is the honest-decline
  companion (expected answer unattainable).

If GEN handles all four with its frozen mechanism, the value-graph extension
is general across composition shapes. If it fails any, the failure defines
GEN's boundary precisely (INFORMATIVE either way, per the task brief).

## 2. The mechanism under test (frozen, unmodified)

GEN is d6_gen.zag at commit 82732a9e8 (digest in NAMECHECK.md Step 1),
unchanged. Recap of the frozen rules:

- Value pool seeded with the query subject; each pool value carries its
  observed kind (pkind: 1 = NODE, 2 = NUM) and provenance (producing MAP and
  input indices).
- Rounds (cap 6): per round, every MAP in id order (1-input MAPs, then
  2-input MAPs) is applied to every pool value present at round start (pool
  order; 2-input MAPs over all (i,j) pairs in lex order), skipping
  already-tried applications.
- Admission (compatibility, empty = compatible): 1-input (m,v) admitted iff
  kind(v) in m.inmask; 2-input (m,v1,v2) iff kind(v1) in m.inmask1 and
  kind(v2) in m.inmask2. Rejected applications are NOT marked tried and are
  re-examined each round (until widening).
- Each tried application prints one line (INTER= / INTER2=) and increments
  TRIES. Result == expected ends the query with success (ANS set, provenance
  closure recorded via observe/observe2). Result >= 0 and != expected joins
  the pool (deduplicated by value). Result -2 joins nothing.
- Quiet round (no new tried application AND no new pool value) triggers ONE
  admission-off phase (WIDEN=1); a second quiet round ends the query with
  ANS=-2 (decline). The round cap (6) also ends the query.

No new behavior classes, no new opcodes, no new admission/trial/recording
rules are authorized in this battery. The only new code is world setups and
the driver (gg_new.zag).

## 3. Opaque naming scheme (frozen; kill bar K7)

Per Micah's critical constraint, no structure, relation, or entity identifier
may carry human domain semantics. The scheme:

- Structures: m0, m1, m2, m3 (indices only). Arity is a class property
  (class 4 = 2-input, the frozen generic ADD2; classes 0/1/3 = 1-input).
- Relations: bare integers 91, 92, 93, 94.
- Entities: bare integers. Subjects 201..206; objects 211+; small integers
  are computed values (never subjects of any fact, hence kind 2 = NUM).
- Queries: Q1, Q2, Q3, Q4a, Q4b.
- Composition shapes are written abstractly, e.g. Z(s) = m2(m0(s), m1(s)).
  Shape words (fan-in, fan-out, DAG, chain, partial) describe composition
  topology, not domains, and are permitted.

Forbidden in gg_new.zag, this PREREG's world descriptions, and the REPORT:
any noun, verb, or adjective denoting a human domain or task (examples of the
banned class: worker, team, shipment, depot, navigation, arithmetic,
planning, causal, grammar, language, audio, image, and their cognates).
A reader of the frozen worlds must be unable to tell what "domain" any
structure belongs to. The K7 audit is a grep over the new files.

## 4. Frozen worlds (all facts fixed here)

Notation: (s, r, o) facts. m_i = (class, rel). Teaching calls use the base
teach/teach2 (observe/observe2 on success only).

### setup_g1 (Q1 FAN-IN): Z(s) = m2(m0(s), m1(s))

Facts:
  (201,91,211),(201,91,212),(201,91,213),
  (201,92,221),(201,92,222),
  (231,93,232)
MAPs: m0 = class 1 rel 91; m1 = class 1 rel 92; m2 = class 4 (2-input);
      m3 = class 3 (distractor).
Teaching:
  teach(m0,201,3); teach(m1,201,2); teach2(m2,3,2,5); teach(m3,231,231)
Contracts after teaching:
  m0 in{1} out{2}; m1 in{1} out{2}; m2 in1{2} in2{2} out{2}; m3 in{1} out{1}
Query: s=201, exp=5. Check: m0(201)=3, m1(201)=2, m2(3,2)=5.

### setup_g2 (Q2 DAG-4): Z(s) = m2(m0(m3(s)), m1(m3(s)))

Facts:
  (203,93,211),
  (211,91,212),(211,91,213),(211,91,214),
  (211,92,221),(211,92,222)
MAPs: m0 = class 1 rel 91; m1 = class 1 rel 92; m2 = class 4 (2-input);
      m3 = class 0 rel 93.
Teaching:
  teach(m3,203,211); teach(m0,211,3); teach(m1,211,2); teach2(m2,3,2,5)
Contracts after teaching:
  m0 in{1} out{2}; m1 in{1} out{2}; m2 in1{2} in2{2} out{2}; m3 in{1} out{1}
Query: s=203, exp=5. Check: m3(203)=211, m0(211)=3, m1(211)=2, m2(3,2)=5.
Shape: a stem (m3) feeding a diamond (m0,m1 fan-out from 211, m2 combine).
Four structures, three levels; not a pipeline, not a single diamond.

### setup_g3 (Q3 CHAIN-3): Z(s) = m2(m1(m0(s)))

Facts:
  (204,91,212),
  (212,92,213),
  (213,93,221),(213,93,222),
  (231,94,232)
MAPs: m0 = class 0 rel 91; m1 = class 0 rel 92; m2 = class 1 rel 93;
      m3 = class 3 (distractor).
Teaching:
  teach(m0,204,212); teach(m1,212,213); teach(m2,213,2); teach(m3,231,231)
Contracts after teaching:
  m0 in{1} out{1}; m1 in{1} out{1}; m2 in{1} out{2}; m3 in{1} out{1}
Query: s=204, exp=2. Check: m0(204)=212, m1(212)=213, m2(213)=2.
Requires pool reuse across 3 rounds (212 added round 1, 213 round 2).

### setup_g4 (Q4a/Q4b PARTIAL): Z(s) = m1(s, m0(s))

Facts:
  (205,91,211),(205,91,212),
  (205,92,213),
  (231,94,232)
MAPs: m0 = class 1 rel 91; m1 = class 4 (2-input); m2 = class 0 rel 92;
      m3 = class 3 (distractor).
Teaching:
  teach(m0,205,2); teach(m2,205,213); teach2(m1,205,2,207); teach(m3,231,231)
Contracts after teaching:
  m0 in{1} out{2}; m1 in1{1} in2{2} out{2}; m2 in{1} out{1}; m3 in{1} out{1}
Q4a: s=205, exp=207. Check: m0(205)=2, m1(205,2)=207. The upstream structure
m0 satisfies exactly one of m1's two input slots (slot 2, NUM); slot 1
(NODE) is satisfied by the query subject itself from the pool seed. This is
the operational meaning of "partial applicability" here.
Q4b: s=205, exp=999 (unattainable by construction: all reachable sums are
< 999 until round 6 exceeds it; 999 itself is never produced). Honest decline
(ANS=-2) is the predicted correct behavior: GEN must not force-fit.

Each query runs on a FRESH world (world_new + setup), so no cross-query
contract contamination.

## 5. Frozen predictions (exact stdout, 3/3 byte-identical)

Driver order: Q1, Q2, Q3, Q4a, Q4b, one o_flush at end. Derivations follow
the frozen GEN rules of Section 2 (admission per observed kind; lex order;
round snapshots; rejected-not-tried).

### Q1 (s=201, exp=5, nm=4)

R1: pool=[201]. m0: 3 (INTER=3, add). m1: 2 (INTER=2, add). m3: 201
(INTER=201, dup). m2: (0,0) rejected (slot1 kind 1 vs in1{2}).
R2: pool=[201,3,2]. m0/m1/m3: indices 1,2 kind-rejected. m2: (0,0),(0,1),
(0,2),(1,0) rejected; (1,1): 6 (INTER2=6, add); (1,2): 5 = exp SUCCESS.
```
INTER=3
INTER=2
INTER=201
INTER2=6
INTER2=5
ARM=GEN PROB=Q1 ANS=5 TRIES=5
```

### Q2 (s=203, exp=5, nm=4)

R1: pool=[203]. m0: -2 (INTER=-2). m1: -2 (INTER=-2). m3: 211 (INTER=211,
add). m2: (0,0) rejected.
R2: pool=[203,211]. m0 on 211: 3 (INTER=3, add). m1 on 211: 2 (INTER=2,
add). m3 on 211: -2 (INTER=-2). m2: all four pairs kind-rejected.
R3: pool=[203,211,3,2]. 1-input MAPs: nothing new admittable. m2: (2,2): 6
(INTER2=6, add); (2,3): 5 = exp SUCCESS.
```
INTER=-2
INTER=-2
INTER=211
INTER=3
INTER=2
INTER=-2
INTER2=6
INTER2=5
ARM=GEN PROB=Q2 ANS=5 TRIES=8
```

### Q3 (s=204, exp=2, nm=4)

R1: pool=[204]. m0: 212 (INTER=212, add). m1: -2 (INTER=-2). m2: -2
(INTER=-2). m3: 204 (INTER=204, dup).
R2: pool=[204,212]. m0 on 212: -2 (INTER=-2). m1 on 212: 213 (INTER=213,
add). m2 on 212: -2 (INTER=-2). m3 on 212: 212 (INTER=212, dup).
R3: pool=[204,212,213]. m0 on 213: -2 (INTER=-2). m1 on 213: -2 (INTER=-2).
m2 on 213: 2 = exp SUCCESS (m3 never reached in R3).
```
INTER=212
INTER=-2
INTER=-2
INTER=204
INTER=-2
INTER=213
INTER=-2
INTER=212
INTER=-2
INTER=-2
INTER=2
ARM=GEN PROB=Q3 ANS=2 TRIES=11
```

### Q4a (s=205, exp=207, nm=4)

R1: pool=[205]. m0: 2 (INTER=2, add). m2: 213 (INTER=213, add). m3: 205
(INTER=205, dup). m1: (0,0) rejected (slot2 kind 1 vs in2{2}).
R2: pool=[205,2,213]. m0: idx1 kind-rejected, idx2: -2 (INTER=-2). m2: idx1
rejected, idx2: -2 (INTER=-2). m3: idx1 rejected, idx2: 213 (INTER=213,
dup). m1: (0,0) rejected; (0,1): kinds (1,2) admitted: 207 = exp SUCCESS
((2,1) never reached).
```
INTER=2
INTER=213
INTER=205
INTER=-2
INTER=-2
INTER=213
INTER2=207
ARM=GEN PROB=Q4a ANS=207 TRIES=7
```

### Q4b (s=205, exp=999, nm=4)

R1: as Q4a R1 (3 tries). pool=[205,2,213].
R2: m0/m2/m3 as Q4a R2 (3 tries). m1: (0,1): 207 (INTER2=207, add);
(2,1): 215 (INTER2=215, add). pool=[205,2,213,207,215].
R3: m1 new admitted: (0,3): 412, (0,4): 420, (2,3): 420, (2,4): 428
(4 tries). pool adds 412,420,428.
R4: m1 new admitted: (0,5): 617, (0,6): 625, (0,7): 633, (2,5): 625,
(2,6): 633, (2,7): 641 (6 tries). pool adds 617,625,633,641.
R5: m1 new admitted: (0,8): 822, (0,9): 830, (0,10): 838, (0,11): 846,
(2,8): 830, (2,9): 838, (2,10): 846, (2,11): 854 (8 tries).
pool adds 822,830,838,846,854.
R6: m1 new admitted: (0,12): 1027, (0,13): 1035, (0,14): 1043, (0,15):
1051, (0,16): 1059, (2,12): 1035, (2,13): 1043, (2,14): 1051, (2,15):
1059, (2,16): 1067 (10 tries). Round cap reached; query ends.
No round is quiet (new values every round), so WIDEN never fires.
999 is never produced (sums pass from 854 to 1027). ANS stays -2.
```
INTER=2
INTER=213
INTER=205
INTER=-2
INTER=-2
INTER=213
INTER2=207
INTER2=215
INTER2=412
INTER2=420
INTER2=420
INTER2=428
INTER2=617
INTER2=625
INTER2=633
INTER2=625
INTER2=633
INTER2=641
INTER2=822
INTER2=830
INTER2=838
INTER2=846
INTER2=830
INTER2=838
INTER2=846
INTER2=854
INTER2=1027
INTER2=1035
INTER2=1043
INTER2=1051
INTER2=1059
INTER2=1035
INTER2=1043
INTER2=1051
INTER2=1059
INTER2=1067
ARM=GEN PROB=Q4b ANS=-2 TRIES=36
```
(Total INTER/INTER2 lines = 36 = TRIES; pool peaks at 23 < 64 cap;
tried2 entries peak at 30 < 64 cap.)

## 6. Frozen kill bars

- K1 UNMODIFIED-MECHANISM: PASS iff (a) ref_gg_base.zag sha256-matches
  d6_base.zag at commit 82732a9e8 (digest in NAMECHECK.md Step 1);
  (b) ref_gg_gen.zag sha256-matches d6_gen.zag at commit 82732a9e8;
  (c) gg_full.zag region diffs are EMPTY (base whole; gen minus main;
  new driver); (d) grep audit: zero new behavior classes, zero new
  opcodes, zero relation-conditional branches outside the setup
  functions.
- K2 FAN-IN: PASS iff Q1 prints EXACTLY the Section 5 block
  (ANS=5, TRIES=5, no WIDEN).
- K3 DAG-4: PASS iff Q2 prints EXACTLY the Section 5 block
  (ANS=5, TRIES=8, no WIDEN).
- K4 CHAIN-3: PASS iff Q3 prints EXACTLY the Section 5 block
  (ANS=2, TRIES=11, no WIDEN).
- K5 PARTIAL: PASS iff Q4a prints EXACTLY the Section 5 block
  (ANS=207, TRIES=7) AND Q4b prints EXACTLY the Section 5 block
  (ANS=-2, TRIES=36, no WIDEN=1 line).
- K6 DETERMINISM: PASS iff 3/3 runs produce byte-identical stdout
  (pairwise cmp); sha256 digests recorded for binary and outputs.
- K7 OPAQUE-NAMING: PASS iff the grep audit finds zero banned-vocabulary
  tokens (Section 3) in gg_new.zag, PREREG.md, and REPORT.md, and all
  structures/relations/entities are referenced by index/integer only.

## 7. Verdict mapping (frozen)

- K1 FAIL: BUILD-FAIL (the mechanism was modified to pass; per Micah's
  constraint, no structure-specific handlers and no new mechanism).
- K2-K5 all PASS (+K1, K6, K7 PASS): GEN-GENERAL. GEN's value-graph
  extension covers fan-in, 4-structure DAG, 3-chain, and partial
  applicability with no new mechanism: the diamond was a trial-space
  limitation with a general fix, not a shape-specific patch.
- Any of K2-K5 FAIL: BOUNDARY-FOUND. The verdict names the failing shape
  and the mechanism-level cause (which GEN rule fails to cover it); this
  is INFORMATIVE, not a failure of the battery. No weakening of bars, no
  post-hoc world edits to force a pass.
- K6 FAIL (nondeterminism): UNDECIDED; decisive rerun named.
- K7 FAIL: BUILD-FAIL (naming discipline broken; the test no longer
  evidences domain-blindness).

## 8. Honest boundaries (pre-declared)

- Behaviors installed as previously-learned MAPs (canonical standing);
  expected-answer verification of acceptance (canonical boundary).
- GEN is researcher-implemented (C380 boundary B3 holds): the claim is
  only that a GENERAL extension of U's principles exists and covers
  these shapes, not that a learner invented it.
- Exactly one generic 2-input class (ADD2, ISA-level addition) is used,
  as authorized in C380 boundary B1. No other new classes or opcodes.
- Q4b exercises the round cap (6) as the termination bound: GEN's
  soundness (decline, never a wrong answer) is shown, but the
  combinatorics of an unsatisfiable value graph are noted, not solved
  (C380 boundary B5 holds).
- The dual-2-input-combiner DAG variant (e.g. Z = m3(m2(m0(s),m1(s)),
  m0(s))) was considered and REJECTED as a world design: with a single
  ADD2 class, small-integer sums collide (m2(3,5)=8 vs m3(5,3)=8),
  confounding path attribution. Testing it cleanly needs a second
  generic 2-input class, which is a base extension requiring its own
  prereg, not smuggled in here.
- Q4a's "partial" reading: the upstream structure satisfies exactly one
  input slot; the other slot is satisfied by the pool-seeded subject.
  Other readings of partial applicability (e.g. kind-mismatched slots,
  multi-value shortfall) are not covered here.

## 9. Implementation plan (frozen order)

1. ref_gg_base.zag, ref_gg_gen.zag: byte-copies of d6_base.zag /
   d6_gen.zag at commit 82732a9e8 (sha256 must match NAMECHECK.md Step 1).
2. gg_new.zag: setup_g1..setup_g4, main() running Q1/Q2/Q3/Q4a/Q4b in
   that order on fresh worlds, single o_flush at end.
3. Assemble: gg_full.zag = ref_gg_base.zag +
   (ref_gg_gen.zag minus main()) + gg_new.zag, via sed region-strip
   and cat. Diff each region against its reference (must be EMPTY).
4. Compile with the pinned safebin znc; run 3x; sha256; pairwise
   byte-compare.
5. REPORT.md with verdict per the Section 7 mapping.

Zag pitfalls (standing, from AGENTS.md): u8-backed z_alloc (in base);
single preallocated output buffer with cursor helpers and one raw-syscall
flush (in base); no _zag_print for dynamic content; if-nesting at most 3
(driver has at most 3); no !(A && B) in while conditions; no `as *i32` +
slice construction; FIFTH defect noted (not used here). Git via
/usr/bin/git directly (safebin git symlink has the EPERM defect);
explicit pathspec commits only; never git reset on the shared branch.
