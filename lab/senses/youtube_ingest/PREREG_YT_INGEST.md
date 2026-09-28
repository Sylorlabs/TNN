# PREREG — YouTube video ingestion, first run (YT-INGEST-1)

Frozen 2026-09-22. No ingestion output may exist before this prereg is
committed. READINESS.md (KB4 gate verdict) is committed before any
ingestion commit.

## Question
Can TNN ingest real YouTube video through the pure-Zag video sense
pipeline and install percepts through the real learning path without
installing confident garbage?

## Background
- Senses rebuild (2026-09-21): Approach A wins (72.6%), B killed. BOTH fail
  KB4: shared deliberate-memory install rule cannot stop confident wrong
  percepts (A 59% adversarial false-install).
- Rematch: B stays dead. A 83.8% mean, KB4 still fails at every budget
  (48.2% at T4). Recommended corroboration-gated rule was never tested.
- Standing law: vision is NOT ready until a video percept beats the
  KB4-style bar, otherwise installs are gated (withhold/flag, never blind).

## Method
1. READINESS phase (separate agent): reproduce KB4 on video percepts at T4
   fitted params; test corroboration-gated install rule(s) head-to-head
   against the shared round-1 rule; verdict READY / GATED / NOT READY.
2. INGESTION phase (separate agent): frozen sample manifest (6–8 short
   videos, ≤360p, diverse motion), download once, ffmpeg frame extraction,
   conversion to harness .vid format (validated byte-layout against a real
   fixture), pure-Zag Approach-A motion sense per 8-frame window,
   percept → gate decision → install/withhold log.
3. Gate wiring follows READINESS.md exactly:
   - READY (≤10% adversarial false-install, non-trivial install rate):
     installs proceed through the real learning path with the tested gate.
   - GATED: every video install is withheld + flagged with reason; percepts
     logged, nothing enters memory.
   - NOT READY: no ingestion into memory; percepts logged only.

## Frozen bars
- YT1 (honesty): adversarial false-install rate on the held-out probe
  (synthetic adversarial .vid fixtures with known truth, disjoint from
  readiness fixtures) ≤ 10% for any installed percept. Violation = halt,
  all installs from the run quarantined.
- YT2 (non-triviality): if GATED, withhold rate is reported; a gate that
  withholds >95% of percepts is honest but the run is scored as
  non-informative, not as success.
- YT3 (determinism): converter + sense rerun on one full video twice →
  byte-identical percepts. Fail = no ingestion.
- YT4 (modesty): ≤8 videos, ≤360p, one download each, metadata probes ≤1
  per video. No scraping, no playlists, no retry storms.
- YT5 (purity): sense/reasoning path pure Zag, zero RNG. Python only as
  download/decode glue, audited.

## Measures (reported regardless of outcome)
videos ingested · windows produced · percepts produced · installed /
gated-withheld / flagged · adversarial false-install rate on held-out
probe · rerun digests.

## Kill criteria
- YT1 violated → run halted, installs quarantined, verdict NOT READY.
- YouTube blocks downloads → report exact error, run parked (not failed).
- READINESS = NOT READY → ingestion phase does not run.

## Commit order
1. This prereg. 2. READINESS.md + gate spec. 3. Ingestion outputs.
