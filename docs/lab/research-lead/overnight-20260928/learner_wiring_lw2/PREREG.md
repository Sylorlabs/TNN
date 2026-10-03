# PREREG: LW2 Learner Invention of the Try-and-Keep Policy (W4)

Status: PREREG-FROZEN 2026-10-02. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/learner_wiring_lw2/` only.
Worker: Learner Policy Invention Worker (subagent, 2026-10-02).
Parent mandate: test whether the learner can invent the try-and-keep
policy (W4) itself, rather than running a supplied schedule.

## 1. Background: the LW1 (C289) gap

LW1 showed the learner CAN self-wire given four pieces: W1 (writable
path), W2 (self-evaluation), W3 (write action), W4 (try-and-keep policy).
But W4 was researcher-authored generic machinery: the fixed schedule
[selftest, wire, selftest, keep iff better]. The learner created the
SPECIFIC link and the keep decision, but not the policy form itself.

Named open gap (LW1 REPORT section 5): a learner that invents W4, the idea
of trying path modifications and keeping measured improvements, with no
researcher-supplied meta-policy. LW1 section 5 stated the requirements:
(i) path-modification present as a candidate action, (ii) a
credit-assignment path from "wiring kept" back to "trying modifications
was valuable", (iii) no researcher code that runs the try/measure loop on
a fixed schedule. LW1 section 9 recommended: give the learner
path-modification as one action among several, a persistent value estimate
per action class updated from its own measured outcomes, and test whether
the try-measure-keep loop for path wiring is discovered rather than
scheduled.

This experiment runs that recommended test (the bandit condition) AND a
stronger test (the construct condition), with a scheduled control and a
no-driver ablation.

## 2. What "invention" means here (preregistered, load-bearing)

Two senses are distinguished BEFORE results:

(a) Strong sense (L3): the learner constructs W4 with no
researcher-authored trial-and-selection machinery at any level, and not by
selecting from a finite researcher-enumerated policy family.

(b) Weak (relativized) sense (L2): the SPECIFIC try-and-keep procedure
for path wiring is produced by generic learner machinery from the
learner's own measurements, and was not written by the researcher. The
machinery may be researcher-authored if it is generic (no path-specific
content, no try-measure-keep template).

Preregistered theoretical claim (the invention regress): in any finite
learner program, the topmost driver is fixed researcher code. If that
driver yields goal-directed policy construction, it embodies
trial-and-selection, which is the abstract form of W4 itself ("try
candidates, measure, retain the better"). Therefore strong-sense invention
of W4 is incoherent as an experimental target: W4's abstract form is the
fixed point of the invention regress, coextensive with goal-directed
learning itself. What CAN be tested is (b): specialization/construction
of the abstract form into a concrete path-wiring policy from experience.
A positive construct result therefore demonstrates L2 construction, NOT
L3 invention. This interpretation is frozen here, before results, so it
cannot be adjusted to flatter the outcome.

What would NOT count (excluded by design): the researcher encoding
try-measure-keep as a candidate policy, or running it on a fixed schedule.
The policy alphabet (section 5) contains only atomic actions plus one
generic conditional; the search is not told what to find.

## 3. World, data, hypotheses (all literals, deterministic, zero RNG)

Same world as LW1 for comparability. Alphabet {0,1,2,3}, strings of
length 4. Hidden rule R: all four symbols distinct. The learner sees only
labeled examples, never R.

TRAIN (12): positives 0123 0132 0213 1023 1203 2013;
            negatives 0012 1103 2231 3320 0101 2323.
VALID (6, learner self-test labels): positives 2301 3012 1230;
            negatives 0011 2202 1313.

Hypothesis slots (2 per episode):
- Helpful hyp H_help: kind=1 MAXCOUNT(1), reject iff some symbol occurs
  more than once. Acquired ONCE at start by Occam selection over k=1..3
  on TRAIN (same as LW1; learner-determined content). On VALID: 6/6.
- Harmful hyp H_harm: kind=2 ALLDISTINCT-NOT, reject iff all four symbols
  distinct (maxcount == 1). Placed by the experiment (disclosed
  manipulation). On VALID: positives (all distinct) rejected, negatives
  (have repeats) accepted: 0/6. Strictly worse than the 3/6 accept-all
  baseline, so wiring it is measurably harmful.
- Neutral hyp H_neut: kind=1 MAXCOUNT(3), reject iff some symbol occurs
  more than 3 times. On VALID the maximum maxcount is 3 (item 2202), so it
  never rejects there: wiring it is a no-op (3/6, same as baseline).

The judge reads the consultation list (W1, 4 slots, learner-writable,
reset to empty at each episode start) and rejects iff ANY wired hyp
rejects. W3 actions: wire(h) appends slot h (no-op if present or full);
unwire(h) removes slot h.

W2: selftest() runs the judge over all 6 VALID items, counts correct
against world labels (experience, same standing as TRAIN labels).

## 4. Episodes

Each episode: consultation list reset to empty; hypothesis slots loaded
per the episode type below. The learner is NOT told the episode type (no
task label). Training episodes (in fixed order): A, B, A, B. Held-out
episodes (new wirings, same alphabet): C, D. All episode scores are the
learner's own selftest measurements; no harness labels are used anywhere.

- Episode A: slot0 = H_help, slot1 = H_harm.
- Episode B: slot0 = H_harm, slot1 = H_neut.
- Episode C (held-out): slot0 = H_help, slot1 = H_help.
- Episode D (held-out): slot0 = H_harm, slot1 = H_harm.

Design rationale: in A, wiring slot0 helps (6/6) and wiring slot1 hurts
(0/6). In B, wiring slot0 hurts (0/6) and wiring slot1 is neutral (3/6).
A fixed blind habit ("always wire slot0") therefore fails half the
training episodes. Only measurement-conditioned wiring succeeds on both.
C and D test generalization to new wirings: C rewards wiring (either
slot), D rewards wiring nothing.

Per-episode optimal scores: A=6, B=3, C=6, D=3.

## 5. Learner machinery (disclosed, generic, domain-neutral)

Atomic actions:
- EVAL: R1 = R0; R0 = selftest(). (Registers R0/R1 persist within an
  episode, init R0 = R1 = -1 at each episode start.)
- WIRE0 / WIRE1: wire slot 0 / 1.
- UNWIRE0 / UNWIRE1: unwire slot 0 / 1.
- IDLE: no-op.
- IFB (generic compare-and-branch): if R0 > R1, skip the NEXT step;
  otherwise execute it.

Policy: a fixed sequence of exactly 5 steps over the 7-action alphabet
(indexed EVAL=0, WIRE0=1, WIRE1=2, UNWIRE0=3, UNWIRE1=4, IFB=5, IDLE=6).
Policy space: 7^5 = 16807 policies, indexed 0..16806 in least-significant
step-last order (step0 = p / 2401, step1 = (p / 343) % 7,
step2 = (p / 49) % 7, step3 = (p / 7) % 7, step4 = p % 7).

Level-2 drivers (the candidate "invention" mechanisms):
- bandit: persistent value estimates Q[a] = sums[a]/counts[a] over three
  atomic actions {WIRE0, WIRE1, IDLE} (untried = 0), updated by the learner
  from its own episode scores (exact integer cross-multiplication, no
  floats). Per episode it executes argmax_a Q[a] (ties: lowest index),
  observes the episode selftest score, updates Q. No within-episode
  measurement, no conditional: this is LW1 section 9's recommended test.
- construct: exhaustive evaluation of all 16807 policies on the four
  training episodes (each episode: fresh list, R0=R1=-1, run 5 steps,
  episode score = final selftest). Retain the strictly-best policy by
  training total; ties keep the lowest index. The retained policy is then
  frozen and run on held-out C, D. The driver is generic: it knows nothing
  about paths, slots, or try-and-keep; it only maximizes measured totals.
  It IS an instance of abstract trial-and-selection at the meta level
  (see section 2); the object-level policy is what is under test.

## 6. Conditions (argv[1] selects)

- scheduled: fixed researcher schedule per episode (control; supplied
  W4 extended to two slots): a0=selftest; wire(0); a1=selftest;
  if not (a1>a0) unwire(0); a2=selftest; wire(1); a3=selftest;
  if not (a3>a2) unwire(1). Episode score = final selftest.
- bandit: as in section 5; one atomic action per episode by argmax Q.
- construct: as in section 5; exhaustive policy search, retain best.
- nodriver: identical to construct, except retention is disabled: the
  first-evaluated policy (index 0) is retained regardless of score.
  Ablation showing measurement-driven retention is load-bearing.

## 7. Preregistered predictions (hand-derived; derivations in section 8)

- P1 scheduled: train episode scores [6,3,6,3], total 18/24; held-out
  scores [6,3], total 9/12. (Supplied W4 works; control.)
- P2 bandit: every episode takes action WIRE0 (index 0); train scores
  [6,0,6,0], total 12/24; final q_sums [12,0,0], q_counts [4,0,0];
  held-out scores [6,0], total 6/12. (Value learning converges to a
  context-blind habit: right on A/C episodes, wrong on B/D. It does NOT
  discover the conditional policy, because a bandit over atomic actions
  cannot represent "wire iff measured better".)
- P3 construct: retained policy index 381 = steps [EVAL, WIRE0, EVAL,
  IFB, UNWIRE0] (the clean single-slot try-and-keep: measure baseline,
  wire slot0, measure, keep iff better else revert); train scores
  [6,3,6,3], total 18/24; held-out scores [6,3], total 9/12, matching
  scheduled exactly.
- P4 nodriver: retained policy index 0 = [EVAL,EVAL,EVAL,EVAL,EVAL];
  train scores [3,3,3,3], total 12/24; held-out [3,3], total 6/12.
  (Without measurement-driven retention, no policy forms.)
- P5: 3 runs per condition byte-identical (sha256).

## 8. Derivation of P3 (policy 381; checkable by hand)

Unconditional policies (no differential IFB branching) do the same wiring
every episode. Final wiring W gives training total 2*scoreA(W) +
2*scoreB(W): W={} -> 6+6=12; W={0} -> 12+0=12; W={1} -> 0+6=6;
W={0,1} -> 6+0=6. Max 12. Any policy scoring above 12 must branch on
measurement via IFB, which requires an EVAL, a wiring change, then EVAL
(baseline R1=3 vs new R0), so IFB can see improvement.

Global max: A-pair <= 12 (EpA max 6), B-pair <= 6 (EpB max 3, via wiring
{} or {1}), so training total <= 18. Policy 381 = [EVAL, WIRE0, EVAL,
IFB, UNWIRE0]: on A, R goes (3,-1)->wire0->(6,3), IFB sees 6>3, skips
UNWIRE0, final {0} -> 6. On B, R goes (3,-1)->wire0->(0,3), IFB sees
0>3 false, executes UNWIRE0, final {} -> 3. Training total 18: optimal.

Minimality (no index < 381 scores 18): indices >= 2401 have step0 != EVAL;
indices 686..2400 have steps[0,1] = [EVAL, WIRE1..IDLE]. Case [EVAL, EVAL,
...] (d1=0): after two EVALs R0=R1=3 with no wiring, and EVAL without an
intervening wiring change cannot separate R0 from R1, so IFB can never
observe improvement: max 12. Case [EVAL, WIRE0, d2, d3, d4] with d2 !=
EVAL: no baseline/after pair exists, IFB either always skips (R0=3 > R1=-1)
or never skips: unconditional, max 12. Case [EVAL, WIRE0, EVAL, d3, d4]
with d3 < 5 (not IFB): d4=IFB is last (skips nothing); otherwise no
conditional: max 12. Case [EVAL, WIRE0, EVAL, IFB, d4], d4 in {0,1}:
d4=EVAL -> B ends wired {0} -> 0; d4=WIRE0 -> same; total 12.
d4=2 (index 380): on B, IFB executes WIRE1 (neutral no-op), final {0} ->
0; total 12. Hence no index below 381 reaches 18, and 381 is the first
optimal policy the search retains. Held-out: C -> (3,-1)->wire0->(6,3),
skip unwire, {0} -> 6. D -> (3,-1)->wire0->(0,3), unwire, {} -> 3.
Total 9/12.

Note the near-miss at index 380: under a training set where slot1 were
helpful on B episodes, the degenerate [EVAL,WIRE0,EVAL,IFB,WIRE1] would tie
at 18. Episode B uses the NEUTRAL hyp in slot1 precisely to break that
degeneracy, so only the principled revert (UNWIRE0) is optimal. This is a
deliberate anti-hack design choice, disclosed here.

## 9. Kill bar

LW2-COMPLETE iff P1, P2, P3, P4, P5 all hold.
- P1: supplied W4 works (control, replicates LW1 at two slots).
- P2: action-value learning alone does NOT invent W4 (valuable negative;
  characterizes the missing representational piece: conditionals).
- P3: generic policy search constructs try-and-keep (381), matching the
  supplied schedule on training and held-out.
- P4: measurement-driven retention is load-bearing (ablation).
- P5: determinism.

Frozen interpretation (section 2): P3 success = L2 construction, not L3
invention. The experiment decides whether W4 can be learner-constructed
from generic machinery and experience; the regress argument decides the
strong-sense question (answered negatively in principle, not by vote).

If P3 fails (search retains a non-try-and-keep policy or a degenerate
one), the verdict is LW2-INCOMPLETE with the retained policy analyzed as
the characterization of what generic search actually finds; sections 2
and 8 already constrain the interpretation.

## 10. Determinism and toolchain

Pure Zag. Zero RNG. All data sets literal. Search order fixed
(0..16806). 3/3 runs byte-identical required per condition. Safebin
toolchain guard recorded in NAMECHECK.md Step 0. No modes, no bridges, no
handlers added to any architecture; all conditions are measurement
configurations inside this standalone experiment. Single-buffer stdout
(one preallocated buffer, one raw syscall write); no _zag_print, per the
pinned-znc stdout lesson. Local allocator on _zag_malloc (this znc build
has no nio_alloc); u8 cells with little-endian helpers; no `as *i32`
slice construction inside functions.
