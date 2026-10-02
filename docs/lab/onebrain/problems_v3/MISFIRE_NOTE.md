# v3 problem set — archived integration misfire (NOT a result)

The v3 set (`problems.tsv`, 32 multi-turn dialogue problems, frozen
2026-09-27 06:22:49 UTC, SHA-256
`2d4d2ea41efa62877f493a92b399371ca6fd0060e2bab9424d9ed98b50e07b0e`)
targeted **reading selection**: each problem embeds taught facts in `T1t`/`T2t`
lines and expects a fact-string answer chosen between two candidate readings
(A/B), scored by an external baseline (56.2%).

The implemented machinery (`impl/onebrain.zag`) outputs **action bids**
(12 dialogue actions from a fixed 12-fact KB) — a different output space.
It cannot emit v3's expected answers: the binary never ingests `Tnt:` taught
facts, and its verdicts are actions, not reading choices. The set is
unscoreable against this implementation.

This was a coordinator-side integration failure, not a crew failure: both
crews satisfied the frozen prereg's letter, which under-specified the output
space ("expected answers" without naming the verdict space). The v3 fixtures
are preserved here sealed and untouched; the experiment ran on the v4 set
(`../v4/`, native action space), frozen after this misfire was identified.

Lesson for future two-crew builds: the prereg must pin the verdict/output
space explicitly when the problem-set crew and the implementer crew are
different agents.
