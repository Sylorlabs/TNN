# Frozen Preregistration: TNN NATIVE-DELIBERATION Epistemics

**Status:** FROZEN — this document is the trial law for the native-deliberation
epistemic line. Any change to design, bars, metrics, or scoring rules requires
a dated amendment authorized by Micah before execution. No amendment may weaken
a kill bar mid-trial.

**Authorization:** Micah's course-correction of the scale-epistemics program
(2026-09-27): "contradiction detector sounds like we're going down the rigid
architecture path — shouldn't the architecture do this natively?" Attempts 1–3
stay frozen for comparison; nothing in them changes.

**Frozen date:** 2026-09-27
**Workdir:** `~/workspace/epistemic_native/`
**Phase:** PREREG ONLY — no implementation in this phase. A separate coordinator
implements from this frozen document; a third red-teams; the parent scores as
honest broker.

---

## 1. Claim under test

> **Claim:** Epistemic status ("does this contradict what I know?") is judged
> by TNN's OWN DELIBERATION on the genuine-deliberation machinery — readings
> over the claim, retrieval of candidate knowledge from the 448-item mass,
> deliberative contradiction judgment, verdict or UNDETERMINED+NEED — and the
> comparison EMERGES from the machinery's bid/elimination/argmax, not from a
> crew-built comparator.

**Anti-claim (what falsifies it):** the verdicts are actually decided by
crew-built machinery smuggled into the build — a value comparator, a dispute
or stance lexicon, a clash-detector module, or feature→verdict shortcuts —
with the ledger as decoration. The red-team plan (§10) is designed to kill
exactly this.

## 2. Background: why the rigid line died

Attempts 1–3 built a rigid pipeline: parse → entity+attribute addressing →
value comparison → verdict. Its failures have rigid fingerprints
(`docs/lab/epistemic_scale/attempt3/WHITEBOX.md` defects D1–D5):

- **D1** topical overlap ≢ evidential support (64 false facts);
- **D2** clash detector = surface-pattern matching (digit-only numbers,
  value-negation only, 14 antonym pairs);
- **D3** support gate vetoed genuine clashes (co-occurrence ≢ corroboration);
- **D4** dispute lexicon overfired on ordinary causal language;
- **D5** opinion detection lexical, not constructional (30/60 missed).

Attempt 3's deliberative-loop redesign did not operationalize
(`TRIAL_REPORT_ATTEMPT3.md` causes M1–M4): SUPPORT went vacuous (0/985 train
addressing pairs — the mass has no paraphrase density), contradiction
detection barely moved (5/84 vs 4/84), the opinion detector regressed
0.957→0.686, and the standing dilemma has no safe operating point
(uncontested-standing: 4 fact→lie FPs; corroborated-standing: 0 lie verdicts
at all). **Proven: the bottleneck is semantic parsing + value comparison,
NOT verdict logic** — so this line does not build a better comparator. It
removes the comparator's job from the crew entirely and tests whether
deliberation itself judges.

Two clean-room lines were quarantined before attempt 3's valid line
(`attempt3/BREACH.md`: train labels directed parser development;
`attempt3-clean/QUARANTINE.md`: implementer saw labels via class column +
class-encoding ID prefixes). The valid line ran under the honest-broker
structure this prereg inherits (§11).

## 3. Provenance: baseline numbers and bar resolution

### 3.1 Verified baselines (re-verified against the frozen documents, 2026-09-27)

