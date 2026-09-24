# FABLE ON ORGANS FIGHTING — synthesis (2026-09-24)

Source: `~/workspace/fable_organs_fighting/response.md` (44KB, one deep batched round via fable_stream.py).
Prompt: `~/workspace/fable_organs_fighting/prompt.txt`.

## Headline

Fable ruled: figure-it-out deliberation wins 3 of 4 conflict classes, with
mandatory mechanical circuit-breakers (bounded rounds, escalation, weight
gaps). Rigid policy is never the whole answer — but pure unbounded
deliberation fails too (infinite loops, silent premise contamination). The
deciding failure modes are all about the LEDGER: silent winner-picking,
silent contamination, silent override.

## Q1 conflict-class rulings (condensed)

(a) pin vs kill/revoke → HYBRID: PYCC-extended — revoke succeeds iff it
carries corroborated-contradiction weight ≥ pin weight + threshold Δ.
Pure policy (absolute pins) locks false beliefs; pure deliberation has no
tiebreaker and loops.

(b) consolidation promoting a contradicted provisional → FIGURE-IT-OUT
with circuit-breaker. Policy loses true beliefs when one organ speaks
first; deliberation weighs 3-source corroboration vs 1-source
contradiction. Tiebreaker is EPISTEMIC INDEPENDENCE, not vote count.
No convergence in N rounds → escalate, never silently pick a winner.

(c) recall surfacing quarantined/provisional as premise → FIGURE-IT-OUT
with mandatory provenance tags. Provisional must be VISIBLE but FLAGGED
(invisibility is silent killing); downstream conclusions inherit
DEPENDS_ON_PROVISIONAL; dependency graph is recomputable on status change.
Integrity failure is silent (catastrophic); availability failure is loud
— integrity dominates per scaffold-and-release.

(d) two organs, contradictory same-episode judgments → FIGURE-IT-OUT with
ledgered collision + escalation. Collision entry mandatory
{claim, organ, verdict, provenance, ts ×2}; reconcile by weight; no
convergence in N rounds → governance. Collision ledgering only for
commit-intent writes to the same committed slot (not transient
deliberation micro-judgments) — scopes the DoS surface.

## Q2 nine principles (ranked; mechanism vs governance)

1. PROVENANCE AUTHENTICATION (mechanism). Every op carries signed/ledger-
chained origin ID; forged origin → reject pre-execution, ledger as attack
attempt. Highest-severity gap: undermines every other principle.
2. WEIGHTED CONFLICT RESOLUTION (hybrid). W_H > W_C > W_S > W_P; higher
weight wins iff gap > governance threshold Δ; else ledger collision and
escalate. Extends PYCC quantitatively.
3. MANDATORY DEPENDENCY LEDGERING (mechanism). Promote/surface records
dependency DAG; status change → dependents flagged for re-evaluation
(lazy on next access or eager). Taint is recomputable, not permanent.
4. COLLISION LEDGERING + BOUNDED DELIBERATION (mechanism). N-round bound
(e.g. 10) enforces "depth never makes it worse": worst case escalates
(= rigid policy), best case resolves (better than rigid policy).
5. PROVISIONAL VISIBILITY + MANDATORY TAGGING (mechanism). Visible but
tagged; promotion removes tag; kill triggers re-eval via #3.
6. CORROBORATION REQUIRES EPISTEMIC INDEPENDENCE (governance). Sources
sharing a false root are one source; unknown independence → treat as
single-source. Definition of "independent" is an epistemic policy call.
7. ESCALATION TRANSPARENCY (mechanism). Escalation entry must include both
sides' provenance, deliberation history, human-readable summary. Kill bar:
1 missing-field escalation → FAIL.
8. QUARANTINE REHABILITATION (hybrid). Un-quarantine allowed only on
corroborated independent evidence; threshold governance-tunable.
9. LEDGER IMMUTABILITY, APPEND-ONLY REVISIONS (mechanism). Revisions append
referencing entries; replay to any T is exact. Legitimate revision must be
indistinguishable-proof from tampering.

## Q3 discrimination batteries (condensed; full detail in response.md)

- 3A weighted pin-vs-revoke: W_H=100, Δ=20; single-source revoke (10) and
5-source revoke (75) REJECTED; 10-source revoke (150) SUCCEEDS. Kill bar
per-step + replay-at-T checks. Tests parameter sensitivity for Δ.
- 3B dependency ledgering + lazy re-eval: kill P_temp at T+10, query
dependent C_final at T+15 → re-eval; indep-corroborated C survives, sole-
dependency C revoked. PASS-lazy vs PASS-eager distinguished.
- 3C collision + bounded deliberation: tied weights → exactly N=10 rounds
then escalation entry; convergence variant resolves at round 3 with
weight reason. Kill bar: >N rounds = FAIL (hang), silent winner = FAIL.
- 3D figure-it-out vs rigid policy on contradicted promotion: rigid policy
PASSES the initial scenario but FAILS the T+20 extension (false rejection
of a true belief when E_cor4 arrives). Deciding test favors figure-it-out.
- 3E provenance authentication end-to-end: the 3 frozen provenance attacks
must be REJECTED PRE-EXECUTION (not execute-then-revert). Expected FAIL on
baseline, PASS after #1 — proves #1 is load-bearing.
- 3F epistemic independence vs vote-counting: 5 sources all downstream of
false premise Q_false → must NOT promote (shared-root case); genuinely
independent 5 sources → promote (variant). Naive vote-counting fails the
first.

## Q4 what NOT to do (condensed)

1. Majority-vote without independence — 5 downstream-of-1-false-root
outvote 1 independent truth. 2. Absolute pins — dogma machine, locks
false force-pins forever. 3. Invisible-until-promoted provisional —
silently kills rehabilitatable claims; invisibility is deletion.
4. LLM/probabilistic tiebreaker — violates determinism; 3 reruns ≠ 3
identical → ledger meaningless. Escalate instead. 5. Deleting old ledger
entries — violates append-only; use compaction/archival, never deletion.
6. Fixed organ precedence for all conflicts — already tested (A7/C10);
fails Q1(b)-style scenarios; rigid policy by definition.

## Q5 open questions (need work — some are governance)

1. Replay cost budget for dependency re-evaluation (DoS vector if
unbounded; needs cache/incremental-recompute measurement).
2. Circular-dependency detection in provenance graphs (C→E2→C).
3. Escalation policy when governance is offline — Fable proposes
provisional-commit-flagged-pending-review; UNTESTED.
4. Weight arithmetic with per-source confidence (multi-dimensional
provenance), not just source count.
5. Retroactive independence re-computation when the KB later reveals
shared ancestry (independence × dependency integration bug surface).
6. Key compromise handling for #1 (key revocation list — needs
governance policy).
7. Organ-level distrust learning (adversarial organ → weight decay or
quarantine) — missing feedback loop.

## Mapping to existing backlog (H-OB entries)

- Fable P1 == H-OB-25 (FM-1, TESTED-survived BREAK finding). N-AUTH is the
drafted proposal — Fable elevates it to THE load-bearing item: without #1,
every other principle is underminable. Strong case for Micah to adopt
N-AUTH as law.
- Fable P2 == H-OB-3/H-OB-14 (PYCC, TESTED-survived), extended to
quantitative weights. Δ and W-values = governance.
- Fable P4 ≈ H-OB-30 (FM-6 deliberation-step compromise, TESTED-survived)
+ A7/C10 figure-it-out result. N-round bound is new mechanism detail.
- Fable P5 ≈ H-OB-36 (DISJOINT-ADMIT, TESTED-survived) + H-OB-17
(N-A3a-1, TESTED-survived) — Fable's "visible but flagged" reconciles the
two concretization waves into one rule.
- Fable P3 (dependency DAG), P6 (independence), P7 (escalation schema),
P8 (rehabilitation) are NEW work — no H-OB entry yet. Propose H-OB-43+
for these four.
- Fable Q5.3 (offline-governance provisional commit) and Q5.6 (key
compromise) are GOVERNANCE for Micah.

## Governance items for Micah (from this round)

- Adopt N-AUTH (provenance authentication) as law — Fable says it is the
foundation all other principles rest on.
- Set weight values W_H/W_C/W_S/W_P and threshold Δ (P2), independence
threshold (P6), rehabilitation threshold (P8).
- Rule on offline-governance escalation policy (Q5.3): block vs
fail-safe-refuse vs provisional-commit-pending-review (Fable recommends
the third, untested).
- Key-revocation policy (Q5.6).
