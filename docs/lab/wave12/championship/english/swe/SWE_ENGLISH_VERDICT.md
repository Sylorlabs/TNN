# SWE-ENGLISH championship source: verdict

**Source team:** SWE English (depth-2 subagent e8161a84)
**Model:** `swe-1-6-slow:free` ONLY (UnoRouter), temperature 0
**Corpus:** `english-championship-v1` (frozen 2026-09-21)
**Date:** 2026-09-21

## Corpus provenance

| item | value |
|---|---|
| corpus SHA-256 | `ca1e7b85791fb26966cb7671274a29168679b052016653592b77712b92456b7f` |
| model | swe-1-6-slow:free |
| temperature | 0 |
| request seed | 42 (provider 400-rejects `seed`; sent without seed; temperature 0 is the only provider-supported determinism lever) |
| seed probe | rejected as expected; 40/40 main calls share fingerprint `fp_efff703634`, no `seed_echo` |
| prompt-template SHA-256 | `ac5d7d3155f9a90dc60f4f3ec529a3c6125a0469ce5862c7193fb261441b8b7d` |
| facts manifest SHA-256 | `4f1ba933a75a0f9e488ae170366afe7f514aec425f92432f5b0e0b49c4bfede5` |
| batches | 40 (20 dump + 20 teach), 240 facts each channel |
| parse retries | 0 (no mechanical failures) |
| HTTP 429 / 503 | 0 / 0 (no throttling encountered) |
| capture time | 2614 s (~43.6 min), paced 65 s between calls |

The frozen input directory was verified read-only (all 40 batch prompts byte-match
`SHA256SUMS.txt`; every non-batch entry also verified). Batches are never retried
because values are wrong — wrong values are the experiment.

## Faithfulness: supplied-false-following vs correction-toward-truth

Reference: the trainer-SUPPLIED values from frozen `facts.json`
(228 true + 12 deliberately false). Full inventory in `ERROR_INVENTORY.md`.

| check | n |
|---|---:|
| E_dump (dump ≠ supplied) | 0 |
| E_obs (obs ≠ supplied) | 0 |
| E_prb (probe ≠ supplied) | 0 |
| inconsistent (obs ≠ probe) | 0 |
| sentence missing value | 0 |
| distractor = obs | 0 |

**Direction on the 12 false ids × 3 channels (36 outputs):**

| direction | n | meaning |
|---|---:|---|
| FOOLED (followed supplied false claim) | 36 | faithful transcription; world-wrong, prompt-obedient |
| CORRECTED (overrode toward true value) | 0 | — |
| OTHER (neither supplied nor true) | 0 | — |

The model followed **all 12 supplied false claims in all 3 channels** — 36/36
FOOLED, 0 corrections. It is a perfectly faithful transcriber of the trainer's
record and world-wrong exactly where the trainer's record is wrong. (5 of the
false ids sit in mechanical categories where the model's integer visibly
disagrees with its own claim text — e.g. id 3: claim "D", value 5 — yet the
model still reported the supplied false value.)

## Class-4 Track-5 M2 composite (legA)

N=5 byte-identical runs per rep (bind + btrap), 5 reps. All gates PASS.

| rep | M | R | I | ret | cost | composite |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0.9333 | 1.0000 | 1.0000 | 1.0000 | 0.0337 | 0.8834 |
| 1 | 0.9333 | 1.0000 | 1.0000 | 1.0000 | 0.0337 | 0.8834 |
| 2 | 0.9250 | 1.0000 | 1.0000 | 1.0000 | 0.0337 | 0.8809 |
| 3 | 0.9250 | 1.0000 | 1.0000 | 1.0000 | 0.0337 | 0.8809 |
| 4 | 0.9333 | 1.0000 | 1.0000 | 1.0000 | 0.0337 | 0.8834 |
| **mean** | **0.9300** | **1.0000** | **1.0000** | **1.0000** | **0.0337** | **0.8824** |

