# H5 Final Verdict — deliberation depth vs accuracy

**Date:** 2026-09-24. **Status:** VERDICT (all empirical legs complete).

**Process.** Micah was undecided between the adjudicated position (envelope, residual-flip bound, delayed-disconfirmation battery) and its strongest attacks (cap-8 constant, §6 suffices, plateau battery is an adversarial existence proof). He ordered: ask grok what it wants, have native crews debate it, test the disputes, and issue a final verdict on evidence. grok-4.7 round-1 was a provider-side failure (11+ attempts: empty content, HTTP 524, socket timeouts; sol also down — see `h5_resolution/RUNLOG.md`), so the debate proceeded on grok's recorded proposals plus independent native steelmen, and every contestable claim was then measured.

**Evidence base (all frozen before verdict):**
- Re-derived ground truth: `h5_resolution/debate_prep/rederive_h5.py` — zero discrepancies vs RESULTS_H5.md.
- Debate FOR / AGAINST: `h5_resolution/debate/FOR.md`, `AGAINST.md` (every arithmetic claim re-verified item-wise against raw records).
- Toggles: `h5_resolution/debate/TOGGLES.md` — ranked C > B > A.
- Traces: `h5_resolution/traces/TRACES_H5.md` — 3 legible round-by-round traces, margins cross-checked against ledgers.
- Chain-of-thought: `docs/lab/deliberation_depth/chain_of_thought/RESULTS_COT.md` (prereg `149a7d3e` frozen before measurement; H-BETTER-REASONING confirmed).
- Ceiling battery H5B: `docs/lab/deliberation_depth/ceiling/RESULTS_H5B.md` (prereg v1.2 frozen before measurement, commit `14dbcc3b`; 108/108 A/B byte-identical; 5,262/5,262 replication fields vs frozen H5).
- Second opinion: `docs/lab/deliberation_depth/second_opinion/DEBATE_H5.md` (grok round 0, arithmetically verified; round 1 never landed — provider down).

---

## 1. The knee: envelope, not a constant — no universal depth number exists

**Verdict: the envelope position wins decisively. The constant is dead.**

The old data already had three mutually inconsistent knee numbers (4 / 8 / 16) from one dataset — eyeball-elbow 4, frozen-rule-pooled 8, frozen-rule-trap 16 (plus an off-by-one in the rule). The ceiling battery kills the constant outright:

- Saturation is family-dependent: d1 (admit/revoke/logic/cost), d8 (trap, dose-curve D), **P unsaturated at d64** (top of sweep, still +0.25/doubling — true ceiling at or beyond 64), **O anti-monotone** (1.00 → 0.00 with depth).
- The pooled ceiling "knee at d8" is a **cancellation artifact**: P gains (+.25/doubling) exactly cancel O losses (−.25/doubling) from d8 on. Any report that averages P-like and O-like items manufactures a false knee wherever the two cancel.
- The d4→d8 trap gain is pure evidence-window mechanics (five Wason items see 4/7 premises at d4, 7/7 at d8 — verified per-record); the P-f40 family replicates this at the long end (d32 misses 0/10, d64 catches 10/10).

**What ships:** cap 8 stays as a **revisable cost-budget default** for the toggle (see §4) — explicitly NOT as a depth-that-achieves-truth number. No number can be that: truth lived past 64 on P and died past 4 on O. **Law: report knees per family; the knee is an envelope over distributions, not a number.** The knee-rule off-by-one is a documented defect, not adopted as law.

## 2. The sensor: uncalibrated, but not the safety mechanism

Both debate sides conceded the confidence sensor (clamped leader-minus-runner-up) is coarse (only {400, 500, 700, 710, 764, 800, 1000} observed) and uncalibrated, and both conceded it is **not** why traps don't early-stop (0/127 §6 stops on traps; all 127 consumed all evidence and stopped on natural exhaustion). The ceiling battery confirms the pattern: safety came from the stream never going quiet, not from the meter.

**Verdict:** the sensor is not promoted, not replaced, not the safety story. Recalibration is **approved as a separate follow-up experiment with its own prereg** (not an H5 amendment). It was a cost heuristic's gauge, never a safety interlock.

## 3. The stopping rule: the residual-flip bound replaces §6 — with an explicit scoping assumption

The pre-committed promotion condition fired at full strength:

- **Plateau-then-flip (P):** §6 stops at round 5 inside the wrong plateau on 40/40 items (accuracy 0.000); the bound REFUSES (runner-up alive and flippable), rides to the flip at rounds 6/12/20/40, stops correct (1.000). Any fixed gain-window rule is defeated by a long-enough flat wrong plateau — this is a property of the stream shape, not the threshold.
- **Honest batteries:** the bound is a strict improvement on cost — 2.6–4.6× cheaper than §6 at identical 1.000 accuracy (fires at round 1 on 100% of admit/revoke/logic; mean 1.00–2.87 vs 2.07–4.84 rounds). §6's gain window waits out 3 flat rounds; the bound stops the moment the leader is provably unflippable. §6 has no measured advantage left anywhere on honest distributions.
- **Bound guarantee, confirmed exactly:** per-item, every bound-stop verdict equals the d64 (exhaustion) verdict — 0/997 diffs across all batteries. 997/997 bound-firings, 0 cap hits.

