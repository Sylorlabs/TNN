# PREREG.md -- FORMAL-COMPOSE: P6 ACYCLIC constraints for DAG composition

Date: 2026-10-03. Worker: FORMAL-COMPOSE. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-KNOWLEDGE REPORT.md (BINDING CONSTRAINTS
mechanism; falsifiable predictions P1-P7; this task implements P6),
COMPOSE-SUSPEND-1 (Hypothesis B substrate, BUILD-PASS),
COMPOSE-BACKCHAIN-1 (Hypothesis A substrate), COMPOSE-PAIR6-ADV
(diamond worlds). This preregistration freezes the mechanism, the
worlds, the adversarial battery, and the kill bars (K1-K5) BEFORE
any implementation file exists. Status of everything below: FROZEN.
Any deviation requires a prereg amendment committed before the
deviating run.

## 1. The gap (why this experiment exists)

In COMPOSE-SUSPEND-1 and COMPOSE-BACKCHAIN-1 every composition goes
through fresh-node interning (`intern`/`th_new` with monotonic tids):
the thunk store is a DAG by construction and the (need,producer)
and on-stack guards are search-termination heuristics. There is NO
`link(existing, existing)` operation: no way to attach an already
built structure as a dependency of an already built composite
without rebuilding. That operation is exactly what L2 adaptive
reuse needs (extend a composite with a new leg, specialize by
attaching a replacement piece, adapt an interface by grafting),
and today nothing constrains it: a composer that links P -> C where
C transitively depends on P commits a directed cycle, and only
downstream evaluation heuristics (the on-stack guard) notice.

P6 (FORMAL-KNOWLEDGE REPORT.md section 7): "on the composition edge
store, adversarial compose attempts that would close a cycle: 0
cycles ever committed across the battery; acyclic diamond/fan-out/
fan-in attempts proceed normally. Failure mode that refutes: any
committed cycle, or any refused acyclic assembly."

