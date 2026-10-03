# Genuine Advantage Scout: ADVANTAGE-MAPPED

Date: 2026-09-30 UTC.
Worker: Genuine Advantage Scout.
Scope: Analysis only. No implementation. No Python. No em dashes.

## Verdict: ADVANTAGE-MAPPED

## Sources (all committed)

- Cost curves: `cost_curves/COSTS.md` (1945c5e34). Measured arena costs, flat curve, qualitative LLM comparison.
- Database baseline: `db_baseline/COMPARISON.md` (d874c0de4). SQLite implements all 7 C2 query types in 288 lines, microseconds per query.
- Machine-native audit: `machine_native_audit/AUDIT.md` (48f9765b5). Prereg claims are database-native, not TNN-native.
- LLM pathfinder: `llm_baseline/PATHFINDER.md` (690dfff84). LLM baseline PATH-BLOCKED (no credential, no spend authorization).
- Arena: 0.676 (46/68) as of `9211de19e` / paper commit `c4de31ca2`. Ten of sixteen capabilities nonzero; six at zero.
- Integration Step B: `integration_step_b/BLOCKED_REPORT.md` (9848741e3). Unified learner cannot absorb causal machinery; architectural incompatibility.
- DDES: `ddes/` (56db8d606). BUILD-PASS, strong L2 guided generation, not L3.
- Invention economics: `invention_econ/` (9ac23932b). Schemas amortize; instances do not.

## Part 1: Measured wins (with sources)

### W1. Zero marginal inference cost
Measured: TNN contestant runs at $0.00 per run, 3/3 runs. LLM side is estimate only (no baseline exists): roughly $3 to $5 per run, $10 to $15 for three runs (COSTS.md, PATHFINDER.md).
Would a rational user care? Yes, conditionally. The compounding is real at high volume, but only for tasks inside the capability envelope (see Part 3). Outside the envelope the comparison is moot.

### W2. Determinism (3/3 byte-identical)
Measured: md5-verified byte-identical outputs across 3 runs, repeatedly (arena v1/v2/v3, DDES, cxconstruct, autosci). LLMs have sampling variance and serving nondeterminism.
Would a rational user care? Yes. Audit, testing, regulated environments, and reproducibility are qualitative advantages, not just cost. This is the strongest non-cost win.

### W3. Local execution
Measured: the contestant is a local binary. No network calls, no API keys, no rate limits, no provider outages. Network egress exists in this environment but the contestant uses none of it.
Would a rational user care? Yes. Offline operation, air-gapped deployment, private data that must not leave the machine, and reliability independent of providers are real requirements for some users.

### W4. State efficiency (16KB)
Measured: the full 53-exposure memory lives in 16384 bytes of persistent state, constant across v1 to v4. An LLM would need its full context window (100K+ tokens) to hold the same exposures, at roughly $0.30 to $0.60 per run just for context (COSTS.md).
Would a rational user care? Yes for long-lived memory at scale. A 16KB state file that survives restarts byte-identically is a genuinely small artifact.

### W5. Latency (microseconds per turn)
Measured: cpu_ms below measurement resolution; seconds total for 131 turns. LLM estimate: 1 to 5 seconds per turn, 2 to 10 minutes per full run.
Would a rational user care? Yes for interactive or real-time use. A 1000x latency advantage is real where it applies.

### W6. Flat cost curve (mechanisms, not resources)
Measured: score 0.352 to 0.676 with +20KB RSS total and zero state growth. Gains came from bugfixes and mechanisms, the inverse of LLM scaling (COSTS.md).
Would a rational user care? Indirectly. It means capability gains do not demand bigger machines. Architecturally interesting; not a direct user-facing benefit.

### W7. White-box traceable state
Measured: DEVINT1 exposes lexicon counts, concept counts, rule stores, contradiction records; DDES derives plans analytically from hypothesis structure; the cxconstruct filter was ablated to show correctness-criticality (4/4 to 0/4 without it).
Would a rational user care? Partially. The user named "traceable beliefs" as an LLM-awkward area. But with no LLM baseline, superiority is unmeasured, and W7 shades into research rather than product.

## Part 2: Non-wins (claims that do not survive scrutiny)

### N1. "Machine-native" epistemic bookkeeping
Killed by the database baseline (d874c0de4): SQLite implements all 7 C2 query types in 288 lines of SQL, 65 microseconds per lookup, 0.8 ms per recursive withdrawal query, with ACID guarantees. The TNN reimplementation would be slower, longer, and less robust.
Verdict: database-native, not TNN-native. A rational user who needs exact provenance and withdrawal analysis uses SQLite, not TNN. The audit (48f9765b5) is confirmed.

### N2. Restart recovery as an "advantage"
Any deterministic program serializes and reloads. This is a correctness property, not an advantage over anything except nondeterministic systems. (Determinism versus LLMs is W2 and stands; determinism versus databases is table stakes.)

### N3. Capability breadth
TNN: 0.676 (46/68), ten of sixteen capabilities nonzero, six at zero: inquiry (C8), causal (C9), procedure (C10), transfer (C12), autonomous goal (C15), language (C16). A frontier LLM would very likely score far higher on first attempt; unmeasured, but near-certain given pretraining generality.
This is the dominant reason a rational user chooses the LLM. All of W1 through W5 are conditional on the task being inside the envelope.

