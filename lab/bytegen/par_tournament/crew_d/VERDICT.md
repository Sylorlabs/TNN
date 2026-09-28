# CREW D — tournament VERDICT (frozen §6)

Coordinator round. Frozen prereg: `../par_dive/PREREG_PAR_DIVE.md` (§2 battery,
§5 red team, §6 adoption bars — the law). Contender prereg:
`../par_dive/contender_d/PREREG_D.md` (D1/D2) + D3 preregistered in this
round's `RUNLOG.md` BEFORE any D3 code existed. Pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Pure Zag,
zero RNG, byte-identical reruns proven by `cmp`/SHA.

NATIVE audio reference: `src/render_native` — rebuilt in this round from
`fork_par/src/render_par.zag` (source diff-identical across the old and
tnn-lab trees) with the pinned znc; the fresh binary is byte-identical to
both pre-existing builds (`render_par`, `render_par_fresh`). NATIVE's
RT-LONG is MEASURED DIRECTLY on this binary in this round — the dive's
disclosed caveat ("no native binary exists in the workspace") is CLOSED.

## §6 bar (frozen)

Overthrow on a path iff: ≥ all 9 quality bars, coherence ≥ NATIVE,
strictly better on ≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE,
COST} with no regression elsewhere, byte-identical reruns, survives §5
red team. A TIE keeps NATIVE. Verdicts per path; this crew builds audio
only — every other path is NOT TESTED.

## D1 MR-BIDI — audio: TIE (re-verified; incumbent keeps)

Every preregistered D1 claim re-verified through the full battery on the
rebuilt binary (source SHA `d6bcb99c…cff88`, unchanged from the dive):

| Leg | Result |
|---|---|
| DET | 4/4 renders SHA `1823f8fa82af3aca23c598b902c53a0df072315c84e7c5509b26625299427ca4` — the SAME sha as the dive's 2026-09-24 runs (cross-session reproducibility) |
| D1-C1 clean vs NATIVE | mix AND wav `cmp`-identical to NATIVE |
| Quality 9/9 | G-PER 0.340, G-STA 1.826, G-LURCH 2.362, G-DRIFT 480.284, G-FLUXm 241.824, G-SIL1 0.000, G-SIL2 0.000, G-CLIP 0.849, G-CREST 3.863 — identical to the dive and to NATIVE |
| CHOP (complete 271-event list) | CHOP-1 0 hard discontinuities; CHOP-2 no silent gaps ≥150 ms; CHOP-3 29 flux spikes, 0 unexplained |
| Coherence | zero-lag xcorr 1.000000; max-lag 1.000000 @ 0 samples; pitch-contour r 1.000000; IOI-contour r 1.000000 |
| RT-LONG | renders the nominal 880 (ZCR 842.5 Hz, −75c disclosed sensor bias) — PAR semantics, documented tie |
| RT-CASCADE frozen | 0 pre-cut / 64 in-window / 0 post-cut diffs |
| RT-EDGE frozen | wav bit-identical to NATIVE |
| Order permutation | seq == rev bit-identical |
| RT-CASCADE sustained | 82,688 diffs, 100% inside fault blocks, 0 outside (confinement baseline) |

D1's 15 s window-cut extension (outside the frozen battery — documented
bonus, re-verified at analyzer level in this round): the A/B excerpts
were re-rendered with the tournament binary (`excerpts/d1_boundary_fade.wav`,
`excerpts/d1_boundary_nofade.wav`, WITHHELD-NOT-FOR-REVIEW) and analyzed
by `tests/verify_d1_edgeAB.py`:
- E1 end transient: nofade ends mid-waveform (|last| = 0.3142 FS);
  fade ends at 0.0000 FS (5 ms raised-cosine release).
- E2 confinement: 214 fade/nofade diffs, all inside the declared
  220-sample region, 0 outside (214 < 220: integer truncation shortfall,
  as disclosed in the dive).
