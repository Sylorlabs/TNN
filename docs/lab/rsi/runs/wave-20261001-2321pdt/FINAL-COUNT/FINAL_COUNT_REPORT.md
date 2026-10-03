# FINAL-COUNT report: wave-20261001-2321pdt WAVE_RECORD.md coherence check

Wave record checked: docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md, verdicts section ("## Verdicts (debated in DEBATE.md)" through "## Queued next").

## Count

47 verdict bullets. Confirmed by `grep -c '^- '` over the verdicts section: exactly 47.

## Verdict labels in order

1. Fork battery: 2 FRESH PASS; 55 RE-CERT PASS; 2 RE-CERT UNTESTABLE; 0 FAIL; archive 48/48 [NEW]
2. H-PI-REV2: BUILD-PASS [NEW]
3. RT-EXEC: EVIDENCE-HOLDS on both [NEW]
4. TNN3-SUBSTRATE: DESIGN-COMPLETE [NEW]
5. H5R2-REPRO: REPRO-PASS [NEW]
6. CONSEQ: VALIDATION-PASS [NEW]
7. CONTLEARN: BUILD-PASS, LEARNOWN-DEMONSTRATED [NEW] (supersession note: integration is MACHINERY-DEPENDENT, per CONTLEARN-OWNED)
8. TNN-3 H5R2: BUILD-PASS, H5R2 ADVANCES [NEW]
9. ARENA inquiry (C8): BUILD-PASS [NEW]
10. F1: BUILD-FAIL [NEW]
11. RT-INT: EVIDENCE-HOLDS on both, no dissent [NEW]
12. RT-GOV: HOLDS on all three axes, one QUALIFY [NEW]
13. ARENA2: BUILD-PASS [NEW]
14. ARENA3: BUILD-PASS [NEW]
15. F1-FOLLOWUP: Part 1 BUILD-PASS, Part 2 NOT-FOUND [NEW]
16. C174: VALIDATION-PASS [NEW]
17. BATTERY: Part 1 VALIDATED, Part 2 1/6 PASS [NEW]
18. DEVANG3: BUILD-PASS [NEW]
19. RT-C174: EVIDENCE-HOLDS, no dissent [NEW]
20. RT-HPIREV2: Part 1 QUALIFY, Part 2 bound PARTIALLY survives [NEW]
21. BATTERY-CLUSTER: COMPLETE [NEW]
22. H5R2-BASELINE: BASELINE-MATCHES via (a) REVERT-TO-LATEST [NEW]
23. C9BAT: GEN-PASS [NEW]
24. RT-SENSE: QUALIFY (BUILD-PASS stands) [NEW]
25. F1-BUFFER: BUFFER-NOT-PREDICTIVE [NEW]
26. ARENA4: BUILD-PASS [NEW]
27. BATTERY-E2: E2-CONTENT-BLIND [NEW]
28. H7R: BUILD-PASS [NEW] (supersession note present, see below)
29. BATTERY-E1: E1-FIRSTCLASS [NEW]
30. H5R2-DECOY: DECOY-DISCRIMINATES [NEW]
31. F1-REPAIR: GREEDY-CONFIRMED [NEW]
32. BATTERY-E3: E3-ORACLE-DEPENDENT [NEW]
33. F2V3: BUILD-PASS [NEW]
34. BATTERY-E6: E6-CONTENT-READ, with H2C-STICKY [NEW]
35. H6R: BUILD-FAIL [NEW]
36. BATTERY-E4: E4-PRECEDENCE [NEW]
37. ARENA5: BUILD-PASS [NEW]
38. F1-REPAIR2: REPAIR2-CONFIRMED [NEW]
39. BATTERY-E5: E5-INSTANCE-ONLY [NEW]
40. ARENA-BLIND: ORACLE-FREE [NEW]
41. H5R2-SKEPTIC2: SKEPTIC-SURVIVES [NEW]
42. BATTERY-E8: E8-BANDWIDTH [NEW]
43. RT-ARENA5: QUALIFY (BUILD-PASS stands) [NEW]
44. CONTLEARN-OWNED: MACHINERY-DEPENDENT [NEW]
45. ARENA-GEN: NARROW [NEW]
46. CONTLEARN-OWNED2: MACHINERY-DEPENDENT [NEW]
47. H5R2-SKEPTIC3: SEPARATED [NEW]

## DRAFT-CHECK discrepancy resolution

(a) Fork battery status tag: the record's fork battery bullet ends with the verbatim text "Commit 668ae8d8f. [NEW] (debate pending)". It carries [NEW], not [RE-CERT]. The [RE-CERT] tokens inside the bullet describe the per-ref battery outcomes (55 RE-CERT PASS, 2 RE-CERT UNTESTABLE); the bullet-level status is [NEW] as required.

(b) H7R supersession note: the H7R bullet carries the verbatim note "(Note: the "3/3 passing" claim in the worker's report is superseded by the H6R BUILD-FAIL verdict recorded below; the substrate halves are H2R PASS, H7R PASS, H6R FAIL.)". Confirmed present. Consistent with bullet 35 (H6R BUILD-FAIL).

## 47th verdict

Bullet 47 is H5R2-SKEPTIC3: SEPARATED [NEW] (gate vs NEWEST-LIVE-ON-KEY separator; pre-registered divergence signature on all four frozen kill bars). Present and correct.

## Duplicates

None. The lane identifiers (text before the colon in each bullet) are all unique; `sort | uniq -d` over all 47 returns empty. The MACHINERY-DEPENDENT label appears twice (bullets 44 and 46, CONTLEARN-OWNED and CONTLEARN-OWNED2) as two distinct lane verdicts, not a duplicated line.

## Coherence verdict

The wave record is coherent at 47 verdicts. Count is 47, label order is as listed, both DRAFT-CHECK discrepancies are understood (fork bullet is [NEW]; H7R carries the supersession note pointing to the H6R BUILD-FAIL), the 47th verdict H5R2-SKEPTIC3 SEPARATED is present, and there are no duplicate verdict lines.

## Label tally (informational)

BUILD-PASS (primary): 12; BUILD-FAIL: 2; red-team verdicts: 7 (EVIDENCE-HOLDS x3, QUALIFY x4 including RT-GOV, HOLDS as the RT-GOV axis verdict); validation/pass-type: 9 (VALIDATION-PASS x2, REPRO-PASS, GEN-PASS, DESIGN-COMPLETE, COMPLETE, VALIDATED, ORACLE-FREE, NARROW); fork battery: 1 (own battery verdict); experiment-outcome labels: 16 (all others). All 47 bullets carry [NEW]. Check: 12+2+7+9+1+16 = 47.
