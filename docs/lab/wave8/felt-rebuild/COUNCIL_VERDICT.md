# FELT COUNCIL — VERDICT

Date: 2026-09-20. Status: **debate complete; nothing run.** Five debaters:
fork adjudication, reposition-prereg drafting, V3 §16 Q1–4, V3 §16 Q5–8,
evidence mining from wave-7/8 artifacts. This document is the council's
synthesized recommendation. Dissent lives in the appendix, not in the
recommendations.

## The three forks

### Fork 1 — RETIRE

The retire case: two clean F≡N trials, and the fidelity evidence says the
feeling was structurally denied a real job twice. If the signal is just
counts wearing a costume, keeping it risks reward-by-another-name and
complicates the five-organ integration for nothing.

**Council position:** Retire stays on the table as the *default outcome*,
not a foregone one. Its win conditions are already written into V3's kill
criteria (K1–K4) plus the council's refinements below. Retire WINS if any
kill criterion fires. Retire LOSES only if the feeling beats no-feel by
>5pp on the preregistered bars, holds direction across scale legs, and
passes every anti-reward probe clean.

### Fork 2 — REBUILD (V3, the faithful strength variation)

The rebuild case: the trials never tested Micah's idea — they tested a
thermometer bolted next to a thermostat wired to other sensors. V3 gives
the feeling real binary votes (INVEST-vs-HOLD, SACRIFICE-vs-SPARE), keeps
"feeling never writes strength" as law, and carries binding kill criteria.

**Council position: ENDORSE V3 as the decision procedure for the strength
idea, with the amendments listed under Q1–Q8 below.** Rebuild WINS if
feeling-informed binary judgments beat the no-feel arm by >5pp with all
probes clean. It LOSES on any single kill criterion — no rescue, no
re-tuning, the feeling retires (subject to the reposition sequencing
below).

### Fork 3 — REPOSITION (feeling → attention/priority)

The reposition case: strength may be the wrong role — strength is
accounting already handled by effort gates. A feeling may fit attention
under scarcity: what to rehearse under a fixed deliberation budget.

**Council position: ENDORSE as a distinct, separately-preregistered
hypothesis.** The reposition prereg is drafted at
`PREREG_FELT_REPOSITION.md` (DRAFT — DO NOT RUN): rehearsal-queue
prioritization as the sharp primary job, feeling-ordered vs recency vs
frequency baselines, identical strength machinery across arms (strength
differences are an INVALID bar), held-out recall probes, anti-reward
probes, binding bars. **A reposition win does not vindicate the strength
claim; a reposition loss does not touch V3.** One council-required
addition: the reposition prereg must gain a wholesale-retire clause — if
the trial shows the feeling reduces to count-ordering, the feeling
retires entirely, because both jobs have then collapsed to "counts by
another name."

### The arrangement (endorsed, with two refinements)

1. **V3 decides the strength idea. Reposition is a different hypothesis,
   not the same idea renamed.** Separation plus preregistration is the
   cure for the design-time drift the fidelity report found.
2. **Refinement A — bounded sequence.** The feeling gets at most two
   jobs: strength-decision (V3) and attention-priority (reposition). If
   both fail their kill criteria, the feeling retires — no third
   renaming. An uncapped sequence makes the feeling unfalsifiable, which
   prereg law forbids.
3. **Refinement B — downstream consequences are preregistered now:**
   - V3 killed by K2 (reward signature) or K4 (harm) → retire wholesale
     immediately. No reposition.
   - V3 killed by K3 (restatement — the feeling adds nothing over
     counts) → retire wholesale; do not run reposition as a feeling
     trial. Re-testing a redundant signal under a new name is
     unfalsifiable by construction. (Contested — see appendix.)
   - V3 killed by K1 (equivalence) but K3′ passed (the feeling carries
     distinct information that moved no strength outcome) → **run
     reposition.** Distinct information might move attention outcomes;
     the hypothesis is live.
   - V3 survives → vindicates the strength idea only. Reposition still
     needs its own trial; no-free-lunch.
4. **K1–K4 refinements:** K1 — require the gap's *direction* to be
   stable across scale legs before declaring equivalence (a single-scale
   call can be curriculum luck); report sub-band effects openly, claim
   nothing from them. K2 — probes target the *mechanism* (e.g.,
   intensity inflation under repeated corroboration with zero new
   information); the probe set is frozen at prereg. K4 — require
   "worse" at 1× **and** at least one scale leg, not a single run.

---

## Q1. Thresholds (θ_invest = prior+25, θ_sacrifice = prior+10)

**Options:** fixed margins as written / adaptive margins in calibrated
units / derive thresholds from calibration data.

