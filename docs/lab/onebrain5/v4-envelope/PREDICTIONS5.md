# PREDICTIONS5 — per-item predictions (written from single-mode microstructure + PREREG5 §2 rules, before freeze)

**Method:** For each v8 item, the single-mode microstructure (fired readings, fact inter, bid22 grounding/grd, margin) was observed. Predictions apply PREREG5 §2 mechanism rules (M1–M7). No fork-mode run on any v8 item preceded these predictions.

**Notation:** predicted winners per mode; V4 effect = sign(onebrain − nov4) in correctness (+1 help, −1 harm, 0 inert). Expected bids: E01–E04 = 16; E05–E20 = 15 (E13=16, E15=16).

## HELP group (E01–E04) — predicted V4 HELPS

Microstructure (all four): readings {0,2}; inter(challenge fact)=4 > inter(correction fact)=2; bid22 grd=0 grounded in correction fact; margin=9.
- rel tie at 2 (both facts' keywords fully inside their clause topics) → M2 sorts by dep: challenge fact dep=1 (bid 19 only) < correction fact dep=2 (bids 16+22) → V4 denies the CHALLENGE fact; bid19 cleaned (M3).
- nov4: reint rule ranks inter first (M5) → bid19 (inter 4) beats bid16 (inter 2) → 19 WRONG.
- onebrain: V4 removed bid19 → reint falls to bid16 → 16 RIGHT.
- nG: alive {16,22} → honest null picks lowest hid = 16 RIGHT. nov4nG: alive {16,19,22} → null picks 16 RIGHT.

| item | single | onebrain | nov4 | nG | nov4nG | V4 effect | reason |
|---|---|---|---|---|---|---|---|
| E01 | 16 | 16 | 19 | 16 | 16 | HELP | V4 denies challenge fact (fid4, dep 1<2); reint would wrongly pick 19 |
| E02 | 16 | 16 | 19 | 16 | 16 | HELP | V4 denies challenge fact (fid1, dep 1<2); reint would wrongly pick 19 |
| E03 | 16 | 16 | 19 | 16 | 16 | HELP | V4 denies challenge fact (fid0, dep 1<2); reint would wrongly pick 19 |
| E04 | 16 | 16 | 19 | 16 | 16 | HELP | V4 denies challenge fact (fid2, dep 1<2); reint would wrongly pick 19 |

## HARM group (E05–E08) — predicted V4 HARMS

Microstructure (all four): readings {2,6}; inter tied at 2; bid22 grd=2 grounded in challenge fact; margin=12; forget target adjacent to "forget" (topic6 non-empty → duel no-conflict predicted by M6).
- rel tie at 2 → M2 sorts by dep: forget fact dep=1 (bid 15) < challenge fact dep=2 (bids 19+22) → V4 denies the FORGET fact; bid15 cleaned (M3).
- nov4: reint → bid15 (branch audits agree on 15) → 15 RIGHT.
- onebrain: V4 removed bid15 → branches fall to 19 → 19 WRONG.
- nG: alive {19,22} → null picks 19 WRONG. nov4nG: alive {15,19,22} → null picks 15 RIGHT.
- E07 note: third fact fid11 (inter 1, rel 1, dep 0) is denied first as least-disruptive; the forget-fact denial follows in round 2. Outcome prediction unchanged.

| item | single | onebrain | nov4 | nG | nov4nG | V4 effect | reason |
|---|---|---|---|---|---|---|---|
| E05 | 15 | 19 | 15 | 19 | 15 | HARM | V4 denies forget fact (fid1, dep 1<2); correct 15 removed |
| E06 | 15 | 19 | 15 | 19 | 15 | HARM | V4 denies forget fact (fid2, dep 1<2); correct 15 removed |
| E07 | 15 | 19 | 15 | 19 | 15 | HARM | V4 denies fid11 then forget fact (fid0); correct 15 removed |
| E08 | 15 | 19 | 15 | 19 | 15 | HARM | V4 denies forget fact (fid4, dep 1<2); correct 15 removed |

## DUEL-PREEMPT group (E09–E12) — predicted V4 INERT (duel pre-empts)

Microstructure (all four): readings {2,6}; forget target >4 tokens after "forget" → reading-6 topic empty → corr(6)=0 by construction; margin=10.
- M6: branch-0 duel in round 1 — challenger reading 2 (corr≥2) kills reading 6 (corr 0) BEFORE V4's 2a runs → 2a suppressed for the whole deliberation (shared ledger).
- Branch winners 19 in every fork mode; onebrain == nov4 == 19 (both WRONG vs expected 15); nG == nov4nG == 19.

| item | single | onebrain | nov4 | nG | nov4nG | V4 effect | reason |
|---|---|---|---|---|---|---|---|
| E09 | 15 | 19 | 19 | 19 | 19 | INERT | duel kills rd6 r1; V4 2a never fires |
| E10 | 15 | 19 | 19 | 19 | 19 | INERT | duel kills rd6 r1; V4 2a never fires |
| E11 | 15 | 19 | 19 | 19 | 19 | INERT | duel kills rd6 r1; V4 2a never fires |
| E12 | 15 | 19 | 19 | 19 | 19 | INERT | duel kills rd6 r1; V4 2a never fires |

## INERT-MARGIN group (E13–E16) — predicted V4 INERT (no fork)

Microstructure: readings {0,7} or {6,7}; margins 18/18/21/21, all >12 → M1: fork=0, subpasses skipped, V4 cannot fire. All modes identical to single.

| item | single | onebrain | nov4 | nG | nov4nG | V4 effect | reason |
|---|---|---|---|---|---|---|---|
| E13 | 16 | 16 | 16 | 16 | 16 | INERT | margin 18 > 12; fork=0 |
| E14 | 15 | 15 | 15 | 15 | 15 | INERT | margin 21 > 12; fork=0 |
| E15 | 16 | 16 | 16 | 16 | 16 | INERT | margin 18 > 12; fork=0 |
| E16 | 15 | 15 | 15 | 15 | 15 | INERT | margin 21 > 12; fork=0 |

## NEAR-MARGIN group (E17–E20) — predicted V4 binds iff margin ≤12

Microstructure: all readings {2,6}, HARM-shape (inter tied or forget-fact inter ≥ challenge; bid22 grd=2 in challenge fact).
- E17: margin 11 ≤12 → fork → V4 denies forget fact → onebrain=19 WRONG, nov4=15 RIGHT → HARM.
- E18: margin 12 ≤12 → fork → V4 denies forget fact → onebrain=19 WRONG, nov4=15 RIGHT → HARM.
- E19: margin 13 >12 → no fork → onebrain=nov4=15 RIGHT → INERT.
- E20: margin 14 >12 → no fork → onebrain=nov4=15 RIGHT → INERT.
- nG/nov4nG: E17,E18 → 19/15 (V4 breaks the null); E19,E20 → 15/15.

| item | single | onebrain | nov4 | nG | nov4nG | V4 effect | reason |
|---|---|---|---|---|---|---|---|
| E17 | 15 | 19 | 15 | 19 | 15 | HARM | margin 11 ≤12; V4 denies forget fact |
| E18 | 15 | 19 | 15 | 19 | 15 | HARM | margin 12 ≤12; V4 denies forget fact |
| E19 | 15 | 15 | 15 | 15 | 15 | INERT | margin 13 >12; fork=0 |
| E20 | 15 | 15 | 15 | 15 | 15 | INERT | margin 14 >12; fork=0 |

## Aggregate predictions

- onebrain: 16/20 (E01–E04 right, E05–E08 wrong, E09–E12 wrong, E13–E16 right, E17–E18 wrong, E19–E20 right) = 4+0+0+4+0+2 = 10/20.
- nov4: E01–E04 wrong (0), E05–E08 right (4), E09–E12 wrong (0), E13–E16 right (4), E17–E18 right (2), E19–E20 right (2) = 12/20.
- Predicted net V4 effect: (4 helps) − (6 harms) = −2 items (onebrain 10/20 vs nov4 12/20).
- V4-effect direction predictions: 4 HELP, 6 HARM, 10 INERT.
