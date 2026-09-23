# H5 — Deliberation Depth: Frozen Definition (Phase 1 Spec)

- **Status:** FROZEN SPEC v1 — Phase 1 (definition). No measurement has been run under this spec.
- **Date:** 2026-09-23
- **Crew:** H5 Crew 1 — Depth Definition (Sol + native debate)
- **Parent program:** H5 (deliberation depth vs accuracy; find the knee)
- **Consumers:** H5 harness crew (implements), H5 battery crew (judgment items), H5 red-team (trap + cost attacks)
- **Amendment rule:** any change to §§4–8 requires H5 program coordinator sign-off, a version bump (v1 → v2), and re-measurement of affected legs. See §12.

## §1 Background and standing law

TNN standing law: **"deliberation adapts to state, no fixed think-count."**
"Deliberation depth" was never operationalized or measured. H5 exists to
measure the depth-vs-accuracy curve and find the knee — the point where more
deliberation stops paying.

Hard constraints inherited from program law:

1. **Zero randomness** anywhere in the AI's decision paths. Every rule here
   must be a deterministic function of observable deliberation state, with
   byte-identical reruns.
2. **Pure Zag** implementation by the harness crew. The spec must be
   implementable without floating-point surprises: all thresholds are
   rational numbers on a fixed-point [0,1] confidence scale.
3. **Adaptivity is the law; fixed depths are the controls.** SHALLOW and DEEP
   are fixed-depth controls against which the state-driven ADAPTIVE rule is
   compared — not violations of the law.

## §2 Debate record

### §2.1 Participants and method

Two-leg structured debate was convened:

- **Leg 1 — external second opinion (Sol via UnoRouter).** Brief capped at
  ~2.6KB (under the 5KB limit). Round 1 asked for steelman/rank/propose on
  five candidate operationalizations. A round 2 (red-team of the draft
  schema) was planned.
- **Leg 2 — native deliberation.** This crew runs at subagent depth 2/2 with
  `can_spawn=no`, so no native Muse subagents could be spawned. The native
  leg was conducted instead as explicitly labeled advocate roles
  (MUSE-A/B/C) with cross-examination, worked through in one deliberation
  and recorded verbatim in method (not fabricated as subagent transcripts).

**Sol availability log (honest record):** at debate time (2026-09-23 ~23:30–23:55
UTC) the UnoRouter endpoint was unhealthy: `gpt-5.6-sol` returned HTTP 524
once and `choices: null` (zero completion tokens) three times; `grok-4.6`
returned HTTP 524; the `:free` models returned HTTP 403 (credential not
authorized). A 3-attempt backoff retry for Sol was left running during
drafting (§2.4 records the outcome). Per Micah's standing rule (any listed
model may serve as second opinion; native preferred), the spec below was
converged from the native leg alone, and **the Sol second-opinion pass
remains open**: if Sol returns, its round-1 position and round-2 red-team
are appended as §2.4/§2.5 and may trigger a v2 amendment — but they cannot
un-freeze v1 without coordinator sign-off.

### §2.2 Candidate operationalizations (as briefed)

| ID | Candidate | One-line steelman |
|----|-----------|-------------------|
| A | Deliberation rounds | The only knob the harness can hold exactly constant across items; clean independent variable |
| B | Evidence items gathered | Depth as information footprint, not time: work done, not cycles burned |
| C | Hypotheses considered / eliminated | Kill-board churn: how many contenders were generated and explicitly killed |
| D | Compute / audit-step budget | Substrate-native cost unit; the honest resource-rationality axis |
| E | Confidence-convergence rule | The standing law made operational: stop when the state settles, not when a counter expires |

Failure modes identified (native leg):

- **A:** round boundaries are a harness convention; degenerate no-op rounds
  inflate "depth" without deliberation → needs a round work contract (§6.4).
  Fixed rounds alone don't express adaptivity → answered by making fixed
  levels the *controls* for the adaptive treatment.
- **B:** "one evidence item" is substrate-dependent; counting needs a frozen
  definition per substrate. Confounded by item difficulty unless within-item.
- **C:** requires the judge to explicitly enumerate hypotheses — an
  architectural commitment not every judge variant can meet. Best as a
  recorded measure, not the treatment knob.
- **D:** the harness cannot *hold constant* what it cannot *predict*: the
  same step-budget buys different work on different items. Keep as the
  **cost axis** (observed), not the treatment (controlled).
