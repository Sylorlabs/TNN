# JUDGE_BRIEF.md: H-PI-REV2 narrowed single-conflict claim

## Provenance

- RENDER_SHA: aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc
  (sha256 of the primary evidence artifact, the sealed executor
  binary s8_exec_bin; transcripts are 3/3 byte-identical per
  world and traceable to this binary)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE:
  - H-PI-REV2 step-5 PASS (wave-20260929-2321pdt): frozen revision
    procedure revises correctly and cheaply on unsealed conflicts.
  - H-PI-REV2 step-6 S6C PASS 13/13 (wave-20260929-2321pdt):
    sealed confirmation of step-5 on 13 held-out conflict cases.
  - H-PI-REV2 step-7 FAIL-bounded (wave-20261001-2021pdt): sealed
    OOD across 4 families; family B (two-conflict) tripped
    K-OOD-W1/W3. Bounding analysis: the revision procedure bounds
    to single-conflict worlds; families A/C/D PASS; the hypothesis
    was not killed, not void.
- NEW_KNOWLEDGE_CLAIM: The frozen revision procedure revises
  correctly and cheaply on all five fresh sealed single-conflict
  worlds (spanning novel bytes, novel conflict positions, longer
  inputs, a novel template shape, and single-conflict variants of
  the step-7 family-B regime) and, on the established two-conflict
  world, flags the uncovered conflict explicitly rather than
  converging silently to a wrong solution.

## Verdict

BUILD-PASS on the narrowed claim only. All frozen kill bars held:
K-SC-W1 fails_total=0 on 5/5 worlds (25/25 EW pairs correct);
K-SC-W2 revision_evals 6/6/6/11/6, all at or under the 25 ceiling;
K-SC-W3 reuse_correct=1 with zero new revision marker lines after
the reuse probe on all 15 runs; K-SC-W4 3/3 byte-identical per
world, exit 0, zero stderr; K-SC-W5 pure Zag throughout;
K-SC-B bound-trip signal S1 (w_fails_total=1), S2
(COUNTEREXAMPLE_DETECTED at the held-out W3 probe), S3 (zero
post-W3 re-revision lines) on 3/3 regression runs against the
step-7 transcript; K-ARCH1 zero cognition source delta
(dd3cb02d... unchanged); K-ARCH2 zero architecture growth
(0/0/0/0/0 semantic cases/modes/bridges/routers/handlers).

## Key evidence

- Prereg (frozen alone before implementation): commit 00b31af53.
- 25 sealed world files with hashes frozen in the prereg: all
  25/25 verified against the frozen hashes at load time.
- Executor binary s8_exec_bin: aee1b6f21a4b5309a3c93e9f66d9c38553bd75db926feeba123207373117ddbc
  (3/3 byte-identical builds; machinery prefix 1-606 byte-verbatim
  from proc_revise2.zag, verified hash 8d2b16ab...).
- 15 run transcripts (5 worlds x 3), per-world sha256:
  A2 a4c05e04d66db34e65796b74b244c55a9471813e760de43a6004b9cd7457aecf,
  B1 f1092c1b5c49757bdfac9083e84765a09eec56526e096ef12ef3ec59cac9a524,
  B2 0e5208fd42cf3025a9c6b0f2f273de0a091ef1f3634dd5c7c8145f43e059f3a7,
  C2 9d4e66a0a6a4c793584b9c01adc56bdb228c622b4e24239166e211deaefdc285,
  D2 8a3ac2a99ce36eeef6566f9a62434e206f05c66f57a791e6e071308779ee8621.
- 3 bound-trip regression transcripts byte-identical to the
  step-7 record (f56080d65aeb2ceba9a8134784872381bd17293d8df48010835b482d17d9268d).
- Full execution record: SEALED_S8_EXEC.md in this directory.

## Boundaries of the claim

This verdict does not establish representational invention,
template invention, or L3 (the bounded-L2 ceiling stands); does
not establish broad generality beyond the tested regimes; and is
not SURVIVES (transfer/reuse beyond the single probe, a second
independent red team, and governance audit remain outstanding).
The step-5 PASS, step-6 PASS 13/13, and step-7 FAIL-with-bounding
records are untouched. No frozen bar was weakened to force the
pass; three pre-freeze world-design slips were found by the
mechanical validator, fixed before the freeze, and disclosed in
the prereg (non-independent design is disclosed, not hidden).

No em-dashes or en-dashes appear in this file.
