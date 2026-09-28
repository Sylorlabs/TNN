# DEBATE RECORD — RNGSCAN v3 vs. stated residual risk (2026-09-20)

**Coordinator:** debate-coordinator subagent (parent: main agent), per Micah's request for agent debates with pros/cons to inform his decision.
**Question:** Build RNGSCAN v3 per the draft amendment, or stop the auditor line and accept a stated residual risk?
**Output:** `VERDICT_SHEET.md` (the decision document). This file is the procedural record.

## Participants

| Voice | Position | Round 1 | Round 2 |
|---|---|---|---|
| proA | **Option A:** build v3 | `r1/proA.md` | `r2/proA.md` |
| proB | **Option B:** accept stated residual risk | `r1/proB.md` | `r2/proB.md` (round 2 written by a fresh agent; original debater completed after round 1) |
| mid1 | **Middle M1:** narrowed-scope / per-frozen-build prescriptive certifier | `r1/mid1.md` | `r2/mid1.md` |
| mid2 | **Middle M2:** replay-first (hardened replay-divergence as primary gate, v2 static as tripwire) | `r1/mid2.md` | `r2/mid2.md` |

Word budgets: round 1 ≤ 600 words, round 2 ≤ 500 words. All met.

## Round structure

- **Round 1:** opening positions. Each debater: thesis, three strongest arguments, honest concession of the strongest argument against with an answer, what the option unblocks and costs. No strawmen; steelman required.
- **Round 2:** rebuttals after reading all three sibling round-1 positions. Each debater: strongest point against them answered, weakest point in another position honestly attacked, concessions/adjustments, one question for Micah.

## Key moves (what changed between rounds)

- **proA conceded:** replay hardening ships standalone without waiting for the static rebuild; a dated residual-risk statement should wrap even a *passed* v3 (a pass is evidence, not proof); M1's per-build certification can run in parallel as a complement, not a rival. Attacked M2's environment-matrix as symmetric inexhaustibility.
- **proB conceded:** adopted M2's preregistered N-run replay matrix with deployment-like conditions and lifted the v3 amendment's replay-hardening section wholesale; adopted M1's per-frozen-build scoping; the statement ships in repo docs next to Arm C results, signed, revocable, with a sunset clause. Attacked proA's "bounded attack surface" — the v2 misses lived *inside* already-listed categories.
- **mid1 sharpened:** narrowed certifier must be *prescriptive* (ban novel idioms from trial builds) not *descriptive*; the honest price is constraining trial-build authors. Delivered the promised K2 replacement for per-build scope (K1′/K2′/K3′). Merged with M2/pro-B on replay doing the heavy verification. Attacked proA's "convergence" — 6/20 plants unscored, convergence claimed on an incomplete round.
- **mid2 conceded:** adopted pro-B's dated residual-risk statement (miss-rate history 2/2 stated plainly); adopted M1's per-frozen-build scoping; keeps v2 static as tripwire. Attacked proA's "bounded surface" as a hypothesis, not a finding — two kills is not convergence.

## Convergences (all four voices, round 2)

1. Replay hardening (N runs, heap pre-dirtying, allocation variation, deployment-like conditions) ships standalone.
2. A dated, version-controlled residual-risk statement is required under every option.
3. Certification scopes to the frozen trial build (hash the artifact, preregister per build).
4. The v2 static scan keeps running as a cheap tripwire without a K2 bar it may never pass.

## Remaining genuine disagreement

Whether to *also* build the full v3 static scanner, and whether Arm C's gate requires a scanner pass — i.e., whether the general-detector shape is worth a third round, or the program should certify behavior per build and disclose the rest.

## Constraints observed

- Pure Zag for any proposed build work; no-RNG law not under debate (only the certification tool).
- No debater decided for Micah; the verdict sheet's recommendation is labeled recommendation-only.
