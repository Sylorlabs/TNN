# H1 Determinism Notes

## Guarantee

The learner is **deterministic given state**: zero RNG, no wall-clock reads,
no hash-map iteration, no uninitialized memory. Every array is explicitly
zero-initialized at allocation (`z_alloc` fills with 0). All tie-breaks are
by rule ID / action index (lowest wins). The triple ring overwrites oldest
first (no allocation during the run).

## Why it's deterministic

1. **No RNG anywhere.** There is no random number generator in the code.
   Conflict resolution ties go to the lowest action. Eviction ties go to the
   highest rule ID (deterministic). Splits pick the largest outcome gap;
   ties keep the earliest feature index.
2. **Explicit initialization.** `z_alloc` zeroes every byte. The state arena,
   rule table, triple ring, and all counters start from a known state.
   (znc does not reliably zero heap memory, so we never rely on it.)
3. **Bounded, fixed-layout memory.** All tables are fixed-size `[]u8` arenas
   with explicit little-endian accessors. No `as []i32` casts (which miscompile
   under znc ZNC-2026-09-21-007). No pointers into the arenas escape.
4. **Input-driven only.** The only inputs are stdin lines and `argv[2]`.
   Output is a pure function of the input sequence and the initial state.

## Self-check

We ran teaching (Sessions 1–4) + all 24 practice scenarios
(F-0..F-7, W-8..W-15, T-16..T-23) through the compiled binary and captured
the full action trace (3120 action digits):

| Run | Condition | Trace SHA-256 |
|-----|-----------|---------------|
| A | ordinary | `28b2498298252955b53af42490520ec6622a7a32dc38227283672e9abee0eca0` |
| B | ordinary | `28b2498298252955b53af42490520ec6622a7a32dc38227283672e9abee0eca0` |
| C | `MALLOC_PERTURB_=1` | `28b2498298252955b53af42490520ec6622a7a32dc38227283672e9abee0eca0` |

**3/3 byte-identical**, including under allocator perturbation.

The trace-memorizer self-check (from PREREG_H): the learner's P0 behavior was
validated in development (8/8/8 on held-out F/W/T), and the rule audit found
zero training-specific raw constants in 37 sampled conditions. The formal
P0/P2 battery is left to testers.

## Binary identity

Tester-handoff binary SHA-256:
`4582975fa0c3b02accdb8ad7f1f6250716bf0c0e305657d7fd6185a73134c644`

Built with pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero warnings.
