# TRIALWALL_DIAGNOSIS: where the transfer refreeze actually blows up

Lane: ARENA-ENG, wave-20261002-0521pdt. Date: 2026-10-02 PDT.
Method: standalone instrumented prototype of the frozen TNN-2 trial-loop
core (`trialwall.zag`, trialwall_bin), extracted verbatim from
`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`, replicating
the sealed transfer T_A phase event-for-event (24 arithmetic-progression
training steps from TRANSFER_REFREEZE_PREREG.md section 3; every query is a
miss, matching the sealed `runs/run1/logs/T_A.log` where ans=-2 on all 17
completed steps). Write-only counters added in header fields 52/56/60 and
the write-only event-log slots (log verified write-only: `lg()` never called
in tnn2.zag). Pure Zag, pinned znc, safebin, no python3.

## 1. The sealed-attempt numbers (from TRANSFER_REFREEZE_RESULT.md)

Per-step wall clock, T_A phase, real frozen TNN-2 via frozen shim:
steps 0-14: 28ms - 390ms each; step 15: 72,646ms; step 16: 124,070ms;
step 17+ never completed. Every query missed (ans=-2), so the trial loop
ran in full on every query and never promoted anything.

## 2. Profile: which branch runs (prototype, per query)

| branch | verifies/query (typical) | graph size per trial |
|--------|--------------------------|----------------------|
| chain (k=2..4) | 0 | n/a (no paths of length 3-5 exist) |
| sum (subsets) | 0 | n/a (comb_present<0; gate closed) |
| count | 4-6 | <=16 links, small |
| single-hop | 4-6 | 1 link, small |

d_chainv=0 and d_sumv=0 on EVERY step 0-15. The sum branch NEVER executes
in the transfer scenario: `comb_present(W)` scans for a type-8 node, and
nothing in the frozen shim, driver, or world files creates one (the only
type-8 allocation in the codebase is inside the `t_p2` unit test).

CORRECTION to TRANSFER_REFREEZE_RESULT.md section 5: its root cause
("sum branch enumerates ALL subsets ... each allocating hundreds of cells")
is factually wrong for the sealed transfer runs. The sum branch is gated
off. The wall is elsewhere.

## 3. Profile: the actual blowup (prototype, steps 0-15)

Per-step deltas (ORIG mode, verbatim trial loop):

- d_alloc (alloc_node calls): 55-81 per step, steady. Trial garbage:
  ~10 small failed-candidate graphs + execute frames + miss_inquire nodes
  per query. Nothing is ever freed.
- Live nodes hg(W,20): 56, 124, 205, 260, 328, 383, 451, 532, 587, 642,
  710, 791, 846, 901, 969 at steps 0-14; 1022 at step 15.
- d_evict (evict_node calls): 0 on steps 0-14; 28 on step 15.
- Wall clock: steps 0-14 total 4.3s; steps 0-15 total 88.2s.
  Step-15 marginal ~84s, vs 72.6s in the sealed real-binary attempt.
- d_exec (execute cell-steps) at step 15: 32. Execution is NOT the cost.

Mechanism: the workspace has a FIXED 1024 node slots. Trial garbage
accumulates ~65 nodes/query with no reclamation, so the table fills at
step ~15. From then on every alloc_node falls through to evict_node,
which scans 1024 nodes and computes bid() per node; bid() does ~5
O(4096) edge scans plus a MEM-edge fanout loop. Measured: ~3s per
eviction, 28 evictions on step 15. Cost per eviction GROWS as the table
stays full, which is why step 16 (124s) is worse than step 15 (72s)
despite smaller term values: the blowup tracks workspace fullness, NOT
term values. There is no branching-factor explosion; it is trial-garbage
accumulation into a fixed-size table with a catastrophic eviction path.

## 4. What this means for the fix

The trial loop's SEARCH is cheap (small graphs, few candidates, all
rejected fast). The wall is pure resource hygiene: dead trial graphs are
never reclaimed. Any approach that reclaims provably-dead trial memory
breaks the wall without touching search order, verify outcomes, or
promotion. The failed candidates are unreachable from all live structures
by construction (only t2_trial holds the root; on reject it is dropped),
so freeing them cannot change any observable trial outcome.

Approach selected for the frozen prereg: EAGER RECLAMATION OF DEAD TRIAL
GRAPHS (free-on-reject graph walk + per-reject edge sweep + scratch-frame
freeing inside t2_exec). See PREREG_TRIALWALL.md.
