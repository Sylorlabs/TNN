# HTD-1 PREREG — efficiency & generation style

**Status: DRAFT — NOT FROZEN.** Six of eight debate slices synthesized. Pending:
E-DE* (deliberation economy — worker still running) and the red-team brief
(program-level kill bars — worker still running). **No building until this
document is frozen and committed as frozen.** When frozen, kill bars are binding.

## §0. The two questions (Micah's words)

1. "Human brains took the free lunch" — ~20W, sparse activation, only relevant
   circuits fire. TNN should wake only relevant parts, not leave everything
   awake. How far can deliberate efficiency go?
2. "How does TNN generate — autoregressive, diffusion, all at once? What's its
   style right now?" Honest context: TNN has NO settled generation style. The
   program built cognition (memory, reasoning control, revision, refusal), not a
   decoder. The units program is still deciding what the atoms are. Generation
   style is genuinely greenfield — everything is tested head-to-head.

## §1. Standing laws (apply to every hypothesis, no exceptions)

- Pure Zag. Zero randomness in any AI decision path.
- Byte-identical reruns: same input + same logged state → byte-identical output.
  Determinism failure = disqualification (law, not a bar — no appeal).
- Prereg before building. Kill bars binding. Every fork tested head-to-head.
- Results reported as they resolve, including honest FAILs.
- Evidence committed under `docs/lab/htd-1/` on `tnn-native-lab`.
- Tie-breaks: every tie-break rule is deterministic AND tested in BOTH
  directions; direction-sensitive verdicts are reported as TIE, no win claimed.

## §2. Bar semantics (normalization)

Debate slices used FAIL/KILL inconsistently. Frozen mapping:
- **Hard-kill bar** (briefs labeled KB/KILL): fires once → hypothesis is
  **KILLED**, terminal, binding. No re-entry.
- **Fail bar** (briefs labeled K/FAIL): fires → hypothesis **FAILS** on that bar;
  documented with evidence; one re-entry allowed (fix and rerun once).
- **Law** (determinism, replay): violation → **disqualified**, no appeal.

## §3. Metrics (metrics-referee spec adopted)

- **Primary efficiency metric:** deterministic Zag-instrumented op counts,
  scalar C = Σ wᵢ·nᵢ, fixed taxonomy frozen at prereg, anti-Goodhart rule
  (uncounted computation = invalid run), weights calibrated once.
- **Secondary:** wall-clock (noisy VM — reported, never decisive alone),
  peak memory. Ledger bytes are co-primary for E-LG* only.
- **Generation quality:** canonical battery Proxy A / B / C (see §5).
- **Determinism gate:** R=5 reruns, SHA-256 byte-identity across all scored
  artifacts; "logged state" = serialized memory store + ledger + config
  snapshot restored per run. Any divergence = invalid run; 2 consecutive
  invalids = BLOCKED (not killed — fix the harness).
- **Referee default hard-kill bars** (apply to every generation hypothesis):
  Proxy A score < 0.50 → KILLED; Proxy B < 25/50 → KILLED.

## §4. Baselines (built once by a referee crew, frozen, gate-passing)

- Efficiency: **B0** always-awake deliberation; **B-fixed-stride** (fenced
  fixed-stride routing — the "dumb sparsity" control); **B-wake-none** and
  **B-inverted** negative controls (must score ≈0 / underperform every real
  gate by ≥20 pts net savings — proves the task is nontrivial and the gate
  signal is real).
- Generation: **G-GREEDY** (best-guess emit, zero deliberation); **naive
  verbatim emit**; **fixed-template fill**.

## §5. Proxy tasks

### Canonical generation battery (all generation hypotheses run all three)
- **Proxy A:** 200 held-out 256-byte span reconstructions (pg100 + sqlite3.c);
  score = byte-exact match rate, mean + 10th percentile.
- **Proxy B:** 50 deterministic trace compositions; binary byte-exact scoring.
- **Proxy C:** 200 constrained fills; 30% constraint-check + 40%
  corpus-consistency + 30% exact-match; all checkers are code, no LLM judges.
