# Arena Contestant Cost Curves: COSTS-MEASURED

Date: 2026-09-30 UTC
Worker: Cost Curve Worker
Scope: Measurement only. No implementation. No Python. No em dashes.

## Verdict: COSTS-MEASURED

## Measured costs (from committed reports)

Three contestant versions ran the frozen CA-2 arena (131 turns, 68 scored
items, 53 exposures). All costs from harness metrics in committed reports.

| Version | Score | Items | examples | tool_calls | cpu_ms | max_rss_kb | max_state_bytes |
|---------|-------|-------|----------|------------|--------|------------|-----------------|
| v1 (8b0f01a9f) | 0.352 | 24/68 | 53 | 0 | ~0 | 3220 | 16384 |
| v2 (0c5b6c631) | 0.573 | 39/68 | 53 | 0 | ~0 | 3224 | 16384 |
| v3 (0f6f1790d) | 0.632 | 43/68 | 53 | 0 | ~0 | 3240 | 16384 |

Sources:
- v1: docs/lab/research-lead/overnight-20260928/arena_tnn_entry/ARENA_TNN_ENTRY_REPORT.md
- v2: docs/lab/research-lead/overnight-20260928/arena_improve/ARENA_IMPROVE_REPORT.md
- v3: docs/lab/research-lead/overnight-20260928/arena_composition/ARENA_COMPOSITION_REPORT.md

## Cost scaling analysis

### The flat cost curve

Score improved 0.352 to 0.632 (+0.280 absolute, +80% relative) while
resource costs stayed essentially flat:

- examples: 53 -> 53 -> 53 (constant; fixed by arena design)
- tool_calls: 0 -> 0 -> 0 (constant; no tools used)
- cpu_ms: ~0 -> ~0 -> ~0 (constant; below measurement resolution)
- max_rss_kb: 3220 -> 3224 -> 3240 (+20KB total, +0.6%)
- max_state_bytes: 16384 -> 16384 -> 16384 (constant; fixed allocation)

### Marginal cost per point

From v1 to v3:
- Score delta: +0.280 (24 to 43 items, +19 items)
- RSS delta: +20KB
- Marginal: ~1KB RSS per additional correct item. ~0.07KB per 0.001 score.

From v2 to v3 (the compositional addition, a genuine new mechanism):
- Score delta: +0.059 (+4 items)
- RSS delta: +16KB (relation store: 64 triples x 48B = 3072B, plus overhead)
- The relation store uses pre-allocated free space within the 16KB state.
  No state allocation increase was needed.

### What drove the improvements

v1 -> v2 (+0.221): Bugfix and format robustness. Two lines of logic.
  Correction events (t:"k") were ignored; now handled. Paraphrase alias
  "fact2" accepted. Zero new mechanisms. Zero resource increase.

v2 -> v3 (+0.059): Genuine new capability (C4 compositional). Relation
  store (64 triples) plus 2-hop inference. Uses existing DEVINT1
  mechanisms (lex_feed, conc_touch, rule_touch). +16KB RSS for the
  relation store code and data. State allocation unchanged.

Key insight: capability gains came from better mechanisms and bugfixes,
not from scaling resources. This is the inverse of the LLM scaling
pattern (more parameters, more data, more compute for more capability).

## Extrapolation: what would 0.8 and 1.0 cost?

### Current zeros (25 items, 0.368 score remaining)

| Cap | Name | n | Status |
|-----|------|---|--------|
| C6 | conflict | 3 | 0.000 |
| C8 | active inquiry | 4 | 0.000 |
| C9 | causal | 3 | 0.000 |
| C10 | procedure | 2 | 0.000 |
| C12 | transfer | 6 | 0.000 |
| C15 | autonomous goal | 1 | 0.000 |
| C16 | language | 6 | 0.000 |

### To reach 0.8 (54/68, +11 items)

Requires adding ~3 of the 7 zero capabilities. Candidates by difficulty:
- C6 (conflict, 3 items): Likely tractable. DEVINT1 has contradiction
  detection (S7). Needs reliability-weighted resolution. Estimated
  cost: similar to C4 (one new store, one handler). +10-20KB RSS.
- C8 (inquiry, 4 items): Requires tool use / question generation.
  No existing mechanism. Harder.
- C12 (transfer, 6 items): Requires cross-domain generalization.
  No existing mechanism. Hardest.

Resource projection for 0.8: RSS 3260-3280KB (+20-40KB from v3).
State may need growth beyond 16KB if new stores exceed free space.
Examples remain 53 (arena-fixed). CPU remains ~0.

The blocker is architectural (missing mechanisms), not resource
scaling. Each new capability needs design, prereg, implementation,
and adversarial testing. Developer effort dominates, not compute.

### To reach 1.0 (68/68, +25 items)

