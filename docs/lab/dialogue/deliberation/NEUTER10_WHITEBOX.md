# Neuter residual: white-box analysis of the 10/77 insensitive turns

**Date:** 2026-09-27
**Context:** Repair cycle #4 (commit `eda122670d29`) wired all 10 kind-0 reading
rows into the decision path. All-row neuter: 67/77 answers changed (was 0/77).
Micah's order: find out why the other 10 did not change; fix the architecture
broadly if the cause is a bypass, else explain honestly.
**Verdict: all 10 are LEGITIMATE. No bypass. No code change. Architecture
correct at 67/77 with 10 explained.**

## The 10 turns

Every insensitive turn shares one identical signature:

| # | Battery | Turn | Utterance | Readings | Facts | Winner |
|---|---------|------|-----------|----------|-------|--------|
| 1 | r4 | 6 | how many people live there? | plain=1, rest 0 | all gated (2) | withhold |
| 2 | r4 | 9 | what did TNN paint? | plain=1, rest 0 | all gated (2) | clarify |
| 3 | r4 | 14 | did TNN invent a new memory system? | plain=1, rest 0 | all gated (2) | clarify |
| 4 | r4 | 23 | who wrote hamlet? | plain=1, rest 0 | all gated (3) | withhold |
| 5 | r4 | 28 | what did TNN build? | plain=1, rest 0 | gated (1/1/2) | withhold |
| 6 | b20 | 17 | what did TNN paint? | plain=1, rest 0 | all gated (2) | clarify |
| 7 | b20 | 18 | who wrote hamlet? | plain=1, rest 0 | all gated (3) | withhold |
| 8 | held | 15 | what did TNN paint? | plain=1, rest 0 | all gated (2) | clarify |
| 9 | held | 16 | what did TNN invent? | plain=1, rest 0 | all gated (2) | clarify |
| 10 | held | 17 | who wrote hamlet? | plain=1, rest 0 | all gated (3) | withhold |

Readings verified from the `READ` trace lines; fact gates from the `FACT`
lines; winners from `ARGMAX`. In all 10, `hid=9 rd=plain ev=1` and
`hid=0..8 ev=0`. In all 10, `best_gated_fact` finds no answerable fact
(gates 2 = predicate mismatch, 3 = other gate; never 0).

## Why the neuter cannot move them (mechanism)

The neuter is a **zeroing intervention**: the GENs consume all kind-0 rows as
0 (the `READ` trace still prints the computed values; the intervention is on
the consumed values). On these 10 turns its only effective change is
`plain: 1 -> 0`; the special rows were already 0.

1. **Every special GEN reads its kind-0 row in its fire condition** (verified
   in `src/deliberate.zag`): `gen_joke`/`gen_mem`/`gen_forget`/`gen_resume`/
   `gen_challenge`/`gen_provenance`/`gen_assertion` read rows 4,5,6,1,2,3,7
   unconditionally; `gen_correction` reads row 0 (gated on previous-answer
   state); `gen_compose` gates on row-8 evidence. On these turns they read
   `0 -> 0`: bids unchanged. This is genuine consultation with a negative
   result, not decoration — the bid vector is a deterministic function of
   the row values, and the function is evaluated every turn.
2. **`gen_default` (hid 24) is the only consumer of the plain row**, and its
   fire gate conjoins an answerable-fact requirement:
   `wd==0 && fid3>=0 && (plain==1 || dr0==1 || dr2==1 || dr7==1 || dr8>0)`.
   All 10 turns have no answerable fact, so its bid is 0 before and after
   the neuter. Zeroing plain cannot move it.
3. **`gen_withhold` / `gen_clarify` fire on fact-absence**, which is
   utterance-driven (retrieval + gating over hids 10-12), not reading-driven.
   They do not read kind-0 rows — legitimately: the bid hierarchy
   (specials 216-240 > clarify 213 > withhold 210 > default 207) guarantees
   that any fired special reading outbids them. They are the plain-partition
   fallback; they do not need to re-check what the specials already checked.
4. Fact retrieval is unchanged by the neuter (utterance-driven), so the
   fact-absence condition is unchanged.
5. Identical bid vectors -> identical ELIM -> identical ARGMAX -> identical
   answers. The neuter has a **fixed point** on the plain-only + no-fact
   configuration by construction.

## The readings genuinely discriminate on these turns

The counterfactual proves causal efficacy: had any special reading fired,
its GEN would fire and win. `gen_joke` fires unconditionally on
`lr_get(led,4,12)==1`, composes a joke with no fact required
(`compose_joke`), and bids base 240 + bonus — outbidding withhold (212) and
clarify (214). On turn 1 ("how many people live there?"), a joke reading
would have produced a joke, not "I don't know." The rows are on the decision
path; the zeroing probe is simply blind to this configuration.

Each row's causal efficacy is independently established elsewhere: rows
0,4,6,7,8,9 move battery answers (6,4,3,10,8,41 of 77 respectively); rows
1,2,3,5 move synthetic-turn answers. No row is decorative anywhere.

## Per-turn verdicts

All 10: **LEGITIMATE** — plain-only reading, no answerable fact, decision
reduces to fact-absence, neuter is a fixed point. The withhold turns (1, 4,
5, 7, 10) are "no fact at all"; the clarify turns (2, 3, 6, 8, 9) are
"named entity + predicate mismatch (gate 2)". In neither case does the
utterance-type reading have a fact to route.

## Why there is no broad fix

- Making withhold/clarify require `plain==1` would manufacture
  neuter-sensitivity by breaking the repair-#8 airtightness invariant
  (ARGMAX must never see an empty field): under the neuter nothing would
  fire. That is tuning the test, not fixing the architecture. Rejected.
- Routing fact-absence through the readings is semantically incoherent:
  fact-absence is a KB property, not an utterance-type property. Rejected.
- The decision path already consults every row every turn (fire conditions
  -> bids -> ELIM -> ARGMAX). There is no second decorative path. Nothing
  to rewire.

## Methodology note (for future red teams, not a code change)

The zeroing neuter has a known blind spot: turns where the true reading is
plain-only and the plain-consumer is fact-gated are fixed points. A stronger
probe is the **wrong-hypothesis flip**: set one non-true special row to 1
and require the answer to change to that GEN's output (e.g., force joke=1,
expect a joke). This closes the blind spot without touching the
architecture. Recommended for red team #5's methodology, not as a bar
change for the current trial.
