# Magnifying-glass chunker — PROMOTION VERDICT (Phase 1, 2026-09-26)

Plain-English verdict: **the magnifying-glass chunker is promoted into live intake.**
The frozen fork's deliberative arm (24/24 correct, 24/24 native, 0 fallbacks) was renamed
into the live entry point `tnn_intake(...)`. The three failed fixed arms (C/W/S) were
removed from production entirely — they survive only in `negcontrol.zag` as explicit
retired negative controls, proving the fork's finding that fixed chunking fails.

## Bars (live intake, 24-question battery)

| Bar | Live | Frozen fork D |
|---|---|---|
| Correct | **24 / 24** | 24 / 24 |
| Native (no fallback) | **24 / 24** | 24 / 24 |
| Fallbacks | **0** | 0 |
| Zoomed (multi-scale) answers | 12 | — |

RUN_R1.out SHA-256: `50c2180d9f46edd337ee8e87c3efe2ddaa2b756919c999b189d604c8d6c745e4`
(byte-identical rerun RUN_R2; delete/rebuild/rerun reproduced RUN_R1 exactly).

## The q22 trap (kept working)

"What is the 2nd letter of fox" over "the quick brown fox": live intake locates `fox`,
zooms to the word, then indexes its 2nd character → `o`. The retired fixed C/S arms answer
`h` (indexing the whole text); the fixed W arm reached `o` only through fallback. The live
trace shows `WORD>CHAR` with the two zooms.

## Files

- `intake.zag` — live public entry point `tnn_intake(...)`; fork machinery renamed `d_*` → `tnn_*`; fixed C/W/S absent; every choice and zoom traced.
- `negcontrol.zag` — retired fixed arms as negative controls only (`nc_c_answer`, `nc_w_answer`, `nc_s_answer`).
- `battery1.zag` / `gen_phase1.py` / `build.sh` — battery, generator, build.
- `evidence/RUN_R1.out`, `evidence/RUN_R2.out` — the two byte-identical runs.
