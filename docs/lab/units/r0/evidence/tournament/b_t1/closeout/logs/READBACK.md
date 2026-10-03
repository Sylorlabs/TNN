# B-T1 expected-value readback probes

Independent reimplementations verify the binary's new/parameterized code
paths produce exactly the values a separate implementation computes.
All deterministic, zero RNG. Run 2026-09-21 against the B-T1 tournament
binary (arms.zag + additive `adaptive_mdl_8` leg).

## 1. MDL segmentation, SEG-row-for-row (Python reimplementation)

`readback_mdl.py` reimplements `mdl_fit`+segment for the UNGROUNDED path with
a `maxlen` parameter (mirrors the crew-validated `xcheck.py` logic).
Compared against the binary's `adaptive_mdl` (maxlen 12) and
`adaptive_mdl_8` (maxlen 8) SEG output, row for row, on 6 inputs:

- rb1.bin: repeated words ("abcdefgh"x30 + "xyzxyzxyz"x20)
- rb2.bin: 100 x 'a' (single-byte repeat)
- rb3.bin: bytes 0..255 x4 (all byte values)
- rb4.bin: prose-like sentence x60 + "spain "x40
- regress/t0.bin: empty input
- regress/t2.bin: smoke input

Result: 12/12 OK (e.g. rb4: 245 segs match at maxlen 12, 368 at maxlen 8).
The maxlen=8 code path emits strictly shorter spans and different tilings,
as expected; both match the independent implementation exactly.

## 2. Hand-computed FNV-1a chunk IDs

IDs verified against hand computation with the SIGNED Euclidean mod used by
`umod1000003` (negative i64 hash + 1000003 if negative — an unsigned mod
gives the wrong value; caught and corrected during probing):

- fixed_window_4 on "abcdefgh": SEG 0 4 <fnv("abcd")> f, SEG 4 4 <fnv("efgh")> f — OK
- raw_micro on "AB": SEG 0 1 65 r, SEG 1 1 66 r — OK
- random_chunks on "hello world": tiling rule
  h = (sum_{j=0..4}(j+3)*b[i+j] + 17*i) mod 7, L = 2+h — 3 chunks, OK

## 3. predictive_surprise cut rule

On "AB": single distinct transition A->B, p18 over 1 transition -> cut at
position 1 (p <= p18). Binary emits two literal segs with IDs matching
hand-computed signed FNV-1a (565918, 236231) — OK.

## 4. Regression vs arms-crew goldens

70 arm x input diffs (10 original selectors x 7 smoke inputs), fail=0.
The maxlen parameterization changed nothing for maxlen=12.

## 5. probe_stores.zag (ZNC-2026-09-19-001 targeted readback)

Compiled with the pinned toolchain and run 2026-09-21:

```
P1 bad=0
P2 bad=0
P3 bad=0
P4 bad=0
STORE-PROBE PASS
rc=0
```

All four hot-store patterns (hash-table insert, candidate fill, mergesort
copy-back, 8-wide sequential incl. i64 extremes) read back exactly. The
compiler miscompile class does not affect this build.
