# PREREG.md -- FORMAL-COMPOSE-DAG5: promotion-based re-ranking on a
# 5-structure multi-diamond DAG composition

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG5. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_dag5/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE-DAG3 REPORT.md (BUILD-PASS
DAG1-DAG6; promotion-based re-ranking generalizes to one
diamond + fan-in/fan-out + 10-link chain; 12 promotes,
maxrank=30, diverge=0). Scope limit of D3: "one diamond +
extensions, driver-issued attaches; no claim on arbitrary
DAGs or learner-issued DAG traffic."

This preregistration freezes the battery, the hand-derived
predictions, and the kill bars (D5-1-D5-6) BEFORE any
implementation file exists. Status of everything below:
FROZEN. Any deviation requires a prereg amendment committed
before the deviating run.

## 1. The gap (why this experiment exists)

D3 proved the promotion mechanism on a single diamond plus
extensions. Open question: does re-ranking handle
multi-diamond DAGs, where promotions must cascade through
converging and diverging paths (two diamonds sharing a
middle layer, cross-links between diamonds, adversarial
attaches closing cycles over the whole stacked structure)?
Two honest outcomes are possible. (A) Promotion composes
the stacked multi-diamond DAG: every acyclic attach becomes
readable, the rank invariant holds at every stage,
promotions converge (diverge=0), and cycle-closing attaches
over the stacked structure stay inert with all valid edges
preserved. (B) The mechanism fails somewhere past one
diamond: a kill bar below states exactly what would refute
it.

## 2. Frozen mechanism (unchanged; under test, not modified)

`es_rerank.zag` is copied byte-identical from
`formal_compose_dag3/` (which verified it byte-identical
against `formal_compose_rerank/`; sha256
8a6de72312d0375bb32d76292dbf97cbb46c8b27d1ce5207a499799b1b051c1c).
No source change. The frozen interface used: es_item_new,
e_add, e_has, es_ndeps, es_dep_at, e_count, es_audit,
es_promotes, es_maxrank, es_diverge, es_rank (via a per-build
d5_rank shim, section 2.1). Discriminator stores
`rr_es_rep.zag` and `es_list_rr.zag` are copied byte-identical
from `formal_compose_dag3/` (cmp-verified).

NOTE: the LATENT BUG flagged in D3 REPORT.md section 4.3
(`es_list_rr.zag`: registered[24] at 1984+1+it overlaps the
i32 counter at 2008 for it=23) is deliberately NOT
triggered here: the battery registers items 4..10 only
(max it=10 < 23), so LIST diagnostics are unaffected.

### 2.1 d5_rank shims (frozen, 3 tiny per-build files)

The battery is catted byte-identical into all three builds;
only the shim differs:

- d5_shim_rerank.zag: `d5_rank(st,w) = es_rank(st,w)`
  (mutable i32 ranks at st+1984, -1 = unregistered).
- d5_shim_rep.zag: `d5_rank(st,w)` reads the rank byte at
  st+1984+w, mapping 255 to -1 (rr_es_rep.zag layout).
- d5_shim_list.zag: `d5_rank(st,w) = 0` (LIST has no rank
  structure; the invariant is expected to read 0 there and
  is not barred on LIST).

### 2.2 d5_inv: the rank-invariant check (frozen)

d5_inv(st) scans every registered item y and every readable
dep w of y (via es_ndeps/es_dep_at) and returns 0 on the
first readable edge with d5_rank(w) >= d5_rank(y), else 1.
Empirical check of "the read graph always has strictly
decreasing ranks".

## 3. Frozen battery (d5_batt.zag)

One state, three stages, one output line per stage. Items
are ids 4..10 (es_item_of is identity below 40).
Registration is explicit and frozen: register 4..10 in
order -> ranks 0..6 (reverse-topological, forcing the slow
path exactly as in D3).

Stage 1 (diamond 1; A=4 -> B=5, C=6; B=5 -> D=7; C=6 -> D=7):
  e_add(4,5,1)
  e_add(4,6,1)
  e_add(5,7,1)
  e_add(6,7,1)

Stage 2 (cross-links, then diamond 2 stacked on D=7:
D=7 -> E=8, F=9; E=8 -> G=10; F=9 -> G=10):
  e_add(5,9,1)   // B -> F (cross-link; slow path)
  e_add(6,8,1)   // C -> E (cross-link; slow path)
  e_add(7,8,1)   // D -> E
  e_add(7,9,1)   // D -> F
  e_add(8,10,1)  // E -> G
  e_add(9,10,1)  // F -> G

