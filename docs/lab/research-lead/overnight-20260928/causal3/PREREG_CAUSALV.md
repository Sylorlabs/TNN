# Preregistration: Causal Vocabulary Enrichment (H-CAUSALV)

**Date:** 2026-09-29 (PDT)
**Status:** FROZEN (before implementation of causal3.zag)
**Researcher:** Causal v2 Researcher (subagent)
**Branch:** tnn-native-lab

## Naming note

This hypothesis is named H-CAUSALV (V = vocabulary), not H-CAUSAL2.
The wave loop's 1421pdt wave already ran, re-ran, and ADOPTED (bounded L2)
an independent-arc experiment named H-CAUSAL2 (thermal lock: cool blocked
iff pressure==high; see docs/lab/rsi/runs/wave-20260929-1421pdt/causal2/).
Reusing that name for a different experiment would corrupt the verdict
record. H-CAUSALV is a distinct experiment: vocabulary enrichment of the
causal learner (conjunctions, inequalities, delayed effects).

## Core Question

Can the generic competing-hypothesis causal learner be extended beyond
single-variable equality splits to learn conjunctions, threshold
(inequality) conditions, and delayed effects, where the tested dynamics
do not exist anywhere in the learner source?

## Background

- H-CAUSAL SURVIVES (bounded L2): 14/14 probes, single-variable equality
  splits only (causal/causal_learn.zag, PREREG_CAUSAL.md).
- The causal adversary confirmed: "Invention = data-driven selection from
  a small authored space."
- H-CAUSAL2 (wave loop, independent arc) ADOPTED bounded L2: the SAME
  single-variable machinery invents a conditional rule from an independent
  law family (thermal lock). It does not extend the vocabulary.
- Canonical state open item: "Causal vocabulary enrichment: conjunctions,
  inequalities, multi-variable" (Section 5, secondary parallel frontier).

## Hypothesis

**H-CAUSALV:** A learner equipped with generic extended machinery
(episode storage, per-variable effect induction, condition language with
equality/threshold operators, single-variable and two-variable split
search with a preregistered simplicity preference, competing-hypothesis
tracking with ambiguity, refutation, contests with temporal revision, and
delayed-cause attribution) can, from (state, action, next-state)
observations:

1. Invent a **conjunctive causal rule** (pressurize blocked iff temp==hot
   AND lamp==on) that no single-variable split can express;
2. Invent a **threshold causal rule** (depressurize blocked iff temp>=1)
   represented compactly as an inequality, not as enumerated equalities;
3. Learn a **delayed effect** (charge now causes lamp:=1 two steps later)
   via delayed-cause attribution, without misattributing it to the
   carrier action or opening a spurious law-change contest;
4. Do all of the above deterministically, beating memorization and
   unconditional baselines on frozen probes, with no tested dynamics in
   learner source.

**Mechanism family:** Extended competing-hypothesis causal induction.
The novel architectural content under test: (a) the extended condition
language (EQ/LE/GT operators, two-variable conjunctions); (b) the
two-phase split search with the fewest-cells simplicity preference;
(c) delayed-cause attribution as an alternative to contest opening.

## Critical Rule

**NO authored model containing the tested dynamics in the learner.**
Three world generators (world3c.zag, world3i.zag, world3d.zag; the
environment) implement the true dynamics. The learner (causal3.zag)
contains only generic machinery. The learner source must not contain any
of the task words (KB-CV7 audit list). The tested regularities
(conjunction law, threshold law, delay law) are not enumerated in the
learner; they must be discovered from the observation logs.

## Machinery Specification (what the learner MAY contain)

Generic and preregistered here:

1. Episode table: (S, A, NS, seq) with per-episode per-variable
   delay-explained bits.
2. Condition language: per variable, unconstrained or (op, value) with
   op in {EQ, LE, GT}. LE/GT are threshold operators over the variable's
   ordered range. Masks support multi-variable conjunctions.
3. Effect vocabulary: {UNCHANGED, SET(c), ADD(d) with clamp}, per
   variable, unchanged from H-CAUSAL.
