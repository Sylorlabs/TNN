# REPORT.md -- COMPOSE-LEARNCOMPOSE-1 (Hypothesis C)

Date: 2026-10-03. Worker: COMPOSE-LEARNCOMPOSE-1. Lane:
`docs/lab/research-lead/overnight-20260928/compose_learncompose_1/`.
Branch: `tnn-native-lab`. Non-ledger task.

## Verdict: BUILD-PASS

Hypothesis C (LEARN-COMPOSE: learner-owned composition policy +
contract-defined revision operators) is implemented in pure Zag,
builds cleanly, and passes all frozen kill bars:

- Main battery: 8/8 problems PASS (Q1, Q1b, Q1rev, CHAIN3, FANIN,
  PARTIAL, Q2, CHAIN10), 3/3 byte-identical runs.
- F-C1/F-C3 battery: 4/4 PASS (W1, W2, W3, ADV), 3/3 byte-identical.
- Blind battery: 15/15 PASS (5 relabeled variants x 3 problems),
  3/3 byte-identical. F-C4 (domain-blindness) holds.
- F-C1a (T2<T1): 4<7. F-C1b (T3<T1): 3<7. F-C2 (Q1rev 7<9).
  F-C3 (NEGREC=1, MODE=REVISE on ADV).

Two prereg amendments were filed BEFORE any implementation commit
(AMEND1: FANIN/CHAIN10 hand-trace corrections; AMEND2: injective
adaptation clarification + W3 base move to avoid substrate bug).
No bars were weakened to force a pass; both amendments corrected
hand-traces or clarified ambiguous rules against the frozen spec.

## What C is

C = A's regressive substrate (verbatim copy of BACKCHAIN-1's
search/execution) + a composition memory M (16 entries) keyed by
(kin, kout, contract-code multiset sketch). On each goal:

1. Cold-start is A's algorithm (so C minus memory = A, isolating
   the memory layer).
2. If M has an entry with similarity >= 2 (3=exact, 2=subset,
   1=kind-only), retrieve the best, adapt its program via injective
   contract matching (distinct roles -> distinct ids; unmapped roles
   -> DROP_UNMAPPED repair), and execute.
3. If the adapted program fails, apply revision operators in frozen
   order (R1 SUBST_FAILED, R2 TRUNCATE, R3 SUBST, R4 APPEND), then
   fall back to cold-start.
4. Record successes (succ++) and verified failures (fail++,
   NEGREC=1). Store revised programs as new entries.

C differs from A (memoryless) by learning from experience, and from
B (two-phase dataflow with hash-consed thunks) by using explicit
retrieval + contract-defined repair/revision rather than lazy
suspension/rebind.

## A vs B vs C

| Dimension | A (BACKCHAIN) | B (SUSPEND) | C (LEARN-COMPOSE) |
|-----------|---------------|-------------|-------------------|
| Q1 tries | 7 | 4 | 7 (cold) |
| Q1b (re-query) | 7 (full re-search) | 0 (rebind) | 4 (retrieve) |
| Q1rev (revision) | 9 (full re-search) | surgical | 7 (revise) |
| FANIN | 4 (cold) | 1 (assemble) | 3 (memory+repair) |
| CHAIN10 | 55 | untested (cap 256) | 108 (misfire+cold) |
| Memory | none | thunk DAG | 16-entry program store |
| Simplicity | simplest | moderate | moderate+ |
| Learning curve | none | none (persistence, not learning) | yes (succ/fail, negative evidence) |
| Cross-shape transfer | no | no | yes (FANIN, W3 via sim-2) |

**Generality:** All three solve the tested worlds. C's memory enables
cross-shape transfer (diamond -> fan-in via subset similarity), which
neither A nor B demonstrates. But C's CHAIN10 misfire (108 vs A's 55)
shows retrieval precision is a real limitation.

**Efficiency:** B wins re-query/revision (0/1 vs 4/7). C never beats B
on efficiency and sometimes loses to A (CHAIN10). C's premium is
learning, not speed.

**Simplicity:** A wins (no memory, no retrieval, no revision). C adds
~400 lines for memory/similarity/adaptation/revision.

**Learnability:** C is the only one with a learning curve (succ/fail
counts, negative evidence, revised programs stored). A is memoryless;
B persists but doesn't learn (rebind is mechanical, not adaptive).

**Verdict:** C demonstrates that a learner-owned composition memory
with contract-defined operators can achieve cross-shape transfer and
accumulate negative evidence, but it does not dominate A or B. B
remains best for efficiency; A for simplicity; C for adaptivity. The
three are complementary, not ranked.

## Architecture accounting

New cognition lines: ~450 (lc_mem.zag, lc_rev.zag, minus substrate
copy). New hardcoded semantic cases: 0. New modes/bridges/handlers: 0
(MODE is a reporting tag, not a dispatch). New learner-state
structures: 1 (composition memory M, 16 entries).

Capability-source delta: The memory enables re-query (Q1b 4 vs 7) and
cross-shape transfer (FANIN 3, W3 3), but the substrate (search,
execution) is unchanged from A. The delta is in the memory layer, not
in new cognitive primitives.

## Bounds and limitations

1. **Retrieval precision:** CHAIN10 retrieved a 3-chain for a 10-chain
   goal (sim-2 subset), wasted 53 tries, then fell back to cold-start.
   The similarity function has no notion of "program length" or
   "structural compatibility" beyond contract multisets.
2. **Revision completeness:** R1-R4 cannot extend a chain (no
   prepend/insert operator) or invent new structure. They only
   substitute, truncate, or append.
3. **Memory capacity:** 16 entries, no eviction policy tested. At
   scale, interference and forgetting would need addressing.
4. **Cold-start dependence:** C's cold-start IS A's algorithm. C does
   not improve first-encounter efficiency; it only amortizes over
   re-queries and transfers.
5. **Substrate bug:** Map id 40 collides with the nm counter (pre-
   existing BACKCHAIN bug). Worked around by avoiding id 40; not fixed
   in substrate (out of scope).

## Conclusion

C is a viable third hypothesis: learner-owned composition memory with
contract-defined revision operators. It passes all bars, demonstrates
cross-shape transfer and negative evidence, and is domain-blind. But
it does not subsume A or B. The honest summary: A for simplicity, B
for efficiency, C for adaptivity. The composition frontier needs all
three insights, not one winner.
