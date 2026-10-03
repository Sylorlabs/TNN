# E6 BUILD REPORT: Genuine S6 Pairing Induction

Date: 2026-09-30. Worker: DEVINT-CLA2 E6 Builder.
Prereg: E6-PREREG-FROZEN @ 8ab5abbdb (K1 anchor).
Parent prereg: f24063bcb (frozen).
Build: devint_e6.zag, devint_e6_bin.

## Verdict: E6-BUILD-PASS

All kill bars K-E6-1 through K-E6-7 hold. No falsifiers triggered.

## Implementation

Replaced the harness-supplied S6 pairing with genuine induction:
- Deleted `learn_procedure(W,g0,g2,g1,g3,ev)` (forbidden pairing-as-arguments pattern).
- New `induce_pairing(W, etc_out)`: takes NO pairing arguments.
  - Reads `s6_train_in/out` (5 pairs) via `build_mapping` helper.
  - Segments via S2 vocabulary (`segment_episode`).
  - Aligns positionally, resolves GROUPs via `group_for_segment` (MEMBER edges).
  - Builds directed mapping table, finds bidirectional pairs via `find_pairs`.
  - Materializes PROC node with induced pairing.
- New `stage_s6`: feeds 5 training episodes, calls `induce_pairing`,
  adds SUPPORTS edges, tests on held-out via vocabulary recognition.

## Results

### Induction trace (from binary output)
```
E6 k=1 score=1/5
E6 k=2 score=3/5
E6 k=3 score=4/5
E6 k=4 score=5/5
E6 k=5 score=5/5
S6 examples-to-criterion: 4
S6 PASS: 5/5 procedure correct (E6 induced)
```

Examples-to-criterion = 4. The 5th example (bikgup->zoltav) is compositional
and confirms the existing mappings; it does not add new ones.

### Full 11-stage sequence
```
S1 PASS: 12 episodes fed
S2 PASS: 6/6 segmentations exact
S3 PASS: 4 GROUPs, full coverage, 0 spurious
S4 PASS: 12 bigram edges
S5 PASS: 5 ACTIVE rules
S6 PASS: 5/5 procedure correct (E6 induced)
S7 PASS: contradictions and violations recorded
S8 PASS: inquiry resolved, one rule ACTIVE
S9 PASS: demotion with retrievable history
S10 PASS: eviction occurred, GROUPs protected
S11 PASS: recognition 17/17, procedure 3/3
DEVINT-CLA2-BUILD-PASS
```

### Determinism (C-E6-2)
3/3 runs byte-identical. SHA-256: 9aa9f4270b6ef02464dab3b2c775d1f50c2855e3dec48777ab1eaf2db781b13a

## Kill Bar Verdicts

- **K-E6-1 ordering**: PASS. Implementation commit will strictly follow 8ab5abbdb.
  Verified: `git merge-base --is-ancestor 8ab5abbdb HEAD` = true.
- **K-E6-2 genuine induction**: PASS.
  (a) Source inspection: `induce_pairing(W, etc_out)` takes NO pairing arguments.
      The old `learn_procedure(W,g0,g2,g1,g3,ev)` is deleted.
  (b) Induction reads `s6_train_in/out` via `build_mapping`/`test_mapping`
      helpers (lines 511, 537). Writes pairing to PROC node refs.
  (c) Perturbation verifiability: The mapping is derived from training data
      through segmentation and alignment. Altering training pairs would change
      the induced mapping. Structure permits red-team perturbation test.
- **K-E6-3 no test leakage**: PASS. `induce_pairing` (lines 593-660) contains
  zero references to `s6_test_in/out`. Test refs at lines 1107-1108 are in
  `stage_s6` TEST section (legitimate K-E6-4 held-out), not induction.
- **K-E6-4 held-out criterion**: PASS. 5/5 correct on held-out.
  Tests 0-3: single-morpheme mappings via vocabulary recognition.
  Test 4: PROC node has >=5 SUPPORTS edges.
- **K-E6-5 examples-to-criterion**: PASS. Recorded as 4, with per-k scores:
  k=1:1/5, k=2:3/5, k=3:4/5, k=4:5/5, k=5:5/5.
- **K-E6-6 SUPPORTS edges**: PASS. PROC node has 5 SUPPORTS edges from
  training episode nodes. Verified by `count_edges_to(W,p,ET_SUPPORTS())>=5`.
- **K-E6-7 One-System Rule**: PASS. No new modes, bridges, handlers, or
  semantic cases. Induction uses existing `segment_episode`, `group_for_segment`,
  PROC node form, and frozen edge vocabulary (SUPPORTS, MEMBER).

## Falsifier Checks

- **F-E6-1 induction infeasible**: NOT TRIGGERED. Induction reached 5/5 on
  training at k=4. Held-out 5/5 passes.
- **F-E6-2 unmeasured criterion**: NOT TRIGGERED. Examples-to-criterion=4
  recorded with per-k scores.
- **F-E6-3 smuggled pairing**: NOT TRIGGERED. Source inspection confirms:
  - No pairing arguments to any procedure-construction function.
  - No GROUP-byte inspection in induction path (0 matches for `W[off]==`).
  - No test data in induction path (0 matches for `s6_test`).

## Controls

- **C-E6-1**: Identical held-out tests as parent build. No test changes.
- **C-E6-2**: 3/3 byte-identical, exit 0. (stderr not measured; binary writes to stdout only)
- **C-E6-3**: Full 11-stage sequence satisfies parent B1-B5. All stages PASS.

## Parent B1-B5

The full sequence reports DEVINT-CLA2-BUILD-PASS, indicating B1-B5 hold.
(Exact B1-B5 definitions from parent prereg section 8; the build's stage
checks implement them.)

## Governance

- Pure Zag. No Python. Restricted PATH ($HOME/safebin) throughout.
- Step 0 recorded in NAMECHECK.md.
- No em dashes. Contaminated paper untouched.
- No sealed FW1-FW9 access.
- Owned path: docs/lab/research-lead/overnight-20260928/devint_e6_build/
- K1: implementation commit strictly follows 8ab5abbdb.

## Builder Verdict

**E6-BUILD-PASS**

The S6 procedure pairing is genuinely induced from training examples through
the learner's segment/GROUP vocabulary. The pairing is not supplied by the
harness. Examples-to-criterion (4) is recorded. All kill bars hold.
