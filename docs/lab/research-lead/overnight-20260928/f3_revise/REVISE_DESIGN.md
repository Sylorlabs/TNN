# REVISE Design: goal-failure-driven revision without world-identity gating

Status: DESIGN-COMPLETE. Design only; no implementation in this commit.
Parent findings: F3 attack RESULT_F3ATTACK.md (commit 531e6069e, verdict F3-ATTACK-KILLS).
Surviving mechanism: trial-driven OP-GROW via F3_grow_search with
condition (b), ablation-proven necessary (H-ABL rejected).
Killed mechanism: goal-failure OP-GROW gated on world-name detection
(H-NAME confirmed).

## 1. The defect to remove

In frozen learner f3_p3.zag (f3_phase3/, commit 41ed1ef9a):

1. Lines ~921-930: `w_worldname()` first byte read into
   `is_conj_w` / `is_neg_w`; these flags select which
   world-specific P-PROP check runs.
2. Lines ~1235-1244: `w_worldname()` first byte read again into
   `is_conj_world` / `is_neg_world`.
3. Line ~1295: `if(is_neg_world==1 && attempt==1)` gates the
   goal-failure OP-GROW. The refutation evidence (goal execution
   state) and the search call were generic; only the decision to
   run was world-specific.
4. Verdict block: `world_pass` computed from the name flags plus
   world-specific literal checks (has_conj / has_neg).

The prereg (97287f87c sections 2 and 7) described the goal-failure
GROW as a general mechanism and a simplified precursor of
Phase 7 REVISE. Neither section disclosed world-name gating.
The rename test (world_tneg_renamed.zag, one-line name change)
proved the behavior appears if and only if the learner
recognizes the name. The defect is therefore not a small
oversight but a control-flow dependency on world identity.

## 2. Design goal

REVISE: a goal-failure revision operator with these properties.

- The trigger is a function of the learner's own outcome state
  only: the goal was not met.
- The evidence is the failed execution trace, used as a
  refutation observation for the same generic F3_grow_search
  that survives ablation.
- The decision to grow, replan, or stop is made by generic
  conditions (search success, attempt budget, cost bound).
- No branch, flag, or data value in the learner depends on the
  world's identity string or on which sealed world is running.
- A world rename must produce byte-identical learner behavior
  (the H-NAME test becomes a standing falsifier).

## 3. Non-goals

- This design does not claim L3 or general causal learning.
  It is bounded L2 infrastructure: the rule slots, the search
  space, and the growth operators remain researcher-supplied;
  what is generic is the decision to revise after failure.
- This design does not revive the F3 Phase 3 BUILD-PASS. Any
  T-NEG-class claim requires a new frozen prereg, a new sealed
  re-run, and a new independent adversary.
- This design does not specify the sealed worlds for the
  re-run. World construction stays with an independent
  adversary under a future prereg.

## 4. REVISE mechanism

### D1. Trigger (generic)

After each goal attempt, the learner reads `w_goal_met(gvals)`.
Let `attempt` count attempts starting at 1 and let ATTEMPT_MAX
be a frozen constant (recommended: 3, so a failed second
attempt can also revise; the exact value is frozen by the
future prereg, not here).

```
revise fires iff (goal_ok == 0) AND (attempt < ATTEMPT_MAX)
```

No other condition. In particular: no world flag, no attempt-1
restriction tied to a specific world, no check of which
literals already exist beyond what the search itself needs.
If the goal is met on any attempt, no revision runs (this
preserves the T-CONJ behavior where attempt 1 succeeds).

### D2. Refutation evidence (generic)

The workspace state `ws` after the failed plan execution is
snapshotted at `t_goal` exactly as the killed code did. This
snapshot is the refutation observation: it is a concrete
counterexample to the rule set that produced the failed plan.
The evidence passed to the search is:

- the failing rule window from `rs`,
- the variable index `yv`,
- the post-failure state `ws` and snapshot time `t_goal`,
- the existing trace buffers.

Nothing about the world's name or intended answer enters here.

### D3. Growth gate (generic, ablation-backed)

For each Y rule with fewer than 3 literals, run the unchanged
`F3_grow_search` including condition (b): a candidate literal is
accepted only if it is true on all true positives of the rule
(the condition H-ABL proved causally necessary; its removal
grows contradictory garbage on both sealed worlds).

- If at least one literal is accepted, set `grew=1` and record
  the grown literal(s) in the trace.
- If none is accepted, emit REVISE_EXHAUSTED and terminate the
  episode as an honest fail. A failed search is information,
  not a crash.

The growth gate decides by search outcome, not by world.

