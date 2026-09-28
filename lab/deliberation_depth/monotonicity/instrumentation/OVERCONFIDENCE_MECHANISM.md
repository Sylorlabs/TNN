# OVERCONFIDENCE MECHANISM — white-box verification (CREW B)

**Date:** 2026-09-24 · **Status:** all four audit decoupling points verified instrumentally; Micah's-law baseline measured.
**Method:** instrumented copy of the H5B ceiling harness (`src/`, built with pinned
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`); per-round TRACE ledger
(round, leader, conf, raw margin, leader/runner scores, evidence consumed, live hyps,
eliminations, residual-flip bound, ground-truth rank, correctness, conf gain).
16 cells (trap ×5 depths, ceiling ×9 configs, logic-ne1 ×2) run twice each; all 32 runs
byte-identical on results+ledgers (A/B diff). 11,070 per-round trace rows analyzed.
Frozen `harness/` and `harness_v2/` untouched. No commits.

---

## 1. The four decoupling points — verdicts

### (1) Sole-survivor pin at 1000 — CONFIRMED (the fatal one)
When the runner-up is eliminated, confidence is *defined* as 1000 by code
(`if(nalive2<=1){st.*.conf=1000;}`), independent of evidence, margin, or truth.
Measured: **1,096/1,096 rounds (100.00%)** with one live hypothesis report conf=1000;
**780/780 elimination events** pin conf=1000 at the exact elimination round.
The "confident liar microsecond" is real: **100 ground-truth kill events**
(truth alive before, dead after) — **100/100 pin conf=1000 at the kill round,
100/100 are wrong at that round**. Canonical trace (`H5B-O-06-00`, d64):
r6 `conf=500 margin=500 correct=0` (wrong leader ADMIT, truth REJECT still alive at rank 2) →
r7 `elim=1 conf=1000 margin=1270 rscore=-1 gtrank=-1 correct=0`.
The elimination event is the microsecond the machine becomes a confident liar:
confidence jumps 500→1000 *because a competitor died*, not because evidence improved.
The formula conflates "no competitors left" with "certainly right."

### (2) Margin measures distance-to-runner-up, not evidence quality — CONFIRMED
The margin distributions for correct and wrong rounds overlap almost completely
(e.g. margin=500: 4,187 correct rounds vs 3,250 wrong rounds; identical coarse buckets
100–5000 on both sides of truth) — the meter cannot discriminate truth from falsehood
at any magnitude. Divergence counts: rounds with **conf≥500 while wrong**: O 240/3,640,
P 3,040/3,740, trap 20/1,791, D 120/1,230. Rounds with **conf=1000 while wrong**:
**O 100/3,640; zero in every other family** — maximum-confidence wrongness exists only
where the stream is adversarial. Confidence actively **rising while wrong**
(gain>0, correct=0): trap 408/1,791 rounds, D 420/1,230, P 320/3,740, O 100/3,640
(the 100 O kill-rounds). The d1 trap catastrophe is the extreme: 127/127 wrong on a
single evidence item, all at conf=100 — the file-wide maximum, zero variance, sensor silent.

### (3) Irreversible elimination; the margin is never re-audited — CONFIRMED
Code: `alive[]` is written exactly three places — init `alive[ai]=1` (line 232),
elimination `alive[h2]=0` (line 272), refutation `alive[second]=0` (line 298).
**No re-admission path exists.** Trace: on all **40/40 O items** the truth is eliminated
in the d16/d32/d64/bound legs; **90 post-kill rounds** have `rscore=-1`, i.e. the
"margin" is just the survivor's own score (`margin=lscore`) — it measures survivors only,
forever. The confidence at release certifies a kill-board state frozen rounds earlier.

### (4) Quantized confidence set — CONFIRMED IN SPIRIT, exact count DIFFERS (reported honestly)
The audit claimed 7 distinct values; across **11,070 per-round trace rows** I observe
**12**: {100,150,200,250,300,400,450,500,600,700,800,1000} (500 alone = 7,099 rows, 64%).
Across 2,161 final verdicts: **11** distinct values. The audit's 7 came from a different
cell mix (their sweep's finals); the exact alphabet is scope-dependent, but the conclusion
stands and is stronger for being measured per-round: the sensor is a coarse scoreboard
with ~1% of the resolution its 0–1000 range advertises, and it is never calibrated to
correctness. No failed pinpoint is hidden here — the count differs, the mechanism doesn't.

---

## 2. Micah's-law baseline: G(d) = mean(conf)/1000 − accuracy ("before" picture)

Law: G(d+1) ≤ G(d) everywhere. Measured on the current harness:

| family | d1 | d2 | d4 | d8 | d16 | d32 | d64 | law violations |
|---|---|---|---|---|---|---|---|---|
| O (40) | −0.690 | −0.500 ⚠ | −0.500 | −0.125 ⚠ | +0.250 ⚠ | +0.625 ⚠ | **+1.000** ⚠ | 5 of 6 steps |
| P (40) | +0.310 | +0.500 ⚠ | +0.500 | +0.375 | +0.250 | +0.125 | +0.000 | 1 |
| D (40) | +0.075 | +0.100 ⚠ | +0.100 | 0.000 | 0.000 | 0.000 | 0.000 | 1 |
| trap (127) | +0.100 | +0.134 ⚠ | −0.046 | −0.085 | −0.085 | — | — | 1 |
| logic_ne1 (223) | −0.500 | — | — | — | −0.500 | — | — | 0 |

The O family is the law's counterexample in pure form: G rises monotonically from
−0.690 to **+1.000 — the maximum possible calibration gap** (mean confidence 1.000 at
accuracy 0.000): perfectly confident, perfectly wrong. Current release policy
(residual-flip bound) as single points: O: G=+0.500 (releases wrong answers at 50%
mean confidence); P: G=−0.500; D: G=−0.200. Adaptive: O: G=−0.500 but only by stopping
before the flip (acc 1.000, 5.0 rounds); P: G=+0.500 (acc 0.000 — it stops before P's
own flip, wrong).

**Per-item violation inventory** (across consecutive depth steps):
- **Unforgivable** (correct 1→0 AND conf non-decreasing): **40 total, all O family** —
  exactly 10 per step at d4→d8, d8→d16, d16→d32, d32→d64 (the calibrated quartile flips).
  Zero in every other family. This is the complete pre-law violation list for the
  unforgivable case.
- **Confidence theater** (wrong→wrong AND conf rising): trap **90/508** (85 at d1→d2,
  5 at d2→d4), D **30/240**, P **40/240** (d1→d2: conf 300→500 while wrong throughout),
  O 0, logic_ne1 0.
- Early O G-increases (d1→d2, before any flip) are confidence inflation on
  still-correct answers — a milder form, counted by the G-law but not the unforgivable rule.

---

## 3. H-RATIONALIZE allocation split — structural confirmation, behavioral shift REFUTED

Per round, relative to the pre-round leader: (a)=attacks[leader] weight,
(b)=supports[leader] weight, (c)=kills. Ceiling d64:

| segment | attack (a) | defend (b) | kills (c) | defend share |
|---|---|---|---|---|
| O pre-flip (740 rds) | 0 | 72,940 | 0 | 1.00 |
| O post-flip (80 rds) | 20,000 | 20,000 | 40 | 0.50 |
| P (860 rds) | 20,000 | 112,940 | 40 | 0.85 |
| D (170 rds) | 15,000 | 26,000 | 40 | 0.63 |
| trap d8 (484 rds) | 63,500 | 50,100 | 86 | 0.44 |

Findings:
- **The flip coincides with a change in who is defended** (grok's prediction ✓):
  pre-flip, 100% of leader-directed weight defends the truth and the truth is *never
  attacked* (attack=0 over 740 rounds — the O streams are engineered with a clean
  pre-flip); post-flip the defense budget flows to the false leader and **all 40 kills
  fire post-flip, 0 pre-flip**, all targeting the truth.
- **Reweighting, not birth** (grok's prediction ✓): the hypothesis pool is fixed
  (2 hypotheses, never gains members); the false leader was present from round 1 on
  all 40 O items. At the flip round the truth is **alive but out-scored in 40/40**
  cases — the flip itself is pure reweighting; the kill follows (grok's conjunction
  bet H-RATIONALIZE × H-ELIM-ASYM is exactly what the traces show, in that order).
- **The *shift* version is refuted structurally**: the machinery has **no deliberative
  operation that attacks the leader**. ELIMINATE (margin≥900) and TEST/refutation
  (margin≥600) both target *rivals of the leader* by construction (code lines 269–272,
  298); the leader can never be challenged, only evidence can nick it. There is no
  (a)-budget to reallocate, so no (a)→(b)+(c) *transition* exists in any trace on any
  family — (b)+(c) are 100% of the challenge budget from round 1. Rationalization here
  is **architectural, not behavioral**: whoever seizes the lead inherits the entire
  defense-and-sniping apparatus. This distinguishes it from the pure exposure-multiplier
  story: exposure writes the flip, but the leader-serving kill machinery is what makes
  the flip irreversible and maximally confident.
- Grok's proposed discriminator (leader-blind reallocation) is not runnable on this
  harness without building a variant — the evidence application is already symmetric;
  the asymmetry lives entirely in the kill ops. The actionable test for mechanism
  crews: symmetric kill operations (an objection kills only if itself validated).

---

## 4. Build / determinism notes

- Pinned compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  `build.sh` reproduces the binary; no `[]i32`/`[]u32`/`[]u16` casts added (u8 arenas only).
- 16 cells × A/B = 32 runs, byte-identical diffs on results and ledgers (`run_cell.sh`,
  per-cell logs in `logs/`).
- Analysis scripts: `analysis/verify_claims.py`, `analysis/calibration_gap.py`,
  `analysis/rationalize_split.py`; outputs in `logs/`.
- One analysis bug caught and fixed mid-stream: round ids were string-sorted
  (`'10'<'9'`), scrambling multi-round items; fixed to int sort and all counts re-verified.
- No commits; frozen harnesses untouched.