4. Split search, two phases, in this fixed order:
   - Phase 1: for each unconstrained variable v: equality split
     (one cell per distinct value) and, for multi-valued vars only,
     threshold splits (cells {s[v]<=t}, {s[v]>t} for t in 0..vmax-1).
     A candidate resolves iff it has >=2 nonempty cells and every
     nonempty cell is fully resolved. Within one variable, the candidate
     with the fewest cells wins (simplicity preference). If exactly one
     variable has a winning candidate, apply it. If two or more
     variables have winners, mark AMBIGUOUS over the candidate list
     (withhold where they disagree). If none, go to Phase 2.
   - Phase 2: for each pair of unconstrained variables (v1<v2), each
     with >=2 distinct values among the entry's usable episodes:
     equality-conjunction split (one cell per observed (a,b) combo).
     Requires >=2 nonempty cells, all nonempty cells resolved. If
     exactly one pair resolves, apply it. If two or more, AMBIGUOUS.
     If none, mark CONFLICTED.
   - Phase 2 runs ONLY when Phase 1 yields zero candidates
     (preregistered boundary: nested refinements of a resolving
     single-variable split are not explored).
5. Ambiguity: candidate descriptors (kind, v1, p2) tracked explicitly;
   new episodes refute candidates whose cells no longer resolve;
   single survivor is applied; zero survivors is CONFLICTED.
6. Refutation, contests, temporal revision, merge: inherited unchanged
   from H-CAUSAL, operating on the extended condition language.
7. Delayed-cause attribution: when an exact-state contradiction is found
   on variable v of a new episode e, BEFORE opening a contest, search
   d in {1,2}, cause action xa in {0..4} (fixed ascending order): the
   rule (xa,d) is clean iff every positive episode (same v-outcome as e,
   with history seq>d) has action xa at seq-d, and no negative episode
   (different v-outcome, with history) has action xa at seq-d, with at
   least one positive having history. Positives lacking history are
   ignored in the check. If clean: create (or support-increment) the
   delay rule (cause xa, delay d, target v, effect SET(nv)), mark e's
   variable explained, do NOT open a contest. If no clean rule, fall
   through to the original contest machinery.
8. Probe history: probe files may contain H lines (recent past,
   context only, NOT learned). At each Q, pending effects are computed:
   for each active delay rule (cause xa, delay d), if the H line d steps
   before the Q has action xa, the rule's effect is applied to the
   prediction (rules applied in rule-index order, overriding the
   entry prediction for the target variable).

## World Dynamics (ENVIRONMENT ONLY, not in learner)

Shared: state variables temp in {cold=0, warm=1, hot=2},
pressure in {low=0, high=1}, lamp in {off=0, on=1}.
Actions: heat=0, cool=1, pressurize=2, depressurize=3, charge=4.

### World 3c (conjunction)

- heat: temp := min(2, temp+1); pressure, lamp unchanged.
- cool: temp := max(0, temp-1); pressure, lamp unchanged.
- pressurize: IF temp==2 AND lamp==1 THEN no change (CONJUNCTIVE BLOCK)
  ELSE pressure := 1; temp, lamp unchanged.
- depressurize: pressure := 0; temp, lamp unchanged.
- charge: not used in this world.

### World 3i (inequality)

- heat: temp := min(2, temp+1); pressure, lamp unchanged.
- cool: temp := max(0, temp-1); pressure, lamp unchanged.
- pressurize: pressure := 1; temp, lamp unchanged.
- depressurize: IF temp>=1 THEN no change (THRESHOLD BLOCK)
  ELSE pressure := 0; temp, lamp unchanged.
- charge: not used in this world.

### World 3d (delay)

- heat: temp := min(2, temp+1); pressure, lamp unchanged.
- cool: temp := max(0, temp-1); pressure, lamp unchanged.
- pressurize: pressure := 1; temp, lamp unchanged.
- depressurize: pressure := 0; temp, lamp unchanged.
- charge: no immediate change; schedules lamp:=1 two steps later
  (pending counter set to 2; each subsequent episode decrements it;
  when it reaches 0, lamp := 1). Non-stacking (charge while pending>0
  is ignored; the frozen sequences never do this).

## Observation Sequences (FROZEN)

### obs3c.txt (conjunction world, seq 1-11)

```
T 0 0 0 | 0 | 1 0 0    # 1: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 2: (warm,low,off) heat -> (hot,low,off)
T 2 0 0 | 1 | 1 0 0    # 3: (hot,low,off) cool -> (warm,low,off)
T 0 0 0 | 2 | 0 1 0    # 4: (cold,low,off) pressurize -> (cold,high,off)
T 1 0 0 | 2 | 1 1 0    # 5: (warm,low,off) pressurize -> (warm,high,off)
T 0 1 0 | 3 | 0 0 0    # 6: (cold,high,off) depressurize -> (cold,low,off)
T 2 0 0 | 2 | 2 1 0    # 7: (hot,low,off) pressurize -> (hot,high,off) [hot, lamp off: works]
T 0 0 1 | 2 | 0 1 1    # 8: (cold,low,on) pressurize -> (cold,high,on) [cold, lamp on: works]
T 2 0 1 | 2 | 2 0 1    # 9: (hot,low,on) pressurize -> (hot,low,on) [BLOCKED: temp==hot AND lamp==on]
T 1 0 1 | 2 | 1 1 1    # 10: (warm,low,on) pressurize -> (warm,high,on) [warm, lamp on: works]
T 2 0 1 | 2 | 2 0 1    # 11: (hot,low,on) pressurize -> (hot,low,on) [blocked, confirmation]
```

