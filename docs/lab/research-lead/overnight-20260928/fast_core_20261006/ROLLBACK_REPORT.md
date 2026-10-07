# Transactional rejection preserves acquisition in a narrow budget window

Date2026-10-07. Prereg14478875e. Frozen reference prefix unchanged.
External generic full-workspace transaction; NOT a production core repair.
Two identifier renames x four budgets x two arms x zero/four misses =32 conditions.

Baseline after acquiring31 (1031 renamed):17 live nodes, one MAP. A rejected
search on this trained world produces54 additional live nodes, scratch total71.
A later successful32 (1032 renamed) acquisition adds20 nodes, baseline total37.
Both arms use identical scratch workspace and post-trial persistent-budget gate.
Arm0 retains below-budget failures; arm1 discards every failure. Budget includes
roots; no commit may exceed it. Readout diagnostics run on disposable copies.

| Budget | Retention final live / later commits (two renames) | Rollback final live / later commits | Explanation |
|---|---|---|---|
|48|37 /2 of2|37 /2 of2|Failure scratch71 denied before retention; no advantage.|
|64|37 /2 of2|37 /2 of2|Same protective capacity rejection; no advantage.|
|80|71 /0 of2|37 /2 of2|Retention commits first failure; later successful candidate needs91, denied.|
|96|91 /2 of2|37 /2 of2|Retention commits one failure but later91 fits; acquisition tie.|

Under four-miss pressure: retention later commits6/8, rollback8/8. Without
pressure: both8/8. At80 both cores COMPUTE the correct candidate answer in
scratch, but only rollback can commit it. This is a lifecycle capacity effect,
not a failure to discover the answer and not evidence for generalized knowing-how.
The pattern is nonmonotone in budget: tighter budgets protect the retention arm by
refusing the whole failed search; at96 enough capacity remains. Preserve these ties.

All32 rollback stress misses (8 stressed conditions x4) leave persistent state
byte-identical; retention undergoes another32 stress misses. All32 conditions preserve old executable31/1031 and cached readout;
all committed later acquisitions yield correct cached32/1032 with two MAPs.
No dangling live edges and no persistent-budget violations. Injected discard probe
mutates6 scratch bytes across old fact/edge/header, persistent differences0 in all
32 probes. No special-case cleanup of facts, references, or task identifiers.

Qualification: rollback_run.sh final execution after instrumentation repair;
three fresh compile-gated nonempty byte-identical runs and binaries; PURE-ZAG-CLEAN;
source/prefix comparison, driver loop/bar lint, bash-n, git diff-check. Final exit0,
instrumentation_unexpected0. Original frozen source unchanged against ownership.
Scientific calculations and integrity comparisons are pure Zag. No project-wide
typecheck exists for these standalone Zag drivers; native compilation checks them.

Limits / attack on positive:
- A persistent COMMIT budget is not a peak allocation limit: denied scratch reaches
  125 nodes. Full WSZ copies are110656 bytes; we did not measure RSS/time or savings.
- Retention is already transaction-wrapped, not original unchecked eviction atNN1024.
- Snapshot isolation trivially protects existing state; it does not qualify an undo
  journal, concurrent mutation, partial rollback, or authority/revocation safety.
- Success still retains earlier rejected candidates inside the same successful trial.
  Here correct32 search adds20 nodes versus first31 acquisition11; not all growth
  classified as useful. No minimal graph extraction or lifetime accounting performed.
- Evidence remains supervised and literal-subject-bound; cached readout uses FACT.
  Rollback fixes none of the prior proposal/ownership/readout limitations.

NEXT: successful-search debris versus generic reachable graph retention, preserving
literal operands, licensing DEP, MAP, answer FACT and frame semantics. Preregister
roots/reference classification first; compare graph execution, revision and cached
readout under the same budget. Alternatively return to highest-ranked identifiable
acquisition plus executable method indexing; no task-specific semantic handler.
