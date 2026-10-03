# PREREG H1: Learner-named procedure objects over the frozen ISA

Lane: TNN3H1, wave-20261001-2021pdt. Phase 1 deliverable. Analysis and
preregistration only; no implementation written, no experiments run.
Grounding: `docs/lab/rsi/runs/wave-20261001-1721pdt/TNN3/HYPOTHESES.md`
(H1, lines 33-58), `ROOT_CAUSE.md`, `ARCH_ACCOUNTING.md`; battery record
`docs/lab/rsi/runs/wave-20261001-1421pdt/sealed_adv/RESULT_SEALED_ADV_BATTERY.md`.

## 0. Step 0 (toolchain guard)

Safebin activated and verified before any other work; recorded in
`NAMECHECK.md` Step 0 of this lane. PATH is safebin only. `which python3`
prints nothing; `which python`, `which perl`, `which node`, `which ruby`
print nothing. All implementation, harness, verifier, scorer, fixture, and
analysis work in this lane is pure Zag compiled by the pinned znc, or shell
invoking znc, running binaries, git ops, and file moves/copies. Any forbidden
executable invocation is automatic PROCESS-FAIL and will be reported.

## 1. Freeze record (ordering is load-bearing)

1. This prereg is committed alone by the coordinator. Its SHA-256 and commit
   are recorded in the wave record before any implementation file exists.
2. Implementation is authorized only after that commit. Implementation freeze
   is recorded by SHA-256 of the target file plus `git diff --stat` against
   the baseline.
3. The independent adversary designs sealed worlds only after the
   implementation freeze, and records a world manifest (SHA-256) before the
   sealed run. The builder lane never sees world files before execution.
4. Any violation of this commit order voids the prereg (unverifiable
   ordering): results cannot be adopted that wave.

Baseline (frozen): `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`,
1591 lines, commit f4de7ff46, SHA-256
`a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`.
Implementation target: `docs/lab/research-lead/overnight-20260928/tnn3_build/tnn3.zag`,
a byte-copy of the frozen baseline with the deletion set in section 3
applied. No other cognition source file may change.

## 2. Hypothesis under test

H1: promote executable graphs from stamped per-instance literals to
learner-owned named objects. The learner gains one generic affordance: LINK
cells into a sequence and NAME the sequence with a learner-chosen handle;
EXECUTE (approved protected machinery) runs any named object. Procedures stop
being keyed by (subject, relation) MAP fields and become addressable
structures the learner creates, references, and reuses across instances.

Cluster addressed: Cluster A (no abstraction tier). Members: M1-W1 (novel
P-then-Q composition, 0/8 in the battery), M1-W3 (shared-step diamond, 0/3),
M3-W1 generalization probes (x+5 on unseen subjects, 0/2). H1 is load-bearing
for H3 and partly for H7/H8: if H1 fails, H7's negative prediction (relearning
the same wrong thing) becomes the expected outcome.

The falsifiable prediction from HYPOTHESES.md, restated as the binding bar:
on a sealed composition world, if the learner creates named procedures but
white-box inspection shows zero reuse of any name across instances (every name
written once and executed once on its demonstrating instance), H1 is dead: the
affordance alone does not produce abstraction, and the missing piece is not
naming.

No L3 claim is available on any outcome of this test. This prereg tests a
substrate affordance, not representational invention (Criterion 0 not met).

## 3. What changes (exact file-level plan and delta accounting)

### 3.1 Deletion list (exact, against the frozen baseline)

- Lines 363-377: `fn t2_asm_chain` (k-hop chain assembler). DELETED.
- Lines 379-396: `fn t2_asm_count` (count assembler). DELETED.
- Lines 379-412 comment included: the count epilogue comment and
  `fn t2_asm_sum` (lines 398-412, subset-sum assembler). DELETED.
- Lines 586-666: `fn t2_trial` in full (the researcher-fixed schema menu and
  search order: k-hop chains k=2..4, then subset sums, then counts, then the
  single-hop fallback at former line ~657). DELETED.
