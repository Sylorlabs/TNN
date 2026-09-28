# R32 Epistemic Qualification V3 — Rejected Evaluator Diagnostic

Status: **REFERENCE_ONLY / REJECTED_EVALUATOR_MISMATCH**

Three seeds (36100–36102) completed before stopping. The A control averaged 0.727273 resolvable correctness and 1.000000 genuine-ambiguity abstention. The authoritative R31 anchors are ~0.9698 hard resolvable and ~0.5717 ambiguity UNKNOWN. The control therefore missed resolvable behavior by -0.242527 and over-abstained ambiguity by +0.428300.

Full D averaged 0.623636 resolvable correctness, 1.000000 ambiguity abstention, and 0.107949 wrong commitment. Relative to this already-invalid A control, D changed resolvable correctness by -0.103636 and wrong commitment by -0.122821.

## Causal classification

**Evaluator construction / baseline mismatch**, not architecture. The simplified A route fails the required equivalence test before any R32 mechanism can be judged. Its strongly confident first-observation behavior commits before reproducing R31's learned reinspection/physical-probe path, while its synthetic irreducible evidence makes UNKNOWN trivial. The 100% ambiguity value is therefore suspicious by construction.

## Decision

- Reject this harness for architecture selection.
- Retain the R32 uncertainty representation as an unjudged candidate.
- Do not run the remaining three seeds: more samples of a failed equivalence control would not repair causal validity.
- Next run must import/reproduce the actual R31 sequential policy/evidence generator as A, then add B/C/D by ablation on the same evidence trajectories.
