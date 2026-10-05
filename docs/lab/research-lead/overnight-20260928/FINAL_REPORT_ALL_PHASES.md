# FINAL REPORT -- ALL PHASES

Lane `ownership`, branch `lane/ownership`. 27 commits.
Covers PHASE 0 through PHASE 15 as executed, with honest status for
every phase including the ones not run.

---

## 0. HEADLINE

Four independent attempts to make selection learner-owned -- learned
contracts, generated proposal shapes, induced procedures, learned
affinities -- **all matched or lost to a simple counting heuristic.**

```
C1681  selection   a fixed heuristic TIES the learner
C1800  generation  a fixed heuristic BEATS the learner
C1850  procedure   a fixed heuristic BEATS the learner
C1860  affinity    a fixed heuristic BEATS the learner (4/4 vs 1/4)
```

That regularity is this session's main empirical result, and it is
stronger than any single experiment in it.

A second regularity is methodological, and it cost me the most:

> **Three of my harnesses could not measure their own bar** -- an
> unreachable expected answer, a primitive alphabet that could not
> reach the shifted family, and a world containing a universal
> structure. All three initially read as clean negatives.

**L3 = 0 throughout.** No architecture was changed. Zero bridges
deleted. Zero promotions claimed.

**Subject to `RED_TEAM.md`, which withdraws two of the claims above
("types are information-theoretically insufficient", "theory found a
bug every time"), narrows two others, and establishes that no
experiment here measured TNN itself.**

---

## 1. PHASE STATUS

| phase | status | outcome |
|---|---|---|
| 0 bridge audit | **done** | 4 structural bridges found, 0 named |
| 1 pair choice | **done** | BR-1/2/3 cluster, frozen with rationale |
| 2 baseline | **done** | BRIDGE-ON/OFF, NOPROBE, PERMUTE, FO, FRESH |
| 3 recruitment | **done** | BR-1 replaced; contracts shown **insufficient** |
| 4 transfer | **done** | fresh query `(20,111)->22`, no source change |
| 5 revision | **done** | two distinct mechanisms, one instant one unstable |
| 6 other-architecture principles | **done** | 3 principles falsified, F-CONTENT falsified |
| 7 finder ownership | **done** | learned generation 0/4, researcher greedy 4/4 |
| 8 learned transformations | **done** | procedure over kind induced; argument gap found |
| 9 self-organizing world | **done** | affinity loses to counting; world collapsed |
| 10 architecture subtraction | **done** | BR-4 solved by retaining provenance |
| 11 H16v4 | **done** | positive control fired, 2 results retracted |
| 12 instrument hardening | **done** | two lints, both validated on fixtures |
| 13 existing open fronts | **surveyed only** | concrete items named, not worked |
| red team | **done** | 3 claims withdrawn, 3 narrowed, 2 instrument defects found |
| 16 large-N counting test | **done** | C1634 resolved: query-conditional arm 12/36 vs COUNT 1/36 |
| 14 bridge retirement | **done as a queue** | 0 deletions; blockers recorded |
| 15 long lifetime recruitment | **done, negative** | precondition held, mechanism still lost |

---

## 2. ARCHITECTURE CHANGES

**None to TNN.** No source file of the canonical learner was touched.

Added:

```
tools/tnn_bars_lint.sh   enforces R3 (recompute every bar)
tools/tnn_loop_lint.sh   enforces loop termination
docs/.../ownership/RULES.md   R1-R10 standing policy
```

The lints are not ceremony. `tnn_bars_lint.sh` catches the exact
defect that hid an evaluator bug for a lane, and `tnn_loop_lint.sh`
was written after a missing loop increment produced a segfault whose
*location moved* whenever unrelated code changed -- indistinguishable
from memory corruption, and it cost several cycles.

---

## 3. STRONGEST SURVIVING RESULTS

**R-A. A syntactic router can be replaced by derived contracts, and its
surface dependence was pure loss.** Contracts probed from each
structure's own graph, plus classes derived from the fact table.

```
router/aligned = 12    router/neutral = FAIL
contract/aligned = 12  contract/neutral = 12
```

Permutation-invariant, facts-only-resistant, 9/10 bars.
**Scope narrowed by KILL-6 below.**

**R-B. Selection responds to consequences and transfers.**
Consequence-weighted selection fixes the C1541 counterexample in
**1 trial**, transfers to a fresh query with no source change, and
reverts to the failure when support is erased. **Downgraded** -- a
fixed length preference also solves it.

**R-C. Two invalidation mechanisms exist and must not be conflated.**
Gate invalidation (structure becomes ineligible) is **instant**.
Consequence revision (stays eligible, becomes wrong) took **12 trials**
and then oscillated. Reporting the first as "revision works" would
have been false, and I made that mistake once.

**R-D. BR-4 is a representation defect, and representation is learner
state.**

```
BASE (count bridge)   SUM->2  COUNT->3  MAX->2    1 of 3
TREAT (MAP retains
       its aggregation)  SUM->15 COUNT->3  MAX->8   3 of 3
FO (provenance erased)  FAILV, loudly
```

One generic executor handles all three aggregations. The count bridge
handled one, by luck.

**R-E. Query-scoped credit is the only learner mechanism that beat
every fixed heuristic.** `2 of 2` against `1 of 2` for every fixed
selector and for global credit. One control.

---

## 4. IMPORTANT KILLS

**KILL-1. Proposal ordering is not a route to L3.** Any wrong linear
parity over GF(2) disagrees with the true parity on exactly half the
rows, regardless of arity. Adding a candidate class does not create a
gradient. Under noise an *apparent* gradient appears (spread 12-16) but
it is sampling variance: facts-only reproduces it exactly. Gradient
reversal collapses the truth 57 -> 7.

**KILL-2. Learned contracts are provably NOT sufficient.** A
legitimately learned structure whose output is class-valid but wrong is
recruited and accepted. Nothing available could reject it. Both the
router and contract arms break identically, so it is not a
bridge-removal regression.

**KILL-2b. Learned selection has never beaten a trivial heuristic.**
Two no-experience selectors -- "prefer the shortest chain" and "take
the first eligible chain" -- tie the learner exactly. In a world built
so fixed preferences cannot win, the learner scores 1 of 2, identical
to every fixed selector. **VOID** per the prereg's own rule.

**KILL-3. Additive support over chain elements is unsound.** `(s,s)`
scores `2*s` and outscores `(s)`, rewarding self-composition.
Oscillates at 18/28 stable; any length-normalising rule restores
27/28.

**KILL-6. Type signatures cannot do routing.** Two mirror-image queries
needing opposite answers share signature key 14. Signature-keyed
routing scores 0 of 2, worse than unscoped.

```
routing from TYPES   ->  insufficient; signatures collide
routing from VALUES  ->  sufficient; and it is memorisation (2 of 2)
```

This is the structural reason BR-1/2/3 exist. A signature-based router
cannot do the job, so the researcher reaches for something
value-specific: `route_line` for punctuation, a lookup table for the
input. **The bridge is not laziness; it is what happens when the
available abstraction is too coarse and something has to give.**

**KILL-7. Three borrowed architectural principles, all falsified.**
Hebbian-style local co-use plasticity, attractor settling, and
predictive-coding-style mismatch records each scored 1 of 2 --
identical to `LEN1`, `LEN2` and `TIES`. All three collapse trivially
into existing substrate, so they are cheap in machinery and worth
nothing in capability.

**KILL-8. Learned generation is brittle to solution-length shift.**
Learned proposal shapes were 3-4 edits; every test instance had a
2-edit solution. The knowledge transferred perfectly between disjoint
distributions and was still useless.

**KILL-9. A learned procedure over edit KIND is insufficient.**
PHASE 8 induced a coherent 3-key table over which *kind* of edit to
make, and it still failed every instance. The researcher's advantage
is not the kind, it is the **argument** -- which instance to change.

---

## 5. BRIDGE AUDIT

```
corpus      105,673 files / 80,991,292 LOC / 987 experiments / 106 lanes
named _TO_ bridges in code      0   (every hit is a comment asserting absence)
named cognitive MODES in code   0   (same)
structural cognitive bridges    4
generic interface mechanisms    1
```

| id | location | what it is | class |
|---|---|---|---|
| BR-1 | `unified_learn.zag:734` `route_line` | syntactic router, 5 role-named routes chosen by input shape | D |
| BR-2 | `unified_learn.zag:423,445` | conditional `(pos,val)` bridge triggered by hardcoded failure policy | D |
| BR-3 | `unified_learn.zag:1008` | candidate-origin taxonomy `-1/-2/0 proc/1 bridge` | D |
| BR-4 | `xio_core.zag:95-99` | re-derives COUNT for any numeric MAP; `sum(103)=15` reported as `count(103)=2` | D |
| BR-5 | `l3_bridge_impl/bridge.zag` | removed a signature enum + 3 recipe branches for 4 generic operators | **B** |

**Cluster finding:** BR-1, BR-2, BR-3 are one missing property in three
disguises -- *deciding which learned structure applies, using that
structure's own properties.*

**Name-based auditing is invalid here and is retired as a method.**
All four bridges are implicit; a grep reports a clean bill of health on
a substantially bridged architecture.

---

## 6. BRIDGE DELETIONS

**Zero.** Two bridges have measured replacements (BR-1, BR-4); zero have
a replacement committed to the canonical learner.

```
BR-1  deletable once committed; replacement MEASURED
BR-3  deletable with BR-1/BR-2
BR-2  BLOCKED on selection; also carries a known F-LEAK defect
BR-4  replacement MEASURED; needs the MAP promotion format changed
BR-5  keep -- already the right shape, and the compression target
```

Per KILL-6, deleting BR-1 without a *general* substitute for type-based
routing does not remove a bridge; it removes the only thing making the
bridge necessary and leaves the capability unimplemented.

---

## 7. METHOD OWNERSHIP PROGRESS

```
applicability   syntax-based routing  ->  learner state      MEASURED
                routing in general   ->  NOT solved         KILL-6
selection       consequence-weighted                        MEASURED
                beating a count heuristic                   NOT achieved
scoring rule    (a+b)/2 is researcher source, 3 chars       OPEN
credit scope    the key was chosen after seeing answers     OPEN
argument        which instance to change                    OPEN  (PHASE 8)
```

---

## 8. SELF-ORGANIZATION PROGRESS

Roles are never declared: value classes are derived, signatures are
learned by probing, and role vocabulary is absent from source
(grep-clean). Two structures with no declared roles composed because
their learned contracts connected.

Not demonstrated: a structure genuinely repurposed across roles. The
one test of it was unmeasurable because the world admitted a universal
structure. **Naming the pattern: a harness that admits a universal
solution cannot test selection, because selection only exists where
competence is distributed.**

---

## 9. FORMAL / META / BELIEF / SCALING (PHASE 13)

Surveyed, not worked. Evidence-based status:

```
l3_rx              CONDITIONAL-PASS 15/16; RX-K10 (independent red
                   team) PENDING because it "requires a different
                   instance" -- concrete, and this session's borrows
                   are all different instances
p6_formal_induce   carries a pre-committed verdict label
                   ZD2-PASS-DEGENERATE-POLICY -- needs scrutiny
p5_unblock, p6_pushdown, p6meta2, p6unblock, trialleak, predopt,
misspath, invfix   highest counts of OPEN/PENDING markers in the corpus
```

Also recorded: the prior **four-pair generality claim is false.** Two
colliding `H1`/`H2` naming schemes plus a preregistration supersession
meant "arithmetic x planning PASS" cites a run that never executed.
Correct count is three pairs. `PROCESS-FAIL (citation)`.

No new scaling numbers were produced. 20k -> 50k -> 100k remains open.

---

## 10. DEFECTS -- 18 FOUND, ALL MINE

The classes that actually mattered:

**Theory disagreed with measurement, and the disagreement found a bug.
Every single time.**
- `z/modulus` always 0 -> all 64 labels corrupted at e=0.15
- `is_target` credited TERN(1,4,5) as solving target (1,4)
- RANDOM 18 against a closed form of 35
- `DEL` never cleared bit 0 -> one instance provably unsolvable

**A harness where every arm scores zero is a broken harness, not a
result.** Four times.
- expected answer was class-2 and therefore unreachable
- goals unreachable (`bitof(3)={3}` is not producible)
- `has()` scanned 8 bits while labels reach bit 21
- primitive alphabet spanned labels 1-4 only

**One buffer used as both scratch and persistent state.** Twice. Both
times it produced a convincing null.

**Printing the learned object found what its score could not.** The
induction had a sign inversion -- it stored `dist_after - dist_before`
and then took the `argmax`, so a good edit's negative delta was
discarded. Reading the printed table showed it recommending INS when
the state was too large.

**A missing loop increment is indistinguishable from memory
corruption** when it feeds the output buffer. Now statically linted.

---

## 11. WHAT I GOT WRONG AND RETRACTED

Preserved because the process is the point.

1. **C1621 "scoped credit revises in 0 trials" -- RETRACTED.** Two
   fixed heuristics with zero experience tie it exactly.
2. **"C1541 replaces BR-1" -- TOO STRONG.** Correct: it replaces
   *syntax*-based routing. Routing in general is impossible from types.
3. **"Learned selection fixes the counterexample" -- DOWNGRADED.** A
   working mechanism, not evidence of learning.
4. **Three revision/repurposing arms measured nothing** because their
   worlds could not produce the answer they were testing.
5. **Three of five PHASE 8 controls were degenerate** -- an all-zero
   table defaults to the same answer the induction found, so
   "erased" was not an ablation.

Each retraction came from applying the standing detector to my own
work rather than to legacy work. That is the practice worth keeping.

---

## 12. WHAT IS MOST USEFUL TO CARRY FORWARD

Not a list of mechanisms. Three statements.

**1. Counting is a strong baseline and most "learned selection" work
should be measured against it first.** Four attempts lost or tied to
it. Any future proposal should have to beat `argmax frequency` before
it is interesting.

**2. The missing abstraction is identified, and it is not a mechanism.**
It is something coarser than a raw value and finer than a type, from
which a novel situation can be placed correctly. Types collide;
values memorise. `route_line` and lookup tables are what happens when
this is missing.

**3. Most negative results in this program came from worlds where a
competent procedure already existed and the learner was asked to
replicate it.** The next experiment must be built where no competent
procedure is *available* to be replicated -- otherwise the honest
expected outcome is a tie, and a tie teaches nothing.

Concretely, the next three experiments, in order:

```
A. Argument selection, the gap PHASE 8 named.
   Extend the induced key to include a facts-derived property of the
   CANDIDATE ARGUMENT (does this label appear in the goal?). If that
   closes the gap, the missing piece was argument selection. If it does
   not, the researcher's advantage is the ability to evaluate a whole
   neighbourhood, which is a far more significant finding.

B. A world where competence is DISTRIBUTED.
   No universal structure, so selection has something to select.
   This is a precondition for any selection claim, learned the hard way
   three times.

C. RX-K10, the one pending red-team bar in l3_rx, which is blocked only
   on "a different instance". This session produced many.
```

## 13. L3 STANDING

**L3 = 0.** Unchanged, and I would argue for keeping it there:

* H16v3 was never tested against any of this; per R4 passing it is
  not the objective.
* The substrates are declared minimal reproductions of the audited
  architectural shape, not the frozen 4-op ISA.
* The audit found the canonical learner *more* bridged than the
  program assumed.
* Selection is partly learner-owned, but its scoring rule, its scope
  key, and its argument selection are not, and the mechanism
  demonstrably picks a wrong applicable structure without consequence
  feedback.
* Four consecutive attempts to improve on counting failed.

No promotion claimed. No architecture changed. The contribution of
this session is a narrowed map and a set of lints, not a capability.