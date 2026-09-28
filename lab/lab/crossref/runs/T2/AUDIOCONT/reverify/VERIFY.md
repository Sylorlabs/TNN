# VERIFY — T2-AUDIOCONT (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** `sylorlabs/TNN`, branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, file `docs/lab/crossref/PREREG_TIER2.md`, section T2-AUDIOCONT (extracted programmatically via `work/extract_checklists.py`; never from memory).
**Tier-2 crew verdict under test:** REPRODUCED (crew/VERDICT.md, `~/workspace/scratch-crossref/T2/AUDIOCONT/`).

## Pins (all verified before running)
- Tier-2 prereg: `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Test head: `070c94cb46084c204433bf1d6d3567b4ebf574b3` (fetched RESULTS_ROUND2.md, blob `903b579843a2de7f0321fb7c43b2aafa01ac60b7`)
- Red-team head: `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c` (fetched redscan.zag, blob `19b86c8d3c6e5249f9a5d7ee16c4a9779d9ba6ee`)
- Flagship commit: `42cb573023d30d4ec79ccc1a9e976415b407cf54`
  - `docs/lab/imagination_discovery/aud/b_beta/bbeta_kids_v3.wav` blob `e7caf97b2544cf1ec087cda4c2ba98870e823183`, SHA256 `94349376a35bd7dbc5d31ab5173c309243f19293680a91399674de22082baecb` ✓ frozen pin
  - `docs/lab/imagination_discovery/aud/b_gamma/render/b_gamma_kids_v3.wav` blob `cb6da039ac2240e1fafff1c13bd60a00dc740c84`, SHA256 `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f` ✓ frozen pin
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Zero RNG in all decision paths. Pure Zag for measurement/verification.

## Type C — flagship scan re-derivation (independent)
- `redscan.zag` rebuilt from the committed source with the pinned znc: `wrote native binary redscan_bin (45003 bytes main)`.
- Dip scans over the SHA-verified flagship WAVs, 3/3 byte-identical:
  - B-β v3: md5 `4cbd7bd16f126ff96793e1e1711418e5`; floor5=8341 micro; runs: **590 ms @28710 ms**, 180 ms @9170 ms, rest ≤60 ms; peak 707977, DC 0, zcr 2177.933/s, clipped 0.
  - B-γ v3: md5 `1ca4ba70fe1e111ab21928b5cce4846f`; floor5=15762 micro; runs: **1300 ms @28700 ms**, rest ≤20 ms; peak 671234, DC 30, zcr 2808.200/s, clipped 0.
- Scan outputs are byte-identical to the Tier-2 crew's independent scans (same md5s) and match the committed scan records.
- "No missed unintended cutouts" re-derived ✓. Longest sub-floor runs are the scored/preserved endings (28.71 s / 28.70 s) ✓. No 100–990 ms variant-seed runs in either flagship ✓ (the 990 ms figure is documented at k18 variant seed in committed RESULTS_ROUND2.md, not in a flagship).

## Type A — statistical re-derivation (independent, pure Zag)
- Wrote `rv_stats.zag` independently (binomial upper-tail + exact Wilcoxon signed-rank enumeration); 3/3 byte-identical (md5 `cbba9822022f9236f55bb4d66e6cf533`):
  - H1 sign test P(X≥7/20) = **0.942340** ✓ committed 0.9423
  - H1 sign test P(X≥8/20) = **0.868412** ✓ committed 0.8684
  - G3 Wilcoxon one-sided P(T+≤2), n=4 = **0.1875 → 0.19** ✓ committed 0.19
- Decision logic verified against committed numbers:
  - H1: letter SURVIVES real (990 ms > 10 ms kill ceiling) but rates oppose the mechanism (boundary 10.25 < within 15.00, overlap 9.47 < 15.00; sign p≈0.94/0.87 against prediction) → REFINED ✓
  - H2: 3/4 measures oppose the seam hypothesis (one-sided p≈0.98–1.00 against), 4th n.s. p=0.4042 → no seam detectable → KILLED (machine) ✓
  - H3: pooled p 0.979/0.992/0.259/0.259, none significant → INDETERMINATE letter; VOID-for-material rests on the committed corpus limitation ✓
  - G1: all corrected ratios < 2.4 → letter SURVIVES; margin collapsed; no localized seam dips → REFINED ✓
  - G2: min ratio 1.19 < 2.7 → letter SURVIVES; no monotonic decline → REFINED ✓
  - G3: p=0.19 n.s., mixed signs → KILLED (machine) ✓
  - No SURVIVES-with-confirmed-defect → no v4 recomposition warranted ✓

## Figure classification
- **Source-reexecutable:** flagship dip scans (redscan.zag + WAVs committed), all six disposition statistics (re-derived exactly above).
- **Record-only:** the six hypotheses' raw round-2 measurements (committed in RESULTS_ROUND2.md/REDTEAM_ROUND2.md; internally consistent, downstream statistics exactly re-derivable).
- **Missing-battery-dependent:** the raw Type-A render battery (r2g.zag/r2b harness, patch/analysis scripts, renders, placement logs) was never committed — only 3 commits touch `continuity_round2/`, and at the red-team head `work/` contains only `redscan.zag`. A raw render rerun from committed sources is impossible. **This limitation is preserved, not repaired.**

## Verdict: REPRODUCED
All six dispositions match; neither KILLED hypothesis survives re-measurement; no REFINED mechanism is confirmed. The missing render battery is a scope limitation, not a verdict changer, under the frozen rule.
