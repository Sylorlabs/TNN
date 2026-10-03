# PREREG.md -- FORMAL-COMPOSE-RERANK: promotion-based re-ranking
# for the B1 boundary

Date: 2026-10-03. Worker: FORMAL-COMPOSE-RERANK. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_rerank/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE REPORT.md (BUILD-PASS K1-K5;
ARM-REP rank-slot store; boundary B1 documented: acyclic
cross-rank attach link(x,x2) with rank(x2) >= rank(x) goes inert
on REP, b1present=0; GATE/LIST commit it; "promotion-based
re-ranking remains the sketched follow-up"); FORMAL-COMPOSE-PORT
REPORT.md (BUILD-PASS K1-K5; rank-slot store as L2 attach-op edge
store); FORMAL-COMPOSE-E2E REPORT.md (BUILD-PASS EK1-EK7; actual
L2-EXTEND-XDOMAIN / L2-SPECIALIZE-XDOMAIN learners on the
rank-slot store end to end; REP vs LIST byte-identical except
the E2E summary line; suggested follow-up verbatim:
"promotion-based re-ranking with these stacks as test bed").

This preregistration freezes the mechanism, the battery, the
hand-derived predictions, and the kill bars (RR1-RR6) BEFORE any
implementation file exists. Status of everything below: FROZEN.
Any deviation requires a prereg amendment committed before the
deviating run.

## 1. The gap (why this experiment exists)

FORMAL-COMPOSE's rank-slot store (ARM-REP) makes cycles
representationally impossible: the read graph always has
strictly decreasing ranks, so no write sequence, not even raw
slot writes, can commit a cycle. The price is the B1 boundary:
the rank rule is sufficient but not necessary for acyclicity. An
acyclic attach x <- x2 (x2 as dependency of x) with
rank(x2) >= rank(x) is written to a head outside x's interpreted
prefix and goes inert. FORMAL-COMPOSE-E2E confirmed the learners
never issue such attaches in their worlds, so B1 never fired
there; but the boundary is real expressiveness left on the
floor, and the sketched follow-up is promotion-based re-ranking:
when a valid acyclic attach is blocked by rank order, re-rank
the nodes to admit it, while keeping cycles structurally
impossible.

Two honest outcomes are possible. (A) A promotion design that
is representational (no admissional gate: no refusal branch, no
reachability check that refuses) and admits every acyclic attach
while keeping every cycle inexpressible. (B) Evidence that the
B1 class forces an admissional decision somewhere, i.e. a proof
sketch plus a failing bar. This prereg bets on (A) with a
concrete mechanism; section 6 states exactly what would refute
it.

## 2. Frozen mechanism

### 2.1 es_rerank.zag: rank-slot store with promotion on link

Same frozen interface as es_rep.zag (es_item_new, e_add, e_has,
es_ndeps, es_dep_at, e_count, e_has_to, ex_eoth, es_raw,
es_audit, es_item_of) plus three diagnostics (es_promotes,
es_maxrank, es_diverge). Items 0..23, same id mapping (MAP ids
0..15, answer ids 40..47). Structural vocabulary only
(item, rank, head, link, edge, store, slot, audit, promote,
target, pass); the no-wire grep audit (walk/count/add/extend/
specialize/graft/diamond/node/num and domain verbs) must return
0 hits.

Layout in st (all i32 via get32/set32 on the u8 state; ranks are
no longer bytes because promotion grows them past 255):
- 1984: rank[24], i32 each, -1 = unregistered (96 bytes)
- 2080: next-rank counter, i32
- 2084: init flag, u8
- 2088: maxrank-seen diagnostic, i32
- 2092: promote-count diagnostic, i32 (slow-path links)
- 2096: diverge-flag diagnostic, i32
- 2112: heads, 24 items * 256 ranks * 4 bytes = 24576 bytes
- 26688: edge pool, 256 records * 12 bytes (child-id, type, next)
- 29760: pool cursor, i32

es_item_new assigns rank = counter++ as before (creation order
is still the initial topological rank).

### 2.2 The link operation (frozen pseudocode)

es_link(st, from, to, typ):
  1. register from/to if unregistered (as es_rep.zag).
  2. write the record (child=to) to head rank(to) of item(from),
     unconditionally (the same slot write as REP).
  3. if rank(to) < rank(from): done (fast path; edge readable).
  4. else (slow path): es_promote(st, item(from), item(to)).

e_add = e_has dedupe (unchanged, over the interpreted prefix)
then es_link. es_raw = es_link without dedupe (section 2.4).

es_promote(st, p, c) with rank(c) >= rank(p), p = parent item,
c = child item:
  Phase 1 (compute target ranks; the new edge is NOT an input,
  it is currently unreadable since rank(c) >= rank(p)):
    t := copy of rank[24]; t[p] := rank(c)+1;
    promotes++; 
    repeat up to 23 passes over every READABLE written edge
    Y->W (readable under current ranks: rank(W) < rank(Y)):
      if t[Y] <= t[W]: t[Y] := t[W]+1, mark changed.
    if a 24th pass would still change anything: diverge=1
    (predicted never; RR6 bars diverge=0).
  Phase 2 (apply + relocate):
    for each item w with t[w] > rank(w):
      for each item y: in y's head[rank(w)], move every record
      whose child-item == w to y's head[t[w]] (order irrelevant);
      rank(w) := t[w]; update maxrank-seen.

Why this is correct (frozen argument, tested by RR4):
Phase 1 computes the least fixpoint of t[p]=rank(c)+1 and
t[Y] >= t[W]+1 over readable edges. Readable edges always form
a DAG (strict rank decrease), so with n=24 items, 23 passes
suffice: t*[Y] = max over readable paths Y->*Z of
init(Z)+len, init(p)=rank(c)+1, init(other)=rank, and every
maximizing path has length <= 23. Hence (a) Phase 1 always
converges (diverge=0); (b) t*[Y] > t*[W] for every previously
readable Y->W, so Phase 2 preserves ALL previously readable
edges; (c) for an acyclic attach (no readable path c->*p),
t*[c] = rank(c) < rank(c)+1 = t*[p], so the new edge becomes
readable (its record sits in head rank(c), inside p's prefix);
(d) for a cycle-closing attach (readable path c->*p of length
k>=1), t*[c] >= t*[p]+k, the new edge's record relocates with c
above p's prefix and stays inert, while every old readable edge
is preserved.

### 2.3 Why this is representational, not admissional (frozen)

1. No refusal branch exists. es_link/e_add/es_raw always write
   the record and return void. There is no reachability check,
   no visited set, no "-1" return on the write path. (Grep
   audit over es_rerank.zag for refus/cyclic/reach/visit must
   show no decision branch; the only loop bound is the 23-pass
   computational bound.)
2. Cycles are impossible by structure, exactly as in
   FORMAL-COMPOSE REP: the read graph is {written Y->W :
   rank(W) < rank(Y)}, and ranks strictly decrease along every
   readable edge for ANY rank assignment and ANY write
   sequence, including raw writes. Promotion only changes which
   edges are readable, never the invariant. refusals=0 is
   structural, printed as a constant by the battery.
3. Promotion is a total function of (store, p, c). It never
   consults cyclicity to decide anything. The 23-pass bound is
   a computational bound (longest readable path < 24), not a
   cyclicity test: on a DAG it always converges, and even a
   hypothetical non-convergence would still complete the write
   (the read graph stays a DAG for any t).
4. The sufficient-but-not-necessary character moves: B1
   attaches (acyclic, rank-incompatible) are now admitted by
   re-ranking; cycle-closing attaches remain inexpressible
   (inert), not refused.

### 2.4 es_raw semantics (frozen)

On RERANK there is no gate to bypass, so es_raw is the same
write+promote operation as es_link without dedupe (mirroring
E2E's "on REP there is no gate to bypass, so this is the same
slot write"). The adversarial battery's raw probes therefore
test whether ANY write path can close a cycle. Predicted: no
(cycles=0, probes inert).

### 2.5 Discriminator stores (frozen)

- rr_es_rep.zag: byte-identical copy of es_rep.zag plus three
  stub diagnostics (es_promotes=0, es_maxrank=counter-1,
  es_diverge=0). Proves the B1 battery is genuinely in the B1
  class: same attaches go inert here.
- es_list_rr.zag: unconstrained flat edge list with the same
  interface (e_add appends with dedupe; read path = all edges;
  es_audit identical algorithm). Proves the batteries are not
  VOID: attaches commit here, adversarial closes cycles.

### 2.6 Driver surgery (frozen, mechanical only)

- ex_learner.zag, ex_world.zag, xs_learner_e2e.zag, xs_world.zag:
  byte-identical copies from formal_compose_e2e/ (verified by
  cmp).
- rr_driver_ex.zag: copy of ex_driver_e2e.zag with exactly
  three mechanical changes: (1) the four store states
  z_alloc(8192) -> z_alloc(65536) (es_rerank.zag needs offsets
  past 8192; allocation size is not printed); (2) capture
  rr_prom0 = es_promotes(stF) immediately before the
  adversarial battery; (3) after "L2-EXTEND-XDOMAIN-END",
  call b1_run(ob,atp) then print "RR-EX prom0=".
  rr_driver_xs.zag: analogous (xs_ emit helpers, "RR-XS").
- b1_batt.zag: self-contained B1 battery (b1_-prefixed emit
  helpers + b1_run), catted into all four builds so the
  battery bytes are identical everywhere.
- b1_main.zag: standalone main for the discriminator
  binaries (calls b1_run, single-syscall write).

## 3. Frozen battery

### 3.1 Learner phase (the L2 stacks as test bed)

rr_ex_bin replays the full E2E EX driver (teach, QA/QB/Q2/Q2B,
NOEXTEND, ABLATE-X, FRESH arms, in-Zag k1-k8 bars and
falsifiers) on es_rerank.zag, then the E2E adversarial battery
on the FULL arm state (3 cycle-closing e_add through the
learner's own interface + 2 es_raw bypass probes). rr_xs_bin
does the same for the XS stack. Prediction: every learner-issued
e_add is newer->older (ex_learner.zag:432 e_add(zid,smid,16),
:540 e_add(aid,mid,14); xs_learner_e2e.zag:617-618
e_add(n,sm,16), e_add(n,smap,16); all from-ids strictly newer
than to-ids), so the fast path handles 100 percent of learner
traffic and prom0=0. The adversarial attaches are slow-path and
must go inert with all valid edges preserved (section 2.2(d)).

### 3.2 B1 battery (frozen; runs on a FRESH state st2 in b1_run)

Controlled DAG, fresh ranks. Register ids 4..15 (items 4..15,
ranks 0..11 in registration order).

```
e_add(9,8,1); e_add(9,7,1); e_add(8,7,1);      // X chain
e_add(6,5,1); e_add(6,4,1); e_add(5,4,1);      // Y chain
e_add(4,9,2);                                   // B1a: 4(r0)->9(r5), acyclic (9 !->* 4)
e_add(12,11,1); e_add(12,10,1); e_add(11,10,1); // Z chain
e_add(7,12,2);                                  // B1b: 7(r3)->12(r8), acyclic (12 !->* 7)
e_add(15,14,1); e_add(15,13,1); e_add(14,13,1); // W chain
e_add(13,6,2);                                  // B1c: 13(r9)->6(r14), acyclic (6 !->* 13)
e_add(9,4,2);                                   // ADV1: cycle-closing (4->9 readable)
e_add(12,12,2);                                 // ADV2: self-loop
es_raw(9,4,2); es_raw(12,12,2);                 // ADV3: raw probes
```

Hand-derived rank trace on RERANK (ranks shown as item:rank;
only changed items listed; verified against the frozen
algorithm in 2.2):

- After X,Y edges: ranks = creation order (4:0,5:1,6:2,7:3,8:4,9:5).
- B1a e_add(4,9,2): slow path. t[4]:=6. Pass1: 5->4 gives
  t[5]:=7; 6->5 gives t[6]:=8. Converged. Ranks: 4:6,5:7,6:8.
  New edge 4->9 readable (child 9 at rank 5 < 6). b1a=1.
- Register 10,11,12 -> ranks 6,7,8 (collide harmlessly with
  4,5,6; heads are per-item). Z edges fast.
- B1b e_add(7,12,2): slow path. t[7]:=9. Fixpoint (5 passes):
  4:12, 5:13, 6:14, 7:9, 8:10, 9:11. New edge 7->12 readable
  (child 12 at rank 8 < 9). b1b=1. All old edges preserved
  (e.g. 4->9: child 9 relocated to head 11 < 12).
- Register 13,14,15 -> ranks 9,10,11. W edges fast.
- B1c e_add(13,6,2): slow path. t[13]:=15. Fixpoint (2
  passes): 13:15, 14:16, 15:17. New edge 13->6 readable
  (child 6 at rank 14 < 15). b1c=1.
- ADV1 e_add(9,4,2): slow path, cycle-closing via readable
  4->9. Fixpoint: 9:13, 4:14, 5:15, 6:16, 13:17, 14:18,
  15:19. New edge's record relocates with child 4 to head
  14; item 9 (rank 13) reads heads 0..12: INERT. a1=0. Every
  old readable edge preserved (4->9: child 9 at 13 < 14).
- ADV2 e_add(12,12,2): slow path, self-loop. Fixpoint:
  12:9, 7:10, 8:11. Record relocates with child 12 to head 9;
  item 12 reads 0..8: INERT. a2=0.
- ADV3 es_raw(9,4,2): slow path again. Fixpoint: 9:15,
  4:16, 5:17, 6:18, 13:19, 14:20, 15:21. Inert. a3=0.
  es_raw(12,12,2): slow path. Fixpoint: 12:10, 7:11, 8:12.
  Inert.
- Final: maxrank=21 (item 15), promotes=7, diverge=0,
  audit=0, all 12 type-1 DAG edges readable (vall=1),
  b1a=b1b=b1c=1 (B1 edges survive the later adversarial
  promotions: 4->9 child 9 at 15 < 16; 7->12 child 12 at
  10 < 11; 13->6 child 6 at 18 < 19), t1=12, t2=3.

On REP (fixed ranks): b1a=b1b=b1c=0 (writes land outside the
interpreted prefix), a1=a2=a3=0, audit=0, vall=1, t1=12,
t2=0, maxrank=11, promotes=0, diverge=0.
On LIST (unconstrained): b1a=b1b=b1c=1, a1=1, a2=1, a3=1,
audit=3 (items 4,9 on the 4<->9 cycle; item 12 on its
self-loop), vall=1, t1=12, t2=7, maxrank=11, promotes=0,
diverge=0.

### 3.3 Battery output lines (frozen format)

b1_run prints exactly:
```
B1 b1a=%d b1b=%d b1c=%d a1=%d a2=%d a3=%d audit=%d vall=%d t1=%d t2=%d\n
B1D maxrank=%d promotes=%d diverge=%d\n
```
rr drivers then print `RR-EX prom0=%d\n` / `RR-XS prom0=%d\n`.

## 4. Frozen kill bars RR1-RR6

- RR1 (B1 expressiveness; the boundary addressed): rr_ex and
  rr_xs B1 lines show b1a=b1b=b1c=1. Discriminators:
  b1_rep_bin shows b1a=b1b=b1c=0 (same attaches inert under
  fixed rank: the battery is genuinely in the B1 class);
  b1_list_bin shows b1a=b1b=b1c=1 (unconstrained store
  expresses them). PASS requires all three arms to match.
- RR2 (cycle impossibility, representational): rr_ex B1 line
  a1=a2=a3=0 audit=0; rr_ex E2E-EX line identical to
  formal_compose_e2e/ex_run_rep_1.txt
  (t16=1 a1=0 a2=0 a3=0 t14=4 audit=0 v16=1 v14=1); rr_xs
  E2E-XS line identical to xs_run_rep_1.txt
  (t16=2 a1=0 a2=0 a3=0 audit=0 v1=1 v2=1) and B1 line
  a1=a2=a3=0 audit=0. b1_list_bin audit=3 (battery not VOID).
  refusals=0 structural on RERANK (no refusal branch exists;
  grep audit). Any committed cycle on RERANK, or any
  adversarial attach readable, FAILS the bar.
- RR3 (no regression on the L2 stacks): rr_ex stdout from
  line 1 through "L2-EXTEND-XDOMAIN-END" byte-identical to
  formal_compose_e2e/ex_run_rep_1.txt (k1=k2=k3=k4=k5=k8=1,
  FALSIFIERS 0, F-COUNT as=272 ae=2); rr_xs likewise through
  "L2-SPECIALIZE-XDOMAIN-END" vs xs_run_rep_1.txt (k1-k8
  PASS, FALSIFIERS 0); RR-EX/RR-XS prom0=0 (learners never
  trigger promotion; creation-order ranks suffice for all
  learner traffic).
- RR4 (preservation under promotion): vall=1 and t1=12 on all
  four binaries; on RERANK b1a=b1b=b1c=1 in the B1 line
  printed AFTER the adversarial attaches (B1 edges survive
  later promotions); t2=3 on RERANK (only the 3 B1 edges
  readable among type-2 writes), t2=0 on REP, t2=7 on LIST.
- RR5 (post-promotion adversarial): entailed by RR2+RR4
  ordering (ADV runs after B1a/b/c commit): a1=a2=a3=0 with
  b1a=b1b=b1c=1 simultaneously. A promotion scheme that
  admitted cycles only after re-ranking would fail here.
- RR6 (determinism and hygiene): all four binaries 3/3
  byte-identical stdout, stderr empty on all 12 runs, zero
  new analyzer warning classes vs the E2E parent
  (benign A0102/B0103/E0101/E0102 only), diverge=0 on both
  RERANK binaries, maxrank=21 <= 255 on the B1 state.

## 5. Exact predicted stdout tails (frozen)

rr_ex_bin: [63 lines byte-identical to ex_run_rep_1.txt,
ending "L2-EXTEND-XDOMAIN-END\n"] then
```
B1 b1a=1 b1b=1 b1c=1 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=3
B1D maxrank=21 promotes=7 diverge=0
RR-EX prom0=0
```
rr_xs_bin: [lines byte-identical to xs_run_rep_1.txt through
"L2-SPECIALIZE-XDOMAIN-END\n"] then the same B1/B1D lines,
then `RR-XS prom0=0`.
b1_rep_bin:
```
B1 b1a=0 b1b=0 b1c=0 a1=0 a2=0 a3=0 audit=0 vall=1 t1=12 t2=0
B1D maxrank=11 promotes=0 diverge=0
```
b1_list_bin:
```
B1 b1a=1 b1b=1 b1c=1 a1=1 a2=1 a3=1 audit=3 vall=1 t1=12 t2=7
B1D maxrank=11 promotes=0 diverge=0
```

## 6. Falsification conditions (what would refute the design)

- Any RERANK run with es_audit > 0: the representational
  claim dies; outcome (B), report the proof attempt as failed.
- Any RERANK B1 line with b1a/b1b/b1c = 0: promotion does not
  admit the B1 class; outcome (B).
- vall=0 or any t1 != 12 on RERANK: promotion breaks valid
  edges; the design is lossy and the bar fails honestly.
- diverge=1: the fixpoint did not converge; investigate
  before any verdict (predicted impossible by 2.2(a)).
- prom0 != 0: a learner attach took the slow path; RR3's
  byte-identity prediction may still hold, but the
  "learners never need promotion" sub-claim fails and must
  be reported.
- If b1_rep_bin shows any b1*=1, the battery is not in the
  B1 class (VOID); if b1_list_bin shows audit=0, the
  adversarial battery is not adversarial (VOID).

## 7. Commit-order self-check

PREREG.md (+ NAMECHECK.md, no implementation) is committed
alone before any .zag file exists. The prereg commit hash is
recorded in REPORT.md. Any amendment is committed before the
deviating run.

## 8. Toolchain guard

safebin mandatory: PATH=$HOME/safebin for all build/run work;
`which python3 python` returns nothing (verified before any
build); pinned znc 2026.07.0-dev; pure Zag for all research
logic (shell only for setup, znc, runs, sha256sum, git).
AGENTS.md miscompile workarounds apply: u8-backed state with
get32/set32 (no `as *i32` slice construction), single
preallocated emit buffer with cursor helpers and one
_zag_raw_syscall write, no `!(A && B)` in while conditions
(grep-checked), shallow if-nesting with hoisted flags,
`_zag_malloc as *u8` pattern, linear scans only. Git: local
commits only, never push, explicit pathspecs, no bare
`git commit`, no `git reset` on the shared branch, git writes
via /usr/bin/git.

## 9. What this does NOT claim

- The store remains researcher-structured, learner-populated
  (same split as FORMAL-COMPOSE/E2E). Constraint induction
  from judgments is still open.
- One predicate (ACYCLIC), one store family, small battery.
  No generality claim beyond these stacks and this battery.
- Promotion cost is not optimized (Phase 1 scans all heads
  per pass); this is a correctness prototype, not a scaling
  result.
- The B1 battery is driver-issued on a controlled state, not
  learner-issued; same standing as E2E's driver-issued
  adversarial battery.
