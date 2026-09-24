# KB-CONTROL CREW B — Verdict

## Mechanism

**Journaled two-phase append-only writes with pointer-swap revisions.**

- One conscious record-byte write site, fenced by V1 (offset==total),
  V2 (capacity), V3 (target bytes zero).
- Revisions append a version at the tail; slot pointer swaps. Deletes
  tombstone. Re-adds include the old triple in the put intent for history.
- Framed, fsynced journal (intent + commit). Hash-chained ledger (81B/entry).
- Rollover advances by full chunk (4096B + 16B trailer with used/seq/KBCT).
- Recovery: journal replay with trailer-checked chunk synthesis; torn
  entries truncated (fail closed); uncommitted intents → DIRTY.

## Test results

| Test | Result |
|------|--------|
| T1: 20,000 deterministic appends | **PASS** — 48m41s, verify OK, 560 chunks |
| T2: 500 near-boundary + 500 arbitrary revises | **PASS** — 4m21s, verify OK, hist=1001 |
| T3: 200 deletes + 200 re-adds | **PASS** — 3m15s, verify OK, hist=1200 |
| T4: 120 crash trials (3 points × put/revise × 20) | **INCONCLUSIVE** — see below |
| T5: three byte-identical complete runs | **PASS** — SHA `69961a9da848bc54` ×3 |
| T6: conscious vs fast benchmark | **DONE** — 23.7× slowdown, 2.72× storage |

## Kill bars

- **K1 (zero cross-slot clobbers)**: **PASS**. 21,400 mutations, zero
  clobbers. The single write site makes cross-slot writes structurally
  impossible.
- **K2 (fail-closed crashes)**: **NOT PROVEN**. The earlier 120/120 T4 run
  was exploratory (weak harness, did not validate ledger consistency).
  A **known defect** exists: crash at point 3 (after journal commit, before
  ledger append) leaves a durable committed mutation without its ledger
  entry. Strict verify accepts this state; recovery does not reconcile it.
  Until the journal↔ledger completeness check and reconciliation are
  implemented and T4 is re-run with strong assertions, K2 cannot be claimed.
- **K3 (three byte-identical runs)**: **PASS**. All 598 files identical.
- **K4 (zero RNG)**: **PASS**. Grep-verified, no RNG in source or decision
  paths.

## Costs

- Appends: 6.85/sec conscious vs 162.6/sec fast (**23.7×**, under 50× bar).
- Storage: 447 bytes/fact vs 165 bytes/fact (**2.72×**).
- The journal (4.6MB) and ledger (1.7MB) dominate the overhead.

## Bugs found and fixed

1. **Trailer seq overlap**: `kb_rollover` wrote seq at `ch-12`, overlapping
   the 8-byte `used` field. Fixed to `ch-8`.
2. **Batch fp bug**: `kb_field_is` advances `fp` on mismatch; the "revise"
   and "delete" checks started mid-line. Fixed by resetting `fp=0`.
3. **Re-add history**: Put-on-tombstone orphaned the old record (census
   `unaccounted`). Fixed by including old triple in re-add put intents.

## Known unresolved defect

**Crash-after-commit missing ledger entry** (affects K2):
- Location: `kb_do_put`/`kb_do_revise`/`kb_do_delete`, `fail_after==3`.
- The commit frame (op=2/4/6) is journaled and fsynced BEFORE the ledger
  append. A crash in this window leaves a durable committed mutation with
  no ledger entry.
- `kb_verify` does not check journal↔ledger completeness; it accepts the
  state as OK.
- `kb_recover` replays the journal but does not reconcile the ledger.
- Required fix: (1) deterministic completeness check in verify, (2)
  reconciliation in recover (append missing ledger entries for committed
  mutations), (3) census binding every committed mutation to exactly one
  ledger entry, (4) re-run T4 with strong point-3 assertions.

## Verdict

**DOES NOT SHIP**. K1, K3, K4 pass. K2 is not proven due to the unresolved
ledger defect. The mechanism is sound (single write site, explicit journal,
deterministic replay), and the measured costs (23.7× slowdown, 2.72×
storage) are within bars. But the crash-after-commit ledger gap must be
closed and T4 re-run before this can ship.
