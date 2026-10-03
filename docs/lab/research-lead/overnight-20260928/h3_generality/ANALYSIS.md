# ANALYSIS.md -- H3 Generality Boundary vs H1/H2

## Verdict: H3-GENERALITY-ANALYSIS-COMPLETE

**Recommendation: (b) Retire H3's structure-derived execution in favor of
H1/H2's black-box composition, preserving H3's wiring-discovery strategy
as a search option.**

## 1. Evidence base

All claims below are grounded in committed reports (read verbatim, not
re-run):

| Report | Content | Status |
|--------|---------|--------|
| `xdomain_typed/REPORT.md` | H1 chain to count, 7/7 kill bars | Canonical PASS |
| `xdomain_value/REPORT.md` | H2 chain to count, 7/7 kill bars | Canonical PASS |
| `xdomain_dataflow/REPORT.md` | H3 chain to count, 8/8 kill bars | PROCESS-FAIL (Python in docs check) |
| `xdomain_dataflow_clean/REPORT.md` | H3 clean reproduction, 8/8 kill bars | PROCESS-PASS (canonical) |
| `xdomain_causal_interv/REPORT.md` | H1+H2 on 3rd pair (causal to intervention), 9/9 kill bars, UNMODIFIED logic | Canonical PASS |
| `xdomain_h3_arith/REPORT.md` | H3 on arithmetic to planning, K1/K7 FAIL, white-box diagnosis | Canonical negative |

The causal-intervention report establishes the generality pattern:
**H1 and H2 solve three structurally different domain pairs with
unmodified mechanism logic**: (1) navigation x aggregation, (2)
arithmetic x planning, (3) causal model x intervention planning.

H3 solves pair (1) but **fails pair (2)**.

## 2. The exact failure

From `xdomain_h3_arith/REPORT.md`, the breaking code is `df_exec_sub`
in `df_patch.zag` (verbatim):

```zag
fn df_exec_sub(W:[]u8,map_id:i32,s:i32,fact_rel:i32)i32 {
  let root:i32=ng(W,map_id,20);
  if(root<0){return -2;}
  if(df_has_inc(W,root)==1){
    return df_count_links(W,s,fact_rel);   // TAKEN for SUM MAP
  } else {
    return df_walk_end(W,s,fact_rel);
  }
}
```

The SUM MAPs are pure unrolled INC chains. `df_has_inc` returns 1, so
`df_count_links(W,103,71)` runs. But sum facts are STAR-shaped:
(103,71,6), (103,71,9). The transitive walk finds (103,71,6), then no
(6,71,*), and returns 1. The correct answer (15 = 6+9) requires
summing OBJECT values, which neither branch can express.

Trace:
```
DF-DISCOVER s=103 r=93
DF-STAGE1 proc=0 rel=91 factrel=71
DF-STAGE1 out=1          <-- should be 15
DF-STAGE1 proc=1 rel=91 factrel=71
DF-STAGE1 out=1
DF-NOWIRE
Z ans=-2
```

Three-way comparison on the same pair (from the report):

| Mechanism | Z | Z2 | Principle |
|-----------|---|----|-----------|
| H1 typed contracts | PASS (3 tries) | PASS | Learned signatures prune pair search; black box |
| H2 value composition | PASS (6 tries) | PASS | Ordered pair search over black-box executions |
| H3 dataflow | FAIL (NOWIRE) | FAIL | Structure-derived execution (2-mode) |

## 3. Is H3's structure-derived execution fundamentally limited?

**Yes.** The limitation is architectural, not a missing mode.

H3's execution maps STRUCTURE to EXECUTION METHOD via a fixed
dispatch:

- INC cells present implies count links transitively.
- Otherwise walk the chain to the endpoint.

This assumes computation type is recoverable from graph shape. SUM
breaks the assumption: INC cells are present (mode 1 selected), but
the facts are star-shaped and the answer is value aggregation, not
link count.

**Why adding modes does not fix it:**

A third mode ("star-shaped facts implies sum object values") would
handle SUM. But then:
- MAX over star facts needs mode 4 (same shape, different reduction).
- AVG needs mode 5.
- A weighted sum needs mode 6.

Each new computation type over the same structural shape requires a
new mode. This is the finite-menu treadmill: the dispatch grows one
benchmark at a time, which the constitution explicitly forbids
("never grown one benchmark at a time").

**Why the two candidate repairs dissolve H3:**

1. **General graph executor.** If `t2_exec` worked on stored graphs,
   H3 would not need the heuristic at all; it would just execute.
   But the report notes `t2_exec` returned -999999 on these graphs.
   Fixing that is a deeper architectural change (making executable
   graphs actually executable), and once fixed, H3's distinctive
   "structure-derived" character vanishes; it becomes black-box
   execution like H2.

2. **Learned execution-type classifier.** Instead of INC-presence,
   learn from the procedure's BEHAVIOR what it computes. But this is
   exactly H1/H2's approach (observe inputs/outputs, never inspect
   structure). Adopting it makes H3 into H1/H2.

The fundamental principle: **structure underdetermines computation.**
The same INC-chain graph shape can mean "count links" or "sum values"
depending on fact geometry (chain vs star) and semantic
interpretation. No finite structural heuristic can capture this
without becoming either a full interpreter (option 1) or a behavior
observer (option 2).

