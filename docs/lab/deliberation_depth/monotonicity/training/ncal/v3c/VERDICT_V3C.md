# VERDICT — NEC v3c: B13 composition redesign (Phase 2)

- **Date:** 2026-09-25 (PDT).
- **Authority:** `PREREG_NCAL_V3C_B13FIX_FROZEN.md` §7 (adoption/kill),
  amendments A1 (superseded) / A2 / A3.
- **Evidence:** `RUNLOG_V3C.md` (full tables, SHAs, trace excerpts).

## Headline

**Design S (variant 26): ADOPTED.** All seven §7 adoption criteria hold:
B13 = 0/0/0 with every G curve at exactly +0.000, B3 = 0/0/0 (better than
m20's 2/2/2, no regression), all other bars pass, T1/T2/T4 CALIBRATING,
T3 0.3812 < 0.470 with bias +0.3020 (the pre-registered honest-miss),
no new red-team breaks, 186/186 A/B/C byte-identical.

**Design S8 (variant 27): KILLED** — B13 = 11/12/12 > 0 (kill criterion i).

**Design D (variant 28): KILLED** — B3 gviol = 6 > 2 (kill criterion ii).

## What the three designs prove together

The §2 lemma is confirmed empirically from both sides:

1. **The trap is real.** With v3b's coarse seeds, the adopted min-latch is
   simultaneously NECESSARY for B3 (D removes it → B3 dies with 6 strict
   d1→d2 rises) and FATAL for B13 (v3b kept it → 22 violations).
2. **The only §6-legal fix is reference-class refinement.** S's narrowest
   exact-cell schema (min_n=1) holds B13 = 0/0/0 AND B3 = 0/0/0
   simultaneously — the tradeoff dissolves when the seed is honest at the
   exact-cell level.
3. **The sufficiency threshold reintroduces the disease.** S8's min_n=8
   backs (O,d) and (admit,d) off pure exact cells into mixed coarser cells
   (G −0.198 / −0.166), reproducing the v3b failure mode at smaller scale —
   exactly the pre-registered kill mechanism.

The honest-knowledge ceiling composition is now: **schema seed at tp=0 as
the latch value; `min(seed, p_raw)` thereafter; no other change to the
adopted mechanism.**

## Adoption details (Design S, per §7)

| # | criterion | result |
|---|---|---|
| 1 | B13 = 0/0/0, nonincreasing | 0/0/0 ✓ |
| 2 | B3 = 2/2/2, no regression | 0/0/0 ✓ (favorable miss; kill is B3>2) |
| 3 | B1=0, B2=0/0, B4≥0.50, B4b≥0.50, B5≥0.20, B6, B7≤0.30, B9=1.0 | 0, 0/0, 1.0, 1.0, 1.0, 1.0, 0.1475, 1.0 ✓ |
| 4 | no tp≥1 rise on always-correct items | 0/3467 trace rises ✓ |
| 5 | T1/T2/T4 CALIBRATING; T3 < 0.470, bias ≥ −0.05 | T1 M1/M2/M3 clean; T2 binds 100% on wrong cells; T3 0.3812/+0.3020 ✓ |
| 6 | no NEW red-team breaks vs m20/FIX1 | RT-A better-or-equal; RT-B same honest residual; RT-C zero rises; RT-D stable; RT-E no channel; RT-F same known implementation break ✓ |
| 7 | determinism | 186/186 byte-identical, SHA-logged ✓ |

## Killed forks (mechanism reasons)

**S8 — killed for coarse backoff.** min_n=8 forces backoff from n<8 exact
cells: (O,d) → mixed (f1,f5) cells with G −0.198 at all six depths,
(admit,d) → G −0.166 at all five depths. The schema's honesty was in the
exact cells; the threshold dilutes it. The §2 corollary's predicted death,
observed exactly.

**D — killed for removing the latch.** With K-A coarse seeds and no latch,
conf = p_raw at tp≥1: strict G rises d1→d2 on D, O, admit, cost, logic,
revoke → B3 gviol = 6, exactly the A2 prediction. Confirms the §2 lemma's
B3 half: the latch is load-bearing for B3 given coarse seeds.

## Disclosures and residuals (carried, not new)

- **RT-B B5 inversion (−0.1007):** consequence A of the adopted latch,
  unchanged by this redesign (B5 = −0.101 on m20). Honest residual, in-class.
- **RT-F 63-byte id cap:** same implementation break as the m20 baseline
  (|err|=1.0/cell on 72-char always-wrong ids on S/S8; FIX1 recommended,
  adoption still open). Not a design choice, not new.
- **RT-E learn B13=3:** consequence A on wrong-first patterns (conf 0 at
  d4/d8/d16 while correct), not a channel — the mechanism does exactly
  what it says.
- **T3 0.3812:** the honest miss on truly-unseen classes (L3 d=1 backoff
  802000 for all five trap points), pre-registered, strictly better than
  m20's 0.470, bias +0.3020 (no bar-ward pessimism).
- **D's T3 = 0.0000** is the disclosed K-A oracle, not celebrated.

## Recommendation

**Adopt Design S (variant 26) as the B13 composition fix.** S8 and D stay
killed with their mechanism reasons on record. Open items for Micah
(unchanged): FIX1 adoption (the RT-F id-cap fix), m15 clause, FIX-A
adoption — none of which this round alters.
