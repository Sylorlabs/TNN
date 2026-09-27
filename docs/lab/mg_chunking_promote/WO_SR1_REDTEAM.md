# WO-SR-1 — production chunker scale repair: red-team report

Date: 2026-09-27. Branch: `tnn-native-lab`. Pure Zag, zero RNG.

## 1. White-box cause

Every live text-intake copy allocated its word table as two 256-byte arenas:

```zag
let woffs:[]u8=nio_alloc(256);
let wlens:[]u8=nio_alloc(256);
```

`enum_words` stores one little-endian u32 offset and one u32 length per word
(4 bytes each), so the tables hold exactly **64 words**. The fill loop had no
capacity check: word 65 wrote at byte offset 256, one past the end of the
slice, and the runtime raised `panic: slice index out of bounds` (exit 1).

The batteryfix copy had the identical defect a second time in `gran_split`,
which materialized per-sentence (granule) offset/length pairs into the same
256-byte table shape: more than 64 period-delimited sentences panicked.

## 2. Repair design (no cliff moved)

- `enum_words` still fills the first 64 table slots exactly as before, writes
  nothing when `n >= 64`, and now **returns the true word count** instead of
  the capped count.
- New accessors: `wt_nth` (scan to the k-th word), `wt_off`/`wt_len`
  (cache hit for k < 64, rescan for k >= 64), `wcur_next` (single-pass
  cursor: offset/length of next word, no table at all).
- `find_word` scans words directly instead of indexing the table.
- Every sequential word loop was converted to the cursor; every random read
  to `wt_off`/`wt_len`. The zoom/span machinery (`mg_zoom`, `soff`/`slen`,
  `zlog`) is untouched, so per-question zoom traces are byte-identical.
- Batteryfix additionally got unbounded granule addressing: `gran_split`
  materializes only its first 64 segments but returns the true count, with
  `gt_nth`/`gt_off`/`gt_len` streaming accessors; kinds 19/20 keep their
  delimiter through the accessors and kind 20 switches to word-space
  accessors over the selected granule.
- There is no new fixed limit: indices >= 64 rescan the original text, which
  is O(n) per access and unbounded. The 64-entry prefix exists only so that
  inputs <= 64 words produce byte-identical output.

## 3. Files fixed (4)

| repo path | before SHA-256 | after SHA-256 | after SHA-1 |
|---|---|---|---|
| `docs/lab/mg_chunking_promote/intake.zag` | `5a4e6789df98ba013dcaa06ff865604e93b887ed666827d82ec5db1db760b1bc` | `ffc9fe9d110662a89130ab1558375ebece7188904b3c0d916b3ec095c0506470` | `c557d1e957b902bfa9158c99cd58a1849a793938` |
| `docs/lab/mg_chunking_batteryfix/intake.zag` | `ba9d1bf772d43e7fab897ecc324b8a6cf8a98843d36895b896eb591852547665` | `7ca6ca3aa4ed2b7d8acb481b0340a098cbd0f5154d3394377b4efe2c6a8b0377` | `26ccbf08e181b9a6e86deb1aa49a24581504bb18` |
| `docs/lab/mg_chunking/intake.zag` | `86a2d38890793dd083fb97c199dc0ca06066c86936da6e34cf9fae0e3da7adaa` | `32f2557acbc0bd215262d49b0e1dfeb41759e11e2291dc12ff262b82f6d54467` | `a44d499b514ab0b9b085e53b2f5104a1d8da5d27` |
| `docs/lab/mg_chunking_learned/base.zag` | `db011722d1a64e65c453b88bac45901d54e466e013c0283ea88dbc0937613941` | `9734a37a2d07a15b0c57470e51e7470b003fa69b07ad9d03bcf495e109847d0d` | `313b3b4560da53d0e1391e4c054185447f8ca29f` |

Before blob ids (git): promote `a070410790686fe057dce4e6a3955c5111649c50`
(76,841 B); batteryfix `33cdbb40ef96…` (95,197 B).

Notes:
- `docs/lab/mg_chunking/intake.zag` is the promotion-evidence snapshot built
  by `build_promotion.sh`; the fix preserves its committed evidence output
  (see §5).
- `docs/lab/mg_chunking_learned/base.zag` defined the same defective
  `enum_words` but has **zero call sites** in `derive.zag`/all hand files, so
  only the guard was added (dead code, zero behavioral surface; verified by
  byte-identical `derive.zag` output).
- `docs/lab/mg_chunking_nextwall/battery2.zag` and
  `docs/lab/mg_chunking_promote/regress_degen.zag` import the promote intake
  and are covered by its fix (regress_degen verified byte-identical, §5).
