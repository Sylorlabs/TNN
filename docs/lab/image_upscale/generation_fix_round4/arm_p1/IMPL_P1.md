# IMPL P1 — PLANE-only forcing mode ("fit planes everywhere")

Prereg: `~/workspace/upscale_r4/PREREG_R4.md` (frozen, arm P1). Implemented
2026-09-27. No post-result tuning; the battery runs belong to the battery
crew — only bridge + sky sanity here.

## Source

`azgen_p1.zag` — copied from committed C3 source
(`r3src/azgen_c3.zag`, SHA-256 `cd5bab26306ae4683eb4882faa864292dbf8130307cff92912d0027d2ca8418f`,
verified before editing) plus the minimal P1 change below.
`azlayers.zag` / `common_az.zag` / `R33_NATIVE_IO_V1.zag` mirrored next to
the source (SHA-identical to `upscale_gen/src/`); `@import` resolves
relative to cwd. `verify_force.py` is the trace/pixel verification script.

## Exact change (diff vs pristine C3)

1. Header comment documenting the preregistered P1 forcing mode and
   `argv(3)=="force"` flag — marked explicitly as preregistered, NOT a
   tunable.
2. `main`: `let arg3:[]u8 = _zag_arg(3);` read unconditionally (never gated
   on `argc`; `""` = absent → pure C3 behavior). `p1force = 1` iff
   `arg3 == "force"` (`_zag_strcmp` returns 1 on equality).
3. `gshapes_fit` gains a trailing `p1force:i64` param, threaded through all
   4 recursive calls and both `main` call sites (7 edits, mechanical).
4. In the `if (gain_take >= bar)` choice block: the least-squares plane fit
   (same `g_plane_fit` call, same `na`/`nb` buffers, same coefficient
   extraction) is now computed for EVERY region reaching the choice code
   (previously only non-ATOM ones); then `if (p1force == 1) { op = 1;
   gret = ex; }` pins the choice to PLANE-FIT. Evidence (`fok`, `mok`,
   `edge`, `pok`) is still measured and recorded identically.
5. PLANE take row: trace reason is `"p1_forced_plane"` when forcing (honest:
   the chooser was pinned, the frozen rule did not fire), else the C3
   `"plane_resid_le_e_half"`. Takes-row layout, construction, recursion,
   split logic, 9/value gain bar, LINES — untouched.

No new functions (no forward-ref risk), no new allocations, no `};`, no
identifier named `try`, no new `as []i32` casts (the pre-existing
`as []i64` plane buffers are unchanged and u64-clean).

## Build verdict

Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
built in `impl_p1/` (~7s). **Clean build** — the same 31 analyzer
warnings as pristine C3 (zero new warnings from the edit). A pristine-C3
reference binary built from the same dir also built clean. Binaries,
`.zag-cache`, and `.zagd.semantic-ready` were deleted after verification;
only sources remain.

C3-equivalence smoke test: P1 binary run **without** the flag on bridge
reproduces the pristine-C3 `upscale_gen.bmp` byte-identically
(SHA `5de1897b679ff735a…`) → the edit changes nothing when the flag is
absent.

## Determinism (all required)

| leg | upscale_gen.bmp SHA-256 |
|---|---|
| P1 force, bridge, run 1 (fresh outdir) | `fea34201b7821c0ead6b436ba269f789ce2eb69399a8c5b8bad6073aeca39c6b` |
| P1 force, bridge, run 2 (fresh outdir) | `fea34201b7821c0ead6b436ba269f789ce2eb69399a8c5b8bad6073aeca39c6b` |
| P1 force, bridge, `env -i`, different cwd | `fea34201b7821c0ead6b436ba269f789ce2eb69399a8c5b8bad6073aeca39c6b` |

All three byte-identical. C3 reference bridge output: `5de1897b679ff735a…`
(unchanged by the force run existing alongside it).

## Region-level force verification (bridge, `verify_force.py`)

Parsed `GEN_TRACE.txt` per-region rows from pristine-C3 and P1-force runs:

| | C3 | P1 (forced) |
|---|---|---|
| regions in trace | 49 | 49 |
| PLANE | 45 | 49 (all reason `p1_forced_plane`) |
| ATOM | 3 | 0 |
| MEAN | 1 | 0 |
| trace reasons | 45× `plane_resid_le_e_half`, 3× `f_le_1_4_and_m_ge_2`, 1× `no_model_vouched` | 49× `p1_forced_plane` |

- **45/45** C3-PLANE regions have a coincident P1 PLANE region with
  identical `(x,y,bw,bh,si)` geometry, and the rendered 2x pixels for all
  45 regions are **byte-identical** between the two outputs.
  → The force changes only the *choice*, never the PLANE rendering.
- P1 partition is identical to C3's on bridge (same 49 region rows), so no
  repartitioning confound: the 3 ATOM + 1 MEAN regions were re-rendered as
  planes with the exact coefficients C3's own (unused) plane fit measured.
- Every P1 forced row still records measured evidence (e, bsse, rsse, edge,
  fok, mok, pok) — honest trace.

## PSNR sanity (frozen metrics.py, SHA `82905ce5…`)

| image | baseline | C3 (rebuilt) | P1 (force) | P1 − C3 |
|---|---|---|---|---|
| bridge | 18.47 | **19.74** ✓ committed | **19.86** | **+0.12** |
| sky | 22.75 | **23.89** ✓ committed | **23.89** | 0.00 |

- Rebuilt pristine C3 reproduces both committed bridge/sky PSNRs exactly.
- Sky: C3 chose PLANE for all 31/31 regions (zero ATOM/MEAN takes), so P1 is
  byte-identical to C3 there (`e07382e5dba0429a…` both).
- Bridge: forcing PLANE on the 4 non-PLANE regions moved 19.74 → 19.86 dB
  (+0.12 vs C3, +1.39 vs baseline). Per the preregistered P1 readings, a
  bridge-only Δ within ±0.10 dB of C3 would already say the deliberation is
  decorative-or-harmful; this single image lands at +0.12 — the battery
  crew adjudicates the preregistered reading on the full battery. No
  tuning was performed; this number is reported as measured.

## Notes for the battery crew

- Run: `./azgen_p1 <indir> <outdir> force` (outdir must pre-exist). Omit the
  third arg for pure C3 behavior.
- `indir` must contain `input.bmp`, `vocab.bin`, `gt.bmp` (vocab.bin frozen,
  SHA prefix `cbead2f7c13e455f` — verified).
- `GEN_TRACE.txt` per-region reason for forced takes is `p1_forced_plane`;
  `op` census on forced runs is PLANE for every region reaching choice.
- Scratch binaries and all run outdirs were deleted; disk reclaimed.
  Sealed battery was never touched.

P1 COMPLETE