Stage 3 (adversarial over the stacked diamonds):
  e_add(10,4,2)  // G -> A: cycle-closing (readable
                 // 4 -> 5 -> 7 -> 8 -> 10)
  e_add(10,10,2) // G -> G: self-loop

### 3.1 Hand-derived rank trace on RERANK (frozen)

Ranks shown as item:rank; only changed items listed.
After registration: 4:0,5:1,6:2,7:3,8:4,9:5,10:6.
maxrank-seen=6 at registration (per D3 amendment 4.1).

- e_add(4,5,1): slow (1>=0). t[4]:=2. -> 4:2. promotes=1.
- e_add(4,6,1): slow (2>=2). t[4]:=3. -> 4:3. promotes=2.
- e_add(5,7,1): slow (3>=1). t[5]:=4. p1: 4->5: 3<=4 ->
  4:5. p2 quiet. -> 4:5,5:4. promotes=3.
- e_add(6,7,1): slow (3>=2). t[6]:=4. p1 quiet.
  -> 6:4. promotes=4.
  D5A state: 4:5,5:4,6:4,7:3,8:4,9:5,10:6. maxrank=6.
- e_add(5,9,1): slow (5>=4). t[5]:=6. p1: 4->5: 5<=6 ->
  4:7. p2 quiet. -> 4:7,5:6. promotes=5. maxrank=7.
  Edge 5->9 readable (5<6).
- e_add(6,8,1): slow (4>=4). t[6]:=5. p1: no edge needs
  the bump (4->6: 7>5; 6->7: 5>3 already). -> 6:5.
  promotes=6. maxrank=7. Edge 6->8 readable (4<5).
- e_add(7,8,1): slow (4>=3). t[7]:=5. p1: 6->7: 5<=5 ->
  6:6. p2 quiet. -> 6:6,7:5. promotes=7. maxrank=7.
  Edge 7->8 readable (4<5).
- e_add(7,9,1): slow (5>=5). t[7]:=6. p1: 5->7: 6<=6 ->
  5:7; 6->7: 6<=6 -> 6:7. p2: 4->5: 7<=7 -> 4:8.
  p3 quiet. -> 4:8,5:7,6:7,7:6. promotes=8. maxrank=8.
  Edge 7->9 readable (5<6).
- e_add(8,10,1): slow (6>=4). t[8]:=7. p1: 6->8: 7<=7 ->
  6:8; 7->8: 6<=8 -> 7:9. p2: 5->7: 7<=9 -> 5:10;
  6->7: 8<=9 -> 6:10. p3: 4->5: 8<=10 -> 4:11.
  p4 quiet. -> 4:11,5:10,6:10,7:9,8:8.
  promotes=9. maxrank=11. Edge 8->10 readable (6<8).
- e_add(9,10,1): slow (6>=5). t[9]:=7. p1: all readable
  edges already consistent (5->9: 10>7; 7->9: 9>7).
  -> 9:7. promotes=10. maxrank=11.
  D5B state: 4:11,5:10,6:10,7:9,8:8,9:7,10:6. All 10
  type-1 edges readable; dia1 intact through diamond 2's
  promotions.
- e_add(10,4,2): slow (11>=6). t[10]:=12. Readable: all
  10 type-1 edges. p1: 8->10: 8<=12 -> 8:13; 9->10:
  7<=12 -> 9:13. p2: 5->9: 10<=13 -> 5:14; 6->8:
  10<=13 -> 6:14; 7->8: 9<=13 -> 7:14. p3: 4->5:
  11<=14 -> 4:15; 5->7: 14<=14 -> 5:15; 6->7: 14<=14
  -> 6:15. p4: 4->5: 15<=15 -> 4:16. p5 quiet.
  Converged in 5 passes. -> 4:16,5:15,6:15,7:14,8:13,
  9:13,10:12. promotes=11. maxrank=16. The 10->4 record
  (head 11 of item 10) relocates with child 4 to head 16;
  item 10 reads heads 0..11: INERT. All 10 type-1 edges
  preserved.