### D4. Replan loop (generic, bounded)

If `grew==1`: rebuild the hypothesis from the grown rule set,
replan, execute, and re-check the goal. Each attempt increments
the NEXPS cost counter, so unbounded replanning is impossible
under the frozen cost bound. The loop is the same code for
every world; worlds differ only in what the search finds.

### D5. World-name ban (audit rule M-REVISE1)

No learner function may call `w_worldname()` in a position
that influences control flow or decision data. Concretely:

- All existing call sites that feed `is_conj_w`, `is_neg_w`,
  `is_conj_world`, `is_neg_world` are deleted.
- Recommended: delete every `w_worldname()` call site in
  learner source. If a harness log line wants the world name,
  the harness (not the learner) emits it.
- Audit M-REVISE1: the token `w_worldname` occurs zero times
  in learner source outside comments. A builder may not
  narrow this audit. Any occurrence in code voids the
  no-gating claim for that build.

This is a textual, third-party-runnable check, in the style
of the L3 bridge M1-M4 audit.

### D6. World-agnostic verdict

The learner no longer computes world-specific pass criteria.
It emits:

- `goal_ok` (goal achieved within the attempt budget),
- the full grown rule set in a machine-readable trace,
- `cost_ok` (NEXPS within bound),
- determinism markers.

World-specific answer checks (the old has_conj / has_neg
literal-pair tests) move to the sealed harness: the harness
compares the emitted rule set against the sealed world's
truth table. The learner must not contain the expected answer
in any form. This removes the second place where world
identity leaked into the learner (the verdict block).

## 5. Why this is general

Under REVISE, the T-NEG sealed run and the renamed-world run
execute identical code paths: attempt 1 fails the goal,
D1 fires, D2 builds the refutation observation, D3 runs the
search, D4 replans. Whether the search finds `!Z@1` depends
only on the evidence and condition (b), not on a name flag.
A world where the first plan succeeds never revises. A world
where no fixing literal exists terminates honestly at
REVISE_EXHAUSTED. The mechanism's behavior is a function of
(observations, search outcome, budgets), never of identity.

## 6. Standing falsifiers for the future builder

The future prereg must freeze at least these falsifiers:

- F-RNAME (H-NAME regression): take any sealed world, change
  only its name string, run the frozen learner 3 times.
  Every emitted line except a harness-side name echo must be
  byte-identical to the sealed run. Any divergence fires
  F-RNAME and kills the build.
- F-RABLN (H-ABL regression): the condition-(b) ablation must
  fail on the sealed worlds, as in the attack. If the
  ablated learner passes, the condition is decorative and
  the mechanism claim is void.
- F-RNAMEAUDIT: M-REVISE1 passes on committed learner source.
- F-RCOST: NEXPS within the frozen bound.
- F-RDET: 3/3 byte-identical runs, zero stderr, pure Zag.

## 7. Relation to the wider program

Revision after counterexample is criterion 12 of the 12 L3
criteria: a claimed invention must be revisable after a
counterexample. The killed F3 code pretended to satisfy this
with a world-specific script. REVISE is the honest precursor:
a generic loop that takes a failed outcome, treats it as
refutation evidence, grows the rule set through the
ablation-backed search, and replans under a budget. It does
not by itself satisfy criterion 12 (that requires an actual
invention claim under test), but it removes the dishonest
version and supplies the machinery a future claim would need.

## 8. Notes for the future builder (not implementation)

Expected diff scope against f3_p3.zag:

- Delete the two world-detection blocks and all four flags.
- Replace the gated `if(is_neg_world==1 && attempt==1)` with
  the D1 trigger and the D3/D4 loop.
- Replace the world-specific verdict block with the D6
  emission block.
- Keep F3_grow_search and condition (b) byte-identical to the
  ablation-tested version; any change there re-opens H-ABL.

No source files, binaries, or run logs are part of this
design commit. The builder's prereg must precede any code.

## 9. Kill bars for this design

- K1 (design complete): this document specifies trigger,
  evidence, growth gate, replan loop, world-name ban with
  audit, world-agnostic verdict, standing falsifiers, honest
  scope, and builder notes. PASS.
- K2 (no world-name gating): the design deletes every
  name-dependent branch and adds M-REVISE1, a textual audit
  that forbids `w_worldname` in learner code. No section of
  this design branches on world identity. PASS.
- K3 (no implementation): no .zag written or modified, no
  binaries, no evaluation runs. Zero Python used. No em or
  en dash bytes in this document (shell byte check before
  commit). PASS.

Verdict: REVISE-DESIGN-COMPLETE.
