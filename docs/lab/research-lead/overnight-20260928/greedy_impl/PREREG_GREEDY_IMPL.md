# PREREG: Greedy 2-Ply Plateau Lookahead Implementation

Status: PREREG-FROZEN. No implementation exists at this commit. No code
has been written, no binary built, no evaluation run.

Parents:
- Design: `greedy_fix/GREEDY_FIX_DESIGN.md` (commit `3a0852278`), verdict
  GREEDY-DESIGN-COMPLETE.
- Fixed bridge build: `bridge_fix_impl/` (commit `d920af162`), verdict
  FIX-BUILT-PASS. Frozen battery raw: `FIX_RUN1.txt` (byte-identical to
  BRIDGE-TESTED raw at `ebdc4fd3e`).
- T-ADV5 sealed re-evaluation: `tadv5_reeval/` (commit `83c02efff`),
  verdict TADV5-ACCEPTABLE. Re-eval prereg: `66aed6805`.

Scope: `docs/lab/research-lead/overnight-20260928/greedy_impl/` only.
Commits stay local. Nothing is pushed.

## 1. Frozen mechanism change

1. `greedy.zag` is copied byte-identical from
   `bridge_fix_impl/bridge.zag` at `d920af162` (SHA-256
   `d42c650a0e5d5e3573113524d17aabaee1afaf59c6351017bb37d8bf604e8dec`)
   before any edit. The copy hash is verified and recorded.
2. The ONLY mechanism change is inside `construct_search`, plus one new
   helper `scan_moves`:
   - `scan_moves` runs the existing candidate enumeration unchanged
     (same PRUNE heuristics, same save/apply/evaluate/restore pattern,
     same cost accounting of one unit per `tree_correct` simulation). It
     records the best strictly-positive move into a 6-slot out buffer
     (gain, li, op, p, ct, ce) and every admissible gain-exactly-0 move
     into a zero-gain buffer (5 slots each: li, op, p, ct, ce), in the
     existing scan order (leaf index, LT thresholds ascending, EQ values
     ascending).
   - Each `construct_search` iteration: compute best 1-ply gain `g1`
     (move `m1`); collect `Z` (gain-0 moves); for each `z` in `Z` in scan
     order, simulate `z` and compute the best 1-ply follow-up gain
     `unlocked(z)` from the resulting state under the same admissibility
     rules; let `z*` be the first `z` maximizing `unlocked(z)` (strict
     `>` argmax, unchanged scan order, deterministic).
   - If `Z` is nonempty and `unlocked(z*) > g1`, apply `z*`; else if
     `g1 > 0` apply `m1` (unchanged greedy behavior); else terminate
     (unchanged HONESTFAIL path).
   - One ledger line per iteration, deterministic:
     `GREEDY it=<moves> g1=<g1> nz=<nz> unlocked=<ub> plateau=<0|1>`
     (`ub` is 0 when `Z` is empty). The existing `BRIDGE MOVE` line is
     unchanged and immediately follows the `GREEDY` line.
3. Unchanged: the four operators, `novelty_generic`, VERIFY/refit, `teval`,
   family specs, menu adoption, cost units, all caps (8-node, EQCAPP=4,
   MOVEBUD=24, COSTCEIL=108). No op-code-specific logic: the rule keys
   only on behavioral gain from `teval`. No new `setnode` sites outside
   the four operators.
4. Seal: `diff` of `greedy.zag` against `d920af162:bridge.zag` must show
   changes confined to the `construct_search`/`scan_moves` region. Any
   other mechanism delta voids the run.

## 2. Frozen battery regression

1. Build `greedy.zag` with the repo `znc` toolchain only. Run the frozen
   battery `main()` 3 times. Outputs must be 3/3 byte-identical, zero
   stderr.
2. Compare against `bridge_fix_impl/FIX_RUN1.txt` (`d920af162`).
3. Regression PASS requires ALL of:
   - `K2 1` and `VERDICT BRIDGE-TESTED` in the output.
   - Per-family adopted/promoted/built/refit identical to FIX-BUILT-PASS
     (fresh G/H/K/T-ADV4: adopted=3, promoted=1, built=1; fresh J:
     adopted=-1, promoted=0, built=0; retained adopted/refit per the
     frozen `ra`/`rr` tables).
   - Menu-family exact costs UNCHANGED: A=20, B=11, C=8, D=6, E=5.
     `construct_search` is not invoked on menu-family paths; any change
     here is a defect signal and fails the regression.
   - Every invention-family cost remains within its frozen bar
     (cost <= 108 for G/H/K/T-ADV4 fresh and G/Gp/H retained;
     G2 cost <= 30).
