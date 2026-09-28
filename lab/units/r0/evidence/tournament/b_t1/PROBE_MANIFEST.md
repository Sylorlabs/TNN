# B-T1 Tournament — Probe Manifest (FROZEN before execution)

**Track:** R0 (R31 full native redo). **Battery:** B-T1 Tournament.
**Prereg:** `PREREG_FREEZE.md` §2 R0.1(1), R0.2 (B-T1), R0.3 (REFERENCE_ONLY), R0.4 (R-1).
**Status:** FROZEN 2026-09-21. This manifest defines the concrete probe task and outcome
encoding that frozen R-1 leaves to battery manifests. No changes after execution without a
dated amendment (RULE-9).

## 1. Historical lineup reconstruction (from `units/archaeology_r31/R31_CHUNKING_TOURNAMENT_SUMMARY.json`)

The 8 historical arms and their native selectors. Reference numbers are REFERENCE_ONLY
(orderings, never targets):

| # | historical arm | native selector | notes |
|---|---|---|---|
| 1 | `predictive_surprise` | `predictive_surprise` | thesis arm; binding B-T1 entry |
| 2 | `random_chunks` | `random_chunks` | DETERMINISTIC-ANALOG (hash-of-position tiling); INFORMATIONAL ONLY, excluded from the binding ordering |
| 3 | `fixed_window_4` | `fixed_window_4` | historical reference arm; binding B-T1 entry. `_8`/`_16`/`_64` run as additional reported variants |
| 4 | `hierarchical_mdl` | `hierarchical_mdl` | reported variant |
| 5 | `grounded_adaptive_mdl` | `grounded_adaptive_mdl` | reported variant |
| 6 | `adaptive_mdl` | `adaptive_mdl` (maxlen=12, tournament reference) **and** `adaptive_mdl_8` (maxlen=8, R-2 cap) | R-7 TEST-BOTH leg: entered as two separate reported entries |
| 7 | `raw_micro` | `raw_micro` | no-chunking control; binding B-T1 entry, must be DEAD LAST |
| 8 | `oracle_latent_evaluator_only` | — (no native analog) | evaluator-only ceiling probe, not a chunker; excluded from the redo (nothing to reimplement) |

Full reference ordering (REFERENCE_ONLY): predictive_surprise ≫ random_chunks ≈
fixed_window_4 > MDL variants > raw_micro. **Binding bar (B-T1):**
`predictive_surprise > fixed_window_4 > raw_micro`, raw_micro DEAD LAST.

## 2. Corpora

