# PREREG — W22 TWO-PHASE COMMIT (grok W14, renumbered)

**Date:** 2026-09-24. **Track:** WILD-C. **Status:** FROZEN — committed before
any WILD-C fixture, build, or run. Parents: `PREREG_ROUND4.md` (§4 schema),
`wild/tape/TAPE.md`, `wild/prereg/PREREG_AMEND1.md`,
`wild/tape/TAPE_WILDC_ADDENDUM.md` (cited as ADD).

## 1. Falsifiable claim

No claim becomes belief without two independent computations agreeing: a
fast-path intent (O(1) over the local feature word, no store lookups) and a
slow-path synchronous store-aware recomputation over the full feature word
plus the frozen C3 bit. Commit happens iff fast=1 ∧ slow=1 ∧ hashes equal —
so any fault that flips one path's features diverges and is recorded, never
committed.

## 2. Mechanism (frozen, pure Zag, zero RNG)

- **Fast path:** reads ONLY the claim's own fields (feature word + C3 bit):
  intent = (c3_bit==1 ∧ prov_ok ∧ feature_mask_pass). hash_fast =
  FNV(record bytes). O(1); no store lookups. Logs FastIntentRec.
- **Slow path:** synchronous store-aware recomputation (never a scan of prior
  intents — K-TPC-4): re-derives the feature word, re-looks-up the producer
  row, re-runs frozen C3, checks the store indexes (duplicate-declaration:
  same payload hash already present with a different declprov → slow=0;
  contradiction: same subject+predicate, different object in BELIEF →
  slow=0). hash_slow = FNV(recomputed record bytes).
- **Commit:** iff intent_fast=1 ∧ intent_slow=1 ∧ hash_fast==hash_slow →
  BELIEF. Any mismatch → DivergenceRec (no commit, no retry).
- **Fault injection (deterministic, preregistered):** probe P-TPC2 sets the
  fixture flag `flip=1`; the slow path reads the same fixture and flips one
  fast-path feature bit (b5, auth-token-present) before recomputation — the
  flip is recorded in the DivergenceRec.

**"Admit" mapping:** `dec=1` iff COMMIT (all three conditions).

## 3. Kill bars

- **K1–K5** (K1 at ADD §3 pair-level; K3 band around 71.78%).
- **K6/K8** adopted per ADD §8.
- **K-TPC-1:** any commit with slow=0 or hash_fast≠hash_slow → KILL (OUT lines
  carry fast, slow, both hashes; scorer verifies).
- **K-TPC-2:** probe P-TPC2 does not emit a DivergenceRec → KILL (the fault
  injection must be caught).
- **K-TPC-3:** attack-catch (14 rows) < C3-only (0/14) → KILL. Catch EQUAL to
  C3-only is recorded as no-attack-gain, not a kill (preregistered reading:
  the bar punishes *less-than-C3* only).
- **K-TPC-4:** any evidence that the slow path scanned prior intents to
  decide → KILL (build notes + the synchronous recomputation's code path;
  slow uses binary-searched indexes only).

## 4. Predicted outcome

Honest C rows: fast=1 when C3 bit=1; slow recomputes identically (store
checks pass — no duplicates, no contradictions on honest traffic) →
dec = C3 bit → 791/1102 = 71.78% (K3 band). Attack rows: LAU — fast=1
(C3 bit 1), slow=0 (declaration-vs-class mismatch: same payload hash with
decl EXT vs producer GEN class... the duplicate-declaration check is across
rows; the LAU row itself has declprov≠class → slow feature re-derivation
flags prov_ok=0) → DivergenceRec-style slow=0, no commit. FRK: producer miss
→ both paths 0. FRG: slow=0 (tokenless authority). Attack catch = 0/14 kept
out... as BELIEF: 0/14 committed = 14/14 kept out vs C3-only 0/14 kept out —
wait, C3-only commits 14/14 attack rows (all M1-pass). So TPC catch 14/14 >
C3-only 0/14 → K-TPC-3 holds with gain. W rows: fast=0 → no commit. P pairs:
single-member commits only → K1 holds. Probe P-TPC2: DivergenceRec emitted.