- Each proxy's proves / does-NOT-prove is documented: A is
  necessary-not-sufficient; B tests plumbing, not poetry; C biases toward
  groundedness by design.

### Slice extension legs (secondary; run after the canonical battery)
- AR slice: HOSR (200 trials, clause/statement units) — kept because AR kill
  bars are anchored to it.
- PA slice: 1,000-passage masked-span set (32–128B masks) + 200-item sqlite
  constraint-generation set.
- CO slice: PROSE-REC (1,000 passages, fixed anchors + 3 named constraints) +
  CODE-REC (300 sqlite functions); G-CO2's 200-item out-of-corpus abstention
  probes; G-CO4's 100-item misfit probes.
- **Dual anchoring:** a hypothesis must pass its own brief's kill bars on its
  brief's proxy AND the referee's floor bars on the canonical battery.

### Efficiency batteries
- **E-SP\*:** CORPUS-QA-60 — frozen 60-question set (30 pg100 / 30 sqlite3.c,
  lookup + discovery split, deterministic ground-truth chunks), frozen
  partition map, S1 and S10 scale legs (S10 = 10 deterministic tagged copies,
  ~900 partitions; workdirs under ~/workspace, never /tmp). E-SP5 runs an
  extended 600-deliberation curriculum (60 × 10 frozen order).
- **E-LG1:** 500-episode debate/revision curriculum on pg100; write()/fsync()
  counts + byte totals + replay byte-compare; 10 kill-restart trials.
- **E-LG2:** 1000-episode runs on sqlite3.c; K ∈ {16, 64, 256} (test all —
  no minimizing).
- **E-LG3:** 1000-episode runs on pg100; H ∈ {64, 128, 256}; 20 forensic
  queries.
- **E-LG4:** verification battery; 50-append staleness trials.
- **E-DE\*:** battery pending the deliberation-economy brief.

### The atom limitation (stated, not hidden)
Unit definitions (chunk/span/unit) are placeholders until the 53
representation arms name the atoms. Bars stay; units swap on rerun. If the
red-team brief sustains the "premature generation testing" objection with a
firable bar, the generation track is narrowed or suspended per that bar —
the prereg will record the ruling explicitly rather than silently proceeding.

## §6. Hypothesis registry with kill bars

### G-AR1 — Deliberative Chunk Commit (sequential)
Every chunk through commit/refuse/rollback; output *is* the ledger.
- K1 fail: per-chunk cost >3× greedy AND fidelity gain <5pp.
- K2 fail: refuse rate >25% (starvation).
- K3 fail: refuse rate <1% AND fidelity <95% (theater).
- K4 fail: citation validity <99%.

### G-AR2 — Span-Tape with Verification Gates (sequential)
Fast planner lays spans (waking only relevant partitions); independent gate
accepts/rejects/escalates.
- K1 fail: gate false-reject >10% on byte-correct spans.
- K2 fail: first-pass accept <85%.
- K3 fail: >10% escalated or any unclosed hole.
- K4 fail: median woken partitions ≥80% (fake sparsity).
- K5 fail: wall-clock ≥ G-AR1 at fidelity ≤ G-AR1.

### G-AR3 — Eliminative Next-Unit Selection (sequential)
Deterministic candidate set (3–7, state-driven, zero RNG); eliminative logic
to one survivor; ties escalate, never silent-pick.
- K1 fail: elimination changes winner vs greedy in <2% of steps.
- K2 fail: no-survivor rollback >10% of steps.
- K3 fail: >20% degenerate rounds.
- K4 fail: cost >4× greedy with fidelity gain <5pp.

### G-AR4 — Cheap Cascade with Checkpoint Backtrack (sequential)
Fast path emits; checkpoints every 8 units verify; failures roll back to the
slow deliberate path.
- K1 fail: total wall-clock ≥ G-AR1 (load-bearing).
- K2 fail: fidelity < G-AR1 − 3pp.
- K3 fail: >5% checkpoints backtrack, or any multi-checkpoint rollback.
- K4 fail: planted-error catch rate <95%.
- K5 fail: >30% of units via slow path.

