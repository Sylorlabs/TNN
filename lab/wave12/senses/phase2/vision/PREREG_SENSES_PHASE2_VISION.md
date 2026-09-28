# PREREG — Senses Phase 2 (vision): RGB8 ingress envelope + OBSERVE contract at operating size

Date: 2026-09-20. Status: **FROZEN BEFORE BUILD.**
Branch: `tnn-native-lab`. Dir: `docs/lab/wave12/senses/phase2/vision/`
(workspace: `~/workspace/tnn-lab/wave12/senses/phase2/vision/`).
Measuring instrument: `../../PROPOSED_QUALBAR_SENSES_2026-09-20.md`
(**PROPOSED, UNSIGNED** — results are reported as "meets proposed bar §X",
never as QUALIFIED).

## Claim

The phase-1 ingress + OBSERVE contract skeleton extends to the proposed
vision operating envelope (RGB8 frames 1×1..64×64) such that proposed-bar
§A–§E (vision) hold: exact refusals with zero state mutation (16), OBSERVE
discipline (8 probes + audit scan), kill/pin/recall semantics (10), 24
paired twins distinguishable through admit → OBSERVE → RECALL with differing
provenance hashes, and 12 realistic-envelope byte-identical round trips.

## Deliberate changes vs phase 1 (provenance: files copied, not moved)

- `se_ingress.zag` copied from `phase1/se_ingress.zag`, then changed:
  - `SE_MAX_PAYLOAD`: 4096 → 12288 (64·64·3). Required by proposed §E-vision
    (64×64 RGB8 = 12,288 B payload).
  - `SE_CAP`: 32 → 64 records (holds 48 twin records + margin in one store).
  - RGB envelope: width/height 1..4 → 1..64. Required by proposed §A-vision
    ("width > 64", "height > 64" refused).
  - Header layout extension (was: reserved@28..48 must be zero):
    channels(i32)@28, bit-depth(i32)@32, reserved[12]@36..48 (must be zero).
    RGB8 requires channels=3, bit-depth=8; PCM16LE requires channels=1,
    bit-depth=16. Required by proposed §A-vision ("channels field ≠ 3",
    "bit-depth field ≠ 8", "reserved param nonzero" as three separate checks).
  - `se_build` sets channels/bit-depth from the encoding id; zeroes the
    remaining reserved bytes.
- `se_memif.zag` copied from `phase1/se_memif.zag` **unchanged** (contract,
  refusal codes -7201..-7210, 16-slot store, 256-entry audit all identical).
- `substrate/` vendored from `phase1/substrate/` (R33_NATIVE_SHA256_V2.zag,
  R33_NATIVE_IO_V1.zag, cl/common.zag); hashes recorded in
  `SUBSTRATE_SHA256.txt`.
- `se2v_main.zag` is new: the vision battery harness. `run_phase2_vision.sh`
  is new: static checks, two builds, two harness runs, replay diff,
  mechanical CL_CHECK verification. No save/reload mode (proposed §I is out
  of scope for this worker).

## Fixture-generation method (deterministic, no RNG)

- All fixtures are authored in the harness from explicit byte literals or
  from `v2v_pattern(payload,w,h,seed)`: `b[i] = (i*37 + seed*11 + 13) & 255`
  — pure index arithmetic, no randomness, no wall clock. Distinct seeds give
  distinct honest frames.
- Twin pairs: build base frame, copy, apply exactly one controlled mutation.
  Every pair's two payloads differ (verified mechanically: recalled bytes
  differ AND provenance sha256 differ); no pair relies on header-only
  differences (payload sha256 would then be identical and the pair would
  fail its own provenance check by design).
- All OBSERVE strengths/judgments/citations are caller-declared constants
  (e.g. strength = 10 + (pair_index % 90)); no observation-byte arithmetic
  feeds any strength value (K-SE5).

## Exact check list (71 counted checks, `CL_CHECK,se2v-<name>,actual,expected`)

