# TRIAL_RESULTS.md — SM1 self-observation loop (2026-09-19)

## Verdict: POSITIVE

The smallest meaningful self-observation loop runs natively and closes:
the system read its own audit ledger, derived a true conclusion about its
own behavior ("I refuse KILL on pinned slots 40% of the time — my pin
criteria are too loose"), predicted its own post-change behavior by
counterfactual self-simulation over recorded history (predicted 1 refusal),
deliberately tightened its pin policy as an audited op (50→80), and the
re-run under the new policy produced exactly the predicted 1 refusal.
The control scenario (already-strict policy, 10% refusal rate) did not
fire — the change is contingent on observed history, not hardcoded.
No falsification criterion triggered.

## Evidence

- Native trial: `trial/sm_trial.zag` (imports `memory_core.zag` op set +
  audit ledger from wave-2 memory agency), compiled with
  `znc_linux_x86_64_abed8aa1` (SHA-256
  `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`),
  executed on this Linux VM.
- Passing evidence: `trial/EVIDENCE_20260920T001954Z/`
  (`run.stdout`: 26/26 `CL_CHECK` actual==expected, `SM_FAILURES,0`,
  runner `TRIAL PASSED`).
- Key lines (`trial/EVIDENCE_20260920T001954Z/run.stdout`):
  - `SM_STAT,A_phase1,10,4,400,1,1` — 10 KILL attempts, 4
    `REFUSED_PINNED`, 400‰ rate, conclusion fired, predicted 1.
  - `CL_CHECK,a2_matches_prediction,1,1` — re-run refused count == predicted.
  - `CL_CHECK,a2_changed,1,1` — behavior actually changed (4→1 refusals).
  - `SM_STAT,B,10,1,100,0,-1` — control: 100‰ < 300‰, no fire, no POLICYSET.
  - `a_replay,0,0` / `b_replay,0,0` — ledger replay == live state (white-box);
    `a_clean_refusals,0,0` — refusals mutated nothing.
- Falsification criteria (PREREG.md): F1–F5 all clear. F1 and F2 were
  additionally validated by negative controls in /tmp (not in the trial
  dir): breaking `sm_simulate` (+5) yields `a_predicted,6,1` and
  `a2_matches_prediction,0,1` (F1 fires); forcing scenario B to fire yields
  `b_fired,1,0`, `b_threshold_unchanged,110,80` (F2 fires). The checks
  genuinely detect a wrong self-model and an unconditional change.
- Determinism: two consecutive binary runs produce byte-identical output.
  System code contains zero RNG (runner greps, clean). Adversity came from
  the hand-designed pressure curriculum, not sampling — verdict cleanly
  separates "the system is deterministic" from "the test was adversarial".

## What this establishes — and does not

- Establishes: a functional self-model loop satisfying all five criteria
  in SELF_MODEL.md §1 (ledger input, white-box derivation, self-prediction,
  audited deliberate change, verification). The "model" is not logging with
  extra steps: it predicts, and the prediction is checked against the
  system's own subsequent behavior.
- Does not establish: that the pin-threshold policy is good (thresholds,
  the 300‰ trigger, and the +30 step are protocol-fixed, as preregistered —
  same honesty boundary as MA1's protocol-fixed values); R27-style
  structural revision (still the open P1 gap); multi-policy or
  cross-regime self-modeling.

## Honest negatives / limits

- The counterfactual sim replays the system's *known* 5-step script over
  recorded ADD values; it does not discover the script from the ledger.
  Script-discovery from raw entries is harder and untested.
- The conclusion vocabulary is one fixed rule (rate ≥ 300‰). A richer
  self-model would derive which *kind* of refusal dominates; not built.
- SM1 scale is 8 slots / ~27 ledger entries. The scaling argument is in
  PREREG.md (self-model state O(1); observe O(window); sim O(ADDs)); the
  10× scale test is explicitly deferred to SM2.

## Next step

SM2 (preregistered in PREREG.md §Scale): 10× slots with a 10×-longer
designed curriculum, ledger window capped at 256 entries, wall-clock
budget per observe+sim pass; assert self-model state size unchanged and
per-pass cost linear in window only. Kill SM2 if per-pass cost grows with
store capacity rather than window length.
