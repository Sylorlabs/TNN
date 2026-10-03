# PREREG V2 (AMENDMENT): BOUNDED-PIN-LIFETIME corrected derivations

Frozen 2026-10-03, after the v1 execution. This is a TRANSPARENT
AMENDMENT to the v1 prereg (committed alone as aaf3fb037). It does not
alter the v1 record: REPORT.md retains VERDICT=FAIL (K3, K4 miss) as
the immutable outcome of the v1 bars. This document names the two
derivation errors, re-derives the TTL predictions from the UNCHANGED
frozen mechanism spec, and re-freezes the corrected kill bars K3' and
K4'. K1, K2, K5, K6, K7, K8 are unchanged from v1. No mechanism code
changes: bounded_pin.zag already implements the spec below; the v2 run
is a fresh 3x execution of the same frozen binary against the
corrected bars.

Why this amendment is legitimate (and not moving goalposts): the v1
K3/K4 bars were falsified by the v1 run, and the failure analysis
identified ARITHMETIC errors in the prereg's hand-trace, not a
post-hoc preference for an outcome. The corrected predictions are
derived here from the frozen spec alone (pin semantics as written in
PREREG.md v1: clock ticks on placement only; reclaim scan is first
slot index s=0..31 with clock-created >= N), and each corrected value
is accompanied by its derivation. The amendment sharpens rather than
softens the bars: K3' predicts an exact non-FIFO partial outcome
(ret=42, rawA=25) that the v1 K3 explicitly ruled out, and K4'
predicts exact PINR-equivalence where v1 predicted partial
reclamation. A reader can check every number below against the spec
without trusting the v1 output.

## The two derivation errors (v1)

Error 1 (killed K4): the v1 trace assumed the pin clock advances on
every relocation ("churn relocation r decides at clock 19+r"). The
frozen spec says the clock is "incremented on every pool placement".
Drops perform no placement, so the clock FREEZES during drop runs.
At N=50, after the 12 churn fills the clock stands at 32; every
subsequent relocation finds max age 32 < 50 and drops, so the clock
never advances and no pin ever expires. TTL50 is behaviorally
identical to unbounded pinning. (N=100 was predicted correctly only
because its horizon argument did not depend on the clock model.)

Error 2 (killed K4 no, killed K3): the v1 trace assumed the
first-expired scan evicts in age order (oldest first), degenerating to
FIFO. The frozen spec says "scan slots s=0..31 for the first used
slot" with clock-created >= N: it is SLOT-INDEX order, not age order.
At N=10, after benign slots 0..9 are evicted (relocs 13..22), the
refilled churn entries in slots 0..9 re-expire (age hits exactly 10)
before the scan reaches the still-expired benign slots 10..19, so
slots 0..9 recycle as a churn buffer and benign slots 10..19 are
never reached. The eviction/drop counts matched v1 (28/0, 48/0); the
retention outcome did not (ret=42, rawA=25, not 0/15).

## Corrected derivations (from the frozen spec)

