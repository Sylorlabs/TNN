# PREREG.md -- FORMAL-COMPOSE-PORT: rank-slot store as the edge store
# for live L2 attach ops

Date: 2026-10-03. Worker: FORMAL-COMPOSE-PORT. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_port/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE REPORT.md (BUILD-PASS K1-K5;
rank-slot store REP: cycles=0 refusals=0 under 7 cycle attempts +
2 raw-write bypasses; GATEB cycles=5 shows admissional collapses
under bypass; suggested follow-up "port the rank-slot store into
a live composition lane as the edge store for L2 attach ops
(extend/specialize/graft)"); L2-EXTEND-XDOMAIN and
L2-SPECIALIZE-XDOMAIN (the attach-op semantics being ported).

This preregistration freezes the mechanism, the worlds, the
adversarial battery, and the kill bars (K1-K5) BEFORE any
implementation file exists. Status of everything below: FROZEN.
Any deviation requires a prereg amendment committed before the
deviating run.

## 1. The gap (why this experiment exists)

FORMAL-COMPOSE proved representational ACYCLIC for a
composition edge store with the missing `compose_link(P, C)`
operation, but on a synthetic diamond substrate: the valid
probes were assembly-shaped (diamond, fan-in, chain, fresh
rebuild), not L2-shaped. The open question, and the suggested
follow-up verbatim from the FORMAL-COMPOSE report, is whether
the rank-slot store works as the edge store for live L2 attach
operations: extend (attach an independently built extension
leg under an existing composite), specialize (attach a binding
const under an existing node), graft (attach an existing
composite from a second structure under an existing composite
of the first). Two failure modes would refute the port:
(1) attach ops that L2 reuse needs stop functioning (false
positives from the rank rule), or (2) the adversarial
cycle-closing attach attempts become committable.

## 2. Frozen mechanism

### 2.1 Composition edge store (all arms)

Port of the FORMAL-COMPOSE substrate. Node record (learner-state
arena S): (rank, map-id | -1 const, const-val, in1, in2, memo,
onstack). Ranks fixed at creation: const rank 0; app rank =
1 + max(rank of deps). MAXN=64 nodes, MAXR=32 ranks.

Operations:
- `nd_new_const(v)`, `nd_app1(m, a)`, `nd_app2(m, a, b)`:
  fresh nodes; construction deps recorded positionally AND in
  the arm edge store via `store_app_edge`.
- `compose_link(P, C)`: the L2 attach primitive. Attaches
  existing node C as a structural dependency of existing node
  P. Total on REP and LIST (returns 0); gated on GATE
  (returns -1 on refusal, 0 on record).
- `raw_link(P, C)`: lowest-level write. On REP identical to the
  slot write (no gate to bypass); on GATE/GATEB/LIST the raw
  flat-list append.

Four arms sharing one base:
- `pc_rep.zag` (ARM-REP): the rank-slot store ported from
  FORMAL-COMPOSE fc_rep.zag: per-item 32 rank-heads; head r
  holds edge records whose child has rank r; compose_link
  prepends C to head rank(C) unconditionally; read path =
  heads 0..rank(P)-1. No cyclicity branch anywhere (no
  reachability, no visited sets, no graph search).
- `pc_gate.zag` (ARM-GATE): flat edge list + inline
  reachability gate on compose_link (refuse -1 if C==P or C
  reaches P).
- `pc_gateb.zag` (ARM-GATEB): identical store to GATE; battery
  driven through raw_link throughout (gate bypassed).
- `pc_list.zag` (ARM-LIST): unconstrained control, flat list,
  unconditional record.

### 2.2 World (frozen)

Arena A MAPs: m0 WALK rel 91 (structure-X entry), m1 COUNT rel
92 (X fold), m2 COUNT rel 94 (X fold2), m3 ADD2, m4 WALK rel 7
(structure-Y entry), m5 COUNT rel 8 (Y fold).

Facts: 202 -91-> 211; 211 -92-> {901,902,903}; 211 -94->
{911,912}; 204 -7-> 212; 212 -8-> {904,905}.

Structure X: c=const(202) r0; x=app1(m0,c) r1; y=app1(m1,x) r2;
w=app1(m2,x) r2; g=app2(m3,y,w) r3. demand(g)=5.
Structure Y: c2=const(204) r0; x2=app1(m4,c2) r1;
y2=app1(m5,x2) r2. demand(y2)=2.
Extension leg (independently built, the L2-EXTEND artifact):
ec=const(202) r0; ex=app1(m0,ec) r1; ew=app1(m1,ex) r2.
demand(ew)=3.

Rename variants (blind battery): vr permutes the three A
relations (91->94, 92->91, 94->92, facts and MAPs together);
vn permutes subjects (202->707, 211->708, 204->709, 212->710);
vk swaps kind polarity (1<->2); V4 = all three jointly.
Demand values are invariant across variants (5, 2, 3).

## 3. Frozen attach battery (pc_main.zag)

Order: build, V1, V2, V3, B1, A1..A7, A8, audit. Each arm
prints `PC-ARM <name>`, `PC-VALID ...`, `PC-ADV cycles=...
refusals=...`, `PC-BOUNDARY ...`, `PC-END`.

### 3.1 Valid L2 attach probes (must all function)

- V1 EXTEND: battery_link(g, ew). Attach the independently
  built extension leg root ew (rank 2) under existing composite
  g (rank 3). Expect link=0, present=1, demand(g)=5.
- V2 SPECIALIZE: battery_link(w, c). Attach binding const c
  (rank 0) under existing node w (rank 2). Expect link=0,
  present=1, demand(w)=2.
- V3 GRAFT: battery_link(g, y2). Attach existing composite
  y2 (rank 2, structure Y) under existing composite g
  (rank 3, structure X). Expect link=0, present=1,
  demand(g)=5.

### 3.2 Boundary probe (informational, disclosed in advance)

- B1: battery_link(x, x2). rank(x2)=1 >= rank(x)=1: acyclic
  but outside REP's interpreted prefix (the sufficient-but-not-
  necessary boundary found in FORMAL-COMPOSE). Expect REP:
  link=0 present=0 (inert); GATE/LIST/GATEB: link=0 present=1
  (committed, no cycle).

