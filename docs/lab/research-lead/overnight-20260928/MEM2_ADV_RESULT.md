# H-MEM2 Red Team: Adversary Report (X-M2-1..X-M2-4)

**Date:** 2026-09-29
**Prereg:** PREREG_MEM2_ADV.md (commit 96b699b16, frozen before any attack code)
**Target:** H-MEM2 SURVIVES (5/5), implementation 749590f90
**Method:** Mechanism functions copied verbatim from mem2_learn.zag (lines 1-289);
only main() and ADV_* functions are new. Pure Zag. No Python.
**Determinism:** 3/3 byte-identical runs, md5 3862198707c991f4cc3c16bad9daf56c.

## Verdict: H-MEM2 DOWNGRADED (not killed)

Four downgrade findings. The five frozen K-M2-1..K-M2-5 bars are NOT
retroactively altered (all pass as literally stated); the downgrade narrows
what the bars establish. Three boundary confirmations. One doc/code bug.
Source audit otherwise clean.

## X-M2-1a: ev1 counterfactual misdescribes the mechanism -- DOWNGRADE

Replicated stream A2 to ev1 through the verbatim mechanism and computed both
the protected and unprotected selections:

```
protected selection: LRU
unprotected selection: LRU
selected-policy protected victim: slot6(proc6)
selected-policy unprotected victim: slot6(proc6)
printed counterfactual (unprotected-LFU): slot5(proc8)
selection unchanged by probation
selected-policy victim unchanged by probation
X-M2-1a DOWNGRADE: printed counterfactual misdescribes the mechanism counterfactual
```

Probation changed nothing for the selected policy at ev1. The mechanism
selected LRU with or without protection, and LRU's victim was slot6/proc6
either way (proc8's lastq=56 is newer than proc6's lastq=35, so LRU would not
have touched the newcomer regardless). The printed "[churn counterfactual]
unprotected-LFU victim=slot5(proc8)" describes what a policy the mechanism
did NOT select would have done. The K-M2-1 bar as literally stated passes
(proc8 survives; unprotected-LFU victim is slot5), but the parenthetical
"causal evidence" claim -- "(the churn that would have occurred)" -- is
false for ev1: no churn would have occurred under the mechanism's actual
selection. (ev2 is genuine as preregistered: selected LFU, unprotected
victim slot6/proc9 vs protected slot4/proc4.)

Downgrade: the probation "causal evidence" at ev1 is invalid. Probation's
demonstrated causal effect is confined to ev2.

## X-M2-1b: useless newcomer probe -- INFORMATIONAL (boundary confirmed)

Stored proc8 with zero subsequent queries, then pressured:

```
protected: LFU evicts proc0 cost=0
unprotected: LFU evicts proc8 cost=0
probation cost delta=0
```

Protecting dead weight cost nothing by the replay metric here (the displaced
proc0 was also cold in the recent window). Confirms honest limitation #3
(age-based, not merit-based) without catastrophic cost in this probe. Not a
kill; recorded as boundary.

## X-M2-2a: F-shift "not uniquely worst" bar is vacuous -- DOWNGRADE

Recomputed from the frozen victim sets and futures how many of the 5 policies
satisfy K-M2-2's F-shift criterion (exists another policy with misses >= mine):

```
F-shift vacuity A2: LFU=pass LRU=pass FIFO=pass LIFO=pass RANDOM=pass => 5/5 satisfy bar
F-shift vacuity B2: LFU=pass LRU=pass FIFO=pass LIFO=FAIL RANDOM=pass => 4/5 satisfy bar
F-shift vacuity C2: LFU=pass LRU=pass FIFO=pass LIFO=FAIL RANDOM=pass => 4/5 satisfy bar
```

On A2 F-shift (misses LFU=0 LRU=5 FIFO=0 LIFO=0 RANDOM=5), EVERY policy
satisfies the bar -- it is literally vacuous and cannot distinguish the
selected LFU from an arbitrary choice. On B2/C2, 4 of 5 satisfy it (only the
LIFO outlier fails). The F-shift component of K-M2-2 provides almost no
evidence that the SELECTION is good; any non-LIFO choice would pass.

## X-M2-2b: adversarial future defeats the selection -- INFORMATIONAL

20-query future of all proc5 (the A2-ev0 LFU victim):

```
misses: LFU=20 LRU=0 FIFO=0 LIFO=0 RANDOM=0
X-M2-2b: selected LFU uniquely worst on adversarial future (confirms honest limit #1)
```

Confirms honest limitation #1 as stated in the prereg. Recorded as boundary.

## X-M2-2c: F-trend is the replay proxy relabeled -- DOWNGRADE

