# PREREG: Substrate Extension to S4/S5 (I2)

Worker: I2, Substrate Extension Worker.
Date: 2026-09-30.
Status: FROZEN. Committed alone before any implementation.

## Mission

Test whether the shared substrate can be extended to host the
representational products of DEVINT1 stages S4 (bigram rules) and S5
(procedures), in addition to the facts/concepts/causal episodes already
demonstrated in SUBSTRATE-INTEGRATED (6e3294a49). Test for interference:
do bigram and procedure facts disturb existing concept facts or causal
entries?

## Background

- Substrate: one 32768-byte workspace, fact triples (entity, attr,
  value) coexisting with episodic causal entries. Capacity: 256 facts,
  64 episodes, 64 entries.
- SUBSTRATE-INTEGRATED: 45 morphemes as facts, 4 concepts formed
  ({bik},{gup},{zol},{tav}), 143 facts total, 5 causal episodes,
  no interference between facts and causal.
- DEVINT1 S4: 12 distinct concept bigrams counted; strongest
  bik->gup:6. S5: 4 rules ACTIVE at support >= 3: bik->gup:6,
  gup->zol:4, gup->bik:3, zol->tav:3.

## K1: S4/S5 representational requirements

### S4: bigram rules

A bigram rule is an ordered pair of concepts (A, B) with a count.
Requirements:
- R1: Store ordered pair (A, B). Order matters: bik->gup differs
  from gup->bik.
- R2: Store count per pair. Counts update as more episodes observed.
- R3: Query: given A, retrieve all (B, count) pairs. Given (A,B),
  retrieve count.

Substrate encoding (fact triples):
- Bigram entity: `bg_N` where N is a small integer index (0..11).
- `(bg_N, "first", A)`: first concept of the pair.
- `(bg_N, "second", B)`: second concept of the pair.
- `(bg_N, "count", "<decimal>")`: observation count as string.
- Count updates via re-learning (latest wins): re-learn
  `(bg_N, "count", "<new>")`. The conflict counter increments,
  which is expected and reported.
- Lookup (A,B)->N: scan bg_0..bg_11, query "first" and "second",
  compare. With 12 bigrams this is 24 fact queries, acceptable.
- Lookup A->all: scan bg_0..bg_11, query "first", collect matches.

This satisfies R1 (ordered via first/second attrs), R2 (count attr,
re-learn for updates), R3 (scan-based lookup).

### S5: procedures (active rules)

A procedure (here, an active bigram rule) is an ordered sequence
with status and support. Requirements:
- R4: Store ordered sequence [A, B] (length 2 for bigram rules;
  encoding supports longer).
- R5: Store status (ACTIVE, etc.).
- R6: Store support count.
- R7: Query: list all ACTIVE procedures; query procedure details.

Substrate encoding (fact triples):
- Procedure entity: `proc_N` where N is a small integer (0..3).
- `(proc_N, "len", "<decimal>")`: sequence length.
- `(proc_N, "step0", A)`, `(proc_N, "step1", B)`: ordered steps.
  Indexed attrs preserve order for longer sequences.
- `(proc_N, "status", "ACTIVE")`: status string.
- `(proc_N, "support", "<decimal>")`: support count.
- Status change via re-learn (latest wins).

This satisfies R4 (indexed step attrs), R5 (status attr), R6
(support attr), R7 (scan proc_0..proc_3, query status).

### S6-S11: representational analysis (no implementation)

- S6 (contradictions): Representable as fact metadata.
  `(proc_N, "contradictions", "<decimal>")`. The contradiction
  DETECTION (comparing episode against active rule) is
  researcher-authored mechanism, not substrate-derived.
- S7 (inquiry): Representable as structured facts.
  `(inq_N, "context", A)`, `(inq_N, "optA", "...")`,
  `(inq_N, "optB", "...")`, `(inq_N, "resolved", "...")`.
  The inquiry GENERATION (selecting what to ask) is
  researcher-authored.
- S8 (revision): Representable as status change.
  Re-learn `(proc_N, "status", "ROLLED_BACK")`.
  The revision DECISION (when to roll back) is researcher-authored.
