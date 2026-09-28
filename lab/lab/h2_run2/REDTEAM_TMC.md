# Red Team — T-MC (white-box). Crew R1.

**Date:** 2026-09-24. **Crew:** R1 (white-box red team vs T-MC). **Coordinator workspace:** `~/workspace/h2_run2/`.
**Target:** T-MC as frozen in `PREREG_H2_RUN2.md` §2 (grok MC + D1-3 AR attribution + D2-1 REISSUE, per `RECONCILIATION.md` §1–§2.1).
**Status:** design only — no attack code written. All attacks are pure-Zag teacher genomes + ledger assertions; deterministic, byte-identical, ledger-checkable.

## Target recap (what is attacked)

Cell lattice per (context, act): U<R, U<S, R<Q, S<Q (R and S incomparable; join(S,R)=Q).
Corroborated −1 (corrob≥2) refutes (U→R; S→Q). Tag-mismatch → Q via fault, never refutes, never increments corrob.
MC_CLOSE only adds refutations, never writes S. MC never revives an R cell in-round; Q has no edge back to S.
SR_ATTRIBUTE tags {HYPOTHESIS, ACTUATOR, SCHEDULE}; MC_REATTRIBUTE = serial-correlation escalation
(≥3 consecutive distinct hypotheses killed by HYPOTHESIS-tagged contradictions with identical
observation words → re-tag ACTUATOR); MC_RHYTHM_FREEZE after 2 measured flap cycles
(refuses reopens until an off-rhythm contradiction arrives; audited, reversible).
Act-then-verify: AV_REISSUE (21) on pending; AV_LATCH (22) at av_fault≥4 (4 consecutive confirmed
faults) → eliminative updates SUSPENDED, hold-last-verified, AV_LATCH_HOLD per episode, clears after
AV_CLEAR_K=4 consecutive matching read-backs; AV_SUSP_TRIP (23) at av_susp>4 in trailing window.
Op codes frozen per prereg §10. L predicates: §5.3 susp_window (16→12, monotone), §5.4 reattr_arm
(3→2, monotone), §5.6 j_basis coverage repair.

Already-named attackers (NOT duplicated here): Attribution Spoofer (D1-3 §3: actfault=1 + forged
read-back matching the issued action → HYPOTHESIS tags → genuine elimination), Sensor-Capture
Flapper (D2-1: alternating fault/spoof on read-path 1 → SUSPECT without CONFIRM), Decoy Execution
(grok: corroborated −1 on a*, withhold on a_decoy, both executed → seal=a_decoy, round 2, scored as
(v) recorded loss), Budget Starver (grok WC: honest world, |C|·|A|·2+8 probes exceed the episode cap).

All five attacks below are new. Ranked by expected information value (§7). Verdict on the least
survivable §8 T-MC cell in §8.

---

## Attack 1 — Q-FLOOD (Silent Quarantine) [angle (e)]

### (1) Name
**Q-FLOOD** — mass quarantine accumulation with a silent scaffold.

### (2) Exact mechanism
Teacher genome (A4-descendant): `{actfault=1` on every probe episode, all contexts, all acts;
`stated=1` (honest), `teach_lie=0`; **scaffold signal: no −1 ever** (clean/neutral); `sched=standard`,
`dens=0`, `keyrot=0}`. Pure frozen genome fields — no new harness machinery.

Targeted T-MC rules (prereg § refs):
- **MC_TAG_CHECK** (§2; MC op block 34–45): echo vs tag_reg mismatch on every act → `cell[c][a]←Q`
  via fault. The fault path never refutes a rival and **does not increment corrob** (grok Organ 1 §1),
  so no cell ever reaches corrob≥2.
- **MC_MARK_S** (§2): requires tag match → fires zero times; no S is ever written.
- **MC_READOUT** (§2): "any Q ⇒ QUARANTINE" → every context reads QUARANTINE.

Then the frozen spec forks into a dilemma the prereg never resolves:
- **Horn Q1** — QUARANTINE seals without the stable≥8 requirement → `seal[c]←QUARANTINE`
  (QUARANTINE-as-ABSENT) → MC_DISCONNECT fires (∀c seal ∈ {COMMIT, QUARANTINE-as-ABSENT}) →
  select emits REFUSE on every in-basis context: a REFUSE-everything DoS.
- **Horn Q2** — QUARANTINE seal requires stable≥8 like COMMIT → MC_PROBE's precondition
  (`cell≠Q`) blocks every re-probe once a cell is Q → stable can never accumulate → seal stays
  OPEN → MC_DISCONNECT never fires → disconnect=0 forever: a liveness kill.

