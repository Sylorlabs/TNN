# GROK47 MANIFEST — everything-everywhere loop inventory

Built 2026-09-21 night. Full item list: `MANIFEST_ITEMS.tsv` (path, kind, tier, owner, size, status, verdict).

## Scale

- Total items: 5282
- By kind: {'md': 1904, 'zag': 2479, 'py': 375, 'jsonl': 524}
- By tier: {'P0': 2894, 'P1': 2221, 'P2': 129, 'P3': 38}
- By owner: {'coordinator': 1311, 'imagination': 39, 'language': 298, 'reasoning': 35, 'representation': 1229, 'senses': 140, 'teacher': 2226, 'memory': 4}

## Tiers

- P0: canonical mechanism .zag + verdict/prereg/findings/ledger docs — full HTRF per item.
- P1: analysis scripts, corpora, other docs — review-level HTRF (grok reads, hypothesizes; test where cheap).
- P2: evidence logs — sampled verification.
- P3: scratch/backup/superseded/cache/raw — inventory only, no loop.

## Owners

teacher/memory/reasoning/language/representation/senses/imagination = sector workers; coordinator = direct grok-first sweep + shared regions (docs/history/ops/work/toolchain). Sibling track coordinators (senses-deep, design/UI-toolkit, Goal-A imagination, Goal-B story) own deep R&D in their areas — this sweep covers their files at review level only, no duplicate deep experiments.

## Coverage tracker (updated 2026-09-22 ~00:30 PDT after merging 7 worker ITEMS_DONE.tsv files, zero conflicts)

| Tier | Total | Done | In-progress | Pending |
|---|---|---|---|---|
| P0 | 2894 | 2202 | 1 | 691 |
| P1 | 2221 | 1768 | 0 | 453 |
| P2 | 129 | 54 | 39 | 36 |
| P3 | 38 | 18 | 0 | 20 |
| **Total** | **5282** | **4042 (76.5%)** | **40** | **1200** |

("Done" counts status done/PASS/review-note. All pending items are coordinator-mapped: new overnight files + review-only sibling-track docs. Merge report: MERGE_REPORT.json.)

Status values: pending / in-progress / done. Verdict values: PASS / FAIL-fixed / FAIL-open / review-note.
