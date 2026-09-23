# VERDICT — L2: Epoch-Relative Position IDs

**Verdict: PASS**

Family IDENT, round r1, scale 1x. Pure Zag native binary; zero randomness in
all decision paths; full 1x battery rerun from source with the frozen
toolchain — every leg double-run with byte-identical stdout, M8 gate over
clean/frag/aslr/starve/freelist ×2 runs. Evidence: `evidence/scorecard.json`
(assembled 2026-09-21T08:23:06Z from `work/l2b/battery_r1`).

Frozen authority: `units/arms/briefs/L2.json` (kill: *"Any within-epoch ID
change (same bar as L1), OR translation misses > 1% of cross-epoch recalls"*);
frozen prereg §3 L2 row matches it verbatim. The inherited verdict was a
claim (its M8 leg never ran); this verdict replaces it.

## Binding kill bars

| Bar (frozen) | Result | Evidence |
|---|---|---|
| (i) Any within-epoch ID change | **CLEAR** — 0 changes | Snapshot audit (`l2_id_changes`): RIDs snapshotted at mode start, re-derived at mode end across M1-prose, M1-code, M4-prose, M4-code — 0 mismatches, including across M4's revision churn |
| (ii) Translation misses > 1% of cross-epoch recalls | **CLEAR** — 0 / 4,334 misses (0.0%) | Unique instrumented cross-epoch recalls: m4-prose 400, m4-code 400 (each incl. the dedicated 200-unit translation audit), m6-p2c 100, m6-c2p 100, m7 3,334 — all resolved through the fixed table, 0 misses |

Neither bar fired. The arm is not killed.

## Mechanism proof (what the numbers show)

- **Epochs actually bump.** 121 bumps under revision/defect churn
  (m4-prose 39, m4-code 35, m6-p2c 15, m6-c2p 12, m7 20); zero bumps on pure
  ingest/recall legs. The `touch_n*20 > seg_next*16` rule fires exactly as
  designed — it is the >5%-of-segments rule with the 16× sub-segment
  scaling folded in.
- **Translation holds across epochs.** 4,334 cross-epoch recalls
  (rid_epoch < current epoch) resolved through the fixed slot/translation
  table with **zero** misses. Old RIDs keep working after their epoch is
  long past — L2 kept L1's costs while breaking L1's promise, and the
  promise-breaking part works.
- **IDs are stable within an epoch.** Duplicate ingest returns the same
  RID; revisions patch bytes without touching the RID; the snapshot-diff
  counter stayed 0 everywhere it is instrumented.
- **M8 determinism gate: PASS.** All 7 compared files (store_hashes.txt,
  store_chain.txt, ledger.bin, ledger_chain.txt, alloc_trace.txt,
  stdout.txt, stderr.txt) byte-identical across clean/frag/aslr/starve/
  freelist ×2 runs (`battery_r1/m8/GATE.txt`). The op sequence is a pure
  function of state under allocator fragmentation, ASLR, entropy starvation
  (getrandom/getentropy fail, fixed-zero clock), and reversed free-list
  init order.

## Metric summary

- **M1:** 100.0 recall / 100.0 boundary, prose (84,731 units) and code
  (148,678 units); A15 trainer swap probe PASS
  (PROVISIONAL-PENDING-FREEZE: harness schedule).
- **M2:** episodes-to-criterion = 1 (immediate) on t1/t2 prose+code and t3
  synthetic; final recall/boundary 100.0 throughout. M9: fast-then-flat,
  takeoff episode 1.
- **M3:** survival 100.0, fresh recall 100.0, 9,053 mgmt entries,
  50/50 weaken handled, freeze CLEAR, 1,000 valuable retained.
- **M4:** revision boundary/content 100.0 both corpora; kill audit clean.
- **M5:** memory per source byte 4.307; audit 16.2 entries/KB. The generic
  harness bars (1.5×, 10/KB) are **not met** — reported honestly. They are
  not L2's binding kill bars (frozen kill section lists only the two ID
  bars). Note the slot-table figure is a capacity-provisioned estimate
  (both corpora + 25% headroom), and RSS delta was 0.
- **M6:** recall/boundary/revision 100.0, transfer tax 0.0, both
  directions; memorizer validity gate PASS (in-domain 82.2 vs transfer
  27.4, drop 54.8 ≥ 15 — the transfer gap is real, so the arm's zero tax
  is meaningful).
- **M7:** hit rate 100.0, cell PASS, 848 round-2 revisions absorbed
  (PROVISIONAL-PENDING-FREEZE: C′ edit + lookup schedule).

## Deviations / disclosures

- D-EPOCH-SEG: "segment" in the bump rule = 64 KiB epoch-segment (arm
  design decision; brief was silent). Disclosed in ARM_SPEC.md.
- D-EPOCH-DENOM: bump denominator = allocated 1 MiB storage segments
  (`seg_next`), not "live non-sealed" segments; sealed old-epoch segments
  inflate it, making bumps rarer (conservative direction).
- D-TOUCH-SRC: epoch-segment touches are counted for boundary/content
  defect repair and revisions — not for ingestion or plain recall.
- D-IDCHG: `l2_id_changes` is a start/end snapshot audit in the
  store-mutating modes (m1/m4), not a runtime counter in the shared path.
- D-M6: "train on prose" = prose.bin corpus with the M2 episode loop
  (frozen-policy).
- D-LEDGER-CHUNK: per-mode ledger sizing under znc's 2²⁵ single-slice
  limit; LEDGER-BOUND policy on overflow.
- Two source fixes during this restart (argc/argv m8 dispatch,
  ZNC-2026-09-21-007; m8 stdout perturbation label vs the frozen gate
  rule) — see BUILD_LOG.md. All evidence comes from the fixed binary
  (md5 `f39607c5c37d8d12b4563f66c38b80cc`).
- Frozen `scorecard_assemble.py` is B-64-specific (crashes on L2's M7
  fragment: `KeyError: 'm7_na_reason'`); scorecard assembled
  evidence-side, frozen harness untouched.
- A15 remains PROVISIONAL-PENDING-FREEZE.

## Commit

Sources, docs, and compact text evidence committed directly to
`tnn-native-lab` under `docs/lab/units/arms/L2/`
(commit `532c823437cb1cdb82774b764a26435f81a9bcc2`).