This task builds the composition edge store WITH the missing
link-existing-existing operation, constrained by representational
ACYCLIC per FORMAL-KNOWLEDGE section 4.3 item 3 ("topological ranks
assigned at link time; a link that would close a cycle has no valid
rank and cannot be encoded").

## 2. Frozen mechanism

### 2.1 Composition edge store (all arms)

Node record (learner-state arena S, opaque integer ids):
(rank, map-id | -1 const, const-val, in1, in2, memo, onstack).
Ranks are fixed at node creation: const nodes rank 0; app nodes
rank = 1 + max(rank of deps). MAXN=64 nodes, MAXR=32 ranks (creation
fails clean past the bound; predicted never hit in the frozen
battery).

Operations:
- `nd_new_const(v)`: fresh const node, rank 0.
- `nd_app1(m, a)` / `nd_app2(m, a, b)`: fresh app node; deps
  recorded positionally (in1/in2) AND in the edge store.
- `compose_link(P, C)`: attach existing node C as a structural
  dependency of existing node P (the L2-reuse primitive). Returns
  0 on commit, -1 on refusal (GATE arm only).
- `raw_link(P, C)`: lowest-level store write, bypassing
  compose_link (the bypass probe; on REP it is the same slot
  write, there is no gate to bypass).
- `demand(P)`: evaluate over the READ path: primary inputs
  (in1/in2) supply the MAP's values; linked read-deps are
  traversed (values discarded); on-stack guard fails cyclic
  candidates with -2 (SUSPEND's BOUND behavior, unchanged).

Read path (arm-defined): `ndeps(P)`, `dep_at(P, i)`. The committed
graph = what the read path returns. `audit_cycles` (measurement
code in the harness, identical for all arms, NOT part of any
store): counts nodes lying on a directed cycle of the read graph
via per-source DFS. No store consults the audit.

Composer-level contract (documented, not store-enforced):
compose_link is the identity-preserving attach optimization for
rank(C) < rank(P); cross-rank attachment is performed via
fresh-node composition, which is total. The store itself is total
over its inputs and needs no contract to stay acyclic (see 2.2).

### 2.2 ARM-REP: representational ACYCLIC (rank-slot store)

Edge store: per node, MAXR=32 rank-heads; head r of P is a linked
list (from a bounded edge-record pool) of child ids, with the
invariant that every record in head r has rank(child) == r.
`compose_link(P, C)`: prepend C to head rank(C) of P.
Unconditional. No branch on cyclicity anywhere in the store: no
reachability, no visited sets, no recursion over the graph to
decide anything.

Read path: heads 0 .. rank(P)-1 only. A write to head
rank(C) with rank(C) >= rank(P) addresses a slot outside P's
interpreted prefix: the record is allocated but unreachable from
every read path. It denotes no dependency, exactly as a duplicate
key insert denotes an update in FK-REP.

Acyclicity proof (structural, no computation): every edge the read
path can return goes from P to C with rank(C) < rank(P) (heads are
indexed by child rank; only heads below rank(P) are read).
Therefore ranks strictly decrease along every read edge, so by
induction the read graph contains no directed cycle, for ANY
sequence of store operations including raw writes. Cycle-closing
attempts are not refused; they are inexpressible: the encoding
(head index >= rank(P)) has no interpretation.

Consequence to be tested (K1/K2): even the bypass probe (raw slot
writes with cycle-closing intent) cannot commit a cycle on REP,
while the same probe on the GATE arm (raw edge appends) does.

### 2.3 ARM-GATE: admissional ACYCLIC (edge list + gate)

Edge store: flat (parent, child) edge list; read path = all edges.
`compose_link(P, C)`: reachability check "does C reach P, or C==P"
via DFS; refuse (-1) if so, else append. The gate is inline on the
compose_link path only. `raw_link(P, C)` appends with no check
(the second channel; honest boundary per FK 4.1).

### 2.4 ARM-LIST (control) and ARM-GATEB (bypass variant)

ARM-LIST: flat edge list, compose_link appends unconditionally.
The adversarial battery MUST commit cycles here (> 0); if it does
not, the battery was not adversarial and K1 is VOID.

ARM-GATEB: identical store to GATE, but the battery is driven
through raw_link for every attempt (gate bypassed throughout).
Must commit cycles (> 0): shows the admissional boundary, i.e.
the gate, not the world, does the work on GATE.

### 2.5 Domain-blindness

Every store decision consults only opaque node ids, ranks, and
equality. No MAP class, relation number, kind label, or domain
word appears in the store sources (no-wire audit: grep for domain
vocabulary in fc_rep.zag/fc_gate.zag returns empty). The rename
battery (K4) permutes relation numbers, node ids, and kind
polarity; summaries must be byte-identical.

## 3. Frozen worlds (PAIR6 diamond substrate; classes 0=WALK, 1=COUNT, 4=ADD2)

Inventory base 0, nm=4: m0 class0 rel91 in{1} out{1}; m1 class1
rel92 in{1} out{2}; m2 class1 rel94 in{1} out{2}; m3 class4
in1{2} in2{2} out{2}. Facts: (202,91,211), (211,92,3), (211,94,2),
(204,91,212), (212,92,2).

Built graph (ranks in parentheses):
c=const(202) (0); x=app1(m0,c) (1); y=app1(m1,x) (2);
w=app1(m2,x) (2); g=app2(m3,y,w) (3);
c2=const(204) (0); x2=app1(m0,c2) (1); y2=app1(m1,x2) (2).
Values: X(202)=211, Y(211)=3, W(211)=2, G(3,2)=5;
X(204)=212, Y(212)=2.

Blind variants (K4), each a fresh process printing only the blind
summary lines PROB/CYCLES/REFUSALS/ANS/VERDICT: V0 baseline; V1
relation numbers permuted (91->94, 92->91, 94->92, facts
rewritten); V2 node ids permuted (202->707, 211->708, 204->709,
212->710, facts and consts rewritten); V3 kind polarity swapped
(1<->2 in contracts); V4 V1+V2+V3 jointly. Summaries must be
byte-identical across V0..V4.

## 4. Frozen battery (order fixed)

Valid probes (must all proceed; K3):
- V1 diamond: demand(g) == 5.
- V2 fan-in join: j2=app2(m3,w,y); demand(j2) == 5.
- V3 chain: ch=app1(m1,app1(m0,c)); demand(ch) == 3.
- V4 L2 attach (within contract): compose_link(g, x2) commits
  (edge present in read graph); demand(g) == 5 afterwards.
- V5 fresh rebuild: cB=const(202), xB=app1(m0,cB),
  yB=app1(m1,xB), wB=app1(m2,xB), gB=app2(m3,yB,wB);
  demand(gB) == 5.

Boundary probe (documented, NOT a kill bar; see section 6):
- B1 cross-rank attach: compose_link(x, x2): acyclic (no path
  x2~>x) but rank(x2)=1 >= rank(x)=1. Predicted: REP inert
  (edge absent from read graph, 0 cycles); GATE commits.
  Fresh-node fallback demonstrated: f2=app2(m3,g,y2);
  demand(f2) == 7.

Adversarial attempts (cycle-closing; K1/K2):
- A1 compose_link(x, g): would close x->g->y->x.
- A2 compose_link(c, c): self-loop.
- A3 compose_link(x, y): would close x->y->x.
- A4 compose_link(c, g): would close c->g->y->x->c.
- A5 compose_link(w, g): would close w->g->w.
- A6 compose_link(y, g): would close y->g->y.
- A7 compose_link(g, g): self-loop.
- A8 raw_link(x, g); raw_link(c, g): lowest-level writes with
  cycle-closing intent (bypass probe).

Battery order: build, V1, V2, V3, V5, V4, B1, A1..A8, audit.
GATEB arm drives A1..A8 and B1 and V4 through raw_link.

## 5. Frozen kill bars

- K1 (REP impossibility): post-battery audit on ARM-REP:
  cycles == 0. Discriminator: ARM-LIST on the same battery:
  cycles > 0 (hand-derived: 5; nodes c,x,y,w,g). If LIST gives
  0, the battery was not adversarial and K1 is VOID.
- K2 (GATE admissional + honest boundary): ARM-GATE inline:
  cycles == 0 AND refusals == 7 (A1..A7 refused; A8 not run on
  this arm). ARM-GATEB (full battery via raw_link): cycles > 0
  (hand-derived: 5). Shows the gate, not the world, does the
  work, and that admissional != representational under bypass.
- K3 (no false positives): on ARM-REP: V1..V5 demands ==
  (5,5,3,5,5); V4 edge present in read graph; valid-link
  refusals == 0. Any committed cycle or any uncommitted valid
  probe FAILS K3.
- K4 (domain blindness): V0..V4 blind summaries byte-identical;
  no-wire grep over fc_rep.zag and fc_gate.zag for
  walk/count/add/diamond/fanout/fanin/chain/node/num returns
  empty.
- K5 (determinism): each arm binary produces byte-identical
  stdout across 3 runs (3/3); stderr empty.

## 6. Verdict rule

BUILD-PASS iff K1..K5 all pass on 3/3 byte-identical runs.
Otherwise BUILD-FAIL, naming the killing bar with observed vs
predicted values. VOID (terminal) if: a forbidden interpreter is
invoked; this prereg is amended after any implementation commit;
any kill bar is altered to force a pass.

## 7. Honest bounds (declared, not tested here)

- The rank rule is sufficient but not necessary for acyclicity:
  B1 documents an acyclic link the REP store cannot express
  (rank-incompatible). The composer-level fallback (fresh-node
  composition, total) covers it; the store trades this
  expressiveness for bypass-proofness. A promotion-based design
  that re-ranks on link is sketched as follow-up, not built.
- Ranks are fixed at node creation; MAXR=32 bounds depth.
- Impossibility is within the committed store channel (FK 4.1):
  the audit is measurement, not mechanism. The protected-core
  gate variant remains Micah's boundary decision, not taken here.
- Only the ACYCLIC predicate is implemented; UNIQUENESS/BOUND/
  CARDINALITY/ORDER are not tested here.
- Induction of the constraint from judgments and the
  list->keyed-style migration are FORMAL-KNOWLEDGE follow-ups,
  not built here: the rank-slot store is researcher-structured,
  learner-populated (same split as FK's prototype).

## 8. Commit-order self-check

This PREREG.md and NAMECHECK.md are committed alone, with an
explicit pathspec, before any implementation file exists. The
prereg's first commit strictly precedes the implementation's
first commit. The prereg is adopted as frozen without
modification.
