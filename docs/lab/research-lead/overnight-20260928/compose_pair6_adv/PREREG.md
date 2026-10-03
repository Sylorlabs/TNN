# PREREG: COMPOSE-PAIR6-ADV -- Does Diamond (Fan-Out) Defeat the Unified Composition Operation U?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Step 0) strictly precedes all implementation.
Worker: compose-pair6-adv. Date: 2026-10-02.

## 1. Question

The unified behavior-contract operation U (COMPOSE-COLLAPSE C319 verdict
SUBSUMPTION; 5th-pair transfer C368 BUILD-PASS) composes linear pipelines:
singles, then ordered pairs (A,B) = B(A(s)). The task describes a critical
finding: **diamond (fan-out) defeats U**, where one structure's output must
feed TWO downstream structures, whose results are then joined.

Key question (frozen): is fan-out a FUNDAMENTAL limitation of the
behavior-contract operation, or does a GENERAL extension of U's principles
cover it? A negative result that precisely defines U's generality boundary is
INFORMATIVE-FAIL territory and is the primary deliverable.

## 2. Background: the unified operation U (frozen, from C319/C368)

Each MAP carries a CONTRACT: observed (input-kind, output-kind) sets as
bitmasks (bit0=NODE, bit1=NUM); empty set = compatible with all. ONE admission
rule, always on: single A admitted iff kin compatible with A.inmask and kout
with A.outmask; pair (A,B), A!=B, admitted iff kin compatible with A.inmask,
A.outmask INTERSECTS B.inmask, kout compatible with B.outmask. ONE execution
rule: ordered trial (admitted singles in MAP-id order, then admitted pairs in
(a,b) id order) with end-to-end verification (result == expected); stage-1
intermediates logged as INTER=. WIDENING: on exhaustive admitted failure,
retry filter-rejected pairs once, log WIDEN=1. Successful trials record kind
observations (contract growth). No modes, no flags. All computation is over
1-input/1-output MAP applications: exec_map(A,m,s) -> value.

Structural fact (frozen): U's trial space is {singles} union {ordered pairs}.
Its contracts are (inmask, outmask): one input kind-set, one output kind-set.
Its execution computes exactly one intermediate per pair trial.

## 3. The diamond test (frozen worlds)

Domain: worker/team/task scheduling (fresh relations 91/92/94; new entities).
The target is a fan-out with a join:

  Z(w) = G(Y(X(w)), W(X(w)))

  X = WALK(91): worker -> team (NODE->NODE)
  Y = COUNT(92): team -> pending-task count (NODE->NUM)
  W = COUNT(94): team -> completed-task count (NODE->NUM)
  G = ADD2: (NUM,NUM) -> NUM (generic 2-input addition; see boundary B1)

Facts (frozen):
  (201,91,211),(202,91,211),(203,91,212),(204,91,212),
  (211,92,901),(211,92,902),(211,92,903),
  (212,92,904),(212,92,905),
  (211,94,911),(211,94,912),
  (212,94,913)

MAP inventory (4 MAPs): m0=X class0 rel91; m1=Y class1 rel92; m2=W class1
rel94; m3=G class4 (2-input ADD2).

Q1 (kind-representative teaching). teach calls:
  teach(m0,201,211); teach(m0,203,212);
  teach(m1,211,3); teach(m1,212,2);
  teach(m2,211,2); teach(m2,212,1);
  teach2(m3,3,2,5); teach2(m3,2,1,3)
Contracts after teaching: m0 in{1} out{1}; m1 in{1} out{2}; m2 in{1} out{2};
m3 inmask1{2} inmask2{2} outmask{2}.
Sealed query: s=202, kin=1, kout=2, expected=5.
Check: X(202)=211; Y(211)=3; W(211)=2; G(3,2)=5. Correct answer 5.

Q2 (misleading teaching, P2b-style discriminator for the extension's
widening). Same facts and inventory. Teaching identical except:
  teach2(m3,211,212,423)
