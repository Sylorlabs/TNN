# ATTACK_PROBEMENU.md - Probe-menu equivalence red-team attack on the F1 constructor

Lane F1, wave wave-20261002-0221pdt. Red-team attack per Criterion 0
C0-B (PREREG_F1.md section 4): construct the strongest adversarial
argument that the F1 mechanism's constructed behavior could be
reproduced by a probe-menu (finite researcher-enumerated answer
family). Either demonstrate the equivalence (killing evidence) or
fail loudly with the evidence that blocks it.

Standing: F1 v4 BUILD-FAILs, so there is no L3 claim to kill. This
attack is the promotion-path battery: any future F1 BUILD-PASS must
survive it. It is recorded here against the current mechanism.

No em-dashes are used in this document.

## 1. Attack target and declared families

Target: the F1 construction machinery (`trial_move` + `burst` in the
frozen lane source `impl/f1_learn_c.zag`; constructor logic identical
to the 2021pdt v4 and the 2321pdt windowed variant, only the trigger
differs, and the trigger is not the menu question). The families
below are declared from the frozen source alone (constructor code
structure: trial enumeration bounds, KB, MAXN), without reference to
any trace contents. The 2021pdt independent adversary's C0-B attack
(SEALED_C0.md, written before its sealed runs) provides the
independently pre-registered parity test for F-A on W2, cited in
section 3.

F-A (single-pick menu): all structures of the form [X; WRITE r0]
where X is one ISA node (op 1..7, operands in the frozen trial
ranges). Finite and enumerable from the source alone. Containment
claim to test: the final structure S is one argmin pick from this
menu.

F-B (bounded-burst menu): all structures reachable from the seed
within a single trigger burst (at most KB=4 construction events).
Containment claim to test: S is one single-burst output.

F-C (vacuous finite family): all graphs of at most MAXN=24 nodes
over the frozen ISA with the world's operand alphabet. Finite and
enumerable from source plus world signature. Containment is trivial.

## 2. Automatic-kill checks (no parity test needed; both checked)

Scan kill: FIRES iff the source contains a fixed-order scan over a
researcher-enumerated relation or candidate set whose result is
reified as structure. The trial scans ISA ops 1..7 (READ, WRITE,
COPY, ADD, EQ, BRANCH, EXECUTE): the frozen protected ISA, approved
generic machinery per the 2026-09-30 ISA ruling, not a
researcher-enumerated relation set (contrast the REPEXPAND {EQ, MUL,
ADD} pattern). DOES NOT FIRE.

Kit kill: FIRES iff the construction kit has a finite
researcher-shaped output set (all outputs instances of one
researcher-fixed shape). Trial outputs are arbitrary single ISA
nodes (any op, any operands in the frozen ranges), not one fixed
shape (contrast the PI_REV2 byte-equality-only kit). DOES NOT FIRE.

## 3. F-A parity attack (single-pick menu)

Parity requirement: one f in F-A with exact I/O parity with S on at
least 60 probes.

Test 1 (fresh sealed evidence, this lane): S_sF = the sF-trained
structure [EQ r0,f0,f1; ADD r0,r0,r0; WRITE r0] (2 constructed
nodes; sealed trace shows 2 episode-indexed construction events at
ep 9 driving buffer error 2->1->0). Probe pool: sF_hidden (30) +
sG_hidden (30) = 60 probes under S_sF's law (y = 2 iff x0==x1).

- S_sF scores: 30/30 on sF_hidden (sealed), 30/30 on sG_hidden
  (transfer run with the frozen sF-trained state). Total: 60/60.
- Best f in F-A: the 8 distinct single-node output functions (x0,
  x1, 0, 2x0, x0+x1, 2x1, eq01, one; BRANCH single-nodes reduce to
  predicting 0 or non-terminating, bounded above by the constant-0
  function) were scored with the pure-Zag probe1 on both truth
  sets. Best: 17/30 on sF_truth (constant 0 and eq01 tie), 15/30 on
  sG_truth. Total: 32/60.
- No f in F-A achieves parity. The gap is 28 probes.

Test 2 (independent pre-registered evidence, cited): the 2021pdt
adversary's single-node brute-force oracle enumerates exactly F-A
(the constructor's own candidate enumeration). On W2 (S_W2 = 3-node
[ADD r0,f0,f0; ADD r0,r0,f1; ADD r0,r0,f1; WRITE]): oracle 0/30 vs
learner 30/30 (SEALED_EVAL.md section 2, wave-20261001-2021pdt).
Parity fails.

F-A attack verdict: FAILS. The final structures are not one complete
pick from the single-node menu.

## 4. F-B parity attack (bounded-burst menu)

The attack fails at the protocol's step 1 (declaration). F-B is not
enumerable from the frozen source alone: each burst's output is the
argmin of measured buffer error over the learner's runtime
experience buffer (trial_move evaluates `buf_err_b` against bxs/bys,
the last up-to-8 truth episodes), and the buffer contents (the
actual x/y values driving selection) are not in the source. A
data-dependent "family" is not a researcher-enumerated family; the
containment argument cannot be made sound.

