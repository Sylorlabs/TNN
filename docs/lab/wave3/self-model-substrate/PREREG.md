# PREREG_SM1 — the self-observation loop (WRITTEN 2026-09-19, BEFORE ANY RUN)

## Hypothesis

A system whose only self-knowledge is its own audit ledger can (a) derive a
true, ledger-recomputable conclusion about its own behavior, (b) predict its
own behavior under a candidate policy change by counterfactual self-simulation
over recorded history, (c) deliberately change its policy as an audited op
contingent on (a)+(b), and (d) verify the prediction by running the new policy.
Scenario B (already-strict policy) must not fire: the change is contingent on
observed history, not hardcoded.

## Mechanics (native Zag, `trial/sm_trial.zag`)

Store: 8 slots, stage=KILL(3), `pin_threshold` starts at 50 (Scenario A) /
80 (Scenario B). Reuses `memory_core.zag` op set + audit ledger; adds two
audited ops: `SM_OP_OBSERVE=9` (slot 0, before==after snapshot so the generic
ledger-replay invariant holds) and `SM_OP_POLICYSET=10` (same convention).
Policy lives in trial code; every change is a ledgered deliberate act.

Deterministic curriculum (identical in A-phase-1, A-phase-2, B):
1. ADD values [90,70,55,40,30,20,10,5] → slots 0..7.
2. Pin pass: PIN every live slot with value ≥ threshold.
3. 8 pressure KILLs, each targeting the lowest-value live slot (ties → lowest
   index).
4. ADD [65,45]; pin pass.
5. 2 pressure KILLs, same selection rule.

Self-observation (`sm_observe`): scan own ledger → `kill_attempts`,
`refused_pinned` (rc==REFUSED_PINNED), rate = refused·1000/attempts.
Conclusion rule: rate ≥ 300‰ ⇒ "pin criteria too loose".
Self-prediction (`sm_simulate`): replay the 5-step script over the ledger's
recorded ADD values with candidate threshold T+30, re-deriving KILL targets
by the same lowest-value-live rule; output predicted refused count.
Fire rule: conclusion fired AND predicted < observed ⇒ `SM_OP_POLICYSET`
(old→new), ledgered. Verification: re-run the curriculum under the new
threshold; actual refused must equal predicted refused.

**No RNG anywhere in the system** (verified by grep in the run script). The
adversarial pressure is hand-designed; seeded harness RNG is not used at all.

## Hand-computed expectations (the falsification anchor)

Scenario A, phase 1 (T=50): pins slots 0(90),1(70),2(55). Kills:
s7✓ s6✓ s5✓ s4✓ s3✓ s2✗ s1✗ s0✗ (5 ok, 3 refused). ADD 65→s3 (pin), 45→s4.
Kills: s4✓, s2✗. **attempts=10, refused_pinned=4, rate=400‰.**
Conclusion fires (400 ≥ 300). Counterfactual sim at T'=80 over recorded ADD
values [90,70,55,40,30,20,10,5,65,45]: pins only s0; kills s7..s1✓, s0✗;
adds 65→s1, 45→s2 (no pins); kills s2✓, s1✓ → **predicted refused = 1**.
1 < 4 ⇒ POLICYSET 50→80 fires.

Scenario A, phase 2 (T=80, same curriculum): pins only s0(90).
**attempts=10, refused_pinned=1** (only the s0 kill), must equal predicted.

Scenario B (T=80 from start): identical to A-phase-2:
**attempts=10, refused_pinned=1, rate=100‰** → conclusion does NOT fire
(100 < 300); threshold stays 80; ledger contains zero POLICYSET entries.

## Falsification criteria (any one ⇒ NEGATIVE verdict)

- **F1 — the model doesn't model itself:** A-phase-2 actual refused ≠
  predicted refused (1). The counterfactual self-simulation is wrong.
- **F2 — not contingent on self-observation:** Scenario B fires a POLICYSET,
  or A's conclusion fires when rate < 300‰. The change is hardcoded /
  "logging with extra steps".
- **F3 — not white-box:** `ma_replay_check` ≠ 0 (ledger replay diverges
  from live state) or `ma_audit_clean_refusals` ≠ 0 (a refusal mutated
  state), or any system mutation lacks a ledger entry.
- **F4 — conclusion not from the ledger:** any printed derived statistic
  (attempts/refused/rate/predicted) ≠ hand-computed expectation above.
- **F5 — no behavior change:** A-phase-2 refused == A-phase-1 refused (4);
  the loop observed but changed nothing.

PASS requires: A fires exactly once, predicts 1, re-runs 1; B never fires;
replay clean; every `CL_CHECK` actual==expected.

## What this does NOT show

That the pin-threshold policy is *good* (thresholds and the 300‰/​+30 rules
are protocol-fixed here, like MA1's protocol-fixed values). Judgment
quality is future work. SM1 proves the *loop machinery*: ledger → true
self-conclusion → checkable self-prediction → contingent deliberate change
→ verification. It also does not show the R27 structural-revision
semantics; that remains the open gap (P1 STRUCT-PROMOTE).

## Scale dimension (program law)

- SM1 scale: 8 slots, ~27 ledger entries per phase, single-threaded, <1s.
- Self-model state: 6 i32 counters + 1 i32 threshold = **O(1) in store
  size and history length** (aggregation reduces history to tallies;
  the sim replays only the recorded ADD-value sequence of the window).
- Cost: one observe pass O(ledger window); one counterfactual sim O(ADDs
  in window). Both linear in the window, constant in store capacity.
- 10×/100× argument: store 8→80→800 does not grow self-model state; the
  window bounds the per-observe work. Nothing here is an N×N table; the
  mechanism is designed to scale by construction.
- Next scale test (SM2, explicit): 10× slots with 10×-longer designed
  curriculum, ledger window capped at 256 entries, wall-clock budget per
  observe+sim pass; assert self-model state size unchanged and per-pass
  cost linear in window only. Not run in SM1.
