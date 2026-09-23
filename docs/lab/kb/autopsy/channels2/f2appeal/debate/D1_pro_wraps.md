# D1 — PRO-WRAPS position paper

**Camp:** PRO-WRAPS. **Thesis:** the judgment-side channel family is truly
exhausted for the frozen threat model; F2's permanent retirement STANDS
(WRAPS), with governance amendment G1 scoping auto-execution to that
threat model only. Evidence: TCP_VERDICT.md (PACKAGE 3, commit a6b9d999)
+ PREREG_FROZEN_F2APPEAL.md (frozen 2026-09-23).

## 1. Three arguments from the measured evidence

**A1 — DPI kills every deterministic re-reading (C2: 0.0000 bits).**
On sense A, J(T(x)) == L(J(x)) held for all 92 test + 93 calibration
fixtures (involution byte-verified; 370/370 judgment reproductions). Every
deterministic (J, Jt)-function is a function of J alone → **0.0000 bits**,
F1 fired, F4 fired at **0.4348** false-install. C2 is the constant INSTALL
function on A, void on B. All four PACKAGE-3 camps accepted the DPI
consequence. A mathematical identity over measured data — no deterministic
re-reading can recover, by construction. (R3's transforms are new
instances of the same identity — §2.)

**A2 — The stochastic member is near-vacuous on BOTH senses (C3: 0.0049 bits).**
C3 (honest re-observation-under-noise, ±300 pcm / ±8 img, frozen seed):
**0.0049 bits** pooled (A: 0.0046, B: 0.0043), P(agree)=0.918,
false-install **0.450** — kill bar fired pooled and both senses. Judgments
are 91.8% noise-stable, uncorrelated with correctness (Y=0: 0.894 vs
Y=1: 0.939). J pre-committed to sign retirement if C3 ≤ 0.15 on both
senses — met; the red team pre-committed to stand down — met. The last
live member is dead on its own terms.

**A3 — Three dead members; none clears the bar.**

| Member | Measured bits | Deploy bar (0.15) | Status |
|---|---|---|---|
| C2 deterministic re-readings | **0.0000** | FAIL (DPI) | F1 + F4 fired |
| C3 stochastic re-observation | **0.0049** | FAIL (both senses) | kill bar fired |
| (c) confidence (shootout) | **0.0797** | FAIL | already dead |
| C1-scout (NOT judgment-side) | 0.9968 | PASS | live, different family |

F2 fired at its maximum (**1.0000** ≥ 0.70); the frozen A2 rule routed the
vacuous case to C3 rather than auto-retiring — the brake held, the decider
confirmed exhaustion. Retirement was earned by measurement, not executed
by clause. "WRAPS" is the label on a measured state of the world.

## 2. Expected-null predictions for R1–R4 (testable)

**R1 — noise-amplitude sweep.** C3 already measures fooled and correct
judgments equally noise-stable; the Y=0-conditional gap (0.045) is dwarfed
by the bar, so the boundary-distance hypothesis has no support.

| Level | Amplitude | Prediction |
|---|---|---|
| L0–L3 | ±50–300 pcm / ±1–8 img | bits **0.00–0.05**, false-install 0.40–0.50 |
| L4 | ±600 / ±16 | bits ≤ 0.10, false-install 0.45–0.60 |
| L5–L6 | ±1200–2400 / ±32–64 | P(agree) collapses → near-universal WITHHOLD → bits ≈ 0 (**a null, not a recovery** — prereg says so) |

No level clears bits > 0.15 with false-install < 0.15. L6 destroys
everything: the absence of signal, not a signal.

**R2 — multi-draw consensus (N=5 majority).** Mechanics predict this helps
CON *less* than one draw. Per-draw agree 0.939 (correct) / 0.894 (fooled)
→ majority-of-5 agreement ≈ 0.998 / ≈ 0.99: the vote becomes a
**near-constant INSTALL function**, squeezing bits toward zero. Predictions:
bits **< 0.02** both configs, false-install **≥ 0.90** (the fooled majority
agrees with itself). Horizon buys agreement, not discrimination.

**R3 — alternative transforms (vflip, signflip, fshift).** Each is an
involution with identity L grounded by the generator (vflip keeps
left-right order; signflip = 180° phase; fshift preserves net translation).
Prediction: on every F3-valid (sense, transform) cell,
J(T(x)) == L(J(x)) everywhere → C2 redux → **0.0000 bits**, F4 fires again.
F3-failing cells are VOID per the frozen rule — a broken judge, not a
recovered channel. Zero valid cells clear the bar.

**R4 — structured noise (V1 block-correlated, V2 ternary).** The C3 null is
about the mechanism (stability ∥ correctness), not the noise distribution.
Correlating or reshaping it cannot create a boundary-distance correlation
that isn't there. Predictions: pooled bits **0.00–0.02** for V1 and V2,
false-install **0.40–0.50**, 2× byte-identical.

## 3. Our falsifier

We concede **NOT WRAPS** iff the prereg's **RECOVERY bar** fires: any R1
level, R2 config, R3 (sense, transform) cell, or R4 variant clears **bits
> 0.15 AND false-install < 0.15** on pooled TEST adversarials, with 2×
byte-identical reruns and 0 cross-check errors — the full frozen deploy
criterion. Under §6 that yields NOT WRAPS with C* (reopening covers ONLY
the recovered member class; confirmation battery on a new frozen seed
before any deploy discussion). No partial credit: a "suggestive" 0.09-bit
blip at one R1 level is a NULL per the prereg we signed.

## 4. Answer to the strongest CON objection

**The objection:** "You tested one adversary construction (δ ≲ σ). WRAPS
overclaims — it retires the family against all adversaries. A stronger or
differently-shaped adversary could make fooled judgments noise-fragile —
and R1–R4 reuse the same frozen band."

**Why it does not move the verdict — and why G1 is the answer:**

1. The objection is *already conceded in the verdict scope* (TCP_VERDICT
   §3): retirement is frozen-threat-model only — one construction, two
   senses, six tasks. We claim nothing about untested adversaries; the
   objection attacks a claim we do not make.
2. The DPI death (A1) is construction-agnostic *within* this family: an
   identity over measured data, not a hypothesis about adversary strength.
3. G1 converts the concession into governance: F2 auto-execution is scoped
   to the frozen threat model; extending retirement to ANY new adversary,
   sense, or task requires a NEW preregistered battery — automatic
   execution against untested threat models is forbidden. That is precisely
   the brake CON wants — answering the scope objection **without reopening
   the measured result**: the measurement stands, the reopening mechanism
   is specified, and Micah decides.

PRO in one line: **WRAPS for what was measured, G1 for what wasn't.**