- **E:** introduces hyperparameters (ε, k) needing principled values;
  confidence must be a real observable, not an inflatable number → must be a
  deterministic function of deliberation state, frozen pre-measurement.

### §2.3 Native role positions and cross-examination

**MUSE-A (rounds advocate).** Depth = number of propose/critique/eliminate
cycles. Implementable exactly; per-round confidence is observable state.

**MUSE-B (evidence/hypothesis advocate).** Depth is work, not time. A round
that gathers nothing is not deep; a round that kills ten hypotheses is.

**MUSE-C (budget/convergence advocate).** The question is resource
rationality. Audit steps are the native cost unit; the adaptive
stop-on-settling rule is the law operationalized.

Cross-examination results (all roles concurring):

1. **A→C:** budget can't be the treatment (not holdable) — conceded; budget
   becomes the observed cost axis, rounds the treatment.
2. **B→A:** empty rounds are not depth — answered by the round work
   contract: a counted round MUST perform ≥1 evidence gather or ≥1
   elimination, else it does not advance the round counter (§6.4). A accepts.
3. **C→B:** hypothesis counting needs architectural commitments — B
   concedes the treatment role; evidence/hypothesis counts become recorded
   dependent measures (§7).
4. **All→E (decisive):** "gain < ε" on *raw* gain would stop deliberation
   when confidence DROPS — but a drop means evidence against the leader,
   i.e. deliberation doing its most productive work. The rule MUST use
   **|gain|** (absolute marginal change): stop only when the state has
   genuinely settled; oscillation (|gain| ≥ ε) keeps deliberating until the
   cap. Unanimous.

### §2.4 Sol round-1 position

**Sol was unavailable during the entire debate window** (6 attempts,
~23:30–23:55 UTC; see Appendix A). The backoff retry script
(`sol_retry.py`, 3 attempts × 90s backoff) confirmed the outage was
persistent, not transient. No Sol position was obtained. The second-opinion
pass is **deferred, not cancelled**: when the endpoint recovers, a Sol
round-1 (position-taking on §2.2) + round-2 (red-team of this schema) may be
run and appended here; if it surfaces a defect, it enters as a v2 amendment
per §12. It does not un-freeze v1 by itself.

### §2.5 Convergence

The five candidates are not five competitors; they are four roles for one
experiment: **rounds = treatment (controlled), audit steps = cost axis
(observed), evidence/hypothesis counts = mechanism traces (recorded),
confidence-convergence = the adaptive treatment (state-driven)**. The schema
(§4) freezes all four in one config.

## §3 Chosen operationalization

**Deliberation depth is operationalized as deliberation ROUNDS** — one round
= one propose → critique → eliminate cycle satisfying the work contract
(§6.4) — with three named levels:

- **SHALLOW** — fixed small round count (control: minimal deliberation).
- **DEEP** — fixed large round count (control: maximal deliberation).
- **ADAPTIVE** — the state-driven stopping rule (§6): stop when absolute
  marginal confidence gain < ε for k consecutive rounds, hard-capped at the
  DEEP round count.

Design invariants (frozen):

1. **One unit of account.** All three levels are expressed in rounds, so
   every comparison speaks one language.
2. **cap_adaptive = rounds_deep, always.** ADAPTIVE is a resource-subset of
   DEEP. If ADAPTIVE matches DEEP accuracy at lower mean cost, that is the
   finding — unconfounded by maximum resource.
3. **Deterministic given state.** The adaptive rule is a pure function of
   (round index, per-round confidence history). No RNG, no wall-clock, no
   scheduler dependence. Identical (item, config) → byte-identical record.
4. **Within-item design.** Every battery item is judged at every sweep point
   and under ADAPTIVE; item identity, substrate snapshot, judge code,
   confidence formula, and audit-step accounting are frozen. Item difficulty
   therefore cannot confound depth — it is differenced out by design.

## §4 DEPTH CONFIG SCHEMA (frozen)

Params file format: **plain-text `key = value`**, one per line, `#` comments,
UTF-8, no sections. (Chosen over JSON: trivially parseable in pure Zag with
no dependency; the harness crew owns the parser but MUST accept exactly this
grammar.) Unknown keys → hard parse error. Missing keys → the frozen
defaults below apply; the harness MUST record the effective config SHA per
run (§7).

