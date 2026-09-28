# RED TEAM REPORT — Upscale Round 4, candidate P2plane

Date: 2026-09-27. Independent red team (not involved in implementation).
Prereg gate: `PREREG_R4.md` ("Red-team gate"); candidate passed BAR 1
(sealed mean +0.539 dB, 10/10 wins, floor +0.00) per `BATTERY_R4.md` §7.
Task: KILL P2plane if it deserves killing.

**Candidate under test:** repaired `impl_p2/azgen_p2.zag` (SHA
`de4bf017…`, capacity repair only) run with `argv[3]=="plane"` —
P2's lineage-restricted take geometry rendered as PLANE-FIT (LS plane
fit at match time, evaluated at 2x) + frozen `vocab_v3.bin` (SHA
`e43cfebf…`). Built with the pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Build validated: bridge P2plane output SHA `94e6090c5150f463…`
byte-identical to the battery's committed run; PSNR 19.20 matches.
Baseline for comparison: repaired pristine `azgen.zag` (SHA `aea60c27…`),
same toolchain. Bicubic reference: PIL 10.2.0 `Image.BICUBIC` on the
exact harness box-downscaled LR (same protocol as `battery_build/bicubic_ref.py`).

Work dir: `~/workspace/upscale_r4/redteam_r4/` (scripts retained;
disposable binaries deleted after scoring per protocol).

## Per-attack verdicts

| # | attack | verdict | headline numbers |
|---|---|---|---|
| 1 | Category-shift traps (R3 killers) | **KILL** | P2plane vs bicubic: diagonal step **−11.57 dB**, circle **−8.34 dB**, gradient+step **−11.96 dB** — worse than the R3 C3 kill numbers (−5.46/−6.54/−7.04). False ramps confirmed numerically. |
| 2 | Close-call ±1/±2 LSB amplification | **KILL (supporting)** | 3/12 perturbations amplify 44–88x (sealed_03 −1 LSB: 88x; −2 LSB: 44x; sealed_04 +2 LSB: 68x, 157 px ≥10 gray levels changed). Silent thin-atom winner flips with no take-count change and no recorded margin. |
| 3a | Operator neutering (PLANE→MEAN-FILL) | **PASS** | Neutering costs **−0.936 dB** sealed mean (per-image −2.32…+0.00) with byte-identical take geometry — PLANE is load-bearing, not decorative. |
| 3b | Fixed-grid planes diagnostic | **PASS** | Uniform 32×32 grid planes, no vocab: **−0.333 dB** mean vs baseline (P2plane +0.539). Dumb grid does not reproduce P2plane — vocab-derived take geometry contributes. |
| 4 | Hardcode audit | **PASS** | No hidden hardcodes, per-image patches, or battery-tuned constants. Two inherited robustness notes (below). |
| 5 | Sealed-image leakage audit | **PASS** | Zero sealed SHAs in any source/binary/vocab/trace; vocab predates sealed images; no sealed-derived decisions in source. |

## Attack 1 — category-shift traps (KILL)

R3's trap generators are not in the workspace; traps were reconstructed
analytically and documented (script `attack1_traps.py`): 256×256 GTs,
LR = harness box-downscale, scored with frozen `metrics.py`.

- `diagonal_step`: binary 255 iff y > x (45° sharp diagonal edge).
- `circle`: binary, 255 inside r=64 of (128,128).
- `gradient_step`: horizontal gradient 0..199 with a sharp +55 LSB step
  at x=128 (discontinuity mid-gradient).

PSNR dB vs GT:

| trap | baseline | P2plane | PIL bicubic | P2plane − bicubic | P2plane − baseline |
|---|---|---|---|---|---|
| diagonal_step | 16.07 | 18.62 | 30.19 | **−11.57** | +2.55 |
| circle | 18.53 | 20.88 | 29.22 | **−8.34** | +2.35 |
| gradient_step | 34.88 | 34.88 | 46.84 | **−11.96** | +0.00 |

P2plane beats baseline on the traps but collapses against bicubic at
**−8 to −12 dB** — substantially worse than the R3 deficits that killed
C3 (−5.46/−6.54/−7.04 on the same trap family).

Mechanism confirmed numerically on `diagonal_step`: in the ±4 px band
around the edge, P2plane's mean absolute error is **87.2** gray levels
vs bicubic's 24.4; the band renders intermediate grays (64, 109–141 —
12 distinct values between the binary 0/255), i.e. the plane fit renders
a **false ramp across the sharp edge**. Far from the edge P2plane still
errs (mean 7.3) where bicubic is exact (0.0). The take geometry is
decided by atom-match gain, which does not penalize edge-straddling —
a plane fit to an edge-straddling block is rendered as a ramp.
This is the same structural defect the R3 red team named
("variance-explained is not model-correctness"), now measured worse.

