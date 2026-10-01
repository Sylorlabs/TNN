# Execute-vs-Cache Policy Analysis

**Status:** ANALYSIS ONLY. No source edits, no implementation.
**Source:** frozen `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
(SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`),
read-only.
**Date:** 2026-10-01.
**Question:** one of four semantic decisions forced by FACT/MAP unification
(duality analysis `6fa7dd2ec`, section 2.2). When a unified knowledge node
carries both a cached answer and an executable graph, which one answers
the query?

## 1. The current accident (frozen TNN-2)

### 1.1 Why the FACT always wins

Trace of `ev_query` (source line 813) on a re-query for a promoted (s, r):

1. `activate(W,s,r)` (line 140) runs first. It scans all live nodes for
   `ng(W,n,0)==1` (hardcoded tag-1 check), matches fields 20/24 against
   (s, r), excludes superseded nodes, returns the max-`bid` node.
2. `promote_graph` (line 533) creates the MAP node (tag 20), then line 543
   calls `ev_teach_in(W,s,r,ans)`. This inserts a FACT with the same (s, r)
   and the promoted answer. The shadow.
3. The shadow FACT is the most recent fact for (s, r). It carries an ET_PRO
   (type 9) self-edge from `ev_teach_in`, which protects it from eviction
   and contributes to retention. On the next query, `activate` finds it.
4. `ev_query` returns `ng(W,n,28)` (the cached answer) immediately. The
   trial, the MAP scan, everything downstream never runs.

There is no MAP query path in frozen TNN-2. No function scans for tag 20
to answer a question. MAPs are written by promotion, revised by
contradiction, executed by `t2_try_verify` during construction and by the
test harness, but never consulted at query time. The procedure the learner
just built is dead on arrival as a cognitive resource; only its output
survives, as a memorized triple.

The "policy" is therefore not a decision. It is an accident of ordering:
`activate` runs before anything that could consult a MAP, and the shadow
guarantees `activate` always finds something. Nobody chose cache-over-execute.
The code layout chose it.

### 1.2 The H2 void as a second instance

The H2 evaluation (`72173fe11`) found the same accident one level up: H2
worlds include direct OBSERVE facts for the query (s, r), so `activate`
returns them immediately and the trial never runs. The evaluation intended
to test the trial's verifier; the query path never reached it. This is the
same structural fact: in frozen TNN-2, the fastest exact-recall path
preempts every downstream mechanism, and nothing downstream gets a vote.

### 1.3 Can executing ever give a better answer than the cache?

At promotion time, no: the MAP answer field, the executed value, and the
shadow FACT are all the same number by construction (`t2_try_verify`
executes the candidate; `promote_graph` stores the executed answer and
teaches it as a fact).

After promotion, the two can diverge only through asymmetric updates:

- **Revision (frozen `t2_revise_graph`):** rewrites the MAP answer field
  (line: `ns(W,m,28,out)`) AND teaches a new shadow fact
  (`ev_teach_in(W,s,r,out)`), while contradicting the old shadow. Both
  updated. Still identical.
- **Revision (copy-and-commit variant `880c87c4c`):** retargets the MAP
  root (`ns(W,m,20,croot)`), updates the answer field (`ns(W,m,28,out)`),
  and the observation is taught as a fact on the `ev_observe` path. Both
  updated. Still identical.
- **Contradiction without MAP involvement:** a new fact is taught and the
  old one superseded. The MAP keeps its old answer but is now invisible
  (the shadow path answers from the new fact). Divergence exists but is
  unreachable: `activate` finds the new fact first.
- **Eviction asymmetry:** the shadow FACT is protected by its ET_PRO edge;
  the MAP is not (its ET_COR/ET_USE self-edges are not counted by
  `is_prot`). Under budget pressure the MAP dies first and the shadow
  survives, which preserves behavior. The reverse (shadow evicted, MAP
  survives) would expose the MAP, but the protection asymmetry makes this
  the rarer direction.
- **Eviction corruption:** the white-box inventory (`b17fee225`) found MAP
  roots destroyed during eviction churn (MAP 45's root pointing at a
  literal cell, MAP 82's root hijacked by another MAP's cell). A corrupted
  MAP executed at query time returns garbage or fails. The cached FACT has
  no such failure mode: it is a triple, not a pointer structure.

The critical architectural fact, verified by reading `execute` (line 192):

- The 4-op ISA (101 SETREG, 102 BRANCHEQ, 103 INC, 104 DEC) operates purely
  on the execution frame. `res_op` resolves operands from frame slots.
  **No opcode reads FACTs from the workspace during execution.**
- Graph literals (tag 902 cells) are baked in at construction time from
  construction-time facts (transfer barrier 4, `cbd7bc803`).
- `t2_exec(W,root,s0)` seeds frame slot 0 with the query subject, but the
  graph body replays baked-in values.

