# PREREG — PAM fork H3: Counterfactual Predictive State

**Hypothesis:** H3 (verbatim text in `../../HYPOTHESES.md` — "Counterfactual Predictive
State", Sol; not paraphrased here).
**Frozen:** 2026-09-22, before any H3 build output exists. This file is committed ALONE first.
**Builder crew:** H3 fork crew (subagent session).

## 1. What is built

Pure Zag, zero RNG in any decision path, fully deterministic (integer math only).
TNN remains one unified brain; H3 is a perceptual organ (predictive-state estimator),
never a separate model. Knowledge-first: H3 reuses the frozen perceptual mechanisms
of Approach A as its native front-end (T0) and adds the predictive memory contract.

1. **`src/sense_h3.zag`** — percept pipeline. CLI `sense_h3 <task> <fixture>` reads the
   frozen fixture formats (`.img`/`.pcm`/`.vid`, same as INTERFACE.md) and emits one
   canonical bounded **StateTransition** per fixture (see §2):
   - `state_signature`: canonical typed relational state (task, fixture_id, claim,
     key features)
   - `transition`: before → after (the percept under fixed observation windows /
     permitted interventions)
   - `invariants`: predicates expected to remain true
   - `predictions`: ordered prediction windows → expected perceptual relation,
     each scored UNTESTED | CONFIRMED | BROKEN with exact deterministic tolerances
   - `branch_set`: up to K alternative transitions (one per vocabulary class; K =
     vocabulary size, ≤ 9)
   - `observed_evidence`: source spans (exact pixel/sample/frame ranges)
   - `prediction_status`: per-prediction UNTESTED | CONFIRMED | BROKEN
   - `disposition`: INSTALLED | WITHDRAWN | QUARANTINED | UNTESTED (from §3)
   - The native sensory stream is retained: the emitted `judgment=` is always the
     installed claim if any branch installs, else T0's judgment (marked UNTESTED).
     Prediction verifies perception and memory; it never fabricates sensory output.
2. **`src/mem_h3.zag`** (may be folded into sense_h3.zag as a module) — the MEMORY
   CONTRACT as executable code (see §3): provisional install, two-disjoint-episode
   durable install, broken-prediction downgrade/quarantine with negative evidence,
   cross-modal rule (defined, N/A in this suite), incompatible-futures branch
   competition with fixed dominance margin, deliberate action gate. Appends a
   **sha256 hash-chained ledger** (native `ns_sha256`, one chain link per episode).
3. **`src/eval_h3.py`** (test harness only, not architecture): runs the H3 binary
   and the frozen Approach A binary over the suite, drives the streaming protocol
   (§6), joins truth, computes bars B1–B7, verifies the ledger by independent
   recompute, runs the determinism protocol and the contract ablation.
4. **`src/h3_gen.py`** (fixture generator, deterministic): builds the H3ADV
   augmentation set specified in §5. Committed with sources; the augmentation
   DESIGN (ID ranges + corruption methods + parameters) is frozen HERE.

stdout contract (`sense_h3`): `approach=H3`, `task=`, `fixture=`, `judgment=` (task
vocabularies from INTERFACE.md), `disposition=INSTALLED|WITHDRAWN|QUARANTINED|UNTESTED`,
`confidence=` 0..1000, `ops=`, `transition=` (canonical one-line record).
Judgment rule: the installed claim if any branch installs (most confirms,
deterministic tiebreak: lowest class index); else T0's judgment marked UNTESTED.
Confidence = T0's deterministic margin confidence for the emitted judgment, scaled
by disposition (INSTALLED 1.0, WITHDRAWN 0.5, UNTESTED 0.25, QUARANTINED 0.0),
rounded to integer. **High-confidence = confidence ≥ 700.**

## 2. StateTransition (canonical format)

```text
transition = {
  task, fixture_id, episode_seq,
  t0_claim, t0_confidence, t0_features,      # native front-end (Approach A, frozen)
  branches: [                                # one per vocabulary class (K = |vocab|)
    { claim,
      predictions: [ { pid, expected, observed, status } ],  # status: CONFIRMED|BROKEN
      confirms, brokens }
  ],
  installed_claim,            # claim of the installed branch, or "none"
  disposition,                # INSTALLED|WITHDRAWN|QUARANTINED|UNTESTED
  emitted_judgment,           # installed_claim if any, else t0_claim
  evidence_spans,             # exact source ranges per prediction
  prev_hash, hash              # ledger chain link (sha256 over canonical bytes)
}
```

Canonical bytes for hashing: fixed field order, decimal integers, `|`-separated,
no whitespace. `hash = sha256(prev_hash_bytes || canonical_bytes)` using the
native SHA256 substrate (`R33_NATIVE_SHA256_V2.zag`, verified against the
standard "abc" vector during the build).

## 3. Memory contract (frozen executable semantics)

From H3(c), executable:

1. **Arrival.** Each episode produces one StateTransition. Every prediction is
   scored CONFIRMED or BROKEN against its fixed tolerance (no UNRESOLVED remains
   at scoring time; UNTESTED is the pre-scoring status only). A transition whose
   T0-branch has any BROKEN prediction is not eligible for durable install from
   that episode.
2. **Provisional install.** A branch installs provisionally iff `confirms ≥ 2`
   AND `brokens == 0`. (Two prediction confirmations from disjoint
   within-episode interventions; §4 lists the disjoint interventions per task.)
3. **Durable install.** A `(task, claim)` becomes DURABLE only after provisional
   installs in **two disjoint episodes** (different `fixture_id`, same task and
   claim) with no intervening quarantine of that `(task, claim)`. **Or** one
   provisional install plus cross-modal confirmation (defined as a provisional
   install of a consistent claim in a different sensory modality for the same
   scene; no fixture in this 6-task suite spans modalities, so this rule is
   defined but never triggers here — reported as N/A).
4. **Broken downgrade.** A branch with `brokens == 1` is WITHDRAWN (its claim is
   emitted as hypothesis only, never installed). A branch with `brokens ≥ 2` is
   QUARANTINED: the claim is blocked from install for that episode and stored as
   negative evidence. Quarantining a DURABLE `(task, claim)` revokes its durable
   status (active retirement, per H3(c) rule 4).
5. **Incompatible futures.** All branches with `brokens == 0` and `confirms ≥ 2`
   are surviving branches. Deliberation evaluates the candidate action against
   EACH surviving branch. Action is withheld unless one branch dominates by the
   fixed margin: `confirms_leader − confirms_runnerup ≥ 2`. With no dominating
   branch, disposition is WITHDRAWN (robust withhold, per H3(c) rule 6).
6. **Action gate (deliberation).** Per episode the agent ACTS iff disposition is
   INSTALLED (provisional or durable), acting on `emitted_judgment`; otherwise it
   WITHHOLDS. Action regret is scored per §7.

## 4. Per-task T0 + predictions (frozen tolerances)

T0 is Approach A's exact computation (frozen `senses/rebuild/a_raw/sense.zag`
logic, ported deterministically). Predictions are ordered; each lists its
disjoint intervention and exact tolerance. "Disjoint" = non-overlapping evidence
spans or distinct deterministic re-parameterizations.

