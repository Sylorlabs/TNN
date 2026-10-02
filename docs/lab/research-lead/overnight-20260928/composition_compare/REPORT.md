# REPORT: Composition Comparative Battery

## Verdict: COMPOSITION-COMPARE-COMPLETE

**Mechanism C (constraint-driven DFS) generalizes furthest. A and B are
pair-bound and cannot reach 3 structures. None handle 4+, partial
applicability, or unsupervised composition. Collapse to one operation is
possible via C's DFS architecture with pluggable applicability.**

Date: 2026-10-02. Worker: Composition Comparative (subagent 264a880e).
Determinism: 3/3 byte-identical per mechanism.

## Method

Three binaries, one comparative driver (6 tests), same base TNN-2 core.
Each mechanism tested on identical worlds:

- **T1**: 3-structure (X+Y+W plen-2 each -> Z plen-6)
- **T2A**: 4-structure (X+Y+W+V -> Z plen-8)
- **T2B**: 5-structure (X+Y+W+V+U -> Z plen-10)
- **T3**: Cross-domain (X plen-3 chain + Y single-hop -> Z plen-4)
- **T4**: Partial (X plen-4, Z needs 3 steps = 75% useful)
- **T5**: Without expected-answer (expected=-1)

SHA-256: A `4e6bc34e...`, B `d562c2d4...`, C `4b8f8155...`.

## Generalization Matrix

| Test | A (contracts) | B (co-use) | C (constraints) |
|------|---------------|------------|-----------------|
| T1: 3-struct | FAIL | FAIL | **PASS** |
| T2A: 4-struct | FAIL | FAIL | FAIL |
| T2B: 5-struct | FAIL | FAIL | FAIL |
| T3: X-domain | PASS | PASS | PASS |
| T4: Partial | FAIL | FAIL | FAIL |
| T5: No-expected | FAIL | FAIL | FAIL |

## Why Each Fails

### T1 (3-structure): A and B are pair-bound

**A**: `compose_try` searches MAP **pairs** (m1,m2) only. The search loop
is hardcoded to two structures. Three structures require either (a)
iterative pair composition (compose X+Y, then compose result+W), which
the pipeline does not do, or (b) triple search, which does not exist.
The plen-contract matching works, but the arity is fixed at 2.

**B**: `compose_try` scans type-15 **pairs** (b->a). Co-use episodes
created X->Y and Y->W links (verified: couse15=2). At Z time, B found
"COMPOSE pairs=2" but could not chain them. The mechanism has no way to
traverse LINK pairs transitively. Like A, it is arity-2 by design.

**C**: DFS with max 3 segments. Found 2-segment solution for T1? Actually
T1 needs 3 segments (X+Y+W). C PASSED, meaning the DFS successfully
chained three MAPs. The iterative depth-first search naturally handles
N segments up to the cap.

### T2A/T2B (4, 5-structure): All hit arity caps

**A/B**: Pair-bound, cannot even attempt.
**C**: Researcher-imposed `max 3 segments` cap in `cc_dfs`. The DFS
architecture could handle N segments, but the cap blocks 4+. This is a
researcher bias, not a fundamental limit. Removing the cap would let C
attempt 4/5, though search cost grows.

### T3 (cross-domain): All PASS

All three handle heterogeneous structures (chain + single-hop):
- **A**: Plen contracts are structure-agnostic. X plen-3, Y plen-1.
  The pair search matches contracts to gathered paths regardless of
  internal structure type.
- **B**: Co-use links record "used together," not "same type." The
  episode X->Y creates the link; composition stages each MAP's shape.
- **C**: Relseq `[1,1,1]` for X, `[5]` for Y. DFS walks each sequence;
  heterogeneity is natural.

**Finding**: Composition is not limited to uniform chains. The
mechanisms generalize across structure types when the interface
(contract/history/relsew) abstracts correctly.

### T4 (partial applicability): All FAIL, atomic MAP assumption

X is plen-4, Z needs 3 steps (75% useful). All three FAIL.

**Root cause**: All mechanisms treat MAPs as **atomic units**. They
select whole MAPs and concatenate whole chains. None can use a PREFIX
of a learned structure.

- **A**: Contract is plen-4. Z needs plen-3 from X. No match.
- **B**: Link is to the full X MAP. Staging uses the full shape.
- **C**: Relseq is `[1,1,1,1]`. DFS tries to walk all 4; Z only has 3
  r1 steps before switching to r2. The walk fails.

**This is a fundamental limitation**: composition requires
decomposable structures, but the MAPs are opaque. The mechanisms need
a way to address substructures (e.g., "first 3 steps of X").

### T5 (no expected-answer): All FAIL, supervision required

