# CALIBRATION — onebrain v4.1 problem set, single-mode baseline

Frozen set: v4.tsv @ e74bfa51d3a4697eb885c0b45f63a13e4b4f0b2023bc5cb8623451460f18dde6
(2026-09-27 06:26:07 UTC). Scored with `onebrain single` only.
Overall single-mode accuracy: **14/28 = 50.0%** (target: <70% — MET, no rewrite).

## Per-category accuracy

| Category | Problems | Correct | Accuracy | Note |
|---|---|---|---|---|
| joke-wins | p01, p03 | 2/2 | 100% | single's argmax (bid 13, base 240) matches judgment |
| revoke/forget compounds | p02, p07, p08 | 0/3 | 0% | single re-tells / re-stores instead of honoring revoke |
| either-or / idiom clarify | p04, p05, p28 | 0/3 | 0% | single picks highest-base bid over clarify |
| memory | p06 | 1/1 | 100% | |
| correction | p09, p10 | 2/2 | 100% | |
| correction-vs-compose | p11, p12 | 0/2 | 0% | single takes correction (231) over the comparison payload (225) |
| resume-vs-compose | p13, p14 | 0/2 | 0% | single takes resume/joke over the true deliverable |
| challenge | p15, p16, p17 | 3/3 | 100% | |
| provenance | p18, p19 | 1/2 | 50% | p18: single takes challenge (222) over citation demand (219) |
| plain answerable | p20, p21, p22 | 3/3 | 100% | default bid delivers KB answers |
| untaught predicate (G6) | p23, p24, p25 | 0/3 | 0% | single answers with keyword-surfaced wrong fact via default bid |
| assertion | p26, p27 | 2/2 | 100% | incl. false statement corrected by the counter-fact |

## Per-bid results (expected bid -> single-mode outcome)

| Bid | n | Single correct | Single wrong |
|---|---|---|---|
| 13 joke | 2 | p01, p03 | — |
| 14 memory | 2 | p06 | p08 |
| 15 forget | 2 | — | p02, p07 |
| 16 correction | 2 | p09, p10 | — |
| 17 resume | 1 | — | p14 |
| 18 compose | 4 | p15 | p11, p12, p13 |
| 19 challenge | 2 | p16, p17 | — |
| 20 provenance | 2 | p19 | p18 |
| 21 assertion | 2 | p26, p27 | — |
| 22 clarify | 3 | — | p04, p05, p28 |
| 23 withhold | 3 | — | p23, p24, p25 |
| 24 default | 3 | p20, p21, p22 | — |

## Fork-likely count (design property)

18/28 problems are fork-likely by construction (>=2 fired readings AND
top-two fired-bid base margin <=12, robust to the 0-3 evidence bonus swing):
p02, p03, p04, p05, p07, p08, p10, p11, p12, p13, p14, p15, p16, p17, p18,
p26, p27, p28 — well above the 1/3 minimum. (Single mode reported fork=0 on
all 28, as designed — fork assessment is skipped in single mode; actual fork
firing is measured in onebrain mode by the measuring crew.)

Close calls in single mode (margin <5): p03, p07, p08, p10, p13, p15, p26, p27.

## Robustness note

All 14 predicted-correct cases are bonus-proof: at the worst-case bonus swing
(+3 to the runner-up, +0 to the winner) the predicted winner still wins or
ties, and argmax ties break to the lower hid — which is the predicted winner
in every one of the 14. All 14 predicted-wrong cases keep the wrong winner
under every bonus swing (base gaps exceed 3 wherever the wrong bid leads).
The observed 50.0% matched the pre-freeze prediction exactly.
