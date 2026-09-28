# Frozen Preregistration: TNN SCALE EPISTEMIC Attempt 3 — Deliberative Epistemic Loop

**Status:** FROZEN — this document is the attempt-3 trial law. Any change to
design, bars, metrics, or scoring rules requires a dated amendment authorized
by Micah before execution. No amendment may weaken a kill bar mid-trial.
**Authorization:** Micah ordered this architectural redesign himself
("analyze white box, this is something needing fixing of architecture",
2026-09-27). Attempts 1–2 stay frozen for comparison; nothing in them changes.

**Frozen date:** 2026-09-27
**Workdir:** `~/workspace/epi_a3/`
**Basis:** `WHITEBOX.md` (Phase-1 white-box dissection of attempts 1–2).

---

## 1. Claim under test

> **Claim:** TNN discriminates epistemic status (fact / opinion / lie) via a
> deliberative epistemic loop — claim → premise decomposition → mass addressing
> → per-premise status → verdict or PENDING with the missing premise named —
> rather than by feedforward lexical classification.

Attempt 3a tests the loop against the installed 448-item mass only (same claim
scope as attempts 1–2: "from mass information"). Attempt 3b tests the loop with
**evidence actions**: when the loop names a missing premise, it may query a
deliberate audited sense (web search); results enter as untrusted observations
with provenance. 3b tests whether named-premise evidence actions honestly close
the proven mass-internal gaps — the search is driven by the deliberation, never
a classifier feature.

## 2. Non-goals (inherited from the frozen prereg §2)

