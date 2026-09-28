# NSR — Native Structural Revision: design

Agent (wave 3), 2026-09-19. Native Zag implementation of R27's proven
learning atom — `diagnosis → proposal → measured base/candidate →
PROMOTE or rollback` — as deliberate, audited, refusable operations.
Schema-faithful to `self_revision_history` (STATE_SCHEMA.md §6) and the
P1 STRUCT-PROMOTE stretch notes (LH-P3/RESULT.md §6), rebuilt without the
parts Micah bans: **no score tables, no accumulators, no argmax-as-
intelligence, no reward signal, no RNG anywhere in the system.**

## 0. The idea in one paragraph

The system's structure is a **symbolic trace**: `(read component,
FILTER_GT threshold, polarity)` over a cue vector — the native analog of
R27's `Trace` (symbolic opcodes over cue vectors, operations not
gradients; STATE_SCHEMA.md §5). Learning is never a number going up or
down. It is a *structural edit* to the trace, proposed in response to a
named diagnosis, measured against the frozen base on paired fresh probes,
and committed only if the candidate is strictly better **and** the base
is measured failing — otherwise rolled back. Every step is an audited op
with a refusal path; the ledger replays to exact state (the MA1
"conscious" test). The P1 stretch proved the promote/rollback *gate*
works natively (6/7 promotions, 1 correct rollback) but built it on dual
2×2 score tables and found it added nothing on a clean protocol at 78%
probe overhead. NSR keeps P1's gate shape and drops the tables: the
thing under revision is symbolic structure, and the trial's adversity is
a regime inversion the base structure cannot survive — the case where
quarantining damage in the candidate is the hypothesized win (LH-P3 §6).

## 1. State (no table, no accumulator, no RNG)

```
slot[2]: { live:u8, read:u8, thresh:i32, inv:u8,   // the symbolic trace
            hits:u8, total:u8,                     // RECORDED probe evidence (replaced per batch)
            edit_idx:u8, diag:u8, neg_streak:u8, tried:u8 }
