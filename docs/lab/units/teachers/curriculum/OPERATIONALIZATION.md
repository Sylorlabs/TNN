# OPERATIONALIZATION — Track B curriculum slices (Crew 5)

**Status:** implements frozen prereg items **T-11** (slice size/count/assignment/flaw
density), **§4 B.4** (TST-1 STIMULUS_REF), **§4 B.7** (flaw placement support),
**§5 M-30** (corpus hashes). Prereg items are PROPOSED per the freeze file's own
status line; this document operationalizes schematic points. Nothing here changes a frozen bar.

## §1 — Slice plan (SLICE-V1)

### 1.1 Size legs (test-both bracket on the load-bearing choice)

Slice size is the load-bearing judgment call (too small: no vocabulary to teach;
too large: unwieldy sessions, sparse flaws), so per RULE-2 it runs as **bracket
legs**, all three built, every teacher arm trains on all three at 1x:

| leg | slice bytes S | status |
|-----|--------------|--------|
| 64K | 65,536 | bracket low |
| 256K | 262,144 | **default** |
| 1M | 1,048,576 | bracket high |

All sizes are far below the 2^25 (33,554,432) znc slice-indexing wall; the
builder asserts `slice_bytes < 2^25` and aborts otherwise.

### 1.2 Boundaries — deterministic function of (corpus, index)

No RNG anywhere. For corpus C with byte length L and leg size S:

- `eligible_end = floor(0.9 * L)` — slices are drawn from bytes
  `[0, eligible_end)` only. The last 10% of each corpus is the **M2 T1 held-out**
  (prereg §5: "last 10% of each corpus by fixed byte offset") and is excluded
  from teaching **by construction** — a teacher arm can never see held-out
  material, so T1 novelty is structural, not trusted.
- `K = min(8, floor(eligible_end / S))` — the 1x slice count for this
  (corpus, leg). Cap 8: 8 slices per corpus type gives 96 flaw judgments per
  type per arm per leg at 1x, paired across arms; more is the 10x leg's job.
- Slice `i` (0-based, `i < K`) = bytes `[i*S, (i+1)*S)` — aligned, disjoint,
  full-size by construction (K guarantees `(i+1)*S ≤ eligible_end`).

Consequence (declared, not a choice): at the 1M leg Shakespeare's eligible
region (5,074,632 bytes) yields K=4, sqlite3.c (8,563,806) yields K=8.
Prose/code are never averaged anywhere in the scorecard, so the asymmetry is
harmless; within-leg arm comparisons stay paired.

### 1.3 Corpus assignment and slice IDs

