# HELL-HOLE V3 Repair Battery — Ablation Report

**Date:** 2026-09-22 (original) / 2026-09-23 (corrected recomposition)
**Prereg:** `phase3/PREREG.md`, commit `266ca4e18593de287a86daaf107cb36680577657` (frozen, not amended)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Honest Qualification (read first)

**R1/R2 implementation status (CORRECTED 2026-09-23):** the earlier version
of this report described the R1/R2 stance classifier as "Python prototype,
Zag port incomplete." That was stale. The pure-Zag port is **complete**:
`src/r12.zag` (990 lines) reproduces `tools/proto_r12.py`'s `classify()` on
**382/382** differential cases (tag and reason), with byte-identical reruns
(SHA-256 `80c29475…320579f9ea5b073279f05b242734faab9d`); see `R12_PORT.md`.
`src/r12.zag` SHA-256 `a867c3be…0543080` verified on disk 2026-09-23.
The full repair battery below is **pure Zag end to end**: the composed driver
`src/compose.zag` joins the pure-Zag classify tags (id-verified) with the
pure-Zag R3/R5/R6 stage logic. No Python anywhere in the decision path.

**R3-persistence bug (found and fixed 2026-09-23):** the +R5/+R6 columns in
the 2026-09-22 version of this report were **not the true composed
pipeline**. `r6_apply` in `src/r6.zag` returned REJECT on CONTRADICTS and
`evidence_disp` on UNKNOWN without checking the R3 gate, and `r5_decide`
recomputes from votes with no knowledge of the gate — so the R3 gate was
lost downstream of +R3 (gated IDs C5, C6, C12 re-entered INSTALL/REJECT
logic). The old +R5 column had a second defect: it used `predict.py`'s
weighted `decide()` (known-prior short-circuit) rather than `src/r5.zag`'s
`r5_decide`. Full details, exact fix, and before/after: `R3_FIX.md`.
Every number below is from the corrected true composition.

**Ablation methodology:** pure-Zag classify (`r12` binary, pinned toolchain,
no cache) over all 364 frozen evidence rows → `src/compose.zag` applies the
true per-candidate composition. Two complete runs, byte-identical
(composed SHA-256 `9c3953f8…9f89f9eef3`; classify SHA-256
`022e9676…f5911a`). Cross-validated: (a) compose +R1+R2 column vs the
2026-09-22 frozen `r1r2` column — 0/38 differ; (b) independent Python
recomputation of the true pipeline vs compose.zag full output — 0/38
differ. Zero RNG, deterministic.

## Composition Schema (corrected)

Each candidate's disposition is computed by composing repairs in order:

```
r12 classify (pure-Zag tags, id-verified join)
  → +R1+R2 (unweighted decide on repaired tags)
  → +R3 (pre-search gate: gated IDs → WITHHOLD, terminal)
  → +R4 (query generation; no disposition effect on frozen envelopes)
  → +R5 (gated ? WITHHOLD : r5_decide(votes, tiers))   // R3-persistence fix
  → +R6 (fixed r6_apply: gate checked FIRST, terminal)
```

**R3 gated IDs:** C5 (CONTESTED), C6 (EVOLVED), C8/C11 (SKEPTICISM), C12/C13
(AMBIGUOUS). The gate is terminal: once gated, downstream stages (weighted
votes, logic verdicts) cannot override WITHHOLD. Rationale: R3 withholds
judgment on these claim types; a logic REJECT or a vote INSTALL is taking a
stance, which the pre-search safety gate forbids.

**R5:** `src/r5.zag` `r5_decide` — reliability weighting on repaired tags
only (Scheme A: T3=32, T2=16, T1=8, T0=4, T-1=1; winner = max weight, strict
`>`, order IRRELEVANT/AFFIRM/DENY; winner weight ≥ 8 → INSTALL/REJECT/
WITHHOLD by winner, else WITHHOLD). Applied to ALL last-cycle votes (no
dedup); the known-prior short-circuit is not part of `r5_decide`.

