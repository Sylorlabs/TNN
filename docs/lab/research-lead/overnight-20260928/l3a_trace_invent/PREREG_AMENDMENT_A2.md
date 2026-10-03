// PREREG AMENDMENT A2 - L3A-TRACE (pre-commit design correction)
// Date: 2026-09-30. Status: FROZEN upon commit. No code committed yet.
// This amendment fixes four defects discovered during diagnostic (pre-commit)
// testing. All diagnostics used /tmp scratch copies; no implementation commit
// exists. K1 unaffected (this amendment precedes any implementation commit).

// DEFECT 1: Beam width 120 cannot solve frozen training tasks.
// Diagnostic: with beam_w=120, T0 (x^2+x) reached only 2/7 (best [PUSH:2,IN0,MUL]).
// Depth-by-depth instrumentation showed the beam saturates with score-2 local
// optima ("2x" programs); at depth 3 (len-4 candidates), 140 programs strictly
// beat the needed prefix [IN0,IN0,DUP,MUL] (1/7, mae 21), filling all 120 slots.
// The exact 5-op solution was never generated. This is a search-config defect,
// not a mechanism defect.
// FIX: beam_w 120 -> 600 (frozen). Verified: T0 solves 7/7 at beam 600.

// DEFECT 2: T2 (A1: x^4+3x^2+1) not solvable by the frozen (score,mae) beam even
// with the invention enabled.
// Diagnostic: with hardcoded reified [IN0,DUP,MUL] and beam 600, phase-2 on
// x^4+3x^2+1 reached only 2/7 ([IN0,TCALL0,PUSH:1,ADD,DUP,MUL,ADD]). The exact
// 7-op solution's prefixes ([TCALL0], [TCALL0,DUP], ...) have 0/7 and mae ~2500
// (x^2 is far from the x^4-dominated target), so the beam prunes them before
// they combine. The beam instead follows [IN0,TCALL0,...] to a 2/7 local optimum.
// FIX: T2 -> x^4+2x^2+x+1. Rationale: the with-invention exact solution
// [IN0,TCALL0,PUSH:1,ADD,DUP,MUL,ADD] (7 ops) has mae-decreasing prefixes that
// the beam follows; verified 7/7 with invention, 2/7 without (beam 600).
// Without-invention minimum exceeds max_len 8 by construction analysis
// (x^4 needs 5 ops via [IN0,DUP,MUL,DUP,MUL]; 2x^2 needs 5; +x+1 needs 3;
// sharing insufficient to fit in 8).

// DEFECT 3: T0 (x^2+x) beam solution lacks the intended [IN0,DUP,MUL] segment.
// Diagnostic: with beam 600, T0 solves 7/7 but via [IN0,PUSH:1,IN0,ADD,MUL]
// (x*(x+1)), which is lexicographically smaller than any [IN0,DUP,MUL]-containing
// 5-op exact program. The recorded trace therefore cannot yield the intended
// segment. This is inherent: x^2+x = x(x+1) always admits the factored form.
// FIX: T0 -> y=x^2. The beam finds [IN0,IN0,MUL] (len 3, 7/7). The task remains
// a genuine training task (the learner must discover x^2 from scratch).

// DEFECT 4: T1 (x^2+3) unsolvable by the beam; DUP never survives lexicographic
// tie-break.
// Diagnostic: with beam 600, T1 reached only 2/7. The [IN0,DUP,MUL] prefix has
// 0/7 (x^2 never equals x^2+3) and loses to 600+ trivial score-1 programs.
// Separately: the beam's lexicographic tie-break always prefers IN0,IN0 over
// IN0,DUP (both compute (x,x)), so the detected segment is [IN0,IN0,MUL]=[1,1,5],
// never [IN0,DUP,MUL]=[1,8,5]. The SEGMENT-MATCH guard's [1,8,5] is unreachable.
// FIX: T1 -> y=2x^2. The beam finds [PUSH:2,IN0,IN0,MUL,MUL] (len 5, 7/7),
// which contains [IN0,IN0,MUL] at offset 1. Guard updated: [1,8,5] -> [1,1,5]
// (both compute "push x*x"; the guard still pins the intended semantics).

// FROZEN (post-A2):
// - T0: y=x^2, T1: y=2x^2, T2 (held-out): y=x^4+2x^2+x+1. x in 0..6, 7 episodes.
// - beam_w=600, max_len=8, expansion universe unchanged (23 base + TCALL).
// - Intended invention: [(IN0,0),(IN0,0),(MUL,0)] = [1,1,5] ("push x*x").
// - Intended T2 with-solution: [IN0,TCALL0,PUSH:1,ADD,DUP,MUL,ADD] (7 ops).
// - Bars (a)-(e), kill bars K1/K2/K3, and C0-A audit A1-A7 unchanged.
// - All changes precede any implementation commit. K1 holds.
