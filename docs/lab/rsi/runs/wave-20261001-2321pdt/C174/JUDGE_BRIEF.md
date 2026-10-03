# JUDGE_BRIEF.md: C174 lane, wave-20261001-2321pdt

RENDER_SHA: not yet committed (rendered before the eval-run commit; see commit id in the lane final report).
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE:
  1. Spec 550fa268b (SHARED-SUBSTRATE-COMPLETE, 619 lines): one keyed
     tag-61 store of pursuit/strategy outcomes, generic write sub_note,
     generic read sub_consec, serving decline, abandonment, retention
     input, trial reorder.
  2. Ledger C174 (SUBSTRATE-CONSOLIDATION, EMERGES, exploratory, no
     frozen prereg); C175 (UTILITY-DESIGN, design only); C180
     (DEDUP-DECLINE-INTEGRATION, decline gate retired, dedup subsumed
     decline); C181/C182/C183 (learner-owned reliability, adaptive
     threshold, source reliability, all exploratory).
  3. CONSEQ lane wave-20261001-2321pdt VALIDATION-PASS: Node2-v2 K-H3
     independently reproduced, consequence record causally necessary,
     scope honestly held to the re-entry template (not the shared
     store itself).
  4. Tonight's directive: the shared consequence substrate as a major
     hypothesis; scope boundary with the concurrent TNN3-SUBSTRATE
     lane (that lane owns the learner construction primitive,
     contradiction trigger, learner standing; this lane owns only
     the shared tag-61 store plus consequence-derived utility).

NEW_KNOWLEDGE_CLAIM: The shared tag-61 consequence store is validated as infrastructure on sealed worlds: one keyed store written via the generic sub_note path serves both trial reorder and retention input, consequence-derived utility judgments change behavior versus fixed bookkeeping (63 vs 103 attempts; 6/6 vs 3/6 held-out answerability), ablating the store reverts behavior to the fixed baseline byte-for-byte, and the Node2-v2 node-local consequence slots migrate to the store with byte-identical K-H3 behavior.

## What was done

Frozen prereg PREREG_C174.md (commit 134af1cb2, kill bars a-e,
seal procedure) before any implementation. Pure-Zag dev harness
(c174_sub.zag: tag-61 store, sub_note/sub_consec, abandonment
lifecycle, reclamation, sub_reorder, sub_utility, sub_victims).
Sealed worlds from frozen seed 20261001 (W-REORDER: 48 trials,
6 families; W-RETIRE: 5 pursuits, 10 structures, 6 held-out
queries), hashes committed (WORLD_MANIFEST.md) before any eval
binary ran. Three arms (S shared store, F fixed bookkeeping,
A ablation), K-H3 migration test, white-box self test.

## Verdict: VALIDATION-PASS

- (a) STORE-SERVES-TWO: PASS. W-REORDER: 121 writes (6 STRATEGY
  + 48 PURSUIT records), 294 reorder reads, same store. W-RETIRE:
  28 writes, 10 retention + 15 utility reads. Consumers obtain
  records only via sub_consec.
- (b) BEHAVIOR-CHANGE: PASS. Reorder: S [0 5 1 2 3 4] vs fixed
  [3 0 5 1 4 2], 63 vs 103 attempts. Retention: S victims
  [7 0 1 6 5] vs F [4 8 3 9 7], answerability 6/6 vs 3/6.
- (c) ABLATION-CAUSAL: PASS. A == F byte-for-byte
  (de193b844847bd73ef6894fe7745dca424ec2fe5432bdba821042e512cd291ae),
  S != F (6c33f7c4cca7833ee2b0bc5ed269f0d8c2007d810f9259ced0a4303783f431f8).
- (d) MIGRATION-COMPAT: PASS. M1 reproduces the K-H3 trace
  (30 30 30 30 30 45, guide 45); M2 byte-identical;
  MIGRATION_MATCH 1.
- (e) DETERMINISM: PASS. 3/3 byte-identical for all six binaries.

## Disclosed fix

After the seal, the `C174_EVAL arm=` metadata line was removed
from eval stdout so kill bar (c)'s whole-output SHA-256 compares
decision channels only (arm identity stays in filenames). No
prereg constant, world, or decision logic changed; the seal is
untouched. Documented in EVAL_RESULTS.md.

## Honest scope

Dev-harness validation of the store as infrastructure, not
TNN-2/TNN-3 integration. Reclamation exercised only in the self
test. Thresholds and weights are researcher scaffolding. No L3,
FW1-FW9, or generality claims. C174 graduates from EMERGES
(exploratory) to validated-on-frozen-bars; the shared substrate
remains a hypothesis for broader worlds, not an established
general mechanism.

## Evidence paths

- PREREG_C174.md, EVAL_RESULTS.md, WORLD_MANIFEST.md (this dir)
- Sources: c174_sub.zag, c174_gen.zag, c174_eval.zag,
  c174_migrate.zag, c174_selftest.zag, build.sh
- Seal: world_sealed.zag
  (e66dab44370eaad23da57cedfef59e202a1f14aec42447addeaec4edad787fc8)
- Runs: runs/eval_{S,F,A}_{1,2,3}.txt, runs/migrate_{1,2,3}.txt,
  runs/selftest_{1,2,3}.txt
- NAMECHECK.md: Step 0 toolchain guard + progress log.

## Nothing else broke

No Python invoked anywhere (safebin PATH, `which python3`
empty throughout). No changes outside the C174 lane directory.
Frozen TNN-2 binary untouched. Nothing pushed.
