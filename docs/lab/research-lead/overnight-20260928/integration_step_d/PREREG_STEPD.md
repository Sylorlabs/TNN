# PREREG: Integration Step D - Merge DEVINT1 and DEVINT2 Curricula

**Status:** FROZEN before implementation. Do not modify after implementation begins.

## Mission

Merge DEVINT1 and DEVINT2 curricula into one binary on the unified backbone.
Closes G1 functionally: "No single binary runs the full developmental curriculum."

## Background

**DEVINT1** (`devint_worker1/devint1.zag`):
- Morpheme stream learner, 11 stages (S1-S11)
- Lexicon, segmentation, concepts, rules, procedures, contradiction, inquiry, revision, memory pressure, delayed reuse
- Prereg: 4b50ff7d4
- W buffer: 16384 bytes

**DEVINT2** (`devint_worker2/devint2_learn.zag`):
- Rule store learner (subj/rel/obj triples), 7 stages (S1-S7)
- Foundation, interference, delayed reuse, soak, correction, memory pressure (two eviction policies), final probe
- Prereg: 29682e102
- W buffer: 8192 bytes

**Unified backbone** (`unified_learn.zag`):
- Router + procedure store + bridge + causal store
- 1892 lines, 65536-byte W buffer (per Step B report)

## Merge Strategy

**Approach:** Sequential composition in a single binary.

The merged binary will:
1. Run the DEVINT1 curriculum (all 11 stages) on the morpheme learner
2. Run the DEVINT2 curriculum (all 7 stages) on the rule store learner
3. Both share a single W buffer and single main()
4. No task IDs or stage labels reach the learner mechanisms
5. Single process, no resets between curricula (persistent learner)

**Rationale:** The curricula test different capabilities:
- DEVINT1: language-like development (segmentation to revision)
- DEVINT2: knowledge management (interference to eviction policies)

Running them sequentially in one binary demonstrates "one continuing learner"
experiencing both developmental trajectories without reset.

**Not in scope:**
- True architectural unification (different state representations)
- Porting to unified_learn.zag's specific router/bridge/causal store
- The Step B architectural incompatibility (2 vs 3 variables) is acknowledged;
  this merge is functional, not architectural

## Kill Bars

**K-D1:** Merged binary compiles with znc, zero errors, zero warnings.

**K-D2:** DEVINT1 stages produce identical output to standalone run.
  - Compare: S1 through S11 stage outputs
  - Must match byte-for-byte (excluding timing fields)

**K-D3:** DEVINT2 stages produce identical output to standalone run.
  - Compare: S1 through S7 stage outputs
  - Must match byte-for-byte (excluding timing fields)

**K-D4:** Single binary, single main(), no process reset between curricula.
  - Verified by inspection: one main() function, no exec/fork

**K-D5:** Pure Zag, zero Python, zero em-dash bytes in all artifacts.

**K-D6:** Determinism: 3/3 runs byte-identical (excluding timing).

## Test Plan

1. Build standalone DEVINT1, capture output to baseline
2. Build standalone DEVINT2, capture output to baseline
3. Build merged binary, capture output
4. Compare DEVINT1 section vs baseline (K-D2)
5. Compare DEVINT2 section vs baseline (K-D3)
6. Run 3x, verify byte-identical (K-D6)

## Files

- `PREREG_STEPD.md` (this file)
- `merged_curriculum.zag` (implementation)
- `STEPD_RESULT.md` (results)
- Baseline outputs in `/tmp` (ephemeral)

## Governance

- Owned path only: `docs/lab/research-lead/overnight-20260928/integration_step_d/`
- Commits local, never pushed
- No Python at any stage
- No em dashes in documentation
