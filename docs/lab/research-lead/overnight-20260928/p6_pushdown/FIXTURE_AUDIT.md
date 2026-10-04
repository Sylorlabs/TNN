# P6-PUSHDOWN — FIXTURE AUDIT (the load-bearing finding)

Lane `p6_pushdown`, branch `lane/p6pushdown`, base `87a822426`.
Companion to `PREREG.md` (frozen alone, commit `ad335b60f`).

This audit was run **before** any learner arm was executed, because the
learner's own induction stage refused to produce a grammar at stages 3-6 and
the reason needed to be established rather than worked around.

## A. WHAT WAS BUILT AND VERIFIED BEFORE THE AUDIT

- The reused world rebuilds on this host with the `_zag_print` shim:
  `p6_gencorpus` stdout sha256 `6507e7985a6fb4ffd8293ebe0a1930247e8bc5bc1e9e09898b68e07c543868bd`,
  3/3 byte-identical, identical to the prior lane's recorded sha.
- All **14 corpora regenerate byte-identical** to the committed artifacts
  (`cmp` clean, 14/14), re-verified after every experiment below.
- The learner translation unit (`p6_corpus.zag` + `p6_learner.zag`) compiles and
  runs. It contains no seed, no grammar table, no `lg_*`, no `ck_*`, no `gp_*`,
  no `gc_*`, no `gm_*`, no `bd_*` symbol.

## B. WHAT THE LEARNER INDUCES WHERE IT WORKS

Measured by `p6_ladder.zag`, which uses **only** the learner translation unit
(no world symbols), so the audit cannot be accused of consulting the checker.

Set A (seed 1009), stage 0, all 220 records:

```
nv (VALID occurrence count per token):
  t05=154  t11=134  t16=188  t19=89  t22=807  t23=167  t28=75
induced roles:
  5=ATOM  11=ATOM  16=ATOM  19=ATOM  22=SEP  23=ATOM  28=ATOM
```

**This is exactly the true instance.** From the world-side probe
`p6_inspect.zag`, seed 1009 stage 0 derives atom tokens `{5,11,16,19,23,28}`
with values `{30,57,38,3,43,0}` and `SEMI = token 22`. The learner recovered
the ATOM role set and the statement separator **from the corpus alone**, with no
seed and no table, by the structural predicates in `r_roles`:

- `rSEP`  = the last symbol of some reduced VALID skeleton;
- `rVAR`  = occurs immediately after a delimiter opener;
- `rATOM` = occurs as the first symbol of some reduced VALID skeleton, or
  immediately before an `rSEP`;
- `rBINOP`= any remaining mid-skeleton symbol.

This is a real induction and it is the first thing in this program where an
opaque-token language's alphabet partition has been recovered correctly from
experience alone. **It is the one positive result this lane produced.**

## C. THE FINDING: STAGES 3-6 OF THE FIXTURE CONTAIN NO NESTED STRUCTURE

`p6_ladder.zag` over all 14 corpora, measuring the complexity each corpus
actually contains:

| set | stage | distinct tokens | max len | mean len | **R1 delimiter pairs found** |
|---|---|---|---|---|---|
| A | 0 | 20 | 16 | 10 | **0** |
| A | 1 | 22 | 18 | 10 | **0** |
| A | 2 | 22 | 18 | 10 | **0** |
| A | 3 | 23 | 31 | 11 | **0** |
| A | 4 | 23 | 31 | 11 | **0** |
| A | 5 | 27 | 32 | 10 | **0** |
| A | 6 | **16** | 16 | 10 | **0** |
| B | 0 | 18 | 16 | 8 | **0** |
| B | 1 | 24 | 15 | 8 | **0** |
| B | 2 | 21 | 16 | 8 | **0** |
| B | 3 | 24 | 22 | 8 | **0** |
| B | 4 | 24 | 22 | 8 | **0** |
| B | 5 | 26 | 21 | 8 | **0** |
| B | 6 | 21 | 16 | 8 | **0** |

