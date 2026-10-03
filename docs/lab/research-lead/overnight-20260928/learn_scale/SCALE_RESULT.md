# RESULT: Learning-to-Learn Scaling

Worker: Learning-to-Learn Scaling Worker.
Date: 2026-09-30 UTC.
Verdict: **SCALE-TESTED** (all frozen kill bars pass).

Prereg: `de63550fa` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`, see section 6).
Implementation: `lscale.zag` (this directory, pure Zag, pure ASCII).
Raw: `SCALE_RAW_1.txt` (md5 `50ec577d0a25c42c9b0d24861597959c`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git only; zero
Python invocations in source, build, execution, or analysis); zero
em-dash/en-dash bytes in wave files (byte-checked); prereg strictly
precedes implementation; commits local on `tnn-native-lab`, owned
paths only.

## 1. What was tested

Whether the schema transfer savings from TRANSFER-TESTED scale across
multiple related families, whether an accumulating transfer record
produces a decreasing examples-to-criterion curve, and whether the
learner rejects transfer on an adversarial unrelated family and
returns to fresh behavior.

Three forms (researcher-supplied): F0 CONST, F1 LIN, F2 EXC.
Six families: A-E are F1 LIN instances with distinct (a, b) and
disjoint subject ranges; X is F2 EXC (default 7, exception at
subj=5001 with obj=3), unrepresentable by F0/F1 once the exception
is in evidence. Three conditions: FRESH (reset per family),
RETAINED (sequential A,B,C,D,E,X, persistent state), CONTROL
(sequential, persistent state except uses[] frozen at 0).

## 2. Measured examples to criterion

| Family | FRESH | RETAINED | CONTROL |
|---|---|---|---|
| A | 20 | 20 | 20 |
| B | 20 | 11 | 18 |
| C | 20 | 8 | 18 |
| D | 20 | 6 | 18 |
| E | 20 | 5 | 18 |
| X (adversarial) | 20 | 20 | 20 |

RETAINED adopted forms: 1,1,1,1,1,2. FRESH X adopted form: 2.
CONTROL X adopted form: 2.

All numbers match the preregistered model predictions exactly
(prereg section 5: fresh 20s; retained 20,11,8,6,5; control
20,18,18,18,18; X 20/20/20).

## 3. Kill bar evaluation

- K1 (spec): PASS. Six families executed; emitted SPEC table matches
  the preregistered specs exactly (A a=2 b=1, B a=3 b=5, C a=1 b=0,
  D a=5 b=3, E a=2 b=9, X F2 d=7 exc 5001->3).
- K2a (decrease): PASS. Retained 20 > 11 > 8 > 6 > 5, strictly
  decreasing.
- K2b (per-family savings): PASS. Retained B..E (11,8,6,5) each
  below fresh (20).
- K2c (total savings): PASS. Retained total 50; 50*10=500 <
  600=100*6. Retained is 50 percent of fresh.
- K3a (rejection): PASS. RETAINED X: strikes[F1]=1 and adopted=2.
- K3b (return to fresh): PASS. Retained X cost 20 within
  [fresh 20, fresh 20 + 6].
- K3c (no wrong-form application): PASS. Retained X adopted=2, not 1.
- K2d (supporting, causal isolation): PASS. CONTROL B..E flat at
  18,18,18,18: no decrease without the accumulating uses[] record.
- K4 (purity and determinism): PASS. Pure Zag; zero Python; zero
  dash bytes; 3/3 byte-identical; exit 0; zero stderr.

## 4. Trace: the exact learner state responsible

### 4a. Positive transfer

The emitted trace lines give, per RETAINED family, uses_before for
F1 and the verification requirement V:

- A: uses_before(F1)=0 -> V=14 -> cost 6+14=20
- B: uses_before(F1)=1 -> V=7 -> cost 4+7=11
- C: uses_before(F1)=2 -> V=4 -> cost 4+4=8
- D: uses_before(F1)=3 -> V=2 -> cost 4+2=6
- E: uses_before(F1)=4 -> V=1 -> cost 4+1=5

The causal chain is: each family brought to criterion increments
uses[F1] (state offsets 16+4*form in the state block); the next
family's verification requirement is computed as
V = max(1, ceil(14 / 2^uses[F1])); smaller V means fewer examples
to criterion. The CONTROL condition freezes uses[] at 0 while
keeping every other mechanism identical (live form persistence,
refit, prior ordering), and its B..E costs are flat at 18. The
only differing state between RETAINED and CONTROL is uses[],
so uses[] is the state responsible for the decreasing curve. The
refit cost is constant (4); the entire curve comes from the
verification discount.

### 4b. Transfer rejection

On RETAINED X, the learner carries live F1 with uses[F1]=5. The
refit buffer is (5000,7),(5001,3),(5002,7),(5003,7). Fitting F1:
a=(3-7)/(5001-5000)=-3, b=7+15000=15007; check subj 5002:
-3*5002+15007=1, truth 7 -> fit FAILS (trace: refit=0).
The learner records strikes[F1]=1, sets live=-1, and KEEPS the 4
refuting examples as the discovery seed (it does not discard its
counterexamples). Discovery continues from example index 4; at
buffer size 6 the prior order tries F1 first (most used) and it
fails again on the buffer containing the exception, F0 fails, and
F2 fits (d=7, p=5001, e=3) -> adopted=2. Verification uses
V=14 because uses[F2]=0. Total cost: 4 (refit) + 2 (to BMIN) +
14 (verify) = 20, exactly the fresh cost.

So the rejection is implemented by three pieces of learner state
working in sequence: (1) the refit-fit predicate returning 0 on
the X buffer, (2) strikes[F1] incrementing to 1 with live set to
-1 (no F1 application on X, satisfying K3c), (3) the kept
refuting examples forcing F2 adoption in discovery. The cost
returns exactly to fresh behavior (20 = 20), not below it: the
learner gains no inappropriate transfer discount on the unrelated
family.

## 5. Interpretation

1. The transfer savings scale: five related families show a smooth
   20 -> 5 curve, a 50 percent total reduction versus fresh, driven
   by a single accumulating counter per form. This is a genuine
   learning-to-learn effect at the level of a learned prior over
   forms, isolated by the frozen-uses control.
2. Rejection is clean and cheap: one failed refit (4 examples),
   one strike, and the learner is back to discovery; the unrelated
   family costs exactly what it costs fresh, with the correct form
   adopted and the wrong form never applied.
3. The kept-counterexample rule mattered: if the refit buffer had
   been discarded, the discovery buffer would have contained only
   default-7 examples and F1 (a=0,b=7) would have been wrongly
   adopted for X. The design choice is load-bearing and is now
   evidence-backed.

## 6. Honest scope and limits

- Three researcher-supplied forms; the learner selects, fits,
  retains, and rejects, but does not invent forms. The V discount
  schedule V = max(1, ceil(14/2^uses)) is researcher-authored
  meta-policy; the learner accumulates the uses record but does not
  choose the schedule. Bounded L1/L2, not L3.
- Transfer is form reuse within the LIN family (novel a, b, subject
  ranges). No transfer across changed arity or task kinds.
- The adversarial family is learnable by a known form (F2); genuine
  open-form rejection (no known form fits) is out of scope.
- Synthetic workload, exact-match prediction, small scale.
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 7. Commit order verification

Prereg `de63550fa` committed alone before `lscale.zag` existed.
`git merge-base --is-ancestor de63550fa HEAD` passes at the result
commit (recorded in the commit message trailer of the result
commit).

## 8. Files

- `PREREG_SCALE.md` (de63550fa, frozen before implementation)
- `lscale.zag` (implementation, pure Zag, pure ASCII)
- `SCALE_RAW_1.txt` (md5 50ec577d0a25c42c9b0d24861597959c; runs 2, 3 identical)
- `SCALE_RAW_2.txt`, `SCALE_RAW_3.txt` (determinism evidence)
- `SCALE_ERR_1.txt`, `SCALE_ERR_2.txt`, `SCALE_ERR_3.txt` (zero bytes each)
- `SCALE_RESULT.md` (this file)
- `lscale` (built binary, not committed)