### §A-vision — malformed/edge ingress battery (16 checks)
Setup: admit one valid 2×2 RGB8 record, OBSERVE it once (live=1). Each of
the 16 is a one-mutation copy of the pristine record; expected refusal code
in brackets:
1. `se2v-a-bad-magic` (byte[0]≠'T') [-7101]
2. `se2v-a-bad-version` (version=2) [-7102]
3. `se2v-a-bad-encoding` (encoding=9) [-7103]
4. `se2v-a-width-0` (width=0) [-7104]
5. `se2v-a-height-0` (height=0) [-7104]
6. `se2v-a-width-65` (width=65) [-7104]
7. `se2v-a-height-65` (height=65) [-7104]
8. `se2v-a-plen-neq-wh3` (2×2, plen=13, 13 payload bytes, valid hash) [-7104]
9. `se2v-a-bad-hash` (one payload byte flipped) [-7106]
10. `se2v-a-trunc-header` (79-byte buffer) [-7101]
11. `se2v-a-trunc-payload` (plen=12, 11 payload bytes present) [-7105]
12. `se2v-a-zero-payload` (plen=0, valid empty-payload hash) [-7104]
13. `se2v-a-plen-over-cap` (plen=12289) [-7104]
14. `se2v-a-channels-neq-3` (channels=1) [-7104]
15. `se2v-a-bitdepth-neq-8` (bit-depth=16) [-7104]
16. `se2v-a-reserved-nonzero` (reserved byte@36=1) [-7104]
Plus uncounted gate lines: `se2v-a-refusals-16` (=16), `se2v-a-n-unchanged`,
`se2v-a-live-unchanged` (K-SE3).

### §B-vision — OBSERVE admission discipline (8 probes + 1 audit scan)
Setup: admit one valid 2×2 record. Probes:
1. `se2v-b-judgment-none` → -7201
2. `se2v-b-judgment-5` → -7201
3. `se2v-b-strength-0` → -7202
4. `se2v-b-strength-101` → -7202
5. `se2v-b-region-2` → -7203
6. `se2v-b-cite-neg1` → -7209
7. `se2v-b-dead-recid` (rec_id=1, only id 0 exists) → -7204
8. `se2v-b-full-refused` (fill 16 slots with uniquely-named
   `se2v-b-fill-00..15` setup lines, then one more OBSERVE) → -7205
9. `se2v-b-audit-scan` → 1 (100% of live slots trace to an OBSERVE entry)

### §C-vision — kill / pin / recall semantics (10 probes)
Setup: admit 3 records; OBSERVE rec0→s0 (USER), rec1→s1 (CORE),
rec2→s2 (USER); pin s0 (setup line, must be MI_OK).
1. `se2v-c-kill-pinned` (kill s0) → -7206
2. `se2v-c-kill-core` (kill s1) → -7207
3. `se2v-c-kill-no-evidence` (kill s2, evidence=0) → -7210
4. `se2v-c-kill-legit` (kill s2, evidence=5) → 0
5. `se2v-c-rekill` (kill s2 again) → -7208
6. `se2v-c-recall-dead` (recall s2) → -7208
7. `se2v-c-recall-twice` (recall s1 into two buffers) → 1 (identical)
8. `se2v-c-recall-no-alias` (mutate recalled buffer, re-recall) → 1 (unchanged)
9. `se2v-c-pin-idempotent` (pin s1 twice) → 1 (both MI_OK, pinned=1)
10. `se2v-c-observe-freed` (OBSERVE rec0 into s2's freed slot) → 1 (MI_OK,
    slot id reused, slot provenance == sha256(rec0 payload) — no ghost)

