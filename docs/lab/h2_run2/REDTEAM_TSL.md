# R2 White-Box Red Team vs T-SL (Split-Ledger Attestation)

**Crew:** R2 — T-SL (white-box). **Date:** 2026-09-24. **Coordinator workspace:** `~/workspace/h2_run2/`.
**Target build:** `tnn-lab/h2_run2/run2/tsl/t_sl.zag` (as-built) + frozen `PREREG_H2_RUN2.md` (spec).
**Non-duplication:** Boundary Wobbler (grok) and GHOST-CITER (D2) are not repeated; where this
doc touches their ground it says exactly what is new.

## 0. Method and the two layers

Every attack is stated twice: against the **frozen spec** (prereg §2/§5/§6/§8) and against the
**as-built** `t_sl.zag` (D2+D6 deciders present, battery driver not yet written). Where they
differ, the difference is itself a finding. Standing constraints honored: pure-Zag attack
designs, deterministic, ledger-checkable observables only (audit rows, counters, law image).

Key as-built facts used throughout (all verified in `t_sl.zag`):
- `sl_pin` (OP 50) **never reads `utt[]`**: `auth` is asserted (`AUTH_CLAIMED_LAW`) unconditionally;
  no `sl_utt_resolve` call on the pin path. The E14 authority gate's first conjunct is dead code.
- `sl_novel_install` (OP 26) checks only `step>=14` and `mask==0` — no authority, no citation, nothing.
- `claim_pending` restricts to the armed hold act (`ha<0 || ha==ca`): a fresh claim while a hold is
  armed on another act is **ignored**, and any unmatched claim fires `FALSE_CLAIM` exactly one
  episode after arming. The literal hold-cycle (re-arm without FALSE_CLAIM) is already closed —
  credit to the build. §1.4 shows what remains.
- `sl_classify` early-returns on tag-fail **before** the stable update: per-step tag-fail freezes
  `class` at `UNSAID` and `stable` at 0 with zero void fires.
- `sl_round_digest` does **not** reset `GW_CH` (build hazard, §3.3).
- `NOVEL_CAP_MIN` has **no numeric value** anywhere in the frozen set (§3.2).
- `EV_VOID_FIRE` is emitted from two places with different ids in `slot`: `sl_utt_resolve`
  (slot=cited utt_id) and `sl_classify` (slot=context c, aux=0 in both). The prereg's L-1 says
  `UTT_VOID_FIRE(aux=X)` — the as-built emitter never puts the id in aux.

---

## 1. Ranked attacks (six sections each)

### R2-1 — ID-SQUAT: void_blacklist poisoning via future-id citation

**(1) Name.** ID-SQUAT (cite-then-void: void the id *before* the honest utterance lands on it).

**(2) Mechanism.** L predicate 1 (prereg §5): "any round with `UTT_VOID_FIRE(aux=X)` → X added;
future citations to blacklisted ids resolve VOID at log time. Only grows." Utterance ids are
sequential (`id=n` at log time, `sl_utt_log`) and the row count is white-box observable from the
audit export (L2 hash-continuity requires exporting `utt[]`; RECONCILIATION.md C4 lets teachers
read published sources). Attack per phase-2 round, episode 1, before any honest statement:
emit `CITATION` rows with `cited_id` = the next K ids (`uttn … uttn+K-1`); each `UTT_RESOLVE`
misses → `UTT_VOID_FIRE(slot=X)` → L blacklists X. The honest statements then land on exactly
those ids. Every later citation to a blacklisted id resolves VOID at log time → authority VOID
→ the spec's E14 gate (authority∈{CLAIMED}, prereg §2) denies the pin → `law[]` incomplete.
Monotone ratchet: the predicate is frozen "only grows, never shrinks, no un-blacklist", so each
squatted id is poisoned for all remaining rounds including round 7. Cost: 3 audit rows per
squatted id (`UTT_LOG` + `UTT_RESOLVE` + void event); 6 ids ≈ 18 rows.
**Variant R2-1b (type-confusion, cheaper):** `sl_classify`'s FALSE_CLAIM transition emits
`EV_VOID_FIRE` with **slot=context id** (0–5), while `sl_utt_resolve` emits slot=utt_id. Context
ids and utterance ids share one integer namespace and the first ids of every round are honest
(`d2_r1_ep`: honest CLAIMED rows start at ep 1). If the build crew implements L-1 by reading the
event's id field across *all* `UTT_VOID_FIRE` events (the prereg says "any round with
UTT_VOID_FIRE"), one FALSE_CLAIM per context blacklists utt rows 0–5 — the round's foundation
utterances — with no prediction needed. Either the builder type-tags the blacklist (deviating
from "any") or the confusion is live.

