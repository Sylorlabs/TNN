# PREREG.md -- COMPOSE-ADVERSARY: sealed worlds for hypotheses A, B, C

Date: 2026-10-03. Worker: COMPOSE-ADVERSARY. Lane:
`docs/lab/research-lead/overnight-20260928/compose_adversary/`.
Branch: `tnn-native-lab`. Task type: NON-LEDGER (claim minting
paused).

Status of everything below: FROZEN. This preregistration freezes
the sealed world designs, the design rationale, the kill bars,
and the sealed evaluation protocol BEFORE any world-builder code
exists. Any deviation requires a prereg amendment committed
before the deviating artifact.

## 1. Adversarial brief

The composition arc produced three hypotheses for one general
composition operation:

- A (BACKCHAIN, COMPOSE-BACKCHAIN-1, BUILD-PASS): lazy
  chronological backtracking with interleaved execution.
  Memoryless.
- B (SUSPEND, COMPOSE-SUSPEND-1, BUILD-PASS): two-phase lazy
  dataflow (ASSEMBLE/EVALUATE/WIDEN/REBIND/REVISE) over
  hash-consed thunks.
- C (LEARN-COMPOSE, COMPOSE-LEARNCOMPOSE-1, BUILD-PASS): A's
  substrate plus a 16-entry learner-owned composition memory
  (retrieve by similarity, injective contract adaptation,
  DROP_UNMAPPED repair, frozen R1-R4 revision, succ/fail +
  NEGREC).

The builders' verdict: complementary, not ranked (A wins
simplicity, B wins efficiency, C wins adaptivity). This
adversary tests that verdict with sealed worlds designed to
(a) falsify each hypothesis at least once, (b) cover fan-out,
fan-in, DAGs, 3/5/10+ structure combinations, partial
applicability, and cycles, (c) find worlds where one hypothesis
clearly dominates, and (d) find worlds where all three fail.

The adversary designs worlds only. Builder code is frozen and
untouched. The adversary does NOT execute any mechanism on the
sealed worlds; that is reserved for the independent sealed
evaluation.

## 2. Frozen mechanism bounds relied upon

All bounds below are read from the builders' frozen source
(preregistered here so the predictions are auditable, not so
the mechanisms may change):

- A1. A's occurrence depth is hard-capped: `occ_new` returns -1
  when ancestor depth d >= 16 (bc_search.zag). A chain needing
  depth 16+ cannot be built.
- A2. A's loop guard is the (need-kind, producer-id) pair on the
  open stack (bc_search.zag `prod_ok`). A producer cannot repeat
  on one root-to-leaf path. Chains need distinct producers.
- A3. A's occ arena holds 1.2M frames. CHAIN10 (9 WALKs) cost
  986,410 frames = sum P(9,k): the design 4.8 exponential worst
  case is real (bc report). Past 1.2M, `occ_new` returns -1,
  which the search misreads as producer exhaustion: the search
  dies and the problem FAILS (no wrong answer; candidates are
  still verified).
- A4. A is memoryless: fresh state per problem. A5. A's WIDEN is
  one-shot and relaxes only kind compatibility, not depth or
  the pair guard.
- B1. B's assembly nests at most 6 deep: `alts` expands
  sub-needs only when `depth < 6` (sus_asm.zag). The deepest
  direct-close grounding is at depth 6, so the longest
  buildable WALK chain is 6 links (+1 COUNT).
- B2. B's thunk table caps at 256 thunks (`th_new`: n>=256
  returns -2; sus_thunk.zag). Sub-need candidate buffers cap at
  128, the top candidate buffer at 256 (sus_asm.zag `alts`
  `cap` arguments). Past the cap, later candidates are
  silently dropped: they can never be evaluated.
- B3. B's MAP table holds 16 ids (sus_base.zag). All sealed
  worlds use ids 0..15 and at most 16 maps.
- B4. B's loop guard is path-based producer exclusion
  (`onpath`; sus_asm.zag), same consequence as A2 for chains.
