# MEM4_RESULT: H-MEM4 Repair of H-MEM3 Red-Team Downgrades

**Date:** 2026-09-29
**Verdict: H-MEM4 SURVIVES (5/5 kill bars).**
**Frozen prereg:** `PREREG_MEM4.md` (commit `3f638bd37`), strictly before
implementation (verified via `git merge-base --is-ancestor`). No amendments.
**Raw evidence:** `MEM4_RAW_OUTPUT.txt` (md5
`7921b0f4bc917d9ccb3627aa41d1ca97`, 3 runs byte-identical via cmp)
**Implementation:** `mem4_learn.zag` (deltas vs `mem3_learn.zag` confined to
R1-R3; `mem3_learn.zag` unmodified)
**Pure Zag. No Python in fixtures, harness, build, execution, or analysis.**
One mechanical text substitution during file editing used Python via exec
(equivalent to sed, on non-research file text); disclosed here. No research
content, expectation, or evidence was produced or altered with Python.

## What was repaired

**R1 (X-M3-1a): full winner-recomputation counterfactual.** `pressure()`
now calls `churn_verdict()`, which recomputes the winner under no
protection (wun = argmin_pol(...,0)) and compares it against the protected
winner (wprot) and their victims (vprot, vun). The verdict is CHURN-FULL:1
iff the winner or the eviction differs, CHURN-FULL:0 iff the winner is
stable and the eviction is unchanged. Both winners and both evictions are
printed. The old selected-policy-only verdict is superseded; its victim
pair is retained as a printed detail line for K-M3-1 continuity. The X-M3-1a
scope gap (verdict :0 while the outcome changed) is closed by construction:
any winner flip or eviction change forces a :1 verdict that names both
winners and both evictions.

**R2 (X-M3-1b): merit-gated probation.** `elig()` now voids age protection
for meritless slots past a short absolute grace. Precisely: for a stored
slot with protection enabled, age = st_seq(ST) - (st_prot(W,s) - PROB())
(queries since the slot was learned). If age < GRACE (3), the slot is
protected. Else, if still within the age window, the slot is protected iff
uses > 0; a meritless slot is eligible. On the X-M3-1b fixture the
never-queried newcomer (proc8, uses=0, age=9) is evictable, the mechanism
evicts it at replay cost 0, and the queried procedure (proc0, uses=6)
survives. Newcomers that demonstrate merit stay protected (K-M3-1 survivor
checks retained and passing).

**R3 (X-M3-2a/b): stronger future independence plus explicit
adversarial-target screen.** New `l1_dist()` computes the L1 distance
between the future's and the W=20 window's per-proc frequency vectors; new
`dist_differs2()` requires L1 >= L1MIN (6). The old `dist_differs()` passed
a single-query flip (L1=2); the new check rejects it. New `fut_score3()`
first screens for ADVERSARIAL-TARGET: if the selected policy's victim proc
is a strict majority of the future, the future is explicitly excluded
(return 2) with a printed diagnosis naming the targeted proc, rather than
silently failing the bar. Robustness against adversarial futures is not
claimed; explicit detection is. The old `dist_differs()`/`fut_score2()` are
retained in source for the low-bar demonstration and regression.

## Kill bar results

- **K-M4-1 (full counterfactual honesty): PASS.**
  (a) On the X-M3-1 fixture at ev1 pre-pressure: wprot=LFU, wun=LFU,
  vprot=slot7, vun=slot7, cprot=0. Merit-gating voided proc8's age
  protection (uses=0, age=9 > GRACE), so the protected and unprotected
  eligible sets coincide and the winner is genuinely stable. The printed
  verdict is `CHURN-FULL:0 (winner stable at LFU; eviction unchanged)`,
  and its natural reading ("probation changed nothing") is now true at
  the outcome level. The old scope gap cannot recur: any flip forces :1.
  (b) On the synthetic flip fixture: wprot=FIFO, vprot=slot0, wun=LFU,
  vun=slot7, churn_verdict returns 1, and the print reads
  `CHURN-FULL:1 (winner flips FIFO->LFU; eviction slot0(proc0)->slot7(proc7))`.
  The flip arithmetic was hand-derived in the prereg and confirmed by the
  frozen run: protected costs LFU=10/LRU=10/FIFO=5/LIFO=5/RANDOM=10
  (FIFO wins tie-break), unprotected costs LFU=0/LRU=0/FIFO=5/LIFO=0/
  RANDOM=0 (LFU wins tie-break).
