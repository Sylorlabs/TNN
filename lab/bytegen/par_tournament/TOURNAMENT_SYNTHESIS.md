# PAR Tournament — Definitive Synthesis (2026-09-24)

**Status: DOCUMENTATION ONLY.** This document synthesizes the nine crews'
verdicts as written. No experimental evidence is altered, re-interpreted,
or extended here. Every claim cites the crew verdict that produced it.

**Ground rules (the law, from the frozen prereg):**
`docs/lab/bytegen/par_dive/PREREG_PAR_DIVE.md` — §2 battery, §5 red team,
§6 adoption bars. Pinned toolchain `znc_linux_x86_64_abed8aa1`. Pure Zag,
zero RNG. Every binary output byte-identical across reruns (`cmp`/SHA-256).
Overthrow iff: ≥ all 9 quality bars, coherence ≥ NATIVE, strictly better on
≥1 of {RT-LONG honest-cents, RT-CASCADE, RT-EDGE, COST} with no regression
elsewhere, byte-identical reruns, survives §5 red team. A TIE keeps NATIVE.

**Crews (9/9 complete):** `crew_a`, `crew_b`, `crew_c`, `crew_c_caveat`,
`crew_d`, `crew_gamma`, `crew_paths`, `crew_servo`, `fable_round1`.
Evidence tree: `docs/lab/bytegen/par_tournament/<crew>/{VERDICT,RUNLOG,src,…}`.

---

## 1. Final standings — audio

| Rank | Contender | §6 verdict | One-line evidence |
|---|---|---|---|
| 1 | **D2 PLANREF** (crew_d) | **WIN — OVERTHROW** | 9/9 bars; fixture output bit-identical to NATIVE; RT-LONG honest-cents 0¢/0¢ vs NATIVE **measured** 1200¢/76.96¢ (dive caveat closed by direct native measurement on a pinned-toolchain `render_native`); no regressions; survives §5 |
| 2 | **B-gate** (crew_b) | **WIN — OVERTHROW**; **SHIP CANDIDATE** (audio renderer) | Superset of B-fix: byte-identical output + all bars on the frozen fixture, plus trap immunity B-fix lacks on the nominal/output paths (GATE-VETO nominal/output vetoes nominal lies; END pitches clamped at render; plan truth preserved for the latch). No §6 bar moves. |
| 3 | A (pure PAR) (crew_a) | **PARTIAL WIN — NATIVE keeps** | Strictly better on statelessness-derived properties: exact coherence (1.0000000000, byte-identical windows), RESPND resolution (RT-LONG 440.00 Hz +0.01¢ vs NATIVE 454.38 Hz +55.6¢), fault containment (0/1,190,699 post-fault), 600 s drift-free recurrence (bed ±1.65 ppm both horizons). Loses single-threaded CPU (−46%) and dense-sum headroom (native servo self-limits at 4.79 FS plan-deviation; A clips from N=2). Per the frozen tie rule the throne stays NATIVE. Characterized tradeoff, not a bug. Robustness champion. |
| 4 | C-gated servo law (crew_servo) | **RECOMMENDED servo law** (refinement, not an overthrow axis) | Meets Micah's criterion "no choppiness when unnecessary": on a correct plan the gate kills 97% of servo adapts (137→4) and 96% of gain movement (9.80→0.36 FS) while keeping 100% of the reproducible wins (octave-latch RT-LONG correction, always-on veto, chord/drift behavior). Frozen battery 9/9 on the winner (G-PER 0.350 — exactly at its bar, noted). Primary gate beats fable's two-tier gfable on every scenario (gfable rejected). |
| 5 | C-gate/plan (crew_c fork) | **RECOMMENDED §5 fix for C** | Kills the cue30 attack (abstain→880 via plan-reference range-reject on the true 30 Hz plan pitch); no regressions — base RT-LONG, lies, poly identical; glide and deep-vibrato strictly improve; cost/edge/cascade identical. Caveats: (1) this is B's actual immunity mechanism (plan-reference sensing), confirmed as the load-bearing difference; (2) it is a safety gate, not recovery — renders nominal 880, not the true 30 Hz. |
| 6 | C-deadband (crew_c fork) | **Viable refinement; tie keeps NATIVE** | 9/9 (G-DRIFT/G-PER slightly better), coherence identical, no regressions, rail-pin concern falsified (clamp+contraction are load-bearing, not the deadband). No strict win in any §6 category; cue30 still fails. Frozen tie rule → NATIVE keeps. |
| 7 | GAMMA H2 (crew_gamma) | **Mastering winner** | Fixed, output-independent mastering gain G (recommended `G = 32767/124074 × 0.95 ≈ 0.25089`, integer form `v*31128/124074`, calibrated once on the four-fixture corpus): kills the gamma disease (0 shared-prefix diffs), dynamics bit-exact, one multiply per sample. H1 rejected: 2.8–3.6× over-conservative, mutates plans, 0.17 dB integer-rounding perturbation, needs per-plan census. HIFI/MOOD2 H3 amendments are UNSIGNED DRAFTS — need Micah's signature before they govern. |
| 8 | D1 MR-BIDI (crew_d) | **TIE — NATIVE keeps** | All claims re-verified on the rebuilt binary (source SHA `d6bcb99c…`, unchanged from the dive). The 15 s window-cut extension re-verified as a documented bonus outside §6 (no overthrow). §5 pass-3 red team: plan-determined decisions, no output→content smuggling. |
| 9 | D3 PLANHEAL (crew_d) | **PARTIAL — not an overthrow** | Strictly eliminates ALL damage (in-window included) under the §2-mandated extended fault models (e.g. sustained 1292-block: 0 diffs vs clean — full recovery where D1 confines 82,688 diffs); but 2× COST is a regression on a frozen axis (median 13.45 s vs native 6.06 s; the audit is a second full render). Reported as damage-elimination win + cost trade; NATIVE keeps. Failure modes: F1 blind to faults whose bytes coincidentally equal plan-pure bytes; F2 a lying plan renders its lie (D2's provenance boundary applies); F3 2× cost. |

**Rejected / falsified:** B v1 clamp-at-parse (REGRESSION — laundered the
30 Hz cue into 40 Hz, fired the latch at 880±55 Hz; the trap battery caught
it; shipped v2 gates at render and preserves plan truth for the latch) —
crew_b. C-gate/rg (preregistered no-op, falsified as a fix) and C-gate/cons
(kills cue30 but regresses legitimate 200¢-deep vibrato → abstains to wrong
nominal) — crew_c. fable gfable two-tier (rejected — primary gate wins every
scenario) — crew_servo.

## 2. Champion designs with evidence

### 2a. D2 PLANREF — tournament winner (overall)

Design (crew_d `VERDICT.md`): plan cross-reference, not a pitch meter.
RESPOND := echo the cue's declared pitch. Trusts the plan TEXT (cue EVENT
fields incl. declared f0; the shared parser) and VERIFIES cue audio ==
plan-pure re-render (gate 2). Sub-octave nominal intent is overridden (the
frozen battery defines 460 as a lie — correct-in-battery).

