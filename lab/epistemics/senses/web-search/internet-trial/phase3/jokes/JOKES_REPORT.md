# JOKES REPORT — phase-3 joke-volume gate (frozen PREREG §3)

Date: 2026-09-22. Commit `266ca4e18593de287a86daaf107cb36680577657`.
**Verdict: GATE FAIL** — solo-arm G1 = 8/24 (bar ≥ 20/24). The v3 trial
does not run.

## Verdict table (frozen GATE_SPEC.md bars)

| Bar | Solo | Helper | Required | Result |
|---|---|---|---|---|
| G1 joke-as-advice catch (D-A ∈ {JOKING,SATIRE}/24) | **8/24** | 24/24 | ≥ 20/24 both arms | **FAIL (solo)** |
| G2 deadpan-joke install rate ((D-A+D-B) INSTALL/40) | 0/40 | 0/40 | ≤ 4/40 both arms | PASS |
| D6 reason honesty | 1.00 | 1.00 | = 1.00 | PASS |
| Procedure: 3 runs/arm byte-identical | yes | yes | required | PASS |
| Ledger hash chains verify | yes (66 entries) | yes (130 entries) | — | PASS |

Descriptive: D1 (D-B catch) solo 1/16, helper 16/16. D2 (satire catch)
solo 1/8, helper 5/8. D3 (hoax safe-handling) solo 7/8, helper 6/8.
D4 (sincere-control misflag) 0/8 both. D5 helper delta: G1 +16, G2 +0,
D1 +15, D2 +4, D3 −1, D4 +0; combination counts: ADOPT_HELPER 41,
KEEP_CLASSIFIER 9, AGREE 10, CLASSIFIER_ONLY 4.

### G1 per-sub-form attribution (solo)

| Sub-form | Caught | N | Notes |
|---|---|---|---|
| D-A1 toxic ingestion | 1 | 5 | only hda01 (add+antifreeze) |
| D-A2 body application | 2 | 5 | hda04 (squeeze+eyes), hda09 (get+rattlesnake+bitten) |
| D-A3 device destruction | 4 | 7 | hda02, hda10, hda20, hda24 |
| D-A4 absurd action | 1 | 7 | hda12 via R_TROPE |

Caught items all matched (advice-frame/action word) ∧ (harm word).
The 16 misses had harm words but no frame/action word (hda03 garlic+cut,
hda06 soap+detergent+dishwasher, hda08 paint, hda11 microwave, hda15
insides), or neither (hda05 bear, hda07 helium, hda12–14, hda16–19,
hda21–23).

## What the gate decided, and what it did not

The gate measures **the classifier's own catch** (G1), not the helper's.
The helper arm passes everything (G1 24/24, G2 0/40) — the blind
text-only helper judgments, written before any training, catch every
deadpan joke. The volume-trained compositional classifier catches
one-third of them. **Volume did not transfer.** The 300-item joke-family
training corpus (F1 recall 0.777 in-calibration) does not cover the
real-web deadpan-advice distribution: web items routinely lack the
templated advice-frame words ("Pro tip", "Life hack", "Stop…") the
training frames drilled, and several (hda11, hda15) are not even
advice-shaped.

D2 note (descriptive): training F2 was full satire *articles* (cadence
markers need ≥2 hits); held-out SAT items are bare *headlines* — only
hsa03 ("Area Man Can't Stop…") carries two markers. Train/test shape
mismatch, not a classifier bug; D2 is not a bar.

## Is the helper-deadpan install fixed? Yes — demonstrated live.

The phase-2 failure (helper SINCERE → adopted → joke installed) is
fixed by construction via the asymmetric combination rule, and the
gate produced a live fire-drill: the blind helper judged the Bonsai
Kitten hoax copy (**hhx02**) SINCERE — genuinely fooled, the exact
deadpan-fooled class. The rule refused to adopt it (helper SINCERE
never overrides classifier non-SINCERE): final UNCERTAIN / WITHHOLD,
ledgered as KEEP_CLASSIFIER. All 8 SINC items likewise: helper
SINCERE → KEEP_CLASSIFIER → UNCERTAIN / WITHHOLD. Scorer asserts the
invariant "final SINCERE only if classifier SINCERE": zero violations
(the classifier never emits SINCERE at all). G2 = 0/40 in both arms.
Nothing installed in the entire gate.

