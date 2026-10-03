# REPORT: H-COLLAPSE-1 Composition Collapse into Fragment DFS

## Verdict: COMPOSITION-COLLAPSE-COMPLETE

**The unified mechanism's whole-MAP DFS path is deleted. All composition
routes through the shared type-15 fragment store plus fragment DFS, with
whole MAPs as (m,0,L) marks. Capability matches the unified mechanism on
every battery test (identical segment MAPs and answers), T4B proves the
fragment path is real, and the patch is 38 lines fewer than the unified
420. 3/3 byte-identical. Zero modes/bridges/handlers.**

Date: 2026-10-02. Worker: Composition Collapse Worker (H-COLLAPSE-1, P0).
Prereg: PREREG.md, commit dada745c8 (frozen before implementation).
Branch: tnn-native-lab, local only, nothing pushed.

## Architecture

One composition operation. compose_try first auto-marks every live chain
MAP m as (m,0,L) into the shared type-15 store (deduplicated, structural
walk only, MAP fields 4/8 never consulted). cl_dfs then searches over
FRAG marks only: candidates come exclusively from type-15 edges with
aux != 0 in edge-id order, resolved through cl_fetch, with reuse of the
same (m,start,len) triple excluded per path. No MAP-structural candidate
walk exists anywhere in the composition path.

Predicates ported to fragments:
- C's principle: cl_fetch satisfiability (constraint walk from the
  mark's entry cell through licensing-fact DEP edges).
- A's principle: plen-contract fallback. A fragment's contract is its
  plen len+1; if the structural fetch fails, a real t2_gather path of
  plen len+1 from cur is accepted. Consulted, not a gate.
- B's principle: cb_has_couse on the source MAP orders candidates
  (history-first, then decreasing len, edge-id stable); composition
  successes write type-15 co-use edges (aux = 0) between consecutive
  segments' source MAPs; ev_cq episode facility retained verbatim.

FRAG marks (aux = (start<<16)|len, always nonzero) coexist with B's
co-use edges (aux = 0) in the one type-15 edge space; both consumers
discriminate on aux. Assembly, verification, and promotion are unchanged
from the unified mechanism (per-segment t2_asm_chain, SEQ-link,
t2_try_verify, promote_graph, LINK14 provenance to each segment's source
MAP). ev_query pipeline unchanged: activate -> rebind_try ->
compose_try -> trial -> bootstrap. One compose_try, one call site.
No COMPOSE_MODE.

## Line Counts (kill bar K8)

| Patch | Lines |
|-------|-------|
| Unified un_patch.zag | 420 |
| Collapse cl_patch.zag | 382 |
| **Delta** | **38 fewer (9%)** |

The whole-MAP candidate walk (cc_relseq/cc_satisfy/un_candidates/un_dfs)
is gone; what remains is the store API plus one DFS over marks.

## Test Results

Battery: the 6 unified tests (frozen protocol) plus T4B. SHA-256
4c898771fdaafe79a7bd0c0daa3faf247cbbde742fe7102a945e0e94e0b4ad5a,
3/3 byte-identical.

| Test | Unified | Collapse | Detail |
|------|---------|----------|--------|
| T1 3-struct | PASS 107 | PASS 107 | COMP-SEGS n=3 (13 26 39), identical segment MAPs |
| T2A 4-struct | PASS 109 | PASS 109 | COMP-SEGS n=4 (13 26 39 52), identical |
| T2B 5-struct | PASS 111 | PASS 111 | COMP-SEGS n=5 (13 26 39 52 65), identical |
| T3 cross-domain | PASS 105 | PASS 105 | COMP-SEGS n=2 (27 42), identical |
| T4 partial | FAIL, no false positive | FAIL, no false positive | ans=-2, terminates; no regression |
| T5 no-expected | decline -2 | decline -2 | compose declines cleanly; no regression |
| T4B seeded frags | n/a | PASS 106 | COMP-SEGS n=2 (45 58); seeded (mx,0,3),(mx,1,3),(my,0,2) consumed |

