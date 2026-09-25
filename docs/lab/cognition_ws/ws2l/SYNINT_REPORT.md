# WS2-L Synonym Integration — Final Report (2026-09-25)

## Verdict: SUBSTRATE-UNIFIED, TRIGGER-SEPARATE

The audit found the synonym learner was **SEPARATE** (own binaries, own
text store, no TNN code path, no lifecycle). The integration makes synonym
beliefs **TNN's own deliberate memories**:

- Every relation = one substrate memory (ma_add, SYN_VAL=1000000+rules)
- Every veto = one negative-value substrate memory (VETO_VAL=-1000000)
- Kill/pin/promote/audit through standard substrate operations
- Retrieval (syn_build) reads LIVE slots only
- No text side store; binary tables indexed by substrate slot

**Honest limitation**: The R1-R4 trigger is still batch ingest, not live
deliberation. See PREREG_SYNINT.md §6 amendment.

## Changes

### New: syn_mem.zag
- SynDb: elastic substrate sharding (works around frozen MA_CAP=256)
- syn_install/kill/pin/promote/is_live/slot_value
- syn_save/syn_load (binary substrate persistence)
- syn_count_live
- tables_save/tables_load (binary content tables)
- Imports frozen memory_core.zag (NOT modified) + lib.zag

### Modified: learn.zag
- Ingest installs relations/vetoes via syn_install (substrate)
- Substrate sync pass: new rows installed, dead slots re-installed
- Persists syntab.bin + synmem.bin (replaces synlearn.txt/synveto.txt)
- New CLI: kill|pin|promote <dir> <w1> <w2>
- dump shows LIVE/DEAD per relation + substrate summary

### Modified: toc_l.zag
- syn_build loads integrated store, filters by syn_is_live
- Killed relations excluded from transitive closure
- Map construction unchanged (byte-identical from identical inputs)

### Amended: PREREG_SYNINT.md
- §6 documents unified vs not-yet-unified status honestly

## Regression Results

| Battery | Score | Required | Status |
|---------|-------|----------|--------|
| Official | 51/51 | 51/51 | PASS |
| Fresh | 6/6 | 6/6 | PASS |
| Distractors | 6/6 | 6/6 | PASS |
| Near-synonyms | 6/6 | 6/6 | PASS |
| Multihop | 4/4 | 4/4 | PASS |
| Morphology | 3/4 (QMO3 tie) | 3/4 | PASS |
| Relations | 112 | 112 | PASS |
| Vetoes | 4 | 4 | PASS |

- Relation/veto sets: byte-identical to frozen store (pairs, rules, lids)
- Determinism: 3x reruns byte-identical (SHA-256)
- GEN: 7 evidences → 4 new relations; 112/112 old intact; 120 live
- Lifecycle: kill (rc=0, DEAD, excluded), pin (rc=102 protects), promote (rc=0)
- Zero RNG: grep clean
- No curated strings in new code

## Seam Map

Evidence ingest (learn.zag) → R1-R4 rules → syn_install → ma_add →
substrate slot + audit ledger → syn_build (filters live[]) →
transitive closure → syn_canon → tocl lookup → grade.

The substrate's live[] is the sole authority on belief. Content tables
are indexed by (shard, slot), not an independent store.
