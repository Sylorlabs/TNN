# CTX — contexts as deliberately-managed memory partitions

Agent H, 2026-09-19. The replacement for the toy's score table + reflex
switch rule. No score table exists anywhere in this design.

## 0. The idea in one paragraph

A **context is a memory partition**: a slot holding the learner's
*declared* belief about a regime, plus *recorded probe evidence* about
whether that belief currently holds. Switching contexts is not a reflex
fired by one bad sample — it is a **deliberate operation** (`CTX_SWITCH`)
that **refuses to commit unless corroborated**: the target partition must
show recorded majority-positive evidence AND the active partition must
show recorded majority-negative evidence. Corroboration is structural —
in the op implementation, like `REFUSED_CORE` — not a policy bolted on
afterwards. This is R27's `diagnosis → proposal → measured → PROMOTE or
rollback` shape, miniaturized into the context mechanism itself.

## 1. State (no table)

```
partition[4]: { live:u8, label:i32,   // the learner's DECLARED regime belief
                hits:u8, total:u8,    // RECORDED probe evidence (observations, not value)
                bad_streak:u8,        // consecutive majority-negative batches
                step_created:i32 }
active: i32                            // index of the committed partition
audit: fixed ledger of every op + refusal (before/after snapshots)
```

What is deliberately absent: there is no `score[c][o]`, no accumulator,
no `+=`, no argmax, no threshold on a scalar. `hits/total` is a *record
of what was observed*, replaced wholesale by each new probe batch — it is
never incremented by a rule. The learner never "adds reward to memory."

## 2. Operations (the learner's action set)

| Op | Effect | Refusal |
|---|---|---|
| `CTX_PROPOSE(label)` | Creates a partition declaring "I believe regime `label` looks like this." Audited. | `REFUSED_FULL` (4 live), `REFUSED_BADLABEL` |
| `CTX_RECORD(slot, hits, total)` | Deliberate act of recording a probe batch's evidence on a partition. Replaces the previous window (observations, not accumulation). Audited. | `REFUSED_NOTLIVE`, `REFUSED_BADSLOT` |
| `CTX_SWITCH(target)` | Commits `active := target` **iff** corroborated (see §3). Audited on every path. | `REFUSED_NOTLIVE`, `REFUSED_SELF` (target==active), **`REFUSED_UNVERIFIED`** |
| `CTX_AUDIT_CHECK()` | Global invariants: refusals never mutated state; ledger replays to exact live state (the MA1 "conscious" test). | — |

### §3. The corroboration rule (the anti-LH-5 mechanism)

`CTX_SWITCH(target)` commits iff ALL hold:

1. `partitions[target].live == 1` and `target != active`;
2. target's recorded evidence is majority-positive: `hits*2 > total && total > 0`;
3. the active partition's recorded evidence is majority-negative: `hits*2 < total && total > 0`.

Otherwise `REFUSED_UNVERIFIED` — the op refuses, state untouched, refusal
audited. **This is the whole fix.** The toy switched on one negative
*sample* (`reward<0 && old>0 → switch`). This mechanism switches only on
*compared recorded evidence*: the new hypothesis must be measured good
AND the old one measured bad. A single misleading sample can corrupt
neither condition, because each condition is a majority over a 16-probe
batch — sixteen corroborating observations, not one.

Note what this is *not*: it is not "the toy's switch rule plus a
corroboration patch." There is no score for the rule to read, no
`reward<0` trigger at all. The trigger is gone; the mechanism is
different. Patching would have kept the table. The table is gone.

## 4. The learner policy (protocol-fixed in HT1 — honest boundary)

The *mechanism* (propose/record/verified-switch) is what's under test.
The *policy* driving it in the HT1 trial is fixed in the harness, exactly
as MA1 fixed values:

- Boot: `CTX_PROPOSE(0)` → active = 0.
- Each episode: harness probes the active partition (16 probes, 15%
  seeded noise), reports `hits/total`; learner `CTX_RECORD`s it.
- If the recorded batch is majority-negative: `bad_streak++`, else reset.
  (One bad batch is information; it is not a switch.)
- If `bad_streak >= 1` (sustained — the active partition is *measured*
  failing): enter verify mode —
  probe every other live partition (16 probes, 15% noise), `CTX_RECORD`
  each; `CTX_SWITCH` to the first with majority-positive evidence.
  If none verifies: `CTX_PROPOSE(1 - active.label)` (alternate the
  declared label), probe it, `CTX_SWITCH` if verified.
- Measurement blocks (every 8 episodes, uncorrupted) are read-only: they
  never feed `CTX_RECORD`. Evaluator/harness separation per H-07.

What HT1 does NOT show: the learner choosing *when* to probe or *which*
label to propose on its own. That judgment is the next phase (HT2). HT1
proves the *mechanism* survives what breaks the table.

## 5. Why this is post-table, not table-with-steps

The steelman: "hits/total is just a 4×2 table." Three differences, all
procedural:

1. **No update rule.** Nothing is ever added to `hits`. Each probe batch
   *replaces* the window. There is no `+=`, no accumulation, no value
   being maximized. The table's essence was `score += reward*100` +
   argmax; both are gone.
2. **Decisions are ops with refusal paths, not function evaluations.**
   `CTX_SWITCH` can say no. `argmax` cannot. Refusal is the observable
   signature of doubt — the thing §1a showed tables lack.
3. **Every commitment carries its reason in the audit ledger.**
   "Why are you in context 1?" → "SWITCH committed at clock T with
   target evidence 14/16 and active evidence 3/16, entry N." The table's
   answer was "because s11 > s10." One of these is intelligence
   substrate; the other is a spreadsheet.

## 6. Relation to the memory-agency work

Partitions are memory slots in the MA sense: deliberately created,
deliberately recorded-upon, never background-decayed. A natural later
step is unifying partitions with MA slots (a partition *is* a USER-region
slot whose value is a declared label + evidence). HT1 keeps the CTX store
separate and small on purpose: one mechanism under test at a time. The
audit/replay invariant is shared with MA1 (`conscious` = no state change
without an audit entry).

## 7. CORE/USER note (serving-later, per program law)

Partitions live in USER space: the learner may propose and switch them
freely. A regime belief that survives long enough could graduate toward
CORE only through the external promotion gate (proposal → measured →
PROMOTE/rollback) — never by unilateral learner action. Not built in HT1;
the mechanism is partition-management, and the graduation rule is future
research.

## ⚠️ Contamination note — 2026-09-20 (R34 hidden-randomness remediation)

This document references the "LH-5 signature" (switch-storm / fragility
pattern). The quantitative LH-5 claims (0%→10% corruption knee, regime
switches 19→181) are **QUARANTINED** — LH-5 trained with
`explore_enabled=1`, engaging the hidden seeded LCG in `r34v3_choose`
(r34 RNG probe, workstream 2/8, commits `072f25aa` / `4976cbf5` on branch
`tnn-native-lab`; Micah's ruling: REMEDIATE). The *phenomenon* referenced here
was independently reproduced under explore-disabled conditions (the HT1/HT2
toy arms showed the same 357-switch storm, collapsed blocks, and 0/16 regime
destruction with exploration off), so the pattern-level reference remains
descriptively valid; only the tainted quantitative claims are suspended.
The original text above is left intact for the record.
