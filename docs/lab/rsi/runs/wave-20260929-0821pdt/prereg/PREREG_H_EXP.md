# PREREG H-EXP: discriminating-experiment invention (NQ3)

Wave: wave-20260929-0821pdt. Candidate class: new capability (fourth
innovation frontier: new experiment). Addresses Micah's Level D
(self-directed evidence) and NQ3 from the 2026-09-29 07:56 PDT canonical
state: "Can the learner invent discriminating experiments?" No mechanism
has attempted it.

## What changes

A new pure-Zag module, exp_learn.zag, owned by this wave (no existing
subsystem is modified, so zero regression surface on frontier files).
Given TWO competing hypotheses supplied as input DATA files (parsed at
runtime, never compiled in), the module:

1. Parses both hypothesis files into rule sets.
2. Enumerates candidate action sequences of length 1..3 over the fixed
   action vocabulary A = {0:heat, 1:cool, 2:pressurize, 3:depressurize,
   4:lamp_on, 5:lamp_off} (6 + 36 + 216 = 258 sequences).
3. Simulates each sequence from the shared INIT state under both
   hypotheses with a generic rule evaluator (first matching rule fires;
   no match means no-op).
4. Selects the shortest, lexicographically-first (by action id) sequence
   whose predicted final states differ between the hypotheses in at
   least one state variable.
5. Emits an inspectable trace: hypothesis names, rules parsed, candidate
   counts, the first discriminator found, per-hypothesis predicted
   final states, the differing variable(s), and the selection.
6. If no candidate discriminates within the length bound, emits an
   exact WITHHOLD line and selects nothing.

## Hypothesis data format (frozen here)

```
HYP <name>
INIT <t> <p> <l>
RULE <a> <v1> <op1> <x1> <v2> <op2> <x2> <sv> <sx>
...
```

a: action id 0..5. v: state var 0=t,1=p,2=l. op: 0==,1!=,2<,3<=,4>,5>=.
v2=-1 means the second condition is vacuous (single-condition rule).
Effect: set var sv to absolute value sx. Rules are ordered; for an
action the FIRST rule whose condition(s) hold fires. Lines starting
with # are comments. The three hypothesis-pair files are frozen with
this prereg (committed in the prereg commit), so the pair contents
cannot be tuned after seeing implementation behavior.

## Frozen hypothesis pairs (committed with this prereg)

Pair P1 (real, prereg/hyp_p1_a.txt vs prereg/hyp_p1_b.txt):
- H1a "lamp-block": pressurize sets p:=1 unless lamp==1 (blocked).
- H2a "temp-block": pressurize sets p:=1 unless temp==2 (safety valve).
- Shared: INIT 0 0 0; heat/cool/depressurize/lamp_on/lamp_off are
  identical in both files.
- Preregistered expected outcome: the unique shortest discriminating
  sequence is [4,2] (lamp_on, pressurize). Length-1 sequences all
  predict identically (verified by hand in the prereg analysis below);
  [4,2] yields pressure 0 under H1a vs 1 under H2a. No other length-2
  sequence discriminates (lamp_on changes only l identically; other
  length-2 pairs leave p predictions equal).

Pair P2 (null, prereg/hyp_p2_a.txt vs prereg/hyp_p2_b.txt):
- H1b vs H2b differ only in rules whose conditions can never hold
  (temp==9, temp==-1; temp is bounded 0..2), so all 258 sequences
  predict identically.
- Preregistered expected outcome: exact WITHHOLD output, no sequence
  selected, exit 0.

Pair P3 (generalization, prereg/hyp_p3_a.txt vs prereg/hyp_p3_b.txt):
- H1c "cold-enables-lamp": lamp_on sets l:=1 only when temp==0.
- H2c "lamp-always": lamp_on always sets l:=1.
- Shared: INIT 0 0 0; all other actions identical in both files.
- Preregistered expected outcome: the unique shortest discriminating
  sequence is [0,4] (heat, lamp_on): after heat temp=1, lamp_on yields
  l=0 under H1c vs l=1 under H2c. Length-1 sequences predict
  identically.

## Frozen kill bars (must ALL pass; bars never move after this commit)

- K-E1 (P1 real pair): stdout contains the selected sequence [4,2] as
  the FIRST selection, and the trace names both hypotheses (lamp-block,
  temp-block) and states that the differing variable is pressure.
- K-E2 (trace inspectability): the P1 trace prints, in order, both
  hypothesis names, the number of rules parsed per hypothesis, the
  number of candidates evaluated per length, the count of sequences
  checked before the first discriminator, and the per-hypothesis
  predicted final states for the selected sequence.
- K-E3 (P2 null): stdout contains the exact line
  "WITHHOLD: no discriminating experiment within length<=3" and does
  NOT contain any "SELECT" line; exit code 0.
- K-E4 (determinism): two runs on P1 are byte-identical (cmp); two runs
  on P3 are byte-identical (cmp).
- K-E5 (generalization, anti-hardcoding): on P3 the module selects
  [0,4] (heat, lamp_on) and the trace names both hypotheses
  (cold-enables-lamp, lamp-always). Passing K-E5 with K-E1 proves the
  selection is driven by the input hypothesis DATA, not by constants
  for the P1 pair, because P3 uses different rule contents and a
  different discriminator.

## Predicted honest boundaries (declared before implementation)

- The action vocabulary A (6 actions), the length bound 3, and the
  state space (t,p,l) are authored. The hypothesis PAIRS are authored
  data. What is NOT authored: the selection outcome for any pair.
- The mechanism is enumerate-and-select, not constructive invention
  (same family as procedure v1). It does not generate new actions,
  does not represent uncertainty quantitatively, and does not plan
  beyond the bound.
- Honest classification target on PASS: bounded structural selection
  toward Level D; explicitly NOT L3 (fails criterion 12 family: no
  revision; hypotheses are supplied, not discovered).
- The true-world execution step (running the selected experiment
  against a hidden law and refuting a hypothesis) is OUT OF SCOPE for
  this wave; the selection plus trace is the frozen claim. The
  execution step is queued as H-EXP2.

## Cost

One new .zag file (estimated 250-400 lines), three hypothesis-pair
fixture files (frozen here), one shell run script (evidence only, runs
the compiled binaries, no analysis logic). Zero Python. Test runs:
6 executions total (P1 x2, P2 x1, P3 x2, plus one extra P1 under a
renamed copy of the pair files to check filename independence).

## Red-team attack plan (pre-registered)

- Hardcoding: grep the implementation for the action sequences 4,2 and
  0,4 and for the hypothesis names; any match outside string printing
  of parsed data is a KILL.
- Try-everything heuristic: K-E3 (null withhold) plus a fourth pair
  with TWO discriminators at different lengths would catch
  longest-first bias; the length-major ordering is asserted in the
  trace by the checked-count field (K-E2).
- Data-drivenness: K-E5 plus the renamed-copy run.
- Byte determinism: K-E4.
- Scope honesty: the verdict must carry the boundary list above; any
  verdict claiming L3 or "genuine invention" is void.
