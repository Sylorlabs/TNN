# Simpler-Explanation Attacks on Generic-Capability Mechanisms

Date: 2026-09-30 UTC
Attacker: A2 (Simpler-Explanation / OOD Adversary)
Targets: C4 Composition and C8 Inquiry (the two GENERIC-CAPABILITY mechanisms)
Method: Analysis + reasoning about baselines. No new code required for
these attacks; the mechanisms' properties are verifiable from source.

## Attack 1: C4 Composition vs Memorization Baseline

### The memorization baseline

A pure memorization baseline for C4 would:

1. During training: enumerate all 2-hop paths from the 6 taught
   relations. For each (a,r1,b) and (b,r2,c), store (a,r1,r2)->c
   in a table.
2. At test: on `hop2|S|R1|R2`, lookup (S,R1,R2) in the table.

This baseline would score 4/4 on the C4 test items. It requires no
relation store, no `learn_rel`, no on-demand composition.

### Why the C4 mechanism is not this baseline

The C4 mechanism (devint1_contestant_v3.zag):

1. **Learns relations incrementally:** `learn_rel` is called on each
   `t:"r"` exposure. It feeds "a r b" through `lex_feed` (lexicon),
   `conc_touch` (concepts), `rule_touch` (rules), then `rel_store`.
   The relation is integrated into the generic DEVINT1 learning path,
   not just stored in a lookup table.

2. **Composes on demand:** On `hop2|S|R1|R2`, it calls
   `rel_get(S,R1)->mid` then `rel_get(mid,R2)->answer`. It does NOT
   precompute 2-hop paths. The composition happens at query time.

3. **Generalizes to new relations:** The relation store has 64 slots.
   If a 7th relation were taught via exposure, `learn_rel` would store
   it (rel_n would become 7). A subsequent `hop2` query using the new
   relation would work immediately, without re-enumeration. The
   memorization baseline would need to re-enumerate all paths.

### Verification from source

- `rel_n` grows 0->6 during exposures (ARENA_COMPOSITION_REPORT.md).
  This confirms incremental learning, not precomputation.
- K8 check: "all 6 taught relations stored, rel_n=6." The mechanism
  learns exactly what was taught, no more, no less.
- The `hop2` handler does two sequential `rel_get` calls. There is no
  2-hop table. The composition is on-demand.

### OOD bounds (where it breaks)

- **3-hop queries:** The mechanism would fail. It only chains two
  `rel_get` calls. This is an honest bound, documented in the report
  ("2-hop only, not n-hop").
- **Fuzzy matching:** The mechanism uses exact match (`rel_get`
  requires exact entity/relation strings). It would fail on
  paraphrased relations. Honest bound ("exact match only").
- **New relation formats:** If relations were taught in a different
  exposure format (not `t:"r"`), `learn_rel` would not trigger. The
  learning is tied to the exposure format, but the storage and
  lookup are generic.

### Verdict on Attack 1

**SURVIVES.** The C4 mechanism is genuinely compositional, not a
memorization table. It learns relations incrementally through the
generic learning path and composes them on demand. The memorization
baseline would achieve the same test score but would not generalize
to new relations without re-enumeration. The mechanism's bounds
(2-hop, exact match) are honest and documented.

---

## Attack 2: C8 Inquiry vs Null Baseline (Do Nothing)

### The null baseline

The null baseline for C8 is what v4 did: on `fact|` lookup failure,
return "UNKNOWN" with no observe request. On `observe_result`, do
nothing (just tick).

This baseline scores 0/4 on C8. It does not request information and
does not learn.

### Why the C8 mechanism is not the null baseline

The C8 mechanism (devint1_contestant_v5.zag):

1. **Actively requests:** On lookup failure, `want_observe=1` is set,
   and the reply JSON includes `"observe":[{"e":"...","a":"..."}]`.
   This is not passive failure; it is an explicit request for the
   missing fact, using the question's own entity/attr fields.

2. **Genuinely learns:** On `observe_result`, the handler parses e/a/v
   from the vals array and calls `learn_fact` (the standard DEVINT1
   path: lexicon, concepts, rule, fact store). This is not a bypass;
   it goes through generic learning.

3. **Demonstrates the loop:** Evidence from run 1: Item 64 ask ->
   "UNKNOWN" + observe request for (Tetaru, material); re-ask ->
   "wooden" (correct). `fact_n` grows 9->13 as the 4 oracle facts are
   learned. The system acquires new knowledge through the inquiry
   loop and uses it.

### Simpler heuristic check

Is there a simpler heuristic than "on gap, request and learn"?

- "On gap, return UNKNOWN": This is the null baseline. Scores 0/4.
  The C8 mechanism does strictly more.
- "On gap, guess randomly": Would not score 4/4. The mechanism
  learns the correct fact and answers correctly.
- "Hardcode the 4 answers": K7 check confirms zero test entity/attr
  names in implementation. The mechanism is general, not hardcoded.

There is no simpler heuristic that achieves 4/4. The mechanism's
behavior (detect gap -> request -> learn -> answer) is the minimal
genuine inquiry loop.

### OOD bounds (where it breaks)

- **No oracle:** If the world does not provide the fact on observe,
  the mechanism would fail. It assumes the observation contains the
  answer. It does not search, experiment, or infer the fact.
- **Multiple gaps:** The mechanism handles one fact per query. If a
  query required multiple missing facts, it would need multiple
  rounds. The current code does one observe request per failed lookup.
- **When not to ask:** The mechanism always asks on gap. It does not
  decide whether asking is worthwhile (cost/benefit), nor does it
  prioritize among multiple gaps. Honest bound from the report: "does
  not plan multi-step information gathering, prioritize among gaps,
  or decide when not to ask."
- **Non-fact gaps:** The mechanism only handles `fact|` lookup
  failures. If the gap were a missing relation, procedure, or causal
  model, it would not request appropriately.

### Verdict on Attack 2

**SURVIVES.** The C8 mechanism is a genuine (if minimal) active
inquiry loop. It detects knowledge gaps, explicitly requests missing
information, learns through the generic path, and uses the learned
fact. The null baseline scores 0/4; the mechanism scores 4/4. There
is no simpler heuristic that works. Bounds are honest and documented.

---

## Summary

| Mechanism | Attack | Result |
|-----------|--------|--------|
| C4 Composition | Memorization baseline | SURVIVES. Compositional, not precomputed. Generalizes to new relations. |
| C8 Inquiry | Null baseline / simpler heuristic | SURVIVES. Genuine inquiry loop. No simpler heuristic works. |

Both GENERIC-CAPABILITY mechanisms survive simpler-explanation
attacks. Their bounds are honest and documented. They represent real
(but minimal) cognitive capabilities.

The ARENA-ADAPTER mechanisms (C6, C9) were not attacked here because
they do not claim to be generic capabilities. They are correctly
classified as format-specific engineering.
