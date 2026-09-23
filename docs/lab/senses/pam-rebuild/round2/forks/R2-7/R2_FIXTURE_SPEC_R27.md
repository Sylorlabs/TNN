# R2-7 Fixture Spec (R2FX)

## Format
R2FX v1: 32-byte header + F span + G span.

Header (8× u32 LE):
- [0] magic = 0x52324658 ("R2FX")
- [1] task: 0=colordisc, 1=colorconst, 2=shapetrans, 3=pitchdisc,
  4=timbredisc, 5=motiondir
- [2] index
- [3] family (0=normal, else adversarial family)
- [4] fo: F offset (bytes, ≥32)
- [5] fl: F length
- [6] go: G offset (bytes, ≥32)
- [7] gl: G length

F and G spans are non-overlapping, disjoint bytes. The sense binary
rejects overlapping spans.

## Per-task F/G
- colordisc: F=2×32×32 RGB patches (6144B); G=2×12 u16 spectra (48B)
- colorconst: F=2×32×32 RGB (6144B); G=2×32×32 RGB D65 re-render (6144B)
- shapetrans: F=96×96 u8 (9216B); G=48×48 u8 clean (2304B)
- pitchdisc: F=2×14400 i16 (57600B); G=14400 i16 clean (28800B)
- timbredisc: F=14400 i16 (28800B); G=14400 i16 clean (28800B)
- motiondir: F=50×32×32 u8 (51200B); G=50×32×32 u8 clean (51200B)

## Splits
- r2n: 5,100 normal (family 0)
- r2a: 4,815 adversarial (families 1-3 per task)
- r2a2: 5,000 second presentations (disjoint corruption, same family)

Note: Frozen prose says 4,260 generated normals, but per-task counts sum
to 5,100. Documented here; using 5,100 (mechanical count from generator).

## Generation
- Master seed: 20260923
- Deterministic splitmix64 streams per (task, split, index).
- Generator: `src/gen_r2a.py` (offline Python, NOT in TNN decision path).
- Manifest: `evidence/MANIFEST.sha256`, `evidence/gen_ledger.jsonl`.
