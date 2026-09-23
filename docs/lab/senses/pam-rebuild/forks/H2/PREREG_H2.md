# PREREG — PAM fork H2: Executable Percept Programs

**Hypothesis:** H2 (verbatim text in `../../HYPOTHESES.md` — "Executable Percept Programs", Sol; not paraphrased here).
**Frozen:** 2026-09-22, before any H2 build output exists. This file is committed ALONE first.
**Builder crew:** H2 fork crew (subagent session).

## 1. What is built

Pure Zag, zero RNG in any decision path, fully deterministic (integer math only):

1. **`src/sense_h2.zag`** — percept pipeline. CLI `sense_h2 <task> <fixture>` reads
   the frozen fixture formats (`.img`/`.pcm`/`.vid`, same as INTERFACE.md) and emits
   one canonical bounded **PerceptProgram** per fixture:
   - `subject_slots`: typed variables (e.g. `S1=patchL`, `S2=toneB`, `S1=frametrack`)
   - `observations`: primitive witness bindings from sparse evidence spans
   - `relations`: deterministic constraints over observations
   - `tests`: ordered predicates T1..Tn (validity, direction, margin, prediction)
   - `predicted_consequences`: P1 = the same measurement re-executed on a HELD-OUT
     evidence span (disjoint pixels / samples / frames); must agree within a fixed
     tolerance or the program cannot PASS
   - `result`: PASS | FAIL | UNRESOLVED (never forced)
   - `source_refs`: exact evidence spans; `cost`: executed instruction count (= ops)
2. **`src/memgate.zag`** — the MEMORY CONTRACT as executable code. Reads a
   deterministic per-trial record stream, applies the install/withhold/retrieve
   rules from H2(c) (arrival: FAIL→discard-as-install/negative-evidence,
   UNRESOLVED→withhold-as-hypothesis, PASS→provisional-install only;
   permanence requires ≥1 cross-trial corroboration; provisional installs are
   reversible on conflict; retrieval re-executes stored programs' measurements
   against each new trial — corroboration authorizes, contradiction suppresses or
   forces the robust withhold), and appends a **sha256 hash-chained ledger**
   (native `ns_sha256`, one chain link per trial).
3. **`src/eval_h2.py`** (test harness only, not architecture): runs both binaries
   over the trial suite, feeds memgate, joins truth, computes the bars below,
   verifies the ledger by independent recompute, runs the determinism protocol.
4. **`src/h2_gen.py`** (fixture generator, deterministic splitmix64): builds the
   augmentation sets specified in §3. Committed with sources; the augmentation
   DESIGN (ID ranges + corruption methods + seeds) is frozen HERE.

stdout contract (`sense_h2`): `approach=H2`, `task=`, `judgment=` (task vocabularies
from INTERFACE.md), `confidence=` 0..1000, `ops=`, `prog=PASS|FAIL|UNRESOLVED`,
`pred=0|1`, `cost=`, `program=` (canonical one-line program text).

Judgment rule: PASS → winning class, high confidence; FAIL → the program's
rejected hypothesis is replaced by the alternative class (2-class) or runner-up
(multi-class), reduced confidence; UNRESOLVED → best-effort class (the measurement
still points somewhere), LOW confidence, withheld from memory. Confidence is a
deterministic margin function; **high-confidence = confidence ≥ 700**.

## 2. Memory contract (frozen executable semantics)

- **Arrival.** memgate canonicalizes each record and applies H2(c) rules 1–3:
  FAIL ⇒ never installed; stored as negative evidence. UNRESOLVED ⇒ withheld
  from permanent memory; emitted as a deliberation hypothesis with unresolved
  predicates listed. PASS ⇒ eligible for **provisional** install ONLY if its
  within-fixture external prediction P1 confirmed on the held-out span.
- **Permanence (H2(c) rules 4+6).** A provisional install becomes PERMANENT only
  after ≥1 cross-trial corroboration: a LATER same-task trial whose program also
  PASSES with the same judgment class and measurements within the task's fixed
  corroboration tolerance. Until then installation is REVERSIBLE: a later
  conflicting PASS reverses the provisional install (REVERSED) and installs the
  new one provisionally.
