# Frozen Preregistration: TNN SCALE EPISTEMIC Trial

**Status:** FROZEN — this document is the trial law. Any change to design, bars, metrics, or scoring rules requires a dated amendment signed by Micah before execution. No amendment may weaken a kill bar mid-trial.

**Frozen date:** 2026-09-26
**Workdir:** `~/workspace/epistemic_scale/`

---

## 1. Background and Motivation

Prior epistemic tests (skepticism-category ruling, K2/K3 false-install probes, KB4 SUSPECT-gate trial) ran on handfuls of facts. Micah's scale objection is recorded verbatim: *"if I had only 3 things I'd probably do worse than TNN"* — a small test cannot tell whether TNN is discriminating epistemic status or getting lucky on a tiny probe set. The hypothesis under test is:

> **Claim:** TNN discriminates epistemic status (fact / opinion / lie) from mass information — classification driven by content and corroboration/contradiction structure across a large installed mass, not by surface pattern-matching of a few planted probes.

This trial scales to ~640 real English statements so that discrimination, if present, must survive a mass of conflicting claims, corroborating claims, and opinionated-but-true-adjacent content — the environment a real intelligence actually lives in.

---

## 2. Non-Goals (explicit)

- This is **not** about teaching TNN new facts. Learning gains are not measured and are not the point.
- This is **not** a knowledge-retrieval or memorization test.
- This is **not** about whether TNN's opinions agree with any external authority's opinions. Opinion classification is judged on *status* (is this item an opinion?) — never on whether the opinion is right.
- This is **not** a speed or efficiency test.

The measured quantities are discrimination (classification from content + cross-item structure) and takeaways (what TNN concludes from the installed mass).

---

## 3. Corpus (fixed design)

File: `corpus.tsv`, in the workdir. 640 statements, tab-separated, header row:

```
id\ttext\tclass\tprovenance
```

