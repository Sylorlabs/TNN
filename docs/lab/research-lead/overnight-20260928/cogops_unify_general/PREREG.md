# C502 PREREG — COGOPS-UNIFY-GENERAL
**Lane:** ARCHITECT-COMPRESSION, branch `arch/cogops-unify`
**Frozen:** 2026-10-03, before any UGEN code exists. Committed alone.
**Claim ids reserved:** C502 (this prereg), C503 (UGEN), C504 (ablation),
C505 (deletion ledger), C506 (verdict).

---

## H0 / H1

* **H1 (subsumption).** There exists ONE general, learner-owned mechanism
  `strat_sel_unified(L,tried,slot)` containing **zero** per-regime constants
  and **zero** regime branches, whose behaviour in each of the 10 distinct
  incumbent regimes is *derived* from learned state, such that on the frozen
  battery it retains capability.
* **H0 (irreducibility / unlearnability).** No such mechanism exists, for one
  of two separable reasons, and the failure is provable rather than a matter
  of taste:
  * **H0-a (pointwise contradiction).** Two incumbents disagree at a *single*
    reachable point of learner state. A single-valued mechanism cannot be
    both.
  * **H0-b (no gradient).** The battery's capability objective is constant
    over the whole parameter family, so no estimation procedure over learner
    state can identify the prior constants `P`, `Q`, `D` — there is nothing
    to learn them from.

Both are *successful* outcomes for this worker. H1 is not required.

---

## FROZEN FIXTURES

| fixture | value | provenance |
|---|---|---|
| frozen prefix | `ref/frozen_prefix.zag`, 1331 lines, sha256 `750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8` | `cogops_learnosc2/c8_learn.zag`, must stay byte-identical |
| base arena | `ref/base.zag`, from `c15_base.zag` sha `fc1f6e73c43a` | + the one documented `o_flush` sink substitution (`PROBE_RAW_SYSCALL_INERT.md`) |
| world | `ref/world.zag` = `c12_world.zag`, sha `46c6b0dc101f` | the world shared by c12..c17 |
| main | `ref/main.zag` = `c15_main.zag`, sha `739ae60a21df`, 792 lines | the main shared by the clean family |
| assembly | `mk.sh <additive> <tag>` → `out/<tag>.txt` | only the additive varies |

**Reference outputs, frozen now, must not change:**
`v15 == cogops_rescueaware/c15_run1.txt` byte-identically;
`v16 == cogops_pessimistic/c16_run1.txt` byte-identically;
`v17 == cogops_hedgeremoval/c17_run1.txt` byte-identically.

**Incumbent capability score** (the number every kill bar is written
against), on the frozen battery:
`agree=1 plans_built=8 plans_loaded=4 trials=6 declines=0 prior=2`.

---

## KILL BARS (frozen; not to be moved)

**B1 — determinism.** Every artefact built by this lane must be
`zbuild.sh --rep 3` clean: 3/3 byte-identical stdout (or, given the sink
substitution, 3/3 byte-identical flushed file). *Fail ⇒ kill.*

**B2 — capability retention vs best incumbent.** UGEN must score
`agree ≥ 1`, `plans_built ≥ 8`, `plans_loaded ≥ 4`, `trials ≥ 6`,
`declines ≤ 0` on the frozen battery. (c15 is the reference best; every
incumbent already ties it — see RECON §4a.) *Any shortfall ⇒ kill.*

**B3 — no regression of the worst.** UGEN must score
`agree ≥ min over incumbents`, `plans_built ≥ min over incumbents`,
`plans_loaded ≥ min`, `trials ≥ min`. *Any shortfall ⇒ kill.*

**B4 — LOC.** The unified additive section must be **strictly fewer source
lines** than the sum of the distinct incumbent additive sections it replaces.
Baseline to beat: the 10 distinct `strat_sel` bodies total
`46+46+42+42+42+53+53+30+61+78 = 493` lines. *Not fewer ⇒ kill.*

**B5 — ZERO new modes.** The unified mechanism must introduce no regime
selector, no config table, no per-regime constant, and no `if` whose purpose
is to select a scoring form. Concretely forbidden: a `match`/`switch` on a
mode id; a lookup table of the tuple `(scope, direction, P, Q, D, hedge)`;
any literal in `{1,2,8}` appearing as a prior/offset. *Violation ⇒ the
"unification" is a menu in a table and does not count; ⇒ kill.*

