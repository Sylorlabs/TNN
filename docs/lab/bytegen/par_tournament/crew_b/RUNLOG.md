# CREW B — PAR Tournament RUNLOG

Date: 2026-09-24. Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG in every binary. Fixture: `~/workspace/tnn-lab/bytegen/fixture/plan_v1.txt`
(30 s / 44.1 kHz / mono). WAV comparisons at MIX level per standing house rule.
Workdir: `~/workspace/tnn-lab/bytegen/par_tournament/crew_b/`.

Prior dive: `~/workspace/tnn-lab/bytegen/par_dive/contender_b/` (VERDICT: OVERTHROW
on RT-LONG + COST; disclosed bug: inverted release envelope — fixed here).

## PREREGISTERED FORK CLAIMS (written before any build)

### B-fix — release-envelope fix
BASELINE: par_dive `render_b.zag` (inverted release: `x=(rem*1024)/rel` with
`env=32768+lsin(lut,256+x/2)` makes notes go SILENT at release onset and swell
to FULL at note end, then hard-cut).
FIX: at all 4 release sites (`voice_closed`, `bus_env_at`, `span_render` hot
loop, `render_bed`) change `x=(rem*1024)/rel` → `x=((rel-rem)*1024)/rel`
(elapsed-release-time form). Nothing else changes.
CLAIM: (1) byte-level diff vs baseline is confined to note release windows
(last `rel` ≤ 150 ms of each note; attack/sustain/coherence windows
byte-identical); (2) all 9 quality gates still PASS with G-PER ≤ 0.350
(the release is now a true fade — envelope autocorrelation should not
regress); (3) coherence xcorr stays 1.000000; (4) COST within ±5% of 8.54 s;
(5) RT-LONG stays 0¢ (440 Hz latch); (6) RT-CASCADE stays 0 post-cut diffs;
(7) determinism: ≥20/20 byte-identical reruns, binary SHA pinned at build.
ACCEPT: no §6 bar regresses vs the dive's B numbers.

### B-gate — B-fix + 40–4000 Hz gate on the FULL pitch path
The dive shipped the gate ONLY on the RESPOND cue (`respond_latch` rejects
cues outside 40–4000 Hz → immune to the 30 Hz trap that breaks NATIVE/C).
B-gate extends it to every pitch that enters the synth:
  1. parse: EVENT f0 clamp tightened [0,20000] → [40,4000] Hz (documented);
  2. `respond_latch`: nominal must be in [40,4000] Hz or the latch ABSTAINS;
  3. `respond_latch`: the latched output `nom*2^k` must be in [40,4000] Hz or
     the latch ABSTAINS (prevents e.g. 30 Hz nominal × 2^k latching to a
     sub-audible or 5000 Hz nominal latching ultrasonic).
CLAIM: (1) frozen fixture renders byte-identical to B-fix (all fixture
pitches in-range → gate is a no-op there); (2) standard RT-LONG still 0¢
(440 cue / 880 nominal → LATCHED 440); (3) NEW vs B-fix: nominal30
(440 cue / 30 nominal) ABSTAINS where B-fix would latch 30×16=480 Hz;
nominal5000 ABSTAINS where B-fix would latch 5000/8=625 Hz; an EVENT at
30 Hz renders clamped to 40 Hz (B-fix renders 30 Hz); (4) cue30/cue5000
stay DEFENDED; (5) all 9 quality gates PASS on the frozen fixture.
ACCEPT: trap battery shows the three new abstains/clamps, fixture battery
shows zero behavioral change.

DESIGN CORRECTION (2026-09-24, during the round): the preregistered
parse-time EVENT clamp was built as v1 and REJECTED by its own trap
battery — clamping the cue event's f0 at parse laundered the 30 Hz cue
into 40 Hz, so the cue gate saw an in-range cue and the latch fired
880→55 Hz (the exact trap the gate exists to kill). v2 (shipped) gates at
the RENDER read sites via `gate_f` and keeps plan truth in the event
fields so `respond_latch` judges the plan's actual claim. All ACCEPT
criteria above hold for v2; the mechanism changed, the behavior claims
did not.

