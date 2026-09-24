# Crew SERVO — VERDICT (PAR tournament, 2026-09-24)

**Recommended servo law: the primary necessity gate (C-gated).**
Micah's criterion — "I don't want choppiness when unnecessary" — is met:
on a correct plan the gate kills 97% of servo adapts (137→4) and 96% of gain
movement (9.80→0.36 FS) while keeping 100% of the reproducible wins
(octave-latch RT-LONG correction, always-on veto, chord/drift behavior).

Recovery note: the first crew finished all experiments but shut down without
writing this verdict or committing. As recovery crew I re-verified everything
below from rebuilt sources/binaries (details §8). One design amendment was
applied during recovery (silence breaks open-persistence, §8.3); all numbers
below are from the amended final build unless marked v1.

## 1. The envelope answer: exactly when the servo helps vs adds choppiness

Head-to-head, 4 builds × 15 scenarios, fresh binaries from regenerated
sources (pinned toolchain `znc_linux_x86_64_abed8aa1`, pure Zag, zero RNG).
`a`=adapts, `v`=vetoes, `dsum`=Σ|Δg| in FS units, `eng`=engagement fraction.

| scenario | stock a/v/dsum/eng | gated a/v/dsum/eng | gfable a/v/dsum/eng | off |
|---|---|---|---|---|
| a_nominal (plan correct) | 137/0/9.80/0.106 | **4/0/0.36/0.003** | 10/0/0.70/0.008 | 0/0/0 |
| b_rtlong_octlie | 9/0/0.77/0.007 | 0/0/0/0 | 0/0/0/0 | 0 |
| c_nearmiss460 | 9/0/0.71/0.007 | 0/0/0/0 | 0/0/0/0 | 0 |
| d_suboct | 9/0/0.77/0.007 | 0/0/0/0 | 0/0/0/0 | 0 |
| e_2oct | 10/0/0.77/0.008 | 0/0/0/0 | 0/0/0/0 | 0 |
| f_vibtort | 10/0/0.80/0.008 | 0/0/0/0 | 0/0/0/0 | 0 |
| f_glide | 10/0/0.78/0.008 | 0/0/0/0 | 0/0/0/0 | 0 |
| g_chord16 (N=16 dense) | 2/0/0.05/0.002 | 0/0/0/0 | 1/0/0/0.001 | 0 |
| h_sus1292 (1292-block corruption) | 0/1295/9.80/1.0 | 0/1295/0/1.0 | 0/1295/0/1.0 | 0 |
| i_rail1/rail2 (adversarial text) | 5/7 /0.32/0.54 | 0/0/0/0 | 0/0/0/0 | 0 |
| drift (440→430 Hz over 950 blocks) | 6/0/0.51/0.005 | 0/0/0/0 | 0/0/0/0 | 0 |
| flap (440/465 Hz every 12 blocks) | 2/0/0.14/0.002 | 0/0/0/0 | 0/0/0/0 | 0 |
| sawbomb (veto-edge attack) | 564/0/86.75/0.436 | **4/18/0.36/0.017** | 10/18/0.70/0.022 | 0 |
| edge14 (+14% sustained) | 140/0/9.92/0.108 | 4/0/0.36/0.003 | 10/0/0.70/0.008 | 0 |

Reading:
- **The servo helps nowhere on correct plans.** On the fixture-correct plan
  (a), stock's 137 adapts are pure model-error hunting (±9% at vibrato
  extrema / attack-release transients); the latch never fires. The gate
  removes 133 of 137 (the 4 survivors are real >15%×3 runs at region 1/5
  attack transients, rb=118–129 — genuine measured deviation, kept by design).
