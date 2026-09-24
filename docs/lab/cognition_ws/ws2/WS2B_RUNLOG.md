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
