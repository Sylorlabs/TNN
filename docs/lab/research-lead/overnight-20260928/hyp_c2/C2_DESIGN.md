# C2 DESIGN: Counterexample-Driven Growth with Non-Myopic Repair

Date: 2026-09-30.
Status: DESIGN ONLY. No implementation. No code written.
Authority: amends Hypothesis C after its falsification.

## 1. References

- C1 prereg: `hyp_c/PREREG_HYP_C.md` (5a9ec56e7)
- C1 result: `hyp_c/HYP_C_RESULT.md` (aae06bac6). Verdict: C-F1 FIRES, falsified.
- Implications analysis: `discovery_implic/IMPLICATIONS_ANALYSIS.md` (bee0f840d), requirement 4: non-myopic repair.
- Battery prereg: `discovery_battery/PREREG_BATTERY.md` (425f7276d).
- Frozen VM: GENEXEC2 semantics from 8d5f58b89 (vm_run, prog helpers, mod_nonneg).

## 2. Why C1 failed

From aae06bac6, the failure is in the repair operator, not the implementation:

1. Single-op repair cannot cross valleys. Building `[IN0, PUSH 2, MUL, PUSH 1, ADD]` for T0 (2x+1) requires the two-step dependency PUSH 2 then MUL. No single op appended to any prefix both fixes the current failing episode and preserves passing episodes along the true path.
2. Must-fix-now biases to constants. On T0 episode (0,1), the first repair is PUSH 1 (fixes it, nothing to break). Structural ops like IN0 fix no single T0 episode (2x+1=x has no train solution), so IN0-led programs are unreachable from the empty prefix.
3. No-breakage blocks stepping stones. Intermediate steps that would enable later fixes are rejected because they break a currently passing episode.

Result: greedy repair picks constants, dead-ends, then splits pathologically (T0: 5 splits for a 1-region function; T3: 24 splits, memorization).

## 3. C2 mechanism

C2 keeps C1's identity: single growing program, no population, no score-ranked retention of partial programs. The driver remains the counterexample set. Three changes make repair non-myopic: bounded lookahead, a net-progress criterion, and chronological backtracking.

### 3.1 State

- `P`: straight-line op list (the growing program), initially empty.
- `best_P`: prefix with the highest train pass count seen in this grow() call, initially [].
- `stack`: choice points. Each records `(prefix_ops, ext_ops)` taken.
- `tabu`: set of `(tuple(prefix_ops), tuple(ext_ops))` already tried in this grow() call.
- `backtracks_used`: counter, initially 0.

### 3.2 Fix search (lookahead)

On failing episode e with current pass count c:

1. Enumerate all op sequences S of length 1..L, where L=3 (frozen), in lexicographic order over the frozen op alphabet: IN0, IN1, PUSH -9..9, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER, LT, EQ, GT.
2. Two-phase evaluation (deterministic, frozen VM 8d5f58b89; div/mod by zero follow VM semantics):
   - Phase 1: evaluate P+S on e only. Discard S unless e passes.
   - Phase 2: for survivors, count train episodes passed by P+S.
3. Exclude any S with `(tuple(P), tuple(S))` in tabu.
4. Select argmax by (pass count desc, length asc, lex asc).
5. If argmax pass count is strictly greater than c, append S to P, push the choice point, update best_P if improved, and continue. Otherwise, no improving fix exists.

Cost control: phase 1 is one program evaluation per sequence (about 40k sequences for L=3 over 34 ops); phase 2 runs only on sequences fixing e, which is a small fraction. Total per fix search is well under 100k evaluations on battery tasks.

### 3.3 Net-progress criterion (replaces no-breakage)

C1 required: fix e AND break no passing episode. C2 requires: fix e AND strictly increase total pass count. This is softer in exactly the way the analysis demands: a repair may break k passing episodes if it fixes more than k, which permits stepping stones that sacrifice a passing episode to make net progress. Pass count is the true train objective, not a heuristic proxy, so unlike A's residual complexity it cannot mislead: every accepted repair strictly improves the objective along the taken trajectory, which means the criterion itself can never create a valley.

### 3.4 Chronological backtracking

If no improving fix exists:

1. If the choice stack is non-empty and `backtracks_used < BMAX` (BMAX=6, frozen): pop the last choice point, add `(prefix, ext)` to tabu, increment `backtracks_used`, and continue (the fix search re-runs at the shallower prefix, now excluding the tried extension, so it returns the next-best candidate).
2. Otherwise: SPLIT (section 3.5).

BMAX is a frozen resource bound with a stated rationale: a handful of backtracks suffices to escape constant traps (T0 needs 1); persistent stagnation after several retractions indicates the straight-line prefix is wrong-headed and the target is likely piecewise, which is the split operator's job. Backtracking terminates because the sequence space is finite and tabu never repeats a (prefix, extension) pair within a grow() call.

### 3.5 Split (unchanged from C1)

