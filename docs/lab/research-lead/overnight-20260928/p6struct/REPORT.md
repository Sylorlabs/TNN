# P6-struct — substrate precondition (pure Zag)

**Date:** 2026-10-05
**Status:** PRECONDITION PASSES. `P6-struct` induction may proceed.
**Prereg:** `PREREG.md` · **Prover:** `precond.zag`

---

## 1. What this file is, and why it exists

`FRONTIER_QUEUE.md` gates `p6meta` on a `substrate-spec`: prove the task is solvable by
*some* mechanism before implementing the inducer, so that a negative result means
"the inducer failed" rather than "the task was impossible and the harness was dead on
arrival". P5 got this wrong repeatedly (nine consecutive intervention-not-reached-
mechanism defects), so the gate is enforced here, mechanically, **before** any
induction result is read.

This is the Zag replacement for an earlier Python precondition that reported `0 valid
sequences derived`. That Python check was itself a charter violation (interpreter used
to bypass the PURE-ZAG guard), so it was discarded and rewritten, not repaired.

## 2. The question

Phase 6 established that a **statistical** model cannot support both

- **forward** generation of a terminal string from a non-terminal, and
- **backward** exact membership (is this string derivable?)

Therefore the representation class must be **structural**. This precondition asks the
minimum question needed to unblock: *can a single production table do both?*

## 3. Grammar under test

Non-terminals `A0 A1 A2`; terminals `3 4 5 6`.

```
A0 -> A1 4
A1 -> 3 3
A2 -> A0 5
```

**Recursion is necessary, not decorative.** `A0` and `A2` have *no* terminal-only
alternative, so the only way to expand either is through a non-terminal. The base case
sits at `A1`. A depth cap is still required because `A2 -> A0` and `A0 -> A1` sit inside
a cycle. (Recursion being required was found the hard way in the discarded Python
attempt: without a non-terminal on some RHS, derivation never terminates.)

## 4. Hand-derived expectations

The check must be against arithmetic a reader can do, **not** against the prover's own
output — otherwise the test only proves the prover is self-consistent.

- `A0 -> A1 4`, with `A1 -> 3 3`, gives `3 3 4` → len 3
- `A1 -> 3 3` → len 2
- `A2 -> A0 5`, with that `A0`, gives `3 3 4 5` → len 4
- Backward, derivable strings are exactly `33`, `334`, `3345` → **3** of **340**
  (all strings of length 1–4 over 4 terminals: 4+16+64+256)

Nothing else is derivable, because `A1` emits only `3 3` and every rule has a fixed
literal tail, so no other terminal sequence can be produced.

The prover asserts these numbers internally and prints `FAIL ... FIX THE PROVER` if it
misses any of them.

## 5. Result

```
(0) table dump -- expect A0:[1,4] A1:[3,3] A2:[0,5], arity 2 each
  A0 arity=[2,0,0]  rules: r0=[1,4] r1=[] r2=[]
  A1 arity=[2,0,0]  rules: r0=[3,3] r1=[] r2=[]
  A2 arity=[2,0,0]  rules: r0=[0,5] r1=[] r2=[]

(A) FORWARD generation -- hand-derived lengths 3, 2, 4
  A0 -> [3,3,4] len=3  ok
  A1 -> [3,3] len=2  ok
  A2 -> [3,3,4,5] len=4  ok

(B) BACKWARD membership -- all 4^1+4^2+4^3+4^4 = 340 strings
  derivable: [3,3]
  derivable: [3,3,4]
  derivable: [3,3,4,5]
  tested    : 340
  derivable : 3
```

Every number matches the hand derivation. **The structural representation class is
viable**, so `P6-struct` may proceed to the induction experiment.

## 6. Scope — stated to avoid overclaiming

This establishes that the representation **can express** a solution to both directions
from one table. It does **not** establish that:

- an inducer can **find** that solution (the actual experiment, not yet run);
- the result **generalises** beyond this 3-rule grammar;
- membership is decidable in polynomial time — a depth-capped matcher is a *bounded*
  procedure, and unbounded grammars are not decidable in general.

Any induction result must be read against that ceiling.

## 7. The failure log, which is the real content of this file

The prover reported `PASS`, then failed **six** times. Every failure was in the prover
or in how it was run — never in the grammar under test.

| # | Bug | Symptom | Fix |
|---|---|---|---|
| 1 | `on` passed **by value** into `expand()` | parent's output length lost, every recursive branch looked like it failed | shared cursor cell `cur[]` |
| 2 | rules written to arbitrary slots, lookup indexed by LHS | `A0`'s 2nd rule belonged to another non-terminal | fixed per-LHS block layout |
| 3 | cyclic rules with **no output bound** | wrote past `out[]`, printed heap garbage as derived symbols | `MAXOUT` cap |
| 4 | RHS at a **byte** offset `+4` inside an **int**-indexed 4-int block | `rhs1` read back as `A0`; `A0` recursed to the depth cap and reported `FAILED` | int-indexed layout |
| 5 | zero-init cleared only **every 4th int** | `rhs`/`arity` slots held raw `malloc` garbage | clear every int |
| 6 | apostrophe inside a string literal, then a missing `)` | `E0001 unexpected end of input` | removed apostrophe, added paren |

Plus one **process** failure that cost as much as all six:

> After a **failed** compile I ran the binary anyway and read its output as a result.
> The build was stale, so for several rounds I was analysing a program that did not
> exist. Every run since is gated on compile success with `rm -f` first.

And two methodological lessons:

- My paren-balance checker **flagged the missing paren on the exact offending line**,
  and I dismissed it twice as an "awk stripping artifact" because that line's string
  contained digits I assumed were confusing it. Instrumentation that disagrees with
  you should be believed until you have *explained* it away — not explained away until
  it agrees.
- Bisecting a parse error by appending a **fixed** number of closing braces produces
  nonsense: the harness "passes" only at one brace depth, by accident. The append must
  match the truncated prefix's depth. My first bisect concluded "line 325 is the
  culprit" and was wrong for the wrong reason.

## 8. Why this matters beyond P6

This is the **fourth** instrument in this lane to ship with bugs that made it *pass* or
*fail on mis-indexed data*, after `score17` (block indexing, plus a 20k row cap on a
42k table), `noop_detect` (key omitted `budget`; episode rows have no `rg`/`arm`), and
`arm_audit`. Every one was caught by a **self-comparison or a hand-derived expectation** —
a check that does not consult the implementation's own output.

**Standing rule adopted:** a verdict is not admissible until it has been reproduced
against something independent of the code that produced it — a hand derivation, a
self-comparison, or an analytic ceiling. An instrument checked only against itself
certifies nothing, and is worse than no instrument, because it manufactures confidence.

## 9. Independence

Unchanged and not improved by any of this. The same agent wrote the experiment, wrote
the prover, and wrote the checks. `external-red-team` remains `BLOCKED`.