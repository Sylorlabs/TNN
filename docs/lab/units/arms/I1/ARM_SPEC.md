# ARM I1 — Strict Tree Hierarchy (`STRUCT`) — Specification

**Track:** A (representation bake-off)
**Arm ID:** I1
**Mechanism:** Strict tree hierarchy
**Frozen prereg:** `sylorlabs/TNN`, branch `tnn-native-lab`, commit `b0b9140c0eda`
**Date:** 2026-09-21

## 1. Mechanism

I1 organizes knowledge as a strict tree hierarchy:

- **L0:** Finest chunks (64-byte units, the atomic storage quantum).
- **L1-L4:** Superchunks formed from runs of 2–8 adjacent same-level chunks.
- **Formation:** After `T_co=7` co-recalls (or deliberate promotion), adjacent runs form a parent superchunk.
- **Single parentage:** Each unit has at most one parent; IDs are level-scoped.
- **Traversal:** Top-down (parent → children) and bottom-up (child → parent) both supported.
- **Maximum level:** 4.
- **Demotion:** After `E=3` unresolved quiet episodes (provisional pending freeze), units demote.
- **Revision:** Marks ancestors stale; stale parents must be rebuilt or dissolved, never silently served.

## 2. ID Scheme

`id = (level << 27) | (corpus << 23) | (serial & 0x7FFFFF)`

- Level: bits 31..27 (0..4)
- Corpus: bits 26..23 (0..9, I1_CSLOT=10)
- Serial: bits 22..0 (23-bit, 8M per corpus/level)

## 3. Formation Dynamics (Validated)

The `probe-formation` mode confirms:
- Episodes 1–6: Zero L1 formations (threshold not reached)
- Episode 7: L1 forms (T_co=7 reached)
- Run length: 8 (default gsize=8, within 2..8)
- 512 L0 units → 64 L1 superchunks (512/8)
- Single parentage enforced
- Adjacent spans only (offset continuity verified)

## 4. Binding Kill Criteria

### (i) L2+ superchunk recall <5% vs flat comparator → KILL
- **Status:** NOT-IMPLEMENTED
- Requires genuine flat comparator with equal measured store cost.

### (ii) Maintenance + stale rebuild >20% of audit ops (per corpus) → KILL
- **Status:** SURVIVE (measured 12.4% on corpus 9)
- Maintenance = form + dissolve/demote + stale-mark
- Measured via per-corpus `mc` counters.

### (iii) L1 boundary agreement <50% with natural breaks → KILL
- **Status:** BLOCKED (natural breaks undefined)

## 5. Modes

One binary; `argv[1]` selects mode (lowercase, e.g. `m1-1x-prose`).

| Mode | Description |
|------|-------------|
| `m1-1x-prose`, `m1-1x-code` | Recall + boundary + ID probe |
| `m2-t1-prose`, etc. | Transfer episodes (T1/T2/T3) |
| `m3-1x` | Management liveness (PIN/WEAKEN/KILL/EVICT) |
| `m4-1x-prose`, `m4-1x-code` | Revision with boundary defects |
| `m5-1x` | Store cost (bytes-per-byte) |
| `m6-p2c-1x`, `m6-c2p-1x` | Cross-corpus transfer |
| `m7-1x` | Corruption dissociation (BLOCKED: A7/A8) |
| `m8-1x` | Determinism under perturbation |
| `probe-formation` | Formation dynamics validation |
| `kill-ii` | Binding kill (ii) measurement |

## 6. Determinism

Zero randomness. All behavior deterministic given state. Byte-identical reruns verified.

## 7. Implementation Notes

- Language: Pure Zag (no Python)
- Single binary: `cl/arm.zag` → native via znc
- Slice limit: No single slice >2^25 bytes (chunked ledgers)
- ID packing: 23-bit serials, level-scoped
- Corpus slots: 10 (0..9); I1_C_M7P=9 for synthetic probes
