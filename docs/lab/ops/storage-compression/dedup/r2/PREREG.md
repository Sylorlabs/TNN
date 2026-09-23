# PREREG — dedup delete-logic round 2 (R2)

Date: 2026-09-23. Task: verify the ENTIRE delete/duplicate chain
(ingest → merge gate → storage → learning reads), port the `sc_seal_tail`
idempotency fix into canonical `adopt/s5_store.zag`, build the missing
ingest-time merge gate, and adversarially probe corroboration under
coordinated lies.

Binary: pure-Zag `dd_r2`, built with pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
New canonical file: `ops/storage-compression/adopt/s5_merge.zag`
(ingest-time exact-value merge gate; imports `s5_store.zag`).
Port: 1-line guard + comment in `adopt/s5_store.zag::sc_seal_tail`
(byte-identical to the already-fixed `dedup/src/s5_store.zag` copy).

Zero RNG anywhere: all fixtures use splitmix64-of-index draws
(deterministic function of the index, same family as round 1).
Every mode is run twice; outputs must be byte-identical (`cmp`).

## Bars

- **B1 — seal-fix port, no resurrection (canonical copy).**
  Scenario on the ADOPT store: 200 facts, cslots=64 (3 full chunks +
  8-slot partial tail), tombstone ids in a sealed chunk AND in the tail
  chunk, then `sc_seal_tail` TWICE + `sc_seal_final`.
  PASS: every deleted id fails `sc_recall`; every live id recalls its
  exact pre-delete value; `sc_replay_check`=0; `sc_manifest_verify`=0;
  live count == 200 − ndel. Sensitivity control: the same driver built
  against the pre-port snapshot MUST fail (deleted id still recalls),
  proving the test detects the bug the port fixes.
- **B2 — merge gate correctness.**
  2,000 claims × deterministic 1–5 copies (≈6,000 `mg_add` calls, 50
  sources, 40 origins). PASS: stored slots == 2,000 distinct values;
  every distinct value recalls exactly once with the right value;
  per-value source record: assert count == copies issued,
  distinct-source count == distinct sources issued;
  `sc_replay_check`=0 and `mg_replay_check`=0.
- **B3 — no silent space waste.**
  After pure merge ingest: zero tag-10 (delete) events in the log
  (merged dupes never reach `sc_add`, so no dupe-failure events either —
  `events_n`==0); `sc_written_bytes`(merged) == `sc_written_bytes`
  (one-copy baseline built with raw `sc_add`) exactly. The 20 B/fact
  audit cost of add-then-delete is not paid.
- **B4 — no lost facts.**
  `sc_digest`(merged store) == `sc_digest`(one-copy baseline).
  Distinct live value sets identical; byte equality of the digest
  proves no fact lost or altered by merging.
- **B5 — full chain under mutation.**
  Merge ingest (600 claims) → `mg_delete` 50 reps → `mg_revise` 30 slots
  to fresh values → re-add 20 deleted values (stored fresh, asserts
  restart) → re-add 20 live values (merged, asserts fold) →
  `sc_seal_tail` twice → `sc_seal_final`.
  PASS: replay=0, manifest=0, `mg_replay_check`=0; deleted ids do not
  recall; all live ids recall ground-truth values; live count arithmetic
  exact; every verdict-installed value's slot recalls the installed value
  (learning reads see what the verdict decided).
- **B6 — adversarial: coordinated lie + sockpuppet flood, origin-diverse
  corroboration.**
  3,000 single-valued claims; 40 honest sources (1 per origin) with
  independent 1/3 noise; 1 bad origin with 8 sockpuppet source ids that
  always assert the SAME false object per claim (shared bad origin).
  Verdict rules compared: A_src (install iff ≥2 distinct SOURCE ids
  agree) vs A_org (install iff ≥2 distinct ORIGINS agree).
  PASS: A_org false installs == 0; A_src false installs ≥ 1 (the attack
  lands on the naive rule — adversarial validity control); every
  sockpuppet-only agreement is withheld under A_org; true claims with
  ≥2 honest origins agreeing are installed under A_org (the origin rule
  introduces no new misses vs A_src on honest traffic).
- **B7 — determinism.** All four modes run twice; `cmp` byte-identical.
- **B8 — purity.** No RNG in new Zag code (splitmix-of-index only);
  build with the pinned toolchain; `--no-analyze` like round 1.

## Kill criteria

Any B1–B6 FAIL rejects the corresponding claim: the port is wrong, the
gate is wrong, or the defense does not hold — fix and re-run, or report
the failure honestly. B7/B8 gate any reported numbers.

## Out of scope (stated, not hidden)

- Legacy trial learners `ops/storage-compression/src/s4_learner.zag` and
  `s5_learner.zag` carry their own unguarded `sc_seal_tail` (hash-chain
  design, superseded by adoption). They are not modified here; flagged
  for retirement in the report.
- The gate merges EXACT values only (the proven-safe direction from
  round 1). Semantic variants and conflict groups remain the scanner's
  and the verdict layer's job — the gate never merges different values
  and never deletes conflicts.
- Origin ids are a u6 contract (0–63) in this implementation; wider
  provenance needs a bigger mask (listed follow-up).
- Physical compaction still unbuilt: merge-on-add avoids the cost
  instead of reclaiming it.
