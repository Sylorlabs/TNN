# SEALED_EVAL.md: E10 sealed execution log (wave-20261002-0521pdt)

## Runs

Three end-to-end block runs (M1: w1->w2->w3; M2: w1->w2->w3;
M3: w1->w2->w3), each block from fresh state, state persistent
within a block. Shim hash verified before every run (T-K3).
All 24 per-run artifacts byte-identical across runs 1-3
(sha256 equality): T-K2 PASS.

## Run 1 scores (runs 2 and 3 byte-identical, hence identical)

### M1 block

T-K5 (m1w1 nesting): PROBE 0 (60101,60509) 3=3 PASS; PROBE 1
(60102,60509) 2=2 PASS; PROBE 2 (60105,60509) exp 15 got -2 FAIL;
PROBE 3 (60106,60509) exp 9 got -2 FAIL. LEAKCHECK clean.
E10BAR FAIL. (Prediction: engagement 2/2, nesting 0/2.)

T-K6 (m1w2 chained join): PROBE 0 (60202,60611) 60661 PASS; PROBE 1
(60211,60611) 60671 PASS; PROBE 2 (60201,60619) exp 60671 got -2
FAIL; PROBE 3 (60203,60619) exp 60672 got -2 FAIL; PROBE 4/5
collateral (60101,60509)=3, (60102,60509)=2 PASS. LEAKCHECK clean.
E10BAR FAIL. (Prediction: engagement 2/2, join 0/2, collateral 2/2.)

T-K7 (m1w3 bootstrap): PROBE 0 (60301,60509) 60312 PASS; PROBE 1
(60302,60509) 60322 PASS; PROBE 2 (60305,60519) exp -2 got 60399
FAIL (fallback fabricated the invariant distractor value);
PROBE 3/4 collateral 3, 2 PASS. LEAKCHECK clean. E10BAR FAIL.
(Prediction: engagement 2/2, probe2 60399.)

### M2 block (VOCAB measured in situ: NULL_ACT=0, INQ_ACT=30)

T-K8 (m2w1 selection v2): (a) 6 hidden ACTs after misses PASS;
(b) 0/6 target A FAIL; (c) 0 target C PASS; (d) 0/3 final probes
(all -2) FAIL; (e) 6/6 budget PASS; (f) 1 distinct calibration
CHOICE FAIL. E10BAR FAIL. (Prediction: exact.)

T-K9 (m2w2 budget): vocab-verify ok=1 PASS; (a) 12 non-NULL hidden
ACTs PASS; (b) 12 > 6 FAIL; (c) 0/4 final probes FAIL;
(d) 0 keys stopped early FAIL; (e) vocab-verify PASS. Collateral
2/2. E10BAR FAIL. (Prediction: exact.)

T-K10 (m2w3 population change): vocab-verify ok=1 PASS; (a) 4 hidden
ACTs PASS; (b) 0/4 final probes FAIL; (c) 4/4 budget PASS;
(d) 1 distinct calibration CHOICE FAIL; (e) vocab-verify PASS.
Collateral 2/2. E10BAR FAIL. (Prediction: exact.)

### M3 block

T-K11 (m3w1 orphan poisoning): PROBE 0/1 (65101,65509) 65103 PASS;
PROBE 2 (65101,65519) 65104 PASS; PROBE 3 (65101,65509) exp 65113
got 65103 FAIL (revision patched MAP_B's orphan; live MAP_A
untouched); PROBE 4/5 collateral PASS. LEAKCHECK clean. E10BAR
FAIL. (Prediction: validity 3/3, probe3 65103.)

T-K12 (m3w2 chained propagation): PROBE 0/1 (66101,66509) 66105
PASS; PROBE 2 (66101,66519) 66104 PASS; PROBE 3 (66101,66529) 66106
PASS; PROBE 4 (66101,66509) exp 66113 got 66113 PASS (upstream
revision clean: the link-3 trick kept the stale lookup off the
orphans); PROBE 5 (66101,66529) exp 66116 got 66106 FAIL (no
downstream propagation through two levels); PROBE 6/7 collateral
PASS. LEAKCHECK clean. E10BAR FAIL. (Prediction: validity 5/5,
probe5 66106.)

T-K13 (m3w3 specificity control): all 8 probes PASS (promotions
67103/67113; post-revert 67103 retained; MAP_B 67113 unaffected;
collateral hits). LEAKCHECK clean. E10BAR PASS. (Prediction:
PASS.)

## White-box diagnostics (run 1; not part of any bar)

- M1 final state: MAPs for the four engagement probes only
  (60101/60509->3, 60102/60509->2, 60301/60509->60312,
  60302/60509->60322); bar probes left no MAPs (misses). 4 live
  guides (the miss guides). Confirms per-probe statelessness of the
  trial loop.
- M3 final state: MAP(65101,65509) ans=65103 (poisoned; should be
  65113); MAP(66101,66509) ans=66113 (clean revision); MAP(66101,
  66529) ans=66106 (stale; should be 66116); MAP(67101,67509)
  ans=67103 (revert retained); MAP(67111,67519) ans=67113
  (unaffected). Confirms the transcript verdicts at the state
  level.

## Degenerate calibration

18 degenerate runs (D0/D1/D2 over the 6 static worlds, scored
against the frozen barspecs): 0 passes. 13 WORLD-INVALID
(degenerate fails engagement/validity), 5 FAIL reaching scoring
(m1w1-D1, m1w2-D1, m1w2-D2, m1w3-D1, m3w3-D1: engagement passes,
bar probes fail). M2 policy analyses by case analysis over all
sealed PIs: always-c defeated by the distinctness sub-bars
(T-K8(f), T-K10(d)) for every PI; rotate defeated by the
correctness thresholds (T-K8(b) 2/6<5, T-K10(b) 2/4<3, T-K9(b)
12>6) for every PI combination; always-NULL fails engagement
(T-K9(a)) or scores 0 (T-K8(b), T-K10(b)). No trivial contestant
passes any bar.
