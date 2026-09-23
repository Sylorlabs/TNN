# ARM I1 — Verdict (1x)

**Date:** 2026-09-21
**Scale:** 1x
**Mechanism:** Strict tree hierarchy (STRUCT)
**Verdict:** **KILLED** — binding kill (ii) fired on real-corpus measurement.

## Summary

I1's strict tree hierarchy builds a genuine, fully-cascading pyramid (L1→L4, single parentage, T_co=7 confirmed) and recalls through it with 100% fidelity. It survives kill (i) with enormous margin and passes the M8 determinism gate 10/10 byte-identical. But on real corpora at real scale, parent maintenance + stale rebuild consume **22.1% of prose's audit ops**, exceeding the frozen 20% kill bar. **Any one binding kill criterion kills I1 — kill (ii) fired. I1 is dead.**

The earlier 12.4% "survive" was measured on a 512-unit synthetic corpus that could not form L2+ superchunks; it understated maintenance at scale and is superseded.

## Binding Kills

### Kill (i): L2+ superchunk recall <5% vs flat comparator → SURVIVE
- **Method:** `kill-i` mode. Phase H: ingest prose (84,731 units), 28 formation episodes, recall every L0 through `recall_hier` (up to topmost live ancestor and back down, byte-verified vs corpus; broken chains fall back to flat `recall_unit` and count as successful-but-not-L2+). Phase F: identical cap (equal allocated store cost by construction), identical ingest, no formation, flat recall.
- **Result:** live superchunks L1=10,592, L2=1,324, L3=166, L4=21 (full 8-wide cascade: 84731→10592→1324→166→21). Hierarchical recall 84,731/84,731 byte-exact; flat 84,731/84,731; **L2+ share = 100.0%** (1000 tenths) vs 5% bar.
- Every recall traverses a level-2+ ancestor. The hierarchy is not decorative. **SURVIVE** with 20× margin.

### Kill (ii): Maintenance + stale rebuild >20% of audit ops (per corpus) → KILL
- **Method:** `kill-ii` mode on REAL corpora. Workload mirrors the battery's operational mix: ingest of all 1x corpora (prose, code, t1/t2/t3 tiers), 20 formation episodes each on prose and code (parent maintenance), a 100-boundary + 100-content defect/revision sweep on prose and code through the real revision API (stale cascades), and the M3 churn schedule on fresh (management ops). Per-corpus counters from the ledger: maintenance = formation ADDs + dissolve/demote KILLs + CAUSE_STALE REVISEs; total = every audit entry.
- **Result (final binary, deterministic):**

| Corpus | Maint | Total | Ratio |
|--------|------:|------:|------:|
| 1 (prose) | 24,164 | 109,295 | **22.1% — KILL** |
| 2 (code) | 21,230 | 170,308 | 12.4% |
| 3–8 (tiers/fresh) | 0 | — | 0% |

- **22.1% > 20%: kill (ii) fires on corpus 1 (prose).** The deep hierarchy that makes kill (i) pass is exactly what makes kill (ii) fail: every formation episode's rehearsal, re-formation, demotion sweep, and stale cascade is a maintenance op, and at 84K units the pyramid's upkeep dominates the audit trail. In steady state (ingest one-time, maintenance ongoing) the share only grows.
- The prior 12.4% reading came from a 512-unit synthetic probe (corpus 9) that formed 64 L1s and nothing deeper — no L2+ cascade, no demotion pressure, no revision load. It is superseded, retained under `raw_logs/superseded-2026-09-21/`.

### Kill (iii): L1 boundary agreement <50% with natural breaks → BLOCKED (unresolved, not killing)
- "Natural breaks" has no operational definition in the frozen prereg §3. Exhaustive programmatic search of `PREREG_FREEZE.md`, the arm catalog, the harness, and `AMBIGUITIES.md` found no reference-break set and no matching rule. The old whitespace heuristic was removed from the source as an assistant invention (circular with this kill). No metric was invented. This bar is unexecutable as frozen; it does not kill I1, and the kill-(ii) verdict does not depend on it.