Evidence: DET 4/4 byte-identical; D2-C1 clean mix AND wav bit-identical to
NATIVE (quality/CHOP/coherence identical to NATIVE); RT-LONG original
`LATCHED f0q=28835840` = 440×65536 exact → 0¢ by construction; near-miss
(460) 0¢; NATIVE measured directly this round on `render_native`: renders
nominal 880 → **1200¢** honest error vs true cue 440, near-miss → 76.96¢.
RT-LONG honest-cents scoreboard: D2 0¢/0¢ vs NATIVE 1200¢/76.96¢ — strictly
better on both, measured, no presumption. RT-LONG multi-trap: e=4 dyad
ABSTAIN code=1 → nominal; e=5 latch 440; e=6 latch 523.25 (f0q=34291712
exact). RT-CASCADE frozen 0/64/0; latch still fires on plan_long with
pre-cut-clean window. RT-CASCADE sustained: ABSTAIN code=3 — no pitch
hallucination. RT-EDGE wav bit-identical to NATIVE. Order permutation
seq == rev bit-identical. §5 red team: 5 adversarial plans — emptywin
ABSTAIN code=1; badwin ABSTAIN code=1; nomlie (`1e18` nominal) LATCHED
f0q=28835840 (nominal ignored by design); chain e=1 latch 440, e=2 ABSTAIN
code=1 (no latch-chaining); hugeamp completes, latch fires (integrity gate
survives deterministic wraparound on both sides). No hangs, no crashes.
Sub-octave nominal lies: near-miss latches the cue's declared 440.
Sustained 1292-block corruption: ABSTAIN code=3, no hallucination, damage
not healed (documented).

