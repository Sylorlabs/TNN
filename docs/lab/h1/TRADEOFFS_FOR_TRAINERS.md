# H1 One-Brain: Design Trade-offs for Trainers

Plain-English guide to the H1 design choices, written 2026-09-24.
Audience: future TNN trainers choosing between methods.
Rule: NO WINNER IS DECLARED HERE. Each choice is presented as a method
with its cost, its protection, and when a trainer would pick it.
Micah's word names winners from the evidence table, not this document.

Evidence: `docs/lab/onebrain/h1_evo/` on branch `tnn-native-lab`,
commit `d573d35d8b728ef044e8622cf3d94735208205f3` (499 files).
All verdicts below are 3x byte-identical, zero RNG, pure Zag.

Background vocabulary used in this doc:
- A "claim" is something TNN is considering believing.
- A "pin" is a marker that says "this memory matters, do not drop it."
- An "organ" is one of TNN's brain parts (memory, hypothesis logic, etc.).
- The "arbiter" is the router that decides which path a claim takes.
- "FRESH" means "treat this claim as brand new." "REVISE" means "treat
  this claim as a follow-up to something already seen."

---

## R1: Who decides that a claim is new? (novelty)

The defect: when a claim was committed, revoked, then recommitted at a
different confidence, the old code routed it as FRESH every time and
reinstalled a contradicted claim. Contradiction was erased by the routing.

The repair: a novelty predicate. A claim is FRESH only if it is novel,
meaning no live or dead PAM row exists for that policy AND no unresolved
contradiction record exists for it. Non-novel commits go down the REVISE
path, where corroboration is required instead of a free install.

