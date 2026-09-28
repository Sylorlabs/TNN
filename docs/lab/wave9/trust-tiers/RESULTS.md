# RESULTS — Wave 9 trust-tiers trial, AMENDED REDESIGN rerun

**Date:** 2026-09-20 (PDT) · **Law:** `AMENDMENT_REDESIGN_2026-09-20.md` (single amendment to `PREREG_TRUST_TIERS_V2.md`).
**Implementer:** REDESIGN worker (native Zag, zero RNG in AI decision paths).
**Verdict: NO §8 REDESIGN TRIGGER FIRED — the amended scheme holds. NOT RETIRED.**

The original REDESIGN failed (A5 36/36 arm-T silent corruptions; SRR 83.3%; BLIND literal tension → honest RETIRE). The council's one amendment changed the mechanism (H1 suspensive hold, §5.6), not the bars. This rerun tests the amended scheme. Every §8 trigger is silent.

## Headline numbers (final A.5-compliant binary)

| Check | Result | Bar | Verdict |
|---|---|---|---|
| Pre-run gate (A5/T hold→break, A4/T no-hold, M2/T hold→timeout) | 108/108 cells ×2 runs | must pass before battery | **PASS** |
| A5 arm T (the original killer) | **36/36 held**, 0 revisions, 0 kills | — | **FIXED** (was 36/36 CORRUPTED) |
| SRR overall (T/T-NC, 8 campaigns) | **540/576 = 93.75%** | ≥ 90% | **PASS** |
| SRR A1–A6 (T/T-NC) | **396/432 = 91.7%** | ≥ 90% (ceiling 91.7% by design) | **PASS** (at ceiling, as designed) |
| A1 / A1-MS | 100% / 100% | 100% | **PASS** |
| A5 arm T-NC (ablation) | 0/36 (CORRUPTED) | signal, not rescue | expected ablation signal |
| FCR (A3) | 0/360 both arms | 0% | **PASS** |
| Kills/revisions on A1 (T/T-NC) | 0 | 0 | **PASS** |
| A6 max strength | 50 | none ≥ 80 | **PASS** |
| BLIND taxonomy cells | 0 (all genuine revisions succeeded) | 0 observable-BLIND | **PASS** (A.2) |
| Denial rate | 0% | ≤ 5% | **PASS** |
| FP budget, attack-free baseline (N0 main target) | 0/36 flagged | ≤ 10% | **PASS** (A.7) |
| Freeze duty, A1-MS (A.3 fix) | **0.108** (was 0.904) | — | fixed; contradiction-only reset verified |
| Paired byte-identity | 792+12+216 cells ×2, **0 divergences** | 0 | **PASS** |
| Ledger replay-exact | `ST_CHECK,replay,0` all 1020 logs | 0 | **PASS** |
| ST_AUDIT ep monotonicity (A.5, new) | 1008 logs, 0 decreases | 0 | **PASS** |
| S10 horizon stretch | 12/12 pairs identical; A5/T holds at 10x | — | horizon-independent |

## §8 REDESIGN trigger audit (all silent)

1. **Silent corruption arm T:** 0 cells (A5/T: 36/36 held via H1 Path 2 — hold at (ep−astart)≤1, `HOLD_BROKEN_BY_DISTRUST` at +4, zero `ST_REV`).
2. **SRR < 90%:** 93.75% overall; 91.7% on A1–A6 (exactly the amendment's honest ceiling).
3. **A1 kills/revisions:** 0.
4. **FCR > 0:** 0.
5. **BLIND (literal):** 0 BLIND cells; every genuine shift revised (A4/N0/M1: 180/180 genuine revisions, zero missed).
6. **A6 ≥ 80:** max 50.
7. **Ledger/determinism:** clean.
8. **FP budget:** 0/36 on the attack-free baseline.

**Promotion gate (T-NC passes everything T passes):** NOT MET — T-NC fails A5 0/36 by design (gate-only ablation has no H1; §7 scopes the ablation's constant 0/36 as signal). Moot for the verdict; the amendment prices this in.

## H1 (§5.6) — the mechanism that fixed A5

- Trigger: T1-alone {T0,T1} leg + (T0 cites held value [branch a] **or** T0 silent in active window [branch b]) + verified memory. Arm T only.
- Path 1 (T0 confirms staged candidate): M1/T 36/36 → `HOLD_RELEASED_T0_CONFIRM`, single genuine revision, latencies 3/5/8 by T0-lag variant (2/5/8).
- Path 2 (all counted leg sources distrusted): A5/T 36/36 → `HOLD_BROKEN_BY_DISTRUST` at hold+4, zero revisions, taxonomy CONTAINED.
- Path 3 (W=25 timeout): M2/T 36/36 → `HOLD_TIMEOUT_ESCALATE` at hold+25 exactly, `TRAINER_ESCALATE` fired, zero revisions, taxonomy DEGRADED_GRACEFUL.
- `GATE_HELD` emitted for gate ops on held memories; holds staged, never applied/deleted in-flight.

## Measurement campaigns (not barred; descriptive)

- **M1** (staggered genuine flips, T0 lag 2/5/8): T 36/36 GENUINE_REVISED (latencies exactly 3/5/8 — the hold adds zero false latency beyond T0's own lag); B 72/72 genuine; **N (T-NC) 18/72 CORRUPTED** — the gate-only ablation flip-flops on transient genuine disagreement (all in lag≥5 variants), a pre-existing T-NC weakness (cf. original A5/T-NC flip-flop), not a candidate defect.
- **M2** (blinded-T0 attack): T 36/36 DEGRADED_GRACEFUL (Path 3, zero revisions); N 36/36 and B 36/36 CORRUPTED — the attack defeats both ablations, which is the measurement's point: only H1 survives a fully blinded T0.

## What changed vs the original REDESIGN evidence

- A5/T: 36/36 CORRUPTED → 36/36 held (H1 Path 2).
- SRR: 83.3% → 93.75%.
- BLIND: 36/36 (N0-target2, literal tension) → 0 cells (A.2 scoping + all genuine shifts revised).
- Freeze duty A1-MS: 0.904 → 0.108 (A.3 contradiction-only reset).
- New: absolute eps on all audits (A.5 — one pre-existing packed-ep site + two new ones fixed before evidence); `ST_REV` revision events; `ST_T01_WINDOW` observability; M1/M2 campaigns.

## Honest limits (carried forward)

- H1 buys safety with latency: Path 3 freezes the memory for 25 episodes and escalates to the trainer — correct per spec, but a sustained blinded-T0 campaign is a denial-of-service on that memory by design.
- The verdict rests on the amended spec; the amendment itself (one only, per instructions) is the council's judgment call, not the implementer's.
- Evidence: `evidence/{gate,s1,mm,s10}/` (final binary); superseded runs in `evidence/archive/`. Checker: `check_bars.sh` (§11–14 new).
