# PREREG: PROPERTY-ZAG

Lane: `propertyzag/`. Branch `lane/propertyzag`. Worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag`.

Claim block: **C500-C5xx**. C377-C466 are contested and MUST NOT be minted.

## 0. Scope and epistemics

Build permanent property-based testing infrastructure for pure-Zag learner
arenas, then run it against three frozen cores. The infrastructure is the
deliverable; the findings are the payoff.

Standing rules, accepted as constraints on every prediction below:

- **The old implementation is NOT ground truth.** Differential tests report
  DISAGREEMENT and adjudicate against a third, independently written oracle in
  this lane. A two-way disagreement is never resolved by seniority.
- **The frozen cores are READ-ONLY.** Where a core must be linked into a
  harness that owns `main`, the core is copied with a mechanical, audited,
  word-boundary rename of exactly seven symbols (`z_alloc`, `get32`, `set32`,
  `emit`, `i64s`, `e64`, `main`, each prefixed `z2_`). Round-trip audit: applying
  the inverse rename to the derived copy must reproduce the original file
  BYTE-IDENTICALLY (sha256 equal). Recorded in `BUILD.md`.
- **`_zag_raw_syscall` is inert on this host.** Every output path in this lane
  uses `_zag_print`. Every run asserts `bytes_emitted > 0`.
- All computation is pure Zag. Shell/git only for orchestration, concatenation,
  hashing, diffing.
- No em dash or en dash bytes in any committed file.

## 1. Threat model: what the infrastructure must catch

A learner arena is a flat `[]u8` with several overlapping record tables and no
runtime type discipline. The failure modes that matter, from charter 112/113/166:

- silent corruption: a malformed structure that the runtime absorbs and then
  reports as success,
- stale derived state: an index that disagrees with the structure it indexes,
- silent capacity loss: an allocator that returns a failure the caller ignores,
- namespace collision: two record kinds sharing one integer domain.

## 2. Frozen invariants (the battery)

Twelve codes. The battery is layout-generic: it is driven by an i32 descriptor
block (`pz_desc_*`), so other lanes can point it at their own arena without
touching the battery.

| Code | Name | Statement |
|---|---|---|
| PZ-I01 | STABLE-IDENTITY | every node liveness flag is exactly 0 or 1; header live-node count equals the number of liveness flags set; no node index outside `[node_lo,node_cap)` is referenced by any live record |
| PZ-I02 | EDGE-ENDPOINT-LIVE | every live edge has `from` and `to` that resolve to live node indices, or lie in a descriptor-declared exempt domain (frame-op encoding, sentinel) |
| PZ-I03 | REF-VALID | every field listed in the descriptor reference table holds a value legal for its declared kind |
| PZ-I04 | PROV-PRESERVED | every live node tagged as learned structure carries at least one provenance edge (kind ET_DEP=1); any header provenance/event cursor sitting at its declared capacity is reported as `AT-CAPACITY` because the runtime drops silently |
| PZ-I05 | EDGE-KIND-LEGAL | every live edge kind is inside the descriptor's declared kind set |
| PZ-I06 | TAG-LEGAL | every live node tag is inside the descriptor's declared tag set |
| PZ-I07 | DEP-ACYCLIC | the sequence-edge (kind 12) subgraph over live nodes is acyclic and every node has at most one sequence-successor |
| PZ-I08 | FRAME-FOREST | the frame-link relation (op field resolved to a node) over live nodes is acyclic |
| PZ-I09 | NAMESPACE-COLLISION | no live node index falls in the frame-operand band `[frame_op_base, node_cap)`; no live operand decodes to a slot whose node index leaves the node table and therefore aliases another record table |
| PZ-I10 | ARENA-DISJOINT | node and edge record byte ranges are disjoint and both fit inside the arena |
| PZ-I11 | INDEX-FRESH | the edge table has no holes below its high-water mark (a hole is a leaked slot, i.e. silently lost capacity) |
| PZ-I12 | REPLAY-DETERMINISM | a canonical hash over live state only (`pz_arena_hash`) is identical across two runs of the same seed and differs across two different seeds |

`pz_arena_hash` covers: every live node's tag, ref fields and value fields; every
live edge's four words; the header cells listed in the descriptor. It must NOT
depend on free-slot positions, otherwise PZ-I11 repair could not be verified
semantically.

### 2.1 Frozen adapters

Generic battery plus per-layout descriptor constructors, which are the only
place a layout literal appears:

- `pz_desc_tnn2()` for `compression_exec/tnn2_frozen_ref.zag`
  (WSZ 110656, node 40B at `64+n*40` for n in [2,1024), edge 16B at
  `41024+e*16` for e in [0,4096), sentinel -1, frame base 1000, live-count
  header cell 20, edge-count header cell 24, liveness field 36,
  event-log header cell 28 with capacity 128, legal edge kinds 1..13,
  legal tags {0,1,2,3,20,21,30,101,102,103,104,902,999},
  reference table = node fields 4,8,12,16,20,24,28,32 all K_OP).
- `pz_desc_c15()` for `cogops_rescueaware/c15_base.zag`: fact-store arena
  (header cell 0 = count, records 12B at `4+j*12`, capacity 128). There are no
  nodes or edges; the battery degenerates to a fact-record scan (I01/I05/I06
  apply to the relation vocabulary, I11 to the count-vs-capacity relationship).
- `pz_desc_c8()` for `cogops_learnosc2/c8_learn.zag` learner-state block
  `L` (16384B, three 4248B capability regions, BIND table at 12744, PLAN table
  at 13000, stats at 13224). Per-capability adapter `pz_c8_stale_scan(L,A)`
  verifies each learned coverage index against the world fact store. This is
  the STALE-INDEX probe proper.

## 3. Frozen kill criteria

- **K1 OUTPUT-NONEMPTY.** Every binary must emit at least one byte. Asserted
  in-binary via a counter, and verified in shell by non-empty stdout.
- **K2 DETERMINISM 3/3.** Every binary byte-identical across 3 runs.
- **K3 BATTERY-SOUND.** The battery must find at least one injected violation
  of each of I01,I02,I03,I04,I05,I06,I07,I08,I09,I11 (I10 and I12 are static /
  run-level and are checked separately). Battery unsound if any injection is
  missed.
- **K4 BATTERY-QUIET-ON-CLEAN.** With no injection, on a freshly built
  well-formed arena, the battery must report ZERO violations. A false positive
  on a clean arena invalidates the battery.
- **K5 CONTAIN-COMPLETE.** After each of the six containment scenarios, the
  re-scan must report zero violations in that scenario's code class, the repair
  must be verified against `pz_arena_hash` (semantic multiset of live records
  preserved for all classes except the code classes that quarantine a node),
  and a healthy probe structure must still answer correctly.
- **K6 CONTINUE-NOT-CRASH.** Each scenario must exit rc=0 with explicit
  diagnostic text naming the code, the offending index, and the action taken.
  A scenario that crashes or that exits silently is a K6 fail.
- **K7 NO-HIDDEN-CORRUPTION.** For each scenario, the battery must be run
  BEFORE any repair, and the runtime's own behaviour under the same corruption
  must be recorded. If the runtime returns success while the battery reports a
  violation, that pair is logged as SILENT-CORRUPTION. Silent corruption is a
  FINDING, not a K-bar failure; the bar is that it is DETECTED and REPORTED,
  never hidden and never merely crashed on.
- **K8 METAMORPHIC-INVARIANCE.** For each of M1-M4 over the frozen world set,
  every answer signature must be invariant up to the declared map. A change is
  a HIDDEN DEPENDENCY finding (charter 164), reported, not suppressed.
- **K9 DIFFERENTIAL-THREE-WAY.** On every generated world, `*_gen`, `*_spec`
  and the independent oracle must agree on the semantic result, except in the
  deliberately-stale arm, where the disagreement is REQUIRED (frozen
  prediction: `*_spec` is stale on a covered relation after new facts are
  added, and agrees with the oracle only after a rebuild).
- **K10 CLEAN-BUILD.** Every binary compiles with the pinned znc, `--target
  macos-arm64`, and emits no forbidden-interpreter activity.

Any K miss is a BUILD-FAIL verdict for this lane. Findings are reported whether
or not the bars hold.

## 4. Seed schedule (preregistered, frozen before implementation)

Deterministic xorshift32, state seeded with `seed ^ 0x5bf03635`, warmed 8
times. No floats, no arrays, no library RNG.

| Range | Count | Use |
|---|---|---|
| 1 - 63 | 63 | random well-formed world topologies for battery-quiet and metamorphic arms |
| 101 - 163 | 63 | random malformed-reference injection schedules (which node/field gets which corruption, drawn from the six scenario families) |
| 201 - 215 | 15 | random distractor loads (relation-count and fact-count sweeps) |
| 301 - 331 | 31 | random entity permutations for the renaming metamorphic arm |
| 401 - 431 | 31 | random observation orders (Fisher-Yates with the same PRNG) |
| 501 - 515 | 15 | differential comparison worlds for ret/vfy/cnt |

Every emitted line carries its seed, so any failure is reproducible by
re-running that seed alone. `pz_seeded_*` entry points make single-seed
replay possible.

## 5. Frozen predictions

- **P1** `tnn2_frozen_ref.zag` violates PZ-I09 out of the box: `res_op` treats
  `op >= 1000` as a frame slot while `alloc_node` mints indices up to 1023, so
  node indices 1000..1023 (24 ids) are unreachable as literals, and the
  collision is REACHABLE because the assembler allocates more than 998 nodes.
- **P2** `tnn2_frozen_ref.zag` violates PZ-I04 under load: `log_ev` returns
  silently at cursor 128, so provenance is dropped with no diagnostic.
- **P3** `tnn2_frozen_ref.zag` violates PZ-I11 and PZ-I07 in the same way after
  one eviction of a sequence-linked node: `evict_node` clears edges whose
  target is the victim, `seq_nx` then returns -1, and `execute` returns 1
  (SUCCESS) for a truncated program. Frozen prediction: the wrong value is
  returned as a success.
- **P4** `tnn2_frozen_ref.zag` violates PZ-I11 when the edge table fills:
  `seq_link` ignores `link_edge`'s -1, dropping sequence edges silently, with
  the same truncated-program success path as P3.
- **P5** `c8_learn.zag` coverage indices go STALE: after facts are added for a
  relation that is already in `ret_cov`, `ret_spec` disagrees with `ret_gen`
  and with the oracle, and `ret_version` still selects the stale `ret_spec`.
- **P6** `c15_base.zag` `ret_gen` silently truncates: it counts past 32 subjects
  but stores only 32, and returns the untruncated count. Frozen prediction:
  `n` returned exceeds the number of slots written.
- **P7** `cnt_gen`/`cnt_spec` saturate at 64 distinct objects while still
  returning a larger count.

## 6. What is SYSTEM-INVARIANT REPAIR and what is COGNITIVE SELF-REPAIR

Preregistered boundary, reported explicitly in the final answer:

- **SYSTEM-INVARIANT REPAIR (this lane builds it).** Generic runtime
  machinery with no knowledge of what the structures MEAN: edge-table
  compaction to remove holes (PZ-I11), dead-endpoint edge neutralisation
  (PZ-I02), quarantine-marking of structurally invalid nodes
  (PZ-I03/I05/I06/I07/I08), and derived-index rebuild for the c8 coverage
  tables. This is `pz_act`.
- **COGNITIVE SELF-REPAIR (this lane does NOT build it, and must not).**
  Deciding that a structure is WRONG and forming a replacement: noticing that a
  MAP's answer disagrees with experience, superseding it, re-deriving a plan.
  That is learner-owned. `pz_act` must never do it; if containment prevents a
  structure from being used, the honest outcome is "no answer", not a
  researcher-authored substitute.

## 7. Frozen boundaries

- Small arenas only: node cap 1024, edge cap 4096, fact cap 128, capability
  coverage 16 relations. Nothing here is a claim about 5k/10k MAP scaling.
- Relation ids and node ids are opaque integers. No world literals in the
  battery, the generators, or the adapters.
- The battery reads structure. It does not execute cognition. It cannot detect
  a wrong answer that is structurally well formed; that is what the
  differential arm is for.
- `pz_act` repair is verified by multiset preservation, not by semantic
  equivalence of behaviour.