# BUILD_LOG.md — ARM X (Degenerate, CTRL)

## 2026-09-21: Source implementation

Implemented `units/arms/X/cl/arm.zag` (one binary, argv[1] mode dispatch)
with BigBuf striped corpus loading, monolithic slot representation,
and M1–M8 modes. Substrate copied from B-64 and verified byte-identical.

### Compiler issues found and fixed
- `ns_sha256` requires output buffer as 2nd arg — fixed.
- `nio_open_write` does not exist — replaced with `nio_open_root` +
  `nio_open_child(..., 1)`.

### Ambiguity A6/M6 (memorizer mapping)
Not applicable to X's implementation; X's m6 reports transfer-phase
recall/boundary/revision/tax in canonical field names.

### Field-name alignment (2026-09-21)
Initial implementation used invented JSON field names. Rewrote all
emissions to the frozen canonical names from b64 + scorecard_assemble.py:
- M1: m1_recall_tenths, m1_boundary_tenths, m1_units, m1_corpus
- M2: m2_episodes, m2_censored, m2_ep0_recall_tenths,
  m2_final_recall_tenths, m2_final_boundary_tenths,
  m9_shape, m9_takeoff_ep, m9_steepness_tenths, m9_late_gain_tenths
- M3: m3_survival_tenths, m3_fresh_recall_tenths, m3_mgmt_entries,
  m3_weaken_handled, m3_freeze, m3_valuable
- M4: m4_rev_boundary_tenths, m4_rev_content_tenths, m4_kill_rate_tenths,
  m4_killsub, m4_episodes
- M5: m5_units_learned, m5_source_bytes_learned, m5_slot_table_bytes,
  m5_ledger_bytes, m5_ledger_entries, m5_corpus_buffer_bytes
- M6: rec_tenths, bnd_tenths, rev_tenths, tax_tenths (transfer phase)
- M7: null hit/reuse/dedup, m7_na_reason, m7_reread_bytes
- Envelope: `METRIC_JSON {"schema":"metrics-v1","arm":"x","round":"r1",...}`

### M6 revision units fix
Initial code computed revision in wrong units (1.0 instead of 100.0).
Fixed to b64's formula: rev_tenths = verified_count × 10.

### M8 artifact compliance
Rewrote t_m8 to emit the gate's exact file set:
store_hashes.txt ("chunk0 <64-hex>"), store_chain.txt, ledger.bin,
ledger_chain.txt, alloc_trace.txt (op/size trace, no addresses).
Removed binary-written GATE.txt (gate script decides). Manifest made
perturbation-agnostic.

### M7 lookup count
X_M7_LOOKUPS=5000 protocol parity, but each X lookup scans 5.4MB with no
index (27GB total, ~45 min). Reduced to 500 lookups (2.7GB) with
documented rationale. M7 is N/A for X regardless.

## 2026-09-21: Battery execution

Built memorizer control from frozen harness source. Ran full 1x battery:
18 legs via run_metric.sh (double-run, byte-identical), M8 gate via
m8_gate.sh (5 perturbations × 2 reruns).

Results:
- All 18 legs: rc=0, stdout IDENTICAL, no FATAL.
- M8 gate: M8GATE PASS (all 10 runs byte-identical artifacts).
- Scorecard assembled with tools/scorecard_x.py (arm label "x").

### 10x
NOT RUN. M1 boundary bar (100.0) cannot pass by frozen design (M-3:
X reports 0.0). X is the null control; 10x conditional not met.

## Evidence
- `scorecard_r1_1x.json` — assembled 1x row.
- `logs/` — per-leg STATUS.txt, fragment.jsonl, m8/GATE.txt.
- `VERDICT.md` — final verdict.