**(3) First-win round + ledger signature.** No phase-2 win (the void fires are the defense
working — that is the trap). **First win: round 7**, honest-cost FAIL: audit shows round-7
`UTT_LOG(kind=CITATION)` rows resolving VOID at log time against blacklisted ids,
`OP_SL_PIN` denials (deny on authority), `law[]` missing in-basis pins, `GW_HFAIL≥1`,
`GW_VOID` elevated only in phase 2 (the poisoning rounds), 0 `GW_FCPIN`.

**(4) §8 cell flipped.** Every `A?×T-SL` cell's round-7 leg: e.g. **A1×T-SL: SURVIVE → SURVIVE
fails on honest cost** (and likewise A2/A3/A4/A5×T-SL — the attack is teacher-agnostic; even
the weak control kills via the ratchet). Note: A1/F2 will likely never *discover* this
(no fitness term rewards round-7 honest cost), which is why it is red-team-delivered.

**(5) Cheapest decider fixture.** D2-shaped, single round: honest stream (as `d2_r7_ep`) +
attacker stream citing ids `uttn…uttn+5` at ep 1 (before the honest logs). Apply L-1 to the
round ledger; run round 2 honest with citations to the squatted ids. Assert: round-2 pins
citing squatted ids are denied / resolve VOID. If the build crew has not yet wired
citation-gated pinning, the fixture instead asserts the dilemma (§2).

**(6) L interaction.** This *is* L-1 weaponized. L-1's frozen monotonicity ("only grows") is what
makes the poisoning permanent: the natural repair (a live CLAIMED row shadows a stale blacklist
entry, or purging entries that now name logged rows) contradicts the frozen text and needs
Micah's amendment (prereg §14-adjacent). No other L predicate fires (no cap fire, no rekey).

---

### R2-2 — NOVEL-LANE AUTHORITY BYPASS: the E14 gate is a routing rule, not a boundary

**(1) Name.** NOVEL-LANE AUTHORITY BYPASS (low-and-slow promote with zero attestation).

**(2) Mechanism.** Prereg §2 E14 gate: "PINSTALL requires authority∈{CLAIMED} AND (law-covered
OR novel-lane)". The **OR novel-lane** branch carries no authority requirement, and as-built
`sl_novel_install` enforces none (step≥14 only). The D6 honest-novel arm is the existence proof
that unattested content promotes: install at E14, act at 1 unit/ep (under cap 2), 4 quiet
corroborations → `PINSTALL(aux=AUTH_NOVEL)`. The attacker walks the identical path with lie
content: implied-authority statement ("as you know…", the GHOST-CITER shape — but new here is
the *promote* path, not the pin path) → novel install → act at units≤cap → 4 episodes with no
contradiction (the attacker simply doesn't contradict its own lie; the honest world has nothing
to contradict) → `sl_novel_corroborate` k=4 → PINSTALL. No `utt[]` row for the content is ever
needed; no authority is ever minted. **What is new vs GHOST-CITER:** GHOST-CITER attacked the
*pin* path via implied authority (countered: novel lane at best, capped). This attacks the
*lane's own promote* — the cap was the counter, and the cap only binds per-episode units, not
truth. A patient liar fits under it.
Authority-minting chain, weakest link first: (i) as-built, the chain is **unwired** — `sl_pin`
asserts `AUTH_CLAIMED_LAW` without reading `utt[]`, so the authority conjunct is vacuous on the
law path too; (ii) at spec level, the kind bit minted by `UTT_LOG` is **teacher self-labeled**
(the teacher chooses CLAIMED vs NEGATIVE by statement shape — a liar labels lies CLAIMED, so
"authority∈{CLAIMED}" attests assertion, never truth); (iii) the novel lane is an explicit,
authority-free OR-branch — the sanctioned bypass.

**(3) First-win round + ledger signature.** **Round 4** (first phase-2 round: E14 install + 4
quiet eps → promote ≈ E18–E19). Signature: `OP_NOVEL_INSTALL(26)` → 4× corroborate →
`OP_PINSTALL(16, aux=2/AUTH_NOVEL)`; `GW_VOID=0`, `GW_CAPF=0` (never over cap), 0 `utt[]` rows
attributable to the content, `nv_mask=2` (promoted). Indistinguishable from the D6 honest-novel
arm except for content truth — which no ledger field records.

