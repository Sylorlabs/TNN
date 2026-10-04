# REPORT.md -- Hypothesis 3: Constraint-Driven Novel Form Invention

## Verdict: INVENTION-CONSTRAINT-COMPLETE

**TNN constructs genuinely novel MAP forms via backtracking search guided
by goal constraints. The search builds chains cell by cell from individual
facts, pruned by structural constraints. No existing MAP is selected,
recombined, or modified. The final form is source-underdetermined: the
source provides general constraint checkers and backtracking machinery,
but the specific form is determined by the goal's constraint values plus
the world's facts.**

## Mechanism

`invent_patch.zag` (~200 lines), unfrozen only. Base is `composition_C`
core (rebind + trial + revision machinery), lines 1-1677; `ev_query`
redefined (standard) plus `ev_query_c` (constraint-carrying).

**Constraint representation**: 6-slot struct [plen, rel_exact_r,
rel_exact_n, first_rel, last_rel, first_lit]. -1 means don't care.
Constraint VALUES come from the driver (goal side), never from the
mechanism.

**Search** (`invent_dfs`): iterative backtracking DFS over fact
sequences. At each chain position, candidates are live facts with
subject == current value, in node id order. Pruning:
- first_rel must match at position 0
- last_rel must match at position plen-1
- rel_exact count must stay reachable: count so far <= N, and
  count so far + remaining positions >= N

**Construction** (`invent_try`): on reaching plen positions, assemble
via `t2_asm_chain`, verify by execution via `t2_try_verify` (must
produce expected), promote via `promote_graph`. Returns answer or -2.

**Verification** (`invent_check`): extracts the MAP's relation sequence
from its executable graph via structure walk (never MAP labels) and
checks every non-don't-care constraint. Used for K1/K2/K3.

**Why not a finite menu**: The search space is the combinatorial product
of fact choices at each position, not an enumerated list. The constraint
language is compositional (plen x rel-count x first-rel x last-rel x
first-lit). The source contains zero test-world values, zero fact ids,
zero value sequences. Three structurally different problems are solved
by the identical general machinery.

## Experiment

Three problems in fresh workspaces. Each teaches a solution fact path
plus distractor short paths, then queries with structural constraints.

Problem 1: plen=5, rel7 exactly 2, first_rel=3, first_lit=3.
World: (3,3,10)(10,7,20)(20,5,30)(30,7,40)(40,9,90) plus distractors
(3,5,11)(11,5,90)(3,7,12)(12,7,90). Goal s=3,r=70,expected=90.

Problem 2: plen=4, rel5 exactly 1, last_rel=9. Decoy dead end forces
backtracking: (50,3,65)(65,5,75) taught first (lower ids, tried first),
but 75 has no outgoing facts. World also has solution
(50,3,60)(60,5,70)(70,7,80)(80,9,150) and distractors (50,7,55)(55,7,150).
Goal s=50,r=71,expected=150.

Problem 3: plen=6, rel7 exactly 3, first_rel=3.
World: (200,3,205)(205,7,215)(215,5,225)(225,7,235)(235,9,245)(245,7,300)
plus distractors (200,5,210)(210,5,300). Goal s=200,r=72,expected=300.

Arms (fresh workspace per problem), 3/3 byte-identical per binary:
- TREAT: invent_on()=1. ev_query_c with constraints.
- NO-INVENT: invent_on()=0 (one-line diff). Standard ev_query (trial).

SHA-256 (first 16 hex): treatment `7daadbec6308bdbd`, control
`2aa88e4d4bfe1b2a`.

## Results

### TREAT: invention constructs all 3 (K1 PASS)

```
=== PROBLEM 1 ===
K3 pre-existing satisfying MAPs=0
INVENT-OK plen=5 map=32
P1 ans=90
P1 MAP id=32 check=1
MAP 32 relseq=[3,7,5,7,9] len=5
=== PROBLEM 2 ===
K3 pre-existing satisfying MAPs=0
INVENT-OK plen=4 map=27
P2 ans=150
P2 MAP id=27 check=1
MAP 27 relseq=[3,5,7,9] len=4
=== PROBLEM 3 ===
K3 pre-existing satisfying MAPs=0
INVENT-OK plen=6 map=35
P3 ans=300
P3 MAP id=35 check=1
MAP 35 relseq=[3,7,5,7,9,7] len=6
```

All 3 invented MAPs satisfy every constraint exactly:
- P1: plen 5, rel7 at positions 1 and 3 (exactly 2), first rel 3, v[0]=3.
- P2: plen 4, rel5 at position 1 (exactly 1), last rel 9. The decoy
  (50,3,65) was tried first (lower node id), dead-ended at 75,
  backtracked, found the solution. Backtracking is logically necessary:
  no plen-4 path exists through the decoy.
- P3: plen 6, rel7 at positions 1, 3, 5 (exactly 3), first rel 3.

### NO-INVENT: trial gets answer right, form wrong (K2 PASS)

```
=== PROBLEM 1 ===
P1 ans=90
P1 MAP id=29 check=0
MAP 29 relseq=[5,5] len=2
=== PROBLEM 2 ===
P2 ans=150
P2 MAP id=37 check=0
MAP 37 relseq=[7,7] len=2
=== PROBLEM 3 ===
P3 ans=300
P3 MAP id=28 check=0
MAP 28 relseq=[5,5] len=2
```

