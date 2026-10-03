# PREREG_MA4 — Signed-value memory agency vs MA3 agency baseline

**Date:** 2026-09-19 (written before any MA4 code runs)
**Design:** `POLICY.md`
**Implementation (to be built):** `trial/ma4_trial.zag` (native Zag)
**Runner (to be built):** `trial/run_ma4.sh`
**Amends:** nothing yet — first registration. Any change after first run
is recorded as a dated amendment below, never silently.

## 1. Hypothesis

A deliberate memory agent with **signed value judgments** (MA4-SIGNED:
negative trust, deliberate negative-judgment ops, pin budget, scheduled
re-evaluation) retains strictly more truly-important memories than the
MA3 AGENCY policy (non-negative trust, unbounded pinning) on adversarial
curricula where early features anti-correlate with importance — while
matching it at the capacity ceiling on standard curricula.

## 2. Mechanics

- Fixed 32-slot store (2 CORE + 30 USER), 500-episode stream, importance
  revealed 25 episodes late — same shape as MA3.
- **Explicit curriculum, zero RNG.** Streams are closed-form functions of
  `(episode, feature, variant)`:
  - `imp(m,v) = 1` iff `(7m + 13v + 3) mod 10 < 3` (~30% important).
  - standard: `f0..f3 = imp·3 + ((13m + 5f + 29v) mod 2)`,
    `f4..f7 = imp·1 + ((11m + 7f + 17v) mod 3)`.
  - adversarial: `f0..f3 = (1−imp)·3 + ((13m + 5f + 29v) mod 2)` (the trap),
    `f4..f7 = imp·2 + ((11m + 7f + 17v) mod 2)`.
  - 3 variants `v ∈ {0,1,2}` (phase offsets) × 2 curricula = 6 cells.
  - This preserves MA3's statistical structure (base rates, trap shape,
    delay) while removing the LCG. MA3's absolute numbers are therefore
  not directly comparable; the in-trial baseline arm is the comparison.
- **Arm BASE** = MA3's AGENCY policy verbatim (non-negative trust
  `[0,256]`, pin-everything while `revelations < 120`, victim = min
  ADD-declared value, admit iff `v_new > v_victim`).
- **Arm SIGNED** = `POLICY.md` (signed trust `[-256,256]`, pin budget 16,
  kill-on-revealed-unimportant, re-evaluation pass at revelation 120,
  fresh-score victim selection, strict-inequality admission gate).
- Both arms run each cell on the identical stream. Deterministic: every
  cell is executed twice; fingerprints must match exactly.

## 3. Primary metric

Per cell: count of truly-important memories still held at end, among
those admitted (same as MA3). Reported per quartile (E51AJ law) for the
SIGNED arm.

## 4. Falsification criteria

Let `H_B(c)`, `H_S(c)` = held-important counts for BASE / SIGNED in cell c.

- **CONFIRM** iff `H_S > H_B` in **all 3 adversarial cells** AND
  `H_S ≥ H_B` in **all 3 standard cells**.
  (Standard has a capacity ceiling: at most 30 important can be held and
  BASE already holds ~30; demanding strict superiority there is impossible
  by construction, so the honest criterion is non-inferiority — no
  regression. This asymmetry is deliberate and preregistered.)
- **FALSIFY** iff `H_S ≤ H_B` in **any** adversarial cell (the signed
  mechanism adds nothing where it was designed to help) OR `H_S < H_B`
  in any standard cell (regression).
- **MIXED** iff neither holds (cannot occur given the definitions cover
  all orderings — listed for completeness; any MIXED outcome triggers a
  prereg amendment explaining the gap before interpretation).
- **INVALID** (stops the experiment, verdict BLOCKED) iff in any cell:
  ledger replay diverges; any CORE slot lost; any successful KILL whose
  before-snapshot was pinned (pinned-while-pinned loss); determinism
  fingerprint mismatch on rerun; binary exit ≠ 0; any `CL_CHECK` mismatch.

Secondary (reported, not gating): drops, kills, unpins, pin counts,
retention rate among admitted, final trust vector.

## 5. Program-law compliance (2026-09-19 update)

1. **No RNG in the AI.** The learner's decisions are deterministic
   functions of state. Tie-breaks: lowest slot index. No random
   exploration, no stochastic policy, no seeded RNG in decision paths.
   The runner greps `ma4_trial.zag` for `rng|rand|srand` and fails the
   run on any match (static check).
2. **Explicit adversarial test.** The curriculum is designed sequences,
   not sampled noise. The verdict distinguishes system determinism
   (rerun fingerprint equality — reported separately) from test adversity
   (arm delta on identical streams).
3. **No banned mechanisms.** No score tables, no N×N scale-up, no reward
   signal in the memory path, no random exploration.

## 6. Scale dimension

MA4 runs at MA3 scale (32 slots / 500 episodes / 8 features) for
head-to-head comparability. The policy's scale argument:

- Per-episode cost: O(F) scoring + O(S) victim scan; re-evaluation once
  at O(S·F + B log B); ledger O(ops). All linear — no step assumes small S.
- Scale-parameterized constants: pin budget `B = S/2`, uncertainty horizon
  `U = 4·S` revelations, ledger capacity ∝ horizon (fail-closed on
  overflow is the safety property; capacity is a deployment parameter).
- **Next scale test (MA5, explicit):** 320 slots, 5000 episodes,
  32 features, ledger cap 65536, same policy with scaled constants.
  Success = determinism holds + adversarial superiority preserved +
  no ledger overflow refusal. If MA4 confirms, MA5 is the follow-up;
  if MA4 falsifies, MA5 does not run on this policy.

## 7. Compute policy

Trivial for native binaries (<1s per full run expected). Clear win →
write it up; debatable tradeoffs flagged with numbers in results.

## 8. Amendments

(none yet)
