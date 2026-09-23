# HTD-1 PREREG — FROZEN 2026-09-21

**Status: FROZEN.** Debate complete (8/8 slices). Kill bars binding. Changes to
rules, metrics, thresholds, or scope require a dated Micah-approved amendment
(standing law). Builds begin only after the referee crew freezes the cost model
(KB-HTD-1.6).

Supersedes `HTD1_PREREG_DRAFT.md` (committed as draft earlier today).

## §0. What changed from the draft (changelog)

1. **Red-team adjudication added (§1).** All seven program-level bars
   KB-HTD-1.1–1.7 adopted with verdicts. The generation-style showdown
   (G-AR1–4, G-PA1–4) is **SUSPENDED** per KB-HTD-1.2 — no units section
   champions exist yet, so emission order/cost/parallelism (atom-relative
   properties) cannot be measured. The debate output is archived as the
   parked test plan, not discarded. Suspension is calendar-independent and
   lifts automatically when champions land.
2. **G-CO\* narrowed to output-gating** (red-team verdict): G-CO2 and G-CO3
   proceed testing only "what must deliberation verify before a candidate is
   released / committed" — atom-agnostic, against settled law. G-CO1, G-CO4
   parked with the generation track.
3. **G-CM1 added — constructed-mode belief gate** (Micah's required
   candidate, recorded 2026-09-21): free elaboration in explicitly marked
   constructed partitions, never committed to the belief store without
   verification. Kill bar: zero leakage of constructed content into factual
   recall. Proceeds as a gating hypothesis (atom-agnostic).
4. **E-DE1–E-DE5 added** (deliberation economy) — proceed narrowed: savings
   measured in FULL COST (deliberation ops + memory-state updates + ledger
   write volume + verification overhead, per KB-HTD-1.5), closed-form cost
   model frozen before building (KB-HTD-1.6), required E-DE2+E-DE4
   composition arm, SKB-SIBLING reclassification rule.
5. **E-SP1–E-SP6 rescoped to relevance-calibration research** (red-team
   verdict): no routing architectures advance without clearing KB-HTD-1.3
   (≥20% total-cost win on ≥500 real deliberative episodes, quality within
   2%). Proxy pilots on CORPUS-QA-60 may run; their data feeds the research
   question (can relevance ground truth be defined on real corpora?).
6. **E-LG1/LG2/LG4 proceed as integrity-gated research** (zero-tolerance
   replay bars intact). **E-LG3 PARKED** as canonical — it explicitly trades
   away cold stream-replay, a law-level tradeoff; fenced experimental arm
   only, pending Micah's dated amendment to the replay law.
7. **Thresholds**: debate-proposed numbers frozen as-is; Micah may amend by
   dated amendment.
8. **E-DE\* open questions ruled**: (a) thresholds per (7); (b) the R3 crew
   freezes the E-DE1 task-class taxonomy and E-DE4 relevance-partition
   declarations before any E-DE build; (c) D-P3's synthetic generator is
   calibration-only — D-P1/D-P2 carry headline weight.

## §1. Program-level kill bars (adopted from the red-team brief)

- **KB-HTD-1.1 (atom-independence gate):** firing test requires re-running
  proxy generation tasks across ≥3 materially different arm families.
  **Verdict at freeze: test not executable** — no settled arm outputs exist.
  The firing test is preserved verbatim in the parked test plan and executes
  when arm outputs exist.
- **KB-HTD-1.2 (champion-availability gate): FIRES.** No units section
  champions → G-AR1–4, G-PA1–4, G-CO1, G-CO4 SUSPENDED until champions land.
- **KB-HTD-1.3 (real-workload efficiency bar):** efficiency architecture
  claims advance past pilot only on ≥20% total-cost win over always-awake on
  ≥500 real deliberative episodes (MA logs, strength-trial traces,
  debate-trace corpora), output quality within 2% of baseline. Below bar →
  PARKED (not killed).
- **KB-HTD-1.4 (transfer-void rule):** a win on workload W must re-measure on
  held-out W' (different deliberation depth, different memory churn);
  transfer gap >50% → claim VOID, hypothesis returns to pilot; two voids =
  PARKED.
- **KB-HTD-1.5 (full-cost accounting):** total cost = compute +
  memory-state updates + audit/ledger write volume + verification overhead.
  Any reported win computed without the ledger term is INVALID (rejected at
  review, not scored as weak).
