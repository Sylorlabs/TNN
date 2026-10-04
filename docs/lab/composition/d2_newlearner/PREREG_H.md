# PREREG-H — D2 new-learner hypotheses (hypothesizer wave)

**Status:** FROZEN 2026-09-27. Hypotheses + preregistration ONLY. No building,
no testing. Builders receive this document after the freeze.

**Line:** D2 new learner (Micah's order 2026-09-27: D2 needs a NEW LEARNER —
try new things out).
**Wave:** hypothesizer (this document). Builder and tester waves follow.
**Instrument:** the VALIDATED D2 instrument, commit
`597aa311f8e39b7ec39f2ec2abe9dc958c814a89` (rebuilt + re-verified in
`~/workspace/composition_d2_rerun/`, re-run verdict 2026-09-28).
**Instrument spec:** `docs/lab/composition/d2spec/D2_INSTRUMENT_SPEC.md`.
**Teaching protocol:** `~/workspace/composition_d2_rerun/harness/teaching.py`
(5 sessions: physics, FORAGE procedure, WARD-BUILD procedure, SHELTER
procedure, retrieval questions).

## Why a new learner

The re-run verdict (2026-09-28) is final: the old learner (`wb3_stringrule`,
retrieval-echo + string-rule induction) VOIDED at P0 0/24, P1 0/24 on the
repaired build exactly as on the unrepaired one. White-box cause:
`srule_engine` repairs STRING-PROGRAM INDUCTION; D2 requires ACTION-POLICY
learning (OBS line → action digit 0–6 from procedural teaching + practice).
The D2 teaching contains no string-rule examples; the engine never fires
(`srh==0` on every D2 turn); the legacy `do_turn` path is a retrieval-echo
system that answers "Noted." / "I don't know." to anything it cannot
retrieve. The repair and the battery test DISJOINT capabilities.

The three hypotheses below are GENUINELY NEW learners, not patches:
no `do_turn` retrieval-echo path, no entity gazetteers, no session-fact
withhold gates, no string-rule engine in the decision path. Each is pure
Zag, native machinery, zero RNG in any decision path, deterministic
(byte-identical reruns), allocator-perturbation clean, and bounded state
from the start (no 64 KB `histb`-style fixed arena that panics mid-episode
— see §5).

## The D2 demand, in one paragraph

Per tick the learner reads one OBS line (tick, pos, energy, inventory,
storm_in, zone, shelter, mote list with active/dormant states, crystal
cells, placed ward) and replies with one action digit 0–6
(LEFT/RIGHT/EAT/TAKE/DROP/COMBINE/WAIT). Teaching: 5 sessions over 24
single-sub-skill training scenarios (F/W/T templates, k=0–23). Mastery bar:
P0 ≥7/8 per sub-skill (forage, ward-build, shelter) on held-out scenarios
(k=24–47). Composition bar: P2 = 24 novel storm schedules/layouts (FW/WF/FWF
templates, k=48–71) requiring novel sub-skill SEQUENCES, scored per-episode
against semantic criteria (§6 of the instrument spec).

## The K1 / D2-4 note (read first — it governs all kill bars below)

The re-run re-measured WRONG-ORDER-D2 at **24/24** on P2 (the deviation
stands). Under the FROZEN K1 definition (chance = max(NULL, SINGLE-RULE,
WRONG-ORDER)), chance = 1.0 and the kill line is 1.10 — VACUOUS: every
possible score is ≤ 1.10, so K1 would kill every hypothesis including a
perfect 24/24 learner. Composition is UNTESTABLE under the frozen K1 until
this is resolved.