## 4. What would it take for H3 to handle SUM, MAX, AVG?

**Minimal honest answer:** H3 would need to stop being H3.

- To handle SUM: detect star-shaped facts, sum object values.
  (Mode 3.)
- To handle MAX: detect star-shaped facts, take max object value.
  (Mode 4. Same shape as SUM; the distinction is semantic, not
  structural.)
- To handle AVG: sum then divide by count. (Mode 5.)

The pattern is clear: each row adds a mode for a (shape,
computation) pair, but shape does not determine computation. The
dispatch table grows without bound while never achieving generality.

**The general solution** is one of:
- (a) Execute the procedure's own graph (needs working t2_exec), or
- (b) Treat the procedure as a black box and observe its behavior
  (this is H1/H2).

H3's contribution was never supposed to be the 2-mode heuristic; it
was the **wiring discovery** (find P with facts from s, execute to
mid, find Q with facts from mid) and the **explicit wiring graph**
as a promotable, reusable record. Those are separable from the
broken execution step.

## 5. Three-mechanism generality comparison

| Dimension | H1 (typed contracts) | H2 (value f(g(x))) | H3 (dataflow) |
|-----------|---------------------|-------------------|---------------|
| Composition principle | Learned I/O type signatures prune pair search | Ordered pair search over executions | Wiring discovery + structure-derived execution |
| Procedure treatment | **Black box.** Signatures from probe observations; structure never inspected. | **Black box.** Direct execution; structure never inspected. | **White box.** MAP structure inspected to select execution method. |
| Pairs solved (unmodified logic) | 3/3: chain to count, arith to plan, causal to interv | 3/3: same | 1/3: chain to count only |
| Failure mode | None observed | None observed | 2-mode heuristic cannot express value aggregation |
| Cognition lines | ~300 | ~250 | ~180 |
| Researcher-owned | Binary NODE/NUM probe kinds; generic contract composition | Mode definitions (CHAIN, COUNT); ordered-pair search | Discovery algorithm; 2-mode dispatch; field12 registry |
| Learner-owned | Signatures, pairs, composite record | Intermediate values, composite record | Registry entries, discovered wiring, promoted record |

**The architectural lesson:** black-box composition (H1/H2)
generalizes because it is representation-agnostic. It never asks HOW
a procedure computes; it observes WHAT it consumes and produces
(H1) or executes it and observes the result (H2). H3 asks HOW and
answers with a 2-branch heuristic that fails on the third
computation type tested.

This is a candidate constitutional principle: **composition should
depend on learned behavior contracts, not on structural heuristics
about how procedures compute.**

## 6. Recommendation

**(b) Retire H3 as a standalone mechanism, with one preservation.**

Retire: H3's structure-derived execution (`df_exec_sub` 2-mode
dispatch). It is fundamentally limited (Section 3), and every repair
path either becomes a mode treadmill or dissolves H3 into H1/H2
(Section 4). Keeping it for "chain-like domains only" (option c)
would preserve a known-bounded special-case engine, violating the
One-System Rule.

Preserve: H3's **wiring discovery strategy** as a search option. The
discover-P-execute-to-mid-discover-Q algorithm is a genuinely
different search strategy from H1's type-pruned pair enumeration and
H2's ordered mode pairs. It found the correct wiring on chain to
count without any type information or mode definitions. As a
pluggable search strategy feeding a black-box executor, it has value.

Preserve: H3's **explicit wiring graph representation** (promoted
record storing P_in_rel and Q_in_rel). This is a cleaner
compositional record than H1/H2's composite MAPs: it names the
wiring, not just the result. It supports the DF-REUSE path
demonstrated in the clean reproduction.

**Concrete next steps:**

1. Do not extend `df_exec_sub` with more modes. Freeze it as a
   negative reference (like SEM was kept as a bounded subsystem):
   an existence proof that structure-derived execution fails at
   the third computation type.
2. Port H3's wiring discovery into the unified composition
   framework as an alternative search strategy, with execution
   delegated to black-box procedure calls.
3. The cross-domain survivor set is H1 + H2. Their 3-pair
   generality with unmodified logic is the strongest composition
   result to date. The next test is a 4th pair designed by an
   independent adversary (per the constitution's L3 bar: sealed
   post-freeze worlds with adversary-designed families).

## 7. What this does not claim

- H1/H2 are not proven fully general. Three pairs is a pattern,
  not a proof. An adversary-designed 4th pair could kill either.
- The binary NODE/NUM type lattice (H1) and the researcher-defined
  modes (H2) are honest boundaries documented in their reports.
  Richer type lattices and mode induction are open work.
- Level 2 (adaptive reuse) and Level 3 (novel intermediate
  structure) composition remain untested for all three mechanisms.
  All current results are Level 1 (exact reuse).

## 8. Deliverables

- `NAMECHECK.md` (toolchain guard, Step 0)
- `ANALYSIS.md` (this file)

Analysis only; no new Zag code, no binaries, no experiments.
All evidence from committed reports read verbatim:
`xdomain_typed/`, `xdomain_value/`, `xdomain_dataflow/`,
`xdomain_dataflow_clean/`, `xdomain_causal_interv/`,
`xdomain_h3_arith/`.

Pure analysis. Paper untouched. Local commit only, nothing pushed.
Zero em/en dashes (byte-verified before commit).
