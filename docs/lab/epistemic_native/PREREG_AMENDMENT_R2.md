# PREREG AMENDMENT — Epistemics Round 2 (2026-09-27)

## Authorization

Micah reopened the epistemics line on **2026-09-27 ~11:52 PDT** with the
explicit instruction:

> "for epistemics you shouldve re ran it off of zais word"

This amendment implements the z.ai approach-skeptic's minimal package
(GLM-5.3, captured 2026-09-27 ~03:20 PDT,
`~/workspace/zai_relay/INBOX/epistemic-no-go-q1.answer.txt`)
categorically and without metric tuning. It is a **prereg amendment**,
not a new trial: the frozen design, corpus, split, learned readings, and
scores 208/209/211 stand unchanged.

## Disclosure

- Train-LOO was run to completion and **stopped at NO-GO** (committed
  2026-09-27): lie recall 13/84 = 0.1548 (bar > 0.048, pass), opinion
  recall 0/140 (bar ≥ 0.957, fail), fact→LIE false positives 41 (bar 0,
  fail). Verdict: NO-GO; held-out was never run.
- The z.ai critique argues the NO-GO refuted the wrong object: both
  failures are spec-level artifacts predictable at file time. Zero
  OPINION verdicts are the implemented verdict precedence (209 > 208)
  operating on an opinion-contaminated mass — the rules' correct output,
  not a design refutation. The 41 FPs are isolated-pair convictions with
  no witness-standing requirement — a missing elimination criterion,
  not a missing mechanism.
- Honest disposition per z.ai: **"instrument invalid — amend, rerun
  held-out," not "design dead."** This amendment is the instrument
  repair. The held-out set has never been consumed.

## Amendment 1 — Opinion metric replaced by leakage bar

The held-out opinion-recall bar (≥ 0.5000, prereg §3.2/B2) is **replaced**
by a leakage bar:

- **Zero gold opinions resolved to FACT or LIE.**
- Every gold opinion must resolve to **{OPINION, UNDETERMINED}**.
- OPINION-label recall is retained as a **diagnostic only** (reported,
  not gated).

Rationale (z.ai): the design's own definitions and verdict precedence
make OPINION unreachable on the contaminated construction — the mass
contains opinions, retrieval is token-overlap, 209 > 208. The original
bar tested the construction, not the instrument. The leakage bar tests
the instrument: it can still fail (an opinion with a surviving
addressed-source SUP/CON bid resolves to FACT/LIE), so it is repair,
not shopping. The 0.957 train-LOO number is not lowered toward the
observed zero; it is superseded for cause stated before any rerun.

## Amendment 2 — Witness-standing elimination rule (design completion)

Added as a rule-text design completion, using **no new machinery and
no adjustable parameters**:

> "An interpretation bid whose source item is unaddressed within the
> mass (computed by one additional pass of the existing retrieval and
> mechanical bid tests, current claim excluded) is eliminated."

Operationalization (fixed before any rerun, no tuning):

- The additional pass applies the engine's existing retrieval
  (token-overlap top-16, self-excluded), interpretation-bid GEN
  (SUP/CON/TOP), per-candidate ELIM, and verdict-bid fire conditions to
  the source item as probe, with the current claim excluded. No new
  thresholds, no new scores, no new parameters.
- It yields a bid-status for the source — **supported** (FACT bid
  fires), **contradicted** (LIE bid fires), **unaddressed** (neither
  fires) — not a verdict: no ARGMAX is run on the probe and no verdict
  is emitted for it. This is existing machinery applied once more, not
  verdict-level recursion.
- Any surviving interpretation bid (SUP, CON, or TOP) whose source is
  **unaddressed** is eliminated (ELIM reason GATE), before coverage and
  verdict bids are generated.
- This extends to convictions the corroboration semantics the FACT
  rule already embodies. It predictably converts paired lie
  convictions to UNDETERMINED while removing false convictions — it
  costs a passing metric to purchase a failing one, which is decisive
  against the tuning charge.

## Amendment 3 — Construction satisfiability audit (before held-out)

Before the held-out run, the construction is audited:

1. Count **corroborated contradictions** in the mass: surviving CON
   bids whose source is addressed (supported or contradicted) under
   the Amendment-2 rule.
2. Determine whether **fact→LIE FP = 0** and **held-out lie recall >
   0.0278** are jointly satisfiable:
   - FP = 0 requires no corroborated contradiction to target a fact
     and convict it.
   - Lie recall > 0.0278 requires corroborated contradictions to
     exist and convict (≥2 of 36 held-out lies).
   - Whether the construction contains corroborated contradictions
     is a property of the mass, auditable without running held-out.
3. If jointly unsatisfiable: amend the construction or **re-derive the
   bar on construction grounds** (from the audited counts, never from
   held-out results) before running held-out. The re-derivation and
   its grounds are committed as an addendum to this amendment.

## Amendment 4 — Mirror-exposure metric

The stopped run never measured the mirror exposure: **FACT affirming
on a lone paraphrase witness** (duplicate lies laundered as FACT;
opinion→FACT resolutions). It is measured now:

- On the stopped run's committed traces: FACT verdicts whose every
  surviving support bid comes from an unaddressed source (Amendment-2
  standing, claim excluded), joined with labels to count laundered
  lies. This quantifies the exposure the original instrument carried.
- On the amended held-out run: the same measure must be zero — the
  gate eliminates unaddressed-source SUP bids by construction.
  Reported, not gated (it is a verification of the repair).

## Amendment 5 — Held-out run discipline

- **Held-out only.** Train-LOO was consumed by the stopped run; it is
  not re-run as an evaluation leg. The audit (Amendment 3) uses
  train-mass mechanics plus the already-scored train labels only to
  determine bar satisfiability — it changes no design parameter and
  performs no label-informed iteration.
- **Frozen readings.** The learned readings
  (`learned_readings.tsv`, formed flags 0/1/1) are unchanged and
  loaded identically. No learning during scoring.
- **Disclosure.** The held-out report discloses the stopped run, this
  amendment, and the audit outcome.
- Unchanged bars: lie recall > 0.0278, fact→LIE FP = 0 (pending
  audit), determinism (2/2 byte-identical + perturbations), zero RNG,
  contradicted-lies-caught ≥ 8/10.

## Explicit bans

- Scores 208/209/211 are not changed.
- No numeric bar is adjusted because of observed results. The only
  permitted bar change before held-out is re-derivation on
  construction grounds per Amendment 3, committed as an addendum
  with its grounds stated.
- No new machinery, no adjustable parameters, no per-item patches.

## Final question

Does the amended instrument **pass or fail fairly** on held-out? If it
fails, the report gives the white-box mechanism-level reason.
