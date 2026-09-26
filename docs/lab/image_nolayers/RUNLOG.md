# RUNLOG.md — image_nolayers

## 2026-09-26

- ~09:27 PDT: order received (Micah): no-layers fork of image capture.
- Built `~/workspace/image_nolayers/`: R33_NATIVE_IO_V1.zag (copied),
  metrics.py (copied), common_nl.zag, nolayers.zag, nlingest.zag,
  nlemit.zag, build.sh, DESIGN.md.
- Audit before compile found 7 issues (arbitrary caps, incomplete trace,
  wrong decision counters, honesty/gaming risk, complexity risk,
  wording, atom capacity); all repaired before building.
- First build: clean, ~3 s. First run: vocabulary
  (17/81/346/1248/3911 atoms at 64/32/16/8/4), 100 regions,
  29.27 dB / 0.9260, residual 11.7%.
- Found stats bug (rolled-back provisional decisions overcounted
  ntake/nsplit); fixed with snapshot/restore; rebuilt.
- ~09:38 PDT: artifact follow-up (Micah): circles-into-pentagons in zoom
  fork. White-boxed to greedy same-direction chord tracing in
  `deliberate_edges`; verified via knowmap segment parse (46 segments
  >=4 px trace the arch) and structure+edges render. No-layers
  eliminates the artifact (smooth arches at 10x).
- Official runs: run/ and run2/, byte-identical on knowmap, all
  renders, DELIBTRACE.txt. Path A == Path B both runs. Exact closure
  both runs (renderA == sealed fixture).
- Gallery: `~/workspace/your_files/image_nolayers_NEW/index.html`
  (self-contained, 7 data-URI images, zero external loads).
- Evidence commit -> `tnn-native-lab` (see PROVENANCE.md).

## Timing

- nlingest: ~100 s/run (vocabulary farthest-point ~15 s, assignment ~80 s).
- nlemit: <1 s. metrics.py: ~1 s.
