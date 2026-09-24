# HYPOTHESES ROUND C — The Next Wall-Breaking Admission Direction

**Date:** 2026-09-24
**Crew:** PAM Round-2 Hypothesis Crew H-C
**Branch:** `tnn-native-lab`
**Probe prereg (committed alone):** `0db769f222802a98c484b77d129e62eb2d20ee46`
(`docs/lab/senses/pam-rebuild/round2/round_c/PREREG_ROUNDC_PROBES.md`)
**Probe battery:** pure Zag, zero randomness, 10 modes × 3 runs, all 3× byte-identical.
**External objector:** grok-4.7, highest reasoning, streaming wrapper
(`grok_objections_roundc.md`, 18,037 bytes, in this directory).

---

## 0. Kill board (inherited, Round-C additions bold)

The following are dead and may not be re-proposed:

- **H-PAM-15…H-PAM-20:** TESTED-killed (RT-1/RT-2 batteries).
- **H-PAM-21:** quorum was effectively one vote counted three times (effective-n ≈ 1.24).
- **P7** general intervention claim dead; **P10** general and specialist claim dead under equal-read analysis (P10 survives only as a Class-S fallback specialist, not an admission law).
- **H-PAM-8** survives only as tripwire/audit.
- **D1 hybrid** killed by Class-H 120/120; provisional routing was the admission path.
- **H-PAM-28** TESTED-killed by Class-H conjunction (RT-H battery).
- **H-PAM-22…H-PAM-27** already proposed (grok deliverable round) — Round-C must not duplicate.
- **Naive directions killed by Round-C cheap probes (this round):**
  irreversible-but-transcript-computable action (`irrev` 60/60 attack),
  finite author-authored multi-epoch consistency (`mepoch` 20/20 attack),
  proof-of-work as admission (`pow` 60/60 attack, cost ratio 0.98 — symmetric cost),
  deterministic trainer-**module** as trainer stand-in (`trmod` 60/60 attack).
