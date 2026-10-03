# T6 Sealed Evaluation: RESULT

Status: T6-PASS. Evaluation complete per the sealed protocol.

Date: 2026-09-30.
Evaluator: T6 Evaluator (subagent of the research coordinator).
Sealed spec: `battery_v2/sealed/T6_SPEC.md`, seal commit `a2b1cb123`.
Gate: `9ad539fc2` (T6-GATE-READY).

## 1. Verdict

T6-PASS. The sealed evaluation executed completely: C2 and D were run
against the sealed T6 train episodes with 3/3 byte-identical runs, zero
stderr bytes, pure Zag throughout; B is dispositioned as not evaluated
(section 6); falsifiers were applied; held-out episodes were revealed
only after all hypotheses reported and checked with an independent
GENEXEC2-P harness. No void condition fired.

This verdict concerns the evaluation, not the hypotheses. Per-hypothesis
outcomes: C2 FAIL (BUDGET), D FAIL, B not evaluated.

## 2. Kill bars (evaluator)

- K1 (sealed spec used): PASS. Train episodes are the exact 12 from sealed
  spec section 3, in order. VM variant is GENEXEC2-P per spec section 1.
  Held-out episodes are the exact 10 from spec section 3, revealed only
  post-report. The sealed exhibited target (11 ops) was re-verified
  22/22 by the independent checker as a harness control.
- K2 (evaluation complete): PASS. Both evaluable hypotheses ran to
  completion; per-hypothesis outcomes vs the sealed predictions are
  recorded in sections 4-6; F-TRICK, F-SMUG, and F-MEM were applied;
  held-out accuracy was measured post-report.
- K3 (pure Zag, 3/3 identical): PASS. Authoring used shell, git, and znc
  only; no Python at any stage; all committed files byte-scanned free of
  em and en dashes. C2: 3/3 byte-identical
  (md5 b78f364884b6d2720d3305911934647c). D: 3/3 byte-identical
  (md5 3c02365e8f612eef14321eabb7fe2e3f). Held-out checker: 3/3
  byte-identical (md5 f2563c7d4d5403a4207893341bad76f7). Zero stderr
  bytes on all nine runs.

## 3. The S3 episode-splice (disclosed for governance review)

The frozen hypothesis binaries hard-code tasks T0-T5 in source and expose
no runtime episode input (verified: no stdin, argv, or file reads in any
of the three sources). Mechanically, the only way to expose the sealed T6
train episodes to the frozen mechanisms is a source-level episode-table
splice. This evaluation performed that splice under these constraints:

1. Mechanism byte-identity. The splice touches ONLY episode-data
   sections: task tables, the VM/task dispatch, the F-TRICK audit
   extension to t==6 (section 8 of the sealed spec requires it), and the
   main loop bound. Every mechanism function is byte-identical to the
   frozen source. Diffs committed here show additions only:
   - C2 (`t6_c2.zag` vs `hyp_c2_clean.zag`): 28 added lines, 1 changed
     line (main loop bound 5 to 6). See `DIFF_C2_SPLICE.txt`.
   - D (`t6_d.zag` vs `hyp_d_v2.zag`): additions only (T6 train builder,
     task name, F-TRICK extension with comment, loop bound, pvm
     assignment). See `DIFF_D_SPLICE.txt`.
2. Reconstruction check. Reassembling the unmodified extracted sections
   reproduces each frozen source byte-exactly
   (`c2_recon.zag`, `d_recon.zag`; cmp clean).
3. Behavioral reproduction. The spliced binaries re-ran T0-T5 and
   reproduce the committed K4-clean outputs byte-identically:
   - C2 T0-T5: md5 d6fc84c095c251afd87e79eee7491f54, identical to
     `hyp_c2_clean/RUN_CLEAN_1.txt`.
   - D T0-T5: md5 78bd633521e8fdbc88f9b9fff819e8a7, identical to
     `hyp_d_v2/HYPD_V2_RAW_1.txt`.
   The splice therefore did not alter mechanism behavior.
4. Train-only exposure. Each T6 task table contains ONLY the 12 sealed
   train episodes. Held-out builders return 0 for the T6 task id; no
   held-out data exists in either driver. Run outputs confirm
   (C2 `HELDOUT 0/0`; D `HIDDEN 0/0`).
5. Ancestry. This evaluation commit strictly follows the seal commit
   `a2b1cb123`, which strictly follows every gate item (verified with
   `git merge-base --is-ancestor` before evaluation).