```ini
# H5 depth config — conforms to DEPTH_DEF.md v1
level               = adaptive   # shallow | deep | adaptive
rounds_shallow      = 2          # fixed rounds for level=shallow
rounds_deep         = 16         # fixed rounds for level=deep
rounds_baseline     = 1          # no-deliberation calibration point (sweep plan only)
sweep_rounds        = 1,2,4,8,16 # recommended measurement sweep (informational)
adaptive_epsilon    = 0.02       # fraction of the [0,1] confidence scale
adaptive_k          = 3          # consecutive settled rounds required to stop
adaptive_cap_rounds = 16         # hard cap; MUST equal rounds_deep (enforced)
round_min_work      = 1          # >=1 evidence gather OR >=1 elimination per counted round
confidence_scale    = 0..1       # fixed-point; per-round; deterministic f(state)
```

Field constraints (harness MUST enforce at load):

- `level ∈ {shallow, deep, adaptive}` exactly; anything else is a parse error.
- `1 ≤ rounds_baseline ≤ rounds_shallow < rounds_deep`; `adaptive_cap_rounds == rounds_deep` (equality enforced, not just documented).
- `0 < adaptive_epsilon < 1`; `adaptive_k ≥ 2`; `adaptive_cap_rounds ≥ adaptive_k`.
- `round_min_work ≥ 1` (integer).
- All numeric fields are integers except `adaptive_epsilon`, which is a
  decimal fraction parsed into the harness's fixed-point [0,1] representation.

## §5 Recommended parameter values (with justification)

| Parameter | Value | Justification |
|-----------|-------|---------------|
| `rounds_shallow` | **2** | One reconsideration cycle past the single-pass baseline: shallow but real deliberation. 1 round = no-deliberation baseline (kept as sweep calibration, not a named level). |
| `rounds_deep` | **16** | 8× SHALLOW; the sweep {1,2,4,8,16} is log-uniform over 4 doublings, bracketing the plausible dynamic range. 16 rounds is large enough that residual gains beyond it would be practically irrelevant to the knee question, small enough to keep the battery affordable. |
| `sweep_rounds` | **1,2,4,8,16** | Log-uniform points make the curve; the knee is read in log2-rounds space (§8). |
| `adaptive_epsilon` | **0.02** | 2% of the confidence scale: demands *meaningful* movement to justify another round. Degrades gracefully under coarse confidence quantization (zero-change rounds still count toward k). |
| `adaptive_k` | **3** | One flat pair can occur from a single neutral-evidence round; three consecutive settled rounds is genuine settling without being so conservative that the rule never fires. |
| `adaptive_cap_rounds` | **16** | Equals `rounds_deep` per invariant §3.2 — non-negotiable. |
| `round_min_work` | **1** | Minimal non-empty contract; stricter values are a harness-tuning choice, not a spec change, but MUST be recorded if changed. |

## §6 The adaptive stopping rule (formal, frozen)

Let `c_1 … c_r` be the per-round confidences after rounds `1 … r`
(`c_i ∈ [0,1]` fixed-point, §6.3). Define `c_0 := c_1`, so the first-round
gain `g_1 = |c_1 − c_0| = 0`. For `i ≥ 1`, `g_i = |c_i − c_{i−1}|`.

**Rule.** After each round `r` (1 ≤ r ≤ cap):

- If `r ≥ k` **and** `g_{r−k+1}, …, g_r` are **all** `< ε` → **stop**, judge now.
- Else if `r == cap` → **stop**, judge now (cap reached; record `cap_hit = true`).
- Else → deliberate another round.

Earliest possible stop is after round `k` (round 3 at recommended values).
The rule references only `(r, c_0…c_r)` — observable deliberation state. It is
a total, deterministic function: no ties, no randomness, no external input.

### §6.1 Why |gain|, not gain

A confidence *drop* means evidence against the leading hypothesis — the most
productive thing deliberation can do. Stopping on raw `gain < ε` would abort
exactly when deliberation is working hardest. Absolute gain stops only on
genuine settling; oscillation continues to the cap. (Unanimous debate
finding, §2.3.4.)

### §6.2 Worked examples (ε=0.02, k=3, cap=16)

- `c = [0.60, 0.60, 0.61]` → gains `g1=0` (definitional, c_0 := c_1),
  `g2=0`, `g3=0.01`, all < ε → stop after round 3, `rounds_used=3`.
- `c = [0.55, 0.90, 0.40, 0.85, 0.86, 0.855, 0.86]` → oscillating gains ≥ ε
  until rounds 5,6,7 settle → stop after round 7.
