# Hypothesis D Result: MAP-Elites / Novelty Control

## Verdict

**D-TESTED.** Control validity: **VALID** (D-F1 and D-F2 did not fire).
Builder verdict: **BUILD-FAIL** on K4 (Python purity violation disclosed; see Governance).

## Outcomes (3/3 deterministic runs, byte-identical excluding WALL_MS)

| Task | Verdict | Evals | Best score | Solution / best program | Hidden |
|------|---------|-------|------------|------------------------|--------|
| T0 2x+1 | SOLVE | 39082 | 9/9 | [PUSH:1 PUSH:-2 IN0 MUL SUB] | 16/16 |
| T1 abs | SOLVE | 76477 | 17/17 | [IN0 PUSH:-2 IN0 MUL MOD NEG NEG] | 8/8 |
| T2 x mod 3 | SOLVE | 134414 | 17/17 | [IN0 PUSH:-3 ... MOD] (11 ops) | 17/17 |
| T3 parity | FAIL | 1000000 | 20/32 | [PUSH:9 IN0 IN1 PUSH:-4 ADD ADD MOD] | 23/39 |
| T4 nested abs (carried) | FAIL | 1000000 | 8/17 | [PUSH:9 IN0 MOD PUSH:1 ADD] | 0/8 |
| T5 fragcomp (carried) | FAIL | 1000000 | 9/17 | [PUSH:2 PUSH:-2 PUSH:-2 IN0 MOD MUL SUB] | 4/8 |
| T4 fresh | FAIL | 1000000 | 10/17 | [PUSH:-2 IN0 PUSH:-2 IN0 MUL MOD MOD] | 8/8 |
| T5 fresh | FAIL | 1000000 | 9/17 | [PUSH:2 PUSH:-2 PUSH:-2 IN0 MOD MUL SUB] | 4/8 |

Carry sizes (persistent archive): T0->654, T1->1790, T2->2988, T3->12068, T4->9980, T5->7064 elites.

## Control validity

- **D-F1** (fail T0): NOT fired. D solved T0 at eval 39082.
- **D-F2** (solve T4 or T5): NOT fired. Both failed (carried and fresh).
- The control is therefore **valid** as a conventional MAP-Elites baseline.

## Predictions vs outcomes

- T0 SOLVE: **outcome matches, mechanism UNCONFIRMED**. The solution
  [PUSH:1 PUSH:-2 IN0 MUL SUB] (computing 1+2x) was found via a single-OP
  replace (PUSH -9 -> PUSH 1) on parent [PUSH:-9 PUSH:-2 IN0 MUL SUB].
  The deceptive prefix [IN0 PUSH:2 MUL PUSH:1] was **never generated**
  (0 PREFIX_EVAL events in 4.4M evals). The predicted ADD-final
  construction did not occur. The P1 postmortem claim is not directly
  tested by this run.
- T1 FAIL: **prediction WRONG**. D solved abs (see Major finding).
- T2 SOLVE: **confirmed**.
- T3 SOLVE: **prediction WRONG**. The 8-op parity chain was not found
  in 1M evals (best 20/32). The search space is harder than predicted.
- T4 FAIL: **confirmed** (carried and fresh).
- T5 FAIL: **confirmed** (carried and fresh).

## Major finding: abs is straight-line solvable (T1)

D discovered **[IN0 PUSH:-2 IN0 MUL MOD NEG NEG]**, a 7-op straight-line
program that computes |x| exactly (17/17 train, 8/8 hidden).

**Verification.** The program computes mod_nonneg(x, -2x):
- x>0: x/(-2x) = -0.5 truncates to 0, so r = x. Result x = |x|.
- x<0: x/(-2x) = -0.5 truncates to 0, so r = x < 0, then r += -2x
  giving -x = |x|.
- x=0: divisor is 0, VM yields 0 = |0|.
The two NEGs are a double negation (identity). All ops are in the
frozen 0..12 universe (no CALL, no comparison, no jump).

**Implication.** The architecture review asserted that "the P1 op
alphabet has no comparison" and that abs "matches the straight line
limit", predicting T1 FAIL. This is **false**. The GENEXEC2 MOD
(nonnegative semantics) enables a sign-extraction trick via
truncated division. T1 does **not** discriminate conditional from
straight-line machinery. Any hypothesis that solves T1 via this
(or a similar) straight-line MOD trick has not demonstrated
conditional structure.

**Battery impact.** T4 (nested abs) and T5 (fragment composition) both
build on |x|. Since |x| is straight-line expressible in 7 ops,
T4/T5 may also be straight-line solvable (just harder to find;
D failed at 1M evals). The battery's discrimination matrix for
T1/T4/T5 should be re-examined. This is a **task-design finding**,
not a control flaw: D-F2 did not fire because D did not solve T4/T5.

## Construction traces (run 1, identical in runs 2-3)

- T0 SOLVE: parent [PUSH:-9 PUSH:-2 IN0 MUL SUB] (niche 21840),
  replace pos 0 with PUSH 1 (template 10) -> [PUSH:1 PUSH:-2 IN0 MUL SUB].
- T1 SOLVE: parent [PUSH:-9 PUSH:-2 IN0 MUL MOD NEG NEG] (niche 31105),
  replace pos 0 with IN0 (template 19) -> [IN0 PUSH:-2 IN0 MUL MOD NEG NEG].
- T2 SOLVE: parent [IN0 PUSH:-9 PUSH:-9 PUSH:-9 PUSH:-9 IN0 MUL DIV MUL ADD MOD]
  (niche 49398), replace pos 1 with PUSH -3 (template 6) -> solution.
- All solutions arose from single-OP replacements fixing a constant or
  input, not from the predicted prefix+ADD composition.

## Determinism

Three full runs (T0-T5 plus T4/T5 fresh reruns). Byte-identical on
all 44,094 deterministic output lines. Only WALL_MS lines differ.
K3 PASS.

## Governance

- Prereg commit 82aaed137 strictly precedes implementation (this result).
- K4 (pure Zag): **FAIL**. A python3 byte-check was executed on the
  prereg after it was written (2026-09-30). Disclosure does not cure.
  Builder verdict is BUILD-FAIL regardless of K1-K3.
- No em/en dash bytes in hyp_d files (shell-verified).
- Only owned paths (docs/lab/research-lead/overnight-20260928/hyp_d/)
  are committed.

## Raw artifacts

- HYP_D_RAW_1.txt, HYP_D_RAW_2.txt, HYP_D_RAW_3.txt (full traces)
- HYP_D_RAW_1.err, HYP_D_RAW_2.err, HYP_D_RAW_3.err (empty)
- hyp_d.zag (implementation), hyp_d_bin (compiled binary)

## Recommendation for the battery

The T1 result overturns a load-bearing assumption. Before T6 is
designed, the battery should replace or supplement T1/T4/T5 with
tasks that are **provably** not straight-line solvable in the
GENEXEC2 op set (accounting for DIV/MOD arithmetic tricks), or
explicitly re-scope them as "straight-line discovery" tasks rather
than conditional-structure discriminators.