so m3's contract is inmask1{1} inmask2{1} outmask{2} (non-representative of
the sealed join (3,2), both NUM). Sealed query: s=202, kin=1, kout=2,
expected=5.

Why U must fail Q1 (frozen analysis): U tries admitted singles
(Y: -2; W: -2; G 1-input: -2; X rejected by kout) then admitted ordered pairs
(7: (X,Y)->3, (X,W)->2, (X,G)->-2, (Y,G),(W,G),(G,Y),(G,W) all v1=-2), then
WIDEN=1 and the 5 rejected pairs (all v1=-2). No single or ordered pair
evaluates to 5; the fork (X feeding both Y and W) and the 2-input join are
outside U's trial space and outside its 1-in/1-out execution. Predicted:
ANS=-2, TRIES=15, WIDEN=1.

## 4. Candidate general extension GEN (frozen design)

GEN generalizes U's trial space from {singles, ordered pairs} to ITERATED
N-ARY APPLICATION OVER A VALUE POOL, keeping every U principle:

- Contracts: per-MAP kind-sets; 2-input MAPs carry (inmask1, inmask2,
  outmask). Learned from teaching executions (observe / observe2) and grown
  by success-recording, exactly as in U.
- Admission (same compatibility rule k_has, empty = compatible with all):
  a 1-input application (m, v) is admitted iff kind(v) is compatible with
  m.inmask; a 2-input application (m, v1, v2) iff kind(v1)~m.inmask1 and
  kind(v2)~m.inmask2. The pair handshake (A.out INTERSECTS B.in, a
  PREDICTION) is replaced by OBSERVED-kind checking: stage 1 actually
  executes, and stage 2 admission tests the observed intermediate's kind.
  This is strictly more informed, never less.
- Trial order (deterministic, U-consistent): round-based. Round r applies
  every MAP (id order; 1-input MAPs, then 2-input MAPs) to every value
  present at round start (pool order), skipping already-tried applications.
  Round 1 = U's singles; round 2 = U's pairs as a subset (plus same-MAP
  re-application, e.g. X(X(s)), which U excludes by x!=y; harmless
  superset). New values (kind-probed, provenance-recorded) join the pool
  for the next round. Round cap 6, pool cap 64 (frozen anti-explosion
  bounds; never binding in these tests).
- Verification: end-to-end, result == expected, exactly as U. Intermediate
  results logged as INTER= (1-input) / INTER2= (2-input).
- Widening (generalized): when a full round adds no new tried application
  and no new value (fixpoint) without success, enter ONE admission-off
  phase (log WIDEN=1 once): retry every untried application with admission
  ignored, in the same deterministic order, until fixpoint or success.
  Triggered solely by learner-observed exhaustive failure, as in U.
- Success-recording (generalized via provenance): each pool value records
  its producing application (m, input indices). On success, observe every
  application in the dependency closure (the success app plus, recursively,
  the producers of its inputs), using observe/observe2 with the actual
  input/output values. For chains this reduces exactly to U's recording.
- Arity is a class property (class 4 = 2-input; classes 0-3 = 1-input),
  like rel2 for MAYBE. No modes, no flags, no domain handlers, no
  diamond-specific code: the fork (X's output feeding Y and W) EMERGES
  because the computed value stays in the pool and is consumable by any
  MAP. Chains of length 3+, multi-forks, and wider joins are covered by
  the same rule with no new templates.

What GEN deliberately does NOT preserve: U's outmask/kout pair-handshake
prediction (subsumed by observed-kind checking); outmask remains learned
contract state (census-visible, grown by recording) but does not gate
pool expansion. This delta is stated, not smuggled (see verdict mapping).

## 5. Frozen predictions (exact stdout, 3/3 byte-identical per binary)

### Arm UNI-D (d6_uni: U's composer functions byte-identical to frozen
ref_uc_uni.zag; base = ref_uc_base.zag plus the allowlisted 2-input support
in Section 7; main runs the collapse battery P1/P2a/P2b/P3/P5 then Q1)