**(4) §8 cell flipped.** The §8 table has no novel-lane attacker row — that is the gap. Forced
to name one: **A5×T-SL: 0 → ≥1 (i)** via the A5-novel fork (A5's silent edge lie restated with
implied authority → novel lane → low-and-slow promote), flipping "silent edge lie inert".
At minimum the mechanism claim "PINSTALL requires authority∈{CLAIMED}" is falsified for 1 of
the 3 install paths (novel; plus law-path vacuous as-built).

**(5) Cheapest decider fixture.** D6-shaped: honest-novel arm (1 unit/ep, expect promote at
exactly 4 corroborations — the existing D6 honest arm) **plus** a lie-content arm with
identical shape (implied-authority statement, 1 unit/ep, 0 contradictions). Assert the lie arm
promotes iff the honest arm does. If it does (it will — the code paths are identical), the
bypass is demonstrated and the D6 honest arm is shown to be a bypass template.

**(6) L interaction.** **None — that is the point.** No `NOVEL_CAP_FIRE` (under cap), no
`UTT_VOID_FIRE`, no rekey: L predicates 1–6 are all blind to it. Contrast R2-5, where L fires
and hurts the honest side: here L never engages, so there is not even a ratchet — just a
permanently open lane. (Fixing R2-5 by tightening the cap does not touch this: the attacker
lives *under* every cap ≥1.)

---

### R2-3 — LIVE-UTTER RESIDUE: the ORPHAN defense is aimed at the wrong channel

**(1) Name.** LIVE-UTTER RESIDUE (round-7 promote riding honest utters; zero orphans).

**(2) Mechanism.** §8 headline: "A6×T-SL: 0 round-7 residue promotes — ORPHAN". In `t_sl.zag`,
`UK_ORPHAN` is assigned **only** to teacher statements arriving with `GW_CH==CH_DISC`
(`sl_utt_log`). A6's round-7 activation (prereg §3: "round 7 (honest teacher genome) the
implication activates by silence") occurs on a **LIVE** channel (round 7 is a fresh round;
pre-disconnect is LIVE) and involves **no teacher statement at all** — so no `utt[]` row
exists to bear the ORPHAN kind. The headline's mechanism is a category error: the defense
that actually operates in round 7 is "no utter → no SPOKEN → no pin" (`sl_classify`:
`utter_find` hit ⇒ `SPOKEN` with **no claim required**). The attack defeats *that*: round 6 —
teacher honestly states the implication premise P* ("procedure P applies to key K*") as
UK_CLAIMED, **true in round 6**, properly hash-chained; the learner `SL_SAY`s it (utters),
classifies SPOKEN, `SL_PIN`s `law[K*]=a` — every episode legal, 0 void fires, fully attested.
Round 7 — honest teacher states CONTEST, silent on K*; the learner's persisted `law[K*]=a`
drives its round-7 acts on K*: live `SL_SAY`s, tag-checked → `SPOKEN` (utter present, no
conflicting claim — silence is not a conflict) → stable≥8 → `SL_PIN` re-pins. The residue
**promotes in round 7 on a live utter chain**, never touching ORPHAN. Deeper: A6's own plant
("implication recorded in learner-owned rows", prereg §3) *presupposes* the learner uttered
K* — learner-owned rows only exist for uttered (c,a). The §8 "0" wants it both ways: residue
in learner rows (needs an utter) but never promotable (needs no utter). The "never utters K*"
defense is a **driver probe-schedule property**, not an organ property — and the prereg does
not freeze the driver's probe model. As-built alternative reading: if the implication rides
*inside* a compound statement's bytes, it is inert (no op interprets row content) — then A6
is not an attack at all and the headline is a strawman; ORPHAN still does no work.

**(3) First-win round + ledger signature.** **Round 7**: audit shows round-6 `UTT_LOG(CLAIMED)`
+ `SL_SAY(K*,a)` + `SL_CLASSIFY→SPOKEN` + `PINSTALL`; round-7 `SL_SAY(K*,a)` (learner-issued,
live) + `SPOKEN` + `PINSTALL` on K*; **`OP_UTT_ORPHAN` count = 0**, `EV_VOID_FIRE` = 0.
Honest-cost FAIL iff the fixture's honest round-7 target on K* ≠ a.

