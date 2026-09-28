# Contender A — Failure modes (where it breaks that others don't)

## 1. COST: ~46% slower single-threaded than native (measured, fundamental)

6 interleaved runs, equivalent s32-mix output: A median 6.40 s, native 4.38 s.
Every A run slower than every native run. Root cause: pure `f(plan,t)`
recomputes oscillator phase per sample per voice with integer division;
native's carried phase is one addition per sample. This is the architectural
price of statelessness, not a bug. PAR's multi-core dividend is not
demonstrated by this single-threaded binary. **Where native wins that A
doesn't: raw single-core throughput.**

## 2. Memory: full-plan materialization

A holds the entire plan, event table, and full-length mix in memory
simultaneously (mix = 8 bytes/sample × duration; the 2^25-byte slice limit
forced the streaming path for >~6 min renders). Native's sequential renderer
can stream with O(1) state. For very long renders A needs the windowed
`seq+streammix` path (verified bit-identical). **Where native wins: constant-
memory streaming.**

## 3. Malformed plan text degrades silently (not rejected)

9 adversarial inputs tested: empty event list, negative duration, 20 kHz,
amp 0, amp 999999, event beyond duration, nonnumeric fields, short event,
triple overlap — none crash or hang, but malformed fields degrade to
silence/bed rather than raising errors (e.g. negative duration → bed-only,
nonnumeric → zero). A strict rail-pin policy would reject; A is permissive.
**Documented behavior, not a crash. Whether §5 wants rejection is an open
prereg question.**

## 4. RESPOND cannot see other RESPONDs' resolutions

By design (order-free formation): pass 2 resolves every RESPOND against the
immutable non-RESPOND spec table only. A RESPOND whose cue is itself a
RESPOND's resolved pitch will NOT chain — it sees the nominal. This is
correct per the order-free semantics (no resolution order exists), but it
means multi-hop cross-references don't propagate. **Native's sequential
formation would chain them (order-dependent).**

## 5. SPMAX=128 / SLMAX=64 capacity caps

The spec table (128) and slot table (64) are fixed-size. Beyond capacity,
RESPOND slots are skipped (guarded, no crash) and events are dropped. Native
has no such cap. Realistic themes are far below it, but it is a hard ceiling
A has and native doesn't.

## 6. No output-adaptive behavior (by construction)

A cannot do anything that requires reading rendered output: no servo
correction, no adaptive dynamics, no feedback-based effects. RT-LONG shows
this as a *strength* (no servo drift: 0.00 vs +53.27 cents), but any task
requiring closed-loop control is inexpressible in pure PAR. **Contender C
(bounded-feedback AR) exists precisely for this gap.**

## 7. Phase-recompute quantization

Pure `f(plan,t)` phase via integer division is exact per sample, but any
future change of arithmetic precision changes ALL samples (no error is
"carried and forgotten"). Deterministic, but brittle to implementation
change — byte-identity is pinned to the exact integer pipeline.

## Summary

A's failure modes are the mirror of its strengths: it pays time and memory
for independence, cannot adapt to its own output, and caps capacity. None
caused a §2 bar failure. The COST deficit is the only one that blocks a
clean §6 overthrow.