### G-PA1 — Flag-and-Fix (parallel)
Full skeleton draft, rule-based verifier flags defect regions, deliberative
commit/refuse/rollback repair in fixed order.
- KB1 hard-kill: exact-match <85%.
- KB2 hard-kill: >5% items need >5 sweeps, or any region committed >3×
  (oscillation).
- KB3 hard-kill: cells-touched ≥0.8× autoregressive on same items.

### G-PA2 — Blank-filling fixpoint (parallel)
All-blank tape + anchors; parallel neighborhood-rule fills; verifier
re-blanks violators; stops at true zero-change fixpoint.
- KB1 hard-kill: exact-match <85%.
- KB2 hard-kill: <90% reach fixpoint ≤8 passes, or any cell re-blanked >3×.
- KB3 hard-kill: cell-writes ≥2× autoregressive.
- KB4 hard-kill: ledger bytes >10× output bytes (median).

### G-PA3 — Eliminative drafts (parallel)
N=4 deterministic drafting policies; eliminative challenge battery; one
repair pass per surviving round; preregistered tie-break.
- KB1 hard-kill: winner exact-match <88%.
- KB2 hard-kill: winner − best-single-policy <3pts (selection theater).
- KB3 hard-kill: >10% hit round cap R=6, or >20% resolved by tie-break.
- KB4 hard-kill: total work >4× autoregressive.

### G-PA4 — Frozen checkpoints (parallel)
L1 outline → L2 spans → L3 bytes; each level certified then frozen; repairs
confined to the failing level.
- KB1 hard-kill: exact-match <85%.
- KB2 hard-kill: L1 first-attempt certification <70%.
- KB3 hard-kill: any freeze violation, or budget-fault rate >5%.
- KB4 hard-kill: >15% items need multi-level repairs.

### G-CO1 — Deliberate skeleton, constrained fill (compositional)
Task record → deliberated skeleton committed → regions filled in dependency
order → mechanical weave + verify.
- KB1 hard-kill: PROSE-REC exact-match <80%.
- KB2 hard-kill: planning-phase ops >60% of total while below AR quality.
- KB3 hard-kill: ≥20% items ship with ≥1 violated committed constraint.
- KB4 hard-kill: skeleton survival <40%.

### G-CO2 — Retrieve, then compose (compositional)
Output = cited memory chunks + frozen glue table; byte-exact citation
verifier; coverage <C% → deliberate ABSTAIN.
- KB1 hard-kill: emitted exact-match <75%.
- KB2 hard-kill: assembly ops >30% of total.
- KB3 hard-kill: ANY citation fault (zero tolerance); uncited fill >5% on
  low-coverage probes.
- KB4 hard-kill: emits on >20% of zero-coverage probes (abstain <90%).

### G-CO3 — Plan-verify-emit (compositional)
Eliminative planning commits a generation *program* (RECALL/FILL/WEAVE/CHECK
ops); dumb executor, zero deviation; plans cached as portable chunks.
- KB1 hard-kill: CODE-REC exact-match <80%.
- KB2 hard-kill: planning <60% of first-run ops, or amortized planning share
  ≥35% by item 10.
- KB3 hard-kill: ANY executor deviation (zero tolerance — RC1-analog line).
- KB4 hard-kill: >25% of committed plans fail post-emission verification.

### G-CO4 — Deliberative templates (compositional)
Pre-committed template library (prereg cap 12) + per-slot schemas; slots in
dependency order; no fitting template → explicit TEMPLATE_MISFIT.
- KB1 hard-kill: CODE-REC exact-match <80%.
- KB2 hard-kill: median per-run ops >65% of G-CO1's.
- KB3 hard-kill: slot-schema violations ≥15%.
- KB4 hard-kill: force-fit rate >10% on misfit probes, or library needs >12
  templates.