### B-lie — plan-lie battery (test battery on the B-fix binary, no code change)
B's RESPOND is sensorless: the rendered cue IS the plan cue, so the latch
trusts plan fields (cue f0, nominal, w0/w1) completely. Map where that trust
breaks with 10 adversarial plans:
  lie1 nominal-lie: cue 440 true, nominal says 1760 (2 octaves off).
  lie2 nominal-lie-down: cue 440, nominal 220.
  lie3 cue-lie: cue FIELD says 440 but the "true" cue (per an independent
    channel — the plan comment) is 880; B cannot know. Expect: latches 440,
    self-consistent, wrong vs ground truth. (Documents the boundary.)
  lie4 cue-lie-up: cue field 880, nominal 880 → k=0, nominal stands (440
    expected by listener). Expect: renders 880.
  lie5 window-lie: RESPOND w0/w1 window excludes the cue (cue at 1.0–2.0,
    window 5.0–6.0, empty) → nvoice=0 → abstain. Expect: nominal stands.
  lie6 ghost-voice: a second zero-duration EVENT inside the window → does
    the polyphony guard count it? Expect: depends on overlap test
    (a2<w1 && b2>w0 with b2==a2 → no overlap → nvoice=1). Documents guard
    edge.
    ACTUAL (corrected during the round): nvoice=2 → ABSTAIN. The overlap
    test `a2<w1 && b2>w0` with the ghost at t=1.5, window [1.0,2.0):
    1.5<2.0 && 1.5>1.0 → TRUE → the zero-duration ghost COUNTS. Safe
    direction (vetoes the latch); documented in VERDICT.md.
  lie7 near-octave cue: cue 622 Hz (≈ between), nominal 880 → k=0 boundary.
    Expect: nominal stands (0.7071 threshold).
    ACTUAL (corrected during the round): k=-1 → LATCHED 440. The rounding
    boundary is exactly 2^-0.5=0.70711; 622/880=0.70682 < boundary → k=-1.
    Probe lie_7b (623 Hz → 623/880=0.70795 > boundary) gives k=0, nominal
    stands. Razor-thin, deterministic, documented in VERDICT.md.
  lie8 cue at gate edge: cue 40 Hz exactly (in-range), nominal 880 →
    k=round(log2(40/880))=round(-4.46)=-4 → 55 Hz. In-range latch to 55 Hz.
    Expect: LATCHED 55. Documents gate-edge behavior.
  lie9 sub-octave nominal lie: cue 440, nominal 110 → k=+2 → 440. The latch
    CORRECTS the lie. Expect: LATCHED 440.
  lie10 double lie: cue field 220 (true 440), nominal 1760 → k=round(
    log2(220/1760))=round(-3.0)=-3 → 220. Expect: latches 220 (cue lie
    amplified through the octave math).
CLAIM: the battery classifies each lie as CORRECTED (latch fixes it),
FOLLOWED (B renders/latches the lie — self-consistent, wrong vs truth), or
ABSTAINED. The provenance boundary: B has no independent sensor, so cue-field
lies are undetectable by construction; the hybrid v2's audio-measured path is
more robust exactly here (documented, not re-tested).

## §5 RED TEAM (densified vs the dive)
- R1 cross-region leakage: standalone `regionmix k` vs in-context slice for
  ALL 10 regions (dive did 10/10 on one adversarial plan; here: per-boundary
  on 3 adversarial plans — legato chain crossing a boundary with vibrato +
  portamento, event starting exactly at a boundary, high-amp event in region
  0). 9 boundaries × 3 plans = 27 probes.
- R2 sustained 1292-block corruption: XOR 0xFF per 1024-sample block over the
  full mix, count post-cut propagation (dive: 0). Re-run on B-fix.
- R3 plan-text adversarial: the 14-plan fz_* corpus from
  par_dive/redteam/plans/ on B-fix: no crash/hang, bounded output.
- R4 polyphonic RESPOND: r_poly.txt + a 3-voice variant.
- R5 sub-octave nominal lies: nominal 220/110/55 with cue 440.
- R6 burst / dropout / DC-shift fault models (RT-CASCADE extension per §3):
  512-sample zeroing @ t=3 s; 4096-sample burst (XOR 0xFFFF) @ t=3 s;
  +0.05 FS DC shift over [3 s, 4 s) — count post-cut diffs vs clean.

## Build log
(see entries below; binary SHAs pinned at each build)

- 2026-09-24: `render_b_fix.zag` = dive `render_b.zag` + 4-site release
  fix (only diff: `x=(rem*1024)/rel` → `x=((rel-rem)*1024)/rel`, bed
  `x=(tout*1024)/ed` → `x=((ed-tout)*1024)/ed`). Built pinned znc
  (2 inherited false-positive dead-loop analyzer warnings, same as dive).
  Binary SHA `41a953669ec04422a69902256649b19613a5918445afe8f36d4030916957ead1`
  (87,146 bytes). Source SHA `637479bdc513f76cdee332e866c1cb87d138a45f0a60591b279ea68626b21a59`.
  Baseline rebuilt from dive source for A/B: SHA
  `432a55e1169d3dfe83624e68605ee5ed8b756461800719700475fc2d9b59fd20`
  (matches determinism_rc/ROOT_CAUSE.md recorded hash — provenance clean).
- 2026-09-24: `render_b_gate.zag` v1 (parse-time EVENT clamp) built, then
  SUPERSEDED: trap battery caught the cue-laundering regression (cue30 →
  latched 55). v2: parse reverted, `gate_f` at 6 render read sites
  (voice_closed, span_render, base_inc_at, legato inc_to, render_bed,
  build_chains endpitch), respond_latch reads plan truth + nominal/output
  vetoes with GATE-VETO log markers. Binary SHA
  `7d02dc052e377940d201b8e370b332088d1086c014d0e11ab7133867baf49585`
  (87,990 bytes). Source SHA
  `54f156cc438306d12ad1903635eb50beb6858f7cab5c84978394e246560287b9`.
- B-lie: no build (test battery on the B-fix binary).
- Key rerun commands:
  `./src/render_b_fix <plan> <out.mix> seqmix` (mix) / `seq` (wav)
  `./src/render_b_fix <plan> <out.mix> regionmix <k>` (standalone region k)
  `python3 tests/coherence_full.py <wav>`
  `python3 ~/workspace/aud_v10/chop.py <wav> tests/events_complete.txt`
  `gate_bin` = `~/workspace/tnn-lab/imagination_discovery/aud/b_alpha/consistency_gate/src/gate_bin`
- Excerpts rendered to `excerpts/` as `WITHHELD-NOT-FOR-REVIEW_*` (policy:
  never presented to Micah; judgment queue comes first).