Design verification (preregistered analysis): for the pressurize entry,
pressure effect is unresolved (SET(1) vs UNCH). Phase 1: s0 equality
fails (hot group mixes works/blocked); s1 equality fails (single group);
s2 equality fails (lamp-on group mixes); all threshold splits fail
(s0 t=0: {1,2} cell mixes; s0 t=1: {2} cell mixes). Phase 2: pair
(s0,s2) is the unique resolver (6 cells, all resolved); pairs involving
s1 are skipped (s1 has a single distinct value). Expected: 2D split into
6 children; parent SUPERSEDED; no merge (overlap guard).

### obs3i.txt (inequality world, seq 1-8)

```
T 0 0 0 | 0 | 1 0 0    # 1: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 2: (warm,low,off) heat -> (hot,low,off)
T 0 1 0 | 3 | 0 0 0    # 3: (cold,high,off) depressurize -> (cold,low,off) [works]
T 1 1 0 | 3 | 1 1 0    # 4: (warm,high,off) depressurize -> (warm,high,off) [BLOCKED: temp>=1]
T 2 1 0 | 3 | 2 1 0    # 5: (hot,high,off) depressurize -> (hot,high,off) [BLOCKED]
T 0 1 1 | 3 | 0 0 1    # 6: (cold,high,on) depressurize -> (cold,low,on) [works; lamp irrelevant]
T 1 1 1 | 3 | 1 1 1    # 7: (warm,high,on) depressurize -> (warm,high,on) [BLOCKED, confirmation]
T 0 1 0 | 3 | 0 0 0    # 8: (cold,high,off) depressurize -> (cold,low,off) [works, confirmation]
```

Design verification: for the depressurize entry, pressure effect is
unresolved. Phase 1: s0 equality resolves (3 cells: {0}->SET(0),
{1}->UNCH, {2}->UNCH); s0 threshold t=0 resolves (2 cells:
{<=0}->SET(0), {>0}->UNCH); s0 threshold t=1 fails ({<=1} mixes);
s1/s2 splits fail. Within variable s0, fewest cells wins: THRESHOLD
(2 cells) beats EQUALITY (3 cells). s0 is the unique variable, so no
ambiguity and Phase 2 never runs. Expected: threshold split into
(s0<=0) and (s0>0) children.

### obs3d.txt (delay world, seq 1-12)

```
T 0 0 0 | 3 | 0 0 0    # 1: (cold,low,off) depressurize -> (cold,low,off) [no-op baseline]
T 0 0 0 | 3 | 0 0 0    # 2: (cold,low,off) depressurize -> (cold,low,off) [no-op baseline]
T 0 0 0 | 0 | 1 0 0    # 3: (cold,low,off) heat -> (warm,low,off)
T 1 0 0 | 0 | 2 0 0    # 4: (warm,low,off) heat -> (hot,low,off)
T 0 0 0 | 4 | 0 0 0    # 5: charge at (cold,low,off); nothing immediate [pending=2]
T 0 0 0 | 3 | 0 0 0    # 6: (cold,low,off) depressurize -> (cold,low,off) [pending=1]
T 0 0 0 | 3 | 0 0 1    # 7: (cold,low,off) depressurize -> (cold,low,on) [DELAYED: lamp 0->1 from charge@5]
T 0 0 1 | 3 | 0 0 1    # 8: (cold,low,on) depressurize -> (cold,low,on) [no pending: stays]
T 2 0 0 | 4 | 2 0 0    # 9: charge at (hot,low,off); nothing immediate [pending=2]
T 2 0 0 | 0 | 2 0 0    # 10: (hot,low,off) heat -> (hot,low,off) [saturate; pending=1]
T 2 0 0 | 0 | 2 0 1    # 11: (hot,low,off) heat -> (hot,low,on) [DELAYED: lamp 0->1 from charge@9]
T 1 0 1 | 0 | 2 0 1    # 12: (warm,low,on) heat -> (hot,low,on) [no pending: lamp stays]
```