- `c` pinned at `1.0` from round 1 → gains `0,0,0` → stop after round 3
  (minimum).
- Never settles → runs all 16 rounds, `cap_hit=true`.

### §6.3 Confidence: what it must be

- Per-round, fixed-point, in `[0,1]`, a **deterministic function of
  deliberation state** (kill-board, evidence set) — never a free number the
  judge can inflate to game the rule.
- **Recommended default** (harness crew may propose an equivalent, but must
  freeze one before measurement): normalized margin
  `c_r = (support(leader) − support(runner-up)) / total_evidence_weight`,
  clamped to [0,1], where support is the harness's frozen evidence-weight
  function.
- The formula is frozen pre-measurement and recorded per run (config SHA
  covers it if expressed as config; otherwise the harness version covers it).

### §6.4 Round work contract (frozen)

A **counted round** MUST perform ≥ `round_min_work` evidence gathers or ≥
`round_min_work` hypothesis eliminations (recommended: 1). A no-op cycle
does not advance the round counter for the stopping rule and does not count
toward `rounds_used`. The harness MUST enforce this; the red-team WILL try
to smuggle no-op work past it (§10.1).

## §7 Per-run record format (frozen)

Every (item, level) run emits exactly one record with these fields, in this
order (harness chooses serialization; TSV recommended):

```
item_id | level | rounds_used | evidence_items | hyp_considered | hyp_eliminated
| audit_steps | conf_final | judgment | correct | cap_hit | config_sha
```

