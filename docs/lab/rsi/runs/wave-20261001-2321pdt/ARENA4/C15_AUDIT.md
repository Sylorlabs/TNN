# C15 (goal) AUDIT (ARENA4, wave-20261001-2321pdt)

Question under audit: is C15 genuinely achievable by a general goal
mechanism, or is it broken/narrow by design like C9 was?

## What C15 is, as implemented

- One item (item 63), cap 15, question string "listnames"
  (sealed/world/turns.jsonl, turn 117; regenerated seed 71503461337030).
- Key (answer_key.json index 63):
  "Kavipe,Sehiru,Zovina,Datamo,Zovinu,Tetaru,Zosumo,Dagumo,Zofiru,Segunu"
  = the 10 world-gen entity names in internal index order e=0..9,
  comma-joined (world_gen.zag lines 632-639).
- v6 refreeze and ARENA2 REMAP both reply "UNKNOWN": C15 = 0.000.

## Scorer: NOT exact match, NOT ordering-fragile

The frozen scorer (competitive_arena/arena.zag, sha256
3899577bc0c15c77711621071c14fd2cd35eab60360dc1ca71a2c2e2038ce076,
matches the refreeze record) scores cap 15 as an order-insensitive
set F1 over comma-split names:

    if(cap==15){
      let ne:i32=split_csv(an,44,ea,12);
      let nr:i32=split_csv(rp,44,ra,12);
      let inter:i32=set_inter(ea,ne,ra,nr);
      if(ne+nr>0){sc=2000*inter/(ne+nr);}
    }

So a reply listing any subset of the 10 names in ANY order gets
partial credit. The ARENA2 lane's rejection reason "ordering-fragile"
is factually incorrect: order does not matter to the scorer.

## Exposure coverage: 9 of 10 entities observable

In the sealed world (refreeze/sealed/run1/world/exposure.jsonl):
- 9 distinct entity names appear in exposure turns (fact and relation
  events). First-appearance order:
  Kavipe Sehiru Zovina Datamo Zovinu Tetaru Zosumo Dagumo Zofiru
- "Segunu" (entity index 9) occurs 0 times in exposure.jsonl: no fact
  turn, no relation turn. It is named only in briefing_tnn.jsonl,
  a static world-gen artifact.

Consequence: a purely experience-based entity roster holds 9 names and
scores 2000*9/(10+9) = 947, i.e. 0.947, in any order. The honest
experience-based answer is 0.947, not 0. The 10th point requires
reading the briefing file.

## Comparison with C9 (the broken-by-design case)

- C9: the only 3/3 mechanism is question-format parsing (true chain
  always listed first), zero experience, zero learned structure.
  The honest causal answer (UNKNOWN) scores 0. Game-only. Correctly
  rejected.
- C15: the passing mechanism is an entity roster built from exposure
  experience and enumerated to satisfy the stated goal. The honest
  experience-based answer scores 0.947 under the frozen scorer.
  Achievable by a general mechanism. NOT game-only.

## Verdict of the audit

C15 is genuinely achievable by a general goal mechanism: maintain a
persistent entity roster in learner state from exposure events, and
enumerate it when the listnames goal is posed. This uses learned
state, no sealed values, no briefing exploit, no format trick. The
ARENA2 rejection is not sustained: its "ordering-fragile" premise is
refuted by the scorer source, and its "narrow enumeration" concern is
answered by the fact that the enumeration operates over
learner-owned experience state, the same pattern the v6 base already
uses for fact/hop2/conflict/zem question handlers.

Two honest limitations are recorded, not hidden:
1. n=1 with a graded scorer. Information gain is modest but real:
   the item discriminates UNKNOWN (0.000), partial roster, and full
   roster. Kill bar is set at >= 0.900, below the honest 0.947
   ceiling, so the bar does not demand the briefing-provided 10th name.
2. The prereg spec (ARENA_PREREG.md) describes C15 as "autonomous goal
   completion (2 goals)" with tools and an action-trace predicate;
   the implemented battery has a single listnames probe. The lane
   builds to the implemented item and notes the spec divergence;
   the mechanism (roster maintenance + goal enumeration) is the
   general capability the probe can actually test.

## Battery notes for the future (not blocking)

- If C15 is meant to test autonomous goal pursuit, implement the
  prereg spec: goal turns with tools, order-insensitive set scoring
  (already the scorer), multiple goal items, all target entities
  discoverable through interaction.
- The sealed-record counts used here are 16 capabilities, 68 items.
  Sibling lane parent tasks said "15 capabilities"; the sealed
  records (battery.json, refreeze REFREEZE_RECORD.md, ARENA2/ARENA3
  per-capability tables) show 16. The sealed records govern.

## Toolchain

Audit performed with safebin PATH only (grep, sed, awk, wc on
committed sources and sealed records). No Python. No source edits.