**B6 — the family must be re-derivable, i.e. the mechanism must be
*identified*.** UGEN must be accompanied by a measurement showing *which*
learned state drives its regime behaviour. If the answer is "a constant I
wrote", B5 is violated in spirit and the claim is downgraded to H0.

**B7 — no researcher-authored fixtures may be used to demonstrate the
mechanism.** Stages S12/S13/S14 use `strat_lesion_*` hand-written tables
(RECON §3). Any capability claim that rests only on those stages is void.

---

## FROZEN MEASUREMENTS TO BE TAKEN (before interpreting UGEN)

**M1 — the dead-mode ledger.** For all 15 named lanes, record
(sha256 of `strat_sel`, sha256 of full stdout). Any two lanes with equal
`strat_sel` sha are redundant by construction. Any two lanes with equal
stdout sha are redundant *on this battery*. Report the count.

**M2 — the parameter grid.** Hold base/world/main/prefix frozen. Sweep the
score template over
`P ∈ {0,1,2,3,4,6,8,12,16}`, `Q ∈ {0,1,2}`, `D ∈ {1,2,3}`,
`hedge ∈ {on,off}`, `direction ∈ {min,max}`, `scope ∈ {ctx}`.
For every cell record the `SUMMARY-DET` capability score.
**Prediction registered in advance:** the capability score is **constant over
the entire grid**. If it is not constant, say so loudly — it would mean the
battery *does* discriminate and H1 becomes worth pursuing hard.

**M3 — the pointwise-contradiction witness.** Exhibit one reachable learner
state at which two incumbents return different strategies, and show that the
state is a single point (not a region): i.e. all cells `strat_sel` reads are
pinned. *If such a witness exists ⇒ H0-a is established and H1 is dead.*

**M4 — ablation.** Remove the unified mechanism (replace with a fixed
first-legal-strategy rule, keeping all learner state updates intact) and
re-measure. *Requirement:* performance must drop. If it does not drop, the
unified mechanism is not load-bearing and the whole exercise is void —
report that.

---

## PREDICTIONS (registered before running M2/M3/UGEN)

* **P1** M1 finds **4** byte-identical-`strat_sel` lane pairs
  (c17≡c18, c17≡c19, c19h≡c19pos, c20h≡c21h) and ≥2 byte-identical-stdout
  pairs beyond them.
* **P2** M2's capability score is constant across the whole grid ⇒ **H0-b**.
* **P3** M3 finds the witness at the S13 or S14 lesioned table ⇒ **H0-a**.
* **P4** Because P2 and P3 both hold, UGEN — whatever its internal algebra —
  cannot be *identified* from this battery. Its retention of the incumbent
  score is therefore **vacuous**, and the correct verdict is
  **`26 → 1` is achievable by DELETION, not by unification.**
* **P5** M4 will show the ablation drops the *trace* metrics (which strategy
  is chosen, rescue count, CTX table contents) but will **not** drop
  `SUMMARY-DET`, because P2 says `SUMMARY-DET` is policy-independent.
  If M4 *does* drop `SUMMARY-DET`, P2 is wrong and I will report that.

## FALSIFIERS — what would make me report H1 instead

1. M2 shows the capability score **varies** over the grid ⇒ the battery
   discriminates ⇒ the regimes are empirically distinct *and* a unified
   mechanism has something to fit. Then I must build UGEN and hit B2–B5.
2. M3 fails to find a pinned-state contradiction ⇒ the incumbents may be
   mutually consistent, and a single mechanism could in principle be
   consistent with all of them.
3. UGEN hits B2, B3, B4, B5 simultaneously *and* B6 shows the regime
   behaviour is genuinely driven by a learned cell ⇒ report H1 with numbers.

## WHAT I WILL NOT DO

* I will not add a mode selector, a config table, or a learned-state cell
  whose only purpose is to reproduce one incumbent's constant.
* I will not report a capability-retention number without also reporting the
  *variance* of that number across the parameter grid (P2/M2). A retention
  number against a constant baseline is not evidence.
* I will not modify `cogops_learnosc2/c8_learn.zag`, any `cogops_*` lane, or
  any file outside `cogops_unify_general/`.
* I will not count `c18`≡`c17`≡`c19` as three "modes" or as a unification
  win. They are one policy in three directories.
