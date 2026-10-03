# Retention Experiment: Consequence-Substrate Retention Input

**Verdict: RETENTION-COMPLETE. MIXED.**

Re-teach node cost is NOT cheaper (identical). Query answerability for
forgotten facts is DRAMATICALLY better (20/20 vs 0/20). The retention
record preserves capability without requiring re-learning.

## 1. Design

**Hypothesis (R5):** When a fact is evicted, a provenance-linked
consequence record (key, content, eviction tick, use count) in the shared
substrate makes later re-learning cheaper.

**Mechanism (unfrozen variant):**
- **Write** (`sub_retain`, called from replacement `evict_node`): on FACT
  eviction, overwrite a pre-allocated pool record in place with
  (s, r, o, tick, use_count). Eviction-safe: no allocation, O(N) scan.
  Pool: 32 records, bid 5 (survives pressure). Overwrite-oldest on full.
- **Read (query)** (replacement `ev_query`): after `activate` fails, check
  RETENTION (s,r) before the decline gate. If found, return content
  directly, skip trial/bootstrap/inquiry. Log p0=2.
- **Read (teach)** (replacement `ev_teach`): before alloc, check RETENTION
  (s,r). If content matches, proceed with teach, then restore use count
  as USE edges (capped at 5). Log p0=1 on retention-assisted teach.
- **Namespace:** RETENTION=3, same tag-61 store as PURSUIT/STRATEGY.
  No new tags, modes, bridges, handlers.

**Consequence re-entry:** eviction (action) -> record (outcome) ->
later query reads it -> changed decision (answer vs trial). Fits the
pattern.

## 2. Battery

- PRE: 32 pool records (bid 5). Both arms identical start.
- P1: teach 20 facts (7000+i,40,8000+i).
- P2: 990 fillers. Exactly 20 evictions kill the P1 facts (oldest bid-0).
- CENSUS: verify death, count records, verify content.
- P3: query the 20 forgotten keys. Measure nodes, edges, correctness.
- P4: re-teach the 20 facts. Measure nodes, edges.
- P5: verify hits.

Treatment (RET_ON=1) vs Control (RET_ON=0). 3/3 byte-identical per arm.

## 3. Results

| Metric | Treatment | Control |
|---|---|---|
| CENSUS facts dead | 20/20 | 20/20 |
| CENSUS ret records | 20 | 0 |
| CENSUS content correct | 20/20 | N/A |
| P3 queries correct | **20/20** | **0/20** |
| P3 total nodes (net) | 0 | 0 |
| P3 total edges (net) | -12 | -13 |
| P4 re-teach nodes (net) | 0 | 0 |
| P4 re-teach edges (net) | 12 | 12 |
| P5 verify hits | 20/20 | 20/20 |

3/3 byte-identical. Treatment SHA-256
626717c01d6ecbf61fa312ba1b0de0ddec4b53531a7a98d85eb421ed536f91e6.
Control SHA-256
bbfb391c9bf086bce032af1fea08e2316a298ceaa5dc9746ab9a1c8914bda058.

## 4. R5: Is re-learning cheaper?

**Re-teach nodes: NOT CHEAPER.** P4 node cost identical (0 net at cap).
A FACT needs 1 node; retention cannot reduce this. The budget-pressure
finding (R5 absent) stands for the teach path.

**Query answerability: DRAMATICALLY BETTER.** Treatment answers 20/20
forgotten queries correctly with 0 net nodes. Control answers 0/20;
trial runs and fails. Retention preserves the capability without
re-materializing the fact.

**Trial avoided:** Treatment skips trial entirely for retained keys.
Control pays trial cost (which fails). The saving is in avoided
computation and preserved answers, not in re-teach allocations.

**Use count:** Was 0 (facts not queried before eviction). The bid-restore
path (USE-edge re-creation on re-teach) is implemented but not exercised.
A follow-up with pre-eviction hits would test it.

## 5. MAPs

NOT covered. Retention stores FACT content (s,r,o). MAP executable
graphs (op cells, literals, provenance) are not serialized. A zombified
MAP cannot be restored from a retention record. Honest limitation:
retention works for FACTs only.

## 6. One-System Rule

Holds. MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.
Same tag-61 store; RETENTION is a namespace, not a mechanism.
The decline gate, retention, and (future) abandonment share the store.

## 7. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 4 (RETENTION namespace,
  pool size 32, USE cap 5, overwrite-oldest policy)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (record contents are learner
  state; the mechanism is researcher-designed)
- SOURCE-ENUMERABLE FORMS: 0
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 20 (P3 retention answers)
- REVISION EVENTS: 0
- COGNITION LINES: ~150 added (substrate core reused; retention new)
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0

## 8. Honest limits

1. Re-teach is not cheaper in nodes. The R5 "cheaper to reverse" claim
   is false for the teach path; true for query answerability.
2. Use-count restore not exercised (uc=0 in this battery).
3. MAPs not covered. Graph serialization is future work.
4. Pool is fixed at 32; overwrite-oldest bounds it, but the bound is
   researcher-set, not learner-owned.
5. Source tag on eviction is hardcoded TAUGHT (driver teaches all).
   Provenance architecture would need source on the FACT node.
6. The retention record itself can be evicted (bid 5 delays, not prevents).

## 9. What this means

The consequence substrate earns its keep as a second consumer (after
decline): one generic store improves both decline (CONSOLIDATION.md)
and retention (this report) with zero new storage machinery.

The deeper finding: **forgetting is not the opposite of learning.**
The system can "remember" (answer correctly) without "re-learning"
(re-materializing). The retention record is a compressed consequence
of the eviction, sufficient for query but not for execution.

For lifetime learning: retention input does not bend DYN-1 (re-teach
cost unchanged), but it prevents capability loss from being total.
A forgotten fact is answerable, not gone.

## Constraints honored

Unfrozen variant only; frozen source untouched (rt_base.zag SHA-256
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd
verified). Pure Zag via pinned znc; safebin; `which python3 python`
empty. Zero em dashes byte-verified. Paper untouched. No sealed worlds.
Nothing pushed.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/retention_exp/`:
- `NAMECHECK.md` (Step 0 toolchain guard, scope, constraints)
- `RETENTION.md` (this report)
- `rt_base.zag` (verbatim frozen, hash-verified)
- `rt_retention.zag` (treatment: substrate + retention + replacements)
- `rt_retention_c.zag` (control: RET_ON=0)
- `rt_driver.zag` (battery driver)
- `rt_full_t.zag`, `rt_full_c.zag` (assembled variants)
- `rt_bin_t`, `rt_bin_c` (compiled binaries)
- `rt_t_run1/2/3.txt`, `rt_c_run1/2/3.txt` (3/3 byte-identical per arm)
