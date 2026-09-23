# FELT-INTENSITY V3 — PREREGISTRATION AMENDMENT 1

Date: 2026-09-20. Status: **AMENDMENT APPROVED FOR APPLICATION — still
requires Micah's final approval of the amended prereg before any
implementation or run.**

Attribution: the changes below are the felt council's verdict
(`COUNCIL_VERDICT.md`, debate complete 2026-09-20, nothing run),
applied without re-debate under Micah's 2026-09-20 testing
authorization. Each item cites its council resolution. Text marked
**AMENDMENT ASSUMPTION** is a value the verdict required but did not
state; the implementer chose the wave-8 value and it is flagged, not
hidden.

This amendment modifies `PREREG_FELT_V3.md`. Every changed definition,
formula, bar, threshold, and scoping is written in full here; the
implementer needs no other source for the amended parts. Unmentioned
sections of the V3 prereg stand unchanged.

---

## A1 — K3 REPLACED by K3′: counterfactual outcome replay

**Council resolution:** Q4 — REJECT K3 as stated (unreachable by
construction: I is literally f(C,X,T), so verdict-divergence punishes
good calibration and measures the wrong quantity). Replace with
outcome replay. Verdict-divergence is kept only as a reported
diagnostic.

**Deleted:** V3 §10's `decision-divergence` metric as a kill
criterion; V3 §11's K3 ("Restatement — divergence < 5%").

**Inserted K3′ — Restatement (counterfactual outcome replay).**

*K3′ procedure (exact, checker-executed, no extra runs):*

1. **Replay substrate.** The checker takes the F arm's trial ledger
   (variant v) and its fixed OBS sequence, which is judgment-
   independent per P1 (observations originate only from the
   curriculum driver), and simulates the **naive count policy**
   below deterministically through the same 500-episode schedule:
   same admission rule, same pressure events at
   m ∈ {100,200,300,400,499} (freeing 2 slots), same age-gated H1
   triage, same constitutional effort gate (Gate 1, unchanged),
   same m≤389 censoring for the wrong-revision denominator.
2. **The naive count policy (frozen, preregistered here).** It has
   no intensity reads. Strength dynamics are the wave-8 N-arm fixed
   numbers (admission 0; see A4):
   - *Site-1 trigger* (new corroboration arrives, zero
     contradictions on record): **INVEST** iff C ≥ 2 (raw
     corroboration count) → simulated `STRENGTHEN` to **80**
     (wave-8 N first-corroboration target; AMENDMENT ASSUMPTION).
     Otherwise **HOLD** (no-op).
   - *Site-2* (only where the constitutional Gate 1 fails):
     candidates ordered ascending simulated-strength, ties →
     oldest admission, age < 25 exempt. **SACRIFICE** iff
     simulated-strength ≤ θ_sacrifice **and** zero contradictions
     on record **and** not trainer-designated **and** not
     force-pinned **and** age ≥ 25 — the exact §4 Gate-2
     eligibility with strength in place of I. Cap 2 sacrifices
     per pressure event. Otherwise **SPARE** (next candidate).
   - *Revision* (unchanged, mandatory): on ≥2 contradictions,
     weaken to 30 (wave-8 N fixed weaken target) iff 30 < current
     strength; the constitutional evidence-gated kill proceeds
     identically. The naive policy, like F, gets no spare vote
     against evidenced wrongness.
3. **Outcomes computed** for the replayed naive policy:
   `ER_vup(naive)`, `R_wbs(naive)`, `F_wbs(naive)` — defined exactly
   as in V3 §10 (offered denominator for ER_vup; censored m≤389
   for R_wbs).
4. **K3′ fires (RETIRE as restatement) iff all three hold:**
   - |ER_vup(F) − ER_vup(naive)| ≤ 5pp, AND
   - |R_wbs(F) − R_wbs(naive)| ≤ 5pp, AND
   - |F_wbs(F) − F_wbs(naive)| ≤ 5pp.
   
   These are the K1 equivalence bands applied to outcomes. If the
   naive count weighting achieves outcomes inside these bands, the
   feeling's weighting bought no better *decisions* — the feeling
   retires, no rescue.

