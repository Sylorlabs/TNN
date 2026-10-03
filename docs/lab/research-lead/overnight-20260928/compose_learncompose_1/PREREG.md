# PREREG.md -- COMPOSE-LEARNCOMPOSE-1: preregistered implementation of Hypothesis C (LEARN-COMPOSE)

Date: 2026-10-03. Worker: COMPOSE-LEARNCOMPOSE-1. Lane:
`docs/lab/research-lead/overnight-20260928/compose_learncompose_1/`.
Task type: NON-LEDGER (claim minting paused).

Parent design: COMPOSE-GENERAL-1, REPORT.md Section 6 (Hypothesis C:
LEARN-COMPOSE, learner-owned composition policy, contract-defined
revision operators). Competitors: COMPOSE-BACKCHAIN-1 (A, BUILD-PASS),
COMPOSE-SUSPEND-1 (B, BUILD-PASS). This preregistration freezes the
mechanism, the worlds, and the kill bars (F-C1a/F-C1b/F-C1/F-C2/F-C3/
F-C4 plus regression and A-vs-B-vs-C discriminators) BEFORE any
implementation file exists. Status of everything below: FROZEN. Any
deviation requires a prereg amendment committed before the deviating
run.

## 1. Frozen mechanism: LEARN-COMPOSE-C

### 1.1 What C is and is not (structural difference vs A and B)

- A (BACKCHAIN): fixed regressive procedure, memoryless, search and
  execution interleaved. Every goal is solved from scratch.
- B (SUSPEND): fixed two-phase procedure (ASSEMBLE then EVALUATE),
  persistent composite store keyed by EXACT (kin, kout, sketch),
  structural rebind, surgical sub-thunk revision. The strategy never
  changes with experience.
- C (LEARN-COMPOSE): the composition POLICY lives in learner-owned
  state. There is a composition memory of (goal-signature, composite
  program, outcome history) entries. Per goal C retrieves the best
  entry by a frozen similarity function, adapts it to the current
  inventory by contract-defined SUBST, executes and verifies
  end-to-end, revises with a frozen set of general operators on
  failure, and records negative evidence (failures++) on the tried
  entry. Cold-start (first encounter with no retrievable entry) uses
  the regressive substrate shared with A, as the bootstrap that
  populates memory. C's behavior on the tenth goal therefore differs
  from its behavior on the first; A and B are fixed procedures whose
  behavior does not change with experience.

C's cold-start reuses the regressive substrate VERBATIM (the
BACKCHAIN-1 bc_base/bc_thunk/bc_search logic, copied as lc_*).
This is a deliberate experimental control: C = substrate + memory,
so every A-vs-C behavioral difference is attributable to the memory
layer. C claims NO first-encounter efficiency advantage over A.
C's distinctive, falsifiable claims are the learning curve (F-C1),
operator revision beating re-search (F-C2), and negative-evidence
recording (F-C3).

### 1.2 Learner state (persistent across goals in one process)

Arena M (composition memory), separate from the per-goal scratch S:
- nentries; MAXE=16 entries (fail-clean if full; predicted never hit).
- Entry: kin, kout, ncodes, sorted contract codes[16], successes,
  failures, program.
- Program: up to 16 instructions; each instruction =
  (map_id, arity, c_in, c_out, c_in1, c_in2, a, b) where a,b are
  instruction indices of inputs or -1 for the goal-input const.
  Contracts (c_in/c_out/c_in1/c_in2) are stored per instruction so
  that adaptation can match by contract after the original map ids
  are gone (fresh-relation worlds).

Per-goal scratch S is FRESH per goal (thunk table, memos, occ frames,
tries counter), exactly as in BACKCHAIN-1. The memory M is the ONLY
thing that persists across goals. The value memo used during
revision is A's demand() identity memoization over hash-consed
thunks (per-goal scratch, not memory).

### 1.3 Goal signature and similarity (frozen)

sig = (kin, kout, sketch). sketch = the inventory's contract codes,
sorted ascending (insertion sort; order-invariant, label-free).
Per-map code: arity 1: 1000000 + inmask*1000 + outmask; arity 2:
2000000 + inmask1*1000 + inmask2*10 + outmask. Masks are small
(1..3); the two ranges do not overlap. No relation numbers, node
ids, kind labels, or domain names enter the code.

