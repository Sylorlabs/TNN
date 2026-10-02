# BUILD.md — scale_learner.zag build recipe

## Toolchain

`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned lab build)

## Exact build invocation

```sh
cd ~/workspace/scale/driver
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  scale_learner.zag -o scale_learner --no-analyze
```

- `--no-analyze` skips the optional analyzer lint pass.
- Output: `scale_learner` (native x86-64 ELF, ~115KB). No external tools.
- Compile time: ~7s wall on the lab VM, 2026-09-21.

## Source layout

| File | Role |
|---|---|
| `scale_learner.zag` | The driver. Single self-contained file, pure Zag, zero RNG. |
| `probe_io.zag` | Build-time probe (not shipped): proved raw-syscall file reading works. |
| `ref/` | Reference material (class3-standardized driver/corpus, t5_core.zag, PREREG/VERDICT). Read-only lineage. |

## What was reused vs written

- **Reused (not reinvented):** the championship class-4 direct learning pattern
  and `t5_core.zag` decision logic — `t5_verify` ported identically,
  `t5_add`'s field writes / return codes / audit contents identical, the
  16-word audit entry layout identical
  (op@0 slot@4 rc@8 b1..b5@12..28 a1..a5@32..48 stage@52 d1@56 d2@60),
  lifecycle constants copied verbatim.
- **Changed for scale (documented, behavior-identical):**
  1. *Chunked memory.* Slot storage → 4096-slot × 24B chunks via pointer
     arena; audit ledger → 16384-entry × 64B chunks; id→slot index chunked
     too. No slice exceeds 2^25 at any N. At N=240k: 59 slot chunks,
     59 index chunks, 30 audit chunks.
  2. *O(1) duplicate check.* Dense id→slot index replaces the prototype's
     O(n) `t5_slot_find` scan (provably identical for dense ids; avoids a
     false superlinear-cost kill-bar trip).
  3. *Per-pass evidence buffers* (the championship's per-fact `t5_ev_init`
     leak becomes two per-pass buffers, reset per fact).
  4. *Slot layout fix.* The value i64 sits at offset 16 (bytes 16–23);
     an earlier draft placed it at offset 20, overflowing 4 bytes into the
     next slot — caught by a 240-fact loop test
     (recalled `0x00000001_00000005` instead of `5`).
- **New (harness-side, FACTSPEC.md frozen 2026-09-21):**
  - Runtime truth from Gutenberg bytes: 10 texts read via raw syscalls,
    words re-derived in Zag (ASCII-lowercased `[a-zA-Z]+` scan; count
    verified against frozen `.tnix` `n_words`), sentence/paragraph
    attribution from frozen `.tnix` (`word_sent`, `word_para`, `sent_para`)
    by word index, per-text FNV-1a frequency hash tables, `meta.json`
    parsed at runtime for `pub_year`/`title_words`.
  - All 24 categories implemented exactly (§3): word_len, alpha_first/last,
    vowel_count, consonant_count, vowel_groups, distinct_letters,
    word_mod97 (iterative mod-97, exact), sent_len_words,
    sent_pos_in_sentence, para_len_words, para_len_sents, word_len_next/prev,
    freq_in_text, is_long, text_words/sents/paras/unique/longest/avg100,
    pub_year, title_words.
  - splitmix64 implemented in Zag (verified byte-identical against Python
    on 5 test vectors; logical shifts via masking since Zag `>>` is
    arithmetic). `is_false(id)` ⟺ `draw(20260921,id) mod 100 < 5`
    (unsigned mod via `sc_urmod`); false supplied values per §4 formula.
  - Verified against materialized ground truth: all 240 `corpus_m10.json`
    rows (truth, supplied, is_false) match; all 114 `corpus_m100.json`
    false_ids match; M=10000 false rate 5.0146% matches spec's 5.015%.

## Truth at runtime: file reading vs embedded constants

`probe_io.zag` proved raw-syscall file IO works (open/read/close via
`_zag_raw_syscall`, exactly 7 args; NUL-terminated paths via `z_cstr`).
**Decision: runtime file reading.** The driver reads the 10 texts + 10
`.tnix` indexes + `meta.json` at startup. The learner never calls truth
functions (`sc_fact_truth`, `sc_supplied`, `sc_is_false` are harness-only;
`sc_teach_value` receives precomputed values).

Perf note: a fresh 8MB `mmap`+`munmap` per text cost ~0.3s wall each in this
sandbox (strace-verified); the driver reuses a single 2MB read buffer.
Corpus init (1.33M words + freq tables) is ~1.4s user, fixed.

## znc quirks respected

- Never `};` after a closing brace.
- Never gate `_zag_arg(n)` on `_zag_argc()` (argc arrives as 0); read
  unconditionally, treat `""` as absent.
- `[]u8` arenas + manual `sc_g32/sc_s32/sc_g64/sc_s64` (never the miscompiled
  consecutive `as []i32` cast pattern).
- Flat sequential `if`s, never 5-deep else-nesting.
- No `slice as *u8` casts; `_zag_slice_ptr` is the pointer API.
- `_zag_arg` results are non-owned (never freed); `_zag_i64_to_str` results
  are owned (freed after printing).
- Chunk `[]u8` values dropped after extracting data pointers; the underlying
  `_zag_malloc`'d memory is manual and never freed.

## Reproducibility

`run.sh` documents the argv convention and runs the N=240 5-rep
byte-identity check. No timestamps/PIDs/RNG; rep id is accepted but NOT
printed, so `diff` across reps is clean.
