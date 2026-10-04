# REPORT: PROPERTY-ZAG

Lane `propertyzag/`, branch `lane/propertyzag`, worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag`.
Prereg commit `e84ace3fe` (PREREG.md + NAMECHECK.md, ALONE, pre-implementation).
Infrastructure commit `14a09bc1f`. This report: see the final commit.

Frozen inputs, unmodified, sha256 first 16:

```
a29972ca8183b285  compression_exec/tnn2_frozen_ref.zag   (1591 lines)
750cb01d086f0f4e  cogops_learnosc2/c8_learn.zag          (1331 lines)
fc1f6e73c43ae8e4  cogops_rescueaware/c15_base.zag        (174 lines)
```

All computation pure Zag. `python`/`node`/etc unreachable and never invoked,
by name or absolute path. Shell used only for worktree creation, `cat`
concatenation, `sed -E -f`, `znc`, running binaries, `sha256sum`, `cmp`,
`grep`, `git`.

## VERDICT

**INFRASTRUCTURE-BUILT, REAL VIOLATIONS FOUND.** All ten kill bars K1-K10 are
met except one explicit sub-case of K5, which is a declared unrepairable class
and is reported as such (below). Verdict is not a pass/fail on the frozen
cores: the cores were not modified and are not claimed to have been improved.

## What was built (2670 lines of pure Zag, 3 binaries, all 3/3 byte-identical)

| binary | sha256 of stdout, 3/3 identical | bytes |
|---|---|---|
| `build/pz_bat` | `dd071680af370cacb326fd811dc0f82a1a4af5f16fd51884af3b20d370359427` | 6028 |
| `build/pz_meta` | `719f53cc9475144048fc5dd1611166742313d78fef2c36399f6cda6df37b0cb2` | 583 |
| `build/pz_diff` | `b9935cf8bf33066d71029cf433a9bc80edfb3f9ba0a9114bbf940edfd942e1d7` | 1453 |

Every binary uses `_zag_print` only and asserts emitted-bytes > 0 in-binary
(K1). The tnn2 rename round-trip audit runs on every build and prints
`ROUNDTRIP-OK`.

- `pz_lib.zag` xorshift32 PRNG (state warmed 8x, outputs masked to 31 bits),
  little-endian i32 cells, one-buffer output formatting.
- `pz_desc.zag` layout-generic arena descriptor: header cells, two 1024-bit
  legal-value bitmaps, and a conditional reference-rule table. This is the
  whole per-arena knowledge base.
- `pz_bat.zag` the battery, 13 codes, `pz_scan` / `pz_report` / `pz_arena_hash`.
- `pz_act.zag` containment: `pz_act`, `pz_quarantine`, `pz_kill_edge_at`,
  `pz_rebuild_counts`.
- `pz_gen.zag` generators: topology, well-formed and adversarial; six
  charter-113 injection families plus four battery-soundness injections;
  Fisher-Yates permutations and record reordering; random worlds.
- `pz_oracle.zag` three independent oracles written from the contract.
- `pz_meta.zag` the four metamorphic transforms.
- `BUILD.md` documents the exact call sequence for another lane.

## Kill bars

| bar | result |
|---|---|
| K1 output non-empty | PASS, all 3 binaries, asserted in-binary |
| K2 3/3 determinism | PASS, all 3 binaries |
| K3 battery soundness (injected violation found for each code) | PASS for I01,I02,I03,I04,I05,I06,I07,I08,I09,I11,I13 (11 of 11 applicable codes; I10 is a static layout check, passed, and I12 is a run-level check, passed) |
| K4 quiet on clean | PASS: fresh `tnn2_init` 0, after a real 3-fact learn+query 0, 63 well-formed generator seeds 0, 63 well-formed c15 seeds 0 |
| K5 contain complete | PASS for 9 of 10 scenario classes; **MISS** for the I09 slot-alias class, which the prereg already declared NOT-REPAIRABLE-ENCODING. The post-repair re-scan still reports it. Reported, not hidden. |
| K6 continue, not crash | PASS: all 10 scenarios rc=0, explicit diagnostics naming code, index, action |
| K7 no hidden corruption | PASS: every scenario scanned BEFORE repair, runtime behaviour recorded separately |
| K8 metamorphic invariance | PASS, 4 transforms, 108 runs, zero hidden dependencies, and every arm is non-vacuous |
| K9 differential three-way | PASS with the preregistered exception: RET 2100/2100 agree, VFY 30/30, CNT 15/15; the deliberately-stale arm disagrees as predicted and is repaired |
| K10 clean build | PASS |

## REAL INVARIANT VIOLATIONS FOUND, WITH MINIMAL REPRODUCERS

### V1. PZ-I09 namespace collision, two independent halves (tnn2)

Half A, literal band. `res_op(W,f,op)` routes `op >= 1000` to a frame slot
while `alloc_node` mints indices up to 1023, so node ids 1000..1023 are
unreachable as literals. Minimal reproducer, 6 statements:

```
tnn2_init(W);  1000x alloc_node;         // ids 2..1001
lit = alloc_node(W);                     // 1002, inside the collision band
ns(W,lit,0,902); write_node(W,lit,4242,0,0,0);
fr = alloc_node(W); ns(W,fr,0,902); fr_set(W,fr,2,777);
res_op(W,fr,lit);                        // OBSERVED 777, INTENDED 4242
```

Observed: `REPRO-A res_op(frame,1002) = 777 intended-literal-value=4242
frame-slot0=777 wrong=1`. The runtime returned a FRAME value where a LITERAL
was intended. This is brief blocker B1, confirmed with a runnable reproducer,
and it is reachable from allocation pressure alone, with no researcher world.

Half B, slot alias. Frame operand encoding is `1000 + slot`, decoded by
`fr_get` as a node index, but the node table is `[0,1024)`. Slot 24 therefore
decodes to node index 1024, whose record starts at byte `64 + 40*1024 = 41024`,
which is exactly `eoff(0)`, the first edge record. Observed:
`REPRO-B node1024.field1=1 edge[0].kind=1 aliased=1`. Any frame slot index at
or above 24 reads the edge table. The frozen assembler only ever emits slots 0
and 1, so this is a latent encoding defect, not a live fault today; the
threshold is 24 and the arena size is 110656, so the largest reachable decoded
index is far out of bounds.

### V2. Silent corruption: a severed program reports SUCCESS (tnn2)

`execute` returns 1 (SUCCESS) whenever the next node has no sequence
successor and the tag is not the conditional opcode. Two frozen paths reach
that state with no diagnostic:

(a) eviction. `evict_node` clears every edge whose source OR target is the
victim. A victim inside a program therefore truncates the chain. Minimal
reproducer: assemble a 2-step chain, `promote_graph` it, then
`t2_kill_edge(cell,12,guard)` (exactly what eviction does).

```
intact:   execute = 1, value = 7003, full-chain value = 7003, correct
severed:  execute = 1, value = 7002, value-WRONG = 1
```

Same query, same runtime, both return SUCCESS, different answers, no
diagnostic. The runtime cannot distinguish "ran to completion" from "was cut".

(b) edge-table saturation. `seq_link` is `link_edge(W,a,12,b,0)` and discards
the `-1` that `link_edge` returns when the 4096-slot table is full. Saturate
the table, then assemble: the intra-program sequence link is silently lost and
the truncated program again returns SUCCESS with the wrong value. Observed
`ARM11b ... rc=1 value=8002 full-chain-value=8003 value-DIFFERS-FROM-INTACT=1
seq_link-return-value-ignored=1`.

### V3. PZ-I04 provenance loss is silent and unrecoverable (tnn2)

`log_ev` returns without writing when the cursor is at 128. After 200 `ev_teach`
events the cursor is 128 and 72 provenance records were dropped with no
diagnostic: `ARM10 events-requested=200 log-cursor=128 capacity=128
dropped-silently=72`. Not repairable: the information is gone. The battery
reports it as `NOT-REPAIRABLE-LOSSY`.

### V4. Stale coverage index, still selected (c8_learn)

`specialize_ret` records fact INDICES at specialisation time. When new facts
arrive for an already-covered relation, `ret_spec` cannot see them, while
`ret_version` keeps selecting it.

```
before add:  gen=0  spec=0  oracle=0  selected-version=2
after 3 new: gen=3  spec=0  oracle=3  selected-version=2   STALE=1
after re-specialise: spec=3  oracle=3  REPAIRED=1
```

The stale procedure is preferred over the correct generic one. Repair is a
single `specialize_ret` call, which is genuine system-invariant repair because
it re-derives the index from the world rather than editing the answer.

### V5. Silent output truncation in two frozen generic procedures (c15 / c8_base)

`ret_gen` counts every match but stores only the first 32, then returns the
uncapped count. Minimal reproducer: 40 facts sharing one (rel,obj).
`P6 subjects=40 ret_gen-returned=40 ret_gen-actually-wrote=32
oracle-returned=40 TRUNCATED=1`.

`cnt_gen` increments its counter only inside the `ns<64` guard, so it silently
returns 64 for 65 distinct objects. `P7 distinct-objects=65
cnt_gen-returned=64 oracle-returned=65 cnt_gen-WRONG=1`.

Neither is a disagreement about semantics, so the three-way differential
agreed with both. Both are truncation bugs found by comparing the RETURNED
value against the value actually STORED, which no amount of agreement between
implementations would have found.

### V6. c15 fact-store capacity drop is silent (c15)

`fact_add` returns without writing at 128 facts. `C15 at-capacity ...
after-overflow-add count=128 SILENT-DROP=1`, reported by the battery as
PZ-I11 AT-CAPACITY.

### V7. The twelve-code structural battery was blind (this lane's own negative result)

On the severed program of V2(a) the original PZ-I01..PZ-I12 battery reported
ZERO violations. An arena can be perfectly well formed by every structural
criterion and still be a corrupt structure, because the corruption is in the
RELATION between the owner and the owned program. Amendment A1 adds PZ-I13
STRUCTURE-OWNERSHIP / PROVENANCE CLOSURE: the multiset of facts licensed by
the program's control-flow closure must equal the multiset licensed by its
owner. It detects the severance (`closure-facts=1 owner-facts=2`), produces
zero false positives on ARM0 and on all 63 well-formed generator seeds, and
containment then removes the owner's licence so `ev_query` no longer returns
the corrupt value.

## Which frozen core is weakest

**`compression_exec/tnn2_frozen_ref.zag`, on containment.** It is the only one
of the three that constructs and interprets programs, and it is the only one
that can return a confident wrong answer: two distinct frozen paths (eviction,
edge-table saturation) make `execute` return SUCCESS on a severed program.
`c8_learn.zag`'s defects are recoverable (a stale index, one re-derivation
away). `c15_base.zag` has only fixed-capacity truncation, with no execution
machinery to corrupt. Ranking on this axis: tnn2 clearly weakest, c8_learn
second, c15_base strongest. `tnn2` is also the only one whose defects are
silent at the point of failure.

## SYSTEM-INVARIANT REPAIR versus COGNITIVE SELF-REPAIR

BUILT HERE, and only this (generic runtime machinery, no knowledge of meaning):

- header live-count and edge-count reconciliation from the tables
- liveness-flag normalisation
- dead-endpoint and impossible-kind edge neutralisation, slot freed, ledger
  kept honest
- quarantine tombstoning of structurally invalid nodes (illegal tag, dead
  reference, dependency cycle, frame cycle, broken ownership closure) with
  incident-edge sweep, mirroring the frozen core's own eviction sweep
- record compaction in record-mode arenas
- index re-derivation for the c8 coverage tables, by re-running the frozen
  `specialize_*` against the world

DELIBERATELY NOT BUILT HERE, and must be learner-owned: deciding that a
structure is WRONG and forming a replacement. `pz_act` never invents a value.
Where containment makes a structure unusable the honest outcome is NO ANSWER,
and every action line says so. `ev_query` returning "no answer" after
quarantine is the intended behaviour, not a failure.

## BOUNDARIES

- Small arenas only: node cap 1024, edge cap 4096, fact cap 128, capability
  coverage 16 relations. Nothing here bears on 5k/10k MAP scaling, and V1 half
  B gets WORSE with scale, not better.
- The battery reads structure. It cannot detect a wrong answer that is
  structurally well formed except through PZ-I13's ownership closure, and even
  that only sees truncation, not a program that is intact and answers wrongly.
  Differential and metamorphic arms exist for that reason.
- The metamorphic arms drive the engine through `ev_query`, which supplies the
  target. They test the structure machinery (assembly, verification,
  promotion, reuse), not the miss policy and not trial-and-error discovery.
- The frozen cores were not modified. Every defect listed is a source-level
  fact about the frozen bytes, reproducible from the reproducers above.
- `pz_arena_hash` proves structural preservation of a repair, not behavioural
  equivalence of behaviour.
- The three metamorphic invariants that PASSED here do not generalise to
  questions with multiple valid structures; every query used has a unique
  correct answer, which is a deliberate restriction.

## NEXT EXPERIMENT

1. Attach the battery to `cogops_learnosc2/c8_learn.zag`'s learner-state
   block L with a real descriptor (BIND table at 12744, PLAN table at 13000,
   stats at 13224). That block has plans, bindings and trajectories that no
   lane currently checks, and it is the most likely place for a stale derived
   index after the kind of revision `t2_revise_graph` performs.
2. Adversarial slot injection: drive frame slot indices into [24, 1024) and
   measure how far out of the arena the decode reaches, turning V1 half B from
   a static alias proof into a measured bound.
3. Extend PZ-I13 from truncation to a full answer-level closure: replay each
   promoted program against its licensed facts and compare, so an intact but
   wrong program is also caught. That is the invariant this lane is missing.
4. Cross-lane: publish the descriptor constructor for any arena so that
   containment becomes a standing gate rather than a per-lane retrofit.