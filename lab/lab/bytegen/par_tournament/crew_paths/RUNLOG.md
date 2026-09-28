# CREW PATHS — run log (PAR tournament, coordinator round)

Task: per-path × contender verdict matrix. Rows: audio (cite siblings, no
re-run), image, video-generative, video-predictive, dialogue. Columns:
NATIVE, A, B, C, D1, D2.

Contender mapping per path (documented, not silent):
- **NATIVE**: the surveyed native pattern per path — image: sequential
  draw-order raster with local carried state, fresh buffers per image
  (`imagination/design/render.zag` pattern; characterization §7); generative
  video: per-frame pure function of frame index, frames rendered in order
  (`imagination_discovery/vid/ocean.zag::o_emit_frame` pattern); predictive
  video: carried output-derived state (frame f+1 planned from rendered frame
  f); dialogue: full conversational state carried
  (`dialogue.zag::do_compose` + salience/history pipeline).
- **A**: pure PAR end-to-end (plan events independent, render = f(plan,x)
  with zero carried state; image pixels evaluable in any order; video frames
  in any order; dialogue turns from the query alone).
- **B**: PAR render, plan-seeded region state (carried state allowed, seeded
  ONLY from the plan at region boundaries — never from prior output; wiped +
  reseeded per region).
- **C**: bounded-feedback servo (region-scoped, plan-derived targets,
  boundary state reset; continuous feedback allowed ONLY intra-region).
- **D1**: bidirectional two-pass (forward plan pass + backward smoothing /
  consistency pass; no output→content feedback).
- **D2**: PLANREF (render, re-render-verify against the plan's declared
  values, latch the plan's value on mismatch — abstain-or-correct).

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned). Pure Zag, zero RNG (deterministic integer hashes / fixed
permutations only). Byte-identity proven by `cmp`/sha256.

## Batteries (adapted from the audio §2 frozen battery — bars explicit)

### IMG (image) — fixture `fixtures/img_plan.txt` (frozen)
Canvas 96×64. Primitives: rect/circle with explicit z; file order ≠ z-order
on one overlap (separates nat draw-order from PAR z-order); one primitive
repeated at two offsets (coherence probe); primitives span all quadrants.
- **IMG-DET**: two renders, `cmp` clean → PASS/FAIL.
- **IMG-PERM**: render with scrambled pixel-evaluation order (fixed
  permutation p(i)=(i·2654435761) mod N, coprime to N) `cmp` vs canonical →
  PASS iff byte-identical. (A must PASS; others reported.)
- **IMG-LEAK** (B/C): poison region-0 state (marker), render, count pixels
  differing vs clean OUTSIDE region 0 → PASS iff 0.
- **IMG-CASCADE**: flip one primitive's color (single-region corruption);
  count quadrants (of 4) with >0 differing pixels vs clean → report (1 =
  contained).
- **IMG-COH**: repeated primitive at two offsets → extract both pixel blocks
  → PASS iff byte-identical.
- **IMG-COST**: min-of-3 CPU user+sys seconds + peak RSS (KB, `/usr/bin/time -v`).
- **IMG-FAIL**: documented failure modes per contender.

### IMG-FORM (image plan formation — Micah's "plans parallelly")
Real code: `score_candidate`/`theme_candidate`/`v1_winner` from
`imagination/design/screens.zag` (224 candidates, strict-> argmax).
`seq`: in-order scan → winner theme plan file. `shard s S`: strided scan,
local best with (score desc, idx asc) tiebreak → prints BEST idx score.
`assemble`: order-free reduce of S shard bests → winner theme plan file.
- Bar: `cmp plan_seq plan_par` clean (incl. scrambled shard input order).
- Re-measure: formation CPU vs real render CPU (`render.zag render v1 lib`),
  formation:render ratio, per-shard CPU ≈ T_seq/S, end-to-end win at S=8
  (dive claims ~5.5×, 19:1 — re-measured, not quoted).

