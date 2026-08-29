# Compute-efficiency results

The human defines the total Resource Envelope. TNN—not the trainer—must decide how many fibers exist and how much of the envelope each fiber consumes.

The evaluator compares dynamic unequal allocation, equal allocation, and serial execution across several resource envelopes. Tool work is shared by exact source/tool/configuration identity so one pending compile can serve all relevant fibers without stale reuse.

| Envelope | Dynamic rounds | Equal rounds | Serial rounds | Dynamic efficiency | Equal efficiency | Serial efficiency |
|---:|---:|---:|---:|---:|---:|---:|


This is a controlled evaluator, not yet the final endogenous allocation mechanism. Production TNN must learn its allocation behavior from consequences rather than receiving the evaluator's formula.
