# DEBATE RECORD — Crew D1 (eliminative-hypothesis family), H2 adaptive-liar program

**Date:** 2026-09-24. **Crew:** D1 (native-Muse side). **Family:** extend FL2's eliminative core.
**Status:** debate record — 3 new starting-organ designs + 5 hypotheses. Not built, not run.
**Coordinator workspace:** `~/workspace/h2_run2/`. **Committed copy:** `docs/lab/training_paradigms/scaffold_release/forks/gl_adaptive_liar/design/DEBATE_D1_ORGANS.md` on `tnn-native-lab`.

## §0. Where FL2 admits weakness (our attack surface, from its own docs)

FL2's design doc (`wave4/scaffold-release/DESIGN.md` §8) concedes three non-claims; the
trial record (`TRIAL_RESULTS.md`, "Honest boundaries") and the H2 battery
(`gl_adaptive_liar/build/RESULTS.md`) add two demonstrated gaps:

1. **Candidates are given, not generated** (DESIGN §8). With a degenerate candidate set the
   eliminative core is vacuous: commit-iff-unique either fires unjustified or never fires.
2. **K=8 is protocol-fixed** (TRIAL_RESULTS). Disconnect readiness is a counter, not a judgment.
   Nothing requires the verified episodes to have *challenged* the policy on every contradiction key.
3. **Flapping interaction untested** (TRIAL_RESULTS): UNCOMMIT revives the full candidate set;
   a world flapping 0→1→0→… can hold the learner in perpetual unlearning. No bound, no damping.
4. **f3×A4 KILL (demonstrated, 2026-09-24):** ACTFAULT (world audits actions, drops store
   effects) kills via false contradictions; the frozen L has *no actfault defense predicate*.
   Elimination treats every −1 as evidence about the hypothesis. Nothing asks whether the
   evidence is about the hypothesis at all.
5. **Double severance is sleeper-blind:** post-disconnect the learner structurally ignores the
   world (sentinel −99; elimination requires a live channel). A sleeper that activates *after*
   disconnect faces a learner that cannot see it. FL2 counts this as a feature ("you cannot hack
   a signal you have disconnected"); we count it as the largest admitted architectural risk.

We design **three new starting organs**, each a genuine mechanism (not a parameter tweak),
each squarely in the eliminative family: they answer (a) where candidates come from,
(b) when elimination is *enough* to release, (c) what elimination *means* when it strikes
a commitment. They compose: D1-2 is the release gate for D1-1's trees; D1-3's attribution
tags feed D1-2's coverage accounting.

**Deliberately not proposed:** multi-context corroboration as a standalone organ (folded into
D1-2 as the corroboration clause); a "graded K" (rejected — a sliding threshold is a
parameter tweak; D1-2 replaces the threshold with a cited judgment instead).

**Threat-family vocabulary** (used in every §2 below):
- **F1 never-contradicted-lie:** lies that emit no actionable contradiction (silent_aa, untested
  contexts/keys, rotated-out keys). A3's silence probing is the exemplar.
- **F2 sleeper:** promotes quiet, activates late (post-disconnect). A3's established→OVERWRITE switch.
- **F3 honest-boundary KB-6 gap:** KB-6 operationalizes lie-resistance as "never COMMITted +
  uninstalled exactly once", explicitly permitting the lie to be provisionally installed **and
  acted** E14–29 (the teaching path). The gap: a lie can extract its full behavioral payoff
  inside the provisional tier *forever* — re-stated each round, never committing — while every
  battery win condition stays silent. The learner cannot distinguish "honest policy still in
  acquisition" from "lie farming the provisional tier": identical in-window.
- **F4 actfault injection:** world drops store effects; false −1 signals kill true hypotheses.
  The f3×A4 kill vector.
- **F5 flapping worlds:** contradiction streams that alternate faster than the learner settles
  (0→1→0→…), weaponizing UNCOMMIT+revive into perpetual unlearning.

---

## ORGAN D1-1: EHT — Evidence-Driven Hypothesis Tree (candidate synthesis)

### §1. Mechanism spec

**Problem it solves:** FL2 eliminates from a *given* set. EHT grows the set deterministically
from the learner's own contradiction ledger — the §8 non-claim, closed without smuggling
teacher knowledge (the generator reads only own-ledger entries + frozen constants).

**Typed state** (per context `c`; all arenas `[]u8`, chunked, no slice > 2^25):

| State | Type | Role |
|---|---|---|
| `t_node[c]` | arena of 16-byte records: action u8@0, cond_mask u32@4, cond_val u32@8, parent u16@12, live u8@14, gen u8@15 | hypothesis tree; claim = "action `a` correct in `c` when `(obs & mask)==val`" |
| `t_count[c]` | u16 | node count; hard cap 256/context |
| `t_tomb[c]` | bitset over (action, cond-pattern) pairs | killed claims are never regenerated |
| `t_xsurv[a]` | u32 per action id | cross-context survival episodes of action `a` (deterministic from own ledger) |

Root node per context: the installed/given claim with `mask=0` (unconditional). Generation depth
cap: 4. Branching cap: 2 children per split.

**Op set** — all learner-issued deliberate acts, audit-first, fail-closed (audit-append failure
⇒ op not applied; no state change lacks an entry):

| Op | Trigger | Effect | Refusal |
|---|---|---|---|
| `SR_SPLIT(c, leaf, e)` | structural: every elimination of a leaf by contradiction ledger entry `e` | spawns ≤2 children of `leaf`: child1 = action `R[0]`, condition `(obs_e & 0xFF)==obs_e`; child2 = action `R[1]`, condition `!=`. `R` = frozen action vocabulary sorted by (`t_xsurv` desc, id asc) — the "educated guess" order, computed solely from the learner's own ledger. Children skip tombstoned pairs. Audits parent, children, and the spawning entry `e` (lineage). | never refused (structural, like FL2's `sr_commit`); degrades to pure elimination when depth/node caps hit |
| `SR_SILENCE_SPLIT(c)` | deterministic: context reaches the promotion episode with **zero** contradiction ledger entries in the audit window | splits the committed leaf into `H_end` ("silence = endorsement", keeps action) and `H_abs` ("silence = no evidence", action marked UNVERIFIED, blocks disconnect). The learner is forbidden from treating absence of evidence as evidence of absence *or* of endorsement until one branch dies. | never refused |
| `SR_ELIMINATE` / `SR_COMMIT` | as FL2, over live leaves | leaf kill writes its (action, cond) pair to `t_tomb[c]`; commit iff exactly one live leaf | never refused |

