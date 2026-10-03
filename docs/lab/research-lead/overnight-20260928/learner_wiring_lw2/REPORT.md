# REPORT: LW2 Learner Invention of the Try-and-Keep Policy (W4)

Verdict: LW2-COMPLETE (with policy-invention analysis, section 5).
Date: 2026-10-02. Worker: Learner Policy Invention Worker (subagent).
Prereg: PREREG.md, frozen and committed (bf523af0b) before implementation.

## 1. Question

LW1 (C289) showed the learner can self-wire given W1 (writable path), W2
(self-evaluation), W3 (write action), and W4 (try-and-keep policy), but W4
was researcher-authored: a fixed schedule of [selftest, wire, selftest,
keep iff better]. The open gap: can the learner INVENT W4 itself, rather
than running a supplied schedule? This experiment tests two candidate
discovery mechanisms (a value-learning bandit over atomic actions, and
generic policy search over a conditional policy space), against a
scheduled control and a no-driver ablation. All predictions were
hand-derived and frozen before implementation.

## 2. Design (summary; full detail in PREREG.md)

Same world as LW1 (length-4 strings over {0,1,2,3}; hidden rule R = all
symbols distinct; same literal TRAIN/VALID). Two hypothesis slots per
episode: helpful H_help = MAXCOUNT(1) acquired by Occam (6/6 on VALID),
harmful H_harm = ALLDISTINCT-NOT (reject iff all distinct; 0/6 on VALID),
neutral H_neut = MAXCOUNT(3) (never rejects on VALID; wiring is a no-op).
Four episode types, learner never told the type: A = (helpful, harmful),
B = (harmful, neutral), C held-out = (helpful, helpful), D held-out =
(harmful, harmful). Training order fixed: A, B, A, B. Per-episode optima:
A=6, B=3, C=6, D=3. A blind "always wire slot0" habit scores 18/36
equivalent here (12/24 train, 6/12 held-out): only measurement-conditioned
wiring succeeds on both A and B.

Four conditions, argv-selected, zero RNG, all data literal:
- scheduled: fixed try-measure-keep schedule over both slots (control).
- bandit: persistent Q over {WIRE0, WIRE1, IDLE}, argmax per episode,
  updated from the learner's own episode scores (LW1 section 9 test).
- construct: exhaustive search over all 7^5 = 16807 five-step policies
  (alphabet: EVAL, WIRE0, WIRE1, UNWIRE0, UNWIRE1, IFB, IDLE; IFB = skip
  next step iff not (R0>R1)), scored by the learner's own selftest on
  training episodes; retain the best (ties: lowest index); freeze and run
  on held-out C, D.
- nodriver: same as construct, retention disabled (policy index 0 kept).

## 3. Results: predictions vs observed (all 12 runs)

| cond      | predicted | observed | match |
|-----------|-----------|----------|-------|
| scheduled | train 6,3,6,3=18/24; heldout 6,3=9/12 | identical | P1 HOLD |
| bandit    | actions 0,0,0,0; train 6,0,6,0=12/24; q_sums 12,0,0; q_counts 4,0,0; heldout 6,0=6/12 | identical | P2 HOLD |
| construct | policy 381=[EVAL,WIRE0,EVAL,IFB,UNWIRE0]; train 6,3,6,3=18/24; heldout 6,3=9/12 | identical | P3 HOLD |
| nodriver  | policy 0=[EVAL x5]; train 3,3,3,3=12/24; heldout 3,3=6/12 | identical | P4 HOLD |

P5: 3 runs per condition byte-identical (sha256; see sha256sums.txt,
plus pairwise cmp). HOLD.

Raw outputs (run1 of each; runs 2 and 3 identical):

scheduled: hyp_param=1; train 6,3,6,3=18/24; heldout 6,3=9/12
bandit:    hyp_param=1; train 6,0,6,0=12/24; actions 0,0,0,0;
           q_sums 12,0,0; q_counts 4,0,0; heldout 6,0=6/12
construct: hyp_param=1; train 6,3,6,3=18/24; policy_index 381;
           policy_steps 0,1,0,5,3; heldout 6,3=9/12
