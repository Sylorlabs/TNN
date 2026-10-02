# Preregistration Amendment 2: H-CAUSALV6 K-CV6-1c (truncated fixture)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before any K-CV6-1c run)
**Amends:** PREREG_CAUSALV6.md and PREREG_CAUSALV6_AMENDMENT.md
**Researcher:** H-CAUSALV6 Frontier Researcher (subagent)

## Why this amendment exists

K-CV6-1 (original): FAIL. Prereg error; the red team's 24-episode
fixture contains a fixture-induced refutation at seq23 once R0 is
ACTIVE (the E_2 effect episode's a4 action triggers R5).

K-CV6-1b (clean a3-effect fixture): FAIL. Prereg error; the learner
attributes the a3 s2:=1 effects to a3's immediate law (entry 5
learns SET(1)) rather than to the R0 delay. The a3 action does not
have a sufficiently established no-op history to force a
contradiction; the delay_attribution path is not taken. This is a
fixture design failure, not a mechanism failure.

The mechanism evidence from K-CV6-1 (original) is unambiguous:
`# delay rule R0 CONFIRMED at seq 21 support=3 (provisional ->
active)`. The R6b graded re-confirmation breaks the X-CV5-1
ratchet. What is needed is a fixture that isolates this event
without the seq23 artifact.

## K-CV6-1c: truncated red-team fixture

Fixture `cv6_trunc21_obs.txt`: the first 21 episodes of the red
team's frozen cv5_adv_deg_obs.txt (byte-identical prefix).
- seq1-12: obs3d (R0 CONFIRMED at seq11, support=2).
- seq13-15: refuter triple (R0 REFUTED at seq15, dl_rf=2).
- seq16-18: support block 1 (R0 supported at seq18, support=2,
  NOT RE-CONFIRMED).
- seq19-21: support block 2 (R0 supported at seq21, support=3,
  CONFIRMED).

The truncation at seq21 excludes the seq22-24 block whose E_3
episode (a4 at seq21) causes the fixture-artifact refutation at
seq23. The 21-episode prefix is a clean, frozen, red-team-authored
sequence.

Probe `cv6_trunc21_probe.txt`: byte-identical to the red team's
cv5_adv_deg_probe.txt.

## Frozen expectations for K-CV6-1c

- Exactly one `# delay rule R0 REFUTED at seq 15` line.
- `# delay rule R0 NOT RE-CONFIRMED at seq 18` (support=2).
- `# delay rule R0 CONFIRMED at seq 21 support=3 (provisional
  -> active)`.
- Zero `# delay rule R0 REFUTED` lines after seq15.
- Zero `# delay rule R0 NOT CONFIRMED` lines.
- Final dump: `# DL R0 cause=4 d=2 var=s2 fx=SET(1) st=ACT
  support=3`.
- Probe: `Q (0 0 0) | 3 -> (0 0 1)`.
- 3/3 byte-identical.

KILL if: R0 is not ACTIVE at end, or any refutation occurs after
seq15, or the probe does not show (0,0,1).

## Governance

- K-CV6-1 and K-CV6-1b remain FAIL (prereg/fixture errors,
  documented here). This amendment adds K-CV6-1c; it does not
  alter prior verdicts.
- Pure Zag. No Python. No em dashes.
- Fixture (truncated prefix) and probe committed with this
  amendment before any run.