- E3 end slope: fade mean|d| 0.01480 FS vs nofade 0.02687 FS over the
  last 220 samples.
- E4: frozen CHOP-1 (0.35 FS single-sample threshold) still does not
  discriminate sub-0.35 end-steps (0/0) — the extension remains proven at
  the sample level, not the CHOP-1 level. The frozen RT-EDGE verdict is a tie
  by design. (§6: the extension is not a frozen axis — no overthrow.)
  (`results/d1_edgeAB.txt`)

§5 red team (§5 item: probe the backward pass for output→content
feedback smuggling): fault injection BETWEEN pass 2 and pass 3
(`tests/redteam_d1_pass3.py`, 15 s window so pass 3 fires, mode
`seq+susfaultmix` = render clean, XOR 64 samples per 1024-block, then run
pass 3 on the corrupted mix):
- T1 decision: `hardstop=1` in the faulted trace — 41,344 faults across
  the window cannot change the decision. Plan-determined, PASS.
- T2 diff-set: 41,344 diffs sus15-vs-clean15, ALL inside the KNOWN fault
  sample sets; 0 diffs elsewhere. The 220-sample fade region contains no
  faulted samples, yet all 220 of its samples are bit-identical between
  the faulted and clean renders — the fade gains are index-pure (any
  content-reactive gain — peak/RMS/DC — would have shifted under 41k
  faults). PASS: no output→content feedback.
- T3 gains: implied fade gains (clean15/nofade15, 20 positive-prefade
  samples) match the index-pure raised-cosine LUT formula reimplemented
  bit-exact in Python: 0 mismatches.
Conclusion: pass 3 reads the mix only as the destination of an
index-pure multiply; decisions come from the plan only. No smuggling.
(`results/d1_redteam_pass3.txt`)

**Verdict: TIE — NATIVE keeps audio on D1's account.** (Unchanged from
the dive; the extension stays a documented bonus outside §6.)

## D2 PLANREF — audio: OVERTHROW (caveat CLOSED by native measurement)

| Leg | Result |
|---|---|
| DET | 4/4 byte-identical (SHA in `results/d2_determinism.sha256`) |
| D2-C1 clean vs NATIVE | mix AND wav bit-identical to NATIVE |
| Quality / CHOP / coherence | identical to the D1 table (fixture output bit-identical to NATIVE) |
| RT-LONG original (nominal 880) | `LATCHED f0q=28835840` = 440×65536 exact → **0¢ honest error by construction** (ZCR vs proper 440 reference: 425.0 Hz, −60c disclosed bias; `results/d2_rtlong_orig_zcr440.txt` — the battery's generic leg passed 880 as the ZCR reference for all schemes, which is not D2's construction; the dedicated measurement is the honest one) |
| RT-LONG near-miss (nominal 460) | `LATCHED f0q=28835840` → **0¢** |
| NATIVE RT-LONG (measured this round on `render_native`) | original: renders nominal 880 → **1200¢** honest error vs true cue 440 (octave error); near-miss: renders nominal 460 → **76.96¢** vs true 440 (pitch error, no octave error). ZCR readings: 842.5 Hz vs 880 construction (−75c disclosed bias); near-miss reading in `results/native_rtlong_near.txt`. |
| RT-LONG honest-cents scoreboard | D2 **0¢ / 0¢** vs NATIVE **1200¢ / 76.96¢** — strictly better on both variants, measured, no presumption |
| RT-LONG multi-trap | e=4 (dyad) ABSTAIN code=1 → nominal; e=5 latch 440; e=6 latch 523.25 (`f0q=34291712` exact) |
| RT-CASCADE frozen | 0 / 64 / 0; latch still fires on plan_long with pre-cut-clean window |
| RT-CASCADE sustained | `ABSTAIN code=3` — no pitch hallucination |
| RT-EDGE frozen | wav bit-identical to NATIVE |
| Order permutation | seq == rev bit-identical |