- Net deletion target: about 155 lines (four assemblers about 75 lines, the
  schema menu order about 80 lines).

### 3.2 What the deletion is replaced with (affordance semantics)

No researcher-authored schema selects the shape of a constructed graph. The
miss path exposes only generic construction through already-existing
machinery: cell allocation (`alloc_node`), guard/set/literal/inc/move cells
(`t2_guard`, `t2_set`, `t2_lit`, `t2_inc`, `t2_mov`), cell sequencing
(`ns`, `seq_link`), edge creation (`link_edge`), and execution
(`execute(W, root, fr)`). Naming and linking ride on the existing node and
edge allocation machinery: a NAME is a learner-created handle cell linked to
a sequence root, addressed by handle rather than by (subject, relation) MAP
fields. The exact call-site surgery (for example the `mp_run` call site at
former line 668) is implementation detail and is NOT frozen here; the
accounting bars in 3.3 govern it.

### 3.3 Capability-source delta accounting (frozen bars on the diff)

- Cognition source lines ADDED: 0. Any added line in a cognition source file
  is PROCESS-FAIL.
- Cognition source lines DELETED: at least 150 (the section 3.1 set, about
  155). Fewer than 150 deleted is PROCESS-FAIL.
- Non-deletion modified lines: call-site rewiring only, no new decision
  logic. Any modified line containing a new conditional, new constant, or new
  semantic case is PROCESS-FAIL.
- New modes, bridges, routers, task-specific handlers, or admission gates: 0.
  Any one is PROCESS-FAIL and an architecture-review trigger.
- New hardcoded semantic cases (beyond the frozen ISA class): 0.
- Verification: `git diff --stat` and a line-accounting pass (pure Zag)
  against the frozen baseline, recorded at implementation freeze.

### 3.4 Learner-facing affordances (white-box observable)

- AFF-LINK: the learner can allocate guard/set cells and sequence them with
  SEQ edges. No researcher schema chooses the sequence shape.
- AFF-NAME: the learner can create a handle cell with a learner-chosen value
  and a NAME edge to a sequence root, forming a named procedure object.
- AFF-EXEC: `execute(W, root, fr)` runs any named object on a frame.
- White-box signature of a name object: a learner-created handle cell, one
  NAME edge from the handle cell to a sequence root, where the sequence is
  built from ISA cells (MOVE, BRANCHEQ, INC, DEC or frozen-baseline cell
  tags) and reachable SEQ edges. The inspection tool records handle value,
  root address, and the instance key of each execution that traverses it.

Note: the EXECUTE placement ruling (seventh protected-core primitive
`EXECUTE(root, frame)` over the 4-op ISA, amendments A-C) was pending at
prereg time. The affordance uses the EXECUTE signature the coordinator
freezes; if the ruling changes the signature, this prereg is amended
transparently and re-frozen before implementation.

## 4. Sealed evaluation design

Worlds are designed by an independent adversary AFTER the implementation
freeze (section 1, step 3), with materially different surface structure from
the battery worlds: new subject id ranges (must not collide with the
40000-49999 ranges used in the battery; adversary records the chosen ranges
in the manifest), new relation ids, new law forms. No trivial M1-W1 or
M1-W3 variants. The builder lane is blind to world files until the sealed
run. Three families:

### 4.1 Family C1: sealed composition (M1-W1 family)