**Plan-provenance caveat (the tournament's recorded boundary):** D2 trusts
plan text and verifies cue audio == plan-pure re-render; it has no sensor
and no independent access to the trainer's intent. Demo
`plans/plan_adv_f0lie.txt` (cue declares 466.16 — a plan typo for intended
440): D2 latches f0q=30550261 = 466.16×65536 exactly — **0¢ vs the plan's
declaration, 99.99¢ vs the trainer's intent**. Cost of plan-provenance: a
lying/mistyped plan owns D2 completely; D2 cannot distinguish plan-typo
from plan-truth. Safety is plan-provenance all the way down — the plan
author is the trust root, and D2's honesty claim is honestly *relative*:
"0¢ vs what the plan declares," never "0¢ vs the truth." (crew_d)

Honesty notes (carried, still true): D2's "0 cents" is by construction (the
latched value IS the plan's declared Q16 f0), not by measurement — the ZCR
instrument reads −60c on D2's own 440 response, disclosed in every result
file. D2's overthrow is on the audio path only.

### 2b. B-gate — audio ship candidate (renderer)

Design (crew_b `VERDICT.md`): B = PAR render with plan-seeded region state
+ plan-field latch. B-gate = B-fix binary behavior on the frozen fixture
plus a 40–4000 Hz pitch gate on the FULL pitch path: every RENDERED pitch
passes `gate_fg` → [40,4000] Hz; the latch additionally vetoes out-of-range
nominals (`GATE-VETO(nominal)`) and out-of-range latched output
(`GATE-VETO(output)`).

B-fix (the fixture-proven base): the release-envelope fix —
`y=((rel-rem)*1024)/rel` → `y=((rel-rem)*1024)/rel` correction at 4 release
sites (`voice_closed`, `bus_env_at`, `span_render` hot loop, `render_bed`);
nodes now fade full→silent instead of hard-cut. Byte-level proof vs the
dive baseline (`432a55e1…`): 152,657 / 1,323,000 samples differ (11.54%),
every one inside a note release window (per-sample check against all 23
event release windows + the bed release; the 12 apparent outliers were ±1-
sample rounding in the checker, each the first sample of a release window).
0 diffs in attack/sustain/gap audio (pre-release sustain: 0 diffs).
Direction: event-0 release window RMS head500=7,908 / tail500=17,274
(inverted: quiet→loud); B-fix head500=17,668 / tail500=6,802 (true fade:
loud→quiet).

Frozen battery (×2) on B-fix: DET 20/20 byte-identical; G-PER 0.324
(bar ≤0.350, improved); G-STA 1.841 (≤3.000); G-LURCH 2.373 (≤5.000);
G-DRIFT 383.553 (≤800.000, improved); G-FLUXm 213.116 (≤350.000, improved);
G-SIL1/2 0.000/0.000; G-CLIP 0.915 (≤0.950); G-CREST 3.860 (≤14.000);
CHOP-1/2/3: 0 / NONE / 16 spikes, 0 unexplained (vs dive's 33, 0 unexpl.);
coherence xcorr 1.000000 zero-lag; pitch/IOI contour r 1.000000/1.000000;
COST 3.77 s mean interleaved (dive 3.48 s; delta within load noise), RSS
20.1 MB — no regression; RT-LONG 440.00 Hz +0.00¢ (spectral; the autocorr
meter locks the 110 Hz bed — honest note disclosed); RT-LONG near-miss 460
stands, 460.00 Hz +0.00¢; RT-CASCADE 1-bit: 1 diff @ fault sample, 0
post-cut; burst/dropout/DC: 0 post-cut diffs on all three; RT-EDGE: 0
pre-14.8 s diffs, cut step 0 (16-bit units), bed fades to exactly 0; order
permutation rev/stride byte-identical. Red team (densified): R1
cross-region leakage 30/30 PASS; R2 sustained 1292-block corruption 0 diffs
(render never reads the mix — corruption cannot propagate by
construction); R3 plan-text adversarial 14 plans, all rc=0, no hangs,
bounded peaks (fail-open parser documented as unchanged behavior); R4
polyphonic RESPND: abstains, nominal stands; R5 sub-octave nominal lies
(220/110/55, cue 440): latch corrects all to 440 (k=+1/+2/+3).

Trap battery on B-gate v2 (specifically verified): cue 30 Hz / nom 880 →
nominal stands → 880 (cue=30 rejected → nominal stands); cue 5000 Hz /
nom 880 → 880 (cue=5000 rejected → 880); cue 440 / nom 30 → LATCHED 480
(GATE-VETO(nominal) → renders 40); cue 440 / nom 5000 → LATCHED 312
(GATE-VETO(nominal) → renders 4000); cue 4000 / nom 40 → LATCHED 5120
ultrasonic (GATE-VETO(output) → renders 40); END 30 Hz → renders 30,
renders 40 (clamped at synth). Battery: frozen fixture byte-identical to
B-fix (`cmp` clean), 9/9 gates identical numbers, RT-LONG 440.00 Hz +0.00¢.

Verdict (crew_b): B-gate is the SHIP CANDIDATE — identical §6 profile to
B-fix on the frozen fixture (byte-identical output, all bars), plus
strictly better trap immunity on the nominal/output paths that B-fix lacks.
No §6 bar moves. **Recommend B-gate over B-fix for adoption.**

Failure modes (tournament update, crew_b): (1) B-fix/B-gate RESPND trusts
plan cue fields completely — no independent sensor; boundary documented
above. (2) B-gate clamps out-of-range END pitches at render (30→40,
5000→4000) — intended, documented; changes plan-faithfulness for hostile
plans only. (3) Gate edge: 40 Hz cue latches to 55 Hz (in-range per gate).
(4) Octave-rounding boundary razor-thin at exactly 2^-0.5. (5) Unchanged
from dive: no amplitude carry across legato (G-PER tradeoff), fixed 80 ms
legato threshold, fixed 3 s regions, prefix-stimulation cost (closed-form
seed still future work).

B-lie (plan-lie battery, B-fix binary, no code change): nominal lies are
CORRECTED when the cue is true (the latch's purpose — works for ±1/±2
octaves); cue-field lies are UNDETECTABLE by construction (lie3/lie10): B
renders the cue from the same field it latches from — self-consistent,
wrong only vs an external ground truth B cannot observe. Drawn boundary:
B's RESPND is a pure function of plan text (fcue, nom, w0, w1); defenses
are well-posedness checks only: single voice, 40–4000 Hz cue gate, |k|≤10
clamp, 2^-0.5 rounding boundary.

### 2c. A — robustness champion (partial win)

Design (crew_a `VERDICT.md`): pure PAR — the generation path never reads
the mix (pure f(plan,t)). Per-axis scorecard vs NATIVE (frozen battery,
fresh builds, pinned toolchain): DET byte-identical (both); QUALITY 9/9
PASS both (tie); COHERENCE 1.0000000000 byte-identical windows vs 0.736557
(die) — A wins; RT-LONG (RESPND trap) 440.00 Hz +0.01¢ vs 454.38 Hz +55.6¢ —
A wins; RT-CASCADE (4 fault models) 0 post-fault diffs (all) vs 5,854
post-fault diffs — A wins; RT-EDGE (truncation) legitimate-only diffs vs —
PASS; §5 red team survives (6/6 probes) vs — PASS; COST single-threaded
CPU 0.92 s vs 0.80 s → ×1.15 — NATIVE wins; Memory peak RSS 15.3 MB vs
15.4 MB tie; dense polyphony: A clips from N=2 (0.03→0.70!), no adaptation
vs servo halves RMS, darkens, AGC 0.5 floor — NATIVE wins (tradeoff).

Overthrow test: requires all quality bars PASS ✓, coherence ≥ NATIVE ✓,
improvement on ≥1 target axis ✓ (coherence, RT-LONG, RT-CASCADE),
determinism ✓, §5 red-team survival ✓, **and no regression elsewhere** ✗.
A regresses on COST (1.15× single-threaded CPU — the architectural price of
per-sample integer-didactic phase recompute) and on dense-polyphony headroom
(no output-adaptive behavior; the native servo's win for the native side,
at 4.79 FS plan-deviation cost). Two regressions are not a tie — **NATIVE
keeps the throne.**

Forks: A-fmt (parallel formation) — byte-identical shards + speedup_form
≈ 0.75× @ S=8: Identity PASS, speedup FAIL (mechanism proven, no measured
speedup in this implementation/environment; E2E impact nil). A-long (600 s
drift): zero drift ±5 ms, motif recurrence exact: PASS. A-poly (dense
polyphony) — confirmed regression: A clips, no output-adaptive behavior;
native servo self-limits at 4.79 FS plan-deviation.

Verdict (crew_a): A's wins are all consequences of one architectural
property — the generation path never reads the mix (pure f(plan,t)). That
property is proven exactly (0/1,190,699 post-fault, byte-identical 600 s
reruns, max|φ(solo)−φ(chord)| = 0). The losses are the price of that
property: no feedback loop means no cost amortization and no self-limiting.
The tournament should treat this as a characterized tradeoff, not a bug —
neither side is "wrong"; they optimize different things.

### 2d. C-gated servo law — recommended refinement

Design (crew_servo `VERDICT.md`): the primary necessity gate (C-gated).
OPEN: dev = |T−m|·100/max(T,m) > X=15% for Z=3 CONSECUTIVE non-silence,
non-vetoed blocks (69.6 ms persistence). CLOSE: dev < 10% (the stock
deadband) for 10 consecutive blocks (1/2-contraction ⇒ 1024× error
reduction; anti-flap). WHILE OPEN: stock update law UNCHANGED —
g←(g+g·T/m)/2, clamp [0.5,2.0], 10% deadband parks inside. WHILE CLOSED:
gain frozen. ALWAYS: region-boundary reset to unity · silence-hold
(T<SILENCE_FLOOR → st=3, gain held, never chased to the rail) · VETO
always-on (unchanged). VETOED blocks: neither increment nor reset the
open/clear counters. SILENCE blocks: reset the open-persistence counter
(amendment S1 — silence is not evidence of sustained deviation; applied
during recovery for the crew's documented intent, fixing the measured v1
flap false-open). PITCH trigger: N/A — SPEC §1 forbids servo pitch
adjustment; the piece-3 latch owns pitch correction.

Threshold grounding (not magic numbers — standing law): X=15% is above the
measured model-error floor (p90=10.3%, max isolated 25.8%, zero runs ≥3)
and below the veto band (2.5×); Z=3 filters the 27 isolated transient
singles seen on the fixture; the 10-block close is the contraction horizon.
All three come from the Step-2 envelope sweep, not from taste.

Head-to-head (4 builds × 15 scenarios, fresh binaries): nominal 137/0/9.80/
0.106 → gated **4/0/0.36/0.003**; sawbomb 564/0/86.75/0.436 → gated
**4/18/0.36/0.017** (the veto-band-edge attack defeated — 25× engagement
kill; veto hygiene intact); edge14 (+14% sustained) deliberately ignored
(preregistered residual-blindness tradeoff — a threshold must sit
somewhere); drift/flap: gate stays shut correctly (a gain servo must not
"correct" a pitch drift the plan itself contains); g_chord16: 0 adapts
(never opens; RMS(2–5 s)=0.825 FS, peak=2.98 FS preserved).
Phase continuity (fable Q2): build-attributable unexplained phase jump 0 on
all four builds. Frozen battery on gated: 9/9 (G-PER 0.350 at the bar —
the 4 residual adapts move it from stock's 0.333; worth watching, not a
failure). CHOP-3 41→32 total (all event-explained): killing gratuitous
adapts removes flux spikes rather than adding them.

**sus5 divergence (documented):** RT-CASCADE sus5 (5 s storm): gated 43338
post diffs — bounded 55-block missed-adapt window, re-converges, no 2-cycle
— vs stock 0 post. This is the DIVERGENCE from stock: under sustained
measurement corruption the gate parks at unity (vetoed blocks are not
evidence, per prereg) while stock's veto re-measures plan-pure and replays
the full clean-hunting trajectory. The gate working as intended (adds
nothing, renders plan-pure) vs stock replaying 9.80 FS of gratuitous
hunting — the stock "win" that matters (corruption fully absorbed, servo
state protected, no wobble) is kept. **Follow-up NOT implemented — flagged
for Micah (see §5).**

### 2e. GAMMA H2 — mastering winner

Design (crew_gamma `VERDICT.md`): after removing the output-derived
normalizer, the absolute-level strategy question: H1 (re-stage plan
energies for gain 1) vs H2 (one fixed, output-independent mastering gain).
Control = old output-derived peak normalizer.

Evidence: clipping (rail samples ±32767, exact counts, 7 variants × 4
hifi fixtures): ctl song/happy/scary 6825/5257/23338; h1 0/0/0/0; h2a
(G=32767/124074) 0/1/0/0 — the 1 rail sample fails a strict zero-rail bar,
hence the backed-off recommendation; h2c (half) 0/0/0/0; revert
(old normalizer) 0/0/0/0. Plan-dynamics preservation (per-1 s-window RMS
ratio vs control): H1 ≤0.17 dB (integer energy-rounding noise); H2 pure
gain — bit-exact dynamics. The old normalizer erases all inter-render
level relationships (quiet calm scaled UP ×0.8746). Gamma proof (R3
retention): shared-prefix diffs — ctl, h1, h2a–d = 0 diffs; revert =
107,428 diffs (the disease returns exactly as the repair recorded).
Consistency gate: level-invariant bars identical across all variants per
fixture — empirical level-invariance confirmed. Cost: H2 one integer
multiply per sample at emit; H1 zero runtime cost but mutates plans and
needs a per-plan census; revert two-pass, most expensive, diseased.

Recommendation: **H2 wins with a safety margin.** G = 32767/124074 × 0.95
≈ 0.25089 (integer form `v*31128/124074`), calibrated once on the
four-fixture corpus, fixed for all renders — 0 rail samples on the measured
corpus with ~0.45 dB headroom, gamma-clean, bit-exact dynamics.
Conservative alternative: h2c half gain ≈ 0.13206. Honest limit of H2: the
constant is calibrated on the fixture corpus; a future fixture hotter than
happy would touch the rail (graceful clipping, no disease). H1 only if
per-plan zero-rail guarantees without corpus calibration are required.

**Broken governance bars (need Micah-signed amendments before altered bars
govern reruns):** `imagination/HIFI-PREREG.md` H3 (says zero rail samples
and peak ≤24000+1 — broken by the repair: gain-1 renders hit 32768 peak
with 5.896%/4.059%/16.936% at rail on song/happy/scary);
`imagination/MOOD2-RESULTS.md` H3 (says zero rail samples and peak exactly
24000 — broken the same way). UNSIGNED DRAFTS are in the crew verdict;
they are **not law until Micah signs** (see §5).

**Surfaced:** the tournament's own `render_par.zag` `wav_write` carries an
output-derived 0.85-FS peak normalizer (`(mix*27852)/peak`) — the
tournament's own gamma-disease instance, same class as the one just
repaired. Unrepaired at tournament close.

## 3. Settled side items

- **C's CHOP-3 caveat (41 vs 29): SETTLED — NOT-A-REGRESSION** (crew_c_caveat).
  The 12 "extra" flux spikes are not new transients the servo creates. They
  are vibrato-extremum flux peaks that exist in PAR at 92–101% of C's
  magnitude, counted only because CHOP-3's per-file adaptive threshold sits
  11.6% lower on C's render than on PAR's. At a common fixed threshold the
  phenomenon inverts: C 13 vs PAR 29, and no C variant's tallest flux peak
  exceeds PAR's own maximum (0.004701, identical). The dive's disclosure
  "the rest are servo-amplified vibrato extrema" is corrected: C's flux at
  those instants is 0.92–1.01× PAR's — **not amplified**. Accurate
  statement: the servo lowers the whole-file flux floor slightly (median
  0.000789 vs 0.000879), which lowers CHOP-3's adaptive threshold, which
  promotes 9–12 borderline vibrato-extremum peaks over the line. A
  measurement-threshold interaction, not a sonic difference. Ablations:
  C-servo-unity (g≡1) = 29 spikes = PAR exactly, byte-identical to PAR's
  WAV; C-servo-off (frozen target, no dynamics) = 53 spikes AND G-PER FAILS
  (0.362 > 0.350) — the servo's dynamics are load-bearing; C-servo-smooth
  (512-sample ramp) = 36 spikes, 9/9 gates PASS, RT-LONG honest-cents win
  preserved. Red team: 64-sample burst at an adapt boundary → veto fired,
  gain trajectory bit-identical to clean (0/1295 blocks diverged); +0.1 FS
  DC for 2 s → tracked as a level (−33.6% max, bounded), re-settled to ±3
  LSBs within 0.8 s. Audibility: every C-only spike's flux peak exists in
  PAR at 92–101% magnitude, all below PAR's smallest counted spike; the
  C−PAR difference signal is harmonic (<2 kHz: 80–83%), −34 to −42 dBFS —
  intended level correction, not a transient.
- **Fable challenger round 1 (crew_paths/fable_round1): all four closed.**
  TEMPO-1 (generative-video temporal coherence, 300-frame red ball):
  PAR seq vs scr byte-identical; centroid jitter par 0.0183/0.0539 px, B
  identical — bar <2 px PASS both. **B does NOT overthrow PAR on generative
  video.** REGION-1 (audio region-boundary phase continuity, 60 s 440 Hz
  tone, 12×5 s boundaries, 440→451 Hz drift; drift-immune per-mark phase
  jump metric, validated on synthetic continuous vs reset): B 0.0854 rad
  PASS (bar mean<0.1 rad), gated-C 0.1841 FAIL, stock-C 0.4321 FAIL —
  **fable's rationale INVERTED by the data**: B beats gated-C ~2× and passes
  the bar C fails; the C-family's event-start phase step is a real (if
  sub-kill) artifact, growing with frequency on the event-rendering path
  (NOT the servo — gated==off==gfable to 4 decimals, zero engagements).
  LATENCY-1 (wall clock, this VM; bars <60 s = 1× RT minimum, <15 s =
  RT-capable): AUDIO 60 s — A 0.92 s CPU, D2 9.60 s, D1 10.18 s,
  gated-C 11.84 s, PAR-off 12.87 s, native 12.47 s, gfable-C 13.51 s,
  stock-C 15.81 s, B 19.94 s — RT-capable: A, gated, gfable, D1, D2,
  PAR/native; NOT RT-capable: B (3× RT) and stock-C (borderline). Nobody
  offline-only. IMAGE 96×64 raster: nat/d1/d2 RT@30fps pass (17.2/19.4/
  14.2 ms); a/b/c miss (48.9–141.8 ms) — C's servo is an 8.2× latency tax
  over NATIVE. SYNC-1 (cross-path AV sync, 30 s bouncing ball @60 fps +
  "boing" per ground contact): |boing onset − ball Y-minimum| PAR+PAR
  mean 0.11 ms max 2.76 ms; servo-video+B-audio mean 8.07 ms max 8.35 ms —
  PASS all combos (bars: every event ≤50 ms AND mean <10 ms); the
  near-boundary control refutes the reseed-delay worry sample-exactly
  (5.01 s boing at sample 220941 on both renders — zero reseed delay).
  **No matrix cell overturned.** Fable's adversarial take (in
  fable_round1/FABLE_R1_SERVO_MAP.md): the gated servo is a good idea but
  execution underspecified — necessity criterion needs perceptual
  grounding; latency cost must be measured; choppiness standard testable
  but incomplete (add phase continuity); the contender map has one
  likely-wrong cell (generative video) and two missing tests (latency,
  cross-path sync) — LATENCY-1 and SYNC-1 have now answered both.
