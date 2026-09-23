# SURVIVOR MECHANISMS — PAMs v2 autopsy (Team 3)

**Date:** 2026-09-23
**Scope:** Extract the load-bearing mechanisms from the two surviving lines
(R2-3, ALIVE on architecture; R2-8, DEAD on architecture, best safety numbers
in the program) and specify what PAMs v2 must be built from.
**Team context:** PAMs v2 must ACCEPT TRUTHS. R2-4 proved 0.0% false installs
is reachable; the missing property is installing TRUE judgments with high
confidence (RK-3 ≥ 85%). Every mechanism below is judged against both bars.

Sources (frozen, read-only — nothing here re-derives them):
- `round2/forks/R2-3/{VERDICT_R2-3.md,PREREG_R2-3.md,src/sense.zag,src/r2p_gates.zag,src/r2p_front.zag}`
- `round2/forks/R2-8/{VERDICT_R2-8.md,PREREG_R2-8.md,BUILD_NOTES.md,src/sense_r28.zag}`
  plus `~/workspace/r28work/{eval_phase1.py,eval_phase2.py,gen_r2q.py}` (Python
  orchestration — analyzed as data, not ported)
- `round2/debates/DEBATE_A_contract_property.md`, `DEBATE_B_self_flagging.md`

---

## 1. R2-3 — the admission instrument (white-box)

### 1.1 What it is

`src/sense.zag`: pure-Zag CLI (94,418-byte native binary from the pinned
toolchain), zero RNG, hash-chained ledger. CLI:

```
sense <gate_id> <pair_dir> <report_path> <ledger_path>
```

It is **not a PAM**. It is an instrument that scores OTHER gates against a
frozen paired battery. A candidate gate is registered as an integer id plus
four functions (`src/r2p_gates.zag`):

- `gate_name(id) -> []u8` — human-readable name (report + ledger header)
- `gate_formation_src(id) -> i32` — 0 = F blob (formation span), 1 = G blob
- `gate_gate_src(id) -> i32` — 0 = F blob, 1 = G blob
- `gate_judge(id, task, evidence) -> i32` — the gate's percept judgment on the
  declared bytes; judgment codes per task are shared (mirror `judge.py`)

The runner enforces:

1. **Rejection before evaluation.** A gate id `gate_valid` rejects, or whose
   src fns return anything outside {0,1}, is REJECTED before any pair runs.
   A gate that cannot name its disjoint evidence sets never executes.
2. **Declared-evidence feeding.** The runner feeds the gate ONLY the bytes it
   declared: formation judgment `jf` on the `formation_src` blob, gate
   judgment `jg` on the `gate_src` blob.
3. **The admission law.** Decision per pair: WITHHOLD iff `jf != jg`;
   otherwise ADMIT.
4. **Mechanical overlap audit.** `gate_src == formation_src` → the gate's
   evidence overlaps formation on every pair (reported as `overlap_pairs`,
   `overlap_pct_x100`). Kill criterion: a candidate that passes while
   `overlap_pairs > 0` FALSIFIES THE INSTRUMENT.
5. **The bar.** Withhold rate on the 1,200 pairs ≥ 90%, else the candidate is
   REJECTED before evaluation. Positive control (id 1, "broken": formation_src
   = gate_src = F) must show 100% overlap and < 50% withhold — an instrument
   that passes everything is decoration.

### 1.2 What "formation-independent evidence" means operationally

Three concrete layers, all frozen before the build:

- **Declared disjoint spans per task** (PREREG_R2-3 §2, from R2_FIXTURE_SET.md):
  colordisc/colorconst — formation = frames 1–60, gate = frames 61–120
  (neutral illuminant); shapetrans — formation = full frame, gate = the
  non-overlapping quadrant holding the target unoccluded (spatial); pitchdisc/
  timbredisc — formation = seconds 0–2, gate = seconds 2–4 (same source,
  uncorrupted token); motiondir — formation = frames 1–50, gate = frames
  51–100 (clean high-contrast).
