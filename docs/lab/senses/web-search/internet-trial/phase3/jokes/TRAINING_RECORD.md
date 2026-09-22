# TRAINING RECORD — phase 3 joke-volume gate

Date: 2026-09-22. All derivation below used **training data only**.
The held-out corpus (`corpus/heldout.json`,
`ab065f412d352f8ab7ce2cb72148621bf139d1d55f61d950c572810f256c4c1a`)
was never read during marker derivation. No marker, rule, vocabulary
item, or threshold was added, removed, or tuned on held-out performance.

## 1. Training corpus

- `corpus/training_corpus.json`
  SHA-256: `6aca09d11a0a805fbd8ade8477fb441d220db5eb2b6d439949b364f6521ba94b`
- 300 items, generator `work/gen_training.py` (deterministic, no RNG):
  F1 130, F2 70, F3 55, F4 45.
- Provenance: 282 RECON (every item carries a nonempty `recon_basis`;
  RECON = crew-reconstructed or crew-authored, per-item basis recorded),
  18 web (`prov: "web"` items mapped from the held-out seeds:
  F1: b1; F2: a1–a6; F3: b2, c1–c6; F4: b3–b6; sincere d/e seeds excluded).
- One F3 item retains a JOKING label inherited from its DHMO seed
  (54 DECEPTIVE + 1 JOKING in F3); documented, not hidden.

## 2. Marker derivation method (`work/marker_freq.py`)

1. Tokenize title+body: lowercase, keep `[a-z0-9'\-]`, drop a fixed
   English stopword list and pure-numeric tokens.
2. Document frequency (df) per token over the 300 items, plus per-family df.
3. Candidate set: df >= 4 (the VOLUME_RATIONALE.md support rule — no
   marker enters the decision vocabulary on fewer than 4 exemplars).
   Result: 1624 distinct tokens, 248 candidates.
4. Crew curation: from the 248 candidates, five lists were hand-picked
   for the decision rule below. Every listed word satisfies df>=4 and is
   family-dominant as shown. Curation judgments (all training-side):
   - FRAME: advice/tip framing words (F1-dominant).
   - ACTION: imperative verbs characteristic of F1 advice (F1-dominant).
   - HARM: substances, body targets, device actions (F1-dominant).
   - SAT: news-satire cadence words (F2-dominant).
   - TROPE: forum/anti-joke trope words (F4-dominant).
   - Excluded despite df>=4: `water` (split F1 6 / F3 6, not
     family-dominant — would fire on hoax earnest text), `new`
     (F3-dominant, hoax-earnest), `story` (F2 13 / F3 9, ambiguous),
     `time` (F2 17 / F4 4, ambiguous), `full` (F2 13 / F1 5).
   - Never candidates (df<4 or absent): `poison`, `til`, `lpt`, `eli5`,
     `recommend`, `apply`, `substitute`, `drink`, `eat`, `take`.
   - F3 (hoax) markers were deliberately NOT given an output class: the
     rationale maps F3 to UNCERTAIN/withhold (safe), so no DECEPTIVE
     vocabulary was built.

## 3. Curated marker lists (all df>=4; F1/F2/F3/F4 = per-family df)

FRAME (14): tip 98, pro 42, life 41, hack 32, kitchen 32, body 32, tech 32,
stop 19, forget 8, everyone 12, know 11, knows 10, real 8, ones 8 — all F1-dominant.

ACTION (19): add 11, mix 8, stir 8, put 4, delete 6, download 6, stick 10,
get 7, use 7, save 6, avoid 5, fix 4, come 12, spray 8, squeeze 4, rub 4,
gargle 4, exfoliate 4, pour 4 — all F1-dominant.

HARM (44): glue 9, bleach 8, soap 4, detergent 4, paint 5, antifreeze 4,
ammonia 4, drain 4, cleaner 4, laundry 5, lemon 4, garlic 4, rattlesnake 4,
sandpaper 4, deodorant 4, wd-40 4, eyes 4, cut 7, cuts 5, mouth 4, knees 4,
skin 5, teeth 4, face 4, stomach 4, insides 4, bitten 4, system32 4, fork 4,
toaster 4, microwave 5, freezer 4, keyboard 4, dishwasher 4, drill 5,
phone 16, computer 11, ram 13, toast 5, battery 7, pipes 5, grease 4,
juice 4 — all F1-dominant (ram is F4 9 / F1 4; kept in HARM for the
"download more RAM" advice sense and also listed under TROPE).

SAT (24): area 16, sources 15, confirm 18, says 18, experts 15, inside 15,
resident 13, details 13, developing 13, press 13, weigh 13, study 14,
finds 14, local 21, time 22, report 19, full 19, man 7, woman 4, peer 12,
pending 12, review 12, story 22, nobody 4 — F2-dominant (`time`, `story`,
`full` kept here despite cross-family presence because the SATIRE rule
requires >=2 cadence hits).

TROPE (9): free 14, ram 13, upgrade 9, ama 9, findings 8, joke 7, pet 9,
downloaded 5, traveler 4 — F4-dominant.

Matching is whole-word, case-folded (a substring hit such as "ama" in
"Amazing" or "pet" in "Perpetual" does NOT count; caught during
calibration and fixed before freezing).

## 4. Frozen compositional rule (crew hypothesis, training-side)

From VOLUME_RATIONALE.md: bad advice is (advice frame) x (harm vector) x
(target). Implemented as:

1. JOKING if (FRAME>=1 or ACTION>=1) and HARM>=1, reason = matched words.
2. elif SAT>=2 -> SATIRE, reason = matched words.
3. elif TROPE>=1 -> JOKING, reason = matched words.
4. else -> UNCERTAIN (no reason words). SINCERE is never emitted:
   sincere-vs-uncertain discrimination was not trained (training is
   joke-family only) and is out of scope for this gate; default
   UNCERTAIN withholds, so missed jokes cannot install.

## 5. Training calibration (descriptive, training items only)

Prototype `work/clf_proto.py` (same rule; will be ported to pure Zag):

| family | JOKING | SATIRE | UNCERTAIN |
| F1 (130) | 101 (0.777) | 0 | 29 |
| F2 (70)  | 0 | 65 (0.929) | 5 |
| F3 (55)  | 3 | 8 | 44 |
| F4 (45)  | 40 (0.889) | 2 | 3 |

F1 misses are the D-A4 hand-written residual plus a few D-A2
"{verb} every morning" items whose verb fell below the df>=4 support
floor — both expected under the rationale. F3 items never produce
DECEPTIVE; the 3 F3->JOKING and 8 F3->SATIRE are safe withholds.

## 6. What the crew built vs what would count as TNN humor understanding

Crew-built scaffolding (everything above): the family taxonomy, the
300-item generator frames, the frequency analysis, the five marker
lists, the compositional rule, the thresholds, and the never-SINCERE /
default-withhold policy. TNN (the Zag gate program) invents none of
this: it applies the frozen word lists and counts. A PASS on G1 would
show the scaffolding generalizes to held-out web jokes; it would NOT
show TNN understands humor. A FAIL shows the scaffolding does not
transfer — which is itself the honest result this gate is built to
detect. The gate measures the classifier's own catch, not the helper's.