**Key evidence:** The +25/+10 were picked against the *old* placeholder
α=12 — the same placeholder thinking the fidelity report flagged, one
generation later. Evidence miner: at α=10, a once-corroborated memory
reads exactly 40 = θ_sacrifice — sacrifice-eligible *despite positive
evidence*; at α=18 it reads 48 and is spared. The sacrifice policy's
meaning flips with calibration luck. Worse: G-C1 (twice-corroborated
right-important must clear 55) passes iff the AUC winner has α≥14 —
the trial's validity is hostage to grid interactions.

**Recommendation: APPROVE-WITH-CHANGE — θ_invest = prior + 1.5α,
θ_sacrifice = prior + 0.5α**, computed from the recorded α, frozen as a
procedure. "Invest only when clearly above the base rate" then always
means ≥2 corroborations of evidence; "sacrifice only the unpromising"
always means <0.5 corroborations — at every grid point. Reachability
holds by construction, so G-C1-as-absolute-check retires gracefully;
G-C2 (AUC ≥ 0.60) keeps the discriminability risk covered. Prereg
amendment only; no new trial.

## Q2. PROBE observation (zero-weight, defect-1 fix)

**Options:** approve PROBE / derive negatives from wrong memories'
pre-contradiction reads / leave AUC unevaluable.

**Key evidence:** Confirmed from raw metrics: proven-negative reads = 0
in all 21 phase-E cells — defect 1 is real. The alternative is
conceptually wrong: pre-contradiction, a wrong memory is evidentially
identical to a right one; labeling those reads "negative" tests
prophecy, not thermometry. PROBE is driver-emitted (P1b static gate:
no learner path can emit it), weight-0 (verified by recompute), and
*no decision path consumes proven-status* — there is no channel for a
perverse incentive.

**Recommendation: APPROVE**, with one genuine bug fix: F4a′ ("max junk
I ≤ prior+10") auto-INVALIDs via designated junk (designations are
independent of ground truth, so designated junk reads 30+γ > 40).
**Scope F4a′, G-C3, and P2c to non-designated junk.** Prereg amendment
only.

## Q3. Defect-2 fix (offered-denominator ER_vup, N-relative bar, 10% refusal FAIL, drop absolute 90%)

**Options:** approve / add an absolute floor / keep absolute 90%.

**Key evidence:** Absolute 90% is unachievable-by-construction (~150
right-important offered into 32 slots). The §2 question is explicitly
comparative, so ER_vup(F) ≥ ER_vup(N) − 5pp *is* the question. "Both
arms terrible" is already guarded: K1 fires on equivalence, and the
absolute non-retention bars (AUC ≥ 0.65, 100% revision, refusal ≤ 10%,
K4 tripwires) keep it honest. An absolute retention floor would
reintroduce the broken-bar problem.

**Recommendation: APPROVE**, with two drafting repairs: (a) define
refusal_rate's denominator explicitly (n_refused / total offered
admissions); (b) anchor the 10% to the wave-8 observed refusal rate
(~31%) or a stated tolerance argument — a bare round number invites
the arbitrariness objection. The 10% anchor can come from re-analysis
of existing ledgers; no new trial.

## Q4. K3 counterfactual (the restatement test)

**Options:** keep verdict-divergence <5% / family of counterfactuals /
outcome replay (K3′).

**Key evidence:** Two debaters independently found K3-as-stated broken.
I is *literally* f(C,X,T) — every intensity-driven policy is
extensionally a count-weighting, so "indistinguishable from the
count-based rule" cannot evidence redundancy; it punishes good
calibration (agreeing with common sense becomes a firing offense); and
verdict-divergence ≠ decision quality (policies can diverge 20% on
verdicts with identical outcomes, or 2% with very different ones).
Evidence miner's analytic bound: projected divergence ≈ <1%, far under
the 5% bar — **once G-C1 passes, K3-as-stated may be unreachable by
construction.**

**Recommendation: REJECT K3 as stated; replace with K3′ — counterfactual
*outcome* replay.** The checker replays the preregistered naive count
policy (INVEST iff C≥2; SACRIFICE iff simulated-strength ≤
θ_sacrifice under the exact §4 eligibility) over F's fixed OBS ledger —
exact, because the ledger is judgment-independent per P1 — and computes
its ER_vup/R_wbs/F_wbs. **K3′ fires (RETIRE as restatement) iff the
naive policy's outcomes land inside the K1 equivalence bands.** This
asks the right question: does the feeling's *weighting* of the
evidence buy better *decisions* than the naive weighting? Keep
verdict-divergence as a **reported diagnostic** (against a family:
raw count, time-weighted, trainer-only, recency-only), not a kill
criterion. Required prereg fixes: state the admission-default
strength (currently missing — the trial and the replay both need it);
align the counterfactual's eligibility wording to the §4 gates.
Checker addition + amendment; no new runs. Cheap sanity check
available now: replay the naive rule over wave-8 F ledgers.