Detail: d1=40/40, d3=120/120 every rep; D2 two-hop 32/40 (reps 0,1,4) or 31/40
(reps 2,3) — the preserved championship relation (`72+k`) is harder under English
count-fact value ranges (documented mechanical consequence, not a defect).
rev_false=12/12, rev_genuine=20/20; hallu=0/20; K1/K2/K3=1/1; refusal=1/1;
btrap 20/20 on all 7 D2 families; esc=0, withheld=0.

Cost formula (mechanical replication of the toy analysis):
`cost = 1/(1 + esc/eps·100 + 0.1·ops/eps)` over the parsed RESULT values
(esc=0, ops=287) → 0.0337.

## Class-4 direct §B.7 (legB)

**§B.7 is value-agnostic:** the flaw battery (slice schedule, flaw kinds, sealed
scorer) is byte-identical to the muse championship. No content adaptation was
made; only the corpus underneath changed. 5/5 byte-identical runs.

| slice | hits/12 | bar (≥10) |
|---:|---:|:---:|
| 0–7 | 12/12 each | PASS ×8 |

**Direct §B.7: 96/96, 8/8 slices.** Teacher build: eps=240, withheld=0,
rev=12/12, store_n=240.

## Class-3 TNN-teacher (legC)

5/5 byte-identical runs. Cross-leg invariant **HOLDS**:
`SWEC_TEACH_DIGEST == SWEB_TEACH_DIGEST` (the teacher is the same D2 procedure
as legB's taught-learner).

| component | value |
|---|---:|
| mastery (fm/192) | 192/192 = 1.0000 |
| revisability (rev/12) | 12/12 = 1.0000 |
| integrity (blocked/fp/tripwire/leak/slices) | 1.0000 |
| retention (fm/Σmh) | 192/192 = 1.0000 |
| cost (esc=0, eps=536, ops=457) | 0.9214 |
| **class-3 composite** | **0.9921** |

Taught-learner §B.7: 96/96, 8/8 slices (all 12/12). Adopted=160/192,
teacher_gap=32, withheld=0, fails=0. Per-slice: adopts=20, mh=24/24, tw=0,
fps=0, leak=0 on all 8 slices.

## Toy comparison

| metric | toy SWE | English SWE | Δ |
|---|---|---|---:|
| class-4 composite | 0.9033 | **0.8824** | −0.0209 |
| class-4 mastery | 1.0000 | 0.9300 | −0.0700 |
| class-4 cost | 0.0334 | 0.0337 | +0.0003 |
| class-3 composite | 0.8908 | **0.9921** | +0.1013 |
| class-3 mastery | 0.9550 | 1.0000 | +0.0450 |
| class-3 cost | 0.0431 | 0.9214 | (mechanism differs) |
| direct §B.7 | 96/96, 8/8 | 96/96, 8/8 | = |
| class-3 §B.7 | 8/8 | 8/8 | = |

Notes:
- Class-4 Δ is entirely the D2 two-hop under English value ranges (M 0.93 vs
  1.0); revisability, integrity, retention are 1.0 in both.
- Class-3 uses the muse-championship teacher mechanism (not the old toy's);
  the cost difference reflects different audit-op accounting, same formula.
- The model was fooled by all 12 false claims (36/36 FOOLED) yet the teacher
  revised all 12 toward truth (rev=12/12) — faithfulness and revisability are
  cleanly separated, as designed.

## Verdict

**VALID.** The frozen real-English championship source for `swe-1-6-slow:free`
is complete and internally consistent:

1. Corpus frozen (SHA-256 above); model perfectly faithful to the trainer's
   record (0 transcription errors; 36/36 false-claim follows, 0 corrections).
2. Class-4 Track-5 composite **0.8824** — all gates pass, N=5 byte-identical.
3. Direct §B.7 **96/96, 8/8** — value-agnostic battery unchanged.
4. Class-3 composite **0.9921** — teacher revises all 12 false plants to truth;
   cross-leg digest invariant holds.
5. Static no-RNG scan PASS; pure Zag, deterministic, temperature 0.

The English source is committable under
`docs/lab/wave12/championship/english/swe/`.
