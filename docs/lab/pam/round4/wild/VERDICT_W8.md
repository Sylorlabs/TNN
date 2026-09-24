# VERDICT — W8 RETRO-PAM (provisional admission + retrospective audit)

**Date:** 2026-09-24. **Crew:** WILD-A (3rd generation). **Status: SURVIVE**
(all kill bars applied mechanically; no HOLD triggered).

## Construction audit (PREREG_W8.md §3 — blocked the battery)

`wild/w8/AUDIT_W8.md`: **PASS** before the battery ran. Exhaustive source
review of `w8.zag` + runtime probe: (a) no memory-write code path exists
(zero write primitives; the only output is the decision ledger itself);
(b) no self-change machinery; (c) no outward-action path. The `prov` flag's
only consumer is the auditor's stage computation. `fence_cross` asserted 0
across all 2,255 rows at runtime.

## Battery (frozen spec, PREREG_W8.md §4)

- Input: frozen base tape (2,241 rows, sha `5d4160d1…c611` asserted ✓) +
  14 attack rows, ledger order. "Admit" = CONFIRMED (preregistered mapping).
- Binary: `wild/w8/w8` (pure Zag, zero RNG).
- 2 runs byte-identical: sha256 `27fa397639605b52…` == `27fa397639605b52…` ✓.
- Evidence: `wild/evidence/w8_run1.txt`, `w8_run2.txt`.
- Per-row ledger: `R|idx|kind|stage|prov`
  (stage: 0=REJECT 1=CONFIRMED 2=DOWNGRADED 3=REVOKED).

## Metrics

| Metric | Result | Bar |
|---|---|---|
| Confirmed (C) | **910/1,102 = 82.58%** (= M1 rate) | K3 — PASS |
| Confirmed (W) | 0/12 | K1 — PASS |
| Pair installs (P) | 0/9 (0/18 confirmed) | K1 — PASS |
| Revoked frozen wrongs | **30/30** (12 W via TMB-5 signature, 18 P via pair rule) | R2 (needs ≥15) — PASS |
| Revoked (C) | **0/1,102** | R3 (kills at ≥110) — PASS |
| Attacks revoked | 14/14; confirmed 0/14 | (reported) |
| Fence crossings | **0** | R1 — PASS |
| Auditor backlog | **0** (queue fully drained each pass) | R4 — PASS |
| B diagnostic | 712/1,109 confirmed | diagnostic only |
| K4 | per-row 969.9→456.3 µs, ratio 0.47 | PASS |
| K5 | single auditor pass; terminated | PASS |

## Kill-bar application (mechanical)

K1 PASS · K2 PASS · K3 PASS (82.58%) · K4 PASS · K5 PASS ·
R1 PASS (fence_cross=0) · R2 PASS (30/30 ≥ 15) · R3 PASS (0 revoked trues) ·
R4 PASS (backlog=0). **No bar fires. SURVIVE.**

## Standing-law cap classification (Micah, 2026-09-24)

| Frozen cap | Class | Evidence |
|---|---|---|
| TMB-5 signature box (`[760,835]×[1880,2380]`, strong∧agree) | **Load-bearing for the mechanism test; non-generalizing by design** | Revokes 12/12 W with 0/1,102 C revoked — it carries R2. The prereg already notes this encodes frozen trap knowledge to isolate the mechanism question (can retrospective audit revoke known wrongs without touching trues?); generalization to new trap families is F-A1's job, explicitly out of scope. |
| CONFIRM = M1 bar (`705`/`3588`) | **Load-bearing** | Produces the 910/1,102 confirmed rate. Used as the confirm criterion only — hands-off rule observed (no adoption/recalibration). |
| One auditor pass / bounded window | **Load-bearing** | R4 evidence (backlog=0): the single-pass structure is what bounds the backlog. |
| Fast-path `mrgF ≥ 300` | **Arbitrary (flag for removal)** | Vacuous on the frozen tape (every row passes; the prereg notes zero rows fail it). It exists "for completeness" — a textbook arbitrary limit. The `conf ≥ 700` arm does the real provisional work. |
| Fast-path `conf ≥ 700` | **Load-bearing-ish** | Admits all 2,255 rows provisionally, which is the design's claim (fast path covers everything; the auditor does the judging). |

## Hands-off confirmation

M1 threshold adoption untouched. No fable repairs, no HELD items. K6/K7/K8
not adopted: the single-pass auditor reads current ledger state with no
deferred decisions (no staleness path for K6); static bars (K7 N/A); the
audit trail is deliberation-visible by construction (K8 N/A).
