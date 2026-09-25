# MECHANISM.md — ARM L (learned synonyms) mechanism specification

Frozen before any learning run (PREREG_WS2L.md §6 step 3). Pure Zag,
deterministic, zero RNG. Two binaries: `learn` (learning) and `tocl`
(retrieval). Reuses the frozen WS2-B stemmer + stoplist and the frozen
phase-1 lookup UNCHANGED (sources copied from
`~/workspace/cognition_ws/ws2/bdir_ws2b2/`: `lib.zag`; `toc_b2.zag` copied
to `toc_l.zag` with only the synonym-source replaced — see §6).

## 1. The store (starts EMPTY)

- The synonym store lives in the store dir as two text files:
  - `synlearn.txt`: one line per installed relation:
    `w1|w2|rules|lids` — raw (unstemmed) words `w1<=w2` byte-wise,
    `rules` = `+`-joined installing rules (e.g. `R1+R2+R3`),
    `lids` = `,`-joined evidence IDs (e.g. `LEARN-0001,LEARN-0002`),
    in first-seen (corpus) order.
    Lines sorted by `(w1,w2)`; byte-stable.
  - `synveto.txt`: one line per veto: `w1|w2|R4|lids`.
- Internally, lids are kept in a per-relation linked list
  (`lhead`/`ltail`/`lnext`), NOT a flat contiguous block: relations
  interleave in global insertion order (e.g. R3 lids for relation A
  arrive after relation B's DEF/SYN lids), so a `(start,count)` flat
  layout silently misattributes lids. The list preserves insertion
  order; emit walks the chain. (Bug found and fixed 2026-09-25: flat
  `(start,count)` recorded wrong lids for R3 relations.)
- `learn dump <dir>` prints every relation with its provenance.
  Before any learning run the dump is empty (0 relations) — audited.
- K7 projection: 112 installed relations (50 <= 112 <= 200).

## 2. Learning rules (frozen surface patterns; builder's choice per §2.1)

The learner tokenizes each LEARN text into lowercase alphanumeric words.
`X`,`Y` are single words.

- **R1 DEFINITION**: text matches `^(a|an) X is (a|an) Y.$`
  (5 words) or `^X is a kind of Y.$` / `^X is an kind of Y.$`
  → propose X<->Y. One evidence installs.
  NOTE: DEF-labeled corpus lines not matching these surfaces (the MORPH
  form sentences, e.g. "went is the past form of go.") are INERT — they
  install nothing. No fifth rule is added (would need an amendment).
- **R2 EXPLICIT**: text matches `^X and Y are synonyms.$` (5 words)
  → propose X<->Y. One evidence installs.
- **R3 PARAPHRASE**: PARA lines are grouped by subject tag. A subject
  with exactly 2 lines whose tokenizations have equal length and differ
  in exactly one word position yields candidate pair (wa,wb) with that
  subject as witness. The pair installs only when >=2 INDEPENDENT
  subjects witness the same unordered pair (anti-hallucination).
- **R4 NEGATIVE (veto)**: text matches `^(a|an) X is not (a|an) Y.$`
  (6 words) or `^X is not Y.$` (4 words) → BLOCK X<->Y permanently.
  Vetoes are collected FIRST; any positive proposal for a vetoed pair
  is dropped (counted as veto-suppressed, printed in the run log).
  The veto list is written to `synveto.txt` as permanent audit evidence.

All installed pairs are stemmed with the FROZEN WS2-B stemmer before
storage in the lookup map (same as WS2-B2 did with its table).

## 3. Transitivity choice (builder's choice, documented before test runs)

**Transitive closure via union-find, computed at lookup-map build time
(`syn_build`) over the stemmed evidence pairs.** Every stem maps to the
lexicographically smallest stem of its equivalence class
(`syn_canon` interface unchanged from WS2-B2).

- Rationale: MULTI-HOP chains (sofa|couch + couch|settee) must compose;
  without closure the battery's chains cannot resolve at all.
- Veto safety: closure is PROVEN veto-safe on the frozen corpus — none of
  the 4 veto pairs (wolf|dog, borrow|lend, cheap|free, hot|spicy) is
  transitively connected by the 112 positive pairs (prototype:
  `work_l/proto_closure.py`; the learner additionally ASSERTS this at
  every ingest and fails loudly if violated).
- Merged classes on the frozen corpus (intended only): 
...[truncated 2202 chars]