### 3.3 Adversarial attach probes (cycle-closing intent)

A1: battery_link(x, g)   (g transitively depends on x)
A2: battery_link(g, g)   (self-attach)
A3: battery_link(y, g)   (g transitively depends on y)
A4: battery_link(y2, g)  (after V3 committed g->y2)
A5: battery_link(ew, ew) (self-attach on the extension root)
A6: battery_link(c, y)   (y transitively depends on c)
A7: battery_link(c2, c2) (self-attach)
Each contributes 1 to refusals iff battery_link returns != 0.
A8 (bypass probe; runs on REP, GATEB, LIST; NOT on GATE-inline
per the frozen design, mirroring FORMAL-COMPOSE): raw_link(x,g);
raw_link(c,g).

### 3.4 Cycle audit

Independent measurement-only audit (identical for all arms):
counts items lying on a directed cycle of the READ graph.

## 4. Hand-derived predictions (must match stdout bytes)

Valid probes (all arms): ext_link=0 ext_present=1 ext_dem=5;
spec_link=0 spec_present=1 spec_dem=2; graft_link=0
graft_present=1 graft_dem=5. Valid-attach refusals = 0 on
every arm.

- REP: cycles=0, refusals=0. B1: b1link=0 b1present=0.
- GATE: cycles=0, refusals=7 (A1..A7 all refused: A1 g reaches
  x; A2 self; A3 g reaches y; A4 g reaches y2 via V3; A5
  self; A6 y reaches c via x; A7 self). B1: b1link=0
  b1present=1.
- GATEB: cycles=8, refusals=0. B1: b1link=0 b1present=1.
- LIST: cycles=8, refusals=0. B1: b1link=0 b1present=1.

Cycle audit hand-derivation for LIST/GATEB (edge sets
identical: V1,V2,V3,B1,A1..A7,A8 all committed):
nodes on directed cycles: c (c->y via A6, y->x->c),
x (x->g via A1/A8, g->y->x), y (y->g via A3, g->y),
w (w->x, x->g->w), g (g->g via A2), c2 (c2->c2 via A7),
y2 (y2->g via A4, g->y2 via V3), ew (ew->ew via A5).
x2, ec, ex lie on no cycle. Total = 8.

## 5. Kill bars

- **K1 (REP impossibility under the L2 attach battery)**:
  PASS iff REP cycles=0 AND REP refusals=0 on pc_main.
  Discriminator: LIST cycles=8 (>=1) on the same battery, so
  the battery was genuinely adversarial; if LIST cycles=0
  then K1 is VOID.
- **K2 (admissional gate + honest bypass boundary)**:
  PASS iff GATE cycles=0 AND GATE refusals=7 AND GATEB
  cycles=8 (>=1). The gate does the work on GATE; bypassing
  it commits cycles; REP survives the same bypass probe
  (A8 raw writes) with cycles=0.
- **K3 (no false positives on L2 attach ops)**:
  PASS iff on REP (and in fact on every arm):
  ext_present=spec_present=graft_present=1,
  ext_dem=5, spec_dem=2, graft_dem=5, and valid-attach
  refusals=0. Any refused valid attach or wrong demand
  value FAILs.
- **K4 (domain blindness)**: pc_blind.zag runs V0..V4 (vr, vn,
  vk, all-joint) as fresh processes per arm; each prints one
  identifier-free summary `PC-BLIND V<i> ANS= CYCLES=
  REFUSALS= ATT=` (ATT = graft presence after the blind
  attach). PASS iff the five lines are byte-identical within
  arm: REP => ANS=5 CYCLES=0 REFUSALS=0 ATT=1 on all five;
  GATE => ANS=5 CYCLES=0 REFUSALS=7 ATT=1 on all five. Plus
  a no-wire grep audit: domain vocabulary
  (walk/count/add/extend/specialize/graft/diamond/node/num)
  returns 0 hits on pc_rep.zag and pc_gate.zag.
- **K5 (determinism)**: all six binaries (pc_rep, pc_gate,
  pc_gateb, pc_list, pc_blind_rep, pc_blind_gate) 3/3
  byte-identical stdout, stderr empty on all 18 runs, zero
  analyzer warnings at compile.

## 6. What this does NOT claim

- The rank-slot store remains researcher-structured,
  learner-populated (same split as FORMAL-COMPOSE).
- The B1 boundary is inherited, not fixed: fixed-rank REP is
  sufficient-but-not-necessary; promotion-based re-ranking
  remains the sketched follow-up. The composer-level
  fresh-node fallback covers the B1 class.
- One predicate (ACYCLIC), one substrate family, small
  battery. Generality to other L2 substrates is not shown.