Structure: two procedures P and Q are demonstrated separately on disjoint
subject sets. Novel subjects require P-then-Q composition to answer.
Composition is not in any menu (the menu is deleted); it must be expressed
as a named sequence referencing two named procedures (per H1) or not at all.
Probes: 8 composition probes, 4 decoy probes (decoys punish memorization of
demonstration values, mirroring the battery's swapped-value decoys).
Collateral: 2 retention probes on demonstrated P/Q instances (mirroring the
battery's collateral discipline).

### 4.2 Family C2: sealed shared-step diamond (M1-W3 family)

Structure: two parent procedures share one step object; the shared step must
be one named object linked by two graphs. Stamped literals cannot express
sharing. Probes: 3 diamond probes, 1 engagement probe (demonstrated parents
answerable), 2 collateral probes.

### 4.3 Family C3: unseen-subject application (M3-W1 generalization family)

Structure: a named procedure demonstrated on seen subjects is probed on
unseen subjects. Probes: 2. Informational coverage only (parameterization
beyond naming is H8's claim, not H1's); not verdict-binding.

### 4.4 Seal and anti-smuggling

The adversary records a world manifest (SHA-256 per world file) before the
sealed run. Anti-smuggling grep over the implementation diff for
adversary-recorded id tokens: any match outside address arithmetic is
PROCESS-FAIL. The coordinator holds world files; the builder receives only
execution transcripts and white-box dumps.

## 5. Frozen kill bars

### 5.1 K-H1-1 (binding white-box reuse bar)

Definition: a reuse event is one learner-created name object (section 3.4
signature) traversed by at least two distinct instance executions (distinct
(subject, relation) instance keys) within the sealed run.
Bar: at least one reuse event in the sealed run constitutes PASS.
Zero reuse events, where white-box shows names were created (every name
written once and executed once on its demonstrating instance), is FAIL and
kills H1 per the falsifiable prediction in section 2.
Counting procedure: pure-Zag inspection of the final state binary, run after
each block; reuse events enumerated with handle value, root address, and the
two instance keys. The counting tool is built after this prereg freezes.

### 5.2 K-H1-2 (composition coverage)

On Family C1: at least 6 of 8 composition probes correct (75%). Decoy
probes must not return memorized demonstration values: more than 1 of 4
decoy probes returning a memorized value is FAIL regardless of composition
score. Bar outcome: PASS requires both conditions.

### 5.3 K-H1-3 (shared-step coverage)

On Family C2: at least 2 of 3 diamond probes correct. The engagement probe
must be correct (validity). Bar outcome: PASS requires both.

### 5.4 K-H1-4 (generalization coverage, informational)

On Family C3: at least 1 of 2 unseen-subject probes correct. Recorded as
coverage; NOT verdict-binding (parameterization is H8's claim).

### 5.5 Process bars (all must PASS or the wave result is void)

- K-P1 (prereg ordering): this prereg's SHA-256 recorded before any
  implementation file exists; implementation commit strictly after; world
  manifest strictly after implementation freeze. Verified by hash plus
  filesystem mtime order.
- K-P2 (determinism): 3 runs per family; transcripts and final-state binaries
  byte-identical across all 3 runs (SHA-256 equality). Zero randomness in
  decision paths.
- K-P3 (frozen binary): implementation target hash verified before each
  sealed block and after the battery; no source edits between.
- K-P4 (seal integrity): world files match the adversary manifest;
  anti-smuggling grep per section 4.4 clean.
- K-P5 (no-leak): zero correct ANSWERs on novel-key probes coinciding with
  cross-world taught values.

## 6. Negative controls (what FAILS H1)

1. K-H1-1 FAIL with names created: H1 is dead (binding falsifier). The
   affordance alone does not produce abstraction; the missing piece is not
   naming. Redirects the procedure-invention frontier away from naming
   affordances.
2. K-H1-1 PASS but K-H1-2 or K-H1-3 FAIL: naming without functional
   abstraction. H1 does not advance to TNN-3; the result points at H2
   (direction/derivation ownership) and H3 (procedure-as-operand) as the
   missing structure.
3. Any execution in the sealed run keyed by (subject, relation) MAP fields
   for newly constructed procedures, or any residual schema-menu order in
   white-box traces: implementation violated the deletion set; PROCESS-FAIL,
   results void.
4. Any forbidden protected semantic operation in the diff
   (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
   LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL, or benchmark/domain
   equivalents): governance violation; PROCESS-FAIL, results void.
5. K-P2 FAIL (nondeterminism) or any randomness in decision paths:
   PROCESS-FAIL, results void.

## 7. Pure-Zag construction

All research logic is Zag compiled by the pinned znc: the implementation,
the white-box inspection tool, the reuse counter, the scorers, world
drivers, fixture provisioning, and any analysis. Shell is used only to
invoke znc, run compiled binaries, perform git ops, and move or copy files.
No Python, C/C++, JavaScript, or Rust at any stage, including glue and
scratch. A single forbidden invocation voids the wave result for this lane
(automatic PROCESS-FAIL), reported honestly in the lane record.

## 8. Determinism protocol

- 3 runs per family (C1, C2, C3), 9 runs total per complete battery.
- No time-based seeds, no hash-order iteration, no nondeterministic input
  order anywhere in the decision path.
- Transcripts compared byte for byte; final-state binaries hashed with
  SHA-256; all three runs must be identical (K-P2).
- Any divergence is investigated as a defect before any result is adopted;
  a second divergence voids the battery.

## 9. Governance boundary

- Frozen ISA (allowed protected-class machinery): ALLOC, READ, WRITE, LINK,
  COPY, COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE, generic state and register
  operations. EXECUTE(root, frame) is approved protected machinery per the
  2026-09-30 ruling, subject to the pending placement amendments noted in
  section 3.4.
- Forbidden as protected semantic operations: FIND_POLYNOMIAL_ORDER,
  DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD,
  MAKE_CONDITIONAL, or benchmark/domain equivalents. Presence in the diff is
  PROCESS-FAIL.
- The ISA basis is never grown one benchmark at a time. No per-world
  opcodes, no benchmark-specific handlers.
- ONE-SYSTEM RULE: no new modes, bridges, routers, or task-specific
  admission gates. Standing question honored: why can the existing general
  architecture not learn this behavior; the answer here is that it could not
  name and reuse, which is what the deleted menu prevented.

## 10. Predicted bar outcomes (recorded before execution)

- K-H1-1: genuinely uncertain; this is the falsifiable core. Prior: the
  affordance may be exercised without reuse, which would kill H1 cleanly.
  That negative outcome is ranked as high information gain.
- K-H1-2: likely FAIL. Composition requires chaining two named procedures,
  which is adjacent to H2's derivation-ownership claim; the H1 affordance
  alone may not produce it.
- K-H1-3: uncertain. Shared-step expression requires the learner to link one
  object from two graphs; no prior evidence it will.
- K-H1-4: likely weak (0-1/2); parameterization is H8's claim.
- Process bars: expected PASS; any FAIL voids the result rather than
  weakening it.

## 11. Verdict rules

- H1 PASSES (adoptable for TNN-3): K-H1-1, K-H1-2, and K-H1-3 all PASS, and
  all process bars PASS. Even then, no L3 claim: the result establishes a
  substrate affordance, not representational invention.
- H1 FAILS (dead): K-H1-1 FAIL with names created. The affordance alone does
  not produce abstraction. The lane records the kill and the redirect
  (H2/H3), and no TNN-3 build may cite naming as the abstraction mechanism.
- H1 WEAK (not adopted): K-H1-1 PASS but K-H1-2 or K-H1-3 FAIL. Naming
  without functional abstraction; blocks adoption pending H2/H3 results.
- Any process bar FAIL, any section 6 negative control triggered: results
  void for the wave; correction proceeds only as fresh preregistration plus
  fresh sealed worlds, never amend-and-promote.

## 12. What a PASS means and what it does not mean

A PASS means: on sealed worlds designed after the freeze, the learner
created named procedure objects and reused at least one across instances,
and that reuse carried composition and shared-step behavior the frozen
menu could never express, with zero cognition source lines added and about
155 deleted. It does not mean: generality beyond the tested families
(FW1-FW9 precedent: a targeted battery establishes no broad generality);
L3 representational invention; or that H3, H7, or H8 are validated. A PASS
advances H1 to replication, stronger red team, scaling, transfer, and
integration per the 11-step frontier pipeline.
