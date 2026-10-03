# REPORT: Learner-Created Cognitive Operation Bodies (LB1)

**Verdict: LB1-COMPLETE** (K1-K8 all PASS on the treat arm).
Prereg `ab31b1a02b1d54f4a27c9c150f87ae73f999af23` strictly precedes
implementation. 3/3 byte-identical, sha256
`01efd9714ff09959cd1ad333acda501ec08101931fe8b73da0161b6ff880ad4c`.

## Question

Can the learner CREATE a cognitive operation body from an empty slot
through experience -- not select it from a researcher-enumerated menu
(cogops_bodies), not select it from a finite researcher-enumerated
schema (cogop_invention)? And can it revise the created body when the
world changes, and retire bodies that do not work?

## What was built

`lb.zag` (~1100 lines, pure Zag, pinned znc): the cogops 8-instruction
interpreter and world families from cogops_bodies (op 0 gather now
correct; REPAIR/DIVERGE/INLINE removed), plus a consequence-driven
open-form constructor, all state in learner cells:

- **Policy** (learner-owned): opcode/bigram/register/imm distributions
  (OPC/BIG/REGR/IMMC), Laplace-smoothed. Seeded from instruction
  statistics of bodies the learner itself experienced as successful
  (tot_n>=10, tot_sum>0); reinforced on above-mean offspring (arms 0,1).
- **Population search**: 8 bodies, 12 offspring/generation, generic
  operators {mutate-one-slot, tweak-a-constant, append, insert,
  delete, crossover, experience-graft, experience-crossover} over an
  open body space (<=16 instructions). No enumerated candidate family.
- **Graded replay credit** (disclosed generic shaping): correct
  YIELD=1000; answer-in-register=400; graph-node discovered=150;
  wrong YIELD=100; else 0. Names no etype, wiring, or answer.
- **Etype-frequency bias** (disclosed shaping): at each construction
  trigger, IMMC gains +2 per etype observed in the learner's own
  recent target-context snapshots.
- **Creation trigger** (generic): slot 5 empty, budget left, >=6
  target snapshots, context unserved (no innate op good at ctx0=0).
  Adopt iff replay >=850 -> origin=4, fresh evaluation.
- **Law change** at ep 400: N3 etype 5->6 (probe ctx0 unchanged;
  the learner detects it only via consequence).
- **Revision trigger**: installed body replays <400 on recent
  snapshots -> population seeded from the current body -> adopt iff
  >=850 and >current+150 -> origin=5.
- **Hand-authored comparison** (researcher-written minimal 6-instr
  gather, replay-only, never installed): HAND-PRE (ep 399),
  HAND-POST (end), FINAL-POST (learner's final body, end).
- **Retirement**: generic rule (tot_n>=12, mean<-0.6).

Four arms, one binary, env RNG reseeded per arm (identical worlds):
T (arm 0, seeded+reinforce+graft), C-noxfer (arm 1, uniform policy,
no experience graft/crossover), C-seed-frozen (arm 2, seeded, no
reinforce, graft), C-menu (arm 3, duplicate op 0 + exhaustive
single-SET-imm enumeration, the menu baseline). 700 episodes/arm.
No INVENT_MODE, 0 modes/bridges/handlers/semantic cases.

## Results (treat arm)

- `CONSTRUCT-ADOPT trials=92 best=1000 len=11` at ep 74: from an
  EMPTY slot, the learner assembled an 11-instruction gather body
  (white-box disassembly in run log; first instr `SET R0,5`).
  Zero ENUM-SEARCH events: it was never enumerated, only sampled,
  mutated, grafted, and selected.
- Late pre-shift N3 live success: **19/19 (100%)**.
- Post-shift (etype 5->6): the installed body's replay fell to 0;
  `REVISE-ADOPT trials=68 best=1000 len=11` at ep 474 (revised body
  contains `SET R0,6`; immc6 weight 1->20). Revision took fewer
  trials than creation (68<92).
- Late post-shift N3 live success: **23/23 (100%)**.
- `RETIRE op=3 ep=61`: the always-wrong predict body was retired by
  the generic consequence rule; the working created body was not.
- Created body is byte-novel vs all 5 innate bodies (white-box check).

## Controls

- **C-noxfer** (no experience transfer): 488 trials (full budget),
  best=150, NO adopt, twice. N3 success 0/19. The graded shaping
  alone gives partial gradient (150 = graph discovery) but cannot
  cross to a working body. Experience transfer is causal (K2B=1).
- **C-seed-frozen** (seeded+graft, no reinforcement): create=68,
  revise=44 trials, all bars pass. Online policy reinforcement added
  no measurable benefit here (frozen was slightly FASTER than T:
  68 vs 92); the seeding, grafting, and bias do the work. Honestly
  reported: the "adaptation" component of the policy is minor in
  this instance.
- **C-menu** (enumeration): 41 trials each way, best=1000, N3 19/19
  and 23/23. The menu also solves and revises -- but by exhaustive
  enumeration (2 ENUM-SEARCH events), not open-form creation
  (K3=0), and its revision is no faster than its creation (K4=0).

## Kill bars

- K1 CREATE (adopt pre-shift, replay>=850, N3 pre>=70%, origin 4/5):
  **1** (1000, 19/19, origin 4).
- K2 POLICY-LEARNED (immc6 rises post-shift AND SET-6 white-box;
  C-noxfer slower-or-fails): **1** (1->20, has_set6=1; noxfer 488
  trials, no adopt).
- K3 OPEN-FORM (0 ENUM events, >=20 trials, novel vs innate):
  **1** (0, 92, novel=1).
- K4 REVISE (adopt post-shift, N3 post>=70%, revise<create trials):
  **1** (1000, 23/23, 68<92).
- K5 VS-RESEARCHER (hand_pre>=850, hand_post<400, final>=850):
  **1** (1000, 100, 1000). The frozen hand body fails post-shift;
  the learner's revised body works.
- K6 RETIRE (op3 retired, slot5 not): **1** (ep 61).
- K7 DETERMINISM: **1** (sha256 match x3).
- K8 NO-MODES: **1** (build.sh guards: no python, no `as *i32`,
  no _MODE tokens, opcodes exactly 1..8).

## Is the learner-created body better than the researcher-authored one?

Nuanced. On **success rate**: equal (both 100% pre-shift). On
**revisability**: the learner's body wins decisively -- after the
law change the frozen hand body scores 100/1000 on replay while the
learner revised its own body back to 1000 (K5). On **efficiency**:
the researcher-authored body wins -- it is 6 instructions vs the
learner's 11 (the learner grafted the full gather scaffold rather
than discovering the minimal straight-line form). Creation, not
optimization: the learner found a working body, not the minimal one.

