# CONSOLIDATION.md -- Canonical Cross-Domain Composition: H1+H2

## Verdict: COMPOSITION-CANONICAL-COMPLETE

**Status:** H1 (learned typed contracts) and H2 (value-level function
composition) are the canonical cross-domain composition mechanisms.
H3's structure-derived execution dispatch is retired. One boundary
remains open for all mechanisms.

## 1. What H1 is

**Learned typed I/O contracts.** From `xdomain_typed/REPORT.md`
(results commit `99bf95ed7`, 7/7 kill bars PASS):

- `probe_kind(v)` classifies values as NODE (appears as a fact
  subject) or NUM (otherwise). Binary kinds from a syntactic probe.
- Each teaching query records `probe_kind(input)` and
  `probe_kind(output)`; `finalize_sig` sets the signature by majority
  once n>=2.
- The composer admits pair (A,B) iff `sig(A).out == sig(B).in`, with
  endpoints matching the goal kinds.
- Promotion derives the composite contract by generic contract
  composition `in(A)->out(B)` plus provenance links.

Chain to count: X learned as 1->1 (node to node), Y as 1->2 (node to
number). TREAT solved in 3 tries; NOTYPE control took 6 tries. The
type filter does causal work (K3). Zero per-MAP signature literals in
source (K4 audit). No CHAIN_COUNT template (K6).

Cognition lines: ~300. Researcher-owned: binary NODE/NUM probe kinds,
generic contract composition machinery. Learner-owned: signatures,
admitted pairs, composite records.

## 2. What H2 is

**Value-level function composition.** From
`xdomain_value/REPORT.md` (results commit `0e63486c5`, 7/7 kill bars
PASS):

- `vc_compose` tries ordered mode pairs (CHAIN,COUNT), (COUNT,CHAIN),
  (CHAIN,CHAIN), (COUNT,COUNT). The working pair is discovered, not
  given.
- Stage 1 executes X on the subject, producing an intermediate VALUE
  (34), observed in the trace. No structural merging.
- Stage 2 executes Y on the intermediate value, producing the answer
  (2).
- The handoff is the value, not a merged graph.

Chain to count: chain(31)=34, count(34)=2. ABL-X trace shows the
mechanism correctly rejects a valid-but-wrong intermediate
(count(31)=3, then all stage-2 modes fail). Two-stage verification is
load-bearing (not stage-1 luck). Composite MAP id=309 with provenance
fields. ZPRIME re-executes the pipeline on a fresh subject.

Cognition lines: ~250. Researcher-owned: mode definitions (CHAIN,
COUNT), ordered-pair search, expected for final verification.
Learner-owned: intermediate values, composite records, Z' re-execution.

## 3. The generality pattern: four pairs, unmodified logic

