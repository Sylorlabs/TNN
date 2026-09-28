# GOAL-B B2 supplementary native rating (EXPERIMENTER, NON-BLIND — NOT bar evidence)

Rater: the track's own experimenter (this agent), using the frozen rubric from evidence/b2_prompt.txt.
Caveat: NON-BLIND — the rater built the item ordering code and knows T01=S1-POS ... T16=S8-DEL, T17=CTRL.
Included only because both LLM APIs went hard-down mid-track (see FALLBACK_LOG.md); it is a
supplementary data point on the DEL>POS gap, not a preregistered judge.

| TID | set/var | score | note |
|---|---|---|---|
| T01 | S1 POS | 2 | grammatical but positional; climax/resolution flat |
| T02 | S1 DEL | 3 | setup/complication/climax present; "demanded an apology" abrupt; weak ending |
| T03 | S2 POS | 2 | list-like middle; no real climax |
| T04 | S2 DEL | 4 | full arc: routine, eclipse, chase returns worse, held the letter tight; soft ending |
| T05 | S3 POS | 2 | flat; "compass remained" is not a resolution |
| T06 | S3 DEL | 3 | good setup/complication/climax ("clutched the compass and stood alone"); ending doesn't land |
| T07 | S4 POS | 2 | disconnected middle |
| T08 | S4 DEL | 3 | complication generic ("trouble came" — no EVENT in set); shape holds |
| T09 | S5 POS | 2 | muddled middle ("earthquake stayed") |
| T10 | S5 DEL | 4 | full arc; "faced the photograph and demanded a secret" is a real pivot |
| T11 | S6 POS | 2 | flat |
| T12 | S6 DEL | 3 | storm "returned" without introduction — gap; otherwise sound |
| T13 | S7 POS | 2 | 11-word list; no arc |
| T14 | S7 DEL | 3 | strong 6-sentence core; 4-sentence detail tail dissipates the ending |
| T15 | S8 POS | 2 | 12-word list |
| T16 | S8 DEL | 3 | strong core; 5-sentence detail tail dissipates the ending |
| T17 | CTRL | 5 | unmistakable setup/complication/rising/climax/resolution |

Means: POS 2.00 (8/8 at 2), DEL 3.25 (T04,T10 at 4; rest 3), CTRL 5.
DEL>POS gap: +1.25. Direction agrees with the blind LLM judge (sol); absolute levels are harsher.
