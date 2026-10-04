# L3_CANDIDATE: one proposal that could pass the bar, and what would have to be true

Companion to `SUF_AUDIT.md` and `PREREG.md` (frozen at `0f7409c6c`).
Worker: REDTEAM-SUF. Claim ID minted for the proposal: none (see section 6 --
a proposal is not a result; it gets an ID only when it is run).

## 0. Why the obvious proposals all fail

Every audited lane died of the same disease, and it is worth naming precisely so
the proposal does not inherit it. In all of them there is a **researcher-written
finite menu** `M` and a **criterion** `c`. The learner's "invention" is
`argmax_{m in M} c(m)`. The trace *looks* like discovery because `c` is computed
from experience. But:

- `M` is enumerable from source (C281: 80 instructions; C287: 41; L3-RX: 4 ops;
  L3-SUF-1: 4 rungs; GPI-3: 3 node kinds).
- `c` is either a transcribed answer key (C281, C287) or a researcher predicate
  (L3-SUF-1's `l_surviving`, L3-RX's `induce_candidate`).

Growing `|M|` does not help. C287 already enumerated `41^3` = 68,921 candidates
and C311 already noted the solution sits at "length 8 among `6^8` candidates".
**A bigger menu is still a menu.** Making `c` smarter does not help either --
a perfect criterion over a closed menu is brute-force search, which the prereg
classifies at L1 (K3).

So the proposal must break exactly one thing: **`M` must not be writable down
before the experiment.** Per prereg E1/E2, there must be no researcher-written
list, no `switch`, no template array, no production list, and no enumeration
variable -- for the structural degree of freedom that carries the claim.

## 1. The proposal: MACRO-OF-UNKNOWN-DEPTH, or "the learner names its own loop"

**Claim shape.** The learner is given a task whose solutions require a
*repetition whose trip count is not known in advance and is not derivable from
any single training example* -- because the trip count is determined by the
world's hidden state, learned only by hitting boundaries. The learner's
structural act is to **emit a repeat construct and then discover, from its own
experience, what the loop's exit condition should be** -- and to *revise that
exit condition* when the world changes.

**What makes this different from C287.** C287's REPEAT template had the exit
condition **supplied**: `compile_loop` writes `BEQ reg5, K` then `BEQ reg6,
loophead` (lines 197-210), i.e. a **count** `K` the learner filled in and an
exit the researcher wrote. The learner's act was choosing `K`. Here:

1. The learner is **not given** a loop template. It is given only the ability to
   emit a **call** to something, and a failure signal.
2. The exit condition must be **constructed by the learner** from its own record
   of what has happened, in a form that does not exist in any menu, and
3. the loop must be **structural**, not a fixed number of unrolled steps -- so
   the trace *cannot* be reproduced by writing down the unrolled program.

## 2. Precisely what would have to be true (E1-E6 instantiated)

This is the falsifiable core. Each item is a *pre-registered bar*, not an
aspiration.

**E1 NO MENU (the load-bearing one).**
- There is **no** loop/repeat/while/iterate token, template, opcode, node kind,
  dispatch case, or production in the learner's source or the frozen core.
  Concretely: no `kind==3` node kind, no `op==7`, no `REPEAT` string, and
  `grep` over the learner returns **zero** hits for any of
  `loop|repeat|iterate|while|until|trip|bound|exit`.
- The learner has a **general, form-agnostic composition primitive** (call a
  named body by id) and a **general counter of observed boundary events**.
  Nothing that *is* a loop.
- **Falsifier:** if the loop is assembled by a generic "re-execute body until
  predicate" call where the predicate is a learned i32 comparison, and that
  comparison is selected from a fixed set of comparisons (==, <, >, <=, >=),
  then the loop **is** a template with five slots and the claim is **L2, dead**.
  This is the single most likely way the proposal dies, and I am naming it in
  advance.

**E2 NOT ENUMERABLE.**
- A reader, given the frozen source before any run, **cannot write down** the set
  of loop forms the learner can emit. The attempted answer must be "it is
  whatever body-and-exit-pair the learner's own episode record supports", and
  that set must be **unbounded in the source**: there is no length cap on the
  exit predicate, and no cap on body length.
- **Falsifier:** if I can write "F = {(body, exit) : body in B, exit in E}" with
  `B` and `E` both finite and literal, E2 fails. Concretely, if the exit
  predicate is always a comparison of one accumulator against one stored
  constant, that is a 2-slot template and I must report L2.

**E3 HISTORY-CAUSAL (the one that must be demonstrated, not argued).**
- Two arms, **identical source**, **identical world**, differing only in the
  learner's accumulated history, must emit **different structural forms**, and
  the difference must be one that **no menu could have contained**.
- Concretely: arm A's history contains a counterexample that falsifies the
  `>=` exit; arm B's does not. Arm A emits an exit built from the *sign of the
  observed overshoot*; arm B emits one built from the *observed boundary count*.
  These are different forms, and neither is a slot value in a common template --
  the **structure** of the exit (what quantity it is a function of) differs.
