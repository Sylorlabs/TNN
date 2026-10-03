# PREREG.md -- FORMAL-COMPOSE-DAG3: promotion-based re-ranking on a
# 3-structure DAG composition (diamond + fan-in/fan-out + deep chain)

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG3. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_dag3/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE-RERANK REPORT.md (BUILD-PASS
RR1-RR6; promotion-based re-ranking resolves the B1 boundary;
tested on 2-structure L2 stacks: 7 promotes, maxrank=21,
diverge=0). FORMAL-COMPOSE-PORT and FORMAL-COMPOSE-E2E
BUILD-PASS (rank-slot store as live L2 attach-op edge store).

This preregistration freezes the battery, the hand-derived
predictions, and the kill bars (DAG1-DAG6) BEFORE any
implementation file exists. Status of everything below:
FROZEN. Any deviation requires a prereg amendment committed
before the deviating run.

## 1. The gap (why this experiment exists)

RERANK proved promotion-based re-ranking on 2-structure L2
stacks (chains with cross-rank attaches). Open question: is
the promotion mechanism general, or does it only work for
2-structure chains? This experiment tests it on a 3-structure
DAG composition: a diamond (A depends on B and C; B and C
both depend on D), extended with fan-out (A gains children E,
F), fan-in (D gains parents E, F: 4 parents total), and a
deep-chain limit probe (a 10-link chain whose promotion must
cascade through all 10 links inside the 23-pass cap).

Two honest outcomes are possible. (A) The promotion
mechanism composes the diamond and the extensions: every
acyclic attach becomes readable, the rank invariant (read
graph strictly decreasing) holds at every stage, promotions
converge (diverge=0), and cycle-closing attaches at three
scales stay inert with all valid edges preserved. (B) The
mechanism fails somewhere past 2-structure chains: a kill
bar below states exactly what would refute it.

## 2. Frozen mechanism (unchanged; under test, not modified)

`es_rerank.zag` is copied byte-identical from
`formal_compose_rerank/` (verified by cmp; sha256 recorded in
REPORT.md). No source change. The frozen interface used:
es_item_new, e_add, e_has, es_ndeps, es_dep_at, e_count,
es_audit, es_promotes, es_maxrank, es_diverge, es_rank (via a
per-build d3_rank shim, section 2.1).

### 2.1 d3_rank shims (frozen, 3 tiny per-build files)

The battery is catted byte-identical into all three builds;
only the shim differs:

- d3_shim_rerank.zag: `d3_rank(st,w) = es_rank(st,w)`
  (mutable i32 ranks at st+1984, -1 = unregistered).
- d3_shim_rep.zag: `d3_rank(st,w)` reads the rank byte at
  st+1984+w, mapping 255 to -1 (rr_es_rep.zag layout).
- d3_shim_list.zag: `d3_rank(st,w) = 0` (LIST has no rank
  structure; the invariant is expected to read 0 there and
  is not barred on LIST).

### 2.2 d3_inv: the rank-invariant check (frozen)

d3_inv(st) scans every registered item y and every readable
dep w of y (via es_ndeps/es_dep_at) and returns 0 on the
first readable edge with d3_rank(w) >= d3_rank(y), else 1.
This is an empirical check of the structural claim "the read
graph always has strictly decreasing ranks", and guards
against implementation bugs (e.g. a relocation bug of the
kind fixed in RERANK PREREG_AMENDMENT1 section A4).

## 3. Frozen battery (d3_batt.zag)

One state, four stages, one output line per stage. Items are
ids 4..23 (es_item_of is identity below 40). Registration is
explicit and frozen.

Stage 1 (diamond; register 4..12 -> ranks 0..8):
  e_add(4,5,1)   // A->B
  e_add(4,6,1)   // A->C
  e_add(5,7,1)   // B->D
  e_add(6,7,1)   // C->D
Stage 2 (adversarial on the diamond):
  e_add(7,4,2)   // D->A: cycle-closing (readable A->B->D)
  e_add(7,7,2)   // D->D: self-loop
