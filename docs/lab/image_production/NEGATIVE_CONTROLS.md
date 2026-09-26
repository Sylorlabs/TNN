# Negative Controls — Retired Image Pipelines

These pipelines lost to adaptive-layers + adaptive-magnification
(`docs/lab/image_adaptivelayers/`, now `docs/lab/image_production/`).
They stay in the repo as evidence and white-box study material but are
**never callable from the live path** — nothing in `docs/lab/image_production/`
imports, calls, or reads from these directories.

Winner numbers (all on the same sealed fixture, `metrics.py`, pre-residual
understanding): **46.35 dB / 0.9955 SSIM / 2.7% residual / 636,451 bytes.**

| Pipeline | Location | Commit | PSNR / SSIM | Residual | Knowledge bytes | Why it lost |
|---|---|---|---|---|---|---|
| Hand-designed layered zoom (magnifying glass) | `docs/lab/image_zoom_fork/` | `2384090e54cf` | 30.80 / 0.9620 | 19.9% (19,051 px) | 1,343,354 | Fixed-grid zoom wastes atoms; variable scale by deliberation beat v2b but is far behind adaptive CART structure |
| Rigid no-layers (exemplar take/split, dyadic grid) | `docs/lab/image_nolayers/` | `3a49b9c7031c` | 29.27 / 0.9260 | 11.7% (11,262 px) | 2,505,092 | Dyadic boundaries misalign with content; ~2x the bytes for ~17 dB less; this fork surfaced the circles-into-pentagons artifact |
| Adaptive no-layers, single-pass | `docs/lab/image_nolayers_adaptive/` | `784a4af282e8` | 30.50 / 0.9183 | 93.1% | 3,682,332 | Closing the grid gap cost 3.7MB and a 93% residual share; error became many small errors — quality-per-byte collapses |
| Fixed-quadtree, TNN-chosen layers | `docs/lab/image_tnnlayers/` | `7421ca9f4b6e` | 43.43 / 0.9937 | 8.2% | 1,963,911 | Strongest parent, but fixed midpoints leave 2.92 dB and 3x bytes on the table; production's adaptive CART + zoom is a strict improvement (free lunch: better quality AND fewer bytes) |

Paths above were verified from the repo tree at each commit (gh-api non-recursive
tree walks, 2026-09-26). Negative-control policy: these trees are frozen evidence.
Any future revival starts from a copy with a preregistered bar, never by
re-pointing the production path at them.
