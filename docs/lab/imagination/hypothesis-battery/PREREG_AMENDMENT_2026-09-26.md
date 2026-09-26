# PREREGISTRATION AMENDMENT — 2026-09-26 ~11:30 PDT

**Amends:** `PREREG.md` (frozen 2026-09-26, commit `8e7887a112f9d3eb225037a4f93f6e3b794405ae`).
**Ordered by:** Micah, sharpening issued ~10:40 PDT 2026-09-26, recorded here ~11:30 PDT.

This amendment **ADDS**. It does not rewrite, soften, or retroactively alter the
original preregistration. All original kill bars stand. The completed verdicts
(H1 KEPT on H1a/b/c; H2 KEPT; H3 KEPT; H4 KEPT; H5 KILLED-as-complete —
commit `1f33f74b8aeec2b19d762e46f9301eb8a1415e15`) are unchanged. Two things
are added: a new hypothesis H6 with its own preregistered bars, and a
sharpened closed-loop test H1d that gives H1 an additional, independent kill
path. H2 is explicitly unchanged.

---

## 1. NEW HYPOTHESIS H6 (Micah's): "it's the ARCHITECTURE — it's not discovered yet"

**Statement:** The sticker is not a knowledge gap (H4), not a consciousness gap
(H1), and not a bug at the composition seam (H3). The fusion architecture
itself — what machinery should exist between "see donor" and "render merge" —
has never been discovered. The current warp+graft pipeline (anatomy →
affine warp → alpha composite) is PROGRAMMER architecture: a human decided the
boxes and the arrows. TNN never invented fusion; it executes our pipeline.
The real architecture hasn't been invented yet.

**How H6 differs from its neighbors:**

| Hypothesis | Claims the problem is |
|---|---|
| H1 | No 3D/anatomical awareness in the merge |
| H3 | The propose→synthesize seam, given the current pipeline shape |
| H4 | Missing anatomical knowledge fed into the current pipeline |
| **H6** | **The pipeline shape itself — the boxes are ours, not TNN's** |

H6 is flagged as **H3's main contender**: H3's "frontier" framing assumes
warp+graft is the right decomposition and localizes the failure to synthesize.
If H6 is right, there is no propose→synthesize frontier — there is a missing
building, and H3's seam dissolves into "wrong decomposition."

**Evidence (tracked, NOT duplicated):** Two forks dispatched ~10:40 PDT
2026-09-26, both running **TNN-native architecture discovery with a
see-its-result loop**:

- **Fork A (front-facing donor):** TNN invents the fusion architecture with
  view-matched donor footage (the H5 confound removed by construction).
- **Fork B (same pair):** TNN invents the fusion architecture on the exact
  donor/recipient pair that stickers under the current pipeline.

Their outcomes are evidence for/against H6. This battery does not duplicate
them; it records their results against the bars below when they land.
**Status at amendment time: both PENDING.**

**Preregistered bars:**

- **H6 is KEPT iff** TNN-native discovery produces a fusion architecture that
  (a) is NOT structurally equivalent to the current pipeline — i.e. it does
  not reduce to 2D landmarks → 2D geometric warp → alpha composite; it must
  introduce a representation or step the current pipeline lacks (articulated
  part pose, visibility/depth reasoning, or something stranger — "let it be
  weird if it helps"), **AND** (b) it renders a merge that either passes
  Micah's bar (one animal with the pig's head, his eyes are the judge) or
  beats the current pipeline's oracle ceiling mechanically: `neck_err < 40px`
  at `cov ≥ 500/1024` (the H3 oracle proved the current pipeline cannot do
  better than `neck_err=120px` at max coverage — 3× better is a different
  building, not a tuned one).

