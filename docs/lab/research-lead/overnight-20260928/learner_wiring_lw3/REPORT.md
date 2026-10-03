# REPORT: LW3 Learner Policy Revision and Transfer

Verdict: LW3-COMPLETE (with revision and transfer analysis, sections 5-6).
Date: 2026-10-02. Worker: Learner Policy Revision Worker (LW3, subagent).
Prereg: PREREG.md, frozen and committed before implementation (see section 8
for the disk-full placement note; prereg content is byte-identical to the
frozen version).

## 1. Question

LW2 constructed policy 381 = [EVAL,WIRE0,EVAL,IFB,UNWIRE0] for path wiring
via generic trial-and-selection (L2, not L3; the invention regress stands).
Two coherent follow-ups remained: (a) when the world changes so that 381
measurably fails, does the learner REVISE the constructed policy from
counterexample experience, rather than discarding it for a fresh exhaustive
search; (b) does the try-keep pattern TRANSFER to a new domain with a
different action space and measurement, specialized by experience rather
than rediscovered from scratch. All predictions were hand-derived and
frozen before implementation, including a uniqueness proof for the
post-change optimum.

## 2. Design (summary; full detail in PREREG.md)

Same world, data, and hypothesis kinds as LW2. New episode types for the
counterexample regime: A2 = (harmful, helpful), B2 = (neutral, harmful),
held-out C2 = (helpful, helpful), D2 = (harmful, harmful). The world change
is that the helpful hypothesis moved from slot0 to slot1.

Part R (revision), modes `revise` and `freshswap`: `revise` replicates the
LW2 construct on (A,B,A,B), evaluates the retained policy on
(A2,B2,A2,B2), then runs a revision driver: steepest ascent seeded AT the
retained policy over 1-edit (30) plus 2-edit (360) neighborhoods, scored by
the learner's own selftest totals, strictly-improving moves only. Then the
revised policy runs on held-out (C2,D2) and, as a diagnostic, on the
original (A,B). `freshswap` is the discard-and-re-search control:
exhaustive 7^5 search on the new regime.

Part T (transfer), modes `transfer`, `fixedmap`, `habit`, `freshsearch`:
new domain of threshold tuning (state p in {0,1,2,3}, hyp = MAXCOUNT(p) on
the same VALID; alphabet EVAL/INC/DEC/IFB/IDLE; episodes T1 with p0=2, T2
with p0=0). The schema [EVAL, X, EVAL, IFB, X'] is researcher-extracted
from 381 (disclosed); `transfer` chooses the (X, X') instantiation per
episode from {(DEC,INC), (INC,DEC)} by the learner's own measurements.
Controls: `fixedmap` (researcher-fixed (INC,DEC), no experience), `habit`
(blind [DEC]x5), `freshsearch` (exhaustive 5^5 = 3125 on (T1,T2)).

## 3. Results: predictions vs observed (all 18 runs)

| prediction | expected | observed | match |
|------------|----------|----------|-------|
| P-R0 phase1 replicates LW2 | policy 381, train 18/24 (6,3,6,3) | identical | HOLD |
| P-R1 counterexample | 381 on new regime: 12/24 (3,3,3,3) | identical | HOLD |
| P-R2 revision | 1 move, 780 evals, final 725, 18/24 | identical | HOLD |
| P-R3 fresh-search control | policy 725 (unique), 18/24 | identical | HOLD |
| P-R4 held-out | 725 on (C2,D2): 9/12 (6,3) | identical | HOLD |
| P-R5 overwrite diagnostic | 725 on original (A,B): 6/12 (3,3) | identical | HOLD |
| P-T1 transfer | choices (0,0), total 12/12, 4 evals | identical | HOLD |
| P-T2 fixed mapping | 10/12 (4+6) | identical | HOLD |
| P-T3 blind habit | 6/12 (3+3) | identical | HOLD |
| P-T4 fresh search | 12/12 (index reported) | 12/12, policy 61 | HOLD |
| P-D determinism | 3/3 byte-identical per mode | sha256 + cmp confirm | HOLD |

Kill bar (all predictions hold): MET. Verdict: LW3-COMPLETE.

Raw outputs (run1 of each mode; runs 2 and 3 byte-identical):

revise:
LW3|mode=revise
LW3|phase1_policy=381|phase1_train=6,3,6,3|total=18|n=24
LW3|retained_on_new=3,3,3,3|total=12|n=24
LW3|revision_moves=1|revision_evals=780|final_policy=725|final_train=6,3,6,3|total=18|n=24
LW3|heldout=6,3|total=9|n=12
LW3|final_on_old=3,3|total=6|n=12

freshswap:
LW3|mode=freshswap
LW3|policy=725|train=6,3,6,3|total=18|n=24

transfer:
LW3|mode=transfer
LW3|T1_choice=0|T1_score=6|n=6
LW3|T2_choice=0|T2_score=6|n=6
LW3|total=12|n=12|evals=4

fixedmap:
LW3|mode=fixedmap
LW3|T1=4|T2=6|total=10|n=12

habit:
LW3|mode=habit
LW3|T1=3|T2=3|total=6|n=12

freshsearch:
LW3|mode=freshsearch
LW3|policy=61|T1=6|T2=6|total=12|n=12

## 4. What the numbers establish

a) The counterexample regime works as designed (P-R1). Moving the helpful
hypothesis to slot1 drops the retained 381 from 18/24 to 12/24: 381 tries
slot0 only, so it wires the harmful-or-neutral slot0 content and reverts
to baseline on every new episode. The failure is measurable by the
learner's own selftest, with no harness labels.

b) The learner revises rather than discards (P-R2, P-R3). Seeded at 381,
one accepted 2-edit move reaches policy 725 = [EVAL,WIRE1,EVAL,IFB,
UNWIRE1]: the try-keep skeleton preserved, slot transposed
(WIRE0->WIRE1, UNWIRE0->UNWIRE1). The revision matches the fresh
exhaustive search optimum exactly (725 is the unique 18/24 policy, proved
in PREREG section 5 and confirmed empirically), at 780 vs 16807 candidate
evaluations (4.6 percent; 3120 vs 67228 episode evaluations). The revision
path is 381 -> 725, a single measured improvement, not a global re-search.

