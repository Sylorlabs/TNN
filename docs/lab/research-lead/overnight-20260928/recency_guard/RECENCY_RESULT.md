# RESULT: Recency-Guarded Earning Experiment (RECENCY-GUARD)

## Verdict: RECENCY-GUARD-CONTAINED

Date: 2026-09-30 PDT.
Prereg: PREREG_RECENCY.md, commit 68c5796d4 (committed alone; K1 verified
below). Implementation: recency_guard.zag in this directory.
Pure Zag, zero Python at every step.

## What changed vs the episodic battery

Identical 3-episode battery (E0 + 3x 30-item waves with inter-wave earning),
except the inter-wave earning rule: earn all surviving flood items (rel 99)
with 2x queries each EXCEPT the highest-subj survivor (the most recent
arrival). The prior wave's door occupant is always the highest-subj flood
survivor, so the rule uses no door knowledge. The eviction policy
(importance formula, FIFO ties) is unchanged; the learner core is carried
over byte-identical from episodic.zag (9c6ee8ba8) except the earning
function and main().

## Kill bars

- K1 (prereg precedence): PASS. `git merge-base --is-ancestor 68c5796d4 HEAD`
  verified after the evidence commit; no implementation file existed in this
  directory before the prereg commit.
- K2 (frozen predictions): PASS. Every frozen prediction matched exactly;
  see the bar-by-bar table below. Verdict per the frozen rule: CONTAINED
  (cumulative sleeper survival 9/10 >= 9/10 AND door-absorption
  EVICT-confirmed in EP2/EP3).
- K3 (purity/determinism): PASS. Pure Zag throughout (build with the pinned
  znc, runs, analysis via shell/grep/awk/sha256sum). 3/3 byte-identical
  runs (sha256 7620e70c8f93d7f85b8e900d4ee30630ac912922ce37129a6bea03258bf462d0),
  exit 0, zero stderr. No em dashes (shell-only check_no_dash.sh clean).
  The compiler emitted 4 non-fatal A0102 analyzer notes (ignored query
  return values), the same disclosed class as the parent builds.

## Bar-by-bar: frozen prediction vs observed

| Bar | Frozen | Observed |
|---|---|---|
| E0_SLEEP | 10/10 | 10/10 |
| E0_EARNED | 10/10 | 10/10 |
| EP1 first eviction | (40,20) | EVICT 40 20 |
| EP1 EVICT victims | (40,20) then 304..328 | exact (26 lines) |
| EP1_SLEEP | 9/10 | 9/10 |
| IW1 survivors / earned | 5 / 4 (329 excluded) | IW1_EARNED 4 |
| IW1_PROBE | 2/2 | 2/2 |
| EP2 first eviction | (329,99) | EVICT 329 99 |
| EP2 EVICT victims | (329,99) then 400..428 | exact (30 lines) |
| EP2 sleeper evictions | 0 | 0 |
| EP2_SLEEP | 9/10 | 9/10 |
| IW2 survivors / earned | 5 / 4 (429 excluded) | IW2_EARNED 4 |
| IW2_PROBE | 2/2 | 2/2 |
| EP3 first eviction | (429,99) | EVICT 429 99 |
| EP3 EVICT victims | (429,99) then 500..528 | exact (30 lines) |
| EP3 sleeper evictions | 0 | 0 |
| EP3_SLEEP | 9/10 | 9/10 |
| IW3 survivors / earned | 5 / 4 (529 excluded) | IW3_EARNED 4 |
| IW3_PROBE_UNPROBED | 3/3 | 3/3 |
| Total EVICT lines | 86 (26+30+30) | 86 |
| FINAL_COMP | 4/4 | 4/4 |
| FINAL_FOUND | 12/12 | 12/12 |
| FINAL_EARNED | 10/10 | 10/10 |
| FOUND_EVICT | 0 | 0 |
| Cumulative sleeper survival | 9/10 | 9/10 |

Comparators: episodic three-wave baseline 7/10; churn single-wave baseline
9/10. The guard restores the single-wave retention level under three
separated waves.

## Mechanism evidence (EVICT log)

Each episode's EVICT sequence confirms the door-absorption mechanism. EP1
opens at the sleeper slot (40,20), then churns the remaining 25 victims
through that same slot (door re-establishes at the sleeper slot, as in
episodic). IW1 earns 300,301,302,303 but NOT 329, leaving the unproven door
occupant at importance 1. EP2's first eviction therefore takes (329,99) --
the prior door occupant, the lowest-index importance-1 slot in scan order --
and the door re-establishes at its slot for the remaining 29 evictions; no
sleeper is touched. IW2/EW3 repeat the pattern with 429 and 529. The bleed
is contained not by changing the eviction policy but by withholding earning
from the most recent arrival, so the revolving door always has an unproven
occupant to sacrifice.

## Lane-closing statement

Adopt the concrete earning discipline: inter-wave (or inter-episode) earning
must skip the most recent arrival. The rule is implementable with no door
knowledge (skip the highest-subj survivor) and, on this battery, restores
9/10 sleeper retention across three separated pressure waves with zero
sleeper evictions in episodes 2-3, zero collateral (foundation 12/12,
Group A 10/10, FOUND_EVICT 0, compositions 4/4). The retention-policy lane
closes here: this was the terminal experiment, and no follow-up variants
are warranted. The remaining honest characterization: the policy protects
demonstrated utility and sacrifices the undemonstrated; the recency guard
extends that protection across episodes by refusing to launder the newest
junk to proven status.

## Files

- NAMECHECK.md, PREREG_RECENCY.md (frozen; committed alone at 68c5796d4)
- recency_guard.zag (implementation)
- recency_guard_bin (built binary, pinned znc)
- RUN1.txt, RUN2.txt, RUN3.txt + .err (raw evidence, 3/3 byte-identical)
- RECENCY_RESULT.md (this file)
- build.err (compiler notes; non-fatal A0102 only)
