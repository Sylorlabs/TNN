# Contender D — RESULTS

Frozen prereg: `../PREREG_PAR_DIVE.md` (read 2026-09-24). Contender prereg:
`PREREG_D.md` (written before any build). Pinned toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG anywhere. All renders below observed 2026-09-24.

Source SHAs (final, post sustained-mode addition to D1):
- `src/render_d1.zag` `d6bcb99c0d1c1b211fcd6ba495656435856e22db3f72b1a80ed35dbe7f3cff88`
- `src/render_d2.zag` `5199cd1d071d784538df011d9f2392e8fa852c5ea50229cbe2787efe8f3bebdd`

Battery runner: `tests/run_battery.sh` (log: `runs/battery.log`, rc=0).

## D1 MR-BIDI (multi-resolution bidirectional)

| Claim | Result |
|---|---|
| D1-C1 clean mix bit-identical to PAR | VERIFIED (`cmp` mix and wav; re-verified after final rebuild) |
| D1-C2 frozen RT-EDGE ties PAR | VERIFIED (edge wav `cmp`-identical to PAR) |
| D1-C4 seq == rev bit-identical | VERIFIED (pre- and post-rebuild) |
| DET byte-identical reruns | VERIFIED — 4 renders, SHA `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4` ×4 |
| Quality 9/9 | PASS: G-PER 0.340, G-STA 1.826, G-LURCH 2.362, G-DRIFT 480.284, G-FLUXm 241.824, G-SIL1 0.000, G-SIL2 0.000, G-CLIP 0.849, G-CREST 3.863 (identical to PAR baseline) |
| CHOP (complete 271-event list `tests/events_full.txt`) | CHOP-1 0 hard discontinuities; CHOP-2 no silent gaps ≥150 ms; CHOP-3 29 flux spikes, 0 unexplained |
| Coherence decomposition | zero-lag xcorr 1.000000; max-lag xcorr 1.000000 @ 0 samples; pitch-contour r 1.000000; IOI-contour r 1.000000 (plan-derived onsets; audio onset detector degenerate on this legato motif — documented in `tests/coherence_full.py`) |
| RT-LONG | renders the nominal 880 (1200c error) — PAR semantics, documented tie as preregistered |
| RT-CASCADE single 64-sample cut @3 s | 0 pre-cut / 64 in-window / 0 post-cut diffs |
| RT-CASCADE sustained 1292-block | 82,688 diffs, ALL inside fault blocks, 0 outside — damage confinement at scale |
| COST (interleaved, wall s) | PAR 15.14/14.57/6.66, D1 16.14/13.28/13.42, D2 10.03/14.42/11.22 — VM-noise-dominated; medians PAR 14.57 / D1 13.42 / D2 11.22, no measurable difference, no regression. Peak RSS unmeasurable on this box (`/usr/bin/time` absent); allocation profile is PAR-identical (same `nio_alloc` sizes; D1 adds nothing). |

### D1 extension (outside frozen §2 — labeled as such)
15 s render-window cut on unclipped plans (`plans/plan_edge_midnote.txt`,
`plans/plan_edge_loud.txt`, excerpt plan `plans/plan_excerpt_d1.txt`):
pass 1 prints `hardstop=1`; the backward 220-sample raised-cosine release
fires only then. Sample evidence: nofade (PAR semantics) ends mid-waveform at
0.247 / 0.259 / 0.314 FS (audible stop transient); D1 ends at 0.0 FS.
Fade/nofade diffs confined to the declared 220-sample region (219–214 samples
differ; the 1-sample shortfall is integer truncation in the fade multiply —
documented, confined). Frozen CHOP-1 (0.35 FS single-sample threshold) does not
discriminate sub-0.35 end-steps — the extension is proven at the sample level,
not the CHOP-1 level. The frozen RT-EDGE verdict remains a tie by design.

## D2 PLANREF (plan-cross-referenced response)

| Claim | Result |
|---|---|
| D2-C1 clean mix bit-identical to PAR | VERIFIED (`cmp` mix and wav) |
| D2-C2 original RT-LONG | VERIFIED — trace `D2 RESPOND e=1 cue=0 LATCHED f0q=28835840` = 440×65536 exactly → **0c honest error by construction** (ties hybrid v2's latch on this case) |
| D2-C3 near-miss RT-LONG (nominal 460) | VERIFIED — `LATCHED f0q=28835840` → **0c** vs hybrid's abstain-to-nominal 76.7c. ZCR on the rendered 440: 425 Hz (−60c sensor bias, disclosed — the 0c claim is construction-exact, never a sensor reading) |
| D2-C4 multi-trap | VERIFIED — e=4 (dyad) `ABSTAIN code=1`; e=5 (single 440) latch 440; e=6 (single 523.25) latch `f0q=34291712` = 523.25×65536 exact |
| D2-C5 sustained 1292-block corruption | VERIFIED — `ABSTAIN code=3` (cue window ≠ plan-pure re-render); no pitch hallucination |
| DET byte-identical reruns | VERIFIED — 4 renders, SHA `1823f8fa…` ×4 (same as D1: identical fixture output) |
| Quality / CHOP / coherence | identical to D1 table above (fixture output bit-identical to PAR) |
| RT-CASCADE single cut | 0 / 64 / 0; latch still fires on plan_long under `faultmix` (window pre-cut is clean) |
| RT-EDGE frozen | wav bit-identical to PAR |
| Order permutation | seq == rev bit-identical |

## Formation parallelism (§4 prototype)

`formation/expand_motif.py`: MOTIF-A expanded two ways — per-index parallel
vs carried-state sequential — produce **byte-identical** plan text
(sha256 `4f3de2b9cef6852c4b1d9b089545b30b77a7effabf2ff98c7e274450edba9ee6`
both). The carried time state is redundant (`t = base + i·step`).
Forensic note: the fixture's `659.25` is 12-TET-**truncated**, not rounded
(440·2^(7/12) = 659.255… → rounds to 659.26); a formation scheme must reproduce
the frozen text's truncation to match byte-identically.

## Excerpts (NEW, for Micah's ears)

- `excerpts/d1_boundary_fade.wav` — 15 s musical phrase hard-cut at the render
  window; D1's 5 ms backward release applied (ends at 0.0 FS).
- `excerpts/d1_boundary_nofade.wav` — same phrase, PAR semantics (ends at
  0.314 FS mid-waveform: the stop transient D1 removes). A/B pair.
- `excerpts/d2_planref.wav` — 4 s cut of the near-miss RT-LONG: 440 Hz cue,
  then the response at exact construction-440 where the plan's nominal lies
  (460). D2's honest-cents behavior, audible.
