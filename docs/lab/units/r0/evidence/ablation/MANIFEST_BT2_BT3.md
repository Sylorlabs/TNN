# B-T2 / B-T3 probe manifest — R0 causal ablation and dose curve (crew B-ABLDOSE)

Track R0, prereg FROZEN (Micah signed 2026-09-21), §2 R0.1 batteries 2 and 3.
This manifest is frozen and committed BEFORE any evidence run.
Battery sources: `units/r0/impl/ablation/` (`bt_common.zag`, `b_t2.zag`, `b_t3.zag`).

## 0. Hard laws

- Pure Zag. ZERO randomness in any AI decision path.
- One fixed environment seed, 20260921, xorshift64* stream. The seed drives
  *environment* inputs only (span contents, gap lengths, noise flips) — never
  an AI decision. Logged in every binary's stdout (`BT2_ENV_SEED` /
  `BT3_ENV_SEED`).
- 1x only (R-9: 10x forbidden until 1x replication bars pass).
- M8: N=5 adversarial allocation perturbations + one repeated baseline run;
  byte-identical stdout/stderr/captures required across all six.
- Expected-value readback probes run FIRST inside every binary (standing rule
  C): a deterministic miscompile is invisible to rerun-diffing, so the
  battery asserts hand-derived expected values, not just determinism.
- Never commit binaries, `.zagd`, `.zag-cache`, corpora, `__pycache__`.

## 1. Span sets (fixed pre-execution)

Deterministic generation, seed 20260921, pairwise-distinct contents:

- Vocabulary: 24 spans, lengths 6..8 (lengths 6..8 chosen so every full
  vocabulary span outranks its own proper substrings under the frozen
  utility rule — utility is strictly increasing in length at fixed
  seen/purity — and therefore promotes into the fixed inventory).
- Rare: 8 spans, lengths 6..8, appear exactly twice each at fixed unit indices.
- Novel: 8 spans, lengths 6..8, never appear during training.
- Contents: printable bytes 33..126. FNV-1a digest of the three tables is
  printed per run (`BT2_MANIFEST_DIGEST`); the probe plan is fixed by this
  manifest, not by the digest.

Consequence bytes: `0xAA` (170) for odd-index spans, `0xBB` (187) for
even-index spans. Consequence bytes never occur inside span contents.

## 2. Training regime (both batteries)

Each training unit: 6–10 vocabulary-span occurrences (gap lengths 1–3),
each occurrence = span bytes + consequence byte, then rare-span insertions.

- Vocabulary spans drawn ROUND-ROBIN (deterministic full coverage from the
  first units).
- Gaps use ONE fixed filler byte, `0x20` (space-like). Rationale: real
  text/code has recurrent separator bytes, and i.i.d. random filler floods
  the frozen 4096-entry proposal bank with noise substrings before the
  vocabulary is learned (observed 2026-09-21 during development: 23/24
  spans promoted under random filler; 24/24 under fixed filler).
- Rare span r appears in exactly the units u with
  `u == (r*37 mod T)` or `u == (r*37+199 mod T)` (two occurrences per dose T).
- All span occurrences of lengths 2..8 at every position are observed with
  label `2+q` (q=1 iff the immediately following byte is `0xAA`).
- Per-span and global consequence counts are kept for the twin-probe
  majority votes (environment bookkeeping, not AI state).
- Trust updates (`r0_dual_trust_update`) every 10th unit; helped=1 except
  every third update (deterministic schedule).
- One `r0_promote` after the full dose. Asserted: all 24 vocabulary spans
  are live chunks afterwards (`vocab_check=24/24`).

## 3. B-T2 hard-grounding probe battery

40 span contents × 5 occurrences = 200 probe occurrences:

- 24 vocabulary spans, 8 rare, 8 novel.
- Two fixed vocabulary spans (indices 7 and 19) use INCONSISTENT consequence
  outcomes across their 5 occurrences (occurrences 1 and 3 flipped), so
  their cross-occurrence consistency b=0.
- Probe episode layout: 8 probe-filler bytes + span + consequence byte +
  8 probe-filler bytes. Probe filler is `0x7F`, ABSENT from training
  (training bytes are 33..126, 0x20, 0xAA/0xBB). Rationale: with training-
  filler bytes in the probe context, greedy longest-match segmentation
  matches filler-anchored boundary chunks ("GGG"+span-prefix) that outrank
  the full span and fragment the target range into ragged literals
  (observed 2026-09-21: 1/24 spans recalled). The 0x7F filler keeps the
  probe context realistic while isolating the span for the chunk route.

Per occurrence:

- `a_raw`: byte-exact re-read of the span range (raw route).
- `a_chunk`: 1 iff greedy segmentation tiles the span range with live
  chunk units (all ids ≥ 0, contiguous, byte-exact reconstruct), else 0.
- `a_dual`: chunk recall, falling back to raw when
  `r0_should_retrieve_raw` fires (the real dual-retrieval API).
- Label-3 (hard grounding per R-1) = recall success AND consistency
  (b=1). Hard score = label-3 occurrences / 200.

Structural expectations (not numeric targets):

- raw ≈ dual (dual falls back to raw where chunks are missing).
- chunk strictly below both: chunk recall succeeds only for the 22
  consistent vocabulary spans (110/200); rare spans (seen=2 < 5) and novel
  spans (unseen) have no chunks (80/200 fail); the 10 inconsistent-span
  occurrences are excluded from label-3 by b=0.
