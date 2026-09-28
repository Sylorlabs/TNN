# Immediate-recall probes — S5 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F5-14 and falsehood F5-15).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F5-01-Q
Q: Enumerate the stages of the znc compile pipeline in order.
Key: The znc pipeline stages in order: parse → desugar → macro-fuse → intrinsic-lower → codegen.

### F5-02-Q
Q: How is the eviction floor computed at the consolidation sweep, and what is the fate of tier-3 records under it?
Key: The consolidation sweep computes the eviction floor as the median cite count; tier-3 records below the floor demote to tier 2.

### F5-03-Q
Q: Define a scale leg and say where its stdout SHA is stored.
Key: A scale leg is a capacity stress run at fixed fact counts; its stdout SHA is recorded in REPORT.md.

### F5-04-Q
Q: How far does the PENDING leak check reach?
Key: The PENDING leak check scans probe answers and chat answers for unverified claims.

### F5-05-Q
Q: Which fact counts do scale legs use?
Key: Scale legs run at 240, 480, 960, 2400, 4800, 9600, and 24000 facts (10x, 20x, 40x, 100x).

### F5-06-Q
Q: What is shown by the 100x leg?
Key: The 100x leg demonstrates zero scale rot: identical recall quality at 24000 facts.

### F5-07-Q
Q: Given the slice index ceiling, what is the chunking rule?
Key: Buffers above 2^25 bytes chunk to 16 MiB slices.

### F5-08-Q
Q: What purpose do MALLOC_PERTURB_ runs serve?
Key: MALLOC_PERTURB_ runs stress the allocator for nondeterminism.

### F5-09-Q
Q: What is the offset rule for back-to-back `as []i32` casts?
Key: For consecutive `nio_alloc(B) as []i32` casts: blocks sit S(B) = round_up_pow2(B) + 8 bytes apart, and every indexed access is compiled with ×8 byte scaling.

### F5-10-Q
Q: Describe the arena workaround.
Key: The arena workaround uses `[]u8` arenas with explicit little-endian accessors instead of `as []i32` casts.

### F5-11-Q
Q: What was behind the dialogue-74 panic?
Key: Dialogue-74 panicked on a 33MB slice indexing past the 2^25 ceiling; chunking fixed it.

### F5-12-Q
Q: For behavioral defects, what outperforms surface patches?
Key: Behavioral defects get white-box deep dives, never surface patches.

### F5-13-Q
Q: In what sense is the pipeline order load-bearing?
Key: Pipeline order is load-bearing: reversing macro-fuse and intrinsic-lower breaks z_alloc callsites.

### F5-16-Q
Q: How fine-grained is determinism verification?
Key: Determinism is verified at byte granularity: identical inputs must produce identical bytes.

### F5-17-Q
Q: Describe the M1 stdout SHA anomaly.
Key: Leg M1's stdout SHA diverged from REPORT.md while verdicts reproduced — a tooling bug, not scale rot.

### F5-18-Q
Q: What inputs does rerun-by-name draw on?
Key: Rerun-by-name reruns from the frozen config, never from latest sources.

### F5-19-Q
Q: Who must sign amendments, and what happens to ones left unsigned?
Key: Amendments are signed by the researcher; unsigned amendments are void.

### F5-20-Q
Q: What must accompany every scale claim?
Key: Every scale claim ships with stdout SHAs, the rerun log, and the byte-diff evidence.