c) The transferred pattern specializes correctly (P-T1..T4). In the
threshold domain, per-episode measurement chose (DEC,INC) on both
episodes for 12/12 at 4 candidate evaluations, matching the fresh
exhaustive search score (12/12) at a tiny fraction of its cost (4 vs 6250
episode evaluations). The experience-free fixed mapping scores 10/12 and
the blind DEC habit scores 6/12, so the measurement-driven instantiation
choice is load-bearing: applying the schema blindly is not enough.

d) Fresh search finds degenerate optima; transfer preserves form. The
fresh-search optimum in the new domain is policy 61 =
[EVAL,EVAL,DEC,DEC,INC], a formless routine that happens to land p=1 from
both starts. The transferred policy [EVAL,DEC,EVAL,IFB,INC] keeps the
try-keep form (measure, try, re-measure, keep-iff-better-else-revert) and
would still behave sensibly from other starts (e.g. p0=3: DEC to p=2
scores 4, not better than 3, so INC reverts to p=3; the degenerate policy
61 from p0=3 gives DEC,DEC,INC to p=2, scoring 4/6). Form preservation is
not scored by the kill bar, but it is the observable difference between
reusing a pattern and stumbling onto a score.

## 5. Revision analysis

This is the deliverable the parent asked for: did the learner revise the
policy, or merely discard it.

The honest answer is revision, in a precisely bounded sense. The driver
never evaluates more than the 390-candidate local neighborhood of the
current policy; it starts from the retained 381; it accepts only strictly
measured improvements; it stops after one verification round with no
improvement. The final policy is provably a 2-edit descendant of 381,
and the single accepted move is exactly the slot transposition the
counterexample evidence calls for (the helpful content moved to slot1;
the try-keep loop now tries slot1). The structure [EVAL, WIRE-slot, EVAL,
IFB, UNWIRE-slot] survives the world change intact. Under the
learning-evidence taxonomy this is L2: a constructed policy adapted by
further experience through generic machinery. It is not L3: the
neighborhood is finite and researcher-defined, and the driver remains
trial-and-selection at the meta level (the regress).

The overwrite diagnostic (P-R5) is the important honest limitation.
Policy 725 scores 6/12 on the original (A,B) episodes, down from 18/24:
counterexample-driven revision adapts to the new regime and FORGETS the
old one. This was preregistered as a diagnostic rather than a failure,
and the outcome confirms the concern: local revision without a retention
mechanism is adaptation, not accumulation. A continuing learner needs
revision that preserves old competence while adding new; that is the next
target (section 9).

## 6. Transfer analysis

The second deliverable: did the try-keep pattern transfer to the new
domain, or was it rediscovered from scratch.

The honest answer is transfer-as-specialization, again L2. The abstract
form was extracted from 381 by the researcher (disclosed in PREREG
section 8; this extraction is the boundary of the claim), but everything
after that is learner-measured: the two candidate instantiations were
scored by the learner's own accuracy measurements in the new domain, per
episode, and the better was kept. The new domain differs in the action
space (INC/DEC instead of WIRE/UNWIRE), the state (a threshold instead of
a consultation list), and the measured quantity (hypothesis accuracy
instead of judge accuracy), so the instantiation is not a relabeling:
(DEC,INC) had to beat (INC,DEC) by measurement on T1 (6 vs 4), and the
tie on T2 was broken by the preregistered first-candidate rule.