Trial finds the correct ANSWER on all 3 via short distractor paths, but
the FORM violates constraints on all 3 (plen 2 vs required 5/4/6; rel7
count 0 vs required 2/3; etc.). This is the "inadequate existing"
demonstration: trial's fact-path enumeration is form-blind. It cannot
even express "relation 7 exactly twice", let alone search by it.

### Kill bar verdicts

K1 (construction): TREAT check=1 on all 3. PASS.
K2 (inadequate existing): NO-INVENT check=0 on all 3. PASS.
K3 (novelty): 0 pre-existing MAPs satisfy constraints on all 3. PASS.
K4 (structural difference): (5,[3,7,5,7,9]), (4,[3,5,7,9]),
(6,[3,7,5,7,9,7]) pairwise different. PASS.
K5 (determinism): 3/3 byte-identical per binary. PASS.
K6 (no hardcoded answers): source grep for test values/fact sequences
returns empty. Constraint values originate in driver (goal side).
PASS.

## SUF Analysis

**Inadequate existing**: Demonstrated by K2. Trial (the existing
constructive mechanism: mutation/recombination over BFS fact paths)
produces the correct answer but a form that violates the goal's
structural constraints. No existing MAP satisfies the constraints (K3).

**New form**: The three invented MAPs (ids 32, 27, 35) have relation
sequences [3,7,5,7,9], [3,5,7,9], [3,7,5,7,9,7]. These exact structures
never existed in learner state before invention (K3 scan found zero).
They are not selections, recombinations, or modifications of existing
MAPs; they are built cell by cell from individual facts.

**Source-underdetermined**: The source code contains no test-world
values, no fact ids, no value sequences (K6 verified by grep). The
constraint checkers are general (work for any relation, count, plen).
The constraint VALUES come from the driver (goal side). The fact
CHOICES come from the world (node id order + constraint pruning).
Three different constraint sets in three different worlds produce three
different forms from identical machinery. Change the world facts and
the invented form changes. The form is determined by (goal + world),
not source.

**Internally evaluated**: `t2_try_verify` executes the constructed
graph on a fresh frame before promotion. Only graphs producing the
expected output are promoted. The structural check (`invent_check`)
is available for post-hoc verification.

**Useful**: Each invented MAP produces the expected answer (90, 150,
300) via the required structural form. The form is not decorative;
it is the executable mechanism that computes the answer.

**Persistent**: Promoted as MAPs in learner state (ids 32, 27, 35),
with DEP provenance edges to licensing facts. They survive in the
workspace and are retrievable via `iv_find_map`.

**Reusable**: The MAPs persist and the `invent_check` machinery can
verify them. Full reuse (applying an invented MAP to a new goal with
matching constraints) is not demonstrated in this wave; the mechanism
is compatible with the existing rebind machinery (which operates on
promoted MAPs regardless of origin).

**Revisable**: The base provides `t2_revise_graph` (surgical revision
on counterexample). Not explicitly tested for invented MAPs in this
wave; the provenance edges (DEP to licensing facts) that revision
uses are written by `promote_graph` for invented MAPs identically to
trial-promoted MAPs.

**Transferable**: The SAME general mechanism solved three structurally
different problems (different plen, different relations, different
counts, different worlds). This is transfer across problem instances.
Cross-domain transfer (e.g., constraints on non-chain structures)
remains future work.

## Relation to Composition A/B/C

Composition selects and chains EXISTING MAPs. Invention constructs
NOVEL chains from INDIVIDUAL FACTS. The building blocks differ
(MAPs vs facts), and no MAP is involved in the invention search.
Composition-C uses goal input/output to select MAPs; Invention-H3
uses goal STRUCTURAL CONSTRAINTS to prune a constructive search.
They are complementary, not overlapping.

## Limitations and future work

1. The constraint language is fixed to 6 structural properties of
   chains. Richer constraints (e.g., on branching structures, on
   value patterns) are future work.
2. The search is over fact sequences, not arbitrary graph topologies.
   Invention of non-chain forms (branching, looping) is future work.
3. Reuse, revision, and cross-domain transfer of invented forms are
   assessed but not fully demonstrated; they are the next experiments.
4. The driver supplies constraints explicitly. Inferring constraints
   from failed attempts (rather than receiving them) is a harder
   problem and future work.

## Files

- `invent_patch.zag`: mechanism (~200 lines)
- `invent_driver.zag`: experiment driver
- `invent_base.zag`: base copy (for reference)
- `invent_full.zag` / `invent_full_ni.zag`: assembled (one-line diff)
- `invent_bin` / `invent_ni_bin`: binaries (pinned znc)
- `invent_compile.txt` / `invent_ni_compile.txt`: build logs
- `invent_run1/2/3.txt`: TREAT transcripts (3/3 byte-identical)
- `invent_ni_run1/2/3.txt`: NO-INVENT transcripts (3/3 byte-identical)

Architecture accounting: +200 cognition lines, 0 new modes, 0 new
bridges, 0 new handlers, 0 new semantic cases. The constraint checkers
are general machinery, not answer templates.
