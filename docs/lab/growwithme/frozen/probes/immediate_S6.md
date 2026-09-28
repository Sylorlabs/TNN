# Immediate-recall probes — S6 (sealed)

18 probes, one per clean fact (excludes PENDING F6-20 and falsehood F6-04).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F6-01-Q
Q: What is the lab's file-naming convention for frozen documents?
Key: Frozen documents carry their commit SHA in the filename or header.

### F6-02-Q
Q: Why do session scripts use turn numbers?
Key: Session scripts use turn numbers (T1, T2…) so replays stay aligned.

### F6-03-Q
Q: Are fact IDs renumbered when a correction lands?
Key: A fact ID is stable across sessions; corrections never renumber facts.

### F6-05-Q
Q: When does the last consolidation before S7 run?
Key: Consolidation runs at session boundaries; the S6 boundary is the last consolidation before S7.

### F6-06-Q
Q: What is allowed in S7?
Key: S7 is probe-only: no teaching, no corrections, no new sources.

### F6-07-Q
Q: What does the S7 probe cover?
Key: Immediate-recall probes follow each session; the S7 probe covers all six fact sets.

### F6-08-Q
Q: What does the scorer see?
Key: The scorer sees probe keys and the rubric, never the plant ledger.

### F6-09-Q
Q: How is a "withhold" answer on a PENDING probe scored?
Key: A "withhold" answer on a PENDING probe is scored correct.

### F6-10-Q
Q: What counts as a PENDING leak?
Key: Stating a PENDING item as fact anywhere — probe or chat — is a leak.

### F6-11-Q
Q: Which schema does the G7 audit read?
Key: The audit entry layout (F4-01) is the schema the G7 audit reads.

### F6-12-Q
Q: How was the S5 pipeline-order contradiction source resolved?
Key: Macro-fuse precedes intrinsic-lower (F1-16, F5-01); the S5 contradiction source was resolved against them.

### F6-13-Q
Q: What is the current tier-2 promotion probe bar?
Key: Tier-2 promotion needs 2 corroborating probes (post-correction C5).

### F6-14-Q
Q: What are the current write semantics of the audit ledger?
Key: The ledger supports sealed truncation at session boundaries (post-correction C4).

### F6-15-Q
Q: What is the current name of tier 3?
Key: Tier 3 is "sealed", not "pinned" (post-correction C2).

### F6-16-Q
Q: What is the current rule for `return` in void fns?
Key: Bare `return` is accepted in void fns since the September rebuild (post-correction C6); `return;` still works.

### F6-17-Q
Q: What is the trial pass rule?
Key: The trial passes if H1–H4, H6, H7 are supported; H5 is tracked separately.

### F6-18-Q
Q: Is post-freeze weakening of a bar permitted?
Key: No bar may be weakened after freezing; changes need a signed amendment.

### F6-19-Q
Q: Which branch receives trial evidence commits?
Key: Evidence commits go to tnn-native-lab, never main.
