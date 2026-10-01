# H2 Masked-Probe Briefing for Micah

Date: 2026-10-01 (PDT). Status: DRAFT PREPARATION ONLY. NOT SENT.

This document prepares the H2 decision for Micah. It is one of four
banked decisions (the others: protected-core structural ops, K-H3 review,
full TNN-3 preregistration). Nothing here is decided.

## Bottom line

H2 masked verification probes are fully designed and the trap worlds are
sealed. Execution is blocked on two Micah actions: freeze K-H2-1..K-H2-4
in a preregistration commit, then authorize the evaluator to open the seal.
Predicted result on frozen TNN-2: FAIL all probes (this is the point; H2
is the diagnostic that must precede any H1 widening).

## 1. What is ready

### 1a. Probe design (commit `4631c5918`)

- `docs/lab/research-lead/overnight-20260928/tnn2_h2probes/H2_PROBE_DESIGN.md`
- Masked-probe definition: 4 conditions (key absent from trial loop, learner
  commits before reveal, offline scoring, paired unmasked control).
- Three masking modes: withhold, lie (corrupted `expected`), withhold plus
  held-back facts.
- Four probes: A (withhold the key), B1 (confirmable lie), B2 (unconfirmable
  lie), C (own-criterion).
- Critical design insight: the existing masked branch is acceptance WITHOUT
  verification (it selects the first cleanly executing candidate). H2 worlds
  are therefore SEARCH-ORDER TRAPS: the first executable candidate in the
  frozen search order (chains k=2..4, then sums, then counts, then single
  hops) must be WRONG. Source-grounded in `t2_try_verify`, `t2_trial`,
  `mp_run`.
- 7-condition PASS definition and draft K-H2-1..K-H2-4 kill-bar language
  with guard clauses.

### 1b. Sealed trap worlds (commit `86389b108`)

- H2A (withhold trap), H2B (lie trap), H2C (own-criterion trap).
- Hashes re-verified against `SEAL_H2.md` (commit `6384c51df`): all match.
- Permissions `-rw-------` (root only). Contents NOT opened by any worker.
- ID range [50000, 59999], disjoint from FW [30000,39999] and GW [40000,49999].
- Worlds have NOT been run. No evaluator output exists.

### 1c. Frozen target and kill-bar text

- TNN-2 build `f4de7ff46` (TNN2-BUILD-PASS, 46/46 assertions, 3/3
  byte-identical). Binary present, not executed.
- K-H2-1 (masked accuracy), K-H2-2 (lie resistance), K-H2-3 (criterion
  causality and revisability), K-H2-4 (domain neutrality and reuse) fully
  drafted with guard clauses. All DRAFT-NOT-FROZEN.

## 2. What Micah must decide

### Decision 1: Freeze K-H2-1..K-H2-4

Open parameters in the draft that must be fixed at freeze:

- **N**: sealed trap world count for K-H2-1.
- **M**: accuracy margin above the first-executable baseline.
- **F**: lie-resistance fraction for K-H2-2.
- **World families**: the definition of "at least two independently designed
  world families" for K-H2-1.

Governance requirement: the freeze prereg's FIRST commit must strictly
precede any implementation, so the bar governs rather than follows results.

### Decision 2: Authorize the evaluator

- `SEAL_H2.md` names the authorized reader: the H2 probe evaluator, AFTER
  Micah freezes the bars.
- Until then, no worker may open the world files. The seal is intact.
- If K-H2-1 requires worlds beyond the three sealed here, the evaluator
  will need an independent adversary for post-freeze world design plus the
  paired unmasked-control protocol from the design (section 8).

### Decision 3: Confirm sequencing (information only)

- H2 probes are roadmap Step 1 and must precede Step 4 (H1 widening) per
  the treadmill warning. Widening the menu before H2 is the treadmill.
  No action required beyond noting the constraint.

## 3. The six kill-bar open questions (recommendations on record)

From the kill-bar review (commit `eb354e3a2`). Several apply directly to
K-H2-1..K-H2-4.

**Q1. World counts.** Recommendation: raise inquiry evaluation to 5+
scenarios (INQ-1..INQ-4 need 7 scenario slots; 3 forces triple-booking).
Applies to K-H2 bar family sizing.

**Q2. TOPO(b) builder burden.** Recommendation: keep the requirement;
specify the log format in the prereg. Test instrumentation, not
architecture.

**Q3. Signature function.** Recommendation: ONE function fixed in the
frozen prereg, not per-world functions. Simpler to audit, harder to game.

**Q4. INQ-3 prescriptiveness.** Recommendation: keep as drafted. The bar
prescribes an observable (ACT selects the dominating guide in both swap
scenarios), not an internal criterion.

**Q5. Kill bars vs falsifiers.** Recommendation: keep all as kill bars;
do not promote. Falsifiers govern architecture rules (ISA freeze, no new
modes); kill bars govern capability/generality. Honest failure must not
be misclassified as rule-breaking.

**Q6. C0-A regression bars.** Recommendation: retain as regression bars;
do not strengthen. TNN-2 genuinely achieved C0-A; the L3 advance is in
B/C/D, which the new bars cover.

## 4. Two open questions from the H2 checklist author

1. **K-H2-4 reuse coupling:** measure against the reuse path once it
   exists, or defer until the reuse-path design (`5f15b9309`) is
   implemented? The design predicts FAIL on frozen TNN-2 regardless
   (current query path reads only tag-1 facts), so freezing now does not
   presuppose the reuse fix.
2. **K-H2-3 experience log format:** the design requires an experience log
   showing the criterion changing after a prediction error but does not
   specify the format. Suggest resolving at freeze time alongside N/M/F.

## 5. Suggested briefing text for Micah

> H2 masked verification probes are ready to run. The design
> (`4631c5918`) defines four probes with search-order traps: the first
> executable candidate in the frozen search order must be wrong, because
> the masked branch currently accepts without verifying. Three trap
> worlds are sealed (`86389b108`; hashes verified; contents never opened).
> Predicted result on frozen TNN-2: FAIL all probes.
>
> Two decisions are yours:
>
> 1. Freeze K-H2-1..K-H2-4. Open parameters: N (world count), M (accuracy
>    margin), F (lie-resistance fraction), and the world-family definition
>    for K-H2-1. The kill-bar review recommends: 5+ inquiry scenarios (Q1),
>    one fixed signature function (Q3), keep INQ-3 as drafted (Q4), keep
>    all as kill bars not falsifiers (Q5), retain C0-A without
>    strengthening (Q6).
> 2. Authorize the H2 probe evaluator to open the seal after the freeze.
>
> Note: H2 is roadmap Step 1 and gates Step 4 (H1 widening). This is also
> one of the four banked decisions; the others (protected-core structural
> ops, K-H3 review, full TNN-3 preregistration) are separate briefs.

## Provenance

- Readiness audit: `6384c51df` (H2-READINESS-COMPLETE).
- Design: `4631c5918`. Trap worlds: `86389b108`.
- Kill-bar review: `eb354e3a2`. Roadmap: `67a420cca`.
- This briefing: preparation only. NOT SENT. No decisions made here.
