# REPORT: Belief under Delayed Evidence and Rediscovery (H extension)

## Question

Belief formation (commit 78e5a5eac) proved rational 3 phase belief revision
with reliability learning and the independence discount both causal by
ablation. Three gaps remained: (1) delayed evidence arriving long after a
belief settled, does the delay itself weaken the prior; (2) evidence
evicted under memory pressure then rediscovered, does the belief double
count or does provenance prevent it; (3) a source reliable for many rounds
that turns adversarial, does reliability learning track the turn.
Rationality is scored relative to the evidence available at the time,
never against omniscience.

## Mechanism

The baseline machinery is carried over unchanged: evidence records, source
reliability learned from verification outcomes only (neutral 1000 until 2
verifications), independence discount (k-th claim by the same source for
the same hypothesis in one episode contributes half the previous), belief
score B = s1 - s2 in milli units, bands U = wmax and T = 2U, statuses
NONE/PROVISIONAL/UNCERTAIN/CONFIDENT with identical cutoffs.

New machinery, all learner state, no new subsystems:

1. Finite evidence table (32 records) with FIFO eviction under memory
   pressure. Eviction drops the receipt but the score contribution
   persists: the learner remembers the bottom line and forgets the detail.
2. Event identity register (128 ids). Every observation carries an event
   id. A re presented event whose id is already registered is rejected:
   no record, no score change, ndup increments. Familiarity without
   recall. Genuine new events (new ids) are always counted.
3. Ablation arm NAIVE: identity register disabled entirely (baseline
   behavior under pressure). Preregistered to double count; it is the bug
   control, scored 0/1 by design.

Honest scaffold split. Researcher scaffold: table layout, FIFO order,
identity register form, band rule forms, discount halving, status cutoffs,
event id assignment. Learner owned: every reliability value, every
support total, wmax, every status verdict, every duplicate verdict, all
provenance answers, the identity register contents.

## World script (fixed, deterministic, no randomness)

Calibration: Sa 1/2 (rel 500), Sb 2/2 (rel 1000), wmax 2000.
Phase A: Sb, Sc, Sd each report H1 moderate once (eids 101-103).
Phase B1 delay: 12 unrelated calibration events on verifiable facts with
fresh sources, all correct, each contribution 1000 below wmax. The delay
holds more events (12) than the entire prior history (7).
Phase B2: fresh sources Se, Sf, Sg, Sh each report H2 strong once
(eids 201-204), contributions 3000 each, wmax becomes 3000.
Phase C: 32 unrelated weak calibration events (memory pressure burst),
then the SAME 4 H2 strong events re presented with identical eids, then
one genuine new H2 strong event (eid 205) from a fresh source.
Phase D (separate state): Sx 20 correct weak calibrations, one Sx H1
moderate observation (eid 3031), 10 wrong weak calibrations, one more Sx
H1 moderate observation with a new eid (eid 3052).

## Results (3/3 byte identical, sha256 8ce75c9108cc26990280ca4209a8a3cfe72feda4dbb761aadb476717fea8056f)

```
PROV cal: Sa rel=500 Sb rel=1000
PROV A: leader=1 status=CONFIDENT s1=6000 s2=0 conf=6000 U=2000 T=4000
PROV B1-delay: leader=1 status=CONFIDENT s1=6000 s2=0 conf=6000 U=2000 T=4000
PROV B2: leader=2 status=CONFIDENT s1=6000 s2=12000 conf=-6000 U=3000 T=6000
PROV C-burst: leader=2 status=CONFIDENT s1=6000 s2=12000 conf=-6000 U=3000 T=6000
PROV C identity: nid=55 seen201=1 seen202=1 seen203=1 seen204=1
PROV C-rediscovery: leader=2 status=CONFIDENT s1=6000 s2=12000 conf=-6000 U=3000 T=6000
PROV C-genuine-new: leader=2 status=CONFIDENT s1=6000 s2=15000 conf=-9000 U=3000 T=6000
NAIVE C-rediscovery: leader=2 status=CONFIDENT s1=6000 s2=24000 conf=-18000 U=3000 T=6000
PHASED rel after 20 correct: 1000
PHASED reliable-phase claim contrib: 2000
PHASED rel after 5 adversarial: 800
PHASED rel after 10 adversarial: 666
PHASED adversarial-phase claim contrib: 1332
ALL PASS
```

Phase A: three independent moderate H1 reports settle the learner at
CONFIDENT H1 (s1 6000 against bar T 4000). Rational 1/1: the evidence is
one sided and clears the learner's own certainty bar.

Phase B1 delay: after 12 unrelated events the status line is bit identical
to pre delay (status, s1, s2, wmax all unchanged). The delay itself does
not weaken the prior: no contrary evidence arrived, so nothing changed.
Rational 1/1. Time passing is not evidence.

