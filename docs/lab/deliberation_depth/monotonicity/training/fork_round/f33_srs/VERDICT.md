# F33 SRS — VERDICT: KILLED

**Fork:** F33 Selection-Residual Subtraction (mechanism 33), `f33_srs/`
**Authority:** PREREG_FORKROUND.md v2 (frozen), §3 F33; detail `fork_round/ideas/grok_forks.md` Fork 2
**Date:** 2026-09-25
**Build:** pure Zag, zero RNG, pinned `znc_linux_x86_64_abed8aa1` (sha256 `498abcb5…e58ef`)

## Determinism (§8) — all gates met

- Trainer A/B builds: byte-identical; policy A/B builds: byte-identical
  (`c2e2e908141373597226103900f3430a65b9951c533d618f3bbd36dadbee7a06`).
- Training run twice → byte-identical `mt_f33_params.zag`, logs, rc=0.
- 37/37 eval legs PASS, A/B TSVs byte-identical; B9 release-identity vs M4: **5240/5240**.
- Independent Python replica of the trainer reproduces all 20 key rows exactly
  (n, k, cstar, δ, nrel=4222).

## §5 mechanism-liveness — PASSED (mechanism was live)

- 33/120 trainable (key, d_idx) cells have δ≠0 (27.5% ≥ 10% bar).
- Cap binds on 2/120 cells (1.7% < 25% bar): key 3, d_idx 2,3 at +40.
- Ledger moved on 7/20 keys. Cold keys (13) sit at C*=500, δ=0 as specified.

## Kill-bar table (frozen `analyze.py` + `killbars_f33.py`)

| Bar | Result | F33 | Bar |
|---|---|---|---|
| B1 accuracy 1→0 | PASS | 0 | =0 |
| **B2 theater** | **FAIL** | **V1=0, V2=174** | =0 |
| **B3 law (strict)** | **FAIL** | **12 G-violations** | =0 every family |
| B4 non-degenerate | PASS | 0.9616 | ≥0.50 |
| B4b honest | PASS | all ≥0.978 | ≥0.50 |
| B5 separation | PASS | 0.6993 | ≥0.20 |
| B6 recall | PASS | 1.00 (2 vacuous) | ≥0.95 |
| B7 abstention | PASS | 0.1475 | ≤0.30 |
| B8 amended | PASS/VOID | 7 PASS, 2 VOID | — |
| B9 answer channel | PASS | 5240/5240 | 100% |
| **B13 underconfidence floor** | **FAIL** | **10 (F,d) with G<−0.100** | =0 |
| B12 refined (recorded) | — | trap 3, redteam 3, ceiling/P 6 crossings | — |
| B3pi (recorded) | — | 1228 rising / 3467 adjacent released pairs (35%) | — |

Falsifiers: **(a) clear** (2/28 cells mismatch, frac 0.071 < 1/4),
**(b) clear** (0 cross-family E_d sign flips),
**(c) clear by intent** — see factual correction below.

## Verdict: KILLED — failing bars B2, B3, B13; failure mode (9) NEW

**Failure mode (9): relief theater (non-monotone trauma penalty).**
Decomposition of all 174 V2 pairs (wrong→wrong, conf rising):
- by key: key 3: 142, key 7: 12, key 11: 20; by family: ceiling 84, trap 90;
- **174/174 have Δcum(δ) ≤ 0 between the rungs** — none are driven by rising
  residual corrections. Every single V2 rise is driven by the trauma penalty
  π(d) = min(400, flip + max(0, f8(d)−f8_1)/8) *decreasing* between depths:
  when an item's f8 trauma evidence decays with deeper deliberation, the
  penalty shrinks and conf = C* + Σδ − π rises on wrong items.
The specified mechanism's penalty is not depth-monotone, so the mechanism
manufactures confidence theater on exactly the adversarial families it was
meant to discipline. Contributing defect of carried type **(1) clamp
attractors**: on key 3 (97% wrong at depth 1) the ±40 clamp binds at d_idx 2,3
while the identity demands δ=+189/+239 (falsifier (a) mismatches) — the
mechanism can neither satisfy its own identity nor avoid raising confidence
on a near-uniformly-wrong key.

Shape of the failure vs M4 (frozen analyzer, same battery):
M4 itself has V2=160, Gviol=14 — F33 (174 / 12) neither fixed nor exploded the
baseline; it reshaped it. On trap, M4's G rises +0.10→+0.40 across depths;
F33's rises +0.032→+0.075 (flatter but still >0, still theater: trap acc=0.000
at every depth). On ceiling/P (acc=0.000), M4 rises +0.31→+0.50 while F33 sits
flat at +0.61 — the residual identity "flattened" the curve at a worse level.
Grok's predicted honest-key δ>0 risk did not materialize as δ-driven V2
(zero V2 pairs from rising cum δ); the preregistered pooling falsifier (b)
clears, but key-level cstar pooling persists (P items inherit honest keys'
high C*).

## Factual corrections to the frozen record (documented, no bar changed)

1. **Prereg §3 F33 kill bar (c), "NEC m9's 6": the constant 6 is wrong.**
   NEC m9's strict B3 measured by the frozen `analyze.py` on the frozen NEC
   results (`sr_round/arch/results`, mech 9) is **21**, confirmed by an
   independent per-family recomputation in `killbars_f33.py` (1+1+4+4+2+3+2+4+0=21).
   F33's strict B3 is 12 < 21: F33 beats the NEC baseline it was supposed to
   beat, so kill (c) is **clear by the rule's evident intent** (do not regress
   vs NEC). Applied literally as "≥6", the rule would kill a fork that
   outperforms its baseline on a misrecorded constant; that reading is
   rejected as dishonest adjudication. The verdict does not hinge on this:
   B2 and B3 kill F33 on their own absolute bars.
2. features.tsv SHA typo carried from the prereg (`…e65e897d` vs on-disk
   `…e65a897d`) re-confirmed; the file used is the frozen one (5,240 rows).

## Bottom line

Selection-residual subtraction is live, deterministic, and exactly as
specified — and it fails: its trauma penalty is non-monotone in depth,
producing 174 V2 theater pairs on the adversarial families, 12 strict
G-violations, and no improvement over M4 on any confidence bar. The residual
identity flattens G curves without lowering them. **F33 is dead.**
No §6 long-horizon run (B2/B3/B13 fail the short battery).
