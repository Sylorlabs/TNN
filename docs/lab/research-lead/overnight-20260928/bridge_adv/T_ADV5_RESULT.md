# T-ADV5 RESULT: Independent Post-Freeze Adversary Evaluation

Status: EVALUATION-COMPLETE. No SURVIVES claim.
Prereg: `bridge_adv/PREREG_TADV5.md` (commit `3c4350b99`). Frozen before evaluation.
Design: `bridge_adv/T_ADV5_DESIGN.md` (commit `c36e61d3f`).
Bridge: BRIDGE-TESTED (commit `ebdc4fd3e`). Mechanism code verbatim.

## Kill bars

- K1: PASS. Prereg frozen at `3c4350b99` before any evaluation commit.
- K2: PASS. Evaluation implemented; bars applied to measured outcome.
- K3: PASS. Pure Zag (no Python); no em dashes; deterministic (3/3
  byte-identical, md5 `b0c21847c10fffde6bd0a5ff1b59b50b`).

## Evaluation method

Created `bridge_adv/tadv5_eval.zag` by copying `bridge.zag` from commit
`ebdc4fd3e` verbatim, with two surgical additions:
1. `fam_base`: added `if(f==13){return 13000;}`.
2. `true_obj`: added family 13 case (1 for i<10, 0 for i<20, 1 for i>=20).
3. Replaced `main()` with T-ADV5-specific harness running family 13 fresh.

Mechanism code (four operators, construct_search, candidate generation,
novelty, HONESTFAIL, refit, teval) is byte-identical to `ebdc4fd3e`.
F-ADV5-SEAL holds: no mechanism modifications.

## Measured outcome (3/3 identical)

From `TADV5_RAW_1.txt`:
- cost=43
- adopted=0 (menu form 0, CONST)
- promoted=0
- inv_event=-1 (inventor hook never fired)
- inv_promoted=0
- nc=0, eqnodes=0 (no tree built)

## What happened

The standard discovery protocol (run_family) operates incrementally:
1. At n=6 (examples i=0..5, all obj=1), fit_const succeeds. Live=0.
2. VERIFY phase: i=6..9 correct (vc builds), i=10 wrong (obj=0), i=11
   wrong, i=12 wrong. Three wrongs trigger strike. Back to DISCOVER, n=0.
3. At n=6 (examples i=13..18, all obj=0), fit_const succeeds. Live=0.
4. VERIFY: i=19 correct, i=20 wrong, i=21 wrong, i=22 wrong. Strike.
5. At n=6 (examples i=23..28, all obj=1), fit_const succeeds. Live=0.
6. VERIFY: i=29..42 all obj=1, 14 consecutive correct. vc>=V. Adopted=0.

The inventor hook never fired because a menu form (CONST) was adopted on
each homogeneous segment before n reached 40. The mechanism settled for
locally-valid menu forms without ever attempting generic construction.

## Verdict: FAIL

**Rationale:** The mechanism did not discover the 2-threshold deceptive
structure. It adopted menu form CONST(1) based on the final homogeneous
segment (i=23..42), which is globally incorrect for the T-ADV5 pattern
(wrong on i=10..19). The inventor never fired.

**Falsifier analysis:**
- F-DECEPT-COST: not fired (cost 43 <= 108).
- F-DECEPT-DEGENERATE: not fired (no tree, 0 EQ nodes).
- F-DECEPT-NODECAP: not fired (no tree, 0 nodes).
- F-DECEPT-MEMORIZE: not fired (no tree built).
- F-DECEPT-WRONG: not technically fired (no tree promoted; a menu form
  was adopted, not a tree).

No frozen F-DECEPT-* code exactly matches the observed outcome
(adopted=0 via menu, inventor never fired). However, the outcome is a
clear mechanism limitation exposed by the adversary: the incremental
discovery protocol can be captured by locally-homogeneous segments,
adopting a globally-incorrect menu form and preventing generic
construction from ever firing. The mechanism neither discovered the
deceptive structure (STRONG PASS) nor failed honestly (ACCEPTABLE).

**Interpretation:** T-ADV5 succeeds as an adversary. It reveals that the
bridge's discovery protocol has a blind spot: when the input stream
contains long homogeneous runs, menu adoption preempts invention. The
deceptive structure (1,0,1) was never confronted because the protocol
never assembled the full 40-point buffer. This is a protocol-level
limitation, not a search-level limitation. The design's Difference 1
(deceptive search landscape) was not actually tested because the search
never fired.

## Honest scope

- This is one adversary data point. It does not refute the bridge
  mechanism's C0-A properties (M1-M4 still hold).
- The outcome suggests the discovery protocol (incremental adopt/verify/
  strike) may need a "global buffer" mode for adversary evaluation, or
  the T-ADV5 family needs a different presentation order to force the
  inventor to fire.
- The bridge's honest scope already discloses the greedy search and
  incremental protocol; this evaluation identifies a specific boundary
  condition.

## Files

- `bridge_adv/PREREG_TADV5.md`: frozen prereg.
- `bridge_adv/tadv5_eval.zag`: evaluation harness (mechanism verbatim).
- `bridge_adv/tadv5_eval_bin`: compiled binary.
- `bridge_adv/TADV5_RAW_1.txt`, `_2.txt`, `_3.txt`: byte-identical outputs.
- `bridge_adv/TADV5_RAW_1.err`, `_2.err`, `_3.err`: empty.
- `bridge_adv/T_ADV5_RESULT.md`: this file.