- **RT-LONG correction is the piece-3 latch, not the servo.** The 9–10 stock
  adapts on (b)–(f) are region-start/model-error transients; gated renders
  0 adapts while the latch fires identically (`k=-1/+1/-2` on b/d/e,
  abstain `rsn=1` on f_glide, nominal `rsn=3` on c_nearmiss460 — confirmed by
  grep on all four builds' fresh logs). Pitch trigger correctly N/A for a
  gain servo (SPEC §1).
- **The gate defeats the veto-edge attack.** sawbomb alternates ×2.38/×1.05
  rendered amplitude (2.38 sits just under the 2.5 veto line): stock adapts
  564 times chasing garbage (86.75 FS of wobble, engagement 0.436). Gated:
  the sawtooth never sustains dev>15% for 3 consecutive blocks → gate stays
  closed; 18 blocks that do hit the veto band are vetoed (hygiene intact);
  4 residual adapts + 0.36 FS — a 25× engagement kill.
- **edge14 documents the deliberate blind spot.** A sustained +14% fault is
  just under X=15: stock adapts 140× (14>10 deadband), the gate ignores it
  (4 residual adapts only). This is the preregistered residual-blindness
  tradeoff — same family as stock's own 10% deadband blindness. A threshold
  must sit somewhere; 15% sits above the measured model-error floor
  (p90=10.3%, 27 isolated singles, zero runs ≥3) and below the veto band.
- **drift/flap: the gate stays shut, correctly.** The H3 servo is gain-only;
  a 440→430 Hz drift changes nothing in RMS (stock's 6 adapts were hunting
  transients at the snap, not the drift). fable's predicted "10-block
  correction transient" assumed a pitch servo — measurement says the plan
  IS the drift; there is nothing to correct. v1's one flap false-open
  (gate OPEN rg=1 rb=356) was a silence-bridging defect, fixed by amendment
  S1 (§8.3); v2 flap: 0 adapts, gate never opens, mix byte-identical to off.
- **g_chord16: no preventive limiting exists to pre-engage.** Stock parks
  after one −0.6 dB step (2 adapts, 0.05 FS); gated never opens (0 adapts).
  Mix RMS(2–5 s)=0.825 FS, peak=2.98 FS preserved — the bar is match-stock,
  not the dive's 0.54 (that number was FORK_AR's old v2-hybrid servo, which
  touched gain AND timbre; misattributed in the task background).

## 2. The recommended servo law (exact values)

```
OPEN:   dev = |T−m|·100/max(T,m) > X=15%  for Z=3 CONSECUTIVE
        non-silence, non-vetoed blocks        (69.6 ms persistence)
CLOSE:  dev < 10% (the stock deadband) for 10 consecutive blocks
        (1/2-contraction ⇒ 1024× error reduction; anti-flap)
WHILE OPEN:   stock update law UNCHANGED — g←(g+g·T/m)/2,
              clamp [0.5,2.0], 10% deadband parks inside
WHILE CLOSED: gain frozen (no adapt)
ALWAYS:  region-boundary reset to unity · silence-hold (T<SILENCE_FLOOR → st=3,
         gain held, never chased to the rail) · VETO always-on (unchanged)
VETOED blocks: neither increment nor reset the open/clear counters
SILENCE blocks: reset the open-persistence counter (amendment S1 — silence
         is not evidence of sustained deviation)
PITCH trigger: N/A — SPEC §1 forbids servo pitch adjustment; the piece-3
         latch owns pitch correction and is untouched in all builds
```

Threshold grounding (not magic numbers — standing law): X=15% is above the
measured model-error floor (p90=10.3%, max isolated 25.8%, zero runs ≥3) and
below the veto band (2.5×); Z=3 filters the 27 isolated transient singles
seen on the fixture; the 10-block close is the contraction horizon. All three
come from the Step-2 envelope sweep, not from taste.

## 3. Red-team results (fable's adversarial plans + gate red team)

- **sawbomb** (veto-edge, §1 table): gate defeats it — 564→4 adapts,
  86.75→0.36 FS. Fable predicted "no stock-vs-gated difference"; the veto
  band edge said otherwise; measurement decides — the gate wins.
- **edge14** (deadband exploitation, +14% sustained): deliberately ignored
  (4 residual adapts, same as nominal). Blind spot documented, not a bug.
- **flap** (spurious-open): v1 false-opened once (silence froze gopen across
  a gap, bridging two marginal transient runs into 3 increments). Amendment
  S1 (silence resets gopen) kills it: v2 flap 0 adapts, mix byte-identical
  to servo-off. The prereg's "3 CONSECUTIVE non-silence blocks" is now
  literally true.
- **drift**: gate closed throughout; output == servo-off (byte-identical
  mix). Correct: a gain servo must not "correct" a pitch drift that the
  plan itself contains.
- **amplitude-flap variant** (Step-6b, planned): 4-block ±30% RMS runs WOULD
  legitimately open the gate (4 consecutive >15%) — the hysteresis cost on
  pathological plans is documented by construction; not run as a separate
  leg since flap+v2 already characterizes the open/close dynamics.

## 4. Veto / sus1292 — honest divergence from the prereg prediction

