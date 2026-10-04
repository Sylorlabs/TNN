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

## C503 AW-03 truncated RETRIEVE invents entities -- COUNT answers 2 instead of 1

### Mechanism (read in source, both defects confirmed)
- **W7** `ret_gen` `c15_base.zag:94` stores subjects only `if(n<32)` but line
  100 writes the **unclamped** `n` into `out[0]`. Consumers then read `n`
  values from a record holding 32.
- **W8** `apply_kind3` `c8_learn.zag:441` accumulates `tot` across ALL
  incoming kind-3 links with no bound, writing `SUBL[ni*128+4+tot*4]`.

### Minimal reproducer
`adversary/aw03.zag`. World (81 facts):
`(1..40,20,9) (101..140,21,9) (0,20,77)`.
Goal 7501: need0 = RETRIEVE(rel20,obj9); need1 = RETRIEVE(rel21,obj9);
need2 = COUNT(rel20, ag1, _) with two incoming kind-3 links from need0 and
need1.

### Exact failure
Probe T (single RETRIEVE, isolates W7):
- reported length **40**
- 32 entries are real world subjects
- **8 entries are `0`** -- the zero-filled tail of the 160-byte output record.
  Those are *invented entities*, and 0 is a syntactically valid id.

Probe F (the diamond, W7 + W8 combined):
- `compose_rc=2` (success)
- **count_REPORTED = 2, ground truth = 1**
- emitted records:
  `[40, 101..132, 0x8] [40, 1..32, 0x8] [1, 2]`

The 16 phantom zeros (8 per source) enter the subject set. Subject 0 is a
real subject with a real fact `(0,20,77)`, so the phantom subject contributes
object 77 and the distinct-object count goes from `{9}` to `{9,77}` = 2.

Note the fan-in total is 80 subjects written into a 128-byte-per-need `SUBL`
region (512 bytes total). That write did not crash -- malloc slack again --
so the observable break is the wrong answer, not the overflow.

### Determinism
3/3 byte-identical, rc=0, non-empty output.
sha256 `b0c278e0af88297ae13ad34c2482d392f819576001f14d6dadd07ed4e0342895`.

## C504 AW-04 subject-blind inversion -- BREAK CONFIRMED, AS PREREGISTERED

`bootstrap_miss` `tnn2_frozen_ref.zag:764` scans node ids 1023 downward for
facts whose **relation** is `r` and **never compares the subject**.

### Minimal reproducer
`adversary/aw04.zag`. Teach `(1,10,7) (2,10,7) (3,10,7) (4,10,7) (5,10,7)
(6,10,7)`. Then `ev_query(W, 999, 10, -2, 0)`. Subject 999 was never taught.

### Exact failure
```
fact_nodes_about_999_before = 0
ev_query_answer            = 7          <- PREREG PREDICTED
fact_nodes_about_999_after  = 1
ev_query_answer_2nd        = 7          <- now served by activate()
```
TNN-2 answers a question about a subject it has **no evidence for**, using
only facts about six *different* subjects, and then **persists the
hallucination as a fact node**. From the second query on, the fabricated fact
is served by the ordinary exact-hit path and is indistinguishable from a
taught fact. No provenance edge distinguishes it.

Controls both PASS (they must refuse, and do):
- relation 11 with mixed objects 7,7,7,8,8,8 -> `-2`
- relation 12 with a single fact (below the `k`=3 threshold) -> `-2`

So the defect is exactly "N recent r-facts agree" with no subject check, and
it fires at the documented threshold.

### Determinism
3/3 byte-identical, rc=0, non-empty output.
sha256 `b14e22a264acfa3b92663f68e847af57adbf36103eec40544c58fc3c45f3b8f8`.

## C505 AW-05 node-id / frame-slot collision -- BREAK CONFIRMED, AS PREREGISTERED

### Mechanism, isolated from any learner policy
`res_op` `:179`: `if(op>=1000) return fr_get(f,op-1000);` else
`if(op>=0) return ng(op,20);`. `alloc_node` `:87` hands out ids `2..1023`.

`adversary/aw05.zag` direct probe, one frame, two literals:

| literal | node id | stored value | `res_op` returns |
|---|---|---|---|
| low | 2 | 4242 | **4242 correct** |
| high | 1013 | 7777 | **0 WRONG** |

`fr_get(fr, 13)` walks `cur=ng(cur,4)` until `ss<4`, landing on node 0
(POLICY_ROOT) and reading its fields. A literal at id >= 1000 is never read
as a node.

### End-to-end: identical structure, only inert padding differs
Query `(1,10)`, absent. World chain `(1,11,2) (2,10,3)`; answer is 3.

| variant | padding facts | max live node id | answer | MAPs promoted | trials accepted |
|---|---|---|---|---|---|
| E_small | 0 | 0 | **3 correct** | **1** | 1 |
| E_large | 996 | 997 | **-2** | **0** | 0 |
| E_large | 1000 | 1001 | **-2** | **0** | 0 |

`trialstat` (tried*1024 + rejected) goes 1024 -> 3075: the candidates were
built and **all rejected**, because every GUARD compared the subject against
POLICY_ROOT's fields instead of the literal. So `t2_guard` `:346` stores a
literal NODE ID in field 8 and `execute` `:202` reads it through `res_op`.

The learner acquires procedures normally until node ids reach ~1000, then
**silently stops acquiring procedures**, and returns `-2`, which is the same
value an honest ignorance returns. No error, no distinct counter, no
distinguishable log entry.

