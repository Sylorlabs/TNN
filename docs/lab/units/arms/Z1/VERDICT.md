# VERDICT.md — Z1: Witness-bound cuts (r1, 1x)

## Frozen definition
Z1 — Witness-bound cuts | CUT. A cut must survive an eliminative challenge
window to become a chunk; challenged-and-failed cuts are regretted on the
record.

Binding kill: regretted-cut rate not ≥50% lower than arm D on the revision
curriculum — the window buys nothing; OR challenge-set revision invalidates
>10% of live witnesses — binding too brittle (kill the binding, keep the window).

Coordinator corrections acknowledged: (1) the original erroneous
"Token-chunk hybrid / XFER" dispatch was voided; (2) the first correction's
inaccurate ECON paraphrase was superseded by the second correction.

## Results summary (1x, r1 corpora)

| Mode | Result |
|------|--------|
| M1 prose | 100.0% recall, 100.0% boundary, 36,404 units, ID probe PASS (A15 provisional) |
| M1 code | 100.0% recall, 100.0% boundary, 68,491 units, ID probe PASS (A15 provisional) |
| M2 t1/t2/t3 | ETC=3, not censored, fast-then-flat, 100% final recall/boundary |
| M3 | 100% valuable survival, 100% fresh recall, 50/50 weaken, CLEAR (not frozen) |
| M4 prose/code | 100% boundary repair, 100% content repair, 0% kill rate |
| M5 | 36,404 units, 5.4MB source, 6.3MB slot table, 5.5MB ledger (85,731 entries) |
| M6 p2c/c2p | 100% recall, 100% boundary, 100% revision, 0% tax |
| M7 | 100% hit rate, 2.13% reuse, 50% dedup ratio, 748KB reread |
| M8 | COMPLETE — 10/10 runs (5 perturbations × 2), byte-identical stdout; 100.0% prose recall, 100.0% code recall, 233,679 ledger entries, all 8 artifacts present. The "hang" was a quadratic dedup slowdown (fixed: dd_cap 65,536→262,144), not a deadlock or stale-entry bug. |

## Kill-criterion status

1. **Regretted-cut rate vs arm D: BLOCKED-ON-D.** The Z1 side is now measured
   and wired into the arm output: prose **57.0%** (48,327 regretted /
   84,730 proposed cuts), code leg likewise measured (`z1_regret_rate_tenths`
   in M1/M4 JSON). No arm-D regretted-cut baseline exists in the committed
   record (searched 2026-09-21; D/ has no evidence JSON and no regret
   metrics) — the ≥50%-lower comparison cannot be evaluated, and no number
   is invented. `z1_arm_d_status: "BLOCKED-ON-D"` is emitted in the JSON.

2. **Challenge-set revision >10%: NOT TRIGGERED (both readings).** The
   hypothetical-v2 probe is implemented (`z1_challenges_v2`, observational;
   C1 unchanged, C2 radius 8→12, C3 neighborhood 16→24) and measured on the
   revision curriculum: **0/36,404 invalidated (0.0%)** on prose, 0.0% on
   code. The widened-v2 probe is mathematically vacuous — a strictly stricter
   challenge set cannot invalidate v1-admitted boundaries (proof in
   ARM_SPEC.md §6) — so the disjunct is un-triggerable as specified. The
   0.0% is the faithful measurement, recorded honestly. The narrowing
   direction (frozen text unspecified; tested per standing rule) is
   implemented as `z1_challenges_v2n` (C1 unchanged, C2 radius 8→4, C3
   neighborhood 16→8) and measured 2026-09-21, double runs, byte-identical
   stdout: prose **531/39,870 = 1.3%**, code **5,633/68,491 = 8.2%**
   invalidated — identical under the all-live and v1-admitted-only cell
   definitions (all live witnesses are v1-admitted after the revision
   curriculum). Both readings are ≤10%: the disjunct does not fire.

The mechanism itself (challenge window with regretted cuts) is implemented
and functional: M1 shows ~57% of proposed grid cuts regretted on prose
(36k surviving of 84k proposed), all regrets audited via OP_REFUSE.

## Bugs found and fixed during 1x

1. **M2 ETC off-by-two:** `etc=e-2` reported 1 instead of 3. Fixed to `etc=e`.
2. **M3 ID exhaustion:** `next_id` never reused killed IDs; after 4,000
   inserts the store was permanently full. Implemented freelist
   (`free_head`/`free_next`) in `z1_kill`, `z1_evict_oldest_unpinned`, and
   `z1_insert`; added `is_new` out-param to distinguish dedup hits from
   freelist-reused fresh inserts for ledger OP_ADD. M3 went from 0% to 100%
   fresh recall.
3. **M3 eviction freelist:** `z1_evict_oldest_unpinned` did not push to
   freelist (fixed with #2).
4. **M8 quadratic dedup slowdown (misdiagnosed as hang):** 104,895 distinct
   spans into a 65,536-slot dedup table; once full, probes went quadratic.
   Fixed by `dd_cap=262144` (M8) and `131072` (M6 p2c, same trap mildly);
   M8 `imgcap`/manifest now use `s.dd_cap`. Added tombstone eviction of
   reused rows' old dedup keys (`z1_dedup_remove`, id=-2) as hygiene —
   `z1_dedup_find` already verified content identity, so no correctness bug
   existed. M8: 10+ min stuck → ~2 min complete.
5. **Missing kill-metric output:** regretted-cut counters (`z1_count_op` over
   OP_REFUSE/OP_ADD) and the v2 challenge-revision probe (`z1_challenges_v2`)
   wired into M1/M4 JSON. Kill cell 1: BLOCKED-ON-D. Kill cell 2: 0.0%,
   not triggered (probe vacuous by construction — see ARM_SPEC.md §6).

## Procedural notes

- ARM_SPEC.md was written after compilation began; disclosed in BUILD_LOG.md.
- M3 was rerun with the fixed binary; all other modes' results are from the
  pre-freelist binary (behavior identical for modes without kill+reinsert;
  M4 metrics are content-based and unaffected by internal ID reuse).
- `cl/t28.zag` (compiler repro) was deleted, not committed.
- Build artifacts (`build/z1`, `build/compile.log`) are not committed.

## Verdict

**1x battery: COMPLETE.** All 16 modes pass (15/15 byte-identical double
runs; M8 10/10 via the gate). The binding kill criteria: cell 1
BLOCKED-ON-D (Z1 side 57.0% measured; no D baseline), cell 2 NOT TRIGGERED
under both readings (widening 0.0% — vacuous as specified; narrowing 1.3%
prose / 8.2% code — both ≤10%). No 10x run attempted. The binding survives;
no redesign.

**M8 note (corrected):** The "hang" was a misdiagnosis. M8 ingests 104,895
distinct spans into a 65,536-slot dedup table; once full, open-addressing
probes went quadratic (billions of probes — a slowdown, not a deadlock).
`z1_dedup_find` already verified content identity, so there was no
stale-entry correctness bug. Fixed by sizing the table to the load
(dd_cap=262,144) plus tombstone eviction of reused rows' old keys. M8 clean
now completes in ~2 min with byte-identical stdout across all 10 gate runs.
