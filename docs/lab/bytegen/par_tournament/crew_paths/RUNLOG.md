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
- MATRIX.md: added "Fable challenger tests" section (TEMPO-1, REGION-1,
  LATENCY-1, SYNC-1) with verdicts. No matrix cell overturned; REGION-1
  adds a new measured axis (B passes boundary phase continuity, C fails).
- This commit: MATRIX.md, RUNLOG.md, fable_chal/src/{tempo1,region1,syncav,tempo}.zag.
  Binaries, .zagd, .zag-cache, .mix, .log, evidence/*.log NOT committed.
