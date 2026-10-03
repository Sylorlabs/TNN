# PREREG: L3 Red Team vs C281/C284 (L3-REDTEAM)

Status: PREREG-FROZEN 2026-10-02, before any attack implementation.
Any change requires a new prereg; this document is never edited after
freezing. Commit-order self-check: this prereg is committed BEFORE any
attack source, binary, or run log exists.

Worker: L3 Red-Team Worker (subagent, 2026-10-02).

## 1. Target

C281 (XDOMAIN-GRAMMAR-L2M, commits e5b747176/762cda924): claims the
learner created a novel generator intermediate M=[INC R0] (bytes
4,0,0) from generic machinery plus labeled experience, with creation
trace, persistence, reuse, revision. C284 (L3-REPRO-TRANSFER, commits
f843cba55/93df97cb2): independent reproduction (byte-identical) plus
transfer to a new sealed world where the learner built a DIFFERENT
intermediate M'=[ADD R0,R0] (bytes 1,0,0).

Mission: adversarially attack the L3 claim. Find flaws in novelty,
sealed-ness, causal attribution, and robustness. Document every
attack, success or failure. Do NOT modify the C281/C284 directories
(xdomain_grammar_l2m/, l3_repro_transfer/).

## 2. Confirmed target facts (from reading committed source/logs)

- m_construct (glm_learner.zag): greedy hill-climb over (op,d,s)
  appends, 80 candidates/round, first-max tie-break in order
  op 0..4, d 0..3, s 0..3; requires strictly positive gain per round;
  stops at score 2, no positive gain, or 6 instructions. Generic: no
  relation literals, no rule shape (grep audits re-confirmed 0/0/0).
- The TREAT path genuinely calls m_construct via m_ensure; the trace
  C-ROUND line is emitted inside m_construct. install_supplied writes
  bytes (4,0,0) with created=0 and is called only from arm_supplied.
- The C281 TREAT trace shows exactly ONE construction round:
  C-ROUND 1 base=0 win=4,0,0 gain=2 score=2. The whole "creation" is a
  single greedy step.
- solve_z promotes a composition iff r==target (the expected answer).
  The distractor relation 74 yields 5->6, a G1-valid construction,
  rejected only because 6 != 25.
- C281 prereg section 4 and C284 prereg section 4 both contain
  frozen hand-derived expectations giving the EXACT program bytes
  ((4,0,0) and (1,0,0)) and traces before implementation.
- tr_learner.zag is sha256-identical to glm_learner.zag
  (ca1110f65bc13b6bc05ba7bfc086a0f06d9e0323f0288f4126887453d9285e1f).