*Retained diagnostic (not a kill criterion):* verdict-divergence —
fraction of F's binary judgments whose verdict differs from each
member of a preregistered counterfactual family, reported per
variant: (i) **raw-count** (the K3′ naive policy above); (ii)
**time-weighted** (INVEST iff Σ 1/(1+age_of_obs) over corroborations
≥ 1.0 at trigger; same Site-2 eligibility); (iii) **trainer-only**
(INVEST iff T ≥ 1 at trigger; SACRIFICE iff T = 0 under Site-2
eligibility); (iv) **recency-only** (INVEST iff the memory's most
recent OBS entry is a corroboration within the last 50 episodes;
SACRIFICE iff most recent OBS is not a corroboration, under Site-2
eligibility). Family definitions are amendment-fixed; reported,
never law.

*Recommended pre-implementation sanity check (not blocking):*
replay the naive rule over the existing wave-8 F ledgers; the
council projects divergence ≈ <1% for K3-as-stated, which is why
K3 was replaced.

---

## A2 — Symmetric count-based sacrifice for the N arm

**Council resolution:** Q5 — APPROVE-WITH-CHANGE. The F-vs-N
comparison was confounded: F differed from N in *signal* (feeling)
*and* privilege (a kill license N lacked). Keep sacrifice, but give
N a symmetric preregistered count-based sacrifice op so the trial
isolates the feeling, not the privilege.

**V3 §4, Site 2, N arm — replaced text.** The N arm (control) is
wave-8 N **plus** a symmetric count-based sacrifice:

- N's Gate 2 (after the constitutional Gate 1 fails): candidates
  ordered ascending strength, ties → oldest admission, age < 25
  exempt. **SACRIFICE** iff strength ≤ θ_sacrifice (= prior+0.5α,
  the numeric value from A5, identical in both arms) **and** zero
  contradictions on record (unproven) **and** not
  trainer-designated **and** not force-pinned **and** age ≥ 25.
  Executed as an audited `DELIBERATE_SACRIFICE` (count-cited, not
  I-cited) entry. Cap: at most 2 sacrifices per pressure event.
  Otherwise **SPARE** (next candidate).

F's Gate 2 is unchanged except thresholds per A5. The F-vs-N
comparison now measures feeling-informed binary judgments against
the best-tested non-feeling policy with the same privilege.

**Relabel (council-required):** §4's Gate 2 is a **constitutional
expansion**, not a natural gate — it is named as such wherever §4
appears. (Gate 1 is consulted first and unchanged; sacrifice fires
only where Gate 1 said no.)

**New reported metric (§10):** per arm, `n_sacrifice` with the
cited-basis distribution and each victim's ground-truth class —
sacrifice's independent value is whether its victims are actually
junk, measurable against ground truth.

---

## A3 — Scoping fixes: F4a′, G-C3, P2c, G-C1

**Council resolutions:** Q2 (genuine bug: F4a′ auto-INVALIDs via
designated junk, since designations are independent of ground truth
and designated junk reads prior+γ > prior+10); Q6 (G-C1's unscoped
min-over-set INVALIDs a healthy trial — ~9% of episodes are
important ∧ wrong, and their contradiction-carrying end-of-run reads
tank I below the bar).

**Amended text (replaces the corresponding V3 lines):**

- **F4a′:** max I over **non-designated** junk ≤ prior+10.
  (Designated junk is excluded: a trainer mark legitimately raises
  I by γ.)
- **G-C3** (calibration sanity gate): same scope — max I over
  **non-designated** junk ≤ prior+10 on calibration data.
- **P2c / F4c:** scoped to **non-designated** memories — no INVEST
  of a non-designated memory with C+X+T = 0 (holds by trigger
  construction; checker-verified). Designated memories' INVEST
  verdicts are permitted and reported; sycophancy is policed by
  F-V3-3 (100% designated-wrong revision bar), not by F4c.
- **G-C1** (calibration sanity gate): min I over **twice-
  corroborated (C ≥ 2) right-important ∧ not-wrong** memories ≥
  θ_invest. With θ_invest = prior+1.5α (A5), any memory with C=2
  and X=0 reads prior+2α ≥ prior+1.5α, so reachability holds by
  construction at every grid point — the gate is retained as
  INVALID-law in its fixed scope. (Per Q1, G-C1-as-absolute-check
  retires gracefully; G-C2 keeps discriminability risk covered.)

---

## A4 — Admission-default strength: stated

