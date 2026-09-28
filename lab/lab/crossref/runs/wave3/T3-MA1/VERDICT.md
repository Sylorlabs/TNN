# VERDICT — T3-MA1 (conscious memory agency verification-of-record)
**Verdict: SPOT-REPRODUCED**
**Crew:** T3-MA1 · **Date:** 2026-09-24 (PDT) · **Method:** Tier-3 verification-of-record + cheapest decisive spot rerun

## Prereg integrity
- `crossref/PREREG_TIER3.md` frozen 2026-09-22, verified intact: local sha256
  `538121d2...` == sha256 of the committed blob `943ab5c9...` on `tnn-native-lab`
  (repo path `docs/lab/crossref/PREREG_TIER3.md`). T3-MA1 section extracted
  programmatically; its re-derive rule governs this verdict.

## Record verification
- MA1 lineage commits, all ancestors of `tnn-native-lab`:
  - `a0f0a60513bb3c2e7642b3ddd113b67553369120` (2026-09-19) — MA1 58/58 trial
  - `e4d1c458ea3b1a430e6396a38f1079db0e376788` (2026-09-24) — REPAIR: MA_CAP
    8→256 regression; trial.zag restored to 8-slot spec, re-verified 58/58,
    3× byte-identical, byte-identical to the 2026-09-19 evidence run
  - `23a02a19f49a9a9847170e1f81d8532403094252` (2026-09-19) — HT1 context
    switching 11/11
- All six spot-rerun sources blob-SHA-verified against the branch before running.

## Spot rerun results (clean checkout, pinned znc, ≥2 byte-identical runs)
| Bar | Result |
|---|---|
| MA1 trial: 58/58 checks, `MA_FAILURES,0` | PASS — 3× byte-identical (sha256 `244907da…`) |
| CORE-unkillable (kill_core_refused=REFUSED_CORE) | PASS |
| kill/pin/promote deliberate ops | PASS |
| Audit replay to exact state (`ledger_replay`, 28/28 entries) | PASS |
| Check battery determinism | PASS — 3× byte-identical; run stdout also byte-identical to the committed repair evidence `EVIDENCE_20260924T071512Z/run.stdout` |
| HT1: 11/11 checks, `HT1_FAILURES,0` | PASS — 3× byte-identical (sha256 `11bde0aa…`) |
| HT1 CTX arm: 11 switches / 10 flips, 0 collapsed blocks, 16/16 both regimes | PASS — number-for-number vs `TRIAL_RESULTS_HT1.md` |
| HT1 toy arm (R34 v3 negative control): 357 switches, 2 collapsed 0/16 blocks, endpoint R1 0/16 | PASS — reproduces the recorded head-to-head |
| RNG audit | Clean — HT1 curriculum uses fixed LCG seed literals (environment fixture); CTX/MA1 decision paths deterministic; MA1 core has no RNG at all |

## Anomaly (does not change the verdict, recorded for the parent)
The task's orientation pins **e8f97d28 / 1a24c9b9 / 06bc7da2 do not exist as
any object on any branch** of `sylorlabs/TNN` (API 422 on all three; full-history
clone confirms). The true MA1 verdict lineage above was substituted and verified
instead. Recommend the parent correct the pin record.

## Conclusion
The 58/58 count re-derives from committed sources and every prereg-named decisive
bar passes on independent spot rerun → **SPOT-REPRODUCED** per the §T3-MA1 rule.
Zero randomness in decision paths; pure Zag; pinned compiler.
