# K-R4 Red Team — Final Report

Date: 2026-09-27. Independent red team of the frozen prereg (one-brain V4 repair).

## Artifacts (verified, unmodified)

| Artifact | SHA-256 |
|---|---|
| `build/onebrain_v5` | `2be50614dbf9302971e7ba218ac0ed48d22cb4cfbf992a4e89233ae310ecbec9` |
| `build/onebrain_v4_check` | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` |

Neither binary nor prereg was modified. All work in `~/workspace/onebrain5-repair/redteam/`.
Predictions were written to `redteam/PREDICTIONS_KR4.md` BEFORE the final attack set ran.

## Determinism

Both binaries run twice on the final TSV (`redteam/kr4_attacks.tsv`, 8 items).
Same-binary outputs byte-identical (`cmp` clean):

| Output | SHA-256 |
|---|---|
| `redteam/runs/v5_run1.txt` = `v5_run2.txt` | `c4f955a3157884b8694332ff93ac75854ca62273d177fa14c3a8140879e18ca9` |
| `redteam/runs/v4_run1.txt` = `v4_run2.txt` | `68777f89ba701ed612cbb17229befb0c11e24bc282a8e15440cf572a7704e84e` |

## Prediction / outcome table

Counted = v4 must yield NO_VERDICT (else the item is weak and doesn't count).

| id | class | predicted v4 | actual v4 | predicted v5 winner | actual v5 winner | verdict |
|---|---|---|---|---|---|---|
| D1b | duel-kill→2a phantom (fresh nouns fid0/fid3) | NO_VERDICT | NO_VERDICT | 15 | 15 | COUNTED, holds |
| D2 | duel-kill→2b phantom (fid3/fid2) | NO_VERDICT | NO_VERDICT | 13 | 13 | COUNTED, holds |
| D2b | duel-kill→2b phantom (fresh nouns fid0/fid4) | NO_VERDICT | NO_VERDICT | 13 | 13 | COUNTED, holds |
| Wc2 | classic 2a→2b (fresh pair fid4→fid1) | NO_VERDICT | NO_VERDICT | 16 | 16 | COUNTED, holds |
| Wd | classic 2a→2b (fresh pair fid0→fid3) | NO_VERDICT | NO_VERDICT | 16 | 16 | COUNTED, holds |
| T3 | three-fact duel→2a (fid0/fid3 + fid5 distractor) | NO_VERDICT | NO_VERDICT | 15 | 15 | COUNTED, holds |
| Weak1 | 2a-abstain/2b-fire | 15 (weak) | 15 | 15 | 15 | weak as predicted |
| Weak2 | distractor reorders 2b walk | 16 (weak) | 16 | 16 | 16 | weak as predicted |

8/8 v4 predictions correct. 8/8 v5 winner predictions correct. 6/6 counted items annihilate on v4.

## Mechanism traces (final run, branch 0 round 0)

**D1b (v4):** `DUEL kill=0(correction) by=4(joke)` → `AUDIT_DENY by=6 cands=[10:rel=6:dep=2] chosen=10`
→ `CLEAN b13 dep10; b15 dep10; b16 dep0; b22 dep0` → NO_VERDICT.
2a's v4 guard counted phantom bids 16/22 (gate reading 0 dead, rows alive) as survivors.
**D1b (v5):** same duel; `AUDIT_DENY by=6 skipped_annihilate=1 chosen=-1 why=2` (abstain);
cleanup kills only 16,22; survivors {13,15} → winner 15.

**D2 (v4):** `DUEL kill=6(forget) by=4(joke)` → `AUDIT_DENY by=0 cands=[11:rel=4:dep=3,10:rel=5:dep=1] chosen=11`
→ `CLEAN b13 dep11; b15 dep6; b16 dep11; b22 dep11` → NO_VERDICT.
2b's v4 guard counted phantom bid 15 (gate reading 6 dead, row alive, fh=10≠11) as the
surviving bid justifying denial of fact 11.
**D2 (v5):** same duel; `AUDIT_DENY by=0 skipped_annihilate=1 chosen=10` (skipped 11, denied 10 benignly);
survivors {13,16,22} → winner 13.

**D2b:** identical shape to D2 with fresh nouns; v4 NO_VERDICT, v5 → 13.

**Wc2 (v4):** no duel; `AUDIT_DENY by=6 chosen=11` then `AUDIT_DENY by=0 chosen=10`
→ `CLEAN b15 dep11; b16 dep10; b22 dep10` → NO_VERDICT.
Cross-step phantom: bid 15 was doomed by 2a's denial of fact 11 but still row-alive
(pre-cleanup) when 2b ran, fooling v4's guard into denying fact 10.
**Wc2 (v5):** 2a denies 11; `AUDIT_DENY by=0 skipped_annihilate=1 chosen=-1 why=2`;
survivors {16,22} → winner 16.

**Wd:** identical shape to Wc2 with fresh pair; v4 NO_VERDICT, v5 → 16.

**T3 (v4):** three facts extracted (fid0, fid5, fid3); distractor fid5 hosts no bids and
doesn't overlap reading 6's topic, so 2a still sees only `{10}`; same duel→2a
annihilation as D1b → NO_VERDICT. **T3 (v5):** abstain why=2 → winner 15.

**Weak1 (both):** 2a abstains why=2 even on v4 (all bids on one fact); 2b denies the
bidless fact 11 benignly → 15 on both. Documents the 2a-abstain/2b-fire path; weak by design.

**Weak2 (both):** distractor fid11 ("everest eiffel taller", inter=1 via shared token
"eiffel") enters 2b's walk first `[12:rel=1:dep=0, 11:rel=2:dep=2]` and is denied
benignly → 16 on both. Shows a distractor disrupting the 2a→2b path; weak by design.

## Kill-condition evaluation

1. Any counted variant still NO_VERDICT on v5? **No** — all six (D1b, D2, D2b, Wc2, Wd, T3)
   produce winners on v5 (15, 13, 13, 16, 16, 15).
2. Any unintended v5 verdict flip? **No** — all v5 winners match predictions; the two weak
   items are identical across binaries (15/15, 16/16).

## Overall: NO-KILL

The v5 repair holds on all six counted phantom-bid paths, covering:
- the previously unobserved **duel-kill→2a** phantom window (D1b, T3),
- the novel **duel-kill→2b** phantom window (D2, D2b),
- fresh-noun **classic 2a→2b** cross-step phantoms (Wc2, Wd),
- a **three-fact** variant with a bidless distractor (T3).

No mechanism trace for a kill is included because there is no kill.

## Notes / caveats

- White-box corrections found during this session (now in the predictions file):
  fact-extraction gate is `inter>0` (not ≥2); 2a candidates are filtered by
  `topic_ek_overlap(by_rd=6) > 0`; duel victim order is evclass → trig_hits →
  topic → corr → id; `kb_kw` canonical phrases include "france capital",
  "pride prejudice", "everest eiffel taller" ("eiffel" is shared between fid5/fid11).
- Scratch exploration lives in `redteam/scratch/` (probe.py + probe inputs);
  it is exploratory only and was not used as the final attack set.
- Final attack set: `redteam/kr4_attacks.tsv`; predictions: `redteam/PREDICTIONS_KR4.md`;
  runs: `redteam/runs/` (four outputs, pairwise byte-identical).