Even waiving the declaration defect: S_R1 (the R1 counterexample
structure [4 4 4 4 4 2], 6 nodes) was built in 5 construction events
across 2 trigger episodes (3 in the W2 burst, 2 in the R1 burst;
2021pdt SEALED_EVAL.md section 5). A single burst caps at KB=4
events, so S_R1 is not a single-burst output. The final structure is
a sequence of data-driven repair steps, not one burst pick.

F-B attack verdict: FAILS (declaration defect; bound exceeded by
sealed evidence).

## 5. F-C parity attack (vacuous finite family)

F-C trivially achieves parity: exhibit f = S itself. This is
post-hoc enumeration in substance (declaring "everything the
machine can output" is not a researcher-enumerated solution
family), and it would "kill" any incremental constructor including
a genuine L3 one. The C0-B protocol's positive-evidence clause
exists precisely to block vacuous-F attacks, and it holds here:

- Incremental construction: sF shows 2 episode-indexed events at
  the trigger episode; T-A shows 3 events across 2 trigger episodes
  (READ then EQ then ADD, with an honest stall between); R1 shows 5
  events across 2 trigger episodes; W2 shows 3; B2 shows the exact
  3-step signature [ADD 0,8,8], [ADD 0,0,0], [ADD 0,0,8].
- No textual counterpart: the sF node pattern (EQ with operands 8,
  9) has 0 occurrences in the frozen lane source (grep count 0);
  the W2 node pattern (4 0 8 8) has 0 occurrences in the 2021pdt
  source (independent adversary's check, cited).

F-C attack verdict: FAILS (vacuous; blocked by positive evidence).

## 6. Steelman rebuttals (strongest counterarguments considered)

(a) "Any deterministic mechanism's I/O on a fixed probe set can be
tabulated, so a lookup-table menu always reproduces the behavior."
Rebuttal: true of every computer program, including a genuine L3
learner. C0-B asks whether the final STRUCTURE was chosen as one
complete answer from a researcher-enumerated family, not whether
I/O is computable. The tabulation argument proves too much and is
blocked by the positive-evidence clause.

(b) "KB=4, MAXN=24, and the frozen operand ranges bound the output
space finitely; the mechanism selects from a finite
researcher-bounded family." Rebuttal: bounded is not enumerated.
The bounds are resource caps (like memory size), not a menu of
answers; the researcher never enumerated the family as the solution
space. Selection among reachable structures is by measured error on
the learner's experience buffer, whose contents are not in the
source.

(c) "The frozen scan order (ops 1..7, operand nesting) is a
researcher-fixed rank; per the PI_REV2 S4 lesson, a fixed rank over
a finite set is menu selection at one remove." Rebuttal: the scan
order only breaks ties among equal-error minimizers; the primary
rank is the learner's own measured prediction error on its own
experience (trial_move keeps the candidate with strictly smaller
buffer error). In PI_REV2 S4 the rank selected independently of the
learner's error signal and matched the tester's intent; here the
rank IS the learning signal. The B2 signature discriminates
empirically: the scan-order-dependent intermediate 4x-via-r0+r0 step
exists only because operand 0 precedes 8 in scan order interacting
with error minimization; a relation menu would predict the direct
5x pick, not the intermediate (2021pdt SEALED_EVAL.md section 2).

## 7. Attack verdict: FAILS LOUDLY

No declared finite family reproduces the F1 constructor's sealed
structures with exact parity; both automatic kills do not fire; the
positive incremental-construction evidence holds. The evidence
blocking the attack, with cited numbers:

1. F-A parity fails on fresh sealed evidence: best single-node f
   32/60 vs S_sF 60/60 (gap: 28 probes).
2. F-A parity fails on independent pre-registered evidence: oracle
   0/30 vs learner 30/30 on W2.
3. F-B is not declarable from source alone (data-dependent burst
   outputs); R1's 5-event structure exceeds the 4-event
   single-burst bound.
4. F-C is vacuous and blocked by positive evidence: 2+ incremental
   events per structure (sF 2, T-A 3 across 2 triggers, R1 5 across
   2 triggers, W2 3, B2 3-step scan-order signature) and
   grep-absent node patterns (0 hits).
5. The selection rank is the learner's measured error on its own
   experience buffer, not a researcher-imposed answer key; the scan
   order only breaks ties.

The F1 constructor is not menu selection. This attack does not
promote the mechanism: the F1 BUILD-FAIL stands, the bounded L2+
ceiling stands, and the rW2 constructor limitation (greedy depth-1
trial overfit) is untouched by this analysis.

Evidence paths: dev/probe1.zag and dev/probe1 (single-node scorer);
sealed6/sF_train.ep, sF_hidden.ep, sF_truth.ep, sG_hidden.ep,
sG_truth.ep (fresh sealed); runs6/1/sF_train.trace,
runs6/1/sF_train.state (S_sF evidence); /tmp/atk_sg.* (attack
transfer run, non-sealed analysis).

No em-dashes are used in this document.
