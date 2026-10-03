# RUNLOG — Upscale Repair Round 2

## 2026-09-27

### Calibration (pre-prereg)
- Replicated baseline SHAPES matching in Python: takes=35, G=18343607 (exact).
- Oracle atom selection on old vocab: +0.025 dB ceiling (222.4M → 221.2M SSE).
- Energy-consistent score predicted: +0.015 dB on old vocab (7/35 winners change).
- Worst take (x=192,y=32, atom 42): atom 42 is TRUE best among 63 atoms.
  Failure is vocabulary coverage, not selection.

### Corpus
- Subagent acquired 12 CC Wikimedia Commons photos (768px, q90).
- SEALCHECK: 0 SHA hits, 0 source-title hits vs 9 sealed test photos.

### Implementation
- azteach2.zag: 12-image corpus, caps 96/96/64/48/64. Compiles clean.
- azgen2.zag: energy-consistent score (g_isqrt, g_precompute_su, rewritten
  gshapes_fit). Full-vocabulary search retained (no top-K). Compiles clean.
- Bug fix: takes/ltakes arrays 16384→65536, nofits 1024→4096 (pre-existing
  panic exposed by new vocab; capacity only, no logic change).

### Teaching
- Run 1: complete, na=96/96/64/48/64, vocab.bin 3.7M.
- Run 2: complete, same na, SHA 51c67ed3...
- Run 3: complete, same na, SHA 51c67ed3... (byte-identical).

### Evaluation
- BAR 1: azgen2 + old vocab on bridge: sse_gen=264825975 vs baseline
  268467517 (+0.059 dB). PASS. Two runs byte-identical.
- Bridge (new vocab): sse_gen=299274866 (−0.47 dB). Two runs byte-identical.
- Sky (new vocab): sse_gen=420174056 vs baseline 409163171 (−0.11 dB).
  Two runs byte-identical.
- Diverse 9 (new vocab): 6/9 wins, mean +0.297 dB. See RESULTS_diverse.tsv.

### Verdict
BAR 1 PASS, BAR 2 FAIL, BAR 3 FAIL. Mechanism (a)+(b) KILLED.
