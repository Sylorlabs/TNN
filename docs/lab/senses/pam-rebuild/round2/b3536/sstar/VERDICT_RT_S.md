# VERDICT_RT_S — B-3536-S*: grok's N/O/P classes vs the composition

**Crew:** RT-S (PAM round-2 swarm, red-team crew)
**Date:** 2026-09-24
**Prereg:** PREREG_RT_S.md (`577829e3`, frozen alone before code)
**Build:** `f1a80f52` (mechanisms verbatim from committed driver `7a1a8422`, unmodified)
**Verdict: KILL — the composition is killed.** All three of grok's kill conditions fired.

## Battery results (3 runs, byte-identical, SHA `bf436a5a…`)

```
N_GATE=120 N_HARM=120 N_S1=120 N_S2=120
O_GATE=120 O_HARM=120 O_S1=120 O_S2=120
OT_ARMT_ADMIT=0
O_TEMPORAL_PRECOMMIT=0 O_TEMPORAL_FAIL=120
P_GATE=120 P_HARM=120 P_S1=120 P_S2=120
HONEST_ADMIT=120 HONEST_HARM_N=0 HONEST_HARM_O=0 HONEST_HARM_P=0
C35J_INSTALL=0 (anchor held) | C36K_INSTALL=0 (anchor held)
C36M: S1=120 S2=0 (anchor held) | C36J: 120/120 carry (held)
```

| Class | Gate | Harm | Bar | Outcome |
|---|---|---|---|---|
| N (honest mint × world-close × dirty label) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| O-numeric (+20 inside window) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| O-temporal (property) | — | fail **120/120** | property kill ≥97 | **KILL** |
| P (remint high-half id) | 120/120 | **120/120** | kill ≥97 | **KILL** |
| HONEST | 120/120 admit | 0/0/0 | loss ≤15% | PASS |
| Anchors C35J/C36K/C36M/C36J | at measured positions | — | hold | PASS |
| Determinism | 3× byte-identical | — | required | PASS |

Grok's pre-run predictions (§6) landed exactly: N 120/120, O-temporal property
kill, P 120/120, honest 120/120 with 0 harm, anchors at positions.

## What each kill means

- **N:** the missing cell. Legal mint (`declassify(v,1)`) + world-copied
  (conf,meas) + dirty `label=0` installs 120/120 on BOTH metrics. Stage 1 falls
  because the tag is genuine (unforgeability is the wrong theorem — nothing was
  forged); stage 2's live predicate never mentions `label`. The serial AND fails
  because each conjunct targets a different attack than the one running.
- **O-temporal:** `c_stage2` records no commitment object before any sample —
  `temporal_fail` on 120/120 trials. The H-36 half of the advertised conjunction
  is not executed in the composition driver; the two-phase reference (arm T)
  refuses 0/120 when actually run, proving the protocol works and the driver
  simply doesn't contain it. An AND that drops a conjunct is not an AND.
- **P:** remint (not splice) of `hi_atk=0x1F2E3D4C` over honest world readings
  installs 120/120 both metrics. Stage 1 passes — the tag's full-64 id IS the
  substitute; stage 2 passes — `admit36` never compares opened id to any world
  value and `cstep`'s low-32 commit cannot see the high half. C35J's 0/120
  covered replay only; the composition's adversary includes the mint.
- **Anchors held:** C35J 0/120 (P is not a splice), C36K 0/120, C36M S1=120/S2=0
  (a chain not reading `wm_i` still misses), C36J 120/120 carry. N/P/O are new
  classes, not renames — the existing classifier bins stay exactly where the
  frozen battery put them.

## Scope

Per PREREG_RT_S §4 (frozen fork): Amendment 1 A2's carve names IDENTITY only.
No post-hoc extension to label/verdict/full-id was applied or needed — the
verdict fires on the harm metric directly. Components keep their scoped
verdicts: R-35 survives as unforgeability-only; R-36 (standalone) survives as
the temporal game actually executed in its own driver.

## Verdict

**KILLED as the composition.** H-PAM-35/36 return to the backlog as
TESTED-killed **as the composition** (PREREG_B3536 §4: no kill-bar repairs for
compositions). The composition admits three whole searchable harmful classes at
120/120 while its honest loss is 0% — it is not an inertness boundary on the
Lemma's win condition (admit-set ∩ S*).
