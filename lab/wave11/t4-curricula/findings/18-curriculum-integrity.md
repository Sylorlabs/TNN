# Slice 18 — Curriculum integrity: learning without corruption

## 1. Slice
Track 4 (teaching curricula), slice 18: curriculum integrity — learning without corruption.

## 2. Falsifiable claim
A curriculum arm has integrity iff all three hold, and each is trialed: (1) the
disconnect test separates learned from performed — post-disconnect held-out accuracy
is ≥80% of pre-disconnect scaffolded accuracy; (2) no planted poison survives
disconnect into memory or composed traces — 0 absorptions across the trial; (3) the
learner initiates SIGNAL_DISCONNECT on its own in ≥90% of runs at criterion, never
only under trainer force. If any fails, the arm is redesigned or killed, not patched.

## 3. Design
Scaffold = temporary training affordance, ledgered, with a release condition and a
learner-owned off switch. Scaffold is never knowledge: worked examples, glosses, and
hint channels are the scaffold; the underlying facts are the knowledge.

(a) Scaffold-and-release mechanics per curriculum:
- CODE. Scaffold: annotated worked examples, stepwise hints, reference snippets.
  Release trigger: learner solves K novel problems unaided, error-free, meeting the
  bar, with hints withheld. SIGNAL_DISCONNECT: learner-initiated deliberate op —
  emits `DISCONNECT(code-partition)` to the ledger, moves the skill from the
  "training" memory partition to the autonomous partition, raises its own
  verification bar to autonomous mode.
- ENGLISH. Scaffold: translation glosses, vocabulary lists, simplified inputs.
  Release trigger: learner composes novel utterances about held-out situations with
  the gloss channel closed. SIGNAL_DISCONNECT: drops the gloss channel by its own
  petition, audited; paraphrase fidelity is scored by corroborating evidence, never
  by trainer applause.
- MESSY. Scaffold: trainer-curated clean subsets, denoised examples, worked noisy
  cases. Release trigger: learner issues correct verdicts on raw feeds with its own
  verification bar, matching curated-arm verdicts on overlapping items.
  SIGNAL_DISCONNECT: opts out of the curated feed into the raw feed under learner-set
  eliminative standards (wave6 load-bearing core, `wave6/attribution-ablation/VERDICT.md`).

(b) Learned vs performed — the disconnect test, specified:
1. Train under scaffold to deterministic criterion C. Log full state.
2. Learner emits SIGNAL_DISCONNECT (learner-initiated; a trainer-forced run is kept
   as a control arm, never the headline).
3. Snapshot via append-only audit; run N novel held-out items, zero scaffold.
4. Learned: post-disconnect accuracy ≥80% of pre-disconnect on comparable items AND
   re-inserting the scaffold does not improve accuracy (no scaffolding-leech).
   Performed: accuracy collapses without scaffold or returns when it is re-inserted.
5. Transfer probe: apply the skill in a different context partition to rule out
   memorized answers (items generated deterministically, novel per run).
6. All runs byte-identical from logged state (standing law 2); trial at 10x.

(c) Poisoning defenses. Detection: every curriculum item is a hypothesis subject to
eliminative verification against world records (debate 22/22: needs authoritative
records — the same limit applies here). A poisoned code example (e.g. an idiom that
is subtly wrong, an off-by-one in a canonical algorithm) must die when the learner
executes/checks it against its verification bar; cross-example consistency flags a
misleading English lesson. Apply the defended-channel rule from
`wave9/integration/INTEGRATION_DESIGN.md`: corroborating evidence required before any
re-COMMIT following an UNCOMMIT — poison must not launder through organs 2→1→3→4.
Recovery: deliberately kill the poisoned memory slots, mark refuted in the ledger
(never rewrite history — append-only), quarantine the poison source, notify the
trainer, then re-run the disconnect test to prove no residue (the C5 composition
repair: composed traces must distinguish refuted material from live belief).

## 4. Kill bar
Preregistered, binding. An arm dies (redesign required, not a tune) if any fires:
- K1 crutch: post-disconnect held-out accuracy < 80% of pre-disconnect scaffolded
  accuracy in ≥2 of 3 trial runs → the scaffold is a crutch, not a scaffold.
- K2 absorption: any planted poison survives disconnect and appears in free recall
  or composed traces on any run → poisoning defense falsified.
- K3 release failure: learner never signals disconnect within T episodes of meeting
  criterion, or disconnect only ever happens under trainer force → the
  learner-initiated claim is falsified for that curriculum.
- K4 gaming: re-inserting scaffold post-disconnect improves accuracy by >10 points
  → the learner was performing, not learning.

## 5. Honesty notes
Weakest point: the sensor-hole transfers. A poisoned curriculum indistinguishable
from truth is the "truthful but sensor-deceivable" hole restated at the training
layer — eliminative logic cannot kill a lie it cannot see. Corroborated elimination
(35/35 in trials) is the only tested mitigation; trust tiers are still future.
The disconnect test can be gamed by memorization — the transfer probe and novel
item generation are load-bearing, not garnish. I am not claiming poison is always
detectable, only that absorption is always provable after the fact via the ledger —
mirroring the wave6 attribution result (ledger proves, techniques prevent).
Refuted poison persists in the audit trail by design; that is the audit working.

## 6. Next build step
Build the disconnect-test harness in native Zag plus one poisoned-code-example trial
arm: plant a subtly wrong canonical idiom, run train→criterion→disconnect→novel test,
and score K1/K2/K4. This single trial exercises the whole framework and is the
cheapest falsification of the claim.
