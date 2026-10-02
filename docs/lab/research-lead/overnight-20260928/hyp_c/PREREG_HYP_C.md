# PREREG: Hypothesis C Implementation (Counterexample-Driven Structural Growth)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. Implementation not yet started.
Authority: Implements hypothesis C from `arch_review/ARCHITECTURE_REVIEW.md` (18be93c3e), evaluated against `discovery_battery/PREREG_BATTERY.md` (425f7276d).
Battery prereg 425f7276d strictly precedes this commit (verified by ancestry).

## 1. Hypothesis

Counterexample-driven structural growth. State is a program P (initially empty, output defined as 0) plus a counterexample set. Loop: evaluate P on all train episodes; if all pass, done. Otherwise take the first failing episode e and attempt repair: search single op appends in deterministic op order for one that fixes e while breaking no currently passing episode (verified by re-evaluation). If a repair is found, append it; the growth step is justified by e. If no repair exists, split: choose a probe from the frozen generic probe family ([IN0/IN1, PUSH k, LT/GT/EQ], k in -4..4) that separates failing from passing episodes, then recursively grow each branch on its own episode subset. Splits nest. The program is a decision tree of straight-line segments grown monotonically, each step justified by a specific counterexample.

No population, no scalar ranking. The driver is the counterexample set. Operators are repair and split, not generate and rank.

## 2. Implementation plan

File: `hyp_c/hyp_c.zag` (pure Zag, no Python).

Components:
1. GENEXEC2 VM: copied from 8d5f58b89 (vm_run, prog helpers, mod_nonneg). Frozen semantics.
2. Task episodes: T0-T5 as frozen in battery prereg. T6 skipped (sealed adversary designs later).
3. Discovery:
   - `grow(eps)`: recursive. Takes episode list, returns compiled program.
   - Repair: deterministic op order (IN0, IN1, PUSH -9..9, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER, LT, EQ, GT). For first failing e, try each op: append to current straight-line prefix, check e fixed AND all passing preserved. Take FIRST that works (no ranking). Log REPAIR event.
   - Split: if no repair, iterate probe family in deterministic order ([IN0,PUSH k,LT/GT/EQ] for k in -4..4, then [IN1,...]). Find first probe that separates failing from passing (both groups non-empty). Partition episodes. Recursively grow each. Compile as: probe + JZ + then_branch + JMP + else_branch. Log SPLIT event.
   - The straight-line prefix is maintained as a list of ops; after a split, the function returns the compiled conditional (recursion handles nesting).
4. Trace: every REPAIR logs (task, episode index, op, passing count before/after). Every SPLIT logs (task, probe ops, left count, right count). Final program logged with region count and CALL count (must be 0 for C).
5. Metrics: per battery prereg section 4 (12 metrics). Carried state: none across tasks for C (each task grows fresh; the hypothesis has no library). Transfer pair: carried vs fresh will be identical; report both.

## 3. Predictions (from review, frozen)

- T0 2x+1: SOLVE via repair chain. Trace: REPAIR events only, no SPLIT.
- T1 abs: SOLVE via split. Trace: REPAIR attempted and shown failing the no-breakage check, then one SPLIT on [IN0, PUSH 0, LT], each branch repaired. Final: 2 regions, 0 CALLs.
- T2 mod3: SOLVE via repair. Trace: REPAIR only.
- T3 parity: SOLVE via repair. Trace: REPAIR only, residual over joint input.
- T4 nested abs: SOLVE via nested splits. Trace: at least 2 SPLIT events, nested. Final: 0 CALLs. KEY DISCRIMINATOR vs B.
- T5 fragment comp: SOLVE via splits. Trace: SPLIT events, 3 regions.

## 4. Kill bars

- K1: C implemented (repair + split, no population, no ranking). Verified by code inspection: no array of candidate programs, no score-based retention.
- K2: T0-T5 tested per battery protocol (frozen episodes, budget 1M evals or 300s per task, 3/3 byte-identical).
- K3: Predictions evaluated. CONFIRMED requires outcome match AND trace showing predicted mechanism via mandatory events (battery prereg section 5). Specifically: C on T4 must show 2+ nested SPLITs and 0 CALLs, else UNCONFIRMED (C-F2 fires if CALLs appear).
- K4: Pure Zag, zero Python invocations, zero em/en-dash bytes, 3/3 deterministic byte-identical.

## 5. Falsifiers (frozen from battery prereg)

- C-F1: C fails T0. Repair operator inadequate; C falsified.
- C-F2: C's T4 trace shows fragment CALLs instead of nested splits. Mechanism falsified.
- C-F3: Split count grows with episode count rather than true regions. Discipline falsified.
- C-F4: Repair maintains ranked population of candidate repairs. C rejected as genuinely different.

## 6. Determinism

Frozen seed: 0xC0FFEE. All op orders, probe orders, and episode orders are deterministic. 3 runs must be byte-identical.

## 7. Governance

Pure Zag only. No Python anywhere (implementation, execution, analysis). No em dashes in committed files. Commits local, owned path `docs/lab/research-lead/overnight-20260928/hyp_c/` only. Use `git commit -- <path>` to avoid sweeping concurrent workers. Prereg committed alone before implementation.