- **Known measurement defect (standing):** the original battery scripts
  (`img_battery.py`, `vidg_battery.py`, `vidp_battery.py`, `dial_battery.py`)
  still use `time.process_time()`, which measures PARENT Python CPU, not the
  Zag child's — every sub-ms per-render figure from those scripts is
  unreliable and must not be cited as child CPU. Valid: `os.times().children_user
  + children_system` or `wait4`, with per-child RSS. The image-FORMATION
  figure (0.112 s one-pass, 0.058 s shards) used shell user+sys timing and
  stands; all LATENCY-1 figures are wall-clock `perf_counter()` around
  direct subprocess calls and stand.
- **Fixture incident:** `fixtures/img_plan.txt` was overwritten mid-session
  by `formimg seq <path>` (argv2 is the output plan path). Reverse-engineered
  from surviving pre-clobber renders and validated: all six mode SHAs
  byte-identical to the recorded pre-clobber values. Provenance and the
  (provably unobservable) residual ambiguity documented in the fixture
  header and RUNLOG.

## 4. Cross-path map (crew_paths MATRIX — confirmed and sharpened)

Hypothesis-map retest (dive map: image→PAR, gen-video→PAR, pred-video→state,
dialogue→state):

- **Image raster → PAR: CONFIRMED.** A wins outright (order-free, z-correct
  coherence 0/180 vs nat 72/180; cascade exact 168 px footprint, 1
  quadrant). B/C lose (region state amplifies faults 9.1× inside the tile,
  1536 px; destroys repeated-primitive coherence 180/180). D1 loses (blur
  halo 224 px; COH 105/180). D2 ties (cascade 168 px exact; 4 plan-latches
  correct draw/z disagreement at probe pixels; COH 66/180 — still FAIL).