- **KB-HTD-1.6 (cost-model-first):** closed-form cost model (what counts as
  work, what counts as overhead, always-awake baseline cost on the chosen
  workload) frozen before any efficiency build. Delivered by the referee
  crew as `~/workspace/htd-1/contracts/COST_MODEL_FROZEN.md`.
- **KB-HTD-1.7 (format credibility): does NOT fire.** The efficiency track
  proceeds narrowed; HTD-1's honest output is "one question answered, one
  parked" — a pass under program law, not a failure.

## §2. Standing laws

Pure Zag. Zero randomness in any AI decision path. Byte-identical reruns
(same input + same logged state → byte-identical output); determinism
failure = disqualified, no appeal. Prereg before building; kill bars
binding; test head-to-head, never minimize; report results as they resolve,
including honest FAILs. Bar semantics: hard-kill (KB/KILL-labeled) = terminal;
fail (K/FAIL-labeled) = documented, one re-entry. Tie-breaks tested both
directions; direction-sensitive verdicts are TIEs.

## §3. PROCEEDING hypotheses

### 3a. Deliberation economy — E-DE1…E-DE5 (proceed narrowed)

Shared baseline: **FULL-DELIB** (expand all hypotheses to fixed depth,
gather all evidence in canonical order, run all checks; no caching, budgets,
or early exit; ties by lowest hypothesis id). Shared correctness bar: outcome
agreement with FULL-DELIB (the claim is "the same thought, cheaper" — >2%
divergence kills). Shared savings bar: ≥15% mean saving in FULL COST (not
deliberation ops alone). Standing bars: SKB-REPLAY, SKB-AUDIT, SKB-ORDER,
SKB-SIBLING (savings from routing or ledger bytes reclassified out, not
counted).

- **E-DE1 — task-class deliberation budgets.** Preregistered table maps task
  class → (max expansion depth, max evidence rounds); exhaustion writes
  BUDGET_EXHAUSTED and refuses/petitions (ledgered), never guesses. KB1:
  >2% divergence vs FULL-DELIB → KILL. KB2: <15% full-cost saving → KILL.
  KB3: BUDGET_EXHAUSTED on >10% of items → KILL (table is fiction). KB4:
  any byte divergence → KILL. Head-to-heads: FULL-DELIB; E-DE2; D-P3
  adversarial ordering; flat-budget arm (does task-classing earn its keep?).
- **E-DE2 — early exit on single survivor.** Stops at |live|==1, emits
  SUFFICIENCY_CERTIFICATE (survivor + per-elimination evidence/rule). Sub-arms:
  (a) naive exit; (b) revival-guarded exit (preregistered monotonicity check).
  KB1: >2% divergence → KILL; arm (a) additionally killed if >5% divergent on
  D-P3 adversarial while (b) stays ≤2%. KB2: <15% saving → KILL. KB3: any
  certificate failing replay → KILL. KB4: byte divergence → KILL.
  Head-to-heads: FULL-DELIB; E-DE1; arm (a) vs (b); D-P3 all orderings.
- **E-DE3 — lazy verification with verification debt.** Load-bearing checks
  now; archival checks deferred as ledgered VERIFICATION_DEBT IOUs; consuming
  a debted outcome forces settlement first (zero tolerance); per-episode debt
  cap with forced settlement on exceed. KB1: settled debt overturning outcome
  counts as divergence; >2% → KILL. KB2: <15% saving → KILL. KB3: any
  consume-without-settle or cap exceedance without forced settlement → KILL.
  KB4: byte divergence → KILL. Head-to-heads: FULL-DELIB; E-DE5 (deferral vs
  narrowing); trigger-sensitivity arms (aggressive vs conservative
  load-bearing classification); debt-cap=0 arm (must reproduce FULL-DELIB
  byte-identically — instrumentation sanity).
- **E-DE4 — deliberation memoization.** Cache keyed by (input-hash,
  relevant-state-hash); CACHE_HIT ledger entries point at originating
  episode; relevance partitions preregistered per task class. KB1: ANY false
  hit → KILL (zero tolerance — proves the relevance declaration unsound).
  KB2: <15% saving or <10% hit rate on duplicate-enriched workload → KILL.
  KB3: any CACHE_HIT replay diverging from originating episode → KILL. KB4:
  hostile hash-collision arm — any hit (rather than miss) → KILL.
  Head-to-heads: FULL-DELIB; narrow vs broad relevance scoping; E-DE1;
  hostile-collision arm (mandatory safety case).
