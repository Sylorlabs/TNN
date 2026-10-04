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