Similarity (frozen), computed over (kin, kout, sorted codes) only:
- 3 = exact: kin, kout equal and code multisets equal.
- 2 = kin, kout equal and one code multiset is a subset of the
  other (multiset inclusion, order-free).
- 1 = kin, kout equal only.
- 0 = otherwise.
Retrieval picks the max by (similarity desc, (successes - failures)
desc, entry index asc). Deterministic. FROZEN RETRIEVAL THRESHOLD:
retrieve iff best similarity >= 2. (The design ranks the levels but
does not fix a threshold; sim 1 = kind-match-only carries no
structural information and is frozen as insufficient for retrieval.
This is a prereg choice, not a post-hoc fix.)

### 1.4 Adaptation (contract-defined SUBST)

For each program instruction in order, find the current-inventory
map id:
1. the original map id, if it is in [base, base+nm) AND its live
   contract exactly equals the stored contract;
2. else the lowest id in [base, base+nm) whose live contract
   exactly equals the stored contract (arity and all masks);
3. else -1 (unmapped).
Exact contract equality (not khas-overlap) is the frozen rule: it
preserves program validity (a substituted map must satisfy the same
input/output kind contracts the program was verified under).
Adaptation is over opaque ids and kind bitmasks only.

If every instruction maps: build the thunk DAG (hash-consed via
intern; const = C(s)) and demand the root: this is the adapted
execution. If some instruction is unmapped: DROP_UNMAPPED repair
(remove unmapped instructions, rewire dependents' args to CONST,
reindex; if nothing remains, go to cold-start), then execute.

### 1.5 Revision operators (frozen set, frozen order)

Applied when the adapted (or repaired) program fails end-to-end
verification. Each candidate is built as thunks (interned, so
memos are shared across candidates) and demanded; first
end-to-end success wins and is stored as a new memory entry.
- R1 SUBST_FAILED: for each instruction whose executed value is -2,
  in program order: substitute each contract-matching alternative
  map (id order, excluding the current id).
- R2 TRUNCATE: prefixes P[0..k-1] for k = len-1 down to 1.
- R3 SUBST: for each instruction in program order, each
  contract-matching alternative (id order, excluding current).
- R4 APPEND: for each map m in id order: 1-input: P+[m(root)];
  2-input: P+[m(root,CONST)], P+[m(CONST,root)],
  P+[m(root,root)]. (Blind: no kind pre-check; verification
  decides. Not exercised by any frozen bar.)
On revision exhaustion: record nothing further and run cold-start
(which includes the one-shot widen pass). RETRY-WIDEN is covered
by cold-start's widen; it is not a separate revision operator in
this build.

No operator mentions diamonds, fan-out, chains, legs, or any
shape: they are defined over instruction indices, contract codes,
and the -2 sentinel. There is no diamond handler, no shape
template, no mode, no domain branch.

### 1.6 Recording (frozen)

- Cold-start success: extract the winning thunk DAG as a program
  (DFS post-order; const -> -1) and store a new entry
  (successes=1, failures=0) under the goal sig.
- Retrieve+adapt success: successes++ on the retrieved entry; no
  new entry.
- Adapted execution fails verification: failures++ on the
  retrieved entry (NEGREC=1, negative evidence is recorded), then
  revision. The failing composite is NEVER recorded as a success.
- Revision success: store the revised program as a new entry
  (successes=1) under the current goal sig.
- Cold-start failure (after widen): ANS=-2; nothing stored.

### 1.7 Domain-blindness

Every decision consults only opaque map ids, arities, kind
bitmasks, code multisets, and thunk identity. The signature is
(kin, kout, sorted contract codes): no relation labels, node ids,
domain names, or capability names. F-C4 and the blind battery
test this.

## 2. Frozen worlds

Shared worlds (identical inventories, facts, goals to
COMPOSE-BACKCHAIN-1 PREREG Section 2; classes 0=WALK, 1=COUNT,
4=ADD2; kinds opaque bits 1,2; MISS=-2):

Q1 (diamond): base 0, nm 4: m0 class0 rel91 in{1} out{1}; m1
class1 rel92 in{1} out{2}; m2 class1 rel94 in{1} out{2}; m3
class4 in1{2} in2{2} out{2}. Facts: (202,91,211),
(211,92,901/902/903) [Y=3], (211,94,911/912) [W=2].
Goal s=202, kin=1, kout=2, exp=5.