## Mode Results (1x, final binary `arm_final`)

| Mode | Result | Key metrics |
|------|--------|-------------|
| m1-1x-prose | PASS | 84,731 units; recall 100.0, boundary 100.0, ID probe PASS |
| m1-1x-code | PASS | 148,678 units; recall 100.0, boundary 100.0, ID probe PASS |
| m2-t1-prose/code | OK | etc=3 (≤3 ✓), ep0=0.0, not censored |
| m2-t2-prose/code | OK | etc=3 (≤5 ✓), ep0=0.0, not censored |
| m2-t3-1x | OK | etc=3 (≤5 ✓), ep0=0.0, not censored |
| m3-1x | **0 (FROZEN-UNDER-PRESSURE)** | V survival 100.0, fresh recall 0.0, mgmt 3050, 50 weakens |
| m4-1x-prose | PASS | boundary 100.0, content 100.0, 1 episode, no killsub |
| m4-1x-code | PASS | boundary 100.0, content 100.0, 1 episode, no killsub |
| m5-1x | METRICS | 2.94 B/B slot table, 3.18 B/B RSS delta, 18.3 audit entries/KB (all above 1.5/10 ranking bars; not kills) |
| m6-p2c-1x | PASS | recall/boundary/revision 100.0, tax 0.0; memorizer validity 54.8pt drop ✓ |
| m6-c2p-1x | PASS | recall/boundary/revision 100.0, tax 0.0 |
| m7-1x | N/A | I1 is STRUCT, not IDENT — per frozen M-33 non-ID arms are N/A |
| m8-1x | **PASS** | 10/10 runs byte-identical across 7 artifacts |
| m9 | info | fast-then-flat on all tiers |

## Forensic notes (post-kill, for the record)

1. **M3 freeze is a second, independent death.** The slot table is append-only: killed/evicted units keep `F_OCC`, so slots are never reclaimed. The M3 churn schedule (8,000 units through 4,000 slots) fills the table and the at-capacity phase freezes with 0 evictions. `FROZEN-UNDER-PRESSURE → M3=0`. A memory system that cannot reclaim space cannot survive churn; the distinguisher worked as designed.
2. **M4/M6 revision now genuine.** A real bug was found and fixed during this run: `read_span` used `nio_read_exact`, which has whole-file semantics and rejects `size>max_bytes`, so every 64-byte source read silently failed — M4/M6-revision could never score above 0. Fixed with true span reads via raw syscalls; M4 100/100 and M6 revision 100/100 are now real (byte-verified against corpus).
3. **M5 RSS measured externally.** In-binary `rss_kb` cannot read `/proc/self/statm` (proc files report size 0; substrate `nio_read_exact` fails). Per the freeze's "harness-measured RSS", peak RSS was measured externally: m5-1x 43,260 KB vs m5-baseline 26,428 KB → delta 16,832 KB = 3.18 B/source-byte.
4. **M7 correctly N/A.** The binary's `m7` mode implements a corruption-dissociation probe that does not match frozen M7; frozen M-33 excludes non-ID arms. Recorded N/A, not scored.

## Determinism

M8 gate **PASS** on the final binary via `harness/m8_gate.sh`: clean / frag / aslr / starve (LD_PRELOAD shim) / freelist × 2 reruns each. All 10 runs byte-identical on `store_hashes.txt`, `store_chain.txt`, `ledger.bin` (15,717,568 B), `ledger_chain.txt`, `alloc_trace.txt`, `stdout.txt`, `stderr.txt` (`m8_compare.py`: `M8GATE PASS`). Perturbation-agnostic stdout; free-list reversal is an accepted no-op (ID-derived placement, no free list — AMBIGUITIES.md A11); starvation surface is empty by construction (no entropy/clock reads in the binary).

## Conclusion

I1 is **KILLED** by binding kill (ii): on real prose at 1x scale, hierarchy maintenance consumes 22.1% of audit ops (>20% bar). The mechanism is real — the pyramid forms, recalls traverse it, revision works, determinism holds — but its upkeep is fatal at scale. No 10x run. The forensic battery is complete and committed for the record.