- B5. B's WIDEN is one pass applying exactly one MAP over
  thunks with observed non-negative memos (sus_asm.zag
  `widen_pass`). It does NOT enforce the loop guard.
- C1. C's cold-start IS A's `solve` verbatim (lc_rev.zag
  `lc_cold`), so C inherits A1-A5 on first encounter.
- C2. C retrieves when similarity >= 2 (3=exact codes,
  2=subset either way, 1=kind-only). Contract code: arity-1 ->
  1000000+in*1000+out; arity-2 -> 2000000+in1*1000+in2*10+out
  (lc_mem.zag). The code carries NO relation id and NO map
  class.
- C3. Adaptation is injective (distinct old ids -> distinct new
  ids); unmapped instructions trigger DROP_UNMAPPED, which
  rewires dependents to CONST (lc_mem.zag).
- C4. Revision order is frozen: R1 SUBST_FAILED, R2 TRUNCATE
  (prefixes), R3 SUBST, R4 APPEND (one MAP at the frontier),
  then cold-start (lc_rev.zag). There is NO prepend/insert
  operator: a program that must grow at its input end cannot be
  reached by revision.
- C5. Memory holds 16 entries; `mem_new` returns -1 past 16 and
  the store is silently skipped (lc_mem.zag). No crash.
- C6. Every retrieved/adapted/revised program is verified
  against exp before it counts. C can therefore never return a
  wrong answer where A succeeds; its failure mode is wasted
  TRIES (efficiency), never correctness.
- C7. C's TRIES counter accumulates across retrieval, revision,
  and cold-start within one problem (lc_rev.zag never resets
  sg(S,4)).

## 3. World design rationale (per family)

Notation: W(m,rel) = WALK id m on rel (in{1}out{1});
C(m,rel) = COUNT id m on rel (in{1}out{2});
G(m) = ADD2 id m (in{2},in{2},out{2}). Missing fact -> -2.
All worlds: <= 64 facts, ids 0..15, kinds 1/2 opaque.

### 3.1 Falsification families (one per hypothesis)

F-A1 CHAIN15 (falsify A: regressive search explosion). 15-link
chain, 16 maps. By A3 the frame cost grows as sum P(15,k)
(CHAIN10 datapoint: sum P(9,k) = 986,410); 1.2M frames are
exhausted long before the answer is found, so A dies via
resource explosion, the exact failure the parent asked to be
demonstrated. B cannot reach depth 15 (B1); C cold-starts into
A's search (C1). Predicted: all three FAIL, for three
different documented reasons (explosion / depth cap /
cold-start inheritance). This separates "A explodes" from
"A is depth-capped": CHAIN15 is within A's depth bound (15 <=
15) yet still kills A.

F-B1 CHAIN7 (falsify B: depth cap). 7-link chain, 8 maps.
A builds it (depth 7 <= 15, A1); B cannot (B1: 6 links max;
verified by depth count in sus_asm.zag; WIDEN adds only one
MAP application and cannot bridge a 7-chain, B5). C inherits
A's success (C1). Predicted: A PASS, C PASS, B FAIL. A and C
dominate B on depth.

F-B2 SUBCAP (falsify B: candidate-buffer cap). Root COUNT with
a 3-link correct chain C1(W3(W2(s))), 15 maps, 11 WALKs. B's
depth-1 sub-need buffer (cap 128, B2) fills entirely with
W1-rooted chains during the first producer's turn (verified by
tracing `alts`: each level's buffer fills before the next
producer is tried, and `onpath` keeps chains
distinct-producer). The correct W3-rooted program is never
interned, so no candidate can match exp; WIDEN applies one MAP
and cannot synthesize the 2-link suffix. A finds it by
chronological search with -2 pruning (A2 pair guard satisfied:
W2,W3 distinct). C cold-starts to A's search. Predicted:
A PASS, C PASS, B FAIL. This is the "256 cap" falsification:
the cap that bites is the 128 sub-buffer (same mechanism as
the 256 top cap).

