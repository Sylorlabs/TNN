# README Replacement Text — Storage Section

## Proposed replacement for the storage claim

**Current (incorrect):** "220 B/fact"

**Proposed:**

> Knowledge storage costs **92 bytes per fact** of logical written data (measured 2026-09-22 via source inspection of the throughput learner: 24B slot + 4B dense index + 64B audit record).
>
> Three separate numbers matter:
> - **Written/logical:** 92 B/fact — the bytes actually encoding the fact.
> - **Virtual allocation:** ~156 B/fact asymptotically (eager audit-chunk reservation; ~159 B/fact at 240K due to chunk rounding).
> - **RSS:** measured separately; follows virtual with allocator overhead.
>
> There is **no persistent disk tier** — heap knowledge disappears on process exit. Persistence is future work.
>
> **Compression results (2026-09-23, definitive 1M-fact matrix, 3 reps each):**
> The S5 scheme achieves **5.53 bytes per fact** — a 94% reduction — while being 4% faster to install and 2.3x faster to recall than baseline. All 96/96 integrity checks pass with byte-identical digests.
>
> S5 combines: 12-byte compact slots, identity indexing (no dense index for sequential IDs), derived audit (successful operations reconstructed from ordered slots rather than stored per-operation), and tagged-width values (per-chunk 1/2/4/8-byte widths with signedness).
>
> Facts remain explicit, countable, individually addressable, revisable, and deletable.

## What this corrects

1. Strikes the 220 B/fact claim (was never measured; actual is 92 B/fact logical).
2. Separates written vs virtual vs RSS (previously conflated).
3. Discloses no persistent disk tier (previously implied).
4. Reports the validated S5 result (5.53 B/fact) with speed data.