- **E-DE5 — proposal-first deliberation.** Frozen cheap heuristic proposes a
  ranking; deliberation verifies in proposal order; the heuristic never
  decides alone. Sub-arms: (a) verify-proposal-only; (b) proposal-ordered
  elimination. KB1: >2% divergence → KILL; arm (a) killed if it saves no more
  than (b). KB2: <15% saving → KILL. KB3: heuristic cost >5% of full
  deliberation → KILL. KB4: byte divergence → KILL. Head-to-heads:
  FULL-DELIB; arm (a) vs (b); E-DE2; degraded-heuristic arm
  (graceful-fallback); random-proposal control (heuristic must earn its keep).
- **Required composition arm: E-DE2+E-DE4 stack** vs FULL-DELIB and vs each
  alone on D-P1/D-P2. Prediction: sub-additive savings. If the stack
  diverges more than either alone → "do not compose" annotation on both.
  Optional: E-DE1+E-DE3 if bandwidth allows.

Batteries: D-P1 (600 pg100 passages, 4-play attribution), D-P2 (600 sqlite3.c
functions, 8-subsystem classification), D-P3 (synthetic adversarial evidence
orderings — calibration-only). Advancement past pilot requires KB-HTD-1.3 on
the real-workload corpus (≥500 real deliberative episodes).

### 3b. Output gating — G-CO2, G-CO3 (narrowed), G-CM1 (new)

The claim is strictly "what must deliberation verify before release/commit" —
no generation-style comparison, no atom assumptions.

- **G-CO2 — retrieve-then-compose gating.** Output = cited memory chunks +
  frozen glue table; byte-exact citation verifier; coverage below threshold →
  deliberate ABSTAIN. KB1 hard-kill: emitted exact-match <75%. KB2 hard-kill:
  assembly ops >30% of total. KB3 hard-kill: ANY citation fault (zero
  tolerance); uncited fill >5% on low-coverage probes. KB4 hard-kill: emits on
  >20% of zero-coverage probes (abstain <90%). Probes: 200-item out-of-corpus
  abstention set.
- **G-CO3 — plan-verify-emit gating.** Eliminative planning commits a
  generation program (RECALL/FILL/WEAVE/CHECK); dumb executor, zero
  deviation. KB1 hard-kill: CODE-REC exact-match <80%. KB2 hard-kill:
  planning <60% of first-run ops or amortized planning ≥35% by item 10. KB3
  hard-kill: ANY executor deviation (zero tolerance). KB4 hard-kill: >25% of
  committed plans fail post-emission verification.
