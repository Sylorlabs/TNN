# EVIDENCE2: Evidence Summary (Experiment 1b, PREREG2)

## Hypothesis

Reflexive recall is broadly harmful; the fix is to route recalled strategies
through deliberation as evaluated candidates, never as reflexes.

## Phase 1: Harm demonstration

**Arms**: Z (random), P (optimal), R_home (reflexive, home KB), R_true (reflexive, regime KB).
**Runs**: 224 total, each twice, byte-identical (SHA-256 verified).

**Results** (median of 2 reruns):
- D1 TIDELOCK v2: R_home=600, R_true=600 (no harm). P=600, Z~114.
- D2 SHIFT: R_home=-1500, R_true=4500 (severe harm, R<Z). P=4500.
- D3 TOOL: R_home=45084, R_true=52000 (moderate harm). P=52834.

**A1** (`evidence/A1_harm_taxonomy.md`): Three harm categories (H1 inversion, H2 silent loss, H0 none).
**A2** (`evidence/A2_gap_quantification.md`): Gap tables per variant.

## The fix: `src/recall_delib.zag`

Shared deliberative module (committed after sealed family, per ordering):
- RECALL: retrieve matching heuristics.
- EVAL: score by claimed (if n<10) or observed mean.
- VERDICT: select action; if distrusted (observed < claimed/2 after 10 samples),
  explore alternatives systematically (5 samples each), then exploit best.
- No domain/scenario/regime branches. Pure Zag, deterministic, no RNG.

Domain agents (`agent_d_d1.zag`, `agent_d_d2.zag`, `agent_d_d3.zag`) wire the
engine to their worlds. All emit ordered RECALL→EVAL→VERDICT traces.

## Phase 2: Fix validation

**D_home** (K5): D= R_home in all domains (600, 4500, 60000). No degradation.

**Gap closure** (K2):
- D2: 90.0% (3900 vs -1500→4500).
- D3: 80.7% (50664 vs 45084→52000).

**A3** (`evidence/A3_neuter.md`):
- (i) 100% of contested turns change decision under EVAL neuter.
- (ii) D_accept (always-accept) falls to 0% closure (90%/80.7% drop).
- (iii) Zero trace mismatches.

**A4** (`evidence/A4_heldout.md`): Sealed held-out family (committed before fix).
- D2: 90.0% closure (100% of in-sample).
- D3: 77.3% closure (95.8% of in-sample).

## Kill bars

All six pass (see `evidence/BAR_RESULTS2.md`).

## Artifacts

- `src/`: All Zag sources (worlds, KB parsers, agents, deliberation module).
- `kb/`: Home and regime-correct KBs (committed verbatim).
- `worlds/`: 12 D1 + 12 D2 + 8 D3 variants, plus 8 sealed held-out.
- `worlds/sealed/SHA_LOG.txt`: Sealed family hashes (pre-fix commit).
- `runs/phase1/`: 224 runs, SHA-256 verified deterministic.
- `runs/phase2/`: 64 D runs.
- `evidence/`: A1, A2, A3, A4, BAR_RESULTS2.

## Independent audits (pending)

Per PREREG2, requires:
1. Blind hardcode auditor over `recall_delib.zag`.
2. Trace-only auditor (given traces, no simulator).

This implementer is depth 2/2 and cannot spawn auditors. Parent agent must dispatch.
