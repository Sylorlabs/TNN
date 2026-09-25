# F36 MEY — Verdict

**Mechanism:** 36 (Marginal-Yield Ledger)  
**Date:** 2026-09-25 UTC  
**Prereg:** `PREREG_FORKROUND.md` §3 F36, §4 (B8 amended §4b), §10  
**Verdict:** **KILLED**  
**Failure mode:** **FM6** (selection)

## Kill table

| Kill | Criterion | Result |
|------|-----------|--------|
| (a) | Nondecreasing-f5 subset has positive C-slope > accuracy-slope at n≥30 | **FIRES** — admit (+0.0073), cost (+0.0063), logic (+0.0005), revoke (+0.0049); acc-slope 0.0 in all four |
| (b) | Strict B3 violations ≥ NEC m9's 6 | **FIRES** — 19 ≥ 6 |
| (c) | Saturated-ceiling B13 failures (predicted risk) | 8 failures, all ceiling D/O; recorded, does not kill |

## Kill-bar table (B1–B9+B13)

| Bar | Result | Detail |
|-----|--------|--------|
| B1 | **PASS** | 0 1→0 transitions |
| B2 | **FAIL** | V1=0, V2=71 (ceiling P:54, D:10; trap:5; redteam:2) |
| B3 | **FAIL** | 19 G-violations (NEC m9: 6); every family has ≥1 |
| B4 | **PASS** | meanConfCorrect=0.9669 |
| B4b | **PASS** | All honest families ≥0.98 |
| B5 | **PASS** | 0.7185 separation |
| B6 | **PASS** | 1.0 recall (or vacuous) |
| B7 | **PASS** | 0.1475 abstention |
| B8 | **PASS/VOID** | PASS on 7 families; VOID on redteam, trap (<4 M4-feasible slots) |
| B9 | **PASS** | 5240/5240 (100%) release+correct identity vs M4 |
| B12 | recorded | G>0 crossings: P:6, redteam:5, D:3, trap:3 |
| B13 | **FAIL** | 8 (F,d) with G<−0.100, all ceiling D/O (saturated) |
| B3pi | recorded | 1158/3467 rising per-item pairs |

## Deltas vs NEC m9

| Metric | F36 MEY | NEC m9 |
|--------|---------|--------|
| B3 violations | 19 | 6 |
| B13 failures | 8 | 6 |
| B2 (V1/V2) | 0/71 | 0/0 (pass) |

F36 is strictly worse than NEC on B2, B3, and B13.

## Why it fails (FM6)

The marginal-yield ledger does not implement its causal story. The confidence
C is dominated by the ledger cell's population ρ, not by marginal yield:

1. **Theater (B2):** Wrong items sorted into high-ρ cells receive rising
   confidence (trap C6: 10→403 while wrong at both depths; ceiling P: 54 V2).
   The ledger assigns population statistics to individuals.

2. **Causal claim wrong (kill a):** On the nondecreasing-f5 subset — where the
   mechanism's own logic says yield cannot be driving confidence — C still
   rises faster than accuracy (which is flat at 1.0). The C-slope comes from
   ledger-cell ρ drift with depth, not from yield.

3. **Law violations (kill b):** 19 strict B3 violations, 3× NEC's count. The
   (m,y) keying does not stabilize the G-curve; cell populations shift with
   depth and drag G upward.

The path rule (yield-drop blocks rise; trauma cuts to C_prev−1) fires
correctly (604/604 verified) but almost never binds: C_prev ≥ C0 in practice,
so C=C0 nearly everywhere. The mechanism reduces to a static ρ lookup — and
the lookup is miscalibrated at the item level.

## §10 adjudication

F36 does not clear B1–B9+B13 (fails B2, B3, B13). Honest families do not clear
(fail B3; kill (a) fires on all four). **KILLED**, FM6.

The B3-vs-B3pi evidence: strict B3 fails (19) while per-item B3pi shows
1158/3467 rising pairs (33%). Both metrics agree the mechanism is
miscalibrated; no support for the unsatisfiability thesis from this fork.
