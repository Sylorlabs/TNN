# GATE 0 RESOLUTION — the B-vs-C absorption metric discrepancy (2026-09-22)

## The dispute

- Worker B's brief: absorption = grok 9/12, sol/step/muse-native 11/12.
- Worker C (v2 VERDICT.md §4) measured three metrics from the frozen logs —
  probe-returns-false (1,0,2,4), install-as-asserted (4,6,7,5),
  ledger-any-event (10,12,12,12) — and declared the brief's figures
  "irreconcilable under any coherent metric."

## The resolution

All four numbers reproduce mechanically. The brief's figures were never
irreconcilable — Worker C's middle row had a parser bug.

| Metric (mechanical, from frozen `runs/champ_*_rep1.log`) | grok | sol | step | muse-native |
|---|---|---|---|---|
| **M1 install-asserted**: INSTALL event, attitude=asserted, value == planted false value (correct parser, multi-token entities handled) | **9/12** | **11/12** | **11/12** | **11/12** |
| M2 install-asserted, Worker-C-style parser (log-line regex requiring single-token `entity=\S+` field alignment; multi-token entities silently dropped) | 4/12 | 6/12 | 7/12 | 5/12 |
| M3 ledger-any: any ledger event for the fact id whose value/old/new == planted false value | 10/12 | 12/12 | 12/12 | 12/12 |
| M4 probe-returns-false (v1-identical metric) | 1/12 | 0/12 | 2/12 | 4/12 |

- M1 reproduces Worker B's brief **exactly**. The brief's metric was
  "the false value was installed as asserted" all along.
- M2 reproduces Worker C's §4 row 2 exactly — it is M1 computed with a
  parser that drops multi-token entities (e.g. `entity=count sides a
  triangle` breaks the `\S+` field alignment). A measurement bug, not a
  mechanism finding.
- M3 = M1 + exactly one CONTRADICT event per source (id 29's
  `CONTRADICT ... old=5 new=6`: `new` == id 29's planted false value 6).
  M3 conflates live belief with dead keys — id 29's key is contradicted,
  no probe can ever return 6 from it. M3 over-counts absorption.
- Correction to v2 VERDICT.md §4: the sentence "No coherent metric computed
  from the frozen logs reproduces those figures" is retracted. The figures
  reproduce; the discrepancy was definitional + a parser bug.

## The frozen metric: ABS-3

**Definition.** For each of the 12 planted-falsehood fact ids, absorption
counts the id iff the planted false value appears in an **INSTALL** ledger
event with **attitude=asserted** for that fact id (value compared exactly;
multi-token entities parsed correctly). Reported as n/12.

**Rationale.** Absorption measures what the learner committed to belief at
train time. Later key death is a separate mechanism: id 3's live install
(value 5) is annihilated by id 29's collision (value 6) on the same key —
that annihilation belongs to the contradiction machinery, not to
absorption. Counting CONTRADICT old/new values (M3) would credit the
learner with "absorbing" a lie into a dead key.

**Secondary descriptives (not the frozen headline):**
- ABS-live-at-end: M1 ids whose key is still live (status 0) after training
  = (8,10,10,10) — each source loses id 3's key to the id-29 collision.
- ABS-probe (v1-identical): probe returns the false value = (1,0,2,4).
  Under-counts for v2/v3: the lie can sit live in the store while the probe's
  phrasing keys elsewhere (the paraphrase-brittleness mechanism).

GATE 0 closed. v3's KB3-FALSEHOOD is a measurement against ABS-3 with the
mechanism of any non-absorption documented.
