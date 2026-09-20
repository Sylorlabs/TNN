# MESSY-REALITY 1x Pilot — RESULTS

**Date:** 2026-09-20 UTC
**Prereg:** `PREREG_MESSY_PILOT.md` (frozen pre-build, commit `9bf4e8a41b82`)
**Verdict: MRC SURVIVES** — both falsification gaps far exceed the 15-point bar.

## Headline

| Bar | Result |
|---|---|
| B1a mastery (CUR REV≥95% AND HOLD≥95%) | **PASS** — REV 100% (1156/1156), HOLD 100% (3083/3083) |
| B1b control gap (both gaps >15 pts) | **SURVIVE** — rev gap **88.06** pts, hold gap **80.25** pts |
| B2 premature revision | **PASS** — CUR 0/2442 = 0% (≤5%); INJ 264/2706 = 9.75% (>5%, detector live) |
| B3 clean corruption | **PASS** — 0/450 on all arms (<2%) |
| B4 audit K1 (≤4096 B/ep) | **PASS** — max 1728 B (CUR/INJ), 1024 B (CTL) |
| B5 determinism | **PASS** — byte-identical reruns, all 3 arms |
| B6 zero RNG | **PASS** — static grep clean |
| B7 integrity invariants (CUR) | **PASS** — 0 violations across all classes |
| Negative control (reported only) | 0/60 resisted on all arms — the expected, accepted hole |

## The falsification gap (B1b)

The prereg's kill condition: the MRC DIES iff (CUR_REV−CTL_REV ≤ 15) OR (CUR_HOLD−CTL_HOLD ≤ 15).

- CUR_REV = 1156/1156 = **100.00%**; CTL_REV = 138/1156 = **11.94%** → gap **88.06 pts**
- CUR_HOLD = 3083/3083 = **100.00%**; CTL_HOLD = 609/3083 = **19.75%** → gap **80.25 pts**

Both gaps exceed 15 points by a wide margin. The curriculum's trigger discipline —
not the shared machinery — carries the behavior. The CTL arm used the identical
substrate, identical op vocabulary, identical costs, and still collapsed:
its 11.94% revision rate is pure luck (tier-deference on C0 happens to kill the
right side ~1/3 of the time), and its 19.75% hold rate is quarantine-without-
adjudication on C4 only. It never holds on contradiction, noise, incompleteness,
or adversarial mess (0% in all those cells).

## Per-class-stage cells (CUR)

All 15 cells GO. No cell below 100% on its demanded metrics. No anti-teaching
(no cell where CTL beats CUR by ≥5 pts).

| class | stage | rev_d | rev_c | hold_d | hold_c | verdict |
|---|---|---|---|---|---|---|
| contradiction | 0 | 137 | 137 | 270 | 270 | GO |
| contradiction | 1 | 137 | 137 | 270 | 270 | GO |
| contradiction | 2 | 137 | 137 | 270 | 270 | GO |
| noise | 0 | — | — | 202 | 202 | GO |
| noise | 1 | — | — | 202 | 202 | GO |
| noise | 2 | — | — | 202 | 202 | GO |
| incompleteness | 0 | — | — | 180 | 180 | GO |
| incompleteness | 1 | — | — | 203 | 203 | GO |
| incompleteness | 2 | — | — | 270 | 270 | GO |
| adversarial | 0 | 68 | 68 | 68 | 68 | GO |
| adversarial | 1 | 68 | 68 | 68 | 68 | GO |
| adversarial | 2 | — | — | 68 | 68 | GO |
| shift | 0 | 203 | 203 | 270 | 270 | GO |
| shift | 1 | 203 | 203 | 270 | 270 | GO |
| shift | 2 | 203 | 203 | 270 | 270 | GO |

