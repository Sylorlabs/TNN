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
| M8 | INCOMPLETE — 1 run completed (old binary, rc=0); 10-run determinism gate not finished. New binary (freelist fix) hangs in M8, likely dedup stale-entry interaction with ID reuse. |

## Kill-criterion status

**BLOCKED.** The two binding kill cells cannot be resolved:

1. **Regretted-cut rate vs arm D:** The arm-D baseline was never built; per
   standing orders I do not invent it. The Z1 regretted-cut rate counter is
   not yet wired into the arm output. Cell status: UNRESOLVED.

2. **Challenge-set revision >10%:** The hypothetical-v2 probe is documented
   in ARM_SPEC.md but not implemented in the arm. The >10% kill cannot be
   evaluated. Cell status: UNRESOLVED.

The mechanism itself (challenge window with regretted cuts) is implemented
and functional: M1 shows ~57% of proposed grid cuts regretted on prose
(36k surviving of 84k proposed), all regrets audited.

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

## Procedural notes

- ARM_SPEC.md was written after compilation began; disclosed in BUILD_LOG.md.
- M3 was rerun with the fixed binary; all other modes' results are from the
  pre-freelist binary (behavior identical for modes without kill+reinsert;
  M4 metrics are content-based and unaffected by internal ID reuse).
- `cl/t28.zag` (compiler repro) was deleted, not committed.
- Build artifacts (`build/z1`, `build/compile.log`) are not committed.

## Verdict

**1x battery: INCOMPLETE — M8 pending.** All non-M8 bars pass. The binding
kill criteria are BLOCKED (no arm-D baseline; v2 probe not implemented).
No 10x run attempted.

**M8 note:** One M8 run completed with the pre-freelist binary (rc=0). The
freelist fix (required for M3) appears to introduce a dedup stale-entry
interaction that hangs M8: when a freelist-reused ID is reinserted, the old
dedup key still maps to that ID, and `z1_dedup_find`'s liveness check does
not verify content identity. Fix requires content verification in dedup_find
or old-key eviction on ID reuse. The 10-run byte-identical gate is not yet
demonstrated.
