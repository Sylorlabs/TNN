# MUL-1 Build Report: MUL-BUILD-COMPLETE (Rung A Primary Arm)

Date: 2026-09-30. Worker: MUL Builder.
Frozen prereg: `docs/lab/research-lead/overnight-20260928/mul_prereg/PREREG_MUL1.md` @ `222899314`.
ISA boundary: `docs/lab/research-lead/overnight-20260928/architecture_rulings/ISA_BOUNDARY_RULING.md` @ `0525377f3`.
K1 verified: both commits are ancestors of HEAD before implementation began.

## Verdict: MUL-BUILD-COMPLETE (Rung A primary arm)

All five frozen predictions P-MUL1..P-MUL5 pass, plus the oracle-audit
shuffled rerun. Determinism: 3 runs byte-identical
(sha256 `72a54993f96b7eb9beb14727947528bbee6dbcd74a7f0fd1f932ac76d893008b`).

## What was built

`mul_build/mul1.zag` (pure Zag, pinned compiler `znc_linux_x86_64_abed8aa1`,
clean build, zero warnings). Single self-contained binary `mul1_bin`.

Architecture:
- Rung A cell vocabulary (ISA mapping): INIT_R0 / INIT_C0 (MOVE literal),
  ACCUM_RX / ACCUM_RY (MOVE result <- ADD), STEP_C (MOVE counter <-
  ADD(counter, literal 1); the literal-1 step), TEST_CY / TEST_CX
  (BRANCHEQ), GOTO(t) (SEQ back-edge). No new arithmetic op. No MUL, SUB,
  or loop primitive in source (K3 scan clean; K4 satisfied).
- Phase 3 discovery: fixed published trial order. Programs enumerated by
  length L = 1..6 (within frozen K = 8), lexicographic over alphabet
  0..6+L. First program scoring 12/12 on the bare exemplars is promoted.
- Promotion materializes the winner as learner-owned workspace PROC nodes
  (root node 0, CELL nodes 1..L with SEQ ref0 and branch ref1). All later
  phases execute from the workspace graph via `ws_exec` (C0-A artifact).

## The promoted structure

`[ACCUM_RX STEP_C TEST_CY GOTO(0)]` (4 cells). Semantics: R and C start
at 0; loop { R += X; C += 1; } until C == Y; output R. This computes X*Y.

Note: the learner found a 4-cell form, not the prereg section-1 6-cell
sketch. It discovered that INITs are unnecessary because slots
zero-initialize (an efficiency improvement; execution-model choice,
documented here, not multiplication-specific). This is a learner-made
structural decision, not a researcher template.

## Test results (frozen predictions)

- P-MUL1: 8/8 held-out probes correct, scaling probe (13,17)->221 correct.
  PASS.
- P-MUL2: Tier 1 (above) + Tier 2 structural on workspace graph:
  (a) back-edge GOTO(0) targets ancestor cell, (b) ACCUM_RX in loop body,
  (c) TEST_CY data-dependent termination, (d) no op writes X/Y. PASS.
- P-MUL3: ablation (PROC root + cells invalidated) -> 8/8 probes
  wrong-or-unknown; core ADD intact on 10 pairs; unrelated fact nodes
  intact. PASS.
- P-MUL4: transfer with different surface encoding (named attributes
  width=6, height=7, not pairs). Query path EXECUTEs the MUL root;
  rect area = 42. PASS.
- P-MUL5: lookup-table control (12 exact-key triples) scores 0/8 on
  probes (frozen ceiling 2). Margin: 8 - 0 = 8 >= 5. PASS.

## Oracle audit (prereg section 7)

1. Trial order published: length-first L=1..6, lexicographic, alphabet
   defined in source. Fixed and deterministic.