- Frozen arms untouched: arm L `e74271015`, arm D `ab79f1a5c7d`
  (`docs/lab/native_authorship/chooser/dlib.zag`), trap battery `af629be25`.

## 4. Before evidence (panic)

Original production intake, boundary driver (flushed per case):

- 63 words: succeeds; 64 words: succeeds;
  **65 words: `panic: slice index out of bounds`, exit 1.**

Original batteryfix intake, 100 period-delimited sentences:
**`panic: slice index out of bounds`, exit 1** (granule table overflow).

## 5. After evidence (fixed)

### 5a. Boundaries and adversarial shapes (production intake, exit 0)

All `correct=1 native=1 fallback=0`:

| case | answer |
|---|---|
| 63 words, last word | `w62` |
| 64 words, last word | `w63` |
| 65 words, last word | `w64` |
| 100 words, last word | `w99` |
| 65th word spelled backwards (streaming index 64) | `46w` |
| count `w` over 100 words (cursor loop) | `100` |
| empty input | `0` |
| all spaces | `0` |
| no spaces, one word | `abc` |
| leading/trailing/doubled spaces | `w2` |
| one 60,000-byte giant word, length | `60000` |
| count `x` in giant word (cursor) | `60000` |
| 10,000 words, last word | `w9999` |

Determinism: two independent runs byte-identical,
SHA-256 `89a64f54d0d2f95686c26d2cbddd4835d9084521da526503d8d8307cdad896ac`.

### 5b. Scale legs (production intake, exit 0)

60 / 600 / 6000 words: no panic at any leg; deterministic output SHA-256
`f148f925bba4a01492eb384d495d48defde9119340c141f1b36219f42fb5f714`
across two runs. (The driver's first probe per leg routes to the known
unrelated kind-0/WO-SR-2 coverage gap; all addressing probes pass. Not a
regression — the original panicked before reaching any probe.)

### 5c. Batteryfix granularity (100 sentences, exit 0)

| case | answer |
|---|---|
| kind 18: count sentences | `100` |
| kind 19: 70th sentence (streaming granule index 69) | `s69a s69b` |
| kind 20: 2nd word of 70th sentence | `s69b` |
| kind 19: 3rd sentence (cached path) | `s2a s2b` |

### 5d. Regression gates — all byte-identical before/after

| suite | result | output SHA-256 |
|---|---|---|
| promote 57-question battery | 57/57 correct, 57/57 native, 0 fallback | `0a34116398fcd22b313c785c1d1037d712a444f18b3925ce49ac29316a41d268` |
| batteryfix battery1 (57Q) | 57/57, 0 fallback | `170bacd71ba5f57c79be20786978964bbb094117e452b1a00d5289cbca351a23` |
| batteryfix battery2 (wall, 26Q) | 26/26, 0 fallback | `cd86da4355b6e059ea829c63ca41de63e4d7d0a0fea84773d661c1827f1be24b` |
| batteryfix battery3 (degen, 41Q) | 41/41, 0 fallback | `42fcb2c5e9eb138dab2838c22dd57453024c095ba88704a33e23870dcf0387ed` |
| mg_chunking snapshot (24Q, promotion evidence) | 24/24 — matches committed `25563035cdf8b1d9de0dd571445533edb7a3e1645d5a09ec54e94b4bf044d69e` | same |
| learned `derive.zag` (57Q) | 57/57, 0 fallback | `45780575f766cd28fc4805b076d43f445d1a68e4e99836b265562a7d622eadcb` |
| promote `regress_degen.zag` (6Q) | 6/6, 0 fallback | `8880c82e8cc99ac3a6a8671dd1daba779b9b2e766012e5f19068655a0064b3fb` |

## 6. Red-team notes

- Attacked shapes: exact 63/64/65 boundary, 100/600/6000/10000 words, no
  spaces, all spaces, empty, 60KB single word, irregular spacing,
  streaming index 64 (first uncached), streaming granule index 69.
- Two independent reruns of every battery above were byte-compared; all
  deterministic (pure Zag, zero RNG).
- Audited residual: `soff`/`slen`/`zlog` span tables keep their per-question
  zoom budgets (unchanged from the original design); the per-word zoom loop
  in the snapshot was converted to the cursor so its *word* reads no longer
  index the table, and zoom ids stay within the original budgets on all
  tested shapes. No new fixed cliff was introduced anywhere.
- Known unrelated gap (pre-existing, out of scope): the scale driver's
  kind-0 first probe documents a WO-SR-2 coverage gap; it fails identically
  on short inputs and is not caused by this repair.

## 7. Promotion note

The winning P4 arm must receive this production fix before promotion. Frozen
trial arms (L `e74271015`, D `ab79f1a5c7d`, trap battery `af629be25`) were
not modified.
