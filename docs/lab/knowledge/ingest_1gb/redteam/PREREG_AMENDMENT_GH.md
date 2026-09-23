# RED TEAM PREREG AMENDMENT — RT-G / RT-H (FROZEN)

**Date:** 2026-09-23. **Branch:** `tnn-native-lab`.
**Amends:** `knowledge/ingest_1gb/redteam/PREREG_REDTEAM.md` (commit `91bca241`).
The frozen prereg is adopted intact and unchanged; this amendment ONLY adds
two attack families ordered by the red-team mission, which the prior prereg
had placed out of scope: exploiting the two newly-known weaknesses —
the `igb_append` padding defect and the `sc_seal_tail` idempotency gap —
through the genuine revise/delete/seal path. All method rules and bars
B-RT1..B-RT4 of the frozen prereg apply unchanged.

**State note:** the gap crew has since closed the three data gaps (true
dedup: 3,565,287 unique facts; 55/55 CAL=OK; new seal
`93862fe1ea4a6944eae30b8fd1a72d27297860643658135ae85f12a03b9e306a`).
Both defects are verified STILL PRESENT in the current frozen
`knowledge/ingest_1gb/build/ingest.zag` (`igb_append` line 833:
`b.*.total=off+(reclen as i64)` — inter-chunk zero-padding never counted;
`sc_seal_tail` line 521 — no idempotency guard; the canonical
`adopt/s5_store.zag` already carries the guard, the ingest copy does not).
All batteries below prove their claims on replica stores built from that
frozen source with the pinned toolchain; the live sealed store is not
mutated.

## RT-G — Exploiting the `igb_append` padding defect

Setup: fresh 2-blob-chunk store (~260,000 records, >33,488,896 blob bytes)
via the genuine ingest binary (frozen source, pinned toolchain), so blob
chunk 1 exists and every slot in it carries a padding-short stored offset.

- **G1 (characterization):** pure-Zag walker: for every installed slot,
  compare the stored slot→blob offset against the true blob offset found by
  scanning blob chunks. Metric: wrong-offset slots per chunk.
  Expect: chunk-0 0 wrong; chunk-1 all wrong.
- **G2 (un-revisable plant):** revise 20 chunk-1 slots (deterministic stride).
  Expect 20/20 fail closed with "revise: id mismatch at offset".
  Attack thesis: a false fact planted in chunk ≥1 cannot be revised — only
  deleted — an accidental force-pin, violating "everything is reversible by
  TNN itself; the only true lock is a human force-pin".
  Kill criterion (defense holds): any chunk-1 revise succeeds AND the new
  text is retrievable via query.
- **G3 (successful revise as corruption primitive):** revise 5 chunk-0 slots
  (offsets correct there). Expect 5/5 report success. Then walk the last
  blob chunk record-by-record before/after and SHA the chunk file.
  Hypothesis: `ig_revise` rebuilds blob-append state from the padding-blind
  stored `btotal` (`bb.used = btotal % IG_BLOB_CHUNK`, `bb.total = btotal`),
  so the replacement record is written at the wrong physical position in
  the last chunk → silent tail-chunk corruption despite reported success.
  Kill criterion: last chunk byte-identical after the 5 revises.
- **G4 (delete path):** delete 20 chunk-1 slots (same stride as G2).
  Expect 20/20 succeed — `ig_delete` never reads blob offsets — and query
  then reports each deleted. Tests the audit's "E3 blocked by store defect"
  claim against the mechanism.
  Kill criterion: any delete fails with an offset-related error.
- **G5 (characterization from G2):** plant-then-deny-correction: install a
  false fact, show revise is impossible while delete remains — the
  reversibility-law violation stated as a measured asymmetry.

## RT-H — Seal-idempotency gap exploitation

- **H1:** pure-Zag harness calling the VERBATIM ingest `sc_seal_tail` twice
  on a sealed multi-chunk store. Expect: nsealed+1 and seal mutation
  (demonstrated, not just diffed).
  Kill criterion: second call is a no-op (nsealed and seal unchanged).
- **H2 (genuine-path audit):** by source inspection of the frozen
  `ingest.zag` plus manifest cross-check (`nsealed == ceil(n/4096)`),
  confirm `ig_ingest` calls `sc_seal_tail` exactly once and that
  revise/delete/sindex/query never call it → the double-seal is NOT
  triggerable through the shipped CLI; latent. Impact characterization:
  any second caller (defensive re-seal flow, crash-recovery tool) silently
  appends a duplicate tail chunk and moves the chain head — seal griefing /
  repudiation. No install/hide exploit is expected through the genuine
  path; that negative result is itself reported with evidence.

## Reporting

Folded into `REDTEAM_VERDICT.md` with per-family numerators/denominators,
root cause of every successful attack, evidence for every failed attack,
and all determinism SHAs. Attack sources (Zag) + glue committed alongside
under `knowledge/ingest_1gb/redteam/`.
