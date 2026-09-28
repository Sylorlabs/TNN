# Why tables and static graphs fail as intelligence substrate

Agent H, 2026-09-19. Program law (Micah): *intelligence is not a table and
not a static graph. The 2×2 score table — and any N×N scaling of it — is a
toy. We are making AI, not a toy machine.*

## 1. What the table is, precisely

The R34 v3 learner core is a 2×2 score table: `score[context][object]`,
updated by `score += reward*100` (clamped ±30000), with decisions by
`argmax` over the active context's row and a switch rule: *one negative
reward on a positively-scored cell (no exploration) → change regime*.

This is not a simplification of intelligence. It is a different kind of
thing. Three structural reasons:

### 1a. A table cannot hesitate

Every decision a table makes is a single function evaluation: `argmax`,
lookup, threshold. There is no intermediate state in which the system
holds a hypothesis *doubtfully* — no "I think the regime changed but I'm
not sure yet." The LH-5 mechanism section proves the cost: the switch
rule treats every negative credit as a regime-change signal, so at 10%
reward corruption the switches explode 19→181 and whole probe blocks
collapse to 0/16. A table's decision step has no capacity for
corroboration, because corroboration requires *withholding* commitment
across multiple observations — and a table has nowhere to withhold it.
The accumulator is a number; the decision is a function of the number.
There is no room between them for doubt.

### 1b. Scaling the table changes nothing about the decision

N×N for larger N is still `argmax` over a row. LH-6 (4×4 scale-up) was
correctly blocked: the fragility lives in the *decision procedure*, not
the table's size. A bigger table fails the same way, with more cells.
"Progress" by table enlargement is motion without movement — which is why
Micah bans it as progress outright.

### 1c. The table's "learning" has no reason attached

A score update is a state change with no audit trail of *why*. `s01` went
from 1500 to 1400 — because of what, exactly? Which observation, weighed
how, against what alternative? The update rule is fixed and reflexive;
the number carries no provenance. Contrast R27's `Trace` objects:
symbolic op sequences over cue vectors with `provenance='SELF_VERIFIED'`,
support, source ids, age. A trace is *evidence with a history*. A table
cell is a number with amnesia.

## 2. Why static graphs fail too

R27 contains real graphs (`MultiViewEntityGraph`, `EntityEventGraph` with
`nodes/alias/merge_history`). They are *memory* — relational storage —
not decision machinery. A graph answers "what is connected to what." It
does not answer "should I commit to this hypothesis." Graph traversal is
as reflexive as table lookup: follow the edges, take the max-weight path.
Put a decision procedure on top of a static graph and you get the same
disease as the table — one function evaluation, no doubt, no refusal —
with extra steps. Graphs are where knowledge *rests*. Intelligence is
what happens *between* observations and commitment, and neither tables
nor static graphs have a between.

## 3. What R27 does instead (the native lead)

The canonical brain's learning is not tabular anywhere that matters:

- **58 structural revision decisions**, each shaped
  `diagnosis → proposal → base/candidate accuracy → compute multiplier →
  PROMOTE or rollback`. This is a *deliberative decision procedure*:
  a hypothesis is named, a candidate is measured against a base, and the
  system commits or refuses. Every promotion carries its reason.
- **435 Trace objects**: verified symbolic operation-sequences over cue
  vectors — evidence, not scores. Operations, not gradients (STATE_SCHEMA
  §5, negative specs N3/N4).
- **Fast/slow two-speed memory** (`ProtectedSkillMemory`): retention with
  different timescales, managed structurally.
- **Zero optimizer state, zero gradient payloads** anywhere in 121,094
  nodes (N1/N2). The brain never did gradient descent; there is nothing
  to "go back to."

The shape to copy is the *revision decision*, not any data structure:
**propose → measure → commit-or-refuse, with the reason recorded.**
That is what the CTX mechanism (CTX_DESIGN.md) miniaturizes for context
management.

## 4. The precise claim (falsifiable, not poetic)

Any finite mechanism can be *described* as a table — that is just
computability, and it is not the claim. The claim is about the **decision
procedure**:

> A substrate whose decision step is a single reflexive function
> evaluation (argmax, lookup, threshold, max-weight traversal) — with no
> intermediate state representing doubt, no corroboration requirement,
> and no refusal path — cannot implement context management that
> survives unpredictable change, because unpredictable change is exactly
> the case where the first sample is misleading.

LH-5 is the existence proof of the failure. HT1 (PREREG_HT1.md) is the
test of the replacement: a mechanism whose switch is a deliberate,
verified, refusable operation must survive the randomized curriculum +
noise that breaks the table.

## 5. What "post-table" does NOT mean

- It does not mean "no arrays in memory." Partitions are stored in
  arrays. The difference is procedural, not representational.
- It does not mean "no numbers." Recorded probe evidence is numeric.
  The difference: evidence is *recorded observations*, never
  *accumulated value* — there is no update rule, no `+=`, no argmax.
- It does not mean the toy was useless. The toy proved long-horizon
  stability (LH-1..LH-4), found the exact fragility address (LH-5), and
  gave us the head-to-head baseline. Toys are scaffolding. The law is
  that you don't live in the scaffolding.

## ⚠️ Contamination note — 2026-09-20 (R34 hidden-randomness remediation)

This document references the "LH-5 signature" (switch-storm / fragility
pattern). The quantitative LH-5 claims (0%→10% corruption knee, regime
switches 19→181) are **QUARANTINED** — LH-5 trained with
`explore_enabled=1`, engaging the hidden seeded LCG in `r34v3_choose`
(r34 RNG probe, workstream 2/8, commits `072f25aa` / `4976cbf5` on branch
`tnn-native-lab`; Micah's ruling: REMEDIATE). The *phenomenon* referenced here
was independently reproduced under explore-disabled conditions (the HT1/HT2
toy arms showed the same 357-switch storm, collapsed blocks, and 0/16 regime
destruction with exploration off), so the pattern-level reference remains
descriptively valid; only the tainted quantitative claims are suspended.
The original text above is left intact for the record.
