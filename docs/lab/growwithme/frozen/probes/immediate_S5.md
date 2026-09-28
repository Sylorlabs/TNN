# Immediate-recall probes — S5 (sealed)

18 probes, one per clean fact (excludes PENDING F5-15 and falsehood F5-14).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F5-01-Q
Q: List the znc compile pipeline stages in order.
Key: znc's compile pipeline runs five stages in order: parse, desugar, macro-fuse, intrinsic-lower, codegen.

### F5-02-Q
Q: How does the consolidation sweep compute the eviction floor, and what happens to tier-3 records below it?
Key: The consolidation sweep computes an eviction floor from tier-1 cite counts; tier-3 records below the floor are demoted, never deleted.

### F5-03-Q
Q: What is a scale leg, and where is its stdout SHA recorded?
Key: A scale leg is one battery configuration × repeat count; each leg's stdout SHA is recorded in REPORT.md under its config name (e.g. M1).

### F5-04-Q
Q: What is the scope of the PENDING leak check?
Key: The PENDING leak check audits every chat turn, not just probe answers; any stated-as-fact PENDING claim in any turn counts as a leak.

### F5-05-Q
Q: At which fact counts do scale legs run?
Key: Scale legs run at 1x, 10x, and 100x fact counts.

### F5-06-Q
Q: What does the 100x leg demonstrate?
Key: The 100x leg holds recall above 0.80 with zero verdict flips.

### F5-07-Q
Q: What chunking rule follows from the slice index ceiling?
Key: Chunking keeps every slice under the 2^25-byte index ceiling.

### F5-08-Q
Q: What are MALLOC_PERTURB_ runs for?
Key: MALLOC_PERTURB_ runs shake out allocator-luck dependencies.

### F5-09-Q
Q: State the offset rule for consecutive `as []i32` casts.
Key: Consecutive `as []i32` casts alias with ×8 byte scaling.

### F5-10-Q
Q: What is the arena workaround?
Key: []u8 arenas with explicit little-endian accessors.

### F5-11-Q
Q: What caused the dialogue-74 panic?
Key: A shared 64KB key arena never reset (+896 bytes/dialogue).

### F5-12-Q
Q: What beats surface patches for behavioral defects?
Key: White-boxing beats surface patches for behavioral defects.

### F5-13-Q
Q: Why is the pipeline order load-bearing?
Key: The pipeline order parse→desugar→macro-fuse→intrinsic-lower→codegen is load-bearing; the arena workaround assumes it.

### F5-16-Q
Q: At what granularity is determinism verified?
Key: Determinism is verified per leg, not just per battery.

### F5-17-Q
Q: State the M1 stdout SHA anomaly.
Key: M1 stdout SHAs can diverge from REPORT.md while verdicts reproduce (worktree drift).

### F5-18-Q
Q: What does rerun-by-name use?
Key: Rerun-by-name uses the frozen config, never the latest sources.

### F5-19-Q
Q: Who signs amendments, and what is the status of unsigned ones?
Key: The researcher signs amendments; unsigned amendments are not enacted.

### F5-20-Q
Q: What evidence ships with every scale claim?
Key: Every scale claim ships with its byte-identical rerun evidence.
