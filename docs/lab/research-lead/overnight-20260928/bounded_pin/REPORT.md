# REPORT: BOUNDED-PIN-LIFETIME comparison (v1 execution)

Date: 2026-10-03. Worker: BOUNDED-PIN-LIFETIME worker (non-ledger task).
Prereg: committed alone as aaf3fb037 (strictly before implementation).
Implementation: bounded_pin.zag (pure Zag), built with the pinned
compiler via safebin znc (`znc 2026.07.0-dev (edition 2026)`), exit 0,
only the benign zagd-unavailable notice.

## Verdict: FAIL (K3, K4 miss)

K1, K2, K5, K6, K7, K8 hold. K3 and K4 miss. 3/3 runs byte-identical
(sha256 6e93317bf1bc4f404e2ad2545c315c16be010c6bb1c2fcb7c0600d5d244a14b4).
The misses are derivation errors in the prereg's hand-trace, not
mechanism defects: the implementation faithfully executes the frozen
pin semantics, and a debug-instrumented build confirms the actual
dynamics. Root-cause analysis below; a transparent amendment with
corrected derivations is filed separately as PREREG_V2.md (it does
not alter this record).

## Results (identical across run1/run2/run3)

| cond     | pol | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|-----|------|-----|----|----|------|------|------|
| PINR-M2  | 3   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| PINR-M3  | 3   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| TTL10-M2 | 4   | 35  | 15   | 42  | 60 | 28 | 0    | 20   | 25   |
| TTL10-M3 | 4   | 35  | 15   | 42  | 80 | 48 | 0    | 20   | 25   |
| TTL50-M2 | 5   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| TTL50-M3 | 5   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| TTL100-M2| 6   | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| TTL100-M3| 6   | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |
| UNPIN-M2 | 7   | 35  | 35   | 100 | 60 | 11 | 17   | 20   | 35   |
| UNPIN-M3 | 7   | 35  | 35   | 100 | 80 | 5  | 43   | 20   | 35   |

Kill bars:
- K1 BASELINE: pre==35 and bacc==20 in all 10 -> PASS
- K2 PINR-REPRO: PINR rows match the frozen MULTI-OWNER-CHURN PIN rows
  (ret=[100,100], ev=[0,0], drop=[28,48]) -> PASS
- K3 TTL10-FIFO-EQUIV: need ret=[0,0], ev=[28,48], drop=[0,0],
  rawA=[15,15]; got ret=[42,42], rawA=[25,25] -> FAIL
- K4 TTL50-PARTIAL: need M2 (post,ret,ev,drop,rawA)=(20,57,10,18,25)
  and M3 (0,0,30,18,15); got (35,100,0,28,35) and (35,100,0,48,35)
  -> FAIL
- K5 TTL100-NORECLAIM-EQUIV: TTL100 rows == PINR rows exactly -> PASS
- K6 UNPIN-PARTIAL: UNPIN-M2 (100,11,17,35), UNPIN-M3 (100,5,43,35)
  -> PASS (exactly as preregistered)
- K7 ADV-FIXED: cf==60 in all five M2 conditions, cf==80 in all five
  M3 conditions -> PASS
- K8 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Root cause of the K3/K4 misses (derivation errors, not code defects)

The prereg's frozen pin semantics say: the clock is "incremented on
every pool placement", and the reclaim scan takes "the first used
slot" (s=0..31) with (clock - created) >= N. The implementation does
exactly this (verified by a debug-instrumented build logging every
reclaim decision as (clock, slot, created)). The prereg's DERIVATION
NOTES, however, hand-traced two things wrong:

Error 1 (kills K4): the trace assumed the clock advances on every
relocation ("churn relocation r decides at clock 19+r"). It does not:
drops perform no placement, so the clock FREEZES during drop runs.
At N=50, after the 12 churn fills the clock stands at 32 and every
relocation drops (max age 32 < 50), so the clock never advances and no
pin ever expires. TTL50 is behaviorally identical to unbounded
pinning (ret=100, drop=28/48), not the predicted partial. The same
freeze applies to N=100 (predicted correctly only because the horizon
argument did not depend on the clock model).