Setup (both doses): 20 benign placements (ticks 0..19, clock=20),
12 churn fills (ticks 20..31, clock=32), pool full. Benign victims in
slots 0..19 (B's writes i=1..10, slot 2(i-1)/2(i-1)+1), churn fills in
slots 20..31.

N=10, M2 (40 churn relocs):
- Relocs 13..22 (clocks 32..41): evict benign slots 0..9 in index
  order (slot j created j, age 32 >= 10). 10 evictions. Clock=42.
  Slots 0..9 now hold churn (created 32..41).
- Reloc 23 (clock 42): slot 0 (created 32, age 10 >= 10) evicted;
  benign slots 10..19 (ages 32..23, all >= 10) are expired but at
  higher indices, never reached. Place tick 42. Clock=43.
- Relocs 24..32 (clocks 43..51): evict slots 1..9 (created 33..41,
  age 10 each). 10 evictions. Clock=52.
- Relocs 33..40 (clocks 52..59): evict slots 0..7 (created 42..49,
  age 10 each). 8 evictions. Clock=60.
- Totals: 12 fills + 28 evictions = 40. ev=28, drop=0.
- Benign survivors: slots 10..19 (i=6..10). post: 5 owner-1 pairs +
  5 owner-2 triples + 0 guards + 5 owner-8 singles = 15.
  ret=100*15/35=42. rawA=5+5+10+5=25. cf=60, bacc=20.

N=10, M3 (60 churn relocs):
- Relocs 13..22: evict benign slots 0..9. 10 evictions. Clock=42.
- Relocs 23..52 (30 relocs, clocks 42..71): slots 0..9 recycle; each
  is re-evicted exactly 10 ticks after placement (age hits 10), so the
  scan never advances past slot 9. 30 evictions. Clock=72.
- Relocs 53..60 (8 relocs, clocks 72..79): evict slots 0..7.
  8 evictions. Clock=80.
- Totals: 12 + 48 evictions = 60. ev=48, drop=0. post=15, ret=42,
  rawA=25, cf=80, bacc=20.

N=50 and N=100, M2/M3:
- Relocs 1..12: fills, clock=32.
- Reloc 13 (clock 32): max age over the pool is 32 (slot 0) < N, so
  no slot is expired -> drop. Drops do not tick the clock.
- Relocs 14..40 (M2) / 14..60 (M3): clock frozen at 32, ages frozen,
  nothing ever expires -> all drop.
- ev=0, drop=28 (M2) / 48 (M3), ret=100, post=35, rawA=35.
  Bit-identical to PINR.

Sharp thresholds (derived, not all tested; the N=20 case is a
follow-up prediction, not kill-barred):
- Shielding threshold N<=10: slot 0, re-placed at tick 32, re-expires
  at tick 32+N; the scan returns to slot 0 at reloc 23 (clock 42).
  Shielding holds iff 32+N <= 42, i.e. N<=10: the low slots recycle
  and benign slots 10..19 survive (ret=42, drop=0).
- 10<N<=32: the refilled slots cannot re-expire before the scan
  passes them; relocs 23..32 evict benign slots 10..19 (each age
  exactly 32 at eviction >= N), so all 20 benign are evicted
  (ret=0, drop=0; exact FIFO footprint).
- Freeze threshold N>32: max achievable age is 32 (clock at first
  pool-full), so nothing ever expires (identical to unbounded).

## Corrected kill bars (v2)

- K1 BASELINE: unchanged (pre==35 and bacc==20 in all 10). VOID on
  failure.
- K2 PINR-REPRO: unchanged.
- K3' TTL10-SHIELDED-PARTIAL (replaces K3): TTL10-M2: post==15,
  ret==42, evict==28, drop==0, rawA==25, conflicts==60. TTL10-M3:
  post==15, ret==42, evict==48, drop==0, rawA==25, conflicts==80.
  Bounded lifetime at N=10 does NOT degenerate to FIFO: the
  slot-index scan recycles the low slots as a churn buffer and half
  the benign victims survive. Capacity fully restored (drop=0),
  robustness partially lost (ret=42).
- K4' TTL50-FROZEN-EQUIV (replaces K4): TTL50-M2 and TTL50-M3 equal
  the PINR rows exactly: ret==[100,100], evict==[0,0], drop==[28,48],
  rawA==[35,35]. N beyond the freeze threshold (32) is behaviorally
  unbounded pinning: the clock cannot advance past 32 once drops
  begin.
- K5 TTL100-NORECLAIM-EQUIV: unchanged.
- K6 UNPIN-PARTIAL: unchanged (held exactly in v1).
- K7 ADV-FIXED: unchanged.
- K8 DETERMINISM: 3/3 byte-identical sha256 on the fresh v2 run.
  VOID on failure.

Verdict v2: PASS iff K1, K2, K3', K4', K5, K6, K7, K8 all hold. Any
miss names the bar and yields FAIL. Thresholds are frozen at the
values above; they are not moved after the v2 run.

Discrimination (v2): K3' vs K2 separates the shielded-partial regime
from unbounded (ret 42 vs 100, drop 0 vs 28); K3' vs the v1 K3 shows
the exact-FIFO prediction was wrong in the sharpest way (ret=42 not
0). K4' vs K3' separates the frozen regime from the recycling regime
on both retention and reclamation. K6 vs K3'/K4' keeps the unpin
mechanism off the TTL frontier: it alone pairs ret=100 with
drop<28/48. The three tested N values (10/50/100) now discriminate
three behaviors (partial recycle / frozen-unbounded /
beyond-horizon-unbounded) instead of the v1's imagined smooth
frontier.

## Answers to the parent questions (v2)

Does bounded lifetime restore capacity without losing robustness? No.
The measured N landscape is three sharp regimes, not a tunable
frontier: N<=10 restores capacity (drop=0) but loses 58 points of
retention (ret=42); N>32 keeps ret=100 but reclaims nothing
(drop=28/48, identical to unbounded). No N achieves ret=100 with
drop=0, because any expiry bound that can reclaim churn history
either also reaches benign history (slot-index order) or never fires
(clock freeze).

What is the optimal N? There is no dominant N on the TTL frontier;
"optimal" is a regime choice. Among tested N, N=10 is the only one
that reclaims anything (drop=0 at ret=42). On retention, the explicit
unpin arm dominates every TTL setting (ret=100, drop=17/43). The
derived-but-untested 10<N<=32 regime (exact FIFO collapse) suggests
N=20 as the sharp follow-up.

## Commit order (v2)

PREREG_V2.md (this file) commits alone, strictly before the v2 run.
The v2 run re-executes the frozen bounded_pin.zag binary 3x; no
source changes. REPORT_V2.md records the v2 verdict.