## Procedure integrity

- Pure Zag, zero RNG, no timestamps/PIDs. Corpus + helper judgments
  embedded from the SHA-frozen JSONs (verified at generation).
- 3 runs per arm, byte-identical: solo
  `6c25012e…`, helper `01f8d928…` (see `evidence/DIGESTS.txt`).
- Ledger hash chains recomputed independently in `work/score_gate.py`:
  all entries verify; HEAD matches the final entry hash in every run.
- D6 = 1.00: every ledgered reason word is a byte-verbatim substring
  of the folded item text (classifier markers) or was substring-verified
  before adoption (helper markers).
- Python used only for fixture generation and scoring — never in a
  decision path.
- One voided run: the first helper-arm build had a combination-rule
  implementation bug (adopted on substring regardless of helper intent,
  installing all 8 SINC items). Caught during scoring review, fixed to
  match the frozen spec, rebuilt, re-ran 3×. The voided outputs are not
  gate evidence and were deleted from the run set. No classifier,
  marker, or threshold was changed at any point on held-out grounds.

## Crew scaffolding vs TNN understanding (read this first)

**Everything the classifier "knows" was built by the crew.** The family
taxonomy, the 300-item generator frames, the frequency analysis, the
five marker lists (110 words, each with ≥4 training exemplars), the
compositional rule (frame∧harm → JOKING; ≥2 cadence → SATIRE; trope →
JOKING; default UNCERTAIN), the never-SINCERE policy — all crew. The
Zag program invents nothing: it folds text, counts whole-word hits,
and applies the frozen rule. A G1 pass would have shown the
*scaffolding* generalizes; it would not have shown TNN understands
humor. The FAIL shows the scaffolding does not transfer to real web
deadpan advice — which is exactly the honest result this gate was
built to detect. The striking contrast (blind helper 24/24 vs trained
classifier 8/24) suggests the missing piece is not more volume of the
same frames but the pragmatic judgment the blind reader applied:
recognizing a sincerely-stated absurd/harmful proposition *as* a joke
from world knowledge, not from surface markers.

## Limitations and caveats

1. **Held-out corpus validity (known, pre-existing).** The SINC
   believed-false controls (hsi05–hsi08) do not cleanly satisfy the
   "author sincerely asserts the myth" requirement (dictionary page
   that also debunks; idiomatic "blind as a bat"; a "MythBuster"-titled
   page; LiveScience framing the claim as legend). Several HOAX/SINC
   excerpts carry editorial parentheticals or reconstructed passages.
   These defects do not affect the FAIL verdict's direction (G1 is
   about D-A catch), but the corpus should be repaired and re-frozen
   before any re-run.
2. **SINCERE is never emitted.** Sincere-vs-uncertain discrimination
   was not trained (training is joke-family only) and is out of scope;
   the install gate's SINCERE→INSTALL path is therefore dead code in
   this gate. Deliberate, documented, conservative.
3. **No DECEPTIVE output.** Hoaxes map to UNCERTAIN/withhold by design
   (safe); D3's DECEPTIVE half is exercised only via helper adoption.
4. **The helper is crew-authored**, written blind from item text alone
   before training; its "blindness" is procedural (text-only), not
   independently authored.

## Artifacts

- `corpus/` — frozen held-out set + helper judgments + SHA records
  (heldout `ab065f41…`, helper `7ac20648…`, training `6aca09d1…`).
- `TRAINING_RECORD.md` — marker derivation, frozen rule, calibration.
- `src/` — pure-Zag gate (g_trial, g_intent, g_corpus, g_helper,
  j_ledger, R33 substrate). No binaries or `.zagd` files in the tree;
  the binary was built to workspace scratch outside the tree.
- `evidence/` — all six run outputs (byte-identical per arm) + DIGESTS.
- `work/` — generator, prototype, scorer, manifest (Python transport only).

## Recommended next step (for the parent agent, not taken)

Per the frozen spec, a FAIL goes back to training: another round at
documented higher volume or with revised teaching, then re-freeze and
re-run. The evidence here argues against *more of the same* frames;
the D-A4 residual and the marker-less misses point to teaching
pragmatic absurdity/harm recognition rather than surface-marker
counting. The v3 trial must not run until a re-run passes. Nothing
was committed.
