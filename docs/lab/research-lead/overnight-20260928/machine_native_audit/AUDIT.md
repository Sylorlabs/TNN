# Machine-Native Audit: C2 (MNSTRESS-1)

Date: 2026-09-30 UTC
Auditor: Machine-Native Audit Worker
Scope: Audit only. No new implementation. No Python. No em dashes.

## Verdict: AUDIT-COMPLETE

## Status at audit time

The C2 worker is still running. Binary built (`/tmp/mns_bin`, 233KB).
State dump produced (`/tmp/mns_d1/state.bin`, 819KB). No result report
committed. No KB1-KB10 measurements available. This audit therefore
assesses the preregistered design against the genuine machine-native
bar, plus current progress. It does not certify measured results.

## What the prereg claims as machine-native

PREREG_MNSTRESS1.md (frozen 2026-09-30) tests a purpose-built epistemic
state engine. The claimed machine-native properties (scale/precision):

1. Exact provenance for every belief (which claims, from which sources)
2. Retention of 500 simultaneous contradictions as UNRESOLVED
3. Dependency-tracked correction propagation
4. Evidence-withdrawal impact analysis (dependency closure)
5. Load-bearing memory identification (sole-support claims)
6. Byte-identical recovery after process restart

The prereg is explicit: "This is a MACHINE-NATIVE claim
(scale/precision), NOT 'TNN is smarter than humans' and NOT an L3
representational-invention claim." It also states: "No human or LLM
comparison scores are claimed here; the human protocol (section 7) is
frozen for FUTURE evaluation only."

## Measured vs claimed

Nothing is measured yet. The table below classifies each preregistered
claim by what it WOULD establish if the kill bars pass.

| Claim | If KB passes | Genuine machine-native? | Assessment |
|-------|--------------|------------------------|------------|
| 1. Exact provenance (KB2: 50/50 exact) | Engine tracks 6000 claims with exact source attribution | YES (weak sense) | A human cannot do this unaided. But any SQL database can. This is database-native, not TNN-native. |
| 2. 500 unresolved contradictions (KB3) | 500 contested slots held open, 0 collapsed | YES (weak sense) | Holding 500 open hypotheses with evidence is beyond unaided human working memory. Genuine scale feat. But again achievable by any system with a table. |
| 3. Correction propagation (KB4) | 40/40 derived beliefs corrected via dependency records | YES (weak sense) | Transitive propagation over a dependency graph is machine-scale computation. Standard in build systems (make) and databases. |
| 4. Withdrawal impact (KB5: 10/10 exact sets) | Exact affected-belief sets on evidence withdrawal | YES (weak sense) | Dependency closure computation. Machines do this; humans approximate. Genuine but standard. |
| 5. Load-bearing memory (KB8 Q7) | Exact set of sole-support claims identified | YES (weak sense) | Graph query. Machine-native in the same sense as any index lookup. |
| 6. Restart recovery (KB7: 50/50 byte-identical) | Serialize, fresh process, reload, identical | NO | Any deterministic program does this. This is a correctness property, not an advantage. Humans do not serialize, so the comparison is vacuous. |
| Latency/RSS metrics (section 6) | ms per query, peak kB reported | NO | Describing execution is not demonstrating advantage. The prereg honestly notes these are VM-observed, not cross-hardware claims. |
| Determinism (KB9: 3/3 byte-identical) | Reproducible outputs | NO | Good engineering. Every deterministic program has this. Not an advantage over anything except nondeterministic systems. |

## The key question

**Does TNN actually exploit being machine-native, or is it just running
on a machine?**

On the evidence of the prereg design: it is just running on a machine.

Every substantive capability in MNSTRESS-1 (provenance store,
contradiction table, dependency graph, withdrawal closure, sole-support
query) is standard database/provenance-system functionality. A
PostgreSQL schema with claim, source, support, contradict, and depends
tables would implement all of it. Nothing in the prereg requires TNN's
specific architecture (white-box rules, concept formation, procedure
learning). The engine's query handlers are authored (prereg section 8
discloses this); the test measures whether authored epistemic
bookkeeping works at 1000-entity scale, not whether TNN learns or
invents anything.

The "machine-native" label is doing rhetorical work that the design
does not cash out. The honest description is: "we built a provenance
tracking system in Zag that handles 6000 claims and 500 contradictions."
That is a real engineering result if the kill bars pass. It is not
evidence of a TNN-specific machine-native advantage.

## Gap analysis: rhetoric vs measured reality

**Rhetoric:** "Machine-native advantage stress test" suggests TNN has
some special edge from being machine-native, relevant to the user goal
of "capability/cost advantages against serious LLM baselines."

**Measured reality (anticipated, pending worker completion):**
Even a clean BUILD-PASS on all 10 kill bars would establish only:

(a) An authored epistemic engine maintains exact bookkeeping at the
    tested scale. This is expected of any correct implementation.
(b) Three ablated baselines (no provenance, collapse contradictions,
    no dependency graph) fail the queries that need the ablated
    machinery. This shows the machinery is necessary for the queries,
    not that it is better than alternatives.
(c) No comparison to humans (protocol frozen for future), no
    comparison to LLMs (explicitly out of scope), no comparison to a
    conventional database (not attempted).

**What would close the gap:**

1. A database baseline. Implement the same 7 query types over the
   same world in SQLite/PostgreSQL. If TNN matches it, the advantage
   is "we can do this in Zag," not "TNN is machine-native." If TNN
   beats it on some dimension (latency, state size, integration with
   learning), that dimension is the actual advantage. Name it.
2. An LLM baseline on the query types. The user goal requires this
   eventually. Q2 (exact provenance) and Q6 (withdrawal closure) are
   the queries where an LLM would likely fail and the engine would
   win. That comparison, when run, is the real machine-native
   advantage demonstration.
3. Integration with learning. The engine is standalone. The user wants
   "traceable beliefs" inside one continuing learner. Until the
   provenance machinery is ported into the unified learner (per the
   Integration Scout's Step B/E), it is a disconnected component.

## Honest scope restatement

IF C2 reports BUILD-PASS, the fair claim is:

"A purpose-built epistemic engine in pure Zag maintains exact
provenance over 6000 claims, holds 500 contradictions unresolved,
propagates corrections through dependency records, computes exact
withdrawal impact sets, and recovers byte-identically after restart.
Ablated baselines confirm each piece of machinery is load-bearing for
its query types. This is bounded engineering, not invention; the
query handlers are authored and the world is synthetic."

The fair non-claim: this does not show TNN beats LLMs, beats humans,
or beats a database at epistemic bookkeeping. Those comparisons are
future work, some explicitly frozen as future protocol.

## Relation to the cost-curve findings

The Cost Curve Worker (COSTS.md, 1945c5e34) measured genuine
inference-cost advantages for the arena contestant: $0 marginal cost,
microsecond latency, determinism, 16KB state, local execution. Those
are real, measured, and relevant to the user goal.

MNSTRESS-1, if it passes, would add: exact epistemic bookkeeping at
scale joins the list of things TNN does cheaply and deterministically.
That strengthens the "traceable beliefs" capability the user named as
an LLM-awkward area. But it does not by itself constitute a
capability/cost advantage against LLM baselines, because the LLM side
of that comparison has not been run (PATH-BLOCKED).

## Files

- This audit: AUDIT.md
- Prereg audited: ../machine_native/PREREG_MNSTRESS1.md
- Implementation (in progress): ../machine_native/mnstress1.zag
- Cost curves: ../cost_curves/COSTS.md
- LLM pathfinder: ../llm_baseline/PATHFINDER.md
- Integration scout: ../integration_scout/INVENTORY.md
