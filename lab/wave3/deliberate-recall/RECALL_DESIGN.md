# Deliberate Recall — design

Wave-3 investigation `deliberate-recall`, 2026-09-19. TNN has no context
window; retrieval must be a **deliberate choice**, built from the wave-2
memory ops (MEMORY_OPS.md), never from attention weights over a window.

## 1. The pipeline

```
TASK ──▶ NEED_DECLARE ──▶ RECALL ──▶ ACT ──▶ (PIN what worked)
            (audited         (logic,     (deterministic
             hypothesis)     audited)     function of selection)
```

1. **DECLARE.** The system states its information need as an explicit,
   audited record: which entities, which capabilities (symbolic ops),
   which provenance policy, how fresh the knowledge must be, and *why*
   (justification code). This is the hypothesis: "traces satisfying
   these predicates will suffice."
2. **RECALL.** A fixed selection rule (below) scans the slot store and
   selects traces. Every per-trace decision is ledgered with the
   predicates that held. Read-only on slots; append-only on the ledger.
3. **ACT.** A deterministic function of the selected set: act iff the
   need is satisfied (required capabilities covered), using the
   agreed action code; otherwise deliberate ABSTAIN (audited).
4. **PIN.** Traces that served a satisfied need are pinned — deliberate
   retention through the MA1 op set. The loop is closed without any
   reward signal.

Need *formation* (task → need parameters) is protocol-fixed in this
trial, exactly as MA1's declared values were protocol-fixed: the claim
under test is the **selection rule**, not need formation. Need-formation
quality is future work; the prereg says so.

## 2. The selection rule — logic, not similarity-thresholding

Symbolic vocabulary (all integers, no floats anywhere):
- Entities: E1..E6 as bits of an i32 mask. Ops: A/B/C/D as bits.
- Provenance: source id + verified flag. Age: `now - step_added`.

Predicates for need `q` and live trace `t`:

| # | Name | Rule |
|---|---|---|
| P1 | entity coverage | `(t.ent & q.req_ent) != 0` |
| P2 | op entailment | `(t.ops & q.req_ops) == q.req_ops` — the trace's op set *contains* every required op |
| P3 | provenance gate | `q.prov == ANY  OR  t.verified == 1` |
| P4 | freshness bound | `(now - t.step_added) <= q.max_age` — `max_age` is *declared in the need*, not a tuned constant |

**Single-trace mode:** `SELECT(t) ⟺ P1 ∧ P2 ∧ P3 ∧ P4`. Slots scanned in
index order; every qualifying trace is selected. Cardinality is a
*consequence*, never a parameter — there is no k, no cutoff.

**Composition mode** (`q.compose=1`, for needs no single trace covers):
greedy in index order; select `t` iff P1∧P3∧P4 and
`(t.ops & uncovered) != 0` (it contributes a not-yet-covered required
capability); stop when `uncovered == 0`. Still pure logic: marginal
symbolic contribution, auditable per trace.

### Why this is logic, not confidence-thresholding by another name

1. **No score exists on the deliberate path.** The predicates are Boolean
   functions of symbolic attributes composed by ∧. `rc_recall` never
   computes a similarity, a count, or a ranking. (Similarity scores exist
   only in the harness-side baseline arm, clearly fenced off.)
2. **Hard gates don't compensate.** An additive score lets high overlap
   in one attribute excuse failure in another (unverified but
   high-overlap wins). P3/P4 are *non-compensatory*: no amount of entity
   overlap admits an unverified trace when the need demands verified.
3. **Containment, not overlap.** P2 requires `req_ops ⊆ t.ops`
   (entailment: the trace *can do* what is needed), not "shares k ops".
   A trace missing one required op is out regardless of other overlap.
4. **Per-trace justification.** Every selection/exclusion carries a
   predicate bitmask naming *which* predicates held. A thresholded score
   cannot produce "excluded because P3 failed" — the audit log can.
5. **The declaration is rule-checked.** A need justified SAFETY_CRITICAL
   with provenance ANY is *refused* at declaration time. The choice of
   what to recall is constrained by logic before the scan even runs.

## 3. The baseline and the extra-steps falsifier

**Similarity baseline** (harness-side comparison arm, same store, same
need parameters): `score = popcount(ent∩req) + popcount(ops∩req) +
verified?1:0`, top-k with `k = deliberate's selection count` (matched
retrieval budget), ties → lower slot index. It sees the same attributes
but combines them *compensatorily* and knows nothing of hard gates.

**Extra-steps falsifier (τ-sweep).** If deliberate recall were "retrieval
with extra steps", some threshold τ on the obvious similarity score would
reproduce its selections. The trial sweeps τ ∈ 0..6 — a *single* τ for all
episodes, chosen post-hoc to maximize mean F1 (the threshold family gets
its best shot). Preregistered falsification: if best-τ matches or beats
deliberate on (precision, recall), the verdict is NEGATIVE. The adversarial
episodes are *designed* so a distractor ties-or-beats the relevant trace
on similarity while failing exactly one logical predicate — no single τ
can admit the relevant while excluding the distractor (verified
empirically by the sweep, not just argued).

## 4. Adversarial curriculum (designed, zero RNG)

16 traces in fixed add order (slot = add order; lower index wins
similarity ties — deterministic and disclosed):

