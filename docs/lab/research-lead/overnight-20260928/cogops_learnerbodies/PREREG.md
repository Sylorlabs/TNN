# PREREG: Learner-Created Cognitive Operation Bodies (LB1)

Frozen before implementation. 2026-10-03. Worker: COGOPS-LEARNERBODIES.
Non-ledger task (claim minting paused).

## Question

Micah priority #5: cognitive-operation bodies becoming increasingly
learner-created. Ruling: RETRIEVE/DERIVE/VERIFY/PREDICT/INQUIRE/
CONSTRUCT must not become permanent human-authored mental modes;
cognitive procedures move into learner-owned structures that can be
learned, selected, composed, revised, specialized, retired, eventually
created.

cogops_bodies showed bodies can be REVISED by the learner, but its
operators (single-SET-imm enumeration, splice) were researcher-authored
and the bodies started as researcher bootstrap. cogop_invention showed
operation invention, but the learner SELECTED from a finite
researcher-enumerated REPEAT schema (honest limit recorded: open-form
structure assembly is the next frontier).

LB1 tests the next step: the learner starts with an EMPTY operation
slot and, through experience (success/failure, consequences), CREATES
the operation body by open-form assembly. No enumerated candidate
family. The assembly policy is consequence-shaped learner state.

## Design (pure Zag, pinned znc, safebin)

Base frame reused from cogops_bodies/cb.zag (cited, not re-derived):
8-instruction interpreter (SET/COPY/ADD/EQ/JNZ/MATCH/READF/YIELD),
5 innate op bodies (op 0 gather now CORRECT, etype SET=1; no planted
bug), generic epsilon-greedy selector, consequence credit, generic
retirement rule, world families F 40% / N1 25% / N2 15% / N3 20%.
N3 = (Q)-[W,etype5]->ans; no innate body serves it (probe ctx0=0).
Slots 5,6 start EMPTY.

The CONSTRUCTOR (replaces REPAIR/DIVERGE/INLINE; all state in learner
cells; no new cognitive mode):

1. Policy (learner-owned): OPC[8] opcode counts, BIG[64] opcode
   bigram, REGR[8] register marginal, IMMC[9] imm-class marginal
   (classes: -1,0..7). Laplace-smoothed (init 1).
   - T (arm 0): seeded from instruction statistics of bodies the
     learner itself experienced as successful (tot_n>=10, tot_sum>0).
     Which bodies count as models is consequence-determined.
   - C-uniform (arm 1): uniform seed (no experience). Tests seeding.
   - C-seed-frozen (arm 2): seeded, but NO reinforcement updates.
     Tests adaptation.
2. Etype-frequency bias (generic machinery, all constructor arms):
   at each construction trigger, IMMC += 2 per etype observed in the
   learner's own recent snapshot rings (all ctx). The learner's
   memories suggest which etypes are worth trying; disclosed shaping.
3. Graded replay credit (generic consequence shaping, disclosed):
   per snapshot: correct YIELD=1000; answer value present in a
   register AND not among the body's own SET immediates=400; a
   register holding a valid node id not among the body's own SET
   immediates=150 (graph discovery); wrong YIELD=100; else 0.
   Mean over the target ctx ring (8 recent snapshots, ring buffer).
4. Population: 8 bodies, 12 offspring/generation, operators
   {mutate-one-slot, append, insert-at-random-position, delete,
   single-point crossover}, all sampling from the policy. Length cap
   12 instructions. Elitist (score desc, length asc, age asc).
   Budgets: creation <=40 generations, revision <=30.
5. Policy update (T, C-uniform): reinforce instruction choices of
   above-median bodies each generation (counts += 1). Consequence-
   shaped; the policy content is learner state.
6. Creation trigger (generic, consequence-driven): every 25 eps from
   ep 50, if slot 5 empty, budget left, target ctx ring >=6 snaps,
   and the context is unserved (no op with appl_mx(o,0)>600 at n>=10).
   Adopt iff best replay >=850. Install to slot 5, origin=4
   (constructed), fresh appl. Log CONSTRUCT-ADOPT with trial count.
7. Law change: at ep 400, N3 etype 5->6 (probe ctx0 still 0; the
   learner detects it only via consequence).
