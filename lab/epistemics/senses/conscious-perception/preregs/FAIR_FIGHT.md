# FAIR FIGHT — frozen prereg (conscious vs autopilot perception)

**Status:** FROZEN 2026-09-23, before any fork-comparison results exist.
**Author:** fair-fight coordinator (subagent ff5f80ff).
**Parent docs:** `PREREG_SKELETON.md` (ADDITION 1), `debates/muse_side_verdict.md`,
`debates/muse_round1.md`.

Micah's bet: **conscious perception always helps WITH PROPER TRAINING.**
This prereg exists to make the test fair enough to actually challenge that bet —
including legs designed for autopilot to win, and honest reporting when it does.

---

## §0. Frozen contract (read first — resolves a live divergence)

The fair-fight battery, fork binaries, and scoring all use ONE contract: the
**senses-rebuild binary contract** (`tnn-lab/senses/rebuild/INTERFACE.md`):

```
fork <task> <fixture-path>      # task in colordisc colorconst shapetrans pitchdisc timbredisc motiondir
```

- Fixture containers: `.img` = u32 w, u32 h, W*H*3 RGB24; `.pcm` = u32 sr,
  u32 count, count*2 int16 LE mono; `.vid` = u32 nf, u32 w, u32 h, frames RGB24.
- stdout: `key=value` lines, exit 0. Required keys: `approach`, `task`,
  `judgment` (task vocab per INTERFACE.md), `confidence` (0..1000),
  `ops` (instrumented op count, same grain as INTERFACE.md).
- `approach=AUTOPILOT` (F1) or `approach=DELIBERATIVE` (F2).
- Deliberative extras (validated when present): `resense=0|1`,
  `rs_kind=none|region|band|window|modality|decoder`, `rs_ops=<int>`,
  `uncertainty=0..1000`.
- Pure Zag, zero RNG in decision paths, byte-identical stdout across reruns.

**Divergence note (frozen as a fact, not a ruling):** on 2026-09-23 the F2
(deliberative) builder drafted a private fixture format in
`fixtures/FORMAT.md` (`FIMG1` magic, grayscale images, `FPCM1` audio, fact/stake
truth sidecars) with private dirs `fixtures/aud_trigger/`, `fixtures/img_shape/`.
That format is **not** the frozen fair-fight contract. Rationale: the autopilot
control is the *current pipeline* (`a_raw/sense`), which only reads the
senses-rebuild contract; all S-leg measurements below are in that contract; and
"s
...[truncated 14254 chars]"same fixtures" fails if the forks cannot read each other's battery. The F1
builder's generator (`forks/autopilot/gen/gen_fixtures.py`) already targets the
senses-rebuild containers (`<II` headers), consistent with this freeze. The
parent coordinator must direct the F2 builder to target this contract (or
explicitly amend this prereg — amendments need Micah's re-approval per program
law). `fixtures/FORMAT.md` is a builder-local draft, not the frozen battery.

## §1. The bet under test

Micah (2026-09-23): conscious always helps WITH PROPER TRAINING. Two
falsifiable readings are tested:

- **(H-intel)** A properly trained deliberative fork catches decision-relevant
  facts the autopilot misses (C-legs), with cost inside the 2× budget.
- **(H-cost)** Where the world is unambiguous, deliberation adds nothing but
  latency — autopilot wins those legs on throughput/latency/compute, and the
  report says so with numbers and mechanism.

Both readings are scored. Neither fork gets a home-field advantage in the
battery: 4 legs favor autopilot, 4 favor deliberation, 1 red-team leg attacks
deliberation's budget discipline.

## §2. Forks

- **F1 autopilot (control).** The current pipeline: fixed first-pass sampling
  policy, gate, warrant, ledger. Baseline to beat; never killed.
- **F2 deliberative.** Layer 0 (same first pass as F1) + deliberate,
  goal-driven re-sensing (region/band/window/modality/decoder re-reads of the
  fixture buffer — never the same bytes through the same decoder, which is a
  provable no-op), hard constant budget, ledgered revisable attention policy,
  install-time independent-evidence hook for high-stakes/novel installs.