- **G-CM1 — constructed-mode belief gate (Micah's required candidate).**
  Two partitions: CONSTRUCTED (free elaboration, explicitly tagged entries)
  and BELIEF (committed knowledge). Elaboration/hypothesis runs freely in
  CONSTRUCTED; promotion to BELIEF requires deliberate verification via
  commit/refuse/rollback; factual recall reads BELIEF only. Falsifiable
  predictions: (P1) zero constructed-tagged content in factual recall; (P2)
  planted falsehoods in constructed mode refused promotion ≥99%; (P3)
  legitimate verified-true constructions promote ≥90% (the gate is a filter,
  not a wall). KB1 hard-kill: ANY constructed content in factual recall
  (zero tolerance — the named kill bar). KB2 hard-kill: planted-false
  promotion rate ≥1%. KB3 fail: legitimate promotion <90%. KB4 hard-kill:
  any untagged constructed content (tagging integrity). Proxy: 500
  constructed-mode elaboration episodes (pg100/sqlite prompts) + 500
  factual-recall probes incl. planted true/false items; leakage measured by
  byte-exact recall-path audit.

### 3c. Sparse routing — E-SP1…E-SP6 (relevance-calibration research)

Research question (no architecture claims): can relevance ground truth be
defined on real deliberative corpora such that an oracle predicts which state
mattered to outcomes? Method: instrument real runs (MA logs, strength-trial
traces, debate traces); label partitions by counterfactual contribution
(ablate-and-replay: removing which partitions changes outcomes?). Proxy
pilots on CORPUS-QA-60 (60 frozen questions, lookup/discovery split,
deterministic ground-truth chunks; S1/S10 legs) feed the same question. The
per-hypothesis bars (wake fraction ≤30%, miss ≤5%, overhead <25% of gross
saved, net ops <90% of B0, S10 gate ≤12× S1) are retained as the pilot
scorecard. **No wake/sleep mechanism advances to an architecture claim
without clearing KB-HTD-1.3.** E-SP6 (sleep-by-default) runs as the
boundary-mapping study it already is.

### 3d. Ledger economy — E-LG1, E-LG2, E-LG4 (integrity-gated research)

Framed as integrity research (can cheaper encodings preserve
replay-to-exact-state?), never as cost-cutting. Zero-tolerance replay bars
intact; full-cost accounting per KB-HTD-1.5 (the "saving" is ledger bytes;
compute + verification overhead of the encoding counted against it).

- **E-LG1 — write batching.** One durable write per episode + episode-open
  marker; crash → deterministic re-execution reproduces the batch. REPLAY
  fail: ≥1 byte divergence over 500 episodes incl. 10 kill-restarts.
  SAVINGS fail: write syscalls saved <60% OR bytes >110% of baseline.
  Internal: episode-close vs fixed-count batching — test both.
- **E-LG2 — checkpoint + delta.** Snapshot every K episodes; word-level XOR
  deltas between. K ∈ {16, 64, 256} — test all. REPLAY fail: any byte
  divergence. SAVINGS fail: bytes >50% of baseline at K=64 or snapshot share
  >20%.
- **E-LG4 — read-path indexes.** Pure derived sidecars (per-slot last-writer,
  per-episode, op-histogram); ledger bytes identical with indexes on/off
  (attacks the measured O(n²) free-slot scan). Fail: ledger byte-compare
  differs; verification >25% baseline ops or maintenance >10%; STALENESS
  fail: any of 50 appends where an index answer ≠ from-scratch scan.
- **E-LG3 — PARKED** (law-level tradeoff: loses cold stream-replay). Fenced
  experimental arm only, explicitly non-canonical, pending Micah's dated
  amendment to the replay law.

### 3e. Metrics spec — PROCEEDS

The closed-form cost models are the load-bearing deliverable for every
future htd flow. Referee crew freezes the taxonomy, weights, ledger term,
and baseline costs (KB-HTD-1.5/1.6) before any efficiency build.

## §4. PARKED track — generation styles (test plan archived)

G-AR1–4, G-PA1–4, G-CO1, G-CO4: SUSPENDED per KB-HTD-1.2. The 8 debate briefs
plus the canonical Proxy A/B/C battery definitions are the parked test plan;
the KB-HTD-1.1 firing test executes when arm outputs exist. Nothing is
discarded. A crew polishes the parked plan into runnable form (P1 below) so
the track can start the day champions land.

## §5. Baselines (built once by the referee crew, frozen, gate-passing)

B0 (always-awake deliberation), FULL-DELIB (no-economy deliberation
pipeline), B-fixed-stride (fenced), B-wake-none / B-inverted negative
controls, naive verbatim emit + fixed-template fill (for the parked track).

## §6. Batteries and frozen artifacts (R3 crew)

CORPUS-QA-60 + ground truth; D-P1/D-P2 item lists (byte offsets);
D-P3 generator (committed); real-workload corpus (≥500 real deliberative
episodes from MA logs, strength-trial traces, debate traces); τ grid;
K/H grids; E-DE1 task-class taxonomy; E-DE4 relevance-partition
declarations; G-CM1 probe lists; out-of-corpus abstention probes.
All under `~/workspace/htd-1/`; workdirs under `~/workspace`, never /tmp.

## §7. Verdict rubric

PASS (beats baselines where applicable + all bars hold) / FAIL (documented,
one re-entry) / KILLED (terminal, binding) / PARKED / VOID (KB-HTD-1.4) /
INVALID (KB-HTD-1.5). Section champions per proceeding family; no overall
winner expected; overall champion only on blowout (≥2× margin on the other
section's home metric under both tie-break directions, no hard-kill trips).
Scenario-fit mapping required for every surviving hypothesis.

## §8. Build order

1. **Foundation crews (parallel, now):** R1 cost-model contract; R2
   baselines + determinism harness (R=5, SHA-256); R3 frozen artifacts;
   P1 parked-plan polish; E-SP-R relevance-calibration design.
2. **On R1/R2/R3 landing:** E-DE1…E-DE5 crews + E-DE2+E-DE4 composition;
   E-LG1/LG2/LG4 crews; G-CO2/G-CO3/G-CM1 gating crews; E-SP proxy pilots.
3. Results committed per result as they resolve under `docs/lab/htd-1/`;
   reported to Micah as they resolve, including honest FAILs and fired bars.
