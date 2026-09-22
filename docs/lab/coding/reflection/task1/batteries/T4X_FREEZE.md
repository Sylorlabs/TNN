# T4x battery — freeze record (2026-09-22)

**Status:** FROZEN. 8 novel-construct items, frozen before any challenger
generation (reflection PREREG §1.2). Any change needs a dated amendment with
Micah's re-approval.

## Amendment 2026-09-22 — provenance disclosure

The eight T4x **families** (recursion, popcount, nested triangle, sentinel
argv sum, character filtering, two accumulators, fizzbuzz dispatch,
run-length encoding) were specified in the reflection prereg. The eight
**concrete item texts** (exact spec wordings, test vectors, expected outputs
in `batteries/t4x.json`, and the reference solutions in `t4x_ref/`) were
authored during Task 1 setup on 2026-09-22 and were **not present in the
original prereg or the prior workspace** — the prereg named the families,
not the items. This is disclosed here rather than left ambiguous: the
novelty claim for T4x rests on (a) the constructs being absent from all
baseline training (audited below) and (b) the items being frozen before any
challenger generation, not on the items pre-dating the prereg.

## Design rationale

Each item requires a construct ABSENT from all baseline training, verified by
source audit of `coding/src/learner.zag` (sha256
`b7e74d1ebe6af2dd7b7863b77d2953a51637dd30b3158420b667d1ef0e74d9ef`):

| item | required construct | audit evidence of absence |
|---|---|---|
| t4x_01 | recursion (recursive fn) | no emitter defines/defines-calls a recursive fn; all loops are `while(i<n)` counted |
| t4x_02 | bitwise reasoning (n%2 / n/2 bit loop) | zero `&`/`|`/`^`/`<<`/`>>` in any emitted code string |
| t4x_03 | nested-loop 2D pattern output | no emitter prints multi-line 2D patterns; all outputs single values/lines |
| t4x_04 | sentinel-terminated argv scan | all emitted loops are counted; no `break`-on-value in emitted code |
| t4x_05 | char-class filtering of a string | emitters transform whole strings (upper/reverse) or count; none filter by class |
| t4x_06 | multi-accumulator, multi-line output | every emitter prints exactly one value + newline |
| t4x_07 | modular dispatch (divisibility cases) | no emitter branches on `%`-conditions |
| t4x_08 | run-length encoding (nested scan + string building) | no emitter builds strings from runs |

Spec wordings avoid all 12 `goal_concept` keywords (so the baseline's
whole-goal matcher cannot fire) and all gate triggers (audit, ledger, rng,
random, weaken, bypass, conceal, hide, self-change).

## Reference solutions

`t4x_ref/t4x_0N.zag` — each verified 2026-09-22 with the pinned toolchain
(`znc_linux_x86_64_abed8aa1 --no-analyze --no-zagd`): compiles rc=0 and
produces exactly the frozen `tests[].stdout` bytes above (t4x_04 verified on
4 argv vectors). These are the frozen oracle; the learner never sees them.

## Battery format

`t4x.json`: harness battery (`mode=gen`, `spec`, `tests` with `args`/`stdout`/`rc`),
compatible with the frozen loop-harness driver protocol (INTERFACE.md).
