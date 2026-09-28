# CRITIC 1 (anti-B-gate) — PREREGISTERED DESIGN + KILL BARS

Date: 2026-09-24. Author: CRITIC 1 (red team, anti-B-gate).
Frozen law: `docs/lab/bytegen/par_dive/PREREG_PAR_DIVE.md` (§2 battery,
§5 red team, §6 adoption bars). Pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Pure Zag. Zero RNG in all decision/render paths. Every binary output
byte-identical across reruns (proven by `cmp`/SHA-256).

**This prereg is written and committed BEFORE any experiment on the
contender below.** Baseline verification only (rebuilding B-gate from its
committed source and reproducing its recorded mix SHA) was done first to
ground the bars.

## 0. Baseline verification (champion's numbers, independently reproduced)

- B-gate source `docs/lab/bytegen/par_tournament/crew_b/src/render_b_gate.zag`
  rebuilt with the pinned toolchain → binary SHA
  `7d02dc052e377940d201b8e370b332088d1086c014d0e11ab7133867baf49585`
  — matches crew_b's recorded `7d02dc05…585` exactly.
- `./render_b_gate plan_v1.txt out.mix seqmix` → mix SHA
  `b7d3a71ebc9066b46a7c493a8cc0c8fe26fa017b22fcba4b2f4de49df9cd8784`
  — matches crew_b's recorded `b7d3a71e…8784` exactly.
- The champion's recorded §6 profile (the bars below) is taken as given
  from crew_b's VERDICT.md.

## 1. The anti-B-gate thesis (why B-gate is the wrong direction)

B-gate = B-fix (plan-seeded region state + release-envelope fix) + a
40–4000 Hz pitch gate (render-path clamp + latch vetoes). The envelope fix
is settled and kept. The other two components are the wrong direction:

1. **Region-carried state is unobservable machinery.** Every region's output
   is already a pure function of (plan, region index): state is wiped at
   every boundary and reseeded from plan-only data (chain-head
   re-simulation). The region mechanism contributes NOTHING to the output
   that a single flat timeline pass does not — it only adds an arbitrary
   3 s constant, per-region allocation churn, and prefix re-simulation that
   is QUADRATIC in the worst case (a legato chain crossing R region
   boundaries is re-simulated R times; a 60 s legato chain costs ~10.5× the
   audio duration in simulation). B is the slowest audio contender
   (LATENCY-1: 19.94 s on 60 s vs A 0.92 s) because of this machinery, not
   because of its synthesis math.
2. **The render-path pitch clamp is an arbitrary limit.** [40,4000] Hz at
   the synth silently rewrites hostile plans (EVENT 30 Hz → renders 40;
   EVENT 5000 Hz → renders 4000). The synth's true representable range is
   the parse rail [0,20000] Hz (grounded in i64 safety, not taste). Per
   Micah's standing no-arbitrary-limits law, the honest gate belongs at the
   DECISION layer (the RESPOND latch vetoes — kept verbatim); the synth
   layer renders the plan faithfully.

## 2. Contender F — "FLAT": the regionless renderer

**Design:** single flat pass over the time-sorted plan. No regions, no
reseeds, no prefix simulation. Phase/vibrato carried in locals across
legato chains (reset at non-legato event starts) — the IDENTICAL recurrence
B's region simulation computes, so the output is IDENTICAL. Per-sample
synthesis math identical to B-gate (B-fix envelope, voice_sample harmonic
stack, portamento, glide, vibrato, bed). `parse_plan`, `build_chains`
(legato detection is plan-derived), and `respond_latch` (the trap defenses
live there) kept verbatim. Overlays still closed-form (`voice_closed`).
Bed single-pass from b0.

**Two deliberate differences from B-gate (preregistered, not regressions):**
- (a) No `gate_f` [40,4000] clamp on the RENDER path or in `endpitch`:
  the synth renders plan pitches faithfully within the parse rails
  [0,20000] Hz. The latch's nominal/output vetoes are UNCHANGED (decision
  layer). On the frozen fixture (all pitches in [110,880]) this is a no-op.
- (b) Strength-reduction of provably-non-negative power-of-two divisions
  to shifts in the hot loop (`(x*h)/4194304` → `(x*h)>>22`, exact for
  x ≥ 0; applied only where the operand is provably non-negative:
  post-fixup phase and wrap32'd vibrato phase). Bit-identical integer math;
  defeats the case where the toolchain emits `idiv` for `/4194304`.

**Falsifiable core claim:** F's mix output on the frozen fixture is
BYTE-IDENTICAL to B-gate's (SHA `b7d3a71e…8784`, `cmp` clean). If the
recurrence is reproduced exactly, every §6 number follows by construction.

## 3. Preregistered kill bars (overthrow iff ALL hold)

Frozen §6 rule: ≥ all 9 quality bars, coherence ≥ champion, strictly better
on ≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE, COST} with no
regression elsewhere, byte-identical reruns, survives §5 red team.

