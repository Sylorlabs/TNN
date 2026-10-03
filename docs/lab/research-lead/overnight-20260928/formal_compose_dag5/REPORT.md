# REPORT.md -- FORMAL-COMPOSE-DAG5: promotion-based re-ranking on a
# 5-structure multi-diamond DAG composition

Date: 2026-10-03. Worker: FORMAL-COMPOSE-DAG5. Lane:
`docs/lab/research-lead/overnight-20260928/formal_compose_dag5/`.
Task type: NON-LEDGER (claim minting paused).

Parent results: FORMAL-COMPOSE-DAG3 REPORT.md (BUILD-PASS
DAG1-DAG6; promotion generalizes to one diamond +
fan-in/fan-out + deep chain; 12 promotes, maxrank=30,
diverge=0; scope limit: "no claim on arbitrary DAGs").

Prereg commit: eabf99981 (PREREG.md + NAMECHECK.md, no
implementation). Amendment: PREREG_AMENDMENT1.md (one
root-caused hand-derivation arithmetic slip, two
maxrank exact-value corrections, no kill-bar substance
changes; committed with this report).

## Verdict: BUILD-PASS (D5-1-D5-6 all green)

Promotion-based re-ranking composes a 5-structure
multi-diamond DAG: diamond 1 (A->B,A->C,B->D,C->D),
two slow-path cross-links (B->F, C->E), and diamond 2
stacked on the middle layer (D->E,D->F,E->G,F->G) all
compose via 10 promotions with diamond 1 intact through
diamond 2's re-ranking; the rank invariant holds
empirically at every stage; both adversarial attaches
over the stacked structure (G->A cycle-closing,
G->G self-loop) converge in 5 passes each (cap 23 never
approached, diverge=0) and stay inert with all 10
type-1 edges preserved; audit=0 throughout.

## 1. Battery

`d5_batt.zag` (shared byte-identical across all three
builds; only a 3-line `d5_rank` shim differs per build).
One state, three stages, one output line per stage:

- D5A: diamond 1 e_add(4,5,1), e_add(4,6,1),
  e_add(5,7,1), e_add(6,7,1), all cross-rank under
  creation-order ranks (registration 4..10 in order ->
  ranks 0..6, reverse-topological, forcing the slow path).
- D5B: cross-links e_add(5,9,1), e_add(6,8,1) (both
  slow path), then diamond 2 e_add(7,8,1), e_add(7,9,1),
  e_add(8,10,1), e_add(9,10,1).
- D5C: adversarial e_add(10,4,2) (cycle-closing over both
  diamonds via readable 4->5->7->8->10), e_add(10,10,2)
  (self-loop).

`d5_inv` empirically checks the rank invariant: every
readable edge strictly decreases in rank (guards against
relocation bugs of the kind fixed in RERANK A4).

Pre-run battery note (measurement honesty, no prediction
change): after the prereg commit but before any build,
the D5C line was changed to re-measure dia1, dia2, xl1,
xl2 from live e_has state instead of reusing stage-1/2
values. Output format and all predictions unchanged.

## 2. Results (3/3 byte-identical per binary, stderr empty)

d5_rerank_bin (actual; matches amended predictions exactly):
```
D5A dab=1 dac=1 dbd=1 dcd=1 inv=1 audit=0 promotes=4 maxrank=6
D5B xl1=1 xl2=1 d78=1 d79=1 d810=1 d910=1 dia1=1 inv=1 audit=0 promotes=10 maxrank=10 t1=10
D5C adv1=0 adv2=0 dia1=1 dia2=1 xl1=1 xl2=1 inv=1 audit=0 promotes=12 maxrank=16 t1=10 t2=0
```
d5_rep_bin (fixed-rank discriminator; all predictions
matched unamended):
```
D5A dab=0 dac=0 dbd=0 dcd=0 inv=1 audit=0 promotes=0 maxrank=6
D5B xl1=0 xl2=0 d78=0 d79=0 d810=0 d910=0 dia1=0 inv=1 audit=0 promotes=0 maxrank=6 t1=0
D5C adv1=1 adv2=0 dia1=0 dia2=0 xl1=0 xl2=0 inv=1 audit=0 promotes=0 maxrank=6 t1=0 t2=1
```
d5_list_bin (unconstrained discriminator; matches amended
predictions exactly):
```
D5A dab=1 dac=1 dbd=1 dcd=1 inv=0 audit=0 promotes=0 maxrank=6
D5B xl1=1 xl2=1 d78=1 d79=1 d810=1 d910=1 dia1=1 inv=0 audit=0 promotes=0 maxrank=6 t1=10
D5C adv1=1 adv2=1 dia1=1 dia2=1 xl1=1 xl2=1 inv=0 audit=7 promotes=0 maxrank=6 t1=10 t2=2
```

## 3. Kill bars D5-1-D5-6