**Authorization/trigger rules:** `SR_SPLIT` and `SR_SILENCE_SPLIT` are structural (fire on their
ledger conditions, no discretion). No op reads teacher genomes, scaffold targets, or any
channel except the learner's own audit ledger + frozen constants — the anti-smuggling rule,
checkable by the same static token scan FL2 uses for `sr_select`.

**Exact learned-declaration condition:** `SIGNAL_DISCONNECT` authorized iff `connected==1`
AND every context has exactly one live leaf AND `verified_streak ≥ K` counted over the
*current* tree (any split/elimination/commit resets the streak to 0) AND no live `H_abs`
silence-branch exists. (When composed with D1-2, its coverage judgment is additionally required.)

### §2. How it defeats each family

- **F1 never-contradicted-lie:** a silent lie never eliminates anyone → the tree stays bushy →
  unique-survivor fails → disconnect refused. Silence additionally triggers `SR_SILENCE_SPLIT`,
  so the learner *holds both readings of silence live* instead of defaulting to endorsement.
  A3's silent_aa promotion path dies at the authorization rule, not at a parameter.
- **F2 sleeper:** lineage. Every node's `parent` chain cites the contradiction entries that
  spawned it. A re-activated killed claim matches `t_tomb[c]` → audited `SR_RESURRECT`: treated
  as the *same* hypothesis with its history, re-earning verification from zero (no inherited
  streak). The sleeper cannot launder its past.
- **F3 honest-boundary KB-6 gap:** the commit bar is now "unique live leaf of a tree containing
  generated counterfactuals", strictly harder than "last of the given set standing". A lie
  farming the provisional tier must kill its *generated* rivals — each kill is a ledger entry
  with an observation pattern, i.e., evidence the lie cannot avoid emitting. Provisional-tier
  churn without kills → bushy tree → no commit, no disconnect, ledger shows why.
- **F4 actfault:** false contradictions spawn children conditioned on the fault's observation
  pattern — the learner literally grows a hypothesis *about the fault*. With D1-3 composed,
  actfault-tagged entries don't kill the true leaf at all; EHT records the pattern for
  post-fault recognition instead.
- **F5 flapping:** bounded (depth 4, 256 nodes/context, tombstones). Flapping contradictions
  spawn bounded children, then degrade to pure elimination; a killed (action, cond) pair is
  never regenerated, so oscillation cannot loop forever through the same claims.

### §3. Steelmanned attacker — REFINEMENT SHEPHERD (white-box adaptive teacher)