| corpus | tag | file | bytes | SHA-256 (pinned, M-30) |
|--------|-----|------|-------|------------------------|
| Shakespeare prose | SHK | pg100.txt (Gutenberg #100) | 5,638,480 | `3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37` |
| sqlite3.c code | SQL | sqlite3.c (amalgamation 3.53.4) | 9,515,341 | `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189` |

Slice ID: `{TAG}-{LEG}-{INDEX:04d}`, e.g. `SHK-256K-0003`, `SQL-1M-0007`.
44 slices total: SHK 8+8+4, SQL 8+8+8.

### 1.4 Scale legs — 10x = more slices, never bigger slices

Per the scale-leg note: slice byte size is fixed across scale legs. The 10x
curriculum = **10 session variants per 1x slice** (rep index r = 0..9):

- session variant key: `1x` (one session), `10x-R0` … `10x-R9` (ten sessions).
- Slice **bytes, ground-truth inventory, and the 12 FLAW-V1 flaw slots are
  identical across reps** (declared) — 10x is a repetition/retention
  stressor, which is exactly what the retention (10%) and revisability (25%)
  verdict weights need. The flaw map is a pure function of the slice id
  (FLAW_PLACEMENT.md), so every rep on a slice plants the same 12 slots.

1x sessions per arm: 44 (16 + 16 + 12 across legs) → 528 flaw judgments.
10x sessions per arm: 440 → 5,280 flaw judgments. One session's stimulus =
exactly one slice's bytes (see STIMULUS_TAPE.md).

### 1.5 What the builder is (and is not)

`builder/build_curriculum.py` is **corpus prep only** — it cuts bytes, counts,
and hashes. It never participates in any AI decision path (no teacher, no
learner, no scorer calls it at trial time; the harness reads its committed
outputs). It is written in Python rather than Zag deliberately: the builder
needs exact SHA-256/file/Unicode-free byte handling, and znc has three
characterized miscompiles on record (ZNC-2026-09-19-001 et al.) — a silent
miscompile in *corpus prep* would poison every downstream trial. The script is
deterministic by construction (no RNG, no clock, no network, no locale; every
ordering is an explicit sort; JSON output uses `sort_keys` + fixed
separators). Byte-identical output across runs is verified in VERIFICATION.md.

## §2 — Ground-truth unit inventory (G-V1)

The deterministic "correct" vocabulary per slice: the answer key for M1-style
mastery scoring and the arm-5 oracle's answer function. **Never shown to the
learner** (seal rule: `sealed/README_SEAL.md`). Any auditor reproduces it
exactly by running `builder/build_curriculum.py` or reimplementing the steps
below — both are specified to the byte.

### 2.1 Procedure (frozen as G-V1)

Given slice bytes `B[0..n)` and corpus type:

1. **Candidate extraction** (single left-to-right pass):
   - *prose*: maximal runs of ASCII letters `[A-Za-z]`, length ≥ 2.
     (Single letters excluded by declaration — they are trivially learnable
     and would inflate mastery counts; the exclusion is documented, not hidden.)
   - *code*: maximal C-identifier runs (`[A-Za-z_][A-Za-z0-9_]*`, length ≥ 2)
     occurring in **code state only**. Comments (`//…`, `/*…*/`) and
     string/char literals (`"…"` with `\"` escapes, `'…'` with `\'` escapes)
     are excluded by a deterministic 5-state lexer (CODE, LINE_COMMENT,
     BLOCK_COMMENT, STRING, CHAR). Rationale: the taught vocabulary for code
     slices is code units, not English words inside comments. The lexer is a
     lexical approximation, not a C parser — sufficient because its only
     contract is determinism, documented here.
   - Record every occurrence as `(start_offset, raw_bytes)`.
2. **Canonicalization**: prose → ASCII lowercase fold (`bytes.lower`, exact);
   code → identity (C is case-sensitive).
3. **Counting**: exact occurrences of each canonical form within the slice.
4. **Recurrence filter**: keep canonical forms with `count ≥ REC_BAR = 3`.
   (Flat across size legs by declaration — leg effects then show up honestly
   in inventory sizes instead of being normalized away.)
5. **Ordering**: sort by `(count descending, canonical bytes ascending)` —
   total order, no ties possible.
6. **Entry**: `{u: canonical bytes (ASCII), count, first: smallest start
   offset among occurrences}`.
7. **Inventory hash**: SHA-256 over the canonical serialization —
   per entry in order: `u32LE(len) || unit_bytes || u64LE(count) ||
   u64LE(first_offset)`, concatenated. Recorded in the manifest as
   `inventory_sha256`.

### 2.2 Sizes (measured, committed)

| leg | slices | stimulus/arm@1x | ground-truth units | flaw slots |
|-----|--------|-----------------|-------------------|------------|
| 64K | 16 | 1,048,576 B | 5,138 | 192 |
| 256K | 16 | 4,194,304 B | 16,671 | 192 |
| 1M | 12 | 12,582,912 B | 33,059 | 144 |
| **total** | **44** | | **54,868** | **528** |

Smallest inventory: 24 units (a 64K code slice) — every slice clears the
≥12 units the flaw-slot function requires (builder asserts, aborts otherwise).

### 2.3 Scoring interfaces (for the scorer / Crew 4 / Crew 6)

- **Mastery hit (type-level)**: a learner-held unit is a hit iff its
  canonical bytes (same canonicalization as §2.1 step 2) are in the slice's
  inventory unit set. For REVISE verdicts, the *revised* span's canonical
  bytes are compared. Precision = hits / learner units; recall = hits /
  inventory units. (The verdict-weight math is T-14's, frozen; this is the
  hit definition it consumes.)
- **Arm-5 oracle answer (occurrence-level)** — reference implementation in
  `builder/oracle_ref.py`, frozen semantics:
  `ORACLE_ANSWER([s,e)) = YES` iff (a) `canonical(B[s:e])` ∈ inventory unit
  set **and** (b) `[s,e)` exactly equals a candidate occurrence from the G-V1
  extraction pass. Consequences, all deliberate: querying "the" inside "there"
  is **NO** (fragment, not an occurrence); a span exactly covering a real
  candidate that fell below REC_BAR is **NO** (not inventoried); out-of-range
  spans are malformed input — the harness rejects them, they are never
  silently answered.
- **M1-style byte-exactness**: inventory units are byte strings; a hit
  requires byte-exact canonical equality. No fuzzy matching anywhere.

## §3 — Flaw-placement support (summary; normative spec: FLAW_PLACEMENT.md)

12 flaws per slice (same 12 for the 1x session and every 10x rep), frozen composition per T-3:
4 wrong-span, 4 false-confidence, 2 missing-grounding, 2 plausible-false.
Crew 5 and Crew 4 derive slots from the **same deterministic function of the
slice id** (FLAW-V1, fully specified in FLAW_PLACEMENT.md —
standalone, no cross-crew blocking): `SHA-256("TNN-TB-FLAW-V1" || 0x00 ||
slice_id || flaw_index)` drives target-unit selection
(`u64be(h[0:8]) mod N_units`), shift magnitudes/directions
(`1 + u64be(h[8:16]) mod 16`, clamped in-slice), and plausible-false
mutations (first zero-count single-byte mutation in a deterministic walk —
verified zero-count by construction). Slot maps are committed under
`sealed/` (seal rule: harness must never expose them to the student process;
auditors may recompute them from the public function).

## §4 — Stimulus tape (summary; normative spec: STIMULUS_TAPE.md)

The shared stimulus for a session is **exactly one slice's bytes,
verbatim**, carried in the tape's stimulus segment. `STIMULUS_REF` references
it by `{slice_id, corpus, corpus_sha256, byte_start, byte_end, slice_sha256,
inventory_sha256, slice_bytes, size_leg, scale_leg, rep_index,
held_out_start}` — content-addressed by SHA-256; the harness verifies
`SHA-256(stimulus) == slice_sha256` (and the inventory hash) before session
start and before replay, else aborts. **§P span offsets are slice-relative**
(byte 0 = slice byte 0): tapes are self-contained, replay never needs the
full corpus, and flaw/manifest coordinates stay valid across scale legs.

## §5 — Files

- `fetch/fetch_gutenberg_100.sh`, `fetch/fetch_sqlite_amalgamation.sh` —
  on-demand corpus fetch (corpora never committed).
- `PROVENANCE.md` — public-domain provenance + pinned corpus hashes (M-30).
- `builder/build_curriculum.py` — the deterministic builder (SLICE-V1 /
  G-V1 / FLAW-V1). `builder/oracle_ref.py` — arm-5 oracle reference.
- `manifests/slices_manifest.json` — 44 slices: id, corpus, byte range,
  slice SHA-256, inventory SHA-256, unit count. Manifest SHA-256:
  `c26a5ca7c724dcb49752762be3e4c1c7ea3cfd3bcc3fde058b92a011ac7ab25a`.
- `inventories/<slice_id>.json` — ground-truth unit lists (answer key).
- `sealed/slot_maps/<slice_id>.json` — the 12 FLAW-V1 flaw slots per slice
  (identical for 1x and all 10x reps). Sealed from the learner per T-4.
- `STIMULUS_TAPE.md`, `FLAW_PLACEMENT.md`, `sealed/README_SEAL.md`,
  `VERIFICATION.md`.
