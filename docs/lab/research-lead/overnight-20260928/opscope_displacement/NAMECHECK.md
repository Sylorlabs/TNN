# NAMECHECK: OpScope Tak-Displacement Attacker (2026-09-30)

Standing rules from LOOP_STATE.md and how this worker honors them:

1. PURE ZAG ONLY (owner red line): every artifact I produce (attack world,
   harness, drivers, analysis) is pure Zag or shell; zero Python at every
   step, including analysis, verification, and byte checks. Any pre-existing
   Python found in the tree is read-only evidence, never executed by me.
2. Shell-only byte checks: dash checks use
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
   only; python3 is never used for byte checks (governance audit finding).
3. No em or en dashes in any loop documentation I write.
4. Prereg strictly precedes implementation: PREREG.md committed ALONE first;
   sealed family generated only after, with seeds/hashes recorded; precedence
   verified via git merge-base --is-ancestor before the results commit.
5. Owned pathspecs only: every git add/commit lists explicit paths under
   docs/lab/research-lead/overnight-20260928/opscope_displacement/ and nothing
   else; git status --porcelain inspected before each commit because other
   workers share this branch.
6. The contaminated internal log
   docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md is
   never edited, staged, or committed by me; I verify an empty diff against it.
7. No history rewrite: provenance incidents are recorded factually, never fixed
   by rebasing or amending. A live .git/index.lock is waited on and retried,
   never removed.
8. Attack only: the OpScope gate is copied byte-identical; my changes are
   confined to the world/harness/drivers in my owned path.
