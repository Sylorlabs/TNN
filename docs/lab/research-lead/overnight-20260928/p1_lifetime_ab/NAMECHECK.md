# NAMECHECK: LIFETIME-AB-1 (lt1)

Static audit of the hard constraints in PREREG section 1.

## 1. One learner instance, one process, no reset, no recompilation

`main` allocates `L` (16384 B, the frozen COGOPS learner state) and `LT`
(8192 B, the additive lifetime block) exactly once and threads the same two
objects through stages A..H with no `z_alloc` of a replacement and no zeroing
between stages. Fact arena `A` is append-only for the whole run.

Grep evidence: `z_alloc(16384)` and `z_alloc(8192)` appear once each in
`main`. Every other learner-state buffer in the file (`L2/T2`, `L3/T3`,
`L4/T4`, `SL/SLT/SA`) is explicitly a CLONE used only by the baseline,
ablation, or TTC phase, and is documented as such at each declaration.

No recompilation between stages: one binary, one `main`, one linear pass.

## 2. No task labels reach the learner

The learner is reachable only through two functions:

```zag
fn lt_episode(L,LT,A,K,kind,p1,p2,RB,CB,TO,SE)
fn lt_query  (L,LT,A,G,K,R,ANS)
```

Neither signature contains a stage id, stage name, stage index, world id,
goal tag, reuse hint, or correctness flag. `lt_episode`'s `kind` is the
modality channel that the frozen core itself already requires
(`ret_episode` / `vfy_episode` / `cnt_episode`); it selects a sensor, not a
task, and carries no stage information.

The harness-side dispatch `mk_goal(which, G)` and `ep_ret/ep_vfy/ep_cnt(id)`
are the only places a stage index or a relation id exists, and both are
called from the driver, never from learner code. `build_upto(A,upto)` and
`feed_stage(...,s)` take a stage index and are harness-only.

Learner-internal counters that could have encoded a stage were deliberately
built NOT to: templates record `origin_q`, the learner's own monotone query
counter, never a stage number. `emit_q` prints `orgq=` from that counter.

## 3. No answer feedback

The learner never receives judgment or consequence. `lt_query` returns the
answer into a caller-supplied buffer and returns only a 0/1 code for
"declined vs answered". Nothing in the learner's decision path reads a
correctness flag.

Consequence, stated as a boundary rather than a defect: the learner cannot
know whether an answer is right. Every correctness number in the output is
evaluator-side (`lt_score` compares against `lt_decl` and against
`lt_oracle`). This is stricter than the mission asked for.

The one place the learner reacts to its own experience is
`lt_fun_observe`, which fires only on triples delivered inside VERIFY
episodes -- observation, not judgement.

## 4. Contract module excluded from the learner's decision path, with reason

`hook_phase1/hq_module.zag` is concatenated and linked, and
`CONTRACT-SELFTEST` exercises `u_check` to prove it executes. It is
deliberately not on the learner's decision path: every entry point that
changes belief (`u_invalidate(judgment, consequence)`, `u_revise`) requires
a ground-truth consequence. Calling them inside the learner would inject the
answer feedback that section 1 forbids. Documented as an exclusion.

## 5. Frozen prefix unmodified

`lt_build.sh` concatenates, and never edits:

* `cogops_rescueaware/c15_base.zag`
* `cogops_learnosc2/c8_learn.zag` (all 1331 lines)
* `hook_phase1/hq_module.zag`

All lane code lives in `lt_world.zag`, `lt_life.zag`, `lt_main.zag`. No
frozen function body was modified. Two lane-local substitutes were required
by compiler defect B16 and are documented at their definitions:
`lt_chain_add` / `lt_chain_clear` (byte-identical layout and semantics to
the frozen `chain_add` / `chain_clear`, stores inlined) and `lt_flush`
(`_zag_print` on the finished buffer, because the frozen `o_flush` is inert,
B15). Neither changes learner semantics.

## 6. Pure Zag

All worlds, goals, oracles, statistics and verdicts are Zag. Shell is used
only for `cat` and for `tools/zbuild.sh`.
`tnn_pure_zag_report` ends `VERDICT: PURE-ZAG-CLEAN` and no forbidden
interpreter was invoked at any point in this lane.

## 7. Preregistration discipline

`PREREG.md` was committed alone, in commit `7f66e5de7`, before any
implementation file existed in the lane directory. Two prereg arithmetic
annotations were found wrong before running and are recorded in
`PREREG_ERRATA.md`; the frozen value SEQUENCES were correct and are what the
oracle is asserted against.

## 8. Result certification status

**NOT CERTIFIED.** Defect B16 (see `DEFECT.md`) is a silent, deterministic
miscompilation of indexed reads that is present in this very binary: two
functions in `lt1_full` return different values for `get32(L,0)` on the same
cells. `zbuild --rep 3` cannot detect it because the corruption is
deterministic. Every number in `lt1_run1.txt` is therefore reported as
UNCERTIFIED in `REPORT.md`, and no claim ID above C500 is asserted.