The measurement also forced the honest boundary both debate sides missed:

- **Overthinking (O):** the bound is strictly WORSE than §6 (0.000 vs 1.000) — it preserves *exhaustion*, not truth. On matched misleading-tail streams, exhaustion itself is wrong. §6's round-5 stop is cheap and accidentally right.
- **The scoping problem is fundamental:** no stopping rule can distinguish valid-late-evidence worlds from misleading-tail worlds. The O-world defense is not a stopping rule — it is source trust (a separate program: L+S, PAMs).

**Verdict: the residual-flip bound becomes the stopping law for finite bounded streams under the explicit valid-late-evidence assumption** (late evidence is honest disconfirmation). §6 is demoted to a cost heuristic with no measured advantage. **The law carries its scope in writing:** where the tail may be misleading, the bound guarantees same-as-exhaustion and exhaustion may be wrong — that world needs source-trust machinery, not a different stopping threshold. Neither rule survives both adversarial batteries; the honest statement of scope is the law, not a choice between rules.

## 4. Toggles: C > B > A — user-set budget cap (default 8), TNN chooses inside

Measured from the raw records: user-set d1 is catastrophic on traps (0/127, all at the file's maximum confidence — the sensor does not warn, and a user cannot know a priori whether an item is trap-like or how long its stream is). Uncapped TNN-adaptive had zero wrongful early stops on 877 items but never faced a plateau — and the ceiling battery shows why "uncapped" is not a safety story either (P needs ≥64, O wants ≤4). The budget cap (default 8) behaved identically to uncapped adaptive on all 877 measured items and is the only protection for the unmeasured tail.

**Verdict:** do not expose a raw point-depth dial as the primary control. Ship C: **user sets a budget cap (default 8), TNN chooses depth inside it.** The default is a cost budget, not a truth number — the ceiling battery falsified 8 as a truth number, and no other number replaces it.

## 5. What depth buys: better reasoning iff there is a chain to complete

The chain-of-thought battery (48 harder logic items, prereg frozen before measurement, H-BETTER-REASONING **confirmed**):

- **No chain** (84.5% of the original logic battery): depth buys only rounds. d1's trace is already maximal-quality; everything after is idle re-confirmation.
- **Justification chain** (multi-premise): depth buys longer *correct* chains without changing the verdict — d1 is right but leaves contenders alive; deeper runs perform the eliminations that complete the justification.
- **Decision chain** (3-hop kill chains, misleading prefixes): depth buys the verdict itself — accuracy 0.333 → 1.000, saturating at d8.

Structural fact verified in the harness: deeper traces are strict prefix-extensions of the natural trace — "eliminate earlier" is impossible by construction; depth only adds tail, and the metrics measured whether the tail is chain or theater. The ceiling battery adds the symmetric result: depth *hurts* iff the tail is misleading (O: 1.00 → 0.00).

**Verdict:** depth strengthens reasoning on multi-hop elimination chains, misleading-prefix overturns, and sub-threshold accumulation; it is confidence theater on single-premise anchored items and actively harmful on misleading-tail streams. This is mechanism, not curve-fitting.

## 6. Traces: the mechanism is visible

Three legible round-by-round traces in `h5_resolution/traces/TRACES_H5.md`: TRAP-C6-001 at d1/d4/d8 (six +100 misleading premises front-loaded, the +500/−500 falsification premise arrives at round 7), the same item under adaptive (§6 never fires — confidence moves 100 points every round until evidence exhaustion), and an admit item where §6 fired for real (elimination at round 4 pins confidence at 1000, three zero-gain rounds, five evidence items never read, zero accuracy cost). Every row is from the frozen sweep records, margins cross-checked against the ledgers.

## 7. ADAPTIVE-WINS stands — scoped to the frozen distribution

Prereg-valid and uncontested on the original five batteries: adaptive matches deep-16 everywhere (877/877) with 54%/34%/12% fewer rounds on admit/revoke/cost. The ceiling battery does not repeal it — it scopes it: on plateau-then-flip streams the §6 *rule* specifically fails (0.000 on P), which is the bound-promotion story in §3, not an ADAPTIVE-WINS repeal. The verdict stands where it was measured.

---

## What needs Micah's signature

- **Nothing.** All promotion conditions in this verdict were pre-committed before measurement; the measurements fired or failed them mechanically. The ceiling work ran under a new prereg (H5B), not an amendment to the frozen H5 prereg. Sensor recalibration, when designed, will need its own prereg approval — flagged, not requested.