### §D-vision — paired twins, S1 discriminability (24 checks)
Per pair: admit both records (one shared 64-cap store), fresh MiStore,
OBSERVE both (caller-declared judgment/strength/cite), RECALL both.
Composite `se2v-twin-<name>` = 1 iff: both admits sequential, both OBSERVEs
MI_OK, both recalls return full length, recalled bytes differ, and the two
slots' provenance sha256 differ. The 7 named by the proposed bar plus the 17
defined here (each pair differs in exactly one controlled item):
1. `px-plus1` — 2×2, pixel[0].R +1.
2. `px-permute` — 2×2, pixels 0↔3 swapped (identical byte histogram).
3. `row-swap` — 3×3, rows 0↔2 swapped.
4. `px-zeroed` — 2×2, pixel[1] set to (0,0,0).
5. `brightness-plus1` — 2×2, every byte +1 (base values ≤ 254).
6. `size-1x1-vs-2x2` — 1×1 vs 2×2 uniform frames.
7. `wh-transposed` — 2×3 vs 3×2 with transposed pixel layout (payload differs).
8. `px-minus1` — 2×2, pixel[2].B −1.
9. `px-chan-zero` — 2×2, pixel[2].G 200→0.
10. `col-swap` — 3×3, columns 0↔2 swapped.
11. `px-chan-rotate` — 2×2, pixel[0] (10,20,30)→(20,30,10) (histogram preserved).
12. `brightness-minus1` — 2×2, every byte −1 (base values ≥ 1).
13. `px-invert` — 2×2, pixel[3] channels replaced by 255−v.
14. `diag-swap` — 3×3, pixels (0,0)↔(2,2) swapped.
15. `corner-px-bump` — 4×4, bottom-right pixel .R +1.
16. `width-plus1` — 4×4 vs 5×4 (same row-major prefix pattern).
17. `height-plus1` — 4×4 vs 4×5.
18. `uniform-gray-step` — 2×2 uniform 100 vs uniform 101.
19. `red-vs-blue` — 2×2 pure red (255,0,0) vs pure blue (0,0,255).
20. `px-relocate` — 3×3, single white pixel at index 0 vs index 8.
21. `lsb-flip` — 3×3, last pixel .R 254→255.
22. `px-plus1-8x8` — 8×8 pattern frame, one pixel .G +1.
23. `phase-swap` — 2×2 checkerboard phase flipped.
24. `tail-byte-plus1` — 3×3, final payload byte +1.

### §E-vision — realistic envelopes (12 checks)
`se2v-e-frame-00..07`: 8× 32×32 RGB8 (3,072 B payload, pattern seeds 1..8).
`se2v-e-frame-08..11`: 4× 64×64 RGB8 (12,288 B payload, pattern seeds 101..104).
Per frame composite = 1 iff admit ok, OBSERVE ok (caller-declared
strength/cite), RECALL returns full record, recalled bytes == admitted bytes.

## Kill bars (binding, carried from phase 1)

K-SE1 replay mismatch (two full runs byte-identical); K-SE2 silent admission;
K-SE3 refusal mutation; K-SE4 aliasing; K-SE5 computed strength (static scan);
K-SE6 RNG/wall-clock/threads/floats (static scan); K-SE7 save/reload identity
(not exercised — §I out of scope, no save mode in this harness); K-SE8
protected kill. Any fired bar → verdict DEAD, witness committed.

## Method

1. Static scans (K-SE5, K-SE6, bare `@import`s) over se_ingress.zag,
   se_memif.zag, se2v_main.zag.
2. Compile twice with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
   record both binary SHA256 (must be identical).
3. `./se2v_bin_a harness` → `logs/run_harness_a.txt`;
   `./se2v_bin_b harness` → `logs/run_harness_b.txt`; diff must be empty.
4. Mechanical: every `CL_CHECK,se2v-*,actual,expected` line must satisfy
   actual == expected; any mismatch fails the run.
5. Verdict per section: A x/16, B x/9, C x/10, D x/24, E x/12 against the
   proposed bar (reported as "meets proposed bar", never QUALIFIED — the bar
   is unsigned).

## Honest boundaries (not claims)

No live camera, no S2 perception, no classifier, no semantics, no
performance. Strength stays caller-declared. PCM validation path is carried
over unchanged and untested here (audio worker's scope). Save/reload (§I),
churn (§H), and full-bar replay/build (§F) beyond this worker's battery are
not covered by this prereg.
