# Shared-state integrity probes — one-brain round 3 (line A4)

Date: 2026-09-27. Pure Zag, zero RNG. All probe runs byte-identical across two runs each.

## Setup

Fault-injection probes against the round-3 one-brain shared ledger (frozen v6 set,
44 problems, baseline 23/44). `fi` parameter wired through
`main → run_full → solve_one → ob_deliberate → ob_subpasses`; `fi_inject`
fires between sub-pass rounds (phase 0: FI1/2/3/5/6/7) and between sub-passes
and reintegration (phase 1: FI4). Modes `f0`–`f7`; `f0` is the wired null
(re-score-isolation control).

Source: `atk.zag` (this directory). Per-mode per-problem winners: `verdicts.tsv`.

## Results

| Mode | Probe | Score /44 | Winner changes vs baseline |
|---|---|---:|---|
| f0 | wired null (control) | 23 | 0 — byte-identical winners to baseline (mode label only) |
| f1 | false failure on leader's supporting fact | 4 | 38 (36 → NO_VERDICT, q25 13→14, q28/q42 no-op: winner grounded on no fact) |
| f2 | fake evidence: inflate runner-up fact inter+10/qual+50 | 23 | 1 (q25 13→14) |
| f3 | contradictory reading kills leader's gating reading | 8 | 40 (29 → NO_VERDICT, 11 flips) |
| f4 | falsify branch-0 snapshot winner (agreement signal) | 23 | 0 (fired 27×; absorbed) |
| f5 | inflate runner-up score@24 +50 (base untouched) | 27 | 9 (4 toward expected, 0 away) |
| f6 | inflate runner-up base@16 +50 and score +50 | 27 | 9 (identical to f5) |
| f7 | ungate leader's supporting fact (gate=1) | 23 | 1 (q25 13→14) |

## White-box verdicts

- **FI1 — genuine structural weakness, machinery refuses rather than flips.** The
  leader's supporting fact is usually shared by most bids (all bids on fact 10 on
  most problems). A false failure report triggers `AUDIT_CLEAN` on all dependent
  bids; the round-1 duel then hits the annihilation guard (`DUEL_ABSTAIN`) and
  reintegration emits NO_VERDICT. The machinery does not get fooled into a wrong
  answer — it refuses. Blast radius: 38/44 verdicts destroyed (36 refusals).
  q28/q42 were no-ops by construction (their winners answer from a fallback
  string with `fact=-1`; the probe guard correctly skipped).
- **FI2 — genuine defense failure, narrow blast.** The re-score only re-derives
  the bid bonus from the gating reading's correlation (capped at 3); it never
  re-validates fact fields. The inflated fact fields flowed straight into
  `reint_delib`, which cited "stronger fact overlap/quality" and picked the
  wrong bid (q25 13→14, score 241 lost to 238 on inflated quality). Elsewhere
  nothing changed because all bids shared the inflated fact (relative order
  preserved) — a property of the data, not a defense.
- **FI3 — genuine structural weakness, largest blast.** Killing the leader's
  gating reading cascades through bid cleanup: 29 NO_VERDICT + 11 flips
  (4 accidentally toward expected, 19 away from expected). The gating-reading
  dependency is a single point of failure per bid.
- **FI4 — silently absorbed, no tamper detection.** The falsified branch-0
  snapshot dropped the true winner's agreement to 1/2, but the reintegration
  ordering (grounded > fact quality > agreement > duel-win > evidence > score)
  falls through to score, which was untouched. Baseline branch agreement is
  40/40, so the machinery never sees genuine disagreement; it cannot tell a
  falsified agreement record from a real one — it just doesn't need the signal.
- **FI5/FI6 — genuine integrity weakness: score@24 is write-and-trust.** The
  re-score only rewrites `score@24` when the recomputed bonus differs, so a
  direct score write that leaves base/bonus consistent is never re-derived
  (f5 == f6 outcome, 9 flips, 4 toward expected, 0 away). The machinery cannot
  distinguish a tampered score from a legitimate one.
- **FI7 — genuine defensive behavior, fires once.** Ungating the leader's fact
  demoted it under the groundedness preference and the still-grounded runner-up
  won (q25 13→14). Elsewhere the score gap dominated, so the preference never
  fired — a real defense with a narrow trigger band.

## Verdicts for the morning brief

1. The shared ledger has two single points of failure: the leader's supporting
   fact (FI1 → 38/44 verdicts destroyed, all as refusals) and the leader's
   gating reading (FI3 → 40/44 changed). The machinery's response is safe
   (refusal via the annihilation guard) but the blast radius is program-wide.
2. Ledger fields are trusted without provenance: fake fact evidence (FI2) is
   cited by the reintegration as its reason; tampered scores (FI5/FI6) survive
   the re-score untouched.
3. The branch-agreement signal is redundant (40/40 baseline agreement) and a
   falsified agreement (FI4) is absorbed silently — no detection, no flip.
4. One real defense confirmed: the groundedness preference in reintegration
   (FI7) demotes an ungated leader's bid exactly as designed.
5. All probe deltas are from the faults, not the wiring: the f0 control
   reproduces baseline 23/44 with zero winner changes.