- e_add(10,10,2): slow (12>=12). t[10]:=13. p1: 8->10:
  13<=13 -> 8:14; 9->10: 13<=13 -> 9:14. p2: 7->8:
  14<=14 -> 7:15. p3: 5->7: 15<=15 -> 5:16; 6->7:
  15<=15 -> 6:16. p4: 4->5: 16<=16 -> 4:17. p5 quiet.
  Converged in 5 passes. -> 4:17,5:16,6:16,7:15,8:14,
  9:14,10:13. promotes=12. maxrank=17. Self-loop record
  relocates to head 13; item 10 reads 0..12: INERT. All
  10 type-1 edges preserved (8->10: 13<14; 9->10:
  13<14; 7->8: 14<15; 7->9: 14<15; 5->9: 14<16;
  6->8: 14<16; 5->7: 15<16; 6->7: 15<16; 4->5: 16<17;
  4->6: 16<17).

Final RERANK: promotes=12, maxrank=17, diverge=0,
audit=0, inv=1 at every stage, t1=10, t2=0. Longest
promotion used 5 passes (cap 23 never approached).

### 3.2 Battery output lines (frozen format)

```
D5A dab=%d dac=%d dbd=%d dcd=%d inv=%d audit=%d promotes=%d maxrank=%d
D5B xl1=%d xl2=%d d78=%d d79=%d d810=%d d910=%d dia1=%d inv=%d audit=%d promotes=%d maxrank=%d t1=%d
D5C adv1=%d adv2=%d dia1=%d dia2=%d xl1=%d xl2=%d inv=%d audit=%d promotes=%d maxrank=%d t1=%d t2=%d
```
where dab=e_has(4,5,1), dac=e_has(4,6,1), dbd=e_has(5,7,1),
dcd=e_has(6,7,1), xl1=e_has(5,9,1), xl2=e_has(6,8,1),
d78=e_has(7,8,1), d79=e_has(7,9,1), d810=e_has(8,10,1),
d910=e_has(9,10,1), dia1=(dab&&dac&&dbd&&dcd),
dia2=(d78&&d79&&d810&&d910), adv1=e_has(10,4,2),
adv2=e_has(10,10,2), t1=e_count(st,1), t2=e_count(st,2).

## 4. Exact predicted stdout (frozen)

d5_rerank_bin:
```
D5A dab=1 dac=1 dbd=1 dcd=1 inv=1 audit=0 promotes=4 maxrank=6
D5B xl1=1 xl2=1 d78=1 d79=1 d810=1 d910=1 dia1=1 inv=1 audit=0 promotes=10 maxrank=11 t1=10
D5C adv1=0 adv2=0 dia1=1 dia2=1 xl1=1 xl2=1 inv=1 audit=0 promotes=12 maxrank=17 t1=10 t2=0
```

d5_rep_bin (fixed ranks 0..6; all type-1 attaches cross-rank):
```
D5A dab=0 dac=0 dbd=0 dcd=0 inv=1 audit=0 promotes=0 maxrank=6
D5B xl1=0 xl2=0 d78=0 d79=0 d810=0 d910=0 dia1=0 inv=1 audit=0 promotes=0 maxrank=6 t1=0
D5C adv1=1 adv2=0 dia1=0 dia2=0 xl1=0 xl2=0 inv=1 audit=0 promotes=0 maxrank=6 t1=0 t2=1
```
(REP notes: 10->4 is a fast 6->0 edge, so adv1=1 is
correct REP behavior, not a cycle: no readable path
4->*10 exists on REP. 10->10 is cross-rank (6>=6) and
inert. inv=1: the single readable edge 10->4 strictly
decreases (0<6). maxrank stub = counter-1 = 6.)

d5_list_bin (unconstrained; d5_rank=0 so inv reads 0):
```
D5A dab=1 dac=1 dbd=1 dcd=1 inv=0 audit=0 promotes=0 maxrank=6
D5B xl1=1 xl2=1 d78=1 d79=1 d810=1 d910=1 dia1=1 inv=0 audit=0 promotes=0 maxrank=6 t1=10
D5C adv1=1 adv2=1 dia1=1 dia2=1 xl1=1 xl2=1 inv=0 audit=7 promotes=0 maxrank=6 t1=10 t2=2
```
(LIST audit hand-count: D5B has no cycle (all paths end at
10; audit=0). D5C adds 10->4 and 10->10: every item
4..10 lies on a directed cycle (4->5->7->8->10->4;
6->7->...->10->4->6; 9->10->4->5->9; 10->10), so
audit=7. max item 10 < 23: the D3-flagged LIST latent bug
cannot fire.)