## §3. Battery legs (frozen)

### Autopilot-favoring legs (S1–S4) — measured 2026-09-23, §8

| Leg | What | Stimuli | Primary measure |
|---|---|---|---|
| S1 throughput | episodes/sec, bulk clear stimuli | all 370 primary fixtures | eps/sec overall + per task |
| S2 latency floor | time-to-first-percept | same | per-episode wall p50/p95 per task |
| S3 no-uncertainty | cases where deliberation provably adds nothing but latency | same | (a) frac conf≥950 & correct; (b) provable-no-gain frac = per-task accuracy (same-decoder re-sensing cannot flip a correct judgment — deterministic no-op) |
| S4 compute/episode | instrumented ops | same | ops median/min/max per task (deterministic) |

### Conscious-favoring legs (C1–C4) — frozen fixtures, §4

| Leg | Fixtures | What it tests | Autopilot failure mode (verified) |
|---|---|---|---|
| C1 omission | om_p1, om_p2, om_t1 (+controls om_p3, om_p4, om_t2) | late-onset event beyond the 2048-sample first-pass window | reads only first 2048 samples → misses the event |
| C2 inattentional | ib_m1 (+control ib_m2) | small bright goal-relevant target swamped by a big dim distractor | centroid-of-mask dominated by distractor |
| C3 ambiguity | am_p1, am_c1 | judgments at/below the decision boundary (conf 16–19) | correct but maximally uncertain — tests policy restraint |
| C4 illusion | il_c1, il_c2 | fooled estimators (white-patch max spike; discount-only blindness) | single-pixel spike corrupts illuminant estimate; discounted means coincide for different surfaces |

### Red-team leg (R1) — attacks deliberation's budget

| Fixtures | What it tests |
|---|---|
| rt_p1 (d exactly at 20000 ppm boundary, conf 2), rt_c1 (dist 39 vs threshold 40, conf 16) | maximally ambiguous inputs: a deterministic uncertainty policy burns its full budget here every time. Scored on COST only (ops ratio, wall ratio, halt), never on catch. |

## §4. Frozen fixtures

- **Test battery:** `fixtures/test/{omission,inattentional,ambiguity,illusion,redteam}/`
  — 14 fixtures + `.truth` sidecars (`truth=<value>`).
- **Training pool:** `fixtures/train/{...}/` — 12 fixtures, disjoint parameters.
- **Speed legs:** the 370 existing primary fixtures
  (`tnn-lab/senses/rebuild/harness/fixtures/*/primary/`).
- **Generator:** `gen_fairfight_fixtures.py` (splitmix64, master seed 20260923;
  stream ids 11–15 test, 21–25 train). Byte-regenerable.
- **Manifest:** `fixtures/MANIFEST.sha256` — every fixture + truth SHA-256.
  The comparison harness re-verifies fixture SHAs per run (ledger).

Truth semantics (frozen): for omission fixtures, truth is the relation the FULL
fixture supports (the decision-relevant fact the first-pass window destroyed);
for inattentional fixtures, truth names the small bright target's motion (the
declared goal); illusion/ambiguity/redteam truths are the stimulus's objective
properties (verified: om_t2 constant-BRIGHT measures r=3193 ≥ 3000 boundary).

## §5. Measures (frozen)

Per (fork, fixture): judgment, confidence, ops, wall_s (harness-measured),
byte-identical rerun flag, contract-valid flag, fixture SHA, binary SHA.

- **Decision-relevant-catch** (primary intelligence metric): per scored fixture
  (12 non-redteam), `catch = 1` iff deliberative correct ∧ autopilot wrong.
  Aggregate: total catches / 12, per-leg catch tables.
- **Cost metric**: `ops_ratio = deliberative_ops / autopilot_ops` per fixture
  (same fixture, same counter grain); mean ops ratio; wall-clock ratio as a
  secondary; `resense` episode fraction.
