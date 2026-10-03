# PREREG.md -- IVWC-ORACLE-FREE: verification with zero consequence observations

Frozen: 2026-10-03. This document fixes the experimental design and
the kill bars K1..K8. It must be committed ALONE (with NAMECHECK.md,
no implementation) before any implementation work. The prereg commit
must strictly precede the implementation commit. Amending a bar after
results invalidates the verdict.

## 1. What this wave is

IVWC-EXPAND3 showed the learner can self-verify pre-execution, but
its verifier trains on TRUE consequences: train plans are executed
on true worlds (train CONSEQ phase) and the bucket table aggregates
(bucket, eff) pairs from those true outcomes. The sealed verdicts
never see sealed truth (commit-before-signal), but the verifier's
training diet is ground-truth outcome data.

This wave removes ALL consequence observations. The learner never
executes any plan on any true world before verdicting -- not in
train (there is no train phase at all), not in commit. Verification
is derived purely from beliefs + committed plans:

- **Arm A (internal-model consequence prediction).** The learner
  steps each committed plan through its OWN beliefs
  (`belief_execute`: same physics shape as the true stepper, but
  reading belief arrays). Predicted eff P = 100*pred_collected /
  pred_energy. Verdict PASS iff P >= T_pred, where T_pred is the
  learner-computed mean of the 12 sealed predicted effs (internal
  batch bar; no world data, no researcher constant). Operational
  meaning of "verification without ground truth": the plan succeeds
  in the learner's own model of the world. Its worth is the model's
  fidelity, measured by the harness against true sealed outcomes
  the learner never observes.
- **Arm B (re-derivation self-consistency).** Two independent
  composers (reverse scan order; greedy nearest-first) recompose
  each sealed case from the same beliefs; the gather-target sets
  are compared. Analytic result (verified empirically in §5):
  the gather set is order-invariant for this composer family, so
  agreement is near-vacuous; this arm is a FINDING, not a bar --
  it tests the task's "self-consistency" suggestion and reports
  the negative honestly.
- **Ablation (belief-content).** The Arm A verdicts are recomputed
  with predictions from scrambled beliefs (independent Fisher-Yates
  on believed walls/items, fixed seed; marginals preserved,
  wall/item mapping broken), against the shared internal bar
  T_pred. Mirrors expand3's K6: shows the accuracy is driven by
  belief CONTENT, not by the prediction machinery alone.

Incorporated by reference (verbatim copies): the world generator,
the belief generator, the NAV+GATHER composer, the true-world
stepper, all frozen seeds, the wp=15/30/45 law-change dial, and
the 12 sealed case identities -- from
ivwc_expand3/PREREG.md and ivwc_expand3/src/ivwc_expand3.zag.
The sealed (bucket, eff) pairs are therefore bit-identical to
expand3's run1 (checked in shell at report time; a finding, not
a bar). The revision protocol is removed (it consumed true
execution evidence; belief-simulated revision would be vacuous).

## 2. Frozen kill bars

Notation per sealed shift: np/nf = #verdict-PASS/#verdict-FAIL;
sp/sf = sum of true sealed eff over PASS/FAIL sets; acc =
#{verdict_A == (eff >= T_pred)}/12; maj = majority share of the
(true) class (eff >= T_pred); acc_ab = ablated accuracy vs the
same class; FP/TP = false/true PASS sets at wp=15 with mean
whole-map belief-error counts (believed-vs-true wall+item cells).

- K1 (commit before signal): PASS iff the world-call counter is
  unchanged across each shift's VERDICT COMMIT block AND the
  section-4 audits confirm code ordering and the learner section
  contains no world-truth tokens.
- K2 (oracle-free diet): PASS iff the section-4 audits hold: no
  expected|answer|key|target tokens; no
  correct|reference_plan|gold tokens; `world_execute(` occurs
  exactly twice in the source (one definition, one call site,
  the sealed scoring block); the LEARNER section contains zero
  `world_` tokens; final world-call count == 36 (12 x 3 shifts).
- K3 (Arm A discriminates, wp=15): PASS iff np > 0 and nf > 0
  and sp*nf > sf*np (strict). Mean true eff of the
  predicted-PASS set must strictly exceed that of the
  predicted-FAIL set.
- K4 (Arm A beats trivial, wp=15): PASS iff acc > maj (strict),
  with the class boundary T_pred learner-computed (no researcher
  constant anywhere in the bar).