## Attack 2 — close-call amplification (KILL, supporting)

3 sealed images (sealed_03: P2plane's largest win +1.73; sealed_04:
edge-dense repaired-panic image; sealed_07: P2plane ties baseline),
LR input perturbed deterministically by +1/−1/+2/−2 LSB (clip 0/255),
P2plane rerun, GEN_TRACE take counts + output-BMP diffs measured
(script `attack2_closecall.py`; the trace records summary counts only —
no per-take records exist, so decision flips are proxied by take-count
changes and output-pixel diffs, stated explicitly).

| image | perturb | take-count Δ | max\|Δout\| | amplification |
|---|---|---|---|---|
| sealed_03 | +1 | 0 | 2 | 2x |
| sealed_03 | **−1** | 0 (LINES G +529) | **88** | **88x** |
| sealed_03 | +2 | 0 | 4 | 2x |
| sealed_03 | **−2** | 0 | **88** | **44x** |
| sealed_04 | +1 | 0 | 3 | 3x |
| sealed_04 | −1 | 0 | 1 | 1x |
| sealed_04 | **+2** | shapes +2, lines −10 | **136** | **68x** |
| sealed_04 | −2 | 0 | 3 | 2x |
| sealed_07 | ±1, ±2 | 0 | 1–2 | 1x |

9/12 perturbations propagate linearly (1–3x). 3/12 flip close-call
decisions with 44–88x amplification — the same defect class as R3's
50–95x on C3, sparser but present. Two distinct flip loci identified:

- **sealed_03 −1/−2**: take counts identical, cascade order identical,
  yet a −1 LSB input change flips a 2×2 block's winning **thin atom**
  (LINES G moves +529 with takes 1136→1136); the stamped atom deviations
  differ by up to 88 gray levels at 2 isolated pixels. The trace records
  no margin — nothing warns the decision was a coin flip.
- **sealed_04 +2**: SHAPES takes 550→552, LINES 16840→16830; 157 output
  pixels change ≥10 gray levels (132 ≥20, 80 ≥40, 27 ≥80, max 136),
  clustered in one region (rows 511–517, cols 470–481) — a localized
  take-geometry flip from a 2-LSB input change.

## Attack 3a — operator neutering, PLANE→MEAN-FILL (PASS)

Red-team-only copy `build/src_p2_NEUTMEAN_redteam_only.zag`: the
`planemode==1` render branch writes the block mean instead of the plane
(`acc = mr/mg/mb`, same geometry, same labels). Built with the pinned
toolchain; binary deleted after scoring.

Sealed battery, PSNR dB (p2plane vs neutered), geometry-identity check
(GEN_TRACE take counts equal ⇒ edit touched only the render branch):

| image | p2plane | neutmean | Δ | geom same |
|---|---|---|---|---|
| sealed_01 | 24.56 | 24.56 | +0.00 | yes |
| sealed_02 | 22.24 | 21.63 | −0.61 | yes |
| sealed_03 | 22.52 | 20.20 | −2.32 | yes |
| sealed_04 | 17.88 | 17.35 | −0.53 | yes |
| sealed_05 | 21.64 | 20.31 | −1.33 | yes |
| sealed_06 | 20.89 | 18.57 | −2.32 | yes |
| sealed_07 | 23.42 | 23.42 | +0.00 | yes |
| sealed_08 | 21.47 | 20.77 | −0.70 | yes |
| sealed_09 | 19.94 | 19.50 | −0.44 | yes |
| sealed_10 | 20.40 | 19.29 | −1.11 | yes |