| # | Bar | Target (champion's number) |
|---|---|---|
| B1 | Fixture mix byte-identical to B-gate | `cmp` clean; SHA `b7d3a71e…8784` |
| B2 | 9/9 quality gates (gate_bin on F's WAV) | G-PER 0.324 (≤0.350), G-STA 1.841, G-LURCH 2.373, G-DRIFT 383.553 (≤800), G-FLUXm 213.116 (≤350), G-SIL1/2 0.000, G-CLIP 0.915, G-CREST 3.860 — identical to B-gate |
| B3 | CHOP-1/2/3 (events_complete.txt) | 0 / NONE / 16 spikes, 0 unexplained |
| B4 | Coherence | xcorr 1.000000 zero-lag; pitch/IOI contour r 1.000000 |
| B5 | DET | 20/20 reruns byte-identical; binary SHA pinned |
| B6 | RT-LONG | 440.00 Hz +0.00¢; near-miss 460 stands |
| B7 | RT-CASCADE | 1 diff @ fault sample, 0 post-cut (1-bit); 0 post-cut on burst/dropout/DC |
| B8 | RT-EDGE | 0 pre-14.8 s diffs; cut step 0 (16-bit units); bed fades to exactly 0 |
| B9 | Plan-order permutation | events in shuffled text order → byte-identical mix (R1-analogue: no order dependence) |
| B10 | **COST (the strictly-better axis)** | strictly faster than B-gate, same machine, interleaved, same mode; target ≥1.5× on the 30 s fixture |
| B11 | Scaling (supports B10) | on a 60 s long-legato-chain plan: F renders in O(T); B-gate's prefix re-simulation exhibits its quadratic blowup — measured, not claimed |
| B12 | Trap battery — latch defenses | cue30/nom880 → 880; cue5000/nom880 → 880; cue440/nom30 → GATE-VETO(nominal); cue440/nom5000 → GATE-VETO(nominal); cue4000/nom40 → GATE-VETO(output); R5 sub-octave lies corrected — ALL identical to B-gate |
| B13 | Trap battery — preregistered render differences | EVENT 30 Hz → renders **30** (B-gate: 40); EVENT 5000 Hz → renders **5000** (B-gate: 4000). Plan-faithful synth by design (§1.2); the vetoes in B12 are the real defense |
| B14 | §5 red team | R1-analogue: B9 + B8 pre-cut identity (causality: no future dependence); R2: 1292-block sustained corruption → 0 diffs rerender-vs-clean (F never reads the mix); R3: 14 fz plans rc=0, no hangs, bounded peaks; R4: polyphonic RESPOND abstains; R5: sub-octave latch corrects |
| B15 | Forensics (600 s drift probe) | identical motifs 300 s apart → byte-identical windows (no long-horizon drift by construction) |
| B16 | Hygiene | zero RNG; pinned toolchain; byte-identical reruns (B5) |

**Overthrow rule:** F overthrows B-gate iff B1–B16 ALL hold. B10 is the
strictly-better axis (RT-LONG/B7/B8 are already at their theoretical optimum
for B-gate and cannot be beaten — only matched). If B1 fails after genuine
debugging, F fails as an overthrow (documented). If B10 fails (no measured
cost win) but B1–B9/B12/B14 hold, the verdict is TIE → B-gate keeps the
ship-candidate status, and F stands as documented proof that the region
machinery is unobservable dead weight.

## 4. Battery plan (same fixtures/methods as crew_b)

- Fixture `bytegen/fixture/plan_v1.txt`; mix-level comparisons (`seqmix`);
  WAV via `seq` for gate_bin/CHOP/coherence.
- Trap plans + lie battery plans + leak plans + plan_edge15.txt from
  `docs/lab/bytegen/par_tournament/crew_b/plans/`; R3 fz corpus from
  `par_dive/redteam/plans/`; `tests/coherence_full.py`,
  `tests/postcut_diff.py`, `tests/events_complete.txt` from crew_b/tests;
  `~/workspace/aud_v10/chop.py`; gate_bin from
  `imagination_discovery/aud/b_alpha/consistency_gate/src/gate_bin`.
- COST: interleaved B-gate/F runs on this VM, same mode, N≥5 each; plus
  the 60 s scaling probe.

## 5. What failure looks like (pre-committed)

- B1 fails and the recurrence cannot be made exact → F is not a valid
  overthrow; VERDICT.md documents the exact sample divergence and why.
- B10 fails (F not strictly faster) → TIE; B-gate keeps its status; the
  region-machinery critique stands as analysis, not as an overthrow.
- Any B2–B9/B12/B14 regression vs B-gate → investigate; if unfixable without
  changing the design, F fails (documented).
- Genuine failure after genuine attempts still raises confidence in B-gate
  and is recorded as a win for the tournament.
