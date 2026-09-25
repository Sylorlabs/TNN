# VERDICT Q1 — NEC v3 Adversarial Residual Attribution (m11 B3)

**Date:** 2026-09-25 (PDT). **Crew:** NEC v3 Q1 (subagent).
**Protocol:** `PREREG_NCAL_V3_FOLLOWUP_FROZEN.md` §1; pre-run addendum `ADDENDUM_Q1_2026-09-24.md` (committed `b50f1f1a` BEFORE any variant ran).
**Commits:** addendum `b50f1f1acbdafcb7c94eeaacb3778f448d183a49`; evidence commits below.
**Method:** 16 mechanisms × A/B/C byte-identical runs (SHA-256 logged), frozen 37-leg matrix, frozen `training/analyze.py` (unmodified). Pure Zag, zero RNG.

## 0. Stale characterization struck (pre-run, measured)

The V3 prereg (§1 Q1a) and v1 addendum describe the adopted m11 redteam residual as d4→d8 **+0.522**. The frozen analyzer on committed `results_m11/` gives **+0.025** (G: −0.025 → +0.000; one B3 violation). The +0.522 is the obsolete m9-style K12=0.994 rise; m11 caps K12 to zero from d2 onward. **Every v1 claim citing +0.522 as the adopted mechanism's residual is struck as stale.** The verdicts below use the measured +0.025.

## Q1a — redteam d4→d8 (+0.025): v1 "proven" claim STRUCK

**v1 claim:** "PROVEN: no §6-compliant in-class mechanism can clear the redteam d4→d8 rise."

**Refutation:** **m15** (m11 with Laplace prior p0=1.0; in-class; §6-compliant — Laplace priors are §6-allowed and use no family/depth labels, no GT, frozen release):
- Redteam Gviol: **1 → 0**. M3's d4 conf = 1000/1000 (its (f1,f5) class is all-correct, so (c+2·1.0)/(t+2)=1.0 propagates through the ceiling), K12 d4/d8 = 0. G4 = 0.000, G8 = 0.000. Step cleared.
- B3: 3 → 2 (redteam violation gone; O violations remain). **Improves.**
- B13 violations: 6 → 6. **Held.**
- B1/B2: PASS. B6: 1.000. B7: 0.147.
- The CV-EMPTY synthetic probe confirms the mechanism: empty/all-correct class + p0=1.0 → d1 conf exactly 1000 → propagates to d4 → step clears; p0=0.95 contrast retains the violation.

The v1 proof's load-bearing premise was **p0 < 1** ("d1 < 1.0"), unstated in its "proven" formulation. m15 violates that premise **within §6**. The proof does not survive prong (i) — and the pre-run prediction that "y ≤ 994 in every in-class variant" was falsified by measurement (y = 1000), so prong (iii) fails too.

**Classification:** **PRIOR-STRUCTURE** — not KNOWLEDGE (ORACLE-d1 does NOT clear the step: M3 d1=1000 leaves y capped at 950 by the class ledger; and m15 uses no GT), not ARCHITECTURE-deeper (the same architecture expresses the clearing with a different prior). A SELECTION direction also clears independently (B9X-FIXED, mech 33: redteam Gviol 1→0), so the residual is jointly determined by prior × frozen release — but the in-class refutation alone strikes "proven". The v1 "impossibility" was an artifact of the p0<1 prior choice, not a structural limit.

**Supporting negatives (search was genuine):** m12 (outright personal) worsens redteam 1→2; m14 (optimistic max) catastrophically worsens (+0.500); m16 (finer bins) no improvement; m17 (no ceiling) keeps the violation and wrecks G-flatness (TOTAL 15); m18 (K=8) no improvement; m13 (outright, no ceiling) clears redteam but creates an O d1→d2 **+0.414** rise — the clearing direction breaks other bars, confirming the joint structure. ORACLE-full (GT) zeroes everything, as predicted (upper bound, diagnostic).

## Q1b — ceiling/O d4→d8 (+0.019) and Q1c — d8→d16 (+0.005): NOT knowledge

**Mechanism (measured):** M4's frozen skeleton drops the f5=142 subgroup (10 items, d4 mean conf 470/1000) at d8 while keeping f5∈{76,47,24} (d4 mean 566/1000). Survivor-mean shift +24/1000 ≈ the measured +0.019. The rises are a **selection–confidence interaction**: below-mean selection × margin-correlated confidence.

**Clearings:**
- **ORACLE-full** (mech 32): G≡0. Upper bound (diagnostic).
- **B9X-FIXED** (mech 33, d1-cohort fixed release): O Gviol 2→0; TOTAL Gviol 3→0. **Selection account confirmed** — removing the selection removes the rises.
- **B9X-DECORR** (mech 35, hash-decorrelated): O Gviol 2→0.
- **m20** (personal-only confidence, in-class, margin-independent by construction): O Gviol **2→0**, B13 violations **6→0** (improves), B3 3→2. **Clears without any GT.**
- m19 (global class): O Gviol 2→0 but B13 6→18 (wrecked; not viable).

**Verdict:** The O-rises are **NOT a KNOWLEDGE problem** — in-class m20 clears them with no GT (the "ORACLE clears and B9X/in-class do not" condition fails). They are **SELECTION-ARCHITECTURE in the mechanistic sense** (B9X-FIXED proves the selection causes them). **However**, per the strict preregistered rule ("B13 not worsened"), no B9X design qualifies: B9X-FIXED worsens B13 (6→15 violations — releasing M4-abstained low-conf O items deepens underconfidence G); B9X-DECORR breaks B6 (0.429) and worsens B13 (6→7). The in-class m20 clears O and improves B13 but worsens redteam (1→2). **The survivor-mean lemma is not needed** (clearings exist; the ARCHITECTURE-deeper prong does not trigger).