P1/P2a/P2b/P3/P5 section: BYTE-IDENTICAL to
docs/lab/research-lead/overnight-20260928/compose_collapse/uni_run1.txt
(18 lines; K1 verifies by head -n 18 diff).

Q1 section (frozen):
```
INTER=211
INTER=211
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=-2
WIDEN=1
INTER=-2
INTER=-2
INTER=-2
INTER=-2
INTER=-2
ARM=UNI-D PROB=Q1 ANS=-2 TRIES=15
```
Derivation: singles Y(202),W(202),G(202) fail (3 tries); admitted pairs in
(x,y) id order: (X,Y):211->3, (X,W):211->2, (X,G):211->-2,
(Y,G):-2, (W,G):-2, (G,Y):-2, (G,W):-2 (7 tries, 7 INTER lines); WIDEN=1;
rejected pairs (Y,X),(Y,W),(W,X),(W,Y),(G,X): all v1=-2 (5 tries, 5 INTER
lines). Total TRIES=15, ANS=-2.

### Arm GEN (d6_gen: GEN composer on the same base; main runs P1/P2a/P2b/P3,
Q1, Q2)

P1:
```
INTER=63
INTER=-2
INTER=-2
INTER=65
ARM=GEN PROB=P1 ANS=65 TRIES=4
```
(r1: X(61)=63, Y(61)=-2; r2: X(63)=-2, Y(63)=65.)

P2a:
```
INTER=44
INTER=-2
INTER=41
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P2a ANS=2 TRIES=6
```
(r1: X(41)=44, Y(41)=-2, D1(41)=41, D2(41)=1; r2: X(44)=-2, Y(44)=2.)

P2b:
```
INTER=44
INTER=-2
INTER=41
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P2b ANS=2 TRIES=6
```
(r1 as P2a; r2: X(44) admitted by kin but fails, Y(44) admitted by OBSERVED
kind(44)=NODE compat with Y.in{1}: succeeds with NO widening. Note: U needs
WIDEN=1 here; GEN's observed-kind handshake is strictly more precise than
U's contract-prediction handshake.)

P3:
```
INTER=34
INTER=-2
INTER=31
INTER=1
INTER=-2
INTER=2
ARM=GEN PROB=P3 ANS=2 TRIES=6
```

Q1:
```
INTER=211
INTER=-2
INTER=-2
INTER=-2
INTER=3
INTER=2
INTER2=6
INTER2=5
ARM=GEN PROB=Q1 ANS=5 TRIES=8
```
(r1: X(202)=211, Y(202)=-2, W(202)=-2; G(202,202) rejected by inmask1{2};
r2: X(211)=-2, Y(211)=3, W(211)=2; G combos rejected; r3: 1-input over
{3,2} rejected by kind; 2-input: G(3,3)=6, G(3,2)=5 SUCCESS.)
Recording closure: observe2(G,3,2,5); observe(Y,211,3); observe(W,211,2);
observe(X,202,211).

Q2:
```
INTER=211
INTER=-2
INTER=-2
INTER2=404
INTER=-2
INTER=3
INTER=2
INTER2=413
INTER2=413
INTER2=422
WIDEN=1
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
INTER2=606
INTER2=205
INTER2=204
INTER2=615
INTER2=624
INTER2=615
INTER2=214
INTER2=213
INTER2=624
INTER2=633
INTER2=606
INTER2=615
INTER2=808
INTER2=407
INTER2=406
INTER2=817
INTER2=826
INTER2=205
INTER2=214
INTER2=407
INTER2=6
INTER2=5
ARM=GEN PROB=Q2 ANS=5 TRIES=47
```
(r1: X(202)=211, Y(202)=-2, W(202)=-2, G(202,202)=404 admitted under the
misleading inmask1{1}/inmask2{1} since kind(202)=NODE;
r2: X(211)=-2, Y(211)=3, W(211)=2, G(202,211)=413, G(211,202)=413,
G(211,211)=422; r3: fixpoint (nothing new admittable) -> WIDEN=1; widening:
15 rejected 1-input apps (X/Y/W over {404,3,2,413,422}, all -2), then
22 rejected 2-input apps in lex order until G(3,2)=5. TRIES=4+6+37=47.)
Recording grows G's contract: inmask1 {1}|{2}, inmask2 {1}|{2}.

GEN census after Q1 (informational, predicted):
```
CENSUS m=0 inmask=1 outmask=1 inmask2=0 n=3
CENSUS m=1 inmask=1 outmask=2 inmask2=0 n=3
CENSUS m=2 inmask=1 outmask=2 inmask2=0 n=3
CENSUS m=3 inmask=2 outmask=2 inmask2=2 n=3
```

## 6. Frozen kill bars

- K1 UNI-FAITHFUL: UNI-D's first 18 stdout lines are byte-identical to
  compose_collapse/uni_run1.txt (U's canonical profile reproduced exactly
  on the extended base: the base change is behavior-preserving on the old
  battery). 3/3 byte-identical runs.
- K2 DIAMOND-DEFEAT: UNI-D Q1 prints EXACTLY the 14-line block in
  Section 5 (ANS=-2, TRIES=15, WIDEN=1). 3/3. This is the INFORMATIVE-FAIL:
  U exhausts its whole trial space (singles, admitted pairs, widened
  rejected pairs) and cannot route one intermediate to two consumers or
  apply a 2-input join.
- K3 GEN-DIAMOND: GEN Q1 prints EXACTLY the 9-line block in Section 5
  (ANS=5, TRIES=8). 3/3. Same inventory, same base, same contracts: the
  defeat is isolated to U's trial-space/routing, and the value-graph
  extension covers it with no diamond-specific code.
- K4 GEN-REGRESSION: GEN P1/P2a/P2b/P3 print EXACTLY the blocks in
  Section 5 (ANS 65/2/2/2; TRIES 4/6/6/6). 3/3. The extension does not
  break U's proven ground. (TRIES differ from U's by construction: GEN's
  trial space is a principled superset; ANS must match.)
