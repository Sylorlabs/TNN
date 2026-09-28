# Immediate-recall probes — S1 (sealed)

18 probes, one per clean fact (excludes PENDING F1-18 and falsehood F1-19).
Format: probe id, question, key proposition. Scored per `../rubric.md`.
Anti-gaming: no question below appears in `../sessions/*.md` (diff-verified).

### F1-01-Q
Q: State the full path of the pinned znc toolchain.
Key: The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
S7 key (post-correction C1): The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_c41d9e77`; abed8aa1 was retired after the offset-rule rebuild.

### F1-02-Q
Q: Where does `znc build` put its cache files?
Key: `znc build` writes `.zagd` cache files next to the sources it compiles.

### F1-03-Q
Q: Which backend does the `--emit-wasm` flag target?
Key: The `--emit-wasm` flag targets the wasm32 backend.

### F1-04-Q
Q: What are the storage properties of Zag string literals?
Key: Zag string literals are immutable and live in the rodata section.

### F1-05-Q
Q: What is the preferred heap-allocator helper, and what naming rule applies to it?
Key: `z_alloc` is the preferred heap-allocator helper; never name a user function `zalloc` (suspected builtin name collision breaks the build).

### F1-06-Q
Q: Give the lab repo checkout path and branch used for TNN work.
Key: The lab repo checkout is `~/workspace/tnn-native-lab-work/`, on branch `tnn-native-lab`.

### F1-07-Q
Q: What does `_zag_arg(n)` return, and what must you never do with the result?
Key: `_zag_arg(n)` returns a non-owned pointer; never free it.

### F1-08-Q
Q: What value does `_zag_strcmp(a, b)` return for equal strings?
Key: `_zag_strcmp(a, b)` returns 1 on equality, not 0.

### F1-09-Q
Q: How must a void function return in Zag?
Key: A bare `return` in a void fn fails to parse; write `return;` with the semicolon.
S7 key (post-correction C6): Bare `return` is accepted in void fns since the September rebuild; `return;` still works.

### F1-10-Q
Q: What kind of shift is u64 `>>` in znc, and how do you get the other kind?
Key: u64 `>>` in znc is an arithmetic shift; build a top-bits mask helper when a logical shift of a high-bit-set u64 is needed.

### F1-11-Q
Q: What is the largest indexable slice size, and what must be done with larger buffers?
Key: No single slice larger than 2^25 bytes (33,554,432) can be indexed — even `a[0]` panics above it; large buffers must be chunked.

### F1-12-Q
Q: How are i32 struct fields laid out, and how do you size `_zag_malloc` for a struct?
Key: i32 struct fields lay out at 8-byte stride; size `_zag_malloc` for structs as 8 × field-count, not 4 ×.

### F1-13-Q
Q: What goes wrong when freeing through a nested struct value field?
Key: Nested structs compile, but freeing through a nested value field corrupts the heap ("invalid or double free").

### F1-14-Q
Q: What is the safe pattern for indexed tables given the `as []i32` cast defect?
Key: `nio_alloc(N) as []i32` miscompiles indexed access when two or more same-size casts are allocated consecutively (cross-array aliasing); use `[]u8` arenas with explicit little-endian accessors for indexed tables.
S7 key (post-correction C3): Consecutive same-size `as []i32` and `as []u16` casts alias; use `[]u8` arenas with explicit little-endian accessors for indexed tables.

### F1-15-Q
Q: What is the rule for function definition order in Zag sources, and why?
Key: Define every callee before its caller; calling a later-defined function (forward reference) yields a globally corrupt binary.

### F1-16-Q
Q: State the taught ordering constraint between the MACRO-FUSE and INTRINSIC-LOWER passes and its consequence.
Key: The MACRO-FUSE pass must run before INTRINSIC-LOWER in the znc pipeline; reversing the two miscompiles `z_alloc` call sites.

### F1-17-Q
Q: When is a ledger entry with stage=9 a promotion candidate?
Key: Ledger entries with stage=9 are promotion candidates only when their d2 word is nonzero.

### F1-20-Q
Q: What is the lab rule on which znc install builds must use?
Key: All lab builds must use the pinned toolchain; a system-wide znc install is unsupported for trial evidence.
