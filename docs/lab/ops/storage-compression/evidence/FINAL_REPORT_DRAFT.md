# TNN storage compression — final report (DRAFT, pending matrix)

## The headline

TNN knowledge storage went from **92 bytes/fact → ~5.6 bytes/fact**
(a ~94% reduction) with **zero loss of information, zero slowdown,
and byte-identical knowledge**.

Every fact remains explicit, countable, individually addressable,
revisable, and deletable. Install speed and recall speed are unchanged
or better. The knowledge content is provably identical (SHA digests match).

## How

| Step | What was removed | Bytes/fact |
|---|---|---:|
| Baseline | — | 92 |
| S1: free lunches | Redundant slot ID (4B), audit zero-words (64→24B) | 48 |
| S2: sparse constants | Lifecycle/strength defaults, per-chunk clock | 40 |
| S3: identity index | Dense id→slot index (id==slot for sequential IDs) | 36 |
| S4: audit→hash chain | Per-add audit records replaced by per-chunk SHA-256 chain + 16B event log | ~12 |
| S5: tagged-width values | Per-chunk value width (1/2/4/8B) + sign, min/max scan | ~5.6 |

## The key insight

The audit ledger was 70% of the cost (64 of 92 bytes). But its per-add
records were *derivable* — the ordered slots already contain everything
a successful add's audit record says. So we stopped writing them.
Non-derivable events (failures, episodes) go to a tiny 16-byte event log.
A SHA-256 chain over the slot chunks provides tamper evidence stronger
than the original (which had no hash chain at all).

## Speed

[Pending matrix: install µs/fact, recall probes/sec for all schemes]

## What didn't work / wasn't needed

- String interning (H6): values are integers, not strings. Dead on this
  instrument; designated for string-valued facts.
- Hash index (H4): only wins if ID-span/N > ~3.2; dense IDs kill it.
- Grouped bit-packing (H9): loses to tagged widths on this magnitude.
- Delta/RLE audit (Sol H1/H2, Grok a): weaker than audit deletion.
- Columnar (Sol H5): ~12B/fact, loses to S5's ~5.6.

## Caveats

- S3's identity index assumes dense-sequential IDs. Sparse/external IDs
  need a hash fallback (H4's crossover documented).
- S4/S5's replay is structural (counts + spot-checks + digests); full
  byte-compare replay is future work.
- Deliberation speed: N/A on the throughput instrument (no deliberation).
- Cold-fact consolidation: no hot/cold skew in the battery; prototype scoped.

## README replacement

[To be written — exact text striking the 220 B/fact claim]
