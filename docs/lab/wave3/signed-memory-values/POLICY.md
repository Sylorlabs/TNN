# Signed-value memory policy (MA4) — design

**Date:** 2026-09-19
**Status:** design, preregistered in `PREREG_MA4.md` before any run
**Answers:** the MA3-extracted requirement (TRIAL_RESULTS_MA3.md): memories
need SIGNED value judgments + the early-lock admission bias must be fixed.

## 1. What MA3 proved and what it left broken

MA3's AGENCY arm (protect-while-uncertain, non-negative trust, pin-everything)
won the standard curriculum 30–0 but lost the adversarial 10–11 vs 30,
because:

1. **Non-negative trust** could not express "this feature pattern predicts
   *unimportance*." Its post-uncertainty gate was vacuous and the store
   sealed shut with early pins (28–29/30 quartile-0 lock-in).
2. **No deliberate negative judgment existed.** The learner could protect
   (PIN) or neglect (leave unpinned), but never declare a memory BAD and act
   on it.

The AUTO arm won adversarial with a *signed* linear predictor + churn. The
signedness was doing the work, not the automaticity. MA4 ports signedness
into the deliberate op set — no reward signal, no gradients, no RNG.

## 2. The signed-value policy

### 2.1 Learner state (all integer, all deterministic)

- `trust[f]`: signed i32 per feature, range `[-TRUST_MAX, +TRUST_MAX]`
  (`TRUST_MAX=256`), initialized to `+64` each. The init is a *declared
  prior* — "features plausibly carry signal" — recorded in the audit trail
  of the design, not learned. It may go negative; that is the point.
- On each delayed revelation of memory `m` with importance `imp ∈ {0,1}`
  and features `x`: `trust[f] += x[f]` if `imp==1`, else `trust[f] -= x[f]`,
  clamped. This is **signed evidence accumulation**, not a reward update:
  no scalar reward ever enters the memory path; the update is a fixed
  integer rule applied to the learner's own declared judgment state.
- Declared value at `MEM_ADD`: `v = Σ trust[f]·x[f] / 64` — signed, can be
  negative. The ADD-time declaration is the audited judgment.

### 2.2 Deliberate negative judgments (the new ops usage)

The learner may now declare a memory bad, in three audited forms:

| Judgment | Op sequence | Meaning |
|---|---|---|
| `JUDGE_WORTHLESS` | `UNPIN` (if pinned) then `KILL` | "Revelation proved this worthless; I remove it deliberately." Applied to revealed-unimportant memories. |
| `JUDGE_UNWORTHY_OF_PROTECTION` | `UNPIN` | "My current signed score for this slot is negative; it no longer deserves protection." Applied in the re-evaluation pass (§2.4). The memory stays until churn kills it — protection withdrawn, destruction still requires the victim rule. |
| `JUDGE_INFERIOR` | `KILL` as churn victim | "This is the lowest-signed-value unprotected memory and the newcomer is strictly better." The ordinary pressure valve, now signed. |

Positive judgments are unchanged: `PIN` (while uncertain, budgeted),
`PROMOTE_TO_LONGTERM` on revealed-important.

### 2.3 Pin budget (fixes early-lock structurally)

`MAX_PIN = 16` of 30 usable slots. PIN is a scarce deliberate resource:
- Phase A (uncertainty, revelations < 120): incoming pinned iff
  `pins < MAX_PIN`.
- Revelation of important: `PROMOTE` to LONG; `PIN` iff `pins < MAX_PIN`.
- The budget is enforced by counting, not by feel. Early pins can never
  seal the store again: at most 16 of 30 slots are ever protected.

### 2.4 Re-evaluation pass (fixes stale protection)

Once, when revelations reach 120 (the end of the uncertainty horizon): for
each pinned USER slot, recompute the fresh signed score from current trust
and stored features. If negative → `UNPIN` (judgment: unworthy of
protection). This is the deliberate "I changed my mind" — audited,
scheduled, deterministic. It cannot fire early (trust is immature) or late
(it fires exactly once, on a deterministic trigger).

### 2.5 Churn rule (signed victim selection)

When the store is full and a newcomer arrives with declared value `v_new`:
- Victim = live, unpinned USER slot with minimum **fresh** signed score
  (`Σ trust[f]·x[f]/64` recomputed from stored features — the learner's
  *current* judgment, not the stale ADD-time declaration).