- Veto behavior is gate-independent: 1295/1295 vetoes on h_sus1292 in
  stock, gated, and gfable. Measurement hygiene intact.
- The prereg's Step-3a prediction ("gated trajectory bit-identical to
  stock-clean") was garbled; the measurement is: stock's veto re-measures
  plan-pure and replays the FULL clean-hunting trajectory bit-exactly
  (gain trace identical clean-vs-sus1292, 1295/1295 blocks; 9.80 FS), while
  gated — whose vetoed blocks are invisible to the gate by explicit prereg
  rule — parks at unity (dsum 0.00, all-unity gain). The mixes differ only
  by the corrupted output bytes, which H3 never heals by design.
- This is the gate working as intended, not a regression: under sustained
  measurement corruption the servo adds nothing and renders plan-pure,
  instead of replaying 9.80 FS of gratuitous hunting. The stock "win" that
  matters (corruption fully absorbed, servo state protected, no wobble)
  is kept.
- Follow-up (NOT implemented — would be a new design decision, flagged for
  Micah/coordinator): feed the veto's re-measured (bit-exact clean) dev
  into the gate FSM instead of skipping vetoed blocks. Predicted effect:
  gated-sus5 post-cut diffs 43338→0 (bit-identity with gated-clean).
  Rejected for now as injecting synthetic evidence into the gate; the
  current rule ("vetoed blocks are not evidence") is the preregistered one.

## 5. Wall-clock honesty

Mean wall over the 15 legs: stock 12.2 s, gated 11.5 s, gfable 11.1 s,
off 10.7 s — no systematic win, all within VM noise. Expected: the gate
does not skip analyze()/plan_rms_raw(); gating is not a wall-clock
optimization. The honest metric is engagement fraction (§1): 34× kill on
nominal, 25× on sawbomb, ∞ (→0) on the RT-LONG family/drift/flap.

## 6. Frozen battery on the winner (gated, fresh build)

| bar | gated | stock-C reference | verdict |
|---|---|---|---|
| DET (2× rerun) | cmp clean | cmp clean | PASS |
| G-PER | 0.350 (bar 0.350) | 0.333 | PASS (at the bar — noted) |
| G-STA | 1.816 (3.0) | 2.020 | PASS |
| G-LURCH | 2.352 (5.0) | 2.518 | PASS |
| G-DRIFT | 479.724 (800) | 477.143 | PASS |
| G-FLUXm | 241.815 (350) | 242.649 | PASS |
| G-SIL1/G-SIL2 | 0.000/0.000 | 0.000/0.000 | PASS |
| G-CLIP | 0.850 (0.950) | 0.849 | PASS |
| G-CREST | 3.985 (14) | 4.324 | PASS |
| CHOP-1/2 | 0 / none | 0 / none | PASS |
| CHOP-3 | 32 total, 0 unexplained | 41 total, 0 unexplained | PASS |
| COHERENCE (motif 2.0–5.4 vs 24.0–27.4 s) | windows byte-identical; xcorr 1.0000000000 @ lag 0 | 1.000000/0.999999 | PASS |
| RT-CASCADE single fault @3 s | 64 in-block diffs, **0 post** | 0 post | PASS |
| RT-CASCADE dropout @3 s | 136 post diffs | 136 post (identical) | PASS (same as stock) |
| RT-CASCADE sus5 (5 s storm) | 43338 post diffs, bounded 55-block missed-adapt window, re-converges, no 2-cycle | 0 post | DIVERGENCE — see §4 |
| RT-EDGE (trunc @15 s) | first diff 14.975 s (bed edge fade, legitimate); 0 before 14.9 s | identical | PASS |
| RT-LONG (octave lie → 440) | 440.00 Hz, +0.0¢ | 440.00 Hz | PASS (all 4 builds) |

Notes: G-PER sits exactly at its bar (0.350 ≤ 0.350 PASS) — the 4 residual
adapts move it from stock's 0.333; worth watching, not a failure. CHOP-3
drops 41→32 total spikes (all event-explained): killing gratuitous adapts
removes flux spikes rather than adding them — consistent with the gate's
purpose. (C-CAVEAT owns the 41-vs-29 spike-count question; this is the
frozen battery re-run, not their ablation experiment.)

## 7. Phase continuity (fable Q2) — all four builds

