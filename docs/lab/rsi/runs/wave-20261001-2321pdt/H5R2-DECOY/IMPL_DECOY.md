# H5R2-DECOY Implementation Record

Lane H5R2-DECOY, wave-20261001-2321pdt. Implements the frozen prereg
PREREG_DECOY.md (freeze commit 51a4fe8e1, 2026-10-02 07:00:11 UTC).
Pure Zag, safebin toolchain, no forbidden executables.

## Ordering and source extraction (read-only, git show)

- Prereg freeze commit: 51a4fe8e1 (2026-10-02 07:00:11 UTC), containing
  only NAMECHECK.md and PREREG_DECOY.md. DECOY_FRAG.zag and this file
  were created after.
- H5R2 substrate extracted from
  9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
  (matches the frozen substrate hash).
- Baselines extracted from 1203b865d352ae8ba380f57350218edd4d637b3a:
  bl_latest.zag d929d50c3b3499b4c1b17bcd9e1319eecf4044f9fb96125e01de35ad1d520220,
  bl_nogate.zag d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
  bl_random.zag c03b4575993ecbdb3a851c75972f4281e210340f90d0c7c6622b8160cf1a0ee1.
  bl_nogate.zag matches the recorded H5R base blob hash (the killed
  mechanism, bit for bit).
- Frozen DRIVER_TMPL.zag extracted from 9db334bd4, SHA-256
  f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af
  (matches the frozen driver hash).
- No working-tree file was used as a build input. Nothing was rebuilt
  from working files.

## DECOY_FRAG.zag (new, this lane)

SHA-256 6acc0965bc456e17229c24c6e7859b0a0dc5533c74e3b81f5708848014f99a6f.
Contents: h5r2_fact_live_id (single live tag-1 fact id on a key),
h5r2_dcy (the frozen D-check: sup==2, one live MAP with f28==c0, every
DEP target live tag-1 non-superseded, no DEP target is the decoy fact,
at least one DEP target is the live fact on K=(b,RF2)), h5r2_d_probe
(the frozen 9-step decoy probe: P1, contradict, P2, revert, decoy
OBSERVE, D-ANS answerability check, P3 revert-MAP query, D-check),
sealed_main_d1 (87xxx, vo5=5) and sealed_main_d2 (88xxx, vo6=1).
No name collisions with DRIVER_TMPL.zag. No OBSERVE on any MAP key.

## Mechanism smoke test (unsealed 9xxx keys, not part of the battery)

Before sealed assembly, the decoy probe pattern was smoke-tested on
disjoint unsealed keys (90101/90301, relations 9001-9004) to validate
the prereg section 1 mechanism claim. Assemblies compiled clean with
the pinned znc (only pre-existing A0102 warnings). Results:

- H5R2: revert MAP DEP edges to (90101,9001,90301) sup=0 and
  (90301,9002,90401) sup=0: anchors to the live reverted fact.
- REVERT-TO-LATEST: DEP edges to (90101,9001,90301) sup=0 and
  (90301,9004,90401) sup=0: anchors to the DECOY fact (r=9004), the
  pre-registered failure signature.
- NO-GATE: DEP edge to (90301,9002,90401) sup=1: anchors to the
  superseded stale fact, its baseline-lane failure mode.
- RANDOM-ANCHOR: this run anchored to the stale fact (chance level).
- All value answers correct on all arms; the decoy fact answered
  correctly (DANS v=90401). The discrimination is provenance-only.

The smoke test used no sealed keys and no sealed output was used to
tune anything; the sealed worlds below use the frozen 87xxx-88xxx spec.

## Build (pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1)

Smoke assemblies for all four arms compiled with zero errors. Sealed
world assembly and compilation happen after the implementation commit,
per prereg 7.1/7.2.

## Deviations from the prereg

None.

## Process

PATH was $HOME/safebin for every command. `which python3` printed
nothing (exit 1) at lane startup and at every check. Shell invoked
only: the pinned znc, built binaries, git read-only ops (show/diff),
and file copies. Zero forbidden-executable invocations. No push. No
files written outside the lane directory and /tmp scratch.
