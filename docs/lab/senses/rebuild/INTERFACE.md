# SENSES REBUILD — Interface contract 2026-09-21

Both approaches implement the SAME binary contract. The harness cannot tell
them apart except by behavior and the `approach=` tag.

## Toolchain

- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Flags: `znc prog.zag --no-zagd --no-analyze --no-foreground-cache -o prog`
- Read `~/workspace/tnn-lab/toolchain/ZAG_PLAYBOOK.md` and `~/AGENTS.md` before
  writing a line. Load-bearing znc facts:
  - `argc` is always 0: read `_zag_arg(n)` unconditionally, treat "" as absent.
  - Never name a function `zalloc`; use `z_alloc`-style helpers.
  - `as []i32`/`[]u32`/`[]u16` miscompile indexed access when 2+ same-size
    casts are allocated back-to-back — use `[]u8` arenas with explicit
    little-endian put/get accessors for indexed tables.
  - `[]u8` slice `==` is NOT content identity — use integer selectors.
  - `_zag_strcmp(a,b)` returns 1 on equality.
  - No single slice > 2^25 bytes may be indexed — chunk large buffers.
  - No stray semicolon after a closing brace (`};` fails the build).
  - Bare `return;` needs the semicolon in void fns.
  - File IO: raw syscalls via the IO substrate
    (`~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag`):
    `nio_open_root(path)` / `nio_read_exact(fd,out,max)` / `nio_write_all` /
    `nio_close`. Paths must be NUL-terminated — copy via a `z_cstr` helper
    first (`_zag_arg` results are NOT NUL-terminated). `_zag_raw_syscall`
    takes exactly 7 args.
  - Initialize every array with a sentinel convention explicitly.

## Fixture formats (all little-endian, all binary)

- **Image** `.img`: u32 width, u32 height, then W*H*3 bytes RGB24.
- **Audio** `.pcm`: u32 sample_rate, u32 sample_count, then count*2 bytes
  int16 mono.
- **Video** `.vid`: u32 frame_count, u32 width, u32 height, then
  frames*W*H*3 bytes RGB24.

Fixtures live in `harness/fixtures/`. Each fixture has a sibling `.truth`
text file: `truth=<value>` (the ground-truth judgment/class).

## Binary contract

One binary per approach: `a/sense` and `b/sense`.

```
sense <task> <fixture-path>
```

- `<task>` ∈ `colordisc colorconst shapetrans pitchdisc timbredisc motiondir`
- Reads `_zag_arg(1)` = task, `_zag_arg(2)` = fixture path. (argc is 0;
  do NOT gate on it.)
- stdout: lines of `key=value`, one per line. Required keys:
  - `approach=A` or `approach=B`
  - `task=<task>`
  - `judgment=<value>` — task-specific:
    - colordisc: `SAME` / `DIFFERENT`
    - colorconst: `SAME_SURFACE` / `DIFFERENT`
    - shapetrans: `CIRCLE` / `TRIANGLE` / `SQUARE`
    - pitchdisc: `SAME` / `HIGHER` / `LOWER`
    - timbredisc: `PURE` / `BRIGHT` / `DARK` / `RICH`
    - motiondir: `STILL` / `N` / `NE` / `E` / `SE` / `S` / `SW` / `W` / `NW`
  - `confidence=0..1000` (integer per-mille; deterministic function of the
    input only)
  - `ops=<integer>` — instrumented op count (see below)
  - Approach A may add `debug_vec=<...>`; Approach B may add
    `percept=<u16-handle>` and `percept2=<u16-handle>` (second percept where
    the task compares two, e.g. the two patches).
- Exit 0 on success; exit non-zero with `error=<reason>` line on failure.
- Determinism: 3 runs of the same binary+fixture must be byte-identical
  stdout. No wall-clock, no uninitialized reads, no RNG.

## Ops counting (comparable across approaches)

Both approaches increment a single global `ops:i64` counter at the same
grain: **one op per fixture element-visit inside an inner loop** (per pixel
visited, per sample visited, per frame-element visited) **plus one op per
vocabulary/distance comparison** (each candidate compared in a decision).
Count honestly; the grain is approximate but applied identically.

## The percept boundary (Approach B only — enforced by review)

- Percepts are opaque `u16` handles into a FIXED vocabulary table compiled
  into the binary.
- The transducer (numbers → percept) is a separate module
  (`b/transducer.zag`). Its internals are not visible to the memory side.
- The memory side (`b/percept.zag`) may ONLY: hold handles, compare handles
  via the vocabulary's fixed relation table (near/far/same, table-driven),
  compose handles into small tuples (e.g. shape = 3 handles).
- It may NEVER: read the RGB/sample bytes, do arithmetic on color channels,
  expose a numeric triple as "the percept". A reviewer must be able to delete
  `transducer.zag`'s numeric code and still have `percept.zag` compile
  against handles alone. If the percept side does arithmetic on raw values,
  it is Approach A wearing a costume and FAILS review.

## Approach A constraints

- The sense delivers values: downsampled arrays, channel triples, sample
  windows are all legal as first-class representations.
- Similarity/difference = arithmetic distance with a fixed threshold.
- No percept vocabulary, no handles.

## Shared deliberate-memory rule (applied by the scorer, identically)

For each fixture the sense emits `(judgment, confidence)`. The scorer holds
installed beliefs per task-stream. Rule: INSTALL the judgment iff no
contradictory installed belief with confidence ≥ exists in that stream;
else WITHHOLD + audit-log. A false install = installed judgment contradicts
`.truth`. The rule is fixed and shared — the approaches differ only in what
their senses emit.

## Build layout

- `a_raw/sense.zag` (+ helpers), built to `a_raw/sense`
- `b_percept/transducer.zag`, `b_percept/percept.zag`, `b_percept/sense.zag`
  (main), built to `b_percept/sense`
- `a_raw/BUILD_LOG.md`, `b_percept/BUILD_LOG.md`: every build command +
  result, determinism check (3 runs byte-identical, sha256 of outputs).
- No `debate_bin`, no `.zagd` files, no `.zag-cache` committed.
