# PREREG — lifecycle-as-advisor (wave 3)

**Status:** preregistered 2026-09-19, BEFORE any implementation compile or trial run.
**Scope:** advisory interface between the lifecycle future-use estimator
(`r34_memory_lifecycle_v1` integer lineage, per `wave2/ruleslab/RULES_SURVEY.md` §5)
and the deliberate memory-agency policy (`wave2/memoryagency/MEMORY_OPS.md` op set).
**Program law compliance:** no RNG anywhere in the system (see §8); explicit
scale dimension (see §7); designed curricula, no seeded harness RNG (see §4).

## 1. Hypothesis

A deliberate memory policy that *consults* a signed future-use estimate as
**advice** — where every accept/reject is an audited deliberate op and the
estimator is structurally incapable of triggering eviction — retains more
truly-important memories at endpoint under memory pressure than the identical
deliberate policy without advice. The advisor contributes a second, signed
signal (learned by delayed full-information credit, the lifecycle-v1
mechanism) that the policy weighs against its own declared values; the
policy, never the estimator, decides.

## 2. Arms (identical curricula, identical policy core)

- **NO-ADVICE (control):** deliberate policy only. Signed declared values at
  ADD (signed per-feature trust, learned by counting delayed revelations —
  deterministic, logic-driven); PIN-under-uncertainty for the first 120
  revelations (MA3's confirmed win, kept); pin budget (CAP−4) with deliberate
  unpin of the lowest-declared pinned memory when the budget binds (fixes
  MA3's early-lock bias); victim = lowest declared value (tie → lowest slot
  index — deterministic); admission iff incoming declared value strictly
  beats the worst candidate. Kills via plain `ma_kill`.
- **ADVICE:** the *same* policy, except at every pressure event it solicits
  a signed suggestion from the advisor for the incoming memory and every
  live unpinned USER candidate, computes adjusted scores
  `c = v + w·a` (`w` = policy-declared advisory weight, calibrated
  deterministically on delayed revelations — agree +4 / disagree −8,
  clamped [0,100], init 25), and kills `argmin c` via the **gated**
  `ma_kill_advised` (op-implementation gate: refuses without a deliberate
  `MA_OP_ADVISE` record naming the slot — `REFUSED_NOADVISE`, structural
  like `REFUSED_CORE`). Every accept/reject is an audited `MA_OP_ADVISE`
  entry (advice value, strength, accepted 0/1, decision code, w before/after).
  Advisor learns by delayed full-information credit on admitted memories at
  revelation (the lifecycle-v1 rule; substrate learning, no reward in the
  learner's declared-value path).

## 3. The structural guarantee (what "the estimator can never evict" means)

1. **Module isolation:** `adv_advisor.zag` takes only `[]u8`/i32, returns
   only scalars; it imports nothing, names no store, no slot, no op.
   Runner static check greps for `@import|MaStore|ma_` — fail if found.
   The advisor cannot address a slot at the type level.
2. **Op-implementation gate:** `ma_kill_advised(s, slot, tok)` verifies that
   `audit[tok]` is a successful `MA_OP_ADVISE` record naming `slot`;
   otherwise `REFUSED_NOADVISE` (audited refusal). No ADVISE record ⇒ no
   eviction, regardless of estimator output. This is in the op
   implementation, not a policy promise — the REFUSED_CORE shape.
3. **Audit invariant:** trial asserts every successful advice-arm kill is
   immediately preceded by its ADVISE record (`adv_kills_gated`), and that
   the advice arm never calls plain `ma_kill` on USER slots
   (`adv_no_plain_kills`), and the control arm holds zero ADVISE records
   (`noadv_no_advise_records`).

## 4. Curricula — explicitly designed, no RNG anywhere

Fixed 32-slot store, 500 episodes, revelation delay 25. Six designed cells
(no seeds — variation comes from designed adversity, not RNG):

| cell | design | what it tests |
|---|---|---|
| v0 | standard base: important = high f0/f1 early evidence honest | replication of MA3's standard win |
| v1 | standard + bursty importance (deterministic clusters) | retention through bursts |
| v2 | standard + late feature drift (t≥250: evidence weakens) | advisor value when own signals degrade |
| v3 | adversarial base: important = high f1 AND low f0 (trap) | MA3's adversarial loss shape |
| v4 | adversarial trap-deep (f0 3-vs-0, exact) | strong trap |
| v5 | early-honest 150 eps, then trap flips | designed regime switch — the world's unpredictability is the test |

Importance schedule: `imp=1 iff ((t*7+3) mod 10)<3` (base; burst variant
uses deterministic 50-episode blocks). Features 0..3 from the closed-form
`n(t,i)=((t*37+i*91+11) mod 4)`. Fully reproducible by hand; the system
itself is deterministic given state, so reruns must fingerprint-match.

## 5. Metrics (per-arm, per-cell; E51AJ law — per-cohort, never aggregate-only)

- Primary: truly-important memories held at endpoint among admitted
  (`ret/tot`), reported per cell and per quartile cohort.
- Advice-accounting: kill-event accepts, rejects, acceptance rate
  (kills only); w start/end; estimator learning sanity (mean |err| first 60
  vs last 60 revelations, as in MA3 DIAG).
- Structural: `cell_valid` (CORE intact, pinned-while-pinned intact, ledger
  replay clean), `adv_kills_gated`, `adv_no_plain_kills`,
  `noadv_no_advise_records`, determinism fingerprint rerun.

## 6. Falsification criteria

- **POSITIVE:** ADVICE `ret` strictly greater than NO-ADVICE `ret` in **all
  6 cells**, AND acceptance rate in (0.05, 0.95) — the advice was genuinely
  weighed, not rubber-stamped and not ignored — AND every structural
  CL_CHECK passes (replay clean, gated kills, isolation grep, determinism).
- **NEGATIVE:** NO-ADVICE ≥ ADVICE on all 6 cells → the advice adds nothing;
  say so plainly. OR acceptance ≤ 0.05 (never trusted — equivalent to adding
  nothing) OR ≥ 0.95 → the interface fails its own definition: at ≥0.95 the
  estimator decides in practice and automaticity has been smuggled back in
  (the MA3-AUTO failure mode returns through the back door).
- **MIXED:** any other split of cell wins/losses.
- **INVALID (stops the read):** any cell invalid (CORE/pinned loss, replay
  divergence, ungated kill), isolation check failure, or determinism
  fingerprint mismatch.

## 7. Scale dimension (program law: mechanisms must be designed to scale)

- Trial scale: 32 slots / 500 episodes / 8 features — the comparison scale,
  inherited from MA3 for comparability.
- Cost model: per-episode worst case O(CAP) victim scan + O(CAP·feats)
  advice scan; memory O(CAP·feats + audit entries). **No pairwise, no N×N,
  no cross-slot structures anywhere** — the advice is a per-slot signed
  scalar solicited on demand, so the interface cost is the same order as
  the victim scan the policy already pays. The audit ledger is the only
  superlinear risk: entries ∝ op count, so the audit cap must grow with
  horizon (4096 entries suffice here; 100x horizon needs ~400k).
- 10x (320 slots / 5000 eps) and 100x scale linearly in time under this
  model. **Next scale test (explicit, not this trial):** one 320-slot /
  5000-episode cell on variant v3 to verify wall-clock linearity and ledger
  sizing. If the per-episode cost deviates from linear, the design's scale
  claim is falsified — record it, don't hand-wave it.

## 8. RNG statement (program law: no randomness in the AI)

- The system (policy + advisor) contains **no RNG**: no random exploration,
  no random tie-breaks (ties → lowest slot index), no stochastic policies,
  no seeded RNG inside the learner. All judgment updates are deterministic
  functions of observed revelations (counting evidence, delta-rule credit —
  logic and verification, not sampling).
- The harness likewise uses **no RNG**: curricula are closed-form designed
  sequences (§4). The verdict distinguishes "the system is deterministic"
  (fingerprint rerun must match exactly) from "the test was adversarial"
  (the v5 regime flip is designed adversity, not noise).

## 9. Compute note

6 cells × 2 arms × 500 episodes — trivial for native binaries. The work is
the advisor isolation + gated-op implementation, not the runs. If the gated
op fights the compiler, the fallback is NOT a silent substitution: record
BLOCKED with the exact compiler error.
