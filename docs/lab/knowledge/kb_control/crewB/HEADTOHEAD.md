# KB-CONTROL CREW B — Head-to-Head: Conscious vs Fast

Benchmark on identical corpus: 20,000 deterministic puts (`work/t1_batch.txt`,
lengths 20–199B via SHA-256), plus 1,000 revises and 400 delete/re-add ops.

## Throughput

| Metric | Conscious | Fast | Ratio |
|--------|-----------|------|-------|
| Appends/sec (20k puts) | 6.85 | 162.6 | **23.7× slowdown** |
| 20k put batch time | 48m41s | 2m03s | — |
| Revise (batch amortized, 1k ops) | 0.261 sec/op | — | — |
| Revise (single CLI, incl. load) | ~3.2 sec/op | ~3.2 sec/op | — |

The 23.7× append slowdown is **under the 50× prereg bar** (no redesign note
required, though the cost is real).

Single-op latency is dominated by journal-replay load time (~3 sec for 20k
records) in both modes; the batch amortizes this to 0.26 sec/op for conscious
revises.

## Storage overhead

| Metric | Conscious | Fast |
|--------|-----------|------|
| Total bytes (20k live facts) | 8,948,600 | 3,290,932 |
| Bytes/fact | 447 | 165 |
| Overhead ratio | **2.72×** | 1.0× |

Conscious breakdown (t5a store):
- journal.dat: 4.6 MB (51%) — framed intent + commit records, fsynced
- ledger.dat: 1.7 MB (19%) — 21,400 hash-chained 81-byte entries
- chunks: 2.4 MB (27%) — 594 × 4KB (data=2,384,940 bytes + trailers/padding)
- slotdir.dat + store.dat: negligible

The journal is the dominant cost. It is the price of crash-safety (intent +
commit framing, read-back verification) and the authoritative replay source.

## What the cost buys

- **K1**: Zero cross-slot clobbers across 21,400 mutations (T1+T2+T3). The
  single conscious write site (V1/V2/V3 fenced) makes clobbers structurally
  impossible.
- **K2**: 120/120 crash trials fail closed (T4).
- **K3**: Three byte-identical complete runs (T5).
- **K4**: Zero RNG (grep-verified).

The fast baseline has none of these properties: no journal, no ledger, no
read-back, no crash safety. It is a throughput reference only.
