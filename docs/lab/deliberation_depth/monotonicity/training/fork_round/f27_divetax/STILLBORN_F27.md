# F27 DIVETAX — STILLBORN (observable-verification failure)

**Date:** 2026-09-24 (PDT). Recorded BEFORE any build, any training run, any eval.
**Fork:** F27 DIVETAX (Divergence-History Honesty Tax), mechanism 27.
**Frozen authority:** `sylorlabs/TNN` branch `tnn-native-lab`, commit `3a2eef44` (v2) —
  `PREREG_FORKROUND.md` §3 (F27) + §5 (observable-verification gate) +
  `ideas/native2_forks.md` FORK 4 (authoritative on mechanism detail; read in full
  before this check).
**Verdict:** STILLBORN per prereg §5. Reported, not killed. The mechanism is
  UNTESTED, not falsified.

## 1. What the fork needs

F27's new feature is f9 = 1000·D/d (integer), where
D = count of depths k < d with L_k ≠ L_1 — the number of deliberation rounds
within the depth-d run whose leader differed from the round-1 leader. The
feature requires per-(item, depth) **leader history** L_k (k = 1..t) from the
run that produced each training cell.

## 2. Observable verification (done before any build)

Checked all three frozen input sources named in the task gate:

| Source | Checked | Leader-history observable? |
|---|---|---|
| `training/features/features.tsv` | 5240 rows, ALL exactly 15 tab cols: `id, family, heldout, depth, t, rel4, correct4, f1..f8`; SHA-256 `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d` (matches frozen) | **NO.** Only leader field is f3 = "1000 if leader changed at any r≤t else 0" — a cumulative ever-changed flag, not a history. |
| `deliberation_depth/items_v2/{admit,revoke,logic,trap,cost}.jsonl` | line format inspected | **NO.** Deliberation *inputs* (hypotheses, evidence, ground_truth). Zero fields matching `leader`. |
| `training/items/ceiling_{D,O,P}_{even,odd}.jsonl` and `deliberation_depth/ceiling/items/ceiling_battery.jsonl` + `monotonicity/redteam/redteam_battery.jsonl` | line format inspected | **NO.** Deliberation *inputs* only. Zero fields matching `leader`. |
| (also checked) `training/features/{admit_A,B,…,redteam,…}.tsv` per-leg splits | same 15-col snapshot format | **NO** — identical column set, no new fields. |

## 3. Exact missing field

**Per-(item, depth) leader history: the leader L_k at each deliberation round
k < d (or equivalently the divergent-depth count D = #{k<d : L_k ≠ L_1}),
logged for the runs that produced the 5240 frozen training cells.**
The harness logged snapshots only.

## 4. Why it cannot be derived from frozen inputs

- f3 = 0 ⇒ D = 0, but f3 = 1000 only implies D ≥ 1 — D = 1 and D = 7 both map
  to f3 = 1000. D is underdetermined; no exact reconstruction is possible from
  the frozen columns (reconstructing it by re-running the harness would be
  *inventing* the observable, explicitly forbidden by the gate).
- The item batteries contain no deliberation outputs at all.
- Per-depth rows of the same item across legs are separate snapshots at target
  depths {1,2,4,8(,16,32,64)} — they do not give the within-run round-level
  leaders L_k for all k < d (e.g. k=3,5,6,7 for d=8).

This is precisely the implementation dependency the ideas file predicted
(FORK 4, "Adversarial notes", third attack): "D requires the harness to log
per-item leader history — if the harness only kept snapshots, this fork has an
implementation dependency the others don't." The harness kept snapshots.

## 5. Gates not reached

- **§5 stillborn fire-rate gate:** uncomputable — f9 requires D, which does not
  exist in the frozen inputs. No numbers to report; the observable check stops
  the fork before this gate.
- **Training:** no training run performed. Optimizer/inits: N/A (never reached
  TRAIN-COORD v2; nothing fitted, nothing vetoed).
- **Eval:** no battery run. No kill-bar table — the fork died at the
  pre-build gate, before any falsification condition could be tested.
- Falsification conditions (a) w9→0, (b) wrong-sign accuracy, (c) B3 ≥ base:
  all UNTESTED.

## 6. Failure-mode taxonomy note

No new numbered failure mode: this is a data-availability death (frozen
feature file lacks the required observable), not a mechanism death. DIVE-TAX's
mechanistic story (returnee tax vs "what doesn't kill me" robustness) remains
genuinely ambiguous and undecided — per the ideas file's own falsification
(c), "the data decides," and the data was never logged.

## 7. Revival condition

If a future feature-generation run logs per-round leader history L_k (or the
count D) per training cell into a frozen features file, F27 can be revived
from this record — the eval-side policy can already track D internally during
its own deliberation runs (deterministic in-run state), so only the
training-side observable was missing.

---
*F27 DIVETAX: STILLBORN at the prereg §5 observable gate. No build, no params,
no eval. Evidence above; nothing invented.*
