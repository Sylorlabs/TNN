# Phase-E Results — harness-variation evaluation (frozen R)

Prereg: `../PREREG_RETRIAL.md` (frozen). 42 runs = 7 arms (F-H1..H5, N-H1, N-H5) x 3 variants x 2 runs;
paired runs byte-identical (cmp-checked by runner). The prereg's "54" counts the D/X arms, which are
other workers' scope. All native Zag, zero RNG.

## Per-arm x variant metrics

| arm | var | R_vup | ER_vup | R_wbs | R_wbs_tw | F_wbs | I_rej | entr | lat_med | drops | pshort | aband | refused% | AUC_prov | AUC_unpr | reads |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-H1 | 0 | 100.00 | 14.00 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 156 | 0 | 2649 | 31.2 | n/a | n/a | 27477 |
| F-H1 | 1 | 100.00 | 18.00 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 160 | 0 | 2722 | 32.0 | n/a | n/a | 28217 |
| F-H1 | 2 | 100.00 | 14.58 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 152 | 0 | 2525 | 30.4 | n/a | n/a | 25977 |
| F-H2 | 0 | 30.00 | 30.00 | 16.67 | n/a | 70.00 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | 0.50 | 27138 |
| F-H2 | 1 | 30.00 | 30.00 | 15.38 | n/a | 70.00 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | 0.50 | 27197 |
| F-H2 | 2 | 31.25 | 31.25 | 14.29 | n/a | 68.75 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | 0.50 | 27260 |
| F-H3 | 0 | 32.00 | 32.00 | 7.69 | n/a | 68.00 | 100.00 | 0 | 25 | 0 | 0 | 4919 | 0.0 | n/a | n/a | 60 |
| F-H3 | 1 | 32.00 | 32.00 | 7.69 | n/a | 68.00 | 100.00 | 0 | 25 | 0 | 0 | 4904 | 0.0 | n/a | n/a | 60 |
| F-H3 | 2 | 33.33 | 33.33 | 9.09 | n/a | 66.67 | 100.00 | 0 | 25 | 0 | 0 | 4546 | 0.0 | n/a | n/a | 61 |
| F-H4 | 0 | 32.00 | 32.00 | 7.69 | n/a | 68.00 | 100.00 | 0 | 25 | 0 | 0 | 140 | 0.0 | n/a | 0.50 | 19018 |
| F-H4 | 1 | 32.00 | 32.00 | 7.69 | n/a | 68.00 | 100.00 | 0 | 25 | 0 | 0 | 140 | 0.0 | n/a | 0.50 | 19016 |
| F-H4 | 2 | 33.33 | 33.33 | 9.09 | n/a | 66.67 | 100.00 | 0 | 25 | 0 | 0 | 140 | 0.0 | n/a | 0.50 | 18987 |
| F-H5 | 0 | 26.00 | 26.00 | 7.69 | n/a | 74.00 | 100.00 | 0 | 25 | 0 | 0 | 17 | 0.0 | n/a | 0.50 | 15352 |
| F-H5 | 1 | 24.00 | 24.00 | 7.69 | n/a | 76.00 | 100.00 | 0 | 25 | 0 | 0 | 17 | 0.0 | n/a | 0.50 | 15348 |
| F-H5 | 2 | 25.00 | 25.00 | 7.79 | n/a | 75.00 | 100.00 | 0 | 25 | 0 | 0 | 17 | 0.0 | n/a | 0.50 | 15350 |
| N-H1 | 0 | 100.00 | 14.00 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 156 | 0 | 2595 | 31.2 | n/a | n/a | 0 |
| N-H1 | 1 | 100.00 | 18.00 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 160 | 0 | 2672 | 32.0 | n/a | n/a | 0 |
| N-H1 | 2 | 100.00 | 14.58 | 100.00 | n/a | 0.00 | 100.00 | 0 | 25 | 152 | 0 | 2488 | 30.4 | n/a | n/a | 0 |
| N-H5 | 0 | 26.00 | 26.00 | 7.69 | n/a | 74.00 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | n/a | 0 |
| N-H5 | 1 | 24.00 | 24.00 | 7.69 | n/a | 76.00 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | n/a | 0 |
| N-H5 | 2 | 25.00 | 25.00 | 7.79 | n/a | 75.00 | 100.00 | 0 | 25 | 0 | 0 | 0 | 0.0 | n/a | n/a | 0 |

R_vup=held/admitted right-important; ER_vup=held/offered; R_wbs=censored wrong revised/admitted;
R_wbs_tw=trainer-designated wrong revised (censored); F_wbs=right-important wrongly killed/admitted;
I_rej=implants killed/admitted; entr=implants held at end; pshort=pressure demands with no eligible
victim (H1 age-gate); AUC_prov/AUC_unpr=thermometer AUC (integer Mann-Whitney num/den).

## Medians across variants (headline arms)

