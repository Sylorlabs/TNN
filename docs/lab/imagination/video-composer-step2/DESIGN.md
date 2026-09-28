# DESIGN — TNN composer organ (video STEP 2)

## Starting state
- STEP 1 (commit 90e03018e01e): deliberate-memory substrate reproduces 24f
  @8fps 320x240 video bit-exact (PSNR inf / SSIM 1.0). Ops: {mem_add, mem_recall}.
- STEP 2 attempt (commit 1a8d040cd7e): CLEAN NEGATIVE. Both memories verified
  intact (48/48 hashes); composition refused — 0 of {propose, evaluate, select,
  synthesize} present. This build supplies exactly those four.

## What the organ is
A single pure-Zag binary, `composer`, with zero RNG in any path. It extends the
deliberate-memory substrate with a deliberation-and-synthesis organ:

1. **Memory**: verbatim frame stores with provenance (frame,row,episode) +
   a **label** per store (the memory's name, e.g. "bunny"). Reuses the
   mem_add/mem_recall pattern from repro.zag (content-addressed recall).
   New: still-image ingest (general PPM reader, any W/H ≤ 640×480) alongside
   the video-frame path.
2. **Perception** (fixed, generic, measurement-only): per memory, over the clip:
   - motion map: per-pixel Σ|gray(f+1)−gray(f)| over consecutive frames
   - texture map: per-pixel |Δx|+|Δy| gradient energy on the middle frame
   - saliency S = motion + texture (integer, u64)
   - thirds grid (3×3 cells); cell density = (cell_mass/total_mass) /
     (cell_area/frame_area), exact integer fixed-point (×10000)
   - **focus** = argmax-density cell (tiebreak: lowest cell index).
   The mechanism does NOT know "head", "face", "pig", or "bunny" as concepts.
   It knows measured subjectness. The trace records all 9 densities per memory.
3. **Instruction parse** (fixed, generic): lowercase the instruction text;
   verb scan: {merge,combine,fuse,mix,blend}→MERGE, {side by side,beside,
   compare}→SIDE, {then,after,sequence,followed}→THEN; nouns = substring match
   against the loaded stores' labels. Unknown verb or unmatched noun → clean
   refusal (documented, rc=1). No per-pair special cases anywhere.
4. **PROPOSE** — plan language (fixed, generic; 18 candidates, enumerated
   every run, parameters derived from measurements):
   - OVERLAY donor→recipient REPLACE: graft donor's focus rect centered on
     recipient's focus-cell center (both directions → 2 plans)
   - OVERLAY donor→recipient ADJOIN: graft donor's focus rect at the recipient
     frame corner minimizing recipient-saliency overlap (both directions → 2)
   - PIP donor→recipient: donor focus rect nearest-neighbor scaled to 160×120,
     pasted at each of 4 corners (both directions → 8)
   - SPLIT_V at x=160 (2 subject orders), SPLIT_H at y=120 (2 orders) → 4
   - INTERLEAVE k=2 (alternate every 2 frames) → 1
   - XFADE n=8 (linear dissolve over 8 frames, the cheap blend) → 1
   XFADE is included deliberately as the rejectable control: the mechanism
   must be able to prefer a deliberate arrangement OVER the cheap blend,
   with recorded reasons.
5. **EVALUATE** — deterministic deliberative standards (fixed weights,
   authored once, applied identically to every candidate):
   score = 35·verb_fit + 30·presence + 20·balance + 10·recognizability
           + 5·parsimony, all criteria 0..10000 fixed-point, exact integer
   arithmetic, no floats, no RNG.
   - verb_fit (programmer-authored rubric, the "deliberative standard"):
     MERGE: OVERLAY 100, PIP 85, SPLIT 60, XFADE 45, INTERLEAVE 40.
     SIDE: SPLIT 100, PIP 70, OVERLAY 50, INTERLEAVE 30, XFADE 25.
     THEN: INTERLEAVE 100, XFADE 55, SPLIT 40, OVERLAY 30, PIP 30.
   - presence = 10000 · donor_retained · recipient_retained, where
     donor_retained = fraction of DONOR's saliency mass inside the grafted/
     shown region, recipient_retained = 1 − (recipient saliency mass covered).
     SPLIT: mass fractions in each half. INTERLEAVE/XFADE: 2500 (each subject
     temporally/blended half-present: 0.5·0.5).
   - balance = 10000 · min(visA,visB)/max(visA,visB) (both subjects comparably
     present; vis = visible saliency-mass fractions).
   - recognizability: 10000 if no rescale; 8000 if 0.5≤scale≤2.0 (PIP);
     3000 for XFADE (dissolve destroys edges — penalized by standard);
     9000 for INTERLEAVE (frames intact).
   - parsimony: 10000 for every plan here (all single-op; documented tiebreak).
6. **SELECT**: argmax total; tiebreak = lowest candidate index. The trace
   records every candidate's five criterion scores + total, the winner, and
   templated reasons generated FROM the scores (which criterion decided it,
   why the top losers lost).
7. **SYNTHESIZE**: generic pixel primitives (programmer-provided, fixed):
   rect_copy (clipped), scale_nn (nearest neighbor), vsplit/hsplit compose,
   interleave, xfade blend. The WINNING plan's measured parameters execute
   on deliberately recalled frames → 24 output PPMs. ffmpeg (outside Zag)
   encodes presentation MP4s, as in prior steps.

## Honesty architecture (load-bearing)
- The plan LANGUAGE, pixel OPERATORS, rubric WEIGHTS, verb→family map, and
  saliency DEFINITION are programmer-provided generic machinery. They contain
  no reference to pig, bunny, or any specific pair.
- The CHOICE (which plan, which rects, which direction, which corner) is the
  mechanism's own: argmax over scores computed from measurements of the
  actual content. No hardcoded plan for this pair exists anywhere.
- Anti-steering controls (built into the test, not the mechanism):
  (a) the rubric is FIXED BEFORE the selection run and validated in a Python
      prototype for discriminativeness (not for winner-picking);
  (b) a SECOND instruction ("show the pig and the bunny side by side") must
      produce a DIFFERENT winner from the same machinery — instruction
      sensitivity is the proof the choice is the mechanism's;
  (c) the full score table ships in the trace; (d) VERDICT.md gives the
      builder's honest call, including any way the result falls short.
- Prototype prediction (to be confirmed or refuted by the mechanism):
  MERGE → OVERLAY bunny→pig ADJOIN (graft the bunny's concentrated focus
  over the pig frame's quietest corner); SIDE → SPLIT_V pig-left/bunny-right;
  THEN → INTERLEAVE. If the mechanism picks otherwise, the trace — not the
  prototype — is authoritative.
- OUTCOME (2026-09-26): the mechanism confirmed all three predictions
  exactly — MERGE→[01] OVERLAY bunny→pig ADJOIN (6544.20), SIDE→[13] SPLIT_V
  pig|bunny (7755.40), THEN→[16] INTERLEAVE (7650.00). Note: the prototype
  used the same rubric logic, so this is a consistency check, not
  independent evidence. The rubric was fixed before the selection run; the
  only post-run source change added a trace reason line (no score changes).

## Still-image ingest (requirement 2)
`composer stillingest <label> <ppm> <workdir>` / `stillecall`: general PPM
reader (any W/H ≤ 640×480, validates magic/dims/maxval), 1-frame memory,
bit-exact roundtrip verified by SHA-256 in Python. PNG: NOT native — PNGs
enter via ffmpeg→PPM pre-conversion (same as video frames); a Zag inflate
decoder is out of scope for this step and documented as such. (The
imagination crew's emit.zag has a PNG *writer*; no PNG *reader* exists
in-repo.)

## Determinism
Every Zag binary runs twice; all outputs (stores, PPMs, traces) byte-compared
(SHA-256). Zero RNG anywhere. Exact integer arithmetic throughout the
deliberation (no float nondeterminism).

## Deliverables
- ~/workspace/video-composer/: src/composer.zag, run_all.sh, DESIGN.md,
  VERDICT.md, traces/, source/PROVENANCE (pig+bunny), metrics/
- ~/workspace/your_files/video_composer_new/: self-contained gallery
  (EVERYTHING as data: URIs — the last two galleries shipped broken on
  relative paths), MP4s: merge winner, rejected candidates (best SPLIT,
  XFADE), side-by-side winner (2nd instruction), dumb ffmpeg control,
  reference clips.
- Commit code+docs+verdict evidence to tnn-native-lab (never main). No
  binaries, stores, caches, or regenerable renders in the repo.

## Open design risks
1. The saliency definition (motion+texture) is crude — it finds "busy
   regions", not objects. The pig's focus may be leg/ground, not head.
   Mitigation: honesty, not tuning — the trace shows exactly what it found
   and why; the rubric's presence criterion genuinely penalizes
   low-subjectness grafts.
2. ADJOIN vs REPLACE margins may be thin — deterministic anyway (exact
   integer argmax + index tiebreak).
3. XFADE must LOSE for MERGE (else the "deliberate" claim is hollow) —
   the recognizability penalty (3000) plus verb_fit (45) should sink it;
   the trace will show it.

## Grok-4.7 design review (2026-09-26, highest reasoning) — disposition

Full review: `/tmp/vc_view/grok_review.md` (8086 bytes, 7 sections).
Verdict section: **"Fundamental flaw requiring rethink"** — grok argues the
design is "a deterministic scoring engine over a programmer-supplied menu of
18 plans, with programmer-supplied numbers, grid, focus rule, and saliency,"
and demands every programmer-provided number/grid/rule be "replaced by a
mechanism that discovers them from data" before building.

Disposition: **BUILD (with modifications)** — grok's bar exceeds the task's
bar, and its demand is out of scope for STEP 2:

1. The task EXPLICITLY authorizes programmer-provided plan language, pixel
   operators, and "deterministic deliberative standards" ("judge candidates
   against the instruction and deterministic deliberative standards"). The
   load-bearing honesty line is: the CHOICE among plans and the REASONS must
   be the mechanism's own — no pair-specific hardcoded plan, no human writing
   the blend. This design satisfies that line: the rubric contains no
   reference to pigs, bunnies, heads, or these clips; the choice is argmax
   over the mechanism's own content measurements.
2. Grok's demand (learned-from-data aesthetics) is a STEP-5 aspiration, not
   a STEP-2 requirement. The task anticipates partial credit: "Partial credit
   is fine IF honest and trace-proven."
3. Grok is wrong on one fact: the "0.09 margin is noise-laundering" claim
   confuses the Python PROTOTYPE (floats) with the mechanism (exact integer
   fixed-point). Whatever margin the mechanism reports is exact and
   deterministic; the trace shows it and VERDICT.md will report it honestly,
   including if it is thin.

Grok's VALID criticisms, adopted:
- (6a) Rubric ablation: build a variant binary with the XFADE
  recognizability penalty removed; confirm the mechanism then selects the
  dissolve. This proves the deliberative standard is load-bearing and the
  trace is honest about it (the standard, not the content, rejects the cheap
  blend — which is the standard's job).
- (6b) Content-sensitivity: run "merge the field and the bunny together" on
  a third memory (pig 9-12s segment, different framing — body/torso vs the
  3-6s head-at-fence); the SAME verb on DIFFERENT content must change the
  winner/parameters, or the choice is not content-driven.
- (6, "second-instruction test is weak"): strengthened to THREE verbs
  (MERGE/SIDE/THEN) on the same pair, PLUS the content-sensitivity pair.
- (5, "builder can ignore any row"): the FULL 18-row candidate tables for
  the main test go into VERDICT.md, not a curated subset.
- (1, focus may miss the subject): the gallery annotates the measured focus
  rects on real frames, clearly labeled as annotations, so Micah's eyes can
  judge whether the mechanism's "subject" matches his.

What this build does NOT claim (unchanged): no object/part correspondence,
no semantic part-swap (the head-swap example is beyond STEP 2's machinery);
the honest claim is "crude-but-genuine compositional deliberation over a
generic plan language with mechanism-owned choice and recorded reasons."
