# Immediate-recall probes — S1 (RE-SEALED 2026-09-27)

18 probes, one per clean fact (excludes PENDING F1-18 and falsehood F1-19).
Re-sealed per prereg amendment AMENDMENT_2026-09-27_PROBE_RESEAL.md: fresh
paraphrases of the frozen questions; keys unchanged from the frozen set.
Scored per the frozen `../rubric.md`.

### F1-01-Q
Q: Give the complete filesystem path where the pinned znc toolchain is installed.
Key: The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
S7 key (post-correction C1): The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### F1-02-Q
Q: In which location are the `.zagd` cache files written when you run `znc build`?
Key: `znc build` writes `.zagd` cache files next to the sources it compiles.

### F1-03-Q
Q: What compilation backend is selected by the `--emit-wasm` flag?
Key: The `--emit-wasm` flag targets the wasm32 backend.

### F1-04-Q
Q: Describe how Zag string literals are stored — mutability and section.
Key: Zag string literals are immutable and live in the rodata section.

### F1-05-Q
Q: Which heap-allocator helper should be preferred, and what must user functions avoid being named?
Key: `z_alloc` is the preferred heap-allocator helper; never name a user function `zalloc` (suspected builtin name collision breaks the build).

### F1-06-Q
Q: Name the directory and branch of the lab repository checkout used for TNN work.
Key: The lab repo checkout is `~/workspace/tnn-native-lab-work/`, on branch `tnn-native-lab`.

### F1-07-Q
Q: What kind of pointer does `_zag_arg(n)` hand back, and what is forbidden on it?
Key: `_zag_arg(n)` returns a non-owned pointer; never free it.

### F1-08-Q
Q: When two strings are equal, what does `_zag_strcmp(a, b)` yield?
Key: `_zag_strcmp(a, b)` returns 1 on equality, not 0.

### F1-09-Q
Q: What is the correct way to exit a void fn in Zag?
Key: A bare `return` in a void fn fails to parse; write `return;` with the semicolon.
S7 key (post-correction C6): Bare `return` is accepted in void fns since the September rebuild; `return;` still works.

### F1-10-Q
Q: Is u64 `>>` in znc arithmetic or logical, and how do you obtain the other behavior?
Key: u64 `>>` in znc is an arithmetic shift; build a top-bits mask helper when a logical shift of a high-bit-set u64 is needed.

### F1-11-Q
Q: Above what size does indexing a single slice panic, and how must oversized buffers be handled?
Key: No single slice larger than 2^25 bytes (33,554,432) can be indexed — even `a[0]` panics above it; large buffers must be chunked.

### F1-12-Q
Q: At what stride do i32 struct fields sit, and how do you compute the `_zag_malloc` size for a struct?
Key: i32 struct fields lay out at 8-byte stride; size `_zag_malloc` for structs as 8 × field-count, not 4 ×.

### F1-13-Q
Q: What heap failure results from freeing through a nested struct's value field?
Key: Nested structs compile, but freeing through a nested value field corrupts the heap ("invalid or double free").

### F1-14-Q
Q: Given the `as []i32` cast defect, what pattern is safe for indexed tables?
Key: `nio_alloc(N) as []i32` miscompiles indexed access when two or more same-size casts are allocated consecutively (cross-array aliasing); use `[]u8` arenas with explicit little-endian accessors for indexed tables.
S7 key (post-correction C3): Consecutive same-size `as []i32` and `as []u16` casts alias; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### F1-15-Q
Q: In what order must functions be defined in a Zag source, and what happens otherwise?
Key: Define every callee before its caller; calling a later-defined function (forward reference) yields a globally corrupt binary.

### F1-16-Q
Q: Which of MACRO-FUSE / INTRINSIC-LOWER must come first in the pipeline, and what does reversing them do?
Key: The MACRO-FUSE pass must run before INTRINSIC-LOWER in the znc pipeline; reversing the two miscompiles `z_alloc` call sites.

### F1-17-Q
Q: Under what condition is a stage=9 ledger entry a promotion candidate?
Key: Ledger entries with stage=9 are promotion candidates only when their d2 word is nonzero.

### F1-20-Q
Q: Which znc installation are lab builds required to use?
Key: All lab builds must use the pinned toolchain; a system-wide znc install is unsupported for trial evidence.
