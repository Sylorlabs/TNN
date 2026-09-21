# Arm N Verdict: PASS

**Arm:** N — Judgment-annotated chunks (ANN)
**Round:** r1, scale 1x
**Date:** 2026-09-21

## Correction acknowledged

The original "No-ID memory" dispatch was erroneous and is VOID (coordinator
correction, 2026-09-21). The true frozen arm, verified from
`~/workspace/tnn-lab/units/arms/briefs/N.json` and `PREREG_FREEZE.md:532`, is
**N — Judgment-annotated chunks** (family ANN): chunks carry deliberate signed
annotations (MA4 generalized from memories to units); signed i64 fixed-point;
saturating overflow; ablation records judgments but ignores them during recall.

All work, evidence, and this verdict pertain to the corrected arm. No-ID
results are excluded.

## Binding kill criteria — none fired

1. **(i) Full beats judgment-free control by ≥5pp on adversarial
   misleading-memory bar:** full=71.5%, control=66.5%, margin=**5.0pp**.
   → NOT FIRED (meets ≥5pp; margin is exactly at threshold — noted as thin).
2. **(ii) Ablation within 2 points of full:** |71.5−66.5|=5.0 > 2.
   → NOT FIRED (judgments are not decoration).
3. **(iii) >10% chunks flip sign >2× in 100-episode window:** 0.0%.
   → NOT FIRED (no churn).

## 1x battery (M1–M9 + adversarial)

| Mode | Result | Bar | Status |
|------|--------|-----|--------|
| M1 prose | 100.0 / 100.0, swap 64/64 | recall ≥95% | PASS |
| M1 code | 100.0 / 100.0, swap 64/64 | recall ≥95% | PASS |
| M2 (×4 tiers) | 1 episode, 100.0 final | criterion | PASS |
| M3 | 100.0 / 100.0, CLEAR | survival | PASS |
| M4 prose | 100.0 / 100.0 | revision ≥70% | PASS |
| M4 code | 100.0 / 100.0 | revision ≥70% | PASS |
| M5 | 84,731 units, cost accounting | informational | PASS |
| M6 p2c | 100 / 100 / 100, tax 0.0 | rec ≥95, bnd ≥90, rev ≥70 | PASS |
| M6 c2p | 100 / 100 / 100, tax 0.0 | rec ≥95, bnd ≥90, rev ≥70 | PASS |
| M7 | hit 100.0%, reuse 2.02, dedup 49.6% | ≥90% / ≥1.5 / ≥40% | PASS |
| M8 | 5×5 artifacts + stdout byte-identical | determinism | PASS |
| n-adv | full 71.5 / ctl 66.5 / abl 66.5 / churn 0.0 | kills (i)(ii)(iii) | PASS |

## 10x scale

**ATTEMPTED — FAILED.** The r10 corpus (52M/91M) exceeds the znc toolchain's
2^25-byte per-slice limit: `read_file` refuses files >33,554,432 bytes, and the
corresponding ledger (54MB) and slot tables (54MB) would also exceed it. This
is a toolchain constraint, not an arm mechanism failure. No 10x row is claimed.

## Provisional (pending Micah's freeze)

- A15 ID-swap schedule (M1).
- A7/A8 M7 edit/lookup schedules.

## Verdict

**PASS.** No binding kill criterion fired. All 1x bars pass. Determinism gate
(M8) holds. The 5.0pp margin on kill (i) is exactly at threshold and is
flagged for scrutiny, but it meets the preregistered ≥5pp bar.
