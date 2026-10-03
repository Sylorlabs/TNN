# REPORT: Parsimony Pressure on Learner-Created Operation Bodies

**Verdict: PARSIMONY-COMPLETE** (K1-K10 all PASS).
Prereg `dd19bcad60dba01d2b9c3088b05e46e2fd79774f` strictly precedes
implementation. 3/3 byte-identical, sha256
`2b1ca5347319446119bd9654a712284b3324f3cb28c297910f44e59dcc0aa9fe`.

## Question

LB1's honest finding: the learner creates working, revisable bodies
(11 instructions) but loses to the researcher-authored 6-instruction
minimal form on efficiency. It grafted the full gather scaffold --
dead trailing code and a never-firing match guard -- rather than
discovering the minimal straight-line form. Creation, not
optimization. This lane adds parsimony pressure: prefer shorter
bodies when success rates are equal. Preregistered questions: (1)
can the learner discover the minimal 6-instruction form through
parsimony pressure? (2) does parsimony pressure interfere with
revisability? (3) what is the tradeoff between parsimony and
revision speed?

## What was built

`pp.zag` (~1450 lines, pure Zag, pinned znc): lb.zag plus two
researcher-authored generic parsimony components (all selection
outcomes and every body byte remain learner-owned):

- **P1. Composite fitness**: `fit(b) = replay(b) - PLEN*len(b)`,
  PLEN=3 (hand-derived, preregistered: max length swing 3*15=45 is
  below the smallest graded-tier gap 50, so pressure can never trade
  a working body for a shorter broken one). Replaces raw-score
  comparison in tournament parent selection, elitist worst-member
  detection, offspring displacement, and best-body selection.
  Adopt bars stay on RAW replay (>=850).
- **P2. Greedy compression**: after CONSTRUCT-ADOPT and
  REVISE-ADOPT, up to 3 passes deleting each instruction whose
  removal does not decrease raw replay on the target ring. The
  compressed body replaces the adopted body (origin unchanged),
  fresh appl evaluation. Every strict decrease logs COMPRESS-DEL.
- **Parsimony refinement** (part of P1): the evolutionary loop runs
  up to 10 generations past the first raw passer (>=850) instead of
  stopping, so selection pressure can discover shorter passers
  (capped by maxgen; the trial cost is measured).

Three arms, one binary, env RNG reseeded per arm (identical worlds);
all use the LB1-treat policy path (seeded + reinforce + graft) and
differ ONLY in parsimony mode:
- arm 0 = P-FULL: P1 + refinement + P2 compression.
- arm 1 = P-SEL: P1 + refinement, NO compression (attribution arm).
- arm 2 = NP: LB1-exact selection (no P1/P2, old early stop).
  In-binary replication of LB1 arm 0.

Law change at ep 400 (N3 etype 5->6) in all arms. Revision trigger
unchanged (installed raw replay <400). No invention mode, 0
modes/bridges/handlers/semantic cases, opcodes exactly 1..8.

## Results

**Q1: YES -- the learner discovered the exact minimal 6-instruction
form.** P-FULL's final body (white-box disassembly):
```
SET R0,6 / MATCH R7,R0->R1 / SET R4,1 / READF R1,R4->R5 /
SET R6,2 / YIELD R6,R5
```
byte-identical to the researcher's hand-authored minimal body except
the etype immediate (6 vs 5) -- which is CORRECT for the post-shift
world (the frozen hand body with imm=5 scores 100 post-shift).
COMPRESS-DONE from=9 to=6 at replay 1000 (create), and from=10 to=6
at replay 1000 (revise). 7 strict-decrease COMPRESS-DEL events total.

Attribution (preregistered):
- P1 alone (P-SEL): 11 -> 9 instructions at create (the
  evolutionary delete operator + composite fitness removed dead
  code, including the JNZ guard, before any compression ran).
- P2 (compression): 9 -> 6 at create, 10 -> 6 at revise.
- Selection pressure contributes modest shortening; compression
  does the decisive minimization to the minimal form.

**Q2: NO interference -- revisability preserved and the
revisability advantage over the frozen hand body is intact.**
P-FULL: REVISE-ADOPT trials=188 best=1000 len=6 (compressed),
post-shift late N3 22/23, FINAL-POST replay 1000 vs hand_post=100
(K5). Revision (188) < creation (212) within P-FULL: LB1's
"revision cheaper than creation" property holds under pressure (K4).

**Q3: Tradeoff quantified (preregistered).** Parsimony costs search
trials (the 10-generation refinement):
- Create: P-FULL 212 vs NP 92 (2.3x).
- Revise: P-FULL 188 vs NP 68 (2.8x).
- P-SEL revise took 368 trials -- the FULL 30-generation budget
  (5.4x) -- and still only reached 10 instructions. Pure selection
  pressure without compression makes revision much slower; the
  compressed 6-instruction seed in P-FULL revised faster than
  P-SEL's 10-instruction seed. Compression not only shortens, it
  makes subsequent revision cheaper than selection pressure alone.

