# PREREG.md -- FORMAL-COMPOSE-E2E: the actual L2 learner stacks on the
# rank-slot store, end to end

Date: 2026-10-03. Worker: FORMAL-COMPOSE-E2E. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_e2e/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE-PORT REPORT.md (BUILD-PASS K1-K5;
ARM-REP rank-slot store ported as the edge store for live L2 attach
ops extend/specialize/graft; valid attaches function, 7
cycle-closing attempts + 2 raw-write bypasses inexpressible,
cycles=0 refusals=0; ARM-LIST discriminator cycles=8; suggested
follow-up verbatim: "Drive the actual L2 learner stacks
(L2-EXTEND-XDOMAIN / L2-SPECIALIZE-XDOMAIN learners) against the
rank-slot store instead of their current unconstrained edge
stores, to test this port end to end."); L2-EXTEND-XDOMAIN
REPORT.md (L2-EXTEND-XDOMAIN-PASS K1-K8); L2-SPECIALIZE-XDOMAIN
REPORT.md (L2-SPECIALIZE-XDOMAIN-PASS K1-K8).

This preregistration freezes the mechanism, the source surgery,
the adversarial battery, the hand-derived predictions, and the
kill bars (EK1-EK7) BEFORE any implementation file exists.
Status of everything below: FROZEN. Any deviation requires a
prereg amendment committed before the deviating run.

## 1. The gap (why this experiment exists)

FORMAL-COMPOSE-PORT proved the rank-slot store works for L2-shaped
attach operations, but on a synthetic two-structure substrate whose
valid probes were battery-shaped (extend/specialize/graft issued by
the driver). The actual L2-EXTEND-XDOMAIN and L2-SPECIALIZE-XDOMAIN
learners were not re-run on the store. Two failure modes would refute
the end-to-end port: (1) the learners' real provenance/delivery edges
(type-16 promotion provenance, type-14 answer-node links) stop being
visible or stop being recorded correctly under the rank rule (false
positives breaking valid L2 reuse), or (2) adversarial
cycle-closing attaches issued through the same edge interface the
learner uses become committable (representational constraint fails
on the real stacks).

## 2. Frozen mechanism

### 2.1 Source surgery (exact, minimal, frozen)

EX stack (from l2_extend_xdomain/):
- `ex_learner.zag`: copy of learner.zag with the edge-store
  functions REMOVED (e_add, e_count, e_has, e_has_to, ex_eoth;
  the contiguous `// ---- edges ----` block) and three hook calls
  ADDED: `es_item_new(st,n)` at the success exit of m_teach and of
  map_create (n = the new MAP id), and `es_item_new(st,aid)` in
  ex_deliver (aid = 40+nn, the answer-node id). Every other byte
  of learner logic is unchanged.
- `ex_world.zag`: byte-identical copy of world.zag.
- `ex_driver_e2e.zag`: new experiment driver (section 2.4).

XS stack (from l2_specialize_xdomain/):
- `xs_learner_e2e.zag`: copy of xs_learner.zag with the xs_edge
  function REMOVED, its two call sites in xs_promote replaced by
  `e_add(st,n,sm,16)` / `e_add(st,n,smap,16)`, and `es_item_new(st,n)`
  ADDED at the success exits of m_teach and xs_promote (n = the new
  MAP id). Every other byte of learner logic is unchanged.
- `xs_world.zag`: byte-identical copy of xs_world.zag.
- `xs_driver_e2e.zag`: new experiment driver (section 2.4).

A diff of each e2e learner against its parent must show ONLY the
removed edge-store block, the hook calls, and (XS) the two call-site
renames. No other learner-logic change is permitted.

### 2.2 The store files (the only new mechanism; frozen interface)

`es_rep.zag` (ARM-REP, shared by both stacks): the rank-slot store
ported from FORMAL-COMPOSE-PORT pc_rep.zag, extended with edge
types. Records are (child, type, next), 12 bytes. Structural
vocabulary only (item, rank, head, link, edge, store, slot); the
K4-style no-wire grep audit (walk/count/add/extend/specialize/
graft/diamond/node/num) must return 0 hits.

Items: 0..23. MAP ids map to items 0..15; extend-stack answer-node
ids 40..47 map to items 16..23. Rank = creation order, assigned by
es_item_new: a creation-time topological rank, valid because the
learners only ever link a newer item to an older one, so every
valid edge goes from strictly higher to strictly lower rank.

Layout in st (both stacks; XS driver grows st to 8192):
- 1984: rank table, 24 bytes (255 = unregistered; lazily
  initialized by es_ensure on first use).
- 2008: rank counter (next rank); 2009: init flag.
- 2048: heads, 24 items * 32 ranks * 4 bytes = 3072.
- 5120: edge pool, 128 records * 12 bytes = 1536.
- 6656: pool cursor (i32).

Interface (identical names/signatures in all three store files):
- `es_item_new(st, id)`: register id (raw id; mapped internally);
  REP assigns creation-order rank and inits 32 heads to -1;
  LIST is a no-op.
- `e_add(st, from, to, typ)`: REP: dedupe via the visible read
  path, then prepend `to` to head rank(to) of item(from),
  UNCONDITIONALLY (no cyclicity branch anywhere). LIST: the
  stack's original flat-store append (EX flavor dedupes, XS
  flavor does not; faithful to each parent).
