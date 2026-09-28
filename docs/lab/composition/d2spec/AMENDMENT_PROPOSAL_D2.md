# D2 instrument spec — 3 items needing Micah's signature before D2 construction

**Status: PROPOSED 2026-09-27 — NOT ENACTED. Requires Micah's signature.**

## Background

Micah signed amendment A7 (2026-09-27), which gated D2 construction on a
written instrument spec held to the D1 bar. The spec is written:
`~/workspace/comp_b4/d2spec/D2_INSTRUMENT_SPEC.md` (grounded in the real
TIDELOCK sim, `docs/lab/invention/survival/src/world.zag` — every mechanism
cited to its source function).

The spec crew flagged 3 points where the spec necessarily goes beyond or
sits in tension with the frozen prereg as amended by A1–A7. These are
frozen-text changes, so they need Micah's word — the spec crew took no
position on them. Each item is independent: sign or decline each one.

---

### Item D2-1. D2 P2 scoring — checkable criteria instead of literal exact-match

**Plain English:** for text rules, "exact match" works — there's one right
answer string. For action sequences, many equally-good paths solve the same
scenario (different routes to the same mote, different foraging orders).
Demanding one exact action string would fail agents that genuinely solved it.
The spec scores each episode pass/fail against checkable criteria instead: a
ward placed before the storm, zero unmitigated storm ticks, enough motes
eaten, alive at the end. The do-nothing probe (P3) keeps literal exact-match
(the all-WAIT action string).

**Frozen text in tension:** §3 P2 (as amended by A3): "Exact-match scoring."

**The change:** for D2 only, P2 episodes are scored per-episode pass/fail
against the spec's verifiable semantic criteria (§6 of the spec), not against
a single reference action string. This is the frozen §1.3 definition of
correctness ("correct is defined by the parts' semantics composed per C's
structure") applied where literal exact-match is infeasible. D1 is
unaffected.

**Sign:** D2 gets a fair scoring rule and can be built. **Decline:** D2
stays unbuildable — no fair scoring rule for action sequences exists under
literal exact-match.

---

### Item D2-2. D2 K6 — scenario-novelty + trace-replay instead of bigrams

**Plain English:** D1's memorization check looks for shared two-letter
sequences between test inputs and training inputs. Action sequences have no
letters, so the mechanism is restated for D2: (1) every test scenario's
storm schedule, layout, and crystal set is verified absent from training by a
committed exact-comparison check (not asserted), and (2) the independent red
team must *fail* to explain any passed episode by replaying a training trace
or by mapping the scenario to the nearest training schedule and replaying
that trace. The teeth are identical: if the red team succeeds → battery VOID,
generator fixed.

**Frozen text in tension:** §7 K6 (as amended by A4): "success holds on
inputs sharing no bigram with any training input."

**The change:** for D2 only, K6 is adjudicated via the spec's committed
novelty checks (N1–N3) plus the red-team trace-replay / schedule-memorization
attacks (§9 of the spec). The bigram mechanism is declared not-applicable to
action sequences with this justification. D1's K6 is unaffected.

**Sign:** the memorization check works for D2. **Decline:** K6 cannot apply
to D2 as frozen.

---

### Item D2-3. D2 P4 — order templates instead of ordered part-pairs

**Plain English:** D1's interference check compares pair (i,j) against its
reverse (j,i) — e.g., forage-then-ward vs ward-then-forage. D2's three
sub-skills combine in *orders* (forage-first vs ward-first templates), so the
check compares order templates (FW vs WF accuracy) using the same 0.25/0.75
asymmetry numbers. The numbers don't move; only the unit being compared
changes, because D2's compositions are sequences, not pairs.

**Frozen text in tension:** §3 P4: per ordered-pair accuracy table;
(i,j) ≤0.25 while (j,i) ≥0.75 → (d).

**The change:** for D2 only, P4's unit is the order template (FW vs WF,
16 items), with the 0.25/0.75 numbers unchanged, adjudicated on the
retrieval-correct (*elig*) set, reclassifying only actual (c) items — per the
red-team 3b fixes wired into the spec. D1's P4 is unaffected.

**Sign:** order-asymmetric interference is testable in D2. **Decline:** P4
cannot apply to D2 as frozen.

---

## What happens next

- If all three are signed: they are enacted as dated amendments and the D2
  build crew is dispatched under the spec + amendments.
- If any is declined: the spec returns for rework on that point, or D2 drops
  the corresponding bar/instrument element (documented, not silent).
- The spec's 6 open questions (§12) are build-crew work, not signature items
  — except open question 1 (whether the dialogue learner can sustain 90–320
  tick per-tick episodes), which is the D2 line's biggest feasibility risk
  and will be the build crew's first spike.
