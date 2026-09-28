# J1 Build Log

## 2026-09-21 — Initial implementation

### Source
- `cl/arm.zag` — single-file J1 implementation (~2200 lines)
- `substrate/R33_NATIVE_SHA256_V2.zag` — SHA-256 (copied from B-64 reference)
- `substrate/R33_NATIVE_IO_V1.zag` — I/O (copied from B-64 reference)

### Compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

### Defects found and fixed

1. **E0204 (bare blocks):** Bare `{...}` blocks with `let` confuse the parser
   ("top-level mutable globals"). Extracted to helper functions
   (`adv_covers`, `j_kill_range`, `j_fresh_recall`).

2. **j_led arity:** `j_defect_content` passed 18 args to 17-param `j_led`.
   Removed one zero.

3. **`~` operator:** Native codegen doesn't support bitwise NOT. Replaced
   `~X` with `(X^-1)` for i32, `(X^0xFFFFFFFF)` for u32.

4. **ShaCtx initializer:** `let ctx:ShaCtx;` without initializer fails
   ("aggregate let needs an aggregate initializer", ZNC-2026-09-21-004).
   Changed to struct literal `ShaCtx{.h0=..., .buf=b, ...}`.

5. **sha_final iput:** Used `iput(out, byte_offset, ...)` which writes 4-byte
   words at byte offsets (overlapping, out-of-bounds). Changed to byte stores
   `out[i]=... as u8`.

6. **slot_insert O(n²):** Scanned all `cap` slots per insert. Fixed to break
   at first never-used slot (probe chain terminator).

7. **Zeroing overhead:** Zeroed full 192MB slot table. Changed to zero only
   `cap*32` bytes.

8. **M8 hash bounds:** 32,000,000-byte chunks hashed as 1MB pieces; last piece
   ran past chunk end (32M not divisible by 1M). Fixed to clamp last piece.

9. **t_m1 probe bug:** A15 swap probes REPLACED normal recalls, causing
   7.6% recall. Fixed to do recall first, probe supplementally.

10. **Hash table load:** `cap = est + est/20` gave 88% load (too slow).
    Changed to `est + est/2` (≤67% load).

### SHA-256 self-test
`./work/j1 shatest` → `SHATEST,PASS`
Incremental implementation matches `ns_sha256` on "abc" and 1000-byte
multi-block input fed in odd chunks (7, 64, 300 bytes).

### znc bugs encountered
- ZNC-2026-09-21-004: annotated slice-let aliasing local struct field
- `~` not supported in native codegen
- Bare blocks with `let` cause E0204

### Performance
- System load ~15.8 on 2 CPUs (shared VM, other crews running).
- M1 prose (5.4MB, ~2M records): ~5-10 min under load.
- Fixed overhead per run: ~10s (mostly scheduling delay).

## 2026-09-21 — Battery runs
(pending)