- The transfer T1 labels mark 25 and 37 (C281's solution outputs)
  invalid, so the old solution scores 0 under T1 by design.

## 3. Attack battery

Audits (source and log evidence, no new builds):

- A1 ORACLE-SELECTION: the rebind "discovery" is exhaustive
  candidate trial with r==target selection. The learner has no
  internal criterion distinguishing distractor 74 from genuine 73;
  5->6 is rule-valid and is rejected only by the answer key.
  Predicted: SUCCESS as a weakening finding (M-origin unaffected;
  the "discrimination, not luck" narrative fails).
- A2 TRANSFER-SEAL: (a) machinery byte-identical, clean of transfer
  literals; (b) transfer prereg pre-derived (1,0,0); (c) T1 labels
  pin C281's solution to score 0. Predicted: SUCCESS as
  characterization: sealed against the OLD solution, but the NEW
  solution was equally worker-pinned in advance; worker-designed,
  not adversarial.
- A3 TRACE-GAMING: could the creation trace be faked by the driver?
  Audit: m_construct emits C-ROUND itself; install_supplied is only
  on the SUPPLIED path; TREAT logs contain no SUPPLIED-INSTALL.
  Predicted: attack FAILS (trace genuine).
- A4 BYTE-RETRIEVAL: is (4,0,0) planted? Grep: the literal appears
  only in the SUPPLIED-INSTALL print line in driver files, never
  written to the M slot on TREAT. Predicted: attack FAILS at byte
  level; but the outcome was hand-derived in advance, so the
  "researcher-pinned argmax" characterization SUCCEEDS.

Empirical variants (H1 stack copies in l3_redteam/, pinned znc,
3 runs each; H1 suffices because m_construct is the shared
mechanism under attack):

- V0 BASELINE: unmodified copy of the C281 H1 stack. Predicted:
  3/3 byte-identical; run-log sha256 equals the committed
  abc3e0182c22f23e73e075549fd977c9f165d6cc000931c4b85f6ba5012ac426.
  Validates the attack harness; any variant deviation is then
  attributable to the patch.
- V1 OP-REMOVAL: learner copy with the op search loop bound 5 -> 4
  (INC unsearchable; basis CPY/ADD/MUL/SET1 only). Predicted:
  C-ROUND 1 base=0 stop, M-BUILD-FAIL score=0, TREAT ARM-RESULT
  FAIL. Shows the learner cannot compose SET1+ADD into a +1
  effect; invention is single-step menu selection over 5 ops.
- V2 TWO-STEP-RULE: driver copy with validity rule G1b (v = D*q+r,
  q in [1,7], r in [2,8]; D+1 invalid, D+2 valid), 18 fresh labels,
  goal target 26 (rule-valid), Z2 target 34. Predicted:
  M-BUILD-FAIL score=0 (no single append gains), TREAT FAIL,
  although [INC R0, INC R0] would score 2/2. Shows the machinery
  cannot cross a zero-gain valley; a minimal rule change destroys
  construction.
- V2S SUPPLIED-CONTROL (same world as V2): installer writes
  [INC R0, INC R0], target 26. Predicted: PASS. Proves the V2 task
  is solvable given M; the blocker is purely the creation step
  (mirror of C281's SUPPLIED diagnostic, resolving to L2 here).
- V3 AMBIGUOUS-LABELS: driver copy with rule G1c (q in [1,7],
  r in [0,7]; both D+1 and 2D valid), labels marking both valid.
  Predicted: C-ROUND 1 win=1,0,0 gain=2 (ADD R0,R0 beats INC R0 by
  op order), M=[ADD R0,R0] score 2/2 created=1, then Z FAIL
  (48 != 25; 48 is rule-valid). Shows a confident WRONG
  intermediate pinned by the researcher's tie-break, not by the
  goal; construction is not goal-directed.
- V4 OPNUM-SWAP: learner copy swapping SET1/INC op codes in m_exec.
  Predicted: C-ROUND 1 win=3,0,0, M bytes (3,0,0), Z solved
  (24->25) but ARM-RESULT FAIL on the p0==4 byte check. Shows the
  kill bar is byte-coupled to arbitrary researcher numbering.
- V5 FACT-ORDER: driver copy inserting (3,73,24) before (3,74,5).
  Predicted: CANDIDATES 73 74 72, 73 promoted on first try, Z PASS,
  distractor never tried. Shows the distractor-first
  "discrimination" narrative is vacuous; the answer key selects
  regardless of order.
- V6 LABEL-SHUFFLE: driver copy with g1_labels insertion order
  reversed. Predicted: run log byte-identical to V0. Expected
  FAILED attack (scoring is order-independent); documents
  robustness.

## 4. Verdict rules

- Each attack is scored SUCCEEDED (predicted flaw manifested) or
  FAILED (target robust on that axis), with evidence.
- Overall: L3-REDTEAM-COMPLETE with the attack ledger. A SUCCEEDED
  attack on M-novelty or sealed-ness weakens or kills the L3 claim;
  SUCCEEDED attacks on robustness bound it; FAILED attacks are
  reported as failed.
- Honest scope: H1 stack only for empirical variants; the
  construction machinery is byte-shared with H2. Expected answers
  remain the harness boundary (as in C281/C284); attacks use them
  only to read out what the machinery selected.

## 5. Build and determinism spec

Pure Zag. Copies only; the C281/C284 directories are never
modified. Pinned znc at
$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1.
No RNG. 3 runs per variant binary; sha256 recorded. 0
modes/bridges/handlers. No em/en dashes in loop documentation.
Paper untouched. Nothing pushed. Commits local on tnn-native-lab
with EXPLICIT pathspecs.
