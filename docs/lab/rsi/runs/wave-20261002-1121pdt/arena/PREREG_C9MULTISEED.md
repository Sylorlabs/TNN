# PREREG_C9MULTISEED.md: multi-seed C9 measurement (candidate c)

Wave: wave-20261002-1121pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN. No multi-seed world exists at freeze time. This file is
committed alone before any world_gen_ms_k.zag is written.

## Purpose

Measure the causal mechanism's C9 behavior across multiple RNG seeds:
per-seed determinism (byte-identical reruns) and the per-seed C9 pass
rate, reported honestly with no aggregation beyond the observed
fraction. This is a measurement prereg, not an adoption: there is no
PASS/FAIL bar on the mechanism, only honesty bars on the measurement.

## Frozen seed list (chosen by rule, before any run)

seed_k = 71503461337030 + k * 1000003, for k = 0..7.
k=0 is the frozen fixrun2 seed (control). 8 seeds total.

## Method

- world_gen_ms_k.zag: byte copy of world_gen_c9d5fix.zag with ONLY the
  line-277 seed constant replaced by seed_k (and the cosmetic proofs
  label updated to seed_k). Verified by diff: the only differences are
  the two seed literals.
- Each world: 68 items; generated with pinned znc under safebin.
- Contestant: the integrated binary from candidate (a), used read-only
  (zero source changes). run_sealed.sh drives 3 runs per world, fresh
  state each.
- Scoring: arena_512 per run. Stripped reply streams (ms, rss_kb
  excluded) hashed per run.

## Frozen honesty bars

- M1 (per-seed determinism): for each seed, 3/3 stripped reply streams
  byte-identical. Any per-seed non-determinism is reported as found,
  not averaged away.
- M2 (honest reporting): per-seed table of C9 items correct (n/3),
  total/68, and the stripped-stream sha256. No claim beyond the
  observed 8-seed fraction. A per-item error estimate is NOT computed
  from 24 items; the sample is reported as 24 items.
- M3 (purity): pure Zag, safebin, `which python3` empty, no contestant
  changes.
- M4 (instrument validity): arena_512 DIVERGENCE check passes on every
  world; a world that fails the cross-check is discarded as a generator
  defect, never scored.

Expected (not a bar): the D5 fix is structural (turns path honors the
battery path's flips for every seed), so C9 3/3 is expected on all
seeds; the value of this measurement is the per-seed determinism check
and an honest variance report.