### Shared efficiency bars (apply to every E-\* hypothesis)
- SH-OVERHEAD fail: gate+dispatch+commit ops ≥25% of gross ops saved.
- SH-RECALL fail: miss rate >5% (>3/60).
- SH-NET fail: total ops ≥90% of B0.
- SH-SCALE fail: S10 per-deliberation gate overhead >12× S1's.
- SH-DET: hard law — any non-byte-identical rerun disqualifies.

### E-SP1 — Per-deliberation selective wake (Micah's core)
Top-64 token-hash signatures per partition; wake iff overlap ≥ τ.
- K1 fail: mean wake fraction >30% at S1.
- K2 fail: no τ achieves miss ≤5% AND net-save ≥10%.

### E-SP2 — Two-tier routing
256-bit zero-false-negative pre-filter (4 u64 ANDs/partition), then deep gate
only on passers.
- K1 fail: ANY tier-1 false negative (zero tolerance, construction guarantee).
- K2 fail: deep gate runs on >20% of partitions at S1.
- K3 fail: tier-1 ops >2% of B0 ops.
- Must beat E-SP1 by ≥3pts net savings at S10.

### E-SP3 — Partition-local deliberation
Reasoning dispatched into woken partitions' local arenas; commits composed
back; attacks merge cost, not scan cost.
- K1 fail: >2/60 answers differ from B0 global deliberation.
- K2 fail: dispatch+commit ops >10% of merge ops saved vs E-SP1.
- K3 fail: any unledgered dispatch or commit.

### E-SP4 — Hierarchical wake
Region gate kills ~7/8 coarsely; chunk gate selects finely inside survivors.
- K1 fail: ANY region-gate false negative (zero tolerance).
- K2 fail: S10 net savings < E-SP1 + 5pts.
- K3 fail: trails E-SP1 by >3pts at S1.

### E-SP5 — Learned wake-masks
Masks are memory, revised by deterministic deliberate revision
(miss→widen, wasted wake→narrow); cold start = E-SP1 exactly.
- K1 fail: cumulative ops don't break even vs B0 within 120 deliberations.
- K2 fail: warmup miss >10% or post-warmup miss >5%.
- K3 fail: ANY mask oscillation within a 60-deliberation window.

### E-SP6 — Sleep-by-default (boundary mapper)
No gate; wake only by explicit citation. Expected to fail SH-RECALL on the
full set — the failure is the finding (boundary map).
- K1: full-set miss reported split by lookup/discovery subsets.
- K2 fail: any wake required a scan (gate ops must verify as exactly 0).
- K3 fail: prereg cannot name the surviving query class in advance.

### E-LG1 — Ledger-write batching
One durable write per episode + episode-open marker; crash → deterministic
re-execution reproduces the batch.
- REPLAY fail: ≥1 byte divergence over 500 episodes incl. 10 kill-restarts.
- SAVINGS fail: write syscalls saved <60% OR bytes >110% of baseline.
- Internal: episode-close vs fixed-count batching — test both.

### E-LG2 — Checkpoint + delta
Full snapshot every K episodes; word-level XOR deltas between; replay =
checkpoint + ≤K deltas. K ∈ {16, 64, 256} — test all.
- REPLAY fail: any byte divergence (1000 episodes + restart trials).
- SAVINGS fail: total bytes >50% of baseline at K=64, or snapshot share >20%.

### E-LG3 — Audit-tiering
Full detail for last H episodes; older compacted to deterministic summaries
(compaction deliberated + ledgered). Honest split: state-replay preserved,
cold stream-replay declared lost in prereg. H ∈ {64, 128, 256} — test all.
- REPLAY-STATE fail: byte-divergent final state.
- SAVINGS fail: bytes >40% of baseline at H=128.
- FORENSIC fail: any of 20 forensic queries differs from baseline.

### E-LG4 — Read-path indexes
Per-slot last-writer / per-episode / op-histogram indexes as pure derived
sidecars; ledger bytes identical with indexes on/off. Attacks the measured
O(n²) free-slot scan.
- fail: ledger byte-compare with/without indexes differs.
- fail: verification battery >25% of baseline ops, or maintenance >10%.
- STALENESS fail: any of 50 appends where an index answer ≠ from-scratch scan.