- **Image formation → PAR.** A wins: seq/shard/assemble theme plans
  byte-identical (SHA `0121763f…`); true one-pass formation 0.112 s user
  CPU; S=2 shards 0.058 s each; S=8 linear projection ≈0.015 s ⇒ ≈7.5×
  idealized.
- **Generative video → PAR: CONFIRMED.** A wins (scrambled frames
  byte-identical to ordered; cascade 1 frame; recurrence frame7==frame0
  PASS). D1 loses on containment AND recurrence (backward temporal
  smoothing is anti-PAR here). B/C tie (servo inert on fixture — disclosed,
  not implied separation). D2 ties (verifies, changes nothing observable).
- **Predictive video → state: CONFIRMED and sharpened.** Only
  *rendered-output* state tracks (NATIVE 2.77 px). Plan-only state (B/C,
  audited zero rendered bytes) cannot repair a wrong motion model (4.95 px).
  A is correct only serialized (= NATIVE with extra steps). D2 latched all
  8 frames on the box-fault probe and recovered byte-identically (strict
  win on fault-recovery) BUT tracking regresses to 4.95 px vs NATIVE's 2.77
  px — the recovery win does not compensate the primary-axis regression
  (cell: LOSE). Fault-recovery and tracking are orthogonal axes; no
  contender dominates NATIVE.
