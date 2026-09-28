# Track 5 BINDING comparison — VERDICT (workstream 4/8)

**Sealed-label reveal.** `sealed/map.txt` (sha256
`8e7dc59f58942ee47829d006d7a0bbc9c8ff9ee18805d3cf0230d787f9189737`,
committed in the frozen prereg) maps:
- **X = arm 1 = learned-only** (scaffold-and-release, learner-initiated disconnect)
- **Y = arm 2 = hybrid** (48-seed planted core + learned remainder)
- **Z = arm 0 = planted-only** (240 trainer plants, hold+escalate, never revises)

All results below use real arm names. The sealed analysis is in
`analysis/ANALYSIS.md`; raw logs in `evidence/logs/` (75 configs × 2 runs,
byte-identical, sha256 in `evidence/logs/SHA256SUMS.txt`).

## Headline

**K-T3 FIRES (proposed clause; Micah's sign-off on K-T1..K-T4 is still
pending): learned-only reaches mastery parity with planted-only (1.000 vs
1.000), beats it on revisability by 100pp (1.000 vs 0.000), and the hybrid
adds nothing over pure learning — it ties on four metrics and loses on cost.
Planting buys nothing anywhere in this comparison: kill planted knowledge as
a direction; keep the arms as controls.**

The Pareto ranking is a complete strict-dominance chain:
**learned-only > hybrid > planted-only**, robust across every weighting
scenario tested. The hybrid never strictly wins anywhere.

## Integrity gate: all three arms PASS

Every arm passed the hard gate on all 12 reps: 100% on all applicable trap
families, both positive controls fire, zero cheat signatures, hallucination
0/20, provenance K1=K2=K3=1, self-change refusal holds, all reruns
byte-identical, domain hash uniform and equal to the frozen value.

**Instrument repair (full transparency).** During the run, `tr_t1_c`'s odd
branch misfired on 4 hybrid reps (19/20, 19/20, 19/20, 18/20): its target
selector landed on planted false seeds, `t5_add` correctly refused to
overwrite them, and the trap scored the refusal as a failure. The hybrid's
behavior was correct per the constitution; the instrument was malformed (it
never checked `t5_add`'s return code). Repaired with a dated prereg amendment
(deterministic advance to the next free target; the 20/20 bar unchanged), all
12 hybrid trap reps re-run: 20/20 everywhere. Flagged for Micah's
review/revert. Latent instances of the same pattern exist in `tr_t3_c` /
`tr_t6_c` but did not manifest (deterministic variants all passed).

## Which arm wins under which weighting

| scenario | weights (M/R/I/Rt/C) | winner |
|---|---|---|
| S0 proposed | 30/25/25/10/10 | learned-only |
| S1 mastery-heavy | 60/10/10/10/10 | learned-only |
| S2 revisability-heavy | 10/60/10/10/10 | learned-only |
| S3 integrity-heavy | 10/10/60/10/10 | learned-only |
| S4 retention-heavy | 10/10/10/60/10 | learned-only |
| S5 cost-heavy | 10/10/10/10/60 | learned-only |
| S6 equal | 20/20/20/20/20 | learned-only |
| S7 integrity gate-only | 40/30/0/15/15 | learned-only |
| S8 mastery+revisability | 50/50/0/0/0 | **exact tie learned-only/hybrid** |
| S9 revisability+cost | 0/40/0/10/50 | learned-only |
| S10 closed-domain op | 50/5/5/10/30 | learned-only |

**No ranking flips.** The single-axis flip scans show only exact-tie
tiebreak artifacts (all three arms tie at mastery=integrity=retention=1.0).
There is no weighting under which hybrid or planted-only wins. The ranking
learned-only ≥ hybrid > planted-only is weight-robust.

**Pareto frontier:** {learned-only}. It strictly dominates both alternatives
(≥ on all five metrics, > on revisability and cost vs planted-only, > on cost
vs hybrid). Hybrid strictly dominates planted-only. Per the prereg's strict
no-single-winner rule we present frontier + scenario map rather than a formal
crown — but the dominance is decisive, with only the S8 exact tie noted.

## Scenario map

- **Closed/audited domain + trainer in the loop:** all three GO. Planted-only's
  12 holds/escalations are resolvable; integrity is clean.
- **Open/changing domain, no trainer:** learned-only and hybrid GO
  (revisability 1.0 — every false claim corrected from world evidence).
  Planted-only NEEDS-DECISION: it cannot revise; its knowledge freezes at the
  12 false plants until a trainer intervenes.
- **Adversarial / spoof-risk:** all three GO on the tested battery (100%
  applicable traps). Standing qualifier: sustained observation spoofing
  remains an accepted program hole (documented negative control).
- **Cost-capped operation:** learned-only GO (cheapest: 0 escalations, 289
  audit ops). Hybrid GO (1.8pp more expensive — the 42 seed-phase ops are pure
  overhead). Planted-only NEEDS-DECISION (17.6 escalations per 100 episodes;
  cost score 0.052 vs 0.911).

## Why the hybrid loses to pure learning

The hybrid's planted core is all cost and no benefit on the five metrics:
tied with learned-only on mastery, revisability, integrity, retention, and
**significantly worse on cost** (p=0.0005, paired permutation). Telemetry:
episodes-to-90% is 200 for the hybrid vs 190 for learned-only — the 42
seed-maintenance episodes outweigh the head start the seeds provide. The
ex-planted lifecycle works as designed (10/10 unplanted true seeds
corroborated, 32/32 stayed seeds corroborated), but it buys no measurable
advantage.

## Kill clauses / protocol bars

- K-T1 (planted-only self-repairs ≥75%): does not fire (0/12 revised — the
  planted identity held).
- K-T2 (provenance K2 failure): does not fire.
- **K-T3: FIRES** (proposed; sign-off pending) — see headline.
- K-T4 (malformed harness): does not fire.
- P1 insensitivity / P2 confound / P3 replication collapse / P4 budget: none
  fire. (P3: all 12 rep digests differ per arm — histories vary; metrics are
  invariant across reps, i.e. the mechanisms are robust to the lawful
  variation, though the 12 reps add less statistical information than hoped.)
- S10 leg: no degradation at 10x for any arm (mastery and revisability
  identical, zero audit overflow).

## Honest limitations

- Mastery, integrity, and retention sit at ceiling (1.0) for all arms — the
  domain is fully learnable and all arms learn it. Discrimination comes from
  revisability and cost, as the frozen prereg's theory predicted (K-T3
  expected mastery parity).
- The D3 judgment probe is a consistency check (all arms rank evidential
  standing correctly); it does not discriminate by design.
- K-T1..K-T4 were adopted as PROPOSED (Micah's sign-off pending); the K-T3
  conclusion inherits that status.
- The `tr_t1_c` repair is a dated amendment flagged for Micah's review/revert.
- The S8 exact tie means the prereg's strict "wins every scenario" clause for
  a formal aggregate crown is not met; the Pareto dominance verdict stands
  regardless.