nodriver:  hyp_param=1; train 3,3,3,3=12/24; policy_index 0;
           policy_steps 0,0,0,0,0; heldout 3,3=6/12

Kill bar (P1-P5 all hold): MET. Verdict: LW2-COMPLETE.

## 4. What the numbers establish

a) Supplied W4 works (P1). The scheduled control reaches 18/24 training
   and 9/12 held-out, replicating LW1's closure of the C283 gap at two
   slots. This is the ceiling the discovery mechanisms are measured
   against.

b) Value learning alone does NOT invent W4 (P2; the valuable negative).
   The bandit converged to always-WIRE0 from episode 1 onward (final
   Q sums [12,0,0], counts [4,0,0]; WIRE1 and IDLE never tried after the
   initial tie). It learned a context-blind habit: correct on A/C
   episodes, wrong on B/D. The failure is representational, not a lack of
   exploration: a bandit over atomic actions cannot express "wire iff
   measured better", because the conditional (measure, compare, branch) is
   not in its action space. Exploration would only oscillate between blind
   habits. What is missing for W4-discovery via value learning is a policy
   space with measurement-conditioned branching.

c) Generic policy search constructs try-and-keep (P3). The exhaustive
   driver, knowing nothing about paths, slots, or try-and-keep, and
   scoring policies solely by the learner's own selftest measurements,
   retained policy 381 = [EVAL, WIRE0, EVAL, IFB, UNWIRE0]: measure
   baseline, wire slot0, measure, keep iff better else revert. That is the
   clean single-slot try-and-keep loop, and it was not written by the
   researcher: the alphabet contained only atomic actions plus one generic
   conditional, and no try-measure-keep template existed anywhere in the
   driver. It matches the supplied schedule exactly (18/24 train, 9/12
   held-out), including generalization to the held-out wirings C and D.

d) Measurement-driven retention is load-bearing (P4). With retention
   disabled, policy 0 ([EVAL x5], no wiring ever) is kept: 12/24, 6/12.
   Trying candidates without keeping measured winners produces nothing.

e) The anti-hack design worked as intended. Policy 380 =
   [EVAL,WIRE0,EVAL,IFB,WIRE1] (measure, wire slot0, and if not better,
   wire slot1 instead of reverting) is a degenerate exploiter that would
   tie at 18/24 if slot1 were helpful on B episodes. Because episode B
   puts the NEUTRAL hyp in slot1, policy 380 scores only 12/24, so the
   search could not settle for the exploit; the optimum it found (381) is
   the principled revert. The hand-derivation in PREREG section 8
   (minimality of 381) was confirmed empirically to the exact index.

## 5. Policy-invention analysis

This is the deliverable the parent asked for: did the learner invent W4,
or did it fail without the supplied schedule? The honest answer has three
parts, all frozen in the prereg before results.

### 5.1 What construct demonstrates: L2 construction, not L3 invention

Policy 381 is genuinely learner-constructed at the object level: the
specific 5-step try-and-keep procedure for path wiring was produced from
the learner's own measurements by generic machinery, with no fixed
schedule and no researcher-encoded try-measure-keep template. Under the
learning-evidence taxonomy this is L2 structural learning (constructing a
new procedure from generic mechanisms), and it is a real result: the
learner now owns a path-wiring policy it was not given.

It is NOT L3 representational invention, for two preregistered reasons.
First, the policy space is a finite researcher-defined family (7^5
policies over a 7-action alphabet); selecting #381 from it is menu
selection, which the L3 bar (C0-B) explicitly excludes. Second, the
meta-driver (enumerate candidates, keep the best by measured score) is
itself an instance of the abstract try-and-keep form: trial,
measurement, retention of the better. The learner did not invent
trial-and-selection; it instantiated the researcher's meta-level
trial-and-selection at the object level (path wiring).

### 5.2 The invention regress (preregistered theoretical claim)

In any finite learner program, the topmost driver is fixed researcher
code. If that driver yields goal-directed policy construction, it
embodies trial-and-selection, which is the abstract form of W4 itself.
Therefore strong-sense invention of W4, with no trial-and-selection
machinery at any level, is incoherent as an experimental target: W4's
abstract form is the fixed point of the invention regress, coextensive
with goal-directed learning itself. You cannot have a learner that
pursues objectives without trial-and-selection somewhere in its
machinery, and try-and-keep IS trial-and-selection applied to
self-modification.