- **Dialogue → state: CONFIRMED and sharpened.** Plan state (entity keys)
  suffices for ordinary ellipsis (T2 "he" — B/C/D1/D2 all get it) but
  *rendered-response* state is required for genuine circularity: only
  NATIVE answers T3 from rendered T2 bytes and byte-repeats T1 for T4. D2 is
  an integrity complement (catches post-compose T5 `no,`→`yes,` corruption,
  latches, restores — NATIVE and B emit the corruption), not an overthrow
  (3/5 < 5/5).

Cross-path notes: B-vs-C separation is fixture-dependent and must not be
oversold (byte-identical on generative video; identical bar outcomes on
image and dialogue despite differing bytes). D2 is the only contender that
ever strictly improves on NATIVE without changing clean behavior (audio
overthrow; dialogue T5 fault recovery; predictive-video box-fault recovery;
image 4 probe latches), but it only overthrows where the plan's declared
values are *right* and NATIVE's output is *wrong* (audio).

## 5. Parked for Micah — DO NOT DECIDE without his word

1. **sus5 follow-up design** (crew_servo §4): feed the veto's re-measured
   (bit-exact clean) deviation into the gate FSM instead of skipping vetoed
   blocks. Predicted effect: gated-sus5 post-cut diffs 43338→0 (bit-identity
   with gated-clean). Rejected for now as injecting synthetic evidence into
   the gate; the preregistered rule ("vetoed blocks are not evidence") is
   the current law. A red-team critic may test it as an alternative design
   (see §7); changing the law itself needs Micah.
