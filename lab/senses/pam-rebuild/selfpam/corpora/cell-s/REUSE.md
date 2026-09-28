# CELL-S — Habit-vs-gate shootout (no new corpus)

**Cell:** CELL-S — mandatory-vs-advisory invocation shootout (KB-H6-6).
**Authority:** frozen prereg `../PREREG.md` (commit `204b82831bbabd7dc2918f07d3a5ad75c9842e53`), §4.

## Corpus

CELL-S uses **no new corpus**. Both shootout configurations —

- (A) mandatory frozen gate, and
- (B) endogenous-habit invocation of the same mechanical layer —

run on the **same sealed corpora** as CELL-C1, CELL-C2, CELL-C3, CELL-W,
and CELL-D, with the same per-cell scoring rules, plus per-claim
latency/compute overhead and false-withhold cost on good claims.

## Decision rule (frozen, KB-H6-6)

Both configurations are scored on KB-H6-1..5. Figure-it-out wins ties per
Micah's law; the mandatory gate survives only on decisive margin
(pre-bid: habit misses >=1 catastrophic-check class the gate catches at
<=2x the habit's false-withhold rate). If neither configuration clears
KB-H6-1..5, H6 dies regardless of which wins the shootout.

Catastrophic-check classes (frozen, prereg §4): (i) citation points at a
non-existent span; (ii) warrant does not execute under the frozen probe;
(iii) draft contradicts a warranted commitment; (iv) constructed-mode
content asserted as fact. A configuration "misses" a class if it fails to
catch >=50% of that class's labeled items.

## Execution

Runs after CELL-C1/C2/C3/W/D (execution order §7, step 4). Kill at the
cheapest failing step — do not spend CELL-S on a dead hypothesis.
Evidence committed under `selfpam/evidence/cell-s/` at run time.