- **H6 is KILLED iff** TNN-native discovery, with the see-its-result loop and
  full inventive freedom, converges on an architecture **structurally
  equivalent** to the current pipeline (landmark detection → geometric warp →
  composite, no new representation) **AND** the result still stickers (fails
  Micah's bar AND `neck_err ≥ 80px` — no better than the current oracle
  ceiling's neighborhood). Then the architecture wasn't the missing piece:
  TNN with full freedom rebuilt the same building, so the failure is in
  execution/knowledge (H4), composition (H3), or awareness (H1) — not
  architectural absence.

- **Weakened (documented, not killed/kept):** discovery produces a
  non-equivalent architecture that still stickers → architecture was necessary
  but not sufficient.

**Decisive H6-vs-H3 observation (preregistered):** if the forks' discovered
architecture has no recognizable propose/synthesize split (or a different
split), H3's framing dissolves and H6 wins that round. If the forks converge
on propose→synthesize with a better synthesize, H3 is refined (not killed)
and H6 is killed.

**Opinion input (NOT evidence):** Fable's completed consultation independently
landed on an architecture claim: *"the missing representation is articulated
part pose; solving a 3D visibility problem with a 2D lookup table."* This is
logged as opinion-input **consistent with H6** (it names a missing
representation — an architectural claim). Per standing protocol (2026-09-24:
Fable's proposals are never applied directly; test first, red-team, report
back), it moves no bar. Only the forks' outcomes are evidence.

---

## 2. SHARPENED H1: closed-loop imagination (new test H1d)

**Micah's words (verbatim in spirit):** "let TNN see its result — don't just
let TNN imagine it without it knowing what it's imagining."

The completed H1a/b/c tests measured the **blind** pipeline (render once,
never look). H1d makes **closed-loop imagination** the experimental center of
H1: render → TNN perceives its OWN render → critiques it → re-renders.

**Protocol H1d (preregistered):**

1. **RENDER.** The step-5 sticker render (commit `9d4d83119a42`,
   `~/workspace/your_files/video_fusion_step5/`). Full frames, never crops or
   thumbnails (full-eyes law).
2. **PERCEIVE.** TNN takes its OWN render through its OWN image intake — the
   same intake machinery it uses for donor/recipient footage. No special-case
   path, no downsampling the question away.
3. **CRITIQUE.** TNN answers, in its own vocabulary and by its own deliberation
   over its perceptual intake: "is this one animal with the pig's head, or is
   it something else?" Not a programmer checklist ("neck attached: Y/N"), not
   an LLM judge's opinion, not a metric threshold — TNN's own perception of
   its own render.
4. **RE-RENDER.** If the critique identifies the failure, TNN re-renders with
   the critique informing the new attempt. The loop runs until TNN declares the
   render acceptable or declares it cannot fix it. Both outcomes are data.

**Honesty constraints (preregistered, binding):**

- The perceiver must be TNN's own intake + deliberation, not a stand-in. If
  the available TNN image machinery cannot do open-ended critique, that is
  recorded AS A FINDING (it bears on H1/H4/H6) — it is NOT worked around with
  an LLM judge and called TNN's perception.
- TNN must possess the concepts "head swap" vs "fur patch / sticker." If the
  concepts must be taught for the test to run, the teaching is logged in the
  protocol, and a "taught" pass is distinguished from a "native" pass.
- The critique question is fixed in advance (above) and identical across loop
  iterations. Full frames throughout.

**Preregistered control:** paired discrimination — TNN is shown its sticker
render and a positive control (a genuine head-swap or the best available
non-sticker) side by side through the same intake and asked which is one
animal. If it discriminates correctly but the H1d critique fails, the gap is
expressive (H4/H6 territory), not perceptual — recorded, and H1 is weakened
rather than held.

**Sharpened kill bar (an ADDITIONAL, independent kill path — H1a/b/c stand):**

- **H1 WEAKENED iff** TNN perceives its own sticker through its own intake
  and reports the failure in its own words ("that's fur on a head, not a head
  swap" or equivalent). It demonstrates imaginal awareness the blind pipeline
  lacked — it can see the merge AS a merge. Weakened, not killed: seeing the
  failure is not fixing it.
- **H1 KILLED iff** TNN names the failure AND the re-render loop converges to
  a non-sticker (passes Micah's bar, or `neck_err < 40px` at `cov ≥ 500/1024`).
  Consciousness of the merge was the missing ingredient, and supplying it
  fixed the failure.
- **H1 HOLDS (full strength) iff** TNN looks at its own sticker through its
  own intake and calls it one animal — or cannot distinguish it from a
  successful head swap in the paired control. It is not conscious of the merge
  even with its own eyes on its own render.

**Status: PREREGISTERED 2026-09-26 ~11:30 PDT. PENDING EXECUTION.**
The H1a/b/c verdict (H1 KEPT for the blind pipeline) is unchanged; H1d does
not retroactively alter completed tests.

---

## 3. H2 — unchanged

Micah's "external force" battery (L1 warp CONVICTED, L2 slot CONVICTED,
L3 fixture CONVICTED, L4 znc EXONERATED) stands exactly as committed. No
amendment.

---

## 4. Scoreboard as amended

| # | Hypothesis | Source | Status |
|---|---|---|---|
| H1 | "Not conscious of the merge" — **sharpened**: closed-loop imagination (H1d) is the experimental center | Micah | **KEPT** (blind pipeline, H1a/b/c). H1d **pending** — can weaken/kill per §2 |
| H2 | External limiters (warp / slot / fixture / znc) | Micah | **KEPT** (3 convicted, 1 exonerated). Unchanged |
| H3 | Propose→synthesize composition frontier | crew | **KEPT**. **H6 is its main contender** — decisive observation preregistered in §1 |
| H4 | Anatomy knowledge gap, not machinery | crew | **KEPT** (with caveats). Unchanged |
| H5 | View mismatch is the whole story | crew | **KILLED as complete**. Unchanged |
| **H6** | **"It's the ARCHITECTURE — it's not discovered yet"** | **Micah** | **PREREGISTERED**. Pending Fork A / Fork B outcomes vs §1 bars |

---

## 5. Commit sequence (amended)

1. `PREREG.md` — frozen before any probe built/run (commit `8e7887a1`). ✔
2. Probe sources + build log, byte-identical reruns (commit `1f33f74b`). ✔
3. `VERDICT.md` — H1–H5 scoreboard (commit `1f33f74b`). ✔
4. **This amendment** — H6 preregistered, H1 sharpened (H1d), scoreboard v2.
5. Fork A / Fork B outcomes → H6 verdict (pending).
6. H1d execution → H1 final (pending).

All commits to `tnn-native-lab`, never main. No step-6 files touched.
Step 6 remains the forward build and is not collided with.
