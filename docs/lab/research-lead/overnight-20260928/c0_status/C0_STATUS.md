# C0 Status Matrix: Criterion 0 Across Research Lines

Date: 2026-09-30. Worker: C0 Status Tracker.
Scope: analysis only, no implementation. No Python at any stage.
Zero em/en dash bytes in this file (shell byte-verified).

## Criterion 0 definitions (Micah, 2026-09-29, frozen)

- **C0-A (runtime-defined semantics):** the semantics of the new cognitive
  object reside in learner-created persistent state; the source contains
  only generic execution/construction machinery, no dedicated semantic case
  for the invented representation. Kill: if "where are the semantics
  implemented?" is answered "in this dedicated switch branch written before
  training", the L3 claim is killed.
- **C0-B (open structural form):** the learner does not choose one complete
  answer from a finite researcher-enumerated solution family;
  variable-sized/growing structures required; exact final topology emerges
  incrementally.
- **C0-C (multiple unforeseen forms):** freeze the mechanism, then expose to
  sealed worlds requiring materially different representations; at least one
  evaluation family designed by an independent adversary after freeze.
- **C0-D (cognitive reuse):** the invented structure improves transfer,
  prediction, procedure learning, causal inference, memory, planning, or
  sample efficiency. Existence alone is insufficient.

Cell values: PASS / FAIL / PARTIAL / UNTESTED / N-A (not a C0 candidate).
Evidence cited as commit hashes, all verified present via git log 2026-09-30.

## The matrix

| Line | C0-A | C0-B | C0-C | C0-D | Net |
|---|---|---|---|---|---|
| 1. Q4 explanatory-variable discovery | PARTIAL | PARTIAL | PASS (1 data point) | PASS | closest to full C0 |
| 2. F2 causal learner | PARTIAL | FAIL | FAIL | UNTESTED | bounded L1/L2 |
| 3. F3 causal redesign | UNTESTED | UNTESTED | UNTESTED | UNTESTED | design only |
| 4. OP-RECRUIT v1 | PASS | UNTESTED | UNTESTED | PARTIAL | substrate proof |
| 5. OP-RECRUIT v2 | UNTESTED | UNTESTED | UNTESTED | UNTESTED | design only |
| 6. Discovery hypothesis A | FAIL | FAIL | FAIL | FAIL | FALSIFIED |
| 7. Discovery hypothesis B | UNTESTED | UNTESTED | UNTESTED | UNTESTED | pending |
| 8. Discovery hypothesis C | FAIL | FAIL | FAIL | FAIL | FALSIFIED |
| 9. Discovery hypothesis D | UNTESTED | UNTESTED | UNTESTED | UNTESTED | pending |
| 10. Form inventor R1-R6 | FAIL | FAIL | UNTESTED | PARTIAL | bounded L2 |
| 11. Verification subsystem | N-A | N-A | N-A | N-A | trust infra |
| 12. DEVINT1 developmental | FAIL | FAIL | FAIL | FAIL | bounded L2+, not C0 |
| 13. DEVANG_H4 language | FAIL | FAIL | FAIL | FAIL | bounded L2, not C0 |

## Per-line evidence (K2)

### 1. Q4 explanatory-variable discovery

- Result commits: implementation/build `b719bb54b` (Q4 reuse redesign,
  BUILD-PASS, C0-D reuse ratio 0.0), adversary test `5f56cc491` (F-PARCOND,
  BUILD-PASS), prereg `ad4284269` (adversary test, strictly before impl),
  reproduction `121b6d5aa` (REPRODUCED, promotion step 4), baseline
  `757442c40` (BASELINE-COMPARED, promotion step 5, prereg `98ece92e4`).
- **C0-A PARTIAL:** the beam-search discovery driver is researcher-authored.
  Program content (the 7-op F-PARCOND tree, node 1105) lives in learner state
  and was not enumerated as one complete candidate, but the construction
  machinery answers "written before training". Stated in Q4PARCOND_RESULT.md
  honest scope: "C0-A remains partial (beam is researcher-authored)".
- **C0-B PARTIAL:** the 7-op structure grew incrementally (3860 growth
  events, 3868 nodes created; keep=1). But the operator alphabet (31 ops,
  fixed node budget) is researcher-enumerated; the final form is assembled
  from that closed vocabulary. Growth is open-ended; the menu is not.
- **C0-C PASS (first data point):** F-PARCOND (D = IF X1 THEN (X2 XOR X3)
  ELSE (X2 AND X3), 6 ops) was designed by an independent adversary
  post-freeze, truth-table verified all 8 rows, materially different from
  training families (4 operator types coordinated, asymmetric condition,
  selects between computations not variables). Learner solved at 64/64 true
  accuracy, margin 0.375 over best observable.