What transfer does NOT show: the schema did not originate in the learner
(the researcher wrote down the abstraction), the candidate family is
finite (2 pairs), and a fresh search reaches the same score. The result
therefore demonstrates that a constructed pattern can be ported to a new
domain by small experience-driven specialization, not that the learner
invents abstractions. Framed against LW2's regress: the abstract
trial-and-selection form, once constructed at the object level in one
domain, is re-specializable to another domain at low experience cost.
That is the coherent, non-mystical reading of "transfer of try-keep".

## 7. Architecture accounting

- New modes: 0. New bridges: 0. New handlers: 0.
- Standalone experiment; nothing merged into any shared substrate.
  Cognition lines added to protected core or learner: 0.
- Researcher-authored generic machinery (disclosed): consultation list,
  selftest, wire/unwire, hyp kinds (MAXCOUNT, ALLDISTINCT-NOT), Occam
  selection, the 7-action and 5-action policy alphabets, EVAL/WIRE/UNWIRE/
  IFB/IDLE/INC/DEC semantics, the revision neighborhood generator, the
  schema candidate enumerator, the exhaustive search drivers, and the
  schema abstraction extracted from 381 for part T. All domain-neutral;
  none encodes try-keep as a template or schedule at the object level.
- Learner-produced state: retained policy 381 (phase 1 replication),
  revised policy 725 (revision driver, 2-edit descendant), per-episode
  schema choices (0,0) in part T.

## 8. Toolchain, determinism, and the disk-full placement note

- Safebin guard (NAMECHECK.md Step 0): PASS. python3/python unresolvable
  under worker PATH; znc 2026.07.0-dev used for the build.
- Pure Zag, zero RNG, zero Python in build, run, or analysis.
- 18 runs total; 6 distinct stdout byte strings; sha256 identical within
  each mode triple (sha256sums.txt) plus pairwise cmp.
- Stdout via single preallocated buffer + one raw syscall write; every
  binary's stdout bytes verified against the preregistered predictions
  before any claim was trusted. No _zag_print used.
- Revision cost: 780 candidate evaluations (390 per round x 2 rounds);
  fresh-search control: 16807. Transfer cost: 4 candidate evaluations;
  fresh-search control: 3125 policies x 2 episodes.
- Placement note: at worker start, /home/hatch was 100 percent full
  (100G/100G used; df confirmed), so the frozen PREREG.md and NAMECHECK.md
  could not be written into the repo immediately. The prereg content was
  finalized BEFORE any implementation was written (freeze ordering
  preserved in substance); all implementation and runs were performed in
  /tmp (separate tmpfs with free space); the prereg file committed to the
  repo is byte-identical to the frozen version (sha256 recorded below).
  No implementation edit preceded the freeze. Frozen PREREG.md sha256:
  recorded at commit time in the commit message.

## 9. Deliverables

- PREREG.md (frozen pre-implementation; byte-identical to the frozen
  version), NAMECHECK.md
- lw3.zag (source), build.sh, compile.log
- lw3_bin (built binary)
- runs/{revise,freshswap,transfer,fixedmap,habit,freshsearch}_run{1,2,3}.txt
  (18 outputs)
- sha256sums.txt
- REPORT.md (this file)

All under docs/lab/research-lead/overnight-20260928/learner_wiring_lw3/.
Committed locally with explicit pathspecs. Nothing pushed (standing red
line). Paper untouched.

## 10. Recommended follow-up

LW4 (cumulative revision): the P-R5 overwrite finding is the sharpest open
problem. Test whether a revision driver can adapt to the counterexample
regime WITHOUT losing the old regime: e.g., a longer policy space (7-9
steps) where try-keep can cover both slots, seeded at 381, with the
revision score summed over old AND new episodes. The question is whether
local revision can EXTEND a constructed policy (structural growth: try
slot0, revert, then try slot1) rather than transpose it. If greedy local
revision cannot cross the valley, that is an informative negative about
the limits of seeded hill-climbing and motivates a different revision
operator.

LW5 (transfer breadth): one new domain is a single data point. Port the
schema to a second structurally different domain (e.g., ordering or
assembly actions) with a larger candidate instantiation family, and test
whether the measurement-driven choice keeps working as the family grows.

Both keep the preregistered interpretation: revision and transfer are L2;
the regress still rules out strong-sense invention claims, so frame
accordingly and do not re-litigate the fixed point.
