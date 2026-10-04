# PREREG — C603 "MAXIMALLY-GENEROUS EXIT-SLOT": the hypothesis after its own gate killed it

Worker: L3-MACRO. Lane: `lane/l3macro`. Dir: `l3macro_unknowndepth/`.
Committed **alone, before any implementation exists**. Gate result: `STEP0_AUDIT.md`
(C600, commit `ce2dd1be9`).

**I am preregistering a hypothesis I expect to fail, and I am preregistering the
failure as the outcome.** C600 established the assigned hypothesis
(MACRO-OF-UNKNOWN-DEPTH) is dead twice over: the frozen core already contains
general iterated-execution constructs (`execute_plan_iter` `c8_learn.zag:994`,
`topo_g` `:804`, `osc_handle` `:1239`), and its exit-condition set is four
hardcoded literals with **no learner-writable slot** (`F_exit = {quiescence,
cap16, stall-repair, cycle-lag}`).

Rather than abandon the question, I test the strongest remaining version of it.

---

## 1. Hypothesis

**H.** If a researcher supplies the learner with a **maximally general
learner-writable exit-condition interface** — far more affordance than the frozen
core offers — then the emittable set of loop forms `F` remains **finite and
enumerable from source**, and the resulting capability, however load-bearing, is
therefore **L2 at best, never L3**.

This is a *negative* hypothesis about a positive one. It is falsifiable: if `F`
came out non-enumerable, or if the decide-from-literals program failed to
reproduce the learner's structural choice, H is false and I must report L3-or-
better, or at minimum report the failure of my own kill.

**Why this is the right thing to run.** The prior literature has been conflating
two independent axes:

- **axis 1 — load-bearingness**: does the invented form actually carry capability
  that its ablations remove?
- **axis 2 — source-underdetermination**: is the form's space non-enumerable from
  source?

Every lane the prior audit examined fails axis 2. **None of them was shown to fail
axis 1.** C287, L3-SUF-1, GPI-3 and CALR are all argued about on enumerability
grounds, with no capability ablation attached, which leaves open the possibility
that their forms are simultaneously *real* and *enumerable*. Separating the axes
is the contribution available here, and it can be done without an L3 claim.

## 2. FROZEN INSTANTIATION — the complete emittable form set, fixed now

Written down **before** the code exists, so the SUF test cannot be widened after
seeing a trace. If implementation forces a change to anything in this section,
this prereg is void and I must re-preregister (bar **S-P5**).

**Frozen basis** — deliberately the *same* alphabet the prior audit used to kill
C281 to L1 (`l3_repro_transfer/orig_glm_learner.zag:17-18`, recovered CALR
`isa.zag:7-10`), so the comparison is direct:

```
ops   : 0=CPY(Rd=Rs) 1=ADD(Rd+=Rs) 2=MUL(Rd*=Rs) 3=SET1(Rd=1) 4=INC(Rd+=1)
regs  : R0..R3 (i32). instruction = (op,d,s), 3 bytes.
world : op 5 = STEP, R[d] = w_step(R[d]).  -- provided; without it the loop is inert
```

**Macro record.** `MACRO = (body, exit)`, the only structural object the learner
emits.

- `body` ∈ `B` = all sequences of basis instructions of length 0..8.
- `exit` = `(src, cmp, thr)` with `src ∈ {R0,R1,R2,R3}` (4),
  `cmp ∈ {LT, EQ, GT, LE, GE}` (5), `thr ∈ ℤ` (learned integer).

**The SUF test, stated as the complete answer.** A reader of my source can write
the emittable set in one line:

```
F  =  B  ×  {R0,R1,R2,R3}  ×  {LT,EQ,GT,LE,GE}  ×  ℤ
```

**I declare in advance that this line is the answer, and that writing it
constitutes a FAIL of the L3 bar.** The charter §7 question — *can a reader
enumerate the structural forms?* — has answer **YES**. The exit is a **3-slot
template with a 5-element comparison menu and a learned constant.** `|B|` is
`≈1.9e15`, and this is irrelevant: `L3_CANDIDATE.md` §0 already disposed of
exactly this move against C287's `41^3` — *a bigger menu is still a menu.* Large
`B` does not make the **form** non-enumerable; it makes the search expensive.
Both facts must be reported and they are independent.