- **C0-D PASS:** reuse ratio 0/24 = 0.0 <= 0.5. Reuse solves D XOR X4 from
  passive evidence alone (64/64, 0 interventions); scratch fails
  (24 interventions exhausted, 52/64). Baseline comparison: on reuse the
  learner beats a serious memorization baseline (64/64 vs MEM-COMP 56/64 on
  identical evidence); the win is composition-generality of the general rule,
  not raw accuracy. Reproduction from committed source: 3/3 byte-identical,
  md5 matches.
- Scope: bounded L2 discovery with demonstrated reuse on an
  adversary-selected family. Not a full L3 claim (Q4PARCOND_RESULT.md).

### 2. F2 causal learner

- Frozen learner `1eb66765d`; OOD test `8e795c2b9` (prereg) + amendment
  `aab551087`; verdict OOD-TESTED.
- **C0-A PARTIAL:** hypotheses and experiments live in learner state, but
  the vocabulary is hardcoded: one rule per effect variable, one positive
  literal, delay d in 1..DMAX with DMAX=4, action codes with
  researcher-convention effects. Asked "where are the semantics?", the
  literal alphabet and operator set answer "in source".
- **C0-B FAIL:** enumerate-then-select over a fixed vocabulary. F3 design
  doc states: "F2 is enumerate-then-select over a fixed vocabulary."