Requires all 7 zero capabilities including:
- C9 (causal): needs DDES or equivalent hypothesis-guided generation
- C10 (procedure): needs procedure invention (F1 frontier)
- C16 (language): needs Zem acquisition (F3 frontier)

These are open research frontiers, not engineering tasks. Resource
cost is unknowable because the mechanisms do not exist yet. The
current 16KB state and ~3.2MB RSS would likely grow, but the binding
constraint is research breakthroughs, not memory.

Honest assessment: 1.0 is not on a cost curve. It is on a research
frontier curve.

## Qualitative LLM comparison

No serious LLM baseline exists (PATH-BLOCKED; see
docs/lab/research-lead/overnight-20260928/llm_baseline/PATHFINDER.md).
The following compares TNN's measured costs against the estimated
costs of running a frontier LLM on the same frozen CA-2 protocol.

### Per-run inference cost

TNN contestant (measured):
- API calls: 0
- Tokens: N/A (no tokenizer; byte strings)
- Dollars per run: $0.00 (local binary)
- Latency per turn: microseconds (in-process)
- Total runtime: seconds for 131 turns
- Determinism: 3/3 byte-identical (md5 verified)

Frontier LLM (estimated from pathfinder):
- API calls: 131 (one per turn, sequential)
- Input tokens: ~150K-300K per full run (131 turns x ~1-2K context)
- Output tokens: negligible (short answers)
- Dollars per run: ~$3-5 (estimate only, at 2026 rates)
- Latency per turn: 1-5 seconds (network + inference)
- Total runtime: 2-10 minutes for 131 turns
- Determinism: No (temperature, nondeterministic serving)

Three runs (as done for TNN determinism check):
- TNN: $0.00, seconds, byte-identical
- LLM: ~$10-15, 6-30 minutes, variance across runs

### Where TNN has a cost advantage

1. **Zero marginal inference cost.** Once built, TNN runs for free.
   Every LLM query costs tokens and dollars. For repeated or
   high-volume use, this compounds.

2. **Determinism.** 3/3 byte-identical outputs. LLMs have sampling
   variance and serving nondeterminism. For applications requiring
   reproducibility, TNN's determinism is a qualitative advantage.

3. **Local execution.** No network dependency, no API key management,
   no data leaving the machine, no rate limits, no provider outages.
   Privacy and reliability advantages.

4. **State efficiency.** 16KB persistent state captures everything
   the contestant learned. An LLM would need its full context window
   (100K+ tokens) to hold the same 53 exposures, at ~$0.30-0.60 per
   run just for context.

5. **Latency.** Microseconds per turn vs seconds per turn. For
   interactive or real-time use, 1000x+ latency advantage.

### Where TNN does NOT have a cost advantage

1. **Capability breadth.** TNN scores 0.632 with 7 capabilities at
   zero. A frontier LLM would likely score far higher on first attempt
   (generalization from pretraining). TNN's cost advantage is moot if
   it cannot do the task.

2. **Development cost.** Each TNN capability required researcher
   design, preregistration, implementation, testing, and adversarial
   review. Weeks of skilled labor per capability. An LLM gets new
   capabilities via prompting (minutes).

3. **Generality.** TNN's mechanisms are arena-specific. The relation
   store does 2-hop compositional queries; it does not do general
   reasoning. An LLM's cost buys general-purpose cognition.

### The honest cost comparison

TNN is cheaper per inference by orders of magnitude ($0 vs $3-5 per
run, microseconds vs seconds per turn, deterministic vs stochastic).

But TNN's capabilities were expensive to develop and remain narrow
(0.632, 9 of 16 capabilities). The LLM's per-query cost buys
capabilities TNN does not have.

The cost advantage is real but conditional: TNN wins on cost for
tasks within its capability envelope, at high volume, where
determinism and locality matter. It does not win on cost for tasks
outside that envelope, because the development cost to expand the
envelope is high and the outcome uncertain.

This is the standard specialization tradeoff, not a free lunch.

## Key question answered

**Does TNN have a cost advantage? Where?**

Yes, on inference: zero marginal cost, microsecond latency,
byte-identical determinism, 16KB state, local execution. These are
measured, not projected.

No, on development: each capability required weeks of researcher
effort. The LLM gets capabilities from pretraining amortized across
all users.

The cost curve is flat because improvements came from mechanisms, not
resources. This is architecturally interesting but does not by itself
constitute a "capability/cost advantage against serious LLM
baselines" until (a) the LLM baseline actually runs, and (b) TNN's
capability envelope expands to cover tasks where the cost advantage
matters.

## Files

- This report: COSTS.md
- v1 costs: ../arena_tnn_entry/ARENA_TNN_ENTRY_REPORT.md
- v2 costs: ../arena_improve/ARENA_IMPROVE_REPORT.md
- v3 costs: ../arena_composition/ARENA_COMPOSITION_REPORT.md
- LLM pathfinder: ../llm_baseline/PATHFINDER.md