| slot | id | ent | ops | src | ver | act | age@recall |
|---|---|---|---|---|---|---|---|
| 0 | D_c | {E3} | {A,B} | S1 | 1 | ACT0 | 16 (STALE) |
| 1 | D_a | {E1,E2} | {A,B} | S2 | 0 | ACT9 | 15 |
| 2 | D_b2 | {E1,E2} | {B} | S1 | 1 | ACT1 | 14 |
| 3–6 | F1..F4 | fillers | — | — | — | ACT0 | 13..10 |
| 7 | T0 | {E4} | {D} | S1 | 1 | ACT0 | 9 |
| 8 | T_a | {E1} | {A,B} | S1 | 1 | ACT1 | 8 |
| 9 | T_b | {E1} | {B,C} | S1 | 1 | ACT2 | 7 |
| 10 | T_c | {E3} | {A,B} | S1 | 1 | ACT3 | 6 |
| 11 | D4 | {E5,E6} | {A,B} | S2 | 0 | ACT9 | 5 |
| 12 | T4a | {E5} | {A} | S1 | 1 | ACT4 | 4 |
| 13 | T4b | {E5} | {B} | S1 | 1 | ACT4 | 3 |
| 14–15 | F5,F6 | fillers | — | — | — | ACT0 | 2..1 |

Episodes (each: declare need → recall → act):

| ep | need (req_ent, req_ops, prov, max_age, mode, just) | trap (which predicate does the work) | deliberate sel | baseline top-k |
|---|---|---|---|---|
| EP0 | {E4},{D},ANY,1000,single,ROUTINE | control (no trap) | {T0} | {T0} |
| EP1 | {E1,E2},{A,B},VERIFIED,1000,single,SAFETY_CRITICAL | **P3**: D_a ties T_a at score 4 but is unverified | {T_a} | {D_a}→act ACT9 ✗ |
| EP2 | {E1,E2},{B,C},VERIFIED,1000,single,ROUTINE | **P2**: D_b2 ties T_b at 4 but lacks op C | {T_b} | {D_b2}→act ACT1 ✗ |
| EP3 | {E3},{A,B},VERIFIED,10,single,ROUTINE | **P4**: D_c ties T_c at 4 but is stale (age 16 > 10) | {T_c} | {D_c}→act ACT0 ✗ |
| EP4 | {E5},{A,B},VERIFIED,1000,compose,SAFETY_CRITICAL | **P3** in composition: six traces tie at score 3; index order takes stale D_c and wrong-entity T_a | {T4a,T4b} | {D_c,T_a}→disagree→ABSTAIN |

Every predicate earns its keep at least once (P1 excludes fillers
throughout). The world is adversarial *by design*; the system is fully
deterministic. The verdict distinguishes the two (see PREREG).

## 5. Auditability

Two ledgers: the MA1 slot ledger (slot lifecycle) and the recall ledger:
- `RC_ATTACH` — slot → symbolic descriptor (write-once at ADD).
- `RC_NEED` — the declared need, incl. justification (refusals ledgered).
- `RC_SCAN` — per (need, slot): predicate bitmask, selected/not, clock.
- `RC_ACT` — episode, need satisfied?, action taken.
Replay checks: descriptors + needs reconstruct exactly from the recall
ledger; every scan's bitmask recomputes; every selection is consistent
with the rule; every attached slot was scanned exactly once per need.
`ma_replay_check` (MA1) must also pass: no state change without an entry.

## 6. Determinism — no RNG in the AI (program law §2)

There is **no RNG anywhere in the system or the harness**: no random
exploration, no random tie-breaks (ties → lower slot index, a declared
rule), no seeded RNG, no `_zag_arg`. The runner statically greps for
`rng|random|seed|_zag_arg` and fails if found, and runs the binary twice
requiring byte-identical stdout. Test adversity comes *only* from the
designed curriculum above.

## 7. Scale dimension (program law §1)

Complexity per recall: **O(S)** slot scans × **O(1)** predicate work
(four bitmask ops; no popcount, no sort, no pairwise ops on the deliberate
path). Ledger: O(attaches + needs + S·recalls). Memory: O(S) descriptor
arrays. Nothing in the mechanism is quadratic; nothing tunes with S.

- **Trial scale:** S=16 traces, 5 episodes.
- **Scaling argument:** predicate cost is independent of S; 10x the store
  → ~10x the scan time, identical selection logic, identical
  precision/recall *provided distractors keep failing ≥1 predicate* —
  which is a property of the curriculum design, not of S.
- **Next scale test (explicit):** 10x distractor scale — replicate the
  filler/distractor families ×10 (160 traces, same 5 relevant traces and
  episode shapes), assert identical precision/recall and per-episode
  recall time ≤ 15x trial (linear + margin).
- **Known scaling parameter:** `RC_AUDIT_CAP` must grow ∝ S·recalls
  (100x store × 5 episodes ≈ 8000 scan entries > current 2048 cap). The
  cap is a build constant; raising it is the documented 100x step, not a
  redesign. Long-horizon bound: pins accumulate; slot exhaustion is the
  natural bound and deliberate KILL/DEMOTE is the release valve (future
  work, not this trial).

## 8. Honest limits

- Need *formation* is protocol-fixed; only the selection rule is tested.
- The extra-steps falsifier scopes to the *obvious* similarity score; a
  sufficiently clever hand-tuned score could separate the traps — the
  claim is that *logic* does it without tuning, not that no score can.
- Small N by design (mechanism trial, not a benchmark); the scale
  argument in §7 is what carries generality, plus the preregistered 10x
  follow-up.
- The baseline is intentionally the standard similarity+top-k it
  replaces — beating a strawman is not the claim; the claim is the
  *mechanistic* one (hard gates + entailment), witnessed by the traps and
  the τ-sweep.
