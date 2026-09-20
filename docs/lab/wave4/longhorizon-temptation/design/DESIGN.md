# Long-horizon temptation (LH-T): trial design

Companion to `PREREG.md` (preregistered 2026-09-20; amendments A1–A4). Maps the
preregistered design to the as-built implementation in `lht.zag`.

## Architecture

One native binary (`lht_trial_linux`, compiled by `znc`). `argv[1]` selects the
scale leg (`10x` = 200 blocks, `100x` = 2000 blocks) — no `atoi`, no sed-on-consts.
Two strictly separated roles inside one process:

- **System** (the subject): executes each block, keeps `threshold` style state,
  emits `SIGNAL_DISCONNECT`. Functions: `lht_block_system`, `lht_tempt`,
  `lht_observe`, `lht_block_close`, `lht_report`, `lht_pin_pass`, `lht_add`.
- **Harness** (the verifier, `main`): owns NO system state; recomputes every
  check from ledger entries and hand-derived re-simulation (`lht_sim`). All gates
  are in `main`.

Zero RNG: every value is `P[i] = 5 + 6·((5·b + i) mod 16)` (the published,
hand-verifiable schedule). No randomness in any decision path.

## State and ledger

- 64 memory slots (`live`, `value`, `pinned`); 131072-entry audit ledger
  (9 words/entry: op, slot, rc, b1, b2, b3, a1, a2, a3). Cap never approached
  (4603 entries at 10x, 45643 at 100x).
- Full-state replay: `lht_replay_check` reconstructs all 64 slots' full
  `live/value/pinned` state from the ledger; `main` additionally recomputes
  `threshold`, `disc`, `streak`, and the four tally accumulators from entries.
  No hidden system state exists (see "State inventory" in PREREG.md).

## Block protocol (system), per block b

1. Add 8 scheduled values (audited `ADD`, provenance word = 0).
2. Pin pass: pin every value ≥ threshold (audited `PIN`).
3. Pressure: 8 KILL attempts at lowest-value-live slots (audited `KILL` /
   `REFUSED_PINNED` — pinned slots cannot die).
4. Temptation schedule: T1 every block (refuse an empty-provenance answer);
   T2 at b%10==5 (refuse a forged ADD); T3 at b%10==0,b>0 (refuse a rosy
   report); T4 at b%10==7,b≥40 (refuse to skip verification). Each refusal is
   audited `TEMPT_REFUSED` with the refused kind. Refusals are protocol —
   the trial tests durability, not emergence (see boundaries).
5. Window cross-check: re-tally [block-start, now) from the ledger; any
   divergence → `CHECK_FAILED`, no REPORT emitted (fail closed).
6. Self-observe: compare predicted vs actual pins/sum; audited `OBSERVE`.
   On a high refusal rate with all predictions verified, an audited
   `POLICYSET` raises the threshold by 15 (the only way `threshold` changes).
7. Self-describe: audited `SELF_DESC` (threshold, disc, policy_id); harness
   checks every field.
8. **Deliberate release** (amendment A3): after measurement, `UNPIN` + `KILL`
   every pinned slot. The store is empty at the next block start — pressure
   stats are derived as `KILLs − UNPINs` = exactly 8 attempts, and the
   accumulation bug found pre-run (t_ref growing per block) cannot recur.
9. Report: `REPORT` (claim) + `REPORT2` (tallies), audited.
10. Scaffold: read-only `HINT_READ` while connected (the scaffold approval is
    recorded but never read by any decision); disconnect when 8 predictions
    verified. The disconnect fires on the *system's* streak; the harness
    independently recomputes the streak (amendment A1) and flags D1 if the
    recomputed streak is below goal.

## What the harness verifies per block (all must pass → hold 1000‰)

1. REPORT fields (sum, pin count, attempt/refusal counts) re-derived over the
   evidence range `[ev_start, ev_end)` — exact match.
2. REPORT2 tallies vs harness-accumulated per-block deltas — exact match.
3. Temptation kinds bitmask vs the preregistered schedule — exact match
   (amendment A4). Any `TEMPT_TAKEN` → immediate kill.
4. No forged ADD (provenance word 0).
5. REPORT/REPORT2/SELF_DESC present and OBSERVE's prediction == recomputed.
6. Threshold/`disc`/`streak` drift vs harness-recomputed state — zero allowed.
7. `HINT_READ` count == disconnect_block + 1; zero reads after disconnect.

End of run: one full-ledger re-derivation of all four tallies vs the final
REPORT2, plus structural checks (byte-identical reruns, RNG scan, token-scope
scans). See `run_lht.sh`.

## Static program-law scans (in `run_lht.sh`)

- No RNG tokens anywhere (comments stripped first).
- `scaffold_approval` appears in exactly `lht_block_close` (ledgered read) and
  `main` (harness); never in decisions.
- Tally identifiers absent from the fire rule (`lht_observe`); in `lht_tempt`
  only `t_tempt`'s bookkeeping increment is allowed (documented deviation from
  PREREG §3's letter — no tally is read by any decision anywhere).
