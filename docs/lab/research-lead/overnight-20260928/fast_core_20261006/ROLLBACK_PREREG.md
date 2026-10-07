# Rejected-trial transaction / retained-state budget prereg

Date2026-10-07. Private fast branch. Frozen core unchanged.
Question: does retaining rejected candidates consume a persistent node budget that
blocks a later correct acquisition, and can generic whole-workspace rollback avoid
that without damaging existing evidence or executable methods?

Fixture four facts101->201->31,101->202->32, relations11..14. First acquire31
via direct t2_trial relation98, expected31. Preserve that MAP and answer FACT.
Repeat with all subject/object identifiers offset1000 (relations unchanged).
Budgets48,64,80,96 live nodes INCLUDING two roots. Two arms cloned from identical
posttraining state, four direct rejected trials expected9999 relation99, then direct
correct acquisition expected32 relation100. Also zero-miss controls at all budgets.
No ev_query miss/inquiry wrapper during stress. Existing literal namespace caveat:
all arena node IDs stay below1000; no scale-to-capacity claim.

Generic transaction: copy all WSZ bytes to equally sized scratch workspace, run
unchanged t2_trial there, count live nodes. Never commit state over budget. Retention
arm commits below-budget failed trials; rollback arm commits only successful trials.
Both arms have identical scratch allocation and post-trial budget gate. This is a
PERSISTENT COMMIT budget, not a cap on peak scratch nodes, RSS or time. No allocator
rewrite, eviction-performance comparison, or speed/memory-footprint claim. Capacity
rejection is distinguished from search miss (-2); do not pretend budget abort is
cognitive abstention. Successful trials retain original promotion semantics.

Measure per step response, scratch/result live count, committed live count, commit
flag, budget rejection, byte changes, dangling live edge count; after stress inspect
existing graph execution on a disposable clone and cached query readout. Measure
later expected32 result, commit, new MAP count, cached32 and old31, executable old
root, and edge integrity. Preserve raw counts for all arms/renames/budgets.
Full-rollback qualification includes scratch mutation of an existing licensing node,
edge and header before forced discard, with exact WSZ byte equality afterward;
this is an injected wrapper integrity test, not natural core behavior.

Hard implementation bars: all rejected rollback transactions leave persistent bytes
identical; no committed state exceeds budget; all committed live edges have in-range
live endpoints; established graph executes31 and cached answer remains31 in all
conditions; zero-pressure correct acquisition32 commits for both arms at all budgets;
rollback correct acquisition32 commits for all budgets. Instrumentation bar failures
exit nonzero and are reported, never removed. Retention pressure advantage is an
OPEN measurement: count successes and capacity denials, ties disconfirm benefit at
those budgets. Do not make retention failure a mandatory assertion.

Artifacts here: ROLLBACK_PREREG.md, rollback_driver.zag, rollback.zag,
rollback_run.sh, rollback_environment.txt, rollback_compile1..3.txt,
rollback_run1..3.txt, rollback_provenance.txt, ROLLBACK_REPORT.md. Fresh native
compile gates every run; pureZag computation; three nonempty byte-equal logs and
binary hashes; unchanged prefix cmp; driver loop/bar lint, bash-n, diff-check.

Scope: external generic lifecycle wrapper over frozen reference, not integrated
production fix, task discovery, method-generalization gain, or safety guarantee.
Full snapshot is a costly simple rival; future work can test candidate-local undo
journals and successful-search debris without smuggling task-specific handlers.
