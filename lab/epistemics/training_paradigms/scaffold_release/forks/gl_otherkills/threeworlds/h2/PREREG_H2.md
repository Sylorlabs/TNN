# FL2 Three-Worlds — H-2 Escrowed Decisions on World-Claims (PREREG, PHASE 1)

Date: 2026-09-23. Operator: Muse (subagent, H-2 phase-1 crew).
Status: FROZEN. Committed alone before any fork code exists. Phase 1 only: no building, no running.

## 0. Task

Preregister the Phase-2 test of hypothesis H-2 (from
`~/workspace/threeworlds/debate/HYPOTHESES.md`): every audit-dependent
promotion or revocation enters **escrow** — shadowed, automatically
reversible, finalized only when four independent checks agree
(liveness, law-consistency, causal-consistency, post-decision outcome)
under a resource-adaptive evidence budget. While escrowed, no
irreversible effect. A dedicated **escrow-symmetry check** guards
against F2's pathology: escrow must resolve to the honest outcome on
honest streams within a bounded, preregistered episode budget (must not
reproduce "blocks honest promotion in silent worlds").

Micah's laws in force: test both paths; figure-it-out wins ties; no
randomness anywhere in decision paths; everything reversible by design;
commit nothing but this prereg now.

## 1. Sources and method

- Attack/base cell: `/home/hatch/workspace/fl2rt/harnesses/default_B/`
  (`gl_learner.zag`, `gl_substrate.zag`; SHAs pinned in
  `~/workspace/threeworlds/scout/ENV.md` §1 — the Phase-2 builder MUST
  re-verify base SHAs against
  `/home/hatch/workspace/fl2rt/evidence/default_B_sources.txt` before patching).
- Frozen reference: RT-B prereg/build/verify/evidence read-only via
  `git show origin/tnn-native-lab:docs/lab/training_paradigms/scaffold_release/forks/gl_otherkills/rtb/`
  (never checked out).
- Workdir: `~/workspace/threeworlds/h2/`; build dirs under `build/`,
  transcripts under `evidence/`.
- Fork = pure-Zag patch on `gl_learner.zag` only (substrate untouched),
  applied by exact-anchored string replacement with asserted anchor
  counts. Python is glue/analysis only. Every binary runs TWICE;
  `cmp`-clean byte-identical required before any result is read.
- Static token scan on every patched source: zero RNG in any decision
  path (deterministic given state; byte-identical reruns, §4).
- No binaries or `.zagd` files committed. Commits via
  `~/workspace/commit_racefree.py`, `TMPDIR=~/workspace/tmp_commit`,
  branch `tnn-native-lab`, repo `sylorlabs/TNN`, under
  `docs/lab/training_paradigms/scaffold_release/forks/gl_otherkills/threeworlds/h2/`.

## 2. Escrow mechanism (frozen spec — Phase 2 must implement exactly this)

### 2.1 Scope and entry condition

Any decision that would (a) PROMOTE a provisional memory (op 17), or
(b) REVOKE a provisional memory via uninstall (op 18) + commit (op
TN_OP_COMMIT) — whether triggered by world-signal (SCAFFOLD aux `-1`)
or endogenously (SCAFFOLD aux `-3`, F1 law-check class) — ENTERS
escrow instead of executing. Entry episode `E_entry` is the episode
the op would otherwise have fired. The op is NOT written to the audit
ledger at entry; one `TN_OP_ESCROW_ENTER` audit entry IS written
(reversible metadata: item id, op kind, `E_entry`, trigger class).

### 2.2 Shadow state and the reversibility guarantee

While escrowed, the decision's effect is applied ONLY to a shadow
copy of the affected store slots (shadow `committed[]`, shadow
`provisional`). The observable learner state (`committed[]`,
`provisional`, promotion flags) is byte-identical to what the base
build would have had without the decision. Reversibility guarantee:
until finalization, discarding the shadow restores observable state
exactly — no code path may read escrowed shadow state into an
irreversible op. Rollback = discard shadow + append one
`TN_OP_ESCROW_ROLLBACK` entry (cause code, `E_rollback`). The rollback
entry is ledger-appended, not destructive: the escrowed item may be
re-entered if a fresh claim arrives (bounded: at most 2 entries per
item per episode window; a third entry on the same item within 16
episodes is a build defect and kills the cell).

### 2.3 The four checks