F-C1 TRAP1 (falsify C: retrieval misfire). Two-problem
sequence in one process (memory persists). TEACH: 2-chain
[X,Y] (stores E1, codes {1001001,1001002}). TRAP1: 16-map
inventory whose code multiset {1001001x12, 1001002x4} is a
superset of E1's -> sim 2 (C2), so retrieval FIRES. The
adapted program [X,Y] executes to -2 (X(s) has no facts), so
NEGREC records fail++. Revision: R1 tries 11 contract-matching
WALK substitutes + 3 COUNT substitutes (all fail); R2
prefixes fail; R3 repeats memoized (0 new tries); R4 appends
16 dead MAPs (16 tries); then cold-start duplicates A's full
search. By C6/C7, C_TRIES = misfire (>0, structurally: at
least the 2 adapted executions) + A_TRIES, so C_TRIES >
A_TRIES STRICTLY. A's memoryless search pays only the search.
Predicted: A PASS, B PASS (record only), C PASS with
C_TRIES > A_TRIES, SIM=2, MODE=REVISE. This falsifies "C's
memory always helps": here learning strictly hurts.

### 3.2 Dominance / complementarity families

D-B1 CYCLE-2HOP (B dominates). One WALK on a cyclic relation;
query needs 2 hops through the SAME map. A's pair guard (A2)
and C's cold-start (C1) block producer reuse -> both FAIL.
B's WIDEN (B5) does not enforce the loop guard: the one-shot
pass applies Wc over the observed-good 1-hop thunk and reaches
the 2-hop value. Predicted: A FAIL, C FAIL, B PASS with
WIDEN=1. An emergent B capability none of the builders'
batteries exercised.