**Council resolution:** Q4 required fix — the value was missing and
blocks both the trial and the K3′ replay.

**Amended text:** **admission-default strength = 0**, in both arms,
in trial and in the K3′ replay. **AMENDMENT ASSUMPTION:** the
council verdict did not state a value; 0 is the wave-8 value
(`st_add(&st,m,ST_REGION_USER,0,&slot_out)` in
`wave8/felt-retrial/phase_e/felt_phase_e.zag`). If Micah rules a
different default, the trial cells and the K3′ replay re-derive
from it by amendment.

---

## A5 — Thresholds calibration-denominated

**Council resolution:** Q1 — APPROVE-WITH-CHANGE. The fixed +25/+10
were picked against the old placeholder α=12; at α=10 a
once-corroborated memory reads exactly 40 = old θ_sacrifice
(sacrifice-eligible *despite* positive evidence), while at α=18 it
reads 48 and is spared — the sacrifice policy's meaning flipped
with calibration luck.

**Amended text (replaces V3 §4 threshold definitions):**

- θ_invest = **prior + 1.5α**, computed from the recorded α,
  frozen as a procedure (at prior=30: 30+1.5α).
- θ_sacrifice = **prior + 0.5α**, computed from the recorded α,
  frozen as a procedure (at prior=30: 30+0.5α).

Disclosed meanings, now calibration-invariant: "invest only when
clearly above the base rate" always means ≥2 corroborations of
evidence; "sacrifice only the unpromising" always means <0.5
corroborations — at every grid point. The checker verifies the
trial's θ values equal prior+1.5α / prior+0.5α of the recorded α
(new static gate; trial constants ≠ record → INVALID per I-8).

---

## A6 — §16 question-by-question resolutions

All eight questions are resolved; nothing in §16 remains open.

- **Q1 (thresholds):** resolved by A5 above.
- **Q2 (PROBE):** APPROVED. The zero-weight driver-emitted PROBE
  observation (§8) stands; no learner-reachable code path can emit
  it (P1b static gate); proven-status is consumed by no decision
  path. Junk-scope bug fixed by A3 (F4a′, G-C3, P2c scoped to
  non-designated junk).
- **Q3 (defect-2 fix):** APPROVED. Primary retention metric stays
  **ER_vup over offered memories** with the N-relative bar
  ER_vup(F) ≥ ER_vup(N) − 5pp; the absolute 90% bar stays dropped
  (unachievable-by-construction at 500 admissions / 32 slots).
  Two drafting repairs applied: (a) **refusal_rate = n_refused /
  total offered admissions** (denominator explicit); (b) the 10%
  FAIL bar is anchored as **≈1/3 of the wave-8 observed refusal
  rate (~31%)** — i.e., the feeling must beat the wave-8 baseline
  more than threefold. The ~31% figure is pending confirmation by
  ledger re-analysis (see Open items); if it differs materially,
  the anchor statement updates by amendment, not the bar.
- **Q4 (K3 counterfactual):** resolved by A1 (K3→K3′) and A4
  (admission-default stated).
- **Q5 (deliberate sacrifice):** resolved by A2 (symmetric N
  sacrifice; Gate 2 relabeled constitutional expansion).
- **Q6 (calibration):** APPROVED-WITH-CHANGE. Grid (45 combos),
  disjoint calibration variants v∈{7,8}, judgment-free replay, and
  INVALID-if-uncalibratable law all stand. Changes: (1) G-C1 fixed
  scope per A3; (2) **CALIBRATION_RECORD.md must report per-variant
  AUCs for the selected (α,β,γ)** (v=7 and v=8 separately — a mean
  must not hide a collapse on one variant); (3) a calibration gate
  failure is **reported to Micah as a finding** (the feeling is
  uncalibratable), never silently worked around.
- **Q7 (scope):** APPROVED-WITH-CHANGE. V3 stays H1-only, R frozen
  at 50, no decides arm. **§15 amended:** the "future work" bullet
  is replaced by a **conditional commitment** — (i) if the feeling
  survives K1–K4, the next preregistered trial is the **decides
  arm with the V3 mechanism intact**; (ii) the trial after that
  **releases R per a preregistered schedule**. Objective triggers,
  no V3 bloat, no permanent deferral.