## Two bugs found and fixed during development (transparent)

1. **Hand body missing status SET**: the first hand-written
   comparison body omitted `SET R6,2` before YIELD, so it yielded
   status 0 and scored 400 instead of 1000 on HAND-PRE. Fixed by
   adding the instruction (researcher-authored baseline bug; the
   prereg did not pin the hand body's byte layout).
2. **Enum-event counter never incremented**: the menu arm logged
   ENUM-SEARCH lines but never incremented the enum_events cell, so
   K3's "zero ENUM events" check was vacuous. Fixed; menu arm now
   correctly scores K3=0.

## SUF analysis (honest)

This is **L2 structural learning, not L3**, and the report states
exactly where the researcher still lives in the loop:

Researcher-owned: the ISA, the interpreter, trial/replay machinery,
the graded shaping (+150/+400), the etype-frequency bias (+2), the
eight generic operators, trigger conditions, adopt bars, budgets.
The etype bias in particular does real work: it makes the constant
discoverable. Without it (and without grafting), C-noxfer shows the
search cannot cross from partial credit to a working body.

Learner-owned: every byte of every created body (white-box novel),
the policy contents (seeded from the learner's own success
experience, reinforced by consequence), which bodies are adopted,
which graft sources prove useful (selection, not prescription),
the revision decision and its timing, the retirement decision.
No body was enumerated from a researcher-authored family; the
constructor never enumerates.

What is genuinely new vs cogops_bodies: bodies are created from
EMPTY by open-form assembly (no bootstrap body, no single-point
variant menu); the proposal policy is consequence-shaped learner
state. What is genuinely new vs cogop_invention: no finite
researcher-enumerated schema -- bodies are arbitrary instruction
sequences, and the found 11-instruction form was assembled, not
selected from a (prologue, step, counter) triple.

Limit: the learner did not invent the IDEA of constructing bodies,
and its search leans on experience-grafting (L2 adaptive reuse --
which is, notably, Micah's current L2 priority). Full L3
(representational invention of the construction idea itself) is
not claimed.

## Follow-ups

- Minimal-form pressure: add a parsimony term so the learner
  compresses the grafted 11-instr body toward the 6-instr form.
- Weaker shaping: reduce/ablate the etype bias to map how much
  hint is necessary (C-noxfer already ablates grafting; bias
  ablation is the remaining axis).
- Second law change (6->7) to test repeated revision and whether
  revision keeps getting cheaper (learning to revise).
- Retire-and-replace: a created body that cannot be revised should
  be retired and the slot freed for fresh construction.
