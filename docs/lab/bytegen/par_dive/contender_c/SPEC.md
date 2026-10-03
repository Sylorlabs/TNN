# Contender C — bounded-feedback AR (Grok H3): specification

Frozen law: `bytegen/par_dive/PREREG_PAR_DIVE.md` §1 contender C, §2 battery,
§5 red team, §6 adoption. Design grounding: `bytegen/grok47/ATTACKS.md`
Attacks 9 (bounded continuous feedback) and 11 (discrete plan-level latch).

## 1. What C is

C renders the frozen fixture plan (`bytegen/fixture/plan_v1.txt`, 30 s /
44.1 kHz / mono) with the verbatim PAR synthesis core (`voice_q16`,
`bed_q16` — the v2 hybrid's piece 1, bit-exact), plus two bounded feedback
mechanisms that the v2 hybrid's AR servo attempted and that hybrid-v2's
deletion removed. C repairs the servo per H3 instead of deleting it:

- **Piece 2 — region-scoped continuous servo.** A per-block gain `g`
  multiplies the plan-pure block render as a uniform scalar. The target is
  plan-derived, never a frozen literal: `T = K_PLAN × plan_rms_raw(block)`
  with `K_PLAN = 49585` (Q16), where `plan_rms_raw` is the analytic RMS of
  the plan content in the block (voice envelope model + bed, including the
  bed's 25 ms edge fade). Update (outside a 10 % model-error deadband):
  `g_next = (g + g·T/m)/2`, `m` = measured block RMS, clamped to
  `[0.5, 2.0]`. Because the gain is a uniform post-render scalar,
  `m = g·S` exactly (`S` = plan-pure block RMS), so for a stationary target
  `g_{n+1} = (g_n + T/S)/2` — a contraction with factor 1/2 toward `T/S`
  (Banach: unique fixed point, no 2-cycles; the deadband parks the orbit
  inside ±10 %; the clamp is a projection onto a convex set).
- **Piece 3 — RESPOND as a discrete plan-level octave latch.** One-shot per
  RESPOND event, gated: the cue window `[rt0−1 s, rt0)` must contain exactly
  one voice (`nvoice == 1`), the two ZCR halves must agree (stationarity),
  and the measured frequency must be in 40–4000 Hz. If the measurement
  disagrees with the plan nominal by more than half an octave, the latch
  corrects by octaves only: `f0 = nominal × 2^k`, `k = round(log2(fm/nom))`.
  Otherwise the nominal is kept. The latch NEVER mutates the plan: the
  corrected execution pitch is a renderer-local annotation in a separate
  `ovr` arena (one i64 per event, 0 = no override); `voice_q16` consults it
  via an `f0ov` parameter. Event existence, timing, kind, and the stored
  nominal pitch are untouched, and the servo is forbidden from pitch
  adjustment entirely (it may touch gain/timbre execution parameters only).

## 2. Regions and boundary reset

Regions are plan-defined: a gap of ≥ 0.5 s with no EVENT activity starts a
new region (RESPOND excluded — it is a control event, not content). Fixture
region starts (samples): `0, 88200, 264600, 418950, 705600, 1058400`
(6 regions). At each region boundary the servo gain resets to Q16 unity
(`65536`); no gain, veto, or latch state crosses a region. The RESPOND latch
fires before the block containing the RESPOND's cue window renders; the
override applies from that block onward within the run.

## 3. Corruption veto (measurement hygiene, not content repair)

If the measured block RMS `m` disagrees with the analytic plan RMS `S`
beyond the veto gate, the block is re-rendered plan-pure into a temporary
buffer and `m` is remeasured there with the exact same per-sample integer
arithmetic as the clean path; the servo updates from the remeasured value.
Corrupted output bytes stay corrupted — only servo state is protected. The
veto is what makes RT-CASCADE report 0 post-cut diffs and the sustained
1292-block attack leave the gain trajectory bit-identical to clean.

## 4. Silence definition

Silence is defined by the PLAN target (`T < SILENCE_FLOOR`), not by measured
output: in plan-silence blocks the gain is held (no update), which prevents
noise-floor chasing and rail pinning. Region boundaries still reset.

## 5. Modes

`seq` (WAV), `seqmix` (raw mix), `fault`/`faultmix` (64-sample XOR @ t=3 s),
`susfault`/`susfaultmix` (every block corrupted), `sus1292`/`sus1292mix`
(exactly 1292 flat 1024-sample blocks corrupted — the frozen §5 attack),
`sus5`/`sus5mix` (first 5 s corrupted, then clean — the settling test),
`dropout`/`dropoutmix` (full-block zero @ t=3 s).

## 6. Build and determinism

Pure Zag, pinned compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG in
the render path. Two renders of the fixture are byte-identical (`cmp`
clean at mix and WAV level). Source SHA-256 (2026-09-24 final):
`0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db`.

## 7. Compliance notes

- No plan mutation: after parsing, the plan arena is never written (verified
  by inspection — zero post-parse `evs` calls; the old latch's
  `evs(ev,e,2,f0)` / `evs(ev,e,8,0)` and the dead hybrid `render_events`
  path were removed 2026-09-24 and replaced by the `ovr` arena).
- The servo adjusts gain only — never event existence, timing, or pitch.
- Targets are plan-derived per block (`K_PLAN × plan_rms_raw`), never
  frozen literals.
- Known approximation: the analytic target uses the plan NOMINAL pitch for
  the voice envelope model, not a latched override pitch (RMS-level effect
  only, inside the deadband).
