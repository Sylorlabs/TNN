# Immediate-recall probes — S3 (sealed)

18 probes, one per clean fact (excludes PENDING F3-20 and falsehood F3-19).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F3-01-Q
Q: Through which gates does every intake turn pass, in order?
Key: The dialogue stack gates every intake turn through G6 (admissibility) then G7 (neuter).

### F3-02-Q
Q: What inputs does G6 reject?
Key: G6 rejects inputs that fail the provenance check.

### F3-03-Q
Q: What is the entity scanner's job?
Key: The entity scanner extracts candidate units from taught facts.

### F3-04-Q
Q: What is a unit?
Key: Units are the atomic answerable items derived from source facts.

### F3-05-Q
Q: What does the correction-state mirror flag?
Key: The correction-state mirror flags facts the researcher has revised.

### F3-06-Q
Q: How does scoped deletion work?
Key: Scoped deletion removes a record plus its derived units atomically.

### F3-07-Q
Q: What sources may chat answers be generated from?
Key: Chat answers are generated from installed records only, never from PENDING.

### F3-08-Q
Q: What is preferred over a low-confidence guess?
Key: A "don't know" answer is preferred over a low-confidence guess.

### F3-09-Q
Q: What text normalization does intake perform before unit extraction?
Key: Intake lowercases all text before unit extraction.

### F3-10-Q
Q: What triggers consolidation — session boundaries or chat turns?
Key: Session boundaries trigger consolidation; chat turns never do.

### F3-11-Q
Q: State the taught SCALE-ROT amendment rerun rule.
Key: The SCALE-ROT amendment reruns legs whose M1 stdout SHA diverges from REPORT.md, even when verdicts reproduce.

### F3-12-Q
Q: State the taught leak-check rule for PENDING items in chat answers.
Key: PENDING items cited in chat answers trip the leak check even when probe answers are clean.

### F3-13-Q
Q: What does every consolidation decision emit?
Key: Every consolidation decision emits a white-box trace: what was considered, what evidence bore on it, the verdict.

### F3-14-Q
Q: What trace visibility does the researcher have?
Key: The researcher can ask for a trace dump of any consolidation decision.

### F3-15-Q
Q: What happens to sources larger than the session's intake budget?
Key: Intake rejects sources larger than the session's intake budget with a logged refusal.

### F3-16-Q
Q: Under what condition does a PENDING item get installed?
Key: PENDING items stay held until the researcher verifies them; nothing auto-installs.

### F3-17-Q
Q: What determinism property does the dialogue stack have?
Key: The dialogue stack is deterministic: same inputs, byte-identical outputs.

### F3-18-Q
Q: When a researcher correction contradicts a source packet, which wins?
Key: Correction turns from the researcher override source-packet claims.