8. Revision trigger: every 25 eps post-shift, if an origin-4/5 body
   is installed and its replay on the recent target ring <400
   (ring>=6, budget left): population = current body + 7 mutants,
   <=30 generations. Adopt iff best >=850 and best > current+150.
   Replace in place, origin=5 (constructed+revised). Log
   REVISE-ADOPT with trial count.
9. Hand-authored comparison (researcher-authored body, replay-only,
   never installed): gather body with SET imm=5 built to scratch.
   Replayed on the target ring at ep 399 (HAND-PRE, expect >=850:
   sanity that it is a good body for the original family) and at
   end of run (HAND-POST, expect <400: frozen, cannot adapt).
   T's final body replayed at end (FINAL-POST, expect >=850).
10. Retirement: generic rule tot_n>=12 and tot mean < -0.6 (unchanged
    principle from cb.zag). Op 3 (predict, always yields wrong
    answer) is the designated retiree; working bodies must not retire.

Arms (one binary, sequential, env RNG reseeded per arm for identical
world sequences):
- arm 0 = T (treat): seeded policy + reinforcement.
- arm 1 = C-uniform: uniform policy + reinforcement.
- arm 2 = C-seed-frozen: seeded policy, no reinforcement.
- arm 3 = C-menu: no constructor; duplicate op 0 to slot 5 and run
  the cogops_bodies single-SET-imm (0..7) enumerator on the target
  ring (origin=2); re-run post-shift for revision. The menu baseline.
  ENUM-SEARCH events logged; T must log zero.

700 episodes/arm. No INVENT_MODE. No new mode/bridge/handler/semantic
case. Interpreter opcodes remain exactly 1..8.

## Kill bars (all checked by the binary; K7/K8 by build.sh)

- K1 CREATE: T logs CONSTRUCT-ADOPT pre-shift with best>=850, AND
  pre-shift late N3 live success (eps 300-399) >=70%, AND
  origin[5] in {4,5}.
- K2 POLICY-LEARNED: (a) T's IMMC count for imm-class 6 is higher
  post-shift than pre-shift (logged) AND the revised body contains
  a SET instruction with imm=6 (white-box cell has_set6); (b)
  trials_to_create(C-uniform) > trials_to_create(T), or C-uniform
  fails to adopt within budget.
- K3 OPEN-FORM (not menu selection): in T's run, ENUM-SEARCH events
  == 0, AND create_trials >= 20, AND novel_flag == 1 (final slot-5
  body differs byte-wise from all 5 innate bodies and the hand
  body; checked in code, body disassembly printed).
- K4 REVISE: T logs REVISE-ADOPT post-shift, AND post-shift late N3
  live success (eps 600-699) >=70%, AND revise_trials < create_trials.
- K5 VS-RESEARCHER: HAND-PRE >=850 AND HAND-POST <400 AND
  FINAL-POST >=850 (T's revised body works where the frozen
  researcher-authored body fails).
- K6 RETIRE: op 3 retired==1 at end of T's arm AND slot 5
  retired==0 (retirement is consequence-driven and does not kill
  working created bodies).
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 recorded).
- K8 NO-MODES: build.sh asserts zero `python`, zero `as *i32`,
  zero cognitive `_MODE` tokens, interpreter dispatch exactly
  opcodes 1..8, no added semantic cases.

OVERALL: K1..K8 all PASS -> LB1-COMPLETE (learner-created bodies).

## Honest boundary (preregistered)

Expected level: L2 structural learning, not L3. Researcher-owned:
the ISA, the interpreter, trial/replay machinery, the graded
shaping (+150/+400), the etype-frequency bias, the five generic
operators, trigger conditions, adopt bars. Learner-owned: every
byte of every created body, the policy contents, which bodies are
adopted/revised/retired, all selection. The learner does not invent
the IDEA of constructing bodies. What is genuinely new vs
cogops_bodies: bodies are created from EMPTY by open-form assembly
(no enumerated variant family, no bootstrap body to repair), and
the proposal policy itself is consequence-shaped learner state.
What is genuinely new vs cogop_invention: no finite
researcher-enumerated schema (the REPEAT form is gone); bodies are
arbitrary instruction sequences up to the length cap.

A FAIL on any bar is informative and will be reported as such; in
particular K2b/K4 failing would show the limits of experience
seeding and revision transfer.
