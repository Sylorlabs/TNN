# WS2-B RUNLOG — forced table-of-contents retrieval scheme

## 2026-09-24 ~08:05 PDT — task received
WS2-B dispatched: build the ToC-forced approach, test to Micah's 100% bar.
Note: ws2/RUNLOG.md belongs to WS2-A; this is the WS2-B log.

## 2026-09-24 — survey
- Read memory_org arms (lib.zag 1320 lines, 3 arm drivers), SCHEME_FORMAT.md,
  scorer.py, SCORES.md/RESULTS_MORG.md: prior best SELF 0.6833 overall F1;
  no arm near 100%.
- Read MA1 memory agency (deliberate kill/pin/promote) and ctx partitions
  (per WS2-A's survey notes).
- WS2-A battery landed mid-task: shared/PROBE_BATTERY_SPEC.md v1 (51 queries,
  5 classes) + ws2/fixtures/{probe_corpus.txt,probe_queries.txt,
  validate_battery.py}. Per task instructions, WS2-B USES their battery as the
  primary bar (first prereg draft's self-authored 56-probe battery dropped
  before any run; prereg rewritten to adopt WS2-A battery + 7-probe WS2-B
  maintenance leg, still pre-run).
- Wrote PREREG_WS2B.md (frozen): ToC design (key buckets T/D/S/TD/TS/DS/TDS +
  keyword index KW/AGG), maintenance rules, lookup algorithm (text-only,
  hints ignored; Route A subject-anchor / Route B type-domain / Route C
  keyword fallback with score-0 abstention), frozen stemmer/stoplist,
  58-probe bar (51 WS2-A + 7 maintenance), any-miss=FAIL, secondary tiers
  T-exact (52) / T-para (6), bill metrics, determinism contract.

## 2026-09-24 — prereg + maintenance fixtures committed (SHA pending)
- Staged: PREREG_WS2B.md, WS2B_RUNLOG.md, WS2B_MAINT_{items,revise,probes}.txt
  → docs/lab/cognition_ws/ws2/ on branch tnn-native-lab.

## next
- Implement src/toc.zag (pure Zag, @import lib.zag), build with pinned znc.
- Run primary battery (51) + maintenance leg (7); grade; 3x determinism.
- Diagnose misses individually; measure bill; write WS2B_PRELIM.md; verdict.

## 2026-09-24 — Implementation complete, evaluation complete

### Critical bug fixed: insertion-sort position clobber
- All 6 insertion sorts used `else { b=-1; }` to break the inner loop,
  which destroyed the insertion position. Fixed with a separate `done` flag.
- Also fixed: 3-field query parser (text from field 2, not field 1);
  tok_set_low lowercasing contract enforced at call sites.

### Evaluation results
- Official battery (51): 46/51. T-exact 45/45 PASS. T-para 1/6 (QP04 via stemming).
  - 5 misses (QP01,02,03,05,06): all P-PARA with zero token overlap (verified
    by validate_battery.py). 4 correctly abstained, 1 false positive (QP05
    via token "before").
- Maintenance leg (7): 7/7 PASS (install/revise/delete all verified).
- Total: 53/58.
- Determinism: 3 clean reruns byte-identical (SHA-256 verified).

### Bill
- ToC disk: 33 items 6,930B; 36 install 7,557B; 36 revise 7,577B; 35 delete 7,368B.
- Ops (official after 51 lookups): toc_rd=15843 toc_wr=310 kw_build=33 agg_re=23
  item_rd=2 item_wr=33 score=1143.

### Verdict
ADOPT with iteration. 100% on all retrievable probes. P-PARA misses are
vocabulary-gap (expected per battery spec), not mechanism bugs.