There is no test where the unified mechanism succeeds and the collapse
fails. Segment selection is byte-for-byte identical on T1/T2A/T2B/T3.

## Kill Bar Adjudication

- K1 T1 PASS: PASS (ans=107, same segments as unified).
- K2 T2A PASS: PASS (ans=109).
- K3 T2B PASS: PASS (ans=111).
- K4 T3 PASS: PASS (ans=105).
- K5 T4 FAILS without false positive, terminates: PASS (ans=-2).
- K6 T5 compose declines (-2), terminates: PASS.
- K7 T4B PASSES (ans=106) with seeded sub-fragment marks: PASS.
  The unseeded T4 FAILS, so the seeds are the causal difference.
- K8 cl_patch.zag STRICTLY FEWER than 420: PASS (382).
- K9 3/3 byte-identical stdout: PASS (sha256 match run1..run3).
- K10 audits: PASS (1 compose_try def, 1 call site, 0 COMPOSE_MODE,
  0 modes/bridges/handlers/semantic cases, no whole-MAP DFS remnants).
- K11 pure Zag, toolchain guard recorded: PASS.

All 11 pass. No unified kill bar was weakened: K1-K6 and K10 reproduce
the unified bars at equal strength; K7 is the additional collapse bar.

## Predicate Evidence

- **C's fetch** did the selection work in all passing tests (segment
  MAPs 13 26 39 / 52 / 65 and 27 42 match the unified run exactly).
- **A's contract** is live as the OR fallback in cl_satisfy (fires when
  the structural fetch fails); it did not need to fire on this battery,
  expected since all MAPs here are pure chains.
- **B's history** is live in both directions: episodes wrote co-use
  edges, candidate ordering consults them (aux==0 discrimination), and
  composition successes wrote new co-use edges (probe: couse 1 -> 3
  across a 3-segment composition; frag marks 0 -> 5 from auto-marking).

## Honest Boundaries

1. **T4 partial applicability**: still fails without seeded marks
   (atomic whole-MAP marks only). The collapse does not invent
   sub-fragments; it makes them consumable. Learner-originated marks
   remain a follow-up hypothesis (as in H-DECOMP-1).
2. **T5 unsupervised**: still requires expected-answer; compose_try
   declines cleanly on expected<0.
3. **Marks are auto-derived, not learned**: (m,0,L) marks are written
   deterministically from MAP structure at compose time. This is the
   collapse step itself (whole MAP = (m,0,L) fragment), not a claim of
   learner-originated decomposition.
4. **Search cost**: same 8-segment bound and edge-scan profile as the
   unified mechanism; the auto-mark pass adds one structural walk per
   live MAP per compose call (deduplicated).
5. The 9% line reduction is modest in absolute terms; the architectural
   win is the deletion of the second search path (one candidate
   source, one DFS), which is what makes T4-style fragments a store
   question rather than a mechanism question.

## Files

- `PREREG.md`: frozen preregistration (commit dada745c8, committed
  before implementation)
- `NAMECHECK.md`: toolchain guard, build records, audits, probe
- `REPORT.md`: this file
- `cl_patch.zag` (382 lines): the collapsed mechanism
- `cl_driver.zag`: the 7-test battery driver (6 unified + T4B)
- `cl_full.zag` (2379 lines): base + patch + driver
- `cl_bin`: pinned znc build
- `cl_run1.txt`, `cl_run2.txt`, `cl_run3.txt`: 3/3 byte-identical runs
- `cl_compile.txt`: compile log

## Recommendation

Adopt the collapsed mechanism as the canonical composition operation:
one candidate source (the shared type-15 fragment store), one DFS, all
three predicate principles preserved, fewer lines, identical capability.
The whole-MAP DFS path is deleted, not deprecated. Next composition work
remains T4 (who writes sub-fragment marks: the learner) and T5
(unsupervised verification), both independent of the collapse.