- Ties → lowest slot index. No RNG anywhere: not in tie-breaks, not in
  exploration, not in the policy.
- Admit (kill victim, add newcomer) iff `v_new > v_victim` strictly.
  Otherwise drop the newcomer. The strict inequality prevents churn loops.
- During phase A (uncertainty) there are no pressure kills — overflow is
  dropped, exactly as MA3. Destruction-before-knowledge stays banned.

### 2.6 What stays from MA3

Protect-while-uncertain, delayed-revelation trust learning, staged autonomy
(all ops at stage KILL in the trial), CORE absolute protection, append-only
ledger with replay check, refusal accounting, per-cohort endpoint scoring
(E51AJ law).

## 3. Why this should beat MA3-AGENCY on adversarial (mechanism)

Adversarial trap: features f0–f3 anti-correlate with importance early.
- MA3: trust clamped at 0 → scores stay non-negative → everything looks
  "not bad" → pins never released → 10–11 important held.
- MA4: trust[f0–f3] goes negative after revelations → unimportant memories
  score negative → `JUDGE_WORTHLESS` kills them on revelation,
  `JUDGE_UNWORTHY_OF_PROTECTION` unpins the rest at the re-evaluation pass,
  churn admits positive-scoring (important) newcomers. The store keeps
  turning over instead of sealing.

Standard curriculum: trust stays positive everywhere; the policy reduces
to "protect confirmed-important, kill revealed-unimportant, churn
lowest-first" — same endpoint as MA3 (30/30 is the capacity ceiling),
with fewer wasted admissions.

## 4. Program-law compliance (2026-09-19 update)

- **No RNG in the system.** The learner's decisions are a deterministic
  function of its state: trust updates, victim scans, tie-breaks (lowest
  slot index), the re-evaluation trigger (revelation count == 120), the
  pin budget counter. The trial binary contains no RNG call in any
  decision path; the runner statically greps for it.
- **Explicit adversarial curriculum.** The harness generates streams from
  closed-form modular sequences of (episode, feature, variant) — no LCG,
  no seeds-as-randomness. Three explicit variants differ by phase offset.
  Test adversity is designed, not sampled.
- **Determinism vs adversity distinguished.** The trial reruns every cell
  and requires fingerprint equality (system deterministic); the verdict
  compares arms on identical streams (test adversarial).
- **Banned as progress:** no score tables (trust is an 8-vector of
  declared judgments, not a value table), no N×N scale-up, no reward
  signal in the memory path, no random exploration.

## 5. Scale dimension

Complexity per episode: O(F) scoring + O(S) victim scan. Re-evaluation:
O(S·F + B log B) once. Ledger: O(ops). All linear in slots S and features
F — no pairwise or combinatorial step. Nothing in the policy assumes
small S: the pin budget, uncertainty horizon, and ledger capacity scale
as explicit functions of S (see PREREG_MA4 §6). The MA4 trial runs at
MA3 scale (32 slots / 500 episodes) for head-to-head comparability; the
scaling claim is a complexity argument plus a named next test (MA5:
320 slots, 5000 episodes), not a hand-wave.

## 6. Known audit gap (honest)

`trust[f]` is learner-cognitive state, not slot state: trust updates are
not ledger entries (MA3 precedent). Mitigations: the update rule is a
fixed deterministic function of the revelation stream; final trust is
printed and folded into the determinism fingerprint; the revelation
sequence is reproducible from the explicit curriculum. If a future
auditor wants trust in the ledger, the op set needs a `JUDGE` op — that
is a design decision for wave-4, not smuggled in here.

## 7. Debatable tradeoffs (flagged, with numbers to watch)

1. **Kill-on-revelation-unimportant vs leave-for-churn.** Chosen: kill
   immediately (clearest negative judgment). Risk: if revelations were
   ever noisy, this destroys before second opinions. Watch: kills/episode
   in the results; the curriculum's revelations are ground truth, so the
   risk is contained to this trial — flagged for any noisier follow-up.
2. **Pin budget 16/30.** Chosen as S/2 (round). A smaller budget protects
   less during uncertainty; a larger one re-admits early-lock. The trial
   reports pin counts; sensitivity is MA5 work.
3. **Fresh-score victim selection vs ADD-time declared value.** Chosen:
   fresh (current judgment). The ADD-time value stays in the ledger as the
   historical declaration; the victim rule uses the live judgment. Both
   are auditable; the choice is recorded here.