2. **"Dice"** — Micah's reply to numbered item 1; intended meaning was
   unclear and must not be interpreted without clarification. (memory/2026-09-24.md)
3. **HIFI/MOOD2 H3 amendments** — UNSIGNED DRAFTS (crew_gamma §9). Not law
   until Micah signs. The broken bars: HIFI H3 "zero rail samples and peak
   ≤24000+1" and MOOD2 H3 "zero rail samples and peak exactly 24000" — both
   broken by the gamma repair (gain-1 renders hit 32768 peak with
   5.896%/4.059%/16.936% at rail on song/happy/scary).
4. **Carried rulings (no re-litigation):** the unphony-loop + new-audio-clips
   round is a FAIL — same as last time, changed notation only (Micah's
   ears, 2026-09-24). Standing requirement: audio analyzer-first (HNR,
   spectra, envelope stationarity, spectral drift, loop-periodicity,
   transient regularity, hum/tonal incl. 50/60 Hz + harmonics), measured
   delta vs the previous version, and SHA-256 identity check on every
   delivered file — no clip reaches Micah without analyzer evidence of a
   real change. Fable must deeply investigate why the loop stays the same;
   TNN should get more inspiration.
5. **Red-team verdict rule (Micah, 2026-09-24):** critics and anti-approach
   skeptics may try to do something better. If they beat B-gate/D2 on the
   frozen battery with preregistered kill bars, the verdict in this
   document changes; if they fail after genuine attempts, confidence in the
   champions rises. Both outcomes are wins. See §7.

