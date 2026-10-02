# ROUTER5_RESULT: H-ROUTER5 Task-Family Consistency Repair

**Verdict: H-ROUTER5 SURVIVES.** All frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER5.md` (commit `13a501fa9`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER5_RAW_OUTPUT.txt` (md5
`0bb790e8adfc5cf22786356c72254f8a`, 3 runs byte-identical)
**Implementation:** `router5_learn.zag` (induction machinery, threshold
compiler, and all H-ROUTER4 diagnostics copied verbatim; new sections:
task-family consistency diagnostic, SWAP curriculum fixture, SWAP audit
section in `main()`). `router4_learn.zag` not modified.
**Pure Zag. No Python.**

## Kill bar results

**K-R5-1 (SWAP detected): PASS.** On the X-R4-1 SWAP curriculum (exact
fixture ported from `r4_adv.zag`), the run emits
TASK-FAMILY-INCONSISTENCY for s0=1 (4 marks: CAUS vs PROC anchor) and
s0=2 (3 marks: PROC vs CAUS anchor). Bitmask tfam=3. The diagnostic fires
on both swapped families.

**K-R5-2a (honest silent): PASS.** Honest curriculum: query anchors
qk=1 PROC (2x PQ), qk=2 CAUS (2x CQ); s0=1 learn PL matches PROC anchor;
s0=2 learn CL matches CAUS anchor. tfam=0. No false positive.

**K-R5-2b (X-R1 tfam+merger): PASS.** X-R1 variant: tfam=1 (s0=1 fires);
MARK-MERGER still fires for CAUS_LEARN (bit 12 set); honest mergers_mask=0.
Both diagnostics agree on the X-R1 attack.

**K-R5-2c (confined tfam+sfanom): PASS.** Confined curriculum: tfam=1
(s0=1 fires for the CL re-mark); SINGLE-FAMILY-ANOMALY still fires
(sfanom=1, s0=2 has no learn marks). Both diagnostics agree.

**K-R4-1 (confined single-family): PASS** (unchanged). **K-R4-2 (honest
no sfanom false positive): PASS** (unchanged). **K-R4-3 (X-R1 merger
intact): PASS** (unchanged). **K-R4-4 (threshold 10/10): PASS**
(unchanged). **K-R4-5 (regression 16/16 + replay 18/18): PASS**
(unchanged).

**K-R5-3 (determinism): PASS.** Three consecutive runs byte-identical
(md5 `0bb790e8adfc5cf22786356c72254f8a`).

## What was repaired

**X-R4-1 (task-swap evasion):** New `audit_task_family` diagnostic.

Principle: the PROC/CAUS family assigned to a content type should be
consistent between its query form and its learn form, as expressed by the
curriculum's own marks. The curriculum's query marks serve as the anchor;
no external reference table is used.

Content-type mapping (researcher-supplied feature semantics, disclosed):
string-like content links plain-string queries (s0=0, qk=1) with
string-pair learn items (s0=1); triple-like content links plain-triple
queries (s0=0, qk=2) with triple-transition learn items (s0=2).

The SWAP preserves distributional shape (both families retain learn
tasks; each task spans one family), so the merger and single-family
diagnostics stay silent. But it breaks family consistency: string-pairs
marked CAUS_LEARN while plain strings are marked PROC_QUERY, and
triple-transitions marked PROC_LEARN while plain triples are marked
CAUS_QUERY. The new diagnostic surfaces both inconsistencies.

The diagnostic flags; it does not alter compilation or routing.
Faithful-compiler semantics preserved.

## Impossibility note (carried from prereg)

Reference-free swap detection is impossible: honest and SWAP curricula
are isomorphic under the PL<->CL permutation. H-ROUTER5 does not claim
otherwise. The repair is a within-curriculum consistency check, not a
ground-truth-free detector.

## Honest boundaries (carried from prereg)

1. The content-type mapping is researcher-supplied feature semantics, a
   general principle (family consistency per content type), not a frozen
   answer table.
2. Family consistency is a heuristic flag, not a correctness verdict. A
   legitimate curriculum assigning string-pairs to the causal learner
   would be flagged for researcher review, which is intended behavior.
3. An attacker who re-marks the query anchors consistently with swapped
   learn marks (coherent re-labeling) evades this diagnostic. That is
   correct: the curriculum is then internally consistent, and no
   within-curriculum check can distinguish it from a legitimate policy
   change. Residual fundamental limit, disclosed.
4. Content types without query anchors stay silent (cannot verify).

## Classification

Bounded L2+ structural learning with provenance diagnostics (unchanged
from H-ROUTER4). The new diagnostic is a within-curriculum consistency
check, not a correctness oracle. NOT L3.

## Governance

- Prereg `13a501fa9` strictly precedes implementation (verified via
  `git merge-base --is-ancestor` before commit; implementation files
  were uncommitted working-tree files at prereg time).
- Governance note: the prereg commit `13a501fa9` swept in 7 EXP6 files
  staged by a concurrent worker (broad index commit). Prereg content
  verified intact; ordering unaffected (no implementation existed yet).
  Recorded, not hidden.
- Pure Zag. No Python at any stage.
- `router4_learn.zag` unmodified. Only new files: `PREREG_ROUTER5.md`,
  `router5_learn.zag`, `ROUTER5_RESULT.md`, `ROUTER5_RAW_OUTPUT.txt`.
- No em dashes in new docs.

## Lineage

- H-ROUTER4 (DOWNGRADED by red team X-R4-1): induction, threshold
  compilation, merger, and single-family diagnostics retained verbatim;
  task-swap evasion repaired by family-consistency diagnostic.
- H-ROUTER5 supersedes H-ROUTER4 as the routing layer for unified-learner
  work.
- The SWAP fixture (`run_induction_swap`) is retained as the regression
  test for future red teams.