- **K-M4-2 (merit-based probation): PASS.** On the X-M3-1 fixture at ev1:
  selected LFU evicts slot7(proc8, uses=0) at replay cost 0;
  has_proc(8)==0 (meritless newcomer evicted), has_proc(0)==1 (queried
  procedure survives), has_proc(9)==1 (newcomer stored). The X-M3-1b harm
  (cost 0 -> 2 to shield a never-queried newcomer) does not occur.
- **K-M4-3 (adversarial future explicit): PASS.**
  (a) On the X-M3-2a fixture: selected=LFU, victim proc=5, fut_score3
  returns 2 and prints `[ADVERSARIAL-TARGET: proc5=20/20 targets selected
  LFU victim]` with `K-M4-3 EXCLUDED`. The disclosed limitation is now
  machine-detected rather than silently failed.
  (b) Single-query flip: dist_differs (old)=1 (the low bar still passes,
  demonstrating X-M3-2b), dist_differs2 (new)=0 (L1=2 < 6, rejected).
- **K-M4-4 (preserved bars): PASS.**
  K-M3-1: A2 ev1 winner LRU, slot6(proc6)/slot6(proc6), proc8 survives;
  A2 ev2 winner LFU, slot4(proc4)/slot6(proc9), proc9 survives.
  K-M3-2: 6/6 PASS under strengthened fut_score3 (L1 values
  14,14,12,8,16,16, all >= 6; selected holds the minimum on all six;
  n_tying_min=1 of 5 throughout). K-M2-3: 5/5 strict selections.
  K-M2-5: band {20,25,30} agrees and is strict at A2 (LFU), B2 (LRU),
  C2 (FIFO). Flat fixture reports TIE on all three windows. K-M3-4:
  FALLBACK-ALL-PROTECTED emitted, fallback flag set, unprotected LFU
  selected (victim slot0/proc0), proc8 stored, no crash.
- **K-M4-5 (deterministic): PASS.** Three consecutive runs byte-identical
  (md5 `7921b0f4bc917d9ccb3627aa41d1ca97`).

FAIL lines in raw output: 0. `ALL BARS PASS` printed, exit code 0.

## Trace excerpts (from MEM4_RAW_OUTPUT.txt, verbatim)

```
pressure event 1 (learn proc9, win=20):
    LFU victim=slot7(proc8) cost=0
    ...
  selected: LFU cost=0 TIE
  evict slot7 proc8 uses=0 lastq=0
  [full counterfactual] protected: LFU victim=slot7(proc8) | unprotected: LFU victim=slot7(proc8)
  [selected-policy] protected-victim=slot7 unprotected-victim=slot7
  CHURN-FULL:0 (winner stable at LFU; eviction unchanged)
  stored proc9 at slot7 prot_until=56
K-M4-2 PASS: meritless newcomer evicted at cost 0; queried procedure survives
```

```
  [full counterfactual] protected: FIFO victim=slot0(proc0) | unprotected: LFU victim=slot7(proc7)
  [selected-policy] protected-victim=slot0 unprotected-victim=slot0
  CHURN-FULL:1 (winner flips FIFO->LFU; eviction slot0(proc0)->slot7(proc7))
K-M4-1b PASS: CHURN-FULL:1 honestly reports winner flips FIFO->LFU, eviction slot0(proc0)->slot7(proc7)
```

```
held-out A2 F-ADV [ADVERSARIAL-TARGET: proc5=20/20 targets selected LFU victim]
K-M4-3 EXCLUDED (A2 F-ADV: adversarial target, out of bar scope)
K-M4-3a PASS: adversarial future explicitly detected and excluded
```

```
pressure event 2 (learn proc10, win=20):
  [full counterfactual] protected: LFU victim=slot4(proc4) | unprotected: LFU victim=slot6(proc9)
  CHURN-FULL:1 (winner stable at LFU; eviction slot4(proc4)->slot6(proc9))
```

Note the A2-ev2 line: the winner is stable (LFU both ways) but the
eviction differs, so the verdict is honestly :1 with "winner stable at
LFU" rather than a flip. This is the precision R1 adds over the old
selected-policy verdict.

## Causal interpretation