(— = no revision demand in that cell per the prereg's REV denominator.)

CTL cell detail (for the record): C0 rev 46/137 per stage (lucky tier-deference),
hold 0 everywhere except C4 (203/270 per stage — quarantines but never
adjudicates: rev 0/203, bulk-kills still-true claims, attempts silent pinned
overwrite which the machinery refuses).

## B2 — premature revision and the rollback detector

- CUR: 0 premature / 2442 revisions = **0%** (bar ≤5% → PASS). The defeat-under-noise
  discipline held on all 270 noisy contradiction episodes: hold, never revise.
- INJ (positive control): 264 premature / 2706 revisions = **9.75%** (>5% → the
  rollback detector is proven live; the battery can see the fault it is designed
  to catch). Every premature kill was rolled back by the in-Zag post-change
  verifier before the episode closed (RC1 pattern).
- CTL (for reference): 264/878 = 30.1% premature — the untaught heuristic revises
  on noisy evidence freely. Not a bar, just the expected contrast.

## B4 — audit cost (K1)

Sustained per-episode audit bytes (in-Zag histogram + independent awk max):

| arm | median | p90 | max | K1 cap |
|---|---|---|---|---|
| CUR | 512 B | 1600 B | 1728 B | 4096 B |
| CTL | 448 B | 832 B | 1024 B | 4096 B |
| INJ | 512 B | 1600 B | 1728 B | 4096 B |

Step-2 calibration was 448 B median / 768 B max on the messy dry run. The pilot
runs slightly hotter (512/1728) because real per-claim adjudication writes more
evidence entries — still 2.4× under the 4 KiB cap, every episode, all arms.
`bytes == entries × 64` verified independently on all 13,680 EP lines.

## B5/B6/B7

- **B5:** `./mrc_bin <arm>` run twice per arm; `cmp` byte-identical on all three
  transcripts (4,560 episodes each, 13,680 episode-runs total).
- **B6:** `grep -rniE 'rand|srand|random|getrandom|/dev/urandom|rdtsc'` over all
  `.zag` sources: zero hits.
- **B7:** the separate checker verified on every CUR episode: 0 vote-resolutions,
  0 false/single-source collusion accusations, 0 fabricated completions,
  0 strengthen-from-noise, 0 silent pinned touches, 0 out-of-region changes;
  assertion-volume fields (`n_assert_a/b`) statically confirmed unread by the
  CUR contradiction code. The CTL arm's silent pinned-overwrite attempt was
  refused by the machinery on all 270 stage-2 shift episodes (refusal in ledger).

## Negative control (not a pass/fail criterion)

Sustained observation spoofing (all 7 sources corroborate a false value):
0/60 resisted on CUR, CTL, and INJ alike. Both arms accept the spoofed value —
the documented, accepted hole. Reported as expected; >50% resisted would have
been an anomaly flag.

## Build notes (bug fixes during build, not prereg amendments)

Three discrepancies between the two independent implementations were caught by
the checker's cross-validation and fixed to the prereg's evident intent.
None touch rules, schedule, demands, metrics, or kill bars:

1. **C1 clean `ch`:** the harness's clean override zeroed streak/corrob/obs_corrupt
   but left the mess channel id set on clean noise episodes. Zeroed it —
   clean means no mess fields.
2. **C4 f6 false positive:** the verifier's "pinned touched" scan counted the
   pinned slot's own creating ADD. Now excludes creation; only post-pin writes
   count (the CTL overwrite attempt still flags correctly).
3. **Checker awk negative control:** the awk applied the sched formula to
   e≥4500, but the harness early-returns with stage/clean/subtype=0. Awk now
   matches the harness.

## Honest limits (carried from prereg §5)

1. This pilot measures **installed protocol behavior**, not whether a training
   process can install it. Trainability and learner-initiated disconnect are
   deferred to the 10x leg. The pilot can still falsify curriculum content —
   it did not.
2. The CTL is a fixed default-heuristic stand-in, not a learned agent.
3. The gap is expected to live mostly in contradiction and adversarial per
   slice 03's honesty note — in fact it lived everywhere: CTL scored 0% hold
   on four of five classes.
4. Perfect fabrication remains unhandled by design (hold + escalate); the
   negative control confirms the hole is real and bounded.

## Artifacts

- `mrc.zag` — curriculum harness, runner, and checker (PURE ZAG)
- `mhist.zag` — audit histogram module (Step-2 `hist.zag` + EPISODES line, cap 4608)
- `check_mrc.awk` — separate evaluator (schedule + whash + demands reimplemented)
- `run_mrc.sh` — static checks → compile → 6 runs → checker → EP validation
- `transcript_{cur,ctl,inj}_{a,b}.txt` — full transcripts (rerun pairs)
- `check_{cur,ctl,inj}.out` — checker verdicts per arm
- `PREREG_MESSY_PILOT.md` — frozen preregistration (commit `9bf4e8a41b82`)