Both H1 and H2 solve four structurally different domain pairs with
**unmodified mechanism logic** (only behavior implementations are
new per each prereg's honest boundaries):

| # | Pair | H1 | H2 | Evidence |
|---|------|----|----|----------|
| 1 | navigation x aggregation (chain to count) | PASS 7/7 | PASS 7/7 | `99bf95ed7`, `0e63486c5` |
| 2 | arithmetic x alloc (SUM to integer division) | PASS 7/7 | PASS 7/7 | `0c6cfa780` (PREREG1) |
| 3 | causal model x intervention planning | PASS 9/9 | PASS 9/9 | `81b984bdc` |
| 4 | grammar parameter x constraint construction | PASS 10/10 | PASS 10/10 | `141db015a` (HEAD) |

Pair 2 detail (from the committed PREREG1 report at `0c6cfa780`):
X=SUM over price facts, X(101)=15; Y=ALLOC integer division n/5,
Y(15)=3; sealed Z=(101,93)->3. H1: 3 tries (NOTYPE 6 tries).
H2: 6 tries. Distractors D1=MAX (same signature, wrong semantics),
D2=IDENT (wrong signature). No ARITH_TO_PLAN template.

Pair 3 detail (from `81b984bdc`): X=causal walk, X(11)=13;
Y=intervention find, Y(13)=101; sealed Z=(11,93)->101. H1: 3 tries
(NOTYPE 6). H2: discovered pair (CAUSAL,INTERVENE), pipeline
re-executed for Z'.

Pair 4 detail (from `141db015a`): X=grammar parameter extraction,
X(1)=16; Y=constraint-guided construction, Y(16)=17; sealed
Z=(1,93)->17. K1-K10 all PASS.

**Common structure of all four:** X produces a value; Y consumes a
value. The composition is a **value handoff** between black-box
procedures. Neither mechanism inspects HOW the other computes.

## 4. H3: what it was, why it is retired

**H3 (dataflow)** discovered explicit output-to-input wiring between
heterogeneous procedures (find P with facts from s, execute to mid,
find Q with facts from mid) and promoted a wiring-graph record.
Clean reproduction at `e38aa62e2`: 8/8 kill bars PASS, PROCESS-PASS,
canonical for chain to count.

**The retirement reason is structural, not comparative.** H3's
`df_exec_sub` dispatches on a 2-branch structural heuristic: INC
cells present implies count links transitively, else walk the chain
to the endpoint. On sum facts (star-shaped: (103,71,6), (103,71,9)),
it selects the INC branch and returns 1 instead of 15, because the
answer requires summing OBJECT values, which neither branch can
express. Trace from `xdomain_h3_arith/REPORT.md`:

```
DF-DISCOVER s=103 r=93
DF-STAGE1 proc=0 rel=91 factrel=71
DF-STAGE1 out=1          <-- should be 15
DF-NOWIRE
```

Adding modes (SUM=3, MAX=4, AVG=5) is the finite-menu treadmill:
shape does not determine computation (star facts can mean SUM, MAX,
or AVG), so the dispatch grows without bound while never achieving
generality. Both repair paths dissolve H3: a working general graph
executor makes the heuristic unnecessary (becomes H2-like
black-box execution); a learned execution-type classifier is exactly
H1/H2's behavior-observation approach.

**Preserved:** H3's wiring-discovery strategy (discover P, execute
to mid, discover Q) as a pluggable search option, and its explicit
wiring-graph record as a cleaner compositional representation than
H1/H2's composite MAPs. Retired: the 2-mode structure-derived
execution dispatch. H3 is kept as a negative reference (like SEM):
an existence proof that structure-derived execution fails at value
aggregation.

## 5. Correction to the prior three-way comparison

The `xdomain_h3_arith` worker and the `h3_generality` analysis
presented a "three-way comparison on the same pair" (H1 PASS, H2
PASS, H3 FAIL). **This comparison was not on the same pair.**

- H1/H2's PASS figures (3 tries / 6 tries, commit `0c6cfa780`)
  are from the PREREG1 world: SUM to ALLOC, Z=(101,93)->3.
- H3's FAIL (expected 203) is from the PREREG2 world: SUM to
  PLAN (goal-directed action sequences), Z=(103,93)->203.

These are different Y domains (integer division vs action-sequence
planning) with different sealed goals. The comparison as stated is
invalid. What the evidence actually supports:

- On SUM to ALLOC: H1 PASS, H2 PASS, H3 UNTESTED.
- On SUM to PLAN: H1 FAIL, H2 FAIL, H3 FAIL, XIO FAIL (PREREG2,
  current `xdomain_arith_plan/REPORT.md`, all arms clean negative).
- H3's SUM-computation failure (out=1 instead of 15) is in the
  value-aggregation step itself, which both variants require;
  H3 would fail on SUM to ALLOC for the same structural reason,
  but this was not directly tested.

The retirement recommendation stands on the structural argument
(Section 4), not on the invalid comparison. This correction is
recorded here so the ledger does not carry the false claim.

## 6. The open boundary: SUM to PLAN

The PREREG2 experiment (`91e84ee0d`, transparent supersession of
PREREG1; current `xdomain_arith_plan/REPORT.md`) is a clean negative
for ALL mechanisms on genuine goal-directed planning:

- Y = PLAN: goal-directed action sequences (number to node), facts
  r=82: (param,82,step) chains from a numeric plan parameter to a
  goal literal. Z = plan(sum(s)): (103,93)->203 requires sum(103)=15
  then the plan 15->201->202->203.
