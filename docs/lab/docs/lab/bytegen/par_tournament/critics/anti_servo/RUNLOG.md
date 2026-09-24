# CRITIC 4 — RUNLOG

## 2026-09-24: preregistration
- Read tournament synthesis, crew_servo VERDICT/RUNLOG/src, crew_c_caveat VERDICT, frozen PREREG_PAR_DIVE, frozen contender-C source + test plans (from GitHub branch `tnn-native-lab`).
- Settled evidence recorded: gated 4/0.36/0.003; sawbomb 4+18 vetoes/0.36; G-PER 0.350; sus5 gated 43338 post-cut diffs; CHOP-3 41-vs-29 settled as threshold interaction.
- Wrote `PREREG_CRITIC.md` (Design 1: X/MEE; Design 2: XY/MEE+veto-feed as design comparison; kill bars B1/B2/S0c/B8/C1/C2/C3).
- Committed prereg to `docs/lab/bytegen/par_tournament/critics/anti_servo/PREREG_CRITIC.md` as `cb3e7a913eb25388d275017f3ce04d6905509011` BEFORE building/running any alternative binary.
- Verified frozen source SHA-256 `0640f28f…` and downloaded crew_servo gated source `c1eca96a…`.

## Build
- Regenerated crew_servo variants from frozen source with `src/gen_variants.py`-equivalent; regenerated gated source **byte-identical** to the committed crew_servo gated source.
- Wrote `src/gen_critic.py` (deterministic string-replacement generator): frozen gated source → `src/render_c_x.zag` (X/MEE) → `src/render_c_xy.zag` (XY/veto-feed).
- Two pre-run compile fixes (both before any experimental result): `slew_ok` scope placement; a duplicated FSM fragment brace imbalance from an editing error (generator rewritten cleanly).
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` for all builds.
- Built: `render_c_stock`, `render_c_off`, `render_c_gated`, `render_c_x`, `render_c_xy`. No binaries committed.

## Anchors (S0a/S0b reproduced exactly)
- Stock nominal: 137 adapts / 9.80 FS / 0.106 engagement.
- Gated nominal: 4 adapts / 0.36 FS / 0.003.
- Trace-parser correction: initial parser counted region-boundary unity resets as gain movement (9.95/0.39); fixed to reset `gprev` on region change → exact reproduction.
- The 4 gated nominal adapts: rg=1/5 rb=118 (T=15056, Tprev=19191, slew 21.5%), rb=119 (T=7087, Tprev=15056, slew 52.9%). All > 15% → S0c PASS (prereg prediction confirmed before X ran).

## First X result
- X nominal: **0 adapts / 0.00 dsum / 0.000 engagement**. XY nominal identical; X-vs-XY nominal WAV `cmp`-clean.
- X nominal mix byte-identical to servo-off mix (servo correctly idle).

## Plans
- crew_servo's RT-LONG octlie / chord16 / drift / flap plans were not committed; regenerated per documented specs into `tests/`:
  - `plan_rtlong_octlie.txt` (440 cue @1s, RESPOND 880 @28s)
  - `plan_chord16.txt` (16 chromatic voices 220–523 Hz — denser than crew_servo's; theirs unrecoverable)
  - `plan_drift.txt` (440→430 over 950 blocks in 50 events, snap to 440)
  - `plan_flap.txt` (440/465 alternating every 12 blocks, 34 events)
- Downloaded contender-C plans (460/suboct/2oct/vibtort/glide/rail1/rail2) from the branch.
- `plans/plan_v1_edge15.txt`: plan_v1 with content ending at 15 s (BED 0.0–15.0; first attempt dropped bed freq/amp fields → silent bed → caught by trace inspection, fixed).
- `work/events_v1.txt`: 271-event complete list (onsets, offsets, vibrato extrema) generated deterministically from plan_v1; calibrated on gated (CHOP-3 32 total matches crew_servo's 32).

## H2H (5 builds × 15 scenarios, `work/run_h2h.py`)
- Full table in `work/h2h/h2h.json` (75 entries). Key: X ≤ gated everywhere; strictly better on nominal/sawbomb/edge14 (4→0, 0.36→0.00); tie on chord16 (35/3.29) and zero scenarios.
- Notable: on the downloaded contender-C plans, the gated law itself already yields 0 adapts on suboct/2oct/vibtort/glide (stock flaps 9–10× single-block; the 3-consecutive rule filters them). The nominal fixture remains the discriminator.
- Chord16 analysis: gate opens rb=106, closes rb=187; m oscillates ±20% (beating), dev never converges — sustained oscillatory model error, MEE's designed boundary.
- Sawbomb: X 0 adapts / 18 vetoes / 0.00 dsum (gated: 4/18/0.36). Edge14: X 0/0.00 (gated 4/0.36 — the 4 are the same transient blocks as nominal, not the +14% scaling).
- Parser convention: adapts = trace `st==1` count (crew_servo convention; binary summary counts veto-hidden adapts). Engagement = (adapts+vetoes)/blocks.
- Race note: two concurrent h2h runs (xy-v3 and stock/off/gated/x) both wrote h2h.json; the later overwrote xy-v3's sus1292 entry with the stale v2 value (0.36). Detected via byte-identity check (mixes identical, JSON disagreed); repaired by re-parsing `run_xy_v3.log`. Lesson: one writer at a time for the results JSON.

## XY bug history (design comparison)
- v1: vetoed blocks skipped the slew computation (`if (veto==0)` guard) → veto-feed ran a gated-style FSM → XY-sus1292 replayed gated-clean (0.36 dsum). Caught by C1 check.
- v2: computed slew on vetoed blocks but kept `if (veto==1 || slew_ok==1)` → veto bypassed MEE → gate still opened on vetoed transient blocks (trace: `ts=0` yet `gs=1` at rb=118). Caught by trace inspection.
- v3: `if (slew_ok==1)` — the veto only changes where dev comes from; MEE applies uniformly. XY-sus1292 → 0.00 dsum. All reported XY results are v3.
- Result: XY v3 ≡ X on all 15 scenarios (metrics + byte-identical mixes). The veto-feed is subsumed by MEE.

## Frozen battery on X
- 9 bars (tools/gate_v10, built from frozen V10 gate): 9/9 PASS; G-PER 0.340 (gated 0.349, stock 0.333).
- CHOP (aud_v10/chop.py + events_v1.txt): 0 / none / 29 total, 0 unexplained.
- Coherence: 1.0000000000; motif windows byte-identical.
- RT-CASCADE (mix-level, memmap chunked): fault 64 diffs (= the fault itself, t∈[3.0,3.0015)s); dropout 1023 diffs confined to the zeroed block [132232,133256), 0 elsewhere; sus5 13888 pre-cut / **0 post-cut**.
- Gated sus5 baseline reproduced: 44021 post-cut diffs (crew_servo: 43338; delta = mix-level vs WAV-level comparison).
- RT-EDGE: first diff 14.975 s, 0 before 14.9 s (bed edge fade, legitimate; reproduces crew_servo).
- RT-LONG pitch: 880.00 Hz −0.0¢ (RESPOND window, band-limited). Cue window reads identically across stock/gated/X (423.56 Hz — bed-harmonic measurement artifact, not a build difference).
- Phase continuity (work/phase_cont.py): 0 build-attributable flags X-vs-gated.
- Note: `seqmix`/`mix` modes write raw s32 (no RIFF header) — the V10 gate and chop.py need real WAVs, produced via `seq` mode (peak-normalized; the gamma disease applies equally to all builds, comparisons are fair).

## Determinism
- `cmp`-clean reruns: X nominal/sawbomb/chord16, XY nominal. SHA-256 recorded for sources and binaries (see VERDICT.md).
- 75/75 h2h mixes SHA-pinned.

## Deviations from prereg (all documented)
1. B1 wording: "strictly fewer on every scenario" read per the prereg's own parentheticals (sawbomb "< 4/< 0.36", edge14 "< gated's", chord16 "≤"). Zero-scenarios tie at 0 — the intent (strict Pareto improvement) is met.
2. Chord16: crew_servo's plan unrecoverable; my regen is denser (gated 35/3.29 vs their 2/0.05). X ties gated — analyzed as MEE's boundary, not a failure.
3. G-SIL1/2 bars: prereg wrote measured values (0.000); actual gate bars are ≤0.02/≤0.5 — measured 0.000 passes either way.
4. C3: prereg prediction (XY≡XY-clean-fault under storm) was wrong; corrected analysis in VERDICT.md. Dropped as moot after XY≡X.
5. RT-EDGE: DUR_S is informational (NSAMP hardcoded); truncation done by ending plan content at 15 s.

## Commit
- `docs/lab/bytegen/par_tournament/critics/anti_servo/`: VERDICT.md, RUNLOG.md, PREREG_CRITIC.md (already), src/gen_critic.py, src/render_c_x.zag, src/render_c_xy.zag, work/*.py, work/h2h/h2h.json, plans/plan_v1_edge15.txt, tests/plan_*.txt, work/events_v1.txt.
- Binaries, .zagd caches, WAVs/mixes, and trace logs excluded.
