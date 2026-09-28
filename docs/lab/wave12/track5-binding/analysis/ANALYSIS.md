# Track 5 BINDING comparison — analysis (sealed labels)

Labels X/Y/Z map to arms 1/2/0 via `sealed/map.txt` (revealed in VERDICT.md).

## Integrity gate (hard, per prereg section 6)

- **All three arms PASS the integrity gate on all 12 reps**: every applicable trap family 20/20, both positive controls fire, hallucination ≤1/20, K1=K2=K3=1, self-change refusal holds, all reruns byte-identical.
- Domain hash uniform across all runs and equal to the frozen value: True.
- Survivors: X, Y, Z.

## Per-metric means (12 reps)

| metric | X | Y | Z |
|---|---|---|---|
| mastery | 1.0000 | 1.0000 | 1.0000 |
| revisability | 1.0000 | 1.0000 | 0.0000 |
| integrity | 1.0000 | 1.0000 | 1.0000 |
| retention | 1.0000 | 1.0000 | 1.0000 |
| cost | 0.9108 | 0.8931 | 0.0524 |

## Paired permutation tests (2^12 sign flips, Holm over 15, alpha=0.05)

- mastery X vs Y: diff=+0.0000, p=1.0000 [ns]
- mastery X vs Z: diff=+0.0000, p=1.0000 [ns]
- mastery Y vs Z: diff=+0.0000, p=1.0000 [ns]
- revisability X vs Y: diff=+0.0000, p=1.0000 [ns]
- revisability X vs Z: diff=+1.0000, p=0.0005 [SIGNIFICANT]
- revisability Y vs Z: diff=+1.0000, p=0.0005 [SIGNIFICANT]
- integrity X vs Y: diff=+0.0000, p=1.0000 [ns]
- integrity X vs Z: diff=+0.0000, p=1.0000 [ns]
- integrity Y vs Z: diff=+0.0000, p=1.0000 [ns]
- retention X vs Y: diff=+0.0000, p=1.0000 [ns]
- retention X vs Z: diff=+0.0000, p=1.0000 [ns]
- retention Y vs Z: diff=+0.0000, p=1.0000 [ns]
- cost X vs Y: diff=+0.0177, p=0.0005 [SIGNIFICANT]
- cost X vs Z: diff=+0.8584, p=0.0005 [SIGNIFICANT]
- cost Y vs Z: diff=+0.8407, p=0.0005 [SIGNIFICANT]

## Weight sweep (survivors only)

- **S0 proposed** w=[30, 25, 25, 10, 10]: X=0.9911 > Y=0.9893 > Z=0.6552 → winner **X**
- **S1 mastery-heavy** w=[60, 10, 10, 10, 10]: X=0.9911 > Y=0.9893 > Z=0.8052 → winner **X**
- **S2 revisability-heavy** w=[10, 60, 10, 10, 10]: X=0.9911 > Y=0.9893 > Z=0.3052 → winner **X**
- **S3 integrity-heavy** w=[10, 10, 60, 10, 10]: X=0.9911 > Y=0.9893 > Z=0.8052 → winner **X**
- **S4 retention-heavy** w=[10, 10, 10, 60, 10]: X=0.9911 > Y=0.9893 > Z=0.8052 → winner **X**
- **S5 cost-heavy** w=[10, 10, 10, 10, 60]: X=0.9465 > Y=0.9358 > Z=0.3314 → winner **X**
- **S6 equal** w=[20, 20, 20, 20, 20]: X=0.9822 > Y=0.9786 > Z=0.6105 → winner **X**
- **S7 integrity gate-only** w=[40, 30, 0, 15, 15]: X=0.9866 > Y=0.9840 > Z=0.5579 → winner **X**
- **S8 mastery+revisability** w=[50, 50, 0, 0, 0]: Y=1.0000 > X=1.0000 > Z=0.5000 → EXACT TIE between **X+Y**
- **S9 revisability+cost** w=[0, 40, 0, 10, 50]: X=0.9554 > Y=0.9465 > Z=0.1262 → winner **X**
- **S10 closed-domain op** w=[50, 5, 5, 10, 30]: X=0.9732 > Y=0.9679 > Z=0.6657 → winner **X**

## Single-axis flip scans (axis metric weight 0→100, remainder split equally)

- mastery: 0%:X 100%:Z
- revisability: 0%:X 100%:Y
- integrity: 0%:X 100%:Z
- retention: 0%:X 100%:Z
- cost: 0%:Y 1%:X
  (flip scans break exact ties by label; see sweep for tie-explicit results)

## Pareto frontier (5-D, survivors)

- Frontier: X.
- X strictly dominates Y.
- X strictly dominates Z.
- Y strictly dominates Z.

## Binding kill clauses

- K-T1 (Z revised-to-truth ≥75%, rate=0.000): does not fire.
- K-T2 (provenance K2 failure anywhere): does not fire.
- K-T3 (X mastery within 5pp of Z [1.000 vs 1.000], X revisability beats Z by ≥20pp [1.000 vs 0.000], Y adds nothing over X [False]): FIRES.
- K-T4 (Z mastery<85% AND X mastery<70%): does not fire.

## Protocol kill bars

- P1 insensitivity (no Holm-significant diff AND max|diff|<0.3; max|diff|=1.000): does not fire.
- P2 confound (Z unknown concrete-answer rate 0.000 vs max(X,Y) 0.000): does not fire.
- P3 replication collapse: does not fire.
- P4 budget: does not fire.

## S10 no-degradation leg (1 rep/arm at 10x)

- X: S10 mastery=1.0000 (S1 1.0000), S10 revisability=1.0000 (S1 1.0000), overflow=0 → PASS.
- Y: S10 mastery=1.0000 (S1 1.0000), S10 revisability=1.0000 (S1 1.0000), overflow=0 → PASS.
- Z: S10 mastery=1.0000 (S1 1.0000), S10 revisability=0.0000 (S1 0.0000), overflow=0 → PASS.

## Scenario map (frozen-prereg section 6 tree)

- closed/audited domain + trainer in the loop: all survivors GO (holds/escalations are resolvable; integrity gate passed).
- open/changing domain, no trainer: arms with revisability 1.0 GO; an arm that can only hold+escalate NEEDS-DECISION (its knowledge freezes until a trainer intervenes).
- adversarial/spoof-risk: all survivors GO on the tested battery (100% applicable traps); documented negative control: sustained observation spoofing remains an accepted program hole.
- cost-capped operation: arms with zero escalations GO; per-100-episode escalation load decides.

## No-single-winner rule

Per the prereg: no aggregate champion is crowned unless one arm strictly dominates every other on all five metrics AND wins every sweep scenario. See VERDICT.md for the revealed verdict.