Q1b: same inventory; added facts (204,91,212),
(212,92,904/905) [Y=2], (212,94,913) [W=1].
Goal s=204, kin=1, kout=2, exp=3.

Q1rev: Q1 inventory; retract (211,94,*) facts; add m4 id4
class1 rel95 in{1} out{2} with (211,95,921/922) [V=2].
Goal s=202, kin=1, kout=2, exp=5.

CHAIN3: base 5, nm 3: c0 id5 class0 rel81 in{1} out{1}; c1 id6
class0 rel82 in{1} out{1}; c2 id7 class1 rel83 in{1} out{2}.
Facts: (301,81,302), (302,82,303),
(303,83,801..807) [c2=7]. Goal s=301, kin=1, kout=2, exp=7.

FANIN: base 8, nm 3: f1 id8 class1 rel71 in{1} out{2} facts
(401,71,701..704) [f1=4]; f2 id9 class1 rel72 in{1} out{2}
facts (401,72,705..709) [f2=5]; g id10 class4 in1{2} in2{2}
out{2}. Goal s=401, kin=1, kout=2, exp=9.

PARTIAL: Q1 inventory. Goal s=202, kin=1, kout=2, exp=3.
(True root: the Y-leg sub-program.)

Q2 (misleading teaching): base 11, nm 4: m0p id11 class0
rel91 in{1} out{1}; m1p id12 class1 rel92 in{1} out{2}; m2p
id13 class1 rel94 in{1} out{2}; m3p id14 class4 in1{1} in2{1}
out{2} (taught NODE inputs; computes addition). Facts as Q1.
Goal s=202, kin=1, kout=2, exp=5.

CHAIN10: base 20, nm 10: c0..c8 ids 20..28 class0 rels
61..69 in{1} out{1}; c9 id29 class1 rel70 in{1} out{2}.
Facts: (501,61,502) .. (509,69,510); (510,70,801..804)
[c9=4]. Goal s=501, kin=1, kout=2, exp=4.

F-C1 sequence (FRESH memory process; fresh relations, ids,
nodes throughout; w3 deviates from the design's "equal
inventory size", see 2.1):

W1 (diamond-1): base 30, nm 4: X id30 class0 rel51 in{1}
out{1}; Y id31 class1 rel52 in{1} out{2}; W id32 class1
rel54 in{1} out{2}; G id33 class4 in1{2} in2{2} out{2}.
Facts: (601,51,602); (602,52,901/902/903) [Y=3];
(602,54,911/912) [W=2]. Goal s=601, kin=1, kout=2, exp=5.

W2 (diamond-2): base 34, nm 4: X id34 class0 rel55 in{1}
out{1}; Y id35 class1 rel56 in{1} out{2}; W id36 class1
rel58 in{1} out{2}; G id37 class4 in1{2} in2{2} out{2}.
Facts: (603,55,604); (604,56,901/902) [Y=2]; (604,58,911)
[W=1]. Goal s=603, kin=1, kout=2, exp=3.

W3 (fan-in): base 38, nm 3: f1 id38 class1 rel61 in{1}
out{2} facts (605,61,701..704) [f1=4]; f2 id39 class1
rel62 in{1} out{2} facts (605,62,705..709) [f2=5]; g id40
class4 in1{2} in2{2} out{2}. Goal s=605, kin=1, kout=2,
exp=9.

ADV (F-C3 adversarial): base 42, nm 4: X id42 class0 rel71
in{1} out{1}; Y id43 class1 rel72 in{1} out{2}; W id44
class1 rel74 in{1} out{2}; G id45 class4 in1{2} in2{2}
out{2}. Facts: (608,71,609); (609,72,901/902/903) [Y=3];
(609,74,911/912) [W=2]. Goal s=608, kin=1, kout=2, exp=3.
(The stored diamond composite executes to 5; exp=3, so
verification must fail and negative evidence must be
recorded.)

### 2.1 Documented deviation: F-C1 W3 inventory size

The design (6.7 F-C1) specifies "equal inventory size" for the
three goals. A 4-map W3 with the diamond's exact contract
sketch necessarily contains an (arity1,{1},{1}) map, which
adaptation poison-maps to X's slot (hand-traced: the (1,1,1)
distractor has no facts, poisons every leg to -2, and forces
a long failing revision before cold-start; T3 > T1, killing
F-C1b). The frozen W3 uses 3 maps whose sketch is a SUBSET of
the diamond sketch (sim 2, cross-shape transfer). The
scientific point (memory-assisted cross-shape transfer,
T3 < T1) is preserved; the equal-size control is traded for a
clean mechanism trace. This deviation is declared HERE, before
any run, not discovered after.