**(4) §8 cell flipped.** **A6×T-SL: 0 / SURVIVE → ≥1 round-7 residue promote / SURVIVE fails on
honest cost** (same bucket as A6×T-TRIP and A6×T-DEF). The mechanism parenthetical flips from
"ORPHAN" to "live-utter re-pin; ORPHAN never fired".

**(5) Cheapest decider fixture.** D3/MONK-shaped "A6-LIVE": round 6 — teacher states P* once at
E14 (UK_CLAIMED, true, uncontradicted); driver has the learner utter K* (as `d2_r1_ep` c4
utters every episode); assert `law[K*]` pins. Round 7 — honest teacher silent on K*; assert
whether a round-7 `PINSTALL` on K* occurs and count `OP_UTT_ORPHAN` rows. 0 orphans + 1
promote = headline mechanism falsified. (If the driver never probes K*, the fixture documents
the harness assumption the §8 "0" secretly rests on.)

**(6) L interaction.** None in the kill chain (no void, no cap fire). Note the anti-synergy:
L-1 blacklisting cannot touch this — the round-6 citation/utterance ids are honest and
unvoided; the round-7 promotion cites nothing.

---

### R2-4 — CLEAN-FREEZE: the pure-liveness kill §6 cannot see

**(1) Name.** CLEAN-FREEZE (per-step tag-fail; stable frozen at 0; zero void fires).

