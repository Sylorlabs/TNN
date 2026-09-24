# CRITIC 4 (anti-servo-gate) — preregistered design + kill bars

Date: 2026-09-24. Author: CRITIC 4 (parent-orchestrator red team, PAR tournament).
Status: PREREGISTERED BEFORE ANY EXPERIMENT. This file is committed before any
binary is built or run. Kill bars below are fixed; the verdict (BEAT /
FALSIFIED) is decided by measurement against them, not by argument.

## 0. Stance

The gated necessity gate (crew_servo's recommended servo law) is the WRONG
solution to choppiness. It thresholds the *symptoms* of model error with a
1-D deviation criterion while keeping — by design — 4 residual adapts on the
nominal fixture that are themselves model-error hunting. The right fix
eliminates model error at the source so the servo never needs to hunt; where
evidence is untrustworthy, a 2-D criterion (deviation × model-trust) beats a
1-D threshold. Two designs are tested head-on below.

Settled context (used, not re-litigated): CHOP-3 41-vs-29 is a
measurement-threshold interaction, not a regression (crew_c_caveat); the
gated law's recorded numbers (servo VERDICT §1/§6: nominal 4 adapts / 0.36 FS
dsum / 0.003 engagement; G-PER 0.350 exactly at bar; sus5 divergence 43338
post diffs vs stock 0); edge14's deliberate blind spot; the parked §5.1
veto-feed follow-up (sanctioned as a design comparison by the critic task,
NOT as a law change — changing "vetoed blocks are not evidence" needs
Micah's word).

## 1. The core argument (what the gate gets wrong)

The gate's 4 residual nominal adapts (rg=1/5, rb=118–129) are documented as
"genuine measured deviation, kept by design." They are not genuine. They are
the analytic `plan_rms` model erring during attack transients: the model's
block-RMS number slews faster than the model is valid, `dev` exceeds 15% for
3 consecutive blocks, and the servo "corrects" a fault that exists only in
the model. Evidence:

- The envelope sweep (servo RUNLOG Step 2) proved the model carries ±9%
  per-block error concentrated at vibrato extrema and attack-release
  transients. The Z=3 persistence filters the 27 isolated transient singles
  but *accepts* the attack-transient runs — the one model-error class with
  runs ≥3.
- A 1-D threshold on `dev` CANNOT separate the two cases: edge14 (+14%
  sustained, low model slew) is ignored while attack-transient model error
  (>15% × 3, high model slew) is kept. The gate keeps the wrong one. The
  separating dimension is model slew, which is plan-derived and
  deterministic.

Design X therefore adds the second dimension: a block is gate evidence only
if the plan model itself did not slew by more than the deviation threshold
within one block. No new constant is introduced — the already-grounded
X=15% is reused: *when the model's own number moves by more than the
deviation bar inside a single block, the block's analytic T is not
trustworthy evidence.*

## 2. Designs (exact)

All builds: pure Zag, zero RNG, pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, from the
frozen source `par_dive/contender_c/src/render_c.zag` (SHA-256
`0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db`,
verified before building). Anchors rebuilt: stock, gated (must reproduce
4/0.36 nominal before any X/XY result counts), off.

### Design X — MEE (model-error exclusion)

The crew_servo gated law EXACTLY (OPEN dev>15% × 3 consecutive non-silence
non-vetoed blocks; CLOSE dev<10% × 10; stock update while open; frozen while
closed; region-boundary unity reset; silence-hold; veto always-on; vetoed
blocks neither increment nor reset counters; silence resets open-persistence
— amendment S1), PLUS:

- New per-region state `Tprev:i64 = 0` (declared with the other gate state;
  region-scoped, so it resets at every region boundary like `gopen`).
- Per non-silence block, after T is computed:
  `slew = |T − Tprev|·100/max(T,Tprev)`; `slew_ok = (slew ≤ 15%)`.
  (First block of each region: Tprev=0 → slew=100% → not evidence.
  Silence blocks: the else-branch is not entered; Tprev stays stale, so a
  post-silence attack transient is conservatively excluded.)
- The gate FSM runs only if `veto == 0 AND slew_ok == 1`. Slew-excluded
  blocks neither increment nor reset the open/close counters — identical
  treatment to vetoed blocks.
- `Tprev = T` at the end of every non-silence block (including vetoed and
  slew-excluded ones — T is plan-derived and unaffected by corruption).
- Trace extended with `ts=` (slew_ok) for forensics; no other behavior
  changes. The adapt law, veto, latch, silence-hold, and region reset are
  byte-identical to the gated build.

Predicted: nominal 4→0 adapts, dsum 0.36→0.00 FS, engagement 0.003→0.000;
G-PER returns from 0.350 toward stock's 0.333 (the 4 adapts that moved it
are gone); sus5 post-cut diffs 43338→0 as a side effect (X-clean never
adapts → gain ≡ unity → vetoed blocks park at unity = the clean trajectory).

