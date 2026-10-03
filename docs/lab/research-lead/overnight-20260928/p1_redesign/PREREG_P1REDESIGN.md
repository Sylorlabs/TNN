# PREREG: P1 Search Redesign (Behavioral Beam)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: F1 (GENEXEC2) repair. The GENEXEC2 wave (BUILD-FAIL) is frozen;
this redesign targets only the P1 search mechanism.

## 1. Failure analysis (from frozen GENEXEC2 evidence)

The P1 beam search (width 100, max_len 12, ordered by
(exact_match desc, mae asc, len asc)) systematically fails on simple
arithmetic tasks: T0 (2x+1) 0/9, T2 (x mod 3) 0/17, T3 (parity) 0/25.
Only T1 (|x|) solved, via P3.

Root cause, confirmed by code inspection of the frozen genexec2.zag:

(a) Deceptive prefixes. A prefix's value lives in its stack state, not
its output. [IN0, PUSH 2] (stack [x,2]) is the crucial stepping stone
for 2x+1 = [IN0, PUSH 2, MUL, PUSH 1, ADD], but its output (top of
stack = 2) is indistinguishable from [PUSH 2] (stack [2], a dead end).
No output-based score can distinguish a stepping stone from a dead end.

(b) Exact-match flooding. [PUSH 1] scores exact=1/9 on T0 by luck
(x=0 gives target 1). At depth 2, hundreds of "lucky constant"
programs ([PUSH c, DUP], [IN0, DROP, PUSH c], [PUSH c, PUSH j, DROP],
etc.) achieve exact>=1 and outrank exact=0 structural prefixes by the
(exact desc) primary key. The beam fills with constants; the path
through [IN0, PUSH 2] is pruned and never recovered.

(c) Non-monotonic MAE. Even MAE-primary scoring fails: the depth-4
prefix [IN0, PUSH 2, MUL, PUSH 1] (stack [2x,1]) has output 1 and
mae=72, looking terrible, yet is one ADD from the exact solution.
MAE cannot see one-step potential either.

Conclusion: any selection criterion based on output quality (exact
count or MAE) is fundamentally blind to prefix potential. The beam
must be organized by state, not by score.

## 2. New design: behavioral beam search

Replace score-ordered beam selection with state-space search:

- A program's identity for search purposes is its full stack signature:
  the tuple of stack contents (as sequences, bottom to top) across all
  train episodes. Two programs with identical signatures are
  observationally equivalent; keep only the shortest (first found on
  tie). This collapses redundant variants ([IN0, DUP] vs [IN0, IN0];
  [PUSH 1, PUSH 2, DROP] vs [PUSH 9, PUSH 2, DROP]) without any score.
- Search proceeds by increasing program length (BFS layers). At each
  layer, expand every retained program by every op in the fixed P1
  universe, compute signatures, and retain programs with unseen
  signatures.
- A program is a solution iff its output (top of stack) equals the
  target on all train episodes. Check every generated program; return
  the first (shortest) solution found. BFS guarantees minimal length
  among explored programs.
- Bound: cap the retained set at CAP programs (default 4000). If a
  layer exceeds CAP after dedup, evict by (exact_match asc, mae desc,
  len desc), i.e., discard the worst-scoring first. Scores are used
  ONLY for cap eviction, never for prioritization. This preserves the
  state-space coverage property whenever the cap is not binding.
- Determinism: fixed op order; ties broken by (len asc, program bytes
  asc). No randomness.

Why this fixes the failure:

- [IN0, PUSH 2] has stack signature ([0,2],[1,2],...,[8,2]), distinct
  from [PUSH 2]'s ([2],[2],...,[2]). Both are retained; the stepping
  stone is never pruned by a score.
- Lucky constants ([PUSH 1], [PUSH 1, DUP], ...) collapse: [PUSH 1]
  and [PUSH 1, DUP] have different signatures ([1] vs [1,1]), so both
  are kept, but [PUSH 5, PUSH 1, DROP] ([1]) duplicates [PUSH 1] and is
  dropped. The constant flood is bounded by the number of distinct
  stack states, not the number of programs.
- The search is complete up to (max_len, CAP): if a solution exists
  within max_len and the cap is not binding on its prefix chain, BFS
  finds it. The cap is a memory bound, not a heuristic prune.

What this design does NOT do:

- No task-specific heuristics. The op universe, signature definition,
  and eviction order are fixed and generic.
- No input-dependence bias, no constant penalties, no lookahead. The
  only task-derived signal used in search is the solution check
  (output == target) and, under cap pressure, the eviction scores.
- This redesign covers P1 only. P2 (CALL composition) and P3
  (conditional assembly) are unchanged and out of scope for this
  prototype.

## 3. Prototype scope

A standalone Zag program (p1proto.zag) implementing:

- The GENEXEC2 stack VM restricted to P1 ops
  {PUSH, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP, SWAP, OVER}.
- The behavioral beam search above (max_len 12, CAP 4000).
- Test harness running T0 (2x+1, x in 0..8), T2 (x mod 3, x in 0..16),
  T3 (parity(a+b), a,b in 0..4) from the frozen task definitions.
- Output: per task, solution program (or best found), exact count,
  layers explored, retained-set size, determinism check.

## 4. Kill bars

- K1 (design): this prereg documents the failure analysis and the new
  design before any implementation. PASS if committed before code.
- K2 (prototype): p1proto.zag builds with znc, runs to completion,
  pure Zag, no Python at any stage, zero em-dash bytes in committed
  files. PASS if all hold.
- K3 (T0 solved): the prototype finds an exact (9/9) program for T0
  (2x+1) within max_len 12. PASS iff exact=9/9. This is the task where
  the old P1 failed (0/9 with best [PUSH:1]).

Secondary (informative, not kill bars): T2 and T3 exact counts,
retained-set sizes, layers explored. These diagnose generality but do
not pass/fail the redesign.

## 5. Honest limitations (frozen)

- Stack signatures use exact integer values; large integers from MUL
  chains create many distinct signatures. The CAP eviction handles
  this, but a pathological task could bind the cap and lose
  completeness. Mitigation (value clamping in signatures) is future
  work if needed.
- BFS by length explores many programs; worst-case time is
  CAP * |ops| * max_len evaluations. For the prototype task sizes
  this is acceptable (thousands of programs, tens of episodes).
- This redesign does not address P2/P3 or the library. It is a
  targeted repair of the P1 search mechanism.
- If K3 fails, the redesign is wrong and the failure analysis must
  be revisited; do not patch with task-specific heuristics.

Verdict: REDESIGN-PROTOTYPED iff K1, K2, K3 all pass.
Otherwise REDESIGN-BLOCKED with the failing bar named.
