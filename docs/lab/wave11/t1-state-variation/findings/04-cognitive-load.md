# Slice 04 — Deterministic Cognitive Load (Track 1: state-dependent variation)

## 1. Slice

Define a deterministic "cognitive load" metric L computed purely from logged internal state,
and a lawful monotone mapping from L to expression depth (terseness, elaboration, alternatives
shown) — so identical inputs with different internal states legitimately produce different
*expression* while verdicts, memory decisions, integrity refusals, and ledger contents stay
byte-identical for identical full state.

## 2. Falsifiable claim

There exists a deterministic load metric L (formula below) such that, over a preregistered
developmental curriculum: (a) L varies with internal state (variance across episodes > bar,
not degenerate), (b) the expression mapping is monotone non-increasing in elaboration with L,
(c) byte-identical replay from full logged state always reproduces both L and the output
exactly, and (d) at maximum load, no integrity refusal and no mandatory ledger entry is ever
suppressed. If (c) or (d) fails once, or (a)/(b) fail at prereg bars, the design is dead.

## 3. Design

**State inputs (all already-logged, replayable counters — enumerated in prereg):**
- `H`: open-hypothesis count (live hypotheses not yet killed/refuted by eliminative logic)
- `S`: context-partition switches in the last K=32 episodes (switch *rate*)
- `C`: pending corroborations (claims awaiting corroborating evidence; cf. wave9 trust tiers)
- `R`: integrity refusals issued in the last K=32 episodes

**Formula (integer arithmetic only — no floats, no RNG, caps fixed in prereg):**

```zag
pub const HMAX:i32 = 64; pub const SMAX:i32 = 32;
pub const CMAX:i32 = 128; pub const RMAX:i32 = 16;

pub fn cognitive_load(h:i32, s:i32, c:i32, r:i32) i32 {
    let hn = min_i32(h, HMAX) * 100 / HMAX;  // 0..100
    let sn = min_i32(s, SMAX) * 100 / SMAX;
    let cn = min_i32(c, CMAX) * 100 / CMAX;
    let rn = min_i32(r, RMAX) * 100 / RMAX;
    // weights 40/25/25/10, integer: (40*hn + 25*sn + 25*cn + 10*rn) / 100
    return (40*hn + 25*sn + 25*cn + 10*rn) / 100;  // L in 0..100
}
```

**Monotone load→expression mapping (documented tiers, decreasing elaboration):**

| L range | Tier | Lawful expression |
|---|---|---|
| 0–20 | FULL | conclusion + all alternatives considered + full evidence |
| 21–50 | NORMAL | conclusion + decisive evidence + alternatives named |
| 51–80 | TERSE | conclusion + decisive evidence pointer; alternatives compressed to one line |
| 81–100 | MINIMAL | conclusion + single decisive evidence pointer |

Monotonicity: if L1 < L2, output(L2) elaboration ⊆ output(L1) elaboration (strictly
non-increasing; verified by diffing node counts on the composition plan). Within a tier,
ordering is deterministic: highest decisive-evidence weight first (integer score, ties broken
by lowest memory slot id — never by recency-of-insertion or hash).

**Floor guarantees (danger case — load NEVER suppresses required content):**

1. **Decision/expression separation.** The refusal *verdict* and memory *decisions* are computed
   upstream of the expression layer. `cognitive_load` only parameterizes the composition plan;
   it has no input edge into verdict, memory-op, or refusal logic. A load value cannot exist
   in the causal chain of a refusal decision.
2. **Required-node manifest.** Every composition plan tags nodes `required` vs `optional`.
   Required: verdict, rule/standard id for refusals, ledger evidence pointers, memory-op
   records. The load reducer may drop only `optional` nodes; a static check (`cl_check` on the
   plan) asserts all required nodes survive at every L before emission.
3. **Ledger path independence.** Ledger appends are unconditional and occur on the record path,
   not the expression path: `ledger_append` is called by the decision layer and is not gated
   by, and does not read, L. Load is *computed from* state; it never *gates* a write.
4. **Refusal floor text.** Even at L=100, an integrity refusal emits the fixed minimum template:
   verdict + violated standard id + one evidence pointer. Terseness applies only to the
   surrounding explanation, never to the refusal triple itself.

## 4. Kill bar

Preregistered; any single firing kills the slice (no repair-in-place, no re-tuning):

- **K1 (suppression):** In any trial run at any L, one integrity refusal suppressed, one refusal
  triple missing a field, or one mandatory ledger entry omitted → KILL immediately.
- **K2 (replay):** Replaying input + full logged state produces a different L or any
  byte-difference in output vs the original run, in ≥1 of 100 replay trials at 10x scale → KILL.
- **K3 (degeneracy):** L's episode-to-episode variance across the 10x developmental curriculum
  < 25 (population variance on 0–100 scale), i.e. the metric doesn't track state → KILL.
- **K4 (monotonicity):** Any pair of states with L1 < L2 where output(L2) contains elaboration
  nodes absent from output(L1) (elaboration increase under higher load) → KILL.
- **K5 (verdict leak):** Any verdict, memory decision, or refusal *outcome* differing between
  two runs that differ only in L-relevant counters (same decision-relevant state) → KILL.

## 5. Honesty notes

- The weights (40/25/25/10) and caps are **arbitrary engineering choices**, not derived theory.
  Per no-free-lunch, they must be benchmarked against at least two alternative weightings
  before any claim that this weighting is "the" load metric; a wrong weighting fails K3, not
  the program.
- Load here is a **compression knob on expression**, not a claim about cognition or
  phenomenology. It says nothing about how hard TNN "thinks"; felt intensity is dead
  (retired 2026-09-20, K4 harm + K3' restatement) and this must not be read as its revival.
- Weakest point: the required/optional tagging is only as good as the composition planner's
  discipline. A builder bug tagging a ledger pointer `optional` would be caught by K1 only if
  the trial actually reaches high load on a ledger-bearing episode — the trial MUST include
  forced high-load episodes with mandatory ledger writes (adversarial scheduling, deterministic).
- Not claiming: that high load *should* make TNN terse (that's Micah's variation goal
  aesthetic — humans under load are terser); claiming only that IF load gates expression, it
  does so deterministically, monotonically, and never touches integrity.
- Interaction risk: deliberate hypothesis-killing (MA1 machinery) lowers H and hence L —
  the learner could in principle game terseness by killing hypotheses. This is lawful
  (hypothesis death is deliberate and audited) but the prereg must log L alongside every
  hypothesis-kill so gaming, if present, is visible in the audit trail.

## 6. Next build step

Build the **composition planner with required/optional node tagging + `cognitive_load` in
native Zag**, then run the 10x determinism suite: 100 replay trials (same full logged state →
byte-identical L and output, targeting K2) interleaved with adversarial forced-high-load
episodes carrying mandatory ledger writes and integrity refusals (targeting K1). One build,
two kill bars tested. If K3 fires (degenerate metric), benchmark two alternative weightings
before concluding anything about load as a concept.
