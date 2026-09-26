# RUNLOG.md — TNN-CHOOSES-ITS-LAYERS (image_tnnlayers)

## 2026-09-26

- Read the no-layers fork (DESIGN.md, VERDICT.md, RUNLOG.md, PROVENANCE.md,
  `nolayers.zag`, `nlingest.zag`, `common_nl.zag`) and the zoom-fork evidence.
  Verified the sealed fixture SHA-256 before new work.
- Designed the fork: fixed mechanism menu {SMOOTH, LINES, SHAPES}; TNN chooses
  count/order/vocabularies/scale set via deterministic survey; commit bar
  G/N >= 9 per candidate on the current residual; revert + record otherwise.
- Implemented `tnnlayers.zag` (mechanisms, survey, renderers, TNNKTLM1
  writer), `tlingest.zag` (deliberation orchestrator), `tlemit.zag`
  (knowmap-only re-render). Pure Zag, zero RNG, deterministic tie-breaking.
- First build clean (pinned znc). First run hit two issues:
  1. `nio_open_child` uses O_NOFOLLOW — the symlinked fixture was rejected;
     copied the fixture as a real file (SHA-256 re-verified).
  2. A transient early hang that did not reproduce (binary starts/prints
     fine; subsequent runs progressed normally).
- SMOOTH committed on the first measured try: G=6260482978, N=287232,
  B=25298 (973 leaves), G/N=21798 >> 9. TNN's chosen order: SMOOTH(1) ->
  SHAPES(3) -> LINES(2).
- SHAPES: rep probe 195 per-mille -> scale set {32,16,8,4} (64 dropped);
  atoms 73/310/1214/4003; 660 regions; G=107772342, B=1828516, G/N=375.
  COMMIT.
- LINES: 56 walks, 48 kept, 8 dropped by per-seg bar; G=132317, N=555,
  B=672, G/N=238. COMMIT.
- Residual: 7806/95744 px (8.2%). Knowledge: 1,963,911 bytes (knowmap.bin).
- Metrics (pre-residual): 43.43 dB / 0.9937 SSIM — beats both baselines.
- White-box: path A == path B (understanding SHA-256 identical); renderA ==
  renderB == sealed fixture (exact closure).
- Pentagon: absent. TNN put LINES last (affinity 173), per-seg bar dropped
  the curved walks, 48 tiny survivors (~4px) didn't facet the arch.
  Bridge-arch crop (110,85)-(230,165) verified visually.
- Determinism: run/ vs run2/ byte-identical on knowmap, all renders, trace.
- Gallery: ~/workspace/your_files/image_tnnlayers_NEW/index.html
  (self-contained, 9 images, no external loads).

## Timing

- SHAPES dominates (farthest-point vocabularies + take/split deliberation),
  as in the no-layers fork. Full ingest is CPU-heavy; the lab VM was heavily
  loaded during the run (~9% CPU share), so wall time was long.

## Adaptive-split arm (no-layers)

- Investigated per the task ("if cheap"). Finding: NOT cheap. The no-layers
  exemplar vocabulary is scale-indexed (atoms are sxs for s in
  {64,32,16,8,4}); content-adaptive split positions would produce
  non-power-of-2 blocks that match no vocabulary scale. The fixed midpoint
  quadtree is forced by the vocabulary design. A true adaptive-split variant
  needs a scale-polymorphic vocabulary — a redesign, not a tweak. Reported
  to parent; no separate arm built (would have been a different experiment,
  not a cheap one).
