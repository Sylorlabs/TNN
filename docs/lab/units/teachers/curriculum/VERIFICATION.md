# VERIFICATION — curriculum build evidence (2026-09-21)

## V1 — Determinism: two full builds, byte-identical

```
python3 builder/build_curriculum.py --corpora-dir /tmp/tnn-corpora --out /tmp/tnn-build1
python3 builder/build_curriculum.py --corpora-dir /tmp/tnn-corpora --out /tmp/tnn-build2
diff -r /tmp/tnn-build1 /tmp/tnn-build2   # no output: identical
```

All 44 inventories + 44 slot maps + manifest byte-identical across runs.
(No RNG, no clock, no network, no locale in the builder — determinism is
structural, this is the receipt.)

Re-verified after the FLAW-V1 variant-key restoration (see commit
"restore leg-tagged session variants"): two fresh full builds with the
fixed builder are byte-identical to each other and to the build1
artifacts above (manifest `d16dc554…f002`).

## V2 — Manifest

- `manifests/slices_manifest.json` SHA-256:
  `c26a5ca7c724dcb49752762be3e4c1c7ea3cfd3bcc3fde058b92a011ac7ab25a`
- 44 slices: SHK 8×64K + 8×256K + 4×1M; SQL 8×64K + 8×256K + 8×1M.
- Every slice: `byte_end ≤ held_out_start` (no held-out violations); every
  slice `slice_bytes < 2^25`.

## V3 — Ground-truth inventories (independent spot checks)

- `SHK-256K-0000`: independent recount of `the` via `re.findall(rb'[A-Za-z]{2,}')`
  → 1335, matches manifest. Slice SHA-256 recomputed from corpus bytes → match.
- Inventory hash recomputed from the canonical serialization
  (`u32LE(len)||bytes||u64LE(count)||u64LE(first)`, sort `(-count, bytes)`)
  → matches `inventory_sha256`.
- Sort order verified total (`(-count, unit_bytes)` strictly increasing).
- Inventory sizes: min 24 units (64K code slice), max 4,709; total 54,868
  units across 44 slices. All ≥ 12 (flaw-slot requirement).

## V4 — Flaw slot maps (4 slices × 12 slots = 48 slots checked)

For `SHK-256K-0000`, `SQL-64K-0003`, `SHK-1M-0002`, `SQL-1M-0007` (slice bytes
re-cut from the corpus files and re-hashed against the manifest — match):
- exactly 12 slots with the frozen 4/4/2/2 type composition per slice;
- wrong-span: `shifted_span` in-bounds, `shift_applied` consistent,
  `base_span` bytes canonically equal the claimed unit;
- false-confidence: span in-bounds, span bytes equal unit,
  `confidence == 255`, `grounding == []`;
- missing-grounding: span in-bounds, span bytes equal unit, `grounding == []`;
- plausible-false: mutated unit has **zero** canonical occurrences in the
  slice (independent recount against the inventory unit set), same length
  and character class as base;
- the slot map is a pure function of the slice id: the 1x session and all
  10x reps on a slice plant the identical 12 slots (FLAW_PLACEMENT.md §1).

## V5 — Arm-5 oracle reference (`builder/oracle_ref.py`)

- YES on a true inventoried occurrence (`the` @ first offset).
- NO on a sub-span (`the` inside `there`) — occurrence-level, by design.
- NO on a span covering a real candidate below REC_BAR — by design.
- Out-of-range span raises `ValueError` (harness must reject, never silently answer).
- Same query twice → same answer.

## V6 — Corpus pins (M-30)

Builder aborts unless inputs match exactly:
`pg100.txt` 5,638,480 B `3cf4b3d4…110a37`;
`sqlite3.c` 9,515,341 B `b1dd5d74…1db28189`.
