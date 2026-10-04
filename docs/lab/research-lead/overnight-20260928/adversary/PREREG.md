# ADVERSARY-WORLDS PREREGISTRATION (C500-C5xx)

**Author:** adversary lane (isolated worktree `/Users/Shared/micah/Documents/TNN/.worktrees/adversary`)
**Role:** NOT a builder. Attack the frozen substrate. Report breaks only. No fixes, no repairs.
**Date:** 2026-10-03
**Target:** charter 106 assumptions; charter 109/164 (opacity), 110 (isomorphism), 111 (non-isomorphic transfer).

## 0. FROZEN SUBSTRATE (verified by me, byte-exact, brief section 7)

| Core | Path (under `docs/lab/research-lead/overnight-20260928/`) | Lines | sha256 first12 |
|---|---|---|---|
| COGOPS base arena | `cogops_rescueaware/c15_base.zag` | 174 | `fc1f6e73c43a` |
| COGOPS learner prefix | `cogops_learnosc2/c8_learn.zag` | 1331 | `750cb01d086f` |
| TNN-2 frozen ref (library slice 1..917) | `compression_exec/tnn2_frozen_ref.zag` | 917 | `7a24eff6bd4f` |

**Not modified.** Every world is a fresh `main()` concatenated AFTER the frozen
library. The originals are never edited. TNN-2's own `main()` (line 1357) and
its self-test battery (lines 918+) are excluded from the library slice so that
exactly one `main` exists in my translation units.

## 1. STRUCTURAL WEAKNESSES I VERIFIED MYSELF (source line citations)

Read in the frozen source, not taken on report:

- **W1 goal-tag-only plan identity.** `plan_find(L,gtag)` at `c8_learn.zag:570`
  compares only `get32(L,13000+pi*56)==gtag`. No arity, no shape, no needs, no
  links in the key. Plan table = 4 slots, 56-byte stride.
- **W2 plan hit skips ALL derivation.** `compose` at `c8_learn.zag:768-781`:
  on `pi>=0` it jumps straight to `execute_plan` with the STORED `(need_index,
  family)` pairs. `learn_bindings` and `topo_g` are never called. So a second
  goal with the same gtag executes under the first goal's family assignment.
- **W3 shape-only family selection.** `try_family` at `c8_learn.zag:484` decides
  family from `nf` and `nf==1+ns*3` and `ag==1` only. Relation identity is never
  consulted. fam0 accepts ANY 2-field need; fam2 accepts ANY 3-field need with
  field1==1.
- **W4 tag-keyed family memoization.** `bind_find(L,tag)` at `c8_learn.zag:458`
  keys the binding table on the need tag ALONE, 8 slots, and `learn_bindings`
  at `:534` only calls `try_family` when `bind_fam<0`. A need tag is therefore
  bound to at most one family for the lifetime of learner state `L`.
- **W5 Kahn emits the LAST ready node.** `topo` at `c8_learn.zag:362-370` scans
  `n2` upward with no break, so `fnd` ends as the HIGHEST-index ready need.
  Plan order is reverse-index among ties.
- **W6 hard arity cliff at 4 needs.** `compose` allocates `W=320` (=4x80),
  `OUTS=640` (=4x160), `SUBL=512` (=4x128), `ord=16` (=4x4), and `topo`/
  `topo_g` allocate `ind=16`, `placed=16`. The comment at `:346` states
  "nneeds <= 3". A 5th need writes past the end of every one of these.
- **W7 RETRIEVE truncation at 32 with a true count.** `ret_gen` at
  `c15_base.zag:94` stores at most 32 subjects (`if(n<32)`) but line 100 writes
  the UNCLAMPED `n` into `out[0]`. Every consumer then reads `n` values.
- **W8 unbounded kind-3 fan-in.** `apply_kind3` at `c8_learn.zag:441` writes
  `SUBL[ni*128+4+tot*4]` with no bound on `tot` across incoming links.