Therefore re-executing a MAP **cannot detect staleness**. It is a closed
replay, not a live query against current knowledge. If the world changed
in a way no contradiction captured, the MAP re-executes the old
computation and returns the old answer, exactly like the cache, at higher
cost. Execution is not fresher than caching in this architecture. It is
the same answer with extra steps, plus a corruption risk the cache does
not carry.

**Honest summary of 1.3:** in frozen TNN-2, execute-vs-cache is a
distinction without a difference for correctness. The two agree whenever
both are intact, and where they can disagree (corruption), the cache is
the safer one. The policy question is real only under a different
execution architecture.

## 2. The policy space

### 2.1 Candidate policies

Assuming a unified node (cached answer + executable root), the options:

- **P1 always-cache:** return field 28. Cheapest. The graph is decorative
  except as revision substrate. This is today's behavior, made explicit.
- **P2 always-execute:** run the graph on every query. Exercises the
  procedure, detects execution failure (-999999) and corruption visibly,
  but costs a frame allocation plus up to 1000 interpreter steps per
  query, and returns the same answer as P1 when intact.
- **P3 execute-on-evidence-change:** re-execute only if a DEP-linked fact
  changed since promotion. Requires tracking a per-node freshness
  watermark. In the current closed-replay architecture this is theater:
  re-execution cannot see the changed facts, so the policy spends
  bookkeeping to reach the same answer.
- **P4 execute-on-cache-miss:** the reuse variant's shape (`ea8fc0ac1`):
  MAP-first when no fact exists. This is not execute-vs-cache; it is
  execute-vs-trial. The policy question as posed assumes both exist.
- **P5 learner-owned:** a policy node (H3-lite direction) selects per-node
  or globally, with an exercised write path driven by experience. The
  learner could learn, for example, that executing is wasteful for stable
  relations and that cache hits suffice.

### 2.2 What information the decision needs

A non-vacuous execute-vs-cache policy needs at least one of:

- **Freshness signal:** has anything the procedure depends on changed?
  Requires DEP-edge watermarks plus execution that actually reads current
  state. Frozen TNN-2 has the edges (provenance) but not the read path.
- **Confidence signal:** how reliable is this procedure? `map_standing`
  computes ET_SUP minus ET_CON over post-promotion edges but has no
  reader (dead signal, per the compression audit `471d0e0f3`). A live
  standing signal could gate execution: execute low-standing MAPs to
  check them, trust high-standing ones via cache. This inverts the naive
  intuition (execute the uncertain, cache the certain) and is the only
  candidate policy where execution adds information: not freshness, but
  self-testing.
- **Cost signal:** frame allocation + interpreter steps vs one field read.
  Always favors cache. Any execute policy pays this unconditionally.

In frozen TNN-2, none of the three signals is live. Freshness is
undetectable by execution (closed replay). Confidence is computed but
unread. Cost always favors cache. **There is currently no information on
which a correct execute-vs-cache decision could be based.** Any
source-fixed policy (P1-P4) is either equivalent to today's accident or
theater. P5 (learner-owned) has nothing to learn from until the signals
exist.

### 2.3 Who should decide

- **Source-fixed** is honest only for P1 (always-cache): it names what the
  architecture already does. P2-P4 source-fixed would be researcher
  judgment calls with no discriminating evidence, the kind of fixed
  constant the theater audit (`e0423538a`) warns against.
- **Learner-owned** is the architecturally coherent answer, but it has a
  bootstrapping problem: the learner needs the freshness/confidence/cost
  signals before the policy choice is learnable, and those signals do not
  exist. Building the policy node before the signals is putting the
  decision before its evidence, which is how T1/T2 theater happened
  (nodes exist, nothing reads or writes them meaningfully).
- **Nobody (the current state)** is what the duality analysis identified:
  "the behavior that the duality currently determines by accident must be
  re-determined by choice. Those choices are where the cognitive
  architecture actually lives, and they are currently made by nobody."

Dependency order, stated plainly: execution-reads-state (or rebinding,
barrier 4) first, then freshness/confidence signals, then the policy.
Choosing the policy before the architecture that makes it matter is
premature.

## 3. Tradeoff analysis

| | Cache (P1) | Execute (P2) |
|---|---|---|
| Cost per query | one field read | frame alloc + up to 1000 steps |
| Answer when intact | correct | identical |
| Answer when world changed silently | stale | equally stale (closed replay) |
| Answer when MAP corrupted | n/a (FACT has no pointers) | garbage or -999999 |
| Detects execution failure | no | yes |
| Exercises procedure (keeps it "alive") | no | yes |
| Needs no new signals | yes | no (needs confidence at minimum) |

