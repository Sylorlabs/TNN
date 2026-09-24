# CREW C — PAR tournament runlog (coordinator round)

Crew: C (bounded-feedback AR, Grok H3). Contender: C + forks.
Task: test ALL FOUR contenders' worth of battery on C — full frozen §2 battery + §5 red team — on stock C and every fork.
Workdir: `~/workspace/tnn-lab/bytegen/par_tournament/crew_c/`.
Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Fixture: `~/workspace/tnn-lab/bytegen/fixture/plan_v1.txt`.
Excerpt policy: excerpts only into `par_tournament/crew_c/excerpts/` labeled WITHHELD-NOT-FOR-REVIEW. NEVER present clips to Micah.

Prior dive (reference, not re-litigated): `par_dive/contender_c/` (SPEC.md, RESULTS.md, REDTEAM_C.md).
C-CAVEAT (separate crew) owns the CHOP-3 41-vs-29 servo-flux-spike regression question — DO NOT duplicate their experiment. Share rebuilt-C binary/source notes with them here (§8).

## 2026-09-24 — setup + rebuild stock C

- [ ] Rebuild stock C from frozen source (`par_dive/contender_c/src/render_c.zag`), verify source SHA-256 = `0640f28f...a26c6d3db`, prove byte-identical reruns (mix level, `cmp` clean).
- [ ] Re-run frozen §2 battery on rebuilt stock C (DET/QUALITY/COHERENCE/COST/RT-LONG/RT-CASCADE/RT-EDGE/FAILURE MODES) + densified §5 red team.

## Preregistered fork claims (written BEFORE building any fork)

