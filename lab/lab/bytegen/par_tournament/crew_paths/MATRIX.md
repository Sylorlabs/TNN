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
| **audio** (siblings) | incumbent | TIE — NO OVERTHROW (crew_a: partial win on quality/coherence/cascade; −46% COST regression blocks §6) | **WIN** — OVERTHROW (crew_b B-fix; release-envelope bug fixed, stands on every §6 bar) | LOSE — NO OVERTHROW (crew_c: stock C fails §5, cue30 confident-wrong latch to 110 Hz; the recommended gate/plan fork is a different mechanism, plan-reference/B-like) | TIE (crew_d: NATIVE keeps) | **WIN** — OVERTHROW (crew_d: caveat closed by native measurement) |
| **image** (raster) | ref | **WIN** — PERM 0 diffs (order-free); COH 0/180 vs nat 72/180 (z-correct); cascade 168 px exact footprint, 1 quadrant | LOSE — cascade 1536 px (whole tile, 9.1× amplification); COH 180/180 | LOSE — same as B on every bar (servo active — bytes differ from B — but changes no outcome) | LOSE — cascade 224 px (blur halo); COH 105/180 | TIE — cascade 168 px exact; 4 plan-latches correct draw/z disagreement at probe pixels; COH 66/180 (still FAIL) |
| **image formation** | n/a (no native formation) | **WIN** — seq/shard/assemble theme plans byte-identical (SHA `0121763f…`); true one-pass formation 0.112 s user CPU (dive's 0.29 s was `render_bin score` double-counting all 224 candidates twice — see RUNLOG); S=2 shards 0.058 s each; S=8 linear projection ≈0.015 s ⇒ ≈7.5× idealized | — | — | — | — |
| **video generative** | ref | **WIN** — frames order-free (scr == seq, 0 diffs; a(scr) byte-identical to nat(seq)); cascade 1 frame; recurrence frame7==frame0 PASS | TIE — cascade 1 frame; COH PASS; **byte-identical to C on this fixture (C servo inert — disclosed, not implied separation)** | TIE — same as B (servo inert here) | LOSE — cascade spreads fault to frames 0–3 (backward smoothing violates containment); recurrence FAIL (frame 0 context-dependent) | TIE — cascade 1 frame; COH PASS; clean render byte-identical to NATIVE (0 latches — verification pass adds safety, changes nothing observable) |
| **video predictive** | ref (tracks: mean 2.77 px) | LOSE as pure PAR (order-free but tracker diverges: mean 4.95 px, final 9.90 px — index-only fiction); A-serialized = byte-identical to NATIVE but concedes parallelism (TIE with extra steps) | LOSE — plan-only state audited clean (zero rendered bytes) but tracker wrong (4.95 px); cannot repair a wrong motion model | LOSE — same as B | LOSE — tracker wrong (4.95 px) + backward smoothing | LOSE — box-fault probe: D2 latched all 8 frames and recovered byte-identically (strict win on fault-recovery) BUT tracking regresses to 4.95 px vs NATIVE's 2.77 px; the recovery win does not compensate the primary-axis regression — no overthrow |
| **dialogue** | ref (5/5) | LOSE — 2/5 (T1,T5); no state → `unknown.` on T2/T3/T4 | LOSE — 3/5 < 5/5; plan entity state resolves ellipsis (T2 "he") but not rendered-wording refs (T3/T4 `unknown.`) — regression on the accuracy axis, no compensating win | LOSE — 3/5; servo inert on fixture (resets to 50/turn, changes no outcome — disclosed) | LOSE — 3/5; backward token pass helps nothing here | LOSE — 3/5 BUT strict win on fault-integrity: T5 post-compose `no,`→`yes,` flip detected, latched, correct answer restored (NATIVE and B emit the corruption); still fails T3/T4 — integrity complement, not overthrow |

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
  (predictive video's nominal velocity) the fault-recovery win does not
  compensate the tracking regression (cell: LOSE); where the win is sub-bar
  (image) it ties. D2's dialogue fault-integrity win likewise does not
  compensate 3/5 < 5/5 (cell: LOSE, integrity complement).
- **Cost honesty (KNOWN DEFECT, unresolved):** the original battery scripts
  (`img_battery.py`, `vidg_battery.py`, `vidp_battery.py`, `dial_battery.py`)
  still use `time.process_time()`, which measures PARENT Python CPU, not the
  Zag child's — every sub-ms per-render figure from those scripts is
  unreliable and must not be cited as child CPU. Valid methods are
  `os.times().children_user + children_system` or `wait4`, with per-child
  RSS (not cumulative `RUSAGE_CHILDREN.ru_maxrss`). The load-bearing image
  FORMATION figure (0.112 s one-pass, 0.058 s shards) used shell user+sys
  timing and stands; all LATENCY-1 figures in this matrix are wall-clock
  `perf_counter()` around direct subprocess calls and stand. Cost
  comparisons await the vidgen scratch-hoisting + timing-method fix rerun.
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
60 s 440 Hz tone, 12×5 s event boundaries, drift 440→451 Hz.
Evidence: fable_chal/evidence/region1.log (CITED), region1_jump.log.
- First metric (windowed quadrature fit) was CONFOUNDED by linear phase drift
  from a ~4 mHz systematic frequency offset in gated-C; the cited metric is the
  drift-immune per-mark phase jump
  `|wrap((φ(tb+5ms)−φ(tb−5ms)) − 2π·f_plan·10ms)|`, validated on synthetic
  continuous (0.0007 rad) vs reset (1.62 rad) steps.
- Cited 11-boundary means (bar: mean<0.1 rad): **B 0.0854 rad PASS**
  (max 0.1345); gated-C 0.1841 FAIL; fable's gfable-C 0.1841 FAIL (identical);
  stock-C 0.4321 FAIL; servo-off 0.1841 FAIL (identical).
- Signed jumps are SYSTEMATIC, not noise: B −0.065…−0.135 rad
  (legato carry), C-family −0.03…−0.39 rad growing with frequency
  (event-rendering path). The C-family step is NOT the servo — gated==off==
  gfable to 4 decimals and the servo logs show zero engagements (gs=0) on
  this clean drift.
- Controls: B's actual regions are 3 s (20 regions), reseed 0.0227 rad;
  single-60 s-event glide control: B 0.0065–0.008 rad (essentially perfect),
  gated-C 0.167 rad (interior estimator noise, no periodic jumps).
- **Verdict: fable's REGION-1 rationale is INVERTED by the data — B beats
  gated-C ~2× on phase continuity and passes the bar C fails.** No matrix
  cell overturned (no contender claimed boundary phase continuity), but the
  B-vs-C separation is now a clean measured audio axis, and the C-family's
  event-start phase step is a real (if sub-kill) artifact. B's win costs
  latency: B is the slowest audio contender (see LATENCY-1).

### LATENCY-1 (real-time rendering viability, wall clock this VM)
Evidence: fable_chal/evidence/latency1.log. Bars: <60 s = 1× RT minimum;
<15 s = RT-capable; >60 s = offline-only.
- AUDIO 60 s: PAR-off 12.87 s, A 0.92 s CPU (cited crew_a, wait4),
  B 19.94 s, stock-C 15.81 s, gated-C 11.84 s, gfable-C 13.51 s,
  D1 10.18 s, D2 9.60 s, native(D) 12.47 s (all rc=0).
  RT-capable: A, gated, gfable, D1, D2, PAR/native. NOT RT-capable:
  B (3× RT) and stock-C (borderline, 15.81 s). Nobody is offline-only.
- IMAGE 96×64 raster (mean/render): nat 17.2 ms, a 55.6 ms, b 48.9 ms,
  c 141.8 ms, d1 19.4 ms, d2 14.2 ms. RT@30fps (33 ms): nat/d1/d2 pass;
  a/b/c miss — C's servo is an 8.2× latency tax over NATIVE.
- DIALOGUE: 46k–81k turns/s all modes (≫ interactive RT).
- TEMPO-1 300f: par 3.5–5.2 s, b 5.4–7.2 s (RT@30fps = 10 s) — both sub-RT.
- SYNC-1: video 1800f ~1.5–2.7 s (~15× RT); audio apar ~3 s (10× RT),
  baudio ~8–10 s (3× RT).
- PREDICTIVE VIDEO 8f: nat 0.108 s, apar 0.027 s, b/c/d 4–5 ms
  (workloads differ: nat is sequential simulation, b/c/d plan-seeded).
- **Verdict: fable's latency point answered with numbers. B's REGION-1
  phase-continuity win comes with the worst audio latency (not RT-capable);
  C's servo costs 8× on image raster. No cell changes.**

### SYNC-1 (cross-path audiovisual synchronization)
30 s bouncing ball @60 fps + "boing" per ground contact. Evidence: sync1.log.
- Determinism PASS on all four renders (video PAR, video servo, audio PAR,
  audio B).
- |boing onset − ball Y-minimum|: PAR-video+PAR-audio mean=0.11 ms
  max=2.76 ms; PAR-video+B-audio identical 0.11/2.76 ms;
  servo-video+B-audio mean=8.07 ms max=8.35 ms.
- Bars: every event ≤50 ms AND mean <10 ms: **PASS all three combos**
  (kill: >50 ms desync — not triggered).
- Near-boundary control (fable's worry: boing 10 ms after B's 5 s reseed):
  apar and baudio both place the 5.01 s boing onset at sample 220941
  exactly — zero reseed delay. Refuted with numbers.
- **Verdict: the per-path map is production-compatible for AV sync.**
  Servo video adds ~8 ms mean offset vs PAR video but stays inside the bar.

### Challenger summary
No matrix cell overturned. TEMPO-1 and SYNC-1 confirm the map (SYNC-1's
near-boundary control refutes the reseed-delay worry with sample-exact
numbers); LATENCY-1 answers the real-time question with numbers — B and
stock-C are ≥1× but not RT-capable on the 60 s audio case, everything else
is; REGION-1 inverts fable's rationale (B passes, C fails) and adds a clean
measured B-vs-C audio axis, with the C-family event-start phase step now a
documented artifact.