- **Generation-time verification.** The R2P generator *asserts* every F is
  verified fooled and every G verified clean; no unverified pair is written.
  The "interventional" character lives HERE — the fixture generator
  intervenes (fools the front on F, keeps G clean) — not in the runner, which
  is observational (it compares two judgments).
- **The withhold itself.** On fooled-front × clean-gate pairs, the naive
  front's judgment on F disagrees with its judgment on G (1200/1200), so the
  reference gate withholds 100%. This is Debate B's cross-validation
  principle (g) mechanized: the check is information-bearing precisely
  because it runs on evidence the formation span did not contain.

Results: reference gate 1200/1200 withheld (100.00%, bar ≥ 90%); broken
gate 1200/1200 overlap, 0/1200 withheld; 3/3 byte-identical runs; all 4
hash chains verified OK. Python↔Zag cross-validation: 0 mismatches on 4,800
compared fields (Python analysis-only).

### 1.3 Limits — the withhold-only analysis (v2-critical)

R2-3's decision rule is **symmetric-disagreement → withhold**. On the R2P
battery every pair is fooled-front × clean-gate BY CONSTRUCTION. Consequences:

1. **It can never ADMIT.** The instrument has no true-install path. A gate
   that withholds 100% of everything — including true, clean presentations —
   scores 100% on B5 and is indistinguishable from the reference gate.
   There is no recall companion, no true-control pairs, no "this gate admits
   truths" measurement. A perverse always-withhold gate passes with the
   reference gate's exact score.
2. **It is a gatekeeper, not a gate.** It scores candidate gates; it installs
   nothing. It can keep bad gates out of the program; it cannot build a good
   one.
