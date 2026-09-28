# AUDIO ROUND 3 — DEBATE JUDGING RUBRIC (draft, pre-positions)

## The law (absolute, non-negotiable)
No synthesizers, period. No oscillators, no formant synths, no LF glottal
models, no parametric excitation, no noise-burst "transient synthesizers",
no physical-model oscillators that are synths by another name.

## Micah's Round-2 ear verdicts (2026-09-24) — binding for Round 3
- CLIP_A glottal_formant = BEST (notation correct, NO STATIC)
- CLIP_B skeleton_refine = middle
- CLIP_C prosody_ab = WORST (lots of static)
STATIC IS THE KILLER. "No audible static" is a HARD GATE for anything
reaching Micah's ears. glottal_formant's clarity is the bar to beat —
without synths. Any fork whose analyzer profile shows static-like energy
(broadband HF hash, transient-rate hash, grain-boundary clicks) must be
killed or repaired before staging, not shipped "for the ears to decide".

## Judging criteria (in order)
0. NO-STATIC (pass/fail per fork): the design must not contain a
   static-generating step (grain-boundary discontinuities, sub-period
   grains, uncorrelated noise layering, hash-indexed anything in the
   audio path). Static suspicion = analyzer must prove it absent.
1. LAW COMPLIANCE (pass/fail per fork): every output sample must trace to a
   recorded sample through a documented transform. Any fork whose chain
   contains a generative step (oscillator, parametric excitation, synthetic
   noise source, FM/AM synthesis) FAILS outright, however good its gates.
   Interpolation/resampling is the contested zone: allowed only if the fork
   defends it as non-generative AND bounds it AND its kill experiment proves
   the real-source content is load-bearing.
2. TESTABILITY: preregistered kill bars with numbers; a self-kill experiment
   that would kill the approach itself; analyzer-first; honest failure mode
   stated. Vague bars ("sounds natural") score zero.
3. NO-SYNTH NOVELTY: where does compellingness come from under the law?
   (selection intelligence, edit planning, layering, performance shaping —
   not new samples). Forks that are just "play the recording" with trivial
   edits score low unless the edit planning itself is the tested novelty.
4. FEASIBILITY in pure Zag, zero RNG, byte-identical reruns.
5. DELTA vs Round 2: must be genuinely different from the synth line AND
   from vowel_fossils (the one prior real-audio fork) — measured
   fingerprint distance, not just a new name.

## Verdict form per fork
- ADOPT (build now) / ADOPT-WITH-REPAIR (build with stated fix) / REJECT
  (with the specific criterion it failed).
- The winning set: 2-4 forks max, covering distinct mechanisms.
- One fork MUST be the conscious-KB-driven editor (Micah's order): the
  editing decisions made by TNN's deliberate memory agency over a KB of
  real audio units, running autonomously.

## After judging
Write ROUND3_PREREG.md: shared laws, shared gates (carry Round-2 gates +
PERIODICITY/HF_ROLLOFF/PROSODY/TRANSIENT), per-fork kill bars transcribed
from the winning positions (verify against the position docs, don't
re-transcribe from memory), deliverables, commit plan. Then dispatch build
crews with restart-resilience orders (incremental commits ≤15 min).
