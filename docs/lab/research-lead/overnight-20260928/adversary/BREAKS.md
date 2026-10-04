# ADVERSARY BREAK LEDGER (C5xx)

Each entry: claim id, prereg ref, minimal reproducer, observed exact failure,
determinism status. No fixes proposed.

## C501 AW-01 gtag-collision -- BREAK CONFIRMED, AS PREREGISTERED

Frozen: `c8_learn.zag:570` `plan_find` keys on the bare goal tag.
`:768-781` `compose` on a plan hit skips `learn_bindings` and `topo_g`.
`:458/534` `bind_find`/`learn_bindings` memoize family per bare NEED tag.

### Minimal reproducer
`docs/lab/research-lead/overnight-20260928/adversary/aw01.zag`, one learner
state L, four probes, world `(1,10,5)(2,10,5)(3,10,5)(1,11,2)(2,11,2)(3,11,2)`.
Ground truth for shape `[rel=10, ag=1, subj=1]` is COUNT = 1.

| probe | goal_tag | need_tag | nf | compose_rc | family used | answer |
|---|---|---|---|---|---|---|
| A | 7000 | 21 | 2 | 2 (built) | 0 RETRIEVE | {1,2,3} |
| B | 7000 | 21 | 3 | **1 (loaded)** | 0 RETRIEVE | **{} WRONG** |
| C | 7001 | 31 | 3 | 2 (built) | 2 COUNT | {1} CORRECT |
| D | 7002 | 21 | 3 | 2 (built) | 0 RETRIEVE | **{} WRONG** |

### Exact failure
- **B**: identical to C in shape and in every field value. Only the goal tag
  matches A. `compose` returns 1 (plan loaded) -- `learn_bindings` and
  `topo_g` are never called -- and B's 3-field need executes under A's stored
  family 0. `ret_gen(rel=10, obj=1)` finds nothing because no fact has
  object 1. Answer is EMPTY. Ground truth is 1.
- **D**: the plan *is* built fresh (compose_rc=2) and `topo_g` *does* run, so
  W1/W2 are NOT the cause here. The family is still 0, inherited from the
  binding memo keyed on need tag 21. `learn_bindings` guards the trial loop
  with `if(bind_fam(L,bi)<0)`, which is false, so `try_family` is never
  consulted and the memo stands. Answer EMPTY. Truth 1.
- **C** is the control: same shape, fresh goal tag AND fresh need tag, binds
  family 2 and answers correctly. The shape is legal; only the key is wrong.

### Why this matters
A need tag is bound to at most one family for the lifetime of learner state.
Any world where the same symbolic tag occurs in two structural roles -- which
is the normal case in a language with shared vocabulary -- silently returns
the wrong procedure for the second role. No decline, no error, no counter
moves. `compose` reports success (rc=1).

### Determinism
`zbuild --rep 3`: 3/3 byte-identical, rc=0,
sha256 `ac4caed49267f77886d0a66e2182de054ac320c36d928f69d9473b79257327b9`.

## C502 AW-02 arity cliff -- PREREG PARTLY WRONG, WORSE BREAK FOUND

**PREREG said** nneeds=5 would crash or contaminate answers. **That did not
happen.** All five needs answered correctly. Reported honestly: that specific
prediction was wrong, and the cause is malloc slack -- `z_alloc(16)` gets a
32-byte-rounded block from the OS allocator, so the 5th need's writes land in
slack. That is an accident of the allocator, not a guarantee of the design.
Extended to a sweep, which found three real breaks.

### Break A -- plan-record stride overflow corrupts the plan table (nneeds 5..8)
`plan_new` (`c8_learn.zag:590-592`) writes step `p` at `13000+pi*56+8+p*12`.
Stride 56 fits `p<=3`. Measured corruption of slot 1 (`L+13056`), fresh L per
arity:

| nneeds | slot1.gtag after | slot1.nneeds after |
|---|---|---|
| 4 | 0 (clean) | 0 |
| 5 | 0 | 21 |
| 6 | 1 | 22 |
| 7 | 2 | 23 |
| 8 | 3 | 24 |

The value written is the **LOWEST need index**, because `topo` (`:362-370`)
has no `break` in its scan and therefore emits the LAST ready node first.
So a single 5-need goal deterministically plants a phantom plan.

### Break B -- phantom plan for goal tag 0 (the "no plan" sentinel)
After one 5-need goal:
- `plan_find(L,0)` returns **1**, not -1.
- A subsequent legitimate **1-need** goal with `goal_tag=0` gets
  `compose_rc=1` ("plan loaded") and a **73-integer answer**:

```
31233123312331233123312331233123312331233123312331231003123113123312331233123
```

That contains `1000` and `1131`. The world contains only entities 1,2,3,5 and
relations 10,11. `execute_plan` read `nn=21` out of `slot1.nneeds`, ran 21
plan steps, and pulled operands out of the binding table. Reported as SUCCESS.

### Break C -- 5th distinct goal tag reports success with no plan
`plan_new` has 4 slots and returns -1 when full. `compose` (`:776-778`) does
**not** check the -1 and calls `execute_plan(pi=-1)`, which indexes `L` at
negative offsets, then returns 2 ("plan built").

| goal tag | compose_rc | plan_find | answer ints |
|---|---|---|---|
| 7300 | 2 | 0 | 4 |
| 7303 | 2 | 3 | 4 |
| 7304 | **2 (SUCCESS)** | **-1** | **0** |
| 7305 | 2 | -1 | 0 |

### Break D -- decline does not invalidate the answer buffer
At nneeds>=9 with distinct need tags, `compose` returns 0 (decline, 8-slot
bind table exhausted) but leaves `ans` holding the PREVIOUS goal's answer. A
caller that checks the return code is safe; a caller that does not silently
reads a stale answer. `ans_total_ints=32` in the n=9..12 rows is arity 8's
answer, not an answer to those goals.

### Determinism
3/3 byte-identical, rc=0, non-empty output.
sha256 `c7837f0459e6414bfba86d073be5f923f04444a0dfa654b45ae4fbcd4aee3748`.
