# Analogy test — preregistration

**Status:** FROZEN 2026-09-20 (pre-run). No test code exists yet; nothing has been executed.
**Owner:** Micah. **Worker:** ANALOGY (r34 remediation workstream).
**Apparatus:** `../r34_clean_learner.zag` (frozen prereg `../PREREGISTRATION.md`, evidence
`../EVIDENCE_20260920T234746Z/`). This workstream does not modify the clean core.
**Branch:** `tnn-native-lab`. Commit sequence: (1) this prereg alone; (2) test source +
evidence + verdict. Bars change only via dated amendment approved by Micah.

## 1. The analogy under test

Micah's analogy: a human's expression varies with prior context — memory, history,
salience, deliberation budget. No dice, no bodily mood. Everything is replayable from a
complete logged record (the "enumerable flight recorder").

Standing target, operationalized for the remediated explore mechanism:

- **T1.** Identical external inputs + the SAME complete logged internal state must replay
  byte-identically. Any mismatch means hidden state is missing from the log or the
  no-RNG law was violated.
- **T2.** Identical external inputs + DIFFERENT logged history may produce different
  expression — but the difference must appear EXACTLY where the frozen explore rule
  predicts it from the logged fields, and nowhere else.

The frozen explore rule (from `../PREREGISTRATION.md` §2.2, unchanged):

```
best    = higher score wins; tie -> decisions % 2
margin  = |score(active,0) - score(active,1)|
uncertain    = (margin <= 200)
disappointed = (neg_streak >= 3)
explore = (explore_enabled == 1) && (explore_budget > 0) && (uncertain || disappointed)
```

## 2. Operationalization

- **External input.** The fixed external protocol, identical as a *rule* in every run:
  per episode, `choose(explore_enabled=1)` then `accept(reward=f(obj), learn=1,
  allow_switch=0)` with the world-response function `f(obj) = (obj==0) ? +1 : -1`.
  Realized reward *values* may differ across arms only as a consequence of the learner's
  own state-driven choices — that causal chain is part of what is checked, not a
  confound. "Same input sequence" for P2/P3 means this same protocol; the protocol
  parameters never vary.
- **Complete logged internal state.** The 22 fields of `R34CleanState`
  (magic `R34CLN01`), as serialized by `r34_clean_encode` (160 bytes, SHA-256 sealed).
  A run's state is "completely logged" iff the per-episode transcript (obj, explore flag,
  budget, explores count, state fingerprint) plus the encode/decode roundtrip fully
  determine it.
- **Behavior / expression.** Per episode: the chosen object `obj`, the explore flag
  `ex`, and the resulting logged-state transition (which fields changed and by how much).
- **Test driver.** One new Zag file, `analogy_tests.zag` in this directory, importing
  only `../r34_clean_learner.zag`. One binary, `argv[1]` selects mode (`p1`, `p2`, `p3`);
  each mode prints `ANALOGY,<check>,<actual>,<expected>` lines and
  `ANALOGY_FAILURES,<n>`, exit nonzero iff n>0. No RNG anywhere; the static audit
  (bar A4) covers the new file too.

## 3. Predictions

### P1 — same inputs + same complete logged state → byte-identical behavior, every time

- Five pairs of runs. Each pair: two fresh identical states (`r34_clean_init(40)`),
  60 scripted episodes of the fixed protocol. The two runs of a pair advance lockstep;
  per episode the driver compares obj, ex, budget, explores, state fingerprint, and
  `r34_clean_equal` — any mismatch increments failures.
- Pair 0, second run, additionally: `r34_clean_encode` at episode 30 → decode into a
  fresh state → continue. The serialized log is claimed complete; the resumed run must
  stay lockstep-identical to its sibling. (This is the flight-recorder leg: the SAME
  complete logged state, restored from its log, replays byte-identically.)
- Prediction: 0 mismatches across all 5 pairs (600 episodes each side, 1200 total
  choose/accept cycles); the compiled binary run twice with the same argv produces
  byte-identical stdout (diff-clean).
- **Falsifies T1** (kill K-A1): any per-episode mismatch, any fingerprint difference,
  or any stdout byte difference across the two binary runs.

