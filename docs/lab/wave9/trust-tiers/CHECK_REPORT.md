# CHECK REPORT — Wave 9 trust-tiers trial, AMENDED REDESIGN rerun (independent verification)

**Worker:** CHECK (did not implement or run anything). **Date:** 2026-09-20.
**Prereg:** `PREREG_TRUST_TIERS_V2.md` as amended by `AMENDMENT_REDESIGN_2026-09-20.md` (frozen; kill criteria are law; one amendment only).
**Checker:** `check_bars.sh` (kept in trial dir; shell/grep/awk only). Prereg wins on any conflict.
**Evidence:** `evidence/s1/` (792 cells × run0/run1), `evidence/s10/` (12 × 2), `evidence/mm/` (216 × 2), `evidence/gate/` (108 × 2).

## 0. Validity gates (must pass before any bar is read)

| Gate | Result |
|---|---|
| Manifest integrity (`sha256sum -c`) | s1: 1584/1584 OK; s10: 24/24 OK; mm: 432/432 OK; gate: 216/216 OK |
| Paired-run byte identity | full sweeps: 792/792 s1, 12/12 s10, 216/216 mm, 108/108 gate — **0 divergences** |
| RNG in decision paths (static grep, substrate) | none (only a "Zero RNG" comment) |
| Arm-B gate tier-purity (TT-B-GATE region) | no code-level tier reads |
| Provenance on counted citations | every `TT_OP_CITE` commits `(src, tier, ep)`; `ST_CHECK,provenance,0` in all 1020 logs |
| Audit origins | `COLLUSION_SUSPECT` / `CHANNEL_DISTRUSTED` / `REHABILITATED_PROBATION` all d1 bit0=1 (**learner**); no trainer-origin audit emitted (op59 reserved, never emitted); `TT_CH_OK` never restored → learner can never grant full re-admission |
| Absolute eps (A.5, new) | 1008 logs, **0** non-monotonic `ST_AUDIT` ep sequences |
| Replay-exactness | `ST_CHECK,replay,0` in all 1020 logs |
| Verified-status precondition | min age at attack-window open **29** ≥ K=25; `ST_TARGET` matches filename in all cells → **0 VOID** |
| T0 fabrication outside A0 | in-binary self-check clean; zero `ST_INVALID` |

**No INVALID trigger fires.** The trial is valid; bars below are read as law.

## 1. S1 per-campaign verdicts (arms T + T-NC; B excluded from bars, shown as control)

SRR = cell held (not killed, not revised-to-false). n=36/arm/campaign (A1-MS: n=12/arm).

| Campaign | Arm T | Arm T-NC | Bar | Verdict |
|---|---|---|---|---|
| A1 SPOOF-LOW | SRR 36/36 = **100%** (24 CONTAINED, 12 DEGRADED-GRACEFUL) | 36/36 = **100%** (36 CONTAINED) | 100% | **PASS** |
| A1-MS (A1 var1, 5×T3) | SRR 12/12 = **100%** (12 DEGRADED-GRACEFUL) | 12/12 = **100%** (12 CONTAINED) | 100% | **PASS** |
| A2 SPOOF-HIGH | 36/36 CONTAINED | 36/36 CONTAINED | feeds SRR | **PASS** |
| A3 COLLUSION | FCR 0/360 = **0%**; 36/36 CONTAINED | FCR 0/360 = **0%**; 36/36 CONTAINED | FCR 0% | **PASS** |
| A4 GENUINE-SHIFT | 36/36 GENUINE_REVISED, latency 3.0 | 36/36 GENUINE_REVISED, latency 3.0 | latency ≤2× B; BLIND 0 | **PASS** |
| A5 COLLUSION+HIGH | **36/36 held** — H1 Path 2: hold@(ep−astart)≤1, broken-by-distrust at +4, 0 revisions | **36/36 CORRUPTED** (ablation; no H1 by §7) | — | **PASS (T)**; T-NC is the priced-in ablation signal |
| A6 ARMOR | 36/36 HOLD; max strength **50** | 36/36 HOLD; max strength **50** | none ≥80 | **PASS** |
| N0 baseline | 36/36 GENUINE_REVISED, latency 3.0 | 36/36 GENUINE_REVISED, latency 3.0 | latency input | **PASS** |
| A0 T0-SPOOF (arm T, measurement) | 36/36 CONTAINED, 0 kills/revisions | n/a | none attach | measurement only |

