# Felt Intensity — Mechanism Design

**Status:** Implemented natively in Zag, trialed 2026-09-20. Trial verdict: **FAIL** on
substantive bars (see `TRIAL_RESULTS.md`). This document describes the mechanism as built.

## 1. What felt intensity is

Felt intensity is an internal, deterministic, white-box sense of how much a held memory
matters. It is:

- **A pure function of audited ledger evidence.** For a memory with value `v` in slot `s`,
  at read time:
  - `C` = count of `OBS_CORROBORATE` entries (slot=`s`, value=`v`) in the ledger prefix
  - `X` = count of `OBS_CONTRADICT` entries (slot=`s`, value=`v`) in the ledger prefix
  - `T` = count of `OBS_TRAINER_MARK` entries (slot=`s`, value=`v`) in the ledger prefix
  - `intensity = clamp(50 + 12*C − 20*X + 25*T, 0, 100)`

- **Read-only.** It never writes memory, never sets strength, never acts. The function
  computes a number and returns it. Nothing else happens.

- **Advisory.** A separate deliberate judgment step may accept the intensity as its
  strength target, temper it, or override it entirely. The judgment — not the feeling —
  is what changes strength, and every judgment is an audited substrate operation with
  a justification code.

- **Provenanced.** Every read is itself an audit entry (`INTENSITY_READ`) recording the
  packed `(C, X, T, intensity)`. Any checker can recompute the value from the ledger
  prefix alone and must get the identical number. In the trial, all 46,050 reads across
  6 cells recomputed exactly (0 failures).

## 2. Why it is not reward (and not reward-by-another-name)

| Reward | Felt intensity |
|---|---|
| Maximized by the policy; the objective | Never maximized; nothing optimizes it |
| Scalar feedback from environment/trainer | Internal computation from the learner's own observation ledger |
| Drives action selection (policy gradient, Q-learning) | Drives nothing; only informs a separate deliberate judgment |
| Typically opaque (a number arrives; why is hidden) | White-box: every input is a named audit entry, recomputable |
| Can be hacked (reward hacking, wireheading) | Cannot be "hacked" — it reads only observations the learner itself emitted; inflating it requires fabricating observations, which are themselves audited |
| Stochastic (noisy reward, exploration bonuses) | Deterministic: same ledger prefix → same intensity, always |

The critical structural guarantee is the **binding rule**: `felt_intensity()` matches ONLY
observation operations. It never reads strength, never reads its own past reads, never
reads judgments, evidence, justifications, kills, or downstream outcomes. There is no edge
from a judgment back into the intensity inputs. This was verified:

- **Statically:** the runner greps for strength writes outside the substrate API (none),
  for RNG tokens (none), and for the frozen formulas (present verbatim).
- **Behaviorally:** every read recomputes from the ledger prefix (F3); junk never exceeds
  neutral 50 (F4a); implants never rise after first contradiction (F4b); no strengthen
  occurs with zero evidence (F4c); no read inputs include non-observation entries (F4d).

If intensity were reward-by-another-name, we would expect: the system optimizing it,
reads influencing reads (feedback loop), or strength judgments feeding back into future
intensity. None occur. The data flows one way: observations → feeling → (separate)
judgment → strength. The feeling is a thermometer, not a thermostat.

## 3. How it plugs into the strength-setting step

The blocked strength trial (`wave4/strength-experiment/PREREG.md`, still BLOCKED) had a
"strength-setting step" where a judgment sets a memory's strength. Felt intensity plugs
into that step **without modifying the blocked preregistration** — this is a parallel
track with its own preregistration (`PREREG_FELT.md`).

The integration point is the **judgment target**:

- **Without feeling (N arm):** the learner's deliberate judgment uses fixed targets
  (80 on first corroboration, 90 on later; 30 when weakening). These are constants —
  the learner decides *when* to judge, but the *target* is hardcoded.

- **With feeling (F arm):** the learner consults `felt_intensity()` at the judgment
  point, then makes a separate deliberate judgment with the intensity as its target
  (accepted, possibly after gating rules). The learner decides *when* to judge AND
  *what the evidence says the target should be* — but the judgment itself (the
  `STRENGTHEN`/`WEAKEN` operation with justification) remains a distinct, audited act.

The feeling never sets strength directly. The substrate's `st_strengthen`/`st_weaken`
are the only strength writers, and they are called by the judgment policy, not by
`felt_intensity()`.

## 4. The three lawful call sites

Per `PREREG_FELT.md` §7, `felt_intensity()` is called only at:

1. **Strengthen-target:** when a new corroboration arrives for a contradiction-free
   memory, read intensity → deliberate `STRENGTHEN` judgment (if target > current).
2. **Weaken-target:** in the revision sweep (≥2 observed contradictions), read
   intensity → deliberate `WEAKEN` judgment (if target < current), then evidence,
   justification, and evidence-gated kill.
3. **Pressure triage:** when slots must be freed, read intensity for each candidate →
   triage ascending (lowest felt importance first), then evidence-gated kill or abandon.

## 5. Trainer as backup/override

The trainer can declare strength directly (`st_trainer_declare`, e.g., 85 at admission
for designated memories) and this emits an `OBS_TRAINER_MARK` — which the feeling
*observes* (+25) but does not *obey*. The mark is social evidence ("the trainer cares
about this"), not a command. If the marked memory later accumulates contradictions,
the feeling falls (the −20/contradiction outweighs the +25 mark at X≥2), the learner
weakens it, and the evidence-gated kill proceeds — **overriding the trainer's
designation**. In the trial, trainer-designated wrong memories were revised at the
same rate as unmarked wrong memories (when they survived to revelation).

TNN-origin vs trainer-origin judgment share is reported per cell. In the trial:
F arm ~46 TNN judgments (strengthen+weaken) vs 10 trainer declarations per cell —
the feeling path is primary, the trainer is backup.

## 6. Implementation

- `felt.zag`: the mechanism. Observation emitters (`felt_emit_obs`), the audited read
  (`felt_read` → `INTENSITY_READ` entry), pack/unpack helpers, and the independent
  ledger-prefix recomputer (`felt_recompute_ok`).
- `felt_trial.zag`: the trial driver (500-episode curriculum, both arms, 3 variants).
- `run_felt.sh`: static gates → compile → 2× runs per cell → byte-compare →
  preregistered-bar validation.
- Substrate (`st_memory_core.zag` + `substrate/`): byte-identical copies of the
  Wave-5 deliberate-memory substrate (hash-verified in the runner).

No RNG. No stubs. The learner is the real deliberate-memory policy. Two runs per
cell are byte-identical (F5 PASS).

## 7. What the trial showed

See `TRIAL_RESULTS.md` for the full report. In brief:

- **Integrity (all PASS):** deterministic (F5), provenance recomputes (F3),
  anti-inflation holds (F4a–F4d), replay exact.
- **Substance (FAIL):** valuable retention 24–26% (bar: ≥90%); wrong-memory revision
  7.7% (bar: 100%).
- **F vs N:** outcome-identical. The feeling was exercised (15k+ reads/cell, all
  valid) but did not change which memories were kept, killed, or revised.

The failure is diagnosed as a **trial-design flaw**, not a mechanism flaw: the
preregistered store dynamics (32 slots, 500 admissions, slot-index triage tiebreak)
create a revolving door that churns 74–94% of valuable memories before their first
observation (age <25). The feeling cannot inform judgments for memories that never
survive to be judged. This is reported honestly as a FAIL; no post hoc tuning was
performed.
