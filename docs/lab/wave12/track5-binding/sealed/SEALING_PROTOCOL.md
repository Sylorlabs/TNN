# Track 5 binding — blinding sealing protocol

**Trial:** Planted-only (A) vs learned-only (B) vs hybrid (C), Zharovia domain.
**Protocol document date:** 2026-09-25 (written post-verdict to close the
documentation gap flagged in `t5-verify/TRACK5_VERDICT_SHEET.md` §9 caveat 3).

## The seal

Sealed arm labels **X, Y, Z**. The label→arm mapping was fixed before the run
in `sealed/map.txt` (this directory):

```
X 1
Y 2
Z 0
```

i.e. **X = arm 1 (learned-only B), Y = arm 2 (hybrid C), Z = arm 0 (planted-only A).**

## The commitment (pre-run, frozen)

The frozen prereg (`prereg/PREREG_T5_BINDING.md`, freeze commit `94486ba602`,
2026-09-20T23:20:01Z) commits the SHA-256 of the sealed file *before any
results existed*:

```
MAP_SHA256 = 8e7dc59f58942ee47829d006d7a0bbc9c8ff9ee18805d3cf0230d787f9189737
```

The mapping file itself was withheld until the verdict, so the mapping could
not be altered post-result: any substituted file would fail the hash check.

## How to re-verify (anyone, any time)

```sh
cd docs/lab/wave12/track5-binding
sha256sum sealed/map.txt
# must print:
# 8e7dc59f58942ee47829d006d7a0bbc9c8ff9ee18805d3cf0230d787f9189737  sealed/map.txt
grep MAP_SHA256 prereg/PREREG_T5_BINDING.md   # frozen commitment — must match
grep -n "X=arm 1" analysis/VERDICT.md         # the reveal — must agree with the file
```

Verified 2026-09-25: file hash == frozen prereg hash == verdict reveal.
Chain intact.

## Timeline (from repo history)

| time (UTC) | event |
|---|---|
| 2026-09-20T23:20:01Z | freeze commit `94486ba602`: prereg + harness; `MAP_SHA256` committed (hash only — the file is NOT in this commit) |
| 2026-09-20T23:28:27Z | results commit `bf8bf6e16e`: evidence + analysis + verdict; `sealed/map.txt` first committed (the reveal); prereg gains the dated T1 instrument-repair amendment (the `MAP_SHA256` line itself is unmodified) |
| 2026-09-21T15:57:52Z | verdict sheet `2bfb7925c8d8`: signed weights + binding kill clauses |

## Note on the §9 "missing map" flag

`t5-verify/TRACK5_VERDICT_SHEET.md` §0.4/§9 reported the sealed map as
missing because the coordinator looked in `src/sealed/` — an empty build
scratch directory — instead of `sealed/` at the trial root. The file was
never missing: it is committed at `docs/lab/wave12/track5-binding/sealed/map.txt`
(blob `608dcdfa`), its SHA-256 matches the frozen prereg commitment, and its
content agrees with both the workstream-4/8 reveal and the coordinator's
independent empirical arm identification (X=B, Y=C, Z=A). The blinding chain
has no cryptographic gap; the gap was documentation, which this file closes.

## What the seal does and does not guarantee

- **Guarantees:** the label→arm mapping revealed at verdict time is the same
  mapping fixed before the run (tamper-evident via the pre-committed hash).
- **Does not guarantee:** that the analyst stayed psychologically blind during
  scoring (procedural; prereg protocol kill bar P3 covers the human
  adjudication step and was NOT TESTED — acknowledged in the verdict sheet).
- The trial binary never reads this file: labels and arm indices are passed
  explicitly on the command line (`bind X 1 0 1`). The seal binds the
  *analysis*, not the execution.