R1: The verdict now answers the outcome-level question ("would the
eviction have differed without protection?") instead of the
selected-policy question ("would the selected policy's victim have
differed?"). On the X-M3-1 fixture the two questions now agree (winner
stable), and on the synthetic flip they disagree and the verdict reports
the disagreement explicitly. The X-M3-1a natural-reading gap is closed.

R2: Probation now tracks demonstrated merit (uses>0) after a short grace,
instead of age alone. The X-M3-1b harm case is repaired at the mechanism
level: the meritless newcomer is evicted at cost 0 rather than shielded
at cost 2. The repair preserves H-MEM's core value (newcomer protection):
a newcomer queried within GRACE keeps protection via the merit tier, and
all builder-stream outcomes are unchanged (every age-protected slot on
those streams is merit-positive or in grace).

R3: The independence check now has teeth (L1>=6 rejects near-duplicates)
and the adversarial future is diagnosed, not hidden. The selection itself
remains replay-based and therefore still vulnerable to adversarial
futures; the honest claim is detection and exclusion, not robustness.

## Classification

Bounded L2 experience-driven policy selection with merit-gated newcomer
protection, outcome-level churn verdicts, and explicit adversarial-future
detection, on researcher-designed skewed-popularity streams. Explicitly
not L3, not policy-form invention. The four H-MEM3 downgrade findings are
repaired; no frozen H-MEM3 bar changed truth value.

## Remaining limits (honest)

1. Menu, window band, and probation constants (PROB=10, GRACE=3, L1MIN=6,
   strict-majority target threshold) are authored; what is
   experience-driven is which menu item wins, when, and the re-selection
   flips.
2. Futures are researcher-frozen and non-adversarial; adversarial futures
   are detected and excluded, not defeated. Robustness is not claimed.
3. Probation is merit-gated with a short grace: a newcomer that would earn
   its first query after GRACE queries but before PROB can still churn.
   The harm window is bounded by GRACE, not eliminated.
4. Strictness holds on skewed regimes; flat workloads tie (demonstrated).
5. The adversarial-target screen uses a strict-majority threshold; a
   future punishing the victim proc at below-majority mass is not flagged.
6. Not yet integrated into the unified learner.
7. The st_query silent-discard property (queries for absent procedures are
   dropped; noted in ADV_MEM3_RESULT.md as untested) is unchanged.

## Lineage

- H-MEM (SURVIVES WITH DOWNGRADE): baseline; newcomer churn, tie-break
  selections, load-bearing window, proxy-only bars.
- H-MEM2 (SURVIVES WITH DOWNGRADE): probation, interleaved queries,
  held-out futures, window band; downgraded on counterfactual honesty,
  future circularity/vacuity, stream-dependent strictness, unimplemented
  fallback.
- H-MEM3 (SURVIVES WITH DOWNGRADE): selected-policy counterfactual,
  implemented fallback, machine-checked independence, stronger future bar,
  scoped strictness; downgraded on counterfactual scope gap (X-M3-1a),
  probation harm (X-M3-1b), adversarial-future vulnerability (X-M3-2a),
  low independence bar (X-M3-2b).
- H-MEM4 supersedes H-MEM3 as the memory-policy layer. The K-M3-1 verdict
  strings are SUPERSEDED by CHURN-FULL (values retained); K-M3-2 is
  retained in strengthened form (fut_score3); K-M2-3, K-M2-5, K-M3-4 are
  retained unchanged. Supersessions are not retroactive: H-MEM3's frozen
  verdicts stand as executed.

## Governance

- Prereg `3f638bd37` strictly precedes implementation (merge-base
  verified). No amendments.
- Mechanism deltas, fixture tables, and flip-state arithmetic were
  hand-derived, then validated in /tmp scratch (pure Zag, never committed)
  before the prereg freeze; scratch output is not evidence. The frozen run
  reproduced every prereg expectation exactly.
- Only H-MEM4-owned files staged/committed (PREREG_MEM4.md,
  mem4_learn.zag, MEM4_RAW_OUTPUT.txt, MEM4_RESULT.md). Concurrent
  workers' files (iu4_adversary staged entries, untracked binaries) were
  not touched; broad git add was never used.
- No Python in fixtures, harness, build, execution, or analysis. One
  mechanical text substitution during file editing used Python via exec
  (sed-equivalent on non-research text); disclosed here. No research
  content was produced or altered with it.
- No em dashes in loop documentation (checked).
- Negative evidence preserved: the old dist_differs low bar is
  demonstrated still passing (K-M4-3b) rather than hidden; the A2-ev2
  winner-stable-but-eviction-differs case is reported verbatim rather
  than simplified.
- Determinism: znc 2026.07.0-dev; harness fully deterministic; 3/3
  byte-identical with md5 7921b0f4bc917d9ccb3627aa41d1ca97.
- All commits local on tnn-native-lab; no push authorized or attempted.
