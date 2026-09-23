# H2 — AUDIOCONT Battery Recovery: RUNLOG

2026-09-23. Tier-3 hardening probe H2 (prereg `PREREG_TIER3_WAVE2.md`).

## Recovery

- Located the battery at
  `~/workspace/tnn-lab/imagination_discovery/aud/continuity_round2/work/`
  (~1.4 GB): `r2g/r2g.zag`, `r2b/*.zag`, `patch_r2*.py`,
  `analyze_common.py`, `analyze_h1/h2/h3/gx.py`, `run_renders.sh`,
  `r2_scores.zag`, WAV renders, placement logs, `*_results.txt`.
- Recursive GitHub tree check: only `redscan.zag` committed under
  `continuity_round2/work/` — the Type-A gap was real.

## Re-execution

- Ran `analyze_h1.py`, `analyze_h2.py`, `analyze_h3.py`, `analyze_gx.py`
  3× each (background sessions proc_9775ab247271, proc_16437f930b49).
- First h1 batch failed (rc=120, empty output) — cwd issue; reran from the
  work dir, all rc=0.
- All 12 outputs byte-identical (SHA-256 r1=r2=r3):
  h1 00aa83b0…, h2 0c96afd3…, h3 edeffef7…, gx 39405cc9….
- Outputs match recovered `h1_results.txt`, `h2_results.txt`,
  `h3_results.txt`, and `g3_results.txt` (G3 section).

## Disposition verification

- Sol-H1 REFINED ✓ (p=0.9423, 0.8684; 990ms max run)
- Sol-H2 KILLED ✓ (299/300; modchange p=0.4042 n.s.)
- Sol-H3 VOID/INDETERMINATE ✓ (p=0.2593 n.s.)
- Grok-G1 REFINED ✗ (script tests different edges; ratios differ)
- Grok-G2 REFINED ~ (ratios EXACT match; mechanism-contradiction not in script)
- Grok-G3 KILLED ✗ (script: INDETERMINATE; T2's p=0.19 from their Wilcoxon)

## Result

Verdict **PARTIAL** (see `H2_VERDICT.md`). Sol battery GAP-CLOSED;
Grok battery does not reproduce T2 — the T2's G1/G2/G3 statistics came
from the crew's independent re-derivation, not from `analyze_gx.py`.
Tier-2 bound stands for the Grok hypotheses.

## Commit

Sources only (no WAVs/binaries/caches) under
`crossref/runs/T3/T3-HARDEN/evidence/audiocont-battery/` with SHA manifest.