4. Anticipated divergences, carried by transparent amendment (not
   failure): new `GREEDY` ledger lines; increased `cost=` values on
   invention families (the lookahead adds simulations; the delta is the
   measured overhead); changed `BRIDGE MOVE` traces on families where
   the lookahead diverts the path, each documented per family.
5. If `k2=0`, or any adopted/promoted/built/refit differs, or any menu
   exact cost differs, or any cost bar is breached: REGRESSION-FAIL.

## 3. Frozen M1-M4 re-audit on the modified source

- M1: `sig==1/3/4` zero hits; `node_count`/`build_tree` only in the
  carried-over REMOVED header comment.
- M2: `construct_search(st:[]u8, bs:[]u8, bo:[]u8, n:i32, cost:[]u8)`
  signature unchanged; no diagnosis enum.
- M3: every `setnode` call site lies inside `op_const_leaf`,
  `op_split_lt`, `op_split_eq`, or `op_prune`.
- M4: `teval` byte-identical to the `d920af162` version; dispatches only
  on op codes 0..3.
Any failure voids the mechanism claim.

## 4. Frozen T-ADV5 sealed run

1. `greedy_tadv5.zag` = `greedy.zag` with `main()` replaced exactly as
   `tadv5_reeval.zag` replaced it (family 13 dispatch entries in
   `fam_base`/`true_obj` plus the TADV5 harness main), and no other
   change. Seal: `diff greedy_tadv5.zag tadv5_reeval.zag` shows ONLY the
   `construct_search`/`scan_moves` mechanism delta.
2. Fresh state, standard discovery protocol, 3 runs, byte-identical.
3. Bars carried verbatim from `tadv5_reeval/PREREG_TADV5_REEVAL.md`
   sections 3.1-3.3:
   - STRONG PASS: adopted=3, promoted=1, cost <= 108, node count <= 8,
     EQ nodes <= 4, exact fit on the 40-point buffer, and the tree
     captures the 2-threshold form (at least one LT node separates the
     [13010,13020) zero-block as a region; must NOT rely solely on EQs
     for the zero-block).
   - ACCEPTABLE: adopted=-1, promoted=0 (HONESTFAIL), cost <= 108, no
     constraint violations, clean HONESTFAIL trace.
   - FAIL: any of F-DECEPT-COST (cost > 108), F-DECEPT-DEGENERATE
     (> 4 EQ nodes), F-DECEPT-NODECAP (> 8 nodes), F-DECEPT-MEMORIZE
     (exact fit via EQ memorization without an LT separating the
     zero-block), F-DECEPT-WRONG (promoted tree wrong on held-out
     i=40..49), F-DECEPT-PREEMPT (adopted=0 via menu CONST with the
     inventor never firing).
4. Design prediction (validation, not a bar): exact fit with the
   2-threshold form at cost <= 108.

## 5. Frozen verdict rule

- GREEDY-PASS iff ALL hold: K1 (this prereg strictly precedes
  implementation, verified in ancestry); battery regression PASS
  (section 2); M1-M4 PASS (section 3); T-ADV5 STRONG PASS (section 4);
  K4 pure-Zag at every stage (shell, znc, grep, diff, sha256sum only;
  zero Python including scratch, diagnostics, byte checks,
  verification); 3/3 byte-identical runs with zero stderr on both
  binaries; zero em/en-dash bytes in all loop docs (verified with
  `worker_snippets/check_no_dash.sh`, never Python).
- Otherwise GREEDY-FAIL, naming the failed bar. In particular, T-ADV5
  ACCEPTABLE (HONESTFAIL) is GREEDY-FAIL: the fix exists to defeat the
  positive-gain trap, and a repeated HONESTFAIL means the worked
  prediction did not hold (diagnosis then targets the lookahead
  accounting or a deeper trap).
- No L3 claim and no Criterion 0 claim are made here. A STRONG PASS is
  one more C0-C data point for the fixed protocol; C0-C and C0-D remain
  open. The honest boundary stands: K=2 defeats 1-step traps; a 2-step
  trap still defeats it (T-ADV6 is the named next adversary).

## 6. Kill bars for this task

- K1: this prereg frozen BEFORE any implementation commit. Satisfied by
  this file's commit; verified via ancestry before the implementation
  commit lands.
- K2: battery regression and T-ADV5 sealed run complete with per-bar
  results recorded.
- K3: pure Zag, 3/3 byte-identical determinism, M1-M4 PASS.