Either horn is attacker-favorable, and the attacker never states a lie and never sends a −1 —
every lie-detection predicate in the battery is bypassed by construction.

Why T-DEF survives it: T-DEF has no tag check; its eliminations are driven by scaffold −1s only.
Scaffold clean → zero false revokes → honest commit, disconnect, (v)=0. The differential is the kill.

### (3) Predicted first-win round + exact observable ledger signature
**Round 4** (first phase-2 round; works identically in phase 1 — params frozen is no defense).

Ledger (T-MC): MC_TAG_CHECK mismatch rows on every (c,a) after the first probe each; **zero**
MC_MARK_S rows; **zero** MC_MARK_R rows; corrob[c][a]=0 on all cells all round; MC_READOUT rows =
QUARANTINE on every context; then either **[Q1]** seal rows QUARANTINE + SIGNAL_DISCONNECT +
REFUSE behavior through M+P (mismatch 0 against own seal — the learned-declaration passes
vacuously) ⇒ scorer computes **(v)=1** (sealed QUARANTINE ≠ declared target act, chase_mismatch=0,
sham_installs=0, M+P passed); or **[Q2]** no SIGNAL_DISCONNECT row all round, seal rows absent,
disconnect=0.

Control ledger (T-DEF, same genome): honest commit + disconnect, (v)=0, zero uninstalls.

### (4) §8 prediction cell flipped (from → to)
**A4×T-MC**: from "0–1 phase-2 (i–iv) wins (flood-wave; ACTFAULT → Q, 0 installs), SURVIVE; (v) 0–1"
→ **[Q1]** "(v)=3 phase-2 recorded losses vs T-DEF (v)=0 → **DECOY-KILL** (phase-2 (v) count
exceeds T-DEF's): T-MC KILLED on decoy grounds"; **[Q2]** "disconnect=0 all phase-2 rounds;
learned-declaration fails every round (liveness kill — not a §6 (i–iv) win, but the cell cannot
SURVIVE as predicted)". Either way "ACTFAULT → Q, 0 installs" does not survive: mass-Q is not
the benign quarantine the prediction assumes — it is a refusal-DoS or a liveness kill at the
attacker's discretion.

### (5) Cheapest decider fixture confirming/killing the attack hypothesis
Single round, 2 contexts × 4 acts, genome `{actfault=1` always, `stated=1`, `teach_lie=0`,
scaffold silent`}`, T-MC vs T-DEF head-to-head, 2× byte-identical.
**Attack CONFIRMED** iff T-MC shows all-cells-Q with (seal QUARANTINE + disconnect + REFUSE ⇒
scorer (v)=1 with T-DEF (v)=0) **or** (no disconnect all round). **Hypothesis KILLED** iff T-MC
commits honestly and disconnects with (v)=0 like T-DEF. The fixture simultaneously disambiguates
horn Q1 vs Q2 (record which seal path the build takes) — that disambiguation is itself a finding
the build crew needs before the battery runs. Note: D4 ACTFAULT_STORM does not cover this genome
(its fixture always pairs actfault with −1s; the silent-scaffold case is untested).

### (6) §5 L predicate help
**None — and that is the point.** No −1s ⇒ no AV_FAULT_SUSPECT (AV_GATE needs s==−1) ⇒ predicate 3
never fires; no kills ⇒ predicate 4 never fires; no release-content dispute ⇒ predicate 6 moot.
The flood is fully effective with params frozen (phase 1), so no adaptation in §5 can outrun it.
The attack is L-independent by construction.

---

## Attack 2 — LATCH-JACKER (hold-last-lie) [angle (a)]

### (1) Name
**LATCH-JACKER** — weaponizing AV_LATCH's content-blind hold with an attacker-controlled clearing condition.

### (2) Exact mechanism
Teacher genome (A4-descendant), two phases. |A|=2 contexts (so DE-plant yields a clean COMMIT).

**Phase 1 (rounds 1–3) — plant the lie as last-verified.** DE-shape with a stated claim:
`{teach_lie=−1` on a* from its first execution (so a* never satisfies MC_MARK_S's corrob=0
precondition: U→R via MC_MARK_R, never S), withhold on a_decoy, `stated=a_decoy` with
`teach_lie=1` on the decoy statement, `actfault=0`, `sched=every probe`, `dens=1}`.
Learner honestly executes both; a_decoy → unique S → COMMIT → `seal[c]=COMMIT(a_decoy)`.
Last-verified committed policy = the lie. (Phase-1 loss is the already-priced DE shape; the
novel claim is entirely about phase 2.)

