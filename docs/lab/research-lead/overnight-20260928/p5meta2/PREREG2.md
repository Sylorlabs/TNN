# PREREG-2 (ADDENDUM): P5 APPARATUS UNBLOCK

Lane `p5meta2`. Claim block **C7xx**. Branch `lane/p5meta2`, forked from
`lane/p5meta` @ `e37b101ce` so that the frozen prereg `24c133b42` and its
implementation are inherited unchanged.

## 0. WHAT IS INHERITED, UNCHANGED

`p5meta/PREREG.md` (commit `24c133b42`, committed alone, contains no `.zag`) is
**adopted in full and unmodified**. Every one of its 14 kill bars K1..K14, its
five conditions, its seven arms, its fids, its metric definitions, its round
schedule, its budgets, its seeds and its section 9 admissions stand as frozen.
**No bar, threshold, condition, arm, family id or seed is changed by this
addendum.** This lane therefore re-runs the *unmodified* prereg.

## 1. WHY AN ADDENDUM AND NOT A NEW PREREG

The prior lane was BLOCKED with no result claimed, because its measurement
apparatus produced an internally inconsistent record. An apparatus fault is not
a hypothesis and is not a result, so repairing it is not a preregistered
change of design. But repairing it must not be smuggled in, so it is declared
here, in advance, with a falsifiable prediction attached.

## 2. THE DECLARED APPARATUS REPAIR (mechanism already localised by reading)

`p5.zag` line 369 declares `res: 0 EX, 1 SA, 2 VA, 3 reached, 4 RU, 5 RR, 6 RA,
7 NS, 8 FC, 9 acc, 10 rounds, 11 arity`. `set32`/`get32` take **byte** offsets.
The record is written and read at byte offsets `0,1,2,...,11` -- one byte apart,
four-byte payloads -- so all twelve 4-byte fields overlap. `set32(res,0,EX)` at
the end of `run_ep` therefore overwrites bytes 0..3, destroying the low three
bytes of `SA`, `VA`, `reached` and `RU`. The reset loop
`while(i<12){ set32(res,i*4,0); }` is the single place that used the correct
4-byte-stride convention, which is the tell: the author had two conventions in
one record.

**This is the byte-versus-cell offset trap.** It is a STORE-ADDRESSING bug in the
lane's own code. It is not an arithmetic bug, not a compiler bug, and not
missing bounds checks: every offset used is within the 64-byte `res`
allocation, so no out-of-range write occurred and no neighbouring allocation
was corrupted.

### 2.1 FALSIFIABLE PREDICTION, REGISTERED BEFORE THE DIAGNOSTIC RUNS

Under the hypothesis "record fields at byte stride 1", the three sentinel
values are a *closed-form consequence* of five surviving byte writes, and must
be reproducible by pure integer layout arithmetic with no learner code at all:
with `b0..b3 = 256`, `b4..b7 = 0` except `b7 = 1`, `b8 = 0`, `b9 = 100`,
`b10 = 64`,

- `get32(res,1)` = `1`                     (the reported `SA`)
- `get32(res,5)` = `65536`                 (the reported `RR`)
- `get32(res,6)` = `1677721856`            (the reported `RA`)
- `get32(res,7)` = `1080295425`            (the reported `NS`)

If a pure-layout Zag program does NOT reproduce all four of those exact
integers, the mechanism is wrong, the byte-offset repair is NOT to be trusted,
and this lane reports BLOCKED again rather than proceeding.

## 3. PRE-REGISTERED DIAGNOSTIC D1 (priority 1, the stated next step)

`p5meta`'s REPORT section 6.1 asks for the reduced runner: **one round, one
tier**, printing `cur,tot,room,take,cnt,budget,found` per iteration. Frozen
expectations, registered now:

- **D1a ARITHMETIC**: `tot` = `4*tier_n(arity)`; `room = tot-cur`; `take =
  min(budget,room)`; `cnt` = number of hypotheses evaluated; the new cursor =
  `cur+cnt`; remaining budget = `budget-cnt`. Non-negative, and
  `cnt <= take <= 24`.
- **D1b STORE**: with the record repaired to byte stride 4, `SA` after one
  round of one tier must equal `cnt`, and `SA` must accumulate monotonically
  across rounds.
- **D1c VERDICT RULE, frozen**: if D1a holds and D1b fails -> STORE bug.
  If D1a fails -> ARITHMETIC bug in the lane's own search code. If both hold
  and the full run is still inconsistent -> something else, report BLOCKED.
  The rule is registered before the run so the answer cannot be reinterpreted.

## 4. PRE-REGISTERED APPARATUS HARDENING

1. **Bounds assertion on every arena access.** Every `get32`/`set32` on `L`,
   `res`, `SCR`, `B`, `P`, `EXB`, `FB`, `AGG`, `EXM`, `POS`, `ORD` is routed
   through a checked wrapper that verifies `0 <= off` and `off+4 <= len`. On
   violation it prints a loud `BOUNDS_VIOLATION` line naming the buffer, the
   offset and the length, and increments a violation counter that `main`
   prints. **Any violation count > 0 is an automatic K2-style apparatus FAIL**
   and the run is reported BLOCKED. The emitted binary has no slice bounds
   checks, so this is the only detector.
2. **Cell-indexed accessors only.** Record fields are reached exclusively
   through `RC_*` accessors that multiply by 4 internally. No bare integer is
   ever passed as a record offset.
3. **No design change.** `RMAX=64`, `SB=24`, `AUDN=16`, `MAXE=256`, `VAUD=32`,
   `V` derivation, `ORD` derivation, `AR` derivation, the reuse phase, the
   verification/audit protocol and the 4-stride restart rule are untouched.

## 5. PRE-REGISTERED OUTCOME MAPPING

- **A1** bounds violations > 0 -> `APPARATUS-FAIL`, no kill bar evaluated.
- **A2** D1c resolves to STORE bug, prediction 2.1 reproduces all four
  integers, repaired run is internally consistent (every (condition,arm) cell
  self-consistent, `SA` in the hundreds, `R=1` iff criterion reached, `RR`/`RA`
  reachable and zero on a fresh empty PLAN) -> apparatus **TRUSTWORTHY**,
  proceed to evaluate K1..K14 of `p5meta/PREREG.md` unmodified.
- **A3** apparatus trustworthy but any K4..K14 fails -> that failure is the
  result, reported as a failure, bars unmoved.
- **A4** prediction 2.1 does not reproduce -> `BLOCKED`, no result claimed.

## 6. NEW KILL BAR FOR THIS LANE (apparatus only; adds to, never relaxes)

- **K15 APPARATUS CONSISTENCY**: zero bounds violations; `SA > 0` on every
  episode that executed the search loop; `RR = 0` and `RA = 0` on every episode
  whose starting PLAN table is empty; `EX ∈ {4,8,...,256}`; `REACH ∈ {0,1}` per
  family and `REACH = 6` on every non-IRRELEVANT (condition, arm); the
  IRRELEVANT per-family `EX` difference between PRIOR and COLD is 0.

K15 FAIL -> `APPARATUS-FAIL`; K1..K14 are not evaluated and no verdict is
claimed. K15 is not a hypothesis about meta-learning; it is the statement that
the instrument works.

## 7. ATTESTATION

This file is committed **alone**, before any `.zag` file exists in lane
`p5meta2` and before any repaired binary has been run. Sections 2.1 and 3 are
falsifiable predictions registered in advance, not post-hoc explanations.
