# Repair Cycle #4 — Evidence Summary (Kind-0 Causal Wiring)

**Date:** 2026-09-27
**Branch:** `tnn-native-lab` (not committed)
**Source:** `~/workspace/delib_r4/src/deliberate.zag`
**Binary:** `~/workspace/delib_r4/build/deliberate_final_bin`

## The void being repaired
Third red team (2026-09-27) voided K5: kind-0 reading rows (HIDs 0–9) were computed
and traced but never consulted. Neutering all readings changed 0/77 answers.

## The repair
Every action generator now reads its shared kind-0 row from the ledger instead of
re-deriving the utterance classification privately:

| HID | Reading | Read site |
|-----|---------|-----------|
| 0 | correction | `gen_correction` fire condition |
| 1 | resume | `gen_resume` fire condition |
| 2 | challenge | `gen_challenge` fire condition |
| 3 | provenance | `gen_provenance` fire condition |
| 4 | joke | `gen_joke` fire condition |
| 5 | memory | `gen_mem` fire condition |
| 6 | forget | `gen_forget` fire condition |
| 7 | assertion | `gen_assertion` fire condition |
| 8 | compose | `gen_compose` gates on shared evidence |
| 9 | plain | `gen_default`/`gen_withhold` routing |

`utter_type()`, `is_correction`, `is_resume`, `is_challenge`, `prov_match` are now
called ONLY from `gen_readings()` (the kind-0 writer). Verified by static grep.

HID 9 changed from always-1 to genuine none-of-the-above (1 iff HIDs 0–8 all zero).

## Test results

### Answer preservation (vs original frozen binary)
| Battery | Answers | Differences |
|---------|--------:|------------:|
| Round 4 | 29 | 0 |
| B20 | 28 | 0 |
| Held-out | 20 | 0 |
| **Total** | **77** | **0** |

### Causal impact (neuter test)
| Variant | Changed |
|---------|--------:|
| All rows neutered (HIDs 0–9) | **67/77** (was 0/77) |
| Row 0 (correction) | 6/77 |
| Row 1 (resume) | 0/77 on batteries; **proven on synthetic turn** |
| Row 2 (challenge) | 0/77 on batteries; **proven on synthetic turn** |
| Row 3 (provenance) | 0/77 on batteries; **proven on synthetic turn** |
| Row 4 (joke) | 4/77 |
| Row 5 (memory) | 0/77 on batteries; **proven on synthetic turn** |
| Row 6 (forget) | 3/77 |
| Row 7 (assertion) | 10/77 |
| Row 8 (compose) | 8/77 |
| Row 9 (plain) | 41/77 |

Rows 1,2,3,5 have zero battery coverage (no resume/challenge/provenance/memory
turns in the frozen batteries). Synthetic proof turns confirm each is individually
causal (neutering changes the answer).

### K1 reversal
0/77 answer differences under reversed GEN call order. PASS.

### K2 counterfactual
Spot check: 1819→1820 KB flip moved birth-year answer covariantly, others identical.

### K3 bijection (structural)
29/29 turns: 10 READ + 12 CAND lines, ARGMAX winner always a valid CAND. No errors.

### K4 accuracy
Identical to baseline: 22/24 scored PASS, 2 FAIL (R4-01 turns 2, 5 — historical,
fail identically on original).

### Determinism
Byte-identical reruns verified (SHA-256 of answer sets match across runs).

## Status
Awaiting fourth red team verdict. If PASS, proceed to commit.
If VOID, repair narrowly per findings.