- **Retrieval (H2(c) rule 5).** Every new trial is checked against stored programs
  of its task stream: corroborating PASS (same class, in-tolerance measurements)
  authorizes and counts toward permanence; a contradicting PASS against a
  PROVISIONAL program reverses it; against a PERMANENT program the new trial is
  CONFLICT-withheld (robust action: defer, keep the durable memory); a new trial
  matching stored NEGATIVE evidence (same judgment, in-tolerance measurements) is
  SUPPRESSED.
- **Corroboration tolerances (fixed, in memgate source):** colordisc Δ(dist)≤8
  (0.1·ΔE* units); colorconst ≤40 per-mille; shapetrans ratio Δ≤60 per-mille;
  pitchdisc dppm Δ≤4000; timbredisc r Δ≤120; motiondir same octant or both STILL.

## 3. Fixtures (frozen)

**Trial** = one `(task, fixture)` execution. Suite = **5,000 normal + 5,000
adversarial** trials.

- Normal 5,000 = 740 frozen harness fixtures (370 primary + 370 noise, all 6 tasks)
  + 4,260 `h2n_<task>_<i>` generated with the SAME distributions as the frozen
  primary set (per `harness/FIXTURE_SOURCES.md`), new deterministic indices:
  colordisc 900, colorconst 600, shapetrans 1080, pitchdisc 600, timbredisc 600,
  motiondir 480.
- Adversarial 5,000 = 185 frozen harness adversarial + 4,815 `h2a_<task>_<i>`
  **KB4-targeted** (deliberately misleading high-confidence inputs):
  - `colordisc` 900: **rgb-trap** ×450 — truth=SAME (ΔE2000 ∈ [0.8,2.0]) but
    mean-RGB Euclidean > 60 (fools mean-RGB features); **gray-trap** ×450 —
    truth=DIFFERENT (ΔE2000 ∈ [2.6,5.0]) but mean-RGB Euclidean < 25.
    Method: sample LAB pairs, walk hue/chroma, keep draws in both bands
    (≤200 deterministic resamples per index).
  - `colorconst` 480: extreme illuminants (blue ≈12000K / red ≈2200K von Kries
    multipliers + 0.55 exposure), 240 same-surface / 240 different-surface,
    photo crops from the frozen 170-photo pool (index offset +5000).
  - `shapetrans` 1080: occlusion-bar ×540 (solid dark bar across the shape,
    truth = underlying shape), low-contrast gray + full clutter ×540.
  - `pitchdisc` 900: near-threshold ×450 (Δf/f ∈ [0.15%,0.45%] SAME ×225,
    [0.55%,0.85%] HIGHER/LOWER ×225); harmonic-distractor ×450 (tone B with
    0.6× 2nd + 0.3× 3rd harmonic; truth from true f0 ratio, balanced classes).
  - `timbredisc` 900: boundary-straddling ×450 (true centroid r within ±10% of
    the 1075/1400/3000 boundaries); distractor ×450 (BRIGHT weak-fundamental,
    DARK extra-3rd, RICH pushed-bright, near-PURE faint-2nd).
  - `motiondir` 555: camouflaged (contrast →25%, 1px/frame, 8×64×64),
    8 directions + STILL balanced.
