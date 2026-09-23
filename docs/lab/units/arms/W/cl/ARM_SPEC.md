# W — Multi-granularity — ARM_SPEC (design)

Status: Implementation spec for the r1 reimplementation. The frozen kill
criterion (briefs/W.json) binds; mechanism details below are the build's
concrete realization.

Frozen §3 row (verbatim, from briefs/W.json):
> W — Multi-granularity | STRUCT | Mechanism: Several grain sizes simultaneously;
> a selector with a justification gate picks per query; no single cut level. |
> Binding kill criterion: Any one: (i) composite battery score does not beat S
> alone by ≥15% — W is S with extra steps; (ii) justification gate refuses >5%
> of selections — the selector is unsound; (iii) determinism gate fails;
> (iv) floor rule fires.

## 1. Levels

Three segmentations maintained simultaneously over identical bytes:

- **L0 — 64-byte atoms.** Independent atom registry. Fixed 64B grid over each
  corpus, including a final partial atom (<64B) at the end of each corpus.
  Atoms are never merged. Each atom has a persistent ID
  `((corpus_id << 24) | offset)`.

- **L1 — S-rule crystallization.** At ingest, 64B atoms (mirroring L0 spans).
  Per episode, S's exact recall-event crystallization applies:
  - Record every unit's recalled/not-recalled flag for the episode.
  - For each adjacent live same-corpus pair: J++ if both recalled;
    Iu++ if the left is recalled without a recalled same-corpus neighbor.
  - Shift recall bits into an 8-episode trailing history.
  - Merge iff J >= 2 AND 5*J >= 3*(J+Iu+Iv) AND the two units' trailing
    histories match over all available bits in min(episode, 8).
  - Merge mints a new ID (with W_CHUNK_BIT), replaces constituents in the
    chronology, tombstones both (audited KILL reason 10), audits the merged
    ADD, and records merge-time J/Iu/Iv.
  - Split proposal (both variants): (Iu+Iv) >= 2*(J+1). Split at len/2,
    mints two IDs (W_FRAG_BIT), replaces the merged unit, tombstones it
    (audited KILL reason 11), audits two ADDs.
  - L2 variant "merge-only" (argv without "ms"): L1 uses merge+split
    (S-exact); only L2 is merge-only.
  - L2 variant "merge+split" (argv "ms" in positions 3..5): L1 uses
    merge+split; L2 also splits.

- **L2 — superchunks.** The S merge rule one level above L1, over adjacent
  live L1 chunks using joint chunk-scale recall. Constituents stay live
  (fusion, not replacement). L2 supers have IDs with W_SUPER_BIT.
  - Merge-only variant: fuse only, no split.
  - Merge+split variant: split scan also applies at L2.

## 2. Selector

Per query, exactly one granularity is chosen:

- **Bucket:** `(floor(log2(query_length)), corpus_id)`.
- **Rule:** Outcome-blind argmax of expected bytes saved, computed from
  logged counters (n, saved) per bucket per level. Evidence snapshot is taken
  BEFORE the query outcome (counterfactual: saved_lvl = max_cost - cost_lvl
  for every available level, where max_cost is over available candidates
  only).
- **Costs:** use actual dynamic lengths. L0 lookup count is ceil coverage
  (number of atoms covering the query), not `qlen/64`.
  - `cost_L0 = W_KQ + ceil_cover * W_KU + qlen`
  - `cost_L1 = W_KQ + W_KU + qlen` (one covering unit)
  - `cost_L2 = W_KQ + W_KU + qlen`
- **Tie-break:** finer level wins (preserves boundary metric; coarser wins
  only on strictly greater expected savings).
- **Justification gate:** independent recomputation of the identical rule
  from the same snapshot. Disagreement => refuse (audited OP_REFUSE),
  counted toward the >5% kill criterion.
- **Committed:** `GRAN_SEL = 0x0B`.
- **Fast path:** 64B queries with L0 available skip the O(n) L1/L2 scans;
  L0 wins by finer-tie-break (evidence for 64B is always zero). Audited
  with a fast-path marker for determinism.

## 3. ID layer

Persistent ID→storage mapping (w_id_add/del/loc). IDs are deterministic
from span; tombstoned IDs never reused. Every atom is dual-registered
(L0 raw store + L1 base unit); the persistent map resolves each atom id to
its L1 copy (w1_ingest_atom's w_id_add overwrites w0_ingest's entry for the
same id). The M1 swap probe (A15) is labeled
**PROVISIONAL-PENDING-FREEZE**: the prereg mandates the probe but not the
remap schedule/function, so a true remap-and-verify probe cannot be built
without inventing the rule. Current implementation resolves each sampled id
live through the ID map and verifies the resolved (level,slot) is live and
its registered span matches the queried atom (r1.1: corrected — the old
check demanded the L0 slot and false-alarmed on the genuine L1 resolution).