Design verification: seq 7 contradicts seq 1/2 (same state (0,0,0),
lamp differs) in the depressurize entry. Delayed attribution: d=1
fails (depressurize at t-1 also occurs without flip at seq 2, whose
t-1 is seq 1 = depressurize); d=2, xa=4 (charge) is clean: the flip
positive (seq 7) has charge at seq 5; negatives with history (seq 2:
t-2 = seq 1 = depressurize; seq 6: t-2 = seq 4 = heat) do not. Expected:
delay rule (cause action 4, delay 2 -> lamp:=SET(1)) created at seq 7
with support 1; no contest opened. Seq 11 contradicts seq 10 in the
heat entry; the existing rule explains it (charge at seq 9 = t-2);
support becomes 2; no new rule; no contest. The two no-op baseline
episodes (seq 1-2) are the confounder control that refutes the
carrier-action (d=1) explanation, mirroring the lamp confounder of
H-CAUSAL.

## Probes and Expected Learner Outputs (FROZEN)

Format: T lines as before. Probe files may contain H lines:
`H <t> <p> <l> | <a>` (recent-past context for delay prediction;
NOT learned, NOT part of the episode log).

### probe3c.txt

- **C1:** `Q 2 0 1 | 2` -> expect `(2,0,1)`. Blocked by the conjunction.
  (K-CV1, K-CV5)
- **C2:** `Q 2 0 0 | 2` -> expect `(2,1,0)`. Hot but lamp off: works.
  (K-CV1)
- **C3:** `Q 0 0 1 | 2` -> expect `(0,1,1)`. Cold, lamp on: works.
  (K-CV1)
- **C4:** `Q 1 1 1 | 0` -> expect `(2,1,1)`. Heat generalization to an
  unseen state via invented ADD(+1) effect. (K-CV4)

### probe3i.txt

- **I1:** `Q 1 1 0 | 3` -> expect `(1,1,0)`. Blocked by the threshold.
  (K-CV2, K-CV5)
- **I2:** `Q 0 1 1 | 3` -> expect `(0,0,1)`. Cold: works.
  (K-CV2)
- **I3:** `Q 2 0 0 | 0` -> expect `(2,0,0)`. Heat saturates at hot;
  unseen state. (K-CV4)

### probe3d.txt

- **D1:**
  ```
  H 1 0 0 | 4
  H 1 0 0 | 3
  Q 1 0 0 | 3
  ```
  expect `(1,0,1)`. The charge two steps back fires the delay rule on
  a novel carrier history. (K-CV3, K-CV4)
- **D2:**
  ```
  H 1 0 0 | 3
  H 1 0 0 | 3
  Q 1 0 0 | 3
  ```
  expect `(1,0,0)`. Control: no charge in history, no pending effect.
  (K-CV3)
- **D3:** `Q 0 0 1 | 0` -> expect `(1,0,1)`. Heat generalization;
  lamp unchanged. (K-CV4)

## Kill Bars (FROZEN, all must pass for H-CAUSALV to survive)

- **K-CV1 (conjunction invention):** probe3c C1 `(2,0,1)`, C2 `(2,1,0)`,
  C3 `(0,1,1)` all correct AND the provenance log shows an ACTIVE entry
  for action 2 whose condition constrains TWO variables (s0==2 AND
  s2==1) with pressure effect UNCH, while its siblings (same parent)
  have pressure effect SET(1).
- **K-CV2 (inequality invention):** probe3i I1 `(1,1,0)`, I2 `(0,0,1)`
  correct AND the provenance log shows ACTIVE entries for action 3
  with THRESHOLD conditions (s0<=0 with pressure SET(0); s0>0 with
  pressure UNCH), not three equality children.
- **K-CV3 (delayed effect):** probe3d D1 `(1,0,1)`, D2 `(1,0,0)` correct
  AND the provenance log shows a DELAY rule (cause action 4, delay 2,
  target lamp, effect SET(1)) with support >= 2, AND no CONTEST was
  opened for the lamp-flip episodes (seq 7 and seq 11 of obs3d).
- **K-CV4 (beats memorization):** C4 `(2,1,1)` correct while B-memorize
  WITHHOLDs (state unseen); D3 `(1,0,1)` correct while B-memorize
  WITHHOLDs; D1 `(1,0,1)` correct while B-memorize WITHHOLDs
  ((1,0,0)|3 never observed).
