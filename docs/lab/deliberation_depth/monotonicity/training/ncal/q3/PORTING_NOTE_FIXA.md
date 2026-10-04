# PORTING NOTE — fixbuild.py → fixbuild.zag (pure-Zag FIX fixture generator)

Date: 2026-09-25. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

## What was ported

`q3/fixbuild.py` (Python, deterministic) → `q3/fixbuild.zag` (pure Zag,
deterministic, zero RNG). Same CLI: `fixbuild <base.tsv> <FIX-A|FIX-B|FIX-C|FIX-D> <out.tsv>`.
All four FIX variants ported; FIX-A is the adopted one.

## Semantic equivalences (the non-obvious ones)

1. **Anchor count (FIX-A): pure integer math.** Python computes
   `need = math.ceil((0.95*t - c)/0.05)` in float. In exact real arithmetic
   `(0.95*t - c)/0.05 = 19*t - 20*c`, always an integer. Verified on all real
   inputs (s1/s10/s100, 84 class-legs): float `ceil` == `19*t - 20*c` in every
   class where anchors are added (0 diffs). The Zag port uses `need = 19*t - 20*c`
   (i64) — no floating point anywhere.
2. **Skip condition (FIX-A).** Python: `c/t >= 0.95` (float division). Zag:
   `20*c >= 19*t` (integer). Verified equivalent on all 84 class-legs (0 diffs);
   boundary flips are impossible here (|c/t − 0.95| ≥ 1/(20t) ≫ ULP for t ≤ 5e5).
3. **Class bins.** `min(f1//150,6)*5 + min(f5//250,4)`. Inputs have
   f1 ∈ [100,1000], f5 ∈ [20,1000] (all ≥ 0), so Python floor-division ==
   Zag truncating division.
4. **IDs.** Python `f"A{cls:02d}{j:06d}"` (uppercase prefix) with lowercase fam
   `a`; same for `C`/`c`, `T`/`t`. Zag formats identically (zero-pad to minimum
   width, never truncated — matches Python's `:06d` for j ≥ 10⁶).
5. **Interleave.** Python sorts placements by (pos, group, seq) with
   pos = (j*n)//a. Zag does a K-way merge: groups in ascending key order
   (class ints; FIX-B single group), per-group cursor emitting while
   (j*n)//a ≤ i before base row i. Same total order; trailing flush kept
   (no-op since pos < n always).
6. **FIX-C global trap counter.** Python's `j` increments per appended trap in
   row order across classes; Zag assigns the same counter during its row-order
   pass and stores it per item.

## znc constraints honored

- No `as []i32`/`as []u32` casts (ZNC-2026-09-21-007): all tables are `[]u8`
  arenas with `au_get32/au_put32/au_get64/au_put64` LE accessors.
- No single slice > 2^25 bytes: input read whole (s100 = 24.8MB < 33.5MB);
  row metadata/pools/anchor items in separate arenas; **output streams** in
  1MB flushes through a chunked truncating-write fd (FIX-A s100 output is
  33.27MB — a single-slice buffer would panic).
- Struct (`FxOut`) only touched through `*FxOut` parameters; no bare blocks;
  `return;` in void fns.

## Equivalence proof (byte-identity, SHA-256)

| Input | FIX | Python SHA-256 | Zag SHA-256 | Match |
|---|---|---|---|---|
| s1 | A | 19a55e961f15f5cbe7e9002faa234f03affa9fbe2d8b9f57f3ef284d3c75eda1 | same | YES |
| s1 | B | 13872571f2e432ee5c21abf337d1617df067212f7bd5d4c85d994eae4a2eff49 | same | YES |
| s1 | C | 561c2b2ac9e24328071a9f45e6fe5661e16873badf74e23aa22d5162c2044880 | same | YES |
| s1 | D | 3cf206da5d4a4a543c41391bcfd3184ad475a450ea7be32584d787c544dd5f19 | same | YES |
| s10 | A | 1d8d05c42d3c017aa98eeb9212aa6e2f6c4b4cf6a9d5f6a21a998838d539fd42 | same | YES |
| s100 | A | 1a29be570ba3fe83adb6c66b5500a515cf1eb8a8a58c59d70f14081c541e41a5 | same | YES |

(One transcription bug caught by the proof: initial build emitted lowercase
`a`/`c`/`t` ID prefixes; Python uses uppercase `A`/`C`/`T`. Fixed; proof
re-run clean.)

The s100 FIX-A output (33,273,050 bytes, 850,600 rows) is byte-identical,
proving the streaming path.

## Deletion

`q3/fixbuild.py` deleted from the repo in the same commit as this port
(Micah: "make it zag, delete the python"). Reference Python outputs above
were generated from the deleted file before removal; the proof stands on
the recorded SHAs.

## Committed source

`q3/fixbuild.zag`, SHA-256
`0086932eaa72aa7c839ae05854d1ddff0e686b4050c1fde4f0047c46895d06a4`.
Two defects found and fixed during the port (both caught by proof/edge
inputs, proof re-run clean on the final source):
1. Lowercase `a`/`c`/`t` ID prefixes vs Python's uppercase `A`/`C`/`T`
   (caught by the s1 byte-identity proof).
2. `nio_alloc(0)` empty-pool check misfire + anchor-item arena sized at
   `nrows` instead of the exact per-class need (caught by the trap
   batteries: a class needing 330 anchors from 150 base rows). Anchor
   arena is now sized from a pre-pass over exact per-class needs.