**R1 delimiter pairs found is 0 in all 14 corpora.** R1 is the learner's
hypothesis-free delimiter discovery: for every ordered token pair it measures
the support of the single-bracket-pair hypothesis and then greedily maximises
`(consistentCount, maxDepth)`. It is not a table; it is a statistic. It finds
nothing because **there is nothing to find**: no corpus at any stage contains a
single balanced token pair. Confirmed directly by token inspection — stage 6's
valid examples include `1XWXWQW]WXWFWQWQW` (16 tokens) and its longest program is
16 tokens, with no `LP`, no `LET`, no `END`, no `IF`, no `PROC`.

Stage 6 is also **strictly less complex than stage 5**: 16 distinct tokens
versus 27, max length 16 versus 32. The ladder does not rise; it collapses.

## D. ROOT CAUSE, ISOLATED IN THE WORLD GENERATOR

`p6_genprobe.zag` (world-side, not in the learner TU) calls the type-directed
generator directly, with **no dedup, no repair and no corpus assembly**, 400
draws per stage:

```
stage 0  avglen=4   checkerOK=6    withNAME=0  nested=0
stage 1  avglen=6   checkerOK=16   withNAME=0  nested=0
stage 2  avglen=6   checkerOK=12   withNAME=0  nested=0
stage 3  SEGFAULT
```

`p6_genprobe2.zag` narrows it further: `gp_prog` at stage 3 segfaults, and
`gp_let` called directly at stage 3 survives one call and segfaults on
approximately the 32nd. `gp_expr` survives 200 calls, `gc_bind`/`gc_unbind`
survive 300, and `gp_stmts` at depth 2 segfaults within 200. So the defect is in
the `LET`-block recursion of `gp_stmts` -> `gp_stmt` -> `gp_let`, not in the
expression generator, the binder, or the RNG (the LCG state was verified
in-range for 60 consecutive draws).

Because `gm_stage` catches nothing, a segfaulting draw in the middle of the
VALID fill loop would abort the whole binary. What actually happens in the
committed corpora is that the draw loop *survives* but `cr_dup` de-duplicates,
so once the shallow programs saturate the 130-slot VALID budget, every deeper
candidate is rejected as a duplicate and the corpus fills with flat programs.
That is why stages 3-6 look like stages 0-2 with a longer tail: the tail is
longer programs of the **same flat shape**, not nested programs.

## E. WHY THIS VOIDS THE COMPLEXITY LADDER (PREREG K9, P6, P8)

PREREG K9 asks for "the highest stage meeting K2" and P6 predicts "the ceiling
is at stage 4 or 5, caused by interaction of scope with block structure".
P8 predicts R1 recovers `{LP,RP}` and `{LET,END}` by stage 3.

**None of these is measurable on this fixture.** The pushdown representation
was the load-bearing change this lane was built to make, and its entire reason
for existing is unbounded nesting. The fixture provides nesting at **no** stage.
A pushdown learner evaluated here would be evaluated on a language that is, as
the data actually stands, **regular**.

Reporting a "complexity ceiling" from this fixture would be reporting the
generator's buffer bug as a fact about induction. It would not be a finding.

Per PREREG section 8 (inherited), this is a **VOID** condition: the fixture does
not instantiate the preregistered hypothesis. It is stated openly here rather
than worked around.

## F. WHAT WAS DELIBERATELY NOT DONE

- The generator was **not** repaired and the corpora **not** regenerated. An
  exploratory patch was written and then **reverted**; the committed world is
  byte-identical to `p6/formal-induce` and all 14 corpora still regenerate
  `cmp`-clean. Repairing the generator would have silently changed the frozen
  experience set that this lane's prereg adopted, which would have been a worse
  violation than reporting the void.
- No learner arm was scored on stages 3-6, because there is nothing there to be
  scored on.

## G. THE CORRECT NEXT STEP (not executed in this lane)

Repair `gp_stmts`/`gp_stmt`/`gp_let` depth handling in the world, re-verify that
stages 3-6 contain real `LP`/`RP` and `LET`/`END` structure by re-running
`p6_genprobe.zag`, regenerate the 14 corpora under a **new disclosed fixture
version**, and only then run R2-R6 and ZD-1/2/3. That is a new prereg, not a
continuation of this one.