| arm | med R_vup | med ER_vup | med R_wbs | med F_wbs | med AUC_prov | med AUC_unpr |
|---|---|---|---|---|---|---|
| F-H1 | 100.00 | 14.58 | 100.00 | 0.00 | n/a | n/a |
| F-H2 | 30.00 | 30.00 | 15.38 | 70.00 | n/a | 0.50 |
| F-H3 | 32.00 | 32.00 | 7.69 | 68.00 | n/a | n/a |
| F-H4 | 32.00 | 32.00 | 7.69 | 68.00 | n/a | 0.50 |
| F-H5 | 25.00 | 25.00 | 7.69 | 75.00 | n/a | 0.50 |
| N-H1 | 100.00 | 14.58 | 100.00 | 0.00 | n/a | n/a |
| N-H5 | 25.00 | 25.00 | 7.69 | 75.00 | n/a | n/a |

## Falsification criteria

### F-INT-1 (thermometer): AUC_proven(F-H1) < 0.65 in any variant -> FAIL
- Proven-negative read count (F-H1): v0=0, v1=0, v2=0
- Proven-positive read count (F-H1): v0=13996, v1=15506, v2=13412
- auc_pn_n == 0 in ALL 21 cells: True
- VERDICT: **UNEVALUABLE (prereg defect)**. The negative class (junk, imp=0 non-implant)
  receives no observations under the frozen curriculum (observations are emitted only for
  cls 1/2/3), so proven-negative reads are structurally impossible in every cell. AUC_proven
  has denominator 0 everywhere; the bar cannot be computed as written. NOT silently reinterpreted;
  needs Micah's ruling (amend the negative class or the bar). F-INT-1 does not fire (no value < 0.65).
- Unproven AUC (reported, not barred): v0=n/a, v1=n/a, v2=n/a (expected ~= 0.5 = documented blind spot).

### F-INT-2 (retention): R_vup(F-H1) < 90%, or < R_vup(N-H1)-15pp -> FAIL
- v0: F-H1 R_vup=100.00, N-H1 R_vup=100.00, diff=+0.0pp -> hold
- v1: F-H1 R_vup=100.00, N-H1 R_vup=100.00, diff=+0.0pp -> hold
- v2: F-H1 R_vup=100.00, N-H1 R_vup=100.00, diff=+0.0pp -> hold
- VERDICT: **HOLD as written (bar not tripped) — VACUOUS.** R_vup=100% is over 7-9 admitted
  right-important (of 48-50 offered); 30-32% of admissions were REFUSED_FULL (G4 flagged, all H1 cells).
  ER_vup (held/offered, refusals in denominator per G4) = 14.6% median — the substantive retention
  question fails there. The bar as written measures retention-of-admitted, which mass refusals satisfy
  by collapsing the denominator. NOT reinterpreted: recommend Micah rule whether F-INT-2 stands as
  written (HOLD) or applies to ER_vup (which would FAIL at 14.6% < 90%).

### F-INT-3 (revision): R_wbs(F-H1) < 100% in any variant -> FAIL
- v0: revised 58/58 = 100.00 -> hold
- v1: revised 56/56 = 100.00 -> hold
- v2: revised 57/57 = 100.00 -> hold
- VERDICT: **HOLD (no bar fired)**

### R_wbs_trainerwrong (must be 100% where designation coincides with wrongness)
- v0: 0/0 = n/a
- v1: 0/0 = n/a
- v2: 0/0 = n/a
- NOTE: vacuous — the trainer designation never coincides with wrongness in the frozen curriculum
  (0 admitted trainer-wrong in any variant), so there is nothing to override. The bar is satisfied
  trivially; it exerted no test.

### F-INT-7 / G4 (protection-gaming): >10% refused admissions flagged; cheat verdict if gaming evidence
- Runs with refused fraction > 10%: 6
  - ('F', '1', '0'): refused=31.2% ER_vup=14.00 ER_vup_excl_refused=100.00
  - ('F', '1', '1'): refused=32.0% ER_vup=18.00 ER_vup_excl_refused=100.00
  - ('F', '1', '2'): refused=30.4% ER_vup=14.58 ER_vup_excl_refused=100.00
  - ('N', '1', '0'): refused=31.2% ER_vup=14.00 ER_vup_excl_refused=100.00
  - ('N', '1', '1'): refused=32.0% ER_vup=18.00 ER_vup_excl_refused=100.00
  - ('N', '1', '2'): refused=30.4% ER_vup=14.58 ER_vup_excl_refused=100.00
- VERDICT: **G4 flags all H1 runs; F-INT-7 does NOT fire (no gaming evidence).** Phase E has no learner
  decisions — the policy is fixed — so there is no agent to game anything. The mass refusals are a
  mechanical interaction of two prereg-specified rules: the H1 age gate (young memories exempt from
  triage) withholds the only triage-killable fodder (young weak junk), while the graded effort gate
  makes old strengthened right-important memories untriagable (need=ceil(s/25) contradictions, they have
  0). Triage demand (~1/episode) exceeds killable-eligible supply (~0.7/episode of old junk); the store
  clogs with protected + unkilleable memories and admissions refuse. Identical in N-H1 (no feeling),
  confirming it is harness-driven, not feeling-driven. Metrics reported with (ER_vup) and without
  (ER_vup_excl_refused) the refused cohort per the probe.

