# CLN-1 TNN arm notes

**Learner binary (pinned):** `coding/reflection/loop/work/learner`
sha256 `399bf907d06c111b1d62164f2fd826ffac524e6b9a3c3c5dca7ffea6e9669375`
(source `learner.zag` sha256 `950bc4b09fd118c790fdaa98c6576bbcd94bf0e32a38a32e416ff20cecfe475d`)

**Gen items (G1–G8, T1–T4):** `learner gen '<spec>' '<patterns>' '<demo>'`, single call each.
**Repair items (R1–R8):** `driver.py --budget 4` (current mainline default: budget 4 = 2x knee, mask=ab prune+branch-and-bound, fail-fast precheck on). Artifact = final-iteration source.

## Results: 15 pass / 5 FAIL

| Spec | Outcome | Mechanism |
|---|---|---|
| CLN-R3 (ARITY) | halt-noregen | patch-arity pads the missing arg with a guessed value (`sub(10,11)` → -1); the missing argument is underdetermined by the seed, test expects `sub(10,0)`. Learner cannot know the intended value. |
| CLN-R4 (SYNTAX) | halt-no-patch | Stray `{` makes znc report "unknown identifier in expression: {" — the misleading compiler message wins the deliberation (NAME+2 beats SYNTAX+1 brace-crosscheck), and there is no patch for it. Toolchain error-message defect, not a learner logic defect. |
| CLN-R7 (LOGIC_VALUE) | halt-noregen | LOGIC_VALUE strategy is regen-from-spec, but the spec "Repair the broken program…" is not a generable T-spec → GEN_FAILURE → halt. The learner cannot re-derive logic without a generable spec. |
| CLN-R8 (LOGIC_VALUE) | halt-noregen | Same mechanism as R7. |
| CLN-T3 (T4 sum 1..20) | UNKNOWN_GOAL | The goal phrasing is outside the learner's generable goal vocabulary (cf. T1|LOOP range_sum which it knows). Genuine capability boundary of current mainline. |

Per prereg §3, the 5 failed specs are excluded from blind judging (no passing TNN
artifact); the 15 passing specs proceed. Means in the verdict tables are computed
over the 15 common specs unless otherwise noted.

**Determinism note:** the learner is deterministic; a "retry" would reproduce the
identical outcome, so the single run stands as the measurement.
