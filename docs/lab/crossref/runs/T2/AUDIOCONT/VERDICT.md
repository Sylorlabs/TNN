# VERDICT — T2-AUDIOCONT (replacement crew)

**Crew:** T2-AUDIOCONT (replacement; predecessor killed by runtime daemon restart; no partial state inherited — clean/ and crew/ were empty dirs, re-cloned).
**Date:** 2026-09-22/23 PDT. **Frozen authority:** `sylorlabs/TNN`, branch `tnn-native-lab`, commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, file `docs/lab/crossref/PREREG_TIER2.md`, section T2-AUDIOCONT (quoted verbatim below, extracted from the pinned object).

## Frozen claims checklist (verbatim, authoritative)

> **Claims:** test head `070c94cb46084c204433bf1d6d3567b4ebf574b3`, red-team head `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c`: six preregistered Sol/Grok-4.6 hypotheses tested in pure Zag, zero RNG, byte-identical — Sol-H2 bridge seams and Grok-G3 density stress KILLED; Sol-H3 frozen-bed material VOID/INDETERMINATE (test changed arrangement not material; corpus too small); Sol-H1, Grok-G1, Grok-G2 REFINED with claimed mechanisms contradicted despite letter-level survival; no hypothesis warranted v4 recomposition; B-β/B-γ v3 flagship scans: no missed unintended cutouts; longest sub-floor runs were the scored/preserved endings; H1 990ms runs only in variant seeds. Recorded defect (excluded from the verdict, tracked separately): the three blinded ear packages structurally deviate from the frozen prereg and must be rebuilt before presentation.
> **Method:** rerun the six hypothesis tests from committed sources in clean checkout (Type A); Type C re-derivation of the flagship-scan no-missed-cutouts claim from committed scan records.
> **Rule:** REPRODUCED if all six dispositions match; NOT REPRODUCED if any KILLED hypothesis survives or any REFINED mechanism is confirmed.

## VERDICT: REPRODUCED

All six dispositions match, verified from committed evidence. The KILLED hypotheses do not survive (neither shows a detectable defect on re-measurement), and none of the REFINED mechanisms is confirmed (each is contradicted by the committed measurements). One scope caveat (below) — it does not change the verdict under the frozen rule.

## Claim-by-claim vs measured

| # | Frozen claim | Measured (this crew) | Status |
|---|---|---|---|
| 1 | sol-H2 bridge seams KILLED | Committed H2 table re-verified: 299/300 edges matched; 3/4 measures run strongly opposite the seam hypothesis (one-sided p≈0.98–1.00 against predicted direction); sole in-direction measure (modulation change 0.8737>0.7513) n.s. p=0.4042. No preregistered measure detects a seam. KILLED (machine) follows. | MATCH |
| 2 | grok46-G3 density stress KILLED | Re-derived exactly in pure Zag (zero RNG, 3/3 byte-identical): bridge-vs-control diffs −0.09/+0.23/−0.44/−0.36 → Wilcoxon directional one-sided p(T+≤2)=0.1875→0.19 ✓ committed 0.19; mixed signs, n.s. Density-stress masking failure not observed. KILLED (machine) follows. | MATCH |
| 3 | sol-H3 frozen-bed material VOID/INDETERMINATE | Committed pooled p-values 0.979/0.992/0.259/0.259 — none significant in the predicted direction → frozen machine letter is INDETERMINATE (the round-2 SURVIVES default was unpreregistered). VOID-for-stated-material rests on the committed corpus limitation (19 wash + 21 wind grains; salt+700000 control reuses 95–100% of standard grains — recorded in committed RESULTS_ROUND2.md) → material claim untestable as stated. | MATCH |
| 4 | sol-H1 REFINED (mechanism contradicted despite letter survival) | Re-derived exactly in pure Zag (3/3 byte-identical): sign-test p(boundary>within 7/20)=0.942340 ✓ committed 0.9423; p(overlap>within 8/20)=0.868412 ✓ committed 0.8684. Letter-SURVIVES is real (max dip run 990 ms > 10 ms kill ceiling), but rates run opposite the mechanism (boundary 10.25 < within 15.00, overlap 9.47 < 15.00). Mechanism contradicted → REFINED. | MATCH |
| 5 | grok46-G1 REFINED | Committed corrected ratios verified arithmetically: ocean bridge midpoints 0.83/1.21/1.50/2.16/0.97, exits 1.84/1.07/1.16/1.26/0.71 — all <2.4 → letter-SURVIVES stands; margin collapsed 0.12→0.71–0.84. Scene-relative floors (0.93–2.43× midpoints) show no localized seam dips; kids reference fails its own bar at 3/5 midpoints → mechanism contradicted → REFINED. | MATCH |
| 6 | grok46-G2 REFINED | Committed ratios 1.38/2.15/1.19/2.18/4.27/2.33/1.99; min 1.19 < 2.7 → letter-SURVIVES stands. Scene-relative 1.23/0.93/1.40/1.28/1.75/1.00/2.14 shows no monotonic decline (maximum at 120 s) → accumulated-drift mechanism contradicted → REFINED. | MATCH |
| 7 | No hypothesis warranted v4 recomposition | Follows from 1–6: KILLED×2, REFINED×3, VOID×1; none is SURVIVES with a confirmed defect. | MATCH |
| 8 | B-β/B-γ v3 flagship scans: no missed unintended cutouts; longest sub-floor runs were the scored/preserved endings | **Independently re-measured (Type C):** committed flagship WAVs (SHAs verified) + committed `redscan.zag` rebuilt from source with the pinned znc. 3/3 byte-identical scans: B-β longest run 590 ms @28.71 s (next 180 ms @9.17 s, rest ≤60 ms); B-γ longest run 1300 ms @28.70 s (rest ≤20 ms). Scan outputs byte-match the committed records. A-NATIVE diagnostics match (peaks 0.707977/0.671234, DC 0/30 µ, zcr 2177.933/2808.200 /s, 0 clipped). Instrument cross-checked against numpy: peak exact, zcr exact, DC/floor exact under the instrument's documented integer-truncation semantics. No unintended cutouts. | MATCH |
| 9 | H1 990 ms runs only in variant seeds | Flagship-side re-measured: neither flagship contains any 100–990 ms sub-floor run other than its ending. The 990 ms figure is from the (uncommitted) variant-seed renders; committed RESULTS_ROUND2.md documents it at k18 (variant seed), not in a flagship. | MATCH |
| 10 | Ear packages structurally deviate (excluded from verdict, tracked separately) | Not adjudicated (out of verdict scope; no ear keys opened by this crew). The deviation is committed in REDTEAM_ROUND2.md §"Ear packages — structural validity". | NOTED (excluded per frozen rule) |

