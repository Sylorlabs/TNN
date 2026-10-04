# R33-N01P: imported-constant fault isolated; casts do not fix it

The sole native primary completed its observations and returned exit1 with6/15
width checks failing. Both clock calls returned -1. Read the full
[raw output](R33_NATIVE_N01P_RUN_PRIMARY_V1/supervisor.stdout) and
[machine result](R33_NATIVE_N01P_RUN_PRIMARY_V1/RESULT.json).

All three imported i32 constants produced pointer-like expected arguments both
implicitly and with an explicit `as i64`. Local i32 variables, local named i32
and i64 constants, an i32-returning function and literal controls matched: nine
checks. This rules out a general explanation that ordinary i32 widening alone
causes the observed failures. It implicates imported-constant visibility or
resolution/lowering in this pinned build; the exact compiler-internal cause is
not established. The two clock observations establish the helper's failure in
this exact fixture, not a theory about every Zag compiler.

Crucially, the proposed N01B cast-only oracle workaround is NOT validated. No
N01B primary has run. Its unexecuted BUILD01 must remain preserved while a new
build uses independently literal-valued expected outcomes and the relevant
cross-module assumptions are reviewed. Native code that consumes imported
constants outside assertions also requires scrutiny; an oracle-only edit must
not conceal corrupted operational inputs.

The driver never called V2 supervision or forked. Native exclusive mkdir
admitted the one root and nio_guard(2) bounded the fixture. Host runtime displayed
0.26seconds and peak RSS1,261,568bytes; CPU displays are rounded, RSS not contained.
All fifteen controls, both negative clock returns, exact source/import/compiler
identity, build and reservation are retained. V2/N01A and all older evidence remain
unchanged. This is disclosed reuse of known engineering failure shapes, not new
scientific evidence, a newborn learner or an architecture/capability improvement.

R27 remains canonical60423/restarts0, zero R33 training and no authority change.