Consequence: the question "can the learner invent W4 ex nihilo" is the
wrong question. The coherent question, which this experiment answers, is
whether a generic trial-and-selection substrate can be specialized by
experience to a new domain (here: the learner's own path), producing a
concrete policy the researcher did not write. Answer: yes, given a
conditional policy space (construct); no, given only atomic action values
(bandit).

### 5.3 What is missing, precisely

For W4-discovery, the experiments isolate two distinct missing pieces:
(i) Without a conditional policy space, value learning learns habits, not
policies (P2). The representational prerequisite is measurement-conditioned
branching (EVAL, compare, IFB), not more exploration or better credit
assignment. (ii) Even with the space, the driver that finds the policy is
necessarily trial-and-selection at the meta level (regress, section 5.2);
there is no level at which "the idea of trying and keeping" appears
without being embodied in machinery. The research frontier is therefore
not ex-nihilo invention of the loop form, but: revision of a constructed
policy after counterexamples, transfer of the try-keep pattern to new
domains, and open-ended policy forms where the space itself is
learner-extended. Those are L2/L3 directions; chasing strong-sense W4
invention is chasing the fixed point.

## 6. Architecture accounting

- New modes: 0. New bridges: 0. New handlers: 0.
- Standalone experiment; nothing merged into any shared substrate.
  Cognition lines added to protected core or learner: 0.
- Researcher-authored generic machinery (disclosed): consultation list,
  selftest, wire/unwire_h, hyp kinds (MAXCOUNT, ALLDISTINCT-NOT), Occam
  selection, the 7-action policy alphabet, IFB/EVAL semantics, the bandit
  update rule, the exhaustive search driver. All domain-neutral; none
  encodes try-and-keep as a template or schedule.
- Learner-produced state: hyp record (kind=1,param=1) via Occam, bandit
  Q-table ([12,0,0]/[4,0,0]), retained policy 381 (produced by the generic
  driver from the learner's measurements; the 5-step sequence itself was
  not researcher-written).

## 7. Toolchain and determinism

- Safebin guard (NAMECHECK.md Step 0): PASS. python3/python unresolvable
  under worker PATH; znc 2026.07.0-dev used for the build.
- Pure Zag, zero RNG, zero Python in build, run, or analysis.
- 12 runs total; 4 distinct stdout byte strings; sha256 identical within
  each condition triple (sha256sums.txt) plus pairwise cmp.
- Stdout via single preallocated buffer + one raw syscall write; every
  binary's stdout bytes verified against the preregistered predictions
  before any claim was trusted. No _zag_print used.
- Construct search cost: 16807 policies x 4 episodes, all deterministic;
  native binary completes in well under a second.

## 8. Deliverables

- PREREG.md (frozen pre-implementation, committed bf523af0b), NAMECHECK.md
- lw2.zag (source), build.sh, compile.log
- lw2_bin (built binary)
- runs/{scheduled,bandit,construct,nodriver}_run{1,2,3}.txt (12 outputs)
- sha256sums.txt
- REPORT.md (this file)

All under docs/lab/research-lead/overnight-20260928/learner_wiring_lw2/.
Committed locally with explicit pathspecs. Nothing pushed (standing red
line). Paper untouched.

## 9. Recommended follow-up

LW3 (policy revision and transfer, the coherent next targets per section
5.3): (a) after the learner constructs policy 381, change the world
mid-stream (swap which slot is helpful; then require wiring BOTH slots
for full score, which needs a longer policy) and test whether the learner
revises the constructed policy from counterexample experience rather than
needing a fresh exhaustive search; (b) test whether the try-keep pattern
transfers to a new domain (a different action space and measurement),
i.e., does the learner reuse the abstract pattern or rediscover it from
scratch. Both keep the preregistered interpretation: construction and
revision are L2; the regress still rules out strong-sense invention, so
frame claims accordingly and do not re-litigate the fixed point.
