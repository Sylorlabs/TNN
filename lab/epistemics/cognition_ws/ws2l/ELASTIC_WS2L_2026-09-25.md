# ELASTIC REMEDIATION WS2-L — 2026-09-25 (no-stupid-limits law)

All fixed capacities in the ARM L learning mechanism (`learn.zag`) and the
learned-synonym loader (`toc_l.zag` `syn_build`) were replaced with
grow-on-demand elastic arenas. Pure Zag, deterministic, zero RNG. Behavior
and output bytes are unchanged on every store the old caps could hold.

## Cap inventory (learn.zag) — all removed

| # | Old bound | Replacement |
|---|-----------|-------------|
| 1 | dump output 65,536 B | `emit`/`emit_pool` grow the buffer |
| 2 | relation tables 4,096 B (1,024 relations) | `rel_add` grows r1o/r1l/r2o/r2l/rrules |
| 3 | lid tables 32,768 B (8,192 entries); lhead/ltail/ln 8,192 B (2,048 relations, hardcoded init loops) | `lid_add` grows lo/ll/lnext and lhead/ltail/ln with -1/0 fill |
| 4 | veto tables 6×1,024 B (256 vetoes) | `veto_add` grows all six arenas |
| 5 | string pool 131,072 B | `pool_copy`/`pool_word` grow via `grow_to` |
| 6 | token workspace 256 B (64 words/line) | `tokenize_words` grows wo/wl per word |
| 7 | PARA tables 1,024 B (256 entries); words `pi*16+q` (16 words/PARA line) | flat word arena (pwo/pwl) + per-entry start offsets (pws); all grow |
| 8 | group tables 1,024 B (256 groups, hardcoded zero32) | g0/gn grow; new gn slots zero-filled |
| 9 | R3 candidate tables 8×2,048 B (512 candidates) | all eight grow per candidate |
| 10 | union-find 4,096 B (1,024 stems); `guard<10000` in uf_find | tables grow; structurally-terminating find (parent links form a forest: each node's parent is written at most once, only roots are attached under roots) |
| 11 | sort/output: ord 4,096 B, out 65,536 B, vord 1,024 B, vout 8,192 B | ord/vord grown to nr/nv; out/vout grow via emit |

Intentional fixed schemas kept (not capacity caps): 20-byte matcher result
handles, 8-byte offset/length handles, `rules_str` buffer (max "R1+R2+R3"),
exact R1/R2/R3/R4 surface-pattern lengths, R3's "exactly two lines per
subject + ≥2 witnessing subjects" (frozen mechanism rules).

## Cap inventory (toc_l.zag syn_build) — all removed

| # | Old bound | Replacement |
|---|-----------|-------------|
| 1 | veto arrays 64×8 (64 vetoes) | va/vb grow per veto |
| 2 | pair arrays 256×8 (256 pairs) | pa/pb grow per pair |
| 3 | stem/parent tables 512×4 (512 stems) | so/sln/par grow per stem |
| 4 | spool 16,384 B, raw 8,192 B, ro 512×4 | tg_spool/tg_grow, all elastic |
| 5 | `guard<10000` find walks (3 sites) | `tg_find` with path compression, structurally terminating |

Audited but unchanged (eval-harness structures sized to frozen corpora, do
not bind learned-synonym loading/retrieval): build_toc key-line table
(4,096 lines), toc_load cell tables (512 cells), cmd_grade class counters
(32 classes).

Load-bearing ceiling (toolchain, not a TNN cap): znc cannot index a slice
≥ 2^25 bytes; growth clamps there per the standing workaround policy.

## Verification

- learn.zag on frozen corpus: `synlearn.txt`/`synveto.txt` byte-identical to
  frozen store (112 relations, 4 vetoes); learn.log identical modulo the
  known 277-vs-276 line-count note.
- Stress (synthetic 10,507-line corpus): 9,001 relations, 10,200 lids,
  300 vetoes, 1,202 PARA entries, 602 groups, 600 R3 candidates, ~18,600
  union-find stems, ~240 KB pool, 262,815 B output — every former bound
  exceeded, run completes, output sorted, byte-identical rerun.
- GEN: second ingest into the stress store → 10,501 relations / 301 vetoes;
  all old relations and lids intact, new evidence learned.
- toc_l.zag on official battery: out/rep/grade byte-identical to frozen
  det refs; 51/51 (PURE 33/33, SUBJ 18/18).
- FRESH 6/6, DIST 6/6, ADV-NEAR 6/6, MULTI-HOP 4/4, MORPH 3/4 (QMO3 tie at
  phase-2 score 2002 — predicted/documented, unchanged).
- Elastic syn_build over the 9,001-relation stress store: 51 lookups
  complete; phase-2 synonym bridge resolves through stress-store relations
  (QS1→S1 via w00002a|w00002b + w00003a|w00003b); vetoed pairs correctly
  excluded (QV1 empty).
