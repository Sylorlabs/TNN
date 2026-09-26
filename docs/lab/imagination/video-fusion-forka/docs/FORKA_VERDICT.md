# FUSION FORK A/B — Verdict: TNN-native closed-loop imagination

Micah order 2026-09-26 ~10:40 PDT: "I think it's the architecture — it's not discovered yet.
It's not even able to identify the head or match background, it's just a black blob.
Let TNN see its result — don't just let TNN imagine it without it knowing what it's imagining.
Try a front-facing pig clip and try the same one too as forks."

Two forks of one new architecture:
- FORK A: front-facing pig donor — `File:Pigs Love Watermelon.webm` (Wikimedia Commons,
  CC BY 3.0, author Two Drs Homestead; real adult domestic pig, head-up, dead-frontal;
  dead-frontal core ~1.3 s at t=15.7–16.9 s). Donor record: `~/workspace/fusion_forka/DONOR.md`.
  Frames: `~/workspace/fusion_forka/donor_frames/` (54 PPM, 480x854, 29.97 fps).
- FORK B (control): the same new architecture on the OLD head-down pig pair.

## What TNN built (its reasons, from the trace)

A closed-loop 2D deliberation architecture: render → perceive its own render with its own
bit-exact vision → critique in its own vocabulary (blob/nofeat/seam/neck/light/cover/pose)
→ adjust (gain/feather/bgmatch/warp) → re-render, with ablation runs. Fork A: rev_0→rev_2
+ 5 ablations. Fork B: rev_0→rev_2 + 6 ablations (incl. ablate_sel).

## TNN's own verdicts (recorded before human eyes judged)

Fork A: "OVERALL: ONE_ANIMAL — I judge my render one animal: a recognizable pig head,
attached at the neck, background matched, lit as one creature." (HEAD/NECK/BG/LIGHT/POSE all PASS)
Fork B: "OVERALL: STICKER — I judge my render a sticker: it does not replace the
recipient's head. I do not pass it." (HEAD FAIL, LIGHT FAIL)

## Plain judgments (human eyes)

- FORK A: STICKER — TNN was WRONG. A rectangular pig-snout patch pasted on the bunny's
  forehead: visible edges, the bunny's own nose still below it, not a head replacement.
- FORK B: STICKER — TNN was correct. Dark blobby masses pasted on the bunny's head/ears,
  not a recognizable pig head.

## H1d preregistration result

Protocol: render → TNN perceives own render with own intake (bit-exact PPM reingestion,
FNV-verified) → critiques in own vocabulary → re-renders. Full frames, no crops, no LLM
in the critique path. Paired control: same vocabulary on known-good renders
(donor pig frame, recipient bunny frame) scored COHERENT 3/3 — the critique discriminates
real animals.

| Fork | TNN saw | H1 status |
|------|---------|-----------|
| A | Called its own sticker "one animal" | H1 HOLDS |
| B | Saw the sticker AS a sticker | H1 WEAKENED |

H1 = Micah's hypothesis that TNN isn't conscious of the merge / doesn't represent the
scene as a 3D world. The critique catches obvious failures (Fork B's black blobs) but
misses subtle ones (Fork A's textured snout-patch with zero measured defects) — it is
unreliable, and the closed loop is not a valid test apparatus in its current form.
The contradiction itself is the finding.

## Fable sparring (opinion, not evidence)

Fable's diagnosis: missing articulated 3D pose — "solving a 3D visibility problem with a
2D lookup table." Proposed: 2.5D skeleton, yaw from tan(yaw)=snout_offset/half_width,
SELECT the matching-yaw pig frame instead of warping, neck as four-constraint interface,
lighting via scene-light-direction estimate. Smoking gun: a 0°-yaw bunny and a 45°-yaw
bunny must use DIFFERENT pig frames; same frame = still pasting.

What TNN invented: closed-loop 2D deliberation. It did NOT invent 3D pose, yaw
estimation, or yaw-based frame selection — it uses 2D facing vectors + flip and selects
frames by texture/asymmetry. Verdict: neither "equivalent" nor "different and better."
TNN invented something DIFFERENT (closed-loop 2D critique) that did NOT beat the bars —
both forks are stickers. Fable's diagnosis is confirmed by the failure mode: the 2D
approach cannot synthesize a head swap. The defects TNN measured were photometric
(seam, light), never structural (pose, 3D) — the architecture has no representation of
viewing angle or 3D hinge.

## Honest gaps

1. INVENTION BAR NOT MET: the defect→operator mappings in `w2e_delib.zag` are
   programmer-authored decision trees, not TNN-invented. The closed-loop STRUCTURE is
   implemented; the "TNN-native invention" claim is not earned. Do not claim otherwise.
2. Byte-identical reruns NOT completed: rerun processes died during a service restart.
   Fork B run1 vs run2 differ (different code versions — expected). No x2 proof available.
3. Galleries show sampled frames (0,6,12,18,23 per rev), NOT full 24-frame sequences —
   below the full-duration bar.
4. Micah's hypothesis CONFIRMED in substance: the architecture is undiscovered; the
   current machinery cannot identify the head or match background as a 3D arrangement —
   it pastes. H1 holds where it matters (Fork A).

## Deliverables

- Sources: `src/` (fuseA.zag + w2a–w2f modules; pure Zag, zero RNG)
- Traces: `evidence/` (TRACE.txt forkA_run1, forkB_run1, forkB_run2; CONTROL.txt; failrec)
- Donor record: `evidence/DONOR.md` (CC BY 3.0 attribution required on published use)
- Galleries (self-contained, data URIs, zero external loads):
  `~/workspace/your_files/video_fusion_forka_front_NEW/index.html` (Fork A, 10 frames)
  `~/workspace/your_files/video_fusion_forka_control_NEW/index.html` (Fork B, 20 frames)