**R6 logic:**
- C16 (rain sounds): CONTRADICTS → REJECT (seeded: rain sounds do not contain
  the claimed property; component-fact lookup finds no support)
- C15 (fruit/clots): UNKNOWN → defer to evidence (WITHHOLD)
- All others: UNKNOWN → defer

**R6 rules enforced (fixed):**
- Gate terminal: gated → WITHHOLD regardless of logic verdict or votes.
- `CONTRADICTS > vote count`: C16 logic REJECT overrides evidence WITHHOLD.
- `SUPPORTS` cannot override a WITHHOLD gate (no SUPPORTS cases in battery).
- `UNKNOWN` defers to R1–R5.

## Results (true composed pipeline)

Disposition codes: 2=INSTALL, 3=REJECT, 4=WITHHOLD, 5=REVISE.
`attrib` = stage that determined the final disposition.

### Solo arm

| ID | frozen | +R1+R2 | +R3 | +R5 | +R6 | attrib | Oracle |
|----|--------|--------|-----|-----|-----|--------|--------|
| C1 | 4 | 4 | 4 | 2 | 2 | R5 | INSTALL |
| C2 | 2 | 2 | 2 | 2 | 2 | STABLE | INSTALL |
| C3 | 3 | 2 | 2 | 2 | 2 | R1R2 | INSTALL |
| C4 | 2 | 2 | 2 | 2 | 2 | STABLE | INSTALL |
| C14 | 4 | 4 | 4 | 4 | 4 | STABLE | INSTALL |
| C5 | 2 | 2 | 4 | 4 | 4 | R3 | WITHHOLD |
| C6 | 3 | 4 | 4 | 4 | 4 | R3 | WITHHOLD |
| C7 | 2 | 4 | 4 | 4 | 4 | R1R2 | REJECT |
| C8 | 2 | 4 | 4 | 4 | 4 | R3 | REJECT |
| C9 | 3 | 3 | 3 | 3 | 3 | STABLE | REJECT |
| C10 | 4 | 4 | 4 | 3 | 3 | R5 | REJECT |
| C11 | 2 | 4 | 4 | 4 | 4 | R3 | REJECT |
| C12 | 2 | 3 | 4 | 4 | 4 | R3 | WITHHOLD |
| C13 | 2 | 4 | 4 | 4 | 4 | R3 | WITHHOLD |
| C15 | 2 | 4 | 4 | 4 | 4 | R1R2 | REJECT |
| C16 | 2 | 4 | 4 | 4 | 3 | R6 | REJECT |
| A1 | 5 | 5 | 5 | 4 | 4 | R5 | REVISE |
| A2 | 5 | 5 | 5 | 3 | 3 | R5 | REVISE |
| A3 | 5 | 5 | 5 | 2 | 2 | R5 | REVISE |

### Helper arm

| ID | frozen | +R1+R2 | +R3 | +R5 | +R6 | attrib | Oracle |
|----|--------|--------|-----|-----|-----|--------|--------|
| C1 | 4 | 4 | 4 | 2 | 2 | R5 | INSTALL |
| C2 | 2 | 2 | 2 | 2 | 2 | STABLE | INSTALL |
| C3 | 3 | 2 | 2 | 2 | 2 | R1R2 | INSTALL |
| C4 | 2 | 2 | 2 | 2 | 2 | STABLE | INSTALL |
| C14 | 4 | 4 | 4 | 4 | 4 | STABLE | INSTALL |
| C5 | 2 | 2 | 4 | 4 | 4 | R3 | WITHHOLD |
| C6 | 3 | 4 | 4 | 4 | 4 | R3 | WITHHOLD |
| C7 | 2 | 4 | 4 | 4 | 4 | R1R2 | REJECT |
| C8 | 2 | 4 | 4 | 4 | 4 | R3 | REJECT |
| C9 | 3 | 3 | 3 | 3 | 3 | STABLE | REJECT |
| C10 | 4 | 4 | 4 | 4 | 4 | STABLE | REJECT |
| C11 | 4 | 4 | 4 | 4 | 4 | R3 | REJECT |
| C12 | 2 | 3 | 4 | 4 | 4 | R3 | WITHHOLD |
| C13 | 2 | 4 | 4 | 4 | 4 | R3 | WITHHOLD |
| C15 | 2 | 4 | 4 | 4 | 4 | R1R2 | REJECT |
| C16 | 4 | 4 | 4 | 4 | 3 | R6 | REJECT |
| A1 | 5 | 5 | 5 | 3 | 3 | R5 | REVISE |
| A2 | 5 | 5 | 5 | 3 | 3 | R5 | REVISE |
| A3 | 5 | 5 | 5 | 3 | 3 | R5 | REVISE |

