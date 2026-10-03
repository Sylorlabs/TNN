# Experiment 2 verdict: one-brain sub-agent dispatch — H1 KILLED by K1

Date: 2026-09-27. Frozen prereg: `PREREG.md` @ `1ab40adceff78d71460b992b078508acea7e8abc`
(frozen before implementation; never amended).

## The question

Micah: can TNN dispatch multiple sub-agents *from the same brain* — sub-deliberations
sharing one ledger/state, then reintegrating into one decision — where the fan-out is
TNN's own machinery, not crew scaffolding?

## What was built and tested

- `impl/onebrain.zag` (1,358 lines, pure Zag, zero RNG): ledger-driven deliberation
  (GEN readings → GEN facts → GEN actions → ELIM → FORK_ASSESS → SUBPASSES → one ARGMAX).
  FORK_ASSESS fires from ledger state alone (≥2 surviving evidence-bearing readings,
  close action-bid margin); two sub-deliberations interleave deterministically over the
  shared ledger; one final ARGMAX. Modes: `single` (no fork), `onebrain`, `ablate`
  (shared-writes-off), `poison` (causal probe), `min` (bare driver).
- `v4/`: 28 frozen ambiguous dialogue problems in the machinery's native action space
  (SHA-256 `e74bfa51…dde6`, frozen before any scoring run). A v3 set targeting
  reading-selection was archived as an integration misfire (wrong output space);
  see `problems_v3/MISFIRE_NOTE.md`.

## Results

| mode     | accuracy |
|----------|----------|
| single   | 14/28 = 50.0% |
| onebrain | 14/28 = 50.0% |
| ablate   | 14/28 = 50.0% |
| min      | 14/28 = 50.0% |

Kill bars: **K1 FIRES** (onebrain does not beat single; ablation matches it exactly).
Of 11 fork-items single got wrong, the fan-out fixed 0. **K2 passes** (poison changed
15/18 fork verdicts — causal cross-talk, purely destructive). **K3 passes** (`min` ≡
`onebrain` byte-identical; fork is the machinery's own decision). **K4 passes weakly**
(3/28 verdicts differ with shared writes off — not decorative, but no accuracy
effect). **K5 passes** (3× byte-identical reruns, all modes). **K6 passes** (no RNG).

## Verdict

**H1 is KILLED by K1, per the frozen prereg.** The ledger-driven fork is genuine
machinery and the ledger is genuinely shared and causal — but fan-out confers no
accuracy benefit, and the observed cross-talk is as often destructive (shared audit
annihilating all candidates → NO_VERDICT, including a self-defeating case where the
forget bid's own reading denies the fact it depends on) as constructive.

## Caveats the red team proved (read before citing this kill)

1. **Weak test power:** only 11/28 items are K1-informative (10 never fork by
   construction; withhold(23) is structurally unfirable; 4 items violate the
   prereg's ≥2-readings spec). Direction on the 11 is unambiguous (0 fixed),
   but the set is thin.
2. **The kill is fragile:** it turns on one unprincipled tie-break in one audit
   rule. A minimal, principled, fully general variant (V4: correction denies the
   least-relevant alive fact; ties broken by fewest dependent bids —
   least-disruptive invalidation) hand-simulates to flip exactly one verdict
   (p08), giving onebrain 15/28 > single 14/28 with ablate at 14/28 — un-firing
   both K1 conjuncts. Hand-simulated only, not run (out of scope under the frozen
   prereg).
3. **Scope:** this kills this implementation's audit vocabulary, not the fan-out
   concept. On 20/28 problems every fired bid shares one supporting fact, so
   denial can only annihilate, never discriminate; the duel channel (the only
   discriminating audit) fired on 2/28 problems.

## Recommended follow-up (new prereg, not an amendment)

Re-test V4-class (least-disruptive invalidation) variants under a fresh prereg:
does a shared ledger whose audits discriminate rather than annihilate give
fan-out a real accuracy benefit? Do not re-run variants against this frozen set
without re-freezing — that would be tuning to the test.