## 3. Frozen kill bars

| Bar | Condition | Verdict if met |
|---|---|---|
| **KB1 (SUF)** | `F` is enumerable from source as in §2 | **NOT L3.** Class ≤ L2. |
| **KB2 (decide-from-literals)** | a program that never calls the learner reproduces the learner's chosen `(src,cmp,thr)` from world literals alone | **DEAD.** |
| **KB3 (load-bearing)** | ablation `A-NOLOOP` solves ≥ 90% of held-out | chain link "pressure" is vacuous; report as vacuous |
| **KB4 (slot matters)** | ablation `A-NOSLOT` solves ≥ full arm | the exit slot carries nothing; the whole hypothesis is inert |
| **S-P5** | I add a structural slot after seeing a trace | wave void, re-preregister |

**Predictions, frozen.** P1: KB1 holds (certain — §2 is arithmetic).
P2: KB2 holds (the exit is chosen by argmax over 20 structurally distinct exits;
the world literals determine the winner). P3: `A-FULL` ≫ `A-NOLOOP` on held-out
trip counts — the loop **is** load-bearing. P4: therefore the honest verdict is
**"load-bearing and enumerable"** — L2, and the two axes are demonstrated to be
independent.

## 4. Fixture (frozen literals, no RNG)

Episode `e` has a hidden trip count `T_e`. The learner sees only the register
state after each `STEP`; it never sees `T_e`. Frozen bands:

- train : `T` ∈ {3, 5, 8, 13} (4 episodes)
- holdout: `T` ∈ {17, 29, 44, 61} (4 episodes, never seen in training)
- world: `w_step(x) = (x*x + 7) mod 97`; the macro's job is to iterate `STEP` and
  exit at the cycle, i.e. when the register returns to a value already seen.

**Incomplete-disambiguation check (adversarial, preregistered).** The
"L3-INR trap" (`SUF_AUDIT.md` §1; C459) is that the hidden quantity is secretly
derivable from one example. Frozen check: for every train episode, assert that
`T_e` is **not** a function of `(x0, x1, ..., x_n)` for any prefix `n < T_e`.
If it is, the fixture is void and I report the fixture void rather than a
result. This is checked by the artifact, not assumed.

## 5. Internal evaluation (charter 45)

The learner selects among exits **by running them** and comparing achieved
outcome against **its own recorded target**, with **free abstention** (an arm that
declines scores no better than one that commits wrongly; no penalty asymmetry).
Forbidden on the selection path, and grepped for: `world_truth`, any label
table, any hand-listed training triple, any expected-value function. The
learner process receives no values the driver withholds from it except `T_e`,
which it never receives in any form.

## 6. Ablations (all three arms, same source, same fixture)

- **`A-FULL`** — exit slot live; learner emits `(body, src, cmp, thr)`.
- **`A-NOSLOT`** — exit frozen to the frozen core's own rule (quiescence), the
  exact construct `c8_learn.zag:1030`; learner may emit only `body`.
- **`A-NOLOOP`** — body executes once. Tests repetition itself.

Reported per arm: solve count on train, solve count on held-out, |F| actually
enumerated, and the chosen exit triple. Capability drop `A-FULL − A-NOLOOP` on
held-out is the **axis-1 number**; `|F|` and the §2 line are the **axis-2
number**.

## 7. Transfer

Train band and holdout band are disjoint and the holdout trip counts (17, 29, 44,
61) all exceed every train trip count (3, 5, 8, 13), so a learner that
memorised a constant cannot transfer. Any held-out solve therefore evidences
that the *form* generalises across unknown depth — which is the honest content
of "transfer" here, and is explicitly **not** evidence of source-
underdetermination.

## 8. Determinism

`zbuild.sh --rep 3`, 3/3 byte-identical stdout, committed at a citable sha256.
Output via `_zag_print` / `_zag_println` only; **never** `_zag_raw_syscall`
(brief §4.0 — inert on this host). Non-empty output asserted in the harness.
Pure Zag for all computation; shell/git orchestration only.

## 9. Claim ID

**C603.** Reserved. Minted only for the implemented result, in whichever
direction it falls. C377-C466 untouched (brief §10.1); C590/C591 belong to
`redteam/suf-audit`; C600-C602 are in `STEP0_AUDIT.md`.