Split fires on stagnation (backtrack budget exhausted, or choice stack empty with no improving fix). It uses best_P's failing/passing partition (not the current P, which after backtracking may be the empty prefix with an empty passing set). Probe selection is C1's frozen rule: first probe from the frozen family ([IN0/IN1, PUSH k, LT/GT/EQ], k in -4..4) that puts episodes on both sides. Recurse grow() on each partition; compile as probe + JZ + branches. If no probe separates, FAIL. Because every split strictly reduces partition size, recursion terminates.

### 3.6 Termination and bounds

- Fix search: finite enumeration, terminates.
- Backtracking: finite tabu space plus BMAX cap, terminates.
- Splits: strictly smaller partitions, terminate.
- Frozen bounds: L=3, BMAX=6, 1M evaluations per task (battery budget).

Trace logging (for a future implementer): every REPAIR logs (sequence, count before/after); every BACKTRACK logs (popped sequence, depth); every SPLIT logs (probe, partition sizes); EVALS total logged per task.

## 4. Transparent amendment: C1 to C2

| # | C1 (5a9ec56e7) | C2 (this design) | Why |
|---|---|---|---|
| 1 | Repair appends a single op | Repair appends a sequence of length 1..3 (L=3 frozen) | Single-op repair cannot express two-step dependencies (PUSH 2 then MUL); observed in aae06bac6 on T0 and T2 |
| 2 | Criterion: fix e AND break nothing | Criterion: fix e AND strictly increase pass count | No-breakage blocks stepping stones; net progress permits sacrificing k passing to fix more than k |
| 3 | Selection: first op in deterministic order that works | Selection: argmax over fixing sequences by (pass count desc, length asc, lex asc), 2-phase eval | First-in-order systematically picks constants (PUSH k); argmax by pass count finds general solutions first (T2: [IN0, PUSH 3, MOD] selected in one repair) |
| 4 | No backtracking; on repair failure, split immediately | Chronological backtracking with (prefix, extension) tabu, BMAX=6 | The first repair choice is often wrong (constant trap); without retraction, no recovery is possible |
| 5 | Split from current P | Split from best_P on stagnation | After backtracking the current prefix may be empty; best_P preserves the most informative partition |
| 6 | (none) | Frozen bounds L=3, BMAX=6 disclosed | Resource bounds keep C2 a bounded discovery mechanism, not unbounded search |

What is NOT changed: single program (no population), counterexample ordering (only sequences fixing the current failing episode are ever considered), the split operator and probe family, the frozen VM, determinism requirements.

## 5. Valley-crossing argument and T0 walkthrough

Claim: C2 solves T0 (2x+1, episodes x=0..8), which falsified C1.

- P=[], c=0, e=(0,1). Fix search: argmax among L<=3 sequences fixing (0,1) by (count desc, length asc, lex). Max count is 1 (no L<=3 sequence fixing (0,1) passes any other episode: constant-1 and x+1 variants all pass only (0,1)). Tie broken by length asc then lex: [PUSH 1] (length 1) beats [IN0, PUSH 1] (length 2). REPAIR [PUSH 1]. P=[PUSH 1], c=1. (The constant trap is still tried first; the difference from C1 is what happens next.)
- e=(1,3). From P=[PUSH 1] the stack is constant [1]; every extension computes a constant, so no extension fixing (1,3) has count > 1. No improving fix. BACKTRACK: pop [PUSH 1], tabu ([], [PUSH 1]).
- P=[], c=0, e=(0,1). Fix search excluding tabu: next argmax is [IN0, PUSH 1] (count 1, length 2; [PUSH 1, ADD] is a semantic no-op extension ordered later). REPAIR [IN0, PUSH 1]. P=[IN0, PUSH 1] (stack [x,1], output 1), c=1.
- e=(1,3). Fix search from [x,1]: no length-1 or length-2 extension both fixes (1,3) and keeps (0,1) (verified by enumeration: 2-op extensions cannot satisfy f(0)=1 and f(1)=3). Length 3: [IN0, ADD, ADD] gives [x,1,x] -> [x,x+1] -> [2x+1], count 9. It is the lex-first length-3 sequence with maximal count ([OVER, ADD, ADD] ties at count 9 but orders later). REPAIR [IN0, ADD, ADD]. P=[IN0, PUSH 1, IN0, ADD, ADD], count 9 = all episodes. DONE.

T0 SOLVES with 3 repairs and 1 backtrack, about 160k evaluations total, well under budget. The valley is crossed by the combination the analysis required: lookahead finds the multi-op fix, backtracking retracts the constant trap, and the net-progress criterion never commits to a non-improving step.

Predicted trace for a future implementer to match: REPAIR, BACKTRACK (1), REPAIR, REPAIR. The exact program may differ in equivalent ways ([OVER, ADD, ADD] instead of [IN0, ADD, ADD]); SOLVE with at most 2 backtracks is the checkable prediction.

