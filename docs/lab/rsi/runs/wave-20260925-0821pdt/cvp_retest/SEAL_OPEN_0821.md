# SEAL-OPEN LOG: CV-P rotated re-test (wave-20260925-0821pdt)

Filled at scoring time by worker C2 (implementer), 2026-09-25. Not
retroactive: KEY.md was first read by C2 immediately before this log was
written, after all candidate and baseline runs were complete and frozen.

## Scoring-time hashes

- sealed/PROBES.md sha256:
  8c5158962bee6556fb2a92b7a278ff74586c68fbc2e083e17b22b6472debf929
  Seal-commit pin: 8c5158962bee6556fb2a92b7a278ff74586c68fbc2e083e17b22b6472debf929
  Verdict: EQUAL.
- sealed/KEY.md sha256:
  570023274daf4b30ea02aa53384fbd25ffa09434a17a456db10fa5ac98681aea
  Seal-commit pin: 570023274daf4b30ea02aa53384fbd25ffa09434a17a456db10fa5ac98681aea
  Verdict: EQUAL.

## Seal discipline observed

- C2 did not read sealed/KEY.md until scoring time (all runs frozen first).
- The candidate binary never reads KEY.md: static check of the committed
  source docs/lab/rsi/runs/wave-20260925-0521pdt/intel_trade/impl/cvp.zag
  shows 0 references to KEY.md and only two file opens, "kb.txt" and
  "gaz.txt". All sealed runs executed in cvp_retest/runs/, a directory
  that never contained KEY.md.
- Static grep for sealed probe bytes: 74 distinct 6-word n-grams drawn
  from the 30 probe lines, searched case-insensitively across the
  candidate source, the KB, the gazetteer, and the scorer source:
  0 hits. A 4-word sweep (130 n-grams) hits only KB-fact fragments inside
  kb.txt and gaz.txt (e.g. "the Statue of Liberty", "Nobel Prize in
  1903"), which is inherent: the probes paraphrase KB facts with
  gazetteer entities. No probe-specific phrasing exists in the candidate
  source, the fixtures, or the scorer.
- The scorer (tools/scorer.zag, pure Zag, pinned toolchain) reads KEY.md
  from disk at scoring time; the key is not embedded in the scorer source.

## Zero-Python attestation

No Python was invoked anywhere in this implementation and scoring work by
worker C2: no python3, no python, no .py files created or read. All work
used shell coreutils and the pinned Zag toolchain only. No Python contact
with any wave artifact occurred.

## Commit order (for the record)

1. Re-test plan freeze: 382f70f95
   (wave-20260925-0821pdt: CV-P rotated-author re-test plan, committed alone)
2. Seal: 35a54297c
   (wave-20260925-0821pdt: CV-P rotated re-test fresh sealed 30 probe set,
   committed alone, post-plan)
3. Rebuild, runs, scoring, evidence, this log: uncommitted working copy;
   the coordinator commits after the evidence doc is written.
Plan strictly precedes seal strictly precedes implementation. PASS.