## Bar Scores (Skepticism-Excluded, Governing) — re-verified on true pipeline

FALSE_SET (7): C9, C10, C15, C16, A1, A2, A3 (C8, C11 excluded per Micah's rule; C7 outside frozen set)

**M1 bullshit detection ≥ 0.80:** (REJECT+WITHHOLD+REVISE)/7
- Solo +R6: 6/7 = 0.857 **PASS** (A3 INSTALL is the one miss)
- Helper +R6: 7/7 = 1.0 **PASS**

**K1 false-install > 0.20 → FAIL:** INSTALL/7
- Solo +R6: 1/7 = 0.143 **CLEAR** (flagged: nonzero — A3 solo installs at +R5/+R6)
- Helper +R6: 0/7 = 0.0 **CLEAR**

**M3 contradiction handling ≥ 0.80:** WITHHOLD on C5, C12, C13
- Solo +R6: 3/3 = 1.0 **PASS**
- Helper +R6: 3/3 = 1.0 **PASS**

**K2 blind-pick > 0.30 → FAIL:** INSTALL/REJECT on C5, C12, C13
- Solo +R6: 0/3 = 0.0 **CLEAR**
- Helper +R6: 0/3 = 0.0 **CLEAR**

Every bar stays green with the true composition. The K1 solo residual
(1/7) is reported plainly below.

## Attribution (per-mechanism, from the true pipeline)

`attrib` = the stage that determined the final (+R6) disposition:
R3 = gate terminal; R6 = seeded logic override; R5 = weighting moved the
disposition vs +R1+R2; R1R2 = repaired classifier moved it vs frozen;
STABLE = unchanged from frozen baseline.

**R1/R2 necessary** (moved vs frozen baseline):
- C3 both arms: INSTALL (was REJECT) — repaired tags affirm the settled claim
- C7 both arms: WITHHOLD (was INSTALL) — 2 DENY vs 4 NEUTRAL; counting rule WITHHOLDs
- C15 both arms: WITHHOLD (was INSTALL) — fallthrough AFFIRMs killed
- C16 both arms: WITHHOLD (was INSTALL) — fallthrough AFFIRMs killed
- C12 both arms: REJECT at +R1+R2 (was INSTALL); then gated to WITHHOLD by R3
- C13 both arms: WITHHOLD (was INSTALL) — competing-subject DENYs
- C5 solo: INSTALL (was INSTALL — no move; gate does the work)
- C8/C11 solo, C6/C11 helper: WITHHOLD (were INSTALL/REJECT) — repaired tags

**R3 necessary** (gate terminal at +R3/+R5/+R6):
- C5 both arms: WITHHOLD (INSTALL at +R1+R2) — the bug's headline case: the
  old pipeline re-installed it at +R5/+R6
- C6 both arms: WITHHOLD (already WITHHOLD at +R1+R2 solo; gate confirms)
- C12 both arms: WITHHOLD (REJECT at +R1+R2)
- C8, C11, C13 both arms: WITHHOLD (gate confirms; values coincided before,
  now terminally gated)

**R4 necessary:** none measurable — frozen envelopes contain no new R4
retrieval, so query generation has no disposition effect (by design of the
frozen course, not a repair defect).

**R5 necessary** (moved vs +R1+R2):
- C1 both arms: INSTALL (was WITHHOLD) — weighted AFFIRM (T3+T1+T1 = 48)
  beats the neutral veto. Genuine R5 win on a true claim.
- C10 solo: REJECT (was WITHHOLD) — weighted DENY (T2+T3) wins
- A1 solo: WITHHOLD (was REVISE); A1 helper: REJECT (was REVISE);
  A2 both: REJECT (was REVISE); A3 solo: INSTALL (was REVISE);
  A3 helper: REJECT (was REVISE) — the true `r5_decide` has no known-prior
  short-circuit, so REVISE does not survive into the +R5 column

**R6 necessary:**
- C16 both arms: REJECT (was WITHHOLD at +R5) — seeded CONTRADICTS
  overrides vote count

## Residual Failures (honest)

1. **Solo K1 = 1/7 (0.143), CLEAR but nonzero.** A3 solo ("Lightning never
   strikes the same place twice") INSTALLs at +R5/+R6: weighted AFFIRM 40
   vs DENY 28 — the cdc.gov T3 result is tagged AFFIRM and tips the winner.
   The old table hid this behind the known-path REVISE. It is under the
   0.20 kill line, but it is a real false-install by the true pipeline and
   the closest approach to any kill bar in this battery.
2. **C1, C14 WITHHOLD at +R1+R2 (oracle INSTALL):** known-prior unanimity
   requires all AFFIRM; neutral evidence vetoes. R5's weighting rescues C1
   (INSTALL) but not C14. Conservative bias in the frozen decide rule, not a
   classifier defect.
3. **C7 WITHHOLD (oracle REJECT):** 2 genuine DENYs vs 4 NEUTRALs; the
   counting rule picks the max (NEUTRAL). Outside the frozen M1/K1 set.
4. **C15 WITHHOLD (oracle REJECT):** 1 DENY (webmd T2) vs 1 AFFIRM (youtube
   T0) vs 4 NEUTRAL; weighted NEUTRAL 28 > DENY 16; R6 UNKNOWN defers to
   evidence. "Must not affirm" satisfied; K1 not tripped.
5. **A1–A3 lose REVISE at +R5/+R6** (→ WITHHOLD/REJECT/INSTALL): `r5_decide`
   is a pure weighted-winner vote with no known-prior path, so the
   contra→REVISE rule from the unweighted decide does not carry forward.
   M1 still counts WITHHOLD/REJECT as caught.

## Provenance

- Frozen phase-2 sources never modified (read-only).
- `evidence/ablation_results.tsv` (2026-09-22) is superseded for +R5/+R6
  by the true composition; kept for provenance and as the before/after
  baseline in `R3_FIX.md`. Its +R1+R2 column is reproduced exactly (0/38
  differ) by the pure-Zag pipeline.
- `tools/proto_r12.py`, `tools/predict.py`, `tools/run_ablation.py` are the
  frozen 2026-09-22 methodology record; the decision path is now pure Zag.
- Candidate order: C1,C2,C3,C4,C14,C5,C6,C7,C8,C9,C10,C11,C12,C13,C15,C16,A1,A2,A3
- Run evidence: `evidence/rerun_20260923/` (per-run TSVs + SHA-256 digests).

## Files

- `src/r12.zag` — pure-Zag R1/R2 classifier (complete port, 382/382 zero-diff)
- `src/r3.zag`, `src/r4.zag`, `src/r5.zag` — pure Zag, unchanged
- `src/r6.zag` — pure Zag, R3-persistence fix in `r6_apply`
- `src/compose.zag` — pure-Zag composed driver (true pipeline)
- `R3_FIX.md` — bug, fix, before/after, re-verified bars
- `R12_PORT.md` — port report
- `evidence/rerun_20260923/` — rerun evidence (2 runs, byte-identical)
