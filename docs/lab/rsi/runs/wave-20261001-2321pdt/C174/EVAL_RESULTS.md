# EVAL_RESULTS.md: C174 shared tag-61 store validation battery

Lane C174, wave wave-20261001-2321pdt. Frozen prereg PREREG_C174.md
(commit 134af1cb2). Pure Zag, safebin PATH, pinned znc,
`which python3` empty (NAMECHECK.md Step 0).

## Verdict: VALIDATION-PASS

All five frozen kill bars pass. The shared consequence substrate
(C174) is validated as infrastructure on sealed worlds.

## Implementation fix after the seal (disclosed)

After the worlds-seal commit and before the eval run, one
eval-driver change was made: the `C174_EVAL arm=` metadata line
was removed from stdout (arm identity remains in the output
filenames). Reason: kill bar (c) compares whole-output SHA-256
across arms; the arm label is metadata, not a decision channel,
and made the comparison vacuous by construction. No prereg
constant, sealed world, generator, store logic, consumer logic,
or decision logic was changed. The seal (world_sealed.zag hash
e66dab44370eaad23da57cedfef59e202a1f14aec42447addeaec4edad787fc8)
is untouched. This is an implementation fix, not a bar move.

## Bar (a) STORE-SERVES-TWO: PASS

W-REORDER (arm S): 121 sub_note writes, 294 sub_consec reads
(294 reorder reads), 0 reclaims. 6 STRATEGY records (one per
family) and 48 PURSUIT records (one per trial) all created via
the generic sub_note path. Trial order recomputed from
sub_consec reads before every trial.
W-RETIRE (arm S): 28 sub_note writes (all 5 pursuit histories),
30 sub_consec reads (10 retention reads, 15 utility reads).
Victim order computed from sub_consec reads on the same store
instance. By source inspection of the committed c174_sub.zag,
every consumer (sub_reorder, sub_victims, sub_utility) obtains
record offsets exclusively via sub_consec; the eval driver's
arm-S diagnostic field dump feeds no decision.

## Bar (b) BEHAVIOR-CHANGE: PASS

W-REORDER: arm S final order [0 5 1 2 3 4] vs fixed [3 0 5 1 4 2];
total attempts 63 (S) vs 103 (F). The learned order ranks the
two best sealed families first (f0 p=0.90, f5 p=0.75).
W-RETIRE: arm S victims [7 0 1 6 5] vs arm F victims [4 8 3 9 7];
held-out answerability 6/6 (S) vs 3/6 (F). Direction on both
worlds favors the consequence-derived judgments (reported, not
bar-gated).

## Bar (c) ABLATION-CAUSAL: PASS

SHA-256 over full outputs, 3 runs each:
- arm A: de193b844847bd73ef6894fe7745dca424ec2fe5432bdba821042e512cd291ae (x3)
- arm F: de193b844847bd73ef6894fe7745dca424ec2fe5432bdba821042e512cd291ae (x3)
- arm S: 6c33f7c4cca7833ee2b0bc5ed269f0d8c2007d810f9259ced0a4303783f431f8 (x3)
A == F byte for byte on both worlds; S != F on both worlds.
Disabling the store reverts every judgment to the fixed
baseline, exactly mirroring the CONSEQ Link 1 causal pattern.

## Bar (d) MIGRATION-COMPAT: PASS

M1 (node-local slots, Node2-v2 rule verbatim) reproduces the
CONSEQ K-H3 decision trace: M1_KH3_OK 1, trace
30 30 30 30 30 45 guide 45. M2 (shared store, per-value
(value,count,source) records via sub_note, 3-revelation rule
via sub_consec): trace byte-identical, MIGRATION_MATCH 1.
3/3 byte-identical: fce270e621ab9ce8a57e6684ab203c2c8199db1a11da586ed8482b6ee26431d7.

## Bar (e) DETERMINISM: PASS

3/3 byte-identical reruns for eval_S, eval_F, eval_A,
migrate_bin, selftest_bin, gen_bin (hashes above and in
runs/).

## Sealed-world mechanics honored

- Worlds generated once from frozen seed 20261001 after the
  implementation commit; hashes committed (WORLD_MANIFEST.md)
  before any eval binary ran.
- Draw tables precomputed so every arm faces the identical
  world regardless of attempt order.
- src_self noise (20 percent of trials) correctly excluded
  from family rates (white-box: FAM 5 rate 800 = 4/5 taught,
  self confirmations not counted as evidence, spec 7.1).
- Abandonment lifecycle fired on the sealed histories:
  pursuit 101 ABANDONED (4 consecutive failures), pursuit 104
  ABANDONED then RE-ENGAGED (F,F,F,S).

## White-box self test

selftest_bin 3/3 byte-identical
(0e8617cc668b84176dbf71f5095c496d53c0aedcd31e6cda0e89c507c89e8fff),
SELFTEST_OK: write/read, success reset of consec_fail,
src_self exclusion, abandonment plus re-engagement,
stalest-first reclamation, reorder with exclusion, utility
formula (760 for the 4-succ/1-fail fixture).

## Honest scope (what this does NOT establish)

- Dev harness, not TNN-2 integration: the store is validated
  as infrastructure, not as a running TNN-3 component.
- Reclamation is implemented per spec 6.2 but exercised only
  in the self test (the battery never fills the store).
- ABANDON_BOUND, utility weights, MINATT, NEUTRAL_PRIOR, and
  the fixed order are researcher-set scaffolding, honestly
  labeled, not learner-owned.
- Migration boundary (prereg section 5): per-value counters
  and the shift register coincide only on worlds without
  interleaved divergent revelations; the K-H3 world has none.
- No claim about L3, FW1-FW9, general intelligence, or the
  final TNN-3 architecture. C174 moves from EMERGES
  (exploratory) to validated infrastructure on the frozen
  bars; broader generality remains untested.

## Commits (local only, never pushed)

- 134af1cb2 PREREG_C174 FROZEN (kill bars a-e, seal procedure)
- b5e0274f7 IMPLEMENT shared tag-61 store + eval harness
- 0096b30ca SEAL worlds (hashes before any eval run)
- (this commit) eval outputs, EVAL_RESULTS.md, JUDGE_BRIEF.md

## Evidence paths

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/C174/PREREG_C174.md
- Sources: c174_sub.zag, c174_gen.zag, c174_eval.zag,
  c174_migrate.zag, c174_selftest.zag, armflag_*.zag, build.sh
- Seal: world_sealed.zag, WORLD_MANIFEST.md
- Outputs: runs/eval_{S,F,A}_{1,2,3}.txt, runs/migrate_{1,2,3}.txt,
  runs/selftest_{1,2,3}.txt
