# Round-2 delete-logic verification — EVIDENCE

Date: 2026-09-23. Task: verify the ENTIRE duplicate/delete chain
(ingest → merge gate → storage → learning reads), port the
`sc_seal_tail` idempotency fix into canonical `adopt/s5_store.zag`,
build the missing ingest-time merge gate, adversarially probe
corroboration under coordinated lies.

Binary: pure-Zag `dd_r2` (driver `dedup/r2/dd_r2.zag`), built with pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` from
`adopt/` — so every mode exercises the CANONICAL store plus the new
`adopt/s5_merge.zag` gate. Zero RNG: all fixtures are splitmix64-of-index
draws (deterministic function of the index). Every mode run twice;
outputs byte-identical (`cmp` clean — B7). Prereg: `dedup/r2/PREREG.md`
(bars B1–B8); reproduce with `dedup/r2/run.sh`.

## 1. The port (B1)

`adopt/s5_store.zag::sc_seal_tail` gained the 1-line idempotency guard
`if(n/cs<s.*.nsealed){return 0;}` (+ comment). The canonical copy is now
**byte-identical** to the round-1 fixed `dedup/src/s5_store.zag`
(`cmp` clean).

Regression scenario (200 facts, cslots=64 → 3 full chunks + 8-slot tail;
tombstones in sealed chunks 0/1/2 and in the tail; `sc_seal_tail` twice):
**ok=1** — all 6 deleted ids fail recall, all 194 live ids recall exact
values, replay=0, manifest=0, live count exact.

Sensitivity control: the same driver built against the pre-port snapshot
fails with `R2_SEALFIX,FAIL,deleted_still_recalls` — the test detects the
bug the port fixes. (Snapshot kept as local scratch only, not committed.)

## 2. Merge gate (B2/B3/B4) — `adopt/s5_merge.zag` (new)

Ingest-time exact-value merge: a duplicate value is never stored again;
its source folds into the per-value record (assert count, source mask,
origin mask). `mg_add` / `mg_revise` / `mg_delete` / `mg_query` /
`mg_replay_check`; src/org ids are a u6 contract (0–63).

2,000 claims × 1–5 copies (6,000 assertions, 50 sources, 40 origins):
**ok=1**.
- 2,000 slots stored, 4,000 duplicates folded — one slot per distinct value.
- Per-value records exact: asserts == copies issued, distinct sources == sources issued.
- **B3 — no silent space waste:** `events_n`==0 after pure merge ingest
  (no delete events, no dupe-failure events — merged dupes never reach
  `sc_add`); `sc_written_bytes`(merged) == `sc_written_bytes`(one-copy
  raw-`sc_add` baseline) **exactly** (25,664 B both). The ~20 B/fact audit
  cost of add-then-delete is not paid.
- **B4 — no lost facts:** `sc_digest`(merged) == `sc_digest`(baseline).
- `sc_replay_check`=0, `mg_replay_check`=0.

## 3. Full chain under mutation (B5)

Merge ingest (600 claims) → 50 `mg_delete` → 30 `mg_revise` (fresh values)
→ 20 deleted values re-added (stored fresh, asserts restart at 1) →
20 live values re-added (folded, asserts increment) → `sc_seal_tail` ×2 →
`sc_seal_final`: **ok=1**. Live 570/620 exact; every live id recalls
ground truth; every deleted id fails recall; replay=0, manifest=0,
`mg_replay_check`=0; every gate value's slot == the recalling id
(verdict → learning-read tie holds through deletes, revises, and the
double seal).

## 4. Adversarial corroboration (B6)

3,000 single-valued claims; 40 honest sources (independent 1/3 noise, each
invents its OWN false object) + 1 bad origin with 8 sockpuppet source ids
asserting the SAME false object per claim (shared bad origin). Verdicts:
A_src (≥2 source ids agree) vs A_org (≥2 distinct origins agree).

| measure | A_src (naive) | A_org (origin-diverse) |
|---|---|---|
| false installs | **1,000** (attack lands) | **0** |
| sockpuppet agreements withheld | — | 1,000 / 1,000 |
| true claims installed | 1,569 | 1,569 (no new misses) |

Calibration: P(true | nsrc=2)=100.0%, P(true | nsrc=3)=**34.8%**
(the coordinated lie concentrates at nsrc=3 — agreement count is not
truth, reproducing round 1's 56.1% finding in the new harness),
P(true | norg=2)=**100.0%**. Every installed value's slot recalls the
installed value (learning reads see what the verdict decided).

**Boundary (measured, not barred):** 500 extra claims where a SECOND
colluding origin joins the lie — A_org false-installs 167/167 of them.
Origin-diversity defeats single-origin coordination; two colluding origins
break it. Provenance must ultimately come from diversity the adversary
cannot manufacture (listed follow-up).

## 5. Verdict

- Delete logic: **right, after the port.** The resurrection footgun is
  closed in the canonical store; tombstones, audit events, replay, and
  manifest are mutually consistent through the full mutation chain.
- Merge gate: **warranted and built** — merge-on-add pays zero delete
  events and byte-identical cost to the one-copy baseline, vs ~20 B/fact
  for add-then-delete with zero reclaimed bytes.
- Corroboration: **source-counting is broken under coordination**
  (1,000 false installs); **origin-diverse counting holds** (0), with a
  known two-origin boundary.

## 6. Follow-ups (not hidden)

- Legacy trial learners `ops/storage-compression/src/s4_learner.zag` and
  `s5_learner.zag` carry their own unguarded `sc_seal_tail` (superseded
  hash-chain design, nothing references them) — retire or port.
- Origin ids are u6 (0–63); wider provenance needs a bigger mask.
- Physical compaction still unbuilt (merge-on-add avoids the cost rather
  than reclaiming it).
- Two-colluding-origins boundary needs a provenance-diversity design.
- Rerun the scanner against the live ≥1 GB store when `run/store/` exists
  (round-1 limitation carries over).
