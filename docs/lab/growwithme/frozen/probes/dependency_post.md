# Dependency post-basic probes — administered at S6/S7 (sealed, 6)

All six pairs, now with basics taught. Each question requires integrating the
advanced B with its basic A. Scored per `../rubric.md` (G6: ≥0.80 correct).

### POST-P1 (pair P1: B=F1-16 S1, A=F5-01 S5)
Q: Given the five znc pipeline stages in order, which pass must run before intrinsic-lower, and what breaks if the order is reversed?
Key: Macro-fuse must run before intrinsic-lower (pipeline: parse, desugar, macro-fuse, intrinsic-lower, codegen); reversing the two miscompiles `z_alloc` call sites.

### POST-P2 (pair P2: B=F1-17 S1, A=F4-01 S4)
Q: Given the 16-word audit entry layout, when is a stage=9 entry a promotion candidate, and what does its d2 word carry?
Key: Only when the d2 word is nonzero; stage=9 marks promotion decisions and d2 carries the promotion's evidence code.

### POST-P3 (pair P3: B=F2-13 S2, A=F5-02 S5)
Q: Given the sweep's eviction-floor mechanics, what happens to a tier-3 memory whose cite count sits below the floor?
Key: It is demoted, never deleted; a tier-3 memory survives the sweep only when its cite count exceeds the eviction floor (computed from tier-1 cite counts).

### POST-P4 (pair P4: B=F2-14 S2, A=F4-02 S4)
Q: Given the G7 causal-consultation rule, what does the neuter audit conclude about a turn whose trace cites a slot consolidation never read?
Key: The trace is decorative and the turn fails the audit — a trace is causally consulted only if the decision read the slot it cites.

### POST-P5 (pair P5: B=F3-11 S3, A=F5-03 S5)
Q: Given the definition of a scale leg, what does the scale-rot amendment require when leg M1's stdout SHA diverges from REPORT.md while verdicts reproduce?
Key: Rerun the leg by name from the frozen config (a leg = one battery configuration × repeat count; stdout SHA recorded per leg in REPORT.md).

### POST-P6 (pair P6: B=F3-12 S3, A=F5-04 S5)
Q: Given the leak check's scope, does a PENDING claim stated in a chat answer trip the check when all probe answers are clean?
Key: Yes — leak. The PENDING leak check audits every chat turn, not just probe answers.
