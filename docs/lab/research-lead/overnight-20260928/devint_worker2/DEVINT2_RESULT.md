# DEVINT2 RESULT: Developmental Integration Worker 2
## Delayed reuse, interference, correction, memory pressure in one persistent learner

Worker: Developmental Integration Worker 2
Date: 2026-09-29 PDT
Verdict: **BUILD-PASS** (all six frozen kill bars pass; see below)
Prereg: `29682e102` (frozen alone before implementation; strict ancestor of this result)
Implementation: `devint2_learn.zag` (pure Zag, no Python)
Raw output: `DEVINT2_RAW_OUTPUT.txt` (md5 9eb7754fd5bc72341f026e9a84a9058b, 29 lines)

Per Micah's 2026-09-29 directive this worker reports BUILD-PASS/BUILD-FAIL
only. No promotion to SURVIVES/BOUNDED/DOWNGRADED/KILLED is claimed; those
require the full 11-step frontier pipeline including independent red team.

## 1. What was built

One persistent continuing learner in a single Zag program, single process,
single main(). Stages are sequential code blocks; no process boundary exists
between stages, so no reset or recompilation between stages is structurally
possible. The learner exposes exactly two operations and never receives stage
labels, task IDs, or mode flags: learn(subj, rel, obj) and
query(subj, rel, expected). Episodes are integer-coded (subject, relation) ->
object; token encoding is disclosed as not under test.

Two twin rule stores run in the same process on IDENTICAL episode sequences
(mirrored learn/query/twohop), capacity 36 each:
- STORE-C: evicts by cognitive consequence:
  importance = 10*(correct - wrong) + 5*dependents - 8*contradictions + 1.
  Age (last_used, taught_tick) does not enter.
- STORE-R: evicts least-recently-used (min last_used tick).

Each rule record carries provenance and predictive books: subj, rel, obj,
correct, wrong, dependents, contradictions, last_used_tick, taught_tick,
superseded_obj, valid. Contradiction revises in place (old label kept in
superseded_obj); the slot is never freed. Retrieval is exact-match only in
v1 (no generalization/backoff; disclosed scope limit). Two-hop composition
uses an authored comparison operator; the LEARNED behavior under test is
premise retrieval, and each used premise registers a dependency link
(dependents++).

## 2. Frozen trajectory (from prereg 29682e102)

- STAGE 1 (foundation): teach 8 animal rules; immediate recall 8/8 (baseline).
- STAGE 2 (unrelated interference): teach 24 disjoint-key rules from
  plant/furniture/number/bird domains (three share relation legs=10 with
  animal rules on different subjects: relation-level interference check);
  query accuracy 24/24.
- STAGE 3 (delayed reuse): recall all 8 Stage-1 rules (no re-teaching since
  Stage 1; verified structurally by grep: zero learn_both calls on subjects
  1-6 outside Stage 1 teaching and Stage 5 contradictions); 6 two-hop
  compositions incl. one cross-domain (Stage-1 + Stage-2 premises).
- STAGE 4 (interference soak): 2 rounds x 24 Stage-2 queries. Makes Stage-1
  rules stale by age while they retain predictive value: the exact
  recency-vs-consequence dissociation.
- STAGE 5 (correction): contradict (cat,legs) 4->3 and (fish,eyes) 2->1;
  probe both; re-probe a 12-rule collateral sample and count changes.
- STAGE 6 (memory pressure): DIVERGENCE_CHECK (must be 0); flood both stores
  with 30 junk rules (taught once, never queried); 26 evictions per store by
  policy; record junk retained and probe-set last_used ticks.
- STAGE 7 (final probe): query the 8-rule valuable-but-old probe set on both
  stores; query the 2 corrected rules on STORE-C.

## 3. Raw results (from frozen binary, 3/3 byte-identical)

- S1_RECALL 8/8 (baseline)
- S2_QUERY 24/24
- S3_RECALL 8/8
- S3_TWOHOP 6/6
- S4_SOAK 24/24 24/24
- S5_CORRECTED 2/2
- S5_COLLATERAL 0
- S6_DIVERGENCE 0
- PROBE_LASTUSED 75 68 104 105 107 108 110 111 (all pre-flood ticks; junk taught at ticks 155-184, so all 8 probes are older than every junk rule)
- S6_JUNK_C 4 S6_JUNK_R 30 (STORE-C evicted 26 junk, kept all 32 pre-flood rules; STORE-R kept all 30 junk)
- S6_COUNT_C 36 S6_COUNT_R 36
- S7_PROBE_C 8/8 S7_PROBE_R 0/8
- S7_CORRECTED_C 2/2 (corrections survive pressure on STORE-C)
- STATEHASH S1..S7 present, ticks strictly increasing: 16, 64, 78, 126, 154, 184, 202; HC==HR through S5, diverging at S6 as designed
- Zero DIVERGENCE-WARN lines; zero stderr; exit 0