### VIDG (generative video) — fixture in `src/vidgen.zag` + `fixtures/vidgen.txt`
8 frames 64×48; frame plan = pure function of frame index (scene params via
deterministic integer hash); frame 7's plan forced == frame 0's plan
(recurrence probe).
- **VIDG-DET / VIDG-PERM** (frames in scrambled order `cmp` clean),
  **VIDG-CASCADE** (corrupt frame 3's plan → count affected frames; PAR bar: 1),
  **VIDG-COH** (frame 7 vs frame 0 byte-identical), **VIDG-COST**.

### VIDP (predictive video) — fixture in `src/vidpred.zag`
8 frames 64×48. World: bright blob moves with TRUE velocity (3,1) px/frame.
Frame f+1's plan = tracker box at centroid of brightest 8×8 block of
RENDERED frame f (genuine output→plan dependence). Plan's nominal velocity
(2,2) is deliberately wrong — truth is visible only in rendered bytes.
- **VIDP-DET**, **VIDP-TRACK** (mean |box−blob| px over frames; nat = 0 by
  construction), **VIDP-PAR** (can frames render in scrambled order and stay
  correct?), **VIDP-CASCADE** (corrupt frame 2's plan blob color → count
  frames with diffs; nat is EXPECTED to propagate — genuine state cost),
  **VIDP-STATE** (audit B/C carried state = plan-derived only, no rendered
  bytes — dump + verify), **VIDP-COST**.
- A's two horns documented exactly (serialize = concede parallelism;
  parallel = plan-fiction tracker divergence, measured).

### DIAL (dialogue) — fixtures `fixtures/dial_kb.txt`, `dial_turns.txt`,
`fixtures/dial_expected.txt` (frozen)
4 turns: (1) plan-derivable comparison question; (2) ellipsis "he" (resolvable
from plan-seeded entity state OR rendered history); (3) "third word of your
last answer" (genuine circularity — needs rendered bytes); (4) "repeat your
answer to the first question exactly" (needs rendered bytes). Turn 5
(red-team): byte-flip fault on the composed response (yes→no) → D2's
re-verify-and-latch vs others.
- **DIAL-DET**, **DIAL-TURN** (per-turn expected answers, pass/fail each),
  **DIAL-CIRC** (turn 3), **DIAL-CARRY** (turn 2), **DIAL-REDTEAM** (turn 5
  fault), **DIAL-STATEMIN** (minimal carried state documented per contender),
  **DIAL-SERVO** (C: does bounded feedback change any correct answer?),
  **DIAL-COST**.

### Verdict rule (tournament §6 analog)
A contender takes a path cell (WIN) iff it meets every applicable bar above
and beats NATIVE on ≥1 axis with no regression elsewhere; TIE keeps NATIVE.
Cells: WIN / TIE / LOSE / PENDING with one-line evidence.

## Progress
- 2026-09-24: workspace scaffolded; batteries defined above; building sources.

## Recovery log (coordinator, 2026-09-24 ~18:45 UTC)
The first PATHS crew (interrupted ~17:32) left MATRIX.md complete but no
challenger tests run and nothing committed. Two recovery crews died in
daemon restarts ("no live runtime handle") at 18:19 and 18:44.
Recovered state before the deaths: fable_chal/src/tempo.zag+tempo1.zag
(built, ran — evidence/tempo1.log), region1.zag+region1_analyze.py (built,
ran — evidence/region1.log, region1_jump.log), syncav.zag+syncav binary
(built, ran — evidence/sync1.log). The coordinator verified these logs
were produced by the current sources (tempo1.zag rebuild reproduces
tempo1.log SHAs; syncav/region1 binaries match their .zag sources by
rebuild) and adopted them.
Remaining work done directly by the coordinator:
- LATENCY-1: timed the 60 s fixture/plan_v1.txt renders on this VM:
  NATIVE 10.98 s, B-gate 11.30 s, C-gated 9.69 s, D1 9.10 s, D2 7.57 s
  (rc=0 all; wall-clock upper bounds on a loaded VM). A cited from crew
  A's report: 0.92 s CPU. All <15 s → RT-capable.
  ⚠ SUPERSEDED — see "Challenger verification pass (2026-09-24 ~19:30 UTC)"
  below. Those figures do not reproduce; the re-measured table stands.
- MATRIX.md: added "Fable challenger tests" section (TEMPO-1, REGION-1,
  LATENCY-1, SYNC-1) with verdicts. No matrix cell overturned; REGION-1
  adds a new measured axis (B passes boundary phase continuity, C fails).
