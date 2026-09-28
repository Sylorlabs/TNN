# ZNC-2026-09-21-007 — Predictive Offset Rule

**Date:** 2026-09-24 (PDT) · **Investigator:** offset-rule subagent
**Compiler (all results):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
**SHA-256:** `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
**Workdir:** `~/workspace/i32-investigation/offset-rule/` (configs, bins, raw outputs, gen.py)

## 1. The rule

For `let x:[]T = nio_alloc(B) as []T` with `T ∈ {i32,u32,u16}` (the mistyped casts),
consecutive heap blocks are spaced `S(B) = round_up_pow2(B) + 8` bytes apart, and
**every indexed access is compiled with ×8 byte scaling** (see §2). Therefore, for
two consecutively allocated arrays `a` (Bₐ bytes) then `b`:

```
b[t]  ≡  a[ S(Bₐ)/8 + t ]        (indices in Zag source terms, i.e. ×8 slots)
```

i.e. `b`'s slot `t` is the same physical address as `a`'s source-index
`S(Bₐ)/8 + t`. The "alias offset" is `S(Bₐ)/8`, determined **only** by the previous
array's byte size — not by element type, array count, or prior allocation history.

Byte form: `addr(b[t]) = addr(a[0]) + S(Bₐ) + 8·t`.

Worked examples (all confirmed by bidirectional clobber tests, §4):

| Bₐ (bytes) | round_up_pow2 | S(Bₐ) | offset (×8 slots) | configs |
|---|---|---|---|---|
| 16 | 16 | 24 | **3** | K_e004 |
| 28 (7×u32) | 32 | 40 | **5** | L_e007 |
| 32 | 32 | 40 | **5** | A_e008 |
| 64 | 64 | 72 | **9** | A_e016 (= the 2026-09-21 probe's 9–11) |
| 128 | 128 | 136 | **17** | A_e032, C4, F_u16_64x2 |
| 192 | 256 | 264 | **33** | A_e048 |
| 256 | 256 | 264 | **33** | A_e064, C1, C3, F_u16_128x3 |
| 400 | 512 | 520 | **65** | A_e100 |
| 512 | 512 | 520 | **65** | A_e128, B_m3/4/5, C2, F_u32_128x3 (= CERT RV3's 65–67), H_struct, J_gap |
| 800 | 1024 | 1032 | **129** | A_e200 |
| 1024 | 1024 | 1032 | **129** | A_e256 (partial — segfault, §6), G_i64_128x2 |
| 2048 | 2048 | 2056 | **257** | A_e512 (partial — segfault, §6) |

Interleaved/dead allocations just add their strides: D1 (512B i32 + dead 512B u8 +
512B i32) → offset 130 = (520+520)/8 ✓; D3 (512B + dead 64B) → 74 = (520+72)/8 ✓.
Pre-allocations (E1–E3), junk statements (J_gap), and struct fields (H_struct) do not
change the rule. Mixed sizes chain per-link: C3 (256B→512B→1024B) gives 33 then 65 ✓.

## 2. Root cause (disassembly, not inference)

`objdump -b binary -m i386:x86-64` on minimal probes shows the index-addressing
sequence for **every** `as []T` indexed access (T = i32, u32, u16, i64, u64):

```
pop   %rax                  ; rax = slice.ptr
mov   $0x8,%rdx
imul  %rdx,%rcx             ; rcx = index * 8      <-- should be ×4/×4/×2/×8/×8
add   %rcx,%rax
mov   %rax,0x0(%rcx)        ; 8-byte store (i32/u32: value pre-wrapped to 32 bits)
```

and symmetrically `mov 0x0(%rax),%rax` (8-byte load; i32/u32 masked to 32 bits and
sign-extended, u16 masked to 16 bits). **The compiler scales every cast-slice index
by 8 bytes regardless of element type.** Native `[]u8` (no cast) correctly uses ×1
with single-byte accesses — so the bug is specific to the `as []T` cast lowering.

Consequences, all following from the ×8 scaling plus `len` kept in **bytes**:

1. **Footprint 2× (i32/u32) / 4× (u16) the allocation.** `a[t]` touches byte `8t`;
   indices `t ≥ B/8` write/read past the `B`-byte block into the heap/next block.
2. **The "aliasing" is address coincidence, not read substitution.** `b[t]` lands at
   `b.ptr+8t`; with `b.ptr = a.ptr+S(Bₐ)`, that equals `a`'s ×8-slot `S(Bₐ)/8+t` —
   which is `b`'s own block. Filling `a` past `B/8` **writes into `b`'s block**
   (proven by clobber tests both directions); reads are faithful to the (wrong)
   address. The 2026-09-21 "b[0..2] read a's slots 9–11" = `a`'s fill wrote `b`'s
   slots 0–2 (B=64: `a[9..15]` → bytes 72–128 = `b`'s bytes 0–56).
3. **Bounds check is against byte length** (`t < B`), so indices up to `B-1` pass
   while only `t < B/8` are in-bounds — the compiler itself permits the OOB.
4. Single arrays are "fine" only in the self-consistent sense; `t ≥ B/8` still
   escapes the block.

## 3. i64 / u64 verdict — CLEAN (re-verified 2026-09-24, writes included)

×8 is the **correct** stride for 8-byte elements: asm shows full 8-byte stores with
no truncation and 8-byte loads with no masking for `as []i64` / `as []u64`, in
plain, struct-field, and function-parameter forms. Runtime write-focused probes
with high-bit 64-bit patterns (`0xAAAAAAAAAAAAAAAA`, `0x5555…`, `0x1234…`), all
byte-identical across 2 runs:

| probe | layout | result |
|---|---|---|
| u64w1 | 3× consecutive u64 512B, overwrite cross-talk check | 0 bad, 0 cross-talk — CLEAN |
| u64w3 | u64 256B+512B+1024B consecutive | 0 bad — CLEAN |
| u64w4 | u64 512B pair with dead []u8 between | 0 bad — CLEAN |
| u64forms | u64 via struct field + fn param, write then read | 222 == 222 — CLEAN |
| i64w1 | 3× consecutive i64 512B, overwrite cross-talk check | 0 bad — CLEAN |
| G_u64_64x3 / G_i64_64x3 / G_i64_128x2 / G_i64_16x2 / G_mix_* | matrix sweep | offsets match rule (benign geometry) — CLEAN |

**The 2026-09-21 harness-audit lead** (`ZNC007_AUDIT.md` site 3: "empirically
observed `as []u64` indexed-write corruption") does **not** reproduce as a u64
codegen bug. It is explained as **victimhood**: a correctly-compiled u64/i64 array
placed *after* a mistyped i32/u32/u16 array is clobbered by the mistyped array's
2×/4× write footprint:

| probe | layout | result |
|---|---|---|
| u64w2 | i32 512B then u64 512B; i32[0..127] written | **63/64 u64 slots clobbered** (model-exact: `a[65..127]` → u64 bytes 0–503) |
| i64victim | i32 512B then i64 512B | **63/64 i64 slots clobbered** — identical |
| u64w5 | u64 512B *before* i32 512B | 0 bad — CLEAN (footprint extends forward only) |

**Disposition of CAST_AUDIT.md §5 / Appendix A (11 functions, PROVISIONALLY-OK):**
no change — they stay PROVISIONALLY-OK, **not** upgraded to SUSPECT. Rationale:
u64/i64 indexed writes are proven correct, and none of the 11 functions has a
mistyped (`i32`/`u32`/`u16`-cast) neighbor that could victimize the u64/i64 arrays:
`audit281.zag::main` and `run_battery.zag::main` sit in i64-only neighborhoods;
the five learner test drivers use i64 pairs only (zero mistyped casts in file);
`harness.zag` med_init/test_smoke u64s neighbor only []u8 and u64 (never indexed /
test scaffolding per the audit). Upgrade to SUSPECT would require a mistyped array
immediately *before* an indexed u64/i64 array — a pattern worth grepping for in
future audits (victim scan), but not present in these 11.

## 4. Method

- **Bidirectional clobber tests** (not passive reads): for each consecutive pair
  (j→k), write magic to `b_j[t]` (t=0..2), read all of `a_k`; then write magic to
  `a_k[s]`, read `b_j[t]`; restore. A hit requires the value to *change* in both
  directions (`R CLOB` + `R CLOBV` lines). 35/38 matrix configs byte-identical
  across 2 runs; 9/9 u64/i64 probes byte-identical across 2 runs.
- Generator: `gen.py` (38 configs: E-sweep 8–512, counts 2–5, mixed sizes, dead
  interleave, pre-allocs, u32/u16/i64/u64, mixed i32/i64, struct, single, gap).
- Fills use per-array value planes (`(k+1)*P + s`) so cross-array writes are
  attributable; tail reads verify before sweeps.

## 5. Strongest three data points

1. **Disassembly of the index scaling** (`bin/min2`, `bin/scale`): `mov $0x8,%rdx;
   imul %rdx,%rcx` before *every* `as []T` access (i32/u32/u16/i64/u64), vs no
   scaling for native `[]u8`. Single root cause, no statistics needed.
2. **30/30 measured offsets equal `(round_up_pow2(B_prev)+8)/8`** across B = 16…
   2048, types i32/u32/u16/i64/u64, counts 2–5, mixed sizes, interleaves, and
   pre-allocations — including the non-obvious power-of-2 rounding (192→256,
   400→512, 800→1024) which the naive `B/8+1` rule gets wrong.
3. **u64w2 victim proof**: i32[0..127] writes clobber exactly u64[0..62] (63/64),
   first bad slot 0 — byte-exact match for the footprint model, explaining the
   audit's "u64 write corruption" without any u64 codegen defect.

## 6. Surprises and open edges

- **Power-of-2 rounding**: `nio_alloc` rounds the request up to a power of 2
  before the +8 stride (192→256, 400→512, 800→1024). Offsets for non-pow2 sizes
  follow the *rounded* size. (Inferred from 3 data points; mechanism — buddy
  allocator vs size classes — not identified.)
- **The +8 stride constant** (B=512→520, B=64→72): consistent across all 30
  points; plausibly an 8-byte heap header, not proven.
- **Segfaults are data**: A_e256/A_e512 (B=1024/2048) and F_u16_256x2 (4×
  footprint) segfault mid-sweep — heap corruption from footprint overflow. Their
  partial outputs still confirm the predicted offsets (129, 257, 65) before
  dying. K_e004 initially panicked on the *probe's* sweep exceeding the
  byte-length bounds check; capping the sweep at `len` fixed it (offset 3 ✓).
- **Non-multiple-of-8 strides** (B+8 not divisible by 8, i.e. odd i32 counts)
  would misalign the overlap; not probed — the rule's integer form assumes
  `(S(Bₐ)/8)` integral.
- `as []u8` cast form (cast back to u8) not probed; native []u8 is ×1-correct.

## 7. Workaround (unchanged, strengthened)

Never use `as []i32` / `as []u32` / `as []u16` for indexed tables — use `[]u8`
arenas with explicit LE accessors. **Extended**: never place an indexed
`as []u64`/`as []i64` array immediately *after* a mistyped cast array either —
the u64/i64 codegen is correct but the neighbor's footprint will eat it. Audit
check: for each indexed u64/i64 array, confirm the preceding heap allocation is
not a mistyped cast (or any writer with a >1× footprint).

## Artifacts

- Reproducers: `configs/*.zag` (38 matrix via `gen.py` + `min2`, `scale`,
  `u64syn`, `u64w1`–`u64w5`, `u64forms`, `i64w1`, `i64victim` hand-written)
- Raw outputs: `raw/*.stdout` (44 files, each byte-identical across 2 runs;
  A_e256/A_e512/F_u16_256x2 partial — segfault, see §6)
- Binaries: `bin/*` · Manifest: `manifest.json` · Runner: `run_all.sh`
- Key disassembly notes: §2 (full dumps reproducible via
  `objdump -b binary -m i386:x86-64 --adjust-vma=0x400000 -D bin/<name>`)
