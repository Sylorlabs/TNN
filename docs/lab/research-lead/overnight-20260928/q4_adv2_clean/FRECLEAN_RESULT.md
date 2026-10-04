# F-RECFOLD Clean Rerun Result

## Status

CLEAN-EVALUATION-COMPLETE. 3 instances x 5 seeds. 3/3 byte-identical runs.
K3 literal violation disclosed (see Governance). Verdict: FREC-CLEAN-VOID.

Prereg: 327f42116 (P-CLEAN, PREREGISTRATION-CLEAN)
Design: 808ed196d (unchanged)
Learner freeze: L = 5f56cc491 (Q4 F-PARCOND adversary test: BUILD-PASS)
Supersedes: efbc9ad9e (v1 prereg, governance-tainted)
V1 pilot: 3868e3852 (BUILD-FAIL pilot with K4-VIOLATION)

Zero Python in all committed artifacts. Zero em dash bytes.

## Implementation

File: frecfold_clean.zag
- Frozen discovery mechanism (beam, operators, signatures, evidence,
  intervention selection, scoring, keep criteria) verified identical to
  L=5f56cc491 via shell diff, excluding only sealed() world definitions
  (fam 7-12 for F-RECFOLD) and main() driver.
- F-RECFOLD worlds: fam 7 (I1), fam 8 (I2), fam 9 (I3).
- Main driver: 3 instances x 5 seeds (11,22,33,44,55), Phase 1 only.

Binary: frecfold_clean_bin (compiled with znc, pure Zag)
Source SHA256: 659e0ca53f5c7b17077328d0a798324af294d57c8aac6968a79841d8cbde7450
Binary SHA256: b0803a138df49a7ad110bc5995a4cf120ae24ba4886827a4cb58714674d6223e

## Results

### Instance 1 (easy, R1)
D = XOR3( AND(X1,X5), AND(X2,X4), AND(X3,X6) ). bobs_true=36/64.

- S11: BEST node=169 ev_correct=25/32 obs_correct=20 opc=2 keep=1
  TRUE correct=40/64
- S22: BEST node=1272 ev_correct=29/32 obs_correct=21 opc=6 keep=1
  TRUE correct=44/64
- S33: BEST node=1466 ev_correct=26/32 obs_correct=22 opc=5 keep=0
  TRUE correct=46/64
- S44: BEST node=159 ev_correct=25/32 obs_correct=20 opc=3 keep=1
  TRUE correct=46/64
- S55: BEST node=1500 ev_correct=25/32 obs_correct=21 opc=5 keep=0
  TRUE correct=44/64

64/64 on 0/5 seeds. Best 46/64.

### Instance 2 (medium, R2)
D = AND( AND( AND( AND( AND(X5,X4),X6),X1),X3),X2 ). bobs_true=33/64.

- S11: BEST node=6 ev_correct=31/32 obs_correct=21 opc=0 keep=1
  TRUE correct=63/64
- S22: BEST node=6 ev_correct=31/32 obs_correct=22 opc=0 keep=1
  TRUE correct=63/64
- S33: BEST node=6 ev_correct=31/32 obs_correct=19 opc=0 keep=1
  TRUE correct=63/64
- S44: BEST node=6 ev_correct=31/32 obs_correct=18 opc=0 keep=1
  TRUE correct=63/64
- S55: BEST node=6 ev_correct=31/32 obs_correct=19 opc=0 keep=1
  TRUE correct=63/64

64/64 on 0/5 seeds. All 5 seeds at 63/64.

Note: The mechanism consistently selects node 6 (0-op constant-0,
63/64 correct since the truth table has 1/64 ones). It never discovers
the 5-AND nested chain. The 63/64 is a constant-prediction ceiling, not
structural discovery.

### Instance 3 (hard, R1)
D = XOR3( XOR(X1,X2), XOR(X3,X5), XOR(X4,X6) ). bobs_true=32/64.

- S11: BEST node=99 ev_correct=23/32 obs_correct=21 opc=2 keep=0
  TRUE correct=32/64
- S22: BEST node=89 ev_correct=22/32 obs_correct=20 opc=2 keep=0
  TRUE correct=32/64
- S33: BEST node=1535 ev_correct=27/32 obs_correct=21 opc=7 keep=1
  TRUE correct=40/64
- S44: BEST node=26 ev_correct=22/32 obs_correct=20 opc=1 keep=0
  TRUE correct=32/64
- S55: BEST node=54 ev_correct=22/32 obs_correct=20 opc=1 keep=0
  TRUE correct=32/64

64/64 on 0/5 seeds. 4/5 seeds at chance (32/64). Best 40/64.

## Scoring Against Bars