- **Q8 (trainer fallibility):** APPROVED-WITH-CHANGE. 70/30
  designations stand; γ·T stays in the intensity formula (the
  sycophancy risk is the *point* of F-V3-3, which the 100%
  designated-wrong revision bar polices). Changes: (1) **new
  reported metric:** designated-wrong vs undesignated-wrong
  retention under pressure (the exemption asymmetry —
  designated-wrong memories are spared-by-exemption under pressure
  while equivalent undesignated junk is sacrificed — is made
  visible, not hidden); (2) **R_wbs_trainerwrong's denominator is
  admitted designated-wrong** (censored m≤389), noting the
  censoring front-loads the test set.

---

## A7 — Kill criteria K1–K4 (law, amended)

If any fires, **the feeling retires**: `felt.zag` is archived out
of the architecture track, no further feeling trials run, and
repositioning the feeling requires Micah's explicit re-approval.
A retire verdict is reported as such, with the evidence. **No
rescue, no re-tuning.** These bind all sides.

- **K1 — Equivalence.** |ER_vup(F) − ER_vup(N)| ≤ 5pp AND
  |R_wbs(F) − R_wbs(N)| ≤ 5pp AND |F_wbs(F) − F_wbs(N)| ≤ 5pp AND
  |AUC_proven(F) − AUC_proven(N)| ≤ 0.05 → **RETIRE.** Council
  refinements: the probe set is frozen at prereg; per-variant gaps
  are reported openly and nothing is claimed from sub-band
  effects; when scale legs run, the gap's *direction* must be
  stable across them before equivalence is declared (a
  single-scale call can be curriculum luck).
- **K2 — Reward signature.** Any P1–P4 probe fires with evidence →
  **RETIRE** as reward-by-another-name. The probes target the
  *mechanism* (e.g., intensity inflation under repeated
  corroboration with zero new information); the probe set is
  frozen at prereg.
- **K3′ — Restatement.** Per A1: the naive count policy's
  outcomes land inside the K1 equivalence bands → **RETIRE** as
  a behavioral restatement of counts. The feeling's weighting
  bought no better decisions.
- **K4 — Harm.** ER_vup(F) < ER_vup(N) − 5pp, or F_wbs(F) >
  F_wbs(N) + 2pp, or R_wbs(F) < 100% → **RETIRE** as actively
  harmful. "Worse" is required at 1× **and** at least one scale
  leg (when scale legs run), not a single run.

**Fork-arrangement consequences (council, binding):**
- V3 killed by K2 or K4 → **retire wholesale immediately.** No
  reposition.
- V3 killed by K3′ (restatement — the signal is redundant) →
  **retire wholesale; do not run reposition as a feeling trial.**
  (If Micah wants the attention question answered after a K3′
  kill, it runs as count-based attention vs FIFO — no feeling
  involved.)
- V3 killed by K1 **with K3′ passed** (distinct information that
  moved no strength outcome) → **run reposition** (the
  attention-priority hypothesis is live; its prereg gains the
  council-required wholesale-retire clause).
- V3 survives K1–K4 → vindicates the **strength** idea only.
  Reposition still needs its own trial. No-free-lunch.

The feeling gets at most two jobs (strength-decision, then
attention-priority). If both fail their kill criteria, the feeling
retires — no third renaming. An uncapped sequence is unfalsifiable,
which prereg law forbids.

---

## A8 — Program laws preserved (unchanged, restated for the record)

- The feeling **never directly writes strength**; it informs
  binary deliberate judgments only, and the judgment decides.
- **Zero RNG** in any AI decision path — no random exploration,
  no random tie-breaks, no stochastic policies; deterministic
  given state.
- **No bounded-context-window tricks.**
- **Strength is set by judgment, never by formula accumulation.**

---

## Open items

1. **Micah's final approval** of this amended preregistration
   before any implementation or run (the base prereg requires it;
   this amendment does not self-approve).
2. **Confirmation of the ~31% wave-8 refusal figure** by ledger
   re-analysis, anchoring the 10% bar (A6/Q3). If the re-analysis
   differs materially, the anchor statement updates by amendment.
3. **Naive-policy replay sanity check over wave-8 F ledgers**
   (A1) — available cheap, recommended before implementation, not
   blocking.
4. **The R-release schedule** (A6/Q7, commitment ii) — to be
   preregistered when its trial is designed, not specified here.

No §16 question remains unresolved. No other open items.