- Reference point from development: raw=dual=950/1000mp, chunk=550/1000mp.
  The bar is the ORDERING (chunk < raw, chunk < dual), not these numbers.

Per-route recall and consistency are reported separately alongside the
hard scores.

## 4. Near-twin discrimination probe set (reference-only, no bar)

24 vocabulary spans × 8 repetitions = 192 trials. Each trial: the true
span or its near-twin (middle byte XOR 0x01), alternating deterministically,
followed by the consequence byte with 20% deterministic outcome noise.

- Raw prediction: exact-content lookup → per-span consequence majority,
  else global majority.
- Chunk prediction: majority vote over the chunk units covering the span
  range, iff fully covered; else global majority.
- Dual prediction: chunk vote when covered, else raw prediction
  (mirrors the dual-retrieval rule).

Scores reported per route. Historical dual 0.8363 vs raw 0.8186 is
reference-only; the battery does not target it. No bar: the twin set
characterizes discrimination, it does not gate.

## 5. Dual compression ratio

Measured on the training dose: re-emit the identical training units and
greedily segment each.

- source = total source bytes.
- stored = live chunk payload bytes + 4 bytes per chunk-index reference
  + literal bytes (one byte per unmatched byte).
- ratio = source / stored (reported in 1/1000).

The ratio measures the compression/indexing layer the dual route adds;
the raw route re-reads the external source (ratio does not imply deletion
of raw evidence). All four components are reported.

## 6. B-T3 dose curve

Fresh arena per dose; train the nested prefix of the deterministic unit
schedule at doses 250, 500, 1000, 2000, 4000, 8000 (the harness dose
schedule); one `r0_promote`; score the §3 dual hard-grounding battery.

Bar metric: dual_active hard-grounding score vs dose — flat or
non-decreasing. R-4 sets no numeric degradation tolerance: the battery
reports every dose value and the maximum adjacent drop, and the formal
tolerance is marked **PENDING-MICAH-AMENDMENT** (proposed: ≤ 25/1000
adjacent drop, i.e. 5 label-3 occurrences; Micah to set).

## 7. M8 adversarial-allocation battery

One binary per config; argv selects leg (0/1) and perturbation (0..4).
Every invocation: expected-readback probe first (exit 2 on failure),
golden mini-run, perturbation, battery, captures.

Perturbation modes (adversarial heap states; the battery never reads
addresses or uninitialized memory, so all modes must be byte-identical):

0. Baseline (no perturbation).
1. Heap pre-fragmentation: interleaved alloc/free of varied sizes before
   the arena is allocated.
2. Held 64 KiB ASLR-equivalent offset: large block held during the run,
   shifting subsequent heap placement.
3. Entropy/clock canary: reads wall-clock time and stack address into
   locals that are never used (pins the optimizer against eliding
   nondeterminism sources; values never enter any decision or output).
4. Free-list order reversal: allocate-then-free in reverse order to invert
   the allocator's free-list order.
5. (mode 4) Mid-run churn: allocate/free storm between training and
   probing (mode index 4 = churn; modes 0..3 are pre-run).

Runner: each config/leg runs perturbations 0..4 plus a repeated
perturbation-0 run; stdout/stderr compared byte-identical across all six
(no normalization except none — outputs contain no addresses or times).

## 8. Golden mini-run (expected values, hand-derived)

Runs inside every battery invocation before the main battery (seed
20260921, leg 0, T=2):

- Each vocabulary span seen ≤ 2 (round-robin over 2 units) → no span
  promotes; 6 filler-boundary artifacts ("GG", "GGG", sig+G, …) reach
  seen ≥ 5 with high purity and promote → `promoted=6`, `live=6`.
- Ground probe on this bank: raw re-reads bytes → 190/200 label-3;
  no span-covering chunks exist → chunk 0/200; dual falls back to raw →
  190/200.
- Twin probe smoke: 192 trials, counts in range.

Any deviation fails the binary (exit 2) before the battery runs.

## 9. Scorecard and prereg-bar mapping

- Scorecard follows `METRICS.md` (flags-as-strings). Conflict noted: the
  harness `ARM_INTERFACE.md` disagrees on flag encoding; this battery
  follows METRICS.md and records the disagreement (no silent deviation).
- R-3 (causal ablation): the prereg sets no numeric ε and no minimum
  compression ratio. Reported: per-route hard scores, dual−raw delta
  (in 1/1000), compression ratio with components. Formal bar marked
  **PENDING-MICAH-AMENDMENT** (proposed: |dual−raw| ≤ 25/1000 and
  ratio ≥ 1.2; Micah to set). Descriptive bar (ordering chunk < raw,
  chunk < dual) is evaluated as PASS/FAIL.
- R-4 (dose curve): formal tolerance **PENDING-MICAH-AMENDMENT**
  (proposed ≤ 25/1000 adjacent drop); descriptive monotonicity reported.
- R-7/R-8: both legs run (argv-selected, one binary). R-9: 1x only.

## 10. Evidence map (repo paths)

- `docs/lab/units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` (this file)
- `docs/lab/units/r0/evidence/ablation/b_t2_leg{0,1}.md` — per-leg
  scorecards, deltas, compression, M8 table
- `docs/lab/units/r0/evidence/ablation/b_t3_leg{0,1}.md` — dose tables,
  monotonicity, M8 table
- `docs/lab/units/r0/evidence/ablation/verdict_bt2_bt3.md` — verdict
  sheet with bar mapping and pending amendments
- Raw run logs: `docs/lab/units/r0/evidence/ablation/logs/`