- K5 GEN-WIDEN: GEN Q2 prints EXACTLY the block in Section 5 (ANS=5,
  TRIES=47, WIDEN=1). 3/3. Failure-triggered widening generalizes to the
  value graph: the misleading contract is detected (fixpoint), routed
  around (admission-off phase), and learned from (inmask growth).
- K6 UNMODIFIED-U-LOGIC: d6_uni.zag's composer region (everything before
  `fn main`) diffed against frozen
  ref_uc_uni.zag's composer region: EMPTY diff. d6_base.zag diffed against
  frozen ref_uc_base.zag: every hunk is in the Section 7 allowlist, each
  with its justification; the P1-P3/P5 replication (K1) independently
  proves behavior preservation. Zero em/en dash bytes in docs; safebin
  guard attested in NAMECHECK.md Step 0; pure Zag.

## 7. Base-change allowlist (frozen; the ONLY permitted diffs vs ref_uc_base.zag)

1. exec_map: one added case `if(cl==4){ return -2; }` before the MAYBE
   fallthrough. Justification: arity-mismatch behavior for the new 2-input
   class; a 1-input application of a 2-input MAP must fail cleanly, not
   fall into MAYBE's walk. Behavior-preserving on all old inventories
   (no class-4 MAP there; proven by K1).
2. New functions (appended): exec_map2 (2-input application; class 4 =
   s1+s2 with -2 propagation; other classes -> -2), m2g/m2p (second-input
   contract table at arena 968, 4 maps x 3 fields), observe2, teach2.
   Justification: the minimal substrate to POSE a fan-out task; no
   composition logic (no admission, trial, widening, or recording rules).
3. New world setups (appended): setup_d1, setup_d2 (facts/MAPs/teaching
   from Section 3 only).
Arena layout for shared regions (facts, MAP table stride 40, tries/found/
ans at 936/940/944, class list) is UNCHANGED. GEN scratch lives at
1024..3916, untouched by U's code paths.

## 8. Verdict mapping (frozen)