- `e_count(st, typ)`: number of VISIBLE edges of type typ
  (REP: scan of interpreted prefixes; LIST: flat-table scan).
- `e_has(st, from, to, typ)` / `e_has_to(st, to, typ)`: visible
  edge queries.
- `ex_eoth(st)`: visible edges with type outside {14,16}.
- `es_raw(st, from, to, typ)`: raw slot write. On REP identical
  to the e_add slot write (no gate exists to bypass); on LIST a
  flat append without dedupe.
- `es_audit(st)`: independent measurement-only cycle count:
  number of items (0..23) lying on a directed cycle of the READ
  graph (all visible edges, any type). Same recursive-reachability
  algorithm in all arms.

Read path (REP): heads 0..rank(P)-1 of item(P). A write to head
rank(C) with rank(C) >= rank(P) lands outside P's interpreted
prefix: the record exists but denotes no edge. Every visible edge
therefore goes from strictly higher to strictly lower rank, so the
read graph is acyclic for ANY operation sequence, including raw
writes. Cycle-closing attaches are not refused; they are
inexpressible. This is the exact representational argument from
FORMAL-COMPOSE-PORT, now running under the real L2 learners.

`es_list_ex.zag` (ARM-LIST, extend stack): faithful copy of the
original learner.zag edge semantics: flat table 64x4B @960,
count @st[2], dedupe on e_add. es_raw appends without dedupe.
es_audit runs the same algorithm over the flat table (all records
visible).

`es_list_xs.zag` (ARM-LIST, specialize stack): faithful copy of
the original xs_learner.zag edge semantics: flat table 64x4B
@1040, count @st[2], NO dedupe on xs_edge (now e_add). es_raw
identical append. es_audit over the flat table.

### 2.3 Binaries (pinned znc 2026.07.0-dev, safebin)

- ex_rep_bin:  ex_learner.zag + ex_world.zag + es_rep.zag +
  ex_driver_e2e.zag
- ex_list_bin: ex_learner.zag + ex_world.zag + es_list_ex.zag +
  ex_driver_e2e.zag
- xs_rep_bin:  xs_learner_e2e.zag + xs_world.zag + es_rep.zag +
  xs_driver_e2e.zag
- xs_list_bin: xs_learner_e2e.zag + xs_world.zag + es_list_xs.zag +
  xs_driver_e2e.zag

Forward references (learner -> es_item_new) are permitted: the
pinned znc resolves them (precedent: pc_base.zag -> arm_nd_init
in FORMAL-COMPOSE-PORT).

### 2.4 Drivers (frozen)

ex_driver_e2e.zag:
- Runs the four original arms with the original queries:
  FULL (QA/QB/Q2/Q2B), NOEXTEND (QA/QB/Q2), ABLATE-X (QA/QB,
  retire mA, Q2), FRESH (Q2 only).
- Computes the original in-Zag bars k1,k2,k3,k4,k5,k8 with the
  original frozen logic and frozen numbers (F-COUNT: FULL Q2
  A_SEARCH=272 A_EXEC=2; falsifiers silent).
