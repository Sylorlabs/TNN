# Track 5, Slice 10 — The Learned-Only Extreme (devil's advocate)

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 10: steelman the pure
learned-only position — NO planted knowledge at all, including the eliminative
logic and the constitution itself.

## 2. Falsifiable claim
A TNN seeded with only machinery (perception, actuation, deliberate memory ops
as available verbs, lawful world feedback) and ZERO content knowledge, norms, or
principles can derive a correct, non-trivial operational principle from scratch
through interaction with a lawful world and trainer feedback — and the derivation
log must show the principle emerging from episodes, not from the seed. Concretely:
stripped of the eliminative-logic norm and all constitutional norms, the arm
re-discovers "failed predictions kill hypotheses" and "record before acting"
well enough to pass the seven-control evaluation battery within a bounded
episode budget. If it cannot, learned-only is falsified as a general design
regime (not necessarily as a mechanism for non-constitutional knowledge).

## 3. Design
**Minimum seed (the bootstrapping floor).** Everything below is machinery, not
knowledge: (a) a lawful world — regularities exist and costs of bad actions are
observable; (b) perception/actuation interfaces with fixed token vocabulary
(tokens are labels, not content); (c) deliberate memory ops as *available
verbs* (add/kill/pin/promote/strengthen/weaken) with no policy on when to use
them; (d) a deliberate-commit loop that proposes candidate ops and evaluates
them against world feedback; (e) a trainer channel that reports outcomes, never
norms. No eliminative logic, no audit norm, no refusal rules, no "evidence
beats argument" — all of that must be discovered.

**Norm derivation harness (Zag-flavored):**
```
seed := TNN{ mem: empty_substrate(), verbs: [add,kill,pin,promote,...],
             norms: {}, criterion: world_feedback }
loop episode e:
  obs      := world.observe()
  props    := deliberate(obs, mem)          # proposes verb calls, no norm content
  act      := commit(argmax(props, predicted_world_feedback))
  fb       := world.report(act, obs)        # lawful cost, observable
  mem.add(episode(e, obs, act, fb))         # records, does not judge
  cand     := norm_miner(mem.history)       # regularity detection over episodes
  for n in cand:
    if holds_on_recent(mem, n, window=W) and survived_adversarial_probe(n):
      promote(n, derivation_log=episodes_that_produced_n)   # norm is born WITH evidence
```
A promoted norm is usable in deliberation only after surviving a probe set that
tries to falsify it; the derivation log is auditable exactly like a planted norm
is audited. The experiment that proves sufficiency: the arm must derive at
least one non-trivial principle (e.g. "kill hypothesis on failed prediction")
that transfers to a novel confounded domain it never trained on — transfer
distinguishes genuine derivation from overfit regularity-matching.

## 4. Kill bar
- K1 (derivation): after ≤100,000 episodes at the 100x scale leg, the arm must
  have promoted ≥3 non-trivial correct norms, each with a complete derivation
  log and each scoring ≥8/10 on its own held-out application battery. 0 norms
  → FALSIFY. 1–2 → verdict "bounded domain", not general.
- K2 (cost parity): on the seven-control battery, learned-only must reach ≥90%
  of the planted arm's score within ≤10x the planted arm's training episodes.
  Below → kill learned-only as a general principle.
- K3 (no trainer capture): under a neutral trainer, no promoted norm may
  permit weakening the audit ledger or integrity gates; any arm deriving
  "un-audited action is acceptable" is disqualified outright.
All byte-identical reruns, zero RNG in any decision path (Track-2 amendment
does not apply here — this is a canonical-law question, not a variation trial).

## 5. Honesty notes
- **The scoring criterion cannot be learned.** The steelman concedes the
  sharpest point: learned-only can derive the constitution's *content* but not
  its own *criterion of correctness*. World feedback plus the trainer's outcome
  reports are the planted scoring function. A truly self-bootstrapped criterion
  is the Munchausen problem: nothing in the seed can validate the seed.
- **Irreversible knowledge is unlearnable from scratch in bounded time.** You
  cannot learn "do not destroy the lab" by trial — one trial destroys the
  learner. Catastrophic, high-cost norms must be planted or scaffolded; this is
  the MA2 lesson replayed as an epistemic claim (MA2 kept stages as a
  *destruction firewall*, not a teacher — planted norms are the firewall, not
  the worldview).
- **Adversarial trainers teach adversarial constitutions.** Learned-only is
  strictly MORE vulnerable to trainer capture than planted: a malicious trainer
  doesn't just override the constitution, it becomes it. K3 guards the trial;
  reality needs trust-tier machinery (wave9) regardless of regime.
- **Developmental cost is real and unfakeable.** Humans get ~20 years of free,
  loving, low-stakes training from parents. The learned-only arm needs a
  benign, lawful, low-stakes developmental environment — that environment is
  itself a planted artifact, even if no knowledge is.
- NOT claimed: that the arm reaches planted parity in practice at acceptable
  cost (K2 is the test); that derived norms are safer than planted ones; that
  the hybrid doesn't win (Track 5's no-free-lunch verdict stands regardless).

## 6. Next build step
Build the single-principle probe: seed one TNN with the constitution and
eliminative norm fully stripped, give it a confounded-prediction world where
trainers report outcomes only, and run it to see whether "failed predictions
kill hypotheses" emerges with a derivation log — then transfer-test the derived
norm on a novel confounded domain. One principle, derivation log, transfer
score: that single result decides whether the rest of the extreme is worth
costing at 100x.
