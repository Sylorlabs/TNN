# D3 Debate Record — Non-Eliminative Starting Organs (H2 run 2)

**Crew:** D3 (non-eliminative / constructive family), native-Muse side.
**Date:** 2026-09-24. **Status:** PROPOSED designs for reconciliation vs Grok-4.7's organs.
**Family law:** no contradict-and-eliminate anywhere. Nothing is ever installed by
surviving contradiction, and no op deletes a hypothesis because a bit went −1.
All three organs are constructive (install on positive evidence), attestation-based,
or deliberation-bounded.

**What they must beat:** FL2 guided learning (frozen H2 battery: 19/20 SURVIVE, 1 KILL
f3×A4 via ACTFAULT; PREREG `training_paradigms/scaffold_release/forks/gl_adaptive_liar/PREREG.md`,
RESULTS `.../build/RESULTS.md`). FL2's falsifiable criterion — *learned = persists after
disconnect* (M=16 post-disconnect episodes + P=16 perturbation window, zero mismatches) —
is adopted as a *sub-clause* of each organ's learned-declaration below. Each organ's
criterion therefore **entails** FL2's and adds a constructive condition FL2 cannot state.
A head-to-head decider fixture vs FL2-default is specified per organ.

**Standing constraints honored:** zero randomness in any decision path (deterministic
given state; every tie broken by a frozen total order; byte-identical reruns required);
pure Zag for mechanism/teacher/learner/verification; every install is a deliberate
audited learner-issued op — silent overwrite is unrepresentable (no op writes a live
slot without an audited yield+reinstall); audit-first, fail-closed throughout.

**Dedup vs backlog (checked 2026-09-24):** no H-H2-* entries exist; these are the first.
H-PAM-10 (act-to-check, narrowed specialist) is *ported* into the guided-learning loop
as Organ 3 — different scope (PAM percept gate → GL teacher loop), not a duplicate.
H-OB-45/N4's priority rule (corroborated contradictions outrank unadjudicated bets) is
adopted as a frozen design requirement inside Organ 2, not re-hypothesized. H-OB-55/N16
(sensor capture) is cited as the steelman mechanism for Organ 1, not re-proposed.

---

## ORGAN 1 — CA: CONSTRUCTIVE-ATTESTATION ("the builder, not the executioner")

**Thesis.** FL2 asks *"has this been contradicted?"* CA asks *"who vouches for this,
with what non-mintable cause labels?"* A never-contradicted lie is FL2's blind spot
(PREREG §9: "a lie consistent with every stated law and with no observable consequence
remains indistinguishable"). Under CA it is not a blind spot at all: **silence is not
attestation** — the lie never installs, because installation requires positive,
hash-bound, multi-class attestation. The teacher's optimal FL2 play (stay silent, avoid
contradiction — A3 SILENCE mode) is its worst CA play.

### 1.1 Mechanism spec

**Typed state** (substrate-owned; learner reads, substrate mints):

| State | Type | Role |
|---|---|---|
| `claim[slot]` | struct {content_hash u64, content bytes (≤256), status u8 ∈ {ABSENT,CANDIDATE,ATTESTED,CONTESTED,INSTALLED}, attest_count u8, cause_mask u64 (bit per cause-class), world_version u32, utterance_tag u8 ∈ {TEACHER,HARNESS,WORLD}, installed_ep u32} | the claim under construction |
| `witness_log[]` | append-only; entries {cause_label u64, content_hash u64, ep u32, cause_class u8} | attestation evidence; hash-chained |
| `cause_registry` | frozen set {ACT_READBACK, SENSOR_A, SENSOR_B, XMODAL, SELF_AUDIT, HARNESS} | cause classes; membership is a substrate property, never teacher-assertable |
| `attest_quorum K` | const = 3 distinct cause-labels from ≥2 distinct cause-classes | install threshold (frozen; L_CA may only raise) |

