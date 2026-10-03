# JUDGE_BRIEF: TNN3H5R2 (H5R2 trial-loop provenance gate)

## Provenance header

- RENDER_SHA: 19dcf2e4436079a4ab6f9cf48b2b6a556f743d0ed1d9d16102249cd5ac970287
  (frozen binary tnn3_h5r2.bin; 3/3 byte-identical builds)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: H5 KILLED (wave-20261001-2021pdt, lane TNN3H5,
  red-team dissent dbf25e447, shadow fact on the MAP key); H5R KILLED
  (wave-20261001-2021pdt, lane TNN3H5R, KB-W2R 8/12: revert MAPs anchored
  DEP edges to superseded facts, breaking the revision chain); both
  prior waves.
- NEW_KNOWLEDGE_CLAIM: Gating trial-loop promotion on live,
  non-superseded licensing facts makes revert MAPs anchor provenance to
  the current post-revision fact, repairing the DEP-based revision
  chain that killed H5R (KB-W2R 12/12, new KB-W3 8/8 on double-revision
  reverts).

## Verdict

H5R2 ADVANCES (BUILD-PASS). All frozen bars pass; no killing negative
control fires; no void condition fires.

## Numbers vs frozen kill bars

- KB-W0 (white-box primary): 36/36 PASS (zero live tag-1 facts on any
  MAP key; every probe answered by the single live tag-20 MAP's f28)
- KB-S1 (substrate gate, pre-run): PASS (t2_prov_ok defined; gate at
  all four t2_trial promote sites; H5R hunks intact; zero shadow-fact
  teaching calls)
- KB-W2R (the killed bar): 12/12 PASS (was 8/12 on H5R); every revert
  MAP's DEP edges target live tag-1 non-superseded facts
- KB-B2R (behavioral): 24/24 PASS
- KB-W3 (new provenance-chain family, two revisions then revert): 8/8
  PASS (exactly 3 superseded MAPs + 1 live MAP with f28==c0; all DEP
  targets live)
- KB-B3 (behavioral chain): 24/24 PASS
- KB-G1R (architecture): PASS (13 added cognition lines, budget <= 15,
  net +9; zero modes/bridges/routers/handlers; zero ISA additions;
  cumulative diff net -4 lines vs the TNN-2 base)
- KB-D1 (determinism): PASS (3/3 byte-identical full-stdout runs per
  world, 4 worlds)
- KB-P1 (process): PASS (zero forbidden-executable invocations; safebin
  PATH; Step 0 recorded)

## Commit ids

- Prereg freeze (alone): dc7df4aba1db84e71e3e0b61c84adbf77244e590
  (2026-10-02 06:30:12 UTC)
- Implementation: 9db334bd4a01d21cce52da3bb2a1c45a10c4c172
  (2026-10-02 06:31:39 UTC)

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/PREREG_H5R2.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/IMPLEMENTATION_H5R2.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.zag
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/tnn3_h5r2.bin
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/DRIVER_TMPL.zag
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/SEALED_H5R2.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/sealed/
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/SEALED_EVAL_H5R2.md
- docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3H5R/NAMECHECK.md

## What broke

Nothing. The single-worker seal-integrity disclosure and mitigations
are frozen in PREREG_H5R2.md section 5.6. Scope is bounded: the frozen
battery tests exactly the preregistered revision-provenance behavior;
no broad generality claim and no L3 claim are established.
