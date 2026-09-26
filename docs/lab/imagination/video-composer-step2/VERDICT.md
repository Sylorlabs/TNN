# VERDICT — video-composer STEP 2: "merge the pig and the bunny together"

Date: 2026-09-26. Mechanism: composer organ, pure Zag, zero RNG.
Test instruction: **"merge the pig and the bunny together"**

## TL;DR

**The deliberation is genuine; the merge is crude.** TNN's composer organ
really did reason: it measured both memories with its own saliency, proposed
18 plans from a generic language, scored each on five criteria, picked the
winner by exact integer argmax, and wrote down why — including why the
closest rival lost by 10.80 points. The choice is proven content-sensitive
(same verb on different content → different winner) and instruction-sensitive
(three verbs → three different winners), deterministic (byte-identical reruns),
and it robustly rejects the cheap dissolve (ablation: removing the dissolve
penalty still doesn't let XFADE win).

**But the winning composition is a corner sticker, not a merge.** The plan
grafts a 107×80 crop of the bunny's face into the top-right corner of the pig
frame. It is deliberate, but it is not the head-swap Micah described, and it
is not much of a "merge" in any human sense. The mechanism's rubric rewards
PRESERVATION (don't damage either subject's measured subjectness); it has no
concept of TRANSFORMATION (take head A, put it on body B). A head-swap is not
expressible in the 18-plan language at all — no plan can do it, so no
deliberation could have chosen it. That is a boundary of the plan language,
not a failure of the deliberation.

**Partial credit, honestly:** the organ works as designed — mechanism-owned
choice with recorded reasons — but STEP 2 does not yet produce imaginative
composition. The deliberation machinery is real; the imagination is crude.

## 1. What the mechanism did (its own trace)

Instruction parsed: `verb=MERGE subjects=[pig,bunny]`.
Perception (motion+texture saliency, thirds-grid, ×10000):
- bunny: focus cell4, rect (106,80)-(213,160) — the face. Correct.
- pig: focus cell7, rect (106,160)-(213,240) — bottom-middle; catches the
  head's edge, front leg, and textured ground. Crude but plausible ("busy
  region", not the head cleanly).

Full candidate table (score = 35·verb_fit + 30·presence + 20·balance +
10·recognizability + 5·parsimony; ×100 scale):

| plan | verb | pres | bal | rec | total |
|---|---|---|---|---|---|
| [00] OVERLAY bunny→pig REPLACE | 100.00 | 26.02 | 37.64 | 100.00 | 6533.40 |
| **[01] OVERLAY bunny→pig ADJOIN** | 100.00 | 28.82 | 33.98 | 100.00 | **6544.20** |
| [02] OVERLAY pig→bunny REPLACE | 100.00 | 11.57 | 24.52 | 100.00 | 5837.50 |
| [03] OVERLAY pig→bunny ADJOIN | 100.00 | 16.80 | 16.89 | 100.00 | 5841.80 |
| [04–07] PIP bunny→pig (4 corners) | 85.00 | 21.60–25.63 | 38.21–45.34 | 80.00 | 5808.10–5829.80 |
| [08–11] PIP pig→bunny (4 corners) | 85.00 | 11.34–14.62 | 19.40–25.02 | 80.00 | 5101.60–5115.60 |
| [12] SPLIT_V bunny\|pig | 60.00 | 22.09 | 95.18 | 100.00 | 6166.30 |
| [13] SPLIT_V pig\|bunny | 60.00 | 28.04 | 95.71 | 100.00 | 6355.40 |
| [14] SPLIT_H bunny/pig | 60.00 | 25.86 | 69.37 | 100.00 | 5763.20 |
| [15] SPLIT_H pig/bunny | 60.00 | 22.43 | 67.55 | 100.00 | 5623.90 |
| [16] INTERLEAVE k=2 | 40.00 | 25.00 | 100.00 | 90.00 | 5550.00 |
| [17] XFADE n=8 | 45.00 | 25.00 | 100.00 | 30.00 | 5125.00 |

Selected: **[01] OVERLAY bunny→pig ADJOIN graft=(213,0)-(320,80)** —
the bunny's face rect pasted at the top-right corner (the corner minimizing
overlap with the pig's measured saliency).

Recorded reasons (from the trace, verbatim in spirit):
- MERGE demands one integrated frame: OVERLAY/PIP fit (100/85); SPLIT
  juxtaposes (60); INTERLEAVE alternates (40); XFADE dissolves (45).
- Closest rival [00] REPLACE lost by **10.80** on presence (28.82 vs 26.02):
  centering the graft on the pig's focus covers more of the pig's
  subjectness; the corner placement preserves it. (This near-tie is
  disclosed, not hidden — the margin is exact and deterministic.)
- Best SPLIT [13] lost by 188.80, decisive: verb_fit (100 vs 60).
- Best PIP [06] lost by 714.40, decisive: verb_fit (100 vs 85).
- INTERLEAVE/XFADE lost by 994–1419, decisive: verb_fit.

## 2. Is the deliberation genuine? (yes — four proofs)

**Instruction-sensitivity** (same pair, three verbs → three winners):
- "merge the pig and the bunny together" → [01] OVERLAY ADJOIN (6544.20)
- "show the pig and the bunny side by side" → [13] SPLIT_V pig|bunny (7755.40)
- "show the pig and the bunny one after the other" → [16] INTERLEAVE (7650.00)

**Content-sensitivity** (same verb MERGE, different content → different winner):
- (bunny, pig) → [01] OVERLAY ADJOIN (6544.20)
- (bunny, field [pig 9–12s, similar framing]) → [01] OVERLAY ADJOIN (6543.20;
  same plan, as the content is genuinely similar — focus cell7 both)
- (hare [bunny 120–123s wide shot], pig) → **[15] SPLIT_H hare/pig (6435.40)**.
  The hare memory's saliency latched onto background trees (focus cell2), so
  overlay plans scored poorly on presence and the split won. The choice moved
  with the measurements, not the labels.

**Ablation** (is the dissolve rejection load-bearing?): variant binary with
the XFADE recognizability penalty removed (3000→10000). XFADE rises
5125.00→5825.00 but STILL loses to [01] (6544.20). The rejection is
overdetermined — verb_fit (45 vs 100) and presence independently disfavor the
dissolve. The standard is doing real work, not one tuned constant.

**Determinism** (zero RNG, byte-identical reruns):
- ingest ×2: stores + traces byte-identical (bunny, pig)
- recall: 24/24 frames bit-exact vs sources, both videos
- still ingest/recall ×2: bit-exact, byte-identical
- compose MERGE ×2: trace + all 24 frames byte-identical

## 3. Is the composition a merge? (no — and why)

The output: the pig video plays full-frame with a 107×80 bunny-face patch
in the top-right corner. Both subjects are present; neither is damaged. It is
a deliberate composite, but it is a **corner sticker**, not a merge. It does
not interpenetrate the subjects, does not relate them, and certainly does not
swap heads.

The deep reason: **every criterion in the rubric is about preservation**
(presence = don't cover subjectness; balance; recognizability = don't
shrink/blend the graft). There is no criterion and no operator for
transformation. A head-swap DESTROYS part of each subject to create something
new — the rubric cannot value that, and the 18-plan language cannot express
it (no segmentation, no part correspondence, no part-level operators). The
deliberation is real, but it deliberates over a language too poor for
imagination. This is the honest boundary of STEP 2.

Secondary honesty notes:
- The pig's measured focus (bottom-middle) is not cleanly the head; the
  saliency is "busy region," not object perception. The trace shows this.
- The [00]/[01] margin (10.80) is thin and turns on the programmer-authored
  corner rule. Deterministic and disclosed, but thin.
- verb_fit carries the MERGE-vs-SPLIT decision (100 vs 60); that number
  encodes the programmer's principle "merge = one integrated frame." The
  principle is stated, generic (no pig/bunny content), and applied uniformly —
  but it is doing heavy lifting, and the verdict does not hide that.

## 4. What would need to change (future steps, not this one)

1. Part correspondence: measure WHICH region of A corresponds to WHICH
   region of B (the hare test shows saliency alone latches onto trees).
2. Transformation operators: part-level grafts (head-swap), not just
   rectangular overlays — plus a rubric criterion that can value creating
   something new, not only preserving.
3. Segmentation: grafts carry background (blue sky in the bunny patch)
   because there is no figure/ground separation.

## 5. Evidence inventory

- Source: `src/composer.zag` (pure Zag, ~1500 lines), `src/composer_ablate.zag`
  (single-constant ablation variant), `run_all.sh`, `DESIGN.md` (+ grok review
  disposition), this file.
- Traces: `runs/compose_merge_A/compose_trace.txt` (main),
  `runs/compose_side/`, `runs/compose_then/`, `runs/compose_merge_hare/`,
  `runs/compose_merge_ablate/`, `runs/compose_merge_field/`.
- Renders: `mp4/` (winner, side, then, xfade/split comparisons, dumb
  control, hare merge, references).
- Gallery: `~/workspace/your_files/video_composer_new/gallery.html`
  (self-contained, all data URIs).
- Key hashes:
  - merge trace: `623644ccb3a2563ad9a648eaac97a48065a705d0c6e1f5f631d074542a90cc3b`
  - merge frame_00: `8bf052e5392f0f854c54ded98194e273b49266e8e555fab770ba688fe3173b46`
  - merge frame_23: `bd6eb91bb0fa9c8249147f676f7d5d1227487815acf1441d8a93110496ecf908`
- Grok-4.7 highest-reasoning review: `/tmp/vc_view/grok_review.md`
  (verdict: "fundamental flaw requiring rethink"; disposition in DESIGN.md —
  build with strengthened agency tests, which this verdict reports).