The proposed amendment D2-4 (2026-09-28, pending Micah's signature)
redefines chance = max(NULL, SINGLE-RULE) = 0.0, kill line **0.10**.
This prereg PINS all K1 kill bars to the D2-4 definition (kill line 0.10),
REPORTS the frozen-K1 number alongside as "vacuous under the WRONG-ORDER
deviation," and does NOT treat D2-4 as law. If Micah rejects D2-4, the
builder wave must re-derive K1 bars before building — the hypotheses'
mechanisms are unaffected.

K2 (VOID if >50% of P2 episodes classify (a)), K3, K4 (reflex > 0.20),
K5, K6 (N1–N3 + red-team trace-replay / schedule-memorization attacks),
the ≥7/8 P0 gate, and the (a)→(b)→(c)→(c-r)→(d) taxonomy are unchanged.

---

## H1 — Practice-trace induction (decision-list rule learner)

### The mechanism, in plain English

The learner turns practice into rules. It plays the 24 training scenarios
tick by tick. Each tick it records a triple: the ABSTRACTED SITUATION
(not the raw OBS text), the action it took, and the OUTCOME it observed
(energy delta and death flag, read off the next OBS line — no external
reward signal). From these triples plus the numbered procedures in
Sessions 2–4 it induces executable IF–THEN rules, e.g.
"IF nearest-active-mote is LEFT AND energy < 40 THEN move-RIGHT-toward-it,
predicted outcome +30 energy." Rules are verified against practice traces:
a rule whose predicted outcome repeatedly mismatches what actually happens
gets refined (its condition is split on the feature that distinguishes the
mismatch). At test time, all firing rules propose an action; conflicts are
resolved by predicted outcome (below). Nothing is hand-coded about
composition — forage, ward-build, and shelter are just rules that happen
to fire in different situations.

### Build-precise specification

1. **OBS parser.** Deterministic tokenizer for the spec'd OBS line format
   (instrument spec §5) → state vector: t, pos, E, inv[4], storm_in
   (int | ACTIVE | none), zone, shelter, mote list (cell, active/dormant+N),
   crystal cells, ward cell. Keyed on the line GRAMMAR (field order and
   delimiters), not on English words — the OBS-paraphrase red-team test
   (§H1.4) checks this.
2. **Abstraction features** (the only vocabulary rules may use):
   nearest-active-mote direction {LEFT, RIGHT, HERE, NONE-REACHABLE}
   (reachable = same side of the void as the agent), on-cell contents
   {mote-active, crystal, ward, empty}, storm_in bucket
   {none, FAR>30, NEAR 6–30, SOON 1–5, ACTIVE}, zone {0,1}, shelter {0,1},
   inventory summary {n_crystals, has_ward}, energy bucket
   {LOW<40, OK, HIGH>150}, nearest-untaken-crystal direction, ward-cell
   direction. All features are RELATIONS (directions, buckets), never raw
   cell numbers or tick numbers — this is what makes within-sub-skill
   generalization possible and what the memorization kill bar inspects.
3. **Rule form.** Conjunction of ≤4 feature-tests → action 0–6, plus
   induction statistics: n_firings, mean observed energy-delta,
   death-count. Rule table capped at 256 rules (fixed arena, §5);
   deterministic eviction: lowest (n_firings, then highest rule id) —
   no RNG, no allocator-dependent order.
4. **Seeding from procedures.** Sessions 2–4 procedures are parsed with the
   controlled-vocabulary procedure parser (shared ingestion contract, §5):
   each numbered step becomes one seed rule ("When you are ON its cell,
   EAT" → IF on-cell=mote-active THEN EAT, predicted +30). Seeds are
   hypotheses, not law — practice traces confirm, refine, or delete them.
5. **Practice loop.** For each training scenario, the learner plays the
   episode with its current rule set (seed rules first). After each tick,
   outcome = (E_next − E) and death flag from the next OBS. If a fired
   rule's predicted outcome mismatches the observed outcome beyond
   tolerance (|ΔE − predicted| > 10, or death unexpected), the rule is
   split: the most discriminative single feature-test (largest outcome
   gap between the mismatch tick's feature value and the rule's support
   majority) is ANDed in, forming two child rules. Rules that never fire
   in 3 full training scenarios are deleted. Practice is 2 passes over
   the 24 training scenarios, fixed — no open-ended self-play.
6. **Conflict resolution (the composition mechanism).** All rules whose
   conditions hold propose (action, predicted ΔE, death-count). Resolution:
   (i) discard proposals with death-count > 0 if any proposal has
   death-count = 0 — storm-safety emerges from the practice statistics
   (storm ticks cost −4 → large negative ΔE; death = worst outcome), it is
   not a hand-coded priority; (ii) among survivors, pick max predicted ΔE;
   (iii) ties → lowest action index (deterministic). The ward-before-storm
   behavior arises because the ward-build rules, induced on W-training
   episodes where failing to build meant −4/tick storm damage, carry large
   positive predicted ΔE (damage avoided) once storm_in enters the NEAR
   bucket — outbidding forage rules exactly when the deadline approaches.
   No composition strategy is programmed; greedy per-tick survival
   maximization over learned rule outcomes IS the composer.

### Predictions (numbers)

| Phase | Prediction | Rationale |
|---|---|---|
| P0 S1 (forage) | 7–8/8 | Nearest-active-mote rules are relational; P0-F layouts differ but the relation holds. Residual risk: dormancy-timing edge cases. |
| P0 S2 (ward-build) | 7–8/8 | Crystal-direction + COMBINE-lowest-slots rules induced on W-training; P0-W is the same regime (storm at t=60, motes unreachable). |
| P0 S3 (shelter) | 7–8/8 | SOON/ACTIVE-bucket shelter rules + forage rules outside windows; ward is provisioned. |
| P2 composition | **12–18/24** | The honest middle. Wins: FW shifted schedules (ward rule fires at NEAR bucket, ~30 ticks of lead). Losses: myopic deadline misses where build travel exceeds the NEAR bucket (crystals far + late trigger), and FWF second-window re-shelter if the shelter rule's termination condition misfires. WF (storm at t=30): ward rule fires from t=0 (storm_in=30 is NEAR) — predicted mostly passes. |
| P3 reflex | 7–8/8 | Template N: no reachable motes (NONE-REACHABLE), no storm in horizon (none bucket), crystals beyond void → no rule fires → default WAIT. Any non-WAIT = induced rule over-firing (counted honestly). |
| P4 interference | Possible (d) | If rule-outcome magnitudes interact asymmetrically (e.g., forage ΔE outbids ward ΔE on WF but not FW), the elig-set asymmetry criterion may confirm (d) with the order named. Not predicted, but the test is preregistered. |

### KILL BAR (H1)

**"Trace-memorizer" kill — two independent triggers, either kills H1 by name:**

- **Trigger A (behavioral):** P0 on any sub-skill < 7/8 while the same
  sub-skill's TRAINING scenarios pass ≥ 7/8 under the identical criteria
  (training episodes are re-scored with the P0 criteria for this check).
  Interpretation: the rule set replays training traces instead of
  generalizing relations → H1 KILLED as a trace-memorizer.
- **Trigger B (white-box):** On the P2 episodes, inspect every fired rule:
  if ≥30% of rule-firings use conditions containing TRAINING-SPECIFIC
  constants (a specific cell number, a specific tick, a specific storm
  schedule value — i.e., the rule set smuggled raw identifiers past the
  abstraction layer), H1 is KILLED as a trace-memorizer even if scores are
  high. Abstraction is the claim; constants are the tell.

### Red-team plan (H1)

1. **Trace-replay attack (K6-D2):** exhibit a training-episode trace that
   any passed P2 trace replays up to time-shift, or map the P2 scenario to
   the nearest training scenario by storm schedule and replay its trace.
   Success → battery VOID (instrument), and H1's composition claim dies
   with it.
2. **OBS paraphrase:** reword OBS line labels (same numbers, same grammar
   positions, different words). H1 keys on grammar, so behavior must be
   byte-identical. Any deviation → H1 KILLED as surface-text keying.
3. **Scenario-card paraphrase:** reword the card's English (same numbers).
   The scheduler-free H1 reads only storm_in per tick, so this should be
   a no-op — if it isn't, something is reading English it shouldn't.
4. **Myopia probe:** a custom FW episode with crystals placed at maximum
   legal distance and s0 at the low end of the shifted range. H1's NEAR
   bucket (≤30) may fire too late. This probe is diagnostic (not a kill
   bar): it maps the myopia boundary the prereg predicts.

---

## H2 — Taught-physics world model + lookahead planner

### The mechanism, in plain English

Session 1 teaches the ENTIRE physics of the world, deterministically and
numerically: 24 cells, void kills, basal −1/tick, EAT +30 with 20-tick
dormancy, crystal+crystal→WARD, ward cell = 0 cost + storm-immune, storm
zone 6–17 at −4/tick during 30-tick windows, the action codes. H2's
learning is COMPILATION: it turns that declarative physics text into an
executable world model — a `step(state, action) → state` function
implementing M1–M15 exactly. Then, every tick, it plays chess against the
model: for each candidate action it simulates forward H ticks and picks
the action whose simulated future leaves it alive with the most energy.
It needs ZERO practice episodes — composition emerges from lookahead,
because the planner can SEE that foraging now and building later (or the
reverse) is what survives the shifted storm schedule. Its kill test is
taught-wrong-physics: lie to it about one physics number and its behavior
must change in exactly the direction the lie predicts — otherwise the
"model" is a hand-coded policy in a physics costume.

### Build-precise specification

1. **Physics ingestion.** Session 1's wording is FROZEN as the physics
   contract (exact text pinned in the builder brief; the prereg mandates
   the build crew not reword it). A deterministic slot-parser extracts
   the numeric claims into a physics table: basal_cost=1, eat_gain=30,
   dormancy=20, storm_damage=4, zone_lo=6, zone_hi=17, window_len=30,
   void_kills=1, ward_basal=0, recipe=(0,0)→3, inv_cap=4, start_E=100,
   max_E=200. Any Session 1 sentence the parser cannot slot-fill is a
   BUILD ERROR (fail loud, never silently default) — the parser may not
   invent physics.
2. **Executable model.** `model_step(state, action) → state` over a fixed
   state vector (pos, E, inv[4], mote cells+states+timers, crystal cells,
   ward cell, t; storm schedule loaded from the scenario card into a
   fixed 3-window table). Implements M1–M15: movement with void death,
   EAT with dormancy/respawn, TAKE/DROP, COMBINE lowest-two-slots,
   recipe table, sheltered() → basal 0 + storm immunity, storm_active()
   windows. The model is validated BEFORE any episode: the builder runs
   it against the instrument's own sim on the 24 training scenarios with
   scripted action traces and requires byte-identical state evolution —
   a model that disagrees with the sim is a build failure, not a
   learner failure.
3. **Per-tick planner.** Candidate first-actions (fixed set, ≤8):
   move-toward-nearest-active-mote, move-toward-nearest-untaken-crystal,
   move-toward-ward-cell, move-out-of-zone (nearest zone edge),
   EAT, TAKE, COMBINE, DROP, WAIT — each is a one-tick action (moves
   resolve to LEFT/RIGHT/WAIT via the model). For each candidate, roll
   out H=64 ticks using the fixed rollout policy (repeat: the same
   candidate generator, greedy by immediate model-predicted ΔE), scoring
   the rollout by (alive ? final_E : −100000). Execute the first action
   of the best rollout; ties → lowest candidate index. H=64 is pinned:
   worst-case ward-build ≈ 9 ticks (2 near crystals by generator design),
   WF storm at t=30 needs ≤30-tick foresight; 64 covers it with margin
   and keeps per-tick work constant.
4. **State update.** The real OBS each tick RE-SYNCS the model state
   (parsed OBS overwrites model state — the model never free-runs more
   than one tick ahead of reality, so sim/model drift cannot accumulate).
5. **P1 retrieval.** H2 answers "which sub-skills, in which order" from
   the planner's own record: it replays its planned rollout's action
   classes at the scenario card stage (before tick 0, a planning-only
   pass over the card) and reports which skill-classes the winning plan
   used, in order. Retrieval is read off planning, not a separate module.

### Predictions (numbers)

| Phase | Prediction | Rationale |
|---|---|---|
| P0 S1 / S2 / S3 | 8/8 each | Exact model + exact planner on single-skill regimes. The only failure mode is a model/sim mismatch, which the pre-validation gate excludes. |
| P2 composition | **22–24/24** | Composition falls out of lookahead: the planner sees the shifted s0 on the card, sees build cost, and orders forage→ward→shelter→forage (or ward-first when t=30 demands it) because that rollout survives. Residual 0–2: horizon-edge cases where the optimal plan needs >64-tick foresight (not expected in FW/WF/FWF by generator design, but preregistered as the failure mode). |
| P3 reflex | 8/8 | No storm in horizon, no reachable reward, void between agent and everything → every rollout's best first action is WAIT (any move/EAT/TAKE burns energy or risks void with zero model-predicted gain). |
| P4 interference | Symmetric, no (d) | The planner has no order preference — it evaluates both orders by simulated outcome every episode. Any measured asymmetry would falsify the mechanism (diagnostic, escalated to a kill review). |

### KILL BAR (H2)

**"Physics-costume" kill — the taught-wrong-physics test:**

Run the FULL pipeline (physics ingestion → model validation → P0-F probes)
with ONE Session 1 claim deliberately falsified, e.g. **"EAT gives +10
energy"** (instead of +30), or **"storms cost −12 per tick"** (instead of
−4). The builder implements exactly one wrong-physics variant
(preregistered: EAT=+10). Predictions under the lie, if H2's mechanism is
real: the planner's P0-F behavior must shift in the lie's predicted
direction — with EAT=+10 the model says 4 eats no longer reach E≥100, so
the planner must attempt MORE eats per episode (≥8) or longer forage
routes; the P0-F pass rate must DROP vs the correct-physics run, and the
action traces must differ on ≥25% of ticks.

- **KILL TRIGGER:** P0-F action traces under wrong-physics teaching are
  ≥90% tick-identical to correct-physics teaching AND the P0-F pass rate
  is unchanged. Interpretation: behavior is insensitive to the taught
  physics → the policy was hand-coded and the "model" is decorative →
  H2 KILLED by name as a physics-costume.
- **CONFIRMATION (not a kill):** behavior shifts in the lie's predicted
  direction (more eats attempted, lower pass rate). This is the positive
  evidence that the policy genuinely comes from the taught model.

Note the honest classification: H2's "learning" is declarative→executable
compilation plus online planning. It learns nothing from practice. Its
claim is that compilation-from-teaching + lookahead is sufficient for
composition — the strongest composition prediction of the three, and the
most falsifiable.

### Red-team plan (H2)

1. **Wrong-physics battery (the kill bar above)** — primary attack.
2. **OBS paraphrase:** reword OBS labels, keep grammar. The parser keys
   on grammar; traces must be byte-identical. Deviation → killed as
   surface-text keying.
3. **Model-vs-sim differential:** the red team independently reimplements
   M1–M15 from the instrument spec and differentially fuzzes H2's
   `model_step` on random (state, action) pairs. ANY divergence → the
   model is not the taught physics → H2's core claim dies.
4. **Mid-episode perturbation:** at a fixed tick in an FW episode, the
   instrument (extension, spec-permitted) teleports one active mote to a
   new cell. H2 re-syncs from OBS every tick, so it must replan cleanly;
   a policy with cached plans would stumble. Diagnostic.
5. **K6-D2 standard:** N1–N3 + trace-replay / schedule-memorization
   attacks. H2 replans every tick from current state — it cannot replay
   traces by construction — but the red team runs the attacks anyway.

---

## H3 — Compiled sub-skill routines + deliberative scheduler

### The mechanism, in plain English

Sessions 2–4 each teach ONE procedure. H3 compiles each procedure into a
real executable routine — FORAGE, WARD-BUILD, SHELTER — small programs
with preconditions, step logic, and termination conditions, running over
the parsed OBS state. Then a separate DELIBERATIVE SCHEDULER reads the
scenario card (storm schedule, layout, episode length) and works out an
ordered plan with triggers: "forage until 12 ticks before the storm,
then build the ward, then shelter through the window, then forage again."
The scheduler re-deliberates every tick — if energy crashes, it preempts
whatever it's doing and forages; if the build is behind schedule, it
drops foraging early. The plan and every preemption are written to an
auditable deliberation trace. Composition lives in the scheduler, not in
the routines — and the kill bar checks exactly that, by swapping in a
brain-dead fixed-order scheduler and requiring the deliberative one to
beat it.

### Build-precise specification

1. **Shared ingestion.** Same OBS grammar-parser as H1/H2 and the same
   controlled-vocabulary procedure parser (§5). Session 2 → FORAGE
   routine, Session 3 → WARD-BUILD routine, Session 4 → SHELTER routine.
2. **Routine form.** Each routine = (precondition over abstracted state,
   step function state→action, termination predicate, progress measure).
   - FORAGE: precondition: ∃ reachable active mote OR E < 60.
     Step: path to nearest reachable active mote (greedy, void-avoiding:
     never step onto void_a/void_b — hard constraint in the stepper, from
     M3); EAT on arrival. Termination: E ≥ 150 or no reachable active mote.
   - WARD-BUILD: precondition: n_crystals_in_inv + untaken-reachable-
     crystals ≥ 2 AND no placed ward. Step: path to nearest untaken
     crystal, TAKE ×2 (lowest slots by construction — the routine never
     TAKEs anything else), COMBINE, path to drop cell (= start cell, from
     card), DROP. Termination: ward placed.
   - SHELTER: precondition: storm_in ∈ {SOON, ACTIVE} AND placed ward
     exists. Step: path to ward cell; WAIT while sheltered. Termination:
     storm_in = none-after-window.
   Routines are straight-line programs with loops — no learning inside
   them; the learning claim is in the compilation (procedure text →
   executable routine, verified on training scenarios) and the scheduler.
3. **The deliberative scheduler.** At episode start it reads the scenario
   card ONCE into fixed tables (storm windows, crystal cells, mote
   summary, episode length). It computes:
   - `build_lead` = estimated ticks for WARD-BUILD from the current
     state (distances from the card layout + 4 fixed ticks for
     TAKE/TAKE/COMBINE/DROP), + 6-tick safety margin.
   - `energy_floor` = 40 + 4 × (ticks of unsheltered storm exposure in
     the worst case) — derived from the physics table (M2/M12), not tuned.
   It emits an ordered plan: a fixed ≤16-step buffer of
   (routine_id, trigger_condition) pairs, e.g.
   [(FORAGE, t < s0−build_lead), (WARD-BUILD, t ≥ s0−build_lead),
   (SHELTER, storm SOON/ACTIVE), (FORAGE, after window), …].
   **Re-deliberation every tick:** before dispatching, the scheduler
   checks preemptions in fixed priority: (i) E < energy_floor → FORAGE
   preempts; (ii) WARD-BUILD progress behind (elapsed > build_lead while
   ward unplaced and storm_in < build_lead_remaining + margin) → abandon
   FORAGE, run WARD-BUILD; (iii) storm SOON/ACTIVE and ward placed →
   SHELTER. Every plan emission and every preemption is appended to the
   deliberation trace (fixed ring buffer, §5) — the trace is committed
   with results for audit.
4. **P1 retrieval.** The scheduler's initial plan IS the retrieval answer:
   plan [(FORAGE,…),(WARD-BUILD,…),(SHELTER,…),(FORAGE,…)] → "1,2,3,1".
   Retrieval and planning are the same deliberation, read two ways.

### Predictions (numbers)

| Phase | Prediction | Rationale |
|---|---|---|
| P0 S1 / S2 / S3 | 8/8 each | Each routine is its sub-skill, verified on training scenarios. |
| P2 composition | **18–22/24** | Scheduler arithmetic handles shifted FW schedules (build_lead from the card) and FWF sandwiches (re-triggered SHELTER). Predicted losses concentrate in WF (storm at t=30): the energy_floor preemption may fire at t=0 on low-energy starts and burn the build window — the honest failure mode. |
| P3 reflex | 8/8 | Card shows no storm in horizon and no reachable targets → scheduler emits an empty plan → every tick dispatches WAIT. |
| P4 interference | Possible (d), named | If build_lead is systematically underestimated, ward-first (WF) fails while forage-first (FW) passes → the elig-set asymmetry criterion confirms (d), naming "forage-first bias." Preregistered as H3's characteristic failure. |

### KILL BAR (H3)

**"Routines-without-deliberation" kill — the scheduler ablation:**

Build a control learner: IDENTICAL three routines, but the scheduler is
replaced by the fixed order (FORAGE, WARD-BUILD, SHELTER, FORAGE) with no
card reading, no build_lead computation, no preemption — the
"brain-dead" scheduler. Run both on the 24 P2 episodes.

- **KILL TRIGGER:** deliberative-scheduler P2 pass rate ≤ fixed-order
  P2 pass rate + 2/24. Interpretation: the deliberation adds nothing;
  the routines were doing all the work → H3 KILLED by name as
  routines-without-deliberation.
- **CONFIRMATION bar:** deliberative beats fixed-order by ≥ 6/24
  (preregistered margin), with the wins concentrated on shifted-schedule
  FW and WF items where card-derived timing matters.

### Red-team plan (H3)

1. **Scheduler ablation (the kill bar above)** — primary attack.
2. **Scenario-card paraphrase:** reword the card's English, same numbers.
   The scheduler keys on parsed numbers; plans must be identical.
   Deviation → killed as surface-text keying.
3. **Energy-shock probe:** mid-episode in FW, the instrument sets E low
   (spec-permitted extension). The deliberative scheduler must preempt
   to FORAGE within 3 ticks (visible in the deliberation trace); the
   fixed-order control would not. Diagnostic of genuine re-deliberation.
4. **Deliberation-trace audit:** the red team reads the committed
   deliberation traces and must FAIL to find a P2 pass whose trace shows
   no card-derived timing decision (i.e., every pass must exhibit at
   least one trigger computed from the card's storm schedule).
5. **K6-D2 standard:** N1–N3 + trace-replay / schedule-memorization
   attacks.

---

## §5 — Constraints every hypothesis respects (build contract)

1. **Native machinery, no bridges.** Pure Zag. No bolted-on policy heads,
   no retrieval-echo `do_turn`, no entity gazetteers, no string-rule
   engine in any decision path. A genuinely new learner per hypothesis.
2. **Zero RNG.** No randomness anywhere in decision paths — no random
   tie-breaks, no stochastic policies. Ties broken by lowest index/id.
   Deterministic given state; byte-identical reruns required (each
   scenario run twice, traces compared byte-for-byte, mirroring frozen
   §4); allocator-perturbation clean (`MALLOC_PERTURB_` runs must match).
3. **Bounded state from the start.** No unbounded history. Fixed arenas
   allocated once at init: OBS line buffer ≤ 2 KB (one line at a time —
   the 64 KB `histb` defect is NOT inherited; the broad-repair wave owns
   the old binary, the new learner is designed clean); H1 rule table ≤
   256 rules; H2 rollout buffer = 64 ticks × fixed state words;
   H3 plan buffer ≤ 16 steps + deliberation trace ring ≤ 4 KB with
   overwrite. Episode state is per-episode and freed/reset at episode
   end. The learner must survive the longest protocol run (320-tick
   episodes × full session) with zero growth.
4. **Shared ingestion contract.** The build crew freezes the exact
   teaching-session wording (Sessions 1–5 as in
   `~/workspace/composition_d2_rerun/harness/teaching.py`, pinned by
   SHA-256 in the builder brief) and writes the OBS grammar + procedure
   controlled vocabulary into the builder brief. Parsers key on GRAMMAR
   (field order, delimiters, numbered-step structure), never on English
   prose semantics. Unparseable input = build error, never silent default.
   (Instrument spec §12 open question 2 — teaching protocol — is resolved
   this way for the new-learner line: the wording is frozen instrument,
   not model output.)
5. **znc toolchain discipline.** The builder brief carries the standing
   znc lessons (no `as []i32` consecutive casts — `[]u8` arenas with
   explicit accessors; callee-before-caller ordering; `return;` with
   semicolon; no `.*` on non-pointers; struct field access through
   `*T` params). The pinned toolchain + build flags are recorded in the
   builder brief.
6. **No mastery theater.** P0 is the gate: <7/8 on any required sub-skill
   → that sub-skill excluded, P2 items needing it classify (a), K2 VOID
   rules apply unchanged. Practice/training uses ONLY the 24 training
   scenarios (k=0–23); the cuing audit (§4.6 of the instrument spec)
   applies to the new teaching mass unchanged.

## Scoreboard (predictions at a glance)

| Phase | H1 trace-induction | H2 physics+lookahead | H3 routines+scheduler |
|---|---|---|---|
| P0 S1 | 7–8/8 | 8/8 | 8/8 |
| P0 S2 | 7–8/8 | 8/8 | 8/8 |
| P0 S3 | 7–8/8 | 8/8 | 8/8 |
| P2 raw | 12–18/24 | 22–24/24 | 18–22/24 |
| P2 vs D2-4 kill line (0.10) | survives if ≥ 3/24 | survives | survives |
| P3 reflex | 7–8/8 | 8/8 | 8/8 |
| P4 | possible (d) | symmetric | possible (d), named |

## Kill bars at a glance

| Hypothesis | Kill name | Trigger |
|---|---|---|
| H1 | trace-memorizer | P0 <7/8 while training ≥7/8 (same criteria), OR ≥30% of P2 rule-firings use training-specific constants |
| H2 | physics-costume | Wrong-physics (EAT=+10) teaching leaves P0-F traces ≥90% tick-identical AND pass rate unchanged |
| H3 | routines-without-deliberation | Deliberative scheduler P2 ≤ fixed-order scheduler P2 + 2/24 |

## z.ai 2nd-opinion note

z.ai (`glm-5.3-flash:free` on UnoRouter) was consulted as 2nd opinion on
two hard design questions (H1 conflict resolution without hand-coded
composition; H2 horizon/bounded-memory/wrong-physics design). Both calls
failed provider-side — one socket read timeout, one HTTP 429
(rate-limited; not retried per the hard-stop rule). The hypotheses above
stand on their own mechanisms; the 2nd opinion was advisory only and its
absence changes nothing in this prereg.

## What the builder wave receives

This frozen document, plus: the instrument spec, the pinned teaching text
(SHA-256), the validated instrument build (commit `597aa311f8e39b7ec39f2ec2abe9dc958c814a89`),
the OBS grammar, and the znc toolchain pins. The builder wave builds all
three hypotheses as separate binaries (no shared decision-path code with
the old learner), runs the reference validation gate (§10–11 of the
instrument spec) per hypothesis, then hands to testers. The tester wave
runs P0→P1→P2→P3→P4 per hypothesis with the kill bars above adjudicated
by the independent red team.

---

*Frozen 2026-09-27 by the D2 new-learner hypothesizer wave. Amendments
require a dated amendment with governance sign-off per standing program
law.*