- K1 PASS + K2 PASS: INFORMATIVE-FAIL for U on fan-out. U's generality
  boundary is drawn: linear pipelines (singles, ordered pairs) only.
  Fan-out (one intermediate feeding two consumers + n-ary join) defeats
  U's trial space, its 1-in/1-out contract shape, and its 1-in/1-out
  execution. This negative result is the primary deliverable.
- K3 + K4 + K5 PASS: GENERAL-EXTENSION-EXISTS. The value-graph operation
  preserves U's principles (kind-set contracts, compatibility admission,
  deterministic ordered trial, end-to-end verification, failure-triggered
  widening, success-recording with contract growth) while covering
  fan-out, longer chains, and wider joins with no shape templates, no
  modes, no domain handlers. Fan-out is then a trial-space limitation
  with a principled fix, NOT a fundamental limitation of the
  behavior-contract idea. The stated delta (prediction->observation
  handshake; outmask not gating expansion) is the precise characterization
  of the extension.
- K1 FAIL: UNDECIDED (the base port broke U; diagnose before any verdict).
- K2 FAIL (UNI-D solves Q1): hypothesis falsified; verdict NO-DEFEAT
  (investigate which U path solved it; the prereg analysis says none can).
- K3 FAIL + K4 PASS: PARTIAL/FUNDAMENTAL-DEFEAT leaning (extension keeps
  old ground but does not cover fan-out; a genuinely new mechanism is
  indicated).
- K4 FAIL: NEW-MECHANISM-or-UNDECIDED (the extension breaks proven ground;
  it is not an extension of U).
- Build failure or nondeterminism: UNDECIDED, decisive experiment named.

## 9. Honest boundaries (pre-declared)

- B1 (ADD2): posing ANY fan-out-with-join task needs a 2-input behavior;
  without one the test is vacuous. Exactly one generic 2-input arithmetic
  class is authorized (ADD-class is ISA-level machinery per the
  protected-core ruling; domain-neutral, no domain semantics). No other
  new classes, opcodes, or relation-conditional branches.
- B2: behaviors are installed as previously-learned MAPs (behavior
  induction not under test; canonical standing). Expected answers verify
  acceptance (canonical boundary).
- B3: GEN is a researcher-implemented candidate extension, not
  learner-invented. The claim is only that a GENERAL extension of U's
  principles exists, not that the learner discovered it.
- B4: the fork-without-join variant (two consumers, no combiner) and
  chains of length 3+ are not separately tested; GEN covers them by the
  same rule, stated not shown.
- B5: widening-phase search is bounded by the round/pool caps; worst-case
  combinatorics of the value graph are noted, not solved.
- B6: GEN's TRIES are not comparable to U's TRIES (superset trial space);
  only ANS comparability is barred (K4).

## 10. Implementation plan (frozen order)

1. d6_base.zag: copy of frozen ref_uc_base.zag + Section 7 allowlisted
   additions (exec_map class-4 case; exec_map2/m2g/m2p/observe2/teach2;
   setup_d1/setup_d2). Verify diff allowlist.
2. d6_uni.zag: copy of frozen ref_uc_uni.zag with ONLY `fn main`
   replaced (P1/P2a/P2b/P3/P5 replication + Q1). Verify composer-region
   diff EMPTY.
3. d6_gen.zag: GEN composer (Section 4) + main (P1/P2a/P2b/P3/Q1/Q2/
   census). New file; reuses base helpers only.
4. Assemble: cat d6_base.zag d6_uni.zag > uni_full.zag;
   cat d6_base.zag d6_gen.zag > gen_full.zag. Compile with the pinned
   znc (hash 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
   Run 3x each; record sha256 of binaries and outputs.
5. Verify K1-K6; write REPORT.md with the verdict per Section 8 mapping.

Zag pitfalls (standing): no `as *i32` + slice construction in functions
(use z_alloc/get32/set32); no _zag_print for dynamic content (single
preallocated buffer, cursor helpers, one raw-syscall flush; verify stdout
bytes); if-nesting kept shallow (hoist flags; E0204 is loud); no
`!(A && B)` in while conditions (De Morgan); no `[]u8 as *u8` casts.
