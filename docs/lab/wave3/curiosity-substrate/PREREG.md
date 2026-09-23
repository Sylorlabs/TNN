# PREREG — curiosity-substrate native wiring trial

Investigator: Wave-3 curiosity-substrate · 2026-09-20 UTC
Status: **written before any trial run.** Prereg amendment A1 (program-law
update) incorporated at write time; no trial had been run, so no results
were amended.

## A1 — Program-law amendment (Micah, 2026-09-19, applied pre-run)

- **No RNG anywhere in the system.** The trial's decision paths, tie-breaks,
  and policies are fully deterministic. Tie-break rule: lowest slot index.
  The curiosity substrate itself was already RNG-free (verified in source).
- **World adversity is a designed curriculum, not random exploration.**
  The noise trap uses a fixed, explicitly-designed 64-bit irregular pattern
  (period 64), not harness RNG. Harness RNG is used nowhere in this trial.
- **Scale dimension is explicit.** See "Scaling argument" below.

## Hypothesis

H1: When the curiosity v1 substrate is wired as the *sole* driver of probe
selection in a closed loop (1-bit persistence predictor per option,
deterministic argmax-curiosity with lowest-index tie-break), the system
exhibits **directed information-seeking**: it concentrates probes on
options where its own prediction error is *changing* (learning in progress
or world changed under it), leaves alone options whose error is stably low,
and rejects options whose error is stably high-but-unlearnable (noise).

Null H0: the score is decorative — probe allocation is no better than
uniform round-robin, or the system is attracted to noise, or the
`|slow−fast|` dynamics term contributes nothing over raw surprise or over
the novelty/staleness terms.

## Design (smallest meaningful wiring)

**Substrate:** lab-ported `curiosity_v1_native.zag` (logic-identical to
repo source; see SUBSTRATE_ANALYSIS.md). Parameters fixed at the values in
the repo's own tests: `fast_rate=0.25`, `slow_rate=0.03`,
`novelty_scale=0.10`, `initial_error=0.0`.

**Caller (system, fully deterministic, zero RNG):**
- 8 option slots. Per slot the system holds one belief bit: `predicted`
  (init 0). On probing slot `o` with world outcome `y`:
  `error = |predicted[o] − y|`; `predicted[o] = y` (persistence predictor);
  `r34c1_observe_error(o, step, error, 0.25, 0.03)`.
- Each step: score all 8 slots with `r34c1_score(step)`, probe the argmax;
  ties → lowest index.

**World (designed adversarial curriculum, deterministic, zero RNG):**
- Slots 0–1, 6–7 — BORING: outcome always 0. Learnable in one probe;
  control for "leave well alone".
- Slots 2–3 — PROGRESS: outcome 1 for the slot's first 12 visits, then 0
  forever. Two learning events per slot (1→learned, then the drop); the
  `|slow−fast|` term should spike at both and then decay.
- Slot 4 — NOISE TRAP: outcome = fixed irregular 64-bit pattern
  (`0x9E3779B97F4A7C15` bitstream, period 64). Unlearnable by a
  1-bit persistence predictor; long-run error rate ≈ 0.5. This is the
  substrate's headline claim under test: *stable noise must not stay
  intrinsically valuable*.
- Slot 5 — REGIME SWITCH: outcome 0 until global step 300, then 1
  forever. Tests directed re-investigation after the world changes under
  the system (the "unpredictable switching must not break the system" test,
  expressed as an explicit designed switch).

600 steps total.

**Baselines (both deterministic):**
- B-ROUND: round-robin probe `step % 8`. The "is curiosity better than
  nothing?" control.
- B-MYOPIC: probe the slot with highest *fast* EMA error (pure raw
  surprise, no dynamics, no novelty/staleness); ties → lowest index. Tests
  whether the two-speed dynamics adds anything over surprise-seeking.

**Trace:** per-step CSV `step,probed,score_0..7,err` for the curiosity
arm, plus per-arm summaries. Determinism check: the curiosity binary is
run twice; traces must be byte-identical.

## Falsification criteria (vacuous ⟺ ANY of F1–F4 holds)

- **F1 — no directed drive:** curiosity arm's probe share on
  {PROGRESS slots 2,3 + REGIME slot 5} is **not greater** than B-ROUND's
  (uniform = 3/8 = 37.5%). If the drive can't beat uniform, it's not
  directed information-seeking.
- **F2 — noise attraction:** curiosity arm spends **more** probes on the
  NOISE slot 4 than on a single PROGRESS slot (2 or 3). The substrate's own
  design claim is that stable noise self-rejects; failing this in the
  substrate's own terms is vacuous.
- **F3 — dynamics term adds nothing:** curiosity arm is **no better** than
  B-MYOPIC on noise rejection (slot-4 probe share) — i.e. the two-speed
  `|slow−fast|` term is decorative over raw surprise.
- **F4 — dynamics term is inert:** ablation — rerun the curiosity arm with
  the dynamics term zeroed (`score = novelty·(1+age/mean_age)` only). If
  the probe sequence is **identical** to the full-score run, `|slow−fast|`
  never changes a decision and is decorative.