3. **Its "intervention" is in the fixtures, not the decision procedure.**
   The runner compares judgments; the fooling was done at suite-build time.
   For v2's INSTALL path, intervention must live in the gate's own decision
   rule (this is exactly what R2-8's leg-ii supplies — §2).

**v2 implication:** keep R2-3's instrument as the admission harness — the
declared-evidence architecture (feed only declared bytes + mechanical
overlap audit) is the program's durable tooling for catching gates that
secretly re-read formation evidence. But v2's install mechanism must come
from elsewhere, because truth acceptance is structurally outside R2-3.

---

## 2. R2-8 — the interventional gate (white-box + port spec)

### 2.1 What was built and why it died

R2-8 = Grok-4.6's HC-6 (P3+P9+P11): INSTALL only if an executable program
derived from the percept (i) predicts successfully on ≥1 held-out source
informationally independent of formation, AND (ii) produces a clear FAIL on
≥3 adversarial perturbations of that source.

- **Pure Zag (lives):** `src/sense_r28.zag` — the percept front-end (adapted
  from Approach A, algorithms unchanged), CLI `sense <task> <fixture_path>`
  → `judgment=, confidence=, margin=, feature=, ops=` lines, zero RNG.
- **Python (died on):** the two-leg gate decision and the hash-chained
  ledger. Architecture violation → DEAD, regardless of numbers.

Measured with the Python gate: **0.11% false installs** (13/11,630, bar
<0.5% — best in the program), **99.5% high-confidence wrongs self-flagged**
(2,440/2,453, bar ≥95%), leg-ii ablation +13.70pp over leg-i-only
(13.81% → 0.11% — the perturbation leg is load-bearing), contract-less
ablation 21.09%. Cost: 5× percept ops. Install profile: **36/11,630
installs (0.3%)** — extreme conservatism; recall NOT measured and almost
certainly fails the 70% bar. R2-8 buys safety by nearly never installing.

### 2.2 The percept contract (already pure Zag — port by keeping)

Per task, integer-only, the binary computes a 4-tuple
`(judgment, confidence, margin, feature)`:

| Task | Judgment vocab | Decision rule | Margin | Feature | K (conf) |
|---|---|---|---|---|---|
| colordisc | SAME/DIFFERENT | half-mean RGB euclid (isqrt) > 40 | \|dist−40\| | dist | 12 |
| colorconst | SAME_SURFACE/DIFFERENT | von Kries white-patch discounted means (per-mille) > 150 | \|dist−150\| | dist | 30 |
| shapetrans | CIRCLE/SQUARE/TRIANGLE | 12×12 downsample, SAD vs prototypes | SAD to nearest OTHER proto | ratio | 70 |
| pitchdisc | SAME/HIGHER/LOWER | zero-cross freq [0.10,0.80)s vs [1.10,1.90)s, rel <2% → SAME | \|fB−fA\| milli | d | 6643 |
| timbredisc | PURE/DARK/RICH/BRIGHT | harmonic spectral centroid, real DFT, nearest of 4 | min margin vs 3 others | r | 27 |
| motiondir | STILL/N/NE/E/SE/S/SW/W/NW | block-match 8 dirs, per-pair votes | vote margin | mag | 1 |

`confidence = 1000*margin/(margin+K_task)`. The K values were recalibrated
from Approach A's (60→12, 120→30, 150→70, 50000→6643, 200→27, 4→1) from the
**median correct margin on the frozen 370 primary**, mapping typical correct
margins to ~750–800 so the 700 gate threshold can fire. **Caveat (do not port
blindly): the K constants were calibrated on the same 370 fixtures scored
for B1.** v2 must re-derive K on a held-out split before freezing.

### 2.3 The gate algorithm (exact, from eval_phase2.py + BUILD_NOTES)

Per trial `(task, kind, idx, truth)`:

- **Presentations.** F-trial: X = Fi (adversarial file), S = Gi (clean
  independent presentation — same truth, fresh measurement, disjoint noise
  stream `pseed = stream_seed(20260923, 700+taskidx, index)`). G-trial:
  X = Gi, S = Fi.
- **Perturbations** (frozen per fixture at suite-build, from gen_r2q.py):
  P1 = Gaussian noise (σ=8 RGB; σ=300 LSB audio), P2 = exposure/gain ×1.25,
  P3 = JPEG q=70 recompress (images/video) / 8-bit quantize (audio).
- **Percept step.** Run the Zag front-end on X, S, P1, P2, P3 → 5×
  `(judgment, confidence, margin, feature)`.
- **Leg-i (cross-source prediction):**
  `leg_i = (jx == js) ∧ (cx ≥ 700) ∧ (cs ≥ 700)`
- **Leg-ii (intervention), per perturbation k:**
  `leg_ii_k = (jp_k != jx) ∨ |fx − fp_k| > 3σ_task`
  Frozen 3σ per task (feature units): colordisc 2.8, colorconst 54.2,
  shapetrans 17.5, pitchdisc 40.2, timbredisc 2.6, motiondir 10.0.
- **Decision:**
  `install = leg_i ∧ all(leg_ii_k)`;
  disposition = INSTALL if install; else FAIL if ¬leg_i; else UNRESOLVED.
- **Ledger.** Hash chain, genesis `SHA256("R2-8-genesis-20260923")`;
  entry = `SHA256(canonical(task,kind,idx,jx,cx,js,cs,disposition,truth,prev))`;
  11,630 entries, head `001f3a17db43dd57`.

**Load-bearing semantics of leg-ii (the discovery).** Note the direction:
leg-ii demands the percept be FRAGILE under intervention — every
perturbation must flip the judgment or move the feature beyond 3σ. This is
the do-operator check (Debate A P11): a percept that does not track its
input under deliberate perturbation cannot be trusted to have formed FROM
the input. A stuck or adversarially stabilized readout FAILS leg-ii.
Leg-i supplies stability across independent sources; leg-ii supplies
responsiveness to intervention. Together they pin the percept from both
sides. The ablation proves leg-ii carries the safety: 13.81% → 0.11%.

**Install profile (from evidence/trials.json):** 36 installs = 31 F-trial +
5 G-trial; 23 correct, 13 false. Dominant pattern: colorconst F-trials
(19/19 correct — the adversarial Fi failed to fool the percept relative to
Gi). The gate installs only when the percept is both stable (leg-i) and
fragile (leg-ii) — a combination true presentations rarely satisfy under
these perturbation strengths either. That is the recall gap v2 must close.

### 2.4 ⚠️ Frozen discrepancy the v2 crew must resolve

The prereg (HC-6, §"Frozen interventional leg") says: "the SAME independent
source is subjected to ≥3 frozen adversarial perturbations" — i.e. F-trial →
perturbations of **Gi** (the independent source). The original driver
`eval_r28.py` implements exactly that mapping. But the REPORTED evidence
(`evidence/trials.json`, `evidence/LEDGER.txt`, written 14:54) was produced
by `eval_phase2.py` with the **flipped** mapping: F-trial → Q (perturbations
of **Fi**, the adversarial source); G-trial → P (perturbations of Gi).

The published safety numbers (0.11% false, 99.5% self-flag, 13.70pp leg-ii
gain) attach to the **flipped** mapping. The prereg's mapping was never
measured in the final battery. **v2 must freeze one mapping and re-measure.**
Recommendation: follow the prereg text (perturb the independent source),
run both mappings in the calibration battery, and report the delta — the
delta itself is informative about whether leg-ii's power is "fragility of
the true percept" or "fragility of the fooled percept".

### 2.5 Load-bearing vs scaffolding

**Load-bearing (port these):**
- The two-leg decision rule with exact semantics: leg-i = agreement on an
  independent source ∧ dual confidence ≥ 700; leg-ii = all-3-perturbations
  flip-or-shift-beyond-3σ; INSTALL ⟺ leg-i ∧ leg-ii.
- The disposition trichotomy INSTALL/FAIL/UNRESOLVED (UNRESOLVED as the
  honest third state — Debate B's synthesis: it is what let the gate be
  safe at 108/108 while programs self-flagged 38.9%).
- The frozen per-task 3σ table in feature units (the noise model the
  intervention is judged against).
- The declared-independence fixture design: Gi = fresh measurement, same
  truth, disjoint deterministic stream; perturbations frozen per fixture at
  suite-build time (P1 noise / P2 gain / P3 compression-quantize family).
- The hash-chained ledger entry format (task, kind, idx, jx, cx, js, cs,
  disposition, truth, prev).

**Scaffolding (do not port):**
- Python orchestration: ThreadPoolExecutor over 46,520 files,
  `percept_cache.json` (perf optimization), `trials.json` (analysis record),
  numpy-based perturbation application (numpy is a build tool; the
  perturbations' DETERMINISM is the property, via `pseed`).
- Bars/ablation computation scripts; the b6 percept-only check.
- The recall-companion generation (incomplete; superseded by v2's recall
  battery).

**Do-not-port-blindly (methodological caveats):** the K-calibration overlap
(§2.2), the mapping discrepancy (§2.4), and two vocabulary mismatches vs
R2-3 — shapetrans codes (R2-3: 0=CIRCLE,1=TRIANGLE,2=SQUARE; R2-8:
cls 0=CIRCLE,1=SQUARE,2=TRIANGLE) and motiondir STILL indexing (R2-3:
8=STILL; R2-8: 0=STILL, 1=N…8=NW). v2 unifies the vocabularies.

### 2.6 Pure-Zag port spec

**Decomposition** (three modules + frozen manifest):

1. **`percept.zag`** — keep `sense_r28.zag`'s six task functions essentially
   verbatim (proven Zag; B6 passed for the front-end). Contract: the in-
   process function returns `(j_code:i32, conf:i64, margin:i64, feat:i64)`;
   the standalone CLI `sense <task> <path>` keeps the key=value output for
   unit use. Judgments compared as small INTEGER codes per task (never
   string-compare in the gate path).
2. **`gate.zag`** — NEW, the decision core. CLI per trial:
   `gate <task> <x_path> <s_path> <p1> <p2> <p3> <truth_code> <ledger_path>`.
   Links the percept functions in-process (no subprocess per file — the
   46,520-file threadpool was scaffolding; the gate runs 5 percepts per
   trial sequentially). Computes leg-i/leg-ii, appends one ledger entry,
   prints disposition. Thresholds and 3σ as frozen `i64` constants.
3. **`runner` (Python glue, allowed)** — generates the frozen trial manifest
   from `SCENES.json` + r2q dir listing (task, kind, idx, 5 paths, truth
   code); the Zag gate does every decision. A second Python script replays
   the ledger independently (R2-3's `src/mirror/verify_ledger.py` pattern).
4. **Ledger format** — adopt R2-3's proven binary-entry style:
   `entry = prev_hash(32) || seq(4BE) || jx(1) || js(1) || leg_i(1) ||
   leg_ii_bits(1) || disposition(1) || truth(1)` → SHA256 → next prev;
   human-readable hex line appended. Byte-deterministic, independently
   re-verifiable, no wall-clock.

**3σ in integer fixed-point** (features are integers; avoid float entirely):
compare `|fx−fp|*10 > T` with T: colordisc 28, colorconst 542,
shapetrans 175, pitchdisc 402, timbredisc 26, motiondir 100.
All arithmetic in `i64`; features are small — no overflow risk at these
magnitudes.

**znc constraints the design respects** (from `~/AGENTS.md`):
- No slice > 2^25 bytes: process one trial at a time; fixture read buffer
  ≤ 8MB (sense_r28's proven size); ledger written incrementally.
- The `as []i32` consecutive-cast aliasing bug (ZNC-2026-09-21-007):
  use `[]u8` arenas with `t_put32`/`t_get32` accessors — sense_r28.zag
  already follows this pattern; copy it.
- `nio_free` only what `nio_alloc` returned; never free `_zag_arg` results
  (both sources obey this; keep it).
- `u64 >>` is arithmetic and `u64 %` is signed: keep ALL gate arithmetic
  in `i64` (R2-3's `(seq >> 24) & 255` on i64 is the proven pattern for the
  4BE seq encoding).
- No 5-deep else-nesting (flatten with early returns — the disposition
  logic is naturally flat); no bare `{...}` blocks (helper functions);
  `return;` with semicolon in void fns.
- `_zag_slice_ptr` for syscalls: both R2-3 and R2-8 built and ran with
  this pattern — keep it verbatim, regression-test one byte-identical run
  against the old artifacts before trusting a fresh binary.
- No single-slice index limits: percept arenas are small (12×12 grids,
  frame buffers); the largest working set is one fixture in memory.
- State: flat structs ≤ 8 fields or global arrays indexed by trial id; no
  nested large structs; never chain `s.field.subfield` — copy to a local
  first (ZNC-2026-09-21-012).
- Build: one build dir containing the sources plus
  `R33_NATIVE_SHA256_V2.zag` + `R33_NATIVE_IO_V1.zag` next to `cl/`;
  toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  writes with O_WRONLY|O_CREAT|O_TRUNC (577), never O_EXCL (the silent-
  stale-file gotcha).
- Zero RNG everywhere in decision paths; all thresholds frozen constants;
  byte-identical reruns required (≥3 + independently verified hash chain).

**Porting order:** (1) `percept.zag` extracted from sense_r28.zag, CLI
byte-identical output vs the old binary on the 370 primary; (2) `gate.zag`
with the leg-i/leg-ii rule, cross-validated against eval_phase2.py's
4,800-field agreement method (R2-3's Python↔Zag xval pattern) on a trial
sample; (3) full-battery run ×3 + independent ledger re-chaining; (4) the
mapping experiment (§2.4) before freezing v2's rule.

---

## 3. THE V2 MECHANISM LIST

Minimal load-bearing set for (a) false installs ≈ 0 AND (b) true
high-confidence installs ≥ 85% (RK-3). Each entry: what it is · which
failure mode it addresses · knowledge-vs-machinery classification.

**M1 — Declared disjoint evidence + mechanical overlap audit** (R2-3).
What: every gate names formation/gate evidence from a frozen per-task
declaration table; the runner feeds only declared bytes and mechanically
audits overlap (kill: pass with overlap > 0 falsifies the instrument).
Addresses: the shared-measurement trap — gates re-reading formation
evidence (killed all six round-1 forks; Debate A §2). Classification:
MACHINERY (runner/audit) + KNOWLEDGE (the per-task disjointness
declarations, frozen in prereg). Role in v2: admission harness for
candidate gates — keeps bad gates out; cannot install.

**M2 — Interventional withhold test** (R2-3 battery; Debate A HC-3).
What: paired fooled-front × clean-gate fixtures; candidate must withhold
≥ 90%. Addresses: gates that cannot detect fooling even when clean
disjoint evidence disagrees. Classification: MACHINERY (battery +
instrument) + KNOWLEDGE (fixture design: how to fool each front-end while
keeping the gate span clean). Role in v2: the admission bar every
candidate gate clears before its install rule is evaluated.

**M3 — Cross-source agreement with dual high-confidence** (R2-8 leg-i).
What: `jx == js ∧ cx ≥ 700 ∧ cs ≥ 700` on an informationally independent
source (fresh measurement / later time / different modality). Addresses:
single-span fooling — the adversary owns one presentation but not the
independent re-measurement. Classification: MACHINERY (the rule) +
KNOWLEDGE (the 700 threshold; what counts as "independent" per task).
Caveat: leg-i ALONE was not enough — ablation 13.81% false installs.
Necessary, not sufficient.

**M4 — Intervention-fragility check** (R2-8 leg-ii).
What: ≥3 frozen perturbations of the adjudicated source must EACH flip
the judgment or move the feature beyond the frozen per-task 3σ. Addresses:
stuck/rote readouts and adversarially stabilized wrong judgments — a
percept that doesn't track its input under do-operator intervention can't
be trusted to have formed from the input. Classification: MACHINERY (rule
+ frozen σ table) + KNOWLEDGE (perturbation families that discriminate
per task; σ values from a frozen noise model). This is R2-8's load-bearing
discovery: leg-ii carried the 13.70pp safety gain (13.81% → 0.11%).

**M5 — INSTALL/FAIL/UNRESOLVED disposition trichotomy** (R2-8; Debate B).
What: UNRESOLVED as an honest third state; INSTALL only on leg-i ∧
leg-ii; FAIL on leg-i failure. Addresses: forced binary decisions that
manufacture false installs from uncertainty (Debate B: the gate withheld
108/108 while programs self-flagged 38.9% — the trichotomy is what made
gate-level safety possible without calibrated self-flagging).
Classification: MACHINERY.

**M6 — Executable warrant executed by the GATE** (Debate A P3 composite;
Debate B layer verdict).
What: the percept is a bounded deterministic program carrying fixed tests;
the GATE (independent mechanism) canonicalizes and executes the tests on
declared evidence; the program's self-result is a triage signal, never the
verdict. Addresses: same-evidence self-certification (H2 kill-2: 38.9%).
Classification: MACHINERY. In v2 this is literally `gate.zag`: an
independent executor of fixed tests on declared evidence.

**M7 — Claim-discriminative challenge** (Debate A P10, from Sol).
What: the check must make competing interpretations predict DIFFERENT
outcomes — perturbations chosen to separate the claimed class from its
strongest plausible alternative, not generic noise. Addresses:
independent-but-non-discriminating evidence (independent irrelevance —
Debate A's joint correction: independence is necessary, not sufficient).
Classification: mostly KNOWLEDGE (per-task discriminative perturbation
design) + MACHINERY (the flip/shift test). Least mechanized survivor;
R2-8's leg-ii is only incidentally discriminative. v2 design work required.

**M8 — Addressable provenance + hash-chained ledger** (Debate A P2 audit
role; R2-3/R2-8 ledgers).
What: every disposition carries addressable evidence spans and lands in a
byte-deterministic, independently re-verifiable hash chain. Addresses:
un-auditable installs and unverifiable safety claims. Classification:
MACHINERY. Never authorizes install — audit property only (Debate A §4
ruling stands).

**M9 — Withholding-first default with paired recall bar** (Debate B (b) +
RK-2/RK-3).
What: default UNRESOLVED; promotion requires positive evidence (M3∧M4);
every safety rate bar ships with its recall pair (RK-3: ≥85% of correct
high-confidence percepts reach INSTALL) so withhold-everything dies.
Addresses: the exact trap v2 exists to avoid — R2-8-style over-conservatism
(0.3% install rate) passing safety bars while accepting no truths.
Classification: KNOWLEDGE (prereg bars) + measurement instrument (the
battery must contain true controls, which R2P lacks and R2Q's recall
companions only began).

**How they compose — the v2 install rule:**

```
INSTALL ⟺ M3 (independent-source agreement, dual conf ≥ 700)
         ∧ M4 (all ≥3 interventions flip judgment or shift feature > 3σ)
         ∧ M1/M2 (the gate itself passed the R2-3 admission instrument)
disposition ∈ {INSTALL, FAIL, UNRESOLVED}                      (M5)
program's self-result = triage signal only, never the verdict  (M6)
every disposition ledger-bound with addressable evidence        (M8)
perturbations designed to discriminate claim vs nearest alternative (M7)
safety bars always paired with recall bars                     (M9)
```

**What v2 must ADD beyond the survivors (the truth-acceptance gap):**
R2-3 cannot admit (withhold-only, §1.3). R2-8 can install but installs
almost nothing (36/11,630, recall unmeasured, near-certainly <70%). So
v2's load-bearing NEW work is the admit-path calibration: vary the 700
threshold, the 3σ table, and perturbation strengths/design, and measure
the ROC (false-install vs true-install) on a NEW frozen suite with true
controls — Debate B's (f) deliberate-revision with the constitutional
anti-gaming veto, answering Grok's post-hoc objection structurally (new
suite, new frozen bar, ledgered revision budget). The ablations prove the
knobs exist (leg-ii moved 13.70pp); the job is finding the operating point
where TRUE high-confidence percepts pass at ≥85% while false stays <0.5%.
M7 (discriminative-by-design perturbations) is the principled lever: a
perturbation that separates the claimed class from its nearest alternative
should break WRONG percepts while leaving TRUE percepts' judgments intact
but their features responsive — which is exactly the leg-i∧leg-ii
conjunction.

---

## 4. Open questions for the v2 fork crews

1. **Perturbation mapping (§2.4):** prereg says perturb the independent
   source; the measured evidence perturbed X. Freeze one, run both in the
   calibration battery, report the delta.
2. **Recall measurement:** R2-8 never measured true-install recall on the
   held-out shapetrans/timbredisc companions. v2's first deliverable is the
   admit-path calibration battery with true controls.
3. **K recalibration:** re-derive the confidence K constants on a held-out
   split (they were fit on the scored 370). Same for the 3σ table —
   confirm it comes from a frozen noise model, not the eval set.
4. **Vocabulary unification:** shapetrans codes and motiondir STILL
   indexing differ between R2-3 and R2-8 (§2.5). One frozen codebook for v2.
5. **Production independent-source protocol:** Gi was a fresh re-render —
   in production this must be a second measurement, later time window, or
   second modality. v2 must define what the independent source IS outside
   fixtures, per task.
6. **Inherit Debate B's repaired bar set:** RK-1 (false installs ≤3%),
   RK-2 (wrong high-conf installed ≤1%), RK-3 (correct high-conf installed
   ≥85%), RK-4 (contract-less ablation ≥100 installs — proves the gate does
   the filtering), RK-6 (escalations ≤5%, p95 ops ≤40% of Approach A), RK-7
   (byte-identical reruns). Attach each bar to its layer (gate vs program
   vs battery) so no future kill-2 tests the wrong layer.
7. **Generality of fragility:** is leg-ii's "must be fragile" requirement
   a law or a quirk of the R2Q perturbation strengths? Test on a second
   perturbation family before declaring it. Note the tension: stronger
   perturbations make leg-ii easier to satisfy for TRUE percepts too
   (feature shifts), which is the admit-path lever — but may also flip
   true judgments (recall loss). The calibration battery decides.
8. **Debate A's composite contract** (executable warrant +
   formation-independent evidence + discriminative-vs-alternatives +
   interventional form) is the property the v2 prereg should name. M1–M9
   above are its mechanism decomposition. The v2 prereg should cite this
   file as the mechanism source.