Success preserved (K2): P-FULL 19/19 pre + 22/23 post; P-SEL 19/19
+ 23/23; NP 19/19 + 23/23 -- all >= 70%. The single P-FULL
post-shift miss (22/23) is a live selector episode: N3 worlds always
contain the etype edge so the 6-instruction body cannot fail a
genuine N3 trial when selected (FINAL-POST replay 1000), and the
selector is epsilon-greedy (~9-10% exploration at those episodes).
Not systematic (other arms 23/23); no bar affected.

K3 replication: NP's experimental lines are byte-identical to LB1
arm 0 (verified by diff: CONSTRUCT-ADOPT trials=92 len=11,
REVISE-ADOPT trials=68 len=11, N3 19/19 and 23/23, HAND 1000/100).
The refactor is faithful; the with/without comparison is valid.

K6: zero ENUM-SEARCH events in all arms; create_trials >= 20
everywhere (open-form, not menu selection). K9: 7 strict-decrease
compression events in P-FULL. K10: op 3 retired in all arms, slot 5
never retired (generic retirement rule intact under parsimony).

## Kill bars

- K1 PARSEFFECT (P-FULL final <= 8 instr AND < NP final): **1**
  (6 < 11).
- K2 SUCCESS-PRESERVED (all arms pre/post N3 >= 70%): **1**
  (19/19, 22/23; 19/19, 23/23; 19/19, 23/23).
- K3 CREATE-REPLICATION (NP trials==92, 88 bytes; P-FULL adopt
  best>=850): **1** (92, 88, 1000).
- K4 REVISE-PARSIMONY (P-FULL revise adopt, post N3 >= 70%,
  revise < create trials): **1** (188 < 212).
- K5 VS-RESEARCHER (hand_pre>=850, hand_post<400,
  final_post>=850): **1** (1000, 100, 1000).
- K6 OPEN-FORM (enum==0, create_trials>=20, all arms): **1**.
- K7 DETERMINISM: **1** (sha256 match x3).
- K8 NO-MODES: **1** (build.sh guards).
- K9 COMPRESS-CAUSAL (>=1 strict-decrease COMPRESS, P-FULL): **1**
  (7 events).
- K10 RETIRE (op3 retired all arms, slot5 not): **1**.

## Two things found during development (transparent)

1. **Guard trip on a comment**: the first pp.zag draft wrote
   "No INVENT_MODE" in the header comment; the K8 `_MODE` guard
   (substring match) correctly failed it in pre-check. Reworded to
   "No invention mode" before compiling. The guard works as
   designed; no code was affected.
2. **Commit argument-order mistake**: the first prereg commit
   attempt used `git commit -- <pathspec> -m "msg"`; everything
   after `--` is a pathspec, so `-m` failed 8x before the error
   was read properly. Re-ran as `git commit -m "msg" --
   <pathspec>` and it landed cleanly (dd19bcad6). Process error,
   no scientific content; the prereg still strictly precedes
   implementation.

## SUF analysis (honest)

L2 structural learning, not L3, and the report states exactly
where the researcher still lives in the loop:

Researcher-owned: the ISA, the interpreter, trial/replay machinery,
the graded shaping, the etype-frequency bias, the eight generic
operators, trigger conditions, adopt bars, budgets, PLEN=3
(hand-derived constant), the composite-fitness comparison rule, the
compression operator and its keep-criterion (replay non-decrease),
the 10-generation refinement length. The learner did not invent the
IDEA of parsimony.

Learner-owned: every byte of every created and compressed body
(white-box novel; the final 6-instruction form was assembled and
minimized, never written by the researcher), the policy contents,
which variants survive composite selection, which deletions are
kept (consequence-determined: a deletion survives only if replay
does not drop -- the behavioral criterion is the soundness
guarantee, including against stale-register artifacts of
intermediate deletion steps), the revision decision and timing,
the retirement decision. No body was enumerated from a
researcher-authored family; the constructor never enumerates.

What is genuinely new vs LB1: the learner now compresses its own
created bodies toward the minimal form (11 -> 6, matching the
researcher's hand optimum) while preserving 100% replay success,
open-form creation, revision after law change, and the revisability
advantage over the frozen hand body. The honest cost: ~2-3x search
trials (preregistered refinement), and selection pressure alone
(P-SEL) is insufficient -- it reaches 9-10 instructions and its
revision runs the full budget. Compression (P2) is the component
that reaches the minimum.

## Follow-ups

- Adaptive PLEN: let the learner own the parsimony coefficient
  (raise it when success is saturated, lower it when the search
  stalls) instead of the hand-derived constant 3.
- Compression inside the loop: run the greedy pass as a mutation
  operator during evolution rather than only post-adopt, and
  measure whether it shortens the 2.3x trial overhead.
- Second law change (6->7): does the minimal 6-instruction body
  keep revising cheaply, or does minimality make each revision
  start from a harder (less slack) seed?
- Weaker shaping: ablate the etype-frequency bias under parsimony
  pressure (LB1's remaining unmapped axis).