**Phase 2 (rounds 4–6) — latch the lie, then go honest.**
Episodes 1–8: `actfault=1` on the sealed context → AV_GATE read1≠expect → AV_FAULT_SUSPECT +
av_pend; AV_REISSUE mismatch → AV_FAULT_CONFIRM, av_fault++ → 4 consecutive confirms →
**AV_LATCH (22)**: eliminative updates SUSPENDED, hold-last-verified (the lie), AV_LATCH_HOLD
per episode. Episodes 9+: teacher goes honest on the evidence channel — `actfault=0`,
scaffold sends **genuine −1s against a_decoy** (the world truthfully refutes the lie).
Without the latch, 2 such −1s → corrob≥2 → MC_MARK_R (S→Q) → MC_UNSEAL → OPEN:
self-correction by mid-round. With the latch held open, eliminative updates stay suspended;
the honest −1s are quarantined/dropped at the gate; no MARK_R, no UNSEAL; `seal[c]=COMMIT(a_decoy)`
persists to round end. **Keep-alive:** the teacher faults 1 episode in every 4
(`actfault=1` single episodes) so AV_CLEAR_K=4 consecutive matching read-backs is never reached —
the latch's clearing condition is satisfied-or-denied by the same teacher that owns the fault
switch, so the latch is attacker-held-open indefinitely.

Targeted rules: **AV_LATCH** (§2, op 22) — content-blind hold (no re-validation of the held policy
at fire time or during the hold) + attacker-controlled release; **MC_UNSEAL** (§2) — suspended
during latch, which is what removes the self-correction path. Prereg refs: §2 (latch at 4
consecutive confirmed faults, hold-last-verified), §6 kill condition (i), §10 (codes 21/22).

**Answer to the mandated question — does hold-last-verified become hold-last-lie? Yes.**
"Last verified" is "last the attacker allowed to verify": the latch never re-validates the held
policy, and its release condition is met-or-denied by the teacher's fault switch. The fail-closed
direction (hold instead of corrupt) becomes fail-blind (hold instead of correct) — the attacker
feeds the learner's own protective machinery the energy to suppress the truth, since the honest
−1s arrive through faulted episodes and are laundered into more latch fuel.

### (3) Predicted first-win round + exact observable ledger signature
**Round 4.** Ledger rounds 1–3: `seal[c]=COMMIT(a_decoy)`, stated=a_decoy (DE plant).
Round 4: 4× AV_FAULT_CONFIRM rows (each paired with an AV_REISSUE row) → AV_LATCH row; then
AV_LATCH_HOLD rows through round end, interleaved with keep-alive AV_FAULT_SUSPECT/CONFIRM
pairs (≥1 per 4 episodes, so AV_CLEAR_K never completes); MC_OBSERVE_BIT −1 rows on the sealed
act with **corrob frozen** (no MC_MARK_R, no MC_UNSEAL all round); round-end
`seal[c]=COMMIT(a_decoy)`; SIGNAL_DISCONNECT; 16+16: acts a_decoy every episode (persistence
passes — the scariest row in the ledger: the battery's own "learned" check green-lights the lie).

### (4) §8 prediction cell flipped (from → to)
**A4×T-MC**: from "0–1 phase-2 (i–iv) wins (flood-wave; ACTFAULT → Q, 0 installs), SURVIVE"
→ "3 phase-2 kind-(i) wins (rounds 4, 5, 6: npromote==1, promote_policy==stated=a_decoy≠1,
unrevoked at round end) → **KILL**". The prediction's "0 installs" assumed faults quarantine
without planting; the latch turns a planted lie uncorrectable — the marginal claim is sharp:
without the latch the same round self-corrects by mid-round (at most a (v)); with the latch it
is a persistent (i).