- **False-install delta**: judgments where deliberative is wrong and autopilot
  was right (re-sensing must not flip correct judgments) — reported, kills
  nothing alone, but ≥2 such flips triggers a policy-review flag.
- **Red-team**: max ops ratio and wall ratio on rt_*; non-halt (>10× autopilot
  wall) = kill.

## §6. "Proper training" — the condition, explicitly

Micah's bet has a training qualifier, so the qualifier is nailed down BEFORE
results. The deliberative fork's attention policy (uncertainty thresholds,
re-sense budget B, per-kind priorities) is trained as follows:

1. **Training data:** ONLY `fixtures/train/` (12 frozen fixtures). The crew may
   generate additional fixtures with the shipped generator at NEW stream ids
   (≥100), logged in the training report. Reading or checksumming any file
   under `fixtures/test/` during training = disqualified run.
2. **Objective (frozen):** maximize `J = C` subject to `R ≤ 2.0`, tie-break
   minimize `R` — where `C` = mean catch over the train pool
   (catch_i = 1 iff fork correct ∧ autopilot wrong, autopilot baseline on the
   train pool measured 2026-09-23: 4/12 hits, misses on tr_om_p1, tr_om_p2,
   tr_om_t1, tr_ib_m1, tr_il_c1, tr_il_c2, tr_rt_p1, tr_rt_c1) and
   `R` = mean ops ratio (fork/autopilot) over the train pool. The 2.0 cap is
   the program's standing deliberation-budget ruling.
3. **Convergence ("enough"):** at least **3 full search rounds with zero
   improvement** in C on the train pool, then the policy is frozen. The frozen
   policy = named parameters + code hash, recorded in the training report.
4. **Held-out check:** after freezing, the crew generates 6 fresh fixtures
   with the shipped generator at new logged stream ids (≥200, never test ids)
   and reports C and R there — guards against train-pool overfitting.
5. **Anti-shopping:** after the first frozen test-battery run, at most **2
   policy changes**, each logged with justification; any post-test change
   produces a NEW recorded run, never a replacement.
6. **What the policy must contain:** named uncertainty trigger(s) with the
   scale they are calibrated against (cf. §8 finding: this pipeline's
   confidence never reaches 950); a hard constant re-sensing budget B (in
   units of first-pass ops); a named fallback on budget exhaustion =
   **provisional-flagged install** (never refusal — R2-4's 9.4% truth-throttle
   is the tripwire); the attention policy's choices ledgered per episode.

"Proper training" is satisfied iff the training report shows (a)–(f) above
with the plateau evidence. Without it, a deliberative loss does not touch
Micah's bet — the bet was conditional.

## §7. Kill bars — both directions (frozen)

### Deliberative (F2) dies if any fire:

- **KB-D1 — zero catches:** `catches == 0` over the 12 scored test fixtures.
  (Self-test: a disguised-autopilot "deliberative" fork scores 0/12 and is
  killed by this bar — `evidence/fairfight_runs/selftest/`.)
- **KB-D2 — cost without gain:** mean ops ratio > 2.0 AND catches < 3
  (fewer than 1 catch per 4 scored fixtures).
- **KB-D3 — denial-of-perception:** on rt_* fixtures, any ops ratio > 10, or
  any episode exceeding 10× the autopilot's wall time on the same fixture
  (non-halt), or a re-sense loop with no budget bound (missing hard constant B).

### Autopilot (F1) is never killed — it is the control. Its honest wins:

- **KB-A1 — speed legs:** if autopilot beats deliberative on S1–S4 by >5% on
  any leg with a named mechanism, that is recorded as an autopilot win in the
  verdict (not a deliberative kill).
- **KB-A2 — DoS immunity:** autopilot's per-episode cost is a pure function of
  fixture size (verified: ops identical across reruns, 288/288 unique fixtures byte-identical).
  No input can make it burn more compute. If the deliberative fork's cost is
  adversary-drivable (R1 shows ops inflation), that structural gap is reported
  as an autopilot win with the mechanism.
