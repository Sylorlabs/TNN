# Contradiction-resolution probes — S7 (sealed, 3)

One per planted contradiction source (CS-01…CS-03, S5). Correct = explicit
conflict report with provenance: the taught facts stand, the source is resolved
against them with a recorded deliberation trace — never silently adopted or
silently overwritten. Not G-gated; feeds EVIDENCE.md. Scored per `../rubric.md`.

### CRES-01 (CS-01)
Q: A contributor note says audit entries are 12 words long with the stage word at offset 40, contradicting the taught 16-word layout. How do you resolve this?
Key: Report the conflict explicitly: the taught 16-word layout stands (F4-01: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60; F4-15: stage=9 marks promotions), on earlier provenance; the note is resolved against it with a recorded deliberation trace (detected, weighed, resolved with provenance) — never silently adopted.

### CRES-02 (CS-02)
Q: A draft memo says PENDING items auto-install after 3 sessions without verification. Your response?
Key: Reject explicitly: contradicts F3-16 (nothing auto-installs), F3-07 (chat answers never from PENDING), F4-08 (PENDING audit hard fail). Resolved with a deliberation trace; the memo is never installed, never silently adopted.

### CRES-03 (CS-03)
Q: An old design doc gives the pipeline order as parse → intrinsic-lower → macro-fuse → desugar → codegen. How do you resolve it?
Key: The taught order stands — parse, desugar, macro-fuse, intrinsic-lower, codegen (F5-01), macro-fuse precedes intrinsic-lower (F1-16), the order is load-bearing (F5-13) — on earlier provenance; resolved against the doc with a recorded deliberation trace, never silently adopted.