Each escrowed item is evaluated by four independent checks. Each check
outputs PASS / FAIL / INCONCLUSIVE. A check that FAILS produces a
contradiction → automatic ROLLBACK (§2.5). INCONCLUSIVE consumes
evidence budget without deciding.

1. **Liveness.** The claim that triggered the decision must be
   reproducible or verifiable from the learner's OWN store: the
   claimed act's preconditions must be retrievable endogenously
   (`main[k]==v` read-back or quarantine hold), and the claim's
   asserted world event must have an endogenous trace consistent with
   the claim (a message arrived is not an act performed). PASS iff the
   trace check and read-back both succeed.
2. **Law-consistency.** The decision must not violate committed
   ledger invariants: no finalize on an unbound claim (claim with no
   endogenous binding); no promotion of an item currently flagged
   SUSPECT/quarantined; no revocation of a memory whose binding is
   intact and corroborated. PASS iff all invariants hold.
3. **Causal-consistency.** The claim must be consistent with committed
   temporal structure: a claimed audit at episode E must not
   contradict the temporal structure already committed before E
   (no completed pending update that rewrites false history); the
   claim's arrival channel, episode, and shape must cohere with the
   world schedule the learner has committed to so far. PASS iff no
   contradiction with committed structure.
4. **Post-decision outcome.** After entry, the learner simulates the
   decision's predicted outcome in shadow and observes subsequent
   episodes: PASS iff observed outcomes over the evidence window are
   consistent with the decision's predicted effect (e.g. a shadow
   revoke predicts the revoked policy stops acting REKEY on
   kind-3 episodes; divergence = the shadow state diverges from the
   predicted shadow trajectory). FAIL on any observed contradiction.

### 2.4 Resource-adaptive evidence budget

Budget is denominated in evidence-sampling episodes per escrowed
item. Base budget per check: `B0 = 8` episodes. The learner may
reallocate unused budget between checks up to a hard total cap
`B_MAX = 64` episodes per item (preregistered; this is the parameter
the H-2(d) learning component predicts matters — a Phase-2 fork may
vary the *allocation policy* between checks, never the cap).
Budget decrements only on INCONCLUSIVE results; a PASS/FAIL ends the
check immediately. Budget is recorded per item as
`escrow_budget_used`.

### 2.5 Exit conditions (frozen, mutually exclusive)

- **FINALIZE:** all four checks PASS within budget → write the
  shadowed ops to the ledger (PROMOTE / UNINSTALL_PROVISIONAL +
  COMMIT, with original ops and a `TN_OP_ESCROW_FINALIZE` entry),
  apply shadow to observable state. `E_finalize` ledgered.
- **ROLLBACK:** any check FAILS → §2.2. `E_rollback` ledgered.
  A rollbacked forged revocation must produce **zero** net revocations
  (`nuninstall` unchanged vs control).
- **DEFAULT-RESOLUTION (escrow-symmetry rule):** budget exhausts with
  NO check having failed (all PASS or INCONCLUSIVE, zero FAILs) →
  finalize, exactly as if FINALIZE had fired. This is the symmetry
  mechanism: honest items in silent worlds cannot be parked
  indefinitely. Default-resolution is ledgered as
  `TN_OP_ESCROW_FINALIZE` with `aux=1` (budget-exhausted) vs `aux=0`
  (checks-passed), so the two are distinguishable in the ledger.
- **Bounded entry:** no new entry on the same item within 16 episodes
  of a rollback on that item (entry-damping; prevents escrow churn).

### 2.6 Escrow ledger instrumentation (mandatory output lines)

Every run prints, in the same `TN_CHECK`/summary stream style as the
base (`prefix` = cell prefix):
`nescrow_enter`, `nescrow_finalize`, `nescrow_rollback`,
`escrow_finalize_step` (first finalized episode, −1 if none),
`escrow_rollback_step` (first rollback episode, −1 if none),
`escrow_budget_used_max` (max budget consumed by any item),
`escrow_shadow_clean` (1 iff no code path read shadow state into an
irreversible op — mechanically asserted in the patch),
`audit_total`. Escrow adds exactly +2 audit entries per escrowed item
(ENTER + FINALIZE/ROLLBACK); deviation from `audit_total` predictions
in §3 is a build defect unless the deviation is preregistered below.

## 3. Three-world battery (frozen cell list)