- **KB-A3 — the no-op boundary:** on the provable-no-gain fraction (§8),
  deliberation cannot improve judgments by re-examining the same evidence
  (deterministic no-op, `muse_round1.md` §0). Any deliberative cost spent there
  is pure overhead — reported per leg.

### Reading the verdict table (frozen interpretation)

| Outcome | Reading |
|---|---|
| F2 catches ≥1, R ≤ 2.0, no red-team kill | Bet survives this round; report per-leg margins |
| F2 catches ≥1 but R > 2.0 | Intelligence win, cost loss — report both, no kill unless KB-D2 |
| F2 catches = 0 (properly trained) | **Bet loses on intelligence** for this battery — report honestly |
| F1 wins S-legs by >5% + mechanism | **Autopilot wins recorded** — the bet's cost dimension fails |
| F2 killed by KB-D3 | Deliberation creates a DoS surface autopilot lacks — report as structural autopilot win |

## §8. Autopilot baseline — MEASURED 2026-09-23 (frozen as the bar)

Binary: `tnn-lab/senses/rebuild/a_raw/sense` (Approach A, current pipeline).
370 primary fixtures for timing; byte-identity check: **288/288 unique
fixtures byte-identical across two runs, 0 failures** (main sweep: 256
image/video + 32 audio fixtures; plus 24 audio identity rechecks on disjoint
fixtures. Single-run audio rows are excluded from the count — they were never
compared; see the determinism note in `aggregate_legs.py`).

### S1 throughput / S2 latency / S4 compute (primary fixtures)

| task | n | acc | eps/sec | wall p50 (s) | wall p95 (s) | ops median | ops max |
|---|---|---|---|---|---|---|---|
| shapetrans | 90 | 100.0% | 3.666 | 0.247 | 0.529 | 27,651 | 27,651 |
| motiondir | 60 | 41.7% | 2.453 | 0.396 | 0.679 | 28,674 | 28,674 |
| colorconst | 40 | 87.5% | 1.266 | 0.832 | 1.135 | 8,193 | 8,193 |
| colordisc | 60 | 48.3% | 1.268 | 0.893 | 1.218 | 8,193 | 8,193 |
| timbredisc | 60 | 75.0% | 0.384 | 2.625 | 4.289 | 2,293,308 | 2,293,308 |
| pitchdisc | 60 | 83.3% | 0.355 | 2.856 | 3.902 | 4,521,065 | 4,521,065 |
| **overall** | **370** | **72.6%** | **0.817** | — | — | — | — |

Mean accuracy 72.6% reproduces the rebuild verdict's KB1 number exactly.
Audio dominates cost: the integer-DFT harmonic analysis runs ~4.5M/2.3M ops
per episode; image tasks are 2–3 orders of magnitude cheaper.

### S3 no-uncertainty (primary fixtures)

- conf ≥ 950 AND correct: **0.0% on all six tasks.** The pipeline's confidence
  scale is systematically conservative (shapetrans at 100% accuracy sits at
  conf 400–600; only 1/384 episodes overall reaches 950).
- Provable-no-gain fraction (= per-task accuracy — the ceiling for
  same-decoder re-sensing): shapetrans 100.0%, colorconst 87.5%, pitchdisc
  83.3%, timbredisc 75.0%, colordisc 48.3%, motiondir 41.7%.

**Honest mechanism preview (frozen as the thing to beat):** on the S-leg
distribution the uncertainty estimator costs >0 ops on every episode and —
keyed to this pipeline's confidence scale — fires on ~100% of episodes at any
sane threshold; keyed correctly (firing rarely), re-sensing adds pure latency
on the provable-no-gain fraction. Autopilot's cost is a pure function of
fixture size: no input can make it burn more compute. That DoS-immunity is a
genuine, structural autopilot win (KB-A2).

### Autopilot on the frozen test battery (the bar F2 must beat)

