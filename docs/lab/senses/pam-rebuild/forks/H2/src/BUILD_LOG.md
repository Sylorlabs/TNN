# H2 — Build log

How the H2 implementation was produced, in order. This is a build diary, not
architecture: the architecture is `src/sense_h2.zag` (pure-Zag percept
pipeline) and `src/memgate.zag` (pure-Zag memory contract gate).

## Starting point (2026-09-23)

The fork inherited substantial uncommitted local work from earlier crews:
`src/sense_h2.zag`, `src/lut.zag`, `src/h2_gen.py`, copied IO/SHA substrates,
and a partially generated fixture corpus. Nothing was committed yet. The
frozen prereg (`forks/H2/PREREG_H2.md`) was not touched and was never
recommitted.

## Repairs to `sense_h2.zag` (implementation defects, prereg untouched)

1. **colordisc vocabulary bug.** The pipeline emitted `SAME_SURFACE` for the
   colordisc task; the frozen vocabulary requires `SAME`. Fixed.
2. **timbre centroid scale bug.** The centroid was computed in Hz-like units
   but compared against per-mille class boundaries (1075/1400/3000), which
   made every timbre judgment nonsense. Replaced with the per-mille form
   `1000 * Σ(h·E_h) / Σ(E_h)`.
3. **Dead O(n²) timbre DFT.** Removed an unused full FFT-like nested loop;
   kept the direct harmonic-energy measurements only. Large operation saving.

Rebuilt with the pinned toolchain
(`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`):
`znc: wrote native binary sense_h2 (198853 bytes main, 0 external tools)`.
The binary is local-only and never committed.

## Smoke test (2026-09-23, one frozen primary fixture per task)

| task | truth | H2 judgment | program | H2 ops | A ops |
|---|---|---|---|---|---|
| colordisc | SAME | SAME | PASS | 1,568 | 8,193 |
| colorconst | SAME_SURFACE | SAME_SURFACE | PASS | 1,568 | 8,193 |
| shapetrans | CIRCLE | CIRCLE | PASS | 6,593 | 27,651 |
| pitchdisc | SAME | SAME | PASS | 1,483,880 | 4,521,065 |
| timbredisc | PURE | PURE | UNRESOLVED | 768,564 | 2,293,308 |
| motiondir | STILL | STILL | PASS | 4,313 | 28,674 |

Correct vocabulary and plausible judgments on all six. Approach A was rebuilt
from its committed source (`senses/rebuild/a_raw/sense.zag`) at
`senses/rebuild/a_raw/sense` for the head-to-head.

## `memgate.zag` — memory contract gate (new, pure Zag)

Implements the preregistered executable-memory contract natively:

- Input record per trial:
  `seq|tcode|fixture|prog|jcode|judgment|confidence|pred|measure|phash|truth`
  (truth is carried through for scoring only; gate rules never read it).
- FAIL → NEGATIVE_EVIDENCE stored, nothing installed.
- UNRESOLVED → WITHHELD.
- PASS + prediction → PROVISIONAL_INSTALL (reversible).
- A later PASS with the same judgment and an in-tolerance measure →
  PERMANENT_INSTALL (corroborated).
- A conflicting PASS while provisional → REVERSED.
- A conflicting PASS against a permanent program → CONFLICT_WITHHELD
  (robust: the durable memory wins).
- A PASS whose measure matches stored negative evidence → SUPPRESSED.
- Later consistent PASS against a permanent program → CORROBORATED.
- Per-task frozen tolerances (from PREREG_H2.md §2, in memgate source):
  colordisc Δ(dist)≤8, colorconst ≤40 per-mille, shapetrans ratio Δ≤60
  per-mille, pitchdisc dppm Δ≤4000, timbredisc r Δ≤120, motiondir same
  octant or both STILL (exact measure match); prediction required to promote.
- Native SHA-256 hash chain over canonical disposition records:
  `prev_hex|hash_hex|canonical_record`, where
  `hash = sha256(raw_prev_32_bytes || canonical_record_bytes)`.

