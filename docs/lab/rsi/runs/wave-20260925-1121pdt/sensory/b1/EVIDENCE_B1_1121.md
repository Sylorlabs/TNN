# EVIDENCE B1-BOUNCE-1121: two-bounce indirect illumination

Wave: wave-20260925-1121pdt. Lane: sensory. Prereg: PREREG_B1_1121.md,
frozen 2026-09-25 11:45 PDT, committed alone as b2b2a3349 before any B1
code existed. Implementation strictly after (commit-order self-check
satisfied: prereg commit b2b2a3349 precedes this commit).

## Provenance (machine-checkable)

- RENDER_SHA (k384, frozen default): ef32cd9732591ebd7a4d0beecb66788f937e8955258aa8daea6c48dac0205795
- RENDER_SHA (k192, data-amount trial): fbb69aa20d7c78089eb352c565aaa757492550dde2d2f3885d49403bd14920d2
- FIRST_RENDERED_WAVE: wave-20260925-1121pdt
- COMPONENT_LINEAGE: none. Built directly on the r8c substrate
  (b1_baseline.zag reproduces the committed r8c hash
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d).
  No prior candidate's code, renders, or constants are reused. The
  sealed queue (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14,
  whirlpool-planform) is untouched.
- NEW_KNOWLEDGE_CLAIM: A post-pass indirect-illumination bounce on the
  r8c substrate moves shadowed land pixels by only ~2/255 on average
  because pass 3's aerial wash already anchors shadows toward the
  horizon color, leaving almost no headroom for a recolor pass.
- STATUS: DISCARDED per frozen kill bars (see below). Never a judge
  queue item. No sealed pair prepared.

## What was built (pure Zag, zero RNG, no Python)

- b1/b1_baseline.zag: byte copy of r8c_alien.zag with the @import
  repointed at the vendored substrate b1/sub/R33_NATIVE_IO_V1.zag.
- b1/b1_bounce.zag: variant with frozen k=384. New pass 3b after
  r8c_pass3, before fixations: a 64x64 pre-light albedo field A0 is
  built in main before the light pass; the variant pass 3 hands its
  blurred shadow map to b1_apply instead of freeing it; each shadowed
  land pixel (luma >= 24) is mixed toward the mean of the below/above
  albedo samples with strength 384*sh/1024/1024. Trace gains a PASS 3B
  block; decision count reads 270.
- b1/b1_k192.zag: identical except the frozen k constant is 192
  (data-amount trial, evidence only).
- b1/b1_verify.zag: frozen-bar verifier (KB3..KB6), pure Zag.
- b1/run_b1.sh: static checks, pins, compile, baseline hash gate,
  reruns, verifier, trace check.

## Frozen bar results (k384, the candidate)

| Bar | Frozen requirement | Measured | Verdict |
| KB1 determinism | two reruns byte-identical | var_r1 == var_r2 (sha256 equal), traces identical | PASS |
| KB2 cost | wall <= 1.55 s (1.5 x 1.03 s base) | 1.066 s vs 1.028 s base | PASS |
| KB3 anti-grain | HF(var) <= 1.02 x HF(base) | ratio 999/1000 | PASS |
| KB4a effect | mean per-channel delta >= 3.5 over sh>512 land px (n=141684) | 2.03 | FAIL |
| KB4b effect spread | >= 25% of those px with mean delta >= 3.5 | 17% | FAIL |
| KB4c effect cap | max per-px per-channel delta <= 80 | 17 | PASS |
| KB5 no flatten/crush | luma varnum >= 0.81 x base; crushed blacks not increased | ratio 99/100; 951 -> 951 | PASS |
| KB6 no new edges | max 4-neighbor delta-field gradient <= 8 | 14 | FAIL |
| KB7 trace | PASS 3B block present, count reads 270 | confirmed | PASS |

## Data-amount trial (k192, evidence only)

Mean delta 0.86 (KB4a FAIL), hit fraction 2% (KB4b FAIL), max delta 15
(KB4c PASS), HF ratio 999/1000 (KB3 PASS), luma varnum ratio 99/100 and
crush 951 -> 951 (KB5 PASS), max gradient 7 (KB6 PASS). Halving the mix
halves the effect and halves the gate-edge gradient (14 -> 7), which
confirms both are mechanism-caused, not noise.

## Killing evidence

1. KB4a/KB4b: the effect is a factor ~1.7 below the frozen floor
   (2.03 vs 3.5; 17% vs 25%). The bounce is real but sub-visible:
   side-by-side 2x crops of the arch shadow and rim shadow show no
   visible difference, consistent with a ~2/255 mean move.
2. KB6: the |delta| field has a max 4-neighbor gradient of 14 (> 8).
   The luma gate (>= 24) and the sky mask are hard on/off switches, so
   the change field has true discontinuities at gate boundaries. This
   is a D-COMP violation: a new edge class the substrate forbids.

Per the frozen verdict mapping (bars conjunctive, no PARTIAL
available): DISCARD.

## Post-mortem: why the consistency check was wrong

The prereg's analytic calibration predicted mean deltas of 3.1
(worst cell) to 14.4 using pure dab colors and forgot two facts about
the substrate: (a) pass 3 applies an aerial wash AFTER the shadow
scaling, pulling every shadowed pixel up to 210/1024 toward the dusty
horizon color (198,168,148), which compresses exactly the headroom the
bounce needs; (b) the pre-light canvas is a blend of many dabs, so
real albedos sit closer to the washed shadow color than any single dab
constant suggests. Lesson for future preregs: calibrate effect-size
bars against the actual base render's pixel statistics with a probe
program, never hand arithmetic on dab constants. This lesson does not
move the frozen bars; it explains the miss.

## Red-team note: knowledge vs architecture

Architecture, not a data gap. The substrate's light pass already
spends the shadow-color budget (flat cool fill plus aerial wash); any
post-pass recolor fights that wash and loses. A bounce mechanism with
real headroom would have to live INSIDE the light pass, replacing the
flat fill and wash rather than following them. That is a different
mechanism, needs its own prereg, and is not pursued this wave (one
candidate max; the stand-down on micro-levers is respected).

## Anomalies

None in the harness: toolchain pin held, substrate pin held, baseline
hash gate held, reruns byte-identical, verifier deterministic. The only
surprise was the candidate's own weakness, which the frozen bars
caught as designed.

## Verdict recommendation

DISCARD B1. Do not bank, do not queue, do not re-freeze this wave.
The evidence, sources, renders, and logs are committed below for the
sibling red-team review.
