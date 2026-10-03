# Step 0 Name-Check: FW Blindness Audit

Date: 2026-09-30. Worker: FW Blindness Auditor.

## Standing rules identified before any work

1. Pure Zag only for research logic. This task is a git/history audit; shell commands
   are used only for orchestration (git operations, file listing, hash checks). No Python
   anywhere. No C/C++/JS/Rust. Shell is not used as a substitute research program.
2. The contaminated paper (docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md)
   is never edited, staged, committed, or cited as canonical evidence. Verified zero-diff
   before and after this task.
3. Owned path only: docs/lab/research-lead/overnight-20260928/blindness_audit/.
   Commit with explicit pathspecs. Never touch other workers' files.
4. No em dashes in loop documentation. Shell-only dash check.
5. Read-only audit posture: do not open the sealed world files beyond what hash
   verification requires. Do not modify sealed files or SEAL.md.
6. Never remove a live .git/index.lock; wait and retry if encountered.

## Scope confirmation

- Seal commit: 396895595 (FW1-FW9 worlds sealed: 16 world files + FW6 responder).
- Audit question: has anything since the seal referenced, read, or modified the sealed
  world files, and have builders kept blindness?
- Builders of concern: CLA-2 builder, CAM-1 builder, ACT builder (all spawned after seal).

Name-check complete before any audit work began.