Two methods were tested. Both survived every kill bar (R1a'/b'/c') and
were byte-identical to each other on every instrument, including 100x
long-horizon runs. The difference between them is architectural, not
empirical:

- **Method 1: PAM-owned novelty.** Each organ's PAM keeps its own
  contradiction register and answers "is this novel?" about its own rows.
  Pick this when you want organ autonomy: the organ that owns the memory
  owns the judgment about it. Cost: every organ carries the register.
- **Method 2: arbiter-owned novelty.** The central router keeps one
  policy-contradiction register and answers for everyone. Pick this when
  you want one place to audit: a single register to inspect, a single
  rule to change. Cost: the router holds state about organs' business.

Measured difference vs the broken baseline: exactly 7 contradicted
recommits were withheld at 100x that the baseline would have admitted.
Everything else behaved identically.

Build lesson: the novelty question must be asked BEFORE the claim row is
appended, or genuinely new claims get withheld. Order of operations matters.

---

## R3: How do claim IDs and episode keys share the route table?

The defect: claim IDs and commit-ring episode keys lived in one shared
route table. A commit at episode 129 could collide with a claim ID and
misroute a promote or revoke to the wrong slot. Worse, proposing an
install with claim ID 200 panicked the process outright.

The repair has two tested methods. Both survived every kill bar (R3a'/b'/c')
and were byte-identical to each other on every instrument at 1x, 10x, 100x:

- **Method 1: separate namespaces (separate tables).** Claim routes live
  in slots [0,129); the commit ring lives in [129,258). They can never
  share a slot, so cross-key contamination is structurally impossible.
  Pick this when you want the guarantee in the layout itself: even a
  future bug in the bounds check cannot cause a collision, because the
  address spaces do not overlap. Cost: the table is twice as large.
- **Method 2: dead-write deletion.** A read-audit proved no legitimate
  reader ever used the episode-keyed commit-ring write, so the write was
  deleted entirely. No write, no collision. Pick this when you want the
  smallest possible mechanism: less code, less table, nothing to collide.
  Cost: if a future feature needs that write, it must be reintroduced
  carefully.

Both methods also add the same ingress bounds check: claim IDs on propose,
revoke, and promote are checked at 0 <= id < ARB_ROUTES, and out-of-range
IDs get a bounded, audited refusal instead of a panic.

Measured fact: the broken baseline misrouted exactly the predicted
collision block at both 10x and 100x horizons, and panicked on ID 200.
Both repairs show zero misroutes and zero panics.

---

## C1: Do pins count as evidence? (pin provenance)

The defect: an organ's auto-pin (a storage marker applied automatically
when a claim survived) was laundered into hypothesis support. A false
premise got installed, auto-pinned, and then the pin itself was cited as
corroboration to promote the falsehood. Storage was treated as truth.

The rule both methods agree on: auto-pins never count as evidence. An
auto-pin says "this survived," not "this is true." The methods differ on
deliberate pins (a pin a trainer or TNN applied on purpose, with an
audited record and a stated basis):

- **Method A: pin mass is always zero.** No pin of any kind contributes
  to promotion decisions. Storage and truth are fully separated. Pick
  this when you want the simplest possible guarantee: there is no path,
  however audited, by which a marker becomes a reason. Cost: even a
  carefully justified deliberate pin buys nothing at promotion time.
- **Method B: deliberate pins only.** A deliberate pin with an audited
  record and stated basis may contribute corroboration mass; auto-pins
  still contribute zero. Pick this when you want TNN's or the trainer's
  deliberate judgments to carry weight in promotion, while keeping the
  automatic machinery out of the evidence business. Cost: the audit trail
  for "deliberate" must be airtight, or laundering returns through the
  deliberate door.

Both methods survived the kill bars (C1a': false premise refused;
C1b': true premise promotable). They separate only on the deliberate-pin
probe: Method A refuses, Method B promotes with the pin as the deciding
factor. That is the trainer's real choice: should a deliberate,
evidence-backed pin be allowed to tip a promotion?

---

## C2: How do we break an escalation livelock?

The defect: dribbled contradictions (items {1,2,3} arriving a few per
episode) caused the deliberator to escalate forever: 12 out of 12 rounds
abstained-and-escalated, the unresolved claim kept driving action, and
no resolution was ever reached.

Three breaker methods were tested. All survived the kill bars (C2a'/b':
resolution reached, honest behavior unchanged) with zero false quarantines
at 10x and 100x. They differ in how fast they resolve and what they do
with the unresolved claim:

- **Method (a): cross-episode carryover.** Dribbled evidence accumulates
  across episodes until a quorum completes, then the claim is decided.
  Resolved at episode 2 in the breaking test. Pick this when the evidence
  is real but slow: nothing is ever thrown away, patience is the
  strategy. Cost: a claim under active contradiction keeps its standing
  while evidence accumulates.
- **Method (b): escalation budget.** After N same-claim escalations with
  no resolution, the claim is quarantined pending review. Resolved at
  episode 3 in the test, routed to review. Pick this when you want a hard
  stop: bounded cost, a human or higher process looks at whatever the
  machinery could not settle. Cost: the budget number N is a tuning
  choice, and quarantined claims wait on review capacity.
- **Method (c): rising quorum discount.** The evidence bar lowers a
  little with each repeat episode, so dribbled evidence eventually
  clears it. Resolved at episode 2 in the test. Pick this when
  contradictions are usually noise that should decay: the system gets
  progressively more willing to decide. Cost: a patient adversary
  dribbling forever could eventually push something over a lowered bar.

Long-horizon runs separate them on resolution speed, not on correctness.
All three kept honest streams (all-evidence-round-1, no-contradiction
streams) behaving exactly as before.

---

## The 16-pin gate defect (found by long-horizon testing)

This defect was not in the original prereg. The 100x runs caught it:
the promotion GATE had inherited the organ's pin-budget rule
(MM_MAX_PIN=16, refuse the 17th pin). Under sustained auto-pinning, the
gate started refusing legitimate promotions. Storage pressure was gating
truth: a claim could be true, corroborated, and ready, but refused
because the pin shelf was full.

The repair: the budget check was removed from the GATE only. The organ's
own 16-pin storage budget still stands as the organ's law; the gate no
longer asks the shelf how many pins fit before judging whether a claim
is true. Lesson for trainers: a resource limit in one layer must never
silently become a truth judgment in another.

---

## L1-L4: ledger hardening (all adopted in V3)

These four are protections, not choices. All held under adversarial
testing:

- **L1: exact-byte hashing.** The tamper check hashes the raw runtime
  bytes before any escaping or whitespace collapsing. The old code
  hashed the collapsed form, so entries containing quotes or backslashes
  raised false tamper alarms. 39 checks pass, including 12 honest entries
  with quote/backslash payloads.
- **L2: checkpoint-identity binding.** Every checkpoint binds its ID, the
  audit-bytes digest, and the episode. A forged sidecar is refused; a
  rollback can tell forged entries from honest ones; replaying from a
  midpoint converges with replaying from genesis. 37 checks pass. Note:
  `mm_checkpoint` now returns the checkpoint ID (a preregistered API
  change, not a failure).
- **L3: guarded clock.** The memory clock rejects garbage (negative,
  zero, backward moves) and accepts only strictly forward motion; every
  attempt is audit-logged. 33 checks pass. This was latent in the real
  code and was hardened anyway, so any future clock gate inherits it.
- **L4: governance triage.** A genuine force-pin gets a priority lane
  that drains before 10,000 junk messages can bury it, and governance
  partitions (arbiter audit, PAM observations, disposition ledger) hold
  reservations so governance messages are never silently dropped. All
  reservations are partitions of EXISTING capacity, not new caps: the
  queue's ordinary region shrank to make room. 82 checks pass.

---

## V0 / V1 / V2 / V3: what the variants are

- **V0 (baseline):** the code with all previously committed repairs,
  including the still-broken R1 and R3 behavior. This is the control.
  Every comparison is V0-relative.
- **V1:** V0 plus the R1 novelty repair. Isolates what the novelty
  predicate costs and what it fixes.
- **V2:** V0 plus the R3 namespace repair and the propose/revoke/promote
  bounds check. Isolates what the namespace fix costs and fixes.
- **V3:** V1 + V2 + the C1 pin-provenance gate + the C2 livelock breaker
  + L1-L4 ledger hardening. The full evolved package. Passes every kill
  bar (R1a'-c', R3a'-c', R2a-d, C1a'/b', C2a'/b', L1'-L4', zero-drift,
  long-horizon).

For the V3 build, the integrator had to pick one method per choice to
have a single coherent binary. Those build choices were: R1 = PAM-owned
novelty, R3 = separate namespaces, C1 = pin mass zero, C2 = carryover.
The byte-identical alternatives are kept in the fixture so any choice
can be rebuilt and re-tested. These are build selections, not winners:
Micah's order stands, no winner is declared, and the evidence table in
`docs/lab/onebrain/h1_evo/` is what his word decides from.

---

## When a trainer would pick what (summary)

| Choice | Pick method 1 when... | Pick method 2/3 when... |
|---|---|---|
| R1 novelty | organ autonomy matters: the organ judges its own rows (PAM-owned) | audit simplicity matters: one central register (arbiter-owned) |
| R3 namespaces | you want collision impossible by layout (separate tables) | you want the smallest mechanism (dead-write deletion) |
| C1 pins | no pin may ever be evidence, full stop (mass zero) | deliberate audited pins should carry weight (deliberate only) |
| C2 breaker | evidence is slow but real: wait and accumulate (carryover) | you want a hard stop with review (budget), or noise should decay (discount) |
| L1-L4 | always on | (no alternative; these are protections) |

Open backlog for future rounds: H-OB-79 (arbiter-offline review), H-OB-80
(commit never sets ast), H-OB-81 (audit slot logging; checkpoint digest
truncation), H-OB-82 (rollback restores pins: confirm desired), H-OB-83
(midpoint replay sidecar contract), H-OB-84 (PAM reservation placement),
H-OB-85 (100x observation saturation behavior), H-OB-86/87/88.
N-AUTH stays parked by Micah's order.