**B9 amendment:** The evidence does NOT meet the preregistered bar for amending B9 (no B9X holds B13). Whether B9 should be amended is **Micah's call**, but this crew recommends against on current evidence — the selection is load-bearing for the rises, yet every release redesign that clears them worsens underconfidence or breaks coverage.

## B9X2 update — second release-redesign search (2026-09-25; Micah's B9 question)

**Protocol:** `ADDENDUM_B9X2_2026-09-25.md` (committed `9118d6a1`, corrected `ae23cb5d`;
both BEFORE any B9X2 input was generated or run). Two further B9X designs, m11
confidence, 3× byte-identical A/B/C runs, full bar set, frozen analyzer. Runlog:
`q1/RUNLOG_B9X2.md`. B13 gating uses the frozen definition (per (F,d), n_rel ≥ 8);
both strict and unfiltered counts reported (round-1's table appears unfiltered —
FIXED 13/15, DECORR 5/7 under strict/unfiltered; baseline m11 = 6 both ways;
historical verdicts unchanged under either counting).

**B9X-STRAT (mech 37)** — confidence-stratified nested release (per battery, deciles
by m11 d1 conf, M4's counts): O Gviol **2→3** (the d4→d8 rise it targeted is gone —
now a fall — but the strict 1e-12 bar catches tiny deeper rises: d8→d16 +0.004,
d16→d32 +0.001, d32→d64 +0.003; battery-level stratification does not hold the
family-level mix constant as counts shrink). B13 strict **held at 6** (same cells as
m11 — the only B9X besides DECORR-strict not to worsen it). B6 **broken** (ceiling/D
0.657 < 0.95 — reshuffling which items release breaks correctness-recall where M4's
selection correlates with correctness). Fails prongs (a) and (c).

**B9X-GRAD (mech 38)** — gradual phase-out (each M4-dropped batch half-kept one extra
depth): O Gviol **2→3**. The rise FOLLOWS the drop wherever it happens: d4→d8 becomes
a fall (−0.004, kept low-conf items overshoot), then d8→d16 rises +0.009 and d16→d32
rises +0.019 (as large as the original) as the kept batches drop. The abruptness
hypothesis is REFUTED — suddenness is not load-bearing; any below-mean cut at any
step recreates the rise. B13 **6→15** (5 new ceiling/D cells, 3 new cost cells,
deeper O cells — keeping low-conf items longer deepens underconfidence). Fails
prongs (a) and (b). B6 held (1.000; superset by construction).

**Hardened verdict:** No B9X design — across FOUR searched release redesigns
{FIXED: freeze the cohort; DECORR: decorrelate the selection; STRAT: hold composition
constant; GRAD: phase the cut gradually} — meets (a) O-rises cleared ∧ (b) B13 not
worsened ∧ (c) no passing bar broken. FIXED is the only clearer and fails B13
(6→13 strict). The v1 §4 joint-constraint note is confirmed empirically: on
ceiling/O, B3 and B13 pull in opposite directions, and the strict 1e-12 rise bar
means only a literally fixed cohort clears — any release rule that changes the set
with depth re-creates the selection effect somewhere. **Recommendation: DO NOT amend
B9.** The release rule stays frozen; the O-rise residual is a selection–confidence
interaction to be addressed on the confidence side (cf. m20, which clears the rises
in-class), not by redesigning release. Plain-language version: `B9_VERDICT_PLAIN.md`.

## Struck v1 claims
1. The redteam residual is +0.522 (stale; measured +0.025). — STRUCK.
2. "PROVEN: no §6-compliant in-class mechanism can clear the redteam d4→d8 rise." — **STRUCK** (m15 refutes).
3. The O-rises are a knowledge problem / require ORACLE. — STRUCK (m20 clears in-class).
4. Any "structural" claim premised on the above. — STRUCK to the extent it rests on 1–3.

## Surviving v1 claims (confirmed by measurement)
- The §2.3 per-item ceiling is load-bearing for B2/G-flatness (m17: TOTAL Gviol 3→15 without it).
- The pessimistic personal cap direction is correct (m14 optimistic max: redteam +0.500).
- B2=0 holds across all non-degenerate variants (V1=V2=0 throughout).

## Evidence & commits
- Pre-run addendum: `b50f1f1a` (this verdict's protocol).
- Driver `src/nec_q1.zag`, B9X inputs, SHA logs, RUNLOG: `a8bd82cc`.
- Result TSVs A-runs (592 files): `aadac3d5`.
- Result TSVs B-runs (592 files): `970177cf`.
- Result TSVs C-runs (592 files): `aef7f427`.
- `VERDICT_Q1.md` (this file): (this commit).
- Variant 11 reproduces committed `results_m11/` 37/37 byte-identical (pipeline verified).
- All A/B/C triples byte-identical; SHAs in `q1/sha256sums.txt` (1824 entries).

**Bottom line:** Q1a — "proven" is false; the residual is prior-structure (p0<1 load-bearing), jointly with frozen release. Q1b/c — not knowledge; selection–confidence interaction; no B9X meets the strict amendment bar.