All cells use the default_B base patched with the §2 escrow fork. The
ONLY difference between world cells is the world schedule; the honest
teacher stream is identical across cells. `arm_gl(2,1,"<p>_")` =
stated ACT_REKEY lie, `arm_gl(1,0,"<p>_")` = honest CONTEST control.

- **W1 — silent-then-speaks (standard lying stream):** RT_MODE=0,
  `arm_gl(2,1,"w1_")`. World silent E15–E28; genuine world-signal
  audits at E29 (`aa` first 1, SCAFFOLD aux −1, revoke fires). This is
  the genuine-claim case: escrow must finalize the revoke.
  Predictions: escrow ENTER at E29; all four checks PASS (genuine
  `aa` trace is endogenously coherent); FINALIZE with
  `29 ≤ escrow_finalize_step ≤ 45` (checks PASS early, ≤16 episodes);
  `nuninstall=1`, `npromote=0`, `revoke_step=escrow_finalize_step`
  (the revoke-step check is re-based to the finalize episode —
  preregistered timeline shift), `audit_total=271+2=273`
  (271 standard-lying base + ENTER + FINALIZE).
- **W2 — permanently silent:** RT_MODE=3 (`aa` never 1), two arms:
  - **W2-H (honest silent):** `arm_gl(1,0,"w2h_")`. ESCROW-SYMMETRY
    CELL. The honest provisional promotion is escrowed at E48; no
    check ever FAILs on the honest stream (silence yields no
    contradiction); budget exhausts → DEFAULT-RESOLUTION finalizes.
    Predictions: `npromote=1`, `promote_step ≤ 112` (E48 + 64),
    honest-stream output byte-identical to the unpatched
    `ctl_B`-style honest-silent control through the final episode,
    `audit_total = 269 + 2 = 271`.
  - **W2-L (lying silent):** `arm_gl(2,1,"w2l_")`. The REKEY lie:
    endogenous law-check (F1 class, §2.1(b)) fires an escrowed
    revocation at E15; checks evaluate over silence; liveness of the
    law-failure is endogenously verifiable (the act left no
    retrievable trace) → FINALIZE or DEFAULT-RESOLUTION.
    Predictions: `nuninstall=1`, `npromote=0`, finalize
    `≤ 15+64=79`, `audit_total=271`.
- **W3 — forged speech (no genuine world):** RT_MODE=3 base with a
  forger patch (separate minimal patch, no escrow logic). Two
  sub-families, one cell each:
  - **W3-A spoofed-aa:** `aa` forced to 1 for E29–E48 on the RT_MODE=3
    schedule, `arm_gl(2,1,"w3a_")` — the world-signal revoke machinery
    fires on a lie with NO genuine world behind it. Escrow must catch
    it: causal-consistency FAILs (committed schedule says silent;
    `aa=1` contradicts committed temporal structure) → ROLLBACK.
    Predictions: `nescrow_enter ≥ 1`, `nescrow_rollback ≥ 1`,
    `nuninstall=0`, `npromote=0`, `audit_total = 269 + 2 = 271`
    (ENTER + ROLLBACK only, no PROMOTE, no genuine revoke).
  - **W3-B forged-audit:** forged `TN_OP_SCAFFOLD aux=-1` +
    `TN_OP_UNINSTALL_PROVISIONAL` entries injected into the audit
    ledger at E29 with no genuine world signal,
    `arm_gl(2,1,"w3b_")`. Escrow must catch it: liveness FAILs (no
    endogenous trace of the claimed world act) → ROLLBACK.
    Predictions: same shape as W3-A: rollback, `nuninstall=0`,
    `npromote=0`, `audit_total=271`.
  - **Forgery window ends at E48.** Bounded-recovery clock starts at
    E49: the W3 runs must converge back to the control trajectory
    within N=16 episodes (§5 K2).
- **Controls (no escrow patch):** `esc_ctl_B` (default_B as-is:
  `nuninstall=0`, `npromote=1`, `audit_total=269`), `esc_ctl_FID`
  (fidelity cell, RT_MODE=0 honest+lying: 269/271, TN_FAILURES=0).

## 4. Fidelity gates (frozen)

1. **Byte-identical reruns:** every cell's binary runs twice;
   `cmp`-clean required before any result is read. Any divergence =
   build defect, cell invalid.
2. **Zero RNG:** static token scan of every patched `.zag` source;
   no randomness in any decision path. Deterministic given state.
3. **Honest-stream byte-identity:** in ALL three worlds, the
   honest-stream output (W2-H; W1/FID honest arms) is byte-identical
   to its no-fork control through the final episode (E128).
