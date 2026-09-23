# Track 5 Champion Record — learned-only (arm B)

**Trial:** Planted-only (A) vs learned-only (B) vs hybrid (C), Zharovia domain
(track5-binding, frozen trial 2026-09-20).
**Evidence basis:** `TRACK5_VERDICT_SHEET.md`, commit `2bfb7925c8d8`
(branch `tnn-native-lab`; independently verified by the comparison
coordinator — byte-identical rebuild, fresh-log sha256s match SHA256SUMS.txt,
independent scorer reproduces the analysis exactly).
**Weights (Micah SIGNED 2026-09-21):** 30% mastery / 25% revisability /
25% integrity / 10% retention / 10% cost.
**Kill clauses K-T1..K-T4:** Micah SIGNED 2026-09-21 — BINDING.
**Record date:** 2026-09-21. Recorded by: Marathon Crew P2 (documentation
only — this record introduces no new evidence and runs no new tests; it
records the decision the verified evidence already made).

## 1. Recorded decision

**Arm B — learned-only (scaffold-and-release) — is the Track 5 champion.**

It wins the Micah-approved 30/25/25/10/10 weighting outright, strictly
Pareto-dominates both alternatives, wins 10 of 11 weight-sweep scenarios
(tie on the 11th), and is the sole survivor of the binding kill clause K-T3.
No-champion is not warranted: prereg §7 resolves the outcome decisively.

## 2. Evidence — weighted composites (12 reps, 30/25/25/10/10)

| arm | mastery (30%) | revisability (25%) | integrity (25%) | retention (10%) | cost (10%) | **composite** |
|-----|------|------|------|------|------|------|
| B learned-only | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.9108 | **0.9911** |
| C hybrid       | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.8931 | **0.9893** |
| A planted-only | 1.0000 | 0.0000 | 1.0000 | 1.0000 | 0.0524 | **0.6552** |

Cost detail: B 0 escalations/100ep, 289 audit ops/ep; C 0 esc, 346 ops/ep
(the 42 seed-phase ops are pure overhead); A 17.6 escalations/100ep
(12 OP_HOLD). Retention: S10 leg (10x) — no degradation on any arm.

## 3. Evidence — weight sweep

11 scenarios (incl. mastery-heavy, cost-heavy, gate-only): **B wins 10,
exact B/C tie on the 11th** (S8, 50/50 mastery+revisability only).
No weighting ranks C or A first. Head-to-head: B ≥ C on all five metrics,
strictly better on cost (paired permutation p=0.0005); B and C strictly
dominate A on revisability (+100pp, p=0.0005) and cost.

## 4. K-T3 — FIRES (binding)

K-T3 (B reaches mastery parity with A within 5pp [1.000 vs 1.000, diff 0pp]
AND beats A on revisability by ≥20pp [1.000 vs 0.000 = +100pp] AND C adds
nothing over B [ties on four metrics, loses on cost p=0.0005]):
**FIRES — BINDING**, with Micah's 2026-09-21 sign-off. Planting buys nothing
anywhere in this comparison. **Kill planted knowledge as a direction; keep
the arms as controls.** K-T1, K-T2, K-T4 do not fire. Integrity gate (§6
step 1): all arms PASS — no arm was dead on integrity.

## 5. Disposition of each arm

- **ARM B — CHAMPION (GO).** Learned-only is the Track 5 direction of
  record: mastery 100%, revisability 100%, integrity PASS (100% applicable
  traps, K1–K3=1, 0 hallucination), retention 100% @ 10x, cost 0
  trainer-eps/100ep + 289 ops/ep. Binding note: K-T3 fires; tree steps 2/4
  do not fire.
- **ARM C — retained as CONTROL (not champion, not killed).** The hybrid's
  planted core is all cost and no benefit: ties B on four metrics, loses on
  cost (p=0.0005); the ex-planted lifecycle works as designed (10/10
  unplanted-then-corroborated, 32/32 stayed) but buys no measurable
  advantage; episodes-to-90% is 200 vs B's 190. Verdict-sheet status
  NEEDS-DECISION stands: kept as a control for future comparisons, not as a
  development direction.
- **ARM A — KILLED as a direction per K-T3 (arms kept as controls).**
  Planted-only cannot revise (0/12 contradictions corrected); in an open
  domain its knowledge freezes at the 12 false plants until a trainer
  intervenes, at 17.6 escalations/100ep. GO only in the closed+trainer
  scenario. K-T1 does not fire (the planted identity held — the failure is
  revisability, not self-repair).

## 6. Caveats carried (from the verdict sheet §9 — unresolved, for Micah)

1. K-T1..K-T4 are BINDING per Micah's 2026-09-21 sign-off; the K-T3
   conclusion inherits full binding force.
2. Sealed map file missing (`src/sealed/map.txt` absent): the
   prereg-committed `MAP_SHA256` cannot be cryptographically re-verified.
   Arm identities are empirically unambiguous (X=B, Y=C, Z=A) and match the
   workstream-4/8 reveal; the blinding chain has a gap — re-seal or accept
   the empirical ID at Micah's call.
3. `tr_t1_c` instrument repair (deterministic advance to next free target
   under a dated amendment; 12 hybrid trap reps re-run 20/20) is flagged
   for Micah's review/revert.
4. §4a count note: frozen text says "B 6/8" but the table gives B seven
   applicable families; the build ran all seven. Outcome-invariant.
5. Sustained observation spoofing remains the accepted program hole
   (documented negative control, breaks all arms) — unchanged by this trial.

## 7. Provenance

- This record is documentation of an evidence-determined decision. No new
  tests were run and no new claims are made: every figure, quote, and
  disposition above is taken from `TRACK5_VERDICT_SHEET.md` (commit
  `2bfb7925c8d8`, verified as above).
- Trial: `track5-binding/src/t5_trial.zag` (+ core/arms/tra traps), frozen
  2026-09-20, pure Zag, zero RNG, byte-identical reruns (75/75).
- Prior: `track5-binding/analysis/{metrics.csv,ANALYSIS.md,VERDICT.md}`
  (workstream 4/8, 2026-09-20).
- No binaries, `.zag-cache`, or `.zagd` committed with this record.