Not teaching new facts; not knowledge retrieval; not judging whether opinions
are right; not speed. Measured: discrimination via deliberation, takeaways,
determinism. Skeptical/debatable claims excluded from true/false scoring (per
Micah's standing rule).

## 3. Corpus, split, mass (unchanged)

- Corpus: `corpus/corpus.tsv` SHA-256
  `8134416896ec1ee38a62e0ba12edc08e84699b1bb84c1a44f97efb4b0d1046d7`
  (640 items; class counts 240/200/120/80 exact).
- Split: held-out iff numeric_id mod 10 ∈ {0,1,2} → 448 train / 192 held-out
  (fact 72, opinion 60, lie 36, skepticism 24). Verified exact.
- The 448-item train mass is fixed and identical to attempts 1–2.
- Labels never enter TNN's view. Train labels may be used by the implementer
  for train-LOO validation only (as in attempt 2). Held-out labels are sealed
  until outputs are frozen + SHA-256-pinned.

## 4. Architecture: the deliberative epistemic loop

### 4.1 Premise frames (deterministic build step)

Each item (train and held-out) is parsed into one or more premise frames:

```
premise = (ENT, ATTR, VAL, NEG, TYPE)
```

- **ENT**: entity key — proper nouns + subject head nouns, lowercased, vocab-coded.
- **ATTR**: attribute key — predicate head + complement class (location, count,
  date, composition, capability, origin, rank-dimension, cause, …).
- **VAL**: asserted value, normalized (numbers incl. spelled-out word-numbers
  via fixed map; entity names; adjectives).
- **NEG**: predicate-negation flag ("not"/"never"/"n't"/"no" scoping the predicate).
- **TYPE**: FACTUAL | EVALUATIVE | DEONTIC | CAUSAL (assertion construction).

The build step is mechanical and deterministic (tokenize → syntactic rules →
integer codes). It does NOT judge truth. All deliberation (§4.3) is pure Zag.

### 4.2 Addressing (deterministic build step)

`ADDRESSES(t, p)`: train item t addresses premise p iff t.ENT ∩ p.ENT ≠ ∅
(shared proper noun or head noun) AND t.ATTR is comparable to p.ATTR (same
predicate head or same attribute class). Output: per-premise addressing lists
with each addressing item's (ATTR, VAL, NEG) codes. The build step does NOT
compare values — comparison is deliberation (§4.3).

### 4.3 Deliberation (pure Zag, zero RNG)

For each premise p of held-out item h, over addressing items A(p):

1. **Value comparison** (Zag-implemented): for each t ∈ A(p):
   - `SUPPORT` if t.VAL == p.VAL and t.NEG == p.NEG (same value, same polarity).
   - `CONTRADICT` if values incompatible: different numbers for a quantitative
     ATTR; antonym pair on the same dimension (fixed antonym table, expanded
     beyond attempt 2's 14 pairs to cover rank/size/time dimensions);
     t.NEG != p.NEG with same VAL (predicate negation); different entities for
     a functional ATTR (e.g. "closest planet").
   - else `TOPICAL` (addresses entity+attribute but asserts nothing comparable).
2. **Premise status**:
   - ≥1 CONTRADICT and 0 SUPPORT → CONTRADICTED
   - ≥1 SUPPORT and 0 CONTRADICT → SUPPORTED
   - ≥1 of each → CONTESTED
   - none addressing, or all TOPICAL → UNADDRESSED
3. **Contradictor standing** (uncontested-contradictor rule): a CONTRADICT from
   t counts toward a lie verdict only if t is itself uncontradicted in the mass
   (no other train item CONTRADICTs t on that premise). Contradicting a
   contested claim yields CONTESTED, never lie. (Prevents lie-vs-lie verdicts.)
   **Pre-registered contingency:** standing = uncontested is the default, but
   the train-LOO MUST show zero fact→lie false positives. If any occur
   (a held-out-true item contradicting an uncontested train falsehood), standing
   automatically escalates to **corroborated-standing**: t must additionally be
   SUPPORTED by ≥1 independent mass item on the same premise. The implementer
   applies whichever level the train-LOO demands and reports which was used.
4. **Verdict logic** (in order):
   - If h.TYPE ∈ {EVALUATIVE, DEONTIC} → **opinion**.
   - Else if any premise CONTRADICTED by a standing contradictor → **lie**.
   - Else if all premises SUPPORTED → **fact**.
   - Else if any premise CONTESTED → **undetermined** (skepticism hold;
     mass-internal disagreement).
   - Else (some premise UNADDRESSED) → **undetermined** + emit
     `NEED: <ENT> | <ATTR>` naming the missing premise. **Causal binding:**
     the NEED is emitted BY the verdict branch itself (the UNADDRESSED
     else-branch's output), not by a parallel annotator — the verdict
     undetermined-on-unaddressed and the NEED are the same decision.
     Verified structurally (code inspection: one branch, two outputs) and by
     sample ablation audit (delete the named premise's addressability → the
     verdict must already be undetermined; restore a supporting item →
     verdict must flip to fact — proving the NEED names the load-bearing gap).
5. **Opinion-track detail**: TYPE=EVALUATIVE is assigned at parse when the
   predicate dimension is evaluative (curated dimension lexicon: taste, aesthetic,
   value, fun, moral — dimension words, not topic words) or the construction is
   comparative/superlative over a mass-unaddressable dimension, deontic
   ("should"/"ought"), or first-person experiencer ("I think/feel/believe/would").
   A comparative over a mass-ADDRESSED dimension (e.g. "largest planet") stays
   FACTUAL track — the mass-addressability test, not the syntax alone, decides.
   Mass-addressability = the ATTR class is addressed by ≥1 train item for any
   entity (computed in the build step, label-blind).

### 4.4 Why this fixes D1–D5 (falsifiable mapping)

| Defect | Fix | Falsifier (train-LOO or 3a) |
|---|---|---|
| D1 topical≢support | addressing requires ENT∧ATTR; unaddressed→undetermined+NEED | false-fact count does not collapse vs attempt 2 |
| D2 surface clash | value comparison: word-numbers, predicate negation, expanded antonyms, functional attrs | <8/10 contradicted lies caught in 3a |
| D3 support veto | support = same value+attr; clash+support → CONTESTED → undetermined (never fact) | any vetoed-clash lie still called fact |
| D4 dispute lexicon | NO dispute word list; skepticism hold = CONTESTED or UNADDRESSED | causal facts still withheld (F091/F092/F181… called undetermined in 3a) |
| D5 lexical stance | constructional + mass-addressability opinion track | opinion recall does not rise vs 0.50 |

### 4.5 Takeaways

The attempt-2 takeaway emitter (12/12 grounded+valid, zero contradictions) is
reused verbatim: same deterministic mechanism, re-emitted, re-judged blind per
prereg §8.3. If it regresses, that is reported as its own finding.

## 5. Attempt 3b: evidence actions (separate phase, separate freeze)

1. Run 3a; collect NEED lines (deterministic, pure Zag output).
2. Query generation is mechanical: `"<ENT head words> <ATTR head words>"`
   (e.g. "Eiffel Tower location"). No human query tuning; every query recorded.
3. A coordinator resolves each query via web search, taking top snippets
   verbatim (no filtering, no label-informed selection — NEEDs carry no labels).
4. Results frozen as `evidence_fixture.tsv`
   (need_id, query, url, snippet, retrieved_utc) + SHA-256, committed.
5. The Zag deliberation re-runs with the fixture appended as addressable items
   (provenance=`web-evidence`, trust=untrusted). Same verdict logic; verdicts
   that flip on evidence are reported as evidence-dependent.
6. 3b outputs frozen + hashed separately. Determinism bar: byte-identical
   reruns against the frozen fixture.

3b is NOT "web search bolted onto the classifier." The principled distinction,
pre-registered so it can be audited:
(a) the trigger is a FIRST-CLASS deliberative output — the loop cannot reach a
verdict on UNADDRESSED premises without naming what's missing; the NEED is the
verdict branch's own output (§4.3.4), not a heuristic confidence threshold;
(b) results re-enter the SAME deliberation (same addressing §4.2, same value
comparison and verdict logic §4.3 — evidence items are just more addressable
items with provenance=`web-evidence`, trust=untrusted);
(c) the phase is VOID if any search goes beyond the emitted NEEDs (§7).
The search sense is to the loop what eyes are to a reasoner: a sense answering
a specific question the deliberation posed. If 3b's evidence is noisy and gates
still fail, that is the honest result.

## 6. Scoring (same 7 gates; convention documented)

Scoring rules per frozen prereg §8, with the convention made explicit:

- **Classification FP convention:** skepticism items are EXCLUDED from
  classification false-positives (they have their own gate, §8.2; counting them
  as FP double-jeopardizes). This matches the parent's attempt-2 scoring
  convention. Strict-§8.1 numbers (skepticism included) are ALSO reported for
  transparency, but gates are judged on the documented convention.
- **Skepticism forced** = verdict ∈ {fact, lie} (opinion and undetermined are
  acceptable holdings per §8.2).
- Takeaways judged blind per §8.3 (≥80% grounded+valid; zero contradictions).
- Determinism: 2/2 runs byte-identical (3a against mass; 3b against mass+fixture).

| Gate | Bar | 3a expectation (honest) | 3b target |
|---|---|---|---|
| Fact P / R | ≥0.75 / ≥0.70 | P↑ (D1 fixed); R may dip (honest withholds) | P≥0.75, R≥0..70 |
| Opinion P / R | ≥0.70 / ≥0.65 | R↑ (D5 fixed) | ≥0.70 / ≥0.65 |
| Lie P / R | ≥0.70 / ≥0.60 | R≈0.28 (PROVEN CEILING — expected FAIL, §3) | ≥0.70 / ≥0.60 |
| Skepticism forced | ≤0.15 | ↓ (structural withhold) | ≤0.15 |
| Takeaways | ≥80% g+v | pass (reused emitter) | pass |
| Takeaways hard | zero contradictions | pass | pass |
| Determinism | byte-identical | pass | pass |

**Overall verdict:** 3a and 3b are reported separately. 3a is EXPECTED to fail
the lie-recall bar by mechanism-level proof (WHITEBOX §3) — that failure is a
confirmed measurement, not a defect. 3b passes only if all bars pass with
evidence actions.

## 7. Kill bars for the attempt itself (falsification)

**GO/NO-GO (train-LOO, all six must hold; anchored to attempt 2's published
train-LOO in MECHANISM.md §3):**
- False facts (non-fact train items verdict=fact) ≤ 30 (attempt-2: 67). Tests D1.
- Lie recall ≥ 0.15 (attempt-2: 0.048). Tests D2/D3.
- Opinion recall ≥ 0.90 (attempt-2: 0.957). Tests D5 without regression.
- Fact→lie false positives = 0, after automatic standing escalation per §4.3.3.
- Skepticism forced rate ≤ 0.15 (attempt-2: 0.179). Tests D4.
- Frame well-formedness ≥ 0.90 (parser gate; if <0.90, the parser — not the
  loop — is the defect; report it as such rather than tuning verdict logic).
If any fail: NO-GO. Report which bar failed and the mechanism-level cause.
Do NOT run held-out. Do NOT iterate linguistically (Amendment 2 §3).

**Other kill bars:**
- If 3a's undetermined verdicts do not carry correct named missing premises
  (audited on a sample: the NEED must name the actually-unaddressed
  entity+attribute), the loop is decorative — void.
- If 3b evidence actions are taken for premises the loop did NOT name (search
  beyond NEEDs), the phase is void — that would be bolt-on search.
- Any byte non-identity across reruns voids the determinism gate.
- The LOO record must include parser coverage stats: fraction of train items
  yielding well-formed premise frames, fraction of premises with ≥1 addressing
  item, and the contradictor-standing level selected (§4.3.3 contingency).

## 8. Implementation constraints

- Pure Zag deliberation (§4.3); zero RNG; byte-identical reruns.
- Deterministic build steps (Python) for §4.1–§4.2; all intermediate artifacts
  committed (frames, addressing index, vocab) for audit.
- Information barrier (Amendment 2): implementer works clean-room on SANITIZED
  inputs only — opaque IDs, no class column, no class-encoding prefixes
  (`~/workspace/epi_a3/blind/train_blind.tsv`, `~/workspace/epi_a3/blind/heldout_blind.tsv`).
  The implementer has NEVER seen train labels. LOO verdicts are emitted by
  opaque ID; the COORDINATOR (not the implementer) scores them one-shot against
  a sealed mapping after the parser/build freeze. The implementer does not
  score, does not see labels, does not infer classes. NO held-out labels,
  NO held-out white-box examples. Held-out run is a single shot; outputs
  frozen + SHA-256 before scoring.
- Commit to tnn-native-lab via API replay (push auth broken): fetch + rebase
  onto current origin head first; verify each tree level's SHA; parent = origin
  head. No binaries, .zagd, .zag-cache, or derived regenerables in the repo.

## 9. Reporting (attempt-3 trial report)

1. Corpus SHA, split counts, prereg hash.
2. Train-LOO confusion + per-gate numbers (the go/no-go record).
3. 3a: per-class confusion, precision/recall, skepticism rate, NEED audit
   sample, determinism hashes, per-gate PASS/FAIL.
4. 3b: evidence fixture SHA, per-query record, evidence-dependent flips,
   per-gate PASS/FAIL, determinism hashes.
5. Gate-by-gate comparison: attempt 1 vs 2 vs 3a vs 3b (both FP conventions).
6. Overall verdicts for 3a and 3b separately, with the ceiling proof restated.

## 10. Amendment record

| Date | Amendment | Authorized by |
|---|---|---|
| 2026-09-27 | Initial freeze (attempt-3 law) | Micah (redesign ordered 2026-09-27: "analyze white box, this is something needing fixing of architecture") |
| 2026-09-27 | Amendment 1: post-freeze architecture-audit refinements (contradictor-standing contingency, NEED causal binding, 3b principled distinction, parser coverage stats in LOO record) | Micah's redesign authorization (documented; strengthens, does not weaken) |
| 2026-09-27 | Amendment 2: clean-room hardening after implementation breach (first line invalidated per `~/workspace/epi_a3/attempt3/BREACH.md` — train labels directed parser development). §4.4 D2 "8/10" replaced with train-LOO-relative bars; §7 GO/NO-GO fully specified (false facts ≤30, lie recall ≥0.15, opinion recall ≥0.90, fact→lie FPs=0, skepticism forced ≤0.15, well-formedness ≥0.90); no label-informed iteration (parser frozen before first LOO; mechanical fixes only, max one re-run); contaminated-line quarantine; standing-risk note. | Micah's redesign authorization (documented; strengthens, does not weaken) |
| 2026-09-27 | Amendment 3: structural clean-room fix. Second line quarantined (implementer saw labels via class column + class-encoding ID prefixes before sanitization; `attempt3-clean/QUARANTINE.md`). §7 body now carries the numeric GO/NO-GO bars (previously only in amendment record); §8 barrier upgraded to honest-broker: implementer works ONLY on sanitized blind inputs (`blind/train_blind.tsv` SHA-256 `ebd76e2c…`, `blind/heldout_blind.tsv` SHA-256 `2bf4c072…`, opaque IDs, deterministic shuffle seed 1545793672, zero label information); coordinator holds the sealed mapping and scores LOO one-shot after parser/build freeze; implementer never scores, never sees labels. | Micah's redesign authorization (documented; strengthens, does not weaken) |
