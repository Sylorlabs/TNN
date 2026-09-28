# R0 ARMS — mechanism specification

Source: `arms.zag` (single binary, `argv[1]` selects the arm). Pure Zag.
Reference: `archaeology_r31/r31_chunking_tournament.py` (recovered Python) and
`ARCHAEOLOGY_R31.md`. Old numbers are REFERENCE_ONLY — orderings, never targets.

## 1. predictive_surprise (THE thesis arm)

Recovered rule: fit transition counts on the stream; `p(a→b) = (c+.25)/(prev[a]+.25·32)`
(alphabet 32 in the reference; 256 on byte streams); surprise = −log p;
threshold = 82nd percentile of surprise over distinct transitions; cut where
surprise ≥ threshold; inventory = 256 most-common raw segments with count ≥ 3.

Native integer-faithful form (no floats anywhere):
- `pfx(a→b) = ((4c+1) << 32) / (4·prev[a]+256)` — monotone in p, fits in i64.
- Since surprise is strictly decreasing in p, "surprise ≥ 82nd percentile"
  ⟺ "p ≤ 18th percentile of p". Threshold = lower-method 18th percentile over
  distinct observed transitions ordered by (pfx asc, a asc, b asc);
  index `⌊0.18·(m−1)⌋`.
- Cut at stream position `i` iff the transition is unseen (reference: p=1e-5 →
  surprise ≈ 11.5 ≥ threshold, always cuts) or `pfx ≤ p18`.
- Inventory: segments counted in a 2^18-slot open-addressing table keyed by
  (FNV-1a, len) with byte-compare disambiguation; entries with count ≥ 3 ranked
  by (count desc, bytes asc); top 256 get IDs 0..255, rest are literals with
  `id = fnv1a64 mod 1000003`.

Deviations from the reference, all documented: alphabet 256 (byte streams);
percentile by lower method instead of linear interpolation (agrees on the
checked cases; ordering constraints only, never numeric targets); inventory
tie-break bytes-ascending (reference: Python most_common = count desc, first-seen
order — first-seen is equally deterministic; bytes-ascending chosen canonical).

## 2. fixed_window_4 / _8 / _16 / _64

Aligned windows of size w; last window may be short. `id = fnv1a64(window) mod
1000003`, kind `f`. (Reference fit a "known" set on training seqs and marked
unseen windows literal; the native single-stream form fits and segments the
same stream, so all windows are known — documented adaptation.)

## 3. adaptive_mdl

Recovered params: enumerate spans 2..12 at every position (see §8 on the 8/12
question); count in a 2^20-slot table; keep spans with `count ≥ 4` and
`savings = (len−1)·count − (len+3) > 0`; rank by (score desc, len desc,
count desc, bytes asc); top 256 motifs; segment by greedy longest-match over a
first-byte index; unmatched positions fall back to single-byte literals.
Reference `scored.sort(reverse=True)` tie-broke equal (score,len,count) by raw
bytes *descending* (Python tuple artifact); native uses bytes ascending —
flagged, ordering-only impact.

The reference "diversity filter" (`if t in seen: continue`) is a no-op over
unique spans — noted here, not reimplemented as behavior.

## 4. grounded_adaptive_mdl

`score = savings + g·count·len` with the grounding term natively adapted:
there are no class labels on a byte stream, so `g` = next-byte concentration
above chance = `max_next/total − 1/256` (downstream discrimination
consistency, cf. prereg R-1's operational definition of grounded consequence).
Computed in fixed point: `gfp = (maxnext·256)/total − 1`, term =
`(gfp·count·len)/256`; only occurrences with a following byte count (tail
occurrences excluded from both numerator and denominator — documented).
Next-byte histograms are computed for the top 8192 candidates by savings
(documented cap; exact below that).

## 5. hierarchical_mdl

Base = adaptive_mdl fit (motifs + first-byte index). Base-chunks are streamed
(O(1) memory); adjacent pair keys `(k1·1024+d1, k2·1024+d2)` counted in a
2^18-slot table; pairs with count ≥ 4 ranked by (gain=count−3 desc, count desc,
key asc); top 96 become merges. Segmentation streams base chunks with 1-chunk
lookahead: a merged pair emits kind `h` with the merge rank; otherwise the base
chunk passes through (`m`/`r`).

## 6. raw_micro — the no-chunking control

One chunk per byte, `id` = byte value, kind `r`. B-T1 requires it DEAD LAST.
Built straight: no sabotage (it gets the same clean I/O and ID path as every
arm), no rescue (no inventory, no motifs, no merges — it cannot compress or
index anything).

## 7. random_chunks — DETERMINISTIC-ANALOG (informational only)

NOT part of the binding B-T1 ordering (`predictive_surprise > fixed_window >
raw_micro`, raw dead last). The recovered reference rule was itself
deterministic ("pseudo-random lengths from local content to avoid state
leakage"); the native form keeps it exactly:

```
h = ( Σ_{j=0..4} (j+3)·b[i+j]  +  17·i ) mod 7      (bytes past end = 0)
L = 2 + h
```

`id = fnv1a64(span) mod 1000003`, kind `x`. Emits a `META deterministic-analog
…` header line and is labeled DETERMINISTIC-ANALOG in all docs and logs.
Zero RNG in any decision path — the name is historical.

## 8. The L_max 8/12 question (R-2/R-7 test-both leg)

R-2 proposes capping MDL span enumeration at L_max ≤ 8; the recovered
historical tournament used max_len=12. The prereg freezes this as an ambiguity
resolved by test-both (Micah's standing rule), not by fiat. The native
implementation parameterizes `mdl_fit(buf, grounded, maxlen)`; two selectors
expose the two legs with byte-identical code paths:

- `adaptive_mdl` — maxlen 12 (historical setting; default, unchanged behavior).
- `adaptive_mdl_8` — maxlen 8 (prereg R-2 proposal).

The grounded re-scan (§4) still enumerates spans 2..12 internally; it is only
ever invoked with maxlen=12 (`grounded_adaptive_mdl`), so behavior is
unchanged. `hierarchical_mdl` builds on the maxlen=12 base for the same reason.
An independent Python reimplementation of the ungrounded MDL fit+segmenter
matches the binary SEG-row-for-row for BOTH maxlen values on six inputs
(empty, single-byte repeat, all-256-bytes, prose-like, smoke t0/t2) — the new
code path is read back, not trusted.

## Shared determinism machinery

- Bottom-up stable mergesorts with total-order comparators; hash tables never
  iterated in probe order for output-affecting decisions (candidates collected
  by slot scan, then sorted).
- `_zag_arg` values never freed; `_zag_i64_to_str` temporaries freed after
  printing; all malloc'd buffers zeroed before use; no slice over 2^25 bytes.
- M8 smoke (`run_smoke.sh`): N=5 plain runs + 3 heap-perturbation modes +
  `setarch -R` ASLR-equivalent + clock/entropy canary audit + round-trip tiling
  check, all diffed by sha256.