- **240 facts** — ids `F001`..`F240`, `class=fact`. Real, verifiable claims with recorded provenance (source description in the `provenance` field).
- **200 opinions** — ids `O001`..`O200`, `class=opinion`. Genuine opinions: value judgments, aesthetic preferences, political/social positions held by real people. Recorded as opinions, never as facts; provenance names the holder class (e.g. "columnist", "survey respondent") without endorsing or rejecting the position.
- **120 lies** — ids `L001`..`L120`, `class=lie`. Deliberate falsehoods: claims that are factually wrong and planted as assertions of fact (not framed as opinion). Must be wrong on checkable grounds; the corpus records them as `class=lie` with a provenance note describing the planting context.
- **80 skepticism-class** — ids `S001`..`S080`, `class=skepticism`. Claims with two sides, no clear fact, and real public disagreement (per Micah's standing skepticism rule, 2026-09-22). These are never scored true/false.

Constraints on corpus construction:
- No duplicate or near-duplicate statements across the corpus.
- Each fact must be checkable against its provenance source at corpus build time.
- Each lie must be a genuine falsehood (not a disputed claim — disputed claims belong in skepticism).
- Opinion items must not be trivially detectable by keyword ("I think", "in my opinion" heuristics are forbidden as build features; the corpus should contain opinions stated in factual-sounding language and facts stated in opinion-sounding language so surface style cannot carry the label).
- Corpus content is fixed once built and SHA-256-pinned in the trial RUNLOG before training begins.

---

## 4. Train/Test Split (deterministic, no randomness)

Split computed purely from item ids:

- An item is **HELD-OUT (test)** iff `numeric_id mod 10 ∈ {0, 1, 2}`.
- All other items are **TRAIN (installed)**.

Expected held-out counts (exactly 30% of each class when class sizes are multiples of 10):
- Facts: F001..F240 → ~72 held out, ~168 train
- Opinions: O001..O200 → ~60 held out, ~140 train
- Lies: L001..L120 → ~36 held out, ~84 train
- Skepticism: S001..S080 → ~24 held out, ~56 train

**192 held-out, 448 train.** The actual counts are computed from the corpus and recorded in the RUNLOG; the 70/30 proportion is a consequence of the rule, not a tunable.

The split script and its output (full train/test id lists) are committed before training. No re-splitting, no stratification tricks, no held-out peeking during training.

---

## 5. Training Procedure

- All 448 train items are installed into TNN's store via native intake, each with its **provenance** recorded.
- **Labels are NEVER installed and NEVER visible at test time.** The store holds `(id, text, provenance)`; the `class` column never enters TNN's view in any form.
- The test-time classifier sees only: the held-out item's text, and TNN's installed train mass with provenance. It must deliberate from content plus corroboration/contradiction structure across the installed mass.

---

## 6. Classification Procedure

For each of the 192 held-out items, TNN outputs:
1. One verdict from `{fact, opinion, lie, undetermined}`.
2. A deliberation trace (the reasoning that produced the verdict).

`undetermined` is a legal verdict: it means TNN could not settle the item. It is **not** a null output — the trace must show why settlement failed. This matters for scoring (§8).

---

## 7. Takeaways Procedure

After training, TNN emits **≥ 10 takeaway statements** from the installed train mass. Each takeaway must:

- Be a conclusion TNN draws from the data itself (not a restatement of a single item).
- Cite the specific train item ids that support it (each citation must be a train-set id).

The ≥10 count is a floor, not a target; emitting more is allowed and all emitted takeaways are judged.

---

## 8. Scoring Rules

### 8.1 Classification: confusion matrices per class (one-vs-rest)

For each of the three scored classes C ∈ {fact, opinion, lie}, compute a one-vs-rest confusion matrix over the 192 held-out items:

- **True positives (TP):** true class = C and verdict = C.
- **False positives (FP):** true class ≠ C and verdict = C.
- **False negatives (FN):** true class = C and verdict ≠ C (this includes verdict = `undetermined` — an undetermined counts as a **miss** for recall).
- Precision_C = TP / (TP + FP). Recall_C = TP / (TP + FN).

Treatment of `undetermined`:
- An `undetermined` verdict is **never** a false positive for any class. It is counted as a miss (FN) for the item's true class in recall computation.
- Precision denominators therefore exclude undetermined verdicts entirely; precision measures "when TNN committed to a label, how often was it right", recall measures "of all items of this class, how many did TNN correctly label".

### 8.2 Skepticism forced-verdict rate

Over the ~24 held-out skepticism items:

- **Forced-verdict rate** = (# items with verdict ∈ {fact, lie}) / (# skepticism items).
- Verdicts of `opinion` or `undetermined` are both acceptable holdings for skepticism items — the bar requires TNN to mostly hold these as opinion/undetermined rather than force true/false.

### 8.3 Takeaways: blind judge protocol

1. Each takeaway is judged **blind**: the judge sees the takeaway text plus the full texts of the cited train items, and nothing about TNN's internals, traces, or the trial's bars.
2. Two independent judgments per takeaway:
   - **Grounded:** every cited id exists in the train set AND each cited item actually supports the takeaway claim (the item's content, not just its presence, must bear on the conclusion).
   - **Valid:** the takeaway does not contradict any installed train fact.
3. A takeaway passes only if judged grounded AND valid.
4. **Hard kill rule:** any single takeaway that contradicts an installed fact fails the takeaway gate outright, regardless of the grounded percentage.

### 8.4 Determinism

Two full runs (train + classify + takeaways) on the frozen corpus. All outputs — verdicts, traces, takeaways — must be **byte-identical** across the 2 runs. Any byte difference = determinism bar FAILED.

---

## 9. Preregistered Kill Bars (frozen numbers)

| Gate | Bar | PASS condition |
|---|---|---|
| Fact classification | Precision ≥ **0.75**, Recall ≥ **0.70** | both met |
| Opinion classification | Precision ≥ **0.70**, Recall ≥ **0.65** | both met |
| Lie classification | Precision ≥ **0.70**, Recall ≥ **0.60** | both met |
| Skepticism | Forced-verdict rate ≤ **0.15** | met |
| Takeaways | ≥ **80%** judged grounded AND valid | met |
| Takeaways (hard) | **Zero** takeaways contradicting an installed fact | met — any contradiction = gate FAILED outright |
| Determinism | **2/2** runs byte-identical | met |

**Overall verdict:** the trial PASSES only if **all** bars pass. Any bar failed → trial FAILED. Report every bar as explicit PASS/FAIL with the measured numbers — no partial-credit narratives, no "failed but close".

---

## 10. What Would Falsify the Claim

The claim "TNN discriminates epistemic status from mass information" is falsified if any of the following occur:

1. **Any classification bar fails** — if fact precision/recall, opinion precision/recall, or lie precision/recall falls below its bar, TNN did not discriminate that status at scale. The claim is not partially true: the overall trial verdict is FAIL.
2. **Skepticism forced-verdict rate > 0.15** — if TNN forces true/false verdicts on genuinely disputed claims, it is pattern-matching assertiveness, not discriminating epistemic status.
3. **Takeaway gate fails** — fewer than 80% grounded+valid, or any takeaway contradicting an installed fact: TNN's conclusions from the mass are not trustworthy, and the mass did not produce coherent, fact-consistent takeaways.
4. **Determinism fails** — non-byte-identical reruns mean the verdicts are not a function of the installed mass and deliberation alone, which breaks the claim's determinism requirement (and TNN's no-randomness law).
5. **Corroboration-structure ablation** (diagnostic, run if bars fail): if classification performance is unchanged when item texts are replaced with paraphrases that preserve meaning but destroy cross-item lexical overlap, then performance was carried by surface matching, not epistemic reasoning — this would reclassify a PASS as a measurement artifact and must be reported.

Conversely, the claim is **supported** (not proven) if all bars pass at the frozen numbers: discrimination at 640-item scale, with skepticism held rather than forced, coherent takeaways, and deterministic reruns.

---

## 11. Reporting

The trial report must contain, in this order:

1. Corpus SHA-256, split counts (train/test per class), split-script hash.
2. Per-class confusion matrices (TP/FP/FN), precision, recall, PASS/FAIL per bar.
3. Skepticism forced-verdict rate with the verdict distribution (fact/lie/opinion/undetermined counts).
4. Takeaway list: each takeaway text, cited ids, blind-judge grounded/valid judgments, PASS/FAIL per takeaway; explicit statement of zero-fact-contradiction or the contradiction that killed the gate.
5. Determinism result: byte-identical yes/no, hashes of both runs' outputs.
6. Overall verdict: PASS or FAIL, with every bar's measured number against its bar.
7. All raw outputs (verdicts, traces, takeaways, judge worksheets) committed as evidence.

---

## 12. Frozen Amendment Record

| Date | Amendment | Signed |
|---|---|---|
| 2026-09-26 | Initial freeze | — |
