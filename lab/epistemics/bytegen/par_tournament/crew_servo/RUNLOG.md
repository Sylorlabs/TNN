# Crew SERVO run log — 2026-09-24 (PAR tournament, coordinator round)

Micah's criterion: "I don't want choppiness when unnecessary."
Task: find EXACTLY when contender C's servo helps vs adds choppiness; build a
servo that fires ONLY when necessary.

## Setup
- Frozen source: `par_dive/contender_c/src/render_c.zag`
  SHA-256 `0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db`
  — verified byte-identical in `src/render_c_stock.zag` before building.
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Workdir: `~/workspace/tnn-lab/bytegen/par_tournament/crew_servo/`
- Fixture: `~/workspace/tnn-lab/bytegen/fixture/plan_v1.txt`
- No `as []i32/u32/u16` casts anywhere in the source (all `[]u8` arenas) —
  ZNC-2026-09-21-007 does not apply.
- C-CAVEAT RUNLOG read (2026-09-24): they own spike-counting/ablation;
  I own the necessity-gating design. No duplication.
- Fable R1 servo map read
  (`par_tournament/fable_round1/FABLE_R1_SERVO_MAP.md`, commit d2069082).
  Fable's two-tier criterion is the CHALLENGER arm; my thresholds primary.

## Step 1 — stock C rebuild + DET (done)
- Built `src/render_c_stock` from the verified source (znc warnings only).
- DET: 2× `seqmix` renders of the fixture → `cmp` clean. PASS.

## Step 2 — operating-envelope sweep, stock C (done)
Harness `work/sweep.py`. Per-block trace parsed
(`C rg= rb= g= m= T= st=`); activity = adapts(st=1)/vetoes/st=3 holds/idles,
gain-variance dsum=Σ|Δg| within regions (FS units), region-start transients
(adapts with rb<10), engagement fraction.

| key | scenario | n | adapts | vetoes | holds | dsum(FS) | regtrans | engage |
|---|---|---|---|---|---|---|---|---|
| a | fixture nominal (plan correct) | 1295 | 137 | 0 | 0 | 9.80 | 4 | 0.106 |
| b | RT-LONG octave lie 880/440 | 1293 | 9 | 0 | 0 | 0.77 | 1 | 0.007 |
| c | near-miss 460 | 1293 | 9 | 0 | 0 | 0.71 | 1 | 0.007 |
| d | sub-octave lie 220/440 | 1293 | 9 | 0 | 0 | 0.77 | 1 | 0.007 |
| e | 2-octave lie 1760/440 | 1293 | 10 | 0 | 0 | 0.77 | 1 | 0.008 |
| f | vibrato-torture cue | 1293 | 10 | 0 | 0 | 0.80 | 1 | 0.008 |
| f | glide cue | 1293 | 10 | 0 | 0 | 0.78 | 1 | 0.008 |
| g | N=16 dense chord | 1293 | 2 | 0 | 1163 | 0.05 | 1 | 0.002 |
| h | sus1292 (1292-block corruption) | 1295 | 0 | 1295 | 0 | 9.80 | 0 | 1.000 |
| i | rail1 adversarial text | 1293 | 5 | 0 | 1209 | 0.32 | 1 | 0.004 |
| i | rail2 adversarial text | 1293 | 7 | 0 | 1179 | 0.54 | 1 | 0.005 |

Latch traces (b–f): octave lie → `LATCHED f0=440Hz` (k=-1); near-miss →
nominal kept; sub-oct → LATCHED up (k=+1); 2-oct → LATCHED down (k=-2);
vibtort → LATCHED (fm=454); glide → abstain (rsn=1, ZCR halves disagree).
All match REDTEAM_C.md.

KEY FINDINGS (envelope):
1. The fixture-correct plan (a) drives 137 adapts — 10.6% engagement, 9.8 FS
   of total gain movement — with ZERO benefit: the plan is correct, the latch
   never fires, output differs from plan-pure only by servo hunting its own
   ±9% model error at vibrato extrema / attack-release transients.