Phase B2: the delayed strong evidence revises the settled belief with
latency 4. After the 1st strong claim the learner is UNCERTAIN leaning H1
(code 12: the 6000 prior still leads the single 3000 claim by 3000, inside
the band); after the 2nd it is tied UNCERTAIN; after the 3rd UNCERTAIN
leaning H2; after the 4th CONFIDENT H2 (first contrary seq 20, revision
seq 23, s2 12000). Rational 1/1. Note the revision bar is identical to the
baseline's 4 contrary pieces: the long delay did not raise or lower what
it takes to overturn a settled belief, and the first-contact response is
directional uncertainty rather than a symmetric flip. The E3 prereg text
carried an arithmetic slip (22 written for the after 1st checkpoint);
it was amended transparently before the frozen evaluation runs and the
corrected expectation (12) held on all 3 runs.

Phase C eviction: the 32 event burst evicted exactly the 23 pre burst
records FIFO, including all 4 H2 records. Scores persisted (s1 6000,
s2 12000, status CONFIDENT H2). belief_why(H2) returns 0 retained
records, while the identity register answers all 4 H2 eids as seen.
Provenance degrades gracefully: the receipts are gone, the familiarity
remains, the bottom line is intact.

Phase C rediscovery, PROV arm: all 4 re presented events rejected as
duplicates (ndup 4), no new records, s2 stays 12000. No double count.
The genuine new event (eid 205) is accepted: s2 rises to 15000. The
register blocks replays without blocking news. Rational 1/1.

Phase C rediscovery, NAIVE arm: the same 4 events are added as fresh
records and s2 doubles to 24000. The standing belief contains the same
evidence twice, and the why provenance listing shows 4 records with no
trace of the duplication. The bug the identity register exists to
prevent appears exactly as preregistered. Scored 0/1 as the documented
bug control.

Phase D: reliability tracks the turn. rel 1000 after 20 correct rounds,
800 after 5 adversarial rounds, 666 after 10, monotonic decrease. The
behavioral consequence is real: an identical Sx H1 moderate claim
contributes 2000 in the reliable phase and 1332 in the adversarial
phase. Rational 1/1: trust follows the observed track record, and the
turn is caught within 5 wrong rounds.

Rationality total: 5/6 (A, B1, B2, C-PROV, D pass; C-NAIVE is the
expected fail bug control).

## Kill bars

K1: 3/3 byte identical, sha256
  8ce75c9108cc26990280ca4209a8a3cfe72feda4dbb761aadb476717fea8056f. Pass.
K2: Phase A st 13, s1 6000, s2 0. Pass.
K3: delay changes nothing (status, s1, s2, wmax). Pass.
K4: latency 4, first contrary seq 20, revision seq 23, final st 23,
  s2 12000. Pass (with the transparent E3 amendment noted above).
K5: PROV arm evicted 23, ndup 4, s2 12000, no new records on
  rediscovery. Pass.
K6: NAIVE arm s2 24000 on rediscovery; the bug appears. Pass.
K7: genuine new event counted, s2 15000. Pass.
K8: rels 1000/800/666 monotonic; contribs 2000 vs 1332. Pass.
K9: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag,
  safebin PATH, no forbidden executables. Unfrozen only, frozen
  untouched, paper untouched, nothing pushed, explicit pathspecs. Pass.

## Architecture accounting

- Cognition lines added: 485 (belief_delayed.zag, self contained).
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- Learner state structures created: one evidence table (32 records, 7
  cells each, FIFO eviction), one source reliability table (64 sources),
  one episode discount table, one event identity register (128 ids).
- Net capability: delay invariance, revision latency under delay,
  eviction with graceful provenance degradation, duplicate rejection
  with no over blocking, adversarial turn tracking, at ~97 lines per
  capability.

## Limitations (honest)

- Eviction preserves score contributions by design. Genuine
  forgetting induced weakening (the belief should fade when its grounds
  are forgotten) is not modeled; that is a separate experiment.
- The identity window is bounded (128 ids); past the window, replays
  become re countable. The bound is explicit in state, not hidden.
- Event strength (weak/moderate/strong) is assigned by the world script
  at observation time, as in the baseline. Strength induction from raw
  observations remains future work.
- Band rule forms (U = wmax, T = 2U) remain researcher scaffold; only
  the values are learner derived, as in the baseline.
- Single binary question; belief interaction across questions untested.
- Not yet merged into the tag-61 consequence substrate. Merge path:
  evidence records and the identity register map to substrate rows;
  eviction and duplicate rejection become substrate behaviors. No new
  subsystem needed.

## Verdict

BELIEF-DELAYED-COMPLETE. Rationality 5/6 relative to evidence at time
(the sixth is the preregistered bug control that behaved as predicted).
Delayed evidence revises a settled belief with the same 4 piece bar as
immediate evidence; the delay itself weakens nothing; provenance via the
event identity register prevents double counting on rediscovery while
the ablated arm double counts exactly as predicted; reliability learning
tracks a reliable to adversarial turn within 5 wrong rounds with a
measured drop in claim weight. Deterministic 3/3 byte identical. Pure
Zag, safebin, unfrozen only, paper untouched, nothing pushed.
