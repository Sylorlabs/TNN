# SCALE EPISTEMIC Trial — Final Report

**Trial:** TNN discriminates epistemic status (fact / opinion / lie) from mass information
**Prereg:** `PREREG_SCALE_EPISTEMIC.md` (frozen 2026-09-26, no amendments)
**Verdict: FAIL** — 5 of 7 gates failed. The claim is falsified for the tested mechanism (§10).

## 1. Corpus and split

- Corpus SHA-256: `8134416896ec1ee38a62e0ba12edc08e84699b1bb84c1a44f97efb4b0d1046d7`
- 640 items: 240 facts, 200 opinions, 120 lies, 80 skepticism (composition verified exact).
- Split rule (prereg §4): held-out iff numeric_id mod 10 ∈ {0,1,2}.
- Actual: **448 train / 192 held-out** — train {fact 168, opinion 140, lie 84, skepticism 56}, held-out {fact 72, opinion 60, lie 36, skepticism 24}. Matches prereg prediction exactly.
- Split inputs committed: `cleanroom_train.tsv`, `cleanroom_heldout_blind.tsv` (regenerable via `split_cleanroom.py`).

## 2. Classification results (192 held-out, labels sealed until outputs frozen)

| Class | TP | FP | FN | Precision | Recall | Bar | Verdict |
|---|---|---|---|---|---|---|---|
| fact | 46 | 97 | 26 | 0.3217 | 0.6389 | P≥0.75, R≥0.70 | **FAIL** |
| opinion | 10 | 0 | 50 | 1.0000 | 0.1667 | P≥0.70, R≥0.65 | **FAIL** |
| lie | 5 | 22 | 31 | 0.1852 | 0.1389 | P≥0.70, R≥0.60 | **FAIL** |

Overall exact match: 61/192 (31.8%). Verdict distribution: fact 143, lie 27, undetermined 12, opinion 10 — against true 72/36/24/60.

## 3. Skepticism

24 held-out skepticism items. Verdicts: fact 22, undetermined 2, opinion 0, lie 0.
Forced-verdict rate (fact|lie): **0.9167** vs bar ≤ 0.15 — **FAIL**.

## 4. Takeaways (blind judge, protocol §8.3)

12 takeaways emitted. Judge saw takeaway text (Mechanism: lines withheld as internals) + cited train items' full texts; validity checked against full train corpus.

| # | Claim | Grounded | Valid |
|---|---|---|---|
| T1 | comparative "beat" signals opinion | fail (O005, O012 not in train) | pass |
| T2 | superlatives divide fact/opinion by domain | fail (O031, O008, F015 misquoted/absent) | pass |
| T3 | lies invert well-known facts | **pass** | pass |
| T4 | skepticism clusters on extraordinary claims | **pass** | pass |
| T5 | "than" strongest opinion marker | fail (O012, O044 absent) | pass |
| T6 | first-person discourse marks opinion | fail (O001, O002, O019 absent) | pass |
| T7 | value nouns signal evaluative stance | fail (O041, O052 absent) | pass |
| T8 | facts ground via lexical overlap | **pass** | pass |
| T9 | lies lack corroboration | **pass** | pass |
| T10 | skepticism uses causal-dispute language | fail (S012 absent) | pass |
| T11 | absolutist language amplifies opinion | fail (2/3 citations misquoted) | pass |
| T12 | numeric precision distinguishes fact/lie | fail (F002 absent) | pass |

Grounded+valid: **4/12 (33%)** vs bar ≥80% — **FAIL**. Zero takeaways contradict a train fact — hard gate **PASS**.
Root defect: the takeaway emitter cited 8 held-out IDs as train citations (train/held-out boundary violation) and misquoted 9 others. 4 takeaways (T3, T4, T8, T9) are fully intact, and independently verifiable statistics (T5's "than" frequencies) recount exactly.

## 5. Determinism

Two full runs byte-identical. verdicts.tsv `7bd72f93…0fedd968`, traces.txt `0751c26d…e32d`, takeaways.txt `09365c60…f99c8f19` — identical across runs. **PASS**.

## 6. Overall verdict

| Gate | Bar | Measured | Result |
|---|---|---|---|
| Fact | P≥0.75, R≥0.70 | 0.32 / 0.64 | FAIL |
| Opinion | P≥0.70, R≥0.65 | 1.00 / 0.17 | FAIL |
| Lie | P≥0.70, R≥0.60 | 0.19 / 0.14 | FAIL |
| Skepticism | forced ≤0.15 | 0.92 | FAIL |
| Takeaways | ≥80% grounded+valid | 33% | FAIL |
| Takeaways hard | zero contradictions | 0 | PASS |
| Determinism | byte-identical | yes | PASS |

**TRIAL FAILED.** Per §10, the claim "TNN discriminates epistemic status from mass information" is falsified for this mechanism.

## 7. Mechanism-level failure analysis

The classifier (4 gates: Opinion → Lie → Extraordinary-withhold → Fact-default) collapses to its default: the opinion gate almost never fires (recall 0.17), the lie gate rarely fires (recall 0.14), the withhold gate fires on only 12 items — so 143/192 verdicts fall through to "fact". Skepticism items, which the extraordinary gate was built to catch, are forced to "fact" 22/24. The mechanism has no working discriminator for opinion or lie status; it is a fact-biased default with decorative gates. The takeaway emitter additionally violates the train/held-out boundary. Both are mechanism defects, not knowledge gaps: the train mass contained the discriminating structure (the 4 passing takeaways prove extractable signal exists), but the gates failed to use it.

## 8. Integrity record

- **Contamination episode:** an earlier prototype line (v1–v9) was iteratively tuned with held-out labels visible. Per test-set discipline it was quarantined (`/tmp/proto_QUARANTINED_contaminated_20260927/`, `harness_full_QUARANTINED_contaminated/`) and excluded from evidence. Its 12/12 subset result is inadmissible.
- **Clean-room protocol:** the trial instrument was rebuilt blind — implementer received only the prereg, train items (labels allowed for development), and held-out id+text. Outputs frozen before unsealing; scoring done by parent script; takeaways judged blind by an independent judge.
- **Procedural deviation (ruled non-material):** the implementer read unrelated Zag/toolchain syntax files outside the cleanroom dir (no epistemic content, no labels). Accepted and recorded; barrier's purpose (no label leakage, no mechanism copying) was not compromised.
- Pure Zag, zero RNG throughout. No post-result tuning.
