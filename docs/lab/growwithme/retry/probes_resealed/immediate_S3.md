# Immediate-recall probes — S3 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F3-20 and falsehood F3-19).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F3-01-Q
Q: Name the gates every intake turn traverses, in sequence.
Key: The dialogue stack gates every intake turn through G6 (admissibility) then G7 (neuter).

### F3-02-Q
Q: Which inputs get rejected by G6?
Key: G6 rejects inputs that fail the provenance check.

### F3-03-Q
Q: What task does the entity scanner perform?
Key: The entity scanner extracts candidate units from taught facts.

### F3-04-Q
Q: Define a unit.
Key: Units are the atomic answerable items derived from source facts.

### F3-05-Q
Q: What gets flagged by the correction-state mirror?
Key: The correction-state mirror flags facts the researcher has revised.

### F3-06-Q
Q: Explain the mechanics of scoped deletion.
Key: Scoped deletion removes a record plus its derived units atomically.

### F3-07-Q
Q: From which sources are chat answers allowed to be generated?
Key: Chat answers are generated from installed records only, never from PENDING.

### F3-08-Q
Q: What should be given instead of a low-confidence guess?
Key: A "don't know" answer is preferred over a low-confidence guess.

### F3-09-Q
Q: How does intake normalize text before extracting units?
Key: Intake lowercases all text before unit extraction.

### F3-10-Q
Q: Is consolidation triggered by session boundaries or by chat turns?
Key: Session boundaries trigger consolidation; chat turns never do.

### F3-11-Q
Q: What does the SCALE-ROT amendment say about rerunning legs?
Key: The SCALE-ROT amendment reruns legs whose M1 stdout SHA diverges from REPORT.md, even when verdicts reproduce.

### F3-12-Q
Q: What is the leak-check rule for PENDING items appearing in chat answers?
Key: PENDING items cited in chat answers trip the leak check even when probe answers are clean.

### F3-13-Q
Q: What is emitted for each consolidation decision?
Key: Every consolidation decision emits a white-box trace: what was considered, what evidence bore on it, the verdict.

### F3-14-Q
Q: What can the researcher see of deliberation traces?
Key: The researcher can ask for a trace dump of any consolidation decision.

### F3-15-Q
Q: How does intake handle a source exceeding the session's intake budget?
Key: Intake rejects sources larger than the session's intake budget with a logged refusal.

### F3-16-Q
Q: When, if ever, is a PENDING item installed?
Key: PENDING items stay held until the researcher verifies them; nothing auto-installs.

### F3-17-Q
Q: What determinism guarantee does the dialogue stack provide?
Key: The dialogue stack is deterministic: same inputs, byte-identical outputs.

### F3-18-Q
Q: If a researcher correction conflicts with a source packet, which one prevails?
Key: Correction turns from the researcher override source-packet claims.