2. (a) First trial is (L=1, [INIT_R0]); the correct 4-cell program was
   trial 4298. 4297 incorrect skeletons precede it (>= 5 required).
   (b) Genuine alternatives present: 72 rejected candidates scored 1..11
   (e.g., [ACCUM_RY ACCUM_RY] scores 1/12; [INIT_R0 ACCUM_RY ACCUM_RY]
   scores 1/12). The space contains wrong-in-interesting-ways loops
   (wrong accumulant, wrong test bound), not trivial variants.
   (c) Construction trace records 72 genuine rejections (>= 3 required);
   first 3 printed in the run log.
3. Shuffled rerun: the 4298 tried programs were Fisher-Yates shuffled
   (LCG seed 222899314) and Phase 3 re-run. A 12/12 program was still
   promoted (`[ACCUM_RX STEP_C TEST_CY GOTO(0)]`), scoring 8/8 on probes
   plus scaling 221. Order is not load-bearing. PASS.

## Template-contamination check (prereg section 5)

Researcher commitments (frozen ceiling): the 7-type vocabulary, K bound,
frame model (x,y read-only; r,c zero-init), length-first lexicographic
order, 12/12 corroboration bar.

Learner-made structural decisions in the promoted graph (at least one
required; six present):
1. ACCUM_RX over ACCUM_RY (which accumulant).
2. TEST_CY over TEST_CX (which termination bound).
3. STEP_C placement (counter stepped by literal 1).
4. GOTO(0) back-edge target.
5. Omission of INITs (zero-init efficiency discovery).
6. 4-cell length (not 5 or 6).

The final graph is not fully determined by researcher choices. F-MUL2
does not trigger on this evidence.

## Falsifier status

- F-MUL1 (memorization): no. Graph has back-edge + accumulation cell;
  scaling probe (13,17)->221 rules out case list.
- F-MUL2 (template): no (see contamination check above).
- F-MUL3 (no transfer): no. P-MUL4 passes on different surface encoding.
- F-MUL4 (core smuggling): no. Zero core source changes; K3/K4 clean.
- F-MUL5 (oracle search): no. Audit 2(a)-(c) and 3 pass.

## Scope notes

- This build implements Rung A (primary arm) per Q2 sequencing. Rung B
  ({MOVE, BRANCHEQ, INC, DEC} with learner-constructed ADD) begins after
  Rung A Phase 4 is judged; not in this build.
- The analogy second arm (ADD loop shape reuse, Q1) is a separate
  experimental condition; not a substitute; not in this build.
- Phase 5 revision probes (zero/negatives, criterion 12) and Phase 6
  adversary (F-MUL1..5, post-freeze family) belong to later pipeline
  steps, not to BUILD.
- The 4-cell solution relies on zero-initialized slots. This is an
  execution-model choice (registers start at 0), not a
  multiplication-specific provision. Documented for red-team review.

## One-System Rule accounting (this build)

- Cognition source lines added: ~450 (mul1.zag; experiment harness,
  learner-generic).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
  New task-specific handlers: 0.
- Learner-state structures created: 1 PROC graph (5 workspace nodes)
  + 2 fact nodes (transfer).
- Capability-source delta: the MUL capability resides in workspace nodes,
  not source. Source contains only the domain-neutral vocabulary and
  the trial/corroboration machinery.

## Files

- `mul_build/mul1.zag`: implementation (pure Zag).
- `mul_build/mul1_bin`: built binary (pinned znc).
- `mul_build/NAMECHECK.md`: toolchain guard record.
- `mul_build/BUILD_REPORT.md`: this file.
- `mul_build/run*.log`: run logs (run3a/b/c byte-identical).

## Toolchain guard

Step 0 executed. `which python3` under default PATH found
`/usr/bin/python3` (unremovable system binary; documented non-use).
Restricted safebin at `~/workspace/mul_safebin` (python excluded);
under safebin PATH, `python3`/`python` are ABSENT. Zero forbidden
interpreter invocations in this wave. Pure Zag for all computation.
Shell used only for znc, binary runs, git, and file moves.
