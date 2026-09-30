# PREREG: Substrate Synergy (concept to procedure, contradiction to revision)

Worker: Substrate Synergy Worker.
Date: 2026-09-30.
Status: FROZEN. Committed alone before any implementation.

## Mission

Test whether learned structures on the substrate become inputs to
other mechanisms. Coexistence was demonstrated in EXTENSION-TESTED
(9ebd48258): 4 concepts + 12 bigrams + 4 procedures + causal episodes
on one 32768-byte workspace without interference. This experiment
tests SYNERGY: mechanism B performs better consuming mechanism A's
output than without it.

## Background

Directive: "Do not stop at 'both structures fit in the same
allocation.' ... Ask: Can one learned structure become input to
another mechanism? This is synergy. Coexistence alone is not enough."

## Synergy direction 1: concept to procedure (sample efficiency)

### Design

World W1: 8 morpheme tokens in 4 concepts (initbyte mapping, the S3
mechanism's output form):
- c0: "bik", "bak" (init 'b')
- c1: "gup", "gop" (init 'g')
- c2: "zol", "zul" (init 'z')
- c3: "tav", "tiv" (init 't')

Concept transition distribution (per bigram, conditioned on current
concept c). AMENDED 2026-09-30 (before implementation): the original
c3 row (to c0 p=0.5) would let a noise pair permanently exceed the
count threshold, making exact-set convergence impossible. Replaced
with a 4-cycle so all strong transitions are gold and noise is weak:
- c0: to c1 p=0.85, to c0 p=0.15
- c1: to c2 p=0.8, to c0 p=0.2
- c2: to c3 p=0.85, to c2 p=0.15
- c3: to c0 p=0.85, to c3 p=0.15

AMENDED 2026-09-30 (calibration fix, before implementation commit):
a pilot run showed noise at p=0.15-0.2 crosses the count>=3
threshold within 30 episodes (8 procedures formed instead of 4),
breaking the Phase-A calibration check. Noise reduced to p=0.02:
noise accumulates at ~0.025/episode, staying below 3 for 100
episodes (2.5 < 3), while signal (~1.2/episode) crosses at ~ep 3.
Final probabilities:
- c0: to c1 p=0.98, to c0 p=0.02
- c1: to c2 p=0.98, to c0 p=0.02
- c2: to c3 p=0.98, to c2 p=0.02
- c3: to c0 p=0.98, to c3 p=0.02
Kill bars K1/K2/K3 and directional predictions P1/P2 are unchanged.
Only the apparatus noise floor is corrected.

Within-concept morpheme choice: uniform over the 2 members.

Generation: LCG (a=1103515245, c=12345, m=2^31), fixed seed. Stream
starts at c0. One episode = 5 consecutive bigrams.

Gold ACTIVE sets (ACTIVE rule: count >= 3, same threshold as S5).
AMENDED (follows the 4-cycle amendment above):
- COND-CONCEPT gold: {(c0,c1),(c1,c2),(c2,c3),(c3,c0)}
- COND-RAW gold: the 16 morpheme pairs spanning those concept pairs.

Conditions (separate fresh workspaces, identical deterministic stream):
- COND-CONCEPT: map each morpheme to its concept via initbyte (the
  concept structure as input), count concept bigrams (16 cells),
  ACTIVE = count >= 3.
- COND-RAW: count morpheme bigrams directly (64 cells),
  ACTIVE = count >= 3.

Metric: episodes-to-convergence = smallest N in 1..100 with
ACTIVE(N) exactly equal to gold. Also F1 of ACTIVE(N) vs gold at
N=10, 20, 40. If never exact within 100 episodes, report
"not converged".

### Measurable prediction P1

N_concept < N_raw. Rationale: in COND-RAW each concept transition's
mass splits across 4 morpheme cells, so each cell needs roughly 4x
the episodes to reach count 3. The concept mapping concentrates
counts into 1 cell per transition. (Amended with the 4-cycle; the
rationale is unchanged.)

## Synergy direction 2: contradiction to revision (world change)

### Design

- Phase A: 30 episodes from W1. Build procedures for ACTIVE concept
  pairs (status ACTIVE, support = count, step0/step1 = concept
  names).
- Phase B: 40 episodes from W2, identical to W1 except:
  c0: to c1 p=0.1, to c2 p=0.8, to c0 p=0.1.
  (AMENDED: matches the 4-cycle W1; only the c0 row changes.)
  One continuous LCG stream; the transition table switches at
  episode 31.
- Contradiction detector (researcher-authored, operates on
  substrate procedure facts):
  - Sliding window of 10 episodes; per-pair window counts.
  - For each ACTIVE proc (X to Y) with Phase-A support s over
    N_A=30 episodes: expected = s*10/30.
    Contradiction iff window_count*2 < expected (rate dropped by
    more than half). Recorded as
    (proc_N,"contradictions","<n>") on the substrate.
  - Revision policy: 2 consecutive contradiction windows imply
    status := "ROLLED_BACK"; promote the pair (X to Z), Z != Y,
    with max window count >= 3 to a new ACTIVE procedure.
- Conditions (separate fresh workspaces, identical stream):
  - COND-REVISE: detector + policy active during Phase B.
  - COND-FROZEN: procedures frozen after Phase A.
- Prediction rule: predict(x) = step1 of the ACTIVE proc with
  step0 == x (highest support wins ties); abstain ("") if none.
- Metric: accuracy = correct/total over all Phase-B bigrams
  (abstention counts as incorrect).

### Measurable prediction P2

acc_revise > acc_frozen on Phase-B bigrams. Rationale: after the
change, c0 to c1 predictions fail (truth is mostly c0 to c2).
COND-REVISE rolls back c0 to c1 and promotes c0 to c2, recovering
accuracy. COND-FROZEN keeps predicting c1.

## Kill bars (frozen)

- K1 (directions specified): PASS iff this prereg specifies 2+
  synergy directions with measurable predictions P1, P2.
  Satisfied by this document.
- K2 (synergy demonstrated): PASS iff P1 and P2 both hold in the
  frozen runs (directional only, no magnitude threshold). If
  either fails, report SYNERGY-LIMITED with the specific
  divergence.
- K3 (purity): PASS iff pure Zag at every stage (source, znc
  build, execution), zero Python invocations, zero em-dash bytes
  in committed files, 3/3 byte-identical runs (md5 recorded),
  exit 0, zero stderr.

## Falsification

- If N_concept >= N_raw: concepts do not help procedure learning
  in this design; report both numbers.
- If acc_revise <= acc_frozen: the contradiction to revision loop
  adds no value; report both numbers.
- If a condition never converges within 100 episodes (S1),
  report "not converged" rather than a number.
- If Phase-A ACTIVE set differs from
  {(c0,c1),(c1,c2),(c2,c3),(c3,c0)},
  the world generator is miscalibrated; report
  SYNERGY-LIMITED with the observed set.

## Honest scope

The concept mapping (initbyte), the contradiction threshold
(half-rate over 10-episode windows, 2 consecutive), and the
revision policy are researcher-authored. The synergy claim is
comparative: B performs better consuming A's output than without
it. This is not a claim that the learner invented revision,
concepts, or the contradiction criterion.

The substrate hosts all structures (concept facts, bigram facts,
procedure facts, contradiction records); the mechanisms operate
on substrate facts via sub_fact_learn / sub_fact_query.

## Governance

- Prereg committed alone before implementation.
- Pure Zag only. No Python at any stage.
- No em dashes in documentation.
- Owned path only:
  docs/lab/research-lead/overnight-20260928/substrate_syn/.
- Commits local on tnn-native-lab. Nothing pushed.
