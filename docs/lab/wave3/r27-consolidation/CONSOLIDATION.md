# Consolidation — what R27's ProtectedSkillMemory is, and what deliberate consolidation adds

**Slug:** r27-consolidation · **Date:** 2026-09-19/20 · **Agent:** Wave-3 investigator

## 1. What ProtectedSkillMemory fast/slow ACTUALLY does in the R27 state

Source: the accepted-state schema map (`brain/STATE_SCHEMA.md` §7), via the
restricted-unpickle stub census. What is verifiable from the artifact:

- `ProtectedSkillMemory` is one of eight structural memory components on
  `r15_master_training.MutableStudent`. Its keys: `fast`, `slow`, `step`,
  `history`, `gram_counts`.
- `fast`/`slow` are **tiers of skill items**, not two copies of one value.
  The learning atom elsewhere in the state is the `Trace`: a verified
  *symbolic op-sequence* (`(('FILTER_GT','PARAM'),('MAP_MUL',2))`) over a
  512-dim cue, with `support`, `sources`, `age`, `provenance='SELF_VERIFIED'`.
  The skill tiers hold items of this kind — structures with provenance —
  while `step` counts development steps and `history` is an audit trail.
- `gram_counts` suggests frequency statistics over substructures (n-grams of
  ops/skills), i.e. the memory tracks *compositional reuse*, not scalar values.

What is **not** in the artifact: the transfer rule. No key records *when* or
*why* an item moves fast→slow. The memory survey (`wave2/memoryagency/`)
establishes the agency status honestly: both tiers were written by the
training harness during development and read by skills — consolidation
happened *to* the system; the system never decided. There is no PIN/KILL/
DEMOTE API, no record of a promotion decision. **The schema gives the
structure (tiers + audit); the policy is undocumented.** Any claim to have
"replicated R27's consolidation rule" would be fabrication. This trial does
not make that claim: it builds the missing policy natively, *inspired by*
the structure.

## 2. The precise difference from the rejected P2 two-speed tables

P2 (`wave2/ruleslab`, trialed 2026-09-19, systematic negative 3/3 seeds) was:

- two exponential moving averages **over the same decision scores** —
  a fast table and a slow table holding the *same kind of number*,
  blended at decision time;
- updated by **automatic decay** (25%-per-8-episode fast decay) on every
  experience — a smoothing device on the decision variable;
- the failure mode was **acquisition drag**: the slow table extended the
  tie-break phase by ~3–4 episodes per regime and the decay taxed fresh
  learning. Two-speed *smoothing* of a value is not consolidation.

R27's structure is a different kind of thing:

| | P2 two-speed | R27 fast/slow |
|---|---|---|
| Unit | a score (scalar per cell) | a skill *item* (symbolic structure + provenance) |
| Relation between tiers | two estimates of one value | working set vs protected store |
| Transfer | continuous blending/decay | discrete promotion of items (unrecorded rule) |
| Audit | none | `history` key exists |
| Agency | n/a (automatic by construction) | absent — harness-owned (the gap this trial fills) |

Conflating them is the exact error the brief warned against. Nothing in
this trial reuses P2's mechanism; the only shared word is "two-speed",
and it refers to different ontologies.

## 3. The native mechanism: deliberate consolidation (`impl/psm.zag`)

Built to answer the schema's open question — *what should the promotion
policy be if the system itself decides?* — under Micah's law: zero RNG in
the system (no random exploration, no stochastic tie-breaks; every tie
breaks by lowest index), no score tables, no RL reward-shaping, no N×N
scale-ups. Skills are structural items `(id, op, param)`; the world emits
observations with verifier verdicts (`verified=1/0`, the R27
`SELF_VERIFIED` analogue — the system receives verdicts, it is never
credited with the verifier's knowledge).

**Deliberate arm** — event-driven, no timers, every op audited:
- `CONSOLIDATE`: fires on the touched candidate the moment it reaches
  `ver ≥ 6` **across ≥ 2 distinct verified contexts** (cross-context
  corroboration — a judgment about evidence quality, not an exposure reflex).
  Slow-tier id conflicts keep the existing skill (first-verified-wins);
  slow-full defers with a history record (never silent eviction).
- `CONDEMN`: fires when a candidate is discredited — never verified,
  `unv ≥ 8`, `age ≥ 8`. The slot becomes a tombstone: signature and
  discredit retained, still matchable, reusable.
- `PREEMPT`: when fast is full and a new observation needs a slot, the
  system *chooses* the most-discredited never-verified tombstone as victim
  (lowest-index tie-break) and records `DISCARD reason=PREEMPTED`.
- `REVIVE`: a condemned form that later verifies is restored (integrity
  path; unreached by design, present so the audit works both ways).

**Automatic arm** (harness-style baseline): scan every 10 episodes, promote
on raw exposure `(ver+unv) ≥ 6`; last-wins slow overwrite; lowest-confidence
slow eviction; no condemn, no preemption; fast-full drops observations.

Scale design: every op is an `O(N_FAST)` scan or `O(1)`; memory is
`O(N_FAST + N_SLOW + N_HIST)`; integer arithmetic only; thresholds are
scale-free (identical constants at 1× and 4×).

## 4. Verdict on the question: is there a structural consolidation mechanism worth keeping?

**Yes — POSITIVE.** The trial (preregistered falsification criteria in
`PREREG.md`, all met) shows the mechanism is real, non-tabular, and load-
bearing:

- **Purity:** deliberate slow-tier purity 1.0 (zero wrong answers, zero
  never-verified skills consolidated) on all three curricula; automatic
  polluted on all three (16/6/64 spurious skills resident in slow).
- **No recall cost:** deliberate `correct` ≥ automatic everywhere
  (80 vs 32/56; 320 vs 128 at 4×) — the corroboration gate blocks noise,
  never true skills.
- **The audit trail shows the decisions working:** C1 deliberate
  consolidated true skills at their 6th verified observation (steps 81–88),
  condemned 8 impostors + 8 fabrications mid-burst (steps 377–384,
  569–576), and fired exactly 4 PREEMPTs at the late-skill pressure points
  (steps 609/649/689/729). C3 shows the corroboration gate delaying a
  consolidation from step 2438 to 2453 until the second context corroborated —
  the deliberate judgment, visible as a number.
- **Scale:** the 4× curriculum (80 skills, 128 slots, 3392 episodes)
  completes with identical constants and a wider deliberate advantage.

What was *kept* from R27 is structural: tiers of items, promotion as a
discrete audited op, an append-only history. What was *added* is the agency
R27 lacks: the system deciding what, when, and what to discard. The
mechanism worth keeping is not "two-speed memory" — it is **corroborated,
audited promotion with deliberate discard**: consolidate on cross-context
verification, condemn the discredited, choose victims under pressure, write
down every decision.

## 5. Honest limitations

1. R27's actual transfer rule is undocumented — this is policy design
   inspired by the schema's structure, not a replication.
2. Verifier verdicts come from the world; the trial tests the consolidation
   policy, not how verification is earned. A closed loop (the system earning
   its own verdicts, R27 `SELF_VERIFIED` literally) is future work.
3. No DEMOTE-from-slow: slow-full only defers at these scales. The explicit
   next scale test is 20× *with* slow-tier pressure to force a DEMOTE policy.
4. The probe's highest-confidence read rule is harness-side, identical
   across arms — not part of the mechanism.