Stage 3 (fan-out / fan-in / extension):
  e_add(4,8,1)   // A->E (fan-out; fast path)
  e_add(4,9,1)   // A->F (fan-out; fast path)
  e_add(8,7,1)   // E->D (fan-in; slow path)
  e_add(9,7,1)   // F->D (fan-in; slow path)
  e_add(10,11,1) // G->H (slow path)
  e_add(11,10,1) // H->G: cycle-closing (10->11 readable)
  e_add(12,4,1)  // I->A (slow path, acyclic)
Stage 4 (deep chain; register 13..23 -> ranks 9..19):
  e_add(23,22,1) ... e_add(14,13,1)  // 10-link chain, fast
  e_add(13,23,1) // cycle-closing on the long chain

### 3.1 Hand-derived rank trace on RERANK (frozen)

Ranks shown as item:rank; only changed items listed.

After registration: 4:0,5:1,6:2,7:3,8:4,9:5,10:6,11:7,12:8.

- e_add(4,5,1): slow (1>=0). t[4]:=2. No readable edges.
  -> 4:2. promotes=1.
- e_add(4,6,1): slow (2>=2). t[4]:=3. Readable: 4->5.
  3<=1? no. -> 4:3. promotes=2.
- e_add(5,7,1): slow (3>=1). t[5]:=4. Readable: 4->5,4->6.
  p1: 4->5: 3<=4 -> t[4]:=5; 4->6: 5<=2? no. p2: quiet.
  -> 4:5,5:4. promotes=3.
- e_add(6,7,1): slow (3>=2). t[6]:=4. Readable: 4->5,4->6,
  5->7. 4->6: 5<=4? no. -> 6:4. promotes=4.
  D3A state: 4:5,5:4,6:4,7:3. All four diamond edges
  readable (children at 4,4,3,3 < parents 5,5,4,4).
- e_add(7,4,2): slow (5>=3). t[7]:=6. Readable: all four
  diamond edges. p1: 5->7: 4<=6 -> 7; 6->7: 4<=6 -> 7;
  4->5: 5<=7 -> 8; 4->6: 8<=7? no. p2: quiet.
  -> 4:8,5:7,6:7,7:6. promotes=5. The 7->4 record (head 5
  of item 7) relocates with child 4 to head 8; item 7
  reads heads 0..5: INERT.
- e_add(7,7,2): slow (6>=6). t[7]:=7. Readable: 4->5,4->6,
  5->7,6->7. p1: 5->7: 7<=7 -> 8; 6->7: 7<=7 -> 8;
  4->5: 8<=8 -> 9; 4->6: 9<=8? no. p2/p3: quiet.
  -> 4:9,5:8,6:8,7:7. promotes=6. Self-loop record
  relocates to head 7; item 7 reads 0..6: INERT. Diamond
  edges all still readable (8<9, 8<9, 7<8, 7<8).
- e_add(4,8,1): fast (4<9). e_add(4,9,1): fast (5<9).
- e_add(8,7,1): slow (7>=4). t[8]:=8. No readable edge
  touches 8: converged immediately. -> 8:8. promotes=7.
  Edge 8->7 readable (7<8).
- e_add(9,7,1): slow (7>=5). t[9]:=8. -> 9:8.
  promotes=8. Edge 9->7 readable (7<8).
- e_add(10,11,1): slow (7>=6). t[10]:=8. -> 10:8.
  promotes=9. Edge 10->11 readable (7<8).
- e_add(11,10,1): slow (8>=7). Cycle-closing (10->11
  readable). t[11]:=9. p1: 10->11: 8<=9 -> t[10]:=10.
  p2: quiet. -> 10:10,11:9. promotes=10. The 11->10
  record relocates with child 10 to head 10; item 11
  reads 0..8: INERT. 10->11 preserved (head 9 < 10).
- e_add(12,4,1): slow (9>=8). t[12]:=10. No readable edge
  touches 12: converged. -> 12:10. promotes=11. Edge
  12->4 readable (9<10).
  D3C state: 4:9,5:8,6:8,7:7,8:8,9:8,10:10,11:9,12:10.
  Type-1 readable: 4->5,4->6,5->7,6->7,4->8,4->9,8->7,
  9->7,10->11,12->4 = 10. Type-2 readable: 0.
- Register 13..23 -> ranks 9..19.
- Chain e_add(23,22,1)..e_add(14,13,1): all fast
  (each from-rank > to-rank). 10 edges, promotes stays 11.