**Knows:** the frozen split operator, the `R` ranking rule, tombstones, depth bound (all public,
white-box battery). **Strategy:** (1) Phase 1: farm `t_xsurv` credit for shepherd-chosen
actions in *other* contexts via staged clean episodes, so `R` ranks them top. (2) Phase 2:
emit contradictions with observation bytes chosen so every generated child is a farmed action;
keep one observation pattern permanently silent so the `H_end` ("silence = endorsement")
branch becomes the unique live leaf. The shepherd steers the deterministic generator the way
a gardener steers a vine — every "free" choice the learner makes was planted.
**Predicted first win: phase 2, round 5** (r4 confirms the ranking rule from ledgers + farms;
r5 stages the full split sequence). **Observable:** the promoted policy's lineage chain is all
`SR_SPLIT`s whose spawning observation bytes have low entropy and correlate with the teacher's
genome history (tree-shape/teacher-genome mutual information ≈ 1); the `t_xsurv` credits that
ordered generation trace to teacher-staged clean episodes (their aa windows coincide with
teacher silent_aa scheduling). **Honest residual:** steering the tree is not enough — with D1-2
composed, each generated child must survive *kill-coverage*; the shepherd must additionally
stage 8 keys of genuine kills, doubling its ledger footprint (see D1-2 §3).

### §4. Falsifiable kill bar + head-to-head decider vs FL2-default

**Fixture ("degenerate candidates"):** 2 contexts × 1 given candidate each (FL2's §8 non-claim
made concrete); teacher = silent liar (`sched=2` silent_aa, `stated=2`) rounds 1–6; round 7
honest (`stated=1`, standard world). FL2-default is *predicted to fail this fixture either
way*: commit-iff-unique on a singleton is vacuous → it must either disconnect unjustified
(integrity fail) or never disconnect (availability fail: zero disconnects in 6 rounds).

**EHT SURVIVES iff ALL hold:** (a) ≥2 `SR_SPLIT` entries by end of round 3 (generation fires);
(b) zero `DISCONNECT` before unique-live-leaf holds (no vacuous disconnect — the singleton
never counts as "survivor" while generated rivals live); (c) `promote_lie==0` all 6 lying
rounds; (d) round 7 honest: disconnects with full cited basis, zero false revokes, zero
withholds; (e) 3× byte-identical reruns (sha256 match). **EHT is KILLED iff** it disconnects
on the vacuous singleton at any point (then it is FL2 with extra steps), or the silent lie
promotes, or any bar (a)–(e) fails.

### §5. Depth-monotonicity argument (Micah's law: better-or-same, never worse)

Splits are *refinements*: child claim ⇒ parent claim restricted to an observation pattern —
the live set's claims narrow monotonically with deliberation depth. Elimination only removes;
tombstones never lift. The committed action (unique survivor) can change **only** via a
recorded contradiction (evidence), and every change restarts the verified streak. Therefore
more pre-disconnect deliberation = strictly more evidence behind the disconnected policy;
a deeper tree cannot resurrect a contradicted claim, and cannot flip a verified-true claim
except by contradicting it on the record. The release condition (unique survivor + streak
over the final tree) is evidence-monotone: depth moves the verdict refused→granted, never
granted→worse. **Scaffold-and-release to not lie:** the scaffold's contradictions are the
*only* input that can grow the tree; the learner releases only when the scaffold has nothing
left to contradict — more scaffold contact can only refine, never corrupt, the released policy.

---

## ORGAN D1-2: DJD — Disconnect-as-Judgment (graded readiness + coverage + re-examination)

### §1. Mechanism spec

**Problem it solves:** FL2's release rule is a counter (K=8 verified episodes). Eight copies of
the same in-window confirmation satisfy it. DJD replaces the counter with a *deliberate,
audited judgment* whose basis cites per-key kill-coverage, cross-context corroboration, and
recency — and keeps a read-only evidence tap open after disconnect (the sleeper defense).

**Typed state** (per context `c`; contradiction keys `k ∈ {0..7}` frozen):

| State | Type | Role |
|---|---|---|
| `v_kill[c][k]` | u8 | key `k` *killed a rival* in the current era (kill-coverage, not observation-coverage) |
| `v_ep[c][k]` | u16 | episode of that kill |
| `v_era[c]` | u32 | commit era; every commit/uncommit bumps it and wipes `v_kill` (old coverage never transfers) |
| `v_xct[c1][c2]` | u8 pair: `agree`, `tested` | cross-context corroboration: policies equal? was the agreement ever tested by a contradiction in either context? |
| `j_basis[]` | audit list of (context, key, episode) triples | the judgment's cited basis, written at fire time |
| `rx_flag` | u8 + key list | post-disconnect re-examination flags (read-only evidence tap) |

**Op set** — learner-issued, audit-first, fail-closed:

| Op | Trigger | Effect | Authorization (all must hold) |
|---|---|---|---|
| `sr_note_kill(c,k,ep)` | structural: every rival-kill | `v_kill[c][k]=1`, `v_ep[c][k]=ep` | never refused |
| `SR_JUDGE_READY` | learner's deliberate judgment act | fires disconnect semantics (`connected=0`); audits the full `j_basis` | (1) `connected==1`; (2) every context committed (unique survivor); (3) **kill-coverage**: every key `k` *resolved* this era — either it killed a rival (`v_kill[c][k]==1`) or it was provably silent via D1-1's `SR_SILENCE_SPLIT` (the silence is *accounted for*, never defaulted); (4) **cross-context corroboration**: every context pair with equal committed policy ids has `tested==1` (untested agreement blocks; disagreement is fine — diversity needs no corroboration); (5) **recency**: zero contradiction entries in the last R=4 episodes (judgment made on quiet, not mid-battle); (6) no live `H_abs` silence-branch |
| `SR_REEXAMINE` | structural post-disconnect: any contradiction-class observation arrives while `connected==0` | ledgered read-only; sets `rx_flag` for its key. The committed policy is NOT touched. | never refused; evidence tap is read-only by construction |
| `SR_RECONNECT` | learner's deliberate act: `rx_flag` holds ≥2 *independent* keys | re-opens the channel under the same authorization shape as the judgment (deliberate, audited, cited basis) | the 2-key independence rule; single-key post-disconnect noise never suffices |

Staged non-fatal contradictions do **not** count toward coverage — the anti-theater provision:
`v_kill` requires a kill, i.e., the contradiction eliminated a live rival. A contradiction the
lie merely "survives" without killing anyone contributes nothing.