### Design XY — X + veto-feed (PARKED §5.1 follow-up as design comparison)

Design X, PLUS: on vetoed blocks, the veto's re-measured (bit-exact clean)
dev is fed into the gate FSM instead of skipping vetoed blocks. Concretely
the FSM condition becomes `(veto == 0 AND slew_ok == 1) OR veto == 1`; on
vetoed blocks `slew_ok` is not required (the re-measured m is clean, so the
dev is trustworthy regardless of model slew — the corruption, not the model,
was the evidence problem there).

This is a DESIGN COMPARISON, not a law change: the preregistered rule
"vetoed blocks are not evidence" remains the law until Micah says otherwise.
XY's verdict recommends (or rejects) the amendment; it does not enact it.

Predicted: XY ≡ X on all 15 scenarios (no clean scenario legitimately opens
the X-gate, so veto-feed changes nothing observable — verified by X-vs-XY
mix `cmp` on all 15); XY sus5 post-cut diffs = 0 (FSM follows clean evidence
through the storm; gain trajectory bit-identical to XY-clean).

## 3. Scenarios (same as crew_servo's 4×15 h2h + frozen battery)

Fixture `bytegen/fixture/plan_v1.txt` unless noted. Modes are the binary's
argv[3]; plans marked (regen) are reconstructed from the documented spec
because crew_servo's work/ was not committed — identical inputs for every
build, regeneration documented in RUNLOG.

| key | plan | mode |
|---|---|---|
| a_nominal | plan_v1.txt | seqmix |
| b_rtlong_octlie | tests/plan_rtlong_octlie.txt (regen: 440 cue @1s + RESPOND 880 @28s) | seqmix |
| c_nearmiss460 | contender_c/tests/plan_long_460.txt | seqmix |
| d_suboct | contender_c/tests/plan_long_suboct.txt | seqmix |
| e_2oct | contender_c/tests/plan_long_2oct.txt | seqmix |
| f_vibtort | contender_c/tests/plan_long_vibtort.txt | seqmix |
| f_glide | contender_c/tests/plan_long_glide.txt | seqmix |
| g_chord16 | tests/plan_chord16.txt (regen: 16-voice dense chord) | seqmix |
| h_sus1292 | plan_v1.txt | sus1292mix |
| i_rail1 | contender_c/tests/plan_rail1.txt | seqmix |
| i_rail2 | contender_c/tests/plan_rail2.txt | seqmix |
| drift | tests/plan_drift.txt (regen: 440→430 Hz over 950 blocks, snap to 440) | seqmix |
| flap | tests/plan_flap.txt (regen: 440/465 Hz alternating every 12 blocks, 34 events) | seqmix |
| sawbomb | plan_v1.txt | sawbombmix |
| edge14 | plan_v1.txt | edge14mix |

Frozen battery on the winner (X): DET (2× cmp clean) + 9 V10 bars via
`consistency_gate/src/gate.zag` (G-PER ≤ 0.350, G-STA ≤ 3.000,
G-LURCH ≤ 5.000, G-DRIFT ≤ 800.000, G-FLUXm ≤ 350.000, G-SIL1/2 = 0.000,
G-CLIP ≤ 0.950, G-CREST ≤ 14.000) + CHOP-1/2/3 (`aud_v10/chop.py`, complete
event list) + coherence (motif 2.0–5.4 s vs 24.0–27.4 s, zero-lag xcorr) +
RT-CASCADE (faultmix single-bit @3s; dropoutmix; sus5mix) + RT-EDGE
(truncated plan @15 s) + RT-LONG pitch meter on b–f + phase continuity
(|φ_end−φ_start| > 0.2 rad unexplained = flag, all builds).

STRETCH leg (genuine fault under storm, distinguishes XY from X): plan with
a genuine sustained +25% render-level deviation over 200 blocks (below the
2.5× veto line, above X=15% — the gate legitimately opens) overlapped with a
veto storm: XY's gain trajectory must be bit-identical to XY-clean-fault;
X parks at unity (documents the cost of "vetoed blocks are not evidence").

## 4. Kill bars

### Step 0 (anchor gate — no X/XY result counts unless these pass)
- S0a: rebuilt stock reproduces 137 adapts / 9.80 FS dsum / 0.106 engagement
  on a_nominal (byte-identical rerun by cmp).
