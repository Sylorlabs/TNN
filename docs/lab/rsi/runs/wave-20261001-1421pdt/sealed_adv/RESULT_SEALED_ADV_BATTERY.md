# RESULT: Post-Freeze Sealed Adversarial Battery on TNN-2 (wave-20261001-1421pdt)

**Battery:** sealed_adv, 9 worlds across 3 mechanism families.
**Prereg:** SEALED_BATTERY_PREREG.md, SHA-256
`b5d54f4d92585840febf58e875a8e6aff0e23a0c88b795faa5bed002c6de8590`,
recorded 2026-10-01 21:41:47 UTC, before any world file existed
(world files first created 21:42:55 UTC). Prereg hash re-verified
unchanged after the battery. No commits made (standing instruction);
freeze ordering by hash plus filesystem timestamps.

**Frozen target:** tnn2.zag `a29972ca...8bd`, freeze_shim2_bin
`9217054c...54`, znc `498abcb5...58ef` (all re-verified post-battery;
git status clean on cognition paths).

**Verdict: all three mechanisms FAIL the sealed battery.**
M1 FAILS (K-S5, K-S6, K-S7). M2 FAILS (K-S8, K-S9, K-S10).
M3 FAILS (K-S11, K-S12, K-S13).
All process bars PASS (K-S1, K-S2, K-S3, K-S4, K-S14, K-S15).
No L3 claim is available on any outcome (Criterion 0 not met; see
prereg section 7, binding).

## Per-world results

### M1: runtime executable-graph construction

**M1-W1 (novel P-then-Q composition):** 0/8 composition probes correct
(all ANSWER -2); 0/4 decoy probes return the consistent majority (all
return the memorized swapped values 40802/40801/40804/40803).
White-box: zero MAPs for subjects 40106/40107; 8 UNCERT nodes for the
misses. K-S5 FAIL.

**M1-W2 (backward traversal):** 2/2 forward engagement probes correct
(MAPs promoted with LITS 41012/41013/41014 and 41022/41023/41024);
0/4 backward probes correct (all -2); 2/2 collateral. K-S6 FAIL.

**M1-W3 (shared-step composition):** 1/1 engagement; 0/3 composition
(all -2); 2/2 collateral. K-S7 FAIL.

**M1 verdict: FAILS.** The trial loop constructs only forward data-path
chains from observed facts. It has no procedure abstraction (M1-W1),
no direction inversion (M1-W2), and no step identity for sharing
(M1-W3). All three failures share one architectural cause: construction
is path-following over the fact graph, not procedure synthesis.

### M2: learner-originated uncertainty to action

**M2-W1 (interactive informant):** Engagement PASS (INQ ACTs after
ANSWER -2). 0 of 8 inquiry ACTs targeted informant A (all CHOICE 30,
mapped to NONE); 0 targeted C. 0/4 final hidden probes correct (all
-2). Budget 8/8 respected. K-S8 FAIL.

**M2-W2 (stale guide):** Validity ACT (pre-resolution) = 30. Bar ACT
(post-resolution, 44101 in context) = 30, not 0. 2/2 collateral.
K-S9 FAIL. The guide for 44101 persists after the uncertainty is
resolved; no resolution transition exists.

**M2-W3 (action content):** 3/3 miss QUERYs yield -2 (validity). The
three episode CHOICEs are 30, 30, 30 (not pairwise distinct). 2/2
collateral. K-S10 FAIL. The guide action is the constant 30 regardless
of what is unknown.

**M2 verdict: FAILS.** The mechanism emits an undifferentiated inquiry
signal (30) whenever a guide's subject is in context. It cannot
discriminate informants (M2-W1), retire resolved guides (M2-W2), or
encode what is unknown in the action (M2-W3). All three share one
cause: the L3 link is a hardcoded constant and the L6 link is absent.

### M3: counterexample-driven revision

**M3-W1 (singleton vs systematic):** Promotion 4/4. Systematic 3/3
(x+5 incorporated). Singleton probe FAIL (returned 42110, the
uncorrected noise, not the original law 42104). Generalization 0/2
(-2 on unseen subjects). White-box PASS (4 MAPs with revised literals
42110/42107/42108/42109). Interference 6/6. K-S11 FAIL.