- Then the adversarial battery on the FULL arm state stF
  (smid from SRC_ID32 = get32(stF,1268); zid = stF[1]-1;
  qa_via captured; QA aid = 40):
  A1 e_add(stF,smid,zid,16); A2 e_add(stF,zid,zid,16);
  A3 e_add(stF,qa_via,40,14); R1 es_raw(stF,smid,zid,16);
  R2 es_raw(stF,zid,zid,16).
- Prints `E2E-EX t16= a1= a2= a3= t14= audit= v16= v14=` where
  t16=e_count(16), a1=e_has(smid,zid,16), a2=e_has(zid,zid,16),
  a3=e_has(qa_via,40,14), t14=e_count(14), audit=es_audit(stF),
  v16=e_has(zid,smid,16), v14=e_has(40,qa_via,14).

xs_driver_e2e.zag:
- Runs the three original arms with the original queries:
  FULL (QA/QB/Q2/Q2B/Q2C/Q2D), GENERAL (QA/QB/Q2/Q2B),
  ABLATE-X (QA/QB, retire mG, Q2). st grown to 8192.
- Computes the original in-Zag bars k1,k2,k3,k4,k5,k8 with the
  original frozen logic and frozen numbers (F-COUNT per-query
  S/E from the XS report); arm_close reimplemented on the store
  interface (ne = visible 14+16+eoth counts; t16 = e_count(16);
  bad = (ex_eoth!=0)).
- Then the adversarial battery on the FULL arm state stF
  (n = st[1]-1; sm1,sm2 derived by scanning mid in 0..nm-1 for
  e_has(stF,n,mid,16)):
  A1 e_add(stF,sm1,n,16); A2 e_add(stF,n,n,16);
  A3 e_add(stF,sm2,n,16); R1 es_raw(stF,sm1,n,16);
  R2 es_raw(stF,n,n,16).
- Prints `E2E-XS t16= a1= a2= a3= audit= v1= v2=` where
  t16=e_count(16), a1=e_has(sm1,n,16), a2=e_has(n,n,16),
  a3=e_has(sm2,n,16), audit=es_audit(stF),
  v1=e_has(n,sm1,16), v2=e_has(n,sm2,16).

## 3. Hand-derived predictions (must match stdout bytes)

### 3.1 Extend stack

Original behavior (both arms; edge ops do not tick, so F-COUNT
is unchanged from L2-EXTEND-XDOMAIN):
k1=k2=k3=k4=k5=k8=1, falsifiers silent; FULL t16=1 (pre-adversarial);
NOEXTEND/ABLATE-X/FRESH t16=0.

Creation ranks on REP (FULL): mD=0, mA=1, mB0=2, aid40=3,
aid41=4, zid3=5, aid42=6, aid43=7.

REP adversarial (hand derivation):
- Valid edges visible: 3->1 (head 1 of item 3; 1<5), 40->1,
  41->2, 42->3, 43->3. t16=1, t14=4, v16=1, v14=1.
- A1 (1->3): rank(3)=5 >= rank(1)=1 -> head 5 of item 1,
  outside interpreted prefix (heads 0..0). Invisible.
- A2 (3->3): head 5 of item 3, prefix is heads 0..4. Invisible.
- A3 (1->40): rank(item16)=3 >= rank(1)=1 -> head 3 of item 1.
  Invisible.
- R1/R2: same slot writes as A1/A2. Invisible.
- a1=a2=a3=0, audit=0.
Expected: `E2E-EX t16=1 a1=0 a2=0 a3=0 t14=4 audit=0 v16=1 v14=1`.

LIST adversarial (hand derivation): flat table after FULL has 5
records (40->1, 41->2, 3->1, 42->3, 43->3); A1/A2/A3 append 3
(EX e_add dedupes: none are dupes); R1/R2 append 2 more.
t16 = 1+1+1+1+1 = 5. a1=a2=a3=1. Cycle audit over the read graph
(items: 1 deps {3,16,3}; 3 deps {1,3,3}; 16 deps {1}; 17 deps
{2}; 18,19 deps {3}): items on directed cycles are 1
(1->3->1), 3 (3->3, 3->1->3), 16 (16->1->16). audit=3.
Expected: `E2E-EX t16=5 a1=1 a2=1 a3=1 t14=5 audit=3 v16=1 v14=1`.

### 3.2 Specialize stack

