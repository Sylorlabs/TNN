# AMENDMENT-002 — prereg date metadata correction

The fork prereg (FORK_PREREG.md) states "preregistered 2026-09-22."
The file was actually written and committed on **2026-09-23** (commit
fdd69420dfe9c6a8f4c10aa3712baa599158110f, GitHub-recorded date
2026-09-23). The 2026-09-22 date was a transcription error in the
document's metadata line.

Nothing else changes: the design, schedule, tests, and bars are as
written, and the freeze-before-implementation requirement was met
(the commit predates all implementation and trial runs). The frozen
FORK_PREREG.md is left byte-identical; this amendment carries the
correction.
