# EVAL_EXEC.md -- COMPOSE-SEALED-EVAL execution record

Date: 2026-10-03. Worker: COMPOSE-SEALED-EVAL. Lane:
`docs/lab/research-lead/overnight-20260928/compose_sealed_eval/`.
Branch: `tnn-native-lab`. Task type: NON-LEDGER (claim minting paused).

This file is written BEFORE any sealed-world execution. The
evaluation protocol is the adversary's frozen PREREG.md
(`../compose_adversary/PREREG.md`), executed verbatim. No new
prereg is authored: the frozen protocol IS the prereg.

## Frozen protocol being executed (PREREG section 6)

1. Copy (do not move) frozen mechanism sources into a fresh
   eval directory OUTSIDE builder lanes. Concatenate:
   - A: bc_base + bc_thunk + bc_search + adv_worlds +
     eval_main_a
   - B: sus_base + sus_thunk + sus_asm + sus_rev + adv_worlds +
     eval_main_b
   - C: lc_base + lc_thunk + lc_search + lc_mem + lc_rev +
     lc_rep + adv_worlds + eval_main_c
   (lc_rep included per section 6's explicit note: "lc_rep
   carries do_prob reporting; it has no main".)
   Compile each with the pinned znc. Eval mains are the
   adversary's frozen templates under
   `../compose_adversary/eval_templates/`.
2. Process grouping: the adversary's eval templates run one
   process per mechanism with FRESH arenas per problem
   (A/S reallocated before every problem; C's M reallocated
   per section-6 group: SEQ1 TEACH->TRAP1->TRAP2 one M,
   SEQ2 TEACH-D->T-FANIN->T-CHAIN one M, fresh M elsewhere).
   Verified before execution: no `global` state in any
   mechanism source, `z_alloc` is `_zag_malloc` (independent
   malloc per arena), and the builders' own mains ran
   multi-problem single processes the same way. One process
   with fresh arenas is behaviorally identical to fresh
   processes here.
3. Each binary run 3 times; require byte-identical stdout
   across the 3 runs. Empty stderr required.
4. Score the HARD/SOFT bars of PREREG section 5 from the
   reported fields. ANS=-2 (or -999) counts as FAIL-to-solve
   for the != bars and as not-exp for the = bars.
5. Panics fail their bar; the panic is reported verbatim.

## Blindness statement

The evaluator has NOT read:
- `../compose_adversary/REPORT.md` (adversary predictions)
- `../compose_adversary/adv_witness.zag`,
  `adv_wit_bin`, `adv_wit_full.zag`, `adv_wit_compile.txt`,
  `adv_wit_run1.txt` (witness expected answers)
- Any builder REPORT.md
The evaluator HAS read the adversary PREREG.md sections 1-8
as required by the task (section 5 bars are the adjudication
criteria; section 6 is the protocol). Execution is mechanical:
concat, compile, run 3x, compare bytes, report fields, check
bars. Predictions cannot influence execution.

## Toolchain

Pure Zag. Safebin mandatory: PATH="$HOME/safebin". Verified
before execution: `znc` resolves to /home/hatch/safebin/znc,
byte-identical (cmp) to the pinned builder toolchain binary
$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1.
`python3` does not resolve in safebin PATH.

## Amendment log

(none)