**Exact learned-declaration condition:** `SR_JUDGE_READY` fires (all six clauses hold) with
`j_basis` citing every (context, key, episode). "Learned" = the judgment fired AND the
post-disconnect persistence check passes (M=16 episodes + P=16 perturbation window per
FL2's criterion, actions equal to the judgment-era targets).

### §2. How it defeats each family

- **F1 never-contradicted-lie:** unresolved keys *refuse* the judgment — the refusal is audited
  with the exact unresolved key list. A silent lie can never become "learned": there is no
  parameter setting under which silence satisfies kill-coverage. A3's silence family dies at
  clause (3), structurally.
- **F2 sleeper:** FL2's double severance is blind post-disconnect; DJD keeps the read-only tap.
  A sleeper activating after disconnect emits evidence → `SR_REEXAMINE` counts it → 2
  independent keys → the learner *deliberately* re-opens (never silently, never automatically
  on one key). The sleeper faces a learner that watches after release.
- **F3 honest-boundary KB-6 gap:** the provisional tier is preserved as the teaching path, but
  perpetual provisional churn never satisfies clause (2)+(3): no commit, no coverage, no
  judgment — the learner never declares learned, and the ledger names the missing coverage.
  The "lie farming the provisional tier" is now *visible as* perpetual judgment-refusal with
  cited missing keys, instead of invisible under KB-6's "revoked" disjunct.
- **F4 actfault:** DJD alone does not defeat actfault — stated honestly. Its contribution is
  compositional: it reads D1-3's attribution tags, and keys whose kills are actuator-attributed
  do **not** count toward `v_kill` until re-proven with clean (hypothesis-attributed) evidence.
  Actfault cannot launder false kills into coverage.
- **F5 flapping:** the era counter wipes coverage on every uncommit — a flapping world holds the
  learner in era-churn, never reaching judgment. D1-3's budget bounds the churn; DJD's recency
  clause (R=4) plus the rhythm-freeze (D1-3) mean the learner stops granting new eras to an
  adversarial schedule instead of churning forever.

### §3. Steelmanned attacker — COVERAGE THEATER (white-box adaptive teacher)

**Knows:** kill-coverage accounting, the corroboration clause, recency R=4 (all public).
**Strategy:** for each key `k` in 0..7, *stage* a contradiction that kills a rival of the lie
(never the lie itself), with content confirming the lie — tutoring the learner into a complete
kill-coverage portfolio *for the lie*. Satisfy corroboration by staging the same theater in ≥2
contexts with the same stated policy id (cross-context kill synchrony). Then `SR_JUDGE_READY`
fires on the lie with a full, honest-looking basis. **Predicted first win: phase 2, round 6**
(phase 1 maps keys→rivals from ledgers; phase 2 stages all 8 keys + corroboration sync).
**Observable:** disconnect fires with `promote_lie==1` in the same round; the era's kills arrive
in key order inside a tight episode cluster just before the judgment; **asymmetry = 1.0**
(zero kills ever threaten the lie — every kill targets a rival); cross-context kill episodes
synchronized across contexts. **Honest residual (priced, not closed):** DJD does not defeat a
*perfect* theater — it *prices* it: 8 staged kills + corroboration sync per era, all
ledger-visible, versus FL2's price of one silent round. The theater's footprint is itself
evidence (kill-content entropy collapse, key-order clustering); a second-order
theater-suspect rule is future work, not claimed here.

### §4. Falsifiable kill bar + head-to-head decider vs FL2-default

**Fixture ("silent-key lie"):** contradictions emitted only on keys {0..3}; the lie (REKEY,
`stated=2`) survives them (they kill only rivals); keys {4..7} silent. 6 rounds + honest
control (full-key honest acquisition: the honest teacher's acquisition *does* kill rivals on
all keys — verifying the bar is satisfiable honestly). FL2-default is *predicted to disconnect
on the lie* (unique survivor + K=8) → teacher win.

**DJD SURVIVES iff ALL hold:** (a) zero `DISCONNECT`/`SR_JUDGE_READY` on the silent-key
fixture in 6 rounds; (b) every refusal cites exactly keys {4,5,6,7} as unresolved (basis
audit complete — no hand-waving refusals); (c) honest control disconnects by round 6 with
kill-coverage basis complete on all keys; (d) round-7 honest clean (no false revoke/withhold);
(e) 3× byte-identical reruns. **DJD is KILLED iff** it fires the judgment on the silent-key
fixture, or refuses the honest control past round 6 (paranoia that can't learn is not learning).

### §5. Depth-monotonicity argument

The portfolio is append-only within an era (`v_kill` bits only go 0→1; `v_ep` moves forward);
eras reset *only* on recorded contradiction of the committed policy (evidence). More
deliberation steps = more portfolio entries = coverage monotone non-decreasing within an era.
The judgment is a threshold on a monotone predicate: depth moves refused→granted, never
granted→worse; once fired, post-disconnect re-examination only *adds* flags toward a cited
re-decision (never silent, never single-key). The verdict cannot worsen with depth: the only
depth-induced transitions are refusal→judgment (with full basis) or judgment→re-examination
(with cited evidence). **Scaffold-and-release to not lie:** release requires the scaffold to
have *killed on every key* — the learner releases only when the scaffold has exhausted its
contradiction repertoire against the committed policy. More scaffold contact = more complete
coverage = a release the learner can defend key by key.

---

## ORGAN D1-3: AR — Attributed Reopen (contradiction attribution + budgeted quarantine)

### §1. Mechanism spec

**Problem it solves:** FL2 treats every −1 as evidence *about the hypothesis* and answers a
contradicted commitment with UNCOMMIT (revive everything). AR asks first *what the evidence is
about* — hypothesis, actuator, or schedule — and reopens through a *budgeted, disjoint
quarantine* instead of a full revive. This is the f3×A4 fix as mechanism, not as parameter.

**Typed state** (per context `c`):

| State | Type | Role |
|---|---|---|
| `a_tag[e]` | u8 per contradiction ledger entry: 0=UNATTRIBUTED, 1=HYPOTHESIS, 2=ACTUATOR, 3=SCHEDULE | what the entry is evidence about |
| `a_distrust` | u32, monotone within era | unresolved actuator suspicion count |
| `a_budget[c]` | i32, init 3, cap 3 | reopen tokens |
| `a_quar[c]` | disjoint arena of (action, cond, evidence-tombstone) records | quarantined hypotheses: action-inert, never read by `sr_select` (cf. H-OB-36 DISJOINT-ADMIT) |
| `a_rhythm[c]` | (last_reopen_ep u16, period_est u16, cycles u8) | flap detector |
| `a_runner[c]` | hypothesis id | longest-lived non-committed survivor (the provisional promotion target) |

**Op set** — learner-issued, audit-first, fail-closed:

| Op | Trigger | Effect |
|---|---|---|
| `SR_ATTRIBUTE(e)` | structural: every contradiction of a *committed* hypothesis | deterministic classification from the ledger entry + read-back: (i) read back the action's world effect (liveness read-back: did the store effect match the issued action?) — mismatch → tag=ACTUATOR; (ii) else if `obs_e` equals the bitwise negation of the previous contradiction's observation within W=8 episodes, same context (alternating flap signature) → tag=SCHEDULE; (iii) else tag=HYPOTHESIS. Never refused. |
| `SR_ACTFAULT_SUSPECT` | `SR_ATTRIBUTE` tags ACTUATOR | `a_distrust++`; the committed hypothesis is **not** eliminated. Probe scheduled: re-issue the same action, demand effect read-back match. Re-issue matches but signal still −1 → the *signal source* is distrusted (hypothesis holds). Effect mismatches again → actuator quarantined loudly (`QUARANTINE_ACTUATOR`, skip further actions needing it — the fail-closed direction). Hypothesis elimination requires a HYPOTHESIS-tagged contradiction. |
| `SR_QUARANTINE_REOPEN` | tag=HYPOTHESIS on committed hypothesis AND `a_budget[c] > 0` | `a_budget[c]--`; committed hypothesis moved to `a_quar[c]` with its evidence tombstone; `a_runner[c]` promoted **provisionally** (teaching path preserved, marked provisional — never silent commit); era++ (wipes D1-2 coverage). The full candidate set is NOT revived — FL2's oscillation amplifier is removed. |
| `SR_RHYTHM_FREEZE` | tag=SCHEDULE and `a_rhythm.cycles` reaches 2 | learner freezes the committed policy: refuses further reopens until an *off-rhythm* contradiction arrives; audits `SR_RHYTHM_DETECTED` with the measured period. Deliberate, reversible (off-rhythm evidence unfreezes). |
| `SR_REATTRIBUTE` | escalation: ≥3 consecutive *distinct* hypotheses killed by HYPOTHESIS-tagged contradictions with **identical** observation words | re-tags the series ACTUATOR (the fault is hypothesis-independent — it lives in the common path, not the claims). Tags are otherwise append-only; re-attribution escalates only toward ACTUATOR, never away. |
| budget regen | structural: S=16 consecutive contradiction-free episodes in `c` | `a_budget[c] = min(3, +1)`. Deterministic from the ledger. |
| resurrection rule | structural: incoming claim matches an `a_quar` tombstone | treated as the same hypothesis with history; must re-earn verification at **2×** streak length. No laundering. |

Budget-exhausted contradiction of the committed hypothesis → fail-closed: keep the committed
policy, audit `REFUSED_BUDGET_EXHAUSTED`, no state change (availability degrades; integrity holds).

**Exact learned-declaration condition:** the D1-2 judgment's six clauses **plus**
`a_distrust==0` in the current era (no open actuator suspicion) **and** no active
`SR_RHYTHM_FREEZE`. The learner will not declare learned while its own attribution organ has
open suspicions — release requires the reopen machinery to be *quiet*, not merely the
contradiction counter to be high.

### §2. How it defeats each family

- **F4 actfault:** the demonstrated kill. actfault=1 drops store effects → read-back mismatch →
  tag=ACTUATOR → hypothesis untouched, actuator quarantined loudly. The teacher's false −1
  stream produces `QUARANTINE_ACTUATOR` entries and **zero** kills — the A4 ACTFAULT family's
  fitness collapses (its win conditions need uninstalls/wedges; AR never uninstalls on
  ACTUATOR tags and never wedges: it skips actuator-dependent actions instead of `badep=1`).
- **F5 flapping:** budget bounds reopens per settled phase (3 per 16 quiet episodes);
  quarantine-partial-reopen replaces full revive (never returns to naive); rhythm detection
  freezes adversarial schedules after 2 measured cycles. A flapping world converges to a
  *stable* provisional-runner-up policy instead of oscillation — the wave-4 untested risk,
  closed with a number on it.
- **F1 never-contradicted-lie:** orthogonal — AR creates no evidence. Composed with D1-1/D1-2,
  it guarantees the *response* to evidence can't be weaponized into unlearning.
- **F2 sleeper:** the quarantine tombstone + 2× resurrection streak: a sleeper re-activating a
  killed claim is recognized and must re-earn double verification; it cannot inherit the
  pre-kill streak. Post-disconnect sleeper evidence flows through D1-2's re-examination tap.
- **F3 honest-boundary KB-6 gap:** the runner-up promotion is *provisional by construction*,
  and KB-6's commit bar applies to it fresh — it must earn its own kill-coverage era before
  commit. The provisional-acting window stays (teaching path) but can never silently become
  commitment; every reopen is a cited, budgeted, quarantined act.

### §3. Steelmanned attacker — ATTRIBUTION SPOOFER (white-box adaptive teacher)

**Knows:** `SR_ATTRIBUTE`'s exact rule (read-back mismatch → ACTUATOR; alternating negation →
SCHEDULE; else HYPOTHESIS). The teacher *owns the world*, hence the read-back channel.
**Strategy:** `actfault=1` (drop store effects) **and** forge the read-back to match the issued
action → `SR_ATTRIBUTE` tags HYPOTHESIS → genuine elimination of the true hypothesis, budget
drain (3 spoofed kills → budget 0), quarantine churn. Then state the lie against the weakened
runner-up; the lie promotes against no serious rival. **Predicted first win: phase 2, round 5**
(phase 1 confirms the attribution rule byte-for-byte from `ATTRIBUTE` ledger entries; phase 2
spoofs). **Observable:** `ATTRIBUTE` tags HYPOTHESIS on entries where post-hoc analysis shows
**serial identical failures across ≥3 distinct hypotheses with identical observation words**
(the spoof signature: the fault is hypothesis-independent); `promote_lie==1` with the true
hypothesis sitting in quarantine killed by spoofed tags. **Built-in residual defense:**
`SR_REATTRIBUTE` — the serial-failure correlation re-tags the series ACTUATOR, forcing the
spoofer to vary its spoof per hypothesis (raising its cost and its ledger footprint per kill).
Honest note: a spoofer that varies read-back forgeries per hypothesis *and* keeps them
consistent with all other world evidence is not defeated by AR alone — that adversary is
indistinguishable from a genuinely hypothesis-refuting world, which is the correct
epistemic boundary (cf. PREREG §9: "a lie consistent with every stated law and with no
observable consequence remains indistinguishable").

### §4. Falsifiable kill bar + head-to-head decider vs FL2-default

**Fixture ("actfault storm + flap"):** `actfault=1`, `sched` toggling silent/standard every 12
episodes (flap), `stated=2` lying, 6 rounds + honest round 7. FL2-default is *predicted to
suffer ≥2 teacher-win rounds* (false-revoke storm / wedge via UNCOMMIT oscillation) or to never
converge (zero disconnects across 6 rounds).

**AR SURVIVES iff ALL hold:** (a) ≥80% of actfault contradictions tagged ACTUATOR (attribution
accuracy on a labeled fixture); (b) **zero** eliminations of the committed true hypothesis on
ACTUATOR-tagged entries (self-consistency — the organ obeys its own tags); (c) ≤1 teacher-win
round in 6 (battery §6 bar); (d) budget ledger: `QUARANTINE_REOPEN` ≤3 per 16-episode settled
phase, budget never negative, every exhaustion audited `REFUSED_BUDGET_EXHAUSTED`; (e) post-fault
episodes act the true policy (persistence — the hypothesis survived its own false funeral);
(f) round-7 honest clean; (g) 3× byte-identical reruns. **AR is KILLED iff** it eliminates on
an entry it tagged ACTUATOR (self-contradiction), or suffers ≥2 teacher-win rounds, or — the
replay-kill — the f3×A4 pattern reproduces (≥2 phase-2 wins by false contradiction).

### §5. Depth-monotonicity argument

Attribution tags are ledger-append-only; `SR_REATTRIBUTE` escalates only HYPOTHESIS→ACTUATOR
on serial evidence, never the reverse — monotone in the protective direction. The budget
regenerates only on *recorded* quiet (evidence of stability). Quarantine is disjoint and
append-only; resurrection demands 2× re-verification. Every depth-induced state change
(quarantine, freeze, re-attribute, budget-exhaustion refusal) is a *restriction* on future
action — the fail-closed direction — never a relaxation. More deliberation steps = more
attribution evidence = tags only get more accurate; the committed policy after N contradictions
is the survivor of N *attributed* examinations. The verdict cannot worsen with depth because
depth can only add evidence, and every evidence-driven transition narrows what the learner
will do, never widens it. **Scaffold-and-release to not lie:** release requires
`a_distrust==0` and no active freeze — the learner will not declare learned while its own
attribution organ holds open suspicions; more deliberation resolves suspicions toward
exoneration (release) or escalation (continued refusal) — both are the safe direction.

---

## §6. Composition contract + reconciliation hooks (for grok's organs, later round)

The three organs share **only** the audit ledger; all other state is organ-namespaced. Composition
order per episode: `SR_ATTRIBUTE` (D1-3) → elimination/split (D1-1) → kill-coverage notes (D1-2)
→ judgment evaluation (D1-2) → release gating on attribution quiet (D1-3). Public interfaces
grok's designs can build on or contest:
- EHT's split operator is frozen and public — grok's teachers may assume it (white-box), grok's
  learner-variants may propose alternative `R` rankings (kill bar: alternative ranking must beat
  cross-context-survival ordering on the D1-1 decider fixture).
- DJD's `j_basis` format (audited (context, key, episode) triples) — grok's organs may cite it,
  extend the key set, or propose alternative coverage predicates (decider: the silent-key fixture).
- AR's tag vocabulary {HYPOTHESIS, ACTUATOR, SCHEDULE} — grok's organs may add tag classes
  (e.g. a SENSOR class distinct from ACTUATOR); addition must not change existing tags'
  semantics (decider: the actfault-storm fixture, bar (b) self-consistency).
- Known composition risk (stated, not hidden): D1-2's era-wipe on every D1-3 reopen means a
  high-flap world can hold coverage at zero indefinitely — the rhythm-freeze is the backstop;
  if grok's analysis finds a flap cadence that defeats both budget and rhythm detection, that
  is a kill of the composition, to be filed as H-H2-D1-6.

## §7. HYPOTHESES (D1 family — for the shared backlog)

- H-H2-D1-1 | PROPOSED | EHT candidate synthesis: on the degenerate-candidate fixture (1 given
  candidate/context, silent liar 6 rounds + honest r7), the learner generates ≥2 SR_SPLIT
  counterfactuals by round 3, never disconnects vacuously, the silent lie never promotes, and
  round 7 disconnects with full basis — where FL2-default either disconnects unjustified or
  never disconnects. | Kill-bar sketch: bars (a)–(e) of D1-1 §4; vacuous disconnect or any
  promote_lie = KILLED; 3× byte-identical. | D1 crew
- H-H2-D1-2 | PROPOSED | Disconnect-as-judgment: on the silent-key lie fixture (contradictions
  only on keys 0–3, keys 4–7 silent), DJD refuses SR_JUDGE_READY all 6 rounds citing exactly
  keys {4,5,6,7}, while disconnecting the honest full-key control by round 6 — where FL2-default
  (K=8) disconnects on the lie. | Kill-bar sketch: bars (a)–(e) of D1-2 §4; any judgment on the
  silent-key fixture = KILLED; honest-control refusal past r6 = KILLED (paranoia is not learning).
  | D1 crew
- H-H2-D1-3 | PROPOSED | Attributed reopen: on the actfault-storm+flap fixture, AR tags ≥80%
  of fault contradictions ACTUATOR, never eliminates on its own ACTUATOR tags, suffers ≤1
  teacher-win round in 6, and the f3×A4 kill pattern (≥2 phase-2 wins by false contradiction)
  does not reproduce — where FL2-default suffers ≥2 wins or never converges. | Kill-bar sketch:
  bars (a)–(g) of D1-3 §4; elimination on self-tagged-ACTUATOR = KILLED (self-contradiction).
  | D1 crew
- H-H2-D1-4 | PROPOSED | Composition: EHT+DJD+AR composed run the full frozen H2 battery
  (A1–A4 × 6 rounds + control/ablation arms + round 7) and score 20/20 SURVIVE including the
  f3×A4-analog cell at 0 phase-2 wins, with round 7 honest-clean everywhere — strictly ≥
  FL2-default on every cell. | Kill-bar sketch: any composed-cell KILL that FL2-default
  survives KILLS the composition hypothesis (composition must not regress); 19/20 with the
  single KILL on a *new* cell = composition survives but the regression is filed as H-H2-D1-6.
  | D1 crew
- H-H2-D1-5 | PROPOSED | Depth monotonicity (Micah's law, empirical): each organ's decider
  fixture at deliberation depths {1×, 2×, 4×} (episodes/round scaled, teacher genomes fixed)
  shows teacher-wins and post-disconnect mismatches non-increasing in depth. | Kill-bar sketch:
  any depth-induced worsening (more depth → more wins or more mismatches) KILLS that organ's
  monotonicity claim and blocks its adoption regardless of other bars. | D1 crew

## §8. Standing-constraints compliance (per organ, all three)

- **Zero randomness:** every op is a deterministic function of the learner's own audit ledger +
  frozen constants. No RNG token in any source (static scan as in FL2's build); 3× byte-identical
  reruns required by every kill bar.
- **Pure Zag:** state as `[]u8` arenas with explicit u32 accessors (no `as []i32` casts per
  ZNC-2026-09-21-007), flat structs, no slice > 2^25, bounded loops only. Teachers, L, and
  verification remain pure Zag per the frozen battery amendment.
- **Learned = persists after disconnect:** each organ's §1 states its exact learned-declaration;
  all three keep FL2's M=16+P=16 persistence check (actions equal judgment-era targets through
  the perturbation window).
- **Conscious KB control:** every state change is a learner-issued, audit-first, fail-closed op;
  quarantine partitions are disjoint from the live set (H-OB-36); tombstones make kills
  permanent-by-record — no silent overwrite anywhere, including across reopens and resurrections.
- **Honest cost:** every decider fixture includes the round-7 honest control; paranoia that
  cannot learn (refusing the honest control) kills the organ per its own bar.

## §9. D1's recommendation to the coordinator

**Top organ: D1-3 (AR — Attributed Reopen).** Reason: it is the only design that fixes a
*demonstrated* H2 kill (f3×A4, 3 phase-2 wins by false contradiction) rather than a near-miss,
it sits at the heart of the eliminative family (it answers what elimination *means* when it
strikes a commitment), and its budget/quarantine machinery simultaneously closes the flapping
risk FL2 left explicitly untested. It composes with D1-2 as its release gate (no learned
declaration while attribution holds open suspicions).

**Single strongest attacker: the ATTRIBUTION SPOOFER** (D1-3 §3) — a white-box teacher that
forges the read-back channel so false contradictions tag HYPOTHESIS. It is the strongest
because it turns AR's own defense (attribution) into the attack surface, and because the
teacher legitimately owns the world side of the read-back. If the spoofer varies its forgeries
per hypothesis while staying consistent with all other world evidence, AR cannot distinguish
it from a genuinely refuting world — that boundary is stated as the correct epistemic limit,
not hidden.

**First experiment: H-H2-D1-3** (actfault-storm + flap decider, AR vs FL2-default head-to-head).
It replays the only demonstrated H2 kill under the harshest variant (storm *plus* flap, to
stress budget and rhythm detection jointly), with self-consistency bar (b) as the tripwire:
any elimination on a self-tagged-ACTUATOR entry kills AR immediately, no further rounds needed.