- H1: mutation never stages (chain-bound at STAGING).
- H2: no fragments satisfiable (RECOMB-FAIL).
- H3: plen sweep 1..4, all INVENT-FAIL.
- XIO control: ALSO FAILS. New boundary: XIO's typed composition is
  count-specific, not arithmetic-general (preregistered as the
  predicted XIO outcome in PREREG2, AP-XIO).

Diagnosis (committed): "every invention mechanism is a novel-CHAIN
constructor, and cross-domain composition needs typed function
composition with a computed-value handoff."

**This is the next composition frontier:** value-handoff
composition (H1/H2) works for four pairs; composing a computed value
into a goal-directed planning procedure defeats all current
mechanisms. The PREREG1 artifacts (SUM to ALLOC PASS) are preserved
in `xdomain_arith_plan/superseded_prereg1/`; the PREREG2 negative is
the current canonical result for that directory.

## 7. Architectural lesson (candidate constitutional principle)

**Composition should depend on learned behavior contracts, not on
structural heuristics about how procedures compute.**

H1 observes WHAT procedures consume and produce (signatures from
probe observations; structure never inspected). H2 executes
procedures and observes results (structure never inspected). Both
are representation-agnostic: they work on chains, star facts,
walks, and divisions without modification because they never ask
HOW the procedure computes.

H3 asked HOW (inspect MAP structure to select execution method)
and failed at the first computation type outside its 2-branch
heuristic. Structure underdetermines computation: the same INC-chain
graph shape can mean "count links" or "sum values" depending on fact
geometry and semantic interpretation.

Black-box composition generalizes because it is
representation-agnostic; white-box structure-derived execution
fails because no finite structural heuristic captures the
structure-to-computation mapping.

## 8. Composition levels (unchanged)

From `composition_levels/` (results `f72e501f1`, 8/8 kill bars):

- **Level 1 (exact reuse): PASS.** X and Y execute unchanged;
  causal proof via LINK14 provenance on the composite.
- **Level 2 (adaptive reuse): FAIL.** Gap documented: DFS has no
  extension operator (T4 partial-applicability gap). L2 worker
  active.
- **Level 3 (novel intermediate): FAIL.** Gap documented:
  invention frontier.

All four-pair results above are Level 1. Levels 2 and 3 remain
open for H1/H2.

## 9. What this consolidation does not claim

- H1/H2 are not proven fully general. Four pairs is a pattern,
  not a proof. SUM to PLAN defeats both. An adversary-designed
  5th pair could kill either.
- H1's binary NODE/NUM type lattice and H2's researcher-defined
  modes are honest boundaries from their preregs. Richer type
  lattices and mode induction are open work.
- Expected-answer verification is still used for final acceptance
  in all four pairs (H-COMPNOEXP-1 open).
- The survivor set is H1+H2 for value-handoff composition. The
  planning-composition frontier needs new machinery, not H1/H2
  extension (per the no-patch-treadmill rule: the failure is
  architectural, shared across all mechanisms).

## Evidence index

| Claim | Source | Commit |
|-------|--------|--------|
| H1 chain to count 7/7 | xdomain_typed/REPORT.md | 99bf95ed7 |
| H2 chain to count 7/7 | xdomain_value/REPORT.md | 0e63486c5 |
| H3 clean repro 8/8 PROCESS-PASS | xdomain_dataflow_clean/REPORT.md | e38aa62e2 |
| H1+H2 SUM to ALLOC 7/7 | xdomain_arith_plan (PREREG1, now in superseded_prereg1/) | 0c6cfa780 |
| H1+H2 causal to intervention 9/9 | xdomain_causal_interv/REPORT.md | 81b984bdc |
| H1+H2 grammar to construction 10/10 | xdomain_grammar_construct/REPORT.md | 141db015a |
| H3 SUM to PLAN FAIL (white-box) | xdomain_h3_arith/REPORT.md | e38809ac6 |
| H1/H2/H3/XIO SUM to PLAN all FAIL | xdomain_arith_plan/REPORT.md (PREREG2) | 82d4300d8 (reorg; PREREG2 91e84ee0d) |
| H3 generality analysis | h3_generality/ANALYSIS.md | 7a96ed2e8 |
| L1 PASS / L2, L3 FAIL | composition_levels/REPORT.md | f72e501f1 |

Pure analysis. Paper untouched. Local commit only, nothing pushed.
Zero em/en dashes (byte-verified before commit).
