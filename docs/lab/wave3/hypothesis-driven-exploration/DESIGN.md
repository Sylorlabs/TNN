# DESIGN — hypothesis-driven exploration (HDE v1)

Wave-3 investigation `hypothesis-driven-exploration`, 2026-09-19.
The direct replacement for ε-greedy: exploration budget is spent ONLY on
tests that discriminate between live, explicitly-represented hypotheses.
No random flips, no adaptive rates on randomness — randomness is gone.

## Program-law compliance (Micah's 2026-09-19 update)

- **No RNG anywhere in the AI's decision paths.** The HDE core has no rng
  field, no LCG, no seeded anything, no stochastic tie-break. Ties resolve
  by a fixed rule (lowest object index). Every decision is a deterministic
  function of the hypothesis registry state. A static check (`grep -i rng`
  over `learner_core.zag` must be empty) is part of the trial evidence.
- **The random-exploration baseline stays** — ε-greedy is the adversarial
  baseline being beaten, which the program law explicitly allows.
- **Adversity = designed curricula** (SINGLE/FLAP/WALK/STORM below), not
  seeded RNG. The world advances an internal LCG tick counter per step, but
  outcomes are a deterministic function of (regime, action) — verified by
  reading `world.zag` (`cw_step`: reward depends only on regime/object).
  The verdict distinguishes "the system is deterministic" (rerun-identical
  TRL lines) from "the test was adversarial" (designed curriculum).

## The mechanism

### Hypothesis registry (the learner's entire memory)

Per context c ∈ {0,1}, two claim slots:

| slot | role | claim text |
|------|------|-----------|
| 0 | incumbent | "object O is the best arm in context c" |
| 1 | challenger | "object O′ is better than the incumbent in context c" |

Each claim: `obj`, `state`, `support`, `refute`, `spent` (test episodes).
Claim states: EMPTY / DORMANT / OPEN / TESTING / CONFIRMED / REFUTED /
ARCHIVED. Plus one cross-context hypothesis slot:

| hypothesis | claim text | test |
|------------|-----------|------|
| H_RECRUIT | "this surprise is a new regime; a fresh context will resolve it" | recruit context 1, probe object 0 |
| H_SWITCH | "this surprise is a known regime; the other context holds the answer" | switch active context, play its incumbent |

H_RECRUIT/H_SWITCH are one-shot action-hypotheses: after the test episode
they are ARCHIVED with the outcome recorded (support=1/refute=1), never
re-tested.

Per context: `displacements` (incumbent swaps so far), `incmax` (incumbent
has achieved the maximum observed reward). Global: `maxrw`.

### The loop: propose → derive test → run → keep/discard/refine

1. **Choose (exploit by default).** Play the incumbent's object. A
   challenger is tested ONLY if it is OPEN *and* the incumbent has not
   achieved max reward (a question that cannot beat the incumbent is not
   asked — derived in `choose`, not by randomness). A live H_RECRUIT /
   H_SWITCH is tested instead (priority to the cross-context question).
   Every test episode is flagged `was_explore=1` and counted.
2. **Accept (credit).** Delayed outcomes route to the matching claim:
   support/refute counters move; CONFIRM at support≥3, REFUTE at
   refute≥2, ARCHIVED as inconclusive at 3 spent tests without decision.
3. **Surprise (negative, non-test outcome on the working hypothesis)**
   → attribute, then propose competing explanations, priority by evidence:
   - **Attribution rule (A3):** the outcome is counted first; if the
     surprise handler forms a cross-context hypothesis (H_RECRUIT /
     H_SWITCH), the triggering negative is reassigned from the arm level
     to the context level — it does not refute the arm claim. A negative
     explained by "wrong context" is not evidence for "wrong arm". Without
     this, regime-change negatives spuriously refute confirmed claims
     (two surprises refuted a 20-support claim in testing).
   - a failed partition falls back to H_ARM (don't loop a refuted idea);
   - other context exists AND has a CONFIRMED incumbent → H_SWITCH
     (use what you know);
   - single context → H_RECRUIT (**preservation before revision**: never
     destroy a confirmed claim to explain a surprise; partition first,
     revise locally only if the partition test fails);
   - multiple contexts but none confirmed → H_ARM (local explanation).
4. **Refine.** CONFIRMED challenger + suspected incumbent (refute≥1) →
   swap. A challenger whose question is moot (incumbent at max reward) is
   never tested. A refuted challenger is re-opened only by a fresh
   surprise (old refutations go stale when the world changes). A
   **confirmed claim lifts the partition-failure block** (new evidence
   supersedes the old failure). An **inconclusive test** (mixed evidence
   inside one test budget — the non-stationarity signature) escalates to
   the context level (H_SWITCH/H_RECRUIT) instead of grinding the arm.
   **Exhaustion backstop:** if the active context holds no live claim at
   all, form H_SWITCH/H_RECRUIT unconditionally.

### What "educated" means here, concretely

- Tests are derived from named claims, each with a recorded verdict —
  the white box shows *why* each exploration episode happened.
- Priority order is evidence-driven (confirmed knowledge > local probe >
  never random), not a rate, not a coin.
- The moot rule ("don't test a question the incumbent already answers
  at max reward") and the stale-refutation rule ("a surprise re-opens
  settled questions") are logic, fixed before the run.

## Scale dimension (required by program law)

The mechanism scales by construction, not by bigger tables:

- **More partitions:** the registry is per-context; adding contexts adds
  claim slots linearly. H_SWITCH generalizes to "argmax over contexts by
  confirmed claims" (v1 has 2 contexts; the rule is stated
  context-count-independent).
- **10×/100× longer horizons:** claims converge to CONFIRMED/REFUTED and
  then cost zero episodes; per-episode work is O(claims), constant.
  Exploration spend is bounded by (surprises × test budget), not by time.
- **Larger memory:** claims are fixed-size structs; 1000 contexts is
  1000× the v1 registry, no algorithmic change.
- **Next scale test (explicit):** 4-context registry on a 3-regime world
  (needs world extension — regimes are currently binary), then
  480-episode horizons checking that exploration spend stays flat after
  convergence. v1 does NOT claim this yet.

## What would show this is "randomness with extra steps"

See PREREG.md falsification criteria F1–F5. In one line: if it explores as
much as ε-greedy while learning no more, its hypotheses never confirm, its
runs aren't rerun-identical, or any RNG is found in its decision path —
it is rejected, and the negative is recorded the same way.