## 4. Frozen bar evaluation

- K-D2-1 (delayed reuse >= 5/6 two-hop, zero re-teaching): 6/6; structural grep confirms zero learn() on Stage-1 keys between Stages 1 and 3. PASS.
- K-D2-2 (interference: Stage-3 recall >= 7/8): 8/8. PASS.
- K-D2-3 (correction: 2/2 new labels, 0 collateral): 2/2 and 0. PASS.
- K-D2-4 (pressure: STORE-C >= 7/8 AND STORE-R <= 2/8 AND C > R strictly): 8/8 vs 0/8. PASS.
- K-D2-5 (determinism: 3/3 byte-identical, exit 0, zero stderr): PASS (md5 9eb7754fd5bc72341f026e9a84a9058b across 3 runs).
- K-D2-6 (persistence: single compile, single run, 7 STATEHASH lines with strictly increasing ticks, DIVERGENCE_CHECK = 0, sequential stages in one main): PASS.

ALL SIX PASS. Verdict: **BUILD-PASS**.

## 5. Answers to the assigned measurement questions

1. Does delayed reuse work, or does the learner need re-teaching? It works:
   8/8 exact recall and 6/6 two-hop compositions after 48 unrelated
   interference episodes plus a 48-query soak, with zero re-teaching.
2. Does unrelated interference destroy earlier learning? No: recall is
   unchanged (8/8 -> 8/8), including with shared relation names across
   domains under exact-match retrieval.
3. Do corrections propagate correctly or cause collateral damage? Correctly
   and locally: 2/2 corrected rules answer new labels; 0/12 unrelated
   predictions changed; superseded labels retained in provenance; corrected
   knowledge survives later memory pressure (2/2 on STORE-C post-flood).
4. Under memory pressure, does the learner keep what is predictively useful
   or just what is recent? The consequence-weighted policy (STORE-C) kept
   8/8 valuable-but-stale rules and evicted 26 never-queried junk rules; the
   recency policy (STORE-R) kept all 30 junk rules and evicted all 8
   valuable-but-stale rules (0/8), including recently corrected knowledge.
   This is a direct empirical dissociation: importance by cognitive
   consequence (predictive value, dependency, contradiction cost) preserves
   useful knowledge that importance by recency destroys.

## 6. Governance and disclosures

- Prereg 29682e102 committed alone before any implementation; ancestry
  verified (this result is a strict descendant).
- Pure Zag throughout: implementation, compile, runs, analysis
  (grep/cmp/md5 only). No Python anywhere.
- No em dashes in any documentation (byte-verified).
- Owned paths only: devint_worker2/PREREG_DEVINT2.md,
  devint2_learn.zag, DEVINT2_RESULT.md, DEVINT2_RAW_OUTPUT.txt.
- Binary built only in /tmp, never staged.
- Compiler warnings (2x A0102 ignored return value in learn_both) are
  non-fatal analyzer notes; build succeeded, behavior verified by the
  DIVERGENCE_CHECK = 0 twin-agreement line.
- Authored infrastructure not claimed as learned: the two-hop comparison
  operator, stage sequencing, integer episode coding, exact-match retrieval
  (v1 has no generalization/backoff).
- Scope limits: synthetic world; 2 deliberately false Stage-1 facts;
  capacity 36 chosen so pressure arrives only at the flood stage.
- This is a builder verdict (BUILD-PASS). Canonical acceptance requires the
  frontier pipeline: independent reproduction, baseline attack, OOD test,
  ablation, transfer, independent adversary, governance audit.
- Coordination: no Worker 1 trajectory material existed in the repo at
  prereg time; Worker 2 used the distinct sequence documented in the prereg
  (delayed reuse / interference / correction / pressure) under the shared
  integration vocabulary (one persistent process, no task IDs to the
  learner, no resets, no recompilation).

## 7. Exact commands (K-D2-6 documentation)

- Compile (once): /home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc docs/lab/research-lead/overnight-20260928/devint_worker2/devint2_learn.zag -o /tmp/devint2_run
- Run (3x): /tmp/devint2_run > /tmp/devint2_outN.txt 2> /tmp/devint2_errN.txt
- Determinism: cmp run1 run2, cmp run1 run3 (identical); md5sum run1 = 9eb7754fd5bc72341f026e9a84a9058b; stderr files 0 bytes; exit 0.