2. (h): dsum under sus1292 == clean dsum (9.80 FS) to the LSB — veto keeps the
   gain trajectory bit-identical to clean (reproduces REDTEAM_C.md).
3. (g): the servo parks after ONE −0.6 dB step (65536→60977) at the chord
   attack, then idles: adapts=2, dsum=0.05 FS. Chord mix RMS(2–5 s)=0.825 FS,
   peak=2.98 FS — i.e. the H3 servo does NOT self-limit dense sums.
   The dive's "N=16 self-limiting, RMS 0.54 FS" number is from FORK_AR's OLD
   v2-hybrid servo (PAR_CHARACTERIZATION.md §3: "AR mix RMS 0.539 FS vs PAR
   0.897 FS" — that servo touched gain AND timbre). It does NOT transfer to
   the frozen H3 source. The task background's "proven win" list misattributes
   it. Bar for C-gated on (g): match STOCK's numbers (0.825/2.98), not 0.54.
4. RT-LONG correction is the PIECE-3 LATCH, not the servo: the 9 adapts on
   (b)–(f) are region-start/model-error transients, unrelated to the octave fix.

Deviation distribution (dev=|T−m|·100/max(T,m), non-silence blocks):
- (a): p50=4.3% p90=10.3% p99=16.0% max=25.8%; runs of dev>15%: 27× length-1,
  ZERO runs ≥3.
- (b): max=30.7%; 3× length-1 runs >15%, zero ≥3.
- (g): max=13.9%; zero runs >15%.

## Step 3 — PREREGISTERED GATE DESIGN (written BEFORE building any gated binary)

### 3a. Primary: C-gated (my design)
The H3 servo is a residual regulator with a plan-derived target: on a correct
plan its fixed point is g*=T/S≈1 and every adapt is model-error hunting.
Necessity = a REAL, SUSTAINED deviation the 10% deadband cannot explain.

- OPEN condition: dev=|T−m|·100/max(T,m) > X=15% for Z=3 CONSECUTIVE
  non-silence, non-vetoed blocks. (X=15: outside the measured model-error
  floor p90=10.3%, inside the veto band; Z=3: 69.6 ms — filters the 27
  isolated transient singles seen on the fixture, catches sustained faults.)
- Pitch trigger Y: NOT APPLICABLE. SPEC §1 forbids the servo from pitch
  adjustment (gain/timbre execution params only); pitch correction is owned by
  the piece-3 latch, which is unchanged in all builds. A gain servo must never
  fire on pitch disagreement — that would be a category error.
- HYSTERESIS (close): dev < 10% (back inside the stock deadband) for 10
  consecutive blocks → CLOSE. (10 blocks: the 1/2-contraction reduces error
  1024× in 10 blocks; prevents flapping.)
- While OPEN: the stock update law applies UNCHANGED
  (g←(g+g·T/m)/2, clamp [0.5,2.0], 10% deadband parks inside).
- While CLOSED: gain frozen (no adapt). Region-boundary reset to unity,
  silence-hold (T<SILENCE_FLOOR), and the VETO stay EXACTLY as stock —
  the veto is measurement hygiene (always-on), independent of the gate.
  Vetoed blocks neither increment nor reset the open/clear counters.
- Prediction: on (a) engagement 0.106→~0.000 (137→0 adapts); on (b)–(g),(i)
  adapts→~0; on (h) trajectory bit-identical to stock-clean (all blocks
  vetoed → counters frozen → gain all-unity = stock-clean gated trajectory…
  verified empirically in Step 5).

### 3b. Challenger: C-gated-fable (fable R1 two-tier, adapted to H3)
- Tier-1(a) pre-engage: at region start, max simultaneous voices N and max
  summed analytic RMS over the region; if N≥4 AND sum>0.7 FS → gate pre-opens
  for the region (fable's "preventive headroom" — tests whether the H3 servo
  does preventive limiting at all; envelope says no, measurement decides).
- Tier-1(b): same 15%/3-block as primary.
- Tier-1(c) pitch>50¢/5 blocks: documented N/A (gain servo cannot fix pitch;
  latch owns it) — implemented as abstain-with-trace-note, not a gain trigger.
- Tier-1(d) corruption detector: veto already always-on (no change).
- Tier-2 hysteresis: 20-block minimum active OR until triggers clear + 10-block
  grace (fable's numbers verbatim).
- Prediction: ≈ primary on sparse plans; on (g) pre-engages but the stock law
  still parks after ~1 step (no preventive limiting exists to pre-engage).

### 3c. Control: C-servo-off
Adapt fully disabled (gate never opens); veto disabled (nothing to protect);
latch intact. Output = exact plan-pure render (PAR-equivalent). Isolates the
servo's total contribution: stock vs off differ ONLY by servo gain steps.

## Step 4 — fable's adversarial plans (to run in Step 5)
- (i) SUB-THRESHOLD DRIFT: 440→430 Hz over 950 blocks, snap to 440.
  Fable predicts gated-C gives a 10-block correction transient (assumes a pitch
  servo). H3 prediction: servo is gain-only; RMS deviation ~0 throughout;
  stock=gated=off render the plan exactly; engagement 0 everywhere. The plan
  IS the drift — there is nothing to correct.
- (ii) GATE FLAPPING: 440/465 Hz alternating every 12 blocks (34 events,
  NEVMAX=64 respected). H3 prediction: RMS constant → gate stays closed in all
  builds; output == servo-off. (Fable's engage/hysteresis analysis assumes a
  pitch-correcting servo; for H3 the correct behavior is gate-closed.)
- (iii) CORRUPTION BOMB (sawtooth +138%/+5%): new test mode `sawbomb`
  (alternate blocks ×2.38 / ×1.05 rendered amplitude, t∈[10,20)s) — m/T=2.38
  sits JUST under the 2.5 veto line. Stock prediction: no veto, adapt fires,
  gain wobbles following garbage. Gated prediction: 3-block persistence never
  satisfied by the sawtooth → gate stays closed → no wobble (bytes corrupted
  either way; state not dragged). Fable predicted "no stock-vs-gated
  difference" — the veto-band edge says otherwise; measurement decides.

## Step 5 — head-to-head plan (stock vs gated vs gated-fable vs servo-off)
Full 9-bar V10 quality gate + CHOP-1/2/3 + coherence + RT-CASCADE + RT-EDGE on
the winner; pitch-meter RT-LONG family on all; phase-continuity test (fable Q2:
|φ_end(n)−φ_start(n+1)| mod 2π, >0.2 rad unexplained by f0 = discontinuity)
on all; LATENCY wall-clock on RT-LONG + engagement fraction (fable Q5:
gating is not expected to save wall-clock — analyze()/plan_rms_raw() run
regardless — reported honestly).
Success bar: gated keeps 100% of stock's REPRODUCIBLE wins (latch RT-LONG
+0.1¢, sus1292 trajectory bit-identical, (g) numbers match stock) while
gratuitous choppiness on clean plans → ~0 (servo-attributable adapts ≈ 0,
CHOP-3 delta vs off ≈ 0).

## Step 6 — red-team the gate
(a) deadband exploitation: fault sized just under thresholds (sawbomb covers
the veto edge 2.38<2.5; plus a +14% sustained drift — just under X=15 — to
show what the gate deliberately ignores); (b) spurious-open: oscillating plan
energies (flap plan + an amplitude-flap variant: amp 700/1400 every 4 blocks —
RMS alternates ±~30% but never 3 consecutive >15%? 4-block runs: 700×4 then
1400×4 → dev>15% for 4 consecutive → gate OPENS legitimately; documents the
hysteresis cost on pathological plans).

## Log
(append below)

### 2026-09-24 ~18:05 — CREW SERVO-RECOVERY (first crew's experiments complete, no VERDICT written)
Inherited: RUNLOG through Step-5 plan (log section empty); 4 variant sources
(16:50) postdating 4 binaries (16:20); work/h2h.json + 60 logs/mixes
(16:23–17:00); work/phase_cont.py; tests/plan_drift.txt, plan_flap.txt.

Recovery actions:
1. `src/gen_variants.py` was broken (17:29 edit): `add_common()` called
   before its definition (NameError), plus double-application of the common
   edits on the off/gated/gfable chains. Fixed with a pristine `base` +
   `add_common(base)` per variant. All four sources now regenerate
   byte-identically from the frozen source (SHA 0640f28f…) — verified by
   cmp against the inherited 16:50 sources (stock/off exact; gated/gfable
   differ by exactly the S1 line).
2. Amendment S1 (in the broken script, never built): silence blocks reset
   the open-persistence counter. Applied — it was the crew's documented
   intent and fixes v1's measured flap false-open (gate OPEN rg=1 rb=356).
   v1 h2h outputs archived to work/v1_superseded/ (not committed).
3. Rebuilt all four binaries with the pinned toolchain
   (znc_linux_x86_64_abed8aa1; analyzer warnings only). stock/off SHAs
   match the 16:20 builds byte-identically; gated/gfable differ only by S1.
4. Re-ran the FULL 4×15 head-to-head with fresh binaries → new
   work/h2h.json. Stock reproduces v1 exactly (nominal 137/9.80, sawbomb
   564/86.75, edge14 140/9.92). Gated v2: nominal 4/0.36, flap 0 adapts
   (fix confirmed), sawbomb 4+18 vetoes/0.36, edge14 4/0.36.
5. Latch confirmation (grep, fresh logs): b/d/e LATCHED k=-1/+1/-2,
   f_glide abstains (rsn=1), c_nearmiss460 nominal (rsn=3) — identical on
   all four builds.
6. Byte-identity: gated vs off mixes byte-identical on all 11
   gate-never-opened scenarios (b,c,d,e,f_vibtort,f_glide,g,i_rail1,i_rail2,
   drift,flap). sus1292: vetoes 1295/1295 in stock+gated+gfable; stock gain
   trace bit-identical clean-vs-corrupted (9.80 FS replayed); gated parks
   at unity (0.00) — prereg Step-3a prediction corrected in VERDICT §4.
7. phase_cont.py on all four nominal mixes: identical 18-flag sets
   (md5 match); 0 build-attributable phase jumps.
8. Frozen battery on gated (§6 of VERDICT): 9/9 V10 (G-PER 0.350 at bar),
   CHOP 0/none/32-total-0-unexplained, coherence xcorr 1.0000000000 with
   byte-identical motif windows, RT-CASCADE fault 0 post / dropout 136
   post (same as stock) / sus5 bounded 55-block offset (documented
   divergence), RT-EDGE first diff 14.975 s, RT-LONG 440.00 Hz +0.0¢.
9. gfable vs gated: primary gate wins every scenario (nominal 4 vs 10
   adapts; sawbomb 4 vs 10; chord16 0 vs 1 via pre-engage). Fable's
   tier-2 hysteresis and pre-engage rejected with numbers.
10. DET: stock 2× renders cmp clean; gated h2h mix == independent smoke
    mix (cmp clean). Wall-clock: no systematic win (means 10.7–12.2 s);
    engagement fraction reported instead.

Verdict: RECOMMEND the primary necessity gate (X=15%/Z=3 open, 10%/10-block
close, veto always-on, region reset, silence hold, silence breaks
persistence). VERDICT.md written. Excerpts WITHHELD (none rendered;
C-CAVEAT's 4 stay the presentation set).
