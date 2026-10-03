# REPORT.md -- FORMAL-COMPOSE-DAG3: promotion-based re-ranking on a
# 3-structure DAG composition

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG3. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_dag3/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE-RERANK REPORT.md (BUILD-PASS
RR1-RR6; promotion mechanism proven on 2-structure L2 stacks:
7 promotes, maxrank=21, diverge=0).

Prereg commit: c956d17f1 (PREREG.md + NAMECHECK.md, no
implementation). Amendment: PREREG_AMENDMENT1.md (five
exact-prediction corrections with root causes; no kill-bar
changes; committed with this report).

## Verdict: BUILD-PASS (DAG1-DAG6 all green)

Promotion-based re-ranking is general beyond 2-structure
chains. A 3-layer diamond DAG (A->B, A->C, B->D, C->D, all
cross-rank under creation-order ranks) composes via 4
promotions; fan-out (A gains 2 more children: 4 readable
children), fan-in (D gains 2 more parents: 4 readable
parents), and a 10-link deep chain all compose; the rank
invariant (read graph strictly decreasing) holds
empirically at every stage; a 10-link promotion cascade
converges in 11 passes (cap 23 never approached,
diverge=0); cycle-closing attaches at three scales
(diamond D->A, pair H->G, 10-chain 13->23) all stay inert
with every valid edge preserved; audit=0 throughout.

## 1. Battery

`d3_batt.zag` (shared byte-identical across all three
builds; only a 3-line `d3_rank` shim differs per build).
One state, four stages, one output line per stage:

- D3A: diamond e_add(4,5,1), e_add(4,6,1), e_add(5,7,1),
  e_add(6,7,1), all cross-rank (registration order
  4..12 = reverse-topological, forcing the slow path).
- D3B: adversarial e_add(7,4,2) (cycle-closing via
  readable 4->5->7), e_add(7,7,2) (self-loop).
- D3C: fan-out e_add(4,8,1), e_add(4,9,1) (fast path);
  fan-in e_add(8,7,1), e_add(9,7,1) (slow path);
  e_add(10,11,1) (slow), e_add(11,10,1) (cycle-closing),
  e_add(12,4,1) (slow, acyclic).
- D3D: register 13..23, chain e_add(23,22,1)..e_add(14,13,1)
  (10 links, fast), e_add(13,23,1) (cycle-closing on the
  long chain).

`d3_inv` empirically checks the rank invariant: every
readable edge strictly decreases in rank (guards against
relocation bugs of the kind fixed in RERANK A4).

## 2. Results (3/3 byte-identical per binary, stderr empty)