Error 2 (kills K3): the trace assumed the first-expired scan evicts
in age order (oldest first), degenerating to FIFO. It does not: the
scan is by slot index. At N=10, after benign slots 0..9 are evicted
(relocs 13..22), the refilled churn entries in slots 0..9 re-expire
(age hits exactly 10) before the scan reaches the still-expired
benign slots 10..19, so slots 0..9 are recycled as a churn buffer and
benign slots 10..19 (i=6..10) are never reached. Result: 10 benign
evicted, 10 survive -> post=15, ret=42, rawA=25, not the predicted
FIFO collapse (ret=0, rawA=15). The eviction/drop counts (28/0,
48/0) matched; only the retention outcome was wrong.

The corrected picture, derived from the frozen spec and confirmed by
the decision log: the N landscape is not the preregistered smooth
Pareto frontier but three sharp regimes. N<=10: the low slots recycle
as a churn buffer and half the benign victims survive (ret=42,
drop=0). 10<N<=32: the buffer cannot re-expire fast enough, all 20
benign are evicted in age order (ret=0, drop=0; exact FIFO footprint,
verified by trace for N=20, untested in this lane). N>32: the clock
freezes at 32 during drops and nothing ever expires (ret=100,
drop=28/48; identical to unbounded). No N achieves ret=100 with
drop=0: the "optimal N" is a regime choice, and on retention the
explicit-unpin arm (K6: ret=100, drop=17/43) dominates every TTL
setting tested.

## What held and what it means

- K2/K5: the substrate is sound. PINR reproduces the parent PIN row
  bit-for-bit, and N=100 reproduces PINR bit-for-bit, so the TTL
  machinery introduces no behavioral drift when pins never expire.
- K6: the unpin prediction held EXACTLY (ev=11/drop=17 in M2,
  ev=5/drop=43 in M3, ret=100 both). Owner-scoped unpin keeps full
  robustness but its capacity restoration is partial and
  dose-sensitive: the unpinned commons is consumed by the
  non-consenting churners (owners 4/8), so the leak persists at 17/43
  vs 28/48. This is the multi-owner generalization of the consent
  caveat, measured rather than narrated.
- K7: the adversary footprint is policy-invariant, so all retention
  differences are policy effects.

## Honest caveats

- The v1 prereg's K3/K4 predictions were wrong; the FAIL verdict
  stands as recorded. The corrected derivations above were
  reconstructed AFTER seeing the results, so they carry less weight
  than a preregistered prediction; PREREG_V2.md re-freezes them as
  explicit v2 bars with the errors named, and the v2 run re-tests
  them.
- The 10<N<=32 regime (full FIFO collapse) is derived, not measured;
  N=20 is the sharp test and belongs to a follow-up prereg.
- The churn adversary is a mechanism stressor, not a sealed world.
  Owner-scoped reads carry over the parent caveat unchanged.
- Per the no-patch-treadmill rule, this lane canonizes no reclamation
  policy and no N value.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked
at any point (shell used only for mkdir, znc, binary execution,
sha256sum, cmp, and file reads/writes; a debug-instrumented copy of
the source was built and run under /tmp for root-cause analysis and
was not committed). One implementation bug was caught and fixed
before any committed run: the first build's reclaim paths omitted the
free-slot fill (every placement dropped). No PROCESS-FAIL condition
triggered. Git writes went through /usr/bin/git directly with
explicit pathspecs; no git reset.

## Commits

- aaf3fb037: frozen prereg v1 (PREREG.md + NAMECHECK.md), alone.
- This commit: bounded_pin.zag, bounded_pin_bin, run1/2/3.txt,
  REPORT.md (v1 VERDICT=FAIL record). Local only, never pushed.