- `item_id`: battery item identifier (battery crew's namespace).
- `level`: `shallow | deep | adaptive` (the treatment).
- `rounds_used`: counted rounds actually run (≤ cap; == fixed N for shallow/deep).
- `evidence_items`, `hyp_considered`, `hyp_eliminated`: mechanism traces (§2.5).
- `audit_steps`: substrate-native cost (the cost axis).
- `conf_final`: final-round confidence, [0,1] fixed-point.
- `judgment`, `correct`: the verdict and its battery-scored correctness.
- `cap_hit`: bool — did ADAPTIVE reach the cap (meaning: censored observation).
- `config_sha`: SHA-256 of the exact config file used (proves frozen-spec compliance).

**Determinism gate:** each (item, level) is run twice; both records MUST be
byte-identical (all fields). A mismatch is a harness bug, not data.

## §8 Measurement discipline (for battery + harness crews)

1. **Within-item design.** Every item × every sweep point {1,2,4,8,16} ×
   adaptive. Item identity, substrate snapshot, judge code, confidence
   formula, audit accounting: frozen across all runs of an item.
2. **Sweep before story.** Measure the full sweep; SHALLOW/DEEP/ADAPTIVE are
   points on (or derived from) one curve, not three separate experiments.
3. **Knee rule (preregistered).** Primary curve: accuracy vs rounds, x-axis
   log2. Let `d(p) = acc(p) − acc(p/2)` be the marginal accuracy gain per
   doubling at sweep point `p ∈ {2,4,8,16}` (percentage points). The knee is
   the smallest `p` such that `d(p) < 1` **and** `d(q) < 1` for every
   `q > p` in the sweep (i.e. gains stay below the bar for the rest of the
   range — guards against a noisy non-monotonic curve declaring a premature
   knee). If no such `p` exists, the knee lies beyond 16 rounds: report
   "not found in range", do not extrapolate. A negative `d(p)` (depth
   hurts) satisfies the bar naturally. Secondary: maximum-curvature point
   of the accuracy-vs-log2(rounds) curve. Tertiary (cost view): accuracy vs
   mean `audit_steps`. All three are reported; the preregistered rule
   governs the headline.
4. **Censoring check.** Report the fraction of ADAPTIVE runs with
   `cap_hit=true`. If ≥ 1/3, the adaptive measurement is censored: the cap
   is too low (or ε too small) — raise via §12 amendment, do not read a
   knee off censored data.
5. **Headroom requirement (battery crew).** Items where SHALLOW already
   saturates (accuracy ≈ 100% at 2 rounds) carry no information about depth;
   the battery MUST include items with headroom (shallow accuracy materially
   below deep), or the curve is flat by construction.
6. **Cost reporting.** Report mean `audit_steps` per level alongside
   accuracy: the knee is a cost-effectiveness claim, and cost must be visible.

## §9 What "depth" is NOT (anti-definitions, frozen)

- **Not wall-clock time.** Time is scheduler- and hardware-dependent; the
  cost axis is audit steps.
- **Not token counts.** There is no LLM in the loop; tokens are not a unit here.
- **Not item difficulty.** Difficulty is held constant by the within-item
  design; depth is the controlled variation.
- **Not confidence itself.** Confidence is the *sensor* for the adaptive
  rule, not the quantity being varied.
- **Not "thinking harder" as a vibe.** If it isn't in the §7 record, it
  didn't happen.

## §10 Red-team anticipations (handoff to the H5 red-team crew)

1. **No-op round smuggling.** Build cycles that satisfy the letter of the
   work contract (e.g. "evidence gathers" of irrelevant facts) while doing
   no deliberative work, inflating `rounds_used` and gaming the adaptive
   stop. The contract (§6.4) is the current defense; break it.
2. **Confidence damping (cost attack).** A judge that moves confidence in
   sub-ε steps prolongs deliberation, burning audit budget. Detectable in
   the `rounds_used` distribution; no spec-level defense — this is a
   judge-integrity finding if demonstrated.
3. **Confidence inflation.** Rising confidence without supporting evidence
   triggers premature adaptive stops. Defense: the deterministic,
   state-derived confidence requirement (§6.3); attack the harness's margin
   formula.
4. **Cap-hunting.** If ADAPTIVE hits the cap on most items it is DEEP in
   disguise. The §8.4 censoring check catches it; try to construct
   item classes that force it.
5. **ε/k post-hoc tuning.** Any "better" (ε, k) found after seeing data is
   inadmissible without a §12 amendment and re-measurement.
6. **Battery laundering.** A battery with no headroom (§8.5) makes every
   depth look equal. Audit the battery for headroom before trusting a flat curve.

## §11 Harness-crew handoff checklist (freeze before ANY measurement run)

- [ ] Confidence formula frozen (§6.3): judge-native or harness margin; [0,1] fixed-point; deterministic.
- [ ] Round boundary defined; work contract (§6.4) enforced in code.
- [ ] Evidence-item counting defined for the substrate in use.
- [ ] Hypothesis considered/eliminated counting defined (explicit kill-board events).
- [ ] Audit-step accounting defined (what increments the counter).
- [ ] Config parser accepts exactly the §4 grammar; enforces all constraints (esp. `adaptive_cap_rounds == rounds_deep`).
- [ ] `config_sha` recorded per run; determinism gate (§7) passing on pilot items.
- [ ] Substrate snapshot frozen per battery item; within-item design implemented.
- [ ] Example config (below) parses and runs end-to-end on one pilot item at all three levels.

### Example config file

```ini
# H5 depth config — DEPTH_DEF.md v1, recommended values
level               = adaptive
rounds_shallow      = 2
rounds_deep         = 16
rounds_baseline     = 1
sweep_rounds        = 1,2,4,8,16
adaptive_epsilon    = 0.02
adaptive_k          = 3
adaptive_cap_rounds = 16
round_min_work      = 1
confidence_scale    = 0..1
```

## §12 Amendments

This spec is frozen at v1 on commit. Changes to §§4–8 (schema, values,
rule, record, discipline) require: (a) H5 program coordinator sign-off,
(b) a version bump recorded at the top of this file, (c) re-measurement of
any leg run under the old version where the change could affect results.
Clarifications to §§9–11 that change no frozen field need only be appended
with a date. The deferred Sol second-opinion pass (§2.1), if it surfaces a
defect, enters through this procedure — it does not un-freeze v1 by itself.

## Appendix A — Sol attempt log

| Time (UTC 2026-09-23) | Call | Result |
|---|---|---|
| ~23:32 | `sol.py brief1 (2500 tok)` | HTTP 524 (origin timeout) |
| ~23:34 | `sol.py brief1 (1800 tok)` | `choices: null`, 0 completion tokens |
| ~23:35 | `sol.py brief1 (1800 tok)` retry | `choices: null`, 0 completion tokens |
| ~23:37 | `unorouter.py chat --model grok-4.6` | HTTP 524 |
| ~23:38 | `unorouter.py chat --model glm-5.3-flash:free` | HTTP 403 (credential not authorized for :free models) |
| ~23:40–23:55 | `sol_retry.py` 3-attempt backoff (90s) | all 3 null-choices; SOL UNAVAILABLE |

---
*End of DEPTH_DEF.md v1 — H5 Crew 1 (depth definition). Phase 1 spec only; no
measurement battery was run under this spec (hard rule).*
