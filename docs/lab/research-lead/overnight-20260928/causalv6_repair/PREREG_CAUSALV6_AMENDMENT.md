# Preregistration Amendment: H-CAUSALV6 K-CV6-1b (clean re-confirmation)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any K-CV6-1b implementation/run)
**Amends:** PREREG_CAUSALV6.md (K-CV6-1 only; K-CV6-2/3/4 unchanged)
**Researcher:** H-CAUSALV6 Frontier Researcher (subagent)

## Why this amendment exists

K-CV6-1 as frozen used the red team's X-CV5-1 fixture
(cv5_adv_deg_obs.txt). Execution revealed a prereg error in the
hand-derived expectation: the fixture's "support blocks"
[C_k a4 no-op, F_k a3 no-op, E_k a4 s2 0->1] use action a4 for the
EFFECT episode. Under CV5 this was harmless (R0 stayed PROVISIONAL,
so dl_retract_check never ran). Under R6, R0 is correctly
re-CONFIRMED at seq21 (the ratchet IS broken), but the E_2 episode
(a4 at seq21) then becomes a cause for a legitimate R5 refutation
at seq23 (a4 at seq21, s2=0 at seq23). The fixture is internally
contradictory once the rule is ACTIVE; it was designed for a
mechanism where R0 never reactivates.

This is a PREREG ERROR (incorrect hand-derived expectation), not a
mechanism failure. The trace proves the R6b graded re-confirmation
works: `# delay rule R0 CONFIRMED at seq 21 support=3
(provisional -> active)`. K-CV6-1 as written is reported as FAIL.

## K-CV6-1b: clean re-confirmation fixture

New fixture `cv6_clean_reconf_obs.txt` (24 episodes):
- seq1-12: byte-identical to causal3/obs3d.txt (R0=(4,2,s2,1)
  CONFIRMED at seq11, support=2, dl_cs=(0,0,0)).
- seq13: `T 0 0 0 | 4 | 0 0 0` (a4 no-op; refuter cause)
- seq14: `T 0 0 0 | 3 | 0 0 0` (a3 no-op; filler)
- seq15: `T 0 0 0 | 1 | 0 0 0` (a1 no-op; refuter effect; s2=0)
- seq16: `T 0 0 0 | 4 | 0 0 0` (a4 no-op; support cause 1)
- seq17: `T 0 0 0 | 1 | 0 0 0` (a1 no-op; filler)
- seq18: `T 0 0 0 | 3 | 0 0 1` (a3, s2 0->1; support effect 1)
- seq19: `T 0 0 0 | 4 | 0 0 0` (a4 no-op; support cause 2)
- seq20: `T 0 0 0 | 1 | 0 0 0` (a1 no-op; filler)
- seq21: `T 0 0 0 | 3 | 0 0 1` (a3, s2 0->1; support effect 2)
- seq22: `T 0 0 0 | 4 | 0 0 0` (a4 no-op; support cause 3)
- seq23: `T 0 0 0 | 1 | 0 0 0` (a1 no-op; filler)
- seq24: `T 0 0 0 | 3 | 0 0 1` (a3, s2 0->1; support effect 3)

Design: the EFFECT episodes use a3 (not a4), following the obs3d
pattern (seq7: a3 s2 0->1). The a3 s2 0->1 is a contradiction for
a3's no-op law, so delay_attribution runs and supports R0 via the
a4 cause at d=2. Crucially, the effect action (a3) differs from
R0's cause (a4), so no spurious refutation is triggered 2 steps
later. The environment is context-stable (all states (0,0,0)),
directly testing the X-CV5-1 scenario.

Probe `cv6_clean_reconf_probe.txt`:
```
H 0 0 0 | 4
H 0 0 0 | 3
Q 0 0 0 | 3
```
(Same structure as the red team's deg probe.)

## Frozen expectations for K-CV6-1b

- Exactly one `# delay rule R0 REFUTED at seq 15` line. (a1 has no
  prior entry; no masking. dl_rf=2.)
- `# delay rule R0 NOT RE-CONFIRMED at seq 18` (support=2, not > 2).
- `# delay rule R0 CONFIRMED at seq 21 support=3 (provisional
  -> active)` (support=3 > 2).
- Zero `# delay rule R0 REFUTED` lines after seq15. (The a3 effect
  episodes do not trigger refutation.)
- Zero `# delay rule R0 NOT CONFIRMED` lines. (R4 path not taken
  for refuted rule.)
- Final dump: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT
  support=4`.
- Probe: `Q (0 0 0) | 3 -> (0 0 1)` (R0 ACTIVE; H=[a4,a3] triggers
  the d=2 delay).
- 3/3 byte-identical.

KILL if: R0 is not ACTIVE at end, or any refutation occurs after
seq15, or the probe does not show (0,0,1).

## Governance

- This amendment does not alter K-CV6-1's FAIL verdict; it adds
  K-CV6-1b as a separate, cleanly preregistered test.
- Pure Zag. No Python. No em dashes.
- Fixture and probe are committed with this amendment before any
  run.
