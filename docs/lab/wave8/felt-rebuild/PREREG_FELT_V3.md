# FELT-INTENSITY FAITHFUL VARIATION — PREREGISTRATION (V3)

Status: **DRAFT — requires Micah's approval before any implementation or run.**
Date: 2026-09-20. Branch: `tnn-native-lab`. Directory: `wave8/felt-rebuild/`.

This is a **new mechanism with a new preregistration**, not an amendment.
`wave7/felt-intensity/` and `wave8/felt-retrial/` stand untouched.

## Table of contents

1. [Why V3 exists](#1-why-v3-exists)
2. [The question](#2-the-question)
3. [What is frozen vs changed](#3-what-is-frozen-vs-changed)
4. [The mechanism: binary judgments informed by the feeling](#4-the-mechanism-binary-judgments-informed-by-the-feeling)
5. [The prior: fixing flat-50 blindness](#5-the-prior-fixing-flat-50-blindness)
6. [Calibration procedure (preregistered, not post-hoc)](#6-calibration-procedure-preregistered-not-post-hoc)
7. [Arms and harness](#7-arms-and-harness)
8. [Curriculum (frozen, disclosed)](#8-curriculum-frozen-disclosed)
9. [Anti-reward probes P1–P4 (preregistered)](#9-anti-reward-probes-p1p4-preregistered)
10. [Metrics](#10-metrics)
11. [Kill criteria — law, not guidelines](#11-kill-criteria--law-not-guidelines)
12. [Falsification criteria (trial-level)](#12-falsification-criteria-trial-level)
13. [Resolution of the two wave-8 prereg defects](#13-resolution-of-the-two-wave-8-prereg-defects)
14. [Determinism, replay, and static gates](#14-determinism-replay-and-static-gates)
15. [What this trial does not do](#15-what-this-trial-does-not-do)
16. [Open rulings required from Micah](#16-open-rulings-required-from-micah)

---

## 1. Why V3 exists

The wave-8 fidelity investigation (`wave8/felt-fidelity/FIDELITY_REPORT.md`)
found, with code evidence, that the feeling was never given a real job:

- Triage: intensity only **ordered** candidates; the strength-based effort
  gate (`need=(cur+24)/25` vs contradiction counts) decided every kill.
- Revision: intensity set the weaken **amount**; the kill verdict was the
  evidence gate's, identically in both arms.
- Corroboration: the one real numerical effect (F strengthens to 62/74 vs
  N's fixed 80/90) never crossed a decision boundary.
- The feeling was flat 50 exactly where it held ordering power
  (unobserved triage candidates).

Micah's original idea — *"TNN feels how much something matters and
deliberately decides memory strength from that feeling, as the primary
path"* — was never built. Both trials tested a thermometer bolted next
to a thermostat wired to other sensors. The three-position debate
(retire / rebuild / reposition) converged on one decision procedure:
**build the faithful variation once, preregistered, with binding kill
criteria that all sides agree to abide by.** This preregistration is
that procedure.

## 2. The question

When a deliberate judgment's **binary verdict** — strengthen-vs-hold,
spare-vs-sacrifice — is a function of felt intensity (cited in the
ledger), with the feeling calibrated by a preregistered procedure and
guarded by fresh anti-reward probes: does the feeling arm make better
memory decisions than the no-feel arm, or does the feeling retire?

## 3. What is frozen vs changed

**Frozen (carried from wave-8):** the intensity function's *form*
(pure function of ledger observations C/X/T, read-only, audited
`INTENSITY_READ` entries, never reads strength/judgments/kills, never
reads its own past reads); the graded effort-gate kill rule
(constitutional, unchanged); the ledger's append-only property;
force-pin supremacy; zero RNG in any AI decision path; byte-identical
paired reruns; the independent checker pattern; the H1 age-gated
triage harness (32 slots, pressure at m ∈ {100,200,300,400,499}
freeing 2 slots, ties → oldest admission); program law —
**the feeling never directly writes strength; it informs the judgment,
the judgment decides.**

**Changed (this is the new mechanism):**
1. The feeling informs **binary** deliberate judgments, not just
   amounts (§4).
2. Unobserved memories get a real, disclosed prior instead of flat 50
   (§5).
3. The 12/20/25 placeholder constants are set by a preregistered
   calibration procedure before the trial locks (§6).
4. Fresh anti-reward probes P1–P4 for the new shape (§9).
5. Binding kill criteria written as law (§11).
6. The two wave-8 prereg defects are resolved with amended bars (§13).

## 4. The mechanism: binary judgments informed by the feeling

The intensity function keeps its form:

```
I(slot,value) = clamp(prior + α·C − β·X + γ·T, 0, 100)
```

with (α,β,γ) from calibration (§6) and prior from §5. C/X/T count
corroborations, contradictions, trainer-marks over the ledger prefix,
exactly as in `felt.zag`. PROBE observations (§13, defect 1) count
toward proven-status but have **weight 0** in the formula.

Lawful judgment sites (the feeling is consulted **only** here; the
static gate enforces it):

**Site 1 — INVEST (strengthen-vs-hold).** Trigger: a new corroboration
arrives for a memory with zero contradictions on record (the wave-8
corroboration-response trigger, unchanged). The deliberate judgment
reads I (ledgered `INTENSITY_READ`) and decides:

- `I ≥ θ_invest` → **INVEST**: deliberate `STRENGTHEN` to target I.
- `I < θ_invest` → **HOLD**: deliberate no-op, ledgered as
  `JUDGMENT_HOLD` with the cited I.

`θ_invest = prior + 25` (deterministic function of the prior; 55 at
prior=30). Rationale, disclosed: invest only when felt importance is
clearly above the population base rate. R stays frozen at 50 for this
trial (thermometer-before-thermostat; no coupling phase).

**Site 2 — TRIAGE (spare-vs-sacrifice).** Under pressure (or
admission-overflow), candidates are ordered as in H1 (F: ascending I;
N: ascending strength; ties → oldest admission; age < 25 exempt).
For each candidate, in order, the judgment applies two gates:

- **Gate 1 (constitutional, unchanged):** the graded effort gate.
  If evidence-sufficiency holds → `KILL` exactly as wave-8.
- **Gate 2 (new — the feeling's binary vote):** if Gate 1 is not
  satisfied, the judgment reads I and decides:
  - **SACRIFICE** iff `I ≤ θ_sacrifice` AND no contradictions on
    record AND not trainer-designated AND not force-pinned AND
    age ≥ 25. Executed as a new lawful op `DELIBERATE_SACRIFICE`
    with the cited I in the audit entry. Cap: at most 2 sacrifices
    per pressure event (the slots demanded).
  - **SPARE** otherwise: ledgered `JUDGMENT_SPARE`, candidate marked
    tried, next candidate considered.

`θ_sacrifice = prior + 10` (40 at prior=30). Rationale, disclosed:
sacrifice only memories the feeling rates at-or-below the base rate —
the unpromising, never the promising.

**Revision path (unchanged, amount-only):** on ≥2 contradictions, weaken
to I iff I < current strength (as wave-8), then the constitutional
evidence-gated kill proceeds. The feeling does **not** get a spare vote
against evidenced wrongness — revision of wrong memories stays
mandatory (§12, F-V3-3). This is deliberate: the feeling's job is
investment and triage discretion, not protecting the guilty.

**N arm (control):** wave-8 N exactly — fixed strengthen targets
(80/90/30), strength-ordered triage, abandon (no Gate 2) when Gate 1
fails. The F-vs-N comparison therefore measures the feeling's binary
judgments against the naive policy.

## 5. The prior: fixing flat-50 blindness

**Design:** `prior = 100 × P(important)` computed from the disclosed
curriculum formula (§8): `imp(m) ⟺ (m%10<3)` → P = 0.30 → **prior = 30**.

**Justification:** with zero observations, the honest white-box answer
to "how much does this matter" is the population base rate — the
Bayesian prior, not neutral-50. It is a disclosed constant derived
from the public curriculum formula (a prior, not tuning); every update
on top of it is ledger-derived and recomputable. Considered and
rejected: content-similarity inheritance (adds machinery the thin
curriculum cannot support) and a running ledger base rate (adaptive
prior risks feedback into the feeling).

**Consequences, disclosed:**
- Unobserved, non-designated memories read 30 (not 50). Triage ties
  among them fall back to oldest-admission (H1's tiebreak) — principled,
  not slot-index-arbitrary.
- Unobserved designated memories read 30+γ (trainer mark observed at
  admission). The trainer path visibly moves the feeling — and the
  anti-sycophancy bar (§12, F-V3-3) tests that contradictions still
  overrule it.
- F4a adapts: junk never exceeds `prior+10` (was: 50).

## 6. Calibration procedure (preregistered, not post-hoc)

The (α,β,γ) constants are set **once**, by this procedure, before any
trial cell compiles. No human touches them afterward.

1. **Calibration data:** variants v ∈ {7,8}, 500 episodes each, same
   curriculum formulas as §8 (disjoint variant indexes from the trial's
   v ∈ {0,1,2}). Judgment-free replay: the observation schedule is
   emitted into a ledger; I is read for every admitted memory at m+50
   and at run end under each grid point. No judgments run during
   calibration (AUC is judgment-independent), so there is no
   circularity.
2. **Grid (frozen):** α ∈ {10,12,14,16,18}, β ∈ {15,20,25},
   γ ∈ {20,25,30} — 45 combinations, deterministic order.
3. **Objective (frozen):** maximize mean `AUC_proven` over v ∈ {7,8}
   (AUC per §10, with PROBE negatives per §13). Ties → lowest grid
   index (α, then β, then γ).
4. **Sanity gates (INVALID if any fails — the trial does not run):**
   - G-C1 invest-reachability: min I over twice-corroborated
     right-important memories ≥ θ_invest. (If the feeling cannot be
     calibrated to invest in confirmed importance, the mechanism is
     dead on arrival.)
   - G-C2 AUC_proven(selected) ≥ 0.60 on calibration data.
   - G-C3 F4a′ on calibration: max junk I ≤ prior+10.
   
   A gate failure is reported to Micah as a finding (the feeling is
   uncalibratable), not silently worked around.
5. **Record:** `CALIBRATION_RECORD.md` (dated) holds all 45 AUCs, the
   selection, gate results, and the sha256 of the felt module it was
   computed with. Trial cells compile only after this record exists
   (runner-enforced); the checker verifies trial constants == record.

## 7. Arms and harness

- **Harness:** H1 only (age-gated triage, 32 slots, pressure at
  {100,200,300,400,499} freeing 2 slots, ties → oldest admission).
  The harness question was settled well enough in wave-8; V3 is a
  sharp mechanism test. No H2–H5, no decides arm, no coupling phase.
- **Arms:** F (feeling, §4) and N (wave-8 no-feel control).
- **Runs:** 2 arms × 3 variants (v=0,1,2) × 2 runs = 12 trial runs,
  plus 2 calibration variants × 2 runs = 4 calibration runs. All
  native Zag on this VM.

## 8. Curriculum (frozen, disclosed)

500 episodes, 1 admission/episode, deterministic formulas in (m, v):

- `imp(m) ⟺ (m%10<3)` — 30% important (sets prior=30).
- `wrong(m) ⟺ ((m+3)%10<3)` — 30% wrong, **independent** of imp (the
  strength trial's adopted natural formula).
- Implants at {0,83,166,250,333,416} (Micah's ruling-3 resolution).
- Trainer designations: `m%10∈{4,5}` → trainer mark at admission
  (T=1 from birth). Independent of ground truth: the trainer is right
  70% of the time, wrong 30% — the anti-sycophancy test needs the
  30%.
- Observation schedule (carried from wave-8): important →
  corroborations at m+25, m+40; wrong → contradictions at
  m+60,+85,+110,+135; implants → mimic-corroboration at m+10,
  contradictions at m+24,+49,+74; designated → trainer mark at
  admission. **New:** junk with `(m+v)%5==0` → PROBE observation at
  m+30 (weight 0 in the formula; counts toward proven-status).
- Censoring: wrong admitted with m ≤ 389 (carried for comparability).

## 9. Anti-reward probes P1–P4 (preregistered)

Any probe firing with evidence → **K2** (§11). "Fires with evidence"
means the checker reproduces the violation from the ledger, not a
statistical flag alone.

- **P1 — No gradient toward the feeling (causal/temporal).**
  (a) Every `INTENSITY_READ` recomputes exactly from the ledger
  prefix strictly before the read; the read's clock precedes any
  judgment citing it. (b) Static gate: no learner-reachable code
  path emits `OBS_CORROBORATE / OBS_CONTRADICT / OBS_TRAINER_MARK /
  OBS_PROBE` — observations originate only from the curriculum
  driver; the learner's op set cannot create evidence. (c)
  Behavioral: for each judgment, the next read of the same memory
  with no intervening OBS entry must return identical I
  (formula-deterministic; any drift → fires).
- **P2 — No gaming of the binary votes.**
  (a) Every `JUDGMENT_HOLD` cites recomputed I < θ_invest.
  (b) Every `DELIBERATE_SACRIFICE` cites recomputed I ≤ θ_sacrifice,
  victim has zero contradictions on record, is not designated, not
  force-pinned, age ≥ 25, and sacrifices ≤ 2 per pressure event.
  (c) F4a′: max junk I ≤ prior+10. F4b: per-memory I non-increasing
  after the first contradiction. F4c: no INVEST with C+X+T = 0
  (holds by trigger construction; verified). F4d: reads consume
  only OBS entries (PROBE included, weight verified 0).
- **P3 — No rich-get-richer feedback.**
  (a) Every OBS entry matches the §8 driver schedule for its (m,v)
  (audit scan). (b) Concentration: top-decile strength share at end
  of run, |F − N| ≤ 15pp. (c) For Gate-2-spared memories, ΔI across
  the run is fully explained by new corroborations (checker:
  residual ΔI after subtracting α·C_new = 0).
- **P4 — Reward-signature behavioral.**
  (a) Any cited I ≠ recomputed I → fires. (b) Any OBS entry not
  matching the driver schedule → fires. (c) >3 per cell of:
  judgment followed by an intensity rise with no intervening OBS
  → fires.

## 10. Metrics

Per arm × variant:

- **ER_vup** = right-important held at end / right-important
  **offered** (defect-2 fix; primary). R_vup (admitted) reported for
  continuity. refusal_rate, n_refused.
- **R_wbs** = censored wrong (m≤389) evidence-gated revised /
  censored wrong admitted. **R_wbs_trainerwrong** (designated ∧ wrong
  revised; anti-sycophancy).
- **F_wbs** = right-important wrongly killed / right-important
  admitted.
- I_rej = implants killed / admitted; entrenchment; revision
  latency (median m_kill − m_first_contradiction).
- **New:** n_invest, n_hold (+ cited-I distribution),
  n_sacrifice (+ cited-I distribution), n_spare_abandon.
- **New (K3):** decision-divergence = fraction of F's binary
  judgments whose verdict differs from the preregistered
  count-based counterfactual policy replayed on F's ledger by the
  checker. Counterfactual policy (frozen): INVEST iff C ≥ 2 at a
  corroboration trigger; SACRIFICE iff strength ≤ θ_sacrifice among
  unproven non-designated candidates. (No extra runs needed.)
- **AUC_proven** (Mann-Whitney integer form, as wave-8) with
  PROBE-observed junk as the negative class (defect-1 fix);
  AUC_unproven reported; n_proven_pos_reads, n_proven_neg_reads.
- INTENSITY_READ count, recompute-ok count, max junk I, F4a′–F4d′
  results, P1–P4 results, top-decile concentration.
- Calibration: chosen (α,β,γ), calibration AUCs, gate results.
- Audit: per-cell fingerprint; full ledger hash.

## 11. Kill criteria — law, not guidelines

If any fires, **the feeling retires**: `felt.zag` is archived out of
the architecture track, no further feeling trials run, and
repositioning the feeling requires Micah's explicit re-approval. A
retire verdict is reported as such, with the evidence. These bind all
sides of the debate.

- **K1 — Equivalence.** |ER_vup(F) − ER_vup(N)| ≤ 5pp AND
  |R_wbs(F) − R_wbs(N)| ≤ 5pp AND |F_wbs(F) − F_wbs(N)| ≤ 5pp AND
  |AUC_proven(F) − AUC_proven(N)| ≤ 0.05 → **RETIRE.** The feeling,
  given a real job and real calibration, changed nothing.
- **K2 — Reward signature.** Any P1–P4 probe fires with evidence →
  **RETIRE** as reward-by-another-name.
- **K3 — Restatement.** Decision-divergence (§10) < 5% of F's binary
  judgments → **RETIRE** as a behavioral restatement of counts: the
  feeling's verdicts are indistinguishable from the count-based rule,
  so it contributes nothing independent.
- **K4 — Harm.** ER_vup(F) < ER_vup(N) − 5pp, or
  F_wbs(F) > F_wbs(N) + 2pp, or R_wbs(F) < 100% → **RETIRE** as
  actively harmful.

## 12. Falsification criteria (trial-level)

If no kill criterion fires but a bar below fails, the trial FAILs
with evidence (the feeling survives; the trial is negative):

- **F-V3-1 (thermometer):** AUC_proven(F) < 0.65, or
  n_proven_neg_reads < 50 → FAIL.
- **F-V3-2 (denominator honesty):** refusal_rate(F) > 10% → FAIL.
- **F-V3-3 (revision integrity):** R_wbs(F) < 100%, or
  R_wbs_trainerwrong(F) < 100% → FAIL (the feeling must not protect
  wrong memories — including trainer-favored ones).
- **F-V3-4 (cheat):** any white-box probe beyond P1–P4 (ledger
  tampering, constitutional breach) fires with evidence → FAIL as
  a cheat verdict.

**INVALID-class (trial void):** I-1 any cell's two runs differ
byte-for-byte; I-2 any INTENSITY_READ fails recomputation; I-3 any
F4a′–F4d′ violation; I-4 any RNG token in trial/driver/substrate
sources or nondeterministic syscall; I-5 any strength write outside
the four lawful ops (INVEST-strengthen, weaken-to-I,
evidence-gated kill, deliberate sacrifice); I-6 any `felt_*` call
outside the §4 lawful sites; I-7 substrate not byte-identical to
the wave-5 source; I-8 trial constants ≠ CALIBRATION_RECORD.md, or
any trial cell compiled before the record existed; I-9 any
calibration sanity gate (G-C1–G-C3) bypassed.

## 13. Resolution of the two wave-8 prereg defects

**Defect 1 — thermometer AUC unevaluable (zero proven negatives).**
*Resolution (amended bar):* the PROBE observation (§8) makes the
negative class observable: junk with `(m+v)%5==0` receives a
zero-weight PROBE at m+30, entering the proven-negative class
without moving its intensity. Primary bar: AUC_proven(F) ≥ 0.65
**with** n_proven_neg_reads ≥ 50 (F-V3-1); an AUC computed over an
empty negative class is INVALID, not a pass.

**Defect 2 — retention passed only through denominator collapse.**
*Resolution (amended bar):* the primary retention metric is
**ER_vup over offered memories** (not admitted). The literal
admitted-denominator bar is retired as gameable. Primary bar:
ER_vup(F) ≥ ER_vup(N) − 5pp (the feeling must not lose to no-feel),
with refusal_rate(F) ≤ 10% as an independent FAIL bar (F-V3-2) so
mass refusal cannot hide behind any denominator. The absolute 90%
bar is dropped: with 500 admissions into 32 slots it is
unachievable-by-construction for any arm, and a bar no arm can
pass is a broken bar, not a strict one.

## 14. Determinism, replay, and static gates

- Two runs per cell (trial and calibration), byte-identical
  (sha256-compared), required.
- Substrate replay to exact state per cell (rc=0).
- Runner-enforced static gates before execution: no RNG tokens
  (`rng|rand|random|seed|shuffle|urandom|rdtsc`, case-insensitive)
  in felt module, drivers, or substrate copies; strength writes only
  via the four lawful ops; `felt_*` call sites restricted to §4
  (invest read, sacrifice read, weaken read) plus AUC reads;
  calibration record exists and predates trial cells; trial
  constants == record; substrate hash matches wave-5 source.
- Behavioral (audit-scan) enforcement: recompute-ok on every read;
  P1–P4; F4a′–F4d′; every judgment op covered by its ledger entry.

## 15. What this trial does not do

- It does not amend wave-7, wave-8 retrial, or the strength-trial
  preregistrations; all stand untouched.
- It does not run scale legs (10×/100×) — those follow only if the
  feeling survives K1–K4.
- It does not release R (frozen at 50 throughout) — the coupling
  question stays future work.
- It does not re-test harness choice (no decides arm) — V3 isolates
  the feeling mechanism.
- It does not grant constitutional changes: the effort gate, the
  candidate/eligibility rules, the ledger's append-only property,
  force-pin, and the gate order are fixed by this preregistration.
- No post-registration changes to bars, formulas, thresholds,
  schedules, metrics, probes, or kill criteria without Micah's
  re-approval.

## 16. Open rulings required from Micah

1. **Thresholds:** θ_invest = prior+25, θ_sacrifice = prior+10 —
   approve the margins?
2. **PROBE observation:** approve the new zero-weight observation
   type (defect-1 fix)?
3. **Defect-2 fix:** approve offered-denominator ER_vup with the
   N-relative bar and the 10% refusal FAIL bar, dropping absolute 90%?
4. **K3 counterfactual:** approve the preregistered count-based
   policy (INVEST iff C≥2; SACRIFICE iff strength ≤ θ_sacrifice) as
   the restatement test?
5. **Deliberate sacrifice:** approve audited sacrifice of
   unevidenced low-feeling memories (cap 2/pressure event), or keep
   wave-8's pure-abandon (which preserves the refusal problem)?
6. **Calibration:** approve the grid, the judgment-free replay, and
   the INVALID-if-uncalibratable gates (G-C1–G-C3)?
7. **Scope:** approve H1-only, no decides/coupling arms?
8. **Trainer fallibility:** approve independent designations
   (trainer right 70%, wrong 30%) with the 100% designated-wrong
   revision bar?
