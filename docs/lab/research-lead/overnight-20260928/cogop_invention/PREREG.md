# PREREG: COGOP-INVENTION (Cognitive Operation Invention Worker)

Frozen: 2026-10-02. This file is committed ALONE before any implementation
source exists. Commit-order self-check is recorded in NAMECHECK.md.

## 1. Mission

From C281: the learner created intermediate M=[INC R0], a generator
program. That was a BODY (a sequence of ops), not a new OPERATION.
This lane tests whether the learner can invent a genuinely NEW operation:
a new primitive with novel semantics, defined by the learner, implemented
from the frozen basis, persisted in learner state, and reused as a
primitive by later invention. It must NOT be a macro for existing ops,
and it must enable something previously impossible.

Target verdict: COGOP-INVENTION-COMPLETE (with novelty analysis).

## 2. Frozen basis (protected core; researcher-written, task-independent)

The interpreter implements exactly six instruction forms over eight i64
registers R0..R7. Task convention: inputs in R0,R1; result read from R0;
all registers zeroed before each run.

- MOVE d, s      : R[d] = R[s]            (op=1, okind 0)
- MOVE d, #i     : R[d] = i               (op=1, okind 1, i in 0..3 for synthesis)
- INC r          : R[r] = R[r] + 1        (op=2)
- DEC r          : R[r] = R[r] - 1        (op=3)
- BEQ r1, op2, T : if R[r1]==val(op2) pc=T else pc=pc+1   (op=4)
- CALL h         : invoke inventory op h (args R0,R1; all regs saved/restored,
                   R0=result on return; depth cap 16, fail-closed)   (op=5)
- RET            : return R0              (op=6)

MOVE/INC/DEC/BEQ are the frozen 4-op ISA. CALL is this experiment's
realization of the already-proposed EXECUTE(root, frame) invocation
machinery: generic, task-independent, frozen. No new protected op is
added by this lane. In particular MUL is NOT added to the core; per the
PROTECTED CORE ISA RULING the test is whether the learner constructs
and persists MUL from the generic basis in LEARNER STATE.

Step cap 20000 per run; any violation (unknown op, negative loop
counter, cap exceeded, R6 clobbered) fails closed. No RNG anywhere.

## 3. Learner machinery (generic; no task-specific structure)

The learner has three parts, all task-independent:

(a) PLANNER: exhaustive search over branch-free straight-line bodies
    (lengths 1..3) over the current inventory instructions
    (basis ops with regs R0..R3 and immediates 0..3, plus CALL h for
    each promoted op). Fixed enumeration order. Reports tried/found.

