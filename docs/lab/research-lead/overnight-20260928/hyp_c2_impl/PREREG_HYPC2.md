# PREREG: Hypothesis C2 Implementation (Counterexample-Driven Growth with Non-Myopic Repair)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. Implementation not yet started.
Authority: Implements the C2 design from `hyp_c2/C2_DESIGN.md` (e658766bd), which
transparently amends Hypothesis C after its falsification (C1 result aae06bac6,
C-F1 FIRES). Evaluated against `discovery_battery/PREREG_BATTERY.md` (425f7276d).
Battery prereg 425f7276d and C2 design e658766bd strictly precede this commit
(verified by ancestry).

## 1. Hypothesis (amends C1)

C2 keeps C1's identity: single growing program, no population, no score-ranked
retention of partial programs. The driver remains the counterexample set. Three
changes make repair non-myopic:

1. Lookahead repair (L=3, frozen): repair appends op SEQUENCES of length 1..3,
   not single ops. Two-phase evaluation: phase 1 keeps sequences fixing the
   current failing episode e; phase 2 counts train episodes passed. Selection
   is argmax by (pass count desc, length asc, lex asc) over the frozen op
   alphabet in lexicographic order.
2. Net-progress criterion: replaces C1's "fix e AND break nothing" with
   "fix e AND strictly increase total pass count". A repair may break k
   passing episodes if it fixes more than k.
3. Chronological backtracking (BMAX=6, frozen): when no improving fix exists,
   pop the last choice point, add (prefix, extension) to tabu, and re-run the
   fix search at the shallower prefix. Split fires only when the choice stack
   is empty or the backtrack budget is exhausted, and splits from best_P
   (the prefix with highest train pass count seen in this grow() call).

Split operator is unchanged from C1: frozen probe family ([IN0/IN1, PUSH k,
LT/GT/EQ], k in -4..4), first probe putting episodes on both sides, recursive
grow() on partitions, compile as probe + JZ + branches. No CALLs.

What is NOT changed from C1: single program (no population), counterexample
ordering (only sequences fixing the current failing episode are considered),
the frozen VM (GENEXEC2 from 8d5f58b89), determinism requirements.

## 2. Implementation plan

File: `hyp_c2_impl/hyp_c2.zag` (pure Zag, no Python).

Components:
1. GENEXEC2 VM: copied from 8d5f58b89 (vm_run, prog helpers, mod_nonneg).
   Frozen semantics. Op codes: PUSH=0, IN0=1, IN1=2, ADD=3, SUB=4, MUL=5,
   DIV=6, MOD=7, NEG=8, DUP=9, DROP=10, SWAP=11, OVER=12, LT=13, EQ=14, GT=15.
2. Task episodes: T0-T5 as frozen in battery prereg. T6 skipped (sealed).
3. Discovery state per grow() call:
   - P: straight-line op list (the growing program).
   - best_P / best_count: prefix with highest train pass count seen.
   - Choice stack: each records (prefix snapshot, extension ops).
   - tabu: set of (prefix, extension) pairs already tried.
   - backtracks_used: counter, cap BMAX=6.
4. Fix search: enumerate all op sequences of length 1..3 in lexicographic
   order over the frozen alphabet (IN0, IN1, PUSH -9..9, ADD, SUB, MUL, DIV,
   MOD, NEG, DUP, DROP, SWAP, OVER, LT, EQ, GT; 34 symbols; 40494 sequences).
   Phase 1: evaluate P+S on failing episode e only, discard unless e passes.
   Phase 2: for survivors not in tabu, count train episodes passed by P+S.
   Select argmax by (count desc, length asc, lex asc). If argmax count is
   strictly greater than current pass count c, append S to P, push the choice
   point, update best_P if improved. Log REPAIR with (sequence, count
   before/after). Otherwise no improving fix exists.
5. Backtracking: if no improving fix and stack non-empty and
   backtracks_used < 6: pop last choice, restore P to the stored prefix,
   add (prefix, extension) to tabu, increment backtracks_used, log BACKTRACK
   with (popped sequence, depth). Else: SPLIT from best_P.
