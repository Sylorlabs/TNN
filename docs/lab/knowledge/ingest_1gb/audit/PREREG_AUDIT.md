# PREREG — AUDIT of the sealed 1GB ingestion store + E2/E3 unblock

**Frozen:** 2026-09-23. Auditor: Muse (subagent). Parent: orchestrator b0bb2563.
**Target of audit:** 1GB ingest run on branch `tnn-native-lab`, report commit
`ebcb273b` (`docs/lab/knowledge/ingest_1gb/REPORT.md`), sealed store
`run/store_full/`, seal `3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87`.
**Frozen source under audit:** `build/ingest.zag` (blob `f46d340862bf…`, matches
local file byte-identically — verified via `git hash-object` vs committed tree).

## §1 Standing rules

- Pure Zag for all verification machinery; Python only for glue/analysis.
- Zero randomness anywhere: all samples are deterministic strides.
- Byte-identical reruns proven by SHA256.
- Frozen prereg (this file) committed alone BEFORE any new battery runs.
- Commits to `tnn-native-lab` via `~/workspace/commit_racefree.py`,
  `TMPDIR=~/workspace/tmp_commit`, lab-relative paths not starting with
  `docs/lab/`. Never commit binaries, `.zagd`, `.zag-cache`, stores,
  `facts.bin`, or blob chunks.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## §2 Audit scope

The auditor verifies the run's claims against its own artifacts; the auditor
is not the adversary. Known open items from REPORT §7 under audit: ingest
determinism (single-run only), sparse-index Python fallback, E2/E3 ID blocker.

### A1 — facts.bin census (`audit/audit_census.zag`, pure Zag)
Stream all of `run/facts.bin` (record: `[1B kind][2B klen BE][4B tlen BE][key][text]`):
count records; verify keys are in non-decreasing unsigned-lexicographic order
(zero inversions); count adjacent equal-key pairs.
- Bar C1: record count == 3,707,990.
- Bar C2: zero sort inversions.
- Bar C3: adjacent-dupe count == 539,418 (== `merge_stats.txt`
  `duplicate_keys`; proves the merge COUNTER saw them — removal is tested
  by A2/A6, not assumed).
Also census the three source bins (`wn.bin`, `wikt.bin`, `wiki.bin`) by record
count; their sum must == 3,707,990 (grounds the report's "4,247,408 input"
claim: 4,247,408 == 3,707,990 + 539,418, i.e. the report derived a phantom
input by assuming dedup worked).

