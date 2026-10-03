# PREREG Amendment A1 (pre-implementation design correction)

Date: 2026-09-30. Amends PREREG_L3A_TRACE.md section 6 (task battery) and the
design-intent paragraph. No implementation exists yet; no results have been
observed; no code has been written. This amendment is committed as a separate
dated addendum before the implementation commit, so K1 (all prereg material
strictly precedes implementation) still holds.

## Change

Held-out task T2 changes from y = 3*x^2 to y = x^4 + 3*x^2 + 1, x in 0..6
(7 episodes). Equivalently y = x^2 + (x^2+1)^2.

## Rationale

Design analysis of the frozen battery showed the original T2 (3*x^2) is solvable
in 5 base-VM instructions without any invention: [PUSH 3, IN0, DUP, MUL, MUL].
Bar (d) T-ABLATE requires the invention-disabled search to NOT reach exact
within the frozen budget (beam 120, max_len 8). A 5-instruction base solution
makes bar (d) vacuous: the bar would fail for a task-design reason, not because
the mechanism lacks the claimed advantage. The prereg's task battery is therefore
broken as written, and per the standing rule a broken prereg is amended
transparently and re-frozen rather than executed as if valid.

## Why the new T2 discriminates (construction analysis, no execution)

With the intended invention ([IN0, DUP, MUL], "push x^2", invoked as TCALL 0):
[TCALL 0, DUP, PUSH 1, ADD, DUP, MUL, ADD] computes x^2 + (x^2+1)^2 = x^4+3x^2+1
in 7 instructions, within max_len 8.

Without invention, every construction needs at least 9: producing x^2 costs at
least 3 instructions ([IN0, DUP, MUL] up to argument order); the value x^2 is
needed twice (once bare, once inside (x^2+1)^2), so either recompute (3+3) or
compute once and DUP (3+1); forming (x^2+1)^2 from a shared x^2 needs
[PUSH 1, ADD, DUP, MUL] (4); the final ADD (1). The cheapest sharing
construction is [IN0, DUP, MUL, DUP, PUSH 1, ADD, DUP, MUL, ADD] = 9
instructions. No factorization avoids the second x^2 instance: x^4+3x^2+1 has no
factorization over the base ops that reuses a single x^2 (unlike 3x^2 = 3*x^2
or x^3+2x^2 = x^2*(x+2), which the PUSH k trick defeats). Hence bar (d) is
non-vacuous: the frozen budget max_len 8 separates the two conditions.

## Bars affected

Bar (c) T-REUSE: unchanged logic (exact 7/7 on held-out T2 AND solution contains
TCALL of the reified name_id); the held-out task instance is now x^4+3x^2+1.
Bar (d) T-ABLATE: unchanged logic (score < 7 with invention disabled); now
meaningful. Bars (a), (b), (e) unchanged. Design-intent paragraph: phase-2 now
solves T2 in 7 instructions using TCALL (was: 5).

## Non-change declaration

No other section of the prereg is altered. The kill bars K1/K2/K3 are unchanged.
