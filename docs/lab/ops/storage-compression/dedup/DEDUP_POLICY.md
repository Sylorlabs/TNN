# Duplicate-fact policy (DEDUP_POLICY)

Status: recommended. Evidence: `EVIDENCE.md`. All numbers below are measured,
not estimated.

## The one-line policy

**Duplicates are never "waste" by default — they are corroboration evidence
and corruption redundancy. Never delete for space: with the current S5
store, deletion *costs* ~20 bytes per fact and reclaims zero. Gate
duplicates at ingest instead, keep conflicts forever, and replicate only
what must survive.**

## Rules

1. **Merge-on-add, not add-then-delete.** The scanner's exact-value map
   runs at ingest: a fact whose value already exists is not stored again.
   Its source id is folded into the claim's per-claim source record
   (count + source mask — the signal exp2's Policy A needs). Proven safe
   direction: the deletion proof (`ok=1`) shows value-level dedup loses
   nothing; doing it at ingest also avoids the 20 B/fact audit cost of
   deleting later (measured: 1.90 MB → 4.15 MB for 112,481 deletions).

2. **Exact duplicates of live claims: one slot per distinct value.**
   Measured redundancy in the fixture: 157,650 facts → 43,837 distinct
   values (3.6×). The surviving representative is deterministic (first id).

3. **Conflict groups are never deleted or merged.** 649 conflict groups /
   2,657 ids in the fixture; the proof's P5 verifies all survive deletion.
   A contradiction is intelligence, not dirt — it is surfaced to
   deliberation, never silently erased. (This is also why the scanner
   *skips* conflicted ids: 1,332 skipped in the proof run.)

4. **Semantic variants are not removed by dedup.** Alias wordings
   (13,186 ids, 3,188 groups) are distinct byte forms of one claim;
   consolidating them is a deliberate, audited operation — not a storage
   janitor's job.

5. **Lone assertions go to the verdict layer, not the scanner.** 41 lone
   conflicting assertions and all 2,352 unique singletons are
   *uncorroborated*, not *duplicated*. Policy: install on ≥2 independent
   sources (measured 0.00% false installs under independent noise),
   withhold otherwise (the measured price: 2,994 true-but-uncorroborated
   claims withheld — correct behavior: withhold when evidence cannot
   resolve).

6. **Tiered redundancy (from exp1).** Redundancy buys *recovery* (+2.1 pp
   survival at 5% corruption); the manifest alone only *detects*.
   - **Tier 1 — constitutional / force-pinned facts:** K ≥ 3 full copies;
     plurality adjudication over canonical values recovers the truth.
   - **Tier 2 — ordinary facts:** one copy + per-claim source record.
     Corruption is detected by the manifest; recovery is by re-fetch
     from the recorded sources (the source list *is* the backup).
   Promotion to Tier 1 rides the existing deliberate pin/promote
   machinery (MA1) — replication is a deliberate act, never background
   accumulation.

7. **Corroboration counts *independent* sources, not assertions.**
   Under a coordinated lie, 2 agreeing sources are only 56.1% reliable
   (3 sources: 92.2%). The source record must therefore track provenance
   diversity — sources sharing an origin count once. Agreement is
   evidence, not truth.

8. **Never install on first sight.** Dedupe-first (Policy B) installs
   34.0% falsehoods regardless of error correlation. First assertion
   starts a claim as SUSPECT; installation needs corroboration.

## Hardening notes (from building this)

- ~~Port the 1-line `sc_seal_tail` idempotency guard to
  `ops/storage-compression/adopt/s5_store.zag`~~ DONE 2026-09-23
  (round-2 verification: canonical copy now byte-identical to the fixed
  `dedup/src` copy; regression + sensitivity control in
  `dedup/r2/EVIDENCE_R2.md` §1).
- Ingest-time merge gate BUILT 2026-09-23: `adopt/s5_merge.zag`
  (`mg_add`/`mg_revise`/`mg_delete`/`mg_query`/`mg_replay_check`;
  exact-value merge, per-value assert/source/origin records).
  Verified in `dedup/r2/EVIDENCE_R2.md` §§2–4.
- Delete events should record the surviving representative id
  (`d1`/`d2` are free) so "deleted X, kept Y" is auditable from the log
  alone.
- Physical compaction (reclaiming tombstoned slot bytes) is still
  unbuilt; until it exists, "delete to save space" is actively
  counterproductive — say so whenever it is proposed.
