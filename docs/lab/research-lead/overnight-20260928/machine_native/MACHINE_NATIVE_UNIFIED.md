# Machine-Native Engineering: Unified Findings (Priorities A, B, C)

Date: 2026-09-30 UTC. Documenter: Machine-Native Documenter.
Scope: document only. No implementation, no new measurements.
All numbers below are quoted from the three committed result reports cited.

## 1. Priority A: Hypothesis populations (HYPPOP-1)

- Report: `hyp_pop/HYPPOP_RESULT.md`, commit `e150624a9`, verdict POP-TESTED.
- Prereg: `a0ca3fd62` (strictly before implementation).
- What: synthetic world of 10 binary variables, 6 true conjunctive causal
  laws, 4 noise variables, 200 episodes x 20 timesteps, one concept shift at
  episode 100. A population of exactly 2,200 competing hypotheses
  (400 singles + 1,800 conjunctions "s1 AND s2 at t predicts dst at t+delay")
  maintained with per-episode incremental evidence updates, per-destination
  top-8 contests after episodes 50/100/150/200 that prune losers, and five
  query types.
- Measured: 205,179 hypothesis-updates applied in 802/1021/892 ms
  (3 runs), ~228k updates/sec, queries 11-14 ms, peak RSS 244-248 kB.
- Baseline: SQLite on byte-identical data (emit_sql mode regenerates the
  world as world.sql). Every baseline output matches the Zag output exactly
  (Q1 top-8 ids/scores, Q2 per-dst best, Q3 trails, Q4 pruned count 0 /
  alive 80, all 5 shift ranks = 1).
- Comparison: ~5x faster incremental feed than SQLite (0.80-1.02 s vs
  3.8-5.0 s wall), ~25x smaller resident footprint (244-248 kB vs ~6.1 MB),
  zero IPC/parse overhead, single 72 kB static binary. Where SQLite wins:
  the feed logic is ~15 lines of declarative SQL versus 637 lines of Zag;
  window-function queries are far more concise; persistence, ACID, and
  ad-hoc queryability that the Zag engine lacks.
- Dynamics findings (information gain beyond the benchmark):
  1. Tautology dominance: delay-0 self-singles are unfalsifiable and win
     every per-destination contest on raw score, occupying all 10 Q2 slots.
  2. Precision-vs-frequency: true conjunctive laws with perfect precision
     (e.g. id 1335: f=23, a=0) were pruned because rare-but-exact hypotheses
     lose to frequent tautologies on raw score. Evidence-count ranking
     without a complexity or tautology guard selects for unfalsifiable
     hypotheses. This connects to the Q4 design note on MDL/compression
     scoring.
  3. Q5 confound disclosed: shift-recovery ranks measured 1,1,1,1,1 because
     the shifted hypothesis ranks first by default in a heavily pruned
     population, not through demonstrated re-ranking. The metric as designed
     is uninformative under these dynamics.
  4. World warts disclosed: delay-0 laws may draw a source equal to the
     destination (stale buffer cell read, deterministic but semantically
     murky); a latent non-termination exists in law generation for dst 0
     with delay 0 under other seeds (frozen seed never triggers it).