## Q5. Deliberate sacrifice (new lawful op)

**Options:** keep DELIBERATE_SACRIFICE / pure-abandon + honest scoring /
symmetric sacrifice for both arms.

**Key evidence:** Not a constitutional breach in the letter (Gate 1 is
consulted first, unchanged; sacrifice fires only where Gate 1 said no)
— but it *is* a constitutional expansion and should be named as one.
The serious issue is a **confound**: F-vs-N currently differs in
*signal* (feeling) *and* privilege (a kill license N lacks). If F wins
K1, we won't know which did it. Evidence miner quantified the harm it
targets: zero pressure events freed too few slots, but ~2.6k
Gate-1-failed abandons cascaded into 152–160 REFUSED_FULL admissions
(30–32%), 41–43 of them right-important. Note: the *refusal* problem
is fixed by the honest metric (§13 defect-2 fix), not by sacrifice —
sacrifice's independent value is whether its victims are actually
junk, measurable via the §10 cited-I distribution against ground
truth.

**Recommendation: APPROVE-WITH-CHANGE.** Keep sacrifice (it
operationalizes "the feeling gets a binary vote"), but **give the N
arm a symmetric count-based sacrifice op** (preregistered rule:
sacrifice iff unproven, non-designated, age≥25, strength ≤
θ_sacrifice, cap 2) — then F-vs-N isolates the feeling, not the
privilege. Relabel §4's Gate 2 as a constitutional expansion, not a
natural gate. Prereg amendment; no new trial.

## Q6. Calibration (grid on v=7,8; argmax; INVALID gates G-C1–G-C3)

**Options:** approve / fix constants at 12/20/25 / widen grid.

**Key evidence:** Judgment-free replay on disjoint variants is genuine
calibration (no circularity — AUC is judgment-independent), caveated
as curriculum-conditional. Winner's-curse risk is bounded by the
coarse grid and two-variant mean; the mitigation is transparency
(all 45 AUCs already required in CALIBRATION_RECORD.md). Reject
fixing 12/20/25: those placeholders produced Gap 4 (the weaker
strengthener) — locking them rebuilds the exact failure Micah refused.
**Genuine bug risk:** G-C1's *min*-over-set, unscoped, will
INVALID a healthy trial — ~9% of episodes are important ∧ wrong
(independent formulas), and their end-of-run reads carry
contradictions that tank I below 55.

**Recommendation: APPROVE-WITH-CHANGE.** (1) Scope G-C1 to
right-important ∧ **not-wrong** memories (wording fix). (2) Add
per-variant AUC reporting for the selected combo (if it wins on v=7
and collapses on v=8, the mean hid it). (3) Keep the grid, disjoint
variants, and INVALID-if-uncalibratable law — a gate failure is
*reported as a finding*, the right scientific posture. Prereg text
fixes; per-variant AUC comes from the same calibration replay.

## Q7. Scope (H1-only, no decides arm, R frozen at 50)

**Options:** approve sharp scope / add decides arm now / unfreeze R.

**Key evidence:** The sharpest objection comes from Micah himself —
his re-trial demand was TNN *choosing among harness variations* via
gated deliberation, and V3 drops the decides arm with "settled well
enough in wave-8." But wave-8's feeling was the *inert* feeling; a
harness-choice test with an irrelevant chooser proves nothing about
choice with a real feeling. Similarly, freezing R repeats half of
Gap 5 — V3 calibrates the feeling but leaves the coupling knob
untouched, and "future work" without triggers is exactly how wave-8's
knob stayed at 50. Against stacking: a decides arm on an unproven
binary-judgment mechanism risks a confounded failure that kills the
feeling for the wrong reason.

**Recommendation: APPROVE-WITH-CHANGE.** V3's H1-only, R-frozen scope
is the right sharp test. The change: amend §15 to replace "future
work" with a **conditional commitment** — (i) if the feeling survives
K1–K4, the next preregistered trial is the decides arm with the V3
mechanism intact; (ii) the trial after releases R per a preregistered
schedule. Objective triggers, no V3 bloat, no permanent deferral.
Prereg text change; no new trial.

## Q8. Trainer fallibility (70/30, 100% designated-wrong revision bar)

**Options:** approve / change the ratio / exclude T from intensity.