audit: fixed ledger, 10 words/entry, cap 8192
clock: i32
```

- Slot 0 = **accepted** structure (drives judgments). Slot 1 =
  **candidate** scratch (quarantine).
- `hits/total` is a *record of what was observed*, replaced wholesale per
  batch — never incremented by a rule. There is no `+=` anywhere.
- `tried` is a bitmask of rejected structural edits for the current
  accepted base — the system's memory of which hypotheses already failed,
  so proposals are educated (systematic), never random.
- **Determinism:** no RNG in the system. Diagnosis is a deterministic
  function of recorded evidence; proposal derivation is a fixed ordered
  edit list; promotion is a measured comparison. Same state → same ops.

## 2. Operations (the learner's action set)

| Op | Effect | Refusal |
|---|---|---|
| `SR_SEED(trace)` | Boot commitment of the accepted structure. | `REFUSED_SEEDED` (already seeded), `REFUSED_BADVAL` |
| `SR_RECORD(slot,hits,total)` | Deliberate act of recording a measured batch; replaces the evidence window. Updates the sustained-failure streak on the accepted slot (deterministic function of the record). | `REFUSED_NOTLIVE`, `REFUSED_BADVAL` |
| `SR_DIAGNOSE()` | Derives the diagnosis code from recorded evidence: streak≥2 → `SUSTAINED`, streak≥1 → `FAILING_MAJORITY`, else `NONE`. The diagnosis is *declared*, not felt. | `REFUSED_NOTLIVE` |
| `SR_PROPOSE()` | Derives ONE structural variant of the accepted trace from the fixed ordered edit list, skipping edits already rejected for this base (`tried` mask). Fills the candidate slot. **Requires a SUSTAINED diagnosis** — a single failing batch only records the diagnosis; proposals are withheld until the failure is corroborated across consecutive batches (amendment A1, PREREG.md). | `REFUSED_NODIAG`, `REFUSED_BUSY`, `REFUSED_EXHAUSTED` |
| `SR_PROMOTE(b_hits,b_tot,c_hits,c_tot)` | Commits candidate → accepted **iff** candidate strictly better than base on the paired batch **and** candidate majority-positive **and** base majority-negative (the corroboration dual-condition, cf. CTX §3). The paired batch is 32 fresh probes (amendment A1). Resets `tried`, clears diagnosis and candidate. | `REFUSED_NOCAND`, `REFUSED_BADVAL`, **`REFUSED_NOTBETTER`** |
| `SR_ROLLBACK()` | Discards the candidate; marks its edit in `tried` (a rejected hypothesis is remembered). | `REFUSED_NOCAND` |
| `SR_AUDIT_CHECK()` | Three invariants: refusals never mutated state; ledger replays to exact live state; accepted structure changed only via `SR_SEED`/`SR_PROMOTE` entries. | — |

**The fixed structural edit neighborhood** (order is the hypothesis
priority — deterministic, educated, no sampling):
0. flip polarity · 1. threshold −100 · 2. threshold +100 ·
3. read next component · 4. read previous component.
Exhaustion is a first-class outcome (`REFUSED_EXHAUSTED`): the system can
say "I have no untried structural hypothesis for this diagnosis."

## 3. Measurement, not reward

`base_accuracy` / `candidate_accuracy` in the R27 schema are accuracies,
not rewards — NSR keeps it that way. The harness measures both traces on
a **paired fresh probe batch** (same probes, learning frozen, probes
never reused for endpoint validation). The promotion gate compares
*recorded observations*; no value signal flows into the system, no
accumulator is updated, nothing is maximized. Compute cost is recorded
per revision as a fixed-point multiplier (probes spent / 16), the native
analog of R27's `compute_multiplier`; `authorship` is the fixed loop id
`NSR_LOOP_V1` (honest boundary: the harness drives the policy, exactly as
HT1 fixed the learner policy — the *mechanism* is what's under test).

## 4. The trial world (designed adversity, deterministic system)

Cue: 8 i32 components in [0,1000). Label regimes (designed,
amendment A3 — every adversity is an explicit curriculum element,
identical on every seed):
- **R0:** label = (c0 > 500) — exact match for the base trace: every
  R0 batch is exactly 13/16 (3 designed flips). No accidental dips.
- **Dip curriculum:** episodes 10–11 carry a 9/16 flip burst
  (monitoring batches only) → 7/16, sustained → exercises the
  propose→measure→rollback path deterministically. Paired/endpoint
  measurements always use standard flips.
- **R1:** label = (c0 ≤ 500) — the structural inverse of the base
  trace's predicate (amendment A2): the base trace scores ~0% here
  (~3/16 with flips), and exactly one neighborhood edit (polarity flip)
  recovers ~13/16. A sum-rule inverse was tried first and correctly
  exhausted — no single-component edit fixes a sum inversion.
- Adversarial flips: exactly 3 of every 16 probes flipped
  (`p % 20 < 3`) — the noise is a designed sequence, not a draw.

Arms: **SHIFT** (R0 24 eps → R1 16 eps → R0 16 eps; two designed
inversions), **NO-SHIFT** (R0 throughout — the churn control),
**FROZEN** (shift happens, revision loop disabled — the cost-of-not-
revising control), **SHIFT-LCG** (same protocol, cue values and flips
from a seeded harness LCG — scaffolding variant, RNG lives in the
harness only, never in the system), **SCALE** (10× horizon, 560 eps, 9
designed inversions — the scale test).

Designed-world batches are exactly 13/16 (R0), 7/16 (dip episodes
10–11), and 3/16 (R1) — the system's determinism makes every seed
reproduce them; the LCG arm adds distributional variety around those
values.

## 5. Why this is post-table (and post-P1-tables)

1. The thing that changes is a **symbolic trace's content**, not a
   number. There is no update rule, no `+=`, no argmax, no threshold on
   an accumulated scalar.
2. Every commitment is an **op with a refusal path** (`REFUSED_NOTBETTER`,
   `REFUSED_EXHAUSTED`, …). A table cannot refuse; this system refuses
   more often than it commits (expected: 2 promotes, 0 rollbacks on the
   designed SHIFT — each promote preceded by a measured rejection of the
   status quo, and the derivation order means wrong hypotheses would be
   tried and rolled back first in richer worlds).
3. Every promotion carries its **reason in the ledger**: diagnosis code,
   base vs candidate evidence, compute multiplier, authorship — the R27
   `self_revision_history` schema, natively.

## 6. Scale dimension (program law)

Per-episode cost is O(1) ops + O(K) probe evaluations; a revision costs
one paired batch; the ledger grows O(episodes + revisions) with fixed
entry size; replay is O(entries). **In-trial:** the SCALE arm runs 10×
horizon / 9 inversions and reports ledger usage vs cap and wall-clock.
**Scaling argument:** nothing in the mechanism is quadratic in horizon,
trace count, or memory size — the ledger is the linear cost, replay the
linear check. **Next scale test (explicit, not run here):** NSR-SCALE2 —
a bank of N traces under simultaneous management (diagnosis scans N,
O(N) per episode), 100× horizon, plus trace-op composition (multi-op
traces), preregistered separately. If SCALE degrades (missed promotes,
ledger pressure, endpoint drop), that result goes in TRIAL_RESULTS as a
negative on the scaling claim.

## 7. What NSR does NOT show (honest boundaries)

- The policy driving the ops (when to record, when to diagnose) is
  protocol-fixed in the harness — the *mechanism* is under test (cf.
  HT1 §4, MA1). Learner-driven invocation is the HT2-class follow-up.
- One trace, one cue family, synthetic world. Generality is not claimed.
- The edit neighborhood is fixed and small; richer hypothesis generation
  (trace composition) is future work.