## 6. Verdict-status rules

- D2's overthrow stands on the audio path only; the plan-provenance caveat
  (§2a) is part of the verdict, not an asterisk on it.
- B-gate is the recommended audio renderer for adoption (superset of B-fix;
  identical fixture behavior; vetoes the nominal/output traps B-fix falls
  for). B-fix's overthrow verdict stands independently on every §6 bar.
- The gated servo law is a recommendation, not an adoption: it needs the
  sus5 follow-up decision (§5.1) and Micah's word before it governs
  production renders.
- GAMMA H2 is the mastering winner; the H3 amendments are unsigned.
- A stays the robustness champion; NATIVE keeps the audio throne against A
  per the frozen tie rule, and against D1/D3.
- The cross-path map (§4) is the tournament's final hypothesis verdict.

## 7. Red-team phase (open)

Per Micah's 2026-09-24 directive, critics of the PAR approach — including
those who hold B-gate/D2 is the WRONG direction — are dispatched with a
mandate to DO SOMETHING BETTER: alternative designs, preregistered kill
bars, the same fixtures, pure Zag, zero RNG. If they beat B-gate/D2, the
verdict in this document changes; if they fail after genuine attempts,
confidence in the champions rises. Results are recorded as they land.

---
*Document written 2026-09-24 from the nine crews' VERDICT.md files as
committed. Evidence: `docs/lab/bytegen/par_tournament/<crew>/`. This file
changes no evidence.*