6. Split: evaluate best_P on the subset for the failing/passing partition.
   Find first probe from the frozen family with episodes on both sides.
   Recursively grow() each partition. Compile as best_P + probe + JZ +
   left + JMP + right. Log SPLIT with (probe, partition sizes).
7. Trace: REPAIR (task, episode, sequence ops, count before/after),
   BACKTRACK (task, popped sequence, depth, backtracks_used),
   SPLIT (task, probe, nleft, nright), FAIL (task, reason).
8. Metrics per task: SOLVE/FAIL, train exact count, hidden accuracy,
   candidate evaluations, wall seconds, repairs, backtracks, splits,
   final program length, CALL count (must be 0), construction trace.
   Carried state: none across tasks (each task grows fresh).

## 3. Predictions (from C2 design section 7, frozen)

- T0 (2x+1): SOLVE. Trace: repairs with at most 2 backtracks (design
  walkthrough: REPAIR, BACKTRACK, REPAIR, REPAIR). C2-F4 fires if more
  than 6 backtracks are used.
- T1 (abs): SOLVE via splits. Trace: straight-line repair stagnates,
  backtrack budget exhausts, split from best_P, recursion solves each
  branch. At most 4 splits.
- T2 (mod3): SOLVE. Trace: single REPAIR [IN0, PUSH 3, MOD], zero
  backtracks.
- T3 (parity): SOLVE. Trace: single REPAIR [IN0, PUSH 2, MOD]. No splits
  (argmax-by-count finds the general solution before splitting).
- T4 (nested abs): SOLVE via nested splits, 0 CALLs. At least 2 nested
  SPLIT events. KEY DISCRIMINATOR vs B preserved: C2 has no CALL
  mechanism and no fragment library.
- T5 (fragment composition): SOLVE via splits, one straight-line repair
  per region.

## 4. Kill bars

- K1: C2 implemented (lookahead repair + net-progress + backtracking +
  split-from-best_P, no population, no ranking). Verified by code
  inspection: no array of candidate programs retained by score; selection
  uses the true train objective (pass count) with chronological retention.
- K2: T0-T5 tested per battery protocol (frozen episodes, budget 1M evals
  or 300s per task, 3/3 byte-identical).
- K3: Predictions evaluated. CONFIRMED requires outcome match AND trace
  showing the predicted mechanism via mandatory events. Specifically:
  C2 on T0 must show the repair/backtrack trace (not degenerate splits);
  C2 on T4 must show 2+ nested SPLITs and 0 CALLs.
- K4: Pure Zag, zero Python invocations, zero em/en-dash bytes, 3/3
  deterministic byte-identical.

## 5. Falsifiers (frozen; any firing falsifies the named claim)

- C2-F1: C2 fails T0. The non-myopic repair is inadequate; C2 is falsified.
- C2-F2: C2's T4 trace shows fragment CALLs instead of nested splits, or
  the T4 program contains CALLs. The mechanism claim is falsified.
- C2-F3: split count on any task reaches the episode count (degenerate
  splitting as in C1's T3, which had 24 splits on 25 episodes).
- C2-F4: T0 requires more than BMAX=6 backtracks. The valley is deeper
  than the design covers.
- C2-F5: any task exceeds 1,000,000 candidate evaluations. C2 is not a
  bounded discovery mechanism.

Note: C2-F4 is distinct from C1's C-F4 (which concerned ranked populations).
C2's selection is argmax by the true train objective with chronological
retention, not score-ranked population retention.

## 6. Determinism

Frozen seed: 0xC2C2C2. All op orders, sequence enumeration orders, probe
orders, and episode orders are deterministic. 3 runs must be byte-identical.

## 7. Governance

Pure Zag only. No Python anywhere (implementation, execution, analysis,
verification). No em dashes in committed files (byte-verified before
commit). Commits local, owned path
`docs/lab/research-lead/overnight-20260928/hyp_c2_impl/` only. Use
`git commit -- <path>` to avoid sweeping concurrent workers. This prereg
is committed alone before any implementation file exists.