- K5 (determinism): PASS iff 3 runs byte-identical (equal sha256).
- K6 (belief-content ablation, wp=15): PASS iff acc_ab < acc
  (strict). Scrambling the beliefs must strictly degrade the
  verdict accuracy against the shared internal bar.
- K7 (edge degrades under law change): PASS iff
  (acc_45 - maj_45) < (acc_15 - maj_15) (strict). The
  internal-model verifier's edge over the trivial rule must
  shrink under strong law change (mirror of expand3 K8).
- K8 (failures concentrate on belief error, wp=15): PASS iff
  |FP| > 0 and |TP| > 0 and mean_err(FP) > mean_err(TP)
  (strict, cross-multiplied). The internal model's false-PASS
  cases must carry strictly more belief error than its
  true-PASS cases -- the predicted limit of oracle-free
  verification: it is blind to its own belief errors.

Verdict: BUILD-PASS iff K1..K8 all PASS. Any FAIL yields
BUILD-FAIL naming the failed bar. VOID conditions: any
forbidden-interpreter invocation (PROCESS-FAIL), or any amendment
to this prereg after implementation begins.

## 3. What is NOT claimed

Mechanism test of oracle-free verification, not a
composition-novelty or L3 claim. The composer is fixed; the claims
concern whether pre-execution self-verdicts derived with zero
consequence observations discriminate sealed outcomes, what
drives them (belief content), where they break (law change,
belief error). One wall-density law-change axis; item law, belief
noise, and energy budget fixed. The sealed scoring pass is harness
ground truth used ONLY for scoring, never observed by the
learner.

## 4. Frozen audit commands (run at report time, shell only)

- A1 (phase ordering): in src/ivwc_oraclefree.zag, within the
  sealed shift loop, the VERDICT COMMIT block (learner_compose /
  belief_execute / learner_compose_rev / learner_compose_nn /
  belief_scramble call sites, no world_execute) textually precedes
  the SCORING block's world_execute call site. Verified by
  reporting grep -n line numbers.
- A2: the LEARNER section (between the `// ===== LEARNER =====`
  and `// ===== MAIN =====` markers) contains zero occurrences of
  `world_buf` or `world_off`.
- A3: zero occurrences of `expected|answer|key|target` in the
  .zag (grep -c -E).
- A4: zero occurrences of `correct|reference_plan|gold` in the
  .zag (grep -c -E).
- A5: sha256 equality across runs/ivwc_oraclefree-run{1,2,3}.txt.
- A6 (oracle-free diet): `grep -o "world_execute("
  src/ivwc_oraclefree.zag | wc -l` == 2 (one definition, one call
  site); the call site passes wseal inside the SCORING block;
  WC-FINAL printed == 36.
- A7 (learner information diet): the LEARNER section contains
  zero occurrences of `world_` (grep -c).

## 5. Why the bars discriminate, and calibration note

- K3/K4 are the direct operationalization of priority #4: they
  fail if internal-model predictions carry no signal about true
  outcomes (e.g., if the internal model were pure noise, or if
  belief error dominated everywhere).
- K6 fails if the verdict accuracy came from the prediction
  machinery alone rather than belief content (scrambled beliefs
  would then score identically).
- K7 fails if law change does not erode the internal model's
  value over the trivial rule.
- K8 fails if the verifier's mistakes are unrelated to belief
  error (the predicted limit would be wrong).
- Arm B is deliberately NOT a bar: analysis shows the gather set
  is order-invariant for this composer family (any
  visit-in-some-order/take-if-reachable composer yields exactly
  {c : believed item at c, believed [start,c] clear}), so
  re-derivation agreement is near-vacuous here; the wave reports
  the agreement rate as a finding (the honest negative for the
  "self-consistency" suggestion).

Calibration: bar DIRECTIONS above are theory-motivated and were
fixed before any probe run. A pre-prereg probe binary in /tmp
(uncommitted, labeled PROBE, same mechanism) was used ONLY to
confirm the bars are non-degenerate (both verdict classes
nonempty, FP/TP sets nonempty, audits satisfiable) -- not to
choose directions. The frozen verdict is computed from the three
post-prereg runs of the committed source. The final source may
differ from the probe in print/diagnostic details only; any
difference is documented in REPORT.md.
