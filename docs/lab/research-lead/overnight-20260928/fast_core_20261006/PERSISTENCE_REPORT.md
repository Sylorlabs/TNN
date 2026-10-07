# Failed trials leave persistent candidate allocations

Date2026-10-06. Prereg08568a74f. Unchanged frozen TNN-2 reference.
Four steps each in independent fresh workspace; baseline live6 (4facts+2roots).

|Arm|Responses|Final live / facts / MAP / instructions /902|
|---|---|---|
|Failed ev_query with expected9999|-2 each|183 /8 /0 /80 /88|
|Failed direct t2_trial with expected9999|-2 each|174 /4 /0 /80 /88|
|Supervised success then three cached no-feedback queries|31 each|17 /5 /1 /4 /5|
|Four direct observedfact cached queries|201 each|6 /4 /0 /0 /0|

Direct rejected trial adds42 live nodes per call:20instruction cells+22902 literal/
frame cells. No MAP promotion, no extraFACT. Count grows through all4 calls.
Query misses additionally create inquiry-related state and FACT nodes: facts5,6,7,8
at steps1..4. Original prereg described facts held constant except successful
promotion, but this assumption fails in the query-wrapper arm. The measured direct
trial control isolates persistence without that extra effect. Do not silently erase
or classify all new FACT nodes as epistemically endorsed world facts.

Interpretation: candidate programs and scratch/literal/frame allocations remain in
the persistent workspace after rejected search in this reference. That consumes
finite arena capacity. It does NOT prove failed programs are endorsed, re-executed,
or causally useful; it does not measure eviction pressure or asymptotic leakage.
Repeated successful cached queries add none, consistent with exact-fact activation.

Source invariant: original core untouched; no candidate cleanup patch. All frozen
response/growth bars match; exception above is a disclosed ancillary prediction
failure, not rewritten prereg. Foursteps below nodecap, no eviction tested.

Verification: persistence_run.sh; three final fresh compile-gated executions,
nonempty identical raw outputs and binary hashes; prefix integritycmp; PURE-ZAG.
No speed claims, production equivalence, independent human replication or AGI claim.

NEXT: prereg equal-arena-budget repeated-miss worlds with generic trial allocation
rollback versus existing retention; measure future correct acquisition and reference
integrity, not just nodecounts. Rollback must preserve established facts/methods and
remove edges to removed nodes; a naive live-bit clear is not a production repair.
Also inspect inquiry-node FACT semantics before calling wrapper growth contamination.