- Honest scope (report's own): the hypothesis FORM (conjunctions) is
  researcher-designed; the test measures population maintenance, update
  efficiency, and contest dynamics, not representational invention.
  Bounded engineering result, not an architectural advantage unique to TNN.

## 2. Priority B: Learned-procedure amortization (AMORT)

- Report: `proc_amort/PROC_AMORT_RESULT.md`, commit `2a8d7bf63`,
  verdict AMORT-TESTED.
- Prereg: `bb5491c00` (strictly before implementation).
- What: one learned procedure, D1 = majority(X1,X2,X3), the kept 5-op tree
  from the Q4-reuse BUILD-PASS (b719bb54b), reproduced exactly. Four arms on
  N = 67,108,864 evaluations (2^26; 3 runs per arm; checksums identical
  across all arms and runs: 4223e82e31000000):
  - E1 TREE-INTERP (Zag): generic recursive interpreter over the node table,
    no memoization. 1.92M evals/sec.
  - E2 SIG-LOOKUP (Zag): the learner's own precomputed truth signature,
    out = (slo >> x) & 1 (verbatim node_pred logic from q4_reuse.zag).
    76.4M evals/sec. 39.9x vs E1.
  - E3 COMPILED-DIRECT (Zag): worker-lowered direct expression
    ((x1&x2)|(x2&x3)|(x1&x3)). 23.4M evals/sec. 12.2x vs E1.
  - B1 C-BASELINE (gcc 13.3.0 -O2): same input cycling, same checksum
    recurrence, no SIMD, no tricks. 137.3M evals/sec. 1.8x faster than the
    best Zag arm.
- Honest interpretation (report's own):
  1. Amortization within TNN is real and large: the same learned function
     executes 12x to 40x faster once it leaves naive tree-interpretation.
  2. The learner's own artifact wins inside TNN: E2 is 3.3x faster than the
     worker-lowered expression and is the fastest TNN execution form. The
     Q4 signature mechanism is effectively a compilation to a lookup table,
     and that compilation is essentially free because the signature already
     exists as a learning byproduct.
  3. No TNN-specific execution advantage over conventional code: gcc -O2 C
     beats the best Zag form by 1.8x (F3 falsifier did not fire only because
     the frozen bar was 2x), and beats the identical direct expression in
     Zag by 5.9x (a znc codegen gap, honestly noted, not a TNN finding).
     Compilation is compilation: TNN's edge, if any, is in learning the
     procedure, not in executing it faster than conventional compiled code.
  4. Scope bound: the bitmask form costs 2^k entries and does not scale to
     large input spaces; the compiled direct form is the scalable
     amortization. For this 6-bit task the table wins; the ranking would
     invert where tables do not fit.
- Honest scope: the E3 lowering was worker-performed, not automatic
  compilation by the learner. One procedure, one task shape (bulk
  re-evaluation). Bounded engineering result.

## 3. Priority C: Lifetime experience storage and re-abstraction (LIFEXP-1)

- Report: `lifetime_exp/LIFEXP_RESULT.md`, commit `ce2b8ea93`,
  verdict LIFETIME-TESTED.
- Prereg: `30b016328` (strictly before implementation).
- What: a synthetic lifetime of 40,000 experiences (t, f0..f3 in 0..15,
  a in 0..7, o in 0..15, r in 0..3), deterministic seed 987654321.
  Structure-of-arrays storage plus counting-sort inverted indexes (one
  N-entry i32 arena per feature, per abstraction code). Two frozen
  abstractions: M1 (old) bins coarse (f0,f1); M2 (new) bins coarse (f2,f3).
  The re-abstraction pass recomputes M2 codes for all 40,000 experiences,
  builds M2 code lists, and fills a 16x16 C1xC2 co-occurrence table; M1
  codes and lists are preserved untouched.
- Correctness: Q2 200/200 patterns, Q3a 64/64 M2-bin queries, Q3b 64/64 code
  spot-checks, Q3c co-occurrence row-sums, Q4 50/50 range scans, Q1 checksum
  over 1000 exact recalls, every result equals brute-force ground truth.
  C1_INTACT=1 (old abstraction bit-identical after re-abstraction).
  STATE_BYTES 1642048.
- Baseline: the Zag program emits world.sql / index.sql / reabstract.sql /
  queries.sql; bash + sqlite3 3.45.1 driver times each phase over 3 reps on
  fresh DBs. All 316 labeled query results match the Zag output exactly
  (3/3 reps).
- Comparison (medians, Zag vs serious SQLite): ingest ~57x (18 ms vs
  1021 ms single-transaction; naive per-statement was 12141 ms), index
  ~8.6x (62 vs 533 ms), re-abstraction ~12x (30 vs 357 ms), queries ~7.7x
  (~190 vs 1467 ms for the same 316 queries), all in Zag's favor. Zag peak
  RSS 1824-1828 kB vs SQLite DB file 4403200 bytes (~2.4x smaller).
  Code: ~800 lines Zag (includes utils, engine, SQL emitter) vs ~15 lines
  SQL + ~60 lines bash driver leaning on the sqlite3 engine.
- The re-abstraction pass, the novel piece for priority C, costs one linear
  scan (~30ms for 40k experiences): applying a new abstraction
  retrospectively to a full lifetime is cheap, the old abstraction survives
  intact, and a translation table (C1xC2 co-occurrence) is recorded. This is
  the mechanical substrate any genuine re-grounding would need; the mappings
  themselves remain researcher-authored.
- Scope bound: inverted indexes cost one i32 per experience per indexed
  feature (8 arenas = 1.28MB here). A million-experience lifetime would need
  the S9 eviction/GC work to stay bounded.
- Honest scope (report's own): bounded engineering result, not a TNN-unique
  architectural advantage. The win comes from in-memory layout and zero
  IPC, not from anything TNN-specific. SQLite buys persistence, ACID,
  concurrent access, and an ad-hoc query language; the Zag engine has none
  of those. Engine-vs-engine on a fixed workload, not a system comparison.

## 4. Unified honest assessment (K2)

Pattern across all three priorities. In each case the comparison is a
purpose-built in-process flat-array engine (Zag) against SQLite, a general
relational database, on a fixed workload:

| Priority | Zag advantage (median) | Footprint | What SQLite keeps |
|---|---|---|---|
| A hyp-pop | ~5x feed, exact match | ~25x smaller RSS | ~15 lines SQL, ACID, ad-hoc queries |
| B amort | 12-40x vs own tree interp; C leads best Zag 1.8x | single-digit MB | (baseline was C, not SQLite) |
| C lifetime | ~57x ingest, ~7.7x queries, exact match | ~2.4x smaller | persistence, concurrency, query language |

The wins all come from the same source: avoiding per-statement and
per-query overhead (SQL parsing, planning, B-tree maintenance, IPC) and
running tight loops over flat arrays in one process. That is an
engine-shape advantage, not a TNN-architecture advantage. Any competent
in-process purpose-built engine (C, Rust, hand-rolled) would show the same
shape of win against SQLite on these workloads. The current baselines do
not test that: priority B did use a C baseline and found C ahead of the
best Zag form by 1.8x on identical work, which is the honest upper bound on
what "machine-native" currently buys in execution speed.

What the three results do establish, positively:

- Scale is feasible in-process: 2,200 competing hypotheses with 205,179
  updates under a second; 40,000 full experiences with inverted indexes in
  1.8 MB; learned procedures amortized 12-40x within the learner's own
  machinery.
- The learner's scoring byproduct (truth signature) is its fastest
  execution form, and that compilation is free: a genuine machine-native
  observation about co-locating learning and execution.
- Retrospective re-abstraction of a full lifetime is one linear scan
  (~30 ms at 40k), with the old abstraction preserved intact and a
  translation table recorded: the mechanical substrate for genuine
  re-grounding exists and is cheap.

What they do not establish:

- No TNN-unique architectural advantage. The reports say this themselves,
  three times, in the same shape.
- The baselines are SQLite (a general DB) and, once, C (which won). No
  comparison against a purpose-built conventional in-process engine, which
  is the baseline that would actually test uniqueness.
- Machine-native speed is necessary infrastructure for the continuing
  learner (one learner must hold hypotheses, procedures, and a lifetime of
  experience without resets), but it is not the differentiator against an
  LLM. The differentiator must be cognitive (Criterion 0); speed is the
  enabler.

Limitations carried forward: S9 slot eviction and S10 string-pool GC bound
the fact store; the inverted-index arenas (one i32 per experience per
indexed feature) bound lifetime scale; the signature amortization form
does not scale past small input spaces (2^k entries); the znc-vs-gcc
codegen gap (5.9x on identical expressions) is a toolchain property, not a
research finding.

## 5. What would constitute a TNN-unique advantage (K3)

A TNN-unique machine-native advantage must satisfy all of the following:

1. **Not reducible to engine shape.** The advantage must not be explainable
   as "in-memory beats IPC," "flat arrays beat B-trees," or "purpose-built
   beats general." The current three results all fail this filter, by their
   own honest accounting.
2. **Beats a purpose-built conventional baseline.** The serious baseline is
   not SQLite; it is a purpose-built in-process engine in C or Rust doing
   the same workload. Until TNN beats that, the claim is "competitive
   engine," not "unique advantage."
3. **Comes from TNN's architecture, not from C-with-extra-steps.** The
   advantage must trace to something only the TNN design does: learner
   state and execution co-located in one substrate, white-box provenance
   preserved at execution speed, or execution forms that exist only because
   the learner created them.

Concrete candidate tests that could demonstrate uniqueness:

- **Free compilation by learning byproduct.** Priority B found the hint:
  the signature already exists because learning needed it, so the fastest
  execution form costs nothing extra. A unique-advantage test: a family of
  tasks where the learner's internal artifacts (signatures, indexes,
  recruited operators) are systematically the fastest execution forms AND
  no conventional pipeline produces equivalent artifacts as a side effect
  of its own operation. The bar: total cost (learn + execute) beats
  (conventional learn-then-compile + execute), not just execute-vs-execute.
- **Adaptive execution chosen by the learner.** Execution forms selected
  per usage distribution by the learner itself (table where tables fit,
  code where they do not, mixed forms), re-chosen as usage shifts, with
  total lifetime cost below any single fixed conventional choice. The
  current amortization is worker-lowered and frozen; learner-driven
  selection would be the architectural content.
- **Provenance-preserving execution at zero marginal cost.** The
  machine-native claim from the 13,040-claim stress result (exact provenance
  50/50, corrections 40/40, withdrawals 10/10) is that TNN tracks belief
  lineage natively. A unique-advantage test: execution that carries exact
  provenance and supports correction/withdrawal with no measurable overhead
  versus provenance-blind execution, where a conventional system pays for
  audit logging separately. The bar is measured, not asserted.
- **Integrated learn-execute loop.** One substrate does both learning and
  execution, and the combination beats separated systems on total lifetime
  cost for a continuing learner (new vocabulary, concept learning,
  procedure invention, corrections, memory pressure, delayed reuse, no
  resets). This is the system-level test the mandate actually needs, and
  no current result runs it.

Non-goals, explicitly: beating an LLM on raw throughput is not the claim
being pursued; the mandate asks for capability/cost advantages on the
things LLMs handle awkwardly (persistent one-shot learning, long-lived
corrections, learner-owned memory, traceable beliefs, active inquiry,
invention, structural adaptation). Machine-native speed is the floor under
those claims, not the claim itself.

## 6. Kill-bar check

- K1 (all three documented): PASS. Sections 1, 2, 3 above, all numbers
  quoted verbatim from the committed reports e150624a9, 2a8d7bf63,
  ce2b8ea93.
- K2 (unified assessment): PASS. Section 4.
- K3 (unique-advantage criteria defined): PASS. Section 5: three
  conjunctive criteria plus four concrete candidate tests, with explicit
  non-goals.

Governance: document only; zero Python invocations at any stage (read via
git show, wrote via file tool, committed via git); zero em/en-dash bytes
(byte-verified below before commit); local commit only on tnn-native-lab;
owned path `docs/lab/research-lead/overnight-20260928/machine_native/`
only, pathspec-restricted commits; nothing pushed.

Builder label: NATIVE-DOCUMENTED.