- **Falsifier:** if the two arms differ only in an integer constant, or only in
  which of N enumerated predicates is chosen, E3 fails.

**E4 NOT BRUTE-FORCE.**
- The loop is **never unrolled**. If a run ever produces an unrolled
  straight-line equivalent of the loop, that run is void for this claim.
- Budget for **nested** loops must be strictly insufficient to solve the task
  flat (verified by the a-fortiori argument the GPI series got burned on --
  C397 K4/K5's "vacuous flat control" failure -- so measure it, do not derive
  it).
- **Falsifier:** a depth budget that lets a flat search reach the solution, or
  any trace that exhibits unrolling.

**E5 CONSEQUENCE-SELECTED.**
- The loop is adopted because it **works on held-out episodes**, and the loop
  is evaluated by **running it and observing consequences** -- not by comparing
  against `world_truth`, not by a `l_surviving`-style researcher predicate, not
  by a transcribed label table.
- The learner may **abstain**; abstention must be free (no penalty asymmetry
  that forces a commit, or the criterion is doing the work).
- **Falsifier:** any reference to an expected-value function, a label table, or
  a hand-listed training triple on the selection path. This kills C287's and
  C281's patterns outright, so the audit must grep for it.

**E6 REPRODUCIBLE.**
- `zbuild.sh --rep 3`, 3/3 byte-identical, artifact committed at a citable sha.
- **Additionally, and this is the part every audited lane lacked:** the audit
  artifact must include a **static-decision test** of the shape
  `suf_audit_decide281.zag`. Before reporting, someone must attempt to compute
  the learner's output from the frozen literals alone, in a program that never
  calls the learner. **If that succeeds, the claim is dead and is reported dead.**
  L3-SUF-1 would have died to a 40-line Zag program. Any lane that has not
  survived its own decide-from-literals test has not been tested.

## 3. The three ways this proposal is most likely to be a lie

1. **The loop is a hidden template.** Overwhelmingly the likeliest failure. The
   frozen COGOPS core already has `cycles_learned` and `compose`; a repeat
   construct may already exist inside the 1331-line frozen prefix. **Step 0 must
   be a source audit of the frozen cores for an existing loop**, and if one
   exists the proposal is dead on arrival -- I would be re-wrapping C287.
2. **The exit predicate is a learned constant, not a learned form.** Covered by
   E3's falsifier.
3. **The "hidden state" is secretly visible.** If the trip count is derivable
   from a single training example, the learner is doing arithmetic, not
   invention. The world must be built so the trip count is a function of
   something the learner sees only as an aggregate over episodes, and the
   sealed key must verify that no single example determines it. (This is the
   "incomplete-disambiguation trap" that killed L3-INR -- C459's actual
   finding -- so it must be checked adversarially, not assumed.)

## 4. What I am NOT proposing

- Not a bigger menu. C287 already showed `41^3` candidates buy nothing.
- Not a smarter criterion. C287's oracle already scored perfectly.
- Not "let the learner choose among N strategies". That is GPI-3's factorization
  and C285's menu selection.
- Not a new vocabulary the researcher contributes. That is GPI-1's NEST
  combinator, which the C303 self-assessment correctly says the learner did not
  invent.

## 5. The standing gate I am asking for

Every future L3 claim should be required to ship, **before** its verdict is
recorded:

1. a `PREREG.md` with an explicit **F-enumerability bar** (the charter section 7
   question, asked and answered in advance);
2. an **F-enumeration appendix** -- the complete emittable-form set with
   `file:line` and literal lists, exactly as `SUF_AUDIT.md` section 3 does;
3. a **decide-from-literals** program (a la `suf_audit_decide281.zag`) that
   fails to reproduce the learner's structural output.

Item 3 is the cheap decisive one. C281's L3 claim died to it in under a page.
It should be run *before* the red team is convened, not after, because every red
team in this audit spent its effort on trigger/oracle/order forensics while the
enumerability question sat unanswered in the source.

## 6. Claim ID

**None minted.** A proposal that has not been implemented has no result to
record. When it is run it takes **C592** (next free in my C59x block; C590 and
C591 are the audit and the correction, and I am deliberately not reusing the
contested C500-C506 range -- see `SUF_AUDIT.md` section 8).

## 7. Falsifiers for this proposal itself

Per prereg S5, stated against my own work:

- **S-P1** I cannot make step 0 (frozen-core loop audit) come back clean.
- **S-P2** The decide-from-literals program reproduces the structural output.
- **S-P3** E3's two arms differ only in a constant.
- **S-P4** The loop is a 2- or 3-slot template with a researcher-written exit.
- **S-P5** I find myself adjusting a bar after seeing the first trace. If that
  happens the wave is void and must be re-preregistered.

Any one of S-P1..S-P4 is fatal, and each is checkable by a third party who has
only the source and the bars. That is the standard the incumbent lanes met, and
the standard L3-SUF-1 did not.