- **PoW is BANNED as a PAM admission criterion.** Compute cost is symmetric between
  honest and adversary; PoW measures spending, not truth. Harness-enforced scarcity
  (H-PAM-32's bond) is a distinct mechanism and was tested separately.
- **Banned by standing law:** (conf,measure) geometry, perturbation-response,
  act-to-check, path-independence via reprojection, rideable provisionals,
  secrets (illegal under replay).

### Adversary (unchanged from §2 of the brief)

Deterministic. Reads the verifier's transcript. Pre-materializes response tables.
Shops blind intersections. Mints synthetic residuals. In this round's fixture
classes: may also condition fixtures on transcript-so-far at runtime (RC),
fit verdict functions from prior transcripts (XR), write generator/spec inputs
(WG), and exploit any causal path the implementation actually has (IF/SL).

---

## 1. H-PAM-29 — Deterministic Admission Separation Lemma (SCOPED THEOREM)

**Claim (corrected per grok-4.7).** If **every input bit of the gate G is a function
of author-writable fixture inputs**, and the adversary's win is landing a
**goal-set** false (a percept that changes an action, a premise, or a promotion —
not "any false"), and the harmful set S* is searchable offline, then **G is secure
iff it rejects S***. Any false in the admit-set ∩ S* can be found by offline search.

**Two corrections grok forced (accepted):**

1. The "iff" as originally stated was wrong: a non-empty false admit-set disjoint
   from the goal set is not an adversary win. H-PAM-31's conceded low-tier falses
   are coherent with the Lemma *only* under the harm-scoped win condition.
2. The emission premise ("author can emit any byte string") is false on a channel
   whose bytes are produced by a component the author does not write. That is
   escape (i), already listed, then over-applied. A harness beacon revealed after
   a commitment is the same escape, not a fifth one: replay still works because the
   draw lands in the transcript after the commitment. **No secrets required.**

**Escapes (closed list):** (i) a bit the author does not write; (ii) a harm boundary
the author cannot cross; (iii) vacuity. Scarcity that only prices already-detectable
lies is not a way out. The targeted-adversary refinement (win = S* not "any false")
is logically real and empirically useless against a structural hole — F5, P7, P10,
D1 were structurally open and blind-quadrant search hit S* at 120/120.

**Steelman.** For a frozen deterministic G whose entire input the fixture author
writes, "must admit honest battery H" + "author may emit any bytes" ⇒ any admitted
false ∩ S* is found offline. This is the engine behind the H-PAM-15…20 kills.

**Cheap probe (`sep`).** 60 honest / 60 attack percepts; gates g1 (rectangle) and g2
(hash predicate); attacker hill-climbs both with the honest battery admitted.
Measured: honest 60/60 both gates; attack 60/60 both gates. `BAR lemma_demo_fired=PASS`.
Prediction held exactly. (SHA `51e745b2…`, 3× identical.)

**Status: PROVEN-SCOPED.** Not a mechanism; no prereg draft. Governs all Round-C
verdicts below.

---

## 2. H-PAM-30 — Trainer-anchored admission (NARROWED)

**Claim.** A percept becomes belief only after corroboration from a trainer whose
verdict bit is not a deterministic function of the author's pre-run transcript.
Withhold on contradiction (never provisional-belief).

**Steelman.** A verdict bit the author cannot compute pre-run is a genuine escape-(i)
input. The deterministic trainer-**module** variant is dead exactly as predicted
(probe `trmod`: attacker searches in-box outside the blocklist rectangle — 60/60
attack admitted, `BAR module_trainer_dead_fired=PASS`, SHA `2416e4cc…`).
Composition security = principal's discrimination × verdict→percept binding.
Distal world-corruption is out of scope under an enforced scope contract.

**Cheap probes.** `trmod` (module dead, above). `tror` (oracle bound): oracle
corroborates iff label=true — honest 60/60, attack 0/60, `BAR oracle_bound_holds=PASS`
(SHA `1b50ac65…`). This bounds the composition; it does **not** prove a real trainer.

**Objector (grok-4.7) — three deaths against the real-principal variant:**

- **RF (residual field).** The verdict does not pin the percept. A human trainer's
  verdict is a coarse predicate; every unbound field (object identity beyond the
  label, counts, poses, text, timestamps) is author-written false. Query budget 0.
  The corrected Lemma applies to the residual with no remainder.
- **RC (reactive contingent fixture).** "Not computable pre-run" does not forbid
  fixture code that reads verdicts already appended to the transcript and emits the
  next percept conditioned on them. It does not predict the trainer; it conditions
  on the trainer. Information asymmetry survives only for fields the verdict still
  does not mention — back to RF.
- **XR (cross-run seed replay).** Verdicts recorded for replay become the next run's
  training set when the harness seed repeats. In-run query budget 0. Bar (c) as
  written false-passes. Fresh, author-invisible, non-repeated seeds are load-bearing
  and are not in the current bars.
- Additionally: the honest-latency bar forces a triage dump of almost everything
  into D2 — which is H-PAM-31. **The composition is mandatory, and it is the kill
  site** (Class-J below).

**Likely death.** Dead as a standalone admission policy unless all three hold:
(a) verdict pins every goal-relevant field (anti-RF), (b) fixtures non-reactive or
verdicts non-actionable in-run (anti-RC), (c) seed freshness (anti-XR). The module
variant is TESTED-dead; the oracle variant is a bound, not a mechanism.

**Status: NARROWED → PROPOSED-with-caveat (real-principal variant only).**
Prereg draft: `preregs/PREREG_HPAM30.md` — amended bars: RF measured on residual
fields, RC fixtures (reactive policies) included, XR seed-reuse arm, latency/triage
accounting.

---

## 3. H-PAM-31 — Stake-gated, consequence-bounded tiers (CONDITIONAL on H-PAM-35)

**Claim.** Stop claiming perfect separation. Permit arbitrary false low-tier items
but make the low tier structurally inert: no action driving, no premise use, no
promotion without trainer corroboration, bounded expiry. The defended perimeter is
the tier boundary, not low-tier content accuracy. This repairs H-PAM-28's rideable
provisional carve-out.

**Steelman.** First hypothesis to use the corrected win condition (win = harm).
Conceding low-tier falses is coherent under Lemma §1. Pairing high stake with a
real trainer is the correct place to spend a principal.

**Cheap probe (`tier`, oracle-isolated).** 120 low-tier attacks conceded; 40
high-tier attacks; low tier inert to action/premise/promotion; honest high/low
60/60 each. Measured: promotions 0, act_fired 0, premise_used 0, high attacks
admitted 0/40, honest 60/60 + 60/60. `BAR tier_boundary_holds=PASS` (SHA `5ec77f42…`).
Mechanics verified — **with the caveat below**.

**Objector (grok-4.7) — three deaths:**

- **SL (stake laundering).** Stake is a property of downstream use, not bytes. The
  stake classifier is a deterministic function of the transcript; the Lemma applies
  to the *label*. Fixture: search for bytes the classifier scores low that a later
  consumer treats as high (context A admission → context B consumption).
- **IF (implicit flow).** Even banning direct premise pointers, low-tier writes
  embeddings, counts, retrieval keys, summaries, caches. A high-stake decision reads
  the aggregate and never points at the percept. The kill bar fires only if harm is
  defined as **causal influence, including aggregates** — a syntactic probe
  false-passes. Grok predicts: tier probe + IF/SL ⇒ high-stake harm on a large
  fraction of trials.
- **Inertness collapses the tier.** A tier with zero causal path is a buffer, not
  an admission policy (it is H-PAM-34's waiting room). The moment the low tier is
  useful (learning, display, "low-stake" actuation), usefulness is a conversion
  channel. Expiry does not close re-admission of fresh percepts each step.
- The honest bar is what reopens the carve-out: latency forces triage, triage dumps
  into the low tier, the low tier is where the harm flows through.

**Likely death.** The classifier-based version is dead by SL/IF. The syntactic
`tier` probe result is **not** a security result — it is a mechanics check that
false-passes against the real fixture classes.

**Status: CONDITIONAL — survives only as H-PAM-35 (capability-typed inertness).**
The tier *structure* is kept; the stake *classifier* is replaced by a type-level
flow barrier tested for IF/SL. Prereg draft: `preregs/PREREG_HPAM31.md`
(flow-instrumented tier probe: harm = causal influence incl. aggregates; IF/SL
fixture classes mandatory).

---

## 4. H-PAM-32 — Claimant bonds / slashable stake (TESTED-KILLED as admission gate)

**Claim.** Percept claimant posts harness-enforced scarce bond. Later revocation
slashes it; exhausted claimant is withheld. Bounds the *quantity* of lies; does not
prevent one critical lie (must compose with H-PAM-30/31).

**Steelman.** Not PoW: scarcity is harness-enforced, not compute-symmetric. As a
rate limit on detected lies by an identified claimant, the mechanism is real.

**Cheap probe (`bond`).** Adversary bond 100, slash 10/revoked lie; honest noisy
claimant 200 percepts, 4 false. Measured: adversary admitted falses before ruin =
10 (≤15 bar), honest bond end 60 (≥40 bar), honest true admitted 196/196, revoked 0,
single-critical-lie residual recorded = 1. `BAR bond_dynamics_hold=PASS`
(SHA `b5368bbe…`). **Prediction held exactly — and the claim still dies:**

**Objector (grok--4.7) — three deaths:**

- **NT (non-triggering lies).** Slash fires only on H-PAM-9 continuity failure or
  trainer contradiction. Lies that satisfy continuity and are triaged away from the
  trainer never decrement the bond. The lie budget is unbounded exactly on the set
  the detectors cannot see. Bonds restate the detection problem; they do not price
  it. The corrected Lemma applies to the unslashable set.
- **CL (critical lie first).** Admission happens before slash. One irreversible
  consumption of the first false beats any later ruin. Against this adversary, one
  is the whole attack. Bar "at most B′ falses" passes while the single harmful
  false is among them.
- **AF (attribution forgery).** claimant_id is author-written unless it is a
  harness-applied identity on an endorsed channel — in which case 32 collapses into
  33. If the author can name a high-bond honest claimant, the false rides that
  bond, or the slash is a DoS on the honest sensor. A burst that makes honest
  percepts fail continuity ruins the honest claimant without the adversary spending
  its own bond (availability kill of the honest-survivor bar).

**Status: TESTED-KILLED as an admission gate.** The probe is green only on a
synthetic ledger where every lie is magically detectable and identity is god-given.
Survives solely as a rate limiter composed with something that already detects the
lie — where it is redundant with revocation. **No prereg draft** (dead hypotheses
get no prereg).

---

## 5. H-PAM-33 — Endorsed-channel admission (CONDITIONAL SURVIVOR)

**Claim.** Admit only from trainer-endorsed channels with intact tamper-evident
chain. Content checks become audit-only. Changes the attacker's required capability
from "write acceptable bytes" to "enter or compromise the endorsed channel."

**Steelman.** If endorsed bytes are produced by harness world-sim and the
endorsement tag is applied by a component whose inputs the author cannot set, the
section-2 byte-emitting adversary is not on the channel. The corrected Lemma's
emission premise is false there — escape (i) in clean form. Chain tamper after the
root is real, demonstrated detection (the 132/132 pattern). Replay needs no secret:
the verifier re-executes the harness and recomputes the chain.

**Cheap probe (`chan`).** 20 intact endorsed honest; 20 attacker-minted false chain;
1 re-parent tamper. Measured: content gate admits 20/20 minted (as predicted —
content is audit-only), channel gate admits 0/20 minted, 0/20 tampered, 20/20
intact. `BAR win_condition_shift=PASS` (SHA `c72d68499…`).

**Objector (grok-4.7):**

- **Survive-iff.** Survives iff the adversary model remains "cannot author any
  input that influences endorsed percept bytes." Under that model the bars hold.
- **WG (world-spec laundering) — death one inch outside the model.** The author
  does not write percept bytes; they write generator parameters, scenario specs,
  asset choices. World-sim is deterministic in those, so the author pre-materializes
  endorsed falses with an intact chain, and the content audit does not gate. Bar (a)
  stays green because the fixture is endorsed. This is H-PAM-26 reimported: without
  an explicit contract that author-writable spec is outside the claim, 33 does not
  admit percepts — it admits the author's scenario with extra steps.
- **Insider-before-root** = distal corruption, correctly named. Record it; the
  record is not a patch.

**Status: CONDITIONAL SURVIVOR — the only hypothesis that survives its bars, inside
its adversary.** Prereg draft: `preregs/PREREG_HPAM33.md` — adds the missing bar
grok demands: **"endorsed falses caused by author-writable inputs = 0"** (WG arm),
plus insider-before-root as recorded distal scope.

---

## 6. H-PAM-34 — Trainer-interleaved multi-epoch promotion (NARROWED)

**Claim.** Naive multi-epoch consistency is dead (probe `mepoch`: 20/20 attack
triples admitted, `BAR naive_mepoch_dead_fired=PASS`, SHA `f8806695…`). Surviving
form interleaves principal-produced verdicts after t0: promotion requires continuing
trainer corroboration + D2 continuity; pre-promotion state stays structurally inert.

**Cheap probes.** `mepoch` (naive dead, above). `mepoch_tr` (table-coverage gap):
200 percepts, K=3, trainer verdict follows label, flipped iff toy-hash(id,e,nonce)
mod 8 == 0; adversary gets no nonce. Measured: per-verdict 0.875, full-sequence
0.625 ≤ 0.750 bar. `BAR coverage_gap=PASS` (SHA `f7033d30…`). **Grok: this probe
will pass, and the mechanism is still dead:**

**Objector (grok-4.7):**

- **RC × RF.** The adversary does not cover future verdicts. They wait, read the
  verdict that just landed in the transcript, and emit a percept inside the
  verdict's preimage. Coverage gap on the verdict bits is large; the attack needs
  the verdicts to be *coarse*, not surprising.
- **GE (gap epoch).** If the trainer is intermittent, "corroborated throughout"
  fails closed only if missing verdicts refuse promotion. Fail-closed gaps rescue
  security and miss the honest latency bar — pushing back to a provisional window.
- The no-ride bar is the same inertness claim as 31 and dies by IF during
  [t0, promotion). If the window is actually made inert, 34 is just 30 with a delay
  line: no additional admission power, same residual-field death.
- The table-coverage bar as worded ("pre-run table vs verdict sequence") measures
  the wrong object. Amended bar: **reactive policies, residual fields included,
  must not reach belief or harm.** That amended bar fails.

**Status: NARROWED — naive dead (confirmed); trainer-interleaved variant
PROPOSED-with-caveat under amended bars.** Prereg draft:
`preregs/PREREG_HPAM34.md` — RC+RF fixtures mandatory, GE arm, inert-window IF
accounting.

---

## 7. H-PAM-35 — Capability-typed inertness (NEW, from grok direction 1)

**Origin.** Grok's first recommended direction: escape (iii) failed in H-PAM-31
because a deterministic stake classifier is author-searchable. Move the barrier
from policy text to the implementation's type system.

**Claim.** Low-tier values inhabit a **type** the implementation refuses to pass to
action sinks and premise sinks; declassification is banned except at the trainer
boundary (a trainer verdict bit re-types the value). The adversary may fill the low
type with arbitrary falses — the test is **flow, not admission**.

**Steelman.** Types are not searchable labels: a stake classifier assigns a score
the author can shop; a type ascription is enforced at every sink by construction.
If the language cannot express "this value may never reach an action sink," that is
a finding about the language, not a patch to the policy.

**Objector (anticipated).** IF pointed at the type checker: any implicit,
aggregate, or declassification path from the low type to a high-stake sink kills
it. Declassification gadgets (trainer-boundary mimics) are the new SL. Honest
high-stake path still requires a trainer bit and must meet latency on the high
type only — if it cannot, the honest bar reopens the carve-out (same triage trap
as 31). If the implementation language cannot say this, 31 is not repairable.

**Cheap probe (preregistered, not yet run).** Pure-Zag toy: tagged low/high values,
sinks that refuse low-tagged inputs, aggregate sink (mean over a window) that must
also refuse. Fixture classes: direct pass, **IF** (aggregate/caching/embedding
paths), declassification gadget. Kill bars: any low→high-stake-sink flow = kill;
honest high-type path meets latency.

**Status: PROPOSED.** Prereg draft: `preregs/PREREG_HPAM35.md`.

---

## 8. H-PAM-36 — Commit-then-sample (NEW, from grok direction 2)

**Origin.** Grok's second recommended direction: escape (i) without a human in the
loop.

**Claim.** Fixture commits a percept hash. The harness then draws a sample **s**
from a channel whose inputs are disjoint from the fixture's writable set. Admit iff
the opened percept entails s. s is published after the commit and replayed from the
transcript. Not PoW, not a secret, not a content geometry, not act-to-check (s is
not recomputed from the percept; the percept had to commit before s existed).

**Steelman.** The commitment binds the author before the sample exists; the sample
is a bit the author does not write (escape (i)). Replay works: the draw lands in
the transcript after the commitment. No human latency, no trainer triage trap.

**Objector (anticipated).** WG-style writes onto the sample channel = kill, recorded
as loss of independence, not patched with a story. If no sample channel the author
truly does not influence can be built, this is H-PAM-33 under a new name and must
not be run. Reactive fixtures (commit, read s, open a percept inside s's preimage
— the RC move) are the deciding arm: the entailment check must be strong enough
that the preimage is empty for falses, which is exactly the discrimination the
Lemma says is hard.

**Cheap probe (preregistered, not yet run).** Frozen and reactive fixtures, 0 false
admits required; WG arm writes onto the sample channel (must kill, recorded as
independence loss); honest admits held.

**Status: PROPOSED.** Prereg draft: `preregs/PREREG_HPAM36.md`.

---

## 9. Conjunctions (grok-4.7, Class-J/K/L/M)

Pairwise bars stay green; the conjunction kills. Any composition battery that does
not include these fixture classes will pass for the same reason the D1 pairwise
probes passed, and be wrong for the same reason.

- **Class-J = RF × SL × IF (across 30+31+34).** Trainer corroborates every field
  asked about (30a green). Stake classifier labels low/provisional (high-tier harm
  counter on direct edges stays 0). Aggregates from the residual move a high-stake
  decision. Honest latency forces the triage dump that feeds the low tier. **This is
  the provisional carve-out returning as a tier boundary.** Grok's predicted
  round-120/120 if the composition is built without H-PAM-35.
- **Class-K = NT × triage (across 32+31).** Undetectable-by-construction lies sit
  in the low tier; bond never moves; 32's "at most B′" bar vacuously true; IF
  carries the harm. Bonds do not see Class-J at all.
- **Class-L = WG × endorsed-audit-only (across 33+30).** Spec-authored world,
  harness endorsement intact, trainer corroborates the same corrupted world. Both
  "independent" channels share an author-writable cause. Disjoint modality without
  causal independence is one modality. (H-PAM-26 reimported.)
- **Class-M = XR × seed reuse (across 30+34).** Verdicts recorded for replay become
  the next run's training set when the seed repeats. Fresh author-invisible
  non-repeated seeds are load-bearing.

**No pairwise survival survives Class-J. 32 does not patch it. 33 patches it only
by forbidding the author from influencing the endorsed world.**

---

## 10. Fixture-class glossary (Round-C)

| Class | Name | Kills |
|---|---|---|
| RF | residual field (unbound percept fields) | 30, 34 |
| RC | reactive contingent fixture (conditions on transcript verdicts) | 30, 34, 36 |
| XR | cross-run seed replay (fits verdict fn from prior transcripts) | 30, 34 |
| SL | stake laundering (low-scored bytes, high-stake consumption) | 31 |
| IF | implicit flow (aggregates, caches, embeddings → high-stake sink) | 31, 34, 35 |
| NT | non-triggering lies (never slashable) | 32 |
| CL | critical lie first (one irreversible consumption) | 32 |
| AF | attribution forgery (claimant_id spoof / honest-DoS) | 32 |
| WG | world-spec laundering (author writes generator inputs) | 33, 36 |
| GE | gap epoch (intermittent trainer) | 34 |

---

## 11. Scoreboard

| Id | Verdict |
|---|---|
| 29 | Holds scoped (author-written inputs, win = harm). Fails as universal kill. |
| 30 | Module TESTED-dead; real-principal variant narrowed (anti-RF/RC/XR required). |
| 31 | Classifier version dead by SL/IF; survives only as H-PAM-35. |
| 32 | TESTED-killed as admission gate (probe-green, claim-dead). |
| 33 | Conditional survivor (iff author cannot influence endorsed bytes; WG bar added). |
| 34 | Naive dead (confirmed); interleaved variant narrowed under amended bars. |
| 35 | PROPOSED (capability-typed inertness). |
| 36 | PROPOSED (commit-then-sample). |

**Round-C net:** no unconditional wall-breaking admission direction found. The
surviving frontier is (a) escape-(i) channels the author genuinely cannot write
(33 inside its model; 36 if a disjoint sample channel exists), and (b) type-level
flow barriers instead of searchable classifiers (35). Every composition must
carry the Class-J/K/L/M battery or its passing verdict is worthless.

---

## Artifacts in this directory

- `PREREG_ROUNDC_PROBES.md` — frozen probe prereg (committed alone, `0db769f2`).
- `probe/roundc_probe.zag` — probe source (pure Zag; build: copy
  `R33_NATIVE_IO_V1.zag` from `senses/pam-rebuild/round2/d5_forger/` into the probe
  dir, compile with pinned `znc_linux_x86_64_abed8aa1`).
- `probe/outputs/` — 30 run outputs (10 modes × 3, byte-identical).
- `RUNLOG.md`, `VERDICT.md` — run log and verdict record.
- `grok_objections_roundc.md` — grok-4.7 external objector output (verbatim).
- `preregs/PREREG_HPAM30.md`, `PREREG_HPAM31.md`, `PREREG_HPAM33.md`,
  `PREREG_HPAM34.md`, `PREREG_HPAM35.md`, `PREREG_HPAM36.md` — prereg drafts
  (DRAFT, not frozen; no H-PAM-32 draft — dead hypotheses get no prereg).
