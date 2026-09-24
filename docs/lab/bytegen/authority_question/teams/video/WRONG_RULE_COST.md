# WRONG_RULE_COST — video

Two directions. Costs are stated mechanically — what bytes change, what bars
fail, what the viewer (Micah's eyes, which outrank all metrics) sees.

## Direction A: feedback admitted where none belonged

The rule says "no continuous feedback, no output-conditioned scene events."
Suppose Micah overrules it and a servo/latch ships in the video path.

### A1. The coherence tax: recurrence 1.0 → <1.0 (certain, structural)

Today: re-render frame `f` at any time → byte-identical bytes. V-DET passes
by construction (48/48 frames, manifest `400ae5c6…938b26ac9`).

With a per-frame servo: frame `f`'s bytes become a function of
(plan, f, measured(frame f−1), …). Standalone re-render of frame 23 no
longer reproduces the shipped frame 23 — V-DET can only pass by re-rendering
the entire sequence in order, carrying servo state. The program loses its
cheapest correctness property (any frame, any time, byte-exact) and gains a
whole-sequence re-render requirement for every fix. Debugging changes
character: "why does frame 30 look wrong?" now requires replaying frames
0–29 with byte-exact servo state, instead of inspecting `F(plan, 30)`.

**Viewer-visible:** none directly — the tax is paid in engineering, until A2.

### A2. Plan-fidelity drift: the servo fights the material law (certain, gradual)

A luminance/chroma servo steers pixels toward its frozen target. Ocean's
color is material-driven by design (round-3 tell repair #3: depth→water
color, sun diffuse, fresnel, foam, fog — no global grade). The servo is a
global grade. Frame by frame, it compresses the authored dynamic range:
deep troughs lifted, sun glitter dulled, fog flattened — all toward the
target the plan didn't author. This is audio's Attack 1 (frozen targets)
with a visual face, and it reintroduces the exact "procedural shader" tell
that cost round 2 its blind judging.

**Viewer-visible:** yes — the scene looks "graded," less like a place.
Micah's blind judges already rejected this look once (round 2 V-BLIND
failure). The bars won't catch it (V-SHARP/V-TEMP can pass on graded
frames); only his eyes will, and he'll be re-judging a solved problem.

### A3. Cascade: one corrupted frame diverts the scene (probabilistic, severe)

With output-conditioned scene events (the denied piece 3), a single
artifact fault (VF-1 bit-flip) doesn't just corrupt one frame — it corrupts
the *measurement* the next frame's plan depends on. The latch fires or
misfires on corrupted evidence; frames `f+1…` are computed from a diverged
plan. Healing now requires re-deriving the tail, not rewriting one file —
and the tail's divergence is silent (no predicate fires, because each frame
is "correct" relative to its corrupted predecessor's plan).

**Blast radius:** 1 file → up to the whole sequence. **Detection:** none —
this is the failure mode with no alarm. Audio's RT-CASCADE measured 5,791
derailed samples from one fault in the AR fork; the video version derails
*content*, which no byte-level predicate distinguishes from authored
content. This is the most expensive wrong-rule cost because it is silent.

### A4. Determinism theater: byte-identical reruns that prove nothing

A deterministic servo preserves rerun-identity (same inputs → same bytes),
so V-DET still passes — while plan-fidelity has drifted (A2) and cascades
are possible (A3). The lab's determinism bars would give a false clean bill
of health. This is the subtlest cost: the metrics say "fine" and the scene
is wrong. (Precedent for metrics-vs-eyes divergence: audio V10, where 9/9
bars passed and Micah's ears still rejected the output.)

### A5. The dither-channel false-positive spiral (certain if bands are tightened)

If feedback is admitted, someone will eventually tighten the detection band
to catch sub-floor tamper (VF-5: ±2 LSB dither). The band then false-positives
on clean frames (hash dither is *supposed* to vary ±2 LSB), and each
false positive "corrects" a clean frame — churning bytes that were already
right. The loop manufactures the faults it was built to catch. The honest
floor (FAULT_ANALYSIS.md C5) exists precisely to prevent this; feedback
admission erodes the discipline that keeps it.

## Direction B: plan-absolute imposed where feedback was needed

The rule says "piece 2 heals artifact faults by re-render." Suppose instead
the strictest reading wins — *no* output measurement at all, pure
plan-absolute, no exception path. (This is the steelman I argued and
rejected in AUTHORITY_RECOMMENDATION.md; here are its costs if it had won.)

### B1. Artifact faults ship to the viewer (certain, on every real run)

Disks flip bits, encoders drop chunks, transfers truncate. Without
detection, VF-1–VF-4 reach the AVI/BMP the judge opens. A single black
frame (F-ZFULL) or duplicated frame (F-DUP, visible as a motion hitch) in a
48-frame blind judging clip is a program-level failure — and unlike a servo
drift, it's *visible*: Micah's eyes catch it, the bars might not
(V-TEMP's 15% ceiling could pass one duplicated pair if the sequence is
otherwise calm... actually F-DUP gives |Δ|≈0, below the 0.5% floor — the bar
catches it, but only if someone runs the bar before judging).

**Cost:** re-render the frame anyway, but *after* the embarrassment, and
without the pipeline to do it mechanically. The exception path doesn't add
risk (false positives are no-ops); refusing it only removes healing.

### B2. No principled place to put future genuine measurement needs (structural)

The honest version of Direction B's risk: someday video may need to measure
something the plan genuinely cannot compute — the clearest candidate is
**hardware-in-the-loop**: rendering to a physical display whose calibration
drifts, or a projector with measured color response. There, the measured
bytes are *not* the buffer bytes, and plan-side computation is impossible
(the display is outside the determinism boundary). A rule that forbids all
output measurement would forbid adapting to the display — the one case
where feedback is irreplaceable (AUTHORITY_RECOMMENDATION.md steelman
point 2 names exactly this boundary).

**Mitigation already in the rule:** the recommendation scopes piece 2 to
"bytes the renderer emitted" and gates piece 3 on plan-incomputability
proof. The rule as written does *not* impose Direction B's strictness — it
imposes "no feedback *into generation*," which leaves the hardware-adaptation
door open through the piece-3 gates. The cost materializes only if the rule
is misread as "never measure anything."

### B3. Slower fault response without the pipeline (operational)

Without a standing detect-and-reassert pipeline, each fault becomes a manual
incident: notice, diagnose, re-render by hand, verify. With 48-frame
sequences at ~2.5 s/frame and blind rounds on a schedule, the operational
cost is small per incident but unbounded in aggregate — and every manual
re-render is a chance to re-render with wrong args (wrong `f`, wrong dir),
introducing the exact faults the pipeline prevents.

## Net assessment

| Wrong direction | Worst cost | Reversibility |
|---|---|---|
| Feedback admitted (A) | **A3**: silent scene cascade, no alarm, blast radius = sequence | Hard — shipped frames carry servo history; rollback = full re-render + rule change |
| Plan-absolute w/o exceptions (B) | **B1**: corrupted frames reach the judge | Easy — add piece 2; false positives are no-ops |

The asymmetry favors the recommendation: Direction A's failures are silent
and structural (A3, A4), while Direction B's failures are visible and cheap
to repair (B1 → add the exception path later at zero risk). When the costs
of being wrong are asymmetric, the rule should fail toward the cheap side.
The two-piece rule does: its piece 2 can only no-op or heal, never corrupt.