- This commit: MATRIX.md, RUNLOG.md, fable_chal/src/{tempo1,region1,syncav,tempo}.zag.
  Binaries, .zagd, .zag-cache, .mix, .log, evidence/*.log NOT committed.

## Challenger verification pass (coordinator, 2026-09-24 ~19:30 UTC)
Re-ran and hardened all four fable challenger tests; corrected the record
where the earlier entries were wrong or unvalidated.

REGION-1 — method fix (the load-bearing correction of this pass):
- Found B's `.mix` is i64 LE samples, not f64 (read render_b_fix.zag
  `mix_write`: `put64` per sample). The earlier analysis decoded f64 and
  produced NaN; the first committed metric then used a windowed-fit phase
  comparison that was CONFOUNDED by linear drift from a ~4 mHz systematic
  frequency offset in gated-C (1.6 rad over 58 s on a glide control).
- Cited metric now: drift-immune per-mark phase jump
  `|wrap((φ(tb+5ms)−φ(tb−5ms)) − 2π·f_plan·10ms)|` (region_jump.py),
  validated on synthetic continuous (0.0007 rad) vs reset (1.62 rad).
- Results (12×5 s events, 440→451 Hz): B 0.0854 rad PASS (<0.1);
  gated-C 0.1841 FAIL; fable's gfable-C 0.1841 FAIL (identical);
  stock-C 0.4321 FAIL; servo-off 0.1841 FAIL.
  Signed jumps are systematic: B −0.065…−0.135 (legato carry),
  C-family −0.03…−0.39 growing with f (event-rendering path, NOT the
  servo — gated==off==gfable to 4 decimals, gs=0 zero engagements logged).
- Controls: B's real regions are 3 s (20), reseed 0.0227 rad; single-60 s
  event glide: B 0.0065–0.008 rad, gated-C 0.167 (estimator noise, no
  periodic jumps on fine grid).
- Fable's REGION-1 rationale is INVERTED by the data: B beats gated-C ~2×
  and passes the bar C fails. Renders + evidence in
  fable_chal/artifacts/WITHHELD-NOT-FOR-REVIEW/region1/ (never shown).

LATENCY-1 — re-measured, earlier table superseded:
- The 18:45 figures (NATIVE 10.98 s, B-gate 11.30 s, C-gated 9.69 s,
  D1 9.10 s, D2 7.57 s) DO NOT REPRODUCE and are withdrawn. They may have
  come from a different fixture or an unrecorded run; the re-measured
  table below (wall-clock perf_counter, rc=0 all) stands.
- AUDIO 60 s (fixtures_region1.txt): PAR-off 12.87 s, B 19.94 s,
  stock-C 15.81 s, gated-C 11.84 s, gfable-C 13.51 s, D1 10.18 s,
  D2 9.60 s, native(D) 12.47 s; A 0.92 s CPU cited (crew_a/RUNLOG.md, wait4).
  RT-capable (<15 s): A, gated, gfable, D1, D2, PAR/native.
  ≥1× but NOT RT-capable: B (3× RT), stock-C (borderline 15.81 s).
- IMAGE raster (mean/render): nat 17.2 ms, a 55.6 ms, b 48.9 ms,
  c 141.8 ms, d1 19.4 ms, d2 14.2 ms. RT@30fps: nat/d1/d2 pass; a/b/c
  miss (C's servo = 8.2× latency tax over NATIVE).
- DIALOGUE: 46k–81k turns/s all modes. TEMPO-1 300f: par 3.5–5.2 s,
  b 5.4–7.2 s (RT = 10 s). SYNC-1 video 1800f ~1.5–2.7 s (~15× RT);
  audio apar ~3 s, baudio ~8–10 s. VIDPRED 8f: nat 0.108 s, apar 0.027 s,
  b/c/d 4–5 ms (workloads differ by design).

SYNC-1 — confirmed + near-boundary control:
- All four renders deterministic (cmp/SHA PASS). PAR+PAR 0.11/2.76 ms,
  PAR+B-audio 0.11/2.76 ms, servo-video+B-audio 8.07/8.35 ms — all PASS.
- Fable's near-boundary worry (boing 10 ms after B's 5 s reseed) REFUTED:
  apar and baudio both place the 5.01 s boing at sample 220941 exactly.

TEMPO-1 — confirmed: par/b deterministic, order-free par, jitter
0.0183 px both, no 10 px kill. B does not overthrow PAR.

MATRIX.md audit (mechanical verdict rule applied):
- dialogue B/C/D1/D2: TIE → LOSE (3/5 < 5/5, regression on accuracy;
  D2's T5 fault-integrity win noted as complement, not overthrow).
- predictive video D2: TIE → LOSE (fault-recovery win does not compensate
  4.95 px vs 2.77 px tracking regression).
- audio stock C: TIE → LOSE (fails §5; gate/plan fork is a different
  mechanism).
- "Cost honesty" note rewritten: the original battery scripts still use
  parent-CPU `time.process_time()` for child renders — KNOWN DEFECT,
  unresolved; only formation (shell user+sys) and LATENCY-1 (wall-clock)
  figures are cited as valid.