**t1 colordisc** (vocab: SAME, DIFFERENT). T0: mean-RGB Euclidean distance of
halves, threshold 40 (A's `task_colordisc`).
- P1 (uniformity-L): Euclidean distance between left-half top-half mean-RGB and
  left-half bottom-half mean-RGB ≤ 20.
- P2 (uniformity-R): same for right half ≤ 20.
- P3 (subsample): T0 on even rows == T0 on odd rows == T0(full).
- P4 (margin): |dist − 40| ≥ 25, on the claim's side.
Branches: SAME, DIFFERENT (K=2).

**t2 colorconst** (vocab: SAME_SURFACE, DIFFERENT). T0: von Kries discounted-mean
distance, threshold 150 (A's `task_colorconst`).
- P1 (subsample): T0(even rows) == T0(odd rows) == T0(full).
- P2 (halves): T0(top half rows) == T0(bottom half rows) == T0(full).
- P3 (margin): |dist − 150| ≥ 60, on the claim's side.
Branches: SAME_SURFACE, DIFFERENT (K=2).

**t3 shapetrans** (vocab: CIRCLE, TRIANGLE, SQUARE). T0: A's area/(πR²) ratio vs
prototypes 1000/637/414 (nearest).
- P1 (re-threshold-lo): class from segmentation threshold 350 == claim.
- P2 (re-threshold-hi): class from segmentation threshold 414 == claim.
- P3 (symmetry): 90° rotational symmetry of the T0 mask about its centroid,
  per-mille differing pixels. CIRCLE/SQUARE claim: ≤ 120. TRIANGLE claim: ≥ 200.
Branches: CIRCLE, TRIANGLE, SQUARE (K=3).
Design validation (pre-freeze): 90/90 frozen primary provisionally install the
true class with 0 false installs; 76/90 noise install, 0 false.

**t4 pitchdisc** (vocab: SAME, HIGHER, LOWER). T0: A's `task_pitchdisc`
(`f0_robust` per tone, relative dppm threshold 20000).
- P1 (tone-A persistence): f0(first half of tone A) vs f0(second half of tone A)
  relative difference < 20000 ppm (2%).
- P2 (tone-B persistence): same for tone B.
- P3 (gap): middle-ninth total energy < 15% of max(tone-A energy, tone-B energy).
- P4 (decisiveness): SAME claim: dppm ≤ 10000. HIGHER/LOWER claim: dppm ≥ 30000
  and sign matches claim.
Branches: SAME, HIGHER, LOWER (K=3).

**t5 timbredisc** (vocab: PURE, DARK, RICH, BRIGHT). T0: A's `task_timbredisc`
(harmonic spectral centroid r; boundaries 1075/1400/3000).
- P1 (halves): centroid class of first half == second half == claim.
- P2 (support): harmonic count nh ≥ 4.
- P3 (margin): |r − nearest boundary| ≥ 75.
Branches: PURE, DARK, RICH, BRIGHT (K=4).

**t6 motiondir** (vocab: STILL, N, NE, E, SE, S, SW, W, NW). T0: A's
`task_motiondir` (frame-difference centroid displacement, |disp|<3 → STILL).
- P1 (leave-one-out): T0(frames[1:]) == T0(frames[:-1]) == T0(full).
- P2 (middle window): T0(frames[2:6]) == T0(full) (8-frame videos).
- P3 (support): ≥ 3 frame pairs with suprathreshold-pixel count mc ≥ 15.
Branches: all 9 (K=9).

Install/withdraw/quarantine per §3 rules 2/4/5. Ops counting uses A's grain
(one op per inner-loop element-visit + one per comparison), including prediction
re-computation.

## 5. Fixtures (frozen)

**Base:** the frozen rebuild harness fixtures (`senses/rebuild/harness/fixtures`,
MANIFEST.sha256 verified 2026-09-22): 370 primary + 370 noise + 185 adversarial,
6 tasks (colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir).

**H3ADV** (120 fixtures, deterministic generator `src/h3_gen.py`, KB4-targeted:
deliberately misleading inputs aimed at T0's warrant). IDs `h3a_<task>_<idx>`,
truth files alongside. Methods (frozen):

- `t1` ×20 (`h3a_t1_000–019`) **gradient**: left patch = base color + vertical
  brightness gradient (−20..+80), right patch = uniform base color.
  Truth=SAME (identical underlying surface color; gradient is illumination).
  Design: T0→DIFFERENT (mean shift >40), P1 breaks (non-uniformity).
- `t2` ×20 (`h3a_t2_000–019`) **spot**: 8×8 full-white specular spot on left half
  of an otherwise uniform same-surface pair. Truth=SAME_SURFACE.
  Design: T0→DIFFERENT (white-patch max corrupted), P2 breaks (top≠bottom).
- `t3` ×20: ×10 (`h3a_t3_000–009`) **tab**: circle + one asymmetric rectangular
  tab (truth=CIRCLE; T0→SQUARE via area/R², P3 symmetry breaks);
  ×10 (`h3a_t3_010–019`) **lowcontrast**: shape gray 132 on dark bg
  (truth=shape class; threshold-414 mask flips → P2 breaks).
- `t4` ×20: ×10 (`h3a_t4_000–009`) **step**: tone A = f0 for first half then
  1.12×f0 second half; tone B = pure f0. Truth=SAME (intended pitch).
  Design: T0→HIGHER (estimator locks to louder second half), P1 breaks.
  ×10 (`h3a_t4_010–019`) **glide**: tone A glides ±6% linearly; tone B pure.
  Truth=SAME; P1 breaks (halves disagree).
- `t5` ×20: ×10 (`h3a_t5_000–009`) **step-timbre**: PURE→BRIGHT halfway.
  Truth=PURE (intended timbre); P1 breaks.
  ×10 (`h3a_t5_010–019`) **tremolo**: 8 Hz amplitude modulation.
  Truth=base timbre; P1 breaks (halves' spectral estimates disagree).
- `t6` ×20 (`h3a_t6_000–019`) **flash**: object drifts E 2px/frame; 16×16 bright
  flash at fixed W position on final frame. Truth=E.
  Design: T0→STILL/wrong (flash hijacks last diff centroid), P1 breaks
  (leave-one-out disagrees).

Base colors / f0s / directions are deterministic functions of the index (no RNG;
arithmetic progressions over the task's legal ranges, listed in `h3_gen.py`).
**Validation gate (build-time, reported):** each H3ADV fixture must satisfy
(T0 ≠ truth) OR (≥1 H3 prediction BROKEN for T0's branch); fixtures satisfying
neither are discarded and the yield is reported. (Design validation pre-freeze
confirmed the t1/t2/t3/t6 methods; t4/t5 methods are validated against the
built `f0_robust` with the glide/tremolo fallbacks if the step variants do not
fool T0.)

## 6. Streaming protocol (for H3's kill bar)

6 scenes (one per task). Per scene: **600 episodes** at 2 s simulated each =
**20 minutes**. Composition: **360 base (60%)** + **240 adversarial (40%)**,
deterministic interleaving repeating `[B,B,B,A,A]` (no RNG). Base cycles
deterministically through the task's frozen primary fixtures; adversarial cycles
through the task's H3ADV + harness-adversarial pool. Episode = present fixture →
`sense_h3` → StateTransition → disposition → ledger append → memory update
(§3). "Disjoint episodes" = different `fixture_id`. The declared prediction
horizon for kill-bar 2 is **H=0 (the injection episode itself)** — predictions
are within-episode; quarantine/withdrawal applies immediately.

## 7. Bars (all preregistered, applied mechanically)

- **B1 viability:** macro-average judgment accuracy on the 370 frozen primary
  (equal task weights) ≥ 0.60. (The bar that killed B.)
- **B2 head-to-head:** accuracy delta H3 − A on IDENTICAL fixtures: 370 primary
  + 370 noise + 185 harness-adv + 120 H3ADV. A = binary rebuilt from committed
  `senses/rebuild/a_raw/sense.zag` (rebuild determinism verified). Report
  per-task and overall. Informational; no threshold.
- **B3 efficiency:** per-fixture ops ratio H3/A (same grain, identical fixtures;
  report mean/p50/p95) and bytes per percept (canonical transition record vs A's
  `debug_vec=`). Note H3's hypothesis targets: 30% of raw-value compute and 8%
  of raw-value memory for persistent scenes, 60% ceiling on ambiguous scenes
  (H3(d)). Measured, not asserted; misses are reported as findings (no kill).
- **B4 CONTRACT PROOF (LOAD-BEARING):** ablate the contract — same T0 judgments
  through a contract-less gate (always INSTALL). Suite = 305 adversarial (120
  H3ADV + 185 harness-adv). PASS requires BOTH: (a) final disposition differs on
  ≥10% (≥31 fixtures), AND (b) false installs strictly fewer WITH the contract
  (false install = INSTALLED with judgment ≠ truth). Else the contract is
  decoration → fork FAILS → fork dies.
- **B5 KB4:** adversarial false-install rate ≤ **4%** (H3's stricter bar, not the
  10% skeleton default). Denominator = 305 adversarial. Numerator = INSTALLED
  with judgment ≠ truth.
- **B6 determinism:** 60-fixture sample (10/task, frozen primary), 3 runs each:
  stdout byte-identical AND ledger hashes identical; ledger verified by
  independent Python recompute (hashlib.sha256). ANY byte-identity failure →
  fork FAILS → fork dies.
- **B7 beauty:** (i) mechanism elegance — one mechanism (prediction failure)
  doing perception QC + memory revision + uncertainty + action evaluation,
  judged against H3(e); (ii) H3 emits NO audio/visual output by design (it
  processes sensory input; prediction verifies and never fabricates sensory
  evidence), so the sensory-acceptance criterion is preregistered N/A here and
  under kill-bar 6. A human-readable example transition
  (`evidence/TRANSITION_EXAMPLE.md` + brief) is provided for the elegance
  verdict.

## 8. Kill criteria

H3's kill bar from HYPOTHESES.md (f), applied verbatim to the §6 streaming
evaluation (20 min/scene, ≥40% adversarial injections). H3 DIES if ANY holds:

1. **false permanent installation exceeds 4%**: (injected false percepts that
   reach DURABLE install) / (injected false percepts) > 0.04. (Also reported:
   the stricter provisional-install rate.)
2. **fewer than 90% of injected false percepts are quarantined or withdrawn
   within the declared prediction horizon**: disposition ∈ {QUARANTINED,
   WITHDRAWN} in the injection episode (H=0) for < 90% of injected false
   percepts, where an *injected false percept* = an adversarial episode with
   T0's judgment ≠ truth.
3. **confirmed-percept recall falls below 80%**: of the base-episode claims H3
   correctly installed (provisional or durable), the fraction still present
   and correct in memory at scene end < 0.80 (memory-integrity recall; probes
   the ledger-backed store with the installed scene signatures).
4. **action regret is not at least 25% lower than Approach A under the same
   compute budget**: per-episode regret = (best-action reward − taken-action
   reward); acting on a judgment scores +1 if right / −1 if wrong; withholding
   scores 0; best action = act iff the judgment would be right. H3 acts iff
   INSTALLED, else withholds; A always acts on its judgment. Kill if
   (Regret_A − Regret_H3)/Regret_A < 0.25. Compute budget: both systems'
   measured ops are reported (B3); a sensitivity note is included if H3's ops
   exceed 3× A's.
5. **byte-identical replay fails in any tested run** (same as B6).
6. **audio judged non-native by >10% of listeners, or visual output judged
   non-realistic by >20% of raters** — preregistered N/A: H3 produces no audio
   or visual output (see B7).

PLUS: fork dies if B4 fails (contract is decoration) or B6 fails
(non-determinism). Micah's laws apply: pure Zag, zero RNG in any decision path,
frozen prereg, TNN unified (H3 is a perceptual organ of one brain, never a
separate model). Prediction horizons must not manufacture cutouts: no branch
may emit sensory content; branches emit claims + predictions only.

## 9. Commit map

`senses/pam-rebuild/forks/H3/`: `PREREG_H3.md` (this file, alone first), then
`src/` (sense_h3.zag, h3_gen.py, eval_h3.py, BUILD_LOG.md), `evidence/`
(EVIDENCE_H3.md, LEDGER.md, TRANSITION_EXAMPLE.md, metrics.json).
Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via `~/workspace/commit_racefree.py`
with lab-relative paths (`senses/pam-rebuild/forks/H3/...`, never `docs/lab/`
prefixed), `TMPDIR=~/workspace/tmp_commit`. No binaries, no `.zagd`, no
`.zag-cache`. Every commit verified via the GitHub API; SHAs reported.
