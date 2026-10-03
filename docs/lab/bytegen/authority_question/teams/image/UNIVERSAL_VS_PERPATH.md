# UNIVERSAL_VS_PERPATH — argued position

Team Image, 2026-09-23. Position: **UNIVERSAL RULE, PER-PATH
INSTANTIATION.** The authority principle is one; its geometry differs
per path. Argued from image evidence below.

## What image evidence shows

**1. The three-piece template fits image with Piece 3 empty — and the
emptiness is a finding, not a gap.** Audio needs the latch because
RESPOND answers a measured external stimulus (cue pitch). Image has no
external-stimulus analog: the plan (strokes, seed, theme) is fully
authored before the first pixel renders. I audited every native image
path for a discrete measured-plan-fact and found none — d_blend reads
are arithmetic operands (PATH_MECHANICS.md), grain reads plan cells,
`d_get` is dead code. An empty Piece 3 is therefore the *correct*
instantiation, and the template's value is proven by the audit it
forced: without the template, "is there a latch here?" is never asked.

**2. The classification criterion is path-independent.** The d_blend
settlement (data flow with plan-fixed operator vs control flow over
measured output) decided a question the audio battery also had to
decide (additive mix accumulation ≠ feedback; carried DSP state ≠
feedback — survey FINDINGS.md classification criteria). One criterion,
applied twice, same answer. If authority philosophy were per-path, each
path would re-derive "what counts as feedback" from scratch — and the
two derivations could disagree, which is incoherent: feedback-ness is
a property of the information flow, not of the medium.

**3. The gamma lesson is path-independent.** Output-derived global
gains break bit-identity, amplify single faults globally, and make
detection targets ill-defined — whether the bytes are samples
(`f3_emit_wav` :1025–1039, the native specimen) or pixels (the
hypothetical auto-contrast post-pass, FAULT_ANALYSIS §F3). The proof
doesn't mention audio or image; it mentions functions of corrupted
outputs. A per-path philosophy would have to re-prove this per path,
and a path that skipped the proof would ship the disease.

**4. The contractivity proof is path-independent.** "Correction map
constant in the corruption ⇒ Lipschitz 0 ⇒ one-step, idempotent,
no 2-cycle" (HYBRID_SPEC §2) holds for 1024-sample blocks and for
128×128 pixel tiles identically. Image's case is strictly stronger
(bit-exact detection, no band floor), which is a *parameter* difference
(detection predicate), not a *principle* difference.

## What genuinely differs per path (the instantiation layer)

| Aspect | Audio | Image |
|---|---|---|
| Plan form | event list (23 events, timing/envelope/pitch) | stroke log (op+8 params, ≤64), op sequence, (scene, seed, W, H) |
| "Region" for Piece 2 | 1024-sample block | 128×128 pixel tile (proposed) |
| Detection predicate | band-based (RMS vs plan_rms, peak edge) — has a floor | bit-exact re-render + diff — no floor |
| Carried state at risk | phase accumulators, filter memory | field cells, canvas pixels (Path C: none) |
| Piece 3 | occupied (octave latch) | audited empty |
| Piece-1 rendering operators that read output | additive mix accumulation | d_blend / f3_blend alpha compositing |

None of these rows changes the rule: plan sole authority; feedback
only on the exception path as plan-pure re-assertion; no continuous
servo; no output-derived global gains. They change *what the plan is*,
*what a region is*, and *which slots are occupied* — implementation
geometry, which must be per-path because the media differ.

## Why not fully per-path (the cost of N philosophies)

1. **Re-litigation cost.** Audio's attack battery (11 attacks) settled
   hard questions: frozen targets (A1), involution instability (A4),
   forward-correction causality (A6), one-loop incoherence (A11). Under
   per-path philosophy, image would re-run equivalents to earn the same
   conclusions — or skip them and risk shipping a v1-style servo under a
   new name. The universal rule imports the verdicts; the per-path
   battery (BATTERY_PREREG_DRAFT.md B-WRONG) only needs to show the
   *instantiations* of the wrong rules fail, not re-derive the theory.
2. **Incoherence risk.** "Feedback" meaning one thing for audio and
   another for image is not pluralism, it's a bug factory — a mechanism
   ruled out on audio (output-derived global gain) could be admitted on
   image by a team that derived a looser criterion, and the codebase
   already contains the specimen (`f3_emit_wav` normalizers) proving
   this happens without a shared rule.
3. **Micah's decision load.** He decides once (the rule), not N times
   (per-path philosophies). Per-path *audits* (is Piece 3 occupied here?
   what is the plan form?) come to him as findings, not decisions.

## Why not fully universal (no per-path anything)

Because the rule without instantiation is unenforceable: "re-render the
region plan-pure" is meaningless until *region* and *plan* are defined
for the path (tile vs block; stroke log vs event list), and the Piece-3
audit must actually be performed per path — I did it for image and it
came back empty; asserting it empty without the audit would be the
vibes-claim Micah has corrected twice. Universality of principle does
not license skipping per-path verification.

## Position, stated for Micah

Adopt **one authority rule for all generation paths** — plan absolute;
output feedback earns authority only on the exception path
(fault/dropout), as plan-pure re-assertion, Lipschitz-0, one-step,
idempotent; no continuous servos; no output-derived global gains;
discrete latches only for demonstrated discrete measured-plan-facts —
and require **a per-path instantiation document** (plan form, region
geometry, carried-state inventory, Piece-3 audit, rendering operators
that read output with their classification) before any path claims
compliance. Image's instantiation is this team's six documents; the
empty Piece 3 is image's audited result, not a template default.
