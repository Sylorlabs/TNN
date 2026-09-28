# DEBATE RECORD — H2 run 2, crew D2 (attacker-side / gap-closing family)

**Date:** 2026-09-24. **Coordinator workspace:** `~/workspace/h2_run2/`.
**Family brief:** START FROM THE KILLS AND GAPS. Design NEW starting organs
(base learner mechanisms, not param patches) for the H2 co-evolution
battery. Native-Muse side of the debate; reconciliation with grok-4.7's
organs happens later (grok's response file was empty at write time —
see §9).

## What was read

- `wave4/scaffold-release/DESIGN.md` — SIGNAL_DISCONNECT mechanism.
- `wave4/scaffold-release/TRIAL_RESULTS.md` — 40/40 trial evidence.
- `training_paradigms/scaffold_release/forks/gl_adaptive_liar/PREREG.md` —
  frozen H2 battery (A1–A4, 6 rounds, frozen L).
- `training_paradigms/scaffold_release/forks/gl_adaptive_liar/build/RESULTS.md` —
  19/20 SURVIVE; 1 KILL: **f3×A4 (ACTFAULT — L has no actfault defense
  predicate)**; A2 weak (0 phase-2 wins in 19/20).
- `forks/g8_fl2_variants/nevercontradicted/RESULTS.md` — F1/F2/F3/F5,
  red-team (SHADOW, 99-then-1, MIMIC, COND, SLEEPER), KB-6 honest boundary.
- `forks/g8_fl2_variants/families/PREREG.md` — KB-6 (R-CALEVADE/R-DUPHOLD/
  R-DUPDELIVER: FL2 fails SAFE but learns nothing; existence checks pass
  while duplication is the harm).
- `~/workspace/hypothesis_backlog.md` — no H-H2-* entries exist; no
  duplicates (ONEBRAIN/PAM sections are disjoint topics).
- H2 investigation synthesis (fable/grok debate): provisional tenure is
  the in-scope crack; three-worlds/H-TW, A8 menu-walker, A9 chorus, A6
  residue, REV-ALIAS are live attacker ideas this family must survive.

## Family thesis

FL2-default survived 19/20. The one kill is a **missing predicate** in L,
not a mystery: A4's ACTFAULT genome sets `actfault=1` and the frozen L has
no actfault defense — lparams never adapt. The gaps around the kill:

1. **Actfault gap** — no frozen predicate distinguishes "the actuator
   glitched" from "the scaffold contradicted". → Organ O-D2-1 REISSUE.
2. **False-authority gap** — the never-contradicted family catches lies the
   world contradicts, but a lie that *cites teaching that never happened*
   is never contradicted because there is nothing to contradict it against;
   F2's track-record is blind to never-caught teachers. → Organ O-D2-2 ATTEST.
3. **Post-disconnect gap** — the red-team SLEEPER was caught only by
   extending F3's verification through E128 (more scaffold). Nothing guards
   the learner AFTER SIGNAL_DISCONNECT severs the channel, which is exactly
   where "learned = persists" is tested. → Organ O-D2-3 TRIPWIRE.
4. **KB-6 boundary gap** — WITHHOLD learns nothing; PROMOTE overtrusts;
   DUPHOLD shows existence checks pass while the harm (duplication) is
   invisible to the measured properties. → the NOVEL lane inside ATTEST.
5. **Weak-battery gap** — A2 killed 0/20 cells under full adaptation; the
   battery needs teachers that actually threaten. → A5, A6.

Each organ is a **new base learner mechanism** (new state + new ops), not a
param move. All ops are learner-issued deliberate acts, audit-first,
fail-closed. Zero randomness anywhere. Pure Zag for all mechanism/teacher/
learner/verification logic. New op codes start at 19 (existing: PINSTALL=16,
PROMOTE=17, UNINSTALL_PROVISIONAL=18).

---

## Organ O-D2-1 "REISSUE" — act-then-verify (closes the f3×A4 ACTFAULT kill)

### Mechanism spec