## 6. T2 walkthrough (brief)

T2 (x mod 3, x=0..8): P=[], e=(0,0). Fix search: [IN0, PUSH 3, MOD] (length 3) computes x mod 3 exactly, count 9, which is maximal. No shorter sequence reaches count 9 (length-1 max is 3 via [PUSH 0]; length-2 max is 4 via [IN0, PUSH 2, MOD]). Argmax selects it first. Single REPAIR, SOLVE, zero backtracks. This is the case C1 could not even start (empty program already minimal under its criterion) and A could not start (IN0 worsened residual).

## 7. Predictions T0-T5

- T0 (2x+1): SOLVE. Trace: repairs with at most 2 backtracks (section 5).
- T1 (abs): SOLVE via splits. Straight-line repair stagnates (abs needs a conditional); backtrack budget exhausts; split from best_P; recursion solves each branch ([IN0, NEG] on negatives, [IN0] on non-negatives). Predict at most 4 splits. Note: probe order may yield more regions than the minimal 2; this is a known C-family quirk, not C-F3, provided split count stays far below episode count.
- T2 (mod3): SOLVE. Trace: single REPAIR [IN0, PUSH 3, MOD] (section 6).
- T3 (parity): SOLVE. Trace: single REPAIR [IN0, PUSH 2, MOD] (count 25 maximal; no shorter sequence reaches it). C2 avoids C1's memorization trap because argmax-by-count finds the general solution before splitting is ever considered.
- T4 (nested abs): SOLVE via nested splits, 0 CALLs. The key discriminator against B is preserved: C2 has no CALL mechanism and no fragment library, so nested structure must appear as nested SPLIT events.
- T5 (fragment composition): SOLVE via splits, one straight-line repair per region.

## 8. Proposed falsifiers (to be frozen by the implementer in PREREG_HYPC2.md)

- C2-F1: C2 fails T0. The non-myopic repair is inadequate; C2 falsified.
- C2-F2: C2's T4 trace shows fragment CALLs instead of nested splits. Mechanism falsified.
- C2-F3: split count on any task reaches the episode count (degenerate splitting as in C1's T3).
- C2-F4: T0 requires more than BMAX backtracks (the valley is deeper than the design covers).
- C2-F5: any task exceeds 1M evaluations (C2 is not a bounded discovery mechanism).

## 9. Why C2 is genuinely different

- Vs beam search: C2 keeps one program, not a population. Selection among candidates uses the true train objective (pass count), never a heuristic proxy, and retention is chronological (backtracking), not score-ranked. There is no elite archive and no ranking across iterations.
- Vs A (21d838921): A's flaw was a heuristic proxy (residual complexity) that is non-monotonic along solution paths. C2's criterion (pass count) is monotonic by construction along the taken trajectory: every accepted repair strictly increases it, so the criterion itself cannot create a valley. Valleys are crossed by lookahead (multi-op jumps over them) and backtracking (retraction), not by tolerating worse scores.
- Vs C1 (aae06bac6): C1 is greedy single-op with no retraction. C2 adds exactly the three remedies the falsification demanded: lookahead, softer criterion, backtracking. If C2 is falsified, it falsifies this specific repair, not counterexample-driven growth in principle; the split operator is untouched and independently testable.

## 10. Honest scope and risks

1. C2 is a systematic counterexample-ordered search with bounded backtracking. Its "discovery" claim rests on counterexample guidance pruning the search (only sequences fixing the current failing episode are considered), the split operator for piecewise structure, and succeeding where greedy C1 failed. It is bounded L2 machinery, not L3 representational invention: the op alphabet, L, BMAX, and probe family are researcher-set.
2. Residual risk: split probe order is inherited unchanged from C1, so T1/T4 may split on semantically awkward probes (C1's [IN0, PUSH -4, LT] before [IN0, PUSH 0, LT]). This may inflate region counts. It does not affect SOLVE/FAIL predictions.
3. Residual risk: BMAX=6 and L=3 are set by the designer. If the battery's true programs needed longer lookahead, C2-F4 would fire honestly. The bounds are disclosed, not tuned to results (no C2 results exist).
4. The net-progress criterion's breakage allowance was not exercised in the T0/T2 walkthroughs (both kept all passing episodes). It is designed capability for cases where a repair must sacrifice a passing episode to make net progress; a future implementer should log when it fires.
5. No implementation, no evaluation, and no Python were involved in this design. The T0/T2 walkthroughs are hand-traced through the specified mechanism, not executed.

## 11. Governance

Design only; no implementation files, no binaries, no execution. No Python used or invoked at any stage. No em dashes in this document. Committed local only, owned path `docs/lab/research-lead/overnight-20260928/hyp_c2/`, with pathspec commit. This design does not freeze a preregistration; a future builder must write PREREG_HYPC2.md (freezing falsifiers C2-F1..F5 or amended versions) strictly before implementing.

**Builder label: DESIGN-COMPLETE.**