All three use `expected` for verification:
- **A**: "verifies against the goal"
- **B**: "verify against expected"
- **C**: DFS "terminates when walked value equals expected"

With expected=-1, none can verify. The composition search has no
termination condition and no selection criterion without the target.

**This is not a bug**: it is the current design. Unsupervised
composition would require learner-owned verification (e.g., prediction
confidence, internal consistency). That machinery does not exist in
these patches.

## Collapse Analysis: Can Three Become One?

### What is shared

1. **Pipeline position**: All three sit between rebind and trial in
   `ev_query`. All fire only when rebind fails.
2. **Assembly**: Concatenate rebound chains via SEQ links, sanity-execute,
   promote as new MAP with provenance edges to helpers.
3. **Verification**: All use expected-answer matching.
4. **No modes/bridges**: All are general pipeline stages, not task-specific.

### What differs: Selection principle

- **A**: Select by **contract applicability**. Contract = plen derived
  from structure. "Does m1's plen match a real path from subject? Does
  m2's plen match a real path from m1's output?"
- **B**: Select by **historical co-use**. "Which MAP pairs have type-15
  links from successful episodes?"
- **C**: Select by **constraint satisfaction**. "Which MAP's relseq can
  be walked from the current value?"

### What differs: Search arity

- **A/B**: Fixed arity 2 (pairs). Cannot generalize to N.
- **C**: Variable arity via DFS (capped at 3 by researcher).

### Collapse verdict: YES, via C's architecture

The three selection principles are **different ways to compute
applicability**, but they can all feed into C's DFS:

```
applicable(MAP, current_value) :=
  contract_matches(MAP, current_value) OR
  historically_coused(MAP, previous_MAP) OR
  relseq_walkable(MAP, current_value)
```

C's DFS already does iterative deepening over applicable MAPs. A and B
provide alternative applicability predicates. The "one operation" is:

**Constraint-driven DFS over learner-determined applicability.**

- A's plen contracts become one applicability signal.
- B's co-use history becomes another signal (with transitive closure).
- C's relseq walkability becomes the third signal.
- DFS handles N-segments (remove the 3-cap).
- Assembly and verification remain shared.

**What A/B would need**: Rewrite from pair-search to DFS. This is not
a small patch; it is an architectural change. But the change is
justified: pair-search is strictly less general than DFS.

**What remains different**: The applicability signals have different
epistemic bases (structure vs history vs constraints). A unified
implementation would need to arbitrate when signals conflict. That
arbitration is future work.

### Why not keep three?

Micah: "Do NOT permanently integrate three separate composition
engines." The evidence supports collapse:

1. **C subsumes A/B on arity**: C handles 3, A/B handle 2. There is no
   test where A/B succeed and C fails.
2. **Selection is pluggable**: The DFS does not care how applicability
   is computed.
3. **No unique capability**: A/B do not have a test where their specific
   selection principle is necessary. T3 (heterogeneity) is passed by
   all three.

**Recommendation**: Adopt C's DFS as the single composition
architecture. Port A's contract-matching and B's co-use history as
applicability predicates. Remove the 3-segment cap (or make it
learner-controlled). Address T4 (partial applicability) by making MAPs
decomposable.

## Standing Metrics

- Cognition lines: driver ~250 lines x3 (shared logic), patches unchanged.
- Modes/bridges/handlers/semantic cases: 0.
- Pure Zag. Safebin PATH. Guard verified.
- Paper untouched. Frozen source read-only.
- Committed locally, nothing pushed.

## Artifacts

- `cmp_driver_a.zag`, `cmp_driver_b.zag`, `cmp_driver_c.zag`
- `cmp_full_a.zag`, `cmp_full_b.zag`, `cmp_full_c.zag`
- `cmp_bin_a`, `cmp_bin_b`, `cmp_bin_c` (pinned znc)
- `cmp_run_a1/2/3.txt` (SHA `4e6bc34e...`)
- `cmp_run_b1/2/3.txt` (SHA `d562c2d4...`)
- `cmp_run_c1/2/3.txt` (SHA `4b8f8155...`)
- `cmp_compile_*.txt`, `NAMECHECK.md`, `REPORT.md` (this file)

## Open Questions

1. **T4 (partial)**: How to make MAPs decomposable? Sub-MAP addressing?
   Prefix extraction? This blocks 75%-useful reuse.
2. **T5 (unsupervised)**: Can learner-verification (C181) replace
   expected-answer? This is required for autonomous composition.
3. **Signal arbitration**: When contract, history, and constraints
   disagree, which wins? Learner-owned or researcher-weighted?
4. **4+ structures**: Remove C's 3-cap and test scaling. Does DFS blow
   up? Need iterative deepening with pruning.