Original behavior (both arms): k1=k2=k3=k4=k5=k8=1, falsifiers
silent; FULL t16=2 (pre-adversarial); GENERAL/ABLATE-X t16=0.

Creation ranks on REP (FULL): mD2=0, mG=1, mB0=2, mS(n=3)=3.
sm1=1 (mG), sm2=2 (mB0) derived by scan.

REP adversarial:
- Valid: 3->1 (head 1 of item 3; 1<3), 3->2 (head 2; 2<3).
  t16=2, v1=v2=1.
- A1 (1->3): head 3 of item 1, prefix heads 0..0. Invisible.
- A2 (3->3): head 3 of item 3, prefix 0..2. Invisible.
- A3 (2->3): head 3 of item 2, prefix 0..1. Invisible.
- a1=a2=a3=0, audit=0.
Expected: `E2E-XS t16=2 a1=0 a2=0 a3=0 audit=0 v1=1 v2=1`.

LIST adversarial: flat table after FULL has 2 records
(3->1, 3->2); A1/A2/A3 append 3 (no dedupe in xs flavor);
R1/R2 append 2. t16 = 2+3+2 = 7. a1=a2=a3=1. Audit (item 1
deps {3,3}; item 2 deps {3}; item 3 deps {1,2,3,3}): items on
cycles are 1 (1->3->1), 2 (2->3->2), 3 (3->3). audit=3.
Expected: `E2E-XS t16=7 a1=1 a2=1 a3=1 audit=3 v1=1 v2=1`.

## 4. Kill bars

- **EK1 (valid extends work on the rank-slot store)**: PASS iff
  ex_rep_bin prints k1=k2=k3=k4=k5=k8=1 AND falsifiers silent
  (ff=0). The learner's real extension behavior (learner-chosen
  k=4, Z promotion, t16 provenance, exact F-COUNT) is unchanged
  on REP.
- **EK2 (REP impossibility on the extend stack)**: PASS iff
  ex_rep_bin prints `E2E-EX t16=1 a1=0 a2=0 a3=0 t14=4 audit=0
  v16=1 v14=1`. Every cycle-closing attach through the learner's
  own edge interface (plus raw-write bypass) is inexpressible;
  every valid edge stays visible.
- **EK3 (LIST discriminator, extend)**: PASS iff ex_list_bin
  prints `E2E-EX t16=5 a1=1 a2=1 a3=1 t14=5 audit=3 v16=1
  v14=1`. If list audit=0 then EK2 is VOID (battery not
  adversarial).
- **EK4 (valid specializes work on the rank-slot store)**: PASS
  iff xs_rep_bin prints k1=k2=k3=k4=k5=k8=1 AND falsifiers
  silent (ff=0). The learner's real specialization (nf=3,
  dual provenance 3->1 and 3->2, exact F-COUNT) is unchanged
  on REP.
- **EK5 (REP impossibility on the specialize stack)**: PASS iff
  xs_rep_bin prints `E2E-XS t16=2 a1=0 a2=0 a3=0 audit=0 v1=1
  v2=1`.
- **EK6 (LIST discriminator, specialize)**: PASS iff xs_list_bin
  prints `E2E-XS t16=7 a1=1 a2=1 a3=1 audit=3 v1=1 v2=1`. If
  list audit=0 then EK5 is VOID.
- **EK7 (determinism)**: all four binaries 3/3 byte-identical
  stdout, stderr empty on all 12 runs, zero analyzer warnings
  at compile.

## 5. What this does NOT claim

- The rank-slot store remains researcher-structured,
  learner-populated (same split as FORMAL-COMPOSE and
  FORMAL-COMPOSE-PORT). Constraint induction from judgments is
  still a FORMAL-KNOWLEDGE follow-up.
- Creation-order rank is sufficient-but-not-necessary (the B1
  boundary is inherited): an acyclic attach from an older item
  to a newer one would go inert on REP. Neither L2 learner
  issues such attaches in these worlds; promotion-based
  re-ranking remains the sketched follow-up.
- One predicate (ACYCLIC), two L2 stacks, small battery. No
  generality claim beyond these stacks.
- The adversarial battery is driver-issued, not learner-issued:
  it tests the store under the real learner's state, not an
  adversarial learner.
