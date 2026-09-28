# Immediate-recall probes — S4 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F4-19 and falsehood F4-18).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F4-01-Q
Q: Lay out the complete audit entry format, with every word offset.
Key: Audit entries are 16 words: op@0, slot@4, rc@8, b1..b5@12..28, a1..a5@32..48, stage@52, d1@56, d2@60.

### F4-02-Q
Q: What makes a consolidation trace "causally consulted" under G7, and what does the audit fail?
Key: A consolidation trace is causally consulted only if the decision read the slot the trace cites; a trace the decision never read is decorative and fails the audit.

### F4-03-Q
Q: How does a session's output get frozen?
Key: Every session's outputs are frozen with a SHA-256 manifest.

### F4-04-Q
Q: What rerun condition must be met before scoring may begin?
Key: Two full reruns must diff byte-identical before scoring.

### F4-05-Q
Q: What is given to the red team, and what is kept from it?
Key: The red team gets the store and the traces, never the plant ledger.

### F4-06-Q
Q: What goes into an erase-price audit?
Key: An erase-price audit lists every strong-memory overwrite with the price paid for it.

### F4-07-Q
Q: What happens to bypass attempts?
Key: Bypass attempts (cheap edits, silent overwrites) are logged as integrity violations.

### F4-08-Q
Q: What is the PENDING audit looking for, and what counts as a hit?
Key: The PENDING audit scans the store for installed unverified items; any hit is a hard fail.

### F4-09-Q
Q: Who is allowed to see probe keys, and at what point are they sealed?
Key: Probe keys are sealed by SHA before the run; the scorer sees the keys, never the ledger.

### F4-10-Q
Q: Which snapshots get committed, and how fine-grained are they?
Key: Store snapshots are committed per session per arm.

### F4-11-Q
Q: What is required when a contradiction source shows up?
Key: A contradiction source triggers a deliberation trace: detected, weighed, resolved with recorded provenance.

### F4-12-Q
Q: How is silently overwriting a contradicted fact classified?
Key: Silent overwrite of a contradicted fact is an integrity violation.

### F4-13-Q
Q: Which researcher review gates validity before implementation starts?
Key: The researcher reviews the frozen session scripts before any implementation begins (validity gate).

### F4-14-Q
Q: What is the intervention audit testing?
Key: Neutering a trace must change the decision, or the trace was decorative.

### F4-15-Q
Q: What is marked by audit entries carrying stage=9?
Key: Audit entries with stage=9 mark promotion decisions.

### F4-16-Q
Q: What information sits in an audit entry's d2 word?
Key: The d2 word of an audit entry carries the promotion's evidence code.

### F4-17-Q
Q: What invalidates a determinism claim?
Key: Two reruns that differ by even one byte void the determinism claim.

### F4-20-Q
Q: What is the different handling for a voided run versus a killed hypothesis?
Key: A voided run (harness failure) is rerun; a killed hypothesis is documented, never rerun to pass.