- e_add(13,23,1): slow (19>=9). Cycle-closing (readable
  path 23->22->..->13). t[13]:=20. p1: 14->13:
  10<=20 -> 21. p2: 15->14 -> 22. p3..p9 continue the
  cascade: t[13+k]=20+k. p10: 23->22: 19<=29 -> 30.
  p11: quiet. Converged in 11 passes (cap 23 not hit).
  -> 13:20,...,23:30. promotes=12. The 13->23 record
  relocates with child 23 to head 30; item 13 reads
  0..19: INERT. All 10 chain edges preserved
  (child 20..29 < parent 21..30).

Final RERANK: promotes=12, maxrank=30, diverge=0,
audit=0, inv=1 at every stage, t1=20, t2=0.

### 3.2 Battery output lines (frozen format)

```
D3A dab=%d dac=%d dbd=%d dcd=%d inv=%d audit=%d promotes=%d maxrank=%d
D3B adv1=%d adv2=%d dia=%d inv=%d audit=%d promotes=%d maxrank=%d
D3C fo1=%d fo2=%d fi1=%d fi2=%d ext1=%d ext2=%d cyc=%d inv=%d audit=%d promotes=%d maxrank=%d t1=%d t2=%d
D3D chain=%d cyc=%d inv=%d audit=%d promotes=%d maxrank=%d diverge=%d t1=%d t2=%d
```
where dab=e_has(4,5,1), dac=e_has(4,6,1), dbd=e_has(5,7,1),
dcd=e_has(6,7,1), adv1=e_has(7,4,2), adv2=e_has(7,7,2),
dia=(dab&&dac&&dbd&&dcd), fo1=e_has(4,8,1),
fo2=e_has(4,9,1), fi1=e_has(8,7,1), fi2=e_has(9,7,1),
ext1=e_has(10,11,1), ext2=e_has(12,4,1), cyc=e_has(11,10,1)
on D3C / e_has(13,23,1) on D3D, chain = count of the 10
chain edges readable, t1=e_count(st,1), t2=e_count(st,2).

## 4. Exact predicted stdout (frozen)

d3_rerank_bin:
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=1 audit=0 promotes=4 maxrank=5
D3B adv1=0 adv2=0 dia=1 inv=1 audit=0 promotes=6 maxrank=9
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=0 inv=1 audit=0 promotes=11 maxrank=10 t1=10 t2=0
D3D chain=10 cyc=0 inv=1 audit=0 promotes=12 maxrank=30 diverge=0 t1=20 t2=0
```

d3_rep_bin (fixed ranks; REP maxrank stub = counter-1):
```
D3A dab=0 dac=0 dbd=0 dcd=0 inv=1 audit=0 promotes=0 maxrank=8
D3B adv1=1 adv2=0 dia=0 inv=1 audit=0 promotes=0 maxrank=8
D3C fo1=0 fo2=0 fi1=1 fi2=1 ext1=0 ext2=1 cyc=1 inv=1 audit=0 promotes=0 maxrank=8 t1=4 t2=1
D3D chain=10 cyc=0 inv=1 audit=0 promotes=0 maxrank=19 diverge=0 t1=14 t2=1
```
(REP notes: 7->4 is a fast newer->older edge, so adv1=1 is
correct REP behavior, not a cycle: no readable path
4->*7 exists on REP. 8->7, 9->7, 11->10, 12->4 are likewise
fast and readable; 10->11, 13->23 cross-rank and inert.
t1=4 counts 8->7,9->7,11->10,12->4; t2=1 counts 7->4.)

d3_list_bin (unconstrained; d3_rank=0 so inv reads 0):
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=0 audit=0 promotes=0 maxrank=8
D3B adv1=1 adv2=1 dia=1 inv=0 audit=4 promotes=0 maxrank=8
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=1 inv=0 audit=8 promotes=0 maxrank=8 t1=10 t2=2
D3D chain=10 cyc=1 inv=0 audit=19 promotes=0 maxrank=19 diverge=0 t1=20 t2=2
```
(LIST audit hand-count: D3B items on cycles {4,5,6,7}=4;
D3C adds {8,9,10,11}=8 (8->7->4->8, 9->7->4->9, 10<->11;
12->4->.. never reaches 12); D3D adds {13..23}=11 on the
13->23->..->13 cycle, total 19.)