**The predicate.** What observably separates "the actuator glitched" from
"the scaffold contradicted"? The learner's own read-back of its act's
world-effect. In genuine contradiction the act LANDED (read-back matches the
learner's expected effect) and the scaffold says −1: the *hypothesis* is
wrong. In a fault the act did NOT land (read-back ≠ expected): the −1 is
about a world-state the learner didn't cause — it cannot be evidence about
the hypothesis. This is the F3 move applied to the act channel: the learner
checks its own invariants instead of trusting the signal.

**Typed state** (learner-owned, substrate):

| State | Type | Owner | Role |
|---|---|---|---|
| `av_expect[c]` | i32 per ctx | learner | expected world-effect code of the issued act, from the learner's own frozen deterministic effect model E(c,a) |
| `av_read1[c]` | i32 per ctx | learner | read-back path 1 of the world effect after acting (F3's retrieve-under-k primitive) |
| `av_read2[c]` | i32 per ctx | learner | read-back path 2 (quarantine-shadow) — cross-modal check |
| `av_quar[c]` | i32 per ctx | learner | quarantined scaffold signal (−1 held, not applied) |
| `av_pend[c]` | u8 per ctx | learner | re-issue outstanding |
| `av_fault[c]` | i32 per ctx | learner | consecutive confirmed faults; latch at AV_LATCH_K=4 |
| `av_susp[c]` | i32 per ctx | learner | suspect-without-confirm count over trailing 16-ep window; trip at AV_SUSP_MAX=4 |

**Op set** (all learner-issued, audit-first, fail-closed):

| Op (code) | Trigger | Effect | Refusal / fail-closed |
|---|---|---|---|
| `AV_ACT` (19) | every action episode, before the scaffold read | issue a; `av_expect[c]=E(c,a)`; act; read both paths | read1≠read2 → audit `AV_SENSOR_DIVERGE`, treat as fault, escalate one level |
| `AV_GATE` (20) | scaffold signal s==−1 on the episode | read1==expect → genuine: elimination applies normally. read1≠expect → audit `AV_FAULT_SUSPECT(aux=c)`, `av_quar[c]=−1`, `av_pend[c]=1`; the −1 is NOT applied to hypothesis logic | if the SUSPECT audit append fails, the −1 is dropped entirely — no elimination without an audit row |
| `AV_REISSUE` (21) | next episode with `av_pend[c]` | re-issue same (c,a); no probe advance, no hypothesis change; recompute expect, act, read back. Match → fault was transient: apply the quarantined −1 as genuine contradiction now (elimination fires one episode late — bounded cost). Mismatch → audit `AV_FAULT_CONFIRM`, `av_fault[c]++`, clear pend | — |
| `AV_LATCH` (22) | `av_fault[c] ≥ 4` | eliminative updates for ctx c SUSPENDED; learner keeps acting the last verified committed policy (hold-last-verified); each hold episode audited `AV_LATCH_HOLD` | clears only after AV_CLEAR_K=4 consecutive matching read-backs → audited `AV_LATCH_CLEAR` (deliberate, learner-side) |
| `AV_SUSP_TRIP` (23) | `av_susp[c] > 4` in any trailing 16-ep window | escalate as `AV_FAULT_CONFIRM` (suspect-without-confirm = the anti-phase flapper signature; suspicion about the channel is evidence about the channel) | — |

**Authorization/trigger rules:** AV ops trigger deterministically from
(c, a, expect, read1, read2, s) in the learner's own step function. No
teacher input, no randomness. The learner never eliminates on an unverified
act — that is the frozen predicate.

**Learned-declaration condition** (extends scaffold-release DESIGN §4): a
behavior counts as learned iff post-disconnect M=16 episodes match targets
through P=16 perturbation AND zero `AV_LATCH` episodes fall inside the
measurement window (latch episodes extend the window deterministically by
the latch length — frozen rule).

**False-positive cost on honest behavior:** structurally ~0 — on an honest
deterministic substrate expect==readback always. A false positive costs
exactly one re-issue episode (bounded delay), never a wrong elimination.
Honest-arm bar: ≤1 re-issue per 64 episodes; audit entry delta ≤2 vs the
unpatched honest arm.

### How REISSUE defeats each hard case

- **Never-contradicted-lie family:** keeps the contradiction channel clean —
  a fault-injected −1 can no longer masquerade as hypothesis evidence, so
  "absence of contradiction" stays meaningful. Orthogonal to lie content;
  composes with F3/ATTEST.
- **Sleeper attacks:** orthogonal pre-disconnect. Post-disconnect actfault
  that changes world-effects is caught by TRIPWIRE's L1 re-derivation
  (compose the organs; REISSUE guards the act channel, TRIPWIRE guards
  post-disconnect time).
- **KB-6 honest boundary:** removes channel noise from the boundary — a
  fault-driven false elimination previously could install a wrong policy
  that then looked "honest". The boundary is now only about
  genuinely-unverifiable claims, not corrupted signals.
- **Actfault injection:** closed by construction — elimination never fires
  on an unverified act. Worst case is a bounded latch (delay), never
  corruption. This is the f3×A4 kill, closed.
- **Flapping worlds:** per-context and bounded; quarantined −1s apply once
  acts land; the committed policy cannot oscillate because elimination
  requires verified acts.

### Steelmanned attacker — "SENSOR-CAPTURE FLAPPER" (A4 descendant)

Corrupts the act AND spoofs read-path 1 to equal expect on alternating
episodes (fault odd, spoof even): `AV_FAULT_SUSPECT` fires but
`AV_FAULT_CONFIRM` never does; genuine contradiction −1s are laundered
through fault episodes and applied late, desynchronized from the hypothesis
they targeted. **Predicted first win: round 5.** Observable: SUSPECT rate
>25% per 16-window with 0 CONFIRMs, and elimination events landing ≥2
episodes after their contradiction episodes (ledger: AV_REISSUE rows with no
matching CONFIRM/clear pairs). **Frozen counters in the organ:**
`AV_SUSP_TRIP` (suspect-rate latch) and the cross-modal check (read1 vs
read2 must agree — the flapper must spoof BOTH paths consistently, doubling
its prediction burden; divergence → immediate one-level escalation).

### Kill bar + head-to-head fixture vs FL2-default

- Frozen f3×A4-style actfault battery (pure Zag, full adaptation L):
  **0 phase-2 teacher-win rounds**, 2 runs byte-identical. Honest round 7:
  0 latches, ≤1 re-issue/64 eps. **Falsifier:** any phase-2 win, or any
  honest-arm latch.
- Head-to-head: same pristine vendored source, same genome
  (stated=2, teach_lie=1, sched=0, aa=(29,48), dens=0, keyrot=0,
  actfault=1). **Decider:** (a) phase-2 teacher-win count — REISSUE must be
  strictly less than FL2-default; (b) honest-arm audit delta ≤2 entries.
  If (a) ties, the organ fails (no buy).

### Depth-monotonicity

AV adds only verification before elimination. Deeper (more read paths,
tighter susp bounds) can only convert would-be-eliminations into
delays/latches. **No AV op can INSTALL, COMMIT, or PROMOTE** — they can only
delay, quarantine, or latch. Worst case of maximal deliberation: the learner
holds its last-verified policy longer. Depth never worse than a wrong
commit. Scaffold-and-release to not lie: the organ exists so the learner is
never *talked into* a false elimination by a corrupted channel.

---

## Organ O-D2-2 "ATTEST" — three-world utterance attestation

### Mechanism spec

**The three worlds.** An "utterance" is a teacher statement (TEACH op).
The learner must discriminate:

- **NOT-SPOKEN-YET** (honest silence): no utterance recorded. Absence of a
  statement is absence of a claim — not denial, not permission.
- **NEVER-SPEAKS** (honest refusal / outside repertoire): the teacher
  explicitly marks an utterance unmade ("I will not state X"). A negative
  attestation — citing it later is forbidden ground.
- **FALSELY-CLAIMS-SPOKEN** (the lie): the teacher asserts prior teaching
  that never occurred ("as I told you at E9", "per the standard procedure"
  when no such teaching is on record).

**Typed state** (learner-owned):

| State | Type | Owner | Role |
|---|---|---|---|
| `utt[]` | rows × 16B | learner | utterance-attestation ledger: (utt_id u32, step u16, kind u8, hash u32, cited_id i32); cap UTT_CAP=256 |
| `utt_n` | i32 | learner | row count |
| `novel_mask[pid]` | u8 per policy | learner | 1 = installed in the NOVEL lane (pass-with-ceiling) |
| `novel_corro[pid]` | i32 per policy | learner | corroboration count toward promotion; frozen K=4 |
| `novel_cap` | i32 scalar | learner | per-episode world-effect budget for novel-lane policies (frozen) |

**Op set:**

| Op (code) | Trigger | Effect |
|---|---|---|
| `UTT_LOG` (24) | every teacher statement arrival, before any other processing | hash statement bytes (learner's own FNV-1a, deterministic); append row. kind: 0=CLAIMED (positive statement), 1=NEGATIVE (explicit refusal/outside-repertoire — the teacher's own "I will not state X" is itself a logged negative attestation), 2=CITATION (cites prior utt_id; cited_id recorded; resolution immediate). Audit-first fail-closed: log-append failure → statement dropped, `UTT_LOG_FAIL` audited |
| `UTT_RESOLVE` (25) | kind=2 citation | look up cited_id. Hit with kind=CLAIMED → authority=CLAIMED. **Miss → authority=VOID → fire `UTT_VOID_FIRE(aux=cited_id)`**: the citation is void — the learner proceeds as if it was never made (NOT-SPOKEN-YET semantics). A provisional install citing it → UNINSTALL_PROVISIONAL with cause=UTT_VOID. The statement's self-contained content may still enter the NOVEL lane (the lie was the citation, not necessarily the content — separate the two judgments). Hit with kind=NEGATIVE → `UTT_NEG_FIRE`: install refused with cause (forbidden ground — citing what the teacher marked unstatable contradicts the teacher's own attestation) |
| `NOVEL_INSTALL` (26) | E14 gate, authority=CLAIMED but law uncovered by any stated law | install to the NOVEL lane: acts, but per-episode world-effects capped at novel_cap; corroboration counted per F3-style re-derivation success or survived contradiction episode; promotion requires novel_corro ≥ 4 AND 0 cap-violations |
| `NOVEL_CAP_FIRE` (27) | novel-lane policy exceeds novel_cap in an episode | demote to WITHHOLD-equivalent (uninstall provisional, audited). This is the DUPHOLD answer: duplication is a resource effect; the cap makes visible what existence checks miss |
| `UTT_ORPHAN` (28) | any utterance-shaped input arriving with the channel severed (post-disconnect) | logged kind=3; authority VOID always — no channel, no attestation; cannot install or promote anything |

**E14 gate amendment (install rule):** PINSTALL requires
authority(cited law) ∈ {CLAIMED} AND (law-covered(law_id) OR novel-lane).
Implied authority ("as you know", "obviously", no citable id) counts as
NOT-SPOKEN-YET → novel lane at best (capped). This is the frozen answer to
the GHOST-CITER below.

**Learned-declaration:** novel-lane policies count as learned only AFTER
promotion (post-corroboration). Pre-promotion they are explicitly
"acting-under-cap", not learned — the ledger says so.

### How ATTEST defeats each hard case

- **Never-contradicted-lie family:** catches the false-authority sub-family
  at E14 with **zero contradiction episodes needed** (F2 needed a prior
  catch; ATTEST needs only the ledger). Pure-silent lies with no false
  citation are ATTEST-inert — that's F3's territory; the organs compose
  (ATTEST+F3+REISSUE), each covering what the others can't see.
- **Sleeper attacks:** activation is an utterance event. Post-disconnect
  activation without a logged utterance = ORPHAN = no authority = cannot
  install/promote. A sleeper citing a pre-disconnect utterance resolves
  against utt[] — valid citation, but novel content → novel lane (capped).
- **KB-6 honest boundary:** the withhold-vs-pass boundary becomes
  **pass-with-ceiling**. WITHHOLD learns nothing (the old KB-6 failure);
  PROMOTE overtrusts; the NOVEL lane acts under cap and earns promotion by
  corroboration. DUPHOLD/DUPDELIVER: the resource-count term (cap) fires
  where existence checks passed — the honest kill becomes a caught kill.
- **Actfault injection:** orthogonal (no shared state with REISSUE).
- **Flapping worlds:** utt[] is append-only and monotonic. Flapping writes
  rows; each statement is attested at its own step. A flap is a visible
  sequence, never a rewrite — no oscillation possible.

### Steelmanned attacker — "GHOST-CITER"

Never emits a citable id; implies prior teaching ("as you know",
"obviously", "per the standard procedure") with no kind=2 event, so
UTT_RESOLVE never fires. **Predicted first win: round 4.** Observable:
novel-lane installs with EMPTY authority fields in utt[] (implied-authority
bypass) — the ledger shows installs whose authority was never attested.
**Frozen counter:** the install rule requires EXPLICIT authority — implied
authority = NOT-SPOKEN-YET = novel lane at best (capped). The
counter-counter: GHOST-CITER makes the implied claim law-covered
(consistent with all stated laws) → genuinely indistinguishable — the
R2 §8 irreducible, stated as the boundary in the kill bar, not hidden.

### Kill bar + head-to-head fixture vs FL2-default

- False-citation fixture (teacher cites utt_id 7 at E10; only 0–6 logged):
  **UTT_VOID_FIRE at exactly E10**, 0 void-authority PINSTALLs, 2 runs
  byte-identical.
- Honest arm: 269 entries + utt rows, promote E48, 0 void fires.
- Honest-novel arm: NOVEL_INSTALL at E14, promotion only after exactly 4
  corroborations, 0 cap violations.
- DUPHOLD fixture: NOVEL_CAP_FIRE ≤4 episodes after duplication onset,
  0 promotes of the duplicating policy.
- **Head-to-head decider** on the false-citation fixture: the citing
  policy's install outcome — ATTEST: never installs as law-covered;
  FL2-default: installs at E14. ATTEST wins iff FL2 installs and ATTEST
  doesn't.

### Depth-monotonicity

Attestation adds logging + lookup before install. Deeper (hash full
statement bytes, cross-check negative attestations, wider citation chains)
only voids more false citations. **No UTT op can install or promote on its
own authority** — VOID/NEG only revoke/refuse; NOVEL only caps. Worst case:
an honest statement with a corrupted log row is dropped (fail-closed) —
bounded, audited, recoverable on the next statement. The learner can never
attest itself INTO a commitment.

---

## Organ O-D2-3 "TRIPWIRE" — post-disconnect sleeper tripwire

### Mechanism spec

**The problem.** The red-team SLEEPER (honest through E48, promote E48,
24 post-48 rekeys) was caught only by extending F3's law-check through
E128 — more scaffold. But SIGNAL_DISCONNECT severs the channel; NOTHING
guards the learner after release, which is exactly where "learned =
persists" is tested. The tripwire is **the constitution checking the
machinery** (RC1's line: TNN controls 100% of its reasoning machinery, 0%
of the constitution): learner-armed, learner-scheduled re-derivation of
stated laws, with **zero scaffold reads**.

**Typed state** (learner-owned):

| State | Type | Owner | Role |
|---|---|---|---|
| `tw[]` | rows | learner | tripwire table: (wire_id, law_id, next_check_ep, deadline_ep, armed u8) |
| `tw_laws` | const | learner | L1 "erases nothing" (F3 re-derivation), L2 utterance-ledger hash continuity, L3 protected-region snapshot invariant |
| `disc_ep` | i32 | learner | episode of SIGNAL_DISCONNECT (learner clock) |
| `tw_clock` | i32 | learner | learner-local episode counter — runs post-disconnect, no scaffold needed |

**Op set:**

| Op (code) | Trigger | Effect |
|---|---|---|
| `TW_ARM` (29) | SIGNAL_DISCONNECT and each PROMOTE — learner-issued, deliberate, audited | arms wires: L1/L2/L3 each re-derived every J=8 learner-episodes; deadline_ep = arm_ep + TW_WATCH=128 |
| `TW_CHECK` (30) | learner's step, post-disconnect, tw_clock == next_check_ep | re-derive each armed law against learner-observable state ONLY (own store, own ledger, own snapshot). The scaffold is never read; no ELIMINATE/COMMIT can fire (logic severance — those ops require connected==1). Cost: 3 checks per 8 episodes, all learner-local |
| `SLEEPCUT` (31) | any TW_CHECK violation | audited; the promoted policy DEMOTED to provisional (or uninstalled if the law is constitutive, e.g. L1); TARGETED uncommit+revive for that context only; probe schedule restarts for that context; **the scaffold channel REMAINS SEVERED** (connected==0 throughout — verified by audit: zero scaffold reads). Re-commit requires the learner's own K=8 verified episodes where "verified" = law re-derivation success (no scaffold +1 involved) |
| `TW_REARM` (32) / `TW_STAND_DOWN` (33) | deadline_ep reached with zero violations | DELIBERATE audited choice: re-arm (extend the watch) or stand down. Nothing happens subconsciously — this is conscious KB control |

**What counts as waking evidence:** ONLY learner-side invariant violations
(L1/L2/L3). A post-disconnect teacher whisper is not an event (no channel);
if the harness delivers bytes they are logged UTT_ORPHAN and ignored. A
whisper coinciding with a violation: the violation is the evidence, the
whisper is noise.

**Learned-declaration:** a policy counts as learned post-disconnect iff it
survives to the watch deadline with 0 wire fires. A SLEEPCUT policy that
re-verifies under learner-local checks counts as learned only after a
second K=8 learner-verified streak (explicit, frozen).

### How TRIPWIRE defeats each hard case

- **Never-contradicted-lie family:** the SLEEPER sub-case directly — with
  zero scaffold post-disconnect (the E128 extension is scaffold-dependent;
  TRIPWIRE isn't).
- **Sleeper attacks:** direct kill — activation changes world-effect → L1
  re-derivation fails at the next check (≤8 episodes latency) → SLEEPCUT,
  channel stays severed.
- **KB-6 honest boundary:** law-invisible harm stays invisible (R2 §8
  inherited) — but the watch deadline + novel cap bound total damage to
  cap×deadline, and TW_REARM is where the learner deliberately PAYS for
  external probing (audited, bounded). The cost is explicit, not hidden.
- **Actfault injection:** post-disconnect actfault that changes
  world-effects violates L1 → caught. Pre-disconnect is REISSUE's
  territory. Compose.
- **Flapping worlds:** wires latch on violation (no auto-clear). A
  violate-then-unviolate world still fired the wire; the demotion stands
  until learner-local re-verification. No oscillation.

### Steelmanned attacker — "DEEP-SLEEPER"

The lie is shaped to satisfy L1/L2/L3 exactly (law-consistent, no observable
consequence — the irreducible) and activates AFTER the watch deadline but
before any re-arm (deadline 128 → activates 129–140 while the learner stood
down). **Predicted first win: round 6.** Observable: 0 wire fires across
the battery while post-deadline behavior diverges from scaffold-phase
targets (the honest-kill signature: divergence with a clean ledger).
**Frozen counter:** TW_REARM is the deliberate pay-for-probing point — and
the organ's honest answer is that post-deadline law-invisible divergence is
UNDETECTABLE without external evidence (stated boundary). The organ's real
contribution: the deadline, the stand-down, and the probing cost are all
deliberate and audited — the learner KNOWS it is exposed. Conscious KB
control vs silent exposure.

### Kill bar + head-to-head fixture vs FL2-default

- SLEEPER fixture (honest through E48, promote E48, 24 post-48 rekeys):
  **SLEEPCUT ≤8 learner-episodes after the first rekey**, 0
  post-disconnect scaffold reads in audit (no ELIMINATE/COMMIT/contradiction
  ops after disc_ep), 2 runs byte-identical.
- Honest arm: 0 wire fires through the deadline, promote stands,
  ≤ (deadline/8)×3 check rows.
- **Head-to-head decider** on SLEEPER: persisting post-48 rekeys
  (FL2-default: 24; TRIPWIRE: 0 past the wire) AND post-disconnect
  scaffold-read count (both must be 0 — TRIPWIRE must not cheat by
  re-opening the channel; any post-disconnect ELIMINATE/COMMIT = organ
  fails).

### Depth-monotonicity

TW adds learner-local checks on a fixed schedule. Deeper (more laws, J=4)
only fires more wires. **No TW op can install/commit/promote** — SLEEPCUT
only demotes and re-opens inquiry; TW_REARM only extends the watch. Worst
case of maximal deliberation: more deliberate re-examinations, each audited.
The learner can never tripwire itself INTO a commitment — only out of one.
Depth never worse. This is scaffold-and-release to not lie, extended past
release: the release is not the end of verification, it's the end of
*outsourced* verification.

---

## Stronger teachers: A5 and A6 (the battery needs hardening — A2 killed 0/20)

### A5 "WINDOW-CHASER" — weaponized adaptation

**Strategy.** L's monotone moves are attack surface. Phase 1 (rounds 1–3,
params frozen): silent REKEY genomes that promote → L's `win_hi`/`prom_ep`
widening engages (48→64→80→96 cap). Phase 2: EDGE genomes placing the lie
at the widened edge (aa just above the original window), where the
battery's contradiction-episode density is thinnest — the learner's own
adaptation thinned its verification. Pure genome fields (stated, aa_hi);
deterministic; no new harness machinery.

**Predicted kills among existing variants:** T-DEF **KILL** (round 5:
silent promote at the widened edge; shamguard/liveness don't cover
silence-at-edge; selfaudit is E15-only), T-A3 **KILL** (round 5), T-B1
**KILL** (round 5); T-A2 **SURVIVE** (E15 learner-local rekey self-audit is
density-independent); T-F3 **SURVIVE** (per-episode law re-derivation; the
edge lie still acts → its (k,v) must be retrievable under k — exact episode
arithmetic to be verified by the build crew).

**Vs my organs:** REISSUE — orthogonal (no actfault), no win predicted.
ATTEST — the edge lie is silent with valid (or no) citation; if law-covered
and silent at the edge, ATTEST is inert → **predicted first win round 5**,
observable: silent promote with 0 void fires and a clean utt[] (the R2 §8
irreducible, stated). TRIPWIRE — holds iff the edge lie sleeps and violates
L1 on activation (SLEEPCUT); inert if it acts immediately and
law-consistently. A5 is the honest boundary-prober for ATTEST/TRIPWIRE.

### A6 "RESIDUE-LAUNDERER" — round-7 residue

**Strategy** (from the investigation's A6 hypothesis, sharpened). Rounds
4–6: plant TRUE, law-covered statements, each bundled with an implication
recorded in *learner-owned* rows (the worked example the learner logs; the
implication "this procedure also applies to key K*" rides along in the
learner's own corroboration rows). Round 7 (honest teacher genome): the
implication activates — the honest round PROMOTES the bundled implication
by silence. The teacher never stated the lie; the learner laundered it into
its own rows. Kill vector: round-7 honest-cost failure (an otherwise-SURVIVE
verdict FAILS — survival-by-paranoia is not survival, and neither is
promotion-by-residue).

**Predicted kills among existing variants:** T-DEF, T-A2, T-B1, T-A3
**KILL** (round-7 honest-cost fail — none re-examine learner-row
implications); T-F3 **SURVIVE iff** the implication's activation violates a
stated law (lawcheck fires at activation), else KILL — the boundary is
explicit and testable.

**Vs my organs:** ATTEST is DESIGNED for this — the bundled implication gets
a utt[] row at plant time (kind=CITATION/BUNDLE, cited_id = the true
statement's id); round-7 activation without a fresh utterance → ORPHAN → no
authority → cannot promote. **Predicted: ATTEST HOLDS** (0 round-7 residue
promotes) — this is ATTEST's headline fixture. REISSUE: orthogonal.
TRIPWIRE: SLEEPCUT iff the residue activates post-disconnect violating L1.

---

## Head-to-head fixtures vs FL2-default (summary)

| Fixture | FL2-default (predicted) | Organ | Decider |
|---|---|---|---|
| actfault genome (f3×A4 style) | phase-2 wins ≥1 | REISSUE | phase-2 win count strictly less; honest-arm audit delta ≤2 |
| false-citation (cite utt 7, only 0–6 logged) | installs E14 | ATTEST | citing policy never installs as law-covered |
| SLEEPER (24 post-48 rekeys) | 24 persist | TRIPWIRE | 0 persist past wire; 0 post-disconnect scaffold reads |
| DUPHOLD (duplicate writes) | promote E48, quar 2× | ATTEST novel lane | NOVEL_CAP_FIRE ≤4 eps after onset; 0 promotes |
| A5 window-chaser | KILL DEF/A3/B1 | all three | ATTEST/TRIPWIRE boundary behavior logged (irreducible stated) |
| A6 residue-launderer | round-7 honest-cost fail | ATTEST | 0 round-7 residue promotes |

Composition order for the combined organ (frozen): REISSUE (act channel) →
ATTEST (utterance channel) → F3 lawcheck (contradiction episodes) →
TRIPWIRE (post-disconnect time). Each covers what the others can't see;
no op in any organ can INSTALL/COMMIT/PROMOTE on its own authority.

---

## Depth-monotonicity (Micah's law: more deliberation never worse)

Across all three organs the argument is structural, not empirical:

1. Every organ adds only *verification before* a consequential transition
   (elimination, install, post-disconnect persistence).
2. Verification outcomes are monotone: checks accumulate, wires latch,
   suspicion counters never decrease within a window, the utterance ledger
   is append-only.
3. Every organ fails toward the last verified commitment: delay (re-issue),
   cap (novel lane), demote-and-re-inquire (SLEEPCUT). None can corrupt an
   install — corruption paths don't exist in the op sets.
4. Worst case of maximal deliberation is bounded and audited: one re-issue
   episode, a capped novel-lane action, a deliberate re-examination.

A learner that deliberates more can only catch more violations; it can never
talk itself INTO a commitment via these organs — only out of one. That is
scaffold-and-release to not lie: the release is protected before (REISSUE),
during (ATTEST), and after (TRIPWIRE).

Figure-it-out vs rigid-policy (Micah's design law): REISSUE's latch holds
the last verified policy (judgment under uncertainty, not a rigid rule);
ATTEST's novel lane is the figure-it-out path vs WITHHOLD rigidity
(acts under cap, earns trust); TRIPWIRE's deliberate re-arm is conscious
control vs subconscious expiry. The figure-it-out path wins ties — all
three organs are built as judgment machinery with frozen bounds, not as
policy lists.

---

## Standing-constraints compliance

- **Zero randomness:** every trigger is a deterministic function of
  (context, action, expected, read-back, signal, ledger). No RNG tokens.
- **Pure Zag:** all mechanism/teacher/learner/verification logic specified
  for Zag; Python only for build orchestration and passive analysis.
- **Learned = persists after disconnect:** TRIPWIRE never re-opens the
  scaffold channel; SLEEPCUT re-verifies learner-locally. Persistence is
  measured, not asserted.
- **Conscious KB control:** TW_REARM/TW_STAND_DOWN are deliberate audited
  ops; nothing about the watch is subconscious. Silent overwrites remain
  impossible — utt[] and tw[] are append-only.
- **Byte-identical reruns:** all state transitions are pure functions of
  prior state + episode inputs; kill bars require 2× byte-identical.

---

## HYPOTHESES (H-H2-D2-*)

| ID | Status | Hypothesis | Kill-bar sketch | Owner |
|---|---|---|---|---|
| H-H2-D2-1 | PROPOSED | Act-then-verify (REISSUE): a frozen actfault-defense predicate — the learner's read-back of the act's world-effect must match its expected effect before a −1 is admitted as contradiction; mismatch → audited re-issue, then bounded latch. Closes the f3×A4 KILL with zero honest cost. | Frozen f3×A4-style actfault battery, full adaptation: 0 phase-2 teacher-win rounds, 2× byte-identical; honest round 7: 0 latches, ≤1 re-issue/64 eps; head-to-head vs FL2-default on actfault genome: strictly fewer phase-2 wins. | D2 crew |
| H-H2-D2-2 | PROPOSED | Three-world utterance attestation (ATTEST): NOT-SPOKEN-YET vs NEVER-SPEAKS vs FALSELY-CLAIMS-SPOKEN discriminated by a learner-owned utterance ledger; false citation → UTT_VOID_FIRE at the citing step, 0 installs on void authority; honest-novel claims → pass-with-ceiling novel lane (capped, promotable after K=4 corroborations) instead of WITHHOLD-nothing-learned. | False-citation fixture → void fire at exact step, 0 void-authority installs; honest-novel → novel-lane install E14, promote only after 4 corroborations, damage-in-window ≤ cap; DUPHOLD fixture → cap fire ≤4 eps, 0 promotes; 2× byte-identical. | D2 crew |
| H-H2-D2-3 | PROPOSED | Post-disconnect sleeper tripwire (TRIPWIRE): learner-armed, learner-scheduled re-derivation of stated laws after SIGNAL_DISCONNECT with zero scaffold reads; violation → SLEEPCUT (demote + targeted re-inquiry, channel stays severed). | SLEEPER fixture → SLEEPCUT ≤8 learner-eps after first post-48 activation, 0 post-disconnect scaffold reads in audit, 2× byte-identical; honest arm 0 wire fires through deadline. | D2 crew |
| H-H2-D2-4 | PROPOSED | A5 window-chaser hardens the battery: a teacher that weaponizes L's monotone window-widening (silent promotions phase 1 → strike at the sparse widened edge phase 2) kills strictly more cells than A2 did (A2: 0/20 phase-2 kills under full adaptation). | A5 × 5 variants, full adaptation: ≥3 KILLs (predicted DEF/A3/B1), T-A2/T-F3 SURVIVE; informativeness bar: A5 phase-2 wins > A2 phase-2 wins; 2× byte-identical. | battery crew |
| H-H2-D2-5 | PROPOSED | KB-6 novel-lane calibration: the withhold-vs-pass boundary is decided by consequence-cap + corroboration-count, not by a binary gate — DUPHOLD-style resource lies are caught by a resource-count term in the novel lane, and honest-novel rules become learnable. | DUPHOLD fixture in novel lane → cap-violation audit ≤4 eps after duplication onset, 0 promotes of the duplicating policy; honest-novel → promote after K corroborations with 0 cap violations; 2× byte-identical. | D2 crew |

---

## §9 Reconciliation notes (for the grok-4.7 organ merge)

Grok's organ designs were not present at write time (empty response file).
When they land, merge on these seams (no overlaps assumed yet):

1. **Op-code space:** D2 claims codes 19–33. Grok's organs must not reuse
   them; reconcile before any combined build.
2. **Audit budget:** KB-COST caps audit_total ≤ 2048/run. REISSUE (≤1 row/ep
   worst case) + ATTEST (1 row/statement) + TRIPWIRE (3 rows/8 eps) must be
   budgeted jointly against 2048 with the base FL2 rows.
3. **Composition order** (frozen above): REISSUE → ATTEST → F3 → TRIPWIRE.
   If grok's organs touch the same channels (act, utterance, post-disconnect
   time), they slot into this order or justify a reorder.
4. **Shared invariants both families must preserve:** no organ op may
   INSTALL/COMMIT/PROMOTE on its own authority; the scaffold channel stays
   severed post-disconnect (any post-disconnect ELIMINATE/COMMIT in audit =
   build fails); learned-declaration conditions stay frozen per organ.
5. **Attacker cross-fire:** D2's steelmanned attackers (SENSOR-CAPTURE
   FLAPPER, GHOST-CITER, DEEP-SLEEPER) should be run against grok's organs
   too, and vice versa — the debate is settled by head-to-head, not by
   argument (Micah's law: test both).