### E-DE\* — deliberation economy (PENDING brief)

## §7. Head-to-head matrix (merged; no minimizing)

**Generation, cross-family (the architectural forks):**
- Each G-\* vs autoregressive best (G-AR\*) — does any non-sequential family
  beat sequential at all?
- G-PA1 vs G-PA2 — flag-driven sparse repair vs blind full-tape fixpoint.
- G-PA1 vs G-PA4 — flat defect order vs hierarchical level order.
- G-PA2 vs G-PA4 — emergent vs planned convergence.
- G-PA3 vs G-PA1/G-PA2 — selection-among-many vs refinement-of-one.
- G-CO1 vs G-CO4 — per-task skeleton vs reusable template (design-cost).
- G-CO1 vs G-CO2 — deliberated fill vs retrieved fill.
- G-CO1 vs G-PA4 — deliberated skeleton vs fixed-level expansion.
- G-CO2 vs G-CO3 — plan over chunks vs plan over ops.
- G-CO3 vs G-CO4 — generated plans vs pre-committed templates (convergence?).
- G-AR2 vs G-AR4 — sparse partitions vs cheap cascade (efficiency mechanisms).
- G-AR3 vs G-PA3 — elimination rounds vs eliminative drafts (same idea?).
- G-CO3 vs RC1 evidence standard (internal control).
- G-PA3 vs debate-trial evidence standard (internal control).
- Ablations: G-AR2 full-wake; G-AR3 set-size-1; G-CO1 reverse dependency
  order (must change zero bytes).

**Efficiency:**
- M1 E-SP1 vs B0 (S1, S10) — the core claim.
- M2 E-SP2 vs E-SP1 (S10) — does the pre-filter earn its keep?
- M3 E-SP3 vs E-SP1 per split — the predicted crossover is itself a finding.
- M4 E-SP4 vs E-SP1 (S1 and S10) — flat vs hierarchical.
- M5 E-SP5 vs E-SP2 (600-delib run) — learned vs static.
- M6 E-SP6 vs all on recall — any hypothesis within 2pts of E-SP6's
  discovery miss rate has a gating problem.
- M7 negative controls B-wake-none, B-inverted (S1).
- E-LG composition legs: E-LG1×E-LG2, E-LG1×E-LG3, E-LG2×E-LG3,
  E-LG1×E-LG4 — then a full-combination leg if each survives alone.
- E-DE\* matchups pending.

## §8. Verdict rubric

- **PASS:** beats both baselines (where applicable) + all kill bars hold.
- **FAIL:** documented with evidence; one re-entry allowed.
- **KILLED:** loses to both baselines or trips a hard-kill bar — terminal,
  binding.
- Section champions per family; **no overall winner expected**. Overall
  champion only on blowout: ≥2× margin on the other section's home metric
  under BOTH tie-break directions, no hard-kill trips anywhere.
- Scenario-fit mapping required: which hypothesis wins on what workload
  (lookup vs discovery; prose vs code; S1 vs S10).

## §9. Build order (after freeze)

1. Referee crew: op-count instrumentation contract + taxonomy + frozen
   baselines (B0, B-fixed-stride, G-GREEDY, naive emit, fixed-template).
2. Frozen artifacts: partition map, CORPUS-QA-60 set + ground truth,
   canonical battery item lists, mask lists, τ grid, region size, K/H grids.
3. Build crews per hypothesis family (parallel; each in its own
   ~/workspace/htd-1/builds/<id>/ workdir).
4. Results committed per result as they resolve under docs/lab/htd-1/.

## §10. Pending (must resolve before freeze)

1. E-DE\* hypotheses + kill bars + battery (worker running).
2. Red-team program-level kill bars — including the "premature generation
   testing" objection and the "efficiency without a workload" objection.
   If sustained, this prereg records the narrowing/suspension explicitly.
3. Open metric questions from the referee (weight calibration, Proxy C
   novelty bias → deferred to HTD-2 "C-novel", offset-shift sensitivity,
   ≥2× wall-clock/op-count discrepancy appendix rule, cross-section
   fairness).