- S9 (memory pressure): MECHANISM GAP. The substrate has fixed
  capacity (256 facts, 64 episodes, 64 entries) with no eviction
  policy. Implementing importance-weighted or LRU eviction requires
  a policy mechanism the substrate does not specify. This is not
  representable in current fact/causal ops; it needs new machinery.
- S10/S11 (reuse/recognition): Queryable via existing fact queries.
  No new representation needed; these are measurement protocols.

## Method

1. Copy substrate.zag core verbatim (all fns through
   sub_causal_query, emit_state).
2. Copy curriculum replay from substrate_integ.zag:
   s1_ep/s2_ep, seg3, feed_morpheme, concept formation,
   5 causal episodes.
3. Add bigram layer:
   - `bg_learn(W, A, B)`: find existing bg_N with first==A and
     second==B via scan; if found, increment count (query, parse,
     re-learn); if not found and nbg<12, create bg_N with
     first/second/count="1".
   - `bg_count(W, A, B)`: scan, return count or 0.
   - Feed the S4 bigram observations: replay S1/S2 morpheme
     sequences, count adjacent pairs. Expected: 12 distinct
     bigrams; bik->gup should reach 6.
4. Add procedure layer:
   - `proc_create(W, A, B, support)`: create proc_N with len=2,
     step0=A, step1=B, status=ACTIVE, support.
   - Create the 4 S5 procedures: (bik,gup,6), (gup,zol,4),
     (gup,bik,3), (zol,tav,3).
   - `proc_list_active(W)`: scan, emit ACTIVE procedures.
5. Main sequence (one run, one workspace):
   - sub_init(W, 3).
   - Replay S1/S2, form concepts (expect 4).
   - Feed bigrams from morpheme sequences (expect 12 distinct).
   - Create 4 procedures.
   - Record 5 causal episodes, run sub_causal_update.
   - Verify: concept_count==4 with identical members (C2==C1);
     bg_count(bik,gup)==6; 4 ACTIVE procedures listed;
     4 causal queries correct; morpheme fact queries correct.
   - Emit SUMMARY with all checks.
6. Run 3 times, verify byte-identical, record md5.

## Kill bars (frozen)

- K1 (requirements specified): PASS iff this prereg specifies
  substrate encodings for S4 bigrams (R1-R3) and S5 procedures
  (R4-R7), plus S6-S11 analysis. Satisfied by this document.
- K2 (extensions implemented, no interference): PASS iff after
  bigram feeding + procedure creation + causal episodes:
  (a) concept_count == 4 with member sets identical to pre-bigram
  state; (b) 12 distinct bigrams with bik->gup count == 6;
  (c) 4 procedures queryable with status ACTIVE and correct
  supports; (d) all 4 prototype causal queries correct;
  (e) morpheme fact queries correct. If any of (a)-(e) fails,
  report EXTENSION-LIMITED with the specific divergence.
- K3 (purity): PASS iff pure Zag at every stage (source, znc
  build, execution), zero Python invocations, zero em-dash bytes
  in committed files, 3/3 byte-identical runs (md5 recorded),
  exit 0, zero stderr.

## Falsification

- If bigram facts disturb concept facts (C2 != C1), the fact
  store does not isolate entity namespaces; report
  EXTENSION-LIMITED.
- If procedure facts disturb causal entries, the regions overlap;
  report EXTENSION-LIMITED.
- If fact capacity (256) is exceeded, report the count and
  EXTENSION-LIMITED (capacity bound, not interference).
- If S9 eviction is attempted and fails, that is expected per
  the mechanism-gap analysis; it does not fail K2 (S9 out of
  scope for implementation).

## Honest scope

This tests representational hosting, not mechanism derivation.
Bigram counting, procedure creation, and concept formation are
researcher-authored Zag operating ON substrate facts. The
substrate provides persistent state with (entity, attr) namespacing.
Whether the learner can DERIVE bigrams/procedures is a separate
question (cf. DDES L3 analysis: guidance vs. substrate).

## Governance

- Prereg committed alone before implementation.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/substrate_ext/.
- Commits local on tnn-native-lab. Nothing pushed.