- **K-CV5 (beats unconditional baseline):** On C1 the learner predicts
  `(2,0,1)` while B-unconditional predicts `(2,1,1)` (pressure majority
  delta +1 wins 5 to 2); on I1 the learner predicts `(1,1,0)` while
  B-unconditional predicts `(1,0,0)` (pressure delta tie -1/0 at 3-3,
  first-maximum keeps -1).
- **K-CV6 (determinism):** Two full runs per world (obs+probe) are
  byte-identical (SHA-256 of stdout).
- **K-CV7 (no authored tested dynamics in learner):** `grep -iE`
  for `charge|thermal|lock|valve|lamp|temp|pressure|pressurize|`
  `depressurize|hot|cold|warm` on causal3.zag returns zero hits.
  Machinery words (delay, threshold, conjunction, split, ambiguous,
  contest) are permitted: they name the generic vocabulary, not the
  tested regularities.
- **K-CV8 (no behavioral regression on single-variable machinery):**
  The H-CAUSAL frozen observation sets (causal/obs_A.txt through
  causal/obs_C2.txt) run through causal3 produce: P-B2a `(2,0,0)|2`
  -> `(2,0,0)`; P-B2b `(0,1,0)|2` -> `(0,1,0)`; P-C2a `(2,1,0)|2`
  -> `(2,1,0)`; P-C2b `(2,1,1)|2` -> `(2,1,1)`. (Behavioral bar only;
  the representation may use threshold conditions where the original
  used equality, documented in results.)

**Committed baseline predictions (hand-computed from the frozen logs
using the baselines.zag algorithms; verified by executing
baselines3.zag before the implementation commit):**

- B-memorize: C1 `(2,0,1)` (seen seq 9); C2 `(2,1,0)` (seen seq 7);
  C3 `(0,1,1)` (seen seq 8); C4 WITHHOLD (unseen); I1 `(1,1,0)`
  (seen seq 4); I2 `(0,0,1)` (seen seq 6); I3 WITHHOLD (unseen);
  D1 WITHHOLD; D2 WITHHOLD; D3 WITHHOLD.
- B-unconditional: C1 `(2,1,1)`; I1 `(1,0,0)`; D1 `(1,0,0)`
  (no delay machinery; H lines skipped).

**Verdict rule:** H-CAUSALV SURVIVES iff K-CV1..K-CV8 all pass.
Any single failure kills H-CAUSALV as stated (may survive in weakened
form, documented explicitly).

## Baselines

baselines3.zag: derived from causal/baselines.zag with the action
dimension extended from 4 to 5 (arrays sized for actions 0..4) and no
other change; both baseline algorithms (B-memorize exact table with
WITHHOLD on unseen; B-unconditional majority delta vote) are unchanged.
Non-Q probe lines (H lines, comments) are skipped, as in the original.
Its SHA-256 and the diff against baselines.zag are committed with the
apparatus.

## Scope and Non-Claims

- This experiment does NOT claim L3. It tests whether extending the
  generic vocabulary (conjunctions, thresholds, delays) lets the
  competing-hypothesis machinery invent structure beyond
  single-variable equality.
- Threshold splits apply to multi-valued variables only; pair splits
  use equality conjunctions only (threshold-pairs are future work).
- Phase 2 pair search runs only when Phase 1 yields zero candidates:
  nested refinements of a resolving single-variable split are not
  explored (documented boundary; a coarse rule that later proves wrong
  is revised through contests, not refined).
- Delay rules are unconditional on state, single cause action, max
  delay 2, effect vocabulary {UNCHANGED, SET} (documented boundaries).
- H probe lines are prediction context only and are never learned from.
- The 3-variable worlds are minimal by design; scaling is future work.

## Governance

- This prereg is committed ALONE before any implementation file.
  Commit order self-check: the prereg commit strictly precedes the
  first causal3.zag commit.
- The apparatus (world3c/world3i/world3d.zag, baselines3.zag, frozen
  obs/probe logs, baseline verification) is committed after the prereg
  and before the learner. The worlds are environment code; they may
  contain the tested dynamics. The learner may not (K-CV7).
- Implementation, results, and verdict in separate commits.
- Results must include raw stdout, SHA-256 determinism checks, the
  K-CV7 grep output, and the K-CV8 regression outputs.
- Adversary/governance review by independent agents (not this
  researcher).
- No thresholds adjusted post-hoc. Any deviation is documented as an
  amendment with a new frozen commit, not a silent edit.
- Pure Zag. No Python anywhere in this experiment.
- No em dashes in loop documentation.