Mean Δ (neutmean − p2plane) = **−0.936 dB**, geometry provably identical
on all 10. Unlike R3's ATOM neutering (≤0.03 dB), neutering PLANE moves
the score almost a full dB: the measured-construction claim is not
hollow — PLANE is load-bearing. (P2plane PSNRs above reproduce the
battery's sealed table exactly, an independent cross-check.)

## Attack 3b — fixed-grid planes diagnostic (PASS)

Pure-Python diagnostic (script `attack3b_gridplanes.py`): uniform
non-overlapping 32×32 LR blocks, per-channel LS plane fit on each
block (same centered-coords math as the Zag plane code), plane evaluated
at 2x; even output positions keep the observed pixel (the pipeline's
KNOWN convention); odd positions get the plane. No vocab file read, no
atom matching, no lineage.

Sealed mean Δ vs baseline: **−0.333 dB** (per-image +1.15…−2.07),
against P2plane's **+0.539**. The dumb fixed grid does not reproduce
P2plane — the vocabulary-derived take geometry (which regions get
planes, at which scales, under the gain bar) contributes roughly
+0.87 dB over planes-everywhere. The vocabulary earns its keep as a
geometry decider; this probe does not kill.

## Attack 4 — hardcode audit (PASS)

Full read of `azgen_p2.zag` (1512 lines; match/load/render paths) plus
a whitespace-insensitive diff against pristine baseline `azgen.zag`
(418 diff lines, all in documented areas): header comment, VOC3 loader
(magic check, 240-byte lineage table, VOC2 rejection rc 9), lineage
restriction in `gshapes_fit`, take stride 9→15, LS-plane helpers
(verbatim C3 post-fix code), plane render branch, repair comment.
No per-image or per-item patches, no disguised lookup tables, no
battery-tuned thresholds. Every numeric constant and its status:

| constant | status |
|---|---|
| gain bar `9*nval` | inherited baseline, preregistered ("same bar as the parent pipeline") |
| `tl_walks(..., 27, 1, 0, ...)` survey | inherited baseline |
| `pxmax = 768*576*3` input cap | inherited baseline; clean failure (`return 1`), not silent |
| SHAPES takes buffer 16384 rows (stride 15), `nofits` 1024 rows | inherited capacity constants; **no bound check** — latent same-class panic risk as the repaired LINES bug (not triggered: battery max 550 takes). Robustness note, not a cheat. |
| VOC3 magic (86,79,67,51), 240-byte table, scale-major offsets | the arm's documented mechanism |
| repair comment citing "sealed_04: 16847 takes" | coordinator-added post-battery; names a sealed image with a take count (not pixels/SHA). Minor seal-hygiene blemish, not a leak. |
| header comment "bridge 18.47 dB vs 25.89 dB" | inherited baseline honest-result note |

`vocab_v3.bin`: magic `VOC3`; bytes 4..1958448 byte-identical to frozen
VOC2 (`cbead2f7…`); 240-byte table at the documented offset; table
counts match the dry-run doc exactly (src0:101, src1:132, src2:2,
sentinel 255: 5 NULL atoms). No sealed content.

## Attack 5 — sealed-image leakage audit (PASS)

- All 10 sealed SHAs from `sealed/SEALED_SHASUMS.txt` (full 64-hex and
  16-hex prefixes) swept across every file in `impl_p1..p4`, `r3src`,
  both vocabs, and the built binaries/sources: **zero hits**.
- "sealed" string references in impl dirs: only (a) the coordinator's
  repair comment, (b) implementer discipline statements
  ("Sealed dir never opened", "implementer never saw sealed pixels").
- mtime analysis (UTC 2026-09-27): `voc3_tool.py` 19:01:45 and
  `vocab_v3.bin` 19:01:47 **predate the first sealed image** (19:02:05);
  `azgen_p2.zag` implementer-final 19:05:13 (~2.5 min after the last
  sealed image, 19:02:42 — consistent with parallel work; content audit
  shows no sealed-derived decisions); repair edit 19:51:25 (coordinator,
  post-battery). The VOC3 lineage table derives from TEACH_TRACE of the
  4 teach images (brick_wall, lake_water, foliage, stone_wall),
  verified by the preregistered dry-run gate — not from sealed pixels.

## Final verdict: KILL

P2plane is an honest mechanism — no hardcodes (attack 4), no leakage
(attack 5), PLANE genuinely load-bearing at −0.94 dB (attack 3a), and
the vocabulary genuinely contributes as a geometry decider (attack 3b).
None of the "hollow claim" probes fired. It is killed on structural
grounds, not on integrity grounds:

1. **Category-shift traps (the designated killers):** −11.57 / −8.34 /
   −11.96 dB vs bicubic on diagonal step / circle / gradient+step —
   worse than the R3 deficits that killed C3. The plane-fit construction
   renders false ramps across sharp edges (measured: intermediate grays
   64–141 in the edge band, 87.2 vs 24.4 mean error).
2. **Close-call amplification:** ±1–2 LSB input changes flip silent
   thin-atom/take decisions with up to 88x output amplification and no
   recorded margin — the same defect class that supported C3's kill.

Mechanism named: **unconstrained least-squares plane rendering on
atom-matched take geometry** — the take geometry is decided by
atom-match gain, which does not penalize edge-straddling blocks, and the
plane fit then renders a false ramp wherever a sharp edge crosses a
take. P2plane passed BAR 1 on real photos, but it collapses on the
preregistered edge traps and its boundary decisions amplify silently.
Per the prereg ("any arm that wins BAR 1 but fails the red team is
KILLED, not shipped"), P2plane is KILLED.

REDTEAM COMPLETE: KILL — P2plane collapses −8 to −12 dB vs bicubic on the preregistered sharp-edge traps (false ramps across edges, worse than the R3 kill numbers) and amplifies ±1–2 LSB perturbations up to 88x through silent decision flips, so it fails the red-team gate despite its honest BAR-1 win.