## 5. Frozen kill bars DAG1-DAG6

- DAG1 (diamond composes via promotion): RERANK D3A
  dab=dac=dbd=dcd=1. Discriminators: REP D3A all 0 (the
  diamond attaches are genuinely cross-rank: the battery
  is in the B1 class, not VOID); LIST D3A all 1
  (unconstrained store expresses them). PASS requires all
  three arms to match.
- DAG2 (cycle impossibility, representational): RERANK D3B
  adv1=adv2=0, D3C cyc=0, D3D cyc=0, audit=0 on all four
  lines; LIST D3B adv1=adv2=1 audit=4, D3C cyc=1,
  D3D cyc=1 (the adversarial probes are genuinely
  cycle-closing). Any committed cycle on RERANK (audit>0
  or any adv/cyc=1) FAILS the bar.
- DAG3 (rank invariant): RERANK inv=1 on all four lines;
  REP inv=1 on all four lines (structural sanity: the
  fixed-rank read path satisfies it too). LIST inv is
  reported, not barred (no rank structure there).
- DAG4 (fan-in / fan-out): RERANK D3C fo1=fo2=fi1=fi2=1
  (A has 4 readable children 5,6,8,9; D has 4 readable
  parents 5,6,8,9), ext1=ext2=1, t1=10, t2=0,
  promotes=11, maxrank=10.
- DAG5 (deep-chain convergence; the limit probe): RERANK
  D3D chain=10, cyc=0, promotes=12, maxrank=30,
  diverge=0, t1=20, t2=0. A 10-link cascade converges in
  11 passes (cap 23 not approached); the cycle-closing
  attach on the long chain stays inert with all 10 chain
  edges preserved.
- DAG6 (determinism and hygiene): all three binaries 3/3
  byte-identical stdout, stderr empty on all 9 runs; zero
  new analyzer warning classes vs the RERANK parent
  (benign A0102/B0103/E0101/E0102 only); no `!(A && B)`
  in while conditions (grep-checked).

## 6. Falsification conditions (what would refute the design)

- Any RERANK run with es_audit > 0: the representational
  claim dies; outcome (B), report honestly.
- Any RERANK D3A line with a dab/dac/dbd/dcd = 0:
  promotion does not admit the diamond class; outcome (B).
- Any RERANK inv = 0: the rank invariant is broken by the
  implementation; outcome (B), investigate the relocation
  path before any verdict.
- diverge = 1: the fixpoint did not converge; investigate
  before any verdict (predicted impossible: the readable
  graph is always a DAG, longest path < 24 items).
- promotes/maxrank mismatch vs section 4: the
  hand-derivation is wrong or the mechanism diverged from
  it; investigate before any verdict, do not re-derive
  post hoc to force a pass.
- If REP D3A shows any dab/dac/dbd/dcd = 1, the diamond
  battery is not cross-rank (VOID). If LIST shows
  audit = 0 on D3B/D3C/D3D, the adversarial battery is not
  adversarial (VOID).

## 7. Commit-order self-check

PREREG.md (+ NAMECHECK.md, no implementation) is committed
alone before any .zag file exists. The prereg commit hash is
recorded in REPORT.md. Any amendment is committed before the
deviating run.

## 8. Toolchain guard

safebin mandatory: PATH=$HOME/safebin for all build/run
work; `which python3 python` returns nothing (verified
before any build); pinned znc; pure Zag for all research
logic (shell only for setup, znc, runs, sha256sum, cmp,
git). AGENTS.md miscompile workarounds apply. Git: local
commits only, never push, explicit pathspecs, no bare
`git commit`, no `git reset` on the shared branch, git
writes via /usr/bin/git on EPERM.

## 9. What this does NOT claim

- One diamond, one fan-in/fan-out extension, one deep
  chain. No claim about arbitrary DAG shapes, 5k/10k
  scaling, or learner-issued DAG attaches.
- The store remains researcher-structured,
  driver-populated. Constraint induction from judgments is
  still open.
- Promotion cost is not optimized (Phase 1 scans all
  heads per pass); this is a correctness probe, not a
  scaling result.
- The battery is driver-issued on a controlled state,
  not learner-issued; same standing as RERANK's
  driver-issued B1 battery.