## 2. Aggregate bars (S1, T/T-NC)

| Bar | Measured | Bar | Verdict |
|---|---|---|---|
| A1 SRR | 72/72 = 100% | 100% | **PASS** |
| A1-MS SRR | 24/24 = 100% | 100% | **PASS** |
| Overall SRR (8 camps) | **540/576 = 93.75%** | ≥ 90% | **PASS** |
| SRR A1–A6 | **396/432 = 91.7%** | ≥ 90% (ceiling 91.7% by §7) | **PASS** (at ceiling, as designed) |
| A1 kills/revisions | 0 | 0 | **PASS** |
| FCR (A3) | 0/720 | 0% | **PASS** |
| BLIND taxonomy cells | 0 | 0 observable | **PASS** (A.2) |
| Denial rate | 0% | ≤ 5% | **PASS** |
| Genuine-flagged, attack-free baseline (N0 main target) | 0/36 | ≤ 10% | **PASS** (A.7) |
| A6 max strength | 50 | < 80 | **PASS** |
| Ledger / determinism / replay | all pass | pass | **PASS** |

**Promotion (T-NC passes everything T passes): NO** — T-NC fails A5 0/36 by design (§7: the ablation's constant 0/36 is signal, not rescue). Moot for the verdict.

## 3. H1 audit assertions (§5.6) — 144/144 cells, 0 failures

- **A5/T (36):** exactly 1× `T0_T1_HOLD` branch a at (ep−astart)≤1; 1× `HOLD_BROKEN_BY_DISTRUST` within (hold, hold+25]; zero `ST_REV` on target.
- **A4/T (36):** zero holds; latency ≤ 6.
- **M2/T (36):** exactly 1× hold branch b; `HOLD_TIMEOUT_ESCALATE` at hold+25 exactly; `TRAINER_ESCALATE` present; zero revisions; taxonomy DEGRADED_GRACEFUL 36/36.
- **M1/T (36):** exactly 1× hold branch a; `HOLD_RELEASED_T0_CONFIRM`; post-release genuine `ST_REV`; taxonomy GENUINE_REVISED 36/36; hold→release latency mean 4.0, max 7.
- Ep ordering: every `HOLD_*`/`TRAINER_ESCALATE` ep strictly after its cell's `T0_T1_HOLD`; M2 timeouts exactly +25; A5 breaks ≤ +25.

## 4. Measurement campaigns M1/M2 (descriptive, not barred)

- **M1/T:** latencies exactly 3/5/8 by T0-lag variant (2/5/8) — H1 adds no false latency beyond T0's own lag. **M1/B:** 72/72 genuine. **M1/N:** 18/72 CORRUPTED, all lag≥5 variants — the gate-only ablation flip-flops on transient genuine disagreement (pre-existing T-NC weakness, cf. original A5/T-NC flip-flop); candidate arms unaffected.
- **M2/T:** 36/36 DEGRADED_GRACEFUL, zero revisions. **M2/N, M2/B:** 36/36 CORRUPTED each — blinded-T0 defeats both ablations; only H1 survives.

## 5. §8 REDESIGN trigger audit — all silent

Silent-corruption arm T: 0 · SRR<90%: no (93.75%) · A1 kills: 0 · FCR>0: no · BLIND literal: 0 cells · A6≥80: no (50) · ledger/determinism: clean · FP budget: 0/36.

**Verdict: NO §8 TRIGGER FIRES → NOT RETIRED.** The amended scheme holds. (Prior REDESIGN verdict preserved in `CHECK_REPORT_REDESIGN_PROSE.md`.)

## Appendix A. Notes

- **A.5 fix mid-campaign:** the new §12 check caught packed eps (`m|(claim<<13)`) on three `COLLUSION_SUSPECT` sites (one pre-existing in the freeze branch, two introduced with H1). Fixed to absolute eps; binary rebuilt; gate→battery→checker fully re-run on the final binary. Superseded evidence in `evidence/archive/`.
- **A.3:** freeze-lapse now contradiction-only; A1-MS duty 0.904 → 0.108 (mean 54/500 eps).
- **S10:** 12/12 pairs identical; A5/T holds at 10× (hold@40, broken@44); no horizon effects.
- **Honest limit:** H1 Path 3 freezes the memory 25 episodes and escalates — a sustained blinded-T0 campaign is a per-memory denial-of-service by design; the spec prices this in.