### A2 — ingest replay (`audit/audit_replay.zag`, pure Zag)
Independent Zag replay of the judgment path over `facts.bin`: gate functions
(`ig_gate`, `ig_cal_bad`, `ig_key_word`, `ig_has_sub`, `ig_key_eq`) copied
verbatim from the frozen source; the lesson harness (65,536-record lessons,
4-record peek, CAL dry-run with 8 probes, CAL-reject staleness of `prev_key`,
per-record gate in accepted lessons) written independently from the spec.
Must reproduce EXACTLY, from `audit.log`/`manifest.txt`:
- lessons=57, lessons_rejected=9,
- reject masks at lessons {3:1, 14:1, 23:1, 28:1, 31:1, 39:1, 43:15, 48:8, 50:4},
- inst=2,597,057, g1=0, g2=462,263, g3=58,846.
- Bar: every number matches; any mismatch is a finding, not a tweak-the-harness
  exercise (the harness is written once from the spec; if it disagrees with the
  binary, the binary's counting is suspect).
Emits `audit/slot2pos.bin`: `[4B n][n × 4B LE facts.bin position]` mapping
install slot → source position (the authoritative ID remap for §4).

### A3 — duplicate audit cost + tombstones
- Parse `run/store_full/store.dat` event section; list (tag, count).
  Bar: exactly 66 events (57 × tag-7 episode + 9 × tag-8 lesson-reject);
  zero per-reject events — i.e. the 462,263 G2 + 58,846 G3 rejections cost
  zero audit bytes. Any tag-1 (add-fail) event is a finding.
- Tombstone spot-check: all 2,597,057 slot flag bytes have bit0 (deleted) and
  bit1 (revised) CLEAR in the sealed store (checked inside A6's pass).
  Bar: 0 tombstones, 0 revised flags pre-E2/E3.

### A4 — seal-tail idempotency at scale (`audit/audit_seal.zag`, pure Zag)
Load the sealed `run/store_full/` (n=2,597,057, nsealed=635). Record seal hex.
Then:
  (i) call the INGEST version of `sc_seal_tail` (verbatim from frozen source:
      `if(n%4096==0){return 0;} return sc_compact_and_seal(…)`);
 (ii) call the CANONICAL version from `adopt/s5_store.zag` (adds
      `if(n/cs<s.*.nsealed){return 0;}` — the 7303b6db idempotency fix).
- Bar: both must be no-ops (nsealed and seal unchanged). Code reading predicts
  (i) DOUBLE-SEALS the tail (nsealed 635→636, seal changes) because the ingest
  port lacks the canonical guard line — PORT_EQUIV.md's "trailing whitespace
  only" verdict on `sc_seal_tail` is therefore suspect and under test.
  The empirical result is reported as-is: PASS only if the guard holds.

### A5 — byte-identical ingest rerun
- Rebuild `build/ingest_bin_audit` from the frozen source with the pinned
  toolchain (no source edits).
- From `knowledge/ingest_1gb/`, run
  `ingest_bin_audit ingest run/facts.bin run/bad.bin run/store_rerun 4078789`
  (same relative argv as the original run so `audit.log`'s INGEST-START line
  matches byte-identically; ncap = 3,707,990×1.1 = 4,078,789 as in the report).
- SHA256-compare vs `run/store_full/`: `store.dat`, all 12 `blob_*.dat`,
  `manifest.txt`, `audit.log`.
- Bar K4: all SHAs identical; seal ==
  `3486716317fb7f39b9d85cba2f3271874a57e68a0587884a9b92000941c85e87`.
- Also rebuild `sparse.idx` in the rerun dir with the frozen
  `extract/build_sparse.py` and compare to `store_full/sparse.idx`
  (determinism of the Python fallback).

### A6 — sparse-index integrity, full coverage (`audit/audit_index.zag`, pure Zag)
Load `run/store_full/sparse.idx`; stream all blob records in global-offset
order (2,597,057 expected). For each record:
  (i) blob id field == running install counter (proves slot == install index);
 (ii) key strictly greater than previous record's key (proves zero duplicate
      installs and no lost-fact shadowing);
(iii) binary search of the index for greatest entry with entry.key ≤ rec.key:
      entry exists, entry.goff ≤ rec.goff, and the next entry (if any) has
      key > rec.key (proves `ig_lookup`'s forward scan starts at/below the
      record and reaches it — full retrievability, not a sample).
- Bar: 2,597,057/2,597,057 verified, 0 violations; flags bit0/bit1 clear
  on all slots (A3 tombstone check folded in).
- E1 re-verification folded in: walk the blob once, count hits of the 1000
  keys in `run/eval_keys.bin` via binary search over the sorted key set.
  Bar: 1000/1000 installed (tests the report's "installed regions" claim).

## §3 E2/E3 — root cause (diagnosed pre-freeze, fix executed under this prereg)

Root cause: eval IDs in `run/rev_ids.txt` / `run/del_ids.txt` are 0-based
POSITIONS into `facts.bin` (3,707,990 records; `gen_eval.py`: `(i*n)//100`),
but `revise`/`delete` take S5 SLOT ids (0..2,597,056, slot s = s-th installed
fact). The spaces diverge at the first rejected record (lesson 0 already
rejects 7,491 G2s). E2 pilot log (`run/e2.log`) shows the mechanism:
positional id 37079 was installed at slot 33760, so the pilot revised the
wrong fact and verification (correctly) failed. The ID spaces are related by
the install subsequence, not by identity.

Fix (no mechanism change): use `audit/slot2pos.bin` from A2 as the
authoritative pos→slot remap. Deterministic sampling on SLOTS:
- E2: 100 slots `s_i = (i·N)//100`, i in 0..99, N=2,597,057; keys recovered
  from `facts.bin` at `slot2pos[s_i]` (Python glue).
- E3: 100 disjoint slots `t_i = (i·N)//100 + N//200`.
Working copy: `run/store_e23/` is byte-identical to `run/store_full/`
(store.dat SHA prefix `e98f85c8600417e2` both); E2/E3 mutate a private copy
`run/store_audit_e23/` so the sealed artifact is never touched.
All revise/delete/query operations are performed by the Zag binary
(`ingest_bin_audit`); batch verification via `bquery` (binary result records:
status/id/tlen/text); Python only drives subprocesses and checks bytes.

### E2 revise proof — bar (prereg §6 E2)
- 100/100 revises return rc=0; `bquery` on the 100 keys returns status=FOUND,
  id == slot, and byte-exact new text.
- 1000 deterministic neighbor slots (stride sample excluding modified slots):
  `bquery` texts byte-identical to pre-revise texts from `facts.bin`.
- `store.dat` event section contains exactly 100 tag-9 (revise) events.

### E3 delete proof — bar (prereg §6 E3)
- 100/100 deletes return rc=0; `bquery` on the 100 keys returns
  status=DELETED with id == slot.
- 1000 neighbors (disjoint from E2/E3 sets): texts byte-identical.
- `store.dat` event section contains exactly 100 tag-10 (delete) events.

## §4 Deliverable

`docs/lab/knowledge/ingest_1gb/audit/AUDIT_VERDICT.md`: every check's numbers
vs bars, the E2/E3 root cause + fix + results, and all integrity violations
found (with severity). Committed to `tnn-native-lab` after the prereg commit.
Audit Zag sources committed alongside the verdict as method evidence.
`slot2pos.bin` stays local (derived artifact, 10MB); its SHA is recorded in
the verdict.

## §5 Kill bars for the audit itself

- AK1: prereg committed alone before any battery runs. (This file.)
- AK2: any A1–A6 bar failure is reported as a finding; bars are not relaxed
  mid-audit. A failed check does not block the other checks.
- AK3: E2/E3 are UNBLOCKED by this audit: 100/100 revise + 100/100 delete
  verified, or a written statement of exactly what still blocks them.
- AK4: no mutation of `run/store_full/`, `run/facts.bin`, or any sealed
  artifact at any point (verified by SHA before/after).
