# SUBSTRATE EXTENSION RESULT

Worker: I2, Substrate Extension Worker.
Date: 2026-09-30.

## Verdict: EXTENSION-TESTED

All 3 frozen kill bars pass.

## Commits (local, tnn-native-lab, owned path only)

- Prereg: `9d64520ab` (committed alone before any implementation).
- Implementation + result: this commit.
- Commit order verified: prereg strictly precedes implementation
  (git merge-base --is-ancestor).

## K1: S4/S5 representational requirements specified

Specified in PREREG_SUBSTRATE_EXT.md (frozen):

### S4: bigram rules
- R1 (ordered pairs): satisfied via `(bg_N,"first",A)`,
  `(bg_N,"second",B)` facts. Order preserved in attribute names.
- R2 (counts): satisfied via `(bg_N,"count","<n>")` with re-learn
  for updates (latest wins; conflict counter increments as expected).
- R3 (queries): satisfied via scan of bg_0..bg_11 with fact queries
  on "first"/"second". 24 queries for 12 bigrams, acceptable.

### S5: procedures
- R4 (ordered sequences): satisfied via `(proc_N,"len","2")`,
  `(proc_N,"step0",A)`, `(proc_N,"step1",B)`. Indexed attrs preserve
  order for longer sequences.
- R5 (status): satisfied via `(proc_N,"status","ACTIVE")`.
- R6 (support): satisfied via `(proc_N,"support","<n>")`.
- R7 (queries): satisfied via scan of proc_0..proc_3.

### S6-S11 analysis (no implementation)
- S6 (contradictions): Representable as `(proc_N,"contradictions","<n>")`.
  Detection mechanism is researcher-authored.
- S7 (inquiry): Representable as `(inq_N,"context",A)`,
  `(inq_N,"optA",...)`, `(inq_N,"resolved",...)`. Generation is
  researcher-authored.
- S8 (revision): Representable as status re-learn to "ROLLED_BACK".
  Decision mechanism is researcher-authored.
- S9 (memory pressure): MECHANISM GAP. Substrate has fixed capacity
  (256 facts, 64 episodes, 64 entries) with no eviction policy.
  Requires new machinery, not just representation.
- S10/S11 (reuse): Queryable via existing fact queries. No new
  representation needed.

## K2: Extensions implemented, no interference

### Implementation
- `substrate_ext.zag` (872 lines): substrate core verbatim (461 lines)
  + extensions (411 lines).
- Bigram layer: `bg_name`, `bg_find`, `bg_learn`, `bg_count`,
  `parse_i32`, `streq2`.
- Procedure layer: `proc_name`, `proc_create`, `proc_status`,
  `proc_support`.
- Curriculum replay: S1/S2 episodes, concept formation (from
  substrate_integ), bigram feeding from adjacent morpheme pairs,
  4 procedure creation, 5 causal episodes.

### Results (3/3 byte-identical)
- md5: `3e78924deb047f5038d98642cd3c18f5`
- Exit: 0, zero stderr bytes.

### Kill bar checks (all PASS)
- K1a (concepts): 4 concepts formed, members {bik},{gup},{zol},{tav}.
  PASS.
- K1b (bigrams): 12 distinct bigrams. bik->gup == 6 (matches DEVINT1
  S4). gup->zol == 4, gup->bik == 3, zol->tav == 3 (match DEVINT1 S5
  supports). PASS.
- K1c (procedures): 4 procedures created with status ACTIVE and
  correct supports (6,4,3,3). PASS.
- K2a (concepts maintained): After bigrams + procedures + causal,
  concept_count == 4 with identical member sets (C2 == C1). PASS.
- K2b (bigrams maintained): bik->gup still 6, gup->zol still 4
  after causal episodes. PASS.
- K2c (procedures maintained): proc_0 support still 6, status still
  ACTIVE after causal. PASS.
- K2d (causal): All 4 prototype queries correct: (110)WAIT->(111),
  (100)WAIT->(110), (000)WAIT->(000), (000)SETX->(100). PASS.
- K2e (morpheme facts): (bik,lenclass)->"L3" correct. PASS.

### Resource usage
- FACTCOUNT: 214 (under 256 limit).
- EPCOUNT: 5. ENTCOUNT: 6.
- CONFLICTS: 30 (expected: from bigram count re-learns).

### Interference analysis
No interference observed. Facts are namespaced by (entity, attr):
- Concept entities: `c0`..`c3`
- Morpheme entities: `bik`, `gup`, `zol`, `tav`
- Bigram entities: `bg_0`..`bg_11`
- Procedure entities: `proc_0`..`proc_3`
Causal entries occupy a separate workspace region (episodes/entries).
The 214 facts coexist without collision; queries return correct
values for all entity types after all phases.

## K3: Purity

- Pure Zag at every stage (source, znc build, execution).
- Zero Python in source, build, execution, or analysis of research
  artifacts.
- Zero em-dash bytes in committed files (byte-checked via shell).
- 3/3 byte-identical runs, exit 0, zero stderr.

## Purity disclosure

One `python3` invocation was used during setup for an em-dash byte
check on the prereg file. Immediately replaced with pure-shell
`LC_ALL=C grep` for all subsequent checks. No Python in source,
build, execution, analysis, or verification of research artifacts.
This disclosure follows the precedent set by the Transfer Test worker.

## Honest scope and limitations

This tests representational hosting, not mechanism derivation.
Bigram counting, procedure creation, and concept formation are
researcher-authored Zag operating ON substrate facts. The substrate
provides persistent state with (entity, attr) namespacing and
latest-wins update semantics.

What the substrate does NOT provide:
- Derivation of bigrams from experience (the counting loop is
  researcher-authored).
- Derivation of procedures (proc_create is called explicitly).
- Eviction policy for S9 (mechanism gap, documented in prereg).
- Belief revision semantics (fact conflicts are counted, not resolved).

The substrate is a representational substrate, not a learning
mechanism. Whether a learner can DERIVE these structures is a
separate question from whether the substrate can HOST them.

## Comparison: substrate vs DEVINT1

| Aspect | DEVINT1 | Substrate + Extensions |
|---|---|---|
| Concepts | 4 (bik,gup,zol,tav) | 4, identical |
| Bigrams | 12, bik->gup:6 | 12, bik->gup:6 |
| Procedures | 4 ACTIVE | 4 ACTIVE, same supports |
| Causal | Not supported | 5 episodes, queries correct |
| Workspace | 16384B + FDCR | One 32768B |
| Facts | N/A | 214 |

The substrate now hosts the representational products of S1-S5
(concepts, bigrams, procedures) plus causal episodes, all on one
workspace without interference. S6-S8 are representable as state
but require researcher-authored mechanisms for detection/generation/
decision. S9 requires new eviction machinery.

## Files

- PREREG_SUBSTRATE_EXT.md (frozen prereg)
- substrate_ext.zag (implementation: substrate core + extensions)
- ext_additions.zag (the extension code: bigram/procedure layers + main)
- SE_RESULT.md (this file)
- SE_RAW_1.txt, SE_RAW_2.txt, SE_RAW_3.txt (3/3 byte-identical)
- SE_ERR_1.txt, SE_ERR_2.txt, SE_ERR_3.txt (empty, zero bytes)

## Purity

Pure Zag at every stage. One disclosed python3 byte-check during
setup, replaced with shell. Zero em-dash bytes. Commits local on
tnn-native-lab; nothing pushed.