`|φ_end(n) − φ_start(n+1)|` vs expected advance, >0.2 rad unexplained =
flag. All four builds flag the SAME 18 boundaries (md5-identical flag
lists) at plan note onsets (ZCR f0-estimator confusion, e.g. block 298
t=6.94 s err=3.092 rad f1=400.9/f2=300.7) — plan-content artifacts, not
servo artifacts. **Build-attributable unexplained phase jump: 0 on all
four builds.** A uniform block gain cannot change phase; confirmed.

## 8. gfable (fable two-tier) vs primary gate — WINNER: PRIMARY

| metric | gated (primary) | gfable (fable R1) |
|---|---|---|
| nominal adapts/dsum | **4 / 0.36** | 10 / 0.70 |
| nominal gate-open frac | 0.017 | 0.049 |
| sawbomb adapts/dsum | **4 / 0.36** (+18 vetoes) | 10 / 0.70 (+18 vetoes) |
| edge14 adapts/dsum | **4 / 0.36** | 10 / 0.70 |
| g_chord16 | **0 adapts** (never opens) | 1 adapt (tier-1a PRE-OPEN) |
| flap/drift/RT-LONG | identical (0) | identical (0) |
| latch/veto | identical | identical |

Fable's tier-2 (20-block minimum-active OR clear+10 grace) keeps the gate
open ~2× longer at every opening (CLOSED rb=150 vs 129) for ~2.5× the
adapts with zero benefit — the stock law has no preventive limiting to
sustain. Tier-1a pre-engage on the dense chord (N≥4 AND sum>0.7 FS) fires
once and the law parks after a single step (1 adapt, dsum 0.00): the
"preventive headroom" hypothesis is falsified for the H3 gain-only law —
there is nothing preventive to pre-engage. **The primary gate wins on
every scenario; gfable is rejected.**

## 9. Recovery appendix (what the first crew left, what I changed)

Inherited: RUNLOG.md through Step 5's plan (log empty), four variant
sources (16:50), four binaries (16:20), work/h2h.json + 60 logs/mixes
(16:23–17:00), work/phase_cont.py, tests/plan_drift.txt + plan_flap.txt.

1. **gen_variants.py was broken** (17:29 edit): `add_common()` called before
   definition (NameError) + double-application of the common edits on the
   off/gated/gfable chains (anchor assert would fail). Fixed by defining a
   pristine `base` and applying `add_common(base)` per variant; all four
   sources now regenerate byte-identically from frozen
   (`0640f28f…`) + the script. stock/off regenerated exactly; gated/gfable
   differ by exactly the S1 line below.
2. **Amendment S1** (was in the broken script, never built): silence blocks
   reset the open-persistence counter (`gopen = 0; // silence is not
   evidence`). Rationale documented in-script: v1's flap false-open came
   from a silence block freezing gopen across a gap. Post-prereg change,
   applied during recovery because it was the crew's clear documented intent
   and it fixes a measured defect. v1 outputs archived under
   work/v1_superseded/ (not committed).
3. **Rebuilt all four binaries** with the pinned toolchain (analyzer
   warnings only, as before). stock/off binaries reproduce byte-identically
   (SHA match with the 16:20 builds); gated/gfable differ only by S1.
4. **Re-ran the full 4×15 h2h** with fresh binaries (the old h2h.json is
   superseded; stock's numbers reproduce v1 exactly: 137/9.80 nominal,
   564/86.75 sawbomb, 140/9.92 edge14).
5. Verified: DET (stock 2× cmp clean; gated h2h==smoke cmp clean),
   latch lines on all builds, gated-vs-off mix byte-identity on all 11
   gate-never-opened scenarios, gain-trace forensics on sus1292/sus5,
   phase_cont.py on all four builds, full frozen battery on gated (§6),
   RT-LONG pitch meter (440.00 Hz +0.0¢ all builds).
6. No `as []i32/u32/u16` casts in any source (all `[]u8` arenas) —
   ZNC-2026-09-21-007 does not apply. No RNG anywhere; every number above
   is from deterministic reruns verified by cmp/SHA.

## 10. What remains for Micah's ears

Excerpts stay WITHHELD: no new audio was rendered for presentation, and
none should be — the 4 excerpts already banked by C-CAVEAT remain the
presentation set. When he listens: the audible difference between
stock-C and gated-C on the fixture is the absence of 133 tiny gain
hunts (10.6%→0.3% engagement); the latch correction, veto protection,
and chord behavior are unchanged. Suggested follow-ups needing his or the
coordinator's word: the §4 veto-feed alternative, and whether the G-PER
0.350-at-bar value warrants a dedicated investigation.
