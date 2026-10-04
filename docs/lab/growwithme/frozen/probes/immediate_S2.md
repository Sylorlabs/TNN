# Immediate-recall probes — S2 (sealed)

18 probes, one per clean fact (excludes PENDING F2-18 and falsehood F2-19).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F2-01-Q
Q: How does the deliberate memory substrate organize its records?
Key: The deliberate memory substrate stores records in slots; each slot holds one unit.

### F2-02-Q
Q: List the memory strength tiers by number and name.
Key: Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = pinned.
S7 key (post-correction C2): Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = sealed.

### F2-03-Q
Q: How far can promotion move a record in one step?
Key: Promotion moves a record up exactly one tier; it never skips tiers.

### F2-04-Q
Q: What does the audit ledger record for each consolidation decision?
Key: The audit ledger records every consolidation decision with its deliberation trace.

### F2-05-Q
Q: When does consolidation run?
Key: Consolidation runs at session boundaries, never mid-session.

### F2-06-Q
Q: Which records does the consolidation sweep drop?
Key: The consolidation sweep drops tier-0 records that probes never cite.

### F2-07-Q
Q: What does a tier-2 record need for promotion to tier 3?
Key: A tier-2 record needs 3 corroborating probes for promotion to tier 3.
S7 key (post-correction C5): A tier-2 record needs 2 corroborating probes for promotion to tier 3; the bar was lowered in the strength-trial rulings.

### F2-08-Q
Q: What are the write semantics of the audit ledger?
Key: The audit ledger is append-only.
S7 key (post-correction C4): The audit ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### F2-09-Q
Q: What provenance does each memory record carry?
Key: Each memory record carries provenance: session id, source line, intake turn.

### F2-10-Q
Q: How is a memory's strength set — and what is explicitly forbidden?
Key: A memory's strength is set by the agent's judgment during consolidation, never by formula.

### F2-11-Q
Q: What does scoped deletion remove?
Key: Scoped deletion removes a record and all its derived units in one atomic operation.

### F2-12-Q
Q: What information is recorded in the correction-state mirror?
Key: The correction-state mirror tracks which facts have pending researcher revisions.

### F2-13-Q
Q: State the taught survival condition for a tier-3 memory at the consolidation sweep.
Key: A tier-3 memory survives the consolidation sweep only when its cite count exceeds the sweep's eviction floor.

### F2-14-Q
Q: State the taught G7 neuter-audit failure condition for a turn.
Key: The G7 neuter audit fails a turn when the trace references a slot that consolidation never read.

### F2-15-Q
Q: Where are deliberation traces stored?
Key: Deliberation traces are stored alongside the decision in the ledger.

### F2-16-Q
Q: Can the researcher see a memory's strength tier?
Key: A memory's strength tier is visible to the researcher on request.

### F2-17-Q
Q: What state does the substrate capture at each session boundary?
Key: The substrate snapshots its full state at each session boundary (versioned snapshots).

### F2-20-Q
Q: What is force-pin and what are its visibility properties?
Key: The researcher can force-pin a memory; force-pin is audited and visible.
