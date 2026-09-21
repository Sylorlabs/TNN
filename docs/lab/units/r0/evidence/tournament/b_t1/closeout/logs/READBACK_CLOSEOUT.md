# B-T1 expected-value readback probes — CLOSEOUT RE-RUN (2026-09-21)

Independent re-run of every probe documented in READBACK.md, against a FRESH
build of `units/r0/impl/arms/arms.zag` (with the additive `adaptive_mdl_8` leg)
using the pinned toolchain `znc_linux_x86_64_abed8aa1 --no-zagd --no-analyze
--no-foreground-cache`. All probes deterministic, zero RNG.

Reimplementation note: `readback_mdl.py` was written from scratch for this
closeout from the Zag source (it was not present in the evidence dir). It
mirrors `mdl_fit`+`mdl_next`+emission for the UNGROUNDED path: FNV-1a/64 with
u64 wraparound, 2^20-slot linear-probe table, candidate rule
(count>=4, savings=(L-1)*count-(L+3)>0), bottom-up mergesort replicated as a
stable Python sort on (score desc, len desc, count desc, bytes asc) with slot
order as the stability key, greedy longest-match with ties broken to the
HIGHEST e (per the Zag `mdl_next` descending-e traversal with strict `>`
update), motif ids = motif index, literal ids = byte value. The hand-computed
probes below were computed from the formulas in comments/source, not from the
reimplementation.

## 1. MDL segmentation, SEG-row-for-row (independent Python reimplementation)

6 inputs (rb1..rb4 prose/synthetic, empty, smoke t2) x maxlen {8, 12} = 12
comparisons of the binary's `adaptive_mdl` (12) and `adaptive_mdl_8` (8) SEG
rows against the independent reimplementation:

```
OK rb1 maxlen=8     OK rb1 maxlen=12
OK rb2 maxlen=8     OK rb2 maxlen=12
OK rb3 maxlen=8     OK rb3 maxlen=12
OK rb4 maxlen=8     OK rb4 maxlen=12
OK empty maxlen=8   OK empty maxlen=12
OK t2 maxlen=8      OK t2 maxlen=12
```

12/12 PASS. (Header `ARMS v=1 arm=...` excluded from the diff — the arm name
differs by construction between binary and probe script.)

## 2. Hand-computed FNV-1a IDs (signed Euclidean mod = umod1000003 semantics)

- fixed_window_4 on "abcdefgh": computed ids 70200 ("abcd"), 795372 ("efgh");
  binary emits `SEG 0 4 70200 f` / `SEG 4 4 795372 f` — PASS
- raw_micro on "AB": `SEG 0 1 65 r` / `SEG 1 1 66 r` — PASS
- random_chunks on "hello world": hand-tiling via
  h = (sum_{j=0..4}(j+3)*b[i+j] + 17*i) % 7, L = 2+h gives
  `SEG 0 2 118044 x / SEG 2 6 425671 x / SEG 8 3 326913 x` — binary identical — PASS

## 3. predictive_surprise cut rule, hand-traced on "AB"

trans[65*256+66]=1, prev[65]=1, m=1 distinct transition.
tp0 = ((4*1+1)*2^32)/(4*1+256) = 82595524; p18 = tp0 (r = 18*(1-1)/100 = 0).
At i=1: p = 82595524 <= p18 -> cut. Segments [0,1) "A", [1,2) "B" with ids
umod1000003(fnv1a) = 565918 / 236231 — binary emits exactly these — PASS
(matches the hand values recorded in READBACK.md).

## 4. Regression vs arms-crew smoke goldens (10 original selectors x 7 inputs)

New binary output vs the arms crew's saved `smoke_out/o_<arm>_<t>_r1.txt`
(their binary, built from the committed pre-leg arms.zag): 70/70 diffs clean.
The maxlen parameterization changed nothing for maxlen=12.

## 5. probe_stores.zag (ZNC-2026-09-19-001 targeted readback)

Recompiled with the pinned toolchain, re-run:

```
P1 bad=0
P2 bad=0
P3 bad=0
P4 bad=0
STORE-PROBE PASS
```

## 6. Source canary

`arms.zag` contains no clock/entropy/pid/RNG references. The only
`_zag_raw_syscall` sites are syscall 0 (read) for stdin ingestion.
Comments mentioning "random" are the `random_chunks` deterministic-analog
description and the prereg zero-randomness-law header. `random_chunks` itself
is the closed-form hash-of-position rule (h = (s + 17*i) % 7), zero RNG.

Closeout readback verdict: PASS on all six probes.
