# Immediate-recall probes — S2 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F2-18 and falsehood F2-19).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F2-01-Q
Q: How are records arranged inside the deliberate memory substrate?
Key: The deliberate memory substrate stores records in slots; each slot holds one unit.

### F2-02-Q
Q: Enumerate the memory strength tiers, giving each number and name.
Key: Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = pinned.
S7 key (post-correction C2): Strength tiers: tier 0 = working, tier 1 = retained, tier 2 = strong, tier 3 = sealed.

### F2-03-Q
Q: What is the maximum tier movement promotion allows in a single step?
Key: Promotion moves a record up exactly one tier; it never skips tiers.

### F2-04-Q
Q: For every consolidation decision, what does the audit ledger capture?
Key: The audit ledger records every consolidation decision with its deliberation trace.

### F2-05-Q
Q: At what point does consolidation execute?
Key: Consolidation runs at session boundaries, never mid-session.

### F2-06-Q
Q: What kind of records does the consolidation sweep discard?
Key: The consolidation sweep drops tier-0 records that probes never cite.

### F2-07-Q
Q: What is required to promote a tier-2 record to tier 3?
Key: A tier-2 record needs 3 corroborating probes for promotion to tier 3.
S7 key (post-correction C5): A tier-2 record needs 2 corroborating probes for promotion to tier 3; the bar was lowered in the strength-trial rulings.

### F2-08-Q
Q: Describe the audit ledger's write semantics.
Key: The audit ledger is append-only.
S7 key (post-correction C4): The audit ledger supports sealed truncation at session boundaries; append-only was the v1 design.

### F2-09-Q
Q: Which provenance fields ride along with each memory record?
Key: Each memory record carries provenance: session id, source line, intake turn.

### F2-10-Q
Q: What determines a memory's strength, and what determination method is banned?
Key: A memory's strength is set by the agent's judgment during consolidation, never by formula.

### F2-11-Q
Q: What exactly disappears under scoped deletion?
Key: Scoped deletion removes a record and all its derived units in one atomic operation.

### F2-12-Q
Q: What does the correction-state mirror keep track of?
Key: The correction-state mirror tracks which facts have pending researcher revisions.

### F2-13-Q
Q: What must hold for a tier-3 memory to survive the consolidation sweep?
Key: A tier-3 memory survives the consolidation sweep only when its cite count exceeds the sweep's eviction floor.

### F2-14-Q
Q: Under what condition does the G7 neuter audit fail a turn?
Key: The G7 neuter audit fails a turn when the trace references a slot that consolidation never read.

### F2-15-Q
Q: Where do deliberation traces live?
Key: Deliberation traces are stored alongside the decision in the ledger.

### F2-16-Q
Q: Is a memory's strength tier visible to the researcher?
Key: A memory's strength tier is visible to the researcher on request.

### F2-17-Q
Q: What does the substrate snapshot at every session boundary?
Key: The substrate snapshots its full state at each session boundary (versioned snapshots).

### F2-20-Q
Q: Describe force-pin and whether it is visible and audited.
Key: The researcher can force-pin a memory; force-pin is audited and visible.
