# PORT DECISIONS — F6 wedge-fix → delete-strong mainline
## 2026-09-26, delete-strong-mainline port of the F6 cite-consumption wedge fix

Base: `~/workspace/strength-delete/` post-holefix (core `d93d882d…`, checker `6dd22c53…`).
Donor: `~/workspace/strength-f6-wedgefix/` (fix commits `de7f59c91`, `20497b8f0`).
Mechanism: deterministic Python merge (`merge_port.py`, `merge_port_checker.py`) —
every edit is an exact-anchor replacement; any missing anchor aborts.

---

### D1. Mainline is the base; the fix is composed in, not transplanted

The delete-strong mainline (trainer-only `st_kill`, `st_delete_strong`,
learner changes, replay/rollback, S-D1..S-D5 law) is preserved intact. The F6
fix contributes: GLOBAL consumption semantics, the cite-lock signal
mechanism, and the checker tie/require rules. Nothing in the mainline's
honest path, pricing, or law text is altered.

### D2. Op-number reconciliation (serialization-safe)

The F6 workstream used `ST_OP_CITELOCK=20`, `ST_OP_CITELOCK_SYS=21`. The
mainline already assigns op 20 to `ST_OP_DELETE_STRONG` (live law; ledgers in
the wild carry it). The port therefore assigns:

- `ST_OP_CITELOCK = 21`
- `ST_OP_CITELOCK_SYS = 22`

Recorded as serialization-safe within the port's ledger version: no existing
op number is reused or shifted; pre-port ledgers parse identically.

### D3. Consumption composition (the core of the port)

F6's D4 (store-wide tombstone) is composed with the mainline's S-D2
(per-slot, generation-scoped tombstoning across ADD reuse):

- The priced-destruction set is the **mainline's four-op set**: `KILL`,
  `KILL_EVIDENCED`, `OVERWRITE`, `DELETE_STRONG`. (The F6 workstream predated
  the holefix and priced only `KILL_EVIDENCED`/`OVERWRITE`; the trainer
  priced-kill path and the one-step delete path must burn cites too, or the
  wedge reopens through them.)
- `st_cite_consumed` scans the destruction's own slot (`dslot`) with a
  per-mode payment window:
  - WINDOWED: `dslot == slot` filter + `st_pay_lo` = last strength-set
    (identical predicate to the pre-port mainline — proven by the S1/S10
    honest matrices being byte-identical, see VERDICT.md).
  - GLOBAL: any `dslot` + `st_pay_lo` = last ADD on `dslot` (F6 D4 verbatim).
- No double-counting: each destruction burns each episode once (distinct-ep
  collection in `st_consumed_list`; early-return on first hit in
  `st_cite_consumed`). No resurrection: tombstones never clear (WINDOWED
  scans the full ledger; GLOBAL has no reset at all).

### D4. WINDOWED ≠ F6's W-mode (deliberate divergence)

The F6 workstream's W-mode reset consumption at the current effort window
(`after_idx`), reproducing the F4b window law. The mainline's signed S-D2
supersedes F4b: a cite that paid for a destruction stays spent for the slot
across ADD reuse. The port's WINDOWED therefore scans the **full** history
(`st_consume_lo` returns -1), exactly reproducing the pre-port mainline
predicate. The F6 battery's W1 expectations do not transfer; the port's
battery asserts the S-D2 behavior instead (W8a: re-cited episodes stay
burned after ADD reuse).

### D5. HYBRID is carried but disqualified

`ST_CITE_HYBRID=2` and its semantics (last-ADD reset, F6 verbatim) are kept
for source compatibility. Per Micah's 2026-09-25 ruling ("slot reuse
resurrecting spent cites is a big issue"), drivers must not select it; the
red-team brief scopes it out. `st_set_cite_mode` accepts it without silent
remap (a silent remap would be worse than an explicit disqualified mode).

### D6. High-water: single implementation kept

The mainline's `st_epoch_highwater` + `st_n(HW)` already matches the signed
S-D1 law and the F6 workstream's `ceil(HW/25)`. Kept verbatim, including
`st_n(0)=0` (recorded per the F6 verdict's open observation; no pricing fork
— out of scope).

### D7. Cite-lock signals on all four priced paths

The F6 workstream wired signals only into `st_kill_evidenced`/`st_overwrite`
(it had no delete path or trainer kill). The port wires `st_citelock_signal`
into all four priced wrappers that can return 121: `st_kill` (trainer path
only — TNN-role calls return 113 before any effort check), 
...[truncated 2948 chars]
