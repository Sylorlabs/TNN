# R33-N17 authoring notes

Status: **compile-only authoring; never continuity evidence**.

`identity.zag` is the first concrete native candidate layer. It statically links the already-consumed read-only N10/N12/N13A substrate and encodes only direct parent identity assertions already established as historical/structural facts: canonical R27 custody, exact R26 raw-SHA linkage, selected R27 dictionary cardinalities, embedded `r26_experiments.R26State`, R26 format/step/restarts and null R26 speech segmenter.

`AUTHORING_BUILD_01/driver.zag` is intentionally a refusal sentinel. Even if launched accidentally it does not open the parent or call `n17_identity`; it prints a refusal and exits 73. A compilation of this source is only syntax/linkage authoring evidence and must not increment R33 diagnostic/training counters or be registered as a continuity invocation.

The semantic-digest implementation is intentionally not guessed yet. Before it is authored, review must settle the exact supported serialized type inventory and Python-compatible canonicalization requirements described in `DESIGN.md`, especially float spelling/default-str behavior and the exact R27/R26 state-dict traversal. The eventual reviewed source must pin/copy the consumed substrate into the candidate freeze rather than treat these authoring imports as mutable live dependencies.

Independent review V1 returned `REQUEST_CHANGES`. The correction artifacts are
`PARENT_TYPE_INVENTORY_SCHEMA.json`, `VERIFIER_CHECK_MATRIX.json` and
`R25_LINEAGE_REQUIREMENTS.md`; they are schema/draft records only. Their
presence does not qualify any continuity level or authorize compilation,
preregistration or execution.