## 4. Trial modes

One binary; `argv[1]` selects the mode, `argv[2]` the corpus dir,
`argv[3]` the outdir (m8-1x only), `argv[4]` the perturbation (m8-1x only),
`argv[3..5]` the variant ("ms" => merge+split). Scale is fixed "1x" (all
modes are 1x legs). (r1.1: dir moved from argv[4] to argv[2] to match the
shared harness convention; the old layout was self-contradictory.)

- `m1-1x-prose`, `m1-1x-code`: one episode, no consolidation. Reports
  m1_recall_tenths, m1_boundary_tenths, m1_units, m1_corpus, m1_id_probe
  (PROVISIONAL-PENDING-FREEZE), m1_materialized_bytes_avg.
- `m2-t1-prose`, `m2-t1-code`, `m2-t2-prose`, `m2-t2-code`, `m2-t3-1x`:
  episodes to criterion (content ≥99.5% AND boundary ≥95%, sustained 3).
  Episode 0 = probe with no ingest (must be ~0). Consolidation only after
  episode boundaries (merges first affect episode 2). T1 modes also report
  M9 descriptors (takeoff, steepness, late gain, shape).
- `m3-1x`: capacity pressure (C_M3=4000 slots, enforced manually).
  V=1000 pinned units; 3000 fresh ingest; 3000 kills; 50 weakens (refused
  on pinned, audited); 4000 fresh ingest with eviction. Reports survival,
  fresh_recall, mgmt_entries (audit-liveness), weaken_handled, freeze flag.
  r1.1 fix: w0/w1/w2_ord_remove now guard against unlinking a slot that is
  not in the order list. Previously wX_ord_append's remove-then-append
  collapsed the list to length 1 on every ingest (head/tail zeroed for fresh
  slots), so eviction took the newest unit instead of the oldest; M3 fresh
  recall collapsed to ~0% and the freeze flag fired spuriously. Fixed
  2026-09-21; M3 now survival 100%, fresh 100%, freeze CLEAR.
- `m4-1x-prose`, `m4-1x-code`: 200 units, 100 boundary + 100 content defects,
  revision episodes (max 20). Reports rev_boundary, rev_content, kill_rate,
  killsub, episodes.
- `m5-1x`, `m5-baseline`: memory footprint. Full prose + 1000-step pressure.
  Reports units_learned, source_bytes, slot_table_bytes, ledger_bytes,
  ledger_entries, corpus_buffer_bytes.
- `m6-p2c-1x`, `m6-c2p-1x`: interference. Train to M2 criterion on T1,
  freeze policy (no consolidation), transfer to other T1. Reports rec, bnd,
  rev, tax (signed mean difference).
- `m7-1x`: BLOCKED pending Micah freeze of A7/A8. Reports m7_na_reason.
- `m8-1x`: determinism gate (r1.1: implemented — ingest prose+code, full
  recall sweep, 2,000 varied-length selector queries, one consolidation
  episode, scaled M3 pressure; artifacts: per-chunk ledger hashes, registry
  id-array hashes, alloc trace; stdout `M8,cok,bok,led,sel,ref`).

## 5. L2 variants

Both variants share the L0/L1 core. Differences:
- **Merge-only** (default): L2 fuses adjacent chunks on joint recall;
  no L2 split.
- **Merge+split** ("ms"): L2 also runs the split scan
  ((Iu+Iv) >= 2*(J+1)).

L1 uses S merge+split in BOTH variants (S-exact); only L2 changes.

## 6. Determinism

Zero RNG in any decision path. Byte-identical reruns required (ordinary
modes run twice). The M8 gate (perturbations: clean, frag, aslr, starve,
freelist) is implemented in r1.1 (`t_m8`); frag/aslr perturb the heap before
`w_new`, freelist/starve are documented no-ops per A11.

r1.1 changes: placement-hint optimization in `w0_place`/`w1_place`/`w2_place`
(provably identical lowest-free-slot assignment, amortized O(1)); selector
instrumentation (`sel_selections`/`sel_refusals` reported by every
query-serving mode); `m8-1x` implemented; CLI aligned to the shared harness
(`argv[2]` = corpus dir).
