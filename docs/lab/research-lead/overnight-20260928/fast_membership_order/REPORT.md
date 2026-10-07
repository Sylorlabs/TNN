# Fast adversarial audit: P6 membership depends on production order

## STATUS / COMMITS
CONFIRMED HARNESS DEFECT, not a learner result.
Fetched ownership base: 91b2acc29731135a143adf27c00400174550eaf1.
Isolated worktree: .worktrees/fast-method-identifiability.
Branch: fast/method-identifiability. Prereg-only commit: 60c44c143.
Experiment source and logs are saved locally, not pushed or merged.
Read prereg, source, and produced raw output BEFORE reading P6 REPORT.md.

## QUESTION / RESULT
Can the current P6 matcher decide exact membership with overlapping child alternatives?
No. Same grammar, different alternative order, different accepted language.

Grammar: A0 -> A1 4; A1 -> 3 | 3 4; A2 empty.
Hand-derived A0 language: {34,344}; union language: {3,34,344}.

| A1 order | Root accepts / correct 2 | Union accepts / correct 3 | False negatives root / union |
|---|---:|---:|---:|
| short first | 1 | 2 | 1 / 1 |
| long first | 1 | 3 | 1 / 0 |

Short first falsely rejects 344 at root and union.
Long first falsely rejects 34 at root, but union accepts through A1.
All four cases (two orders x original/renamed terminals) sweep 340 strings.
No false positives. Terminal bijection 3<->6, 4<->5 reproduces the signature.
Each forward witness is oracle-valid. Empty-table ablation rejects all 340.

## CAUSE
p6struct/precond.zag match returns one locally successful child endpoint.
When a following parent symbol fails, it cannot resume that child at a different
alternative. derivable also unions all NTs, concealing one rooted false negative.
The original fixture has one alternative per NT and cannot expose this defect.

## VERIFICATION
- Compiler SHA matches documented 3093d12d...; environment PURE-ZAG-CLEAN.
- Reused the entire original prefix before main byte-for-byte (cmp verified).
- 3 fresh compiles gated all executions; all run exits 0.
- Binary hashes identical: cba7bc7f6687d5ec8cf4ee665b7a1fd05182f7f31139d161d183539b052a73e8.
- run1/2/3.txt byte-identical (cmp verified), nonempty.
- Driver exit 0 means predicted defect signature verified, not membership passed.
- Additional post-prereg sanity control: original fixture freshly compiled from
  an exact source copy and rerun: 340 tested, 3 derivable, PRECONDITION PASSES.
  Logs original_compile.txt/original_run.txt and source original_precond.zag.
- Zag compile is the available type/build check; no separate typechecker needed.
- No matcher repair was made, and no original ownership files were changed.

## WHAT THIS KILLS
The current implementation as a general exact-membership evaluator for induced
multi-alternative grammars. Rule order could masquerade as learned structure gain.
A single grammar table is not sufficient by itself: both interpreters must implement
the declared grammar semantics. Rename invariance alone did not catch this failure.

## WHAT IT DOES NOT KILL / BOUNDARIES
The original narrow precondition reproduces. Production tables can represent
both tasks. This does not test learner acquisition, transfer, revision, graph
causality, or L3. No independent human replication; same-model adversarial audit.
It does not address ambiguity, true recursive grammars, or resource scaling broadly.

## SOURCE / REPORT AUDIT AFTER THE RUN
- The original grammar dependency graph is A2 -> A0 -> A1: acyclic. The report
  says these dependencies sit inside a cycle, which is false. Recursive function
  calls do occur, but this is not evidence of a recursive language or depth transfer.
- PREREG S4 expects empty productions to accept everything. The unchanged parser
  rejects everything. A scientifically meaningful ablation need not destroy correct
  rejection: measure loss of acceptance on positives and retained rejection separately.
- PREREG S7 forbids any source constant equaling a learned production, which is not
  an ownership criterion: generic primitive symbols may coincide legitimately.
  Audit information flow and complete-form enumeration instead.
- Finite source primitives do not by themselves refute open-form creation: distinguish
  an explicit finite menu of complete solutions from compositional/unbounded syntax.
- A normalized finite-state model can generate and decide positive-support membership;
  the report's broad statistical-versus-structural impossibility is not established
  by this fixture. That is a theoretical counterexample, not an experiment run here.

## NEXT DECISIVE TEST — HANDOFF
Before spending on induction, implement bounded endpoint-set/chart membership
in a separate lane, declaring designated-root versus any-NT semantics explicitly.
Gate it on this unchanged oracle fixture: both orders and both renamings must
accept exactly 2 root and 3 union strings, zero mismatches over 340 each.
Then add one truly recursive grammar and independent bounded-language oracle;
distinguish membership false negatives from an explicit derivation-depth limit.
Only after scorer qualification run learner-versus-facts-only on unseen depth,
with fixed experience, state erasure, and equal-search-budget baselines.
