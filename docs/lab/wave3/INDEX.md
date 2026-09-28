# Wave 3 — Post-toy investigations: index

20 parallel investigations to replace the toy system. Program law: no score tables,
no NxN scaling-as-progress, no RL reward-shaping as paradigm, no RNG in AI decision
paths, scaling of real mechanisms required, white-box throughout.

| # | Investigation | Verdict |
|---|---|---|
| 1 | [core-user-separation](core-user-separation/) | POSITIVE |
| 2 | [curiosity-substrate](curiosity-substrate/) | BLOCKED |
| 3 | [deliberate-recall](deliberate-recall/) | POSITIVE |
| 4 | [developmental-curriculum](developmental-curriculum/) | POSITIVE |
| 5 | [hypothesis-driven-exploration](hypothesis-driven-exploration/) | NEGATIVE |
| 6 | [hypothesis-state-substrate](hypothesis-state-substrate/) | POSITIVE |
| 7 | [learner-driven-switching](learner-driven-switching/) | POSITIVE |
| 8 | [lifecycle-as-advisor](lifecycle-as-advisor/) | MIXED |
| 9 | [native-structural-revision](native-structural-revision/) | POSITIVE |
| 10 | [non-toy-evaluation](non-toy-evaluation/) | POSITIVE |
| 11 | [perceptual-origins](perceptual-origins/) | NEGATIVE |
| 12 | [portable-runtime](portable-runtime/) | MIXED |
| 13 | [r27-consolidation](r27-consolidation/) | POSITIVE |
| 14 | [self-model-substrate](self-model-substrate/) | POSITIVE |
| 15 | [signed-memory-values](signed-memory-values/) | POSITIVE |
| 16 | [teaching-without-tables](teaching-without-tables/) | POSITIVE |
| 17 | [trace-composition](trace-composition/) | POSITIVE |
| 18 | [trace-op-semantics](trace-op-semantics/) | NEGATIVE |
| 19 | [unified-partition-slots](unified-partition-slots/) | POSITIVE |
| 20 | [whitebox-at-scale](whitebox-at-scale/) | POSITIVE |

## Headline results

- 14 POSITIVE, 2 MIXED, 3 NEGATIVE, 1 BLOCKED.
- Post-toy spine: unified memory slots + signed agency + selective audit; eliminative
  hypothesis logic; deliberate consolidation/promotion; symbolic recall + trace
  composition; native structural revision.
- Dead: HDE v1 (preregistered kill), prediction-based future-use advisory (redesign or kill),
  all table machinery, historical recovery of R27 perceptual params and trace-op semantics
  (proven unrecoverable from repo — leads: pre-git session files, codex_restore_v62).
- Blocked: curiosity-substrate (znc bug ZNC-2026-09-19-001); portable-runtime backends
  (wasm codegen, arm64 syscall lowering).

## Next
The single most important next experiment: integrate the five mechanisms into one native
system and run it through the developmental curriculum at 10x scale, scored by the
non-toy evaluation protocol's seven-control battery with preregistered kill criteria.