### Determinism
3/3 byte-identical, rc=0, non-empty output.
sha256 `d1aee85aac526f9792c653870e868045a244c6891b7482dfb1706be29bb6ecb0`.

## C506 AW-06 eviction -- BLOCKER B7 CONFIRMED, THRESHOLD LOCATED

`evict_node` `tnn2_frozen_ref.zag:254` picks the strictly minimal `bid` and
breaks ties by first-in-scan from `hg(W,8)`. `is_prot` `:221` needs an ET_USE
edge with clk>0; `decay` `:153` drains those clocks.

`adversary/aw06.zag`: pad with N facts on relation 77, then teach 6 new facts
on relation 10, then query each. Fresh workspace per row.

| padding facts | live before | of 6 new facts correct | LOST |
|---|---|---|---|
| 1000 .. 1016 | 1000..1016 | **6** | 0 |
| 1017 | 1017 | 5 | 1 |
| 1018 | 1018 | 4 | 2 |
| 1019 | 1019 | 3 | 3 |
| 1020 | 1020 | 2 | 4 |
| 1021 | 1021 | 1 | 5 |
| 1022 | 1022 (arena full) | **0** | **6** |

Loss is exactly linear: one fact lost per live node beyond 1016. At full
capacity the learner **accepts six new facts and retains none of them**, and
every one of the six queries returns the wrong value. No error, no counter.
B7 is confirmed and its threshold is 1017 live nodes, not 6 sequential facts
in the abstract.

### Determinism
3/3 byte-identical, rc=0.
sha256 `b9a21eeca792935961aad7157f80609ece38237501acb773fb8c073a563aff5d`.

## C507 AW-07 opacity / rename metamorphic -- NEGATIVE CONTROL PASSES, NO LEAKAGE

Charter 109/164. Two COGOPS worlds, structurally identical, with every
entity id, relation id, goal tag and need tag permuted, and different world
LABEL strings ("ALPHA" vs "ZZQQ").

| | goal tag | need tag | compose_rc | answer |
|---|---|---|---|---|
| ALPHA | 7000 | 21 | 2 | `[3, 1, 2, 3]` |
| ZZQQ | 5555 | 88 | 2 | `[3, 901, 902, 903]` |

`answers_correspond_under_f = 1`. **No leakage of human-readable vocabulary
found**, exactly as preregistered. Reported as a negative control, not a
break.

**Boundaries of this negative result, stated because a bare pass would
mislead:** the frozen cores contain no string literals and read no string
input, so this only shows the integer machinery is name-blind. It says nothing
about the harness, which is full of literal ids and hand-written goals, and it
does not touch C501/C502, which are defects of id-SENSITIVE identity, not of
vocabulary.

### Determinism
3/3 byte-identical, rc=0.
sha256 `660eb07650163ae6bc05e1238649a7958b6481ea99e9792a5df662e7e453b0b2`.

## C508 AW-08 isomorphism BROKEN -- answer depends on insertion order alone

Charter 110. Same 7-fact set, only the teaching order differs:
`(1,10,7)(2,10,7)(3,10,7)(5,10,7)(6,10,7)(7,10,7)(4,10,9)`.
Query `ev_query(999,10)`, subject never taught.

| variant | order | answer | facts persisted about 999 |
|---|---|---|---|
| O1 | dissenter `(4,10,9)` taught FIRST | **7** | 1 |
| O2 | dissenter `(4,10,9)` taught LAST | **-2** | 0 |
| O3 | O1 plus 8 distractors on unused relations | 7 | -- |

**Same fact set, different answer, by order alone.** O3 confirms the effect
is specifically recency and not a count effect: irrelevant distractors change
nothing.

Mechanism: `bootstrap_miss` `:764` scans node ids 1023 **downward**, so the
at-most-6 objects it compares are the six most recently *allocated* nodes.
"The most recent r-facts agree" is an artefact of insertion order, and the
system then encodes that as a fact (O1 persists one).

### Determinism
3/3 byte-identical, rc=0.
sha256 `a4982756f3bbc62b9ef8340f9c2e63876110bbb6a5fa9459d21dcebe10ffab68`.

## C509 AW-09 non-isomorphic transfer -- single-valued answer TYPE erasure

Charter 111. `activate` `:140` scans tag-1 nodes matching `(s,r)`, keeps the
max-`bid` one, and returns `ng(W,n,28)`: **one i32**. `ev_query` returns one
i32. A question whose answer is a SET has no representation.

| world | true objects for (2,10) | answer | discarded |
|---|---|---|---|
| W-MULTI star `(2,10,3)(2,10,4)(2,10,5)(2,10,6)` | 4 | **3** | **3** |
| W-MULTI same facts, order reversed | 4 | **6** | 3 |
| W-SINGLE chain `(2,10,3)(3,10,4)(4,10,5)(5,10,6)` | 1 | 3 | 0 (correct) |

Two independent failures in one table:
1. **Type erasure.** The 4-object question returns one member, chosen by the
   `bid` tie-break, with no refusal and no signal that a set was needed. The
   chain is answered correctly *only because* its answer happens to fit the
   single-i32 type. So the chain "works" and the tree does not for a reason
   that has nothing to do with structure.
2. **Order sensitivity.** Reversing only the insertion order of the same four
   facts changes the answer from 3 to 6. The value returned for a 4-valued
   question is decided by node allocation order, not by the world.

### Determinism
3/3 byte-identical, rc=0.
sha256 `e0fc55a144a614b7de38e2a5a0890240696679522b406e6c81efbad54f7b9e86`.
