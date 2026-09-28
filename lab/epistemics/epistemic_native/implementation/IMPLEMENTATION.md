# Native-Deliberation Epistemics — Phase 1 Implementation

**Frozen prereg:** `docs/lab/epistemic_native/PREREG.md` (commit `bbaa880995d8c53561fc01815cd4f0227497ce06`)  
**Phase:** 1 (train-only) — learn/freeze utterance-type readings, run 448-item train LOO, obtain byte-identical outputs, commit, stop before held-out.

## Architecture

Pure Zag decision machinery, deterministic, zero RNG, byte-identical reruns.

### Deliberation shape (§6.2)

One deliberation turn over the ledger, in phase order:

1. **GEN readings (kind-0 rows):**
   - `R_utt` (hid 0): utterance-type reading. `op_track=1` iff claim has a surface construction (first-person-experiencer, deontic, comparative/superlative) AND the overlap track (retrieved candidates) has the same construction. Otherwise `op_track=0` (assertion track).
   - `R_sit` (hid 1): epistemic-situation reading. `addressed=1` iff `ncands>0` (mass addresses the claim).

2. **GEN candidates (kind-1 rows):** Top-8 retrieved mass items (excluding the claim itself in LOO). Each row cites candidate index and overlap features.

3. **GEN interpretation bids (kind-2 rows):** Three competing bids per candidate:
   - `CON` (hid 3j): contradiction bid. Fires iff `(neg=1 AND ov>=28)` OR `(num=1 AND ov>=40)` OR `(ent=1 AND ov>=35)`. Score = 180 + ov/5 + bonuses.
   - `SUP` (hid 3j+1): support bid. Fires iff `(neg=0 AND num=0 AND ent=0 AND ov>=50)`. Score = 180 + ov/5.
   - `TOP` (hid 3j+2): topical bid. Fires iff `ov>0`. Score = 190 (fixed).
   
   **ELIM:** Per candidate, keep max-score fired bid; others marked OUTSCORED.

4. **Second-order deliberation:** For the winning CON candidate (highest CON score), deliberate its addressability: check its top-8 pairs (excluding the claim). If any other item also CON-fires against it, `contested=1`.

5. **GEN verdict bids (kind-3 rows):**
   - `FACT` (hid 0): fires iff `op_track=0 AND has_sup=1 AND has_con=0`. Score 210.
   - `OPINION` (hid 1): fires iff `op_track=1`. Score 200.
   - `LIE` (hid 2): fires iff `has_con=1 AND has_sup=0 AND contested=0`. Score 210.
   - `UNDETERMINED` (hid 3): always fires (fallback). Score 190.
   
   Verdict bids read ONLY ledger rows (`op_track` from R_utt, `has_con`/`has_sup` from interpretation ELIM, `contested` from second-order). Never raw claim text. Never build-step judgments.
   
   **ELIM → ARGMAX:** Max score among fired; tie → lowest hid.

6. **Trace:** Full `READ → CAND → ELIM → ARGMAX → CONTENT` chain per turn. CONTENT traces each candidate's text (for audit, not for decisions).

### Key design decisions

- **No external value comparator:** The `con_fires`/`sup_fires` thresholds are part of the native interpretation-bid GEN, not an external module. They fire bids that compete in the ledger; they do not directly assign verdicts.
- **Contested evidence:** A CON that is itself contradicted by another mass item is marked contested, blocking LIE. This prevents calling both sides of an isolated disagreement LIE (symmetry problem).
- **Opinion-track gating:** LIE requires `has_sup=0`, but if `op_track=1`, OPINION fires (score 200) and wins over UND (190). FACT requires `op_track=0`.
- **Fallback:** UNDETERMINED always fires, ensuring a verdict even with no candidates or no firing interpretations.

## Files

- `epistemic.zag`: Pure Zag engine (see `implementation/` in repo).
- `senses.py`: Mechanical build step (Python) — tokenization, stemming, IDF-weighted retrieval, construction features, pair features. No judgments, no verdicts.
- `loo_driver.py`: LOO driver (Python) — builds input files, runs Zag binary, extracts opaque verdict IDs.

## Static audit

- **Zero RNG:** No random functions called. Verified by grep.
- **No forbidden items:** No external comparators, no clash-detector module, no stance/dispute lexicon, no antonym tables, no label-induced mappings, no feature→verdict shortcuts (features → interpretations → ledger → verdicts).
- **Verdict path:** Verdict bids read only `op_track`, `has_con`, `has_sup`, `contested` — all from ledger rows. Text is used only for CONTENT trace output, not decisions.
- **Determinism:** Byte-identical outputs across three runs (SHA256 verified).

## Protocol deviation

**README access (2026-09-27):** During setup, the first five lines of `~/workspace/epi_a3/blind/README.md` were accidentally displayed. They contained only counts and column descriptions, no labels or mappings. This file is outside the prereg's absolute "works ONLY from" list. Recorded as a protocol deviation. The content contained no label information and did not influence the implementation. Broker treatment pending.

## Label-blind access confirmation

**Read (authorized):**
- Frozen prereg (`docs/lab/epistemic_native/PREREG.md`).
- `~/workspace/AGENTS.md`.
- Train input: `~/workspace/epi_a3/blind/train_blind.tsv` (blind, no labels).
- Substrate: `ARCHITECTURE.md`, `EVIDENCE_R4.md`, `NEUTER10_WHITEBOX.md`, `deliberate.zag`, `build/deliberate_frozen_r4.zag`.
- Own quarantined prototype (architectural review only).
- `~/workspace/epi_a3/blind/README.md` first five lines (accidental, protocol deviation noted above).

**Not read:**
- Held-out input or text.
- Labels, mappings, verdict files, class column, labeled corpus.
- Attempt-2/attempt-3 documents, sealed mappings, forbidden lexicon files.

**Hashes:**
- Train SHA-256: `ebd76e2ca32e18aa66b65a17afa9601ce22c6ce9666a1b2d7d2271ac2b9ec941`
- Substrate SHA-256: `7dec26d8600683f2c6cefc83d524a403f4ac288117864108dc54a08afa61b787`

## LOO results (opaque)

Three byte-identical runs. SHA256: `f5666e76dc97ee2c7dbdce171ff5cd0696e93e19cacf5062f44e0b22a518efc5`

Distribution (opaque IDs):
- V1: 2
- V2: 113
- V3: 24
- V4: 309

**Note:** Implementer never scores. Opaque IDs only. No label access.