A unit test (7 hand-authored records) exercised every transition:
provisional→permanent, conflict-withheld against permanent, reversal,
negative-evidence suppression, unresolved withholding. The ledger chain was
independently verified in Python (`hashlib.sha256`), and memgate reruns are
byte-identical.

One implementation bug was found and fixed during testing: the fixture field
was clobbered by a scratch parse of the judgment field (buffer aliasing);
a dedicated fixture buffer was added.

## Fixture generation (deterministic, uncommitted corpus)

`src/h2_gen.py` generates the frozen-count corpus: 4,260 normal + 4,815
adversarial fixtures (plus `.truth` sidecars), all seeds derived
deterministically from `(task, variant, index)`. Generation was first run
serially, then — when the timbre boundary-search proved slow — sharded by
`(task, adv, index-range)` across 9 parallel workers (`/tmp/h2_worker.py`,
scratch only). Every worker skips already-existing indices; a drift check
regenerated a sample of pre-existing fixtures with the current script and
confirmed byte-identical output, and 88 sampled pre-existing files hashed
before the restart still match after the full run (`sha256sum -c`, 0
failures). Final counts verified mechanically: 4260/4815, no missing
indices. The committed `evidence/FIXTURES_MANIFEST.sha256` records the
exact corpus bytes; the corpus itself is not committed.

## Evaluation

`src/eval_h2.py` (test harness only): runs `sense_h2` and the rebuilt
Approach-A binary over the identical ordered 10,000-trial suite, parses and
validates all stdout keys/vocabularies, feeds H2 records through memgate,
independently verifies the ledger, runs the contract-less shared-rule
ablation, and computes B1–B5, the H2 kill criteria, and the B6 inputs.
`src/det_h2.py` runs the B6 determinism protocol (60 fixtures × 3 runs,
memgate × 3, independent ledger recompute, Approach-A × 3).

Harness robustness fix (2026-09-23, no frozen bar/tolerance/contract rule
touched): the 10k-ledger file write in memgate flaked intermittently
(2 failures in 6 runs, `error=ledger_write_failed`, always under extreme CPU
oversubscription — two 12-thread evals on 2 cores) while every successful run
emitted a byte-identical ledger (5/5 identical, valid 10,000-link chain).
`eval_h2.py` now retries the memgate invocation (up to 6 attempts) instead of
asserting on the first attempt. The contract logic itself never failed; only
the ledger file write did.

Binary-snapshot fix (2026-09-23, harness only): the 02:02 UTC eval run lost
4,355/10,000 trials because another crew deleted and rebuilt
`senses/rebuild/a_raw/sense` mid-sweep (binary absent ~02:02–02:13; every
error was `ENOENT` on the A path, H2 side clean). `eval_h2.py` now snapshots
both binaries into `evidence/_evalwork/` at sweep start, verifies presence,
and records both SHA-256s in `metrics.json` (`sense_h2_sha256`,
`sense_a_sha256`). The A snapshot is byte-identical to a fresh rebuild from
committed `sense.zag` with the pinned toolchain (verified 2026-09-23:
`68db15216d9dc75a10839212ac5349195248f5ae113a7e37dc336795db8e35a1`).

Both binaries' run health (clean runs, bad-read counts) is reported by the
eval itself in `evidence/metrics.json`.

## Committed files

- `src/sense_h2.zag`, `src/lut.zag` — pure-Zag H2 percept pipeline + tables
- `src/memgate.zag` — pure-Zag memory contract gate
- `src/h2_gen.py` — deterministic fixture generator
- `src/eval_h2.py`, `src/det_h2.py` — test-only harnesses
- `evidence/EVIDENCE_H2.md`, `evidence/LEDGER.md`,
  `evidence/PROGRAM_EXAMPLE.md`, `evidence/metrics.json`,
  `evidence/FIXTURES_MANIFEST.sha256`
- `src/BUILD_LOG.md` (this file)

Never committed: compiled binaries (`src/sense_h2`, `src/memgate`, the
rebuilt A binary), `.zag-cache/`, `.zagd.semantic-ready`, scratch probes,
`__pycache__/`, or the generated fixture corpus.
