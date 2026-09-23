# TNN wave11 · Track 1 · Slice 03 — Deliberation Budget (remaining)

## 1. Slice
State-dependent deterministic variation via a per-episode deliberation budget whose
*remaining* value modulates only expression (elaboration depth, alternative-path
tracing, verbosity), never verdicts, memory decisions, integrity refusals, or
constitutional ledger contents.

## 2. Falsifiable claim
A deterministic budget B_ep, replenished each episode by a lawful function of logged
state and consumed at fixed per-op costs, changes *expression* across budget regimes
while leaving every protected output identical: over 600 episodes (300 high-budget,
300 low-budget, deterministic regime assignment), verdict agreement with the
unlimited-budget control = 600/600, constitutional-ledger hash identical across
regimes given identical protected-state inputs, and replay from logged full state
(including B_rem) reproduces all output byte-identically 600/600 — while trace-node
counts differ ≥2:1 between top and bottom budget deciles (the dial moves expression,
not judgment).

## 3. Design
**Ordering is the safety mechanism.** Each episode runs in two phases: (1) verdict
formation — eliminative logic runs to its own termination criteria, atomic w.r.t.
budget, writing only protected state; (2) expression — receives `(verdict, B_ep)`
and holds no write handle to protected state. Budget can exhaust only in phase 2,
so exhaustion can never change a verdict, only shorten its expression.

```zag
// Prereg constants (fixed before build)
const BASE_ALLOWANCE: i64 = 4096;   // expression steps per episode
const COST_ELAB_NODE: i64 = 64;     // one elaboration / evidence node
const COST_ALT_PATH:  i64 = 256;    // exploring an eliminated alternative in the trace
const COST_TOKEN:     i64 = 1;      // emitted output token
const L_THRESH: [3]i64 = [256, 1024, 2048]; // L1/L2/L3 entry thresholds

fn replenish(ledger: *Ledger, ep: i64) -> i64 {
    // Lawful: deterministic function of logged state. Novelty = count of
    // new context/hypothesis events since last episode, read from the ledger.
    let novelty: i64 = count_new_contexts(ledger, ep - 1, ep);
    return clamp(BASE_ALLOWANCE + novelty * NOVELTY_K, BUDGET_FLOOR, BUDGET_CAP);
}

fn level(rem: i64) -> i64 { // elaboration level 0..3
    if rem >= L_THRESH[2] { return 3; }
    if rem >= L_THRESH[1] { return 2; }
    if rem >= L_THRESH[0] { return 1; }
    return 0;
}

fn express(verdict: Verdict, b: *Budget, trace: *TraceStream, out: *Out) {
    emit_L0(verdict, out);          // verdict + one-line justification: ALWAYS emitted first
    spend(b, L0_COST);              // reserved; cannot fail
    while level(b.remaining) >= 1 && more_elaboration(verdict) {
        if !spend(b, COST_ELAB_NODE) { break; }       // exhaustion -> stop, output stays valid
        emit_node(verdict, trace, out);
        if level(b.remaining) >= 2 && !spend(b, COST_ALT_PATH) { break; }
        emit_alt_path(verdict, trace, out);           // eliminated alternatives: L2+
    }
    log_budget_record(b.ep, b.base, b.base - b.remaining, b.remaining == 0);
    // L0=verdict+1 line; L1=+key evidence; L2=+eliminated alternatives; L3=+full path/counter-considerations
}
```
Budget consumption is deterministic: fixed per-op costs, op counts a deterministic
function of state, one budget record `{ep, base, spent, exhausted}` logged per
episode (constant structure — values vary lawfully, structure never does).
Expression trace lives in a separate **trace stream**, not the constitutional
ledger; the ledger records verdicts, memory ops, integrity decisions, and budget
accounting only. At exhaustion, output is the already-emitted valid L0 core plus
a `[BUDGET-EXHAUSTED]` marker in the trace stream — graceful terse fallback.

**Why adaptive, not arbitrary:** this mirrors human time pressure — less time →
shorter answer, same conclusion. The replenishment rule allocates elaboration to
where deliberative demand (ledger-measured novelty) is highest, conserving it on
routine episodes. Adaptivity is tested, not assumed: the budget arm must beat a
fixed-L2-elaboration control on audit-answer-rate per trace cost (§4, K5).

## 4. Kill bar
Preregistered; any one fires → idea dead as specified:
- **K1 (verdict leak):** verdict agreement with unlimited-budget control < 600/600 → KILL.
- **K2 (protected-state leak):** memory-decision sequence or constitutional-ledger
  hash differs across budget regimes given identical protected-state inputs → KILL.
- **K3 (replay break):** any episode's output not byte-identical on replay from
  logged full state (incl. B_rem) → KILL.
- **K4 (dead dial):** trace-node count ratio (top vs bottom budget decile) < 2:1 → KILL
  (budget modulates nothing).
- **K5 (adaptivity claim):** budget arm audit-answer-rate per trace cost < fixed-L2
  control → adaptivity claim dead; mechanism survives only as variation, not as
  "adaptive".
- **K6 (exhaustion safety):** any budget-exhausted episode missing the L0 core, or any
  integrity refusal losing its standard citation at L0 → KILL.
- **K7 (demand tracking):** Spearman correlation between B_ep and episode novelty
  < 0.5 → replenishment rule recalibrated once; if still < 0.5 → KILL the rule
  (keep constant-budget fallback only if K1–K4 hold).

## 5. Honesty notes
- The trace/ledger split is new implementation surface: a builder bug could leak
  budget-dependence into protected state. K2 exists for exactly this; the split
  must be enforced by phase separation (no write handle), not by convention.
- "Adaptive" is asserted, tested by K5/K7 — if it fails, the mechanism is a
  cosmetic dial, not an effort allocator. That would still satisfy Micah's variation
  goal, but I am not claiming adaptivity until the trial says so.
- Terse fallback risks hiding refusal rationale from human auditors: mitigated by
  always carrying the refusal standard citation at L0 (K6), but auditor-visible
  terseness vs full trace is a real UX cost, not a free lunch.
- Adversarial novelty floods could inflate B_ep (more elaboration) — but budget
  cannot reach verdicts by construction, so exploit value is limited to trace
  verbosity; still worth a probe in t3-integrity-redteam.
- Leans on committed evidence: RC1/RC2/RC3 reasoning control (40/40 at
  1x/10x/100x, docs/lab/ on branch tnn-native-lab) for the phase-separation /
  self-change-gate precedent; wave5/6 integrity results (137/137) for the
  trap battery reused in K1/K6.
- I am NOT claiming this models human cognition — only that the demand→elaboration
  mapping is a deterministic, state-dependent, replayable analogue of time pressure.

## 6. Next build step
Implement the budget accountant + L0–L3 expression gate as a standalone native
module against the existing deliberative-standards harness, then run the
600-episode K1–K4 protocol (verdict agreement, ledger-hash equality, byte-identical
replay, ≥2:1 expression ratio) before wiring it into any production path — the
single run that decides whether the dial is real and the gate is clean.