- S0b: rebuilt gated reproduces 4 adapts / 0.36 FS / 0.003 on a_nominal.
- S0c: from the gated nominal trace, ALL 4 adapt blocks satisfy
  slew = |T−Tprev|·100/max(T,Tprev) > 15%. (If any adapt block has slew ≤
  15%, Design X as specified is falsified at the design level: the residual
  adapts are not attack-transient model error, and the verdict is FALSIFIED
  with the trace published.)

### X BEAT bars (ALL must pass; X strictly better than gated on nominal)
- B1: a_nominal: X adapts < 4 (target 0) AND dsum < 0.36 FS (target 0.00).
- B2: frozen battery on X: 9/9 bars incl. G-PER ≤ 0.350 (target ≤ 0.333);
  CHOP-3 0 unexplained.
- B3: coherence: motif windows byte-identical; zero-lag xcorr 1.0000000000.
- B4: DET: 2× renders cmp clean per new build; X-vs-off mix byte-identical
  on every gate-never-opened scenario.
- B5 (red team): sawbomb adapts ≤ 4, vetoes ≥ 18, dsum ≤ 0.36;
  edge14 adapts ≤ 4 (blind spot documented, unchanged);
  drift 0 adapts AND mix == off; flap 0 adapts AND mix == off;
  g_chord16 0 adapts, RMS(2–5 s) = 0.825 ± 0.005 FS, peak = 2.98 ± 0.02 FS;
  sus1292 1295/1295 vetoes, gain parks at unity (dsum 0.00);
  rail1/rail2 0 adapts; b–f latch lines identical to gated
  (k=-1/+1/-2, rsn=1, rsn=3), 0 adapts.
- B6: RT-CASCADE single fault 0 post-cut diffs; dropout 136 post diffs
  (identical to stock); RT-EDGE first diff 14.975 s (legitimate bed edge),
  0 diffs before 14.9 s; RT-LONG 440.00 Hz +0.0¢ on b (all builds).
- B7: phase continuity: 0 build-attributable unexplained phase jumps; the
  same 18 plan-content flags as stock/gated/off (md5-identical flag lists).
- B8: X sus5: post-cut diffs = 0 (bit-identity with X-clean).

### XY design-comparison bars
- C1: XY passes B1–B7 identically to X; X-vs-XY mixes cmp-clean on all 15
  scenarios.
- C2: XY sus5: post-cut diffs = 0 (bit-identity with XY-clean) vs gated's
  43338.
- C3 (stretch): genuine-+25%-fault-under-storm: XY gain trajectory
  bit-identical to XY-clean-fault (adapts as clean would); X parks at unity.

## 5. Verdict rules

- **BEAT**: S0a–S0c + B1–B8 ALL pass → Design X strictly beats the gated law
  on Micah's criterion (nominal adapts 4→0, dsum 0.36→0.00, no regression
  anywhere, sus5 divergence eliminated as a side effect). Recommendation:
  the gated law is SUPERSEDED by MEE.
- **BEAT+**: BEAT + C1–C3 pass → additionally recommend the veto-feed
  amendment to Micah (his word required to change the law).
- **PARTIAL**: X passes B1–B7 but B8 fails (or vice versa) → report exactly
  which bars passed/failed with numbers; no recommendation change without
  all bars.
- **FALSIFIED**: S0c fails, or any of B1–B7 fails after genuine attempts
  (e.g. G-PER > 0.350, any red-team regression vs gated, DET failure) →
  document everything tried with traces and numbers; confidence in the
  gated law rises. A genuine falsification is a win for the tournament.
- No new audio excerpts for presentation; rendered artifacts stay local,
  never shown to Micah. Audio analyzer-first: no progress claim without
  waveform measurement + SHA-256 identity on every file.

## 6. Procedure (in order)

1. Commit this prereg (this file) to
   `docs/lab/bytegen/par_tournament/critics/anti_servo/PREREG_CRITIC.md`.
2. S0: rebuild stock/gated/off from frozen source; verify S0a–S0c.
3. Generate X/XY sources via exact-string edits on the verified gated
   source; build; DET.
4. Run 5-build × 15-scenario h2h; parse traces (adapts/vetoes/dsum/
   engagement/latch lines); X-vs-XY cmp.
5. Frozen battery on X (9 bars + CHOP + coherence + RT-CASCADE/EDGE/LONG +
   phase continuity + sus5).
6. Stretch leg if time permits.
7. Write VERDICT.md + RUNLOG.md; commit; report BEAT / FALSIFIED / PARTIAL
   with numbers and commit SHAs.