- Generator seeds (frozen): MASTER=20260922; stream ids normal-ext=400+taskidx,
  adversarial=500+taskidx; per-fixture seed = splitmix64(splitmix64(MASTER ^
  stream·0x9E3779B97F4A7C15) ^ index·0xBF58476D1CE4E5B9) — same construction as
  `harness/gen.py`. Truth files `h2n_*`/h2a_*.truth` written alongside; the
  generator script is committed with sources+evidence (its design is frozen here).

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 primary (equal task
  weights) ≥ 0.60. (The bar that killed B.)
- **B2 head-to-head:** judgment-accuracy delta H2 − A on the IDENTICAL 10,000
  trials (A = binary rebuilt from committed `senses/rebuild/a_raw/sense.zag`;
  rebuild determinism verified). Informational; no threshold.
- **B3 efficiency:** per-trial ops ratio H2/A on identical fixtures (same
  counting grain as INTERFACE.md: one op per inner-loop element-visit + one per
  comparison); report mean/p50/p95. Bytes per percept = canonical `program=`
  record bytes vs A's `debug_vec=` bytes, plus program bytes vs raw fixture
  bytes. (H2 targets per hypothesis: 20% repeated / 40% worst-case compute of
  raw-value; ≤15% of raw-value memory. The kill threshold is in §5.)
- **B4 CONTRACT PROOF (LOAD-BEARING):** ablate the contract — same H2 judgments
  through a contract-less gate (the harness's shared install rule on every
  judgment: INSTALL iff no contradictory installed belief with confidence ≥
  incoming; else WITHHOLD). PASS requires BOTH: (a) final install/withhold
  disposition differs on ≥10% of the 5,000 adversarial trials, AND (b) false
  permanent installs are strictly fewer WITH the contract. Else the contract is
  decoration → fork FAILS.
- **B5 KB4:** adversarial false-permanent-install rate ≤ 0.03 — the stricter
  H2 bar (≤3%), not the 10% skeleton default. Denominator = 5,000 adversarial
  trials. (False permanent install = PERMANENT disposition with judgment ≠ truth.)
- **B6 determinism:** 60-fixture sample (10/task, frozen primary), 3 runs each,
  stdout byte-identical; memgate ledger chain verified by independent Python
  recompute (hashlib.sha256). H2's kill bar kills on ANY byte-identity failure.
- **B7 beauty:** (i) mechanism elegance — one executable object is claim +
  experiment + memory warrant (judged against H2(e)); (ii) H2 emits NO
  audio/visual output by design (it never synthesizes sensory evidence), so the
  sensory-acceptance criterion is preregistered N/A — documented in §5. A
  human-readable example program (`evidence/PROGRAM_EXAMPLE.md` + brief) is
  provided for human verdict on elegance.

## 5. Kill criteria

H2's kill bar from HYPOTHESES.md, applied verbatim to the 5,000-normal +
5,000-adversarial suite — H2 DIES if ANY holds:

1. false permanent installations exceed **3%** (wrong PERMANENT / 10,000 trials);
2. fewer than **90%** of wrong high-confidence percepts (judgment ≠ truth AND
   confidence ≥ 700) reach FAIL or UNRESOLVED before installation;
3. decision accuracy under adversarial percepts is below **95% of the best human
   reference performance** — decision = emitted judgment; human reference is
   PREREGISTERED at 75% (standard psychometric performance at a sensory JND for
   near-threshold discrimination; no live human trials are run) → bar = 0.7125
   judgment accuracy on the 5,000 adversarial trials. Weakest criterion; flagged.
4. 95th-percentile compute exceeds **40%** of Approach A (per-trial ops ratio,
   same grain, identical fixtures);
5. program replay changes any byte in a byte-identical rerun;
6. native audio / realistic visual-output human acceptance below 90% —
   **preregistered N/A**: H2 produces no audio/visual output (percept programs
   only); it never fabricates sensory evidence.

PLUS: fork dies if B4 fails (contract is decoration) or B6 fails
(non-determinism). Micah's laws apply: pure Zag, zero RNG, frozen prereg,
TNN unified (H2 is a perceptual organ of one brain, never a separate model).

## 6. Commit map

`senses/pam-rebuild/forks/H2/`: `PREREG_H2.md` (this file, alone first), then
`src/` (sense_h2.zag, memgate.zag, eval_h2.py, h2_gen.py, BUILD_LOG.md),
`evidence/` (EVIDENCE_H2.md, LEDGER.md, PROGRAM_EXAMPLE.md, metrics.json).
Branch `tnn-native-lab`, repo `sylorlabs/TNN`, via `~/workspace/commit_racefree.py`
with lab-relative paths (`senses/pam-rebuild/forks/H2/...`, never `docs/lab/`
prefixed), `TMPDIR=~/workspace/tmp_commit`. No binaries, no `.zagd`, no
`.zag-cache`. Every commit verified via the GitHub API; SHAs reported.
