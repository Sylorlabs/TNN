# G1 ARM_SPEC — Pressure-driven coarsening (family CUT)

**Status:** KILLED (see DEATH_CERTIFICATE.md)  
**Prereg:** frozen commit b0b9140c0eda, branch tnn-native-lab  
**Mechanism source:** ALPHABET_G-L.md §G1 (observed 2026-09-21)

## 1. Mechanism (frozen)

- Occupancy = live_slots / capacity (pure function of logged state).
- WARN at 80%, CRITICAL at 95% (frozen integers).
- At CRITICAL, triage: pick lowest-value *adjacent* chunk pairs (MA4 signed value, tie → lowest slot, deterministic), coarsen via `add(superchunk covering both spans)` + `kill(left)` + `kill(right)`, audited (`OP_ADD` + 2× `OP_KILL` + `OP_MERGE` linking the three).
- Pinned chunks (incl. human force-pins) immune, never selected.
- Negative-value chunks selected first (triage spends them first).
- Incoming stream cut policy: at ≥WARN, new chunks cut at 2× current mean live length until occupancy drops strictly below WARN (hysteresis).
- Bytes never lost: kills drop records; spans remain addressable in append-only byte store; `OP_MERGE` stores both cut points so later deliberate re-split (`OP_SPLIT`) is byte-exact.
- Implemented only from kill/pin/promote primitives + `OP_MERGE`; no new privileged op.

## 2. Kill criteria (frozen — any one kills)

1. **Thrash:** ≥5% of triage-merged superchunks re-split by deliberate revision same run → dies.
2. **Value-blindness:** byte-exact recall on pinned chunks drops >1% vs no-pressure control at matched occupancy → dies.
3. **Junk fusion:** ≥10% of superchunks never recalled nor re-split → dies.

No denominator minimum invented.

## 3. Implementation

**File:** `cl/arm.zag` (single binary; mode via `argv[1]`).  
**Compiler:** frozen `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

**Core structures:**
- Slot table: id-derived hash (order-independent), linear probe; fields: ids, offs, lens, corps, flags, shifts, pidx, vals, mleft, mright, mpar (all cap×u32/i32).
- Flags: F_OCC, F_LIVE, F_PIN, F_SUPER, F_TOUCH (recalled/re-split), F_SHIFT, F_PATCH, F_VAL.
- Dedup: (corpus,off,len)→serial; persistent serial mapping.
- Audit ledger: 64-byte entries (op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60). LEDGER-BOUND: stops when full, scored on what completed.
- Insertion-order queue (FIFO eviction fallback, audited policy_code=1).
- Allocation tracing (no addresses logged).

**Modes:** M1 (single-corpus recall + provisional N=64 trainer-remap probe, labeled PROVISIONAL-PENDING-FREEZE), M2/M9 (learning curve), M3 (churn: 1000 valuable pinned + 3000 fresh / 3000 kill / 50 weaken / 4000 fresh; cap=4000), M4 (defect 200, deliberate revision ≤20 episodes), M5 (cost accounting + baseline), M6 (transfer), M7 (provisional formulas), M8 (combined M1/M3 + 5 perturbations ×2, byte-identical artifacts).

## 4. Test results (1x partial)

| Mode | Result |
|------|--------|
| M1 prose | 100.0 / 100.0 (84731 units) |
| M1 code | 100.0 / 100.0 (148678 units) |
| M2 t1-prose | 100.0 / 100.0, 1 episode |
| M3 | survival 100.0, fresh 94.6, mgmt 18590, weaken 50/50; **K3 FIRES** (1102/1102 superchunks untouched = 100% ≥ 10%) |

**Verdict:** KILLED by criterion (iii) junk fusion. No 10x. See DEATH_CERTIFICATE.md.

## 5. Ambiguities (logged, interpreted literally)

- **A1:** M3 probe does not recall superchunk serials nor follow merge linkage; K3 fires on test design as much as arm behavior. Logged, applied literally.
- **A2:** K3 denominator: live superchunks (1102); total-ever (2404) same outcome.
- **A3:** K1 "same run" revision opportunity: M3 has no deliberate revision; M4 does. Evaluated per-run.
- M1 N=64 swap schedule: PROVISIONAL-PENDING-FREEZE (not frozen).
- M7 formulas: PROVISIONAL-PENDING-FREEZE.