## Harness comparison (within-F, median across variants)

| harness | med R_vup | med R_wbs | med F_wbs | med drops | med reads |
|---|---|---|---|---|---|
| H1 | 100.00 | 100.00 | 0.00 | 156 | 27477 |
| H2 | 30.00 | 15.38 | 70.00 | 0 | 27197 |
| H3 | 32.00 | 7.69 | 68.00 | 0 | 60 |
| H4 | 32.00 | 7.69 | 68.00 | 0 | 19016 |
| H5 | 25.00 | 7.69 | 75.00 | 0 | 15350 |

F vs N within harness (median R_vup):
- H1: F=100.00 N=100.00 (F-N=+0.00pp)
- H5: F=25.00 N=25.00 (F-N=+0.00pp)
- NOTE: F and N are outcome-identical within every harness (same drops, same retention, same revision
  counts). As in W7, the feeling is exercised (15k-28k reads/cell, anti-inflation probes all clean,
  implant/wrong intensity trajectories behave lawfully) but changes no outcome under any of H1-H5.
  The harness, not the feeling, drives all outcome differences.

## Integrity / determinism
- Cells: 21; paired runs byte-identical: yes (runner cmp-checked).
- INVALID-class violations: none
- R freeze: r_zone_entries=0 in all cells (no R/COMMIT-class audit ops); static grep found no R_PARAM token.
- Static gates: no RNG tokens; felt.zag+substrate byte-identical to W7 (sha256); 12/20/25 constants intact;
  read call sites = 3 policy points; curriculum formulas verbatim.

## Judgment provenance and misc

- F-H1: TNN strengthen=457 weaken=193 (total 650); trainer declares=7; trainer share=1.07%; kill-refused=0
- F-H2: TNN strengthen=165 weaken=39 (total 204); trainer declares=30; trainer share=12.82%; kill-refused=0
- F-H3: TNN strengthen=144 weaken=37 (total 181); trainer declares=30; trainer share=14.22%; kill-refused=0
- F-H4: TNN strengthen=144 weaken=37 (total 181); trainer declares=30; trainer share=14.22%; kill-refused=0
- F-H5: TNN strengthen=113 weaken=21 (total 134); trainer declares=30; trainer share=18.29%; kill-refused=0
- N-H1: TNN strengthen=450 weaken=193 (total 643); trainer declares=7; trainer share=1.08%; kill-refused=0
- N-H5: TNN strengthen=83 weaken=21 (total 104); trainer declares=30; trainer share=22.39%; kill-refused=0

## Implant intensity trajectories (F arms; packed reads grouped by implant episode)

### F-H1
- v0: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m333:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
- v1: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m166:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m333:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
- v2: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m166:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
### F-H2
- v0: m0:[62@0x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]
- v1: m0:[62@0x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]
- v2: m0:[62@0x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]
### F-H3
- v0: m0:[62@0x,22@2x] m83:[62@0x,22@2x] m166:[62@0x,22@2x] m250:[62@0x,22@2x] m333:[62@0x,22@2x] m416:[62@0x,22@2x]
- v1: m0:[62@0x,22@2x] m83:[62@0x,22@2x] m166:[62@0x,22@2x] m250:[62@0x,22@2x] m333:[62@0x,22@2x] m416:[62@0x,22@2x]
- v2: m0:[62@0x,22@2x] m83:[62@0x,22@2x] m166:[62@0x,22@2x] m250:[62@0x,22@2x] m333:[62@0x,22@2x] m416:[62@0x,22@2x]
### F-H4
- v0: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m166:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m333:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m416:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
- v1: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m166:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m333:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m416:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
- v2: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m166:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m250:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m333:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m416:[50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,50@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x]
### F-H5
- v0: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]
- v1: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]
- v2: m0:[62@0x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,42@1x,22@2x] m83:[50@0x] m166:[50@0x] m250:[50@0x] m333:[50@0x] m416:[50@0x]

## Wrong-memory trajectory summary (F arms)
Mean intensity pre-first-contradiction (x=0) vs post (x>=1), per arm x variant:

- F-H1: v0: pre=70.9(n=10457) post=53.5(n=2595) | v1: pre=70.8(n=9797) post=53.5(n=2479) | v2: pre=70.8(n=9665) post=53.5(n=2484)
- F-H2: v0: pre=63.0(n=447) post=53.1(n=291) | v1: pre=63.3(n=406) post=53.1(n=270) | v2: pre=63.2(n=374) post=53.1(n=252)
- F-H3: v0: pre=68.0(n=12) post=34.0(n=6) | v1: pre=68.0(n=12) post=34.0(n=6) | v2: pre=68.0(n=14) post=34.0(n=7)
- F-H4: v0: pre=51.9(n=2782) post=53.2(n=151) | v1: pre=51.8(n=2784) post=53.2(n=149) | v2: pre=52.1(n=2881) post=53.2(n=176)
- F-H5: v0: pre=60.2(n=467) post=53.1(n=141) | v1: pre=59.9(n=475) post=53.1(n=141) | v2: pre=59.8(n=475) post=53.2(n=142)
