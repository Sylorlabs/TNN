PROPOSED measurement configs — NEVER EXECUTED against the frozen batteries.

The prereg §2 measurement matrix could not run: 0/877 frozen battery/red-team
items parse in the frozen harness (see RESULTS_H5.md). These configs are the
execution crew's PROPOSED mapping of the frozen DEPTH_DEF.md v1 values onto
the frozen harness's config keys, staged for H5 coordinator review/approval
under prereg §12 (amendment) before any measurement leg runs:

  rounds_shallow=2 / rounds_deep=16 / rounds_baseline=1 / sweep 1,2,4,8,16
    -> sweep p in {1,2,4,8}: mode=shallow, shallow_rounds=p
    -> sweep p=16:           mode=deep, deep_rounds=16
  adaptive_epsilon=0.02 -> epsilon=20 (thousandths)
  adaptive_k=3          -> adaptive_min_rounds=3, stability_window=3
  adaptive_cap_rounds=16 -> adaptive_max_rounds=16 (= rounds_deep, enforced)
  (DEPTH_DEF has no confidence threshold -> conf_threshold=0, vacuous)
  elim_margin=900, refute_threshold=600, evidence_cap=64
    -> frozen deliberation-procedure params, carried over from the smoke
       configs the determinism proof was recorded with (judge held constant;
       only the depth level varies).

KNOWN FORMAL GAP (documented, not hidden): the frozen harness's adaptive rule
is not DEPTH_DEF §6 verbatim. DEPTH_DEF: stop iff r>=k and |c_i - c_{i-1}| < e
for the last k rounds. Harness (dlb_delib.zag, frozen): stop iff r>=amin,
r>=stab_win, conf>=conf_thr, leader unchanged over last stab_win rounds, and
margin[r]-margin[r-stab_win] < epsilon. Differences: (a) harness uses
cumulative margin gain over the window, not per-round absolute gains;
(b) a margin DROP (negative diff) counts as "settled" in the harness but
keeps deliberating under DEPTH_DEF's |gain|; (c) harness adds the
leader-stability condition; (d) conf_threshold is extra (set to 0 = vacuous
here). With conf_threshold=0 these configs are the closest implementable
approximation of the frozen rule on the frozen harness. If the coordinator
wants the DEPTH_DEF rule verbatim, the harness needs a code change (new
frozen commit + re-proof of determinism), not a config change.
