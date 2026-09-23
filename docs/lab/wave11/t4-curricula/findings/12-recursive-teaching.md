# Slice 12: Recursive teaching — TNN as curriculum designer

## 1. Slice

Teaching TNN to teach: (a) self-directed learning — TNN deliberately identifies its own
knowledge gaps and designs its next learning episodes; (b) peer teaching — one TNN
instance deliberately constructs training episodes for a second TNN instance, evaluated
by the student's independent battery scores.

## 2. Falsifiable claim

A taught TNN can deliberately construct a curriculum (ordered episodes with prereqs,
diagnostics, and release criteria) that produces a strictly better student than a
matched baseline curriculum designed by the fixed external scaffold — measured by the
student's score on an independent, teacher-blind seven-control evaluation battery — and
gap-detection driven by deliberate contradiction/falsification machinery (not loss
gradients) identifies genuinely weak topic regions, evidenced by diagnostic probes
confirming the gap before the student studies them. The claim dies if (kill bar below)
the teacher's advantage vanishes once the scaffolded baseline is matched on episode
count and ordering information, or if self-directed "gaps" fail independent probe
confirmation at rates no better than chance.

## 3. Design

Two organs, both native Zag, both fully deliberate (zero RNG; all selection is by
deterministic rules over logged state):

**GAP organ (self-directed):** TNN keeps a topic ledger T: topics -> {claims, verdicts,
probes-failed}. Gap-detection = deliberate *challenge self-probing*: for each topic, the
system constructs adversarial probes from its own claims (contradiction attempts using
the eliminative hypothesis machinery — "given claim C, generate the strongest
refutation R from existing records"). A gap is declared when: (1) the self-probe
refutes or weakens a held claim (falsification, not loss), or (2) a held claim has no
supporting evidence chain (provenance gap — the architecture already proves it cannot
see evidence genuineness, wave5/6, so provenance gaps are first-class citizens), or
(3) the claim set on a topic is internally contradictory (suspensive-contradiction
hold per wave9 H1). Gap list is ordered by a deliberate priority rule (e.g.,
CORE-adjacent first, then by probe-failure count) — fixed rule, no sampling. Mastery
bar: a gap closes only when newly constructed evidence + eliminative verification passes
post-learning; learner-initiated SIGNAL_DISCONNECT then releases the scaffold. "Good
student" metric: gap-detection precision — fraction of self-declared gaps confirmed by
an independent probe battery (teacher-blind) — plus learning efficiency (episodes per
closed gap vs baseline).

**TEACH organ (peer teaching):** teacher TNN has topic mastery M (verified by battery).
Teacher constructs episode list E for student S: each episode = {prereq claims, new
claims to install, evidence records to present, eliminative checkpoints}. Teacher's
deliberative constraint: every taught claim must survive the teacher's own eliminative
verification over the same evidence it presents — teacher may not teach claims it
cannot verify itself (this is the Track 5 firewall: the same deliberative standard
that held 100% over 2595 temptations in wave5 is the load-bearing anti-planting
mechanism). Student S trains on E, then takes the independent seven-control battery
that the teacher never saw. Teacher score = S's battery delta vs scaffold-baseline
student matched on episode count. Self-vs-peer comparison: the same TNN first runs
GAP-driven self-direction, then designs E for a fresh student instance; the two
student outcomes must both beat baseline, or only one is claimed.

## 4. Kill bar

KILL if any of: (a) teacher-trained student battery delta ≤ scaffold-baseline delta
±2 points on the seven-control battery across two matched runs (byte-identical replay
required); (b) GAP self-declared gaps confirm at ≤60% on the independent probe
battery (baseline: random topic selection confirms at the probe's base rate, to be
measured in the same run — no-free-lunch comparison is mandatory, not optional);
(c) any taught claim in E is later proven false against authoritative records and
the teacher's deliberative check failed to catch it — this is a Track 5 integrity
kill, not just a curriculum failure; (d) teacher's E contains episodes the teacher
itself could not pass (verified by running teacher through E checkpoints).

## 5. Honesty notes

Weakest points: (1) the debate experiment needed authoritative world records to revise
false belief (22/22); teacher E inherits that limit — without ground-truth records,
"peer teaching" is unverifiable belief transfer, and Track 5 planting risk is real:
a teacher TNN could deliberately install false claims in S, and the ledger proves
nothing was tampered with but cannot spot fabrication (wave5/6 honest limit). The
teacher-must-verify rule mitigates but does not eliminate this — a lying self-change
slipped past the gate in RC1 and was only caught post-change; the same race exists
here. (2) Self-directed gap detection can degenerate into confirmation theater:
self-probes are only as adversarial as the prober; a system that designs its own
tests tends to pass them. The independent probe battery is load-bearing, not
decoration. (3) I'm NOT claiming TNN learns faster in any absolute sense — only that
deliberate gap-driven ordering beats fixed scaffold ordering per episode, and that
peer teaching transfers verified knowledge without corruption. (4) Scale is
untested: RC3 ran 100x episodes; recursive loops compound cost — a 10x self+peer leg
must rerun byte-identically before any scaling claim.

## 6. Next build step

Build the GAP organ first, alone: implement deliberate self-probing (contradiction
attempts via the eliminative machinery over the topic ledger) on a fixed topic set
with a teacher-blind probe battery as ground truth, and measure gap-confirmation
precision vs random-topic baseline. If precision doesn't beat chance, the whole
recursive-teaching claim dies before a single peer episode is designed — cheapest
falsification in the slice.