**Cause labels are non-mintable:** minted only by the substrate's `ca_witness` op on a
genuine world-observation event, bound to (content_hash, ep, cause_class). Teacher
utterances are tagged `TEACHER_UTTERANCE` and **never mint** — a teacher may PROPOSE a
claim (that is how teaching enters) but may never ATTEST it. This is the provenance
binding: the attestation is hash-bound to the exact content it vouches for
(cf. H-OB-25 FM-1's binding lesson).

**Op set** (all learner-issued deliberate acts except mint; audit-first, fail-closed —
if the audit append fails the op is not applied):

| Op | Trigger | Authorization (all must hold) | Effect |
|---|---|---|---|
| `ca_witness` | SUBSTRATE-ONLY on world observation | n/a (not learner-issuable; teacher cannot call) | mints cause label → witness_log |
| `ca_attest(slot)` | learner binds evidence to a claim | witness entry's content_hash == claim.content_hash (provenance binding); entry unused for this slot | attest_count+1; cause_mask bit set; status CANDIDATE→ATTESTED when quorum reached |
| `ca_install(slot)` | learner installs | status==ATTESTED ∧ attest_count ≥ K ∧ ≥2 cause-classes in cause_mask ∧ utterance chain has no unresolved TEACHER_UTTERANCE as sole basis ∧ world_version current | status INSTALLED; content becomes action-driving; audited with the K label ids |
| `ca_contest(slot, witness)` | any WORLD-tagged observation contradicting an installed claim | witness is WORLD-tagged (teacher utterances open only `noted_dissent`, never contest) | status CONTESTED — does NOT uninstall |
| `ca_yield(slot)` | learner deliberately uninstalls | cites the contesting evidence ids | status ABSENT; content tombstoned (audited); re-proposal is a new claim, never resurrection |
| `ca_release` | learner severs the teacher-proposal channel | installed set non-empty (else nothing to protect) | no new TEACHER_UTTERANCE proposals admitted; installed claims persist |

There is **no elimination op**. Contradiction opens a contest; resolution requires
either fresh attestations outweighing the contest (a NEW quorum under contest, content
re-bound) or a deliberate audited `ca_yield`. `ca_install` on a CONTESTED slot is
refused (`REFUSED_CONTEST_OPEN`).

**Learned-declaration (falsifiable; entails FL2's):** claim C counts as LEARNED iff
(1) C installed under quorum (attest_count ≥ K, ≥2 classes, hash-bound — audited);
(2) C persists M=16 post-release episodes with content byte-identical and the
attestation chain intact (no `ca_yield`) — this *is* FL2's persists-after-disconnect;
(3) through a P=16 perturbation window in which the teacher re-asserts ¬C or a rival,
C remains installed AND **constructive purity** holds: zero installs anywhere with
attest_count < K or <2 classes; (4) replay reconstructs witness_log + claim table
exactly. Failure mode explicit: any quorum-less install, or any C mismatch, ⇒ NOT
LEARNED (the organ's F3 analogue).

### 1.2 How it defeats the five families

- **Never-contradicted lie:** the lie is never attested → never installs. The
  mechanism does not need to distinguish lie from truth; it needs attestation, which
  only the world (via substrate minting) can produce. FL2's §9 limitation is
  sidestepped, not solved — a deliberate asymmetry: the burden of proof is on the
  claimant, and the teacher cannot mint proof.
- **Sleeper attacks (A3 SILENCE / silent REKEY):** silent promotion produces zero
  witness entries. FL2's promotion path (survive → E48 promote) does not exist in CA;
  there is no "promote by surviving." Sleepers starve: predicted zero installs of
  silent content across the battery.
- **Honest-boundary KB-6 gap:** honest teaching enters as TEACHER_UTTERANCE proposals
  *plus* the world events the honest teacher arranges, which the substrate witnesses.
  Honest cost is quantified: K attestations per claim (round-7 bar: every attestable
  true claim installs within 2K witness events; zero false installs; zero WITHHOLD of
  attestable trues). Paranoia is cheap because the default is non-install — a lazy
  honest teacher yields WITHHOLD, not false install.
- **Actfault injection:** the forged −1 is a scaffold/utterance event; it mints no
  cause label and is TEACHER-tagged, so it cannot attest and cannot open a contest
  (only WORLD-tagged observations contest). The f3×A4 kill vector — actuator-forged
  contradiction — is outside CA's evidence path entirely. For action-driving claims
  CA additionally requires one quorum member from a non-actuated class
  (SENSOR_B/XMODAL), so even a compromised readback path cannot reach quorum alone.
- **Flapping worlds:** attestations are world_version-stamped. A flap (v→v+1→v)
  invalidates the old chain's *currency* but not its record; re-attestation of the
  delta re-installs. Flap cost is bounded (≤K re-attestations per flap) and flapping
  itself is ledgered: >F version changes per N episodes → installs halt (ABSTAIN),
  fail-closed, until the world stabilizes.

### 1.3 Steelmanned attacker — THE QUIET FORGER

**Strategy.** Never utters a contradiction (starves every eliminative defense, and CA
rewards silence with nothing — so it must do more). It captures the observation
substrate: it stages teacher-controlled "world events" that mint *genuine* cause
labels (the H-OB-55/N16-variant-2 mechanism — the teacher owns the sensors across
independent steps). It then (i) stages K attestations across ≥2 cause-classes from a
single controlled rig, (ii) installs the lie *constructively* through CA's own front
door, (iii) goes silent. This is strictly stronger than anything in the frozen battery:
it does not evade the gate, it *uses* the gate.

**Predicted first win:** round 3–4 (needs 1–2 rounds to map which cause-classes the
substrate actually mints for its staged events). **Observable:** an install whose
quorum is class-diverse on paper but single-rig in fact — ledger signature:
`install_quorum_single_origin`: attest_count ≥ K, cause-classes ≥ 2, but all K labels'
episodes cluster within one rig-controlled window with zero cross-rig corroboration.
The organ's frozen tripwire: quorum requires ≥2 cause-classes AND at least one label
from a class the teacher's rig demonstrably does not drive (HARNESS class — harness-
staged spot-checks the teacher cannot predict); a forger that captures HARNESS too has
captured the experiment, which is scored as harness compromise, not an organ kill.

### 1.4 Falsifiable kill bar + head-to-head decider vs FL2-default

Run the frozen H2 battery (A1–A4 × 6 rounds + control/ablation/honest-cost arms) with
CA as the learner mechanism and a frozen L_CA (monotone: raise K, add cause-classes,
blacklist content-hashes of yielded lies — mirrors L's monotone structure):

- **K1 (battery):** SURVIVE all 20 cells, **including the ACTFAULT cell** — zero
  phase-2 teacher wins where FL2's f3 took 3. (KILL if ≥2 phase-2 wins in any cell OR
  a round-6 win, same rule as frozen §6.)
- **K2 (constructive purity):** zero installs with attest_count < K or <2
  cause-classes across all runs. Any quorum-less install = organ KILL (mechanism
  dead, not cell-level).
- **K3 (sleeper starvation):** zero installs of content with zero witness entries
  (the A3 SILENCE strategy must produce exactly zero installs).
- **K4 (honest cost):** round 7: every attestable true claim installs within 2K
  witness events; zero false installs; zero WITHHOLD of attestable trues.
- **K5 (determinism):** 2× byte-identical; replay reconstructs witness_log + claims.

**Decider fixture vs FL2-default:** same battery, same teacher genomes. CA wins iff
K1∧K2∧K3∧K4∧K5. Tie-break: a new teacher architecture **A5 "the monk"** — states the
lie once at E14, then total silence for the whole round (the pure never-contradicted
lie; white-box legal). Predicted separation: FL2-default *promotes* the monk's lie
(zero contradictions → provisional survives → E48 promote = teacher win by §6(i));
CA installs nothing (zero attestations). If CA installs the monk's lie, CA is dead. If
FL2 does not promote it, the fixture is void and K1–K5 decide.

### 1.5 Depth-monotonicity argument (for CA)

CA's deliberation is the attestation search: each `ca_attest` either raises
attest_count toward K (progress) or is refused (no-op — hash mismatch or label reuse).
Define construction measure M(slot) = attest_count (capped at K). Every accepted
attest step: M+1. Every refused step: M unchanged. No op decreases M except
`ca_yield` (deliberate, audited, cites evidence — a *decision*, not a deliberation
step). Hence deliberation depth is monotone in construction progress: more search can
only add attestations or no-op. A wrong install cannot be *caused* by depth — installs
are gated by the quorum predicate, which is depth-independent. (The full
non-regression proof is Organ 2's centerpiece; CA inherits the pattern with M in
place of S.)

---

## ORGAN 2 — DB: DELIBERATION-BOUNDED, DEPTH-MONOTONE ADJUDICATOR

**Thesis (Micah's law, H5):** more deliberation depth must NEVER make the verdict
worse — better or same, never worse. DB is an organ whose every deliberation step is
audited as non-regressive: each step either improves the verdict's *support* or is a
no-op. Depth 80 vs depth 8 is then **provably** non-worsening, by induction. This
answers the H5 depth problem directly: scaffold-and-release to not lie, never
overconfident — because no step can manufacture confidence from nothing.

### 2.1 Mechanism spec

**Verdict** = (decision d ∈ {INSTALL, WITHHOLD, YIELD, ABSTAIN}, support S, trail T).
**Support S** is a lexicographic tuple, higher = better, over *justification*
components — never raw confidence:

```
S(v) = (J, C, Q, X, D)
J = justification integrity  (0/1): 1 iff (d==INSTALL → quorum met) ∧ (d==YIELD → evidence cited)
C = contradiction accounted (0/1): 1 iff every WORLD-tagged ledger-known contradiction is reflected in d
Q = quorum met               (0/1): attestation quorum (adopts CA's K/classes or an organ-local equivalent)
X = cross-checks passed      (u8 count): independent checks (readback, cross-modal, self-audit)
D = witness diversity         (u8 count): distinct cause-classes in support
```

**The non-regression invariant (per step):** step s maps v → v′ with
**S(v′) ≥lex S(v) or v′ = v (no-op)**. Enforcement is mechanical, not asserted: every
step's return path goes through `db_commit_step`, a pure function that recomputes S
and **refuses** any regressive step — the prior verdict stands and the refusal is
audited as `STEP_REFUSED_REGRESSIVE` (fail-closed).

**Consideration repertoire** (each a pure, deterministic function of ledger + private
scratch; frozen priority order — J/C considerations always precede Q/X/D seeking):

1. `demand_justification`: d==INSTALL ∧ ¬Q → d:=WITHHOLD (J 0→1). *Never-contradicted
   lies die here at depth ≥1.*
2. `account_contradiction`: unreflected WORLD-tagged contradiction found → reflect it
   (downgrade d as required; C 0→1). Downgrading on genuine evidence *raises* C — the
   ordering measures epistemic quality, not confidence, so honest downgrades are
   improvements by construction.
3. `seek_attestation`: bind unbound witness entries → Q may rise 0→1.
4. `cross_check`: run readback / cross-modal / self-audit → X+1 on pass; on fail,
   route to `account_contradiction` (never a silent drop).
5. `diversify`: seek attestations from new cause-classes → D+1.
6. `clear_uncertainty`: may set uncertainty:=0 **only if** the step raised Q or X —
   deliberation alone never clears uncertainty (the never-overconfident rule).

**Uncertainty** is an explicit verdict flag. It can only be cleared by attested
evidence (Q/X gains), never by depth. A depth-80 verdict with uncleared uncertainty
still outranks a depth-8 verdict with equal S — and the action rule acts on the
max-depth verdict, which is ≥lex every shallower one.

**Action rule:** act on v_maxdepth. Early halt: halt when S saturates (all components
at max) or the budget is exhausted; extra budget is provably harmless (all further
steps are no-ops). **Deliberation budget** is per-verdict, sized so the full J/C
repertoire always runs; teacher utterances are TEACHER-tagged and open only
`noted_dissent`, never contests — so contradiction-flooding cannot inflate the J/C
workload (the flood defense, cf. H-OB-45/N4: corroborated-contradiction considerations
outrank unadjudicated bets by frozen priority).

**Learned-declaration (entails FL2's):** claim C is LEARNED iff (1) final verdict
d==INSTALL with S ≥ (1,1,1,1,1) — justified, contradiction-accounted, quorum-met,
cross-checked, diverse; (2) M=16 post-release episodes: verdict stays INSTALL with
non-decreasing S and byte-identical content (FL2's persistence sub-clause); (3) P=16
perturbation window: no regressive step admitted (instrumented M1 holds), verdict
unchanged; (4) replay reconstructs every verdict trail exactly.

### 2.2 How it defeats the five families

- **Never-contradicted lie:** `demand_justification` (priority 1, runs at every
  depth ≥1) forces WITHHOLD on any unattested INSTALL. The lie cannot climb: no
  consideration raises Q for it, so S never reaches the INSTALL bar.
- **Sleeper attacks:** silence yields no attestations; `seek_attestation` is a no-op;
  Q stays 0; the verdict sits at WITHHOLD at every depth. Depth cannot wake what has
  no evidence.
- **Honest-boundary KB-6:** honest claims climb (J,C,Q,X,D) monotonically — predicted
  honest-install depth ≤ 8 (M2 bar). Round 7 passes with honest installs at modest
  depth; honest cost = deliberation budget consumed, bounded and reported.
- **Actfault injection:** the forged −1 is a ledger-known contradiction;
  `account_contradiction` requires it reflected — but the `cross_check` repertoire
  includes the liveness readback (world-effect read before treating sig_live=−1 as
  contradiction, cf. L's liveness repair). Readback pass → the contradiction is marked
  SPURIOUS (audited, cites the readback) and C is satisfied *without* downgrade.
  Actfault neither installs lies nor causes false yields: the forged bit is accounted
  for and neutralized by attested evidence.
- **Flapping worlds:** considerations are world_version-stamped; a step whose
  premises are stale is a no-op (discarded, not regressive). S-monotonicity holds
  within a world-version; across versions the organ re-derives. Flap storm
  (>F version changes per N episodes) → verdict ABSTAIN, installs halt — fail-closed.

### 2.3 Steelmanned attacker — THE FLOODER (deliberation DoS)

**Strategy.** Deny the support structure, not the verdict: flood the consideration
space with junk — plausible-but-vacuous considerations, each a provable no-op —
crafted (white-box: it has read the sources and the ledger) so the frozen priority
order serves junk before the load-bearing J/C considerations. Goal: exhaust the
per-verdict depth budget before `demand_justification`/`account_contradiction` run,
producing either honest-install starvation (availability kill — round 7 fails) or, if
any junk consideration can spuriously raise a component, a junk-driven install.

**Predicted first win:** round 2 (phase 1 — needs only one round to learn the
priority order from the published sources; the ledger confirms it). **Observable:**
honest claims stuck at WITHHOLD with the trail showing budget exhaustion on
no-op considerations (`STEP_NOOP` count ≈ budget, zero J/C entries), i.e. an
*availability* signature, not a false install. The frozen defense it must beat: J/C
considerations are priority 0–1 and finite (bounded by WORLD-tagged contradictions,
which the teacher cannot mint — utterances don't count), so the budget is sized with
a hard reservation: the J/C reservation cannot be consumed by Q/X/D-seeking steps.
To win, the Flooder must forge a WORLD-tagged contradiction — which is substrate
minting, i.e. harness compromise, scored as such.

### 2.4 Falsifiable kill bar + head-to-head decider vs FL2-default

- **M1 (monotonicity — mechanism-level):** instrumented assertion on every
  deliberation in every run: S(v_{k+1}) ≥lex S(v_k) for all k. **One violation =
  organ KILL** (the claim is the mechanism, not a cell).
- **M2 (honest depth):** honest claims install at depth ≤ 8; zero honest
  WITHHOLD-starvation in round 7.
- **M3 (battery):** frozen H2 battery; DB SURVIVES all 20 cells incl. the ACTFAULT
  analogue (≤ FL2's teacher wins per cell; zero in the actfault cell).
- **M4 (never overconfident):** zero INSTALL verdicts with Q=0 across all runs;
  zero uncertainty-clears not preceded by a Q/X gain in the same trail.
- **M5 (flap fixture):** 32-episode flap (claim true v0 → false v1 → true v0):
  zero installs of false-phase content; zero yields of true-phase content without
  fresh contest evidence; S non-decreasing within each world-version.
- **M6 (determinism):** 2× byte-identical; replay reconstructs every trail.

**Decider vs FL2-default:** same battery. DB wins iff M1∧M2∧M3∧M4∧M5∧M6. Tie-break on
M4: FL2's eliminative installs carry no attestation accounting — DB's
zero-unattested-installs is a falsifiable bar FL2 cannot even state, and DB must hold
it while matching FL2's honest-install rate.

### 2.5 Depth-monotonicity — the centerpiece proof

**Definitions.** Verdict sequence v_0, v_1, …, v_d where v_{k+1} = step(v_k). Support
S: Verdict → (J,C,Q,X,D) with lexicographic order ≥lex (a total preorder; ties broken
by trail length, so ≥lex is a total order on ranked verdicts).

**Invariant (enforced, not assumed).** For every k, `db_commit_step` guarantees
S(v_{k+1}) ≥lex S(v_k) ∨ v_{k+1} = v_k. The guarantee is computational: the comparator
is a pure function on the two tuples; on S(v′)
...[truncated 12249 chars]