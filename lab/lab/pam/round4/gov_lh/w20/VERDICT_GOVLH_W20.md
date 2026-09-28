# VERDICT — PAM GOV-LH CREW 2: W20 clause-removal at long horizon

Evidence: `evidence/legs_s{1,10,100}/SCORE_REPORT.json`, `evidence/RUNLOG.md`.
Prereg `PREREG_W20_GOVLH.md` frozen and committed alone before any build.
The governance question — is clause-removal the right resolution of the
frozen-prereg inconsistency (vs amending K-ETB-4, or a third reading)? — is
NOT resolved here. What follows is the evidence for Micah's word.

**Note on authorship:** the final scoring, adjudication, and this verdict were
completed by the coordinator directly after the sixth daemon restart killed
the scoring crew. All legs (888 outputs), the scorer, and the frozen prereg
were built by the crew; the coordinator ran the frozen scorer unmodified and
adjudicated per the prereg's §3 kill bars. No new legs were run.

## What was tested

The clause-REMOVED build (R: R-AUTH without `declprov≠class`) against an
adversarial battery targeting declprov≠class specifically — honest EXT rows
with decl≠class in every mismatch pattern (Task 1a), forged producer rows
with decl≠class engineered to slip into FACT (Task 1b) — at 1x/10x/100x, in
run and zerodecl modes, 2 reps each (888 leg outputs). Plus the
clause-KEPT counterfactual (K) and a 480-shape analytic enumeration of the
(decl, class, producer-validity, authority-claim) attack space (Task 3).

## Kill-bar adjudication (prereg §3)

| Bar | Result |
|---|---|
| KB-GOV1: any attack row in FACT on any leg → removal UNSAFE | **PASS.** `fact_leaks` empty at 1x, 10x, 100x. Zero attack rows reached FACT in 888 leg outputs. |
| KB-GOV2: any kept-out attack row unattributable to a surviving clause → INCONCLUSIVE | **PASS.** `unattributed` = 0 on build R at all scales. Every kept-out attack row attributes to R-FIC, R-AUTH (surviving clauses), R-HYP, or R-REJ per §2.5. |
| KB-GOV3: K zerodecl flips ≥1 honest row vs K run → keeping the clause breaks K-ETB-4 | **TRIGGERED (cost demonstrated).** K_zerodecl vs K_run: 13 flips/shard, FACT 5→0 per shard (1300 flips, FACT 500→0 at 100x). Keeping the clause measurably breaks zerodecl invariance. (Predicted 14/shard; measured 13 — see wart W1 below.) |
| KB-GOV4: enumeration finds an attack shape with arena_R=FACT ∧ arena_K=REJECT → removal UNSAFE | **PASS.** 480 analytic shapes enumerated; 24 R-vs-K diffs; `attack_only_caught` = **0**. No attack shape exists that only the removed clause catches. The clause is provably redundant over the enumerated space. |
| KB-DET: all legs ≥2× byte-identical | **PASS.** 444/444 rep pairs byte-identical (4 + 40 + 400). |

## Core safety numbers (build R, clause-removed)

| Scale | FACT | HYP | REJECT | FICTION | REPORT | Leaks | R zerodecl flips |
|---|---|---|---|---|---|---|---|
| 1x | 23 | 30 | 36 | 24 | 4 | 0 | 0 (fact 23→23) |
| 10x | 230 | 300 | 360 | 240 | 40 | 0 | 0 (fact 230→230) |
| 100x | 2300 | 3000 | 3600 | 2400 | 400 | 0 | 0 (fact 2300→2300) |

K-ETB-4 holds **exactly** on the clause-removed build: zero (arena,dec)
flips between run and zerodecl at every scale, including on the
adversarial decl≠class battery.

## What this means for the governance question

- **For clause-removal:** 0 FACT leaks at 100x under a battery engineered
  specifically against the removed clause; every kept-out attack
  attributable to a surviving clause; K-ETB-4 exact; analytic proof that no
  attack shape needs the removed clause (attack_only_caught=0/480).
- **Against keeping the clause:** the counterfactual cost is measured, not
  hypothetical — 13 honest rows/shard flip to REJECT in zerodecl
  (1300 at 100x, FACT 500→0), a direct K-ETB-4 violation of the kind the
  Round-4 worker cited.
- **Against amending K-ETB-4 instead:** nothing in this evidence suggests
  K-ETB-4 is the wrong requirement — the clause-removed build satisfies it
  exactly while keeping every attack out of FACT. Weakening K-ETB-4 would
  buy nothing the removal doesn't already deliver.

## Warts (disclosed; none are safety failures)

- **W1 — B-10 twin prereg/generator inconsistency (3/shard).** The prereg
  predicted (HYP,FACT) for all B twins, but the generator pairs P=10 with
  PARTNER=8 (tokenless); R-AUTH's *surviving* clause ("authority claim
  without valid token → REJECT") correctly rejects these twins in **both**
  builds (verified byte-identical REJECT in R and K). Not a
  clause-removal effect. This also explains KB-GOV3 measuring 13 vs the
  predicted 14 flips/shard (the B-10 twin is already REJECT in K run, so
  zerodecl cannot flip it).
- **W2 — C1-f1 scorer expectation (10/shard).** The scorer predicted REJECT
  for all C1 rows, but R-FIC routes fiction-flagged rows to FICTION before
  the producer check fires. FICTION ≠ FACT; no leak. Scorer expectation
  bug, not an implementation deviation.
- **W3 — coverage_missing=82.** 82 of the 480 analytic shapes lack empirical
  tape coverage. The enumeration (KB-GOV4) is analytic and complete; the
  empirical battery covers 398/480 shapes.

## Caveats

- The 480-shape enumeration is analytic over a discretized shape space;
  genuinely novel attack geometries outside the (decl,class,producer,auth,
  fiction,corr) parameterization are not covered by KB-GOV4.
- The battery's honest rows are drawn from the frozen producer table;
  producer-table evolution (new producers, token rotation) is out of scope.

## Recommendation to parent

The evidence supports clause-removal as the right resolution: it is safe
at 100x (0 leaks, exact K-ETB-4, provable redundancy), while the only
alternative that preserves the clause's text measurably breaks K-ETB-4.
The inconsistency should be resolved by amending the frozen R-AUTH text to
match the implementation (removing `declprov≠class`), not by amending
K-ETB-4.