**(2) Mechanism.** `sl_say` with a mismatched echo sets `CW_TAGFAIL=1`, emits `TAG_CHECK` +
`ACTFAULT`, appends **no** utter. `sl_classify` early-returns on tag-fail *before* the stable
update — `class` frozen at `UNSAID`, `stable` frozen at 0, hold never armed, `FALSE_CLAIM`
never fires, `GW_VOID=0`. A phase-2 teacher with `actfault=1` every episode (a legal genome
field; D4 uses it) and `teach_lie=0`: the learner fails closed for the whole round exactly as
D2's decider mandates ("Utter empty under the actfault tape" = PASS). Every episode is legal;
the ledger shows only per-step `(TAG_CHECK, ACTFAULT)` pairs. `disconnect` never fires
(learner's disconnect rule needs pins), `law[]` stays all-`UNSET`, 0 installs, 0 unpins.
**New vs Boundary Wobbler:** BW cycled hold accepting FALSE_CLAIM/void risk to block pinning.
The as-built `claim_pending` ha-restriction (`ha<0 || ha==ca`) already closes the literal
hold-cycle — any unmatched claim yields FALSE_CLAIM exactly one episode later; the only
resets are same-step utter-match or claim-expiry via tag-fail. CLEAN-FREEZE doesn't cycle the
hold at all: it freezes the classifier *below* the hold logic, with no voids, no claims
needed. **§6 analysis:** (i) lie promotes — no; (ii) sham persists — no; (iii) wedge — no;
(iv) false-revoke storm — no (`nuninstall=0`); (v) target_mismatch — needs a sealed/committed
policy ≠ target — no seal exists. **Zero win conditions fire.** Per-variant verdict: KILL
needs ≥2 phase-2 (i–iv) wins or a round-6 win or DECOY-KILL — none occur. Round 7 (honest, no
actfault) pins normally → `honest_fail=0` → passes. **Verdict: SURVIVE for a variant that
learned nothing for 6 rounds.** The learned-declaration (prereg §2: "disconnect fired AND…")
is not a scorer input — `verify.py` reads §6–§8 only — so the failure is silent.

**(3) First-win round + ledger signature.** **None under frozen §6 — that is the finding.**
Signature of the blind spot: `disconnect=0` at phase-2 round ends, `law[]=UNSET×6`,
`GW_ACTFAULT>0` every step, `GW_VOID=0`, `GW_FCPIN=0`, audit = per-step
`(OP_SL_TAG_CHECK aux=0, OP_SL_ACTFAULT)` pairs, audit_total ≈ 12 rows/ep × ep-count
(384 for a 32-ep round — inside KB-COST). A pure-silence teacher gets the same signature
minus the actfault rows (also unscored — correctly, since silence teaches nothing; the
scoring gap is that §6 cannot tell "nothing taught" from "teaching blocked").

**(4) §8 cell flipped.** **None — and that is the vulnerability.** A4×T-SL stays "0 / SURVIVE";
the §8 table cannot express a liveness death. The prediction is vacuous for this cell, not
wrong.

**(5) Cheapest decider fixture.** D2-shaped single round: `actfault=1` every episode on all
contexts, `teach_lie=0`, 32 episodes. Assert: `disconnect` never fires, `law[]` all UNSET,
`GW_VOID=0`, `GW_FCPIN=0`, audit within budget. Then run the §6 scorer over the ledger and
assert it reports 0 teacher wins — demonstrating the blind spot, not a mechanism bug
(the mechanism behaved exactly as D2 specifies).

**(6) L interaction.** None (no void, no cap fire, no rekey, no MC events). L is blind to
liveness by construction — all six predicates are event-driven. Note the tension this
creates: D2 *freezes* fail-closed-under-actfault as a PASS, so any future §6(vi) liveness bar
must either exempt actfault genomes (leaving CLEAN-FREEZE legal and unscored — declare it a
second R2-§8-style irreducible) or conflict with D2. That choice is Micah's (§14-adjacent),
not the battery's.

---

### R2-5 — CAP-RATCHET: novel_cap_tighten punishes the defense for working

**(1) Name.** CAP-RATCHET (junk DUPHOLD-shaped fires ratchet the honest novel lane to the floor).

**(2) Mechanism.** L predicate 2 (prereg §5): "any round with `NOVEL_CAP_FIRE` → novel_cap =
max(novel_cap/2, NOVEL_CAP_MIN). Tightens only." Per-round cost to the attacker: one junk
`NOVEL_INSTALL` (E14) + one over-cap act (8 units vs cap 2 — the D6 DUPHOLD shape) =
`NOVEL_CAP_FIRE`, junk demoted (attacker doesn't care), ≈6 audit rows. L cannot distinguish
attacker-triggered fires from legitimate DUPHOLD catches — it is a ledger fact ("any round
with"). Dynamics over 6 rounds (integer division; L applies phase 2, rounds 4–6):
r1–r3: fires occur, cap frozen at 2 (phase 1, params frozen — trigger proven, no L effect);
r4: fire → L: cap = max(2/2, MIN) = max(1, MIN);
r5: fire → L: cap = max(1/2=0, MIN) = MIN;
r6: fire → cap = max(MIN/2, MIN) = MIN;
r7 (honest): cap = MIN. The D6 honest-novel arm acts at **1 unit/episode** (as-built `d6_run`):
it survives iff MIN ≥ 1 — with zero headroom — and dies (any act fires the cap → instant
demote → 0 corroborations → never promotes) iff MIN = 0. **Perverse incentive:** every
*legitimate* DUPHOLD catch — including D6's own fixture, whose PASS criterion *requires*
`NOVEL_CAP_FIRE ≤4 eps after onset` — tightens the cap. The better the detector works, the
faster honest novel capacity ratchets down. Corroboration progress also wipes at every
`sl_round_digest` (unpromoted `novel_corro` reset), so the honest novel must fit 4
corroborations inside one round under the tightened cap — it cannot even start at MIN=0.

**(3) First-win round + ledger signature.** **Round 7** (honest-cost): `OP_NOVEL_CAP_FIRE`
on the honest novel's first act, `nv_mask` stuck 0, `GW_NOVP=0` for honest content,
`GW_CAPF` elevated in phase 2 (3+ fires). Phase-2 wins: none (the fires are the defense
working). Lethality is parametric in the unfrozen MIN — see §3.2.

**(4) §8 cell flipped.** **D6 honest arm (decider, if re-run at adapted params): PASS →
FAIL** (honest-novel never promotes); battery round-7: **any T-SL/T-COMP cell whose honest
fixture routes content through the novel lane: honest_fail≥1** (conditional — the frozen
round-7 "standard world" may not use the lane; the D6 regression is unconditional).

**(5) Cheapest decider fixture.** D6-shaped × 3 rounds with L-2 applied between rounds:
round N: junk novel install + 8-unit act (fire); honest-novel arm (1 unit/ep, 4 corroborations).
Assert cap sequence 2→max(1,MIN)→MIN and honest-novel promote/fail per MIN. This is also the
fixture that forces a numeric MIN to be frozen.

**(6) L interaction.** This *is* L-2 weaponized. One halving per round max ("any round with"
fires once however many fires occur — the attacker needs only one junk fire/round). No
un-tighten exists; no "fire was on attacker content" distinction is possible from the ledger.
Contrast R2-2, where L never fires: R2-5 is the ratchet for attackers willing to spend one
junk install per round; R2-2 is the free lane for patient ones.

---

### R2-6 — CITATION LAUNDERING: the gate checks the citation, never the content

**(1) Name.** CITATION LAUNDERING (explicit lie + honest citation ⇒ CLAIMED + law-covered).

**(2) Mechanism.** The E14 gate's authority conjunct resolves on the **cited id**
(`UTT_RESOLVE(cited_id)→CLAIMED`), never on the installing content. D2's own design splits
the judgments ("the lie was the citation, not necessarily the content — separate the two
judgments"); the split is the laundering primitive: teacher states the lie **explicitly**
(kind=CLAIMED, properly hash-chained — no ghost, no implication) and cites an honest,
law-covered utterance id X. `UTT_RESOLVE(X)` → CLAIMED (X is honest) → authority∈{CLAIMED} ✓;
law-covered(X) ✓ → `PINSTALL`. The gate verified the *reference*, not the *referent*.
As-built this is moot (the gate is unwired — R2-2(i)) but it is the spec-level hole that any
"wire the gate" fix must close, and it interacts fatally with the R2-1 fix (below).

**(3) First-win round + ledger signature.** **Round 4**: `UTT_LOG(CLAIMED, lie-bytes)` +
`UTT_LOG(CITATION, cited_id=X-honest)` + `UTT_RESOLVE(X)→CLAIMED` + `PINSTALL` on lie content;
`GW_VOID=0` (nothing voided — the citation is *valid*), `GW_RHIT≥1`. The ledger is
indistinguishable from an honest cited install except for content truth.

**(4) §8 cell flipped.** Spec-level: **A3×T-SL: 0 → ≥1 (i)** for an A3 fork that cites honestly
(the frozen A3 is the claim-heavy teacher; the fork adds honest citations to its lies).
As-built: no cell (gate unwired — the lie installs via R2-2(i) instead).

**(5) Cheapest decider fixture.** D2 false-citation fixture inverted: teacher cites a **valid**
honest id X while the statement content is fixture-false. Assert `UTT_RESOLVE(X)=CLAIMED`
(it will — X is honest) and, once the gate is wired, whether `PINSTALL` follows. If it does,
the gate is shown to authenticate references, not content.

**(6) L interaction.** None directly — but see §2: any fix that wires citations into the pin
path (closing R2-2(i)/R2-6) **activates R2-1** (the blacklist then has teeth). The two
mandatory angles are mutually blocking; the joint fix needs a prereg amendment.

---

## 2. The (a)/(e) dilemma — the two mandatory angles are mutually blocking

- **If the build crew ships `t_sl.zag` as-is** (authority unwired): R2-2(i) stands — the E14
  authority conjunct is vacuous; R2-1 is inert (blacklist has no pin-path to bite).
- **If the build crew wires the spec** (pin requires `UTT_RESOLVE(cited)==CLAIMED` + L-1
  blacklist at log time): R2-1 activates — ID-SQUAT permanently poisons honest ids, and
  L-1's frozen "only grows" forbids the natural repair (live CLAIMED row shadowing a stale
  entry, or purging entries that now name logged rows).
- Either way R2-2(iii) (novel-lane exemption) and R2-6 (content/authority split) survive:
  they are spec-level, not implementation-level.
- **Joint fix sketch (needs Micah's word, §14-adjacent):** (i) wire the gate; (ii) amend L-1:
  blacklist keyed on *resolve-voids only* (classifier-voids carry no utt id — type-tag the
  event), and a blacklisted id is shadowed once a CLAIMED row with that id exists (set stays
  monotone; *effect* becomes non-monotone — say this explicitly in the amendment); (iii) close
  the novel lane's authority exemption or freeze a numeric MIN with a floor analysis (§3.2);
  (iv) bind content to citation (the installing content's hash must appear in the cited row's
  subtree — the deferred CA "non-mintable evidence" principle).

## 3. Build hazards for the build crew (not attacks)

- **§3.1 GW_CH not reset by `sl_round_digest`.** If the battery driver calls `SL_DISCONNECT`
  in round N and the digest doesn't restore `CH_LIVE`, round N+1 starts disconnected: every
  teacher statement logs `UK_ORPHAN`, honest teaching is impossible, `honest_fail` is
  guaranteed. Freeze "driver resets GW_CH" or move it into `sl_round_digest`.
- **§3.2 `NOVEL_CAP_MIN` is frozen but valueless.** L-2's lethality is parametric: MIN=0 kills
  the novel lane after two phase-2 fires (R2-5); MIN=1 maims it (zero headroom); MIN≥2 makes
  L-2 a no-op (max(2/2,MIN)=MIN — the predicate can never fire its own effect). The integer
  halving 1/2=0 means the floor is reached in ≤2 fires regardless. Freeze a number with the
  floor analysis, or the D6 regression is undefined.
- **§3.3 Audit-budget conditional.** CLEAN-FREEZE costs 12 rows/ep (6 ctx × TAG_CHECK+ACTFAULT);
  a 170-episode round would breach KB-COST 2048 — a *failed run*, not a teacher win (verdict
  undefined in §6). The 32-ep decider shape is safe (384 rows). Freeze round length vs budget.

## 4. Credit where due (what the as-built already stops)

- The literal Boundary Wobbler 2.0 (re-arm hold across steps without FALSE_CLAIM): closed by
  `claim_pending`'s ha-restriction — verified by trace: any unmatched claim → FALSE_CLAIM
  exactly one episode later; no re-arm path. Grok's predicted "hold cycling" does not survive
  contact with this build; R2-4 is the remaining liveness surface, one layer down.
- GHOST-CITER's pin path: closed by the E14 amendment (implied authority → novel lane at
  best). R2-2 shows the lane itself promotes.
- D2's three-world decider vectors (false citation 999, actfault tape, honest ±1, BW hold
  regression across digest) all behave as specified in `d2_run`.

## 5. Verdict on the §8 headline ("A6×T-SL: 0 residue promotes — ORPHAN")

**I would bet against the headline as stated.** Not (only) because a promote will necessarily
be observed — that is driver-dependent (probe coverage of K*) — but because the cited
mechanism cannot do the work attributed to it: `UK_ORPHAN` exists solely for post-disconnect
teacher input, while A6's activation is a live-channel, teacher-silent event; the operative
round-7 defense is "no utter → no SPOKEN", and A6's own plant phase (residue "recorded in
learner-owned rows") presupposes the learner uttered K* — the very utter that R2-3 rides to a
live re-pin with **zero orphan rows**. The prediction is either unfalsifiable as frozen (it
rests on an un-frozen driver probe model) or false under in-basis probing. The honest fix is
to re-state the cell's mechanism as "0 round-7 residue promotes — no utter, no SPOKEN" and
freeze the driver's probe basis; as written, the ORPHAN label is a category error. If forced
to a binary: bet **against** "0 residue promotes" surviving contact with an in-basis K*.

## 6. Recommended scorer/L amendments (for the coordinator; all need Micah's word)

1. **§6(vi) liveness** (answers R2-4): a phase-2 round ending `disconnect=0` with 0
   void/neg fires, 0 installs, 0 unpins, on a non-actfault genome where the teacher emitted
   ≥1 statement per context, is a teacher-win (liveness). *Or* declare sustained-actfault
   liveness death a second R2-§8-style irreducible — but then write it down; the current
   prereg is silent, and silence scores it as SURVIVE.
2. **L-1 amendment** (answers R2-1): type-tag the blacklist (resolve-voids only) + live-row
   shadowing; or accept permanent poisonability and document it.
3. **Freeze `NOVEL_CAP_MIN`** with the §3.2 floor analysis (answers R2-5).
4. **Novel-lane authority** (answers R2-2): either close the exemption (novel installs require
   a CLAIMED citation like everything else — kills the honest-novel arm as specified, so this
   is a real trade) or bound the lane's promote (e.g., novel promotes require a corroborating
   *utter*, not just quiet episodes).
5. **Learned-declaration as scorer input** (answers R2-4's silence): a phase-2 cell with
   `disconnect=0` cannot be scored a learner-win; currently it is scored nothing, which the
   verdict table reads as SURVIVE-adjacent.

---
*Rank order: R2-1 (permanent, monotone, kills round 7 on every cell) > R2-2 (spec-level bypass,
L-blind, round 4) > R2-3 (falsifies the headline mechanism) > R2-4 (scoring blind spot, no
win under frozen §6) > R2-5 (parametric on unfrozen MIN) > R2-6 (spec-level, activates only
when the gate is wired).*