- **W9 node-id / frame-slot namespace collision.** `res_op` at
  `tnn2_frozen_ref.zag:179` reads `op>=1000` as a frame slot, `op>=0` as a
  node id. Node ids run 2..1023 (`alloc_node` at `:87`), so ids 1000..1023 are
  live operands that are silently reinterpreted. `t2_guard` at `:346` puts a
  LITERAL NODE ID in field 8, and `execute` at `:202` reads it through
  `res_op`.
- **W10 subject-blind inversion.** `bootstrap_miss` at
  `tnn2_frozen_ref.zag:763-788` scans node ids 1023 downward for facts whose
  RELATION is `r`, ignores the subject entirely, and if the last <=6 objects
  are all equal it concludes `s r v0` for the querying `s`.
- **W11 eviction tie-break.** `evict_node` at `:254` picks strictly-minimal
  `bid`, ties broken by first-in-scan starting from `hg(W,8)`; no protection
  beyond a decaying `ET_USE` clock.

## 2. OUTPUT DISCIPLINE (brief 4.0)

`_zag_raw_syscall` is INERT on this host. The frozen `c15_base.zag:52` `o_flush`
uses it. **I therefore redefine `o_flush` AFTER concatenating the frozen
sources**, so my copy shadows nothing (Zag concatenates; a later definition of
the same name is a redefinition error, so instead I never call the frozen
`o_flush` from my `main` -- see section 3). All my output goes through my own
`a_flush` which uses `_zag_print`. Every reproducer asserts non-empty output.

## 3. PREREGISTERED ATTACKS

Each world is pure Zag, sealed (no parameters read from the environment), and
prints a self-declared expected-vs-actual line.

### AW-01 `gtag-collision`
One learner state `L`. Goal A then goal B, **identical goal tag**, different
shape: the same need tag `T11` carries `nf=2` in A and `nf=3` with field1==1 in
B (i.e. a RETRIEVE need in A, a COUNT need in B).
- **Prereg prediction:** `compose(A)` returns 2 (plan built). `compose(B)`
  returns 1 (plan loaded) and `learn_bindings`/`topo_g` are NOT called for B.
  B's COUNT need executes under A's stored family 0, i.e. `ret_gen(rel, ag)`,
  and the answer record is a subject list for `(rel, 1)` instead of a distinct
  object count. **No decline, no error, no counter showing degradation.**
- **Kill bar:** any output where B's answer is a count. If B declines or errors
  loudly, the attack FAILS and I say so.

### AW-02 `arity5`
Single goal with **5 needs**, all `nf=2` (RETRIEVE, a legal family).
- **Prereg prediction:** `mat_inputs` writes `W+320` inside a 320-byte
  allocation; `topo` writes `ind/placed/ord` past 16 bytes; `SUBL`/`OUTS`
  overflow. Expected: heap corruption -- either a crash, or values that are not
  the world contents. Either outcome is a break because the substrate documents
  `nneeds<=3` and never bounds-checks.
- **Kill bar:** correct 5-need answer with no memory error.

### AW-03 `fanin-overflow`
Two RETRIEVE sources each with 40 subjects, both feeding one COUNT need via
incoming kind-3 links (a diamond/DAG, W8). Fan-in total = 80 subjects into a
128-byte-per-need `SUBL` region.
- **Prereg prediction:** `ret_gen` reports count 40 but stores 32 (W7), so
  `apply_kind3` reads 40 values per source (8 of them from the NEXT need's
  output record), `tot` reaches 80, and the write at `SUBL+4+80*4` is 324 bytes
  past the start of need 0's slot. Expected: the COUNT answer is contaminated
  with integers that are not objects in the world, or a crash.
- **Kill bar:** a correct distinct-object count AND every consumed subject is a
  real world subject.

### AW-04 `subject-blind-inversion` (TNN-2)
Teach 6 facts `(s_i, r, 7)` for i=1..6, six DISTINCT subjects, one relation.
Then `ev_query(999, r, -2, 0)` for a subject never taught.
- **Prereg prediction:** trial loop finds nothing (`t2_gather(999,...)` returns
  1 path, the trivial one, so no 2-hop), then `bootstrap_miss` returns 7 AND
  `ev_teach_in` writes a NEW FACT NODE asserting `(999, r, 7)`. TNN-2 answers a
  question about an unseen subject using only other subjects' facts, and
  persists the answer as an observation.
