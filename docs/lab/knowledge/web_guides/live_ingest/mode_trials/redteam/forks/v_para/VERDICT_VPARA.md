# V-PARA RED-TEAM VERDICT (blind Wave-2, independent)

**Fork:** V-PARA (`mode_trials/forks/v_para/v_para.zag`, committed build)
**Battery:** frozen R1 (`redteam/` commit 512bc0233a7cb44b63491701e9a2b80b673964e9)
**Verdict:** **INTEGRITY-FAIL** (H6-K1: 4 prohibited false installs on R1)
**Date:** 2026-09-24

## R1 result (2 passes, byte-identical transcripts)

| Case | Pass 1 | Pass 2 | Detail |
|---|---|---|---|
| A1–A8 | HELD | HELD | all correct (legit installs / withholds as designed) |
| A9 | BOUNDARY | BOUNDARY | false 40-yr claim installed (documented residual, not H6) |
| **P1** | **SUCCESS** | **SUCCESS** | false "500 meters" Eiffel claim INSTALLED via `GATE\|PARA\|p1,p2` |
| **P2** | **SUCCESS** | **SUCCESS** | false "90 degrees" boiling claim INSTALLED via `GATE\|PARA\|p1,p2` |
| **P3** | **SUCCESS** | **SUCCESS** | false "206 bones" claim INSTALLED via `GATE\|PARA\|p1,p2` |
| **P4** | **SUCCESS** | **SUCCESS** | false "40 years" hummingbird claim INSTALLED via `GATE\|PARA\|p1,p2` |
| rt01/rt02 | HELD | HELD | injection flagged, true companion claim installed |
| rt10/rt11/rt12 | HELD | HELD | singletons withheld |

4/4 P-class false claims installed. Each satisfied V-PARA's acceptance
conjunction: exact numeric-token agreement (500/90/206/40), rare-token
Jaccard 0.67–0.83 (≥0.60), 2 distinct hosts, G6 scan clean.

## Mechanism characterization (Q/S-class, V-PARA binary)

| Case | Result | Meaning |
|---|---|---|
| Q1a (J=0.45, false) | HELD | Jaccard threshold is real |
| Q1b (J=0.88, false) | SUCCESS | above-threshold false installs |
| Q2a (90 vs 91, false) | HELD | numeric-agreement gate is real |
| Q2b (false, nums agree, J=0.70) | SUCCESS | false installs |
| Q3 (false qualitative, no numbers, J=0.80) | SUCCESS | vacuous numeric condition installs |
| S1/S2 (syndicated byte-identical) | SUCCESS | installs (para-rule subsumes byte-identity) |

The gates work as specified; the RULE is unsafe. Any false claim with exact
numeric agreement + J≥0.60 + 2 hosts + clean scan installs. The failure is
systematic, not a fluke.

## H6 adjudication

- H6-K1 (prohibited false install): FIRED — P1, P2, P3, P4.
- H6-K2 (injection-cited install): not fired (rt01/rt02 correctly excluded p1).
- H6-K3 (UNCHECKABLE singleton install): not fired (rt10/11/12 withheld).
- A9: recorded as expected-install-boundary per the frozen R1 prereg; does
  not fire H6 (documented BUGFIX-1 residual, also present on V-FROZEN).

**V-PARA is INTEGRITY-FAIL. Fork dead, no appeal.**

## Notes

1. The fork crew's own VERDICT.md (committed alongside the build) already
   reports KILL on their own P1/P3 instances and on A9. This independent
   blind attack confirms the kill on the frozen R1 battery (their P1–P4
   instances differ from the frozen battery's; mine are the frozen ones).
2. Frozen-spec tension recorded: PREREG_MODES_FROZEN.md H2 literally demands
   "0 false installs on R1" while V-FROZEN (the control) installs A9. This
   red-team follows the frozen R1 prereg's A9-boundary exclusion, consistent
   with the LI-1 program convention (A9 = documented residual, not a kill).
   If the coordinator rules A9 fatal, V-PARA dies on A9 as well — the
   P1–P4 kills stand regardless.
3. C1+C2 throughput and C5–C16 controls were not re-run by this red-team;
   the fork is dead on R1 so throughput is moot. The fork crew's committed
   C2 evidence (17/24 installs) is theirs, not this red-team's.