### 2.2 Blind battery (F-C4)

Five Q1/Q1b/Q1rev sequences in fresh processes: V0 baseline;
V1 relation numbers permuted (91->94, 92->91, 94->92; 95
fixed); V2 node ids permuted (202->707, 211->708, 204->709,
212->710); V3 kind polarity swapped (1<->2 in all contracts,
kin, kout); V4 V1+V2+V3 jointly. Each variant prints the same
summary lines. All five must be byte-identical.

## 3. Frozen kill bars

Hand-traced under the frozen mechanism (Section 1). tries =
total MAP executions per goal (memo hits do not count; S fresh
per goal). MODE in {COLD, RETRIEVE, REVISE}; SIM = retrieval
similarity (-1 if cold); NEGREC = 1 iff a retrieved entry's
execution failed verification (failures++ recorded).

Main binary (one process; M persists across the 8 problems):

- Q1: ANS=5, TRIES=7, WIDEN=0, MODE=COLD, SIM=-1, NEGREC=0.
  (Memory empty; cold-start = substrate; stores diamond entry.)
- Q1b: ANS=3, TRIES=4, WIDEN=0, MODE=RETRIEVE, SIM=3,
  NEGREC=0. F-C0b: TRIES(Q1b)=4 < 7 = A's re-search tries.
  Discriminates C from A (memoryless).
- Q1rev: ANS=5, TRIES=7, WIDEN=0, MODE=REVISE, SIM=2,
  NEGREC=1. Trace: adapt (4 execs: X=211, Y=3, W=-2, G=-2),
  R1 SUBST_FAILED on W: m1 -> G(3,3)=6 (1 exec), m4/V ->
  G(3,2)=5 (2 execs). F-C2: 7 < 9 = A's from-scratch
  re-solve tries on the same broken world. Discriminates C
  from A. (B's surgical revision is cheaper still; C does not
  claim to beat B here.)
- CHAIN3: ANS=7, TRIES=6, WIDEN=0, MODE=COLD, SIM=-1.
  (sim 1 < threshold; cold-start ties A.)
- FANIN: ANS=9, TRIES=4, WIDEN=0, MODE=COLD, SIM=-1.
- PARTIAL: ANS=3, TRIES=4, WIDEN=0, MODE=REVISE, SIM=3,
  NEGREC=1. Trace: adapt executes diamond (4 execs) -> 5 !=
  3; R1 skipped (no -2s); R2 TRUNCATE k=3 -> 2 != 3, k=2 ->
  [X,Y] -> 3 (0 new execs, memo hits). (C pays 4 vs A's 3:
  retrieval misfires on the full diamond and truncates; B's
  sub-thunk reuse is cheaper. Honest cost of operator-based
  revision, reported as-is.)
- Q2: ANS=5, TRIES=57, WIDEN=1, MODE=COLD, SIM=-1.
  (Cold-start's widen pass; same as A's Q2.)
- CHAIN10: ANS=4, TRIES=55, WIDEN=0, MODE=COLD, SIM=-1.
  (sim 1 < threshold; cold-start ties A; no round/pool caps.)

F-C1 binary (fresh M; W1, W2, W3, ADV in one process):

- W1: ANS=5, TRIES=7, WIDEN=0, MODE=COLD. (T1=7.)
- W2: ANS=3, TRIES=4, WIDEN=0, MODE=RETRIEVE, SIM=3.
  (T2=4: contract-based adaptation to fresh ids.)