**Key evidence:** 70/30 is defensible — adversarial enough to bite
(~30 designated-wrong per run), not so adversarial that γ·T becomes
noise. No direct conflict between the 100% bar and the sacrifice
exemption: they operate on different paths (revision stays mandatory;
the feeling gets no spare vote against evidenced wrongness), and the
mechanism walk shows contradictions still overrule a γ-boosted I.
**But there is a retention asymmetry:** designated-wrong memories are
spared-by-exemption under pressure while equivalent undesignated junk
is sacrificed — trainer-favoritism in retention, currently unreported.
On excluding T from intensity: the sycophancy risk is the *point* of
F-V3-3, not a reason to dodge it — keeping γ·T tests whether the
feeling can take trainer input and still be overruled by world
evidence, which is the "backup/override" dynamic made empirical.

**Recommendation: APPROVE-WITH-CHANGE.** Approve 70/30; keep γ·T.
Changes: (1) add a reported metric comparing designated-wrong vs
undesignated-wrong retention under pressure (make the exemption
asymmetry visible); (2) confirm R_wbs_trainerwrong's denominator is
*admitted* designated-wrong (noting the m≤389 censoring front-loads
the test set). Ledger re-analysis within the planned runs; no new
trial.

---

## What needs a trial vs what doesn't

**Settleable by prereg amendment alone (no new data):** Q1 (adaptive
thresholds), Q2 (PROBE + junk-scope fix), Q3 (denominator + anchor),
Q4 (K3→K3′, admission-default strength), Q5 (symmetric N sacrifice +
relabel), Q6 (G-C1 scope + per-variant AUC), Q7 (conditional
commitment in §15), Q8 (retention-asymmetry metric), the fork
arrangement refinements, the reposition wholesale-retire clause.

**Settleable by re-analysis of existing wave-7/8 data (cheap, no new
trial):** the 10% refusal anchor (Q3); the naive-policy replay sanity
check over wave-8 F ledgers (Q4 diagnostic).

**Genuinely needs the new trial:** whether the feeling's binary
judgments beat no-feel (V3's §2 question); whether the calibration
gates pass (G-C1–G-C3 are empirical); whether feeling-ordered
rehearsal beats recency/frequency (reposition's question).

---

## Appendix — dissenting and contested notes

**D1 (Q1):** A critic could hold fixed +25/+10 margins as simpler and
"likely fine" at the expected grid point (α=18). The council's answer:
"likely works" is not a principle, and the failure mode is a voided
trial. One paragraph of prereg buys the adaptive rule.

**D2 (Q4):** The fork adjudicator proposed testing restatement against
a *family* of counterfactuals with the 5% verdict-divergence line kept;
the Q1–4 debater holds verdict-divergence is the wrong quantity
entirely and only outcome replay is coherent. The council adopts K3′
(outcome replay) as the kill criterion and keeps the family as
reported diagnostics — both positions are preserved in the design.

**D3 (fork sequencing):** Expect pushback that if V3 is killed by K3
(restatement), reposition should still run — "attention is different
enough to test anyway." The council's majority answer: K3 failure
means the signal is redundant; re-testing a redundant signal under a
new name is unfalsifiable by construction. If Micah wants the
attention question answered after a K3 kill, run it as count-based
attention vs FIFO — no feeling involved.

**D4 (Q5):** Minority note — the symmetric-N-sacrifice fix could be
seen as changing what N *is* (wave-8's tested control). The council's
answer: N's identity is "the best-tested non-feeling policy," and a
preregistered count-based sacrifice rule keeps it that while removing
the privilege confound. The alternative — F winning on privilege
rather than signal — is worse.

**D5 (Q6):** On G-C1's min-over-set: the majority holds min is right
(the claim is "the feeling *can* be calibrated to invest in confirmed
importance" — one clean failure falsifies it). Compromise position
noted: mean ≥ θ_invest AND min ≥ θ_invest − 15.

**D6 (Q7):** A council minority could argue the decides arm belongs IN
V3 because Micah's re-trial demand explicitly required TNN choosing
among variations. The majority holds the line at sharpness: sequence
it, don't stack it.

**D7 (Q8):** On γ·T: a reasonable member holds "feeling" should mean
world-derived-only and trainer marks belong at the judgment layer as
cited evidence. The majority keeps γ·T with the 100% bar as guard;
the clean fallback if the council splits is a third arm (F_noT,
γ=0) — costlier, reserved.

**D8 (arrangement):** The bounded two-job sequence (Refinement A) may
meet resistance from the maximalist test-everything instinct. The
council's position: the sequence is preregistered, so it *is*
testing, not arguing — and an uncapped sequence makes the feeling
unfalsifiable, which prereg law forbids.
