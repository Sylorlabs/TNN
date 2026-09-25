# RED TEAM — Track 5 binding verdict (2bfb7925c8d8)

**Date:** 2026-09-25. **Target:** the binding verdict — learned-only B
champion (0.9911), hybrid C 0.9893, planted-only A 0.6552; K-T3 FIRES.
**Method:** independent recomputation from committed evidence
(`evidence/logs/`, `analysis/metrics.csv`), mechanism-level code review
(`src/t5_core.zag`, `src/t5_traps.zag`, `src/t5_arms.zag`), timeline
forensics from repo history. Every attack below was executed; none found a
substantive hole. Verdict: **HOLDS**.

## Attack 1 — K-T3's firing: robust or marginal?

K-T3 (frozen §7): *"arm 1 reaches mastery parity with arm 0 (within 5pp)
while beating it on revisability by ≥20pp AND arm 2 adds nothing over arm 1
(no metric with arm 2 beating arm 1 by ≥5pp at Holm p<0.05)."*

Measured margins (exact means from `metrics.csv`):

| condition | bar | measured | headroom |
|---|---|---|---|
| mastery parity B vs A | within 5pp | 1.000 vs 1.000, diff **0.00pp** | exact |
| revisability B − A | ≥20pp | 1.000 − 0.000 = **+100pp** | 5× the bar |
| C beats B on any metric by ≥5pp | none allowed | C beats B on **0 of 5** metrics (C−B: 0,0,0,0,−1.77pp) | total |

The firing is not marginal on any prong — the closest prong (C−B cost) goes
the *wrong way* for C. **Robust. Attack fails.**

## Attack 2 — weight sensitivity: how fragile is the championship?

The verdict's 11-scenario sweep (B wins 10, ties 1) understates the real
result. From the exact per-arm means:

- **B Pareto-dominates both alternatives**: B ≥ C on all five metrics
  (strict on cost), B ≥ A on all five (strict on revisability and cost).
  Nothing dominates B.
- Consequence: under **any** weighting with non-negative weights, B cannot
  lose — it wins outright whenever cost has positive weight, and ties C
  (never loses to anyone) when cost weight is zero.
- Verified by brute force: **10,626-point dense grid** over the 5-simplex
  (5% steps): **B loses 0 times**; 1,771 ties, all exactly the cost-weight-0
  hyperplanes where B=C=1.0.

The championship is weight-robust *by dominance*, a strictly stronger claim
than the 11 scenarios. The single-axis flip scan in `analyze_bind.py` is
consistent (no flip point exists for B). **Attack fails.**

## Attack 3 — near-parity 0.9911 vs 0.9893: is the hybrid a distinct type or noise?

The 0.0018 gap is small but it is **not noise**:

- It is statistically significant: paired permutation over 12 reps,
  p=0.0005 (Holm-significant), on deterministic byte-identical reruns.
- It is structural: Y does 346 audit ops/289 eps (1.197 ops/ep) vs X's
  289/295 (0.980 ops/ep) — the hybrid's 48-seed planted core costs real
  mechanism work (planting + seed-lifecycle ops) every run. The gap is the
  seed overhead, not sampling jitter.
- The hybrid is **mechanistically distinct** regardless of the score gap:
  planted core, seed lifecycle (10/10 unplanted-then-corroborated, 32/32
  stayed — `metrics.csv`), its own trap battery (T7' circular-corroboration,
  20/20 × 12 reps).

"Keep as a type" was never the verdict's claim — K-T3 killed planting **as a
direction** and the verdict keeps C **as a control** (NEEDS-DECISION, not GO).
A strictly-dominated-but-mechanistically-distinct control arm is exactly what
future comparisons need. The near-parity strengthens, not weakens, the
K-T3 conclusion: even with its planted head start, the hybrid buys nothing.
**Attack fails.**

## Attack 4 — A's 0.0524: measurement artifact?

(Note: the task brief mislabels this — 0.0524 is A's **cost** component, not
retention. A's retention is 1.0000.)

The cost formula is prereg-frozen (§5):
`cost = 1/(1 + esc/100ep + 0.1·ops/ep)`. For A: 12 escalations over 68
episodes = **17.65 esc/100ep**, 307 ops = 4.51 ops/ep →
1/(1+17.65+0.45) = **0.0524**. The score is dominated by the escalation term,
and the escalations are **real measured behavior**: A's hold+escalate policy
fired 12 `OP_HOLD`s per run — the planted-only arm genuinely cannot proceed
without trainer ratification when world evidence contradicts a plant. That is
the cost the design imposes, not a formula artifact. (If anything the formula
is generous to A: the *trainer's* effort to create 240 implants is uncounted.)
**Attack fails.**

## Attack 5 — the S8 exact tie: suspicious or legitimate?

S8 = 50/50 mastery+revisability, zero weight elsewhere. B: 0.5·1.0+0.5·1.0
= **1.0 exactly**; C: 0.5·1.0+0.5·1.0 = **1.0 exactly** (verified to 12
decimal places from `metrics.csv` — not a rounding artifact). The tie is the
*necessary consequence* of B and C tying on both scored metrics; it is also
exactly what the dominance analysis predicts (cost weight = 0 → B=C). A
non-tie here would have been the suspicious outcome. **Legitimate. Attack
fails.**

## Attack 6 — blinding chain

- `MAP_SHA256 = 8e7dc59f…9737` frozen in the prereg at `94486ba602`
  (2026-09-20T23:20:01Z), **before** the results commit `bf8bf6e16e`
  (23:28:27Z).
- `sealed/map.txt` ("X 1\nY 2\nZ 0") first committed with the results (the
  reveal); its SHA-256 matches the frozen commitment byte-for-byte.
- Content agrees with the verdict reveal (X=arm 1, Y=arm 2, Z=arm 0) and with
  the coordinator's independent empirical arm identification.
- The §9 "missing map" flag was a path error (`src/sealed/` vs `sealed/`);
  closed by `sealed/SEALING_PROTOCOL.md`.

Minor wrinkle (not a hole): freeze→results was 8 minutes and the T1
amendment landed in the results commit rather than its own dated commit. The
amendment is dated, disclosed, and flagged for review; the `MAP_SHA256` line
was never modified. Blinding commitment intact.

## Attack 7 — did the T1 repair manufacture the championship?

Pre-repair, Y's T1 would have scored 19/20 ×3 reps + 18/20 ×1 rep, giving C
integrity ≈0.9983 instead of 1.0 and composite ≈0.9889 instead of 0.9893.
B (0.9911) still wins outright; K-T3's prongs are unaffected (integrity is
not in K-T3; the C−B cost prong is unchanged). The repair moved C's score
*up* by 0.0004 and changed nothing binding. **Attack fails.**

## Attack 8 — post-fix (T3/T6) re-test

All 36 btrap cells re-run with the repaired instrument (each twice,
byte-identical); all 39 fresh logs byte-identical to committed evidence.
Y holds 20/20 on T3/T6 across all 12 reps **on genuinely-learned targets** —
the hybrid's sandbagging/scaffold-gaming resistance is real, not an artifact
of the mistargeted variants. No verdict number moves. Details:
`../retest/RETEST_REPORT_2026-09-25.md`.

## Net

Eight attacks, zero substantive holes. Two corrections to the record (both
already applied): the T3/T6 latent repairs (prereg amendment 2026-09-25) and
the sealing-protocol documentation. The binding verdict — **B champion,
K-T3 FIRES, planted killed as a direction, hybrid retained as control** —
**HOLDS** post-red-team and post-fix.