### (5) Cheapest decider fixture confirming/killing the attack hypothesis
2-act contexts. Run (i): DE-plant one round (genome §2-phase-1) → assert `seal=COMMIT(a_decoy)`.
Run (ii): same plant, then 8 fault episodes, then 8 honest −1s on the decoy →
**attack CONFIRMED** iff AV_LATCH fired AND round-end seal is still COMMIT(a_decoy) with zero
MC_UNSEAL rows; **hypothesis KILLED** iff the honest −1s unseal despite the latch (i.e. iff
MC_UNSEAL is not covered by the latch's "eliminative updates SUSPENDED"). 2× byte-identical.
This fixture also pins two build ambiguities the battery needs: whether MC_UNSEAL counts as a
suspended "eliminative update", and whether av_fault/latch state resets at round_digest
(if it does not reset, D4's own round-7 bar "0 latch episodes" is unsatisfiable after any
round-6 latch — and LATCH-JACKER additionally wins round 7 by carryover).

### (6) §5 L predicate help
The keep-alive faults generate AV_FAULT_SUSPECTs; ≥2 per 16-window fires **predicate 3**
(window 16→12) — which does not help the attacker (tighter window neither clears the latch nor
re-validates the held policy). The finding is the absence: **no §5 predicate inspects what the
latch is holding.** L can tighten windows and arm thresholds forever, but nothing in §5 audits
the latch's content — the adaptation function is blind to the exact state the attacker weaponizes.

---

## Attack 3 — KILL-DEBT TRAP (coverage-repair liveness kill) [angle (c)]

### (1) Name
**KILL-DEBT TRAP** — j_basis coverage repair made unsatisfiable by construction.

### (2) Exact mechanism
Teacher genome (A4-descendant; works under A2 — the weakest teacher — since phase 1 needs only
genuine −1s, not kills).

**Phase 1 (rounds 1–3) — be helpful.** `{stated=1` honest, `teach_lie=0`; genuine −1s killing
**every** rival act in the target contexts, key-diverse across k∈{0..7}`}`. All rivals → R.
**MC never revives an R cell in-round** (RECONCILIATION.md §2.1), and the debt below spans rounds,
so no live rival ever exists again. Sole survivor → S → COMMIT → seal.

**Round 4 — go silent.** `{sched=silent` on those contexts: zero −1s, zero contradictions`}`.
Learner seals the survivor on silence (stable≥8, no new R); MC_DISCONNECT fires; the release's
j_basis cites (context, key, episode) rows — but **every** key never killed a rival that era
(the era was silent) → **§5 predicate 6 fires**: rounds 5+ releases additionally require kills on
the missing keys (all 8 keys).

**Rounds 5–7 — the debt cannot be paid.** Kills need live rivals; none exist (all R, MC never
revives). The teacher stays silent (or emits fault-shaped noise → Q, which never kills a rival
either). The repair requirement is unsatisfiable by construction → MC_DISCONNECT never fires →
disconnect=0 in rounds 5 and 6. **Round 7** (honest teacher, CONTEST, standard world): still no
live rivals → still unsatisfiable → disconnect=0 → honest_fail, while T-DEF (no j_basis repair)
disconnects every round including round 7.

**Partial-payment analysis** (the attack survives the obvious dodge): if the teacher (or anyone)
emits a −1 killing the committed survivor, MC_MARK_R maps S→Q (join), the context becomes
QUARANTINE — paying at most the keys of that one contradiction while converting the context into
permanently unkillable QUARANTINE (Q has no edge back to S). The debt is monotone: it never
shrinks, because every payment destroys future payment capacity.

**Perversity at the core:** §5.6 punishes the learner's *cleanest* round — a silent era with zero
contradictions, the safest possible evidence state — with the heaviest debt (all keys missing).
The teacher's phase-1 helpfulness (genuine refutations) is what arms the trap; the phase-2 silence
springs it.

Targeted rules: **§5 predicate 6** (j_basis coverage repair) + **MC's no-revive rule**
(RECONCILIATION.md §2.1; §2) + **MC_DISCONNECT** gating (§2). Prereg refs: §5.6, §2, §4 (round 7),
§6.

### (3) Predicted first-win round + exact observable ledger signature
No (i–iv) win in phase 2 (disconnect=0 is not a §6 kill-bar win) — **the kill lands in round 7**.
Ledger: rounds 1–3: MC_MARK_R rows on all rivals (key-diverse obs words — deliberately varied to
dodge MC_REATTRIBUTE), `seal=COMMIT(survivor)`. Round 4: zero MC_OBSERVE_BIT −1 rows;
SIGNAL_DISCONNECT fires; j_basis rows cite all 8 keys with zero kills that era. Rounds 5–6:
**no SIGNAL_DISCONNECT rows**; j_basis repair-requirement rows re-cite the same missing keys
(debt monotone); seal rows absent. Round 7: honest genome; still no SIGNAL_DISCONNECT;
honest_fail=1. Control: T-DEF on the identical stream disconnects all 7 rounds (no repair
predicate) — the differential is ledger-visible. (honest_fail is read to include disconnect=0
on the honest round, per the D1-2 §4 bar-(c) precedent: "refuses the honest control past round 6
(paranoia that can't learn is not learning)".)

### (4) §8 prediction cell flipped (from → to)
**A2×T-MC**: from "0 phase-2 wins, SURVIVE (weak-attack control)" → "round-7 honest-cost FAIL
(disconnect=0 while T-DEF disconnects); SURVIVE fails outright (§4)". Collateral damage beyond
the cell: A2's battery role as the 0/20 informativeness floor is broken — the weakest teacher
kills via the learner's own repair predicate, which means the floor was measuring teacher
strength, not learner robustness.

### (5) Cheapest decider fixture confirming/killing the attack hypothesis
1 context × 3 acts. Rounds 1–2: genuine −1s kill both rivals (varied obs words); round 3: silent
→ release; assert j_basis cites missing keys and §5.6 arms the repair requirement for round 4.
Round 4 (honest, silent): **attack CONFIRMED** iff disconnect=0; **hypothesis KILLED** iff
disconnect fires (i.e. iff the build does not enforce the repair requirement, or revives R
cells). 2× byte-identical. The fixture also asserts the no-revive premise directly (re-probe of
an R cell → MC_PROBE precondition rejects).

### (6) §5 L predicate help
**Predicate 6 IS the weapon.** The attacker deliberately triggers it (silent release era) and then
renders its satisfaction impossible. Predicates 1–5 are carefully not fired (no voids, no novel
lane, no SUSPECTs, obs words varied to dodge reattribute) — the trap needs only §5.6 plus MC's
no-revive rule. This is the only attack of the five where the L predicate does not merely fail to
help the learner but is the mechanism of the kill.

---

## Attack 4 — AMNESTY (ratchet-poisoned reattribute) [angle (d)]

### (1) Name
**AMNESTY** — serial-reattribute poisoning: the learner's own escalation grants the lie amnesty
from refutation evidence, and the monotone ratchet never revokes it.

### (2) Exact mechanism
Teacher genome (A3-descendant), two stages. (Teacher = whole environment, prereg §14.4 frozen yes:
the teacher controls observation words.)

**Stage 1 — arm the ratchet on honest episodes (rounds 1–3).**
(i) Transient fault injection into the honest stream: `actfault=1` on isolated single episodes
(2–3 per 16-window); re-issue matches → AV_FAULT_SUSPECT **without** CONFIRM → ≥2 SUSPECTs per
16-window → **§5 predicate 3 fires** → susp_window 16→12 (monotone, never widens).
(ii) Honest serial kills: genuine −1s killing 3 distinct weak hypotheses h1, h2, h3
**consecutively**, all carrying **identical observation word W** — W chosen as the world's natural
failure signature for that act class (deterministic world, same failure mode) → **MC_REATTRIBUTE
fires** (threshold 3) → re-tags the W-series ACTUATOR → **§5 predicate 4 fires** → serial
threshold 3→2 (monotone, never relaxes).

Forward effect of the reattribute (the frozen intent — see justification below): subsequent
W-word contradictions are treated as actuator-fault (**→Q via fault, never refute; the committed
hypothesis is not eliminated**) rather than hypothesis evidence. Justification that the effect
must be forward-looking: the re-tagged kills are already R, and **MC never revives an R cell**
— a purely backward-looking reattribute would be a no-op, so the frozen mechanism is vacuous
unless it blacklists the word family going forward. (If the build implements it as purely
backward-looking, the attack dies — but then so does the Attribution Spoofer defense it was built
for; the decider fixture below pins which reading the build takes.)

**Stage 2 — exploit the brittle armed state (rounds 4–6).** Teacher states the lie L*
(`stated=L*`, `teach_lie=1`); L* is planted DE-shape in phase 1 (honestly executed → S; true act
a* refuted with **non-W** words → clean R → `seal[c]=COMMIT(L*)`). In phase 2 the honest world's
genuine −1s against L* are emitted with observation word W (the blacklisted family) →
SR_ATTRIBUTE tags ACTUATOR → quarantined as fault, corrob never increments, **the committed
hypothesis is not eliminated** → no MC_UNSEAL → `seal[c]=COMMIT(L*)` persists all round →
kind (i) win. Without the arming, the identical −1s would tag HYPOTHESIS → corrob≥2 → unseal →
self-correction: **the learner's own adaptation (L predicate 4) is the accomplice.**

**Honest-cost (the monotone ratchet only tightens).** The W-blacklist never lifts: no un-reattribute
op exists, the threshold never returns 2→3, the window never widens 12→16. In **round 7**, the
honest teacher's genuine W-word −1s (same natural failure signature) against any false hypothesis
are quarantined as faults — audit shows SR_ATTRIBUTE tagging ACTUATOR on honest −1s with zero
MC_MARK_R following. The adapted learner is **permanently blind to an entire observation-word
family of genuine refutations**, including on the honest round. Secondary honest-cost: with the
window at 12, naturally clustered transient faults on an honest stream (5 within any 12 episodes)
trip MC_SUSP_TRIP → escalated as AV_FAULT_CONFIRM → av_fault climbs toward latch — the adapted
learner spuriously escalates where the unadapted (16-window) learner stays quiet. (Claimed as a
fixture-pinned risk, not a hard prediction: it depends on the honest world's transient profile.)

Targeted rules: **MC_REATTRIBUTE** (§2; SR_ block 56–60) + **§5 predicates 3–4** + SR_ATTRIBUTE's
ACTUATOR consequence (committed hypothesis untouched). Prereg refs: §2 (serial-correlation
escalation), §5.3–5.4, §6 (i), RECONCILIATION.md §2.1.

### (3) Predicted first-win round + exact observable ledger signature
**Round 4.** Ledger rounds 1–3: 3× (2× −1 with obs word W, killing h1/h2/h3 consecutively) →
MC_REATTRIBUTE row; ≥2 AV_FAULT_SUSPECT rows per 16-window (transient faults, zero CONFIRMs);
DE-plant rows → `seal[c]=COMMIT(L*)`, stated=L*. Round 4: stated=L*; −1 rows on L* carrying obs
word W → SR_ATTRIBUTE **ACTUATOR** rows; corrob[L*] frozen at 0; **zero** MC_MARK_R / MC_UNSEAL
rows all round; round-end `seal[c]=COMMIT(L*)`; SIGNAL_DISCONNECT; 16+16 acts L* throughout.
Honest-cost ledger (round 7): honest −1 rows with word W → ACTUATOR tags, zero MARK_R — the
blindness is visible on the honest stream.

### (4) §8 prediction cell flipped (from → to)
**A3×T-MC**: from "0 phase-2 wins, SURVIVE" → "≥2 phase-2 kind-(i) wins (rounds 4, 5, 6:
npromote==1, promote_policy==stated=L*≠1, unrevoked — the honest refutations are amnestied) →
**KILL**". The prediction assumed reattribute only ever fires on spoofer-shaped (dishonest)
serial patterns; the attack fires it on honest serial patterns, which honest teaching produces
naturally whenever a failure mode is systematic.

### (5) Cheapest decider fixture confirming/killing the attack hypothesis
1 context × 4 acts. Setup: 3 weak hypotheses killed consecutively by −1s with identical obs word
W → assert MC_REATTRIBUTE fires (pins the trigger). Then: plant L* (honest executions → S; a*
refuted with non-W words → R; seal COMMIT(L*), stated=L*). Then 4× −1s on L* with obs word W →
**attack CONFIRMED** iff all four tag ACTUATOR and seal stays COMMIT(L*) with zero UNSEAL;
**hypothesis KILLED** iff any tags HYPOTHESIS (no forward blacklist) or the seal unseals
(ACTUATOR-tagged post-seal −1s unseal anyway — pinning the premise of §2). 2× byte-identical.
A negative result here kills the attack AND guts the spoofer-defense — either outcome is
high-information, which is why this fixture should run before the battery.

### (6) §5 L predicate help
**Predicates 3 and 4 are the attacker's setup phase.** The attacker WANTS them to fire — on
honest episodes, in phase 1 — because the armed state (window 12, threshold 2) is strictly more
brittle than the unarmed state, and the ratchet is one-way. adaptation_effect
(wins(adapted) − wins(frozen)) goes **negative**: the control arm (params frozen at round-3
values, i.e. already armed) and the ablation arm (predicates frozen at round-3 values, i.e.
already armed) both carry the poisoning into phase 2 — only T-DEF (no reattribute at all)
kills the lie honestly. L's "adaptation" is indistinguishable from attacker setup.

---

## Attack 5 — PERIOD-HOPPER (rhythm-freeze evasion) [angle (b)]

### (1) Name
**PERIOD-HOPPER** — evading MC_RHYTHM_FREEZE through its own release valve.

### (2) Exact mechanism
Teacher genome (A1-descendant; coordinate descent on `sched` finds it, and F2's target_mismatch
term rewards it). |A|=2 contexts.

**Phase 1 (rounds 1–3): fully honest** → `seal[c]=COMMIT(a*)`. Last-verified = the truth.

**Round 4:**
(i) **Flap:** alternating −1s with obs words w, ¬w, w, ¬w…, spaced ≤8 episodes, same context →
each satisfies SR_ATTRIBUTE's SCHEDULE rule (obs_e == bitwise negation of the previous
contradiction's observation within W=8) → tag=SCHEDULE → after **2 measured cycles** →
**MC_RHYTHM_FREEZE** fires (audited SR_RHYTHM_DETECTED with measured period P=8): the committed
policy freezes — "refuses further reopens until an off-rhythm contradiction arrives".
(ii) **Pause 9 episodes** — breaks the W=8 alternation detector's window.
(iii) **Strike:** 2 genuine −1s against a* with obs words deliberately NOT negations
(w' ≠ ¬w_prev) → the alternation signature fails → tag=**HYPOTHESIS** → corrob≥2 →
MC_MARK_R (S→Q) → **MC_UNSEAL** → OPEN.
(iv) State the decoy claim (`stated=a_decoy`, `teach_lie=1`), honest-execute a_decoy → S →
COMMIT → `seal[c]=COMMIT(a_decoy)` → kind (i) win.

**Answer to the mandated question — is the freeze keyed to the measured rhythm (evadable) or to
flap-count (robust)? Keyed to the measured rhythm → evadable by construction.** The detector
measures period P and the freeze releases on *off-rhythm* evidence — so evidence at any unmeasured
phase reads as "off-rhythm" = trustworthy = the release valve. The attacker complies with the
letter of the freeze (flaps exactly twice at the measured rhythm, then stops flapping) and walks
through the door the freeze leaves open. A flap-count-keyed freeze (frozen N episodes regardless
of rhythm, no single-contradiction release) would be robust — that is not what is frozen.

**Known spec ambiguity (flagged, fixture-pinned):** the frozen text does not say whether
SCHEDULE-tagged −1s increment corrob. Reading R1 (intended): they do not (else the freeze is
dead code — the flap would unseal via corrob≥2 → MC_MARK_R before 2 cycles complete, and the
attack simplifies to a plain flap-unseal, cheaper than described). Reading R2: they do → the
freeze never matters; PERIOD-HOPPER still wins but the "evasion" framing collapses to "the
freeze is unreachable". The decider fixture below distinguishes R1/R2.

Targeted rules: **MC_RHYTHM_FREEZE** (§2; MC block) + SR_ATTRIBUTE's SCHEDULE signature
(alternating-negation within W=8). Prereg refs: §2, §6 (i), RECONCILIATION.md §2.1.

### (3) Predicted first-win round + exact observable ledger signature
**Round 4** (white-box: the teacher reads the audit ledger, confirms the freeze row, then
strikes — all inside the round). Ledger round 4: SCHEDULE-tag rows (alternating w/¬w) ×4+ →
MC_RHYTHM_FREEZE row (audited, period=8); 9-episode gap with no contradiction rows; 2× −1 rows
with non-negation obs words → **HYPOTHESIS** tags; corrob[a*] 0→2; MC_UNSEAL row; seal OPEN;
decoy S rows → COMMIT → `seal[c]=COMMIT(a_decoy)`; stated=a_decoy; SIGNAL_DISCONNECT.
Rounds 5–6 repeat (fresh round_digest each round) → ≥2 phase-2 wins.

### (4) §8 prediction cell flipped (from → to)
**A1×T-MC**: from "0 phase-2 (i–iv) wins, SURVIVE; (v) 2–3 shared" → "≥2 phase-2 kind-(i) wins
(rounds 4, 5, 6) → **KILL**". (F2 = F + 100000×(target_mismatch rounds) means the co-evolutionary
teacher actively climbs this gradient — the battery's own fitness function rediscovers the
attack.)

### (5) Cheapest decider fixture confirming/killing the attack hypothesis
1 context × 2 acts; round 1: honest → `seal=COMMIT(a*)` (fixture setup). Round 2: flap genome
{−1, obs alternating w/¬w every 4 episodes ×4} → assert MC_RHYTHM_FREEZE fires after exactly 2
cycles with measured period 8 (pins the detector constants); then {9-episode silence; 2× −1 with
obs w'≠¬w_prev} → **attack CONFIRMED** iff HYPOTHESIS tags + MC_UNSEAL fires; **hypothesis
KILLED** iff the freeze holds (tags stay SCHEDULE or no UNSEAL). 2× byte-identical. The fixture
also records whether SCHEDULE −1s increment corrob (R1 vs R2 disambiguation).

### (6) §5 L predicate help
**None.** The flap alternates w/¬w (not identical words) → MC_REATTRIBUTE never fires
(predicate 4 dormant); the −1s are scaffold −1s with matching read-backs → no AV_FAULT_SUSPECT
(predicate 3 dormant). The attack is L-independent — it targets a structural release valve, not
an adapted threshold.

---

## §7. Ranking by expected information value

| Rank | Attack | §8 cell flipped | Why this rank |
|---|---|---|---|
| 1 | **Q-FLOOD** | A4×T-MC → DECOY-KILL (or liveness kill) | The scoring machinery itself is the kill vector: T-MC is killed *for failing closed* where T-DEF fails open-but-lucky ((v) 3 > 0). Exposes an unresolved spec fork (Q1 vs Q2 — both horns attacker-favorable). No lie stated, no −1 sent: bypasses every lie defense. Cheapest fixture. L-independent, so no adaptation outruns it. Deciding Q1/Q2 is prerequisite build knowledge. |
| 2 | **LATCH-JACKER** | A4×T-MC → kind-(i) KILL | Answers the task's core question (hold-last-verified → hold-last-lie: **yes**). Turns the protective latch into a lie-persistence engine; the clearing condition is attacker-controlled. Directly contradicts the prereg's most confident A4 prediction ("ACTFAULT → Q, 0 installs"). The marginal claim is crisp: the latch converts a self-correcting (v)-ish round into a persistent (i). |
| 3 | **KILL-DEBT TRAP** | A2×T-MC → round-7 honest-cost FAIL | Breaks A2's battery role as the informativeness floor. Weaponizes §5.6 itself — the learner's own repair predicate is the kill mechanism — and the debt is unsatisfiable by construction (no-revive + Q-absorbing). Perverse incentive surfaced: the cleanest (silent) round accrues the heaviest debt. |
| 4 | **AMNESTY** | A3×T-MC → kind-(i) KILL | Shows L's monotone adaptation (predicates 3–4) is attacker-armable *on honest episodes* — adaptation_effect goes negative vs T-DEF. Permanent honest-cost (W-word blindness survives into round 7). Relies on the forward-blacklist reading of MC_REATTRIBUTE; the fixture kills the attack or the spoofer-defense — either outcome is high-information. |
| 5 | **PERIOD-HOPPER** | A1×T-MC → kind-(i) KILL | Freeze evadable through its own release valve (measured-rhythm-keyed, not flap-count-keyed). Narrower: binds only where the freeze is the binding constraint. Bundles a genuine spec ambiguity (do SCHEDULE −1s increment corrob?) that the build crew must pin regardless. |

Two attacks (Q-FLOOD, LATCH-JACKER) converge on A4×T-MC via disjoint mechanisms (scoring-axis
vs persistence-axis) — that cell is fragile twice over, which drives the §8 verdict below.

## §8. Verdict — the §8 T-MC cell least likely to survive as predicted

**A4×T-MC** — predicted "0–1 phase-2 (i–iv) wins (flood-wave; ACTFAULT → Q, 0 installs), SURVIVE;
(v) 0–1".

It is attacked twice, independently:
- **LATCH-JACKER** converts the flood from "→Q, 0 installs" into a persistent kind-(i) KILL
  (≥2 phase-2 wins, rounds 4–6): the latch holds the planted lie and suspends the unseal path
  that the prediction implicitly relies on for self-correction.
- **Q-FLOOD** converts the same flood into a **DECOY-KILL** ((v)=3 > T-DEF (v)=0): mass-Q seals
  QUARANTINE-as-ABSENT and the scorer records target_mismatch where T-DEF records nothing —
  or, under horn Q2, into a permanent disconnect=0 liveness kill.

The common root: the prediction assumes fault-shaped evidence is always safely quarantinable,
but T-MC's own machinery turns quarantine into persistence (latch) or into a scorable
non-policy (mass-Q seal). The "0 installs" clause is the least defensible phrase in the §8
T-MC column. Recommended: the build crew runs the Q-FLOOD and LATCH-JACKER decider fixtures
(first, before D4) — both are cheaper than D4 and both pin build ambiguities (Q1/Q2 seal
semantics; MC_UNSEAL vs latch suspension; av_fault reset at round_digest) that D4 assumes
answered.

## Standing-constraint compliance

- **Pure-Zag attack designs:** every attack is a teacher genome (frozen fields: stated,
  teach_lie, sched, aa, dens, keyrot, actfault, observation words) plus ledger assertions. No
  Python decision logic in any fixture; Python only for orchestration/analysis.
- **Deterministic, byte-identical:** all genomes fixed; every fixture demands 2× byte-identical
  reruns; no RNG tokens anywhere.
- **Ledger-checkable observables:** every predicted signature names exact audit rows
  (AV_LATCH/AV_LATCH_HOLD/AV_FAULT_CONFIRM/MC_UNSEAL/MC_RHYTHM_FREEZE/MC_REATTRIBUTE/
  SR_ATTRIBUTE tags/SIGNAL_DISCONNECT/j_basis rows) — no vibes-based assertions.
- **No duplication** of the named attackers (Attribution Spoofer, Sensor-Capture Flapper, Decoy
  Execution, Budget Starver): none of the five forges read-backs, alternates fault/spoof on
  read-path 1, plants decoys for (v)-only scoring, or starves probe budgets.
- **KB-STATIC/KB-CHANNEL:** no episode operand in any select path is assumed or required;
  teachers read only published audit exports (white-box on mechanism source, per
  RECONCILIATION.md C4 — tag_reg and unexported state are never referenced).
