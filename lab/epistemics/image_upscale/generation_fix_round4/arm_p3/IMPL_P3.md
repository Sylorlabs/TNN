# IMPL_P3 — Arm P3: inverted architecture (measured base, atoms as licensed residuals)

Implemented 2026-09-27 from the frozen `PREREG_R4.md`. Source: `azgen_p3.zag`
(SHA-256 `b77fe3eed5f79d98126eb818aa911049f5978e28e3bbc2268856173ef0787f19`,
1808 lines), derived from the verified round-3 C3 source
(`r3src/azgen_c3.zag`, SHA-256 `cd5bab26306ae468…` — verified byte-identical
before editing). Pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Build: `cd impl_p3 && znc azgen_p3.zag -o <bin>` (the three `.zag`
symlinks are build support pointing at the shared layer files in
`../recon_build/`; `@import("./azlayers.zag")` resolves from the build cwd).

## The exact mechanism

**BASE (measured ladder, frozen rule — C3's non-atom path, unchanged):**
per region reaching operator choice, compute the least-squares plane fit
(`g_plane_fit`, unchanged); base = PLANE-FIT iff plane residual ≤ e/2
(`2*resid <= e`, `pok=1`), else MEAN-FILL.

**LICENSED RESIDUAL (frozen rule):** iff the structural license holds
(`fok`: `4*bsse <= e` AND `mok`: `rsse >= 2*bsse` — the C1/C3 bars,
recorded in the prereg, not fit) AND the winner atom's key deviations over
the measured base reduce the measured residual energy on the block's
observed input-res pixels, stamp the atom's full-res deviations ONTO the
base. The atom never replaces the base. Regions failing either condition
keep the measured base. The pure ATOM-STAMP path (C3's op=0) does not exist
in P3.

**Honest-improvement arithmetic** (new `g_resid_check`, exact integer;
also documented in the source header):
- `px` = the pixels the fit/match measured (input workspace at fit time —
  the block's observed pixels).
- `baseval_c = m_c + g_pterm(na_c·u, da) + g_pterm(nb_c·v, db)` with
  `u = 2·xx−(bw−1)`, `v = 2·yy−(bh−1)`, `da = bh·g_csq(bw)`,
  `db = bw·g_csq(bh)` — the EXACT integer evaluation the commit and the
  2x render use. `(na_c, nb_c)` are the fitted plane slope numerators for
  a PLANE base, all ZERO for a MEAN base.
- `keydev_c = r_i16le(vbuf, vkb_si + best·kmb + (yy·s+xx)·6 + 2·c)` — the
  winner atom's RAW key deviations (the same raw deviations the commit
  subtracts; the render adds their full-res body).
- `sse_base = Σ_c Σ_px (obs − baseval_c)²`
- `sse_atom = Σ_c Σ_px (obs − baseval_c − keydev_c)²`
- Residual path iff `sse_atom < sse_base` (strict). The check vouches the
  atom's KEY form at input res; the render stamps the atom's FULL-RES body
  (its 2x2-box-downscale parent) — the same key/body relationship the
  baseline commit/render use. Operator-honest gain credited for op=3:
  `e − sse_atom`.

**Take encoding:** stride-16 rows, op at +6. **op=3 = PLANE+ATOM residual**:
+5 = winner atom index, +7..9 = block mean, +10..15 = base plane slope
numerators (fitted slopes for a PLANE base; ZEROS for a MEAN base, so the
render adds the atom deviations onto the flat mean). op=1 (PLANE-FIT) and
op=2 (MEAN-FILL via nofits) are C3's paths, unchanged.

**Render (op=3):** 2x pixel = base plane evaluated at 2x
(`up = ox−(bw−1)`, `vp = oy−(bh−1)`, same 2x evaluation as op=1) PLUS the
atom's full-res body deviations `r_i16le(vbuf, ab + (oy·S+ox)·6 + 2·c)`.
Labeled **3 (CONSTRUCTED-SHAPES)** — shapes-path construction; the trace
distinguishes op=3 from op=1 honestly, so the label is never misleading.

**Commit (op=3):** subtract `base + keydevs` at input res (same formula as
the honest check, so what is measured is what is subtracted).

**Trace:** per region — evidence (`e bsse rsse edge fok mok pok`) + base
choice (`base=PLANE/MEAN`) + license outcome + residual outcome
(`resok=0/1`) + reason string:
- `p3_base_plane_resid_licensed` / `p3_base_mean_resid_licensed` (op=3 taken)
- `p3_base_plane_unlicensed` / `p3_base_mean_unlicensed` (no license)
- `p3_base_plane_resid_rejected` / `p3_base_mean_resid_rejected`
  (licensed, but the honest-improvement check failed)

**Unchanged from C3 (byte-identical in rule):** matching, recursion, split
logic, the 9/value gain bar, the take gate (`e − bsse >= 9·nval`), commit
threshold (`Gh >= 9·Nh`), LINES path, label set, BMP/GEN_SCORES/TILES output
formats.

## Diff summary vs C3 (383 diff lines)

1. Header comment rewritten: P3 mechanism + honest-improvement arithmetic
   + op=3 take encoding (was C3 deliberation doc).
2. New `g_resid_check` helper (after `g_plane_fit`, callees-before-callers).
3. `g_tr_region`: +2 params (`baseop`, `resok`), prints `base=`/`resok=`,
   op=3 name `PLANE+ATOM`.
4. `gshapes_fit` deliberation: plane fit always computed; base = PLANE iff
   `pok` else MEAN; license (`fok && mok`) gates `g_resid_check`;
   `sse_atom < sse_base` → op=3 take (atom + base numerators in row,
   gain `e − sse_atom`); else op=1 take (gain `ex`, C3-identical) or
   op=2 nofit (gain 0). The op=0 ATOM-STAMP branch is deleted.
5. `gshapes_commit`: op=1 branch fenced, new op=3 branch (base + keydevs).
   The op=0 branch remains as dead-but-harmless documentation of the
   encoding (op=0 is never recorded in P3).
6. `g_render_shapes`: op=1 branch fenced, new op=3 branch (plane at 2x +
   full-res body deviations, label 3).
7. Trace banner line updated to P3.

## Determinism (bridge, `upscale_gen.bmp` SHA-256)

| run | SHA-256 |
|---|---|
| bridge run 1 | `937b7fdbd0cda9c8a37f544d10f055735f4e8169caf1a02c136ec2505431eb42` |
| bridge run 2 (fresh outdir) | `937b7fdbd0cda9c8a37f544d10f055735f4e8169caf1a02c136ec2505431eb42` |
| bridge run 3 (`env -i`, fresh outdir) | `937b7fdbd0cda9c8a37f544d10f055735f4e8169caf1a02c136ec2505431eb42` |

Byte-identical across 2× reruns + allocator-perturbation (`env -i`) run.
Sky single run SHA: `e07382e5dba0429a97e61581550f88c03a2b58f11907ef8cb5464c908bd8d7a`.

## Sanity PSNRs (raw, reported without tuning — task §6)

| image | baseline | C3 (committed) | **P3** | Δ vs baseline | Δ vs C3 |
|---|---|---|---|---|---|
| bridge (512×184) | 18.47 | 19.74 | **19.63** | +1.16 | −0.11 |
| sky (768×512) | 22.75 | 23.89 | **23.84** | +1.09 | −0.05 |

(sse_gen: bridge 200345689, sky 316830330. Round-4 BAR 2 needs each ≥
baseline − 0.10: bridge 19.63 ≥ 18.37 ✓, sky 23.84 ≥ 22.65 ✓ — sanity
pair only; the full battery was NOT run per the task.)

## Residual-path region counts (raw)

| image | takes | op=3 (residual) | licensed but rejected | unlicensed |
|---|---|---|---|---|
| bridge | 48 | **0** | 3 (`p3_base_plane_resid_rejected`) | 45 plane + 1 mean-nofit |
| sky | 31 | **0** | 0 | 31 plane |

The residual path fired **zero times** on bridge+sky. On bridge the
structural license held in 3 regions and the honest-improvement check
rejected all 3 — the gate works, the atoms earned nothing on real pixels.
The −0.11/−0.05 dB deltas vs C3 are exactly the regions where C3 stamped
ATOM and P3 kept the measured base (C3's atom path was already ~decorative
at 3.7%).

## Positive control (synthetic — the op=3 path is real and correct)

Because op=3 never fired on real images, the new render/commit code was
unexercised. A synthetic 64×64 indir (each 32×32 block = 128 + si=0 atom
26's raw key deviations, no clamping) was built and run (scratch only,
deleted after): **4/4 blocks took op=PLANE+ATOM** (`base=MEAN`,
`resok=1`, `reason=p3_base_mean_resid_licensed`, `bsse=0`, `fok=1`,
`mok=1`). An independent Python oracle recomputed all 12,288 constructed
pixels from the vocab body + block means: **12,288/12,288 byte-exact,
all labeled 3** — the op=3 render path is verified. The commit path uses
the textually identical `baseval + keydev` formula as the honest check
(verified by inspection; the check itself fired correctly with
`resok=1` on the synthetic and `resok=0` with `resid_rejected` on bridge).

## Notes for the coordinator

- Do NOT run `~/workspace/upscale_r4/sealed/` with this or any arm —
  implementer never saw sealed pixels (per task §7).
- No binaries, `.zagd`, `.zag-cache`, or outdirs remain in `impl_p3/`;
  only `azgen_p3.zag`, `IMPL_P3.md`, and the three build-support symlinks.
- No post-result tuning was performed; all numbers above are raw.

P3 COMPLETE