d3_rerank_bin (actual; matches amended predictions exactly):
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=1 audit=0 promotes=4 maxrank=8
D3B adv1=0 adv2=0 dia=1 inv=1 audit=0 promotes=6 maxrank=9
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=0 inv=1 audit=0 promotes=11 maxrank=10 t1=10 t2=0
D3D chain=10 cyc=0 inv=1 audit=0 promotes=12 maxrank=30 diverge=0 t1=20 t2=0
```
d3_rep_bin (fixed-rank discriminator; all predictions
matched unamended):
```
D3A dab=0 dac=0 dbd=0 dcd=0 inv=1 audit=0 promotes=0 maxrank=8
D3B adv1=1 adv2=0 dia=0 inv=1 audit=0 promotes=0 maxrank=8
D3C fo1=0 fo2=0 fi1=1 fi2=1 ext1=0 ext2=1 cyc=1 inv=1 audit=0 promotes=0 maxrank=8 t1=4 t2=1
D3D chain=10 cyc=0 inv=1 audit=0 promotes=0 maxrank=19 diverge=0 t1=14 t2=1
```
d3_list_bin (unconstrained discriminator; matches amended
predictions exactly):
```
D3A dab=1 dac=1 dbd=1 dcd=1 inv=0 audit=0 promotes=0 maxrank=8
D3B adv1=1 adv2=1 dia=1 inv=0 audit=4 promotes=0 maxrank=8
D3C fo1=1 fo2=1 fi1=1 fi2=1 ext1=1 ext2=1 cyc=1 inv=0 audit=8 promotes=0 maxrank=8 t1=11 t2=2
D3D chain=10 cyc=1 inv=0 audit=18 promotes=0 maxrank=1 diverge=0 t1=22 t2=2
```

## 3. Kill bars DAG1-DAG6

- DAG1 (diamond composes via promotion): RERANK D3A
  dab=dac=dbd=dcd=1; REP D3A all 0 (genuinely
  cross-rank: the battery is in the B1 class, not VOID);
  LIST D3A all 1 (unconstrained store expresses them).
  PASS.
- DAG2 (cycle impossibility, representational): RERANK
  D3B adv1=adv2=0, D3C cyc=0, D3D cyc=0, audit=0 on all
  four lines; LIST D3B adv1=adv2=1 audit=4, D3C cyc=1,
  D3D cyc=1 (adversarial probes genuinely cycle-closing).
  No committed cycle on RERANK anywhere. PASS.
- DAG3 (rank invariant): RERANK inv=1 on all four lines;
  REP inv=1 on all four lines. The read graph is
  empirically strictly decreasing through 12 promotions
  including a 10-link cascade. PASS.
- DAG4 (fan-in / fan-out): RERANK D3C fo1=fo2=fi1=fi2=1
  (A: 4 readable children; D: 4 readable parents),
  ext1=ext2=1, t1=10, t2=0, promotes=11, maxrank=10.
  PASS.
- DAG5 (deep-chain convergence; the limit probe):
  RERANK D3D chain=10, cyc=0, promotes=12, maxrank=30,
  diverge=0, t1=20, t2=0. The 10-link cascade converged
  in 11 passes; the cycle-closing attach on the long
  chain stayed inert with all 10 chain edges preserved.
  PASS.
- DAG6 (determinism and hygiene): all three binaries 3/3
  byte-identical stdout, stderr empty on all 9 runs;
  zero analyzer warning classes (only the environmental
  "zagd unavailable" notice); no `!(A && B)` in while
  conditions (grep-checked); pure Zag; safebin pinned
  znc throughout. PASS.

## 4. Prediction discrepancies (all root-caused, none touch
## the bars; see PREREG_AMENDMENT1.md)

1. RERANK D3A maxrank 8 (predicted 5): prereg arithmetic
   error; `es_item_new` sets maxrank-seen at registration
   (ranks 0..8 before any promotion). The frozen rank
   trace is confirmed digit-for-digit (promotes=4, D3B
   maxrank=9 as predicted).
2. LIST D3C t1=11 (predicted 10) and D3D t1=22
   (predicted 20): prereg arithmetic errors; stage 3
   writes 7 type-1 edges, all readable on LIST.
3. LIST D3D audit=18 (predicted 19), maxrank=1
   (predicted 19): LATENT BUG in the discriminator store
   `es_list_rr.zag` (parent lane's file, copied
   byte-identical): `registered[24]` flags at
   1984+1+it overlap the i32 registration counter at
   2008 for it=23. Registering item 23 clobbers the
   counter (19->2) and makes audit skip u=23. Never
   fired in the parent battery (max item 15). Deliberately
   not fixed: it affects only LIST diagnostics, the
   arm's VOID-discrimination (audit=18>0) is intact, and
   the mechanism under test (`es_rerank.zag`, disjoint
   layout) is unaffected. Flagged for the parent lane.

## 5. Limits and generality notes

- The mechanism handled fan-out, fan-in, and a diamond
  with no special cases: promotion is a total function
  of (store, parent, child); the diamond needed no new
  logic beyond what the 2-structure chains exercised.
- The 23-pass cap is tied to the 24-item limit (longest
  readable path < 24). The 10-chain used 11 passes. A
  store with more items would need the cap revisited;
  the cap is a computational bound, not a cyclicity
  test, and non-convergence still completes the write
  with the read graph a DAG.
- maxrank grows with promotion depth (30 here; heads
  support 256 ranks). Promotion count grows with the
  number of cross-rank attaches (12 here). Phase 1 scans
  all heads per pass: correctness prototype, not
  optimized (standing).
- Creation-order registration (the learners' pattern)
  takes the fast path; the slow path fired only on
  deliberately reverse-topological registration. This
  matches RERANK's prom0=0 finding: learner traffic
  never needs promotion, but the substrate admits
  cross-rank composition when it arises.
- Scope: one diamond, one fan-in/fan-out extension, one
  deep chain; driver-issued attaches on a controlled
  state. No claim about arbitrary DAG shapes,
  learner-issued DAG attaches, or 5k/10k scaling.

## 6. Files

Lane `docs/lab/research-lead/overnight-20260928/formal_compose_dag3/`:
PREREG.md (frozen, commit c956d17f1), PREREG_AMENDMENT1.md,
NAMECHECK.md, `d3_batt.zag` (battery), `d3_main.zag`,
`d3_shim_rerank.zag` / `d3_shim_rep.zag` /
`d3_shim_list.zag` (d3_rank shims), `d3_build.sh`,
`es_rerank.zag` (byte-identical to parent lane, sha256
8a6de72312d0375bb32d76292dbf97cbb46c8b27d1ce5207a499799b1b051c1c),
`rr_prelude.zag`, `rr_es_rep.zag`, `es_list_rr.zag`
(byte-identical copies, cmp-verified), REPORT.md.
Build artifacts (`*_bin`, `d3_full_*.zag`,
`d3_compile_*.txt`, `*_run_*.txt`, `*_run_*.err`) are not
committed.

Commits local only, explicit pathspecs, no push.