§5 red team (re-run on the rebuilt binary + new provenance mapping):
- 5 adversarial plans (`results/d2_adversarial.txt`): emptywin ABSTAIN
  code=1; badwin ABSTAIN code=1; nomlie (`1e18` nominal) LATCHED
  f0q=28835840 — nominal ignored by design; chain: e=1 latch 440, e=2
  ABSTAIN code=1 (no latch-chaining); hugeamp: completes, latch fires
  (integrity gate survives deterministic wraparound on both sides). No
  hangs, no crashes.
- Sub-octave nominal lies: near-miss latches the cue's declared 440.
- **Plan-provenance boundary (mapped exactly):** D2 trusts the plan TEXT
  (cue EVENT fields incl. declared f0; the shared parser) and VERIFIES the
  cue audio == plan-pure re-render (gate 2). It has no sensor and no
  independent access to the trainer's intent. Demo `plans/plan_adv_f0lie.txt`
  (cue declares 466.16 — a plan typo for intended 440): D2 latches
  `f0q=30550261` = 466.16×65536 exactly — 0¢ vs the plan's declaration,
  99.99¢ vs the trainer's intent. **Cost of plan-provenance:** a
  lying/mistyped plan owns D2 completely; D2 cannot distinguish plan-typo
  from plan-truth. Safety is plan-provenance all the way down — the plan
  author is the trust root, and D2's honesty claim is honestly
  *relative*: "0¢ vs what the plan declares," never "0¢ vs the truth."
- Sustained 1292-block corruption: ABSTAIN code=3 on the latch; no
  hallucination; damage not healed (documented).

**Verdict: D2 OVERTHROWS NATIVE on audio.** 9/9 bars, coherence =
NATIVE (bit-identical fixture output), strictly better on RT-LONG
honest-cents (0¢/0¢ vs measured 1200¢/76.96¢) with no regression
elsewhere (every other leg ties NATIVE bit-identically), byte-identical
reruns, survives §5. The dive's caveat is closed: the comparison is now
against NATIVE measured directly on a pinned-toolchain native binary,
not against presumed reference behaviors.

Honesty notes (carried from the dive, still true): D2's "0 cents" is by
construction (the latched value IS the plan's declared Q16 f0), not by
measurement — the ZCR instrument reads −60c on D2's own 440 response,
disclosed in every result file. D2 is a plan cross-reference, not a
pitch meter; the prereg says so plainly. D2 defines RESPOND := echo the
cue's declared pitch; sub-octave nominal intent is overridden (the
frozen battery defines 460 as a lie, so this is correct-in-battery).

## D3 PLANHEAL — audio: PARTIAL WIN on extended RT-CASCADE (no §6 overthrow)

Preregistered in `RUNLOG.md` before any D3 code existed. Mechanism: PAR
render (phase 1, verbatim) + plan-pure audit in fixed 1024-sample blocks
+ restoration of differing blocks with plan-pure bytes (phase 2).

| Leg | Result |
|---|---|
| DET | 4/4 byte-identical |
| D3-C1 clean vs NATIVE | mix AND wav bit-identical to NATIVE (audit repaired 0 samples — provably no-ops clean); 9/9 bars, CHOP, coherence all tie NATIVE |
| RT-CASCADE frozen (64-sample XOR @3 s) | **0 pre / 0 in-window / 0 post diffs** — audit detected and restored the corrupted block (repaired 1024 samples: block-granular). PAR/D1/D2: 0 / 64 / 0 (damage confined but the 64 in-window samples stay corrupted). |
| RT-CASCADE extended — burst (4096 @10 s) | 0 diffs vs clean everywhere (repaired 5120 = 5 blocks) |
| RT-CASCADE extended — dropout (1024 zeroed @20 s) | 0 diffs vs clean (repaired 2048 = 2 blocks; the dropout straddles a block boundary) |
| RT-CASCADE extended — DC shift (+10000 over 8192 @5 s) | 0 diffs vs clean (repaired 9216 = 9 blocks) |
| RT-CASCADE sustained 1292-block | 0 diffs vs clean (repaired all 1,323,000 samples — full recovery where D1 confines 82,688 diffs) |
| RT-LONG | PAR semantics (renders nominal) — documented tie |
| RT-EDGE frozen | bit-identical to NATIVE |
| Order permutation | seq == rev bit-identical |
| D3-C5 COST | ~2× NATIVE wall-clock (the audit is a second full render) — DOCUMENTED TRADE |