| # | Measure | Value | Provenance |
|---|---|---|---|
| B1 | A2 held-out Fact P / R | 0.5327 / 0.7917 | `epistemic_scale/attempt2/SCORING.md` gate table |
| B2 | A2 held-out Opinion P / R | 0.9375 / 0.5000 | same (tp=30, fp=2, fn=30 → R=30/60) |
| B3 | A2 held-out Lie P / R | 0.5000 / 0.0278 | same (tp=1, fn=35 → R=1/36) |
| B4 | A2 held-out skepticism forced | 0.6667 (16/24) | same |
| B5 | A2 held-out exact | 88/192 (45.8%) | same |
| B6 | A2 train-LOO Fact P / R | 0.637 / 0.845 | `epistemic_scale/attempt2/MECHANISM.md` §3 |
| B7 | A2 train-LOO Opinion P / R | 0.887 / 0.957 | same (134/140 → R=0.9571) |
| B8 | A2 train-LOO Lie P / R | 1.000 / 0.048 | same (4/84 → R=0.0476) |
| B9 | A2 train-LOO skepticism forced | 0.179 | same |
| B10 | A3 valid-line train-LOO lie recall | 0.060 uncontested / 0.000 corroborated (bar 0.15) | `epistemic_scale/attempt3/TRIAL_REPORT_ATTEMPT3.md` §3 |
| B11 | A3 valid-line train-LOO opinion recall | 0.686 (bar 0.90) | same |
| B12 | A3 valid-line fact→lie FPs | 4 (uncontested) → 0 (corroborated) | same |
| B13 | A3 held-out | NOT run (NO-GO at train-LOO) | same |
| B14 | Held-out lies contradicted by train facts | 10/36 (attempt 2 caught 1) | `epistemic_scale/attempt3/WHITEBOX.md` §3 |
| B15 | Held-out lies asserting attributes the mass never addresses | 26/36 → PROVEN mass-only lie-recall ceiling ≈0.28 < 0.60 bar | same (information-theoretic; deliberation does not dissolve it) |

Convention note: attempt-2's parent scoring and attempt-3's prereg §6 judge
classification gates with skepticism items EXCLUDED from false positives
(skepticism has its own forced-verdict gate; counting them as FP
double-jeopardizes). Strict-convention numbers are reported alongside for
transparency (cf. `WHITEBOX.md` §1 discrepancy note). This prereg keeps that
convention.

### 3.2 The provenance flag — resolved

The parent's bars cite "attempt 2's lie recall" and "the 0.957 lexicon floor"
without naming the evaluation. The evidence shows:

- 0.957 is attempt-2's **train-LOO** opinion recall (B7); its **held-out**
  opinion recall was 0.5000 (B2).
- Attempt-2's lie recall was 0.0278 held-out (B3) and 0.048 train-LOO (B8).

**Resolution (frozen):** each bar applies **per-evaluation against the
same-evaluation attempt-2 number**:

| Bar | Train-LOO (448) | Held-out (192) |
|---|---|---|
| Lie recall (parent: "beat attempt 2") | **> 0.048** (B8) | **> 0.0278** (B3) |
| Opinion recall (parent: "no regression below the floor") | **≥ 0.957** (B7) | **≥ 0.5000** (B2) |
| Fact→lie false positives (parent: "above attempt-3's 0 (corroborated)") | **= 0** (B12 corr.) | **= 0** |

**Coherence check (no flag-back required):** the bars are jointly satisfiable
on both evaluations — attempt 2 itself satisfied lie R>bar ∧ opinion R≥floor ∧
fact→lie FP=0 simultaneously on train-LOO (B7, B8, MECHANISM.md confusion: Fact
row has 0 lie verdicts), and the held-out lie bar (>0.0278) sits well under the
proven 0.28 ceiling (B15). No bar contradicts the evidence. The 0.60 lie bar
from attempt-3's prereg is NOT carried over (proven unreachable mass-internally,
B15).

## 4. Corpus, split, mass (unchanged from attempts 1–3)

- Corpus: `docs/lab/epistemic_scale/corpus/corpus.tsv`, SHA-256
  `8134416896ec1ee38a62e0ba12edc08e84699b1bb84c1a44f97efb4b0d1046d7`
  (640 items; class counts 240/200/120/80 exact).
- Split: held-out iff numeric_id mod 10 ∈ {0,1,2} → 448 train / 192 held-out
  (fact 72, opinion 60, lie 36, skepticism 24). Verified exact.
- The 448-item train mass is fixed and identical to attempts 1–2.
- Labels never enter TNN's view (§11).

