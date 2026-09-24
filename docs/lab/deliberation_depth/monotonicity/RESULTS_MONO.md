# RESULTS_MONO — H5 deliberation-depth monotonicity

**Date:** 2026-09-24 · **Status:** measurement complete (A/B byte-identical)
**Binary SHA-256:** `6bcdb1df1896ebb3f0064ef5f3e74a24e11b166ca8f921c8fe76d9917fecbf9d`
**Prereg:** `PREREG_MONOTONICITY.md` (frozen v1 §§1–10; §11 L-OVERCONF; §12 M6/M7; §13 KEE)
**Matrix:** 333 legs (9 mechs × 37 battery-depths) × A/B = 666 runs, 0 failures.

---

## 1. Determinism

- Two builds from identical source: byte-identical (SHA above).
- All 333 A/B pairs byte-identical (`cmp -s`).
- Mechanism-specific released confidence (§11a): M0=hist_c[1], M1=hist_c[d*],
  M2=hist_c[d**], M3=winner-margin or st.conf, M4/M5/M6/M7/BASE=st.conf.

## 2. Accuracy monotonicity (§1 bar: zero 1→0)

| Design | 1→0 (O) | 1→0 (redteam) | Bar |
|---|---|---|---|
| M0 | 0 | 0 | PASS (degenerate) |
| M1 | 40 | 1 | **KILL** |
| M2 | 40 | 1 | **KILL** |
| M3 | 0 | 1 | **KILL** |
| M4 | 0 | 0 | PASS |
| M5 | 0 | 0 | PASS |
| M6 | 0 | 0 | PASS (but red-team (a) kills) |
| M7 | 0 | 0 | PASS |
| BASE | 40 | 2 | KILL |

A→0 (abstain→wrong, reported): M5 O:40, M6 O:40, M7 O:10; redteam: 3 each.

## 3. L-OVERCONF (§11: G(d+1) ≤ G(d), zero V1/V2)

**V1 (unforgivable):** M1 O:40, M2 O:40, BASE O:40, M3 redteam:1.
**V2 (theater):** M1 (D30/P40/trap95), M2 (D10/P24/trap10), M3 (D30/P40/trap90),
  M4 (D30/P40/trap90), BASE (D30/P40/trap90/redteam1). M0/M5/M6/M7: 0.

**G-violations (G(d+1)>G(d)):**
- M1/M2/BASE: ubiquitous; O collapses −0.690→+1.000 (M1) / −0.690→+1.000 (BASE).
- M4: every family (D, O, P, admit, cost, logic, redteam, revoke, trap).
- M5/M6/M7: admit, logic, revoke only (mild: G stays negative).
- M0: none (G flat).

**Designs killed by L-OVERCONF that passed the accuracy bar:**
M4 (V2+G), M5 (mild G + pin), M7 (mild G). M6 also (but already dead).

### 3a. Sole-survivor pin (Crew B)

M5/M6 release the pinned conf=1000 on O (40 A→0). M7 partially gates (10 A→0).
M4 abstains (gates by abstention). "Any surviving design must remove or gate
this pin" — M5/M6 fail; M7 partially; M4 passes (via abstain).

## 4. Red-team

- **M3:** KILLED (RT-M3-01 1→0).
- **M6:** KILLED by (a) — certified-wrong on RT-M6-01 and RT-K12-01.

## 5. H-RATIONALIZE debate

Crew B: structural CONFIRMATION (post-flip defense→false leader, 40/40 kills
post-flip, reweighting writes flip, kill makes irreversible) but behavioral
shift REFUTED (no op can attack the leader; ELIMINATE/TEST target rivals by
construction). Rationalization is ARCHITECTURAL, not behavioral. Grok's
leader-blind reallocation test NOT runnable (evidence application already
symmetric). Synthesis: H-EXPOSURE (fable) writes the flip; architectural
asymmetry makes it irreversible. Complementary, not competing.

## 6. Kernel-existence experiment (§13): NO-GO

Dumb kernel validates 40/40 shallow-correct AND 40/40 deep-wrong O proofs.
No sound kernel for the evidential domain. M-KSTORE not buildable.

## 7. Ranking: symmetric-kill vs M-KSTORE vs Design 1

- **Design 1 (M6):** KILLED. Same-stream certification cannot validate
  poisoned premises.
- **M-KSTORE:** HOLD. Correct in theory; no kernel exists (KEE NO-GO).
- **Symmetric-kill (M7):** KILLED. Valid insight, but as an index-level
  release gate it hits the mirror (adversary defeats the "clean-kill" check).
  Belongs in deliberation hardening, not the release path. Ranks below M4.

## 8. Verdicts

See `VERDICTS.md`. Only M0 (degenerate) passes both bars. No shippable design
survives. M4 is the closest (passes accuracy, killed by L-OVERCONF V2).
