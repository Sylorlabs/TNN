# PREREG: Substrate Integration Test (I2)

Worker: I2, Substrate Integration Worker.
Date: 2026-09-30.
Status: FROZEN. Committed alone before any implementation.

## Mission

Test whether the shared substrate (SUBSTRATE-PROTOTYPED, 2835e5641)
can host the cognitive state built by the merged curriculum's feed
schedule, maintaining the 4 FDCR concepts from Step E while also
handling causal episodes in one continuing run.

## Background

- Shared substrate: one 32768-byte workspace, nvar as runtime header,
  fact triples (entity, attr, value) coexisting with episodic causal
  entries (condition mask, UNCH/SET effects, ambiguity, parents,
  support). Prototype demonstrated facts AND causal episodes on one W.
- Merged curriculum (Step D): DEVINT1 S1-S11 (morpheme stream learner)
  + DEVINT2 S1-S7 (rule store), mechanical composition, single binary.
- Step E: FDCR FORM/MERGE ported to DEVINT1 concept layer. S1/S2
  morphemes feed con_form with features (length class, initial byte).
  Result: S3-FDCR-CONCEPTS 4. The 4 true morphemes are bik, gup, zol,
  tav (all length 3; initials b, g, z, t).

## Scope (explicit)

"Handle the curriculum" means: ingest the curriculum's experience
stream as substrate-native operations and maintain queryable cognitive
state. It does NOT mean porting DEVINT1's mechanisms (segmentation
DP, lexicon statistics, rule induction, procedure learning, inquiry
planning, revision machinery, memory-pressure eviction). The substrate
is a representational substrate; the test is representational
coverage.

Concretely:
- S1/S2: the 18 utterances are replayed. Each is segmented by exact
  fixed-width-3 split (all true morphemes are length 3; the S1/S2
  utterances are concatenations of bik/gup/zol/tav with no residue;
  verified by inspection of s1_ep/s2_ep). Each morpheme is fed as
  substrate facts: (morph, "lenclass", "L3"), (morph, "initbyte", X).
  Concept formation is implemented in Zag USING substrate facts:
  group morphemes by (lenclass, initbyte); for each group maintain
  (concept_N, "feat_len", L), (concept_N, "feat_init", X),
  (concept_N, "member", morph). This mirrors Step E's con_form
  feature-set matching (order-normalized; here features are already
  canonical) and MERGE (identical feature sets share one concept).
- Causal phase: the 5 substrate-prototype episodes (SETX/WAIT world)
  are recorded via sub_episode and processed via sub_causal_update,
  in the SAME run after concept formation, on the SAME workspace.
- S4-S11 declarative products (bigram rules, procedures,
  contradictions, revisions) are NOT replayed. Rationale: they
  require mechanisms (rule induction, procedure synthesis) beyond
  the substrate's fact/causal representation. This is reported as a
  representational limitation, not hidden. The core "morpheme
  sequence AND causal episodes in one run" test does not depend on
  them.

## Method

1. Copy substrate.zag core verbatim: z_alloc, emit, i32s, get32,
   set32, header accessors, sub_init, sub_str, sub_streq,
   sub_fact_learn, sub_fact_query, ep_off, ep_state, ep_act,
   ep_next, sub_episode, en_* accessors, ent_create, ent_add_sup,
   cond_matches, ent_consistent, popcnt, sub_causal_update,
   sub_causal_query, emit_state.
2. Add curriculum replay:
   - s1_ep/s2_ep/s1_len/s2_len copied verbatim from Step E source.
   - seg3(s, n): fixed-width-3 segmentation; asserts n%3==0.
   - feed_morpheme(W, s, off): learn (morph,"lenclass","L3") and
     (morph,"initbyte",<char>) facts; then concept accumulation:
     scan concepts 0..ncon-1 for matching (feat_len, feat_init);
     if found, add (concept_N,"member",morph) fact; else create
     concept N with feature facts and member fact.
   - concept_count(W): number of concepts formed.
   - concept_members(W, N, out): list members via fact query scan.
3. Main:
   - sub_init(W, 3).
   - Replay S1 (12 utterances) then S2 (6 utterances).
   - Record concept inventory C1 (count and members).
   - Record 5 causal episodes, run sub_causal_update.
   - Record concept inventory C2 (count and members).
   - Run causal queries (the 4 prototype queries).
   - Run fact queries (morpheme features).
   - Emit SUMMARY with all checks.

## Kill bars (frozen)

- K1 (curriculum loaded, concepts formed): PASS iff after S1/S2
  replay, concept_count == 4 AND the member sets equal
  {bik}, {gup}, {zol}, {tav} (matching Step E's 4 concepts; order
  of concept indices irrelevant).
- K2 (causal AND concepts maintained): PASS iff after causal
  episodes + sub_causal_update, concept_count == 4 with identical
  member sets (C2 == C1), AND all 4 prototype causal queries return
  the expected values, AND fact queries for morpheme features
  return correct values.
- K3 (purity): PASS iff pure Zag at every stage (source, znc build,
  execution), zero Python invocations, zero em-dash bytes in
  committed files, 3/3 byte-identical runs (md5 recorded).

## Falsification

- If concept_count != 4, the substrate's fact representation does
  not support Step E's concept formation; report SUBSTRATE-LIMITED
  with the divergence.
- If C2 != C1 (concepts disturbed by causal learning), the
  "coexist on one workspace" claim fails; report SUBSTRATE-LIMITED.
- If causal queries differ from the prototype, integration broke
  causal learning; report SUBSTRATE-LIMITED.

## Comparison

Substrate concept inventory vs Step E S3-FDCR-CONCEPTS 4:
both should be {bik},{gup},{zol},{tav}. Substrate causal queries
vs prototype: identical expected values. Any divergence is
reported, not smoothed over.

## Governance

- Prereg committed alone before implementation.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/substrate_integ/.
- Commits local on tnn-native-lab. Nothing pushed.
