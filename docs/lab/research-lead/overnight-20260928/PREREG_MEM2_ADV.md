# PREREG: H-MEM2 Red Team (X-M2-1..X-M2-4) -- FROZEN

**Date:** 2026-09-29
**Status:** FROZEN (committed before any attack code is written or executed)
**Target:** H-MEM2 SURVIVES (5/5), commits d926eb0f6 (prereg), 749590f90 (result)
**Method:** Assume the H-MEM2 claim is false. Attack in pure Zag. Mechanism
functions copied verbatim from mem2_learn.zag; only main() replaced.
Deterministic 3/3 required for empirical attacks.

## Attack X-M2-1: Probation causal evidence (ev1 counterfactual)

The K-M2-1 bar prints "[churn counterfactual] unprotected-LFU victim" as
"causal evidence" that probation prevented churn. But the SELECTED policy at
A2-ev1 was LRU, not LFU. The printed counterfactual compares against a policy
the mechanism did not select.

**Procedure:** Replicate stream A2 to ev1. Compute the protected selection
(identical to pressure()) and the unprotected selection (select_win with
use_prot=0 for every policy). For the protected-selected policy, compare its
protected victim vs its unprotected victim.

**Kill criterion (DOWNGRADE):** If the unprotected selection still selects
LRU at A2-ev1 (so the mechanism's outcome is unchanged) AND the selected
policy's unprotected victim is not the newcomer proc8, then the printed
"churn counterfactual" does not describe what the mechanism would have done.
The K-M2-1 bar as literally stated still passes, but the "causal evidence"
interpretation is narrowed: probation changed nothing for the selected
policy at ev1. (ev2 is expected to be genuine: selected LFU, unprotected
victim slot6/proc9 differs from protected slot4/proc4.)

**X-M2-1b (useless newcomer, informational):** Stream with 7 hot procs and
one newcomer stored then never queried. Pressure with and without probation.
Quantify the replay-cost penalty of protecting dead weight. Expected to
confirm honest limitation #3 (age-based, not merit-based); recorded as
boundary, not kill.

## Attack X-M2-2: Future-validation bars

**X-M2-2a (F-shift vacuity).** For each frozen F-shift future, count how many
of the 5 policies satisfy "not uniquely worst" (exists another policy with
misses >= mine), computed from the frozen victim sets and futures.

**Kill criterion (DOWNGRADE of K-M2-2's F-shift component):** If on any
F-shift future all 5 policies (or 4 of 5) satisfy "not uniquely worst," the
bar has no discriminating power there: it cannot distinguish the selected
policy from an arbitrary choice. Hand computation from MEM2_RAW_OUTPUT:
A2 F-shift misses are LFU=0 LRU=5 FIFO=0 LIFO=0 RANDOM=5, so all 5 satisfy
the bar (vacuous). The harness recomputes this from the mechanism.

**X-M2-2b (adversarial future, informational).** 20-query future of all
proc5 (the A2-ev0 LFU victim). Score all 5 policies' misses. Expected: LFU
uniquely worst, defeating the selection. This confirms honest limitation #1
(adversarial futures defeat any replay selection); recorded as boundary.

**X-M2-2c (F-trend circularity, informational).** F-trend futures are
"proportional to the W=20 window," the same distribution the selector
minimizes replay cost on. Compute per-policy replay costs (W=20) vs F-trend
misses and report rank agreement. Expected: argmin coincides by
construction; F-trend adds little beyond the replay proxy. Recorded as
narrowing of "validates against future queries rather than only the replay
proxy."

## Attack X-M2-3: Window band generality

The 5/5 strictness and band stability were verified on researcher-designed
skewed-popularity streams. Test whether the mechanism alone guarantees
strictness.

**Procedure:** Novel stream, flat popularity: 8 procs learned, then 40
queries round-robin (each proc 5x). Run band_check {20,25,30} and the sweep.

**Kill criterion (DOWNGRADE of generality, not of frozen bars):** If the
band on the flat stream yields ties (no strict winner) at any W in
{20,25,30}, then strictness is a joint property of (mechanism + skewed
stream), not of the mechanism. The frozen 5/5 stand, but "selects
experience-driven eviction policies strictly" is narrowed to
skewed-popularity regimes. (A flat stream is a natural workload, e.g. scan
with uniform attention.)

## Attack X-M2-4: Source audit

(a) Verify mechanism functions match the prereg: PROB=10, prot_until set at
store, elig() skips protected iff use_prot=1, RANDOM k=(ev*5+1)%neligible
over eligible in slot order, fut_score semantics, band_check {20,25,30}
strict-and-equal.
(b) No test-answer literals in mechanism functions (victim, replay_cost,
select_win, is_strict, elig, nelig, st_learn, st_query, fut_score,
band_check, sweep_print, pressure): grep for proc-id constants in those
functions; stream/future literals live in main() only.
(c) The prereg claims "If every stored slot were protected (pathological),
selection falls back to unprotected choice and reports it." Verify whether
this fallback exists in code. Kill criterion (DOC BUG): if absent, the
documented behavior is unimplemented.
(d) MEM2_RESULT.md sweep table vs MEM2_RAW_OUTPUT.txt: raw shows C2-ev0
W=35:FIFO*; the result doc's table shows W=35:LFU~. Flag the transcription
error against the authoritative raw output.

## Verdict rule

H-MEM2 is KILLED only if a frozen bar's stated outcome is falsified.
DOWNGRADED if any X-M2-1, X-M2-2a, or X-M2-3 kill criterion is met (claim
narrowed, bars intact). X-M2-1b, X-M2-2b, X-M2-2c are boundary confirmations.
X-M2-4 findings are reported as doc/code bugs as found.

## Deliverables

- mem2_adv.zag (mechanism verbatim, new main)
- MEM2_ADV_RAW.txt (3/3 byte-identical runs)
- MEM2_ADV_RESULT.md (verdict per attack)
- This prereg (frozen before implementation)

Pure Zag. No Python.
