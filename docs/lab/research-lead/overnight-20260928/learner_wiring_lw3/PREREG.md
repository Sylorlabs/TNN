# PREREG: LW3 Learner Policy Revision and Transfer

Status: PREREG-FROZEN 2026-10-02. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/learner_wiring_lw3/` only.
Worker: Learner Policy Revision Worker (LW3), subagent, 2026-10-02.
Parent mandate: from C290 (LW2), test (a) revision of the constructed
policy 381 after counterexamples, and (b) transfer of the try-keep
pattern to a new domain.

## 1. Background: what LW2 established and what it left open

LW2 (C290, verdict LW2-COMPLETE) showed that generic trial-and-selection
machinery, scoring candidates solely by the learner's own selftest
measurements, constructs policy 381 = [EVAL,WIRE0,EVAL,IFB,UNWIRE0] for
path wiring: measure baseline, wire slot0, measure, keep iff better else
revert. That is L2 construction, not L3 invention: the policy space was a
finite researcher-defined family (7^5), and the meta-driver was itself an
instance of abstract trial-and-selection (the invention regress, LW2
REPORT section 5.2, stands and is not re-litigated here).

LW2 REPORT section 9 named the coherent follow-ups, which this prereg
adopts verbatim: (a) after the learner constructs policy 381, change the
world mid-stream and test whether the learner REVISES the constructed
policy from counterexample experience rather than needing a fresh
exhaustive search; (b) test whether the try-keep pattern TRANSFERS to a
new domain (different action space and measurement), i.e., whether the
learner reuses the abstract pattern or rediscovers it from scratch.

## 2. What "revision" and "transfer" mean here (preregistered)

Revision (part R): the learner retains policy 381, encounters new
episodes where 381 measurably fails, and a revision driver seeded AT 381
explores only local edits (1- and 2-step substitutions), accepting
strictly measured improvements on the new episodes. Success is NOT just
reaching a good score: the final policy must be a short edit path from
381 (structure preserved, not discarded), must match the optimum found
by a fresh exhaustive search control, and must cost a small fraction of
the fresh-search evaluations. A driver that throws 381 away and re-runs
exhaustive search is the CONTROL, not revision.

Transfer (part T): the abstract schema of 381, [EVAL, TRY, EVAL, IFB,
REVERT], is instantiated in a NEW domain (threshold tuning: different
action space {EVAL, INC, DEC, IFB, IDLE}, different measured quantity).
The schema itself is researcher-extracted from the learner-constructed
381 (disclosed extraction, section 6); the instantiation choice (which
concrete (TRY, REVERT) pair) is made by the learner's own measurements
in the new domain, choosing among the candidate pairs by experienced
score. Controls: a researcher-fixed mapping (no experience), a blind
habit policy, and a fresh exhaustive search in the new domain.

Interpretation, frozen: positive results in R and T demonstrate L2
revision and L2 specialization/transfer. They do NOT demonstrate L3:
the revision neighborhood is finite, the schema is extracted by the
researcher, and the meta-drivers remain trial-and-selection (regress).
What would NOT count: re-running exhaustive search and calling it
revision; a researcher hand-mapping the schema to the new domain and
calling it transfer; any new mode, bridge, or handler.

## 3. World, data, hypotheses (all literals, deterministic, zero RNG)

Identical to LW2 for comparability: alphabet {0,1,2,3}, strings of
length 4, hidden rule R = all symbols distinct (learner never sees R).

TRAIN (12): positives 0123 0132 0213 1023 1203 2013;
            negatives 0012 1103 2231 3320 0101 2323.
VALID (6): positives 2301 3012 1230; negatives 0011 2202 1313.

Hypothesis slots, 2 per episode; hyp store records [kind, param]:
- helpful: kind 1 MAXCOUNT(khelp), khelp = 1 by Occam on TRAIN (6/6).
- harmful: kind 2 ALLDISTINCT-NOT (0/6 on VALID).
- neutral: kind 1 MAXCOUNT(3) (3/6 on VALID, wiring is a no-op).

Consultation list (4 slots, learner-writable, reset per episode); judge
rejects iff any wired hyp rejects; selftest = correct count on VALID.

Original episode types (LW2): A = (helpful, harmful), B = (harmful,
neutral), C = (helpful, helpful), D = (harmful, harmful).

NEW episode types (the counterexample regime; learner not told the type):
- A2: slot0 = harmful, slot1 = helpful. Optimum: wire slot1 only = 6/6.
- B2: slot0 = neutral, slot1 = harmful. Optimum: wire nothing = 3/6.
- C2 (held-out): slot0 = helpful, slot1 = helpful. Optimum 6/6.
- D2 (held-out): slot0 = harmful, slot1 = harmful. Optimum 3/6.

Training order for part R: A2, B2, A2, B2 (fixed). The world change is:
the helpful hypothesis moved from slot0 to slot1, and slot0 now holds
harmful-or-neutral content. Policy 381 tries slot0 only, so it must fail
here; that failure is the counterexample experience.

Policy alphabet (unchanged): 0=EVAL, 1=WIRE0, 2=WIRE1, 3=UNWIRE0,
4=UNWIRE1, 5=IFB, 6=IDLE. IFB: skip next step iff R0 > R1. Index order:
step0 = p/2401, step1 = (p/343)%7, step2 = (p/49)%7, step3 = (p/7)%7,
step4 = p%7.

## 4. Part R: revision after counterexamples

Modes (argv-selected): `revise`, `freshswap`.

`revise` runs four phases in one binary:
- Phase 1 (replication): exhaustive construct on (A,B,A,B), retain best
  by train total, ties to lowest index. This must reproduce LW2.
- Phase 2 (counterexample): evaluate the RETAINED policy (whatever
  phase 1 produced) on (A2,B2,A2,B2); report per-episode scores.
- Phase 3 (revision driver): steepest ascent seeded at the retained
  policy. Neighborhood = all 1-step edits (5 positions x 6 alternative
  actions = 30) plus all 2-step edits (C(5,2) x 36 = 360), 390 candidates
  per round. Each candidate scored by train total on (A2,B2,A2,B2) using
  the learner's own selftest measurements. Move to the best candidate
  iff strictly better than current (ties: lowest index); repeat until no
  strict improvement. Log moves, candidate evaluations, final policy.
- Phase 4 (held-out + overwrite diagnostic): run the revised policy on
  held-out (C2,D2); then run it on the ORIGINAL (A,B) and report.

`freshswap` (control): exhaustive search over all 7^5 = 16807 policies on
(A2,B2,A2,B2), retain best (ties: lowest index), report index and train
total. This is the "discard and re-search" baseline.

### Hand-derived predictions (part R)

P-R0 (replication): phase 1 retains policy 381 = [0,1,0,5,3], train
18/24 = (6,3,6,3). This is LW2's P3, reproduced.

P-R1 (counterexample): retained 381 on (A2,B2,A2,B2) scores 12/24 =
(3,3,3,3). Derivation: on A2, [EVAL,WIRE0,EVAL,IFB,UNWIRE0] measures
baseline 3, wires harmful slot0 (accuracy 0), measures 0 which is not
greater than 3, unwires, final 3. On B2, it measures 3, wires neutral
slot0 (no-op, still 3), 3 is not greater than 3, unwires, final 3. The
constructed policy measurably regresses (18/24 to 12/24): the
counterexample experience.

P-R2 (revision): the revision driver reaches train 18/24 at policy 725
= [0,2,0,5,4] = [EVAL,WIRE1,EVAL,IFB,UNWIRE1], in exactly 1 accepted move
and 780 candidate evaluations (390 per round: one move round plus one
verification round with no improvement). Derivation: on the new regime,
episode scores are deterministic per policy and repetitions are
identical, so train totals take values 2*(a+b) with a in {0,3,6} (A2
end-wiring {}, {0}, {1}, {0,1} give 3, 0, 6, 0) and b in {0,3} (B2
end-wiring without slot1 gives 3, with slot1 gives 0). Totals possible:
{0,6,12,18}; 24 is impossible (B2 ceiling is 3). 381 scores 12. The
unique 18-scorer is 725 (proof in section 5), which differs from 381 in
exactly 2 steps (WIRE0->WIRE1, UNWIRE0->UNWIRE1), so it lies in the
2-edit neighborhood and is the unique strict best of the 390 candidates.
Round 2 finds no strict improvement over the global optimum. The final
policy preserves the try-keep skeleton [EVAL, WIRE-slot, EVAL, IFB,
UNWIRE-slot] with the slot transposed: revision, not discard. Candidate
cost 780 vs 16807 for fresh search (4.6 percent).

P-R3 (control): `freshswap` retains policy 725, train 18/24. The
revision result matches the fresh-search optimum exactly.

P-R4 (held-out): revised 725 on (C2,D2) scores 9/12 = (6,3).
Derivation: on C2, baseline 3, wire helpful slot1 (6), 6 > 3 so IFB
skips UNWIRE1, final 6. On D2, baseline 3, wire harmful slot1 (0),
0 > 3 false so UNWIRE1 executes, final 3.

P-R5 (overwrite diagnostic, preregistered): revised 725 on the ORIGINAL
(A,B) scores 6/12 = (3,3). Derivation: on A, baseline 3, wire harmful
slot1 (0), revert, final 3. On B, baseline 3, wire neutral slot1
(no-op, 3), 3 > 3 false, unwire, final 3. Counterexample-driven revision
adapts to the new regime but OVERWRITES the old competence (was 18/24).
This limitation is recorded honestly; it is diagnostic, not a kill-bar
failure: the bar is that revision works on the new regime, and the
overwrite is reported as a finding for the continuing-learner agenda.

## 5. Uniqueness proof for 725 (hand derivation, frozen)

Claim: 725 is the unique policy scoring 18/24 on (A2,B2,A2,B2).

Per-episode ceilings: A2 max 6, achieved only by end-wiring exactly
{slot1} (any wiring containing harmful slot0 scores 0; empty scores 3).
B2 max 3, achieved only by end-wiring without slot1 (any wiring with
harmful slot1 scores 0). So 18/24 requires end-wiring {1} on A2 episodes
and slot1-free end-wiring on B2 episodes.

A policy without IFB has identical end-wiring on both episode types,
hence at most 12/24. So IFB is required with a branch that differs
across episodes. IFB skips the next step iff R0 > R1, where registers
come from EVALs (EVAL sets R1=old R0, R0=current accuracy; initial
R0=R1=-1). A branch difference requires two EVALs straddling a wiring
whose effect differs by episode. From empty: WIRE0 gives A2 3->0, B2
3->3; WIRE1 gives A2 3->6, B2 3->0. After straddling WIRE0, (R0,R1) =
(0,3) on A2 and (3,3) on B2: no skip on either (0 > 3 false, 3 > 3
false). After straddling WIRE1, (R0,R1) = (6,3) on A2 and (0,3) on B2:
skip on A2 only. So the only differentiating conditional is
EVAL, WIRE1, EVAL, IFB with the skipped step executed on B2 only. The
executed step must repair B2 (list {1}, accuracy 0) to slot1-free:
UNWIRE1 is the only such action (UNWIRE0/WIRE0/WIRE1/EVAL/IDLE/IFB all
leave B2 at 0; verified by case). Positions: IFB at l skips l+1, so with
5 steps the skeleton EVAL,WIRE1,EVAL,IFB,UNWIRE1 must occupy positions
0,1,2,3,4 in order (any leading non-EVAL action pushes the index above
725 without helping; any gap makes the 5-step budget overflow). Hence
the unique optimum is index 0*2401 + 2*343 + 0*49 + 5*7 + 4 = 725.

## 6. Part T: transfer to a new domain

New domain: threshold tuning. Learner state is a threshold p in
{0,1,2,3}; hypothesis = MAXCOUNT(p) (reject iff maxcount > p),
evaluated on the SAME VALID items (world labels = experience).
Alphabet: 0=EVAL, 1=INC, 2=DEC, 3=IFB, 4=IDLE. EVAL: R1=R0,
R0=accuracy(p). INC: p=min(3,p+1). DEC: p=max(0,p-1). IFB: skip next
iff R0 > R1. Policy length 5. Episodes: T1 with p0=2, T2 with p0=0.
Accuracy by hand: p=0 -> 3/6 (rejects all: positives wrong, negatives
right); p=1 -> 6/6; p=2 -> 4/6 (positives right; negatives: 2202 right,
0011 and 1313 wrong); p=3 -> 3/6 (rejects none).

The transferable schema, extracted by the researcher from the
learner-constructed 381 (disclosed extraction): [EVAL, X, EVAL, IFB,
X_prime], the abstract try-keep form. Candidate instantiations:
(X, X_prime) in {(DEC,INC), (INC,DEC)} (the two directed try actions;
EVAL/IFB/IDLE as X are degenerate and excluded by the schema, which
requires a state-changing try action).

Modes: `transfer`, `fixedmap`, `habit`, `freshsearch`.

`transfer`: per episode independently, evaluate both schema candidates
from p0 using the learner's own accuracy measurements, keep the
strictly better (ties: first candidate). Report choices and scores.
`fixedmap`: researcher-fixed mapping (INC,DEC) with no experience, both
episodes. `habit`: blind [DEC,DEC,DEC,DEC,DEC] (the analog of LW2's
bandit habit: a context-blind action routine). `freshsearch`: exhaustive
search over 5^5 = 3125 policies on (T1,T2), retain best (ties: lowest
index), report index and total.

### Hand-derived predictions (part T)

P-T1 (transfer): T1 keeps (DEC,INC) scoring 6/6; T2 ties 6/6 vs 6/6 and
keeps the first candidate (DEC,INC) scoring 6/6; total 12/12 with 4
candidate evaluations. Derivation: T1 from p0=2: (DEC,INC) =
[EVAL,DEC,EVAL,IFB,INC]: EVAL gives 4; DEC to p=1; EVAL gives 6 with
R1=4; 6 > 4 so INC skipped; final 6. (INC,DEC): EVAL 4; INC to p=3;
EVAL 3 with R1=4; 3 > 4 false so DEC executes to p=2; final 4. T2 from
p0=0: (DEC,INC): EVAL 3; DEC floors at p=0; EVAL 3 with R1=3; 3 > 3
false so INC executes to p=1; final 6. (INC,DEC): EVAL 3; INC to p=1;
EVAL 6 with R1=3; 6 > 3 so DEC skipped; final 6.

P-T2 (fixed mapping): (INC,DEC) on T1 = 4/6, on T2 = 6/6, total 10/12.
Experience-free schema application underperforms measurement-driven
instantiation.

P-T3 (blind habit): [DEC]x5 on T1: p 2->1->0->0->0->0, final 3/6; on T2:
p stays 0, final 3/6; total 6/12. The context-blind routine fails where
the measurement-conditioned schema succeeds.

P-T4 (fresh search): reaches 12/12 (ceiling; e.g. [EVAL,DEC,EVAL,IFB,INC]
achieves it). The retained lowest-index optimum is REPORTED as observed
(score predicted, index not hand-predicted).

## 7. Determinism and kill bar

P-D: 3 runs per mode (6 modes: revise, freshswap, transfer, fixedmap,
habit, freshsearch; 18 runs total), byte-identical stdout within each
mode triple (sha256 + pairwise cmp).

Kill bar: P-R0, P-R1, P-R2, P-R3, P-R4, P-R5, P-T1, P-T2, P-T3, P-T4, and
P-D ALL hold. Then verdict: LW3-COMPLETE (with revision and transfer
analysis). Any prediction failure is reported as observed with the
deviation analyzed; the bar is not moved.

## 8. Architecture accounting (preregistered)

New modes: 0. New bridges: 0. New handlers: 0. Standalone experiment;
nothing merged into any shared substrate. Cognition lines added to
protected core or learner: 0. Researcher-authored generic machinery
(disclosed): consultation list, selftest, wire/unwire, hyp kinds,
Occam selection, both policy alphabets, EVAL/WIRE/UNWIRE/IFB/IDLE/INC/DEC
semantics, the revision neighborhood generator, the schema candidate
enumerator, the exhaustive search drivers. All domain-neutral; none
encodes try-and-keep as a template or schedule at the object level.
Learner-produced state: retained policy 381 (phase 1), revised policy
725 (phase 3), per-episode schema choices (part T). The schema
abstraction in part T is researcher-extracted from 381; the
instantiation choice is learner-measured. This extraction is the honest
boundary of the transfer claim (L2, not L3).

## 9. Falsifiers and honest limitations (preregistered)

- If phase 1 does not reproduce 381, the revision seed differs from the
  preregistered one; results are reported as observed, not forced.
- If the revision driver needs the fresh-search control to match (i.e.,
  local revision stalls below 18/24), that is an informative negative
  about greedy revision, reported as such.
- P-R5 is expected to show overwrite (6/12 on old episodes); if instead
  the revised policy retains old competence, that is reported as a
  surprise, not a failure.
- Part T uses 2 candidate pairs; a wider schema family is explicitly
  out of scope. The claim is specialization of the constructed pattern
  to one new domain, not general transfer.