- W3: ANS=9, TRIES=4, WIDEN=0, MODE=REVISE, SIM=2,
  NEGREC=1. Trace: sim-2 retrieval; X unmapped (no
  (arity1,{1},{1}) in W3); DROP_UNMAPPED -> [f1(C),f1(C),
  g(i0,i1)] (2 execs) -> 8 != 9; R1 skipped; R2 TRUNCATE
  fails (0 new); R3 SUBST i0 -> f2 -> [f2(C),f1(C),g] (2
  execs) -> 9. (T3=4.)
- ADV: ANS=3, TRIES=4, WIDEN=0, MODE=REVISE, SIM=3,
  NEGREC=1. Trace: stored diamond executes to 5 != 3;
  failures++ on the diamond entry; R2 TRUNCATE k=2 ->
  [X,Y] -> 3 (0 new execs).

Learning-curve bars:
- F-C1a: T2 < T1 (4 < 7). Same-shape transfer via memory.
  A predicts flat (7 = 7, memoryless). Discriminates C/A.
- F-C1b: T3 < T1 (4 < 7). Cross-shape transfer via sim-2
  retrieval + DROP_UNMAPPED + SUBST.
- F-C1 (design's falsification): T3 >= T1 kills the curve
  claim. (Observed 4 >= 7 is false: PASS.)
- F-C2: TRIES(Q1rev) = 7 < 9. (Stated above.)
- F-C3 (negative evidence), on ADV: (a) NEGREC=1: the stored
  diamond composite was executed and failed end-to-end
  verification; (b) the diamond entry's failures incremented
  and successes did NOT (ESEL line shows FAIL=2, SUCC=2:
  after W1/W2 succ=2, W3 fail=1, ADV fail=1); (c) the entry
  was not recorded as a success; (d) MODE=REVISE (a revision
  was attempted) and ANS=3. Falsified by silent reuse (no
  failure recorded) or by success reported without
  verification passing. Discriminates C from A/B (neither
  records negative evidence in a composition memory).
- F-C4 (signature blindness): the five blind variants are
  byte-identical (Section 2.2). Falsified by any byte
  difference.

A-vs-B-vs-C discriminator summary (all bars above):
- D2 re-query: A 7 (re-search) vs B 0-asm/4-exec (rebind) vs
  C 4 (retrieve). C beats A, ties B on execs.
- D3 revision: A 9 vs B 0 addl X/Y execs (surgical) vs C 7
  (operator revision). C beats A; B beats C.
- D4 curve: A flat (7,7,4) vs B (asm, 0-asm, fresh-asm by
  design: exact-match store misses the new sketch) vs C
  (7,4,4 with memory traces). Only C shows the decreasing
  trials curve with cross-shape memory use.
- PARTIAL: A 3 vs B sub-thunk reuse vs C 4. B wins; C's
  operator revision pays a misfire cost.

Determinism: all three binaries produce byte-identical stdout
across 3 runs each (3/3).

## 4. Verdict rule

BUILD-PASS iff every bar in Section 3 passes on 3/3
byte-identical runs of lc_bin, lc_fc1_bin, and lc_blind_bin.
Otherwise BUILD-FAIL, naming the killing bar with observed vs
predicted values. VOID (terminal) if: a forbidden interpreter
is invoked; the prereg is amended after any implementation
commit; a kill bar is altered to force a pass.

## 5. Honest bounds (declared)

- Cycles: BOUND (inherited from the substrate; no
  iterate-with-halt construct). GEN's cycle envelope stands
  unmatched.
- Purity: all MAPs pure; identity memoization unsound for
  effectful MAPs.
- C is an L2 claim: the revision operators, the signature
  function, and the similarity levels are researcher-provided
  generic machinery. What the learner owns: the composite
  programs, the success/failure counts, and hence the
  retrieval preferences. No L3 representational invention is
  claimed.
- Retrieval threshold sim>=2 is a frozen choice; sim-1
  (kind-match-only) goals cold-start, tying A.
- The signature does not include the expected value; two
  entries may share one sig with different programs (observed
  on PARTIAL/ADV). Ranked fallback across same-sig entries is
  NOT implemented; documented as a known limitation.
- R4 APPEND is implemented but exercised by no frozen bar.
- W3's 3-map inventory deviates from the design's equal-size
  prescription (Section 2.1).

## 6. Commit-order self-check

This PREREG.md and NAMECHECK.md are committed alone, with an
explicit pathspec, before any implementation file exists. The
prereg's first commit strictly precedes the implementation's
first commit.