### Fork C-gate — range-gated ZCR pitch path
Source delta vs stock: apply the 40–4000 Hz range gate to the ZCR-derived pitch `fm` on the pitch path (abstain from the octave latch when the raw ZCR-implied frequency is out of range), instead of only inside the latch decision.
Claim G1 (dive's candidate fix, honest prediction): the 30 Hz harmonic trap does NOT die — the trap's false reading (fm=79 Hz) is in-range, so the gate is a no-op on every existing RESPOND trace; cue30 still latches 880→110 Hz. RT-LONG +0.1¢ survives unchanged (fm=456 in-range).
Claim G2 (mechanism note): B's immunity is plan-reference immunity, not gate immunity — B reads the plan cue pitch (30<40 → reject). C's sensor cannot see 30 Hz through its harmonics.
Follow-up variants (same fork family, preregistered): C-gate/cons (consistency gate: latch only if the ZCR measurement agrees with the octave-implied pitch within ±200¢ — predicted to kill cue30 but break vibdeep, which currently latches correctly at 474¢ measurement distortion) and C-gate/plan (B-style: read the cue's plan pitch, range-gate it, octave-correct against it — predicted to kill cue30 AND keep RT-LONG/vibdeep). All three run the full RESPOND battery (octlie, octlie_low, 2oct, nearmiss, poly, vibdeep, glide, cue30, cue5000, harm13).

### Fork C-deadband — 5% deadband
Source delta vs stock: `DEADBAND_PC` 10 → 5.
Claim D1: more adaptations on the fixture (model error 5–10% now acted on), gain parks inside ±5%; quality gates still pass; CHOP-3 spike count does not decrease (servo steps more often — predicted flat or slightly worse flux count).
Claim D2 (tradeoff): on adversarial rail texts (rail1/rail2/ramp) the gain stays bounded by the same clamp [0.5,2.0] and contraction — the deadband is NOT the rail-pin defense's load-bearing wall, so narrowing it does not open a pin; it only raises adaptation count. Quantify: gain range + adapt count on rail1/rail2 for 10% vs 5%.
Claim D3: the known deadband-blindness weakness (≤10% model error never corrected) shrinks to ≤5% — a 9%-off plan now converges toward the analytic target instead of keeping the offset forever.

### Fork C-poly — polyphonic RESPOND battery
Source delta vs stock: NONE (stock C binary). This fork is a test battery, not a code change: where does the servo/latch pitch inference break under polyphony?
Claim P1: the latch abstains (nvoice≠1 → rsn=0) on all true polyphonic cues — no hallucinated pitch, nominal kept. Break point predicted at masking: a loud second voice that ENDS before the cue window still counts (overlap test is on [w0,w1)) — verify; and octave-dyad cues (440+880) where ZCR-of-sum might read a single harmonic series.
Claim P2 (dive forensics §3): ZCR-of-sum on dyads reads the perceptual "missing fundamental" inconsistently vs the latch's nvoice gate — document where the two disagree; the servo itself does no pitch inference (gain only) so it cannot break here, only the latch can.

## Battery plan per binary (stock C, C-gate×3 variants, C-deadband; C-poly uses stock binary + new plans)

- DET: 2× `seqmix` renders of fixture, `cmp` clean (mix level).
- QUALITY: 9 V10 gates (`aud_v10` defs) + CHOP-1/2/3 via `~/workspace/aud_v10/chop.py` with the complete 271-event list, on the WAV render.
- COHERENCE: `tests/coherence_c.py` (motif 2.0–5.4 s vs 24.0–27.4 s; zero-lag + ±50 ms max-lag xcorr + pitch/IOI/centroid contour correlations).
- COST: 5 interleaved runs each vs stock; wall-clock + peak RSS.
- RT-LONG: cue 440 @ t=1, RESPOND @ t=28 nominal 880 → cents error (honest: ZCR pitch meter on response window); variants: 460 near-miss, 220 sub-oct, 1760 2-oct, vibrato, glide, poly, cue30.
- RT-CASCADE: `faultmix` (64-sample XOR @ t=3 s) → post-cut diff count (mix level); EXTEND: burst (multi-block), dropout (full-block zero), DC-shift fault models.
- RT-EDGE: plan truncated @ 15 s → first-diff sample vs full plan; legitimate (release tail) vs illegitimate; CHOP-1 on cut renders.
- FAILURE MODES: documented per binary.
- §5 red team (densified): cross-region leakage probe at EVERY boundary (6 regions → per-boundary diff counts, not just one cut); sustained 1292-block re-verify (gain trajectory bit-identical to clean); plan-text rail pins (rail1/rail2/ramp/alt/stationary); polyphonic RESPOND; sub-octave lies; vibrato/glide vs ZCR.

## §6 verdict frame (per binary): ≥9/9 bars, coherence ≥ NATIVE, strict win ≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE, COST} with no regression elsewhere, byte-identical reruns, §5 survival. Tie keeps NATIVE.

## Log
(append entries below as work lands)

### 2026-09-24 — Stock C full battery (rebuilt binary, pinned toolchain)
- Source SHA `0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db` — matches frozen dive SHA exactly.
- DET: 2× seqmix renders, `cmp` clean; SHA `7472ad89f8102b03c72111c3be2511279b77ddc65e07e55a07579181c84a838c`. Trace: blocks=1295 vetoes=0 adapts=137 latched=0 kept=0.
- QUALITY (WAV): 9/9 PASS — G-PER 0.333, G-STA 2.020, G-LURCH 2.518, G-DRIFT 477.143, G-FLUXm 242.649, G-SIL1 0.000, G-SIL2 0.000, G-CLIP 0.849, G-CREST 4.324.
- CHOP (events_complete.txt, 296 lines): CHOP-1 0 PASS, CHOP-2 none PASS, CHOP-3 41 total / 0 unexplained. Reproduces the known C-CAVEAT item; no separate caveat experiment run.
- COHERENCE: xcorr 1.000000 / 0.999999 (lag 0); pitch/centroid/IOI 1.000000; onsets 10/10.
- RESPOND (11 plans, FFT fundamental as honest pitch meter; latch ZCR kept as detector report): base 440→440 ✓; 460 near-miss→460 ✓; 220 lie→440 ✓; 1760 lie→440 ✓; cue30: fm=79 k=-3 → LATCH 110, measured 110.00 Hz (ATTACK WORKS); cue5000→880 ✓; glide→880 (rsn=1) ✓; harm13 110/220→110 ✓; heavy vibrato→440 ✓; poly nvoice=2→abstain 880 ✓.
- Measurement lesson: full-window ZCR/autocorr contaminated by 110 Hz bed; FFT peak 50–2000 Hz is the honest output-pitch meter (1 Hz resolution → reports 440.00 vs dive's 440.02).
- RT-CASCADE (region-aware block boundaries; region 1 blocks start at 88200+43×1024=132232, NOT 132096): fault 0 post-fault diffs; dropout (veto=1) 0; burst 8 blocks (veto=8) 0; dcshift +16FS (veto=1) 0. Corrupted bytes persist by design; servo state fully protected.
- Footgun hit & fixed: new modes `burstmix`/`dcshiftmix` were missing from the mix_write dispatch → silently wrote WAV (44-byte header + int16), producing 2646044-byte "truncated" files. This is the exact redteam-documented mode-dispatch footgun. Fixed by adding both modes to the dispatch list; rebuilt render_c_fx.
- RT-EDGE (fixture truncated @ 15 s, BED 0–15, events t0<15 kept): first diff at 14.975 s = the bed's 25 ms edge fade (legitimate content difference); 0 diffs before 14.9 s. Servo is causal; truncation does not leak backward.
- Densified cross-region leakage (6 regions @ 0/2.0/6.0/9.5/16.0/24.0 s): 5 adversarial plans, each smuggling a loud 880 Hz amp-3000 event just before one internal boundary without altering region structure (verified regions=6 identical). Post-smuggle gain traces vs clean: b1: 1208 blocks 0 diffs; b2: 1035/0; b3: 884/0; b4: 604/0; b5: 259/0. No earlier-region state leaks into later-region servo.
- sus1292 re-verify: 1295/1295 block gains bit-identical clean vs sustained-corruption; 1295 vetoes; gain range under attack 0.8763–1.1574.
- COST: median 11.63 s (min 8.27, max 15.93), peak RSS 15832 KB. No /usr/bin/time on VM; used wall-clock + /proc VmHWM polling (cost.py).
- Gain range (fixture): [0.8763, 1.1574]; all 1295 within clamp [0.25, 4.0]. No rail-pin.

### 2026-09-24 — C-gate/rg (explicit measured-path range gate)
- Source SHA `82a0911125ab1274ffdeb8632828329816c2e77b11f985ff3e573c667d506c71`. Compiled clean.
- Fixture mix: byte-identical to stock (SHA 7472ad89…); rerun cmp clean.
- RESPOND: identical to stock on all 11 cases. cue30: fm=79 → LATCH 110, measured 110.00 Hz. The explicit range gate is a NO-OP — the false 79 Hz reading is already in-range. Preregistered prediction confirmed. REJECT as a fix.

### 2026-09-24 — C-gate/cons (±200¢ consistency gate)
- Source SHA `01ae76ab1431cf2d137a8ced10e04e3feff8dff4493d4d263698d45f87f487a2`. Compiled clean.
- Fixture mix: byte-identical to stock; rerun cmp clean.
- RESPOND: base RT-LONG survives (440). cue30: rsn=5 abstain → renders nominal 880, measured 880.00 Hz (trap killed via abstention).
- TRADEOFF (preregistered concern confirmed): deep-vibrato probes (8 Hz @ 200¢/300¢/400¢, cue 440): stock latches correctly to 440 at 200¢ (fm=530/590, k=-1); cons ABSTAINS (rsn=5) at 200¢ → renders 880. At 300¢+ both keep nominal (k=0). So cons breaks a legitimate case stock handles. REJECT (regression elsewhere).

### 2026-09-24 — C-gate/plan (B-style plan-reference + range gate)
- Source SHA `3560d538a6bc1feaff947dfda5686a0a7ee6f1c81bc14d814e8796f683710033`. Compiled clean.
- Fixture mix: byte-identical to stock; rerun cmp clean.
- RESPOND: cue30 → reads plan cue 30, range-rejects → 880, measured 880.00 Hz. cue5000 → 880. Glide: LATCHES 440 (stock abstains → 880). Deep vibrato at ALL depths → 440 (fixes the 300¢+ nominal-fallback). Poly still abstains (nvoice=2). All other cases match stock.
- Strongest gate variant; changes mechanism from output sensing to plan-reference sensing (this is B's actual immunity mechanism). Caveat: does not render the true 30 Hz — a safety gate, not a recovery.

### 2026-09-24 — C-deadband (5% deadband)
- Source SHA `b1294126bd7c82e878157516a201a90c58d40afa8099d9188606f98e1555d431`. Compiled clean.
- DET: 2× renders cmp clean; SHA `936566e36de0782849bc8c1ee2584a7dd21ada6ed99faeeef6391f169c8b42d2`. Trace: blocks=1295 vetoes=0 adapts=513 (vs stock 137).
- QUALITY: 9/9 PASS — G-PER 0.324, G-STA 2.152, G-LURCH 2.642, G-DRIFT 404.902, G-FLUXm 245.019, G-SIL1/2 0.000, G-CLIP 0.850, G-CREST 4.442. (G-DRIFT and G-PER slightly better than stock.)
- CHOP: 0 / none / 41 total 0 unexplained — identical to stock.
- COHERENCE: 1.000000 / 0.999999, all contours 1.0, 10/10 onsets — identical to stock.
- Gain range: [0.8801, 1.1896] vs stock [0.8763, 1.1574]; all within [0.25, 4.0]. No rail-pin.
- Rail probes (stock→db adapts, vetoes=0 both): rail1 5→8, rail2 7→22, ramp 23→67, alt 5→10, stationary 103→294. Preregistered rail-pin concern does NOT materialize — clamp+contraction are the load-bearing walls, not the deadband.
- RESPOND: all 11 cases identical to stock, including cue30 → LATCH 110 (latch path untouched; deadband is a servo refinement, not a §5 fix).
- Output vs stock: max abs diff 3012 Q16 units (1.4e-6 FS), mean 220 — real but tiny.
- RT-EDGE: first diff 14.975 s, 0 before 14.9 s — identical to stock.
- COST: median 11.62 s, RSS 15832 KB — identical to stock.

### 2026-09-24 — C-poly (stock binary + 7 polyphonic plans)
- Octave dyad 440+880, detuned unison 440+445, triad, loud+quiet, partial overlap, edge overlap, loud-voice-ends-before-window: ALL true overlaps → nvoice=2/3 → abstain → nominal. Even a quiet second voice triggers abstention (count-based, not audibility-based). Loud voice ending before [1,2) → nvoice=1 → correct 440 latch.
- Failure mode is conservative blindness (nominal fallback), NOT hallucinated ZCR-of-sum pitch.

### 2026-09-24 — Cue30 measured outputs (FFT, honest)
- stock: 110.00 Hz (wrong latch) | gate_rg: 110.00 Hz (trap survives) | gate_cons: 880.00 Hz (nominal) | gate_plan: 880.00 Hz (nominal).
- Red-team criterion: the attack's power is the CONFIDENT WRONG latch (110 Hz = neither cue 30 nor nominal 880). Abstention to nominal is the safe failure mode. No fork renders the true 30 Hz.

### 2026-09-24 — Rebuilt-C source/binary notes (for C-CAVEAT)
- All binaries rebuilt 2026-09-24 with pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` from the sources above (SHAs listed per fork). Stock source SHA matches the frozen dive SHA exactly.
- `render_c_fx.zag` (SHA `b8d95c6523b4cf5d95124d928096675f9b5a8fa04cbb40413383d072a05843a8`): stock + burst/dcshift fault-injection modes + fixed mix_write dispatch. In clean seqmix mode it is BIT-IDENTICAL to stock (0 diffs over 1323000 samples).
- Do NOT commit: binaries, `.zag-cache/`, `.zagd.semantic-ready` under `crew_c/src/`.
