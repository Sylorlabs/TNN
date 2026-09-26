# VERDICT — Phase B2b (PREREG_LH §2b/§2c)

## §2b Control on real references

| Axis | Hit rate | Bar ≥70% | RC0 p<0.01 | RC1 ≤25% | Verdict |
|------|----------|----------|------------|----------|---------|
| Pitch | 28/40 = 70.0% | PASS (borderline) | p=1.9e-12 PASS | 0.0% PASS | **PASS** |
| Envelope | 39/40 = 97.5% | PASS | p=6.1e-10 PASS | 0.0% PASS | **PASS** |
| Prosody | 29/40 = 72.5% | — | p=4.4e-13 | 27.5% **VOID** | **SCORER VOID** |

**§2b: PARTIAL.** Pitch and envelope pass with valid scorers. Prosody's scorer
is void (ANOM-009: RC1 27.5% > 25%), so the 72.5% cannot be certified. The
"each ≥70%" bar is not fully met. Battery-level caveat (ANOM-011): the
prereg's ≥95% scorer-sanity floor to independent manifest labels cannot be
established (no independent labels exist for the battery targets), so per
the prereg's own rule the §2b battery is VOID on that condition — the
reported hit rates stand as measured quantities with this caveat.

## §2c Closed-loop correction

| Criterion | Bar | Fresh | Deep | Verdict |
|-----------|-----|-------|------|---------|
| ERR(3)/ERR(0) ≤ 0.80 | 0.965 | 0.944 | **FAIL** |
| Wilcoxon p < 0.01 | 0.275 | 0.045 | **FAIL** |
| ≥16/20 strictly improve | 10/20 | 13/20 | **FAIL** |
| Sign agreement ≥ 80% | 76.5% | 88.2% | Fresh FAIL, Deep PASS |
| Sawtooth / instability | 6/4 | 4/3 | — |

Fresh ERR ratio rescored 2026-09-26 with the corrected aggregate formula
sum(ERR3)/sum(ERR0) (scorer SHA
7a4c232a1b96aa1a9a2b52a5b843c35a3c604c7c3f246ea2898ab8421e726224);
the earlier draft value 0.951 was from the per-case-mean implementation.

**§2c: FAIL.** The closed-loop correction does not reliably improve over
open-loop on either fresh or deep state.

## Depth

- Depth curve: pitch 0.4→0.9→0.9→0.6; env stable ~1.0; pros variable (void).
- Paired early-vs-deep (pitch): 65% → 75% (+10pp). **No DRIFT-FAIL.**
- History benefits repeats (recalled deltas improve re-render).

## 3× determinism (requirement: 3 completed runs, byte-identical)

- r1 and r3: byte-identical, 160/160 targets (journals canonicalized +
  220/220 WAVs by SHA-256). See evidence/rerun_identity_r1r3.json.
- r2: 159/160 targets complete before the VM reboot (ANOM-010); partial,
  does NOT count as a completed rerun.
- r4: third complete 160-target run in progress (launched post-reboot,
  2026-09-26). 3× byte-identity claim is PENDING r4 completion.
- Zero RNG in the native trial path (pure Zag).

## B-F1 bearing (prosody: planner vs loop)

**Bearing: planner/representation.** The prosody failures (CV term dominating
ERR; vibrato clamp saturating at 0.5 depth) indicate a vocabulary/range
ceiling, not loop instability. The loop DOES attempt CV correction; the
representation cannot express high-CV references. The F0 destabilization
cases are a separate loop-reliability issue.

No structural decision is made; the bearing is reported for B-F1.

## Overall

**§2b: PARTIAL** (2/3 axes pass with valid scorers; prosody scorer void).
**§2c: FAIL** (closed loop does not reliably improve).

The pure-Zag controller achieves strong open-loop control on pitch and
envelope, but the closed-loop correction is unreliable and the prosody
measurement instrument failed validation. These are honest negative results
that inform the B-F1 redesign.