## 5. The 26/36 wall — scoping decision (frozen)

**Decision: (a) — scope the trial to mass-visible judgments +
UNDETERMINED+NEED with causally-bound NEEDs.** No evidence actions in this
trial. Deliberation does not find absent facts; for the 26/36 unaddressed
lies the only honest mass-internal verdict is UNDETERMINED with the missing
premise named.

**Consequences, stated plainly:**

1. Held-out lie recall has a PROVEN ceiling of 10/36 ≈ 0.28 (B14/B15). The
   trial's lie bars (>0.0278 held-out, >0.048 train-LOO) are set under it.
   The trial does NOT test whether lie recall can reach 0.60 — that bar is
   dead for any mass-internal architecture by proof.
2. NEED emission is still REQUIRED and audited (§8): the deliberation must
   pose the question it cannot answer (the ask-for-more-info hook exists as a
   first-class output, causally bound to the verdict branch). It is simply
   not resolved by a sense in this trial.
3. A follow-up **evidence-action line** (NEED → deliberate audited web sense
   as untrusted observations, per attempt-3 prereg §5's design) is explicitly
   NAMED as future work and is NOT preregistered here. Attempt 3's 3b never
   ran (NO-GO rendered it moot: with SUPPORT vacuous, retrieved evidence had
   no working verdict arm — TRIAL_REPORT §5); the native line must first
   prove its verdict arm works mass-internally before any sense is attached.

## 6. Architecture: native deliberation

### 6.1 Substrate

The genuine-deliberation machinery from the dialogue line
(`docs/lab/dialogue/deliberation/ARCHITECTURE.md`; frozen
`build/deliberate_frozen_r4.zag`, SHA-256
`7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787`;
repair cycle #4; fourth red team PASS — `REDTEAM4_REPORT.md`): ledger rows,
GEN/ELIM/ARGMAX phase ordering, trace protocol (READ/CAND/ELIM/ARGMAX/
CONTENT), causally-bound readings (neuter-proven: all-row neuter changed
67/77 answers; the 10 insensitive turns are legitimate fixed points per
`NEUTER10_WHITEBOX.md`).

### 6.2 Required deliberation shape (pinned; implementation latitude inside)

For each claim, one deliberation turn over the ledger, in this phase order:

1. **GEN readings (kind-0 rows)** over the CLAIM: utterance-type readings
   (assertion / evaluative-construction / deontic / first-person-experiencer /
   plain — §7) and epistemic-situation readings. Readings are the SOLE
   classifiers: no other code may classify the claim.
2. **GEN candidate rows** for retrieved mass items: deterministic retrieval
   proposes candidates; each candidate's CONTENT is traced (the dialogue
   line's FACT-row analog). Retrieval proposes; it does not judge.
3. **GEN interpretation bids**: for each candidate, COMPETING readings of the
   same evidence bid against each other (e.g. "candidate X supports the
   claim" vs "candidate X contradicts the claim" vs "candidate X is merely
   topical"). **The comparison EMERGES here** — from these bids competing
   in ELIM/ARGMAX — not from a precomputed boolean.
4. **GEN verdict bids** (FACT / OPINION / LIE / UNDETERMINED+NEED) whose fire
   conditions read ONLY ledger rows (readings' evidence fields, surviving
   interpretation bids). Never raw claim text, never build-step outputs.
5. **ELIM → ARGMAX → trace.** Verdict = argmax winner; ties → lowest hid
   (substrate convention). Close-call protocol (margin <5 → CLOSE +
   2×CONTENDER + REVIEW) inherited from the substrate.

Ledger dimensions, bid base scores, and bonus schedules are the implementer's
choice — committed, auditable, and subject to the K1 reversal bar (§10).

### 6.3 What the implementer MAY build

- **Substrate mechanics**: may port ledger primitives, the GEN/ELIM/ARGMAX
  loop, trace emitters, and neuter hooks from the frozen repair-#4 line.
  These are settled substrate, not the hypothesis. The delta (what was
  ported vs written) is documented.
- **New epistemic GEN functions**: all readings, candidate handlers,
  interpretation bids, and verdict bids are NEW. No dialogue-classification
  logic (joke/resume/challenge/…) may leak in; the red team audits this.
- **Deterministic mechanical preprocessing** (Python build steps, committed):
  tokenization, a lexical retrieval index over the 448-item mass, and
  mechanical constructional feature codes (comparative/superlative syntax,
  deontic modals, first-person experiencers — syntax-level, deterministic).
  These are the SENSES. They carry no epistemic judgment.
- **The learning phase** (§7): deliberation over the mass that forms the
  utterance-type readings.

### 6.4 What the implementer may NOT build (crew-built comparator ban)

- NO value comparator: no `clash()`/`SUPPORT`/`CONTRADICT` module computing
  booleans outside the deliberation and handing them to the ledger.
- NO dispute lexicon, NO stance lexicon, NO antonym table used to drive
  verdicts — neither hand-authored nor label-induced (attempt 2's log-odds
  lexicon is the explicit anti-pattern).
- NO feature→verdict shortcuts: nothing outside GEN/ELIM/ARGMAX may assign,
  veto, or reweight a verdict. Retrieval rank/thresholds may not drive
  verdicts.
- NO label use anywhere: no class column, no label-induced statistics, no
  "opinion vs non-opinion" splits, no crew-authored word→verdict mappings
  (§7, §11).
- NO RNG anywhere (§9 K5).

**The bright line:** the crew builds senses (mechanical, deterministic,
judgment-free) and the deliberation engine; TNN's deliberation builds the
judgments. Any epistemic decision attributable to a crew artifact rather than
to a ledger bid competition is a red-team kill (§10, family 4).

### 6.5 Why this dissolves D1–D5 (falsifiable mapping)

| Defect | Native-dissolution mechanism | Falsifier |
|---|---|---|
| D1 topical≢support | "merely topical" is a competing interpretation bid; it must LOSE in ELIM for a FACT verdict — topical overlap alone cannot win | false-fact count does not collapse vs attempt 2 |
| D2 surface clash | contradiction is not a pattern list but a surviving contradict-interpretation bid over retrieved candidates, argued against support/topical bids in the ledger | <8/10 contradicted lies caught (§9 H1) |
| D3 support veto | no support gate exists to veto anything; competing bids adjudicate in ELIM; clash+support coexistence yields a surviving CONTESTED reading → UNDETERMINED (never FACT) | any vetoed-clash lie still called FACT |
| D4 dispute lexicon | no dispute word list exists; the skepticism hold = a surviving contested-evidence reading (mass-internal disagreement surfaced BY deliberation), never causal verbs | causal facts withheld (F091/F092/F181-type items called UNDETERMINED) |
| D5 lexical stance | opinion track = learned constructional readings + deliberated mass-addressability (§7), never a word list | opinion recall regresses below §3.2 floors |

## 7. Utterance-type knowledge: LEARNED, not hardcoded (standing law)

Surface markers ("I think", "should", evaluative adjectives, comparatives)
are knowledge TNN forms through deliberation over the mass — **facts first,
then utterance types learned, never hardcoded** (Micah's standing law).
They are neither a hardcoded lexicon nor banned by ontology.

### 7.1 Learning protocol (frozen)

- **Data:** the 448-item train mass ONLY, via the sanitized blind input
  (`~/workspace/epi_a3/blind/train_blind.tsv`, SHA-256 `ebd76e2c…`; opaque
  IDs, zero label information). No labels, no class column, no ID prefixes.
- **What is learned:** kind-0 utterance-type readings (evaluative-
  construction, deontic, first-person-experiencer, plain-assertion, …) as
  ledger-row definitions: each reading specifies how its evidence is computed
  per claim from mechanical constructional features, PLUS the formation
  record — which mass deliberations formed it and which addressability
  outcomes justify its epistemic role ("sarcasm is this and is used like
  this": the reading carries its learned use-conditions).
- **How:** a learning phase runs the deliberation machinery over the mass in
  study mode. For each mechanical constructional pattern, the deliberation
  poses the addressability question — "are claims built this way decided by
  the mass?" — via retrieval + interpretation bids. Patterns whose claims are
  systematically unaddressable, and whose interpretation bids never converge
  to FACT/LIE, form the opinion-track reading. **The mapping from
  construction to epistemic track is formed by this deliberation, never
  asserted by the crew.** The mass-addressability test itself is a
  deliberation (retrieval attempt + interpretation bids), not a build-step
  boolean.
- **Freeze point:** learning completes BEFORE any scoring. The learned
  readings (definitions + formation record + SHA-256) are committed.
  Train-LOO and held-out run with readings FROZEN — no learning during
  scoring, no per-item adaptation. Any change to the readings after the
  first scored run voids the trial.
- **FORBIDDEN in learning:** labels; the class column; label-induced
  statistics (no log-odds, no opinion-vs-non-opinion splits); crew-authored
  word→verdict or construction→verdict mappings; reading attempt-3's
  WHITEBOX.md §3 itemization or any labeled corpus to "check" formation
  (§11 denylist).

### 7.2 Learned-reading validity bars (part of the red-team brief, §10)

A learned reading is VOID if neutering it changes no verdict (decorative —
`NEUTER10_WHITEBOX.md` standard) or if the wrong-hypothesis flip (force the
reading to 1 on a claim it should not fire on) does not move the verdict to
that reading's bid. Formation records without causal readings are not
knowledge; they are annotation.

## 8. Verdict space (pinned)

TNN emits exactly one of:

- **FACT** — the assertion-track reading fired, retrieval returned addressing
  candidates, and the support-interpretation bids won ELIM/ARGMAX.
- **OPINION** — a learned utterance-type reading fired and its bid won.
- **LIE** — a contradict-interpretation bid survived ELIM uncontested (no
  surviving support bid for the same premise; no surviving
  contested-evidence bid undermining the contradictor).
- **UNDETERMINED + NEED** — no verdict bid survived, or a contested-evidence
  reading survived (mass-internal disagreement → the structural skepticism
  hold), or retrieval returned nothing addressable, or close-call. The NEED
  names the missing premise (`NEED: <entity> | <attribute>`-equivalent) and
  is emitted BY the verdict branch itself — the undetermined verdict and the
  NEED are one decision (causal binding, inherited from attempt-3 prereg
  §4.3.4). Verified by sample audit: the NEED must name the
  actually-unaddressed gap; decorative NEEDs void the trial.

Skepticism items (corpus class) are NOT a verdict TNN emits — per Micah's
standing rule they are excluded from true/false scoring. They are scored by
the forced-verdict gate: verdict ∈ {FACT, LIE} counts as forced;
OPINION or UNDETERMINED are acceptable holdings (§12).

## 9. Kill bars

**GO/NO-GO (train-LOO, broker-scored one-shot; ALL must hold or NO-GO —
do not run held-out):**

| # | Bar | Anchored to |
|---|---|---|
| K1 | Lie recall **> 0.048** | B8 |
| K2 | Opinion recall **≥ 0.957** | B7 (the lexicon floor — learned, not hardcoded, must match it) |
| K3 | Fact→lie false positives **= 0** | B12 (corroborated) — "don't buy recall with convictions of truth" |
| K4 | Determinism: 2/2 runs byte-identical (SHA-256 pinned) | substrate standard |

**Held-out (single shot, broker-scored one-shot; ALL must hold):**

| # | Bar | Anchored to |
|---|---|---|
| K1h | Lie recall **> 0.0278** | B3 |
| K2h | Opinion recall **≥ 0.5000** | B2 |
| K3h | Fact→lie false positives **= 0** | parent's bar |
| K4h | Determinism: 2/2 runs byte-identical (SHA-256 pinned) | substrate standard |
| K5 | **Zero RNG**: static audit (no RNG imports/calls in any language) + the byte-identical reruns | Micah's law: no randomness in decision paths |
| K6 | **≥8/10 contradicted lies caught**: of the 10 white-box-identified held-out lies contradicted by train facts (`WHITEBOX.md` §3: L020, L021, L022, L030, L040, L050, L051, L060, L062, L120 — original corpus IDs, mapped to blind IDs by the broker), at least 8 receive verdict LIE | B14 — "the native design must catch these, the signal exists" |

K6 is the operationalized white-box constraint: attempt 2 caught 1/10 with a
broken detector; a native deliberation that cannot use proven-present signal
falsifies the claim even if K1h passes on the unaddressed remainder.

**Other kill conditions:**

- Any verdict-relevant kind-0 row that is BOTH neuter-inert AND
  wrong-hypothesis-flip-inert is decorative → the native claim is VOID
  (§10 family 4; `NEUTER10_WHITEBOX.md` methodology).
- Static audit finds a verdict-path read of raw claim text or build-step
  judgment output bypassing the readings → VOID (the "no re-derivation"
  rule: classification helpers are called ONLY from the reading GEN —
  `ARCHITECTURE.md` "Reading-Row Causal Wiring").
- Any byte non-identity across reruns voids the determinism gate.
- Any label use by the implementer (labels, class column, labeled corpus,
  sealed mappings, verdict files, lexicon files — §11) voids the line; the
  broker quarantines it as attempt 3's two lines were quarantined.

## 10. Red-team plan (six families, adapted to epistemics)

The red team works from the frozen implementation + this prereg only, with
its own scripts and binaries; it touches nothing in the implementation
workdir. Verdict per family: PASS / VOID with mechanism-level evidence.

| # | Family | Bar | Adaption |
|---|---|---|---|
| 1 | **Reversal** (K1) | 0 verdict differences under mechanically reversed GEN call order (trace emission order cosmetic, as in `REDTEAM4_REPORT.md`) | deliberation order-independence, not answer luck |
| 2 | **KB flips** (K2) | (a) flip a mass item's asserted value → verdict on the addressing claim moves covariantly; (b) flip an unrelated item → byte-identical verdicts (locality); (c) plant a mass item contradicting the contradictor → the LIE verdict collapses to UNDETERMINED (native anti-false-conviction: contested evidence must surface IN deliberation, not via a standing module) | the native replacement for attempt-3's standing rule |
| 3 | **Bijection** (K3) | independent trace parser: every turn has the full READ→CAND→ELIM→ARGMAX→CONTENT chain; every fired bid cites its reading row; ELIM reasons in {PRE_FAIL, GATE, OUTSCORED}; no verdict without a surviving bid; ARGMAX winner always a valid CAND | trace-ledger structural audit |
| 4 | **Decorative / bypass** (K5, critical) | (a) static audit: every kind-0 row's evidence field has a read site on a fire-decision path; classification helpers called ONLY from the reading GEN; no verdict-path reads of raw text or build-step judgments. (b) dynamic neuter matrix: all-row neuter + per-row neuters must move verdicts (changed-sets map onto utterance/epistemic types; rows with no natural coverage proven causal on synthetic turns — `REDTEAM4_REPORT.md` §4c precedent). (c) **wrong-hypothesis flips** (stronger probe per `NEUTER10_WHITEBOX.md` methodology note): force each non-true reading to 1 → verdict must change to that reading's bid. Any verdict-relevant row neuter-inert AND flip-inert = decorative → VOID | kills the smuggled-comparator anti-claim |
| 5 | **Close-call** | synthetic margin-<5 cases → CLOSE + 2×CONTENDER + REVIEW, margins mutually consistent across trace lines | substrate protocol, epistemic bids |
| 6 | **Traps** | (a) planted lie-vs-lie mass pairs → UNDETERMINED, never LIE; (b) claims addressing nothing → UNDETERMINED+NEED with the NEED naming the actual gap (sample-audited); (c) opinion constructions over mass-ADDRESSED dimensions → must NOT be OPINION (addressability decides, not syntax); (d) deontic/first-person constructions → OPINION only via the learned reading, never via crew rule | honesty under adversarial mass |

## 11. Implementer protocol (label-blind; honest broker)

- The implementer works ONLY from: (1) this frozen prereg; (2) the four
  deliberation substrate documents (`docs/lab/dialogue/deliberation/
  ARCHITECTURE.md`, `EVIDENCE_R4.md`, `NEUTER10_WHITEBOX.md`,
  `REDTEAM4_REPORT.md`); (3) the sanitized blind inputs
  `~/workspace/epi_a3/blind/train_blind.tsv` (448 items + header, SHA-256
  `ebd76e2ca32e18aa66b65a17afa9601ce22c6ce9666a1b2d7d2271ac2b9ec941`) and
  `~/workspace/epi_a3/blind/heldout_blind.tsv` (192 items + header, SHA-256
  `2bf4c0724b27bfd7ffbf8c58e23de1d30c1be80a9bbea0a121cc2836bf20ff06`)
  — opaque IDs, zero label information.
- **FORBIDDEN** (any access voids the line; list pinned in this prereg):
  `~/workspace/epi_a3/_coordinator/MAPPING.sealed`,
  `~/workspace/epi_a3/attempt3-clean/idmap.sealed`,
  any `*verdicts*.tsv` (incl. `~/workspace/epi_a3/attempt3-final/
  loo_verdicts.tsv`, `loo_verdicts_corr.tsv`),
  `dispute_final.txt`, `stance_final.txt`, `cleanroom_train.tsv`,
  `harness_full_QUARANTINED_contaminated/`,
  the labeled corpus `docs/lab/epistemic_scale/corpus/corpus.tsv`,
  and ALL of `docs/lab/epistemic_scale/attempt2/` and
  `docs/lab/epistemic_scale/attempt3/` (preregs, whiteboxes, reports,
  mechanisms, scorings — including the WHITEBOX.md §3 itemization, which
  names lie IDs).
- The implementer does not score, does not see labels, does not infer
  classes. Train-LOO verdicts are emitted by opaque ID; the PARENT (honest
  broker) holds the sealed mapping and scores one-shot after the
  learning+build freeze. Held-out is a SINGLE shot; outputs frozen +
  SHA-256-pinned before scoring.
- No label-informed iteration: the parser/senses, the learning phase, and
  the deliberation are frozen before the first scored run. At most ONE
  mechanical re-run for crashes/non-convergence (no linguistic tuning).
  The broker reveals no scores until all outputs are frozen.

## 12. Scoring

- Per frozen prereg §3.2 bars, judged on the parent convention (skepticism
  excluded from classification FPs; strict-convention numbers also reported).
- Skepticism forced = verdict ∈ {FACT, LIE} (reported; attempt-2/3 bar ≤0.15
  as a non-kill guardrail).
- Takeaways: the attempt-2 emitter (12/12 grounded+valid) is re-emitted and
  judged blind per the same rubric — REPORTED for continuity, not a kill bar.
- Report: corpus SHA, split counts, prereg hash; train-LOO confusion +
  per-gate numbers (the GO/NO-GO record); held-out confusion, P/R per class,
  skepticism rate, K6 item checklist, NEED sample audit, determinism hashes,
  red-team family verdicts; gate-by-gate comparison attempt 1 vs 2 vs 3 vs
  native (both FP conventions); overall verdict with the ceiling (B15)
  restated.

## 13. Commit protocol

API replay (push auth broken): fetch + parent on the CURRENT origin tip at
commit time; verify each tree level's SHA by walking non-recursively (never
`?recursive=1` — it truncates on large trees); raw urllib if the gh-api
wrapper chokes on IncompleteRead. No binaries, `.zagd`, `.zag-cache`, or
derived regenerables in the repo. Reference implementation:
`~/workspace/growwithme/api_commit.py`.

## 14. Amendment record

| Date | Amendment | Authorized by |
|---|---|---|
| 2026-09-27 | Initial freeze (native-deliberation epistemic line) | Micah's course-correction 2026-09-27 ("shouldn't the architecture do this natively?") |