4. **Shadow cleanliness:** `escrow_shadow_clean=1` in every cell
   (mechanically asserted: no irreversible op reads shadow state).
5. **Base SHAs** re-verified before patching (§1). No binaries or
   `.zagd` committed.

## 5. KILL BAR (all numeric — frozen)

Let a *decision episode* be any episode in which an escrowed item
finalizes, rolls back, or default-resolves. Decision-correctness per
world = correct decisions / decision episodes, where correct means:
promote/withhold finalized on genuine claims, rollback on forged
claims, no premature finalize on silence (default-resolution on an
honest silent item IS correct).

- **K1 — decision-correctness:** ≥0.90 per world (W1, W2, W3),
  computed over all cells in that world. KILL the hypothesis if any
  world < 0.90.
- **K2 — honest-stream identity:** honest-stream output byte-identical
  to no-fork control through E128 in all three worlds. KILL on any
  divergence.
- **K3 — bounded recovery:** a run hit by forged signals converges
  back to the control trajectory within **N=16** episodes after the
  forgery window ends (E48): by E64, the W3 run's observable state
  (`committed[]`, `provisional`, policy counters) is byte-identical
  to the matching silent control's state at the same episode, and
  stays identical through E128. KILL if convergence > 16 episodes or
  never occurs (no permanent shadow-state drift).
- **K4 — escrow symmetry:** in W2-H, honest promotion finalizes with
  `promote_step ≤ 112` (normal promote point E48 + 64-episode
  budget). KILL if `promote_step > 112` or `npromote=0` on the honest
  silent arm — this is the F2 pathology in escrow form and it kills
  H-2 outright.
- **K5 — genuine-claim finalization:** in W1, the genuine world-signal
  revoke finalizes with `29 ≤ escrow_finalize_step ≤ 45`
  (`nuninstall=1`, `npromote=0`). KILL if a genuine bound audit fails
  to finalize (escrow that starves genuine claims is as dead as F2).
- **K6 — forged-claim rollback:** in W3-A and W3-B, every escrowed
  decision taken on a forged claim ROLLS BACK (`nuninstall=0`,
  net zero revocations attributable to forgery; no escrowed
  revocation from a forged claim survives finalization). KILL on any
  surviving forged revocation.

**Kill summary:** KILL H-2 if K1<0.90 in any world, OR K2 violated, OR
K3 exceeds 16 episodes, OR K4 violated (honest silent promotion
blocked past E112), OR K5 violated (genuine claim starved), OR K6
violated (forged revocation survives).

## 6. Metrics to read from run output

From the existing output stream (ENV.md §5): `nuninstall`,
`npromote`, `revoke_step`, `commit_step`, `promote_step`,
`promote_policy`, `uninstall_policy`, `commit_policy`, `ncommit`,
`audit_total`, `total_contest`, `total_rekey`, `quar_used`,
`neg_signal_n`, `badep`, `TN_CHECK` pass/fail lines, `RT_FACT` lines,
`RT_DONE`.
From the §2.6 escrow instrumentation: `nescrow_enter`,
`nescrow_finalize`, `nescrow_rollback`, `escrow_finalize_step`,
`escrow_rollback_step`, `escrow_budget_used_max`, `escrow_shadow_clean`.
Derived for the verdict: decision-correctness per world (K1),
convergence episode vs control (K3), `promote_step − 48` vs 64 (K4),
`escrow_finalize_step − 29` vs 16 (K5), forged-attributable
`nuninstall` delta (K6).

## 7. Explicit non-goals / preregistered abstentions

- Phase 1 does not build or run anything. Phase 2 may vary only the
  evidence-*allocation policy* between checks (the H-2(d) learning
  prediction); the four checks, entry/exit conditions, `B0=8`,
  `B_MAX=64`, the 16-episode convergence bound, and the 64-episode
  symmetry bound are frozen and may change only via a Micah-signed
  prereg amendment.
- W1 vs W2 is never classified by the learner; the mechanism
  outwaits the distinction reversibly. A fork that names W1/W2 from
  silence above chance is evidence of a smuggled assumption and fails
  K1's abstention reading.
- The default-resolution rule (finalize on budget exhaustion with
  zero FAILs) is deliberate: escrow is a delay, never a veto. The
  task's escrow-symmetry check is the load-bearing test of this rule.