## 5. Frozen kill bars D5-1-D5-6

- D5-1 (stacked multi-diamond composition via promotion):
  RERANK D5A dab=dac=dbd=dcd=1; D5B
  xl1=xl2=d78=d79=d810=d910=dia1=1 (cross-links attach on
  the slow path; diamond 2 composes on top of diamond 1).
  Discriminators: REP D5A all 0 and D5B all 0 (every
  type-1 attach is genuinely cross-rank: the battery is in
  the B1 class, not VOID); LIST D5A all 1 and D5B all 1
  (unconstrained store expresses them). PASS requires all
  three arms to match.
- D5-2 (cycle impossibility on the stacked DAG,
  representational): RERANK D5C adv1=adv2=0 and audit=0 on
  all three lines; LIST D5C adv1=adv2=1, audit=7 (the
  adversarial probes are genuinely cycle-closing over the
  stacked structure). Any committed cycle on RERANK
  (audit>0 or any adv=1) FAILS the bar.
- D5-3 (rank invariant): RERANK inv=1 on all three lines;
  REP inv=1 on all three lines. LIST inv is reported, not
  barred.
- D5-4 (cross-link convergence): RERANK D5B promotes=10,
  maxrank=11, t1=10, dia1=1. The six stage-2 attaches
  (two cross-links + diamond 2) compose via 6 promotions
  while preserving all four diamond-1 edges through
  diamond 2's re-ranking.
- D5-5 (adversarial cascade on stacked diamonds; the
  limit probe): RERANK D5C promotes=12, maxrank=17,
  diverge=0, t1=10, t2=0, dia1=dia2=xl1=xl2=1. Each
  adversarial attach converged in 5 passes through two
  stacked diamonds plus cross-links (cap 23 not
  approached); both cycle-closing attaches stayed inert
  with all 10 type-1 edges preserved.
- D5-6 (determinism and hygiene): all three binaries 3/3
  byte-identical stdout, stderr empty on all 9 runs; no
  `!(A && B)` in while conditions (grep-checked); pure
  Zag; safebin pinned znc throughout.

## 6. Falsification conditions (what would refute the design)

- Any RERANK run with es_audit > 0: the representational
  claim dies; outcome (B), report honestly.
- Any RERANK D5A line with a dab/dac/dbd/dcd = 0, or D5B
  with any xl/d78/d79/d810/d910/dia1 = 0: promotion does
  not admit the multi-diamond class; outcome (B).
- Any RERANK inv = 0: the rank invariant is broken by the
  implementation; outcome (B), investigate the relocation
  path before any verdict.
- diverge = 1: the fixpoint did not converge; investigate
  before any verdict (predicted impossible: the readable
  graph is always a DAG, longest readable path < 11 items).
- promotes/maxrank mismatch vs section 4: the
  hand-derivation is wrong or the mechanism diverged from
  it; investigate before any verdict, do not re-derive
  post hoc to force a pass.
- If REP shows any type-1 attach = 1, the battery is not
  cross-rank (VOID). If LIST shows audit = 0 on D5C, the
  adversarial battery is not adversarial (VOID).

## 7. Commit-order self-check

PREREG.md (+ NAMECHECK.md, no implementation) is committed
alone before any .zag file exists. The prereg commit hash is
recorded in REPORT.md. Any amendment is committed before the
deviating run.

## 8. Toolchain guard

safebin mandatory: PATH=$HOME/safebin for all build/run
work; `which python3 python` returns nothing (verified at
worker startup before any build); pinned znc; pure Zag for
all research logic (shell only for setup, znc, runs,
sha256sum, cmp, git). AGENTS.md miscompile workarounds
apply. Git: local commits only, never push, explicit
pathspecs, no bare `git commit`, no `git reset` on the
shared branch, git writes via /usr/bin/git on EPERM.

## 9. What this does NOT claim

- Two stacked diamonds + two cross-links + adversarial
  probes, driver-issued on a controlled state. No claim
  about arbitrary DAG shapes beyond this battery, 5k/10k
  scaling, or learner-issued DAG attaches.
- The store remains researcher-structured,
  driver-populated. Constraint induction from judgments is
  still open.
- Promotion cost is not optimized (Phase 1 scans all
  heads per pass); this is a correctness probe, not a
  scaling result.
