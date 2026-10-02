# BRIDGE RESULT: L3 Bridge (generic construction replacing recipes)

Status: BRIDGE-TESTED (K2=1). No SURVIVES claim.
Prereg: `PREREG_L3BRIDGE.md` (commit `19ce88021`). Frozen before implementation.
Design: `l3_bridge/L3_BRIDGE_DESIGN.md` (commit `e4f8642fc`).

## Kill bars

- K1: PASS. Prereg frozen at `19ce88021` before any implementation commit.
- K2: PASS. Bridge implemented; frozen battery expectations met (see below).
- K3: PASS. C0-A audit M1-M4 passes on committed `bridge.zag` (see section
  "C0-A audit").
- K4: PASS. Pure Zag (no Python in source, scratch, diagnostics, or
  verification); no em dashes in loop documentation; deterministic
  (3/3 byte-identical runs).

## What was built

`bridge.zag` derives from `form_inventor/inventor.zag` (commit `1b8e032c4`).

REMOVED (deleted):
- `diagnose()` signature enum and all branches.
- `build_tree(st, sig, dp)` and all three recipe branches.
- `node_count(sig)` lookup.
- Sig-keyed `novelty_check()`.

ADDED:
- Four generic operators: `op_const_leaf`, `op_split_lt`, `op_split_eq`,
  `op_prune`. Every `setnode` call in the file occurs inside one of these
  four (M3 verified).
- Generic candidate generation: LT thresholds at output boundaries among
  sorted distinct covered subject values; EQ values among covered values
  whose output differs from the leaf majority; split constants by majority
  vote per side. Candidate order frozen: leaves in index order, LT before
  EQ, increasing parameter.
- `construct_search(st, bs, bo, n, cost)`: greedy hill-climbing. Gain =
  correct-after minus correct-before (B_node = 0, frozen and disclosed).
  Applies the single best strictly positive-gain move per round. Stops on
  no positive gain, 8-node cap, or 24-move budget. Returns 1 iff exact fit.
- Generic behavioral novelty: no menu form (0/1/2) and no live invented
  form fits the buffer.
- Generic HONESTFAIL.
- Refit via fresh `construct_search` on the 4-example buffer in scratch;
  adopt iff exact fit AND structurally equivalent to the live tree (same
  node count, same ops, same child pointers; values ignored).

FAMILY 12 (T-ADV4, frozen in prereg): step with embedded exception.
true_subj(12,i)=12000+i; true_obj: i<5 ? (i==2 ? 9 : 0) : 5. The old recipes
cannot build it (diagnose returns 0). The search builds
IF(x<12005, IF(x==12002, 9, 0), 5): 7 nodes, 1 EQ node.

## Battery results (from BRIDGE_RAW_FINAL.txt, deterministic)

FRESH:
- G (6): cost 62, adopted 3, promoted 1. (ceiling 108)
- H (8): cost 68, adopted 3, promoted 1.
- K (10): cost 68, adopted 3, promoted 1.
- J (9): cost 181, adopted -1, HONESTFAIL. No promotion.
- T-ADV4 (12): cost 70, adopted 3, promoted 1. 7 nodes, 1 EQ node.

RETAINED (A,B,C,D,E,G,Gp,H,G2 on persistent state):
- A-E: adopted 1, costs 20/11/8/6/5 (exact, unchanged).
- G: adopted 3, refit 0 (strike: rebuilt tree not structurally equivalent
  to live), re-invented, cost 62.
- Gp: adopted 3, refit 1 (rebuilt step tree structurally equivalent to
  live step tree), cost 17.
- H: adopted 3, refit 0 (strike), re-invented, cost 65.
- G2: adopted 2 (menu form), refit 0, cost 26 (includes refit search
  overhead of 6).

All falsifiers silent: no F-RECIPE, no F-NOVEL-FAIL, no F-DEGENERATE
(max 2 EQ nodes observed, cap 4), no F-COST, no F-MENU-REDUCIBLE.

## C0-A audit (frozen M1-M4; runnable by third party)

- M1: PASS. `sig==1`, `sig==3`, `sig==4` return zero hits. `node_count`
  and `build_tree` appear once each, both in the header comment explicitly
  marking deleted legacy code ("REMOVED: ...").
- M2: PASS. `construct_search(st:[]u8, bs:[]u8, bo:[]u8, n:i32, cost:[]u8)`
  accepts the failure buffer and budgets; no diagnosis enum.
- M3: PASS. Every `setnode` call occurs textually inside `op_const_leaf`,
  `op_split_lt`, `op_split_eq`, or `op_prune`. (Simulation restore in
  `construct_search` uses direct `set32` field writes, not `setnode`.)
- M4: PASS. `teval` is byte-identical to the INVENTOR-TESTED commit
  `1b8e032c4` version; dispatches only on operator codes 0..3.

Any M-check failure would have voided the C0-A claim. None failed.

## Disclosed deviations and optimizations

1. B_node = 0 (prereg disclosed): gain is pure correct-count improvement.
   Rationale: any positive per-node cost vetoes genuine single-exception
   splits (1 fix vs 3 nodes). Complexity is controlled by the 8-node cap,
   24-move budget, and F-DEGENERATE EQ cap.
2. Candidate pruning (implementation optimization, does not change the
   argmax): LT thresholds only at output boundaries; EQ values only where
   output differs from leaf majority. A non-boundary LT threshold can be
   slid to a boundary without decreasing gain; an EQ split of a
   majority-output point cannot have positive gain.
3. Refit adopts the rebuilt tree (not just refreshes params) when
   structurally equivalent. This preserves the old "same form?" semantics
   without signatures.
4. Retained G2 cost is 26, not 20 (refit search overhead). The prereg did
   not freeze retained G2 cost; the check uses a bound (<=30).

## What this does NOT claim

- No L3 claim. C0-C (independent post-freeze adversary) and C0-D
  (cognitive reuse) remain open per design section 8.
- T-ADV4 was designed by the builder after the prereg freeze, not by an
  independent party. It is a step toward C0-C, not C0-C.
- Residual researcher footprint (disclosed in design section 8): operator
  vocabulary {const, <, ==, if}; B_node=0 and the gain rule; budgets
  BMAX/node-cap/move-budget/cost-ceiling. OP-RECRUIT v2 is the track that
  removes the operator-vocabulary footprint.

## Files

- `bridge.zag`: implementation (pure Zag).
- `bridge_bin`: compiled binary (build artifact, not for attribution).
- `PREREG_L3BRIDGE.md`: frozen prereg.
- `BRIDGE_RAW_FINAL.txt`: authoritative deterministic output (3/3 identical).
- `BRIDGE_RAW_1.txt` through `BRIDGE_RAW_5.txt`: intermediate runs
  (superseded; kept for audit trail).
- `BRIDGE_RESULT.md`: this file.
