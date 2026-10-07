# Failed trial persistence - prereg

Date2026-10-06. Unchanged frozen TNN-2 prefix, fast private branch.
QUESTION: does rejected search leave executable/literal/frame nodes in workspace,
or are transient candidate allocations reclaimed? H-transient vs H-persistent-debris.
Source allocates trial nodes via alloc_node, no obvious cleanup in t2_trial.

Fixture four facts:101->201->31 and101->202->32, relations11..14.
Independent fresh arena per arm. Repeated4 operations:
A ev_query(101,99,9999,0): expected cannot match any terminal ->-2.
B t2_trial(101,99,9999,0,0,0): direct trial no query/miss inquiry wrapper.
C first ev_query(101,99,31,0), then3 cached no-feedback queries.
D four cached exact observedfact queries(101,11,-2,0).

Count live node types FACT1, MAP20, instructions101..104, scratch/literal/frame902,
other types, all live nodes; header node allocation count20. Baseline all4 facts,
noMAP or instructions. Report each step's response and counts, facts held constant
except C promotedanswer. Prediction: A/B failed steps accumulate instructions902;
C first acquires, later cached queries no new trialinstructions (902 may differ if
query unrelated scratch, record). D never gainsinstructions/MAP.
Bars: A/B remain-2,MAP0, instructions grow monotonically and final>baseline;
C responses31 all4, MAP1 and instructions unchanged afterfirst;
D direct responses201 all4, MAP0,instructions0. No fixed undocumented allocation
counts required. No overflow/eviction intentionally (4 steps only).

This is persistent workspace allocation, NOT proof a failed method is endorsed or
behaviorally reused. Memory nodes may be deliberately recyclable; test their causal
role later. Does not demonstrate scale/memory leak unbounded, production behavior,
or unique intelligence limit. Monotonic tiny counts cannot establish complexity.

Artifacts PERSISTENCE_PREREG.md, persistence_driver.zag, persistence.zag,
persistence_run.sh, persistence_compile1..3.txt,persistence_run1..3.txt,
persistence_provenance.txt,PERSISTENCE_REPORT.md. PureZag counts; fresh3 builds/
runs; originalprefix cmp; nonempty deterministic logs, instrumentation mismatchexit1.
Ignore binary; no cleanup patches. Preserve report failures, not tune bars.
Next: same memory budget with repeated misses and controlled eviction, compare
candidate-state cleanup vs existing core. Cleanup fork generic orchestration only,
not evidence of improved method acquisition until heldout behavior measured.
