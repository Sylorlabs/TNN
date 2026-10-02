# B-T5 frozen spec — programmatic extract

Source: units/PREREG_FREEZE.md (§2, lines 371-451)
SHA-256 of source file: 0e07ad031a808782cd41e711ccee90995cd36584ade4c303b4a3364d35063863
Extraction command:
  sed -n "371,451p" units/PREREG_FREEZE.md
Extracted: 2026-09-21 (UTC), by MARATHON CREW 5

```
## §2 — Track R0: R31 full native redo (Micah's decision, 2026-09-21)

R31 endogenous chunking is **redone in full, natively in Zag, with all tests re-run** — not
referenced, not reduced to two arms. This track validates the resurrection claim AND supplies
the native implementation + validated parameters that arm D and the predictive-surprise arm
are built on.

### R0.1 Scope — five batteries, reimplemented against the native substrate

1. **Tournament** — native re-run of the 8-arm tournament (predictive_surprise,
   random_chunks, fixed_window_4, MDL variants, raw_micro/no-chunking) on byte streams of
   text/code.
2. **Causal ablation** — raw_active vs chunk_active vs dual_active hard grounding, native;
   near-twin discrimination included.
3. **Dose curve** — 250 → 8000 training units natively; bar is no degradation.
4. **Split/merge dynamics** — recovered Zag dynamics: split fires iff `use_count ≥ 3 AND
   conflict ≥ learned_conflict AND utility ≤ learned_utility_floor`; merge fires iff
   `pair_seen ≥ learned_pair_seen AND joint_gain − separate_regret ≥ learned_gain`. Bar:
   dynamics occur, are ledger-auditable, boundaries shown mutable (a recruited chunk split
   then re-merged on the record).
5. **Support-gap recruitment** — teacher supplies only a grounded whole experience; learner
   recruits the largest unsupported raw span iff it meets learned min-support and beats the
   runner-up by a learned margin, else abstains (−1). Bar: hard-battery performance holds
   across 1–16 exposures.

All five run at **1x first; 10x only after the 1x replication bars pass** (R-9). Pure Zag,
zero RNG in AI decision paths, N=5 + adversarial perturbations hard gate.

### R0.2 Replication-fidelity bars (qualitative orderings — pass/fail)

- **B-T1 Tournament:** `predictive_surprise > fixed_window > raw_micro`, raw_micro (no
  chunking) **dead last**. (Full reference ordering, REFERENCE_ONLY:
  predictive_surprise ≫ random_chunks ≈ fixed_window_4 > MDL variants > raw_micro.)
- **B-T2 Ablation:** `dual_route ≈ raw_active` on hard grounding (within tolerance ε,
  R-3) **while adding compression** (minimum ratio, R-3); **chunk-only is rejected**
  (must lose to dual/raw on hard grounding).
- **B-T3 Dose curve:** flat or non-decreasing across 250 → 8000; no degradation
  (tolerance, R-4).
- **B-T4 Support-gap:** hard-battery score at or above floor (R-5) across 1–16 exposures;
  no collapse at 1 exposure.
- **B-T5 Dynamics:** split/merge fire under recovered conditions and are auditable; exact
  counts are REFERENCE_ONLY.

### R0.3 REFERENCE_ONLY handling

All old Python numbers (tournament 0.7376/0.4988/0.4928/~0.47/0.4489; ablation
0.9213/0.7533/0.9209; dose 0.36–0.40; support-gap 0.89–0.92) are **REFERENCE_ONLY**:
ordering constraints, never targets. The native redo is what counts as evidence. Hitting an
old number exactly is not required; violating an ordering is a replication FAIL.

### R0.4 "Grounded consequence" for text/code (PROPOSED — R-1, load-bearing)

Purity is operationalized as the **majority-label fraction** over grounded consequence labels,
where a consequence label for a span occurrence is defined by **(a) recall success** of the
span in a probe episode and **(b) downstream discrimination consistency** (the span's presence
predicts the same probe outcome across occurrences). Micah must approve/amend — the redo
cannot be built without this definition.

### R0.5 Anti-exploit and architecture requirements

- **Giant-span compression exploit explicitly barred** (L_max cap, R-2; compression term
  capped/weighted so grounding dominates — the reference docs rejected this exploit as a
  criterion and so does this prereg).
- **Dual route, not chunk-only**, is what gets preregistered (the old verdict rejected
  chunk-only; raw matched dual on hard grounding, so chunks must earn their place as
  compression/indexing with the raw route intact).
- **Test-both legs** for redo judgment calls (R-7): purity definition, promotion thresholds,
  inventory size — recovered-parameter leg vs re-derived leg, both run.
- **Redo feeds arms D and predictive-surprise:** the native implementation + validated
  parameters are their baseline. **Non-overlap rule:** the redo track validates the mechanism;
  arms D / F-S / F-B test it in the bake-off. Numbers are not double-counted across tracks.

### R0.6 Redo kill conditions

- Any B-T1…B-T5 ordering violated at 1x → replication FAIL; the resurrection claim is
  suspended pending a dated amendment (the arm D line does not proceed on an unvalidated
  base).
- M8 gate applies to the redo track identically (T-16).

---

```