## Positive criteria (all of P1–P4 required)

- **P1:** curiosity probe share on {2,3,5} > B-ROUND's 37.5%.
- **P2:** slot-4 (noise) probes < slot-2 (progress) probes in the
  curiosity arm.
- **P3:** REGIME slot 5 is probed within 20 steps of the step-300 switch
  (directed re-investigation after change).
- **P4:** the F4 ablation produces a *different* probe sequence AND the
  full score beats the ablated score on noise rejection (slot-4 share).

Verdict mapping: all P1–P4 → POSITIVE; any F1–F4 → NEGATIVE (kill with
evidence); mixed P/F → MIXED with the exact split named.

## Scaling argument (required dimension)

Per-slot state: 2×f32 + i32 + i64 = 16 bytes → **O(N) memory**.
`r34c1_observe_error`: **O(1)** per observation.
`r34c1_score` per step: O(N) over slots (mean-age + argmax scan).
Fixed EMA rates ⇒ no decaying learning rates, no growing state;
`mean_age` grows with step but is a plain f64 — the staleness ratio
`age/mean_age` stays O(1) as step→∞, so scoring does not diverge on long
horizons. Nothing in the mechanism is tied to N=8.

**10x/100x claim:** the same code scales to N=1000 slots and 10⁶ steps
with no structural change (memory ≈ 16 KB for N=1000; per-step work ≈
1000 score evaluations of ~20 flops each).
**Next scale test (explicit):** N=128, 20,000 steps, same four curriculum
classes, plus *two simultaneous* regime switches at different steps, to
test whether directed re-investigation survives concurrent change.
Only runs if this trial is not NEGATIVE.

## White-box spot checks (recorded here so a pass means something)

- W1: unit-test the ported substrate against the repo tests' three
  assertions (progress separation > 0.02; stable-noise fast/slow
  convergence; stale > fresh with equal dynamics/count), plus determinism
  (`r34c1_state_equal` on a copied state).
- W2: hand-compute slot 0's `fast` EMA for the first 4 steps of the trial
  from the trace and check exact f32 agreement.
- W3: negative case — corrupt one byte of a copied state array;
  `r34c1_state_equal` must return 0.

## What this trial does NOT claim

- The persistence predictor is trial scaffolding, not part of the
  substrate; results speak to the *wired loop*, not to curiosity in
  general.
- N=8 is a mechanism test, not a scale test (scale is argued, then tested
  next only on non-negative verdict).
- No reward signal anywhere; no RL; no randomness in the system.

## Post-invalid-run amendment (2026-09-20 UTC)

**Status of original trial:** INVALID. Do not use for verdict.

**Apparatus defects found:**

1. **ZNC-2026-09-19-001 (toolchain codegen defect):** The pinned `znc` miscompiles array stores in multi-store contexts. Symptoms:
   - `r34c1_init`'s 4-store loop: `last_seen[i]` stored as 0 (not -1) for i<N-3; `count[i]` stored as -1 (not 0) for i>=N-3.
   - Multiple i64 stores to one array corrupt the last 3 elements of the i32 array allocated immediately before it (isolated repro confirmed).
   - `r34c1_observe_error` (the substrate's core update!): in complex calling contexts, emits phantom stores and/or computes wrong values. Single call in simple context works (unit test passes). In a loop, fails deterministically (probe36: RC_FAIL at step 13). 20 unrolled calls: one missed count increment.
   - The defect is context-sensitive and deterministic per binary. It affects the trial's hot path (600 observe_error calls), making mode 0 (full curiosity) and mode 1 (round-robin) unrunnable. Modes 2 (myopic) and 3 (ablated) happen to run clean in their specific binary contexts.

2. **Uninitialized harness arrays:** `pred`, `visits`, `probes` were allocated but not explicitly initialized (violates playbook's no-zeroed-allocation rule). Fixed with explicit init.

3. **Baseline starvation:** Original highest-fast-error baseline (mode 2) deterministically locks onto slot 0 (all fast errors tie at 0, lowest-index tie-break). It is not a meaningful surprise-seeking control. Preserved as-is for the record; F3 cannot be evaluated against it.

**Apparatus fixes applied (before rerun):**
- Unrolled straight-line init with canary guard array + verify-by-read (INIT_VERIFIED).
- Explicit init of all harness arrays.
- Self-test validating `r34c1_observe_error` codegen in the trial binary (SELFTEST). The self-test FAILS (SELFTEST,0), confirming the trial binary's codegen is defective.

**Verdict on rerun:** The full-curiosity arm (mode 0) cannot be run reliably on this toolchain. The trial is BLOCKED for F1, F2, F3 (all require mode 0). Modes 2 and 3 produced valid traces and are reported as partial evidence. The substrate's mathematics are validated by the unit test (WB_FAILURES,0).

**Original prereg criteria F1-F5 are NOT evaluated** (except F4-partial and F5-partial from modes 2/3). This amendment does not modify the criteria; it records that they cannot be tested due to apparatus failure.