- D5-1 (stacked multi-diamond composition via promotion):
  RERANK D5A dab=dac=dbd=dcd=1; D5B
  xl1=xl2=d78=d79=d810=d910=dia1=1 (cross-links attach
  on the slow path; diamond 2 composes on top of
  diamond 1). REP D5A all 0, D5B all 0 (every type-1
  attach genuinely cross-rank: the battery is in the B1
  class, not VOID); LIST D5A all 1, D5B all 1
  (unconstrained store expresses them). PASS.
- D5-2 (cycle impossibility on the stacked DAG,
  representational): RERANK D5C adv1=adv2=0, audit=0 on
  all three lines; LIST D5C adv1=adv2=1, audit=7 (every
  item 4..10 lies on a directed cycle once 10->4 closes
  the stacked structure; the adversarial probes are
  genuinely cycle-closing). No committed cycle on RERANK
  anywhere. PASS.
- D5-3 (rank invariant): RERANK inv=1 on all three
  lines; REP inv=1 on all three lines. The read graph is
  empirically strictly decreasing through 12 promotions
  including two 5-pass cascades over stacked diamonds
  plus cross-links. PASS.
- D5-4 (cross-link convergence): RERANK D5B
  promotes=10, maxrank=10, t1=10, dia1=1. The six
  stage-2 attaches (two slow-path cross-links + diamond
  2) compose via 6 promotions while all four diamond-1
  edges survive diamond 2's re-ranking. PASS.
- D5-5 (adversarial cascade on stacked diamonds; the
  limit probe): RERANK D5C promotes=12, maxrank=16,
  diverge=0, t1=10, t2=0, dia1=dia2=xl1=xl2=1. Each
  adversarial attach converged in 5 passes through two
  stacked diamonds plus cross-links (cap 23 not
  approached); both cycle-closing attaches stayed inert
  with all 10 type-1 edges preserved. PASS.
- D5-6 (determinism and hygiene): all three binaries
  3/3 byte-identical stdout, stderr empty on all 9 runs;
  only the environmental "zagd unavailable" notice in
  compile logs (same as D3); no `!(A && B)` in while
  conditions (grep-checked); pure Zag; safebin pinned
  znc throughout (toolchain guard verified at startup:
  `which python3 python` empty under safebin PATH).
  PASS.

## 4. Prediction discrepancies (all root-caused, none touch
## the bars' substance; see PREREG_AMENDMENT1.md)

One arithmetic slip in the hand-derivation: e_add(8,10,1)
pass 1 wrote t[7]:=9 instead of t[7]:=8 (the 7->8 edge
reads the already-updated t[8]=7, so 6<=7 fires and sets
t[7]:=8). The +1 cascaded into D5B maxrank (11->10) and
D5C maxrank (17->16). The mechanism's actual trace was
verified digit-for-digit by a scratch diagnostic
(/tmp/d5_diag.zag, not part of the battery): the live
rank vector after every e_add matches the corrected
trace exactly, the trace is a valid relaxation fixpoint,
the invariant holds, all 10 type-1 edges are readable,
and both cycle-closing attaches are inert. Every other
predicted bit and counter matched unamended.

## 5. Limits and generality notes

- Promotion is a total function of (store, parent,
  child): the stacked multi-diamond DAG needed no new
  logic beyond what the 2-structure chains and the
  single diamond exercised. Cross-links issued on the
  slow path composed exactly like diamond edges.
- The longest promotion used 5 passes (both adversarial
  attaches; the 8->10 attach used 4). The 23-pass cap is
  tied to the 24-item limit (longest readable path < 11
  here); a store with more items would need the cap
  revisited. Non-convergence still completes the write
  with the read graph a DAG.
- maxrank grows with promotion depth (16 here; heads
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
- The D3-flagged LIST latent bug (registered[24] at
  1984+1+it vs the i32 counter at 2008 for it=23) cannot
  fire here: max item is 10. It remains flagged for the
  parent lane.
- Scope: two stacked diamonds + two cross-links +
  adversarial probes, driver-issued attaches on a
  controlled state. No claim about arbitrary DAG shapes
  beyond this battery, 5k/10k scaling, or learner-issued
  DAG attaches.

## 6. Files

Lane `docs/lab/research-lead/overnight-20260928/formal_compose_dag5/`:
PREREG.md (frozen, commit eabf99981), PREREG_AMENDMENT1.md,
NAMECHECK.md, `d5_batt.zag` (battery), `d5_main.zag`,
`d5_shim_rerank.zag` / `d5_shim_rep.zag` /
`d5_shim_list.zag` (d5_rank shims), `d5_build.sh`,
`es_rerank.zag` (byte-identical to the D3 lane copy,
sha256 8a6de72312d0375bb32d76292dbf97cbb46c8b27d1ce5207a499799b1b051c1c),
`rr_prelude.zag`, `rr_es_rep.zag`, `es_list_rr.zag`
(byte-identical copies, cmp-verified), REPORT.md.
Build artifacts (`*_bin`, `d5_full_*.zag`,
`d5_compile_*.txt`, `*_run_*.txt`, `*_run_*.err`) are not
committed.

Commits local only, explicit pathspecs, no push.
