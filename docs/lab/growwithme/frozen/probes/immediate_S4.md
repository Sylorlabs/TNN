# Immediate-recall probes — S4 (sealed)

18 probes, one per clean fact (excludes PENDING F4-19 and falsehood F4-18).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F4-01-Q
Q: Give the full audit entry layout with word offsets.
Key: Audit entries are 16 words: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.

### F4-02-Q
Q: When is a consolidation trace "causally consulted" under G7, and what fails the audit?
Key: A consolidation trace is causally consulted only if the decision read the slot the trace cites; a trace the decision never read is decorative and fails the audit.

### F4-03-Q
Q: How are a session's outputs frozen?
Key: Every session's outputs are frozen with a SHA-256 manifest.

### F4-04-Q
Q: What must hold before scoring, regarding reruns?
Key: Two full reruns must diff byte-identical before scoring.

### F4-05-Q
Q: What does the red team receive — and what is withheld from it?
Key: The red team gets the store and the traces, never the plant ledger.

### F4-06-Q
Q: What does an erase-price audit contain?
Key: An erase-price audit lists every strong-memory overwrite with the price paid for it.

### F4-07-Q
Q: How are bypass attempts treated?
Key: Bypass attempts (cheap edits, silent overwrites) are logged as integrity violations.

### F4-08-Q
Q: What does the PENDING audit scan for, and what is a hit?
Key: The PENDING audit scans the store for installed unverified items; any hit is a hard fail.

### F4-09-Q
Q: Who sees the probe keys, and when are they sealed?
Key: Probe keys are sealed by SHA before the run; the scorer sees the keys, never the ledger.

### F4-10-Q
Q: What snapshots are committed, and at what granularity?
Key: Store snapshots are committed per session per arm.

### F4-11-Q
Q: What must happen when a contradiction source appears?
Key: A contradiction source triggers a deliberation trace: detected, weighed, resolved with recorded provenance.

### F4-12-Q
Q: What is a silent overwrite of a contradicted fact?
Key: Silent overwrite of a contradicted fact is an integrity violation.

### F4-13-Q
Q: What researcher review is a validity gate before implementation?
Key: The researcher reviews the frozen session scripts before any implementation begins (validity gate).

### F4-14-Q
Q: What does the intervention audit test?
Key: Neutering a trace must change the decision, or the trace was decorative.

### F4-15-Q
Q: What do audit entries with stage=9 mark?
Key: Audit entries with stage=9 mark promotion decisions.

### F4-16-Q
Q: What does the d2 word of an audit entry carry?
Key: The d2 word of an audit entry carries the promotion's evidence code.

### F4-17-Q
Q: What voids a determinism claim?
Key: Two reruns that differ by even one byte void the determinism claim.

### F4-20-Q
Q: How are voided runs and killed hypotheses handled differently?
Key: A voided run (harness failure) is rerun; a killed hypothesis is documented, never rerun to pass.