D-C1 TRANSFER (C uniquely transfers). One process:
TEACH-D (diamond, stores E1), T-FANIN (2-leg fan-in, direct
COUNT legs), T-CHAIN (2-chain). T-FANIN codes
{1001002x2,2002022} are a subset of E1's diamond codes ->
sim 2; X unmapped -> DROP_UNMAPPED rewires both legs to CONST
(C3) -> adapted program succeeds immediately. T-CHAIN codes
{1001001,1001002x2} likewise sim 2; G unmapped -> drop ->
[X',Y',W'] whose last instruction W'(X'(s)) = exp. Neither A
nor B transfers: both solve from scratch. Predicted: all
PASS; C with MODE=REVISE (repaired), SIM=2 on both. This is
the "C dominates" world: cross-shape transfer with no
re-search and no re-assembly.

D-C2 TRAP2 (C revision boundary; contrasts F-C1). Same
16-map inventory as TRAP1, new facts: correct program is
[W1,X,Y] (one substitution from TRAP1's stored [Z,X,Y]).
C retrieves E2 at sim 3, adaptation is identity, exec fails
(Z(s) = -2), R1 SUBST_FAILED substitutes Z->W1 and SUCCEEDS.
Predicted: A PASS, C PASS with C_TRIES < A_TRIES, MODE=REVISE.
Paired with F-C1, this maps C's revision boundary precisely:
1-edit (substitute) is repaired; the 2-edit TRAP1 needs
(prepend-equivalent growth at the input end, C4) is not.

### 3.3 Shared-failure families (all three fail)

S-ALL1 CYCLE-3HOP. Same cyclic world as D-B1; query needs 3
hops. B's one-step WIDEN (B5) cannot bridge 2 missing links;
A/C blocked by the pair guard. Predicted: all FAIL. Tests
the "no iterate-with-halt" shared boundary: none of the three
can traverse a productive cycle.

(S-ALL2 is F-A1 CHAIN15, which also fails all three, for
documented per-hypothesis reasons.)

### 3.4 Axis-coverage families (robustness; all should PASS)

X-CHAIN5: 5-link chain (5-structure combination), fresh
relations. X-FANOUT5: one intermediate feeding 5 COUNT
consumers joined by a 4-ADD2 tree (fan-out axis).
X-FANIN5: 5 independent WALK->COUNT legs joined by a 4-ADD2
tree (fan-in axis, 5 legs). X-DAG10: 10-MAP DAG: 2-chain ->
shared X -> two diamonds -> ADD2 join (general DAG, 10+
structures, neither pure fan-out nor pure fan-in; max B depth
5). X-PARTIAL: 5-leg fan-in with 2 legs factless (partial
applicability): the answer is the sum of the 3 live legs;
mechanisms must compose from the applicable subset (dead
legs evaluate to -2 and prune). All predicted PASS for A, B,
C; TRIES recorded for efficiency comparison.

## 4. Declarative world specifications

Format per world: maps as (id, class, rel, inmask, outmask,
inmask1, inmask2, arity); facts as (s, r, o); query as
(s, kin, kout, exp); witness as MAP application sequence.
Classes: 0=WALK, 1=COUNT, 4=ADD2. Node ids use per-world
hundreds ranges; counts (exp) are small ints; no collision.

### F-A1 CHAIN15
Maps: ids 0..14 class 0 rel 61+i in 1 out 1 ar 1 (i=0..14);
id 15 class 1 rel 76 in 1 out 2 ar 1.
Facts: (501,61,502),(502,62,503),(503,63,504),(504,64,505),
(505,65,506),(506,66,507),(507,67,508),(508,68,509),
(509,69,510),(510,70,511),(511,71,512),(512,72,513),
(513,73,514),(514,74,515),(515,75,516),
(516,76,801),(516,76,802),(516,76,803),(516,76,804).
Query: (501,1,2,4). Witness: W1..W15 then C. 19 facts.

### F-B1 CHAIN7
Maps: ids 0..6 class 0 rel 61+i in 1 out 1 ar 1;
id 7 class 1 rel 68 in 1 out 2 ar 1.
Facts: (501,61,502),(502,62,503),(503,63,504),(504,64,505),
(505,65,506),(506,66,507),(507,67,508),
(508,68,801),(508,68,802),(508,68,803),(508,68,804).
Query: (501,1,2,4). Witness: W1..W7 then C. 11 facts.

### F-B2 SUBCAP
Maps: ids 0..3 class 1 rel 71+i in 1 out 2 ar 1 (C1..C4);
ids 4..14 class 0 rel 81+j in 1 out 1 ar 1 (W1..W11, j=0..10).
Facts: (501,82,601) [W2], (601,83,602) [W3],
(602,71,701),(602,71,702),(602,71,703),(602,71,704) [C1=4],
(501,81,699) [W1 dead end]. C2..C4, W4..W11: no facts.
Query: (501,1,2,4). Witness: C1(W3(W2(501))). 7 facts.

### F-C1 TEACH (C only, stores E1)
Maps: id 1 class 0 rel 91 in 1 out 1 ar 1 (X);
id 2 class 1 rel 92 in 1 out 2 ar 1 (Y).
Facts: (201,91,211),(211,92,901),(211,92,902),(211,92,903).
Query: (201,1,2,3). Witness: Y(X(201)).

### F-C1 TRAP1 (A/B fresh; C after TEACH in one process)
Maps: id 0 class 0 rel 90 in 1 out 1 (Z); id 1 class 0
rel 91 in 1 out 1 (X); ids 2..11 class 0 rel 93+k in 1 out 1
(W1..W10, k=0..9); id 12 class 1 rel 92 in 1 out 2 (Y);
ids 13..15 class 1 rel 103+l in 1 out 2 (D1..D3, l=0..2).
Facts: (201,90,211) [Z], (211,91,212) [X],
(212,92,911),(212,92,912),(212,92,913),(212,92,914),(212,92,915)
[Y=5], (201,93,700),(201,94,701),(201,95,702),(201,96,703),
(201,97,704),(201,98,705),(201,99,706),(201,100,707),
(201,101,708),(201,102,709) [W dead ends],
(201,103,921),(201,103,922),(201,104,923),(201,104,924),
(201,105,925),(201,105,926) [D1=D2=D3=2].
Query: (201,1,2,5). Witness: Y(X(Z(201))). 23 facts.

### D-C2 TRAP2 (C after TRAP1 in one process; A/B fresh)
Maps: same 16 as TRAP1.
Facts: (201,93,213) [W1], (213,91,212) [X],
(212,92,911),(212,92,912),(212,92,913),(212,92,914),(212,92,915)
[Y=5]. Z, W2..W10, D1..D3: no facts.
Query: (201,1,2,5). Witness: Y(X(W1(201))). 7 facts.

### D-C1 TEACH-D (C only, stores diamond E1)
Maps: id 0 class 0 rel 91 in 1 out 1 (X); id 1 class 1
rel 92 in 1 out 2 (Y); id 2 class 1 rel 94 in 1 out 2 (W);
id 3 class 4 rel 0 in 0 out 2 in1 2 in2 2 ar 2 (G).
Facts: (202,91,211),(211,92,901),(211,92,902),(211,92,903),
(211,94,911),(211,94,912).
Query: (202,1,2,5). Witness: G(Y(X(202)),W(X(202))).

### D-C1 T-FANIN (C after TEACH-D; A/B fresh)
Maps: id 0 class 1 rel 71 in 1 out 2 (C1); id 1 class 1
rel 72 in 1 out 2 (C2); id 2 class 4 rel 0 in 0 out 2
in1 2 in2 2 ar 2 (G1).
Facts: (401,71,701),(401,71,702),(401,71,703),
(401,72,704),(401,72,705).
Query: (401,1,2,5). Witness: G1(C1(401),C2(401)).

### D-C1 T-CHAIN (C after T-FANIN; A/B fresh)
Maps: id 0 class 0 rel 91 in 1 out 1 (Xp); id 1 class 1
rel 92 in 1 out 2 (Yp); id 2 class 1 rel 94 in 1 out 2 (Wp).
Facts: (301,91,311),(311,92,801),(311,92,802),(311,92,803),
(311,92,804),(311,94,811),(311,94,812),(311,94,813).
Query: (301,1,2,3). Witness: Wp(Xp(301)).

### D-B1 CYCLE-2HOP / S-ALL1 CYCLE-3HOP
Maps: id 0 class 0 rel 61 in 1 out 1 ar 1 (Wc).
Facts: (501,61,502),(502,61,503),(503,61,502).
2HOP query: (501,1,1,503). Witness: Wc(Wc(501)).
3HOP query: (501,1,1,502). Witness: Wc(Wc(Wc(501))).

### X-CHAIN5
Maps: ids 0..4 class 0 rel 61+i in 1 out 1;
id 5 class 1 rel 66 in 1 out 2.
Facts: (501,61,502),(502,62,503),(503,63,504),(504,64,505),
(505,65,506),(506,66,801)..(506,66,806).
Query: (501,1,2,6). Witness: W1..W5 then C. 11 facts.

### X-FANOUT5
Maps: id 0 class 0 rel 91 in 1 out 1 (X);
ids 1..5 class 1 rel 92+i in 1 out 2 (Y1..Y5, i=0..4);
ids 6..9 class 4 rel 0 in 0 out 2 in1 2 in2 2 ar 2 (G1..G4).
Facts: (202,91,211),
(211,92,901),(211,92,902),
(211,93,903),
(211,94,904),(211,94,905),(211,94,906),
(211,95,907),(211,95,908),
(211,96,909),(211,96,910).
Counts 2,1,3,2,2; exp 10. Query: (202,1,2,10).
Witness: X; Y1..Y5; G1(Y1,Y2); G2(Y3,Y4); G3(G1,G2);
G4(G3,Y5). 11 facts.

### X-FANIN5
Maps: ids 0..4 class 0 rel 61+i in 1 out 1 (W1..W5);
ids 5..9 class 1 rel 71+i in 1 out 2 (C1..C5);
ids 10..13 class 4 rel 0 in 0 out 2 in1 2 in2 2 ar 2 (G1..G4).
Facts: (401,61,501),(501,71,701),(501,71,702),
(401,62,502),(502,72,703),(502,72,704),(502,72,705),
(401,63,503),(503,73,706),
(401,64,504),(504,74,707),(504,74,708),(504,74,709),(504,74,710),
(401,65,505),(505,75,711),(505,75,712).
Leg values 2,3,1,4,2; exp 12. Query: (401,1,2,12).
Witness: W1..W5; C1..C5; G1(L1,L2); G2(G1,L3); G3(G2,L4);
G4(G3,L5). 17 facts.

### X-DAG10
Maps: id 0 class 0 rel 60 in 1 out 1 (W0); id 1 class 0
rel 61 in 1 out 1 (W1); id 2 class 0 rel 62 in 1 out 1 (X);
id 3 class 1 rel 71 in 1 out 2 (Y1); id 4 class 1 rel 72
in 1 out 2 (Z1); id 5 class 4 rel 0 in 0 out 2 in1 2 in2 2
ar 2 (G1); id 6 class 1 rel 73 in 1 out 2 (Y2); id 7
class 1 rel 74 in 1 out 2 (Z2); id 8 class 4 rel 0 in 0
out 2 in1 2 in2 2 ar 2 (G2); id 9 class 4 rel 0 in 0 out 2
in1 2 in2 2 ar 2 (H).
Facts: (301,60,302),(302,61,303),(303,62,310),
(310,71,711),(310,71,712),(310,72,713),(310,72,714),
(310,72,715),(310,73,716),(310,74,717),(310,74,718),
(310,74,719),(310,74,720).
a1=2,b1=3,a2=1,b2=4; exp 10. Query: (301,1,2,10).
Witness: W0;W1;X;Y1;Z1;G1;Y2;Z2;G2;H(G1,G2). 13 facts.

### X-PARTIAL
Maps: ids 0..4 class 0 rel 61+i in 1 out 1 (W1..W5);
ids 5..9 class 1 rel 71+i in 1 out 2 (C1..C5);
ids 10..13 class 4 rel 0 in 0 out 2 in1 2 in2 2 ar 2 (G1..G4).
Facts: (401,61,501),(501,71,701),(501,71,702),
(401,62,502),(502,72,703),(502,72,704),(502,72,705),
(401,63,503),(503,73,706),(503,73,707),(503,73,708),
(503,73,709),(503,73,710).
Legs 1..3 live (2,3,5); legs 4,5 factless. exp 10.
Query: (401,1,2,10).
Witness: W1;W2;W3;C1;C2;C3;G1(L1,L2);G2(G1,L3). 13 facts.

## 5. Frozen kill bars

HARD bars (all must hold for the adversary's predictions to
be confirmed; a failure is reported as a failed prediction):

- K-ADV-A1 (CHAIN15): A_ANS != 4 AND B_ANS != 4 AND C_ANS != 4.
- K-ADV-B1 (CHAIN7): A_ANS = 4 AND B_ANS != 4 AND C_ANS = 4.
- K-ADV-B2 (SUBCAP): A_ANS = 4 AND B_ANS != 4 AND C_ANS = 4.
- K-ADV-C1 (TRAP1): A_ANS = 5 AND B_ANS = 5 AND C_ANS = 5.
- K-ADV-C2 (TRAP2): A_ANS = 5 AND C_ANS = 5.
- K-ADV-T1 (T-FANIN): A_ANS = 5 AND B_ANS = 5 AND C_ANS = 5.
- K-ADV-T2 (T-CHAIN): A_ANS = 3 AND B_ANS = 3 AND C_ANS = 3.
- K-ADV-D1 (CYCLE-2HOP): A_ANS != 503 AND B_ANS = 503 AND
  C_ANS != 503.
- K-ADV-D2 (CYCLE-3HOP): A_ANS != 502 AND B_ANS != 502 AND
  C_ANS != 502.
- K-ADV-X1 (X-CHAIN5): A/B/C ANS = 6.
- K-ADV-X2 (X-FANOUT5): A/B/C ANS = 10.
- K-ADV-X3 (X-FANIN5): A/B/C ANS = 12.
- K-ADV-X4 (X-DAG10): A/B/C ANS = 10.
- K-ADV-X5 (X-PARTIAL): A/B/C ANS = 10.
- K-ADV-M1 (TRAP1): C_SIM = 2 AND C_MODE = 2 (REVISE).
- K-ADV-M2 (CYCLE-2HOP): B_WIDEN = 1.
- K-ADV-M3 (T-FANIN and T-CHAIN): C_SIM = 2 AND C_MODE = 2.
- K-ADV-E1 (TRAP1): C_TRIES > A_TRIES (strict; structurally
  guaranteed by C6/C7: misfire >= 2 tries + identical
  cold-start).

SOFT bars (informative; failure does not void the battery):

- S-ADV-E2 (TRAP2): C_TRIES < A_TRIES (predicted: R1 revision
  succeeds cheaply, ~8 vs ~40).
- S-ADV-E3: TRIES/DEXEC recorded on all axis worlds for the
  efficiency comparison (no frozen inequality).

Void rules: if K-ADV-M1 fails (retrieval did not fire as
designed), K-ADV-E1 is VOID (its structural guarantee assumed
the misfire path). If any world panics instead of returning
ANS, the corresponding bar FAILS and the panic is reported
verbatim (a panic is not a predicted outcome anywhere).

## 6. Sealed evaluation protocol (for the parent/evaluator)

1. Build: copy (do not move) the frozen mechanism sources into
   a fresh eval directory OUTSIDE builder lanes. Concatenate:
   A: bc_base + bc_thunk + bc_search + adv_worlds +
      eval_main_a. B: sus_base + sus_thunk + sus_asm + sus_rev +
      adv_worlds + eval_main_b. C: lc_base + lc_thunk +
      lc_search + lc_mem + lc_rev + lc_world? NO: lc_world is
      the builder world file; use adv_worlds instead. So C:
      lc_base + lc_thunk + lc_search + lc_mem + lc_rev +
      lc_rep + adv_worlds + eval_main_c. (lc_rep carries
      do_prob reporting; it has no main.) Compile each with the
   pinned znc. Template eval mains live in this lane under
   eval_templates/ (reporting mirrors the builders' mains:
   PROB/ANS/TRIES/WIDEN[/MODE/SIM/NEGREC]/VERDICT lines).
2. Process grouping (memory semantics):
   A and B: every problem in a FRESH process (fresh arenas;
   mirrors bc_main/sus_main per-problem freshness).
   C: F-C1 sequence (TEACH, TRAP1, TRAP2) in ONE process, M
   persisting, S fresh per problem; D-C1 sequence (TEACH-D,
   T-FANIN, T-CHAIN) in ONE process; every other C problem in
   a FRESH process.
3. Run each binary 3 times; require byte-identical stdout
   across the 3 runs (determinism bar, per loop standard).
   Empty stderr required.
4. Score the HARD/SOFT bars from the reported fields. ANS=-2
   (or the -999 sentinel) counts as FAIL-to-solve for the
   != bars and as not-exp for the = bars.
5. The adversary has NOT executed any mechanism on these
   worlds. The first mechanism execution on sealed worlds
   happens in this evaluation.

## 7. Sealing statement

- Builders (BACKCHAIN-1, SUSPEND-1, LEARNCOMPOSE-1 workers)
  have not seen these worlds: they were designed after all
  three BUILD-PASS reports, in this separate lane, and no
  builder lane file was read for world content (only mechanism
  bounds, Section 2).
- The world builders (adv_worlds.zag, written after this
  prereg commit) are validated SOLELY by adv_witness.zag, an
  independent pure-Zag reimplementation of the substrate
  (fact store + WALK/COUNT/ADD2 + -2 semantics) that executes
  the Section 4 witness for each query and asserts the value
  equals exp. The witness checker uses NO mechanism code.
- No bar was tuned to any mechanism execution output,
  because no mechanism was executed on sealed worlds.

## 8. Amendment log

(none)
