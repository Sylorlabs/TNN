# H2 — AUDIOCONT Battery Recovery: VERDICT

**Verdict: PARTIAL** (Sol battery GAP-CLOSED; Grok battery does not reproduce T2)

Date: 2026-09-23. Tier-3 hardening probe H2, prereg `PREREG_TIER3_WAVE2.md`.

## Recovery

The full Type-A render battery was recovered from the T2-AUDIOCONT crew
workdir (`~/workspace/scratch-crossref/T2/AUDIOCONT/`):
`imagination_discovery/aud/continuity_round2/work/` (~1.4 GB) containing
`r2g/r2g.zag`, `r2b/*.zag`, `patch_r2*.py`, `analyze_common.py`,
`analyze_h1/h2/h3/gx.py`, `run_renders.sh`, `r2_scores.zag`, WAV renders,
placement logs, and results files.

A recursive GitHub tree check confirmed only `redscan.zag` was ever
committed under `continuity_round2/work/` — the battery sources were
genuinely absent from git (the Type-A gap was real).

## Re-execution (all 3/3 byte-identical, zero RNG)

| analysis | SHA-256 (r1=r2=r3) | recovered results match |
|---|---|---|
| analyze_h1.py | 00aa83b0… | h1_results.txt ✓ |
| analyze_h2.py | 0c96afd3… | h2_results.txt ✓ |
| analyze_h3.py | edeffef7… | h3_results.txt ✓ |
| analyze_gx.py | 39405cc9… | g3_results.txt ✓ (G3 section only) |

## Disposition comparison vs Tier-2 verdict

| # | hypothesis | T2 disposition | re-executed | match |
|---|---|---|---|---|
| 1 | Sol-H2 bridge seams | KILLED | 299/300 edges; p=0.9831/1.0000/0.9995 against; modchange 0.8737>0.7513 p=0.4042 n.s. | **YES** |
| 2 | Grok-G3 density stress | KILLED (p=0.19) | machine verdict: INDETERMINATE (no Wilcoxon in script) | **NO** |
| 3 | Sol-H3 frozen-bed | VOID/INDETERMINATE | p=0.2593/0.2593 n.s.; corpus limits confirmed | **YES** |
| 4 | Sol-H1 | REFINED | p=0.9423 (7/20), p=0.8684 (8/20); 990ms max run | **YES** |
| 5 | Grok-G1 | REFINED | script tests different edges; ratios 0.12/0.66/1.07/0.51 vs T2's 0.83/1.21/1.50/2.16/0.97 | **NO** |
| 6 | Grok-G2 | REFINED | ratios 1.38/2.15/1.19/2.18/4.27/2.33/1.99 EXACT match; letter-SURVIVES confirmed | **PARTIAL** |

## Reading

**The Sol battery (H1/H2/H3) is GAP-CLOSED.** All three re-execute
byte-identically and reproduce the Tier-2 dispositions with exact
statistic matches.

**The Grok battery is NOT closed.** The recovered `analyze_gx.py` is a
genuine artifact (its G3 section matches the recovered `g3_results.txt`),
but it does not reproduce the Tier-2 verdict's G1/G3 dispositions:
- G1: the script tests "oceanwf world-bed uniformity" at different edges
  with a different reference; the T2's "corrected ratios" (midpoints
  0.83/1.21/1.50/2.16/0.97) come from the T2 crew's independent
  re-derivation of committed evidence, not from this script.
- G3: the script verdicts INDETERMINATE; the T2's KILLED (p=0.19) came
  from their Wilcoxon re-derivation.
- G2: the ratios match exactly and letter-SURVIVES is confirmed, but the
  REFINED mechanism-contradiction (scene-relative, no monotonic decline)
  was the T2 crew's additional analysis, not in the recovered script.

**The Tier-2 bound stands as the final word for G1/G2/G3**: independent
re-measurement + statistical re-derivation (the T2 crew's work), not the
recovered battery. The recovered sources are committed for provenance.

## Artifacts committed

Under `crossref/runs/T3/T3-HARDEN/evidence/audiocont-battery/`:
- `sources/` — r2g.zag, r2b/*.zag, patch_*.py, analyze_*.py, r2_scores.zag,
  run_renders.sh (source only, no WAVs/binaries/caches)
- `re-execution/` — h1/h2/h3/gx outputs (r1, with SHA manifest for r1=r2=r3)
- `H2_VERDICT.md`, `H2_RUNLOG.md` (this file's siblings)

The 1.4 GB of WAV renders, compiled binaries, `.zag-cache`, `.zagd`, and
`__pycache__` are NOT committed (excluded by policy; listed in manifest).