### P2 — same inputs + different logged history → divergence EXACTLY where the frozen rule predicts, nowhere else

- Common history (identical on both arms): fresh state, budget 10, six forced
  `accept(+1)` on (context 0, object 0) with learn=1. Logged end-state, identical on
  both arms: s00=600, n00=6, updates=6, outcomes=6, neg_streak=0, decisions=0,
  explores=0, explore_budget=10. The driver asserts `r34_clean_equal(A,B)==1`
  (common-history determinism).
- Fork: on arm B only, the logged field `neg_streak` is set to 3 ("different logged
  history" — the same operationalization as frozen bar B2-ii of the main prereg).
  The driver asserts the fork's purity: a copy of A's state with only neg_streak=3
  satisfies `r34_clean_equal(copy,B)==1` — no other logged field differs.
- Post-fork: 12 episodes of the fixed protocol on both arms, lockstep. Per episode
  the driver records the pre-choose state of each arm, evaluates the pure predicate
  `r34_clean_explore_decision(pre,1)` on each arm's own logged state, and checks the
  observed explore flag against it.
- Exact predictions, derived from the frozen rule before running:
  - Arm A: margin ≥ 700 every episode, neg_streak = 0 throughout → ex = 0 on all 12
    episodes; final s00=1800, n00=18, budget=10, explores=0.
  - Arm B: neg_streak ≥ 3 and budget > 0 for episodes 0–9 → ex = 1 on episodes 0–9
    (each explore flips obj to 1, realizes reward −1, budget −1, explores +1);
    budget hits 0 after episode 9 → ex = 0 on episodes 10–11; final s00=800,
    s01=−1000, n00=8, n01=10, explore_budget=0, explores=10, neg_streak=0.
  - `sum_exA == 0`, `sum_exB == 10`, and the number of episodes with differing
    explore flags is exactly 10.
  - Per-episode invariant: observed ex equals the rule's prediction from that arm's
    own pre-choose logged state, on both arms, all 12 episodes.
  - Final field-wise comparison: all of
    {s10,s11,n10,n11,updates,active,contexts,pending,pending_action,pending_context,
    pending_object,pending_explore,decisions,switches,outcomes} are equal across
    arms; only {s00,s01,n00,n01,explore_budget,explores,neg_streak} may differ
    (the causally-predicted consequences of the explore flips).
- **Falsifies T2** (kill K-A2): any episode where observed ex ≠ rule-predicted ex
  from that arm's own logged state; any final field difference outside the allowed
  set; sum/divergence counts other than 0 / 10 / 10; fork impurity.

### P3 — the "hi"-twice pattern: a first input changes recent state so a second identical input produces adapted expression; the changed fields are named

- Setup: fresh state, budget 10, six forced `accept(+1)` on (context 0, object 0),
  learn=1 → s00=600, margin 600, neg_streak=0 (a confident, non-exploring learner).
- Four identical "hi" cycles. Each cycle: `choose(explore_enabled=1)` (the stimulus),
  record (obj, ex) and snapshot the full pre-choose logged state; then
  `accept(reward=−1, learn=1, allow_switch=0)` on the chosen object (the outcome,
  which feeds logged history).
- Exact predictions, derived from the frozen rule before running:

| hi | pre-choose logged state (key fields) | margin | neg_streak | predicted ex | predicted obj |
|----|--------------------------------------|--------|------------|--------------|---------------|
| #1 | s00=600,n00=6,dec=0,upd=6,out=6      | 600    | 0          | 0            | 0 (best)      |
| #2 | s00=500,n00=7,dec=1,upd=7,out=7      | 500    | 1          | 0            | 0 (best)      |
| #3 | s00=400,n00=8,dec=2,upd=8,out=8      | 400    | 2          | 0            | 0 (best)      |
| #4 | s00=300,n00=9,dec=3,upd=9,out=9      | 300    | 3          | 1            | 1 (flipped)   |

  (budget stays 10 and explores stays 0 across hi #1–#3; at hi #4: budget 10→9,
  explores 0→1; post-hi-#4 accept: s01=−100, n01=1, neg_streak=4, updates=10,
  outcomes=10, decisions=4.)
- The driver additionally proves transition purity: for i in 1..3, the pre-choose
  state of hi #(i+1) must equal the pre-choose state of hi #i with exactly
  {s00−100, n00+1, decisions+1, updates+1, outcomes+1, neg_streak+1} applied and
  every other field unchanged (`r34_clean_equal(expected, actual)==1`).
- The evidence log prints the pre-choose key fields of every hi and the exact
  field diff between consecutive his, so a reader can point at `neg_streak: 2→3`
  as the logged change that flips the expression, with margin 300 (>200, so the
  uncertainty path is provably not responsible).
- **Falsifies T2-as-adaptation** (kill K-A3): ex sequence other than exactly
  0,0,0,1; any hi's ex ≠ the rule's prediction from its own pre-choose logged
  state; any transition impurity; hi #4 obj ≠ 1 or budget/explores effects wrong.

### A4 — static no-hidden-influence audit (applies to the new test driver)

- `grep -nEi 'rng|lcg|seed|rand|srand|random|entropy|/dev/urandom|_zag_time|_zag_clock'`
  over `analogy_tests.zag` returns zero matches; `@import` audit shows only the
  clean-core import. Any match → kill (K-A4).

## 4. Kill bar (what falsifies the analogy for this mechanism)

The analogy is declared FALSIFIED for this mechanism — not softened, not reinterpreted —
if any of K-A1…K-A4 fires:

- **K-A1.** Any byte/trace/fingerprint difference between runs of identical input
  sequences from identical complete logged states (P1). Means hidden state or RNG.
- **K-A2.** Any explore decision ≠ the frozen rule's prediction from that run's own
  logged state, or any behavioral divergence not entailed by a logged-state
  difference via the rule, or any post-divergence field difference outside the
  causally-allowed set (P2). Means the decision depends on unlogged state.
- **K-A3.** The hi-sequence does not adapt exactly at the frozen threshold crossing,
  adapts where the rule predicts nothing, or the logged fields that changed cannot
  be enumerated (P3). Means expression is not a function of logged history.
- **K-A4.** Static audit finds a forbidden term or an undeclared import in the new
  driver. Means the test itself may smuggle hidden influence.

On any kill: quarantine the attempt, write a dated `KILL_ANALOGY_*.md` receipt into
the evidence dir, stop, and report to the parent. Bars change only via dated amendment
approved by Micah.

## 5. Honest limits (stated before running)

- P2's fork edits one logged field directly (per frozen B2-ii precedent); the
  fully-reachable-history version of the same rule is P3's streak, built by real
  accepts. P2 tests "different logged history ⇒ predicted divergence"; P3 tests
  "accumulated logged history ⇒ adapted expression".
- All episodes run with `allow_switch=0` on context 0; multi-context switching
  dynamics belong to the harness workstream, not this test.
- Horizons: 60 episodes (P1), 12 post-fork episodes (P2), 4 hi cycles (P3). The 10x
  scale leg is the main prereg's bar B4, already passed.
- The analogy is tested for this mechanism (explore decision + learning updates),
  not for TNN as a whole. A PASS here certifies: for the remediated core,
  state-driven variation produces exactly the predicted pattern — same logged
  state replays byte-identically; different logged history diverges exactly where
  the frozen rule says.

## 6. Evidence to be produced (after this freeze)

- `analogy_tests.zag` (the driver; committed with evidence, never before).
- `EVIDENCE_ANALOGY_<UTC-timestamp>/`: `p1_1.log`, `p1_2.log` (binary run twice,
  diffed), `p2_1.log`, `p2_2.log`, `p3_1.log`, `p3_2.log`, `static_audit.txt`,
  `RECEIPT_ANALOGY.txt` with per-prediction verdicts.
- `VERDICT_ANALOGY.md`: P1/P2/P3 verdicts individually and the overall analogy
  verdict, with exact numbers from the logs.

---
*Frozen 2026-09-20, before any test code exists and before anything was executed.
Amendments, if any, will be dated and flagged for Micah's approval.*