The tradeoff is asymmetric in a way that favors cache under every
currently-realized condition. Execute wins only on two counts, both
about the procedure's health rather than the answer's correctness:
failure detection and liveness. Those are real values in a long-lived
learner (a corrupted MAP discovered at query time is better than one
discovered never), but they are maintenance values, not cognitive ones.
They do not make the answer better. They make the system more honest
about its own decay.

The case where the tradeoff genuinely matters, and does not exist yet:
**execution that reads current state.** If the graph could consult facts
at execution time (a fact-reading opcode, or literal rebinding at
execution), then execute-vs-cache becomes freshness-vs-cost, the classic
memoization tradeoff, and the policy is learnable from experience
(stable relations → cache; volatile relations → execute). That
architecture does not exist. Barrier 4 blocks it.

## 4. Relation to revision

The copy-and-commit substrate (`880c87c4c`) keeps the MAP answer field
and the shadow fact synchronized on every successful revision (two field
writes on the MAP node; the observation taught as fact on the
`ev_observe` path). Revision therefore does not create an
execute-over-cache case: after a correct revision, both agree.

Revision creates the opposite pressure. The revision substrate's whole
point is that the MAP is mutable state under repair while the FACT is
append-only history. After several revisions, the MAP node has been
retargeted multiple times (V3: root 12→16→20) while the fact lineage has
forked. The MAP is the live object; the facts are its audit trail. In a
unified node this distinction collapses structurally, but the lifecycle
question the duality analysis named (full vs minimal bookkeeping for
promoted nodes) is the same question as execute-vs-cache asked about
time: which representation is primary, the procedure or its outputs?

One concrete interaction: under copy-and-commit, a revision that fails
verification leaves the original MAP untouched and supersedes the
candidate. If the query policy were P2 (always-execute), a query landing
between contradiction and successful revision would execute the stale
graph. Under P1 (always-cache), it returns the stale cached answer. Both
stale; neither worse. The revision window does not discriminate the
policies either.

The blame-assignment analysis (open) may eventually discriminate: if a
composed plan's fragments carry per-fragment confidence, executing the
plan exercises the fragments and localizes failure, while caching hides
it. That is a future architecture's argument for execute, not this one's.

## 5. Verdict

**EXECUTE-CACHE-COMPLETE.**

Findings:

1. The current "policy" is an accident of query-path ordering plus the
   shadow teach. Nobody chose it. (Section 1.1.)
2. In frozen TNN-2's closed-replay execution architecture, executing a
   MAP cannot return a better answer than the cached FACT. The
   distinction is vacuous for correctness; it is live only for cost
   (cache wins) and maintenance honesty (execute wins). (Sections 1.3, 3.)
3. No information currently exists on which a correct policy could be
   based: freshness undetectable by execution, confidence computed but
   unread, cost one-sided. Any policy chosen now is either today's
   accident renamed or theater. (Section 2.2.)
4. Dependency order: execution-reads-state (barrier 4) → signals
   (freshness, confidence) → policy. Choosing the policy first repeats
   the T1/T2 pattern. (Section 2.3.)
5. Revision (including copy-and-commit) keeps the two representations
   synchronized and does not discriminate the policies. (Section 4.)
6. The policy becomes a genuine cognitive decision only if execution can
   consult current state. Until then, the honest source-fixed choice is
   P1 (always-cache), named explicitly rather than arrived at by
   accident, and the learner-owned version (P5) is blocked on signals
   that do not exist.

## 6. Standing architectural metric (this analysis)

| Metric | Value |
|---|---|
| RESEARCHER-OWNED STRUCTURAL DECISIONS | 0 (analysis; the accident itself is researcher-owned) |
| LEARNER-OWNED STRUCTURAL DECISIONS | 0 |
| SOURCE-ENUMERABLE FORMS | 3 assemblers (unchanged) |
| SUF DECISIONS | 0 |
| LEARNER-INTERNAL CRITERIA | 0 |
| REUSE EVENTS | 0 |
| REVISION EVENTS | 0 (analysis) |
| COGNITION LINES | 0 added, 0 modified (read-only) |
| MODES | 0 |
| BRIDGES | 1 (`ev_query` router, unchanged) |
| HANDLERS | 0 |
| SEMANTIC CASES | 0 |

## 7. Explicit non-claims

- This analysis does not recommend a policy. It characterizes why the
  decision is currently vacuous and what would make it real.
- It does not establish SUF, L3, C0-D, or any frozen-battery gain.
- The claim that MAP execution cannot detect staleness rests on reading
  `execute` (line 192): the 101-104 ISA has no fact-reading opcode. If a
  later architecture adds one, this analysis's central finding lapses and
  should be re-done.
- The maintenance-honesty argument for execute (failure detection,
  liveness) is noted as real but non-cognitive; it does not by itself
  justify the cost.
- No implementation is proposed. Section 2.1 lists the policy space for
  gap analysis, not as a work plan.