### N4. Development cost
Each TNN capability required researcher design, preregistration, implementation, determinism testing, and adversarial review: weeks of skilled labor per capability. An LLM gets aimed at a new task by prompting: minutes.
For any task outside the envelope, the rational move is prompting an LLM, not funding a research program.

### N5. "One continuing learner"
Integration Step B is BLOCKED (9848741e3): the unified learner (2 variables, flat 16-rule causal store) cannot absorb the validated causal machinery (3 variables, episodes, contests) without a redesign. The scout's Steps A through J assumed compatibility that does not exist. The "one learner" is further away than the inventory suggested, and G2 may be a false gap.
A rational user evaluating "the system" sees a set of components, some stranded, not a product.

## Part 3: The honest comparison

The user's standing question: "Why would a rational user still choose an LLM instead of TNN?"

Measured answers, in order of importance:

1. The LLM can do the task. TNN is at 0.676 with six capabilities at zero, including language, causal reasoning, procedure learning, transfer, and autonomous goals. Until the LLM baseline runs we cannot quantify the gap, but on breadth it is large.
2. The LLM is cheaper to aim at a new task. Prompting costs minutes; a new TNN capability costs a research cycle.
3. The LLM is general-purpose. TNN's mechanisms (relation store, conflict store, 2-hop lookup) are arena-specific.

TNN's measured wins (W1 through W5) matter only inside the capability envelope. Outside it, they do not enter the decision.

## Part 4: Smallest envelope where TNN wins

All of the following must hold:

1. The task sits inside the ten working capabilities: one-shot facts, delayed fact use, paraphrase, 2-hop compositional queries, corrections, uncertainty handling, representation, long interference survival, conflict tracking, restart recovery.
2. High volume: thousands of runs, so $0 marginal cost compounds against per-query API pricing.
3. Determinism required: audit trails, regression testing, reproducibility, or regulated output where byte-identical reruns matter.
4. Locality required: offline or air-gapped operation, private data, no external API dependency.
5. Latency sensitive: interactive or real-time use where microseconds beat seconds.

The product-shaped core: a deterministic, local, zero-marginal-cost persistent knowledge appliance. It learns facts in one shot, retains corrections, tracks conflicting evidence explicitly (both values kept, conflict reported), answers 2-hop compositional queries, survives restarts byte-identically, all in 16KB of state, microseconds per query, no network.

What it is not: a general reasoner (N3), a database replacement (N1: use SQLite), or a system that invents representations (no L3 anywhere; DDES is strong L2).

Honest size of the envelope: narrow. Roughly "deterministic personal knowledge base with conflict tracking." The moment the task needs language understanding, causal reasoning, procedure learning, transfer, or autonomous goals, the rational user picks the LLM.

## Part 5: Real product or just research?

Answer: mostly research, with a narrow product-shaped core.

The product-shaped core (W1 through W5 inside the ten-capability envelope) is real and measured. It is not nothing: a deterministic offline knowledge appliance with exact conflict tracking and compositional query at zero marginal cost is a thing some users would choose.

But three facts keep the program in the research column for now:

1. No LLM baseline exists (PATH-BLOCKED). We cannot claim the envelope is competitive even where TNN works, because the comparison has not run. The LLM might serve the same nine capabilities with lower total cost once developer time is counted.
2. The envelope is narrow and expensive to expand. Each new capability costs weeks of research labor. The F1 (executable semantics), F2 (autonomous science), and F3 (developmental language) frontiers are open research, not engineering tasks.
3. The components do not cohere. Integration Step B failed on architectural incompatibility. The "one continuing learner" the user requires does not exist as a binary; DEVINT1 and DEVINT2 are separate processes, the causal machinery is stranded, and the arena contestant is a branch.

The genuinely TNN-native research (white-box rules, learned concepts, procedure learning, DDES guided generation, schema persistence economics from 9ac23932b) is the long-term bet. The database-native parts should be SQLite; reimplementing them in Zag is engineering theater.

Recommendation: retire the "machine-native advantage" claim. Claim the measured bundle instead: deterministic, local, zero-marginal-cost persistent memory with conflict tracking. That is honest, measured, and product-shaped. Everything else is research, and should be labeled as such.

## Claim ledger

| Claim | Disposition |
|-------|-------------|
| TNN has zero marginal inference cost | CONFIRMED (measured, $0.00/run) |
| TNN is deterministic (byte-identical) | CONFIRMED (measured, md5-verified) |
| TNN runs locally with no network dependency | CONFIRMED (measured) |
| TNN holds full memory in 16KB state | CONFIRMED (measured, constant across versions) |
| TNN answers in microseconds per turn | CONFIRMED (measured, below resolution) |
| TNN has a machine-native epistemic advantage | KILLED (d874c0de4: SQLite does it in 288 lines, faster) |
| TNN beats LLMs on capability or cost | UNMEASURED (PATH-BLOCKED; no claim permitted) |
| TNN is one continuing learner | FALSE at present (Step B blocked; components stranded) |
| There is a real product here | PARTIAL (narrow appliance core is product-shaped; the program is research) |

## Files

- This report: `docs/lab/research-lead/overnight-20260928/genuine_advantage/SCOUT.md`
