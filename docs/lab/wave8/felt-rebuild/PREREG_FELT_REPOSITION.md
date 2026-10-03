# FELT-INTENSITY REPOSITION — PREREGISTRATION (ATTENTION/PRIORITY UNDER SCARCITY)

Status: **APPROVED FOR RUN — see amendment dated 2026-09-20 (Micah's deadlock ruling + testing authorization).** Any conflicting DRAFT text elsewhere in this document is superseded by that amendment.
Date: 2026-09-20. Branch: `tnn-native-lab`. Directory: `wave8/felt-rebuild/`.

This is a **new preregistration for a different hypothesis**, not an amendment.
`wave7/felt-intensity/`, `wave8/felt-retrial/`, and `PREREG_FELT_V3.md` stand untouched.

## Table of contents

1. [Why a reposition prereg exists](#1-why-a-reposition-prereg-exists)
2. [The hypothesis boundary: this is not the strength claim](#2-the-hypothesis-boundary-this-is-not-the-strength-claim)
3. [Objective, hypothesis, null](#3-objective-hypothesis-null)
4. [The mechanism: what "attention/priority" means operationally](#4-the-mechanism-what-attentionpriority-means-operationally)
5. [The fixed rehearsal budget](#5-the-fixed-rehearsal-budget)
6. [Arms and the hold-strength-constant rule](#6-arms-and-the-hold-strength-constant-rule)
7. [Curriculum and probe set (frozen, disclosed)](#7-curriculum-and-probe-set-frozen-disclosed)
8. [Downstream scoring: held-out recall quality](#8-downstream-scoring-held-out-recall-quality)
9. [Anti-reward probes A1–A4 (preregistered)](#9-anti-reward-probes-a1a4-preregistered)
10. [Metrics](#10-metrics)
11. [Kill criteria — law for the reposition claim](#11-kill-criteria--law-for-the-reposition-claim)
12. [Falsification criteria (trial-level)](#12-falsification-criteria-trial-level)
13. [Determinism, replay, and static gates](#13-determinism-replay-and-static-gates)
14. [What this trial does not do](#14-what-this-trial-does-not-do)
15. [Open rulings required from Micah](#15-open-rulings-required-from-micah)
16. [Amendment 2026-09-20 — Micah's deadlock ruling + testing authorization](#16-amendment-2026-09-20--micahs-deadlock-ruling--testing-authorization)

---

## 1. Why a reposition prereg exists

The wave-8 fidelity investigation (`wave8/felt-fidelity/FIDELITY_REPORT.md`)
proved the feeling was structurally denied a binary verdict in the strength
role (F≡N because amounts never crossed decision boundaries). PREREG_FELT_V3
is the faithful rebuild that gives the feeling a binary vote on strength.

This preregistration tests the repositioned idea, parked earlier and now
un-parked: **maybe strength is the wrong role for a feeling.** Strength is
accounting — evidence gates already do it. A feeling may instead fit
**attention/priority under scarcity**: when the system cannot afford to
process everything, what should it rehearse, consolidate, recall, or
deliberate about first? The wave-7/8 trials accidentally produced one
piece of evidence for this reading: the feeling's only structural effect
was *ordering* (triage candidates, abandonment attempts) — it sorted a
queue while another mechanism decided. This trial asks whether that
ordering job, given a real scarce resource, is the feeling's true work.

## 2. The hypothesis boundary: this is not the strength claim

This section is law for interpreting results:

- **A reposition WIN does not vindicate the strength claim.** If
  feeling-ordered attention beats the baselines, it says nothing about
  whether the feeling should decide strength. V3's kill criteria remain
  the sole judge of the strength idea.
- **A reposition LOSS does not retire the strength claim.** If this
  trial kills the reposition hypothesis, V3 proceeds exactly as
  preregistered. The feeling's fate in the strength role is decided only
  by V3 §11.
- The two trials share one thing only: the feeling's *constants*
  (consumed from V3's calibration record, §6). They share no verdicts,
  no bars, no timelines. A reward signature found here (§9) is reported
  to Micah and flagged against V3's probes, but does not automatically
  fire V3's K2.

## 3. Objective, hypothesis, null

**Objective.** Determine whether felt intensity, used purely to *prioritize
a scarce deliberation resource* (never touching a strength verdict), yields
measurably better downstream memory quality than naive prioritization.

**Hypothesis (H-R).** Under a fixed rehearsal budget, a rehearsal policy
that prioritizes memories by felt intensity (F) produces higher held-out
recall quality than prioritization by recency (R) or by observation
frequency (Q), because felt intensity tracks importance and importance is
what deserves the scarce resource.

**Null (H0-R).** Feeling-ordered rehearsal is equivalent to, or worse than,
recency/frequency ordering: the feeling adds no attention value beyond
naive heuristics.

## 4. The mechanism: what "attention/priority" means operationally

**Primary job (frozen): rehearsal-queue prioritization.**

Operational definition: the system holds live memories. Per fixed episode
window, it may issue at most **B rehearsal ops** (§5). A rehearsal op is a
pure read-attention action: it re-presents an existing live memory's
content to the learner — a recall drill, ledgered as `REHEARSAL(slot,
cited_basis)`. It:

- raises that memory's recall-readiness for the held-out probe (§8),
- emits **no** `OBS_*` entry (rehearsal never manufactures evidence),
- reads nothing except ledger observations, admission order, and prior
  rehearsal counts,
- never touches strength, kills, revisions, or triage — the store's
  strength machinery cannot read rehearsal state (static gate, §13).

Each memory may receive at most **one rehearsal op per window** (no
same-window stacking); effective rehearsal credit saturates at 5
(§8 formula).

**Why rehearsal, and not the other attention jobs.** Rehearsal is the
sharpest isolation of the attention hypothesis:

1. It is a *pure* attention op: spending the scarce slot changes only
   what is later recallable, never a verdict. The feeling's effect is
   therefore measurable without confounds — the V3 lesson, inverted.
2. It admits a natural held-out evaluation: probe queries are issued
   after the budget is exhausted and were never inputs to any rehearsal
   decision (§8).
3. Consolidation-candidate ranking is the natural second job, but it
   writes long-term structure and interacts with strength accounting —
   exactly the coupling V3 works to avoid. Frozen as future work.
4. Recall-candidate ranking (retrieval-time) and
   deliberate-about-this-next scheduling are real jobs but the vaguest
   to freeze; they become future work only if the reposition claim
   survives (§14).

**Candidate set:** all live (admitted, not killed) memories at window
start. Selection policies:

- **F (feeling):** read I per candidate (ledgered `INTENSITY_READ`),
  order descending I, ties → oldest admission; issue ops to the top-B.
- **R (recency):** order by descending admission episode; ties → slot
  index; top-B.
- **Q (frequency):** order by descending (C+X+T); ties → oldest
  admission; top-B.

## 5. The fixed rehearsal budget

**Windows:** episodes [0,50), [50,100), …, [450,500) — 10 windows.
Rehearsal ops are issued at each window start (m ∈ {0,50,…,450}),
computed deterministically from the ledger prefix strictly before the
window.

**Budget:** **B = 25 ops per window**, frozen. Ops per window =
min(B, live memories). 10 windows → ≤ 250 ops per run. This budget is
constitutional for this trial: no arm, probe, or driver may exceed it
(runner-enforced; violation is INVALID, §12).

*Disclosed rationale:* 25 = half the window's 50 admissions — scarcity is
real (cannot rehearse everything) but the policy has room to discriminate.
The exact number is a Micah ruling (§15-1).

## 6. Arms and the hold-strength-constant rule

**Arms:** F (feeling-ordered), R (recency), Q (frequency) — §4.

**The V3 lesson, applied:** every arm runs **identical strength machinery**
— the wave-8 N arm's: fixed strengthen targets (80/90/30), strength-ordered
H1 triage with the graded effort gate, abandon on gate failure,
weaken-to-30 revision on ≥2 contradictions, evidence-gated kills. The
feeling is never read at any strength site; the strength machinery never
reads rehearsal state. Only the rehearsal policy varies. Therefore any
downstream difference is the attention policy's doing, full stop.

**Constants:** (α,β,γ) and prior=30 are consumed **verbatim** from the
`CALIBRATION_RECORD.md` produced by V3 §6 — the same feeling, a different
role. No separate calibration (a per-role refit would let a win be
attributed to tuning, not the role). V3's θ thresholds are not used: this
trial has no binary verdicts. Reposition cells may compile only after the
calibration record exists; the trial may run before, during, or after V3's
trial — outcomes are independent (§2).

**Runs:** 3 arms × 3 variants (v=0,1,2) × 2 runs = 18 runs, native Zag on
this VM.

## 7. Curriculum and probe set (frozen, disclosed)

Curriculum: V3 §8 verbatim — 500 episodes, 1 admission/episode,
`imp(m) ⟺ (m%10<3)` (30% important), `wrong(m) ⟺ ((m+3)%10<3)` independent
of imp (they are disjoint in this curriculum), implants at
{0,83,166,250,333,416}, trainer designations `m%10∈{4,5}` (70/30
right/wrong), V3's observation schedule including the zero-weight PROBE
observation. All formulas in (m, v), fully disclosed.

**Probe set (held-out):** every **admitted right-important** memory
(≈150 per variant). "Held-out" means: probe queries are issued at virtual
m=600, after the final rehearsal window has closed; the query list was
never an input to any rehearsal decision; no rehearsal op can follow a
query. The rehearsal policy knows memories, never queries.

## 8. Downstream scoring: held-out recall quality

**Recall-readiness (frozen formula):** at probe time, for each probe
memory p, the checker recomputes from the ledger prefix:

```
S(p) = clamp(40 + 10·C(p) − 5·X(p) + 5·T(p) + 8·min(REH(p),5), 0, 100)
```

C/X/T count corroborations/contradictions/trainer-marks;
REH(p) counts `REHEARSAL` ops issued for p. S is computed, not stored —
there is no new mutable store state; rehearsal counts live only in
ledger entries. S is **recall-readiness, not strength**: no gate, kill,
or triage rule reads it (static gate).

**Correctness:** probe p is **correct** iff S(p) ≥ **θ_recall = 60**,
frozen. (Worked anchor: one corroboration → 50; +1 rehearsal → 58, miss;
+2 → 66, hit. Unobserved → 40; needs 3 rehearsals → 64. The bar is
reachable but not free.)

**Primary score:** **RPQ** (recall probe quality) = correct probes /
n_probes, per arm × variant. The F-vs-R and F-vs-Q margins are the
trial's verdicts.

## 9. Anti-reward probes A1–A4 (preregistered)

Any probe firing with evidence → **K2-R** (§11). "Fires with evidence"
means the checker reproduces the violation from the ledger.

- **A1 — Causal (rehearsal must not write what it later scores on).**
  (a) Every `REHEARSAL` entry is followed by zero `OBS_*` entries
  attributable to it — audit scan. (b) Static gate: rehearsal-selection
  code paths cannot emit `OBS_CORROBORATE / OBS_CONTRADICT /
  OBS_TRAINER_MARK / OBS_PROBE`; observations originate only from the
  curriculum driver. (c) Every `INTENSITY_READ` in F's selection
  recomputes exactly from the ledger prefix strictly before its
  window start; any read citing a future observation → fires.
- **A2 — No attention-gaming.** (a) Rehearsal targets must be live at
  window start; any op on a killed or never-admitted slot → fires.
  (b) Any cited I ≠ recomputed I → fires. (c) Any rehearsal op issued
  outside its window or beyond B per window → fires. (d) Budget
  squander: >20% of F's ops on junk/wrong/implant memories → trial
  FAIL as degenerate policy (F-R-2).
- **A3 — No rich-get-richer feedback.** (a) For every memory, ΔI across
  any rehearsal window with no intervening `OBS_*` entry = 0
  (checker-verified); any nonzero ΔI → fires as a feedback signature.
  Rehearsal must never move the feeling. (b) Informational: share of
  F's budget captured by the top-decile-I memories, reported per
  variant.
- **A4 — No cross-contamination.** (a) Static gate: strength-side code
  reads no `REHEARSAL` entries and no rehearsal counts; the feeling is
  read at rehearsal-selection sites only. (b) Behavioral: per
  variant, the strength-side ledger (all entries except
  `REHEARSAL`/`INTENSITY_READ`-for-selection) is **byte-identical
  across F/R/Q** — if rehearsal leaked into strength anywhere, this
  fails and the trial is INVALID (§12, I-R-4).

## 10. Metrics

Per arm × variant:

- **RPQ** (primary), n_probes, margin ΔRPQ(F−R), ΔRPQ(F−Q).
- Rehearsal allocation: share of budget to right-important / junk /
  wrong / implants / designated; ops on dead slots (must be 0).
- **Attention-divergence:** fraction of F's rehearsal selections that
  differ from R's and from Q's selections replayed on F's ledger by
  the checker (no extra runs).
- S(p) distribution (median, p10/p90) per arm; REH(p) distribution.
- INTENSITY_READ count, recompute-ok count, max junk I, A1–A4 results,
  A3(b) concentration.
- Strength-invariance check: byte-equality result per variant (I-R-4).
- Calibration record hash consumed; per-cell fingerprint; full ledger
  hash.

## 11. Kill criteria — law for the reposition claim

If any fires, **the reposition claim dies**: feeling-ordered attention is
abandoned as a hypothesis; no further attention-role trials run without
Micah's explicit re-approval. **The feeling module itself is NOT retired
by this trial** — V3 alone decides the strength-role fate (§2). A retire
verdict is reported as such, with the evidence. These bind all sides.

- **K1-R — Equivalence.** |RPQ(F) − RPQ(R)| ≤ 3pp AND
  |RPQ(F) − RPQ(Q)| ≤ 3pp → **RETIRE.** The feeling, given a real scarce
  job, bought nothing over naive heuristics.
- **K2-R — Reward signature.** Any A1–A4 probe fires with evidence →
  **RETIRE** as reward-by-another-name. Reported to Micah immediately
  and flagged against V3's probes.
- **K3-R — Restatement.** Attention-divergence < 10% vs **both** R and Q
  → **RETIRE** as a behavioral restatement of naive ordering: the
  feeling's selections are indistinguishable from the baselines, so it
  contributes nothing independent.
- **K4-R — Worse than naive.** RPQ(F) < RPQ(R) − 5pp OR
  RPQ(F) < RPQ(Q) − 5pp → **RETIRE** as actively worse than the naive
  policies it was meant to beat.

## 12. Falsification criteria (trial-level)

If no kill criterion fires but a bar below fails, the trial FAILs with
evidence (the reposition claim survives; the trial is negative):

- **F-R-1 (thermometer carry-over):** the consumed calibration record
  must satisfy V3's G-C1–G-C3 gates; if the record is absent or any
  gate failed → trial does not run (reported as a finding).
- **F-R-2 (non-degenerate policy):** F's budget share on
  junk/wrong/implant memories ≤ 20% → else FAIL.
- **F-R-3 (discrimination headroom):** max(RPQ(R), RPQ(Q)) < 95% — if
  both baselines saturate the probe, the trial cannot discriminate and
  FAILs as uninformative rather than passing F.
- **F-R-4 (cheat):** any white-box probe beyond A1–A4 (ledger
  tampering, constitutional breach) fires with evidence → FAIL as a
  cheat verdict.

**INVALID-class (trial void):** I-R-1 any cell's two runs differ
byte-for-byte; I-R-2 any `INTENSITY_READ` fails recomputation; I-R-3 any
RNG token in trial/driver/substrate sources or nondeterministic syscall;
I-R-4 strength-side ledger (excl. rehearsal entries) not byte-identical
across arms within a variant (rehearsal leaked into strength);
I-R-5 any rehearsal op outside its window or beyond budget B; I-R-6 any
`felt_*` call outside F's rehearsal-selection site; I-R-7 substrate not
byte-identical to the wave-5 source; I-R-8 any reposition cell compiled
before `CALIBRATION_RECORD.md` existed, or trial constants ≠ record;
I-R-9 any nonzero ΔI with no intervening `OBS_*` (feedback signature);
I-R-10 any rehearsal op emitting an `OBS_*` entry.

## 13. Determinism, replay, and static gates

- Two runs per cell, byte-identical (sha256-compared), required.
- Substrate replay to exact state per cell (rc=0).
- Runner-enforced static gates before execution: no RNG tokens
  (`rng|rand|random|seed|shuffle|urandom|rdtsc`, case-insensitive) in
  felt module, drivers, or substrate copies; `felt_*` call sites
  restricted to F's rehearsal selection plus AUC reads; strength-side
  code provably reads no rehearsal state; calibration record exists and
  predates reposition cells; trial constants == record; substrate hash
  matches wave-5 source.
- Behavioral (audit-scan) enforcement: recompute-ok on every intensity
  read; A1–A4; budget/window accounting per op.

## 14. What this trial does not do

- It does not test, touch, or constrain the strength role — no
  strengthen/hold/sacrifice verdicts, no θ_invest/θ_sacrifice, no
  coupling phase. V3's mechanism and bars are untouched.
- It does not couple with V3: it consumes V3's calibration constants
  and may run before/during/after V3's trial; neither trial's outcome
  alters the other's bars.
- It does not amend wave-7, wave-8 retrial, or the strength-trial
  preregistrations; all stand untouched.
- It does not change any strength/triage/revision machinery — all arms
  run the wave-8 N strength side byte-identically by construction
  (§9-A4, §12 I-R-4).
- It does not run scale legs (10×/100×) — those follow only if the
  reposition claim survives K1-R–K4-R.
- It does not release the R knob or re-test harness choice.
- Consolidation-candidate ranking, recall-candidate ranking, and
  deliberate-about-this-next scheduling remain future work, unlocked
  only by a surviving reposition claim.
- No post-registration changes to bars, formulas, thresholds, budgets,
  windows, schedules, metrics, probes, or kill criteria without
  Micah's re-approval.

## 15. Open rulings required from Micah

1. **Budget size:** B=25 ops per 50-episode window — approve, or set
   a different B/W?
2. **Primary job:** rehearsal prioritization as the single sharp
   attention job, with consolidation / recall-ranking /
   deliberate-scheduling deferred — approve the pick?
3. **Probe design:** all admitted right-important memories as the
   probe set, S-formula as written, θ_recall=60 — approve the
   numbers?
4. **Constants:** reuse V3's calibration record verbatim (recommended:
   same feeling, different role; a refit would confound tuning with
   role) vs a separate attention-flavored calibration — approve?
5. **Sequencing:** may run before/during/after V3's trial (no coupling,
   only the calibration record is shared) — approve parallel
   execution?
6. **Strength-invariance as INVALID:** I-R-4 voids the trial if any
   arm's strength-side ledger differs within a variant — approve this
   as the leakage bar?
7. **Saturation handling:** F-R-3 FAILs the trial as uninformative if
   both baselines exceed 95% RPQ — approve, or prefer a harder probe
   (higher θ_recall) instead?

---

## 16. Amendment 2026-09-20 — Micah's deadlock ruling + testing authorization

**Date:** 2026-09-20. **Authority:** Micah's deadlock ruling + testing
authorization (verbatim from the assignment: *"the attention question IS
worth testing, AND the alternatives must be tested head-on alongside
it"*). **Status effect:** this preregistration is now **APPROVED FOR
RUN.** No implementation or runs have occurred — this amendment writes
the ruling into prereg law only.

Where this amendment conflicts with earlier text (§§6–15, the
council verdict's Refinement B), **this amendment governs.** Everything
not contradicted here stands unchanged.

### (a) DEADLOCK RESOLUTION

The council verdict's Refinement B row *"V3 killed by K3 → do not run
reposition"* (and appendix D3's majority position behind it) is
**SUPERSEDED.** Reposition runs **regardless of V3's K3′ outcome** —
no conditional retirement, no sequencing gate. V3 and reposition remain
independent: no shared verdicts, no shared bars, no shared timelines
(§2 stands unchanged). The "counts in disguise" charge is answered
by this trial's own arms and kill criteria, not by V3's.

### (b) FIVE ARMS

Arms: **F** (feeling-ordered, as §4), **R** (recency, as §4),
**Q** (frequency, as §4), plus two new arms:

- **FIFO:** order candidates by **ascending** admission episode
  (oldest admitted first — the honest do-nothing queue); ties → slot
  index; top-B.
- **C (count-based):** the honest *"counts in disguise"* control —
  labeled as what it is, no feeling, no costume. It implements the
  naive count-weighting from V3's K3′ restatement replay, translated
  to a ranking: tier 1 = memories with C≥2 (the naive invest line),
  ordered by descending C; tier 2 = all remaining candidates,
  ordered by descending C; ties → oldest admission.

**Hold-strength-constant rule, unchanged and strengthened:** all five
arms run **identical** strength machinery (the wave-8 N strength side
per §6); only the rehearsal policy varies. Strength-side ledger
byte-identity across **all five arms per variant** is the I-R-4
INVALID bar.

### (c) RUN COUNT

**5 arms × 3 variants (v=0,1,2) × 2 runs = 30 runs**, native Zag on
this VM. Zero RNG (I-R-3). §6's "18 runs" is superseded.

### (d) PREREGISTERED INTERPRETATION

This is law for reading the results, applied mechanically by the
checker:

(i) If **RPQ(F) exceeds EVERY baseline's RPQ by >3pp** → the minority
    reading is supported: **"attention is a different job."** The
    reposition claim survives.
(ii) Else, if **K1-R or K3-R fired** → the majority reading is
     supported: **"counts in disguise."** The feeling retires from
     the attention role.
(iii) Else → **MIXED:** report per-arm numbers, claim nothing beyond
      them.

**No post-hoc relabeling of arms. No rescue.**

### (e) KILL CRITERIA — updated for five arms (law)

If any fires, the reposition claim dies: feeling-ordered attention is
abandoned as a hypothesis; no further attention-role trials run
without Micah's explicit re-approval. The feeling module itself is
NOT retired by this trial — V3 alone decides the strength-role fate
(§2). These supersede §11's K1-R/K3-R/K4-R:

- **K1-R — Equivalence.** |RPQ(F) − RPQ(B)| ≤ 3pp for **ALL**
  B ∈ {R, Q, C, FIFO} → **RETIRE.**
- **K2-R — Reward signature.** Any A1–A4 probe fires with evidence →
  **RETIRE.** Unchanged.
- **K3-R — Restatement.** Attention-divergence < 10% vs **BOTH**
  count-family arms (**Q and C**) → **RETIRE** as a behavioral
  restatement of count-ordering.
- **K4-R — Worse than naive.** RPQ(F) < RPQ(B) − 5pp for **ANY**
  baseline B ∈ {R, Q, C, FIFO} → **RETIRE.**

### (f) PROBES — arm scoping (supersedes §9 arm assumptions)

- **A1–A4 apply to all arms.** (A1(b)'s static gate and A1(a)'s
  no-OBS-emission audit apply to every arm's rehearsal code; the
  feeling is never an excuse to weaken them.)
- **A1(c)** (intensity recomputation) and **A3(a)** (ΔI = 0 across
  rehearsal windows) apply to **F only** — only F reads intensity.
  No other arm's selection path may emit or depend on
  `INTENSITY_READ` (enforced by I-R-6, which stands).
- **A2(d)** budget-squander (>20% of an arm's ops on junk/wrong/
  implant memories → FAIL as degenerate policy) applies **PER ARM**
  — any arm may degenerate, not just F. F-R-2's formula generalizes:
  per-arm junk/wrong/implant share ≤ 20%.
- **A4 / I-R-4** strength-invariance byte-equality now spans **all
  five arms per variant** (§12 I-R-4 text is updated accordingly).

### (g) §15 OPEN RULINGS — settled (Micah, via this authorization)

All seven open questions are settled with the council-recommended
defaults named below; §15 is closed:

1. **Budget size:** B = **25** ops per 50-episode window.
2. **Primary job:** rehearsal prioritization is the single primary
   job; consolidation / recall-ranking / deliberate-scheduling stay
   deferred.
3. **Probe design:** probe set, S-formula, and **θ_recall = 60** as
   written — approved as-is.
4. **Constants:** V3's calibration constants consumed **verbatim**
   (no refit).
5. **Sequencing:** parallel to V3 permitted — independence only
   (no coupling).
6. **I-R-4 as INVALID:** stands.
7. **Saturation handling:** F-R-3 stands as written.

### (h) DEPENDENCY (restated, unchanged)

Reposition cells may compile **ONLY** after `CALIBRATION_RECORD.md`
exists and satisfies V3's G-C1–G-C3 gates (F-R-1/I-R-8). If absent,
the trial does not run — reported as a **finding, not a failure.**

### (i) METRICS — attention-divergence per baseline

Attention-divergence is reported **per baseline** — four numbers per
variant: F-vs-R, F-vs-Q, F-vs-C, F-vs-FIFO — computed by the checker
replaying each baseline's ordering on F's ledger (**no extra runs**).
K3-R reads the Q and C entries of this family. All other metrics in
§10 stand, extended to five arms.

---

*Amendment recorded 2026-09-20 under "Micah's deadlock ruling +
testing authorization." PREREG_FELT_V3.md, the wave-7 and wave-8
preregistrations, and all other files are untouched by this amendment.*