- **Kill bar:** `ev_query` returns -2 (honest miss) and creates no node.

### AW-05 `op1000-ceiling` (TNN-2)
Two identical sub-experiments in separate workspaces. E-small: 3 chained facts,
query the 2-hop endpoint -- trial loop promotes a chain graph. E-large: the same
3 chained facts, but preceded by enough `alloc_node` calls to push the chain
graph's LITERAL node ids to >= 1000.
- **Prereg prediction:** E-small promotes (a T_MAP node exists). E-large
  promotes NOTHING: `res_op` reads every literal as `fr_get(fr, litid-1000)`,
  which walks the frame pointer to node 0 and returns POLICY_ROOT's fields
  (`-1,0,0,0`), so every GUARD compares the subject against `0` and the graph
  fails closed with `-999999`. Reported as "no answer found" -- indistinguishable
  from a genuine ignorance. **Silent, total, unreported learning collapse at a
  hard node-id ceiling of 1000.**
- **Kill bar:** E-large promotes the same graph as E-small.

### AW-06 `evict-six`
Fill the arena to capacity with facts, then teach 6 more facts.
- **Prereg prediction:** fewer than 6 of the 6 new facts survive as queryable,
  because `evict_node` breaks `bid` ties by scan order and newly created nodes
  have `bid==0`, identical to each other and to other fresh nodes.
- **Kill bar:** all 6 new facts retrievable by `activate`.

### AW-07 `opacity` (metamorphic, charter 109/164)
World A and world B are **structurally identical**; every entity id, relation
id, operation id and world label is permuted. The world LABEL STRING differs
("ALPHA" vs "ZZQQ").
- **Prereg prediction:** byte-identical output. If they differ, human-readable
  vocabulary is leaking into behaviour.
- **Note:** the frozen cores contain no string literals and take no string
  input, so I predict PASS. This is an honest negative control and I will
  report it as such rather than as a break.

### AW-08 `iso-order` (isomorphic stress, charter 110)
Same facts, same structure, three surface changes:
(a) entity ids renumbered (isomorphism),
(b) observation order reversed,
(c) irrelevant distractor facts added on unused relations.
- **Prereg prediction (a):** byte-identical. **(b):** DIFFERENT. `bootstrap_miss`
  at `:764` scans node ids 1023 downward, i.e. it is recency-ordered, so which
  <=6 objects it samples is a function of insertion order; and `ret_gen`/
  `cnt_gen` return first-seen order. **(c):** different where a global
  quantity is read -- `ev_act` ranks by `bid` over the WHOLE edge set, so
  distractors change the policy chosen.
- **Kill bar for (b),(c):** all three variants produce identical answers.

### AW-09 `transfer-chain-to-tree` (non-isomorphic, charter 111)
The same relation `r` presented as (i) a chain `a-b-c-d`, then (ii) a tree
`b` with three children. Query the node under `b` in each.
- **Prereg prediction:** TNN-2's trial loop only assembles CHAINS
  (`t2_asm_chain` walks a single SEQ path) and single hops; a tree's answer
  requires the `t2_asm_count` path, which fires only via `t2_rels` +
  `t2_chain` at `:636-647`. So the answer is reachable but via a completely
  different code path with different trial counts -- i.e. the transfer is not
  structural, it is a template switch keyed on `di`.

## 4. METHOD RULES

- Pure Zag for ALL computation. Shell/git orchestration only.
- `zbuild.sh X.zag --rep 3` asserts 3/3 byte-identical stdout on every reproducer.
- Prereg committed BEFORE any run.
- Every failure preserved as evidence with a minimal reproducer (charter 158).
- Explicit pathspecs on every commit. Never `git commit -a`.
- Claim IDs C500+.
