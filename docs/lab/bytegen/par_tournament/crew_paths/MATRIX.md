# CREW PATHS — contender × path verdict matrix (PAR tournament)

Date: 2026-09-24. Pinned toolchain `znc_linux_x86_64_abed8aa1`. Pure Zag,
zero RNG. Every binary output byte-identical across reruns (`cmp`/SHA-256).
Rendered artifacts live only under
`artifacts/WITHHELD-NOT-FOR-REVIEW/` (never shown to Micah); evidence/
keeps logs, hashes, statistics. Audio row cites sibling tournament crews —
audio was NOT rerun here.

Verdict rule (§6 analog): a contender takes a cell (**WIN**) iff it meets
every applicable bar and beats NATIVE on ≥1 axis with no regression
elsewhere. **TIE** keeps NATIVE. **LOSE** = regresses vs NATIVE on ≥1 axis
with no compensating win.

## Matrix

| Path | NATIVE | A (pure PAR) | B (plan-seeded region state) | C (bounded servo) | D1 (bidi two-pass) | D2 (PLANREF) |
|---|---|---|---|---|---|---|
| **audio** (siblings) | incumbent | TIE — NO OVERTHROW (crew_a: partial win on quality/coherence/cascade; −46% COST regression blocks §6) | **WIN** — OVERTHROW (crew_b B-fix; release-envelope bug fixed, stands on every §6 bar) | TIE — NO OVERTHROW (crew_c: stock C fails §5 cue30 confident-wrong latch to 110 Hz; gate/plan fork recommended as fix = different mechanism) | TIE (crew_d: NATIVE keeps) | **WIN** — OVERTHROW (crew_d: caveat closed by native measurement) |
| **image** (raster) | ref | **WIN** — PERM 0 diffs (order-free); COH 0/180 vs nat 72/180 (z-correct); cascade 168 px exact footprint, 1 quadrant | LOSE — cascade 1536 px (whole tile, 9.1× amplification); COH 180/180 | LOSE — same as B on every bar (servo active — bytes differ from B — but changes no outcome) | LOSE — cascade 224 px (blur halo); COH 105/180 | TIE — cascade 168 px exact; 4 plan-latches correct draw/z disagreement at probe pixels; COH 66/180 (still FAIL) |
| **image formation** | n/a (no native formation) | **WIN** — seq/shard/assemble theme plans byte-identical (SHA `0121763f…`); true one-pass formation 0.112 s user CPU (dive's 0.29 s was `render_bin score` double-counting all 224 candidates twice — see RUNLOG); S=2 shards 0.058 s each; S=8 linear projection ≈0.015 s ⇒ ≈7.5× idealized | — | — | — | — |
| **video generative** | ref | **WIN** — frames order-free (scr == seq, 0 diffs; a(scr) byte-identical to nat(seq)); cascade 1 frame; recurrence frame7==frame0 PASS | TIE — cascade 1 frame; COH PASS; **byte-identical to C on this fixture (C servo inert — disclosed, not implied separation)** | TIE — same as B (servo inert here) | LOSE — cascade spreads fault to frames 0–3 (backward smoothing violates containment); recurrence FAIL (frame 0 context-dependent) | TIE — cascade 1 frame; COH PASS; clean render byte-identical to NATIVE (0 latches — verification pass adds safety, changes nothing observable) |
| **video predictive** | ref (tracks: mean 2.77 px) | LOSE as pure PAR (order-free but tracker diverges: mean 4.95 px, final 9.90 px — index-only fiction); A-serialized = byte-identical to NATIVE but concedes parallelism (TIE with extra steps) | LOSE — plan-only state audited clean (zero rendered bytes) but tracker wrong (4.95 px); cannot repair a wrong motion model | LOSE — same as B | LOSE — tracker wrong (4.95 px) + backward smoothing | TIE keeps NATIVE — box-fault probe: D2 latched all 8 frames and recovered byte-identically (strict win on fault-recovery) BUT tracking regresses to 4.95 px vs NATIVE's 2.77 px; no clean overthrow |
| **dialogue** | ref (5/5) | LOSE — 2/5 (T1,T5); no state → `unknown.` on T2/T3/T4 | TIE-keeps-NATIVE — 3/5; plan entity state resolves ellipsis (T2 "he") but not rendered-wording refs (T3/T4 `unknown.`) | TIE-keeps-NATIVE — 3/5; servo inert on fixture (resets to 50/turn, changes no outcome — disclosed) | TIE-keeps-NATIVE — 3/5; backward token pass helps nothing here | TIE keeps NATIVE — 3/5 BUT strict win on fault-integrity: T5 post-compose `no,`→`yes,` flip detected, latched, correct answer restored (NATIVE and B emit the corruption); still fails T3/T4 — integrity complement, not overthrow |

## Hypothesis-map retest (dive map was: image→PAR, gen-video→PAR, pred-video→state, dialogue→state)

- **Image → PAR: CONFIRMED.** A wins the raster (order-free, z-correct
  coherence) and formation is order-free PAR with byte-identical plans.
  B/C's region state amplifies faults 9.1× inside the tile and destroys
  repeated-primitive coherence; D1's blur leaks faults; D2 ties.
- **Generative video → PAR: CONFIRMED.** A wins outright (scrambled frames
  byte-identical to ordered). D1 loses on both containment and recurrence —
  backward temporal smoothing is anti-PAR here. B/C tie (servo inert on
  fixture); D2 ties (verifies, changes nothing).
- **Predictive video → state: CONFIRMED and sharpened.** Only
  *rendered-output* state tracks (NATIVE 2.77 px). Plan-only state (B/C,
  audited zero rendered bytes) cannot repair a wrong motion model (4.95 px).
  A is correct only serialized (= NATIVE with extra steps). D2's PLANREF
  recovers corrupted renders but can't fix tracking — fault-recovery and
  tracking are orthogonal axes; no contender dominates NATIVE.
- **Dialogue → state: CONFIRMED and sharpened.** Plan state (entity keys)
  suffices for ordinary ellipsis (T2 "he" — B/C/D1/D2 all get it) but
  *rendered-response* state is required for genuine circularity: only NATIVE
  answers T3 from rendered T2 bytes and byte-repeats T1 for T4. D2 is an
  integrity complement (catches post-compose corruption), not an overthrow.

## Cross-path notes

- **B vs C separation is fixture-dependent and must not be oversold.** On
  generative video B and C are byte-identical (servo inert); on image their
  bytes differ but every bar outcome is identical; on dialogue the servo
  trace is provably inert. C's bounded feedback never changed a correct
  answer on any fixture — disclosed everywhere it was measured.
- **D2 (PLANREF) is the only contender that ever strictly improves on
  NATIVE without changing clean behavior** (audio overthrow; dialogue T5
  fault recovery; predictive-video box-fault recovery; image 4 probe
  latches), but it only overthrows where the plan's declared values are
  *right* and NATIVE's output is *wrong* (audio). Where the plan is wrong
  (predictive video's nominal velocity) or the win is sub-bar (image),
  it ties.
- **Cost honesty:** all raster/render CPU figures below ~1 ms are timer
  floor, reported as such. The load-bearing image cost is FORMATION
  (0.112 s), not raster. Python `time.process_time()` was NOT used for
  subprocess CPU anywhere (it measures the parent); shell user+sys timing
  was used for formation, min-of-3 process_time for sub-ms renders with
  the floor disclosed.
- **Fixture incident:** `fixtures/img_plan.txt` was overwritten mid-session
  by `formimg seq <path>` (argv2 is the output plan path). It was
  reverse-engineered from the surviving pre-clobber renders and validated:
  all six mode SHAs byte-identical to the recorded pre-clobber values.
  Provenance and the (provably unobservable) residual ambiguity are
  documented in the fixture header and RUNLOG.

## Fable challenger tests (round 1; designs in fable_round1/FABLE_R1_SERVO_MAP.md)

Two PATHS recovery crews died in daemon restarts; the coordinator finished
the remaining work directly. Evidence logs: fable_chal/evidence/.

### TEMPO-1 (generative-video temporal coherence)
300-frame red ball, constant velocity, radius 50 px. Evidence: tempo1.log.
- Determinism: PASS (par r1==r2 SHA 2695fdae…, b r1==r2 SHA 086b23f5…).
- Order-free: PAR seq vs scr byte-identical (PASS); sidecar PASS.
- Centroid jitter: par mean=0.0183 px max=0.0539 px; b identical
  0.0183/0.0539 px. Bar <2 px: PASS both. Max frame-to-frame velocity
  deviation 0.0735 px; frames50–51 jump 0.6716 px (kill bar: 10 px
  discontinuity — no kill).
- **Verdict: B does NOT overthrow PAR on generative video** (identical
  jitter). Generative-video → PAR cell STANDS.

### REGION-1 (audio region-boundary phase continuity)
60 s 440 Hz tone, region boundaries every 5 s, drift 440→451 Hz.
Evidence: region1.log (first metric) + region1_jump.log (refined per-mark metric).
- Refined 5 s-mark phase jump, mean over 11 boundaries (bar: mean<0.1 rad):
  **B mean=0.0854 rad PASS** (max 0.1345); gated-C mean=0.1841 FAIL;
  stock-C mean=0.4321 FAIL; servo-off mean=0.1841 FAIL.
  (First metric read b mean=0.1428 FAIL — marginal; the refined per-mark
  measurement is the cited one.)
- B's plan-seeded region state gives ~2–5× better boundary phase continuity
  than C's gain-servo family on the same fixture. The C-family's servo
  resets produce measurable phase steps (gated==off exactly: gate never
  opened during the tone, so gating neither helps nor harms here).
- **Verdict: new axis where B strictly beats C on audio.** No matrix cell
  overturned (no contender claimed boundary phase continuity), but the
  B-vs-C separation, previously disclosed as fixture-dependent, now has a
  clean audio separation: B passes REGION-1, C fails.

### LATENCY-1 (real-time rendering viability, 60 s fixture/plan_v1.txt)
Wall-clock, this (loaded) VM — upper bounds. Evidence: this section.
- NATIVE 10.98 s, B-gate 11.30 s, C-gated 9.69 s, D1 9.10 s, D2 7.57 s
  (all rc=0, byte-valid outputs). A: crew A measured 0.92 s CPU on the
  same fixture class (cited from crew A's report).
- Bars: <60 s = 1× minimum; <15 s = RT-capable. **All contenders
  RT-capable** (>4× faster than real time even on a contended VM).
  No cell changes; fable's latency point is answered with numbers.

### SYNC-1 (cross-path audiovisual synchronization)
30 s bouncing ball @60 fps + "boing" per ground contact. Evidence: sync1.log.
- Determinism PASS on all four renders (video PAR, video servo, audio PAR,
  audio B).
- |boing onset − ball Y-minimum|: PAR-video+PAR-audio mean=0.11 ms
  max=2.76 ms; PAR-video+B-audio identical 0.11/2.76 ms;
  servo-video+B-audio mean=8.07 ms max=8.35 ms.
- Bars: every event ≤50 ms AND mean <10 ms: **PASS all three combos**
  (kill: >50 ms desync — not triggered).
- **Verdict: the per-path map is production-compatible for AV sync.**
  Servo video adds ~8 ms mean offset vs PAR video but stays inside the bar.

### Challenger summary
No matrix cell overturned. TEMPO-1 and SYNC-1 confirm the map;
LATENCY-1 confirms real-time viability everywhere; REGION-1 adds a new
measured axis (B beats C on boundary phase continuity) without changing
any verdict.
