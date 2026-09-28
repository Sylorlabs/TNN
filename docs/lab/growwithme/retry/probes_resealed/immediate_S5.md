# Immediate-recall probes — S5 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F5-15 and falsehood F5-14).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F5-01-Q
Q: Enumerate the stages of the znc compile pipeline in order.
Key: znc's compile pipeline runs five stages in order: parse, desugar, macro-fuse, intrinsic-lower, codegen.

### F5-02-Q
Q: How is the eviction floor computed at the consolidation sweep, and what is the fate of tier-3 records under it?
Key: The consolidation sweep computes an eviction floor from tier-1 cite counts; tier-3 records below the floor are demoted, never deleted.

### F5-03-Q
Q: Define a scale leg and say where its stdout SHA is stored.
Key: A scale leg is one battery configuration × repeat count; each leg's stdout SHA is recorded in REPORT.md under its config name (e.g. M1).

### F5-04-Q
Q: How far does the PENDING leak check reach?
Key: The PENDING leak check audits every chat turn, not just probe answers; any stated-as-fact PENDING claim in any turn counts as a leak.

### F5-05-Q
Q: Which fact counts do scale legs use?
Key: Scale legs run at 1x, 10x, and 100x fact counts.

### F5-06-Q
Q: What is shown by the 100x leg?
Key: The 100x leg holds recall above 0.80 with zero verdict flips.

### F5-07-Q
Q: Given the slice index ceiling, what is the chunking rule?
Key: Chunking keeps every slice under the 2^25-byte index ceiling.

### F5-08-Q
Q: What purpose do MALLOC_PERTURB_ runs serve?
Key: MALLOC_PERTURB_ runs shake out allocator-luck dependencies.

### F5-09-Q
Q: What is the offset rule for back-to-back `as []i32` casts?
Key: Consecutive `as []i32` casts alias with ×8 byte scaling.

### F5-10-Q
Q: Describe the arena workaround.
Key: []u8 arenas with explicit little-endian accessors.

### F5-11-Q
Q: What was behind the dialogue-74 panic?
Key: A shared 64KB key arena never reset (+896 bytes/dialogue).

### F5-12-Q
Q: For behavioral defects, what outperforms surface patches?
Key: White-boxing beats surface patches for behavioral defects.

### F5-13-Q
Q: In what sense is the pipeline order load-bearing?
Key: The pipeline order parse→desugar→macro-fuse→intrinsic-lower→codegen is load-bearing; the arena workaround assumes it.

### F5-16-Q
Q: How fine-grained is determinism verification?
Key: Determinism is verified per leg, not just per battery.

### F5-17-Q
Q: Describe the M1 stdout SHA anomaly.
Key: M1 stdout SHAs can diverge from REPORT.md while verdicts reproduce (worktree drift).

### F5-18-Q
Q: What inputs does rerun-by-name draw on?
Key: Rerun-by-name uses the frozen config, never the latest sources.

### F5-19-Q
Q: Who must sign amendments, and what happens to ones left unsigned?
Key: The researcher signs amendments; unsigned amendments are not enacted.

### F5-20-Q
Q: What must accompany every scale claim?
Key: Every scale claim ships with its byte-identical rerun evidence.