A strict literal reading of sealed spec S3 ("any change voids") would make
T6 evaluation impossible for source-frozen tasks; the sealer's own
predictions presuppose evaluation is possible, and S3 itself mandates the
harness step ("the harness exposes ONLY the train episodes to each frozen
hypothesis"). This splice IS that harness step, disclosed with its
verification evidence for governance review.

## 4. C2 result: FAIL (BUDGET)

Driver: `t6_c2.zag` (splice of frozen `hyp_c2_clean.zag`,
sha256 3f734a4c1b11986766154de3bb3d6f8e2a8f897ee886939f2f8c2dfa06952392).

- `RESULT t=6 BUDGET len=0 evals=1000001 repairs=14 backtracks=9
  splits=1 calls=0 fsmug=1 vm=P`
- `VERIFY train 1/12`, `HELDOUT 0/0`. Final program empty.
- Full trace in `T6C2_RUN_1.txt` (3/3 identical).

Trace summary. C2's repair found both region maps: the diagonal repair
`[IN1 IN1 MUL]` (and variants `[IN1 DUP MUL]`, `[IN0 IN0 MUL]`) fixing
ep=0, and the off-diagonal repair `[IN0 IN1 ADD]` (and `[IN1 IN0 ADD]`)
fixing ep=5, with backtracking between them. It then attempted exactly one
split: probe `[IN0 PUSH -3 EQ]`, partitioning 1 vs 11 episodes, a
degenerate point-isolating split (a==-3 catches only ep=11), NOT the
diagonal/off-diagonal partition. After the split it repaired ep=11 with
the constant `[PUSH -2]`, re-repaired ep=0/ep=5 on the remaining 11, and
exhausted the 1M budget.

Falsifiers: F-TRICK silent (no SOLVE). F-SMUG clean (`fsmug=1`; the P-VM
alphabet contains no ablated opcodes). F-MEM not applicable (no SOLVE).

Prediction vs observed (sealed spec section 7: C2 conditional SOLVE with
split events partitioning diagonal from off-diagonal, each region
repaired, 0 CALLs). Observed outcome is FAIL, so the prediction is NOT
CONFIRMED (outcome mismatch under the confirmation rule).

Mechanism note. The sealed key discriminator, whether C2's repair
synthesizes the nonlinear diagonal region, fired POSITIVE at the repair
level: repair repeatedly synthesized a*b forms for the diagonal episodes
and a+b for the off-diagonal episodes. What failed: (a) the split
mechanism produced only a degenerate point-isolating partition, never the
equality partition; (b) C2's frozen P-VM alphabet (29 symbols) contains no
jump opcodes (no JZ/JNZ/JMP), so even a correct partition could not be
composed into a conditional program. The sealed SOLVE prediction appears
to have assumed jump-capable composition that C2's frozen alphabet lacks.
On GENEXEC2-P, C2's reachable set is polynomials; no polynomial computes
T6 (any polynomial matching a+b on all off-diagonal integer points is
identically a+b, which misses the diagonal).

## 5. D result: FAIL (predicted FAIL CONFIRMED)

Driver: `t6_d.zag` (splice of frozen `hyp_d_v2.zag`,
sha256 b7c381484f4179239a68c949e006aa359d05e965bd0fdd771048c8f0de8a57e1).

- `TASK 6 t6sealed`, `VM p`, `TRAIN_N 12`, `CARRY_IN 3143`
  (archive carried from T5 per battery protocol; `CARRY_DROPPED_INVALID 0`).
- `VERDICT FAIL`, `EVALS 1000000` (budget exhausted), `BEST_SCORE 9`,
  `BEST_PROG [IN0 IN1 ADD]`.
- `PVM_TRAPS 0`, `TRICK_CHECK silent`, `HIDDEN 0/0`, `CALLS 0`,
  `OCC_NICHES 6076`.
- Full trace in `T6D_RUN_1.txt` (3/3 identical).

The best program `[IN0 IN1 ADD]` (a+b) scores 9/12: the 7 off-diagonal
episodes plus the diagonal fixed points (0,0) and (2,2). A second 9/12
program appeared in the improvement trace
(`[IN1 PUSH:-1 IN0 MUL SUB ADD ADD NEG NEG]`).

Falsifiers: F-TRICK silent (no SOLVE; the mandated T6 audit line confirms
it). F-SMUG clean (`PVM_TRAPS 0`; P-VM alphabet). F-MEM not applicable.

Prediction vs observed (sealed spec section 7: D predicted FAIL;
straight-line only; a D v2-SOLVE would trigger a V2 audit). Observed FAIL
with the predicted mechanism visible in the committed trace: MAP-Elites
over straight-line P-VM programs (29 templates, no jump opcodes in the
alphabet), 1M evaluations, no control flow ever produced. Outcome matches
under v2-SOLVE and the trace shows the predicted mechanism. Prediction
CONFIRMED.

## 6. B status: NOT EVALUATED

B's frozen implementation (`hyp_b/hyp_b.zag`, freeze `69730b4ab`)
targets the v1 discovery battery on the full VM. B's prereg
(`9e2fbd134`) was never amended with a case-capable base constructor,
so the prereg section 4 star condition (sealed spec section 7) was never
satisfied and no v2/P-VM B mechanism was ever frozen. Running B's full-VM
mechanism on the T6 episodes would test a different, non-sealed task;
any P-VM-invalid solution would void under F-SMUG. The sealed conditional
prediction for B (FAIL unless amended) stands as recorded expectation,
unmeasured. No B code was modified.

## 7. Held-out accuracy (post-report revelation)

Checked with `t6_heldout.zag`, an independent harness embedding lines
1-208 (through `pvm_valid`) of the frozen GENEXEC2-P source
(`genexec2p.zag`,
sha256 00c496e3ffb64f40fc0bedca6f158b43e755fd326ed6ba22f379d8af35c599cc),
run only after all hypotheses reported (C2 3/3 and D 3/3 complete).
3/3 byte-identical runs, zero stderr.

| Exhibited program | PVM_VALID | ops | ablated op | jump | train | held-out |
|---|---|---|---|---|---|---|
| C2 (empty) | 1 | 0 | no | no | 1/12 | 0/10 |
| D `[IN0 IN1 ADD]` | 1 | 3 | no | no | 9/12 | 7/10 |
| D 9-op best-trace | 1 | 9 | no | no | 9/12 | 7/10 |
| Sealed target (reference) | 1 | 11 | no | yes | 12/12 | 10/10 |

Cross-validation: the checker's train scores reproduce each hypothesis's
own reported train scores (C2 1/12, D 9/12), confirming the transcription
of the exhibited programs. The sealed target's 22/22 confirms the checker.

v2-SOLVE (exact on ALL train episodes AND ops <= 40): no hypothesis
achieved it. C2 1/12, D 9/12.

## 8. Falsifier summary

- F-TRICK: silent on T6. No hypothesis exhibited a jump-free GENEXEC2-P
  program achieving v2-SOLVE. The task stands; it is NOT void.
- F-SMUG: clean. No DIV, MOD, LT, EQ, or GT in any exhibited program
  (main plus fragment bodies; both hypotheses exhibit CALL-free,
  fragment-free programs).
- F-MEM: not applicable; no SOLVE exhibited.

## 9. Battery v2 T6 record

| Hypothesis | Sealed prediction | Observed | Confirmation |
|---|---|---|---|
| C2 | conditional SOLVE | FAIL (BUDGET, 1/12) | NOT CONFIRMED (outcome mismatch) |
| D | FAIL | FAIL (9/12, budget) | CONFIRMED |
| B | FAIL unless amended | not evaluated (no v2 mechanism) | recorded expectation, unmeasured |

No L3 claim follows from battery success alone (prereg section 3.6).
T6 produced no SOLVE on any hypothesis, so no Criterion 0 sequence is
triggered by T6.

## 10. Files (all under t6_eval/)

- `t6_c2.zag`, `t6_d.zag`: T6 evaluation drivers (disclosed splices).
- `t6_heldout.zag`: post-report held-out checker.
- `c2_head.zag`, `c2_mid_orig.zag`, `c2_mid_t6.zag`, `c2_tasks_orig.zag`,
  `c2_tasks_t6.zag`, `c2_core.zag`, `c2_main_orig.zag`, `c2_main_t6.zag`,
  `c2_recon.zag`: C2 splice parts and reconstruction proof.
- `d_head.zag`, `d_tasks_orig.zag`, `d_tasks_t6.zag`, `d_core.zag`,
  `d_core_t6.zag`, `d_main_orig.zag`, `d_main_t6.zag`, `d_recon.zag`:
  D splice parts and reconstruction proof.
- `t6_heldout_head.zag`, `t6_heldout_main.zag`: checker parts.
- `DIFF_C2_SPLICE.txt`, `DIFF_D_SPLICE.txt`: splice diffs vs frozen.
- `T6C2_RUN_1.txt`, `T6C2_RUN_2.txt`, `T6C2_RUN_3.txt`: C2 raw outputs.
- `T6D_RUN_1.txt`, `T6D_RUN_2.txt`, `T6D_RUN_3.txt`: D raw outputs.
- `T6HELD_RUN_1.txt`, `T6HELD_RUN_2.txt`, `T6HELD_RUN_3.txt`: checker outputs.
- `T6_EVAL_RESULT.md`: this file.

Builder label: T6-EVAL-COMPLETE. Verdict: T6-PASS.
