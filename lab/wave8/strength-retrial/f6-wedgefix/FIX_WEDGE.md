# F6 GLOBAL cite-consumption wedge — fix record (2026-09-26)

## The wedge

Under F4b, the citation single-use rule (new refusal `121`) was enforced
per-slot in every mode. In GLOBAL mode the law says a citation episode can
pay for only ONE destruction EVER — but the mechanism only remembered
consumption on the slot where the destruction happened. An attacker could:

1. Consume episodes 0–3 in a destruction on slot A.
2. Re-cite episodes 0–3 against slot B.
3. Destroy slot B for free (episodes already spent).

The red-team battery (G1–G13) confirmed the per-slot tombstone held on one
slot but did not stop cross-slot reuse. This is the D4 hole.

A second hole (D2): destruction pricing used CURRENT strength, not the
high-water mark. WEAK0→JUST→KILL priced a strength-90 memory at the
weakened strength — a free-destruction path. Micah signed the high-water
pricing amendment (2026-09-25): price = `ceil(HW/25)` where HW is the
maximum strength since the latest successful ADD/OVERWRITE.

## The fix (mechanism)

### D4: store-wide tombstone (`st_cite_consumed`)

In GLOBAL mode, `st_cite_consumed` now scans successful `KILL_EVIDENCED`
and `OVERWRITE` destructions on ALL slots (not just the queried slot).
Each destruction's payment window is derived from its own slot
(`st_pay_lo(s,dslot,d)`), so cross-slot lineage is never confused.

WINDOWED and HYBRID modes keep the exact F4b per-slot scan — byte-identical
behavior proven below.

Result: a citation episode consumed by a successful GLOBAL destruction is
consumed store-wide, on any slot, forever. The cross-slot probe
(slot 2 OW consumes 0–3, slot 3 cites 0–3, slot 3 KILL) now returns `121`.

### D2: high-water pricing (`st_epoch_highwater`)

Ported from the F1 Fork A winner. The epoch begins at the latest successful
ADD/OVERWRITE; the helper tracks the maximum before/after strength through
all successful strength writes. `st_kill_effort_check` (and the checker's
KILL/OVERWRITE verification, sharing the same helper) now prices
`ceil(HW/25)` and gates the stage requirement on HW.

Result: WEAK0→JUST→KILL with zero cites returns `109` (not enough cites
for the high-water price), never a free destruction. WEAK50 + four fresh
cites → `0` (correctly priced at the high-water mark).

### Cite-lock audit signals (new, audit-only)

Two signal ops make the wedge visible without changing rc semantics:

- `ST_OP_CITELOCK` (slot signal): emitted after a GLOBAL `121`
  priced-destruction refusal, IFF the target slot is cite-locked, defined
  as: the slot is live AND at least one cited episode exists in the
  current effort window AND every cited episode in the window is consumed.
- `ST_OP_CITELOCK_SYS` (system signal): emitted when all 14 user-capacity
  slots are occupied/live and every one is cite-locked — the terminal
  14/14 wedge. Transition-deduped (fires once per entry into the state).

Both are SYSTEM-role, `rc=0`, before==after. They change no return code,
no state, no consumption, no effort window. The checker independently
re-derives the lock predicate and REQUIRES the slot signal after every
GLOBAL `121` on an actually cite-locked target.

### Performance: batched consumption query (`st_consumed_list`)

The store-wide tombstone made the honest driver's per-candidate
`st_cite_consumed` scan quadratic (G HONEST 1x went from seconds to a
300s timeout). `st_consumed_list` computes the identical predicate in one
O(destructions × window) pass into a caller buffer; the driver does O(1)
membership tests per candidate. Episode selection is exactly unchanged
(W HONEST byte-identical), and G HONEST 1x now finishes in ~67s.

## Verification

### W1–W7 wedge battery (new, `f6_wedge_battery.zag`)

Covers: full-store wedge from a finite pool, stale KILL/OVERWRITE,
cross-slot D4 reuse, rollback and trainer paths, H16/H17, WEAK0/WEAK50
high-water regressions, signal gaming and rollback, four-fresh-cite
recovery, cheap-lock attempts, checker/replay/refusal integrity.

- Two runs byte-identical (`BATTERY BYTE-IDENTICAL x2`).
- `WB_VERDICT fail=0`.
- Finite-pool budget: P=8 allows exactly two strength-90 destructions,
  then the pool is exhausted store-wide (14/14 stale attempts → `121`).
- Four genuinely fresh episodes recover a full cite-lock: KILL → `0`,
  then ADD → `0`. Reusing those episodes → `121`.

### G1–G13 red-team shapes

All 13 sequences produce byte-identical rc streams on pristine vs fixed
binaries (two runs each). No prior `121` became `0`.

Correction to the red-team table: G8's final KILL is `109` on BOTH
pristine and fixed (the re-cites after rollback are `111` dups, so the
post-strengthen window has zero cites — `109`, not `121`). The table's
`121` was a recording error; the binaries agree, so there is no
regression.

### Mode-0 / WINDOWED compatibility (vs pristine F4b)

- W ATTACK: byte-identical.
- W STRESS (S8/S16/S32): byte-identical.
- W HONEST: byte-identical.
- H ATTACK: byte-identical.
- H HONEST: byte-identical.

### G ATTACK (A1–A8)

All 8 pass on the fixed binary, byte-identical across two runs
(`fail=0` × 10). A8 (`st_kill` force path) is a trainer-instrument
control, not TNN-reachable behavior.

### Honest use under G

G HONEST 1x: `ok=99, abandons=287, c121=0, ckfail=0, fail=0`.
The abandons are the intended P/4 finite-pool budget: 400 episodes fund
at most 100 kills (4 per kill); the driver starves exactly at the pool
limit. This is the D4 law working as designed, not a regression —
pristine's per-slot tombstone let episodes be reused across slots
(14 × 400 episode-slots). Real TNN mints fresh episodes continuously;
the test pool is finite.

## Files

- `strength_core.zag` — D4 tombstone, D2 high-water, cite-lock signals,
  `st_consumed_list`.
- `strength_checker.zag` — shared high-water verification, cite-lock
  checkers (`ck_verify_citelock`, `ck_verify_citelock_sys`).
- `f6_trial.zag` — batched honest-driver candidate scan.
- `f6_rt.zag` — driver-only `SLOT<n>` selection for cross-slot tests.
- `f6_wedge_battery.zag` — W1–W7 battery.
- `evidence/` — byte-identical run logs, pristine-vs-fixed comparisons.

## Disposition

- **D4: CLOSED.** Store-wide tombstone proven by cross-slot probe and
  W1–W7; no prior `121` became `0`.
- **D2: CLOSED.** High-water pricing shared by mechanism and checker;
  WEAK0→JUST→KILL cannot destroy for free.
- **G mode: ADOPTABLE** pending Micah's sign-off on the two law
  amendments (both already signed 2026-09-25).
