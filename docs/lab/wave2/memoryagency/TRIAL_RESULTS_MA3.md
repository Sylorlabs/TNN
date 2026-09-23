# MA3 Trial Results — Long-Horizon Memory Agency vs Lifecycle Eviction

**Date:** 2026-09-19
**Preregistration:** `PREREG_MA3.md`
**Implementation:** `trial/ma3_trial.zag` (native Zag, compiled with `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze --no-foreground-cache`)
**Runner:** `trial/run_ma3.sh`
**Evidence:** `trial/EVIDENCE_MA3_20260919T224748Z/` (compile + run logs)

## Verdict: MIXED — standard curriculum confirms, adversarial does not

Per the preregistration: CONFIRM requires AGENCY to retain strictly
more truly-important memories in **both** curricula; FALSIFY requires
AUTO ≥ AGENCY in **every** cohort. Neither holds:

- **Standard curriculum:** AGENCY wins 3/3 seeds (30 vs 0 important held).
- **Adversarial curriculum:** AUTO wins 3/3 seeds (30 vs 10–11 important held).

The prereg anticipated this shape explicitly: *"the experiment is worth
running even if only the standard curriculum confirms."*

## Method (as preregistered)

Fixed 32-slot store, 500-episode stream, importance revealed 25
episodes late. Both arms run on the identical curriculum per cell
(2 curricula × 3 seeds = 6 cells):

- **Standard:** important = high features f0/f1 (early evidence points
  the right way).
- **Adversarial:** important = high f1 AND low f0; f0 is anti-correlated
  with importance early (the trap); f2/f3 correlate with unimportance.

**AGENCY** (deliberate, MA1-native): pins every incoming memory while
uncertain (first 120 revelations), then judges deliberately — unpins
revealed-unimportant memories, promotes revealed-important ones, kills
only the lowest-valued victim, using a learned per-feature trust
(explicit declared values, no gradients).

**AUTO** (lifecycle-v1 integer port, no fallback needed — the port
compiled and ran): signed linear value predictor learned by delayed
credit, evict-lowest-predicted on pressure. Credit applies to retained
memories at revelation (delayed full-information, per the source).

Primary metric: count of truly-important memories still held at end
(among those admitted). Determinism verified by cell rerun
(fingerprint match). Structural checks per cell: CORE intact,
pinned-while-pinned never lost, ledger replay clean — all passed
(`CL_CHECK,cell_valid,0,0` in all 6 cells, `MA_FAILURES,0`).

## Results

Held / admitted (retention % among admitted):

| Curriculum | Seed | AGENCY | AUTO | Winner |
|------------|------|--------|------|--------|
| standard | 7331 | 30/30 (100%) | 0/12 (0%) | AGENCY |
| standard | 12345 | 30/30 (100%) | 0/5 (0%) | AGENCY |
| standard | 999 | 30/30 (100%) | 0/10 (0%) | AGENCY |
| adversarial | 7331 | 11/11 (100%) | 30/72 (41%) | AUTO |
| adversarial | 12345 | 10/10 (100%) | 30/78 (38%) | AUTO |
| adversarial | 999 | 10/10 (100%) | 30/70 (42%) | AUTO |

Tally: wins=3, losses=3, ties=0 → **MIXED**.

Cohort detail (`MA3_COHORT`): AGENCY's held memories concentrate in
quartile 0 (episodes 0–124) — 28–29 of 30 in standard, 9–10 of 11 in
adversarial. AGENCY locks in early pins and then cannot admit later
episodes (store fills with pinned memories; 434–469 drops per run).

## Mechanism: why each arm wins where it does

**Standard — AGENCY wins because protection beats blind eviction.**
AUTO's predictor starts at zero, so its first evictions (from episode
~30) are blind. Important memories evicted before their revelation
never contribute delayed credit — the predictor cannot learn from its
own eviction mistakes, a structural flaw in "evict-lowest with an
online predictor under delayed credit." It ends holding 0 important
memories on all 3 seeds. AGENCY's protect-while-uncertain rule never
evicts blindly: it pins everything, waits for revelations, then
unpins the revealed-unimportant. Result: 100% retention of admitted
important memories.

**Adversarial — AUTO wins because signed values beat non-negative
trust.** AGENCY's trust is non-negative and its post-uncertainty pin
gate (`v >= 0`) is vacuous — it cannot express "this feature pattern
predicts *unimportance*." It keeps pinning, the store seals shut with
early pins, and it admits only 10–11 important memories (all retained,
but far too few). AUTO's signed linear predictor learns a negative
weight on the trap feature f0 and keeps churning: admits 70–78
important, holds 30.

## What this means (and does not)

- **Confirmed:** deliberate protect-while-uncertain agency is decisively
  better than evict-lowest-online-predictor when early evidence is
  honest (30 vs 0, 3/3 seeds). The failure mode it avoids — destroying
  memories before the learner knows their value — is real and
  catastrophic (AUTO's 0% is not a near-miss).
- **Not confirmed:** that this agency policy is sufficient. Under
  anti-correlated features it is too conservative: perfect retention
  of a trickle (100% of 11) loses to imperfect retention of a flow
  (41% of 72).
- **Not falsified:** agency as such. The adversarial loss traces to a
  specific, identified policy weakness (non-negative trust + vacuous
  gate), not to deliberation itself.

## Design requirement for the next iteration

The two mechanisms have complementary strengths. The follow-up
policy should combine them:

1. Keep deliberate protect-while-uncertain (the standard-curriculum
   win is too large to discard).
2. Replace non-negative trust with **signed value judgments** so the
   agent can express negative evidence ("this pattern predicts
   unimportance") — the missing piece the adversarial curriculum
   exposes.
3. Fix the early-lock bias: AGENCY's quartile-0 concentration
   (28–29/30) shows it stops learning new admissions once pinned.
   A deliberate *re-evaluation* pass (unpin-and-reap on a schedule,
   or a pin budget) is needed.

No new trial was launched; per the prereg, the MIXED verdict calls
for a redesigned agency policy, not a rerun of this one.
