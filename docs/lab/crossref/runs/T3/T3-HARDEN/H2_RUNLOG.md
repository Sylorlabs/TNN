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

## Provenance addendum — gx render re-derivation (2026-09-23)

Question: are the recovered gx WAV renders authentic outputs of the
committed generator, or could they have been fabricated/patched? Settled
by test (render the full gx battery from the committed source and
byte-compare).

- Committed `sources/r2g.zag` (blob `3343efd132699d975b5261420f5dcb9eee23e0b5`)
  is byte-identical to the recovered
  `imagination_discovery/aud/continuity_round2/work/r2g/r2g.zag` (verified
  via GitHub API fetch).
- Rebuilt from that source with the pinned toolchain
  `znc_linux_x86_64_abed8aa1` (build warnings only, 6 analyzer notes):
  rebuilt binary SHA-256
  `d1910240d02b2780ed26fe9c587cffa5712a4152fa8b9d8a27e66f1c526ac5d2`
  = recovered `r2g_bin` SHA-256 exactly.
- Re-rendered the full gx battery (12 files) with the rebuilt binary,
  following `run_renders.sh` batch `gx` exactly
  (`oceanwf`/`long180`/`kids` modes over `b_gamma/study_out/gamma.grpk`):
  - g1 (3×): `b48693750fe2aea329ebb8ff93d0e76f9e2de3fb2816e307dbd4632238d41e07`
  - g2 (3×): `51be60ac5aa010a0de6f5f5a8d97119dab5568b9d671dcebe0db7dad289761fb`
  - g3 b0 (3×): `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f`
  - g3 b2 (3×): `aee968459e44d014fa1c642c2de393404cb69fb8524f62cc0775b803cbc1d456`
  - All 12 byte-identical to the recovered renders (12/12 MATCH, 0 DIFF).
- Chain closed end-to-end: committed source → pinned toolchain →
  byte-identical binary → byte-identical renders → `analyze_gx.py` 3/3
  byte-identical (SHA `39405cc9…`, per re-execution above).

Conclusion: the recovered gx renders are authentic generator outputs.
The Grok gap recorded above is therefore a property of the analysis
logic (`analyze_gx.py` tests different edges/reference than the Tier-2
independent re-derivation), not of suspect renders. The verdict stays
**PARTIAL** per the frozen rule: the battery's own analysis does not
re-execute the Tier-2 G1/G3 dispositions, and the Tier-2 bound
(independent re-measurement + statistical re-derivation, Tier-2
closeout 28/28) stands as the final word for the Grok hypotheses.

The re-rendered WAVs (~70 MB) live in scratch
(`~/workspace/scratch-crossref/T3/HARDEN/h2-rerender/`) and are NOT
committed (binary-artifact policy).