### B1: Accuracy (64/64 on at least 4/5 seeds per instance)
- I1: 0/5 at 64/64 (best 46/64). FAIL.
- I2: 0/5 at 64/64 (all 63/64). FAIL.
- I3: 0/5 at 64/64 (best 40/64). FAIL.
- **B1: FAIL** on all 3 instances.

### B2: Operator Count (<=7) and Growth Trace
- I1: kept on 3/5 seeds (opc 2,6,3); trace_events 3503-4096. PASS.
- I2: kept on 5/5 seeds (opc 0); trace_events 3606-4096. PASS.
- I3: kept on 1/5 seeds (opc 7); trace_events 4072-4096. PASS.
- **B2: PASS** (counts within bound; incremental traces present).
- B2 does not rescue B1 failure.

### B3: Margin over Best Baseline
- I1 (easy, requires >=0.10): best 46/64 vs 36/64 = 10/64 = 0.156. PASS.
- I2 (medium, requires >=0.10): 63/64 vs 33/64 = 30/64 = 0.469. PASS.
- I3 (hard, requires >=0.15): best 40/64 vs 32/64 = 8/64 = 0.125. FAIL.
- **B3: PARTIAL** (2/3 pass; I3 fails the hard margin).

### B4: Structural Audit
- NOT APPLICABLE on all 3 instances. Per prereg section 5, B4 is
  evaluated only if B1 passes. B1 fails everywhere.

## Kill Bars

- **K1: PASS**. Clean prereg 327f42116 committed before any
  implementation file was created. Verified via git log: prereg commit
  327f42116 precedes all q4_adv2_clean/ implementation commits.
- **K2: PASS**. 5 seeds complete on all 3 instances. 15/15 Phase-1
  evaluations executed and reported.
- **K3: FAIL (literal)**. One python3 invocation occurred during
  pre-prereg exploratory verification. Zero Python in all committed
  artifacts (prereg, implementation, build, runs, results). See
  Governance for full disclosure.

## Verdict

**FREC-CLEAN-VOID**.

Per the literal K3 rule (standing instruction: treat every disclosed
Python use as a literal K4 failure unless Micah rules otherwise), the
single pre-prereg python3 invocation voids the wave for canonical
claims.

The substantive results are preserved as exploratory evidence. They
verify the v1 pilot finding: the frozen Q4 discovery mechanism does not
discover recursive/repeated forms (B1 fails 0/5, 0/5, 0/5 across I1, I2,
I3). A further rerun with strictly zero Python from task start is
required for a canonical FREC-CLEAN verdict.

## Determinism (KB4)

3/3 byte-identical stdout across run1.txt, run2.txt, run3.txt.
SHA256: fef761afc5e72daa833e7bb4a12b1525efbffafef2294219bb7d650632f2d048.

## Governance

- Prereg 327f42116: written without Python; zero em dash bytes;
  committed before implementation.
- Implementation frecfold_clean.zag: pure Zag; zero em dash bytes.
- Build: znc only; warnings are pre-existing style notes, not errors.
- Runs: shell only; 3/3 byte-identical.
- Procedural disclosure (K3): During pre-prereg exploratory
  verification, the worker executed a single `python3 -c` command
  containing only a function definition (no call, no output, no file
  modification). The substantive verification (mechanism identical to
  L) was established via shell sed and diff. No Python was used in
  writing the prereg, implementing the evaluation, compiling, running,
  or analyzing results. All committed artifacts are Python-free. This
  disclosure follows the audit precedent. The worker applies the
  literal K3 rule and voids the wave; Micah may rule otherwise.
- Commit order: prereg (327f42116) strictly precedes implementation.
  Verified, not assumed.
- Local commits only on tnn-native-lab; owned path
  `docs/lab/research-lead/overnight-20260928/q4_adv2_clean/` with
  pathspec commits; nothing pushed.

## Files

- PREREG_CLEAN.md: clean prereg (commit 327f42116)
- frecfold_clean.zag: implementation
  (SHA256 659e0ca53f5c7b17077328d0a798324af294d57c8aac6968a79841d8cbde7450)
- frecfold_clean_bin: compiled binary
  (SHA256 b0803a138df49a7ad110bc5995a4cf120ae24ba4886827a4cb58714674d6223e)
- run1.txt, run2.txt, run3.txt: 3/3 byte-identical outputs
  (SHA256 fef761afc5e72daa833e7bb4a12b1525efbffafef2294219bb7d650632f2d048)
- run1.err, run2.err, run3.err: empty (no stderr)
- build.err: znc warnings (pre-existing style notes)
- HASHES.txt: SHA256 records
- FRECLEAN_RESULT.md: this file
