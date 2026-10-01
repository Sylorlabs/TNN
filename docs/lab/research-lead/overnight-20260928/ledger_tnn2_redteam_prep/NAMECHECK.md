# NAMECHECK: TNN-2 Red-Team Cycle Ledger Update

Worker: Ledger Updater (red-team cycle, C150-C159).
Date: 2026-10-01 UTC.
Task: record the red-team, compression, governance, synthesis, and
analysis results of the TNN-2 cycle. First ledger updater (commit
503a3bedc) recorded C143-C149; this update appends C150-C159 plus a
freeze-status note. Owned path: ledger files only.

## Step 0: Toolchain guard (mandatory)

Command executed at startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing under the restricted
PATH; `guard-check-done` printed. No forbidden executable invoked at
any point in this task. All reading done with `git show` and `read`;
no research computation performed. Guard: PASS, no PROCESS-FAIL.

## Step 1: Claim inventory (read from committed reports, not fabricated)

- C150: construction red team, commit 340e94e3e, verdict
  CONSTRUCTION-ATTACK-SUCCESS. Report: tnn2_redteam_construction/CONSTRUCTION_REDTEAM.md.
  Classification: L2 structural-learning mechanism, not L3. C0-B/C0-C fail.
- C151: inquiry red team, commit 4e329c772, verdict
  INQUIRY-ATTACK-SUCCESS. Report: tnn2_redteam_inquiry/INQUIRY_REDTEAM.md.
  Classification: L1/L2/L4 learner-originated PASS; L5 real but trivial;
  L3 hardcoded (constants 30/-999); L6 absent. Below L2 as inquiry.
- C152: revision red team, commit 687ba0219, verdict
  REVISION-ATTACK-SUCCESS. Report: tnn2_redteam_revision/REVISION_REDTEAM.md.
  Classification: L1 parameter filling in researcher-authored repair
  template; T2-REVISE trace is L0 storage. C0-A/B/C fail; C0-D
  unestablished. No L3.
- C153: compression analysis, commit b2a6ae82c, verdict
  COMPRESSION-ANALYSIS-COMPLETE. Report: tnn2_compression/COMPRESSION_ANALYSIS.md.
  1591 lines; ~103 dead-in-cognition; sum assembler test-gated and dead
  in production; ~32 pending bootstrap_miss experiment; ~32 unification.
- C154: governance audit, commit 622363372, verdict GOVERNANCE-AUDIT-PASS
  (step 11). Report: tnn2_governance/GOVERNANCE_AUDIT.md. Caveat: freeze
  evaluation still running at audit time; evaluator must close its own
  K-FZ2 bars.
- C155: frontier scout, commit 65effc909, verdict FRONTIER-SCOUT-COMPLETE.
  Report: tnn2_frontier/FRONTIER_BACKLOG.md. 17 ranked research questions;
  questions only, no claims.
- C156: revision generalization, commit edbb0e9b5, verdict
  REVISION-GENERALIZATION-ANALYSIS-COMPLETE. Report:
  tnn2_revision_generalization/REVISION_GENERALIZATION.md. K-T2-6
  process loophole attribution; five repair topologies; analysis only.
- C157: red-team synthesis, commit 42b4dfa91, verdict
  REDTEAM-SYNTHESIS-COMPLETE. Report: tnn2_synthesis/REDTEAM_SYNTHESIS.md.
  Shared cause: "enumerated-schema / filled-slot". H1/H2/H3 hypotheses.
  Freeze interpretation: capability vs generality distinction.
- C158: alternative explanations, commit ccee9e5e6, verdict
  ALTERNATIVE-EXPLANATION-ATTACK-COMPLETE. Report:
  tnn2_altexp/ALTERNATIVE_EXPLANATIONS.md. Unified hypothesis: form
  from researcher, content from learner; "answer-fed not answer-derived".
  Falsification criteria stated. Does not promote or demote TNN-2.
- C159: inquiry generalization, commit dedfad368, verdict
  INQUIRY-GENERALIZATION-ANALYSIS-COMPLETE. Report:
  tnn2_inquiry_generalization/INQUIRY_GENERALIZATION.md. Derived
  question sketch within frozen ISA; resolution via type-3 supersession;
  constant-action root cause: prereg spec gap (K-T2-4/K-T2-5
  letter-vs-spirit). Shared cause note: verdicts without structures.

## Step 2: L-classification and C0 discipline

- Do NOT upgrade or downgrade the builders' TNN2-BUILD-PASS (C144) or
  TNN2-REPRO-PASS (C145). Red teams attack mechanism generality, not
  frozen kill bars. Recorded as mechanism-generality results only.
- L3 achieved anywhere: zero (unchanged).
- All 10 reports read in full before ledgering. No report contents
  fabricated; every number and classification above is sourced from the
  named committed reports.

## Step 3: Freeze-score discipline

- NO FREEZE SCORE RECORDED. The CORE-FREEZE-TNN2 evaluator is still
  running. The TNN-3 prerequisites analyst (commit f795807cc) found
  the evaluator's on-disk draft internally inconsistent: it claims a
  5/9 FW score but lists only 4 passing worlds, and marks K-FZ2-4
  PENDING while the draft verdict line says COMPLETE. The draft is
  NOT adopted. Recorded status: evaluation in progress, draft
  inconsistent, awaiting reconciled commit.

## Step 4: Style and scope

- No em dashes used in this document or the ledger append.
- Contaminated paper (TNN_RESEARCH_PAPER_20260929.md) untouched.
- No other worker's output modified. Only the canonical ledger and
  this NAMECHECK were written.

## Verdict: LEDGER-REDTEAM-CYCLE-COMPLETE
