# Arm N Verdict: PASS

**Arm:** N — Judgment-annotated chunks (ANN)
**Round:** r1, scale 1x
**Date:** 2026-09-21

## Corrections acknowledged

**First correction (2026-09-21):** The original "No-ID memory" dispatch was
erroneous and is VOID (coordinator correction). The true frozen arm, verified
from `~/workspace/tnn-lab/units/arms/briefs/N.json` and `PREREG_FREEZE.md:532`,
is **N — Judgment-annotated chunks** (family ANN). All work, evidence, and this
verdict pertain to the corrected arm. No-ID results are excluded.

**Second correction (2026-09-21):** The coordinator's earlier message(s) quoted
the frozen §3 row as paraphrase from memory — that paraphrase is superseded and
was NOT built or scored against. The verbatim frozen §3 row (byte-verified by
the coordinator against frozen commit `b0b9140c0eda` via the GitHub API) is
authoritative. On 2026-09-21 I programmatically byte-compared
`briefs/N.json` (authority #1) against the verbatim row (authority #2):
name, family, mechanism, and kill fields are **byte-identical** — no
disagreement, no block. The implementation, battery, and scoring below were
built per the brief text, which is exactly the verbatim frozen row.

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
