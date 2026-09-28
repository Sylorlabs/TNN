# ADDENDUM — JOB 1 NEEDS-WORK fix round (FIX1): dated pre-run freeze (2026-09-25)

- **Status:** FROZEN — 2026-09-25 (PDT). Committed BEFORE the fix
  build/scored validation runs, per PREREG_NCAL_V3B_FROZEN.md §2.2
  NEEDS-WORK path.
- **Parent:** `PREREG_NCAL_V3B_FROZEN.md` §2.2; red-team verdict
  `job1/VERDICT_JOB1.md` (RT-F white-box diagnosis, committed same
  round).

## The break (RT-F)

`src/nec_v2d.zag`: `nec_cmp_id` compares at most 63 id bytes
(`while(k<id.len && k<63)`) and returns 0 (no match) whenever
`id.len > 63`. `nec_store` persists only the first 63 bytes + NUL.
Therefore an item id longer than 63 bytes NEVER matches its own
slot. Every observation is treated as a first observation:
conf = d1prior = 950 on every cell, personal ledger never accumulates.
Confirmed on the binary: 72-char always-wrong ids emit 950 on all 25
cells (|err|=0.95/cell, systematic); short-id controls correct.

## The principled in-class fix (FIX1)

Lookup correctness, not a mechanism change. No bar, threshold, or
confidence rule is touched.

- Slot layout: instead of a 64-byte id-text copy, each 64-byte slot
  stores two i64s — the id's byte offset in the input buffer (`ibuf`)
  at i64-index `n*8`, and the FULL id length at i64-index `n*8+1`.
  (16 bytes used; slot stride unchanged.)
- `nec_cmp_id(id, slots, slot, ibuf)`: reads (offset, length);
  returns 0 if lengths differ; else compares all `id.len` bytes
  against `ibuf[offset..offset+len]`. No length cap — arbitrary id
  lengths are handled (this also removes the arbitrary 63-char hard
  limit, per standing law).
- `nec_find` gains an `ibuf` parameter, passed through.
- `nec_store(id, idoff, …)`: records `(c0s, id.len)`; no byte copy.
- Call sites: `nec_find(…, ibuf)`; `nec_store(id, c0s, …)`.

## Pre-registered validation (must ALL pass)

1. **Baseline preservation:** fixed binary reproduces the frozen
   adopted m20 outputs **byte-identically** at s1/s10/s100
   (SHAs `84ffaf89…`, `20ff1d10…`, `f6a38269…`). Any byte difference
   on ids ≤63 is a fix failure.
2. **Attack fixed:** on `rtf_collide.tsv`, long-id (72-char)
   always-wrong items emit `950,0,0,0,0` (was 950×25); long-id
   always-correct emit 950×5; byte-identical to short-id controls.
3. **Determinism:** A/B/C byte-identical on all validation runs,
   SHA-logged.
4. **Toolchain:** pinned `znc_linux_x86_64_abed8aa1` (`498abcb5…`),
   zero RNG.

## Scope

ONE fix round. Source: `job1/fix1/src/nec_v2d.zag` (full source copy
+ fix). Binary built locally only (never committed). Evidence:
validation outputs + SHA logs. If any validation fails, the fix is
rejected and RT-F is reported as break-with-fix-direction (not
adopted).