Compared per-proc frequencies of each F-trend future against the W=20
selection window it was "proportional" to, computed through the verbatim
mechanism state:

```
F-trend frequency identity A2: IDENTICAL frequencies (F-trend = replay proxy relabeled)
F-trend frequency identity B2: IDENTICAL frequencies (F-trend = replay proxy relabeled)
F-trend frequency identity C2: IDENTICAL frequencies (F-trend = replay proxy relabeled)
```

All three F-trend futures have exactly the same per-proc query frequencies as
the W=20 window the selector minimizes replay cost on (e.g. A2: 0:4, 7:4,
3:4, 6:2, 1:2, 2:2, 5:1, 4:1 in both). The F-trend "misses" are therefore
mathematically identical to the replay costs (confirmed: raw output shows
identical per-policy numbers). F-trend provides ZERO independent validation;
it re-checks the same distribution the selection was optimized on. The
K-M2-2 claim "its selections validate against future queries rather than
only the replay proxy" is false for F-trend. The only non-circular future
evidence is F-shift, whose bar is vacuous/weak per X-M2-2a.

## X-M2-3: strictness is stream-dependent, not a mechanism guarantee -- DOWNGRADE

Novel flat-popularity stream (8 procs, 40 round-robin queries, each proc 5x --
a natural uniform-attention workload):

```
flat: 40 round-robin queries (each proc 5x)
 W=20:LFU~ TIE
 W=25:LFU~ TIE
 W=30:LFU~ TIE
X-M2-3 DOWNGRADE: band not strict on flat stream; strictness is stream-dependent
```

The operating band {20,25,30} -- strict on all three frozen skewed streams --
degenerates to ties on flat popularity. The 5/5 strict selections are a joint
property of (mechanism + researcher-designed skewed streams), not of the
mechanism. The H-MEM downgrade (7/8 tie-break decisions) is repaired on the
frozen streams, but the mechanism does not guarantee strictness; it cannot
produce a strict selection when the workload gives it nothing to discriminate
on. "Selects experience-driven eviction policies strictly" is narrowed to
skewed-popularity regimes.

## X-M2-4: source audit

(a) Mechanism matches prereg: PROB=10 (line 33), prot_until set at store
(line 75), elig() skips protected iff use_prot=1, RANDOM k=(ev*5+1)%neligible
over eligible slots in slot order (line 122), fut_score and band_check
semantics as frozen. PASS.

(b) No test-answer literals (proc5/6/8/9/10) in mechanism functions
(lines 1-289). Stream/future literals live in main() only. PASS.

(c) DOC BUG: the prereg states "If every stored slot were protected
(pathological), selection falls back to unprotected choice and reports it."
This fallback is NOT implemented. victim() returns -1 when no slot is
eligible; replay_cost() maps -1 to 999999; there is no unprotected-fallback
path and no report. The documented behavior does not exist in code. (Not
triggered by the frozen streams; a latent doc/code mismatch.)

(d) MEM2_RESULT.md sweep table vs MEM2_RAW_OUTPUT.txt: verified identical
via grep (C2-ev0 W=35:FIFO* in both). No transcription error. PASS.

## Revised classification

Bounded L2 experience-driven policy selection with newcomer protection, on
researcher-designed skewed-popularity streams, with the following narrowed
readings:

1. Probation's causal evidence is valid at ev2 only; the ev1 counterfactual
   compares against a non-selected policy.
2. Held-out future validation is circular for F-trend (identical frequency
   distribution to the selection window) and vacuous/weak for F-shift (5/5
   and 4/5 policies pass the bar). The "goal vs proxy" distinction does not
   survive: F-trend IS the proxy, and F-shift's bar cannot tell the selected
   policy from an arbitrary one.
3. Strictness (5/5) holds on the frozen streams but is not a mechanism
   guarantee; flat workloads degenerate to ties.
4. The all-protected fallback described in the prereg is unimplemented.

What stands: 5/5 frozen bars pass as stated; probation mechanically protects
newcomers (ev2 causal); the band {20,25,30} is genuinely wider than H-MEM's
point; re-selection flips LFU->LRU->LFU are strict and experience-driven;
determinism holds.

## Artifacts (adversary-owned only)

- mem2_adv.zag (mechanism verbatim lines 1-289 from mem2_learn.zag; ADV_*
  functions and main() new)
- MEM2_ADV_RAW.txt (authoritative; md5 3862198707c991f4cc3c16bad9daf56c)
- MEM2_ADV_RESULT.md (this file)
- PREREG_MEM2_ADV.md (frozen at 96b699b16 before implementation)

Pure Zag. No Python. Commit order valid (prereg strictly precedes result).
