# REPORT: PROXY-REDESIGN -- structural interchangeability proxy (redun3)

## Headline verdict: PROXY-DISCRIMINATES

B9 PASS. The redun3 proxy (mutual runner-up coverage + dormancy)
discriminates genuine redundancy from adversarial activity on all
5 streams, reproducing the MA4C-MULTISTREAM K=3 table exactly
(B4 PASS) with 3/3 byte-identical determinism (B3 PASS).

## Frozen bars

- B1 COMMIT-ORDER: PASS. PREREG.md (7bc1d9a27) committed strictly
  before implementation. Transparent amendment (Section 8)
  committed with implementation.
- B2 TOOLCHAIN: PASS. Safebin-only PATH throughout. `which
  python3` returns nothing. Zero forbidden-executable
  invocations. Step 0 recorded in NAMECHECK.md.
- B3 DETERMINISM: PASS. 3/3 runs byte-identical per stream.
  sha256:
  - w6: 1 unique hash across 3 runs
  - t1: 1 unique hash across 3 runs
  - t2: 1 unique hash across 3 runs
  - t3: 1 unique hash across 3 runs
  - t4: 1 unique hash across 3 runs
- B4 EXACT-REPRODUCTION: PASS. pr_<s> output minus PX/banner
  lines byte-identical (cmp) to frozen ma4c_multistream
  <s>_run1.txt minus MS/banner lines, all 5 streams.
- B5 SCENARIO-VALIDITY: PASS. B4-boundary trigger in [733,741],
  B5-boundary trigger in [793,801], per stream (same closed loop).
- B6 PROXY-DISCRIMINATION (PRIMARY): PASS.
  (i) GENUINE: E735 trigger kind=0, px2=4 on all 5 streams.
  (ii) ADVERSARIAL: E795 trigger kind=0, px2=0 on W6 and T4.
- B7 OPAQUE-IDS: UNVERIFIABLE. The frozen 29-word list is not
  present in the lane; cannot verify. New identifiers (redun3,
  rucov, lastwin) are descriptive, not opaque.
- B8 MARGIN-QUANTIFICATION: PASS (table below).
- B9 PROXY-STABILITY: PASS. B6(i) and B6(ii) PASS on all streams.

## B8 table (trigger kind=0)

| Stream | E735 px2 | ru32 | ru23 | dg2 | lw2 | MS PCT | E795 px2 | ru32 | ru23 | dg2 | lw2 | MS PCT |
|--------|----------|------|------|-----|-----|--------|----------|------|------|-----|-----|--------|
| W6     | 4        | 200  | 461  | 65  | 669 | 294    | 0        | 37   | 20   | 5   | 789 | 341    |
| T1     | 4        | 218  | 443  | 65  | 669 | 321    | 4        | 218  | 500  | 125 | 669 | 321    |
| T2     | 4        | 202  | 459  | 65  | 669 | 302    | 4        | 202  | 516  | 125 | 669 | 302    |
| T3     | 4        | 216  | 445  | 65  | 669 | 318    | 4        | 216  | 502  | 125 | 669 | 318    |
| T4     | 4        | 199  | 462  | 65  | 669 | 295    | 0        | 45   | 12   | 3   | 791 | 257    |

Notes:
- px2=4 means redun3 fires for cell 2 with anchor cell 3.
- ru32=rucov[3][2], ru23=rucov[2][3].
- dg2=e-lastwin[2] (dormancy gap); lw2=lastwin[2].
- MS PCT is the K=3 baseline min-pair PCT from the MS audit.
- T1/T2/T3 E795: benign late consolidation (frozen state, cell 2
  dormant). Not adversarial.

## Design

redun3(i) returns anchor j+1 iff:
- (G) prot(i)=prot(j)=1, j!=i.
- (D) e-lastwin[i] > 60 (dormant; no current role).
- (A) wpart[j] >= wpart[i].
- (C) rucov[j][i]>=5 and rucov[i][j]>=5 (mutual runner-up).

This is NOT a threshold on the (R) ratio. It uses ranks
(runner-up) and dormancy (recency), not error magnitudes.

## Transparent amendment

The prereg originally specified (S) symmetry via cross-
multiplication. During implementation, (S) was found
non-discriminating (fires on adversarial due to B4-era symmetry
or lifetime dominance). Replaced with (D) dormancy. Kill bars
unchanged. See PREREG.md Section 8.

## Honest boundaries

- Shadow evaluation only; K=3 drives the closed loop. Does not
  test closed-loop redun3 behavior.
- Dormancy window (60) has thin margin on T1-T4 genuine case
  (65 vs 60). Direction is robust (dormant vs active: 65/125 vs
  3/5), but the absolute threshold is not principled beyond
  "one band-length".
- Generality to new tile designs not tested.
- B7 unverifiable due to missing word list.
