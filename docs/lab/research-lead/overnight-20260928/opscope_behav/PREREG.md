# PREREG: OpScope Cross-Context Behavioral Validation (FROZEN)

**Date:** 2026-09-30 (PDT). **Status:** FROZEN. Committed alone before any implementation.

**Lineage:** OPSCOPE-R1R4-PASS (51c54e262 / c60bfbe7a, bounded L2) ->
GATE-STRESS-FAIL (37d4212d / ebd62fe5: Family A confound installs, 5/20) ->
OPSCOPE-DISPLACEMENT-LOAD-BEARING (ae9c3f13e / 54d3e3ca9: position-0 negator
provably uninstallable, positional assumption load-bearing).
This is the FINAL admission-gate experiment in the OpScope lineage per the
2026-09-30 ONE-SYSTEM RULE directive. No further gate variants follow; the
final report answers the standing question on position-independent negation
instead of proposing another gate.

## 1. Design

The six count bars (epc, reclen, sup, mtch-rate, div, zero-parameter gate)
in `proposal_check` are REMOVED as the admission criterion. They are replaced
by cross-context behavioral validation. The DELETION operator semantics
(prefix to DEFAULT, suffix to op-records, residual grounding) are UNCHANGED.
No new operator type, no new semantic case, no new mode, no new bridge.

### 1a. Candidate pre-screen (efficiency only, not admission)

A word w (0..11) is a validation candidate iff it is not already trigger-bound
and has at least one DELETION signature event (dstat[w].mtch > 0) in training.
The signature is the semantic core (scope systematically absent); the pre-screen
does not admit, it only bounds compute. The Family A confound passes the
pre-screen (it is a perfect spoof); admission is decided behaviorally.

### 1b. Admission criterion (all must hold for INSTALL)

For each candidate w, in word-id order 0..11, at end of training (seen=100):

**Step 1 - Tentative grounding.** Copy learner state to scratch. Run the
existing `reground` procedure on the copy with w as trigger. This yields the
tentative operator with no live-state mutation.

**Step 2 - (ii) Held-out non-degradation.** Let V be the frozen held-out set
(episodes 100..119, never trained on; documented limitation: V is also the
final reporting set; the check is relative, not tuned).
- acc_base = TEST_ACC of interpret() on V with the CURRENT live operator table
  (all previously accepted operators, without w).
- acc_with = TEST_ACC of interpret() on V with the tentative w-operator added.
- (ii) PASSES iff acc_with >= acc_base. If (ii) FAILS, w is REJECTED outright
  (no fallback; a degrading operator is never installed).

**Step 3 - (i) Cross-position probe.** Let p* = w's most frequent training
position (ties: smallest). Synthesize one probe: take the first v in V
containing w at p*, keep its target object fixed, move w to p' (p'=0 if p*!=0
else p'=1), recompute the probe target T' with the world oracle on the same
object (counterfactual: same referent, different word order).
- (i) PASSES iff the tentative operator predicts T' correctly on the probe
  AND predicts correctly on every v in V containing w at p*.
- If (i) PASSES: INSTALL with posmask = 0 (unrestricted, position-general).
- If (i) FAILS but (ii) PASSED: go to FALLBACK.
- If (ii) FAILED: REJECT (already decided).

**Step 4 - FALLBACK (explicit positional scope restriction).** Only reachable
when (i) fails and (ii) passes.
- Require single-position correctness: the tentative operator predicts
  correctly on EVERY v in V where w occurs at p*.
- If yes: INSTALL with posmask = (1<<p*) and record the restriction. The
  router (`find_op`) is modified so a restricted operator fires ONLY when its
  trigger occurs at a valid position. The restriction is behavioral, not just
  documentation: outside its validated position the operator does not fire.
- If no: REJECT.

**Step 5 - Real installation.** If accepted, run `reground` on the LIVE state
with w, then set oppos[w_slot] = posmask (0 = general, else restriction).
`oppos[8]` (i32) is the only new learner-state structure.

### 1c. What is NOT changed

- DELETION signature, residual grounding, reground replay: unchanged.
- `interpret`, `baseline`, `learn_keep`, `learn_event`, `learn_update`: unchanged.
- `retire_check`: REMOVED (superseded by pre-installation (ii); the battery has
  no distribution shift during training; documented).
- The six count bars and `gate_pass` as admission: REMOVED.
- `diag_bars`: kept for diagnostics (not admission).

## 2. Frozen families and predictions

All families use the frozen R1R4 world generator lineage with FAM variants.
Seeds: B1=2001, B2=2002, B3=2003. Each family run 3x, byte-identical required.

### Family B1: R1R4 original battery (no regression)

Training: "tak not <color>" NEGs (not at position 1), DIRECT/REL/SIZE as frozen.
Predictions:
- P1: "not" INSTALLS via FALLBACK with posmask=(1<<1). Rationale: (ii) passes
  (acc_with=20/20 >= acc_base=17/20, the F4 ablation reference); strict (i)
  fails (the position-1-grounded DELETION operator cannot handle the
  position-0 probe, as the displacement attack proved); single-position
  correctness holds (T1 3/3 at p*=1).
- P2: "tak" REJECTED. Rationale: the tak-operator (trigger at position 0)
  zeroes DEFAULT via reground and routes everything through mixed op-records;
  (ii) fails (degrades held-out below acc_base).
- P3: No other word installs. Only "not" has mtch>0 among non-tak words with
  a coherent signature; "tak" is rejected per P2.
- P4: TEST_ACC=20/20, T1 (ep 109..111) 3/3, F1=1 (OPREC trig=1, sig=0,
  created>0, sup>=4; T1 3/3), F2=1, F4=1 (ablation: removing operators drops
  T1 and acc), F5=1 (acc>=16, size 3/3). VERDICT: OPSCOPE-R1R4-PASS.
- P5: OPREC for "not" carries posmask=(1<<1); `find_op` skips it when "not"
  is not at position 1 (white-box check).

### Family B2: Gate-stress Family A (confound must be rejected)

Training: R1R4 + grn-NEG spoof block ("tak not grn <color>", grn at position 2).
Predictions:
- P1: "grn" REJECTED. Rationale: (ii) fails decisively. With the "not"
  operator installed (validated first, w=1 before w=4), acc_base=20/20;
  tentatively adding the grn-operator gives acc_with=5/20 (the installed
  confound mispredicts "tak grn sph"/"tak grn cub" where grn is at position 1).
  5/20 < 20/20. No fallback (fallback requires (ii)).
- P2: "not" INSTALLS via FALLBACK with posmask=(1<<1), as in B1/P1.
  (Validated before "grn" in word-id order; its (ii) is computed against the
  no-not-operator baseline.)
- P3: CONFOUND_GRN_INSTALLED=0 (white-box). TEST_ACC=20/20.
  TRUE_NOT_INSTALLED_WHITEBOX=1.
- P4: Probes: PROBE_CONF_NEG ("tak not grn red") 3/3 via not-operator;
  PROBE_HARM_DIRECT ("tak grn cub") 3/3 (no grn-operator to mispredict).
- P5: VERDICT line OPSCOPE-R1R4-PASS (the battery is defended, not attacked).

### Family B3: Displacement ("not tak <color>", not at position 0)

Training: R1R4 with NEG blocks rewritten to "not tak <color>" (FAM=4 lineage).
Predictions:
- P1: "not" INSTALLS via strict (i) with posmask=0 (UNRESTRICTED).
  Rationale: (ii) passes (acc_with=20/20 >= acc_base=17/20; the tentative
  position-0 operator predicts {tak} on all NEG episodes and T1 3/3, and does
  not touch DIRECT/REL/SIZE). Strict (i) passes: the position-0-grounded
  operator carries rich op-records (op_k(tak)={tak}, op_k(color)={tak}, since
  the empty prefix forces R=T); on the synthesized position-1 probe
  ("tak not <color>", same object) it predicts or_default(tak)|op_k(color)
  = {tak}|{tak} = {tak} = T'. This OVERCOMES the Position-0 Lemma blindness:
  the old zero-parameter gate was provably blind (cs==cb); the behavioral
  gate is not.
- P2: TEST_ACC=20/20 (up from the 17/20 no-operator baseline measured in the
  displacement attack). T1 ("not tak grn", ep 109..111) 3/3.
  PROBE_D1 ("not tak red") 3/3, PROBE_D2 ("not tak grn") 3/3.
- P3: TRUE_NOT_INSTALLED_WHITEBOX=1. F4=1 (ablation drops T1 3/3 -> 0/3 and
  acc 20/20 -> 17/20, proving the installed operator causes the gain).
- P4: VERDICT line OPSCOPE-R1R4-PASS.
- P5 (honest scope): the installed operator is correct on this battery
  because every "not" episode is a NEG with T={tak}. The operator implements
  "after not, predict {tak}" via op-records. This is no more degenerate than
  the position-1 operator ("tak not red" -> {tak} via DEFAULT(tak) + deleted
  scope); both delete the color contribution. The claim is bounded L2.

## 3. Kill bars

- K1 (prereg precedence): this prereg is committed ALONE before any
  implementation file exists. Verified by git merge-base --is-ancestor.
- K2 (frozen predictions): 3 families x 3 runs, byte-identical per family.
  PASS requires EVERY prediction P1..P5 in all three families to match as
  frozen above. Any mismatch on any P-item in any family is FAIL. In
  particular: B1 "not" installs ONLY via FALLBACK with posmask=(1<<1)
  (strict (i) must FAIL for it); B2 "grn" REJECTED (no install under any
  route); B3 "not" installs via STRICT (i) with posmask=0 (fallback route
  for it is a FAIL).
- K3 (purity/determinism): pure Zag + shell only, zero Python at every step
  (build, runs, analysis, byte checks via shell-only check_no_dash.sh).
  3/3 byte-identical runs per family (sha256). Exit 0, zero stderr.
  No em/en dashes in docs. Contaminated paper untouched (empty diff).
  u8-backed cells only in new Zag code (no `as *i32` + slice in functions).

## 4. Honest scope (frozen)

- Ceiling: bounded L2. The redesign does not invent operator semantics; it
  changes the admission criterion from distributional to behavioral.
- The (ii) validation set V doubles as the reporting set (documented
  limitation; the check is relative acc_with >= acc_base, not tuned).
- The (i) probe uses the world oracle for the counterfactual target
  (documented limitation; a fully autonomous process would need its own
  validation signal).
- The FALLBACK documents positional restriction explicitly; the old gate's
  positional assumption was hidden. OPSCOPE-R1R4-PASS remains a
  position-contingent L2 result, now with the contingency RECORDED in state
  (posmask) rather than implicit.
- Architecture delta is reported in the results (per ONE-SYSTEM RULE):
  source lines added/removed, new semantic cases (zero new), new modes (zero),
  new bridges (zero), new task-specific handlers, learner-state structures.

## 5. Verdict labels

- All K-bars pass: OPSCOPE-BEHAV-PASS (bounded L2).
- Any K-bar fails: OPSCOPE-BEHAV-FAIL with the failing bar and item named.