(b) CONSTRUCTOR: systematic trial over the generic REPEAT form:
      prologue P in {P0..P5} x step S (flat body, length 1..2, over
      current inventory) x kreg K in {R0..R5},
    compiled to:
      P ; MOVE R5,R[K] ; L: BEQ R5,#0,END ; S ; DEC R5 ;
         BEQ R6,#0,L ; END: RET
    with R6 hard zero (synthesis never writes R5/R6/R7).
    Prologues (generic frame setup: save inputs x accumulator init):
      P0=[]  P1=[MOVE R0 #0]  P2=[MOVE R0 #1]
      P3=[MOVE R3 R0; MOVE R4 R1]
      P4=[P3; MOVE R0 #0]  P5=[P3; MOVE R0 #1]
    First candidate passing ALL training pairs is verified on held-out
    probes, then promoted. The specific step content is discovered by
    trial; it is not written by the researcher.

(c) PROMOTER: on train+probe success, appends the compiled graph to the
    persistent op inventory with a contract {name, arity 2, domain,
    found prologue/step/kreg, train n/n, probe n/n}. Later stages may
    use CALL h to a promoted op as an ATOMIC instruction; the
    constructor never inspects a promoted op's graph (opaque reuse).

## 4. Stages (tasks where the current op set is insufficient)

Stage 1: invent OP_ADD. Vocabulary: {MOVE,INC,DEC}. Domain N^2.
  Train (10): (0,0)->0 (0,1)->1 (1,0)->1 (2,3)->5 (5,7)->12 (8,8)->16
              (13,4)->17 (16,16)->32 (11,2)->13 (6,15)->21
  Probes (6): (3,9)->12 (10,10)->20 (15,1)->16 (4,12)->16 (9,6)->15
              (14,14)->28

Stage 2: invent OP_MUL. Vocabulary: {MOVE,INC,DEC,CALL OP_ADD}.
  Train (10): (0,0)->0 (0,7)->0 (1,9)->9 (2,3)->6 (3,4)->12 (5,5)->25
              (6,7)->42 (10,10)->100 (12,8)->96 (16,16)->256
  Probes (6): (2,9)->18 (4,6)->24 (7,7)->49 (9,11)->99 (13,13)->169
              (15,3)->45

Stage 3: invent OP_POW (a^b, 0^0=1). Vocabulary:
  {MOVE,INC,DEC,CALL OP_ADD,CALL OP_MUL}. Domain N^2 (verified on grid).
  Train (10): (0,0)->1 (0,1)->0 (0,3)->0 (1,4)->1 (2,3)->8 (3,2)->9
              (4,2)->16 (2,4)->16 (3,3)->27 (4,4)->256
  Probes (6): (1,0)->1 (2,0)->1 (2,2)->4 (3,1)->3 (4,3)->64 (0,2)->0

Pair outputs are computed by the driver (world_add/world_mul/world_pow);
learner functions receive only pair arrays and never call world_*.

## 5. Impossibility proofs (preregistered; the "not a macro" test)

A macro for existing ops = a fixed finite branch-free straight-line
expansion over the pre-invention vocabulary, behaviorally equivalent
on the whole domain. The planner emits exactly such bodies.

T1 (stage 1): No straight-line body over {MOVE,INC,DEC} computes ADD on
  any domain containing (0,0),(0,1),(1,0). Proof: by induction every
  register always holds (input_i + c) or (constant c) for body-fixed
  i,c. So R0_out is a+c0, b+c1, or c2. (0,0) and (0,1): not a+c0
  (0 vs 1 with same a); not b+c1; not const. The other cases are
  symmetric. Hence no flat body, of ANY length, computes ADD.

T2 (stage 2): No straight-line body over {MOVE,INC,DEC,CALL OP_ADD}
  computes MUL on N^2. Proof: CALL OP_ADD maps (R0,R1)->R0+R1, so by
  induction R0_out = a*a0 + b*b0 + g (fixed integers). (0,0)->0 gives
  g=0; (1,0)->0 gives a0=0; (0,1)->0 gives b0=0; then (2,3)->6 gives
  0=6, contradiction.

T3 (stage 3): No straight-line body over {MOVE,INC,DEC,CALL OP_ADD,
  CALL OP_MUL} computes POW on N^2. Proof: the body computes a fixed
  polynomial P(a,b) (MUL of polynomials is polynomial). Fix a=2:
  Q(b)=P(2,b) is a univariate polynomial with Q(b)=2^b for all b in N.
  R(b)=Q(b+1)-2Q(b) has infinitely many integer roots, so R is the zero
  polynomial; comparing leading coefficients (c vs 2c) forces c=0, so
  Q is zero, contradicting Q(0)=1.

Consequence: the invented ops cannot be macro-expanded into the
pre-invention vocabulary uniformly. Their execution uses
input-dependent iteration, which no flat body replicates. This is the
rigorous sense in which they are genuinely new operations relative to
the learner's pre-invention cognitive vocabulary.

## 6. Novelty criteria (preregistered)

N1 learner-defined semantics: the step content of each op is found by
   the constructor's systematic trial, not written by the researcher.
   Source check: constructor code contains no task answers.
N2 not a macro: T1..T3 prove no fixed flat expansion over the
   pre-invention vocabulary is uniformly equivalent.
N3 enabling: each stage's task class is provably unsolvable by the
   planner alone (T1..T3) and becomes solved after promotion.
N4 opaque reuse: stage 2's found step must contain CALL OP_ADD; stage
   3's found step must contain CALL OP_MUL; the constructor treats
   promoted ops atomically.
N5 ablation: stage-2 invention with OP_ADD removed from the inventory
   must FAIL; stage-3 invention with OP_MUL removed must FAIL.
N6 persistence and use: each op persists in the inventory with a
   contract and is used by the planner as a single-instruction body
   ([CALL h] solves all training pairs) and by the next stage's
   construction.

Honest limit (stated now, analyzed in REPORT): the 4-op basis is
Turing-complete in the idealization, so the invented ops add no
computability-theoretic power. The novelty is cognitive: named,
contracted, reusable operations compressing input-dependent iteration
into the learner's bounded plan vocabulary, each becoming the next
invention's primitive.

## 7. Kill bars and predictions

K-COGOP-1 prereg order: this file committed alone before any
  implementation file exists (self-check in NAMECHECK.md).
K-COGOP-2 frozen basis: interpreter implements exactly the six forms
  of section 2; source has zero task-specific structure in learner
  code; zero occurrences of mode/bridge/handler; zero `as *i32`;
  zero _zag_print; zero python.
K-COGOP-3 stage predictions:
  P1 planner baselines fail: 0 bodies of length <=3 pass all training
     pairs at every stage (stage1 tried=65640, stage2 tried=70643,
     stage3 tried=75894).
  P2 stage 1 invents OP_ADD: 10/10 train, 6/6 probes; promoted with
     contract; expected discovery (P0,[INC R0],R1).
  P3 stage 2 invents OP_MUL: 10/10 train, 6/6 probes; found step
     contains CALL OP_ADD (handle 0); expected (P4,[MOVE R1 R3;
     CALL OP_ADD],R1).
  P4 stage 3 invents OP_POW: 10/10 train, 6/6 probes; found step
     contains CALL OP_MUL (handle 1); expected (P5,[MOVE R1 R3;
     CALL OP_MUL],R1).
  P5 ablation A: stage-2 constructor with OP_ADD removed reports
     INVENTION-FAIL (0 candidates pass).
  P6 ablation B: stage-3 constructor with OP_MUL removed reports
     INVENTION-FAIL.
  P7 grid validation: OP_ADD 289/289 on [0,16]^2; OP_MUL 289/289 on
     [0,16]^2; OP_POW 25/25 on [0,4]^2.
  P8 determinism: 3 runs byte-identical (sha256 equal).
  P9 post-invention planner: single-instruction bodies [CALL OP_ADD],
     [CALL OP_MUL], [CALL OP_POW] solve 10/10 training pairs.
K-COGOP-4 novelty analysis: REPORT contains T1..T3, the N1..N6
  analysis, and the honest computability limit.

Verdict COGOP-INVENTION-COMPLETE iff K-COGOP-1..4 all pass.

## 8. Determinism and toolchain

Pure Zag. No RNG. Fixed enumeration orders. Binary run 3x;
sha256sums recorded; cmp byte-equality required. Safebin toolchain
guard per governance (Step 0 in NAMECHECK.md).

## 9. Deliverables

In docs/lab/research-lead/overnight-20260928/cogop_invention/:
PREREG.md (this file, frozen first), NAMECHECK.md, REPORT.md,
cogop.zag, build.sh, compile.txt, run1.txt, run2.txt, run3.txt,
sha256sums.txt, cogop_bin. Commits use explicit pathspecs; nothing
is pushed.