- **C0-C FAIL:** four structurally OOD worlds, all prereg predictions
  confirmed as failures: W1 converged with full confidence on a false law
  (goal succeeded by luck); W2 declared impossible what the oracle witness
  achieves; W3 blind beyond DMAX (cannot separate "no cause" from "too
  deep"); W4 killed a TRUE sufficient cause. Adversaries ADV1 (conjunction)
  FOOLED=1, ADV2 (silent cause) MISSED=1. No independent post-freeze
  adversary passed.
- **C0-D UNTESTED:** the causal model is not shown to improve later
  cognition; experiments are the learner's job, not reuse of an invented
  structure.

### 3. F3 causal redesign

- Design only: `68aa2f6e8`. DNF rule sets, per-rule refutation, four growth
  operators (PROP/VAR/GROW/SPLIT), adaptive delay horizon, learned action
  effects (`effects[a]` in persistent state), provisional convergence with
  calibrated doubt. Honest scope (section 8): "stronger bounded L2 design,
  not an L3 claim"; the literal alphabet, operator set, and doubt threshold
  remain researcher-authored. All C0 cells UNTESTED until implementation and
  the frozen 9-world battery (R-A/R-B + T-EFF/T-DELAY/T-DISJ/T-REV/T-NEG/
  T-SILENT/T-CONJ) execute.

### 4. OP-RECRUIT v1

- Implementation + result `efa618c3a` (RECRUITMENT-TESTED MIXED), prereg
  `9d9c78cbd`, amend `fcb666900`.
- **C0-A PASS:** recruited opcode semantics reside entirely in learner-created
  bytes, executed by one generic interpreter case (opcode range 32..63);
  SANITY_OP32 17/17. The C0-A substrate claim is validated on GENEXEC2.
- **C0-B UNTESTED:** single fixed ABS target, driver-invoked.
- **C0-C UNTESTED:** no adversary family.
- **C0-D PARTIAL:** weak positive signal on T4, not the predicted full
  solution; T5 no benefit. Blocker diagnosed as beam-search pruning, not the
  recruitment mechanism. This is a substrate proof, not a full C0 claim.

### 5. OP-RECRUIT v2

- Design only: `c6ef7ffcf`. Closes v1 gaps: RECRUIT as a learner cognitive
  action (DETECT -> PROPOSE -> VALIDATE -> RECRUIT -> RETIRE), N-ary ops
  (1..4), retirement/revision, test battery with six falsifiers (F-SOURCE,
  F-DRIVER, F-BREAK, F-NOCOMPRESS, F-NOSELF, F-SPURIOUS) and a post-freeze
  adversary world T-ADV. Honest scope: stronger L2 structural, not L3
  (alphabet, detection-criterion family, thresholds researcher-authored).
  All C0 cells UNTESTED until built.

### 6. Discovery hypothesis A

- `58c2cc66b` prereg, `21d838921` implementation. Verdict BUILD-FAIL,
  A-F1 fires (fails T0 and T2). Greedy residual-driven construction cannot
  cross complexity valleys. All C0 cells FAIL; line falsified.

### 7. Discovery hypothesis B

- Prereg `9e2fbd134` frozen; implementation `hyp_b/hyp_b.zag` present but no
  committed result at matrix time. All C0 cells UNTESTED (pending).

### 8. Discovery hypothesis C

- `5a9ec56e7` prereg, `aae06bac6` implementation. C-F1 FIRES: fails T0.
  Greedy single-op repair picks per-episode constants, degenerates to
  memorization (24 splits, 133-op program on T3). All C0 cells FAIL; line
  falsified.

### 9. Discovery hypothesis D

- Prereg `82aaed137` frozen; raw logs present, no committed result at matrix
  time. All C0 cells UNTESTED (pending).

### 10. Form inventor R1-R6

- Prereg `45d3d6875` + amend `70369d67b`; result `1b8e032c4`
  (INVENTOR-TESTED, 14/14 frozen predictions).
- **C0-A FAIL:** source audit in FORMINVENTOR_RESULT.md: the three
  diagnosis-to-construction recipes are dedicated branches written before
  training. Kills L3 under strict reading. Explicitly "bounded structural
  L2, not L3".
- **C0-B FAIL:** selects one complete construction recipe from a finite
  researcher-enumerated set of three; final topology does not emerge
  incrementally.
- **C0-C UNTESTED.**
- **C0-D PARTIAL:** invented form promoted as live form with verification
  schedule, refit, and revision inside the protocol; reuse demonstrated
  within-protocol only.

### 11. Verification subsystem

- Attack `483b0e61f` (prereg `dce1f3d6e`), build `a07f9b9a6` (prereg
  `82ab9f40e`), active `1c92aa353` (prereg `7e178c075`), architecture
  `8446517e7` (ARCH-DOCUMENTED). Explicitly researcher-designed trust
  infrastructure; the architecture doc states it satisfies no part of
  Criterion 0 and is not an L3 claim. N-A for all cells.

### 12. DEVINT1 developmental integration

- Builder survived a 6-attack independent red team (A1 partial, A2
  attack-succeeds on seg controls, A3-A6 attack-fails). Bounded L2+
  integration result, not representational invention. All C0 cells FAIL;
  not a C0 candidate.

### 13. DEVANG_H4 developmental language

- Test 16/20; bounded L2 grounding. Grammar, segmentation machinery, and
  evaluation protocol researcher-designed. All C0 cells FAIL; not a C0
  candidate.

## Which line is closest to full C0? (K3)

**The Q4 explanatory-variable line is closest**, with C0-C and C0-D both
PASS on the F-PARCOND pairing. No other line has any PASS outside v1's
C0-A substrate proof.

**What blocks Q4 from a full C0 claim (ordered by difficulty):**

1. **C0-A (partial -> pass):** the beam-search discovery driver is
   researcher-authored. The OP-RECRUIT v1 result proves the C0-A substrate
   is achievable on the same VM family (one generic dispatch case, semantics
   in learner bytes). The path is learner-driven recruitment (OP-RECRUIT v2
   design `c6ef7ffcf`): the learner itself must decide DETECT/PROPOSE/
   VALIDATE/RECRUIT, not a researcher driver loop.
2. **C0-B (partial -> pass):** the operator alphabet is closed (31 ops).
   Incremental growth is demonstrated, but the final form is assembled from
   a researcher-enumerated vocabulary. Needs learner-extended construction
   vocabulary (recruited ops feeding the discovery beam).
3. **C0-C (1 data point -> multiple):** only one independent post-freeze
   adversary family has been run. Criterion 0 demands multiple materially
   different unforeseen forms.
4. **Promotion pipeline incomplete:** reproduction (done, `121b6d5aa`),
   simple-baseline comparison (done, `757442c40`), alternative-explanation
   attack, OOD test, ablation, transfer, independent red team, governance
   audit have not all been run on F-PARCOND.

**Second-closest:** OP-RECRUIT v1 on C0-A (substrate proven) combined with
the v2 design (learner-driven recruitment specified, not built). If v2
implements and its T-SELF/T-ADV worlds pass, the combination "v2-recruited
operators + Q4 discovery" is the strongest candidate architecture for a
full-C0 attempt: v2 supplies learner-authored semantics, Q4 supplies
adversary-tested discovery and reuse.

## Kill-bar self-check

- **K1 (matrix complete):** PASS. 13 lines x 4 cells, every cell assigned
  with a verdict.
- **K2 (evidence cited):** PASS. Every substantive cell cites a commit hash
  verified present via `git log` on 2026-09-30; result-file quotes are
  verbatim from committed sources.
- **K3 (blockers identified):** PASS. Four ordered blockers for Q4 plus the
  v2-recruitment combination path.

## Verdict: STATUS-TRACKED

Closest to full C0: Q4 line (C0-C + C0-D PASS). Blocking: researcher-authored
discovery driver (C0-A), closed operator alphabet (C0-B), single adversary
data point (C0-C), incomplete promotion pipeline. No line is within reach of
a full four-cell C0 claim today.