§5 red team: sustained corruption between phase 1 and the audit →
full recovery, 0 diffs; faults straddling audit-block boundaries
(dropout case) → repaired; fault injection between the two phases shows
the audit reads the mix only to compare and writes only plan-pure bytes
— no output→content feedback (generation decisions never revisited).
Failure modes (preregistered): F1 blind to faults whose bytes
coincidentally equal plan-pure bytes; F2 a lying plan renders its lie
and the audit passes (trusts the plan like PAR — D2's provenance
boundary applies); F3 2× cost.

**Verdict: partial win — D3 strictly eliminates ALL damage (in-window
included) under the §2-mandated EXTENDED fault models where
confinement-only schemes (PAR/D1/D2) keep in-window damage; but the 2×
COST is a regression on a frozen axis, so per §6 this is NOT an
overthrow.** Reported as: damage-elimination win + cost trade, NATIVE keeps.

## COST (interleaved, same machine; 3 runs each, peak RSS via /proc VmHWM)

| Binary | wall s (run1 / run2 / run3) | median | peak RSS |
|---|---|---|---|
| render_native | 4.35 / 6.91 / 6.06 | 6.06 | ~13,032 KB |
| render_d1 | 3.61 / 5.86 / 5.96 | 5.86 | ~13,048 KB |
| render_d2 | 5.98 / 5.77 / 8.07 | 5.98 | ~13,048 KB |
| render_d3 | 7.52 / 13.45 / 15.31 | 13.45 | ~13,052 KB |

Raw: `results/cost_interleaved.txt`. Native/D1/D2 are indistinguishable
within VM noise (the dive saw the same); D3 median 13.45 / native 6.06 =
**2.22×** — the audit is a second full render, exactly the preregistered
trade. Peak RSS is identical across all four (~13 MB); the audit adds no
memory pressure.

## Path matrix

| Path | D1 | D2 | D3 |
|---|---|---|---|
| Audio | TIE | **OVERTHROW** (caveat closed) | PARTIAL (extended-cascade win, cost trade) |
| Video | NOT TESTED | NOT TESTED | NOT TESTED |
| Dialogue | NOT TESTED | NOT TESTED | NOT TESTED |
| Image | NOT TESTED | NOT TESTED | NOT TESTED |

## Excerpts (NEW renders, WITHHELD-NOT-FOR-REVIEW — never for Micah)

- `excerpts/d1_boundary_fade.wav` — 15 s phrase hard-cut at the render
  window, D1's 5 ms backward release (ends ~0.0 FS).
- `excerpts/d1_boundary_nofade.wav` — same phrase, PAR semantics (ends
  mid-waveform: the stop transient D1 removes). A/B pair.
- `excerpts/d2_planref.wav` — 4 s cut (`plans/plan_excerpt_d2.txt`): 440 Hz
  cue at 0.5–1.5 s, then the response at exact construction-440 where the
  plan's nominal lies (460).

## Honesty notes

- D3's repair is block-granular (1024 samples): "repaired" counts exceed
  fault sizes (1024/5120/2048/9216 for the four models). The restored
  bytes are exactly plan-pure — vs-clean diffs are 0 in all cases.
- The fixture's `659.25` 12-TET truncation note (dive) still applies to
  any formation work; not re-tested here.
- D2's overthrow is on the audio path only; the RT-LONG axis is where
  the plan-cross-reference design wins. Nothing in this round changes
  D2's documented failure modes (F1–F4, PREREG_D.md).
