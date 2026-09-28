# HYPOTHESIS BATTERY — SCOREBOARD (as amended 2026-09-26 ~11:30 PDT)

Question: why does video fusion produce a sticker instead of a head swap?
Prereg: `PREREG.md` (frozen pre-test) + `PREREG_AMENDMENT_2026-09-26.md` (adds H6, sharpens H1).
Evidence: `VERDICT.md` (H1–H5, committed `1f33f74b`). Method: pure Zag, zero RNG, byte-identical reruns.

## Current standings

| # | Hypothesis | Whose | Verdict | Decisive number |
|---|---|---|---|---|
| H1 | "It's not conscious about it" — no coherent 3D world/anatomy. **Sharpened:** closed-loop imagination (render → TNN sees own render → critiques → re-renders) is the experimental center | Micah | **KEPT** (blind pipeline). H1d closed-loop test **preregistered, pending** — can weaken/kill | Facing flips 180° f=0→f=1; 15/24 valid; 0 depth/occlusion refs in source; compositor has no tuck/behind |
| H2 | "Some external force is limiting it" | Micah | **KEPT** — unchanged by amendment | Warp CONVICTED (Δcov=511/1024, neck 119px off); slot CONVICTED (neck 34px half-vs-half); fixture CONVICTED (snout 28px); znc EXONERATED (Python==Zag) |
| H3 | Failure is the propose→synthesize composition frontier | crew | **KEPT**. ⚔️ **H6 is its main contender** | Oracle 2D: cov=837 but neck_err=120px — 2D can't do both |
| H4 | Anatomy knowledge gap, not machinery | crew | **KEPT** (caveats: "eyes" suspect, snout lands in body) | Part-aware warp Δcov=+192/1024 (kill needed <100) |
| H5 | View mismatch is the whole story | crew | **KILLED as complete** | Best view-matched: cov=1011 but neck_err=70px (bar needed <10px) |
| H6 | **"It's the ARCHITECTURE — it's not discovered yet."** Current warp+graft is programmer architecture; the real fusion architecture hasn't been invented | Micah | **PREREGISTERED, pending** — Fork A (front-facing donor) + Fork B (same pair), TNN-native architecture discovery w/ see-its-result loop | Kill: forks converge on pipeline-equivalent architecture that still stickers. Keep: forks invent a non-equivalent architecture that beats the oracle ceiling (neck_err<40px @ cov≥500) or passes Micah's eyes |

## Open threads

1. **H6** — awaiting Fork A / Fork B outcomes vs the preregistered bars.
   Fable's opinion ("missing representation is articulated part pose; solving a
   3D visibility problem with a 2D lookup table") logged as opinion-input
   consistent with H6, NOT evidence.
2. **H1d** — closed-loop protocol preregistered, awaiting execution with TNN's
   own intake (no LLM stand-ins; honesty constraints in the amendment).
3. **H3 vs H6** — decisive observation preregistered: if the forks' discovered
   architecture has no recognizable propose/synthesize split, H3's framing
   dissolves and H6 wins the round.

## What would change the board

- H1d: TNN sees its own sticker and says "that's fur on a head" → H1 weakened;
  sees + fixes via re-render loop → H1 killed.
- Forks converge on warp+graft-equivalent + still sticker → H6 killed
  (failure is execution/knowledge/composition/awareness, not architecture).
- Forks invent non-equivalent architecture beating neck_err<40px @ cov≥500 →
  H6 kept; H3's seam framing under pressure.
