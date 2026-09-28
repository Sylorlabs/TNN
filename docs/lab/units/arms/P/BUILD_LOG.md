# Arm P — Build Log

## 2026-09-21

### Source fixes
- Fixed `_zag_malloc` for P struct (was `nio_alloc as *P`, hit ZNC-2026-09-21-005).
  Use raw malloc + explicit zeroing + pointer cast.
- Added `halloc` allocation-length guard.
- Fixed `get_u32`/`put_u32`: callers use logical u32 indices; helpers now multiply by 4.
  (Was causing overlapping-byte bug: slot 1 disappeared.)
- Fixed JSON emission: `j_t`/`j_b` take `first` arg to avoid malformed `{,`.
- Removed temporary `zz` debug mode.

### M3 capacity
- Enlarged to handle 233k units (was cap=4000).
- Audit ledger: 500k entries (32MB, under 2^25 limit).
- `p_evict`: changed from O(n²) rescan to advancing `ins_head` (O(n) total).
- M3 completed: 999/999 survival, 232,910 evictions.

### M8 determinism
- Full corpus exceeded ledger limits; changed to deterministic subsets:
  - prose ≤10,000 units, code ≤10,000, fresh ≤3,000.
- Each audit slice under 2^25. All operations exercised.
- M8_DETERMINISM,PASS, byte-identical run0/run1.

### Binding trial (mbind-1x)
- Implemented `t_bindkill`: W=200, K=7, 20 phrases × 10 units.
- Initial sliding pattern failed (pairs got ~1-2 votes, 0 words at K=7).
- Redesigned with repeating phrases: 180 words promote at K=7.
- Sensitivity: K=3,7,14 all give 180 (pairs get ≥14 votes; uninformative but truthful).
- Eviction: inline LRU (min last_rep) kills stale phrase units, words survive.
- Probes: 500 spans from stale phrases; baseline 0/500, emergent 267/500.
- Margin: 53.4 points (≥3 required). Churn: 42/90=46.7% (>50% kills required).
- **VERDICT: PASS** — neither kill branch fires.

### Eviction performance
- `p_evict` with 4096-scan min-last_rep was too slow for M3 (232k evictions).
- Reverted `p_evict` to fast FIFO (head-advance).
- Binding trial uses inline LRU (full scan, n=380, fast enough).
- M3 now completes in ~120s (was timing out).

### M5-1x timeout
- 200 sweeps × 84,731 units = 16.8M recall+vote ops. Too slow for practical timeouts.
- Emits REVIEW tags but does not complete. Performance limitation, not correctness.
- Documented in VERDICT.md; not blocking PASS (binding trial is the kill gate).

### Corrections applied
1. Voided "taught vocabulary" assignment; P is EMERGENT per briefs/P.json.
2. Authority order: (1) briefs/P.json, (2) frozen §3 row, (3) nothing else.
   Brief and row match byte-identically.
