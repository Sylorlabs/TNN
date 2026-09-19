# N17 independent review V1 — disposition

Disposition: **REQUEST_CHANGES**.

The review found that the current N17 design correctly preserves the
historical-only boundary and the compile-only identity binary, but it was not
ready for preregistration-only implementation because the parent type/layout
inventory, exact native verifier check matrix, Python/NumPy-sensitive known
answers, required negative controls, final native runtime boundary and R25
lineage inputs were not yet frozen.

This correction packet adds a machine-readable inventory schema, a source-derived
draft verifier matrix, explicit R25 lineage requirements and the required
review boundary. The matrix is deliberately marked draft and the inventory
schema unpopulated; no continuity level is claimed and no execution is
authorized by this record.