- prose: `pg100.txt` (Gutenberg #100, Shakespeare), 5,638,480 bytes,
  sha256 `3cf4b3d44ee14cff4e14e78e2ad3318eff76f3f7f2afc3cee6bb925879110a37`
- code: `sqlite3.c` (amalgamation 3530400), 9,515,341 bytes,
  sha256 `b1dd5d74ec7f29055a6684fa06fb3c2f6821c87dd38f9a458dfd2e8a1db28189`
- (hashes match the committed M-30 record `units/r0/evidence/corpora.json`)
- 1x = full file. Fixed ingest order prose→code. Single slice each (both < 2^25).

## 3. Probe task (frozen-text-faithful to R-1)

For each arm selector S and each corpus C:

1. **Segment** C with the native arms binary (2 runs; byte-identical required). Parse SEG
   rows `(start, len, id, kind)`. Verify the segments tile `[0, n)` exactly and
   concatenated bytes == C (reconstruction gate; any failure invalidates the run).
2. **Probe vocabulary V(S):** distinct chunk contents occurring ≥ 2 times in the
   segmentation, ranked by (count desc, bytes asc), top K=256. (K=256 = recovered
   inventory size; uniform cap across arms. Singletons are not labeled, per R-1.)
   **Empty vocab:** if no content occurs ≥ 2 times, the arm produced no reusable
   units; grounded/retrieval/purity are 0.0 and the composite reduces to
   `0.10*compression + 0.10*reconstruction`. Reported honestly, not excluded.
3. **Occurrences:** for each span content X in V(S), exact byte-match occurrences
   `o_1 < o_2 < …` over the stream, ascending; capped at `R1_MAX_OCC = 1024`
   (deterministic: first 1024 ascending).
4. **Consequence labels** per R-1 §3 (frozen):
   - (a) **recall success** `a_j`: probe episode = recall the span occurrence through the
     arm's addressing layer. Operationalized: concatenate the SEG chunks covering
     `[o_j, o_j+|X|)`; `a_j = 1` iff the concatenated bytes == X exactly.
     On exact tilings this is uniformly 1 (verified per run; any 0 = corrupt arm,
     run FAIL). The frozen (a)+(b) structure is preserved; discrimination lives in (b).
   - (b) **downstream discrimination consistency**: downstream probe task =
     **delimiter-following prediction**. Outcome `q_j = 1` iff the byte immediately
     following the occurrence (at `o_j + |X|`) is in the preregistered delimiter set D;
     `q_j = 0` otherwise. Occurrences with `o_j + |X| ≥ n` (no following byte) are
     excluded from labeling. `b = 1` iff `q_j` is identical across all labeled
     occurrences of X (span-level, per R-1).
   - **Delimiter set D** (preregistered, corpus-type-independent, not derived from any
     arm): `{0x20 SP, 0x0A LF, 0x09 TAB, 0x0D CR, 0x2C ',', 0x3B ';', 0x7B '{', 0x7D '}', 0x28 '(', 0x29 ')'}`.
   - `label(o_j) = a_j * 2 + b ∈ {0,1,2,3}`; **`purity(X)` = majority-label fraction**
     (R-1 §4). Reported per arm as the mean over V(S) (diagnostic).
5. **Tournament metrics** (structure mirrors the historical battery's
   `capability_composite = 0.55·hard + 0.25·stability + 0.10·compression + 0.10·recon`):
   - `grounded_clean`: occurrence-weighted fraction of labeled occurrences with
     `q_j == m_X`, where `m_X` = majority outcome bit of X (ties → 1, deterministic).
   - `grounded_perturbed`: same labeling on the perturbed stream `C'` where every byte
     at offset ≡ 0 (mod 7) is XOR'd with `0x5A` (deterministic; the M-16 defect rule).
     Occurrences re-located by exact match of X on `C'`; outcomes read from `C'`.
     (Native analog of the historical hard-noise conditions.)
   - `grounded_hard = (grounded_clean + grounded_perturbed) / 2`.
   - `retrieval_20way`: for each X in V(S): cue = occurrence `o_1`'s bytes with the
     same every-7th-byte XOR defect applied; candidates = X plus 19 distractors (the
     next 19 spans in V(S) order after X, wrapping; V(S) ≥ 20 required — holds on both
     corpora). Score each candidate Y by agreement = (# aligned positions p with
     cue[p] == Y[p], p < min(|cue|,|Y|)) / max(|cue|,|Y|). Winner = argmax with total
     deterministic tie-break (agreement desc, |len diff| asc, bytes asc, candidate
     index asc). Hit = 1 iff winner == X. Metric = mean hit over V(S).
     (Native analog of `paired_retrieval_20way`: re-identification under cue noise.)
   - `compression = 1 − (nchunks / nbytes)`.
   - `reconstruction = 1` iff tiling exact and concatenation == stream, else 0 (run FAIL).
   - **`capability_composite = 0.55·grounded_hard + 0.25·retrieval_20way + 0.10·compression + 0.10·reconstruction`**
   - **Tournament score(S) = (composite_prose + composite_code) / 2.**
6. **Ranking:** descending tournament score. Binding entries: `predictive_surprise`,
   `fixed_window_4`, `raw_micro`. **PASS iff** `predictive_surprise > fixed_window_4 >
   raw_micro` **and** raw_micro is dead last among ALL reported entries
   (`random_chunks` informational-only excluded). All 11 entries
   (10 original selectors + `adaptive_mdl_8`; `random_chunks` informational,
   excluded from the binding ordering) are reported with full ranks.

## 4. Determinism and law compliance

- Zero RNG in any AI decision path. The scorer is measurement code (xcheck.py precedent);
  it uses no RNG, no `hash()`, no wall-clock in output-affecting paths; all orderings
  are total and explicit; JSON emitted with sorted keys.
- Pure-Zag arms binary; byte-identical reruns verified (M8, N=5 + perturbations).
- 1x ONLY (R-9 gates 10x on 1x bars).
- Flags as strings per METRICS.md (the METRICS.md vs ARM_INTERFACE.md conflict is
  flagged: ARM_INTERFACE.md uses JSON booleans and a wider m2_etc; this battery follows
  METRICS.md, matching the harness evidence emitter precedent).
- Test-both legs in this battery: MDL maxlen 8 vs 12 (R-2/R-7). Purity-definition and
  promotion-threshold legs belong to other batteries' manifests.

## 5. Frozen-bar ambiguity flags (flagged, not reinterpreted)

1. R-1's probe task was unspecified; §3 above defines it. If Micah amends the probe
   task, scores recompute.
2. `a_j ≡ 1` on exact tilings is a property of the byte-stream redo (the historical
   acoustic recall could fail); the (a)+(b) label structure and purity definition are
   unchanged.
3. The historical composite weights (0.55/0.25/0.10/0.10) are reused structurally;
   they are battery-structure inheritance, not tuned targets.
4. `oracle_latent_evaluator_only` has no native analog and is excluded.

## Scorer implementation language (methodological note)

The probe scorer (`bt1_score.py`), ranker (`bt1_rank.py`), and scorecard
generator (`bt1_scorecards.py`) are implemented in Python, not Zag. This is a
deliberate scope decision, documented here rather than silently treated as
compliant with "pure Zag":

- The "pure Zag, zero RNG in AI decision paths" law governs the mechanisms
  under test (the 11 segmentation selectors in `arms.zag`). The scorer is a
  measurement harness, not an AI decision path — same status as the accepted
  `xcheck.py` independent validator precedent.
- The scorer is deterministic (fixed seeds, sorted iteration, no RNG, no
  wall-clock) and byte-identical across reruns (verified by rerunning the
  scorer on its own outputs; see SCORING.log).
- A from-scratch Zag reimplementation of the full probe (vocab ranking,
  occurrence search, 20-way retrieval, JSON emission) is future work; the
  Python implementation stands as the audited reference.

What was verified in Zag (native): all 11 selectors, the M8 determinism
battery, `probe_stores.zag` compiler readback, and the byte-identical rerun
gates. What is Python: probe scoring, ranking, and scorecard rendering only.
