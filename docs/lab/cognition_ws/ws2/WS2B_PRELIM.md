# WS2-B Preliminary Findings — Forced ToC Retrieval Scheme

**Date:** 2026-09-24
**Worker:** WS2-B direct
**Status:** Implementation complete, evaluation complete, 53/58

## Summary

Built a deliberately-managed Table of Contents (ToC) for TNN cognition memory
in pure Zag. The ToC is updated on install/revise/delete and consulted on
every lookup. No raw item text is scanned during retrieval.

**Result: 53/58 probes PASS (46/51 official + 7/7 maintenance).**

The 5 misses are all P-PARA (paraphrase) probes with **zero exact-token
overlap** (verified by the official `validate_battery.py`). Per the battery
spec, these are EXPECTED to be NOT_RETRIEVABLE — they document the vocabulary
gap. Per the frozen prereg §5, T-para failures are reported as a diagnostic
tier.

## Critical Bug Found and Fixed

**Insertion sort position-clobber bug** (all 6 insertion sorts in toc.zag):

The pattern `else { b=-1; }` to break out of the inner shift loop destroyed
the insertion position. When the loop exited because it found the correct
insertion point (not at index 0), `b` was clobbered to -1, so the key was
always inserted at position 0, duplicating entries and losing data.

**Fix:** Use a separate `done` flag to break the loop while preserving `b`.

This bug corrupted:
- `tok_set_low` (token sorting) → malformed KW and cells
- `sort_ids`, `sort_tok`, `sort_lines` (ToC construction) → duplicate/missing keys
- `sort_rank` (candidate ranking)
- `sort_by_id` (item ordering)

**Additional fixes:**
- 3-field query parser: text was taken from field 1 (K) instead of field 2
- `tok_set_low` now lowercases input at call sites (contract enforcement)

## Evaluation Results

### Official Battery (51 probes): 46/51

| Tier | Result |
|------|--------|
| T-exact (45 non-PARA) | 45/45 PASS |
| T-para (6 P-PARA) | 1/6 (QP04 via stemming) |

**Misses (all T-para, zero token overlap):**
- QP01: "why do moonwalkers hop gently under weak selenian attraction" → PP01.
  Route 3, 0 candidates. Zero token overlap (moonwalk≠astronaut, hop≠bounce, etc.).
  Correctly abstained.
- QP02: "why does pickled kraut fizz while bacteria dine fortnights" → PP02.
  Route 3, 0 candidates. Zero token overlap. Correctly abstained.
- QP03: "when should withered limbs be trimmed prior to sprouting" → PP03.
  Route 3, 0 candidates. Zero token overlap. Correctly abstained.
- QP05: "which witticism about beginning before readiness" → PP05.
  Route 3, 1 candidate (PP03, score 1 via token "before").
  FALSE POSITIVE: "before" appears in both query and PP03's KW.
  PP05 has zero overlap. Vocabulary gap.
- QP06: "why does sacred song linger inside basilica masonry" → PP06.
  Route 3, 0 candidates. Zero token overlap. Correctly abstained.

### Maintenance Leg (7 probes): 7/7 PASS

- W01-W03 (after install): all pass
- W04-W05 (after revise NW01): all pass
- W06-W07 (after delete NW02): all pass, W07 correctly abstains (K=0)

### Determinism

Three complete clean-store reruns: **byte-identical** across all outputs
(toc.txt, kw.txt, cells.txt, manifest.txt, out.txt, rep.txt). SHA-256 verified.

## Bill

### ToC Disk Sizes (synthetic 33/36/35-item stores)

| Checkpoint | toc.txt | kw.txt | cells.txt | manifest.txt | Total |
|------------|---------|--------|-----------|--------------|-------|
| 33 items | 3,135 | 1,839 | 1,938 | 18 | 6,930 |
| 36 after install | 3,417 | 2,007 | 2,115 | 18 | 7,557 |
| 36 after revise | 3,417 | 2,017 | 2,125 | 18 | 7,577 |
| 35 after delete | 3,323 | 1,961 | 2,066 | 18 | 7,368 |

Official 33-item store: toc.txt 6,989, kw.txt 2,164, cells.txt 1,730,
manifest.txt 18, items.txt 2,656 (13,557 total).

### Operation Counters (official store after 51 lookups)

```
toc_rd=15843 toc_wr=310 kw_build=33 agg_re=23 item_rd=2 item_wr=33 score=1143
```

- toc_rd: ToC key comparisons during lookups
- toc_wr: ToC lines written during build
- kw_build: items tokenized for KW
- agg_re: subject aggregates rebuilt
- item_rd/item_wr: item file reads/writes
- score: candidate scoring operations

## Verdict

**ADOPT with iteration.** The forced-ToC scheme achieves 100% on all
retrievable probes (T-exact 45/45, maintenance 7/7). The 5 P-PARA misses are
a fundamental vocabulary-gap limitation of exact-token matching, not a
mechanism bug — they are correctly abstained (4/5) or flagged as false
positives (1/5). The battery spec itself expects these to fail.

**Recommended iteration:** Add a synonym/paraphrase bridge layer (still
deterministic, e.g., a frozen synonym table) to address T-para without
compromising the exact-match precision that gives 100% on T-exact.