## Frozen pins (all verified; recorded before running)

- Tier2 prereg (authoritative): `7b2100d09911c5c10252c5756c7def288e70bd1f`
- Test head: `070c94cb46084c204433bf1d6d3567b4ebf574b3`
- Red-team head: `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c`
- Round-2 frozen prereg commit: `9d1dbf865e36ff3bd13a66c696af60e08fc94d95` (PREREG_ROUND2.md byte-identical across all three heads; RESULTS_ROUND2.md byte-identical between test and red-team heads)
- Flagship commits: `42cb573023d30d4ec79ccc1a9e976415b407cf54`; WAV SHAs verified: B-γ `18cb055571a8a595fa8f080adbf613188407a3c4f2815dd2e1ce41befc54eb8f`, B-β `94349376a35bd7dbc5d31ab5173c309243f19293680a91399674de22082baecb`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Clean clone: `~/workspace/scratch-crossref/T2/AUDIOCONT/clean/repo` (blobless + explicit fetches; `git fsck` clean). Zero RNG; ≥3 byte-identical runs on every re-derivation.

## Caveats / scope notes

1. **The raw Type-A render battery is not re-executable from committed sources.** Only three commits touch `docs/lab/imagination_discovery/aud/continuity_round2/`; at the red-team head, `work/` contains only `redscan.zag` — the r2g.zag/r2b harness, patch scripts, analysis scripts, renders, placement logs, and scan records were never committed (the frozen prereg promised "fixed sources committed after"; that did not happen). Per the frozen method I replicated from committed sources only: independent flagship re-measurement, instrument verification, and exact statistical/decision-logic re-derivation. The render-dependent raw numbers were verified for internal consistency and exact re-derivability of their downstream statistics, not regenerated.
2. **Task-text pin anomaly:** the dispatch text expected pin `e15eebc5c4ec`. It is not a commit/tree/blob in sylorlabs/TNN and appears nowhere in the frozen prereg or SCOPE. All pins named by the frozen authority verified; proceeded without STOP. Recommend the parent correct the template value for this crew.
3. Statistical formulation note: the committed G3 p=0.19 uses the directional one-sided Wilcoxon (T+ = sum of positive ranks, P(T+≤2)=3/16=0.1875). A min(W)-formulation gives 0.375; conclusion (n.s., KILLED) is identical either way.
4. NON-INTERFERENCE honored: no live-tree files were read into this replication beyond orientation; all measured inputs came from pinned git objects.
