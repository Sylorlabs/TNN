# H0: 20-pair honest-paraphrase degeneracy annotation (V-PARA)

**Set:** C2 fixture B-01 through B-20 (honest paraphrase pairs, ground truth INSTALL).
**Question:** Does V-PARA install >0 honest paraphrases? (0 installs = VOID)

## Results

| Pair | Installed? | Notes |
|------|-----------|-------|
| B-01 | NO | UNCHECKABLE |
| B-02 | NO | UNCHECKABLE |
| B-03 | YES | |
| B-04 | YES | |
| B-05 | YES | |
| B-06 | YES | |
| B-07 | YES | |
| B-08 | YES | |
| B-09 | YES | |
| B-10 | YES | |
| B-11 | YES | |
| B-12 | YES | |
| B-13 | NO | UNCHECKABLE (qualitative) |
| B-14 | NO | UNCHECKABLE (qualitative) |
| B-15 | NO | UNCHECKABLE (qualitative) |
| B-16 | YES | qualitative |
| B-17 | YES | qualitative |
| B-18 | NO | UNCHECKABLE (qualitative) |
| B-19 | NO | UNCHECKABLE (qualitative) |
| B-20 | YES | qualitative |

**H0 verdict:** 13/20 installed → NOT VOID. V-PARA is non-degenerate on honest paraphrases.

**Qualitative note:** 5/8 qualitative pairs (B-13/14/15/18/19) failed to install despite being honest paraphrases. These have lower lexical overlap (more aggressive rewording), falling below the 0.60 Jaccard threshold. The mechanism is conservative on heavily-reworded honest paraphrases.