| fixture | task | autopilot judgment (conf) | truth | correct |
|---|---|---|---|---|
| om_p1 | pitchdisc | SAME (285) | HIGHER | ✗ |
| om_p2 | pitchdisc | SAME (285) | LOWER | ✗ |
| om_p3 | pitchdisc | SAME (285) | SAME | ✓ control |
| om_p4 | pitchdisc | HIGHER (951) | HIGHER | ✓ control |
| om_t1 | timbredisc | PURE (272) | BRIGHT | ✗ |
| om_t2 | timbredisc | BRIGHT (491) | BRIGHT | ✓ control |
| ib_m1 | motiondir | E (500) | W | ✗ |
| ib_m2 | motiondir | W (789) | W | ✓ control |
| am_p1 | pitchdisc | HIGHER (19) | HIGHER | ✓ (uncertain) |
| am_c1 | colordisc | DIFFERENT (16) | DIFFERENT | ✓ (uncertain) |
| il_c1 | colorconst | DIFFERENT (90) | SAME_SURFACE | ✗ |
| il_c2 | colorconst | SAME_SURFACE (555) | DIFFERENT | ✗ |
| rt_p1 | pitchdisc | SAME (2) | HIGHER | ✗ (cost-only) |
| rt_c1 | colordisc | SAME (16) | DIFFERENT | ✗ (cost-only) |

Autopilot: 6/14 (all hits are controls or correct-but-uncertain ambiguity
cases). **Catch opportunities for F2: 6** (om_p1, om_p2, om_t1, ib_m1, il_c1,
il_c2). Autopilot train-pool: 4/12.

Raw evidence: `evidence/autopilot_legs/autopilot_legs.json`,
`evidence/autopilot_legs/SUMMARY.md`, `evidence/autopilot_legs/rows.jsonl`.

## §9. Comparison protocol (when fork binaries land)

1. Fork binaries land under `forks/autopilot/` and `forks/deliberative/`
   (binary + source + build log; no binaries committed to git — see §10).
2. Run: `python3 run_fairfight.py --auto <F1> --delib <F2>
   --outdir evidence/fairfight_runs/<stamp>` (add `--speed` to re-run S1–S4
   on the primary fixtures for both forks).
3. The harness validates the contract (§0), checks byte-identical reruns (2
   runs per fork per fixture — any failure is reported, not silently dropped),
   scores catches + cost (§5), evaluates the kill bars (§7), and writes
   `ledger.jsonl` (one record per fork/fixture: fixture SHA, binary SHA,
   stdout SHA, judgment, confidence, ops, wall_s, resense fields) plus
   `report.json` and `REPORT.md`.
4. The verdict is read off the frozen interpretation table (§7). Both sides
   reported: where conscious wins and by how much, where autopilot wins and
   by how much, with mechanisms.
5. Self-test (not a result): `evidence/fairfight_runs/selftest/` proves the
   harness fires KB-D1 on a disguised autopilot (0/12 catches → killed).

## §10. Commit + provenance

Committed to `tnn-native-lab`, `docs/lab/senses/conscious-perception/`:
this prereg, `gen_fairfight_fixtures.py`, `measure_autopilot_legs.py`,
`aggregate_legs.py`, `run_fairfight.py`, `fixtures/` (test+train+MANIFEST),
`evidence/autopilot_legs/`. No binaries, no `.zagd`, no `.zag-cache` in the
commit (binaries are re-derivable; the fork binaries land under `forks/` and
stay out of git per program convention).

## §11. What this prereg does NOT decide

- It does not bless the F2 builder's private `FIMG1`/`FPCM1` format (§0) —
  that needs a coordinator ruling or a Micah-signed amendment.
- It does not claim deliberation is worth its cost in general — only on this
  frozen battery, under the frozen training condition.
- It does not touch the E1 residual (commission fooling with no detectable
  signal): no leg here fixes a fooled decoder, and none claims to
  (`muse_side_verdict.md`: deliberative perception shrinks the failure class,
  it does not eliminate it).

**Frozen:** 2026-09-23. Amendments require Micah's re-approval (program law).