**M3-W2 (double revision):** Promotion and first-revision probes
correct (43103, 43109). Second-contradiction probe FAIL (returned
43109, not 43119). White-box: MAP ans=43109, LITS 43102/43109
(the first revision's literal; the second contradiction silently
no-oped). 2/2 collateral. K-S12 FAIL.

**M3-W3 (reverted revision):** Promotion probes correct (43703).
Post-revert probe FAIL (returned 43703, not 43713). White-box: MAP
ans=43703, LITS 43703 (unchanged; the revert left the stale taught
fact, which short-circuits relearning). 2/2 collateral. K-S13 FAIL.

**M3 verdict: FAILS.** The operator is last-write-wins literal
patching: it incorporates noise as readily as signal (M3-W1), cannot
revise twice on one link (M3-W2), and a failed revision vetoes
recovery (M3-W3). All three share one cause: revision has no evidence
model and no representation of the law beyond the patched instance.

## Process bars

- K-S1 (prereg ordering): PASS. Hash recorded before world generation;
  mtime order verified; hash unchanged post-battery.
- K-S2 (determinism): PASS. All 9 world transcripts byte-identical
  across 3 runs per block (sha256 equality).
- K-S3 (frozen binary): PASS. Shim hash verified before each block
  and after the battery; tnn2.zag hash unchanged; git clean.
- K-S4 (seal integrity): PASS. World files match generation manifest.
  Anti-smuggling grep over frozen cognition sources finds exactly one
  token in 40000-49999: the integer 41024 in `fn eoff`
  (`return 41024+e*16`), a pre-freeze edge-block byte-offset constant
  (64 + 1024*40), present in the frozen commit, used only for address
  arithmetic, never as a world id. No battery id token appears in
  source. Documented here as a known benign match; the bar's
  anti-smuggling intent (no smuggled world ids) is satisfied.
- K-S14 (retention): PASS. 12/12 collateral probes correct (100%,
  bar 75%).
- K-S15 (no-leak): PASS. Zero correct ANSWERs on novel-key probes
  coinciding with cross-world taught values; all novel probes
  returned -2.

## Failure clustering (no-patch-treadmill)

The nine failures cluster into three architectural causes, one per
mechanism, each falsifying the mechanism's generality claim:

1. **M1: construction without abstraction.** The trial loop is a
   path-finder over observed facts, not a procedure constructor. It
   cannot compose (W1), invert (W2), or share steps (W3) because it
   has no representation of a procedure distinct from the facts that
   demonstrated it.

2. **M2: signaling without content or lifecycle.** The inquiry
   pathway emits one constant action and never retires guides. It
   cannot select informants (W1), forget resolved uncertainties (W2),
   or discriminate what is unknown (W3) because the guide carries no
   content and the architecture has no resolution transition.

3. **M3: patching without an evidence model.** Revision overwrites
   literals on contradiction with no counting, no generalization,
   and no recovery from failed patches. It incorporates noise (W1),
   stalls on second contradiction (W2), and blocks relearning after
   revert (W3) because there is no representation of evidential
   support or law structure.

These are not nine requests for nine patches. They are evidence that
the frozen core lacks: (a) a learner-owned procedure representation
separable from demonstration facts; (b) a content-bearing, lifecycle-
managed uncertainty signal; (c) an evidence-weighted revision
operator. Any TNN-3 proposal should address these as general
substrate gaps, with at least three structurally different hypotheses
per bottleneck, before new mechanisms are added.

## Artifacts

- Prereg: SEALED_BATTERY_PREREG.md
- Worlds: m1w1_world.txt, m1w2_world.txt, m1w3_world.txt,
  m2w1_template.txt, m2w1_truths.txt, m2w2_world.txt, m2w3_world.txt,
  m3w1_world.txt, m3w2_world.txt, m3w3_world.txt
- Tools (Zag source + binaries): sealed_score.zag, score_m2w1.zag,
  inspect_state.zag
- Driver: m2w1_driver.sh
- Transcripts: m1_run{1,2,3}_w{1,2,3}.txt, m2_run{1,2,3}_w{2,3}.txt,
  m2w1_trans_run{1,2,3}.txt, m2w1_log_run{1,2,3}.txt,
  m2w1_world_run{1,2,3}.txt
- Final states: m1_state_run1.bin, m2_state_run1.bin,
  m3_state_run1.bin (run1; runs 2/3 were transient)
