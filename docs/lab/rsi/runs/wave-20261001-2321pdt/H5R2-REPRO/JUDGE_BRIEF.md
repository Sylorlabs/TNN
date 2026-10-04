# JUDGE_BRIEF: H5R2-REPRO (independent reproduction of TNN3H5R H5R2)

## Provenance header

- RENDER_SHA: 19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287
  (reproduced binary built independently from committed source; 3/3
  byte-identical builds; matches the lane's frozen binary bit for bit)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: TNN3H5R H5R2 BUILD-PASS as the reproduced artifact
  (lane TNN3H5R, single worker as coordinator/builder/evaluator; sealed
  battery on the t2_prov_ok provenance gate); this lane performed no
  implementation, only extraction, rebuild, and re-execution.
- NEW_KNOWLEDGE_CLAIM: Independent re-execution from the committed
  sources reproduces the lane's sealed evaluation exactly (all bars,
  all world hashes, binary bit-identical), so the H5R2 BUILD-PASS
  verdict survives independent reproduction.

## Verdict

REPRO-PASS. Every number in the lane's SEALED_EVAL_H5R2.md reproduces
exactly from the committed sources; the rebuilt binary is bit-identical
to the frozen binary; all four sealed world outputs are byte-identical
to the lane's 3/3 runs; the commit order is clean.

## Numbers vs the lane's frozen bars (lane reported vs repro observed)

- KB-W0 (white-box primary): 36/36 vs 36/36 (zero live tag-1 facts on
  any MAP key in all 36 SNAP-IN lines; every probe answered by the
  single live tag-20 MAP's f28; zero FAIL lines)
- KB-W2R (the killed bar): 12/12 vs 12/12 (exactly 2 superseded MAPs +
  1 live MAP per probe; every DEP edge targets a live tag-1
  non-superseded fact; zero DEP edges to superseded facts)
- KB-B2R (behavioral): 24/24 vs 24/24 (16 B2R probe-answers on
  double-contradiction probes + 8 on revert probes; all returned values
  match expected)
- KB-W3 (provenance-chain family): 8/8 vs 8/8 (exactly 3 superseded
  MAPs + 1 live MAP with f28==c0; all DEP targets live)
- KB-B3 (behavioral chain): 24/24 vs 24/24 (12 per world; zero
  FRESH-FAIL/C1CON-FAIL/C2CON-FAIL/F28-FAIL)
- KB-D1 (determinism): 3/3 byte-identical full-stdout runs per world vs
  identical (all four world output hashes match the lane report exactly)
- KB-S1 (substrate gate): PASS vs PASS (re-verified on extracted
  committed file)
- KB-G1R (architecture): PASS vs PASS (re-verified diff; no modes,
  bridges, handlers, ISA additions, or forbidden operations)
- KB-P1 (process): PASS vs PASS (safebin PATH; `which python3` empty;
  zero forbidden-executable invocations)
- Negative controls NC-1R2/NC-3R2/NC-5R2/NC-6R2/NC-7R2: none fired;
  commit order verified strict: prereg dc7df4aba < implementation
  9db334bd4 < sealed e20ba5402.

## Commit ids

- Prereg freeze (alone):
  dc7df4aba1db84e71e3e0b61c84adbf77244e590 (2026-10-02 06:30:12 UTC)
- Implementation:
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172 (2026-10-02 06:31:39 UTC)
- Sealed worlds + evaluation:
  e20ba54020dde7e38050dda9e54727d826fc7b45 (2026-10-02 06:34:48 UTC)

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/REPRO_H5R2.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-REPRO/JUDGE_BRIEF.md
  (this file)

## What broke

Nothing. No divergences found. Scope is bounded: this reproduces the
lane's sealed battery; it establishes no new generality or L3 claim.
