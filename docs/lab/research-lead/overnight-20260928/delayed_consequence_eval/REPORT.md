# REPORT: Delayed Consequence Evaluation (DCE)

Worker: Delayed Consequence Evaluation worker (subagent, 2026-10-02).
Prereg: `delayed_consequence_eval/PREREG.md`, frozen at commit
c0cff4c48 (PREREG.md + NAMECHECK.md only; no implementation existed).
Implementation: `src/delayed_consequence.zag` (558 lines), built with
the pinned znc to `bin/delayed_consequence`.

## Verdict: DELAYED-CONSEQUENCE-PASS (K1..K10 all pass)

The learner committed to a composite, survived interference, took a
delayed unannounced kill, and revised correctly using only its own
recorded prediction as reference. The no-record control failed to
revise, proving the commitment record did the work.

## Per-bar results (frozen bars from PREREG section 6)

K1 commitment ordering: PASS. Seal verified at commit, post-P2,
post-kill, post-P4 in D1/D2/D4; record.epoch (3) equals driver
commit_epoch (3); commit_epoch 3 < kill_epoch 8 (D1/D2/D3) and 18
(D4). Record bytes provably predate the kill.

K2 D4 record survival: PASS. Seal verified after 14 interference
episodes (seal 1117151291, identical to D2 since the record bytes are
identical); phase-4 attribution correct (composite 1, cause fact 3).

K3 correct attribution (D2): PASS. attr_composite=1 (B),
attr_cause=3 (F3). The learner re-licensed B's licenses, found F3
dead, named the right composite and the right cause.

K4 reliability direction: PASS. D1: relA 120 -> 130 (confirm rise).
D2: relB 120 -> 60 (demote), and 60 < relA 110.

K5 D3 contrast: PASS. The no-record variant attributed to composite
C=2 (recency rule), not B; cause unresolved (-1); B stayed active at
rel 120; follow-up query still selected B=1; evaluator execution of
that choice returned FAIL (-1). It failed to revise, as required.

K6 researcher-expected-value audit: PASS. grep over the source for
EXPECT, CORRECT_ID, RIGHT_ANSWER, TARGET_ID, ANSWER_KEY returns 0
hits. Learner revision branches only on record fields and observed
licensing state; the kill schedule never enters the learner path.

K7 determinism: PASS. 3/3 runs byte identical, sha256
bf34bd2e03907e07be68ceacf2cb9a9fad4a1a317104acd2a6ced18b8e276cdd
(runs/run1.txt, run2.txt, run3.txt; cmp clean).

K8 architecture: PASS. 0 new edge/MAP types, opcodes, modes, bridges,
handlers, semantic cases. Standalone file; TNN core untouched
(word-boundary grep for mode/bridge/handler/opcode: 0 hits).

K9 follow-up preference (D2/D4): PASS. Post-revision query selects
A=0 in both arms; executing it returns 60 (not FAIL).

K10 interference non-leakage: PASS. kill_epoch (8/18) strictly after
last P2 epoch (7/17) in all arms; vol ledger and licensing identical
pre/post P2 (leak=0 all arms); no P2 episode altered F0..F3 licensing.

## Commitment and evaluation traces (from runs/run1.txt)

D1 (commit-sound control): teach A,A,B -> relA=120 relB=110. Commit
A: pred 60, r_at 120, maxvol 0, epoch 3, cksum 2067, seal 1132866607.
P2 [C,D,E,C], seal ok. Kill F3 at epoch 8, seal ok. P4: re-exec A ->
60, d=0, confirm, relA=130, no attribution. Follow-up: A, out 60.

D2 (critical arm): teach B,B,A -> relB=120 relA=110. Commit B: pred
50, r_at 120, maxvol 2 (volatility signal recorded but discounted),
epoch 3, cksum 2062, seal 1117151291. P2 [C,D,E,C], seal ok. Kill F3
at epoch 8, seal ok. P4: re-exec recorded B -> FAIL, d=51 vs recorded
50; re-license -> F3 dead; attr (B,F3); relB 120 -> 60; B retired;
observed_kills[F3]=1. Follow-up: A (110 > 60), out 60.

D3 (no-record control): same teaching as D2, commit B behaviorally
but has_rec=0 (no record written). P4: current-best re-exec B ->
FAIL observed; no recorded prediction, no commitment binding;
frozen recency rule demotes last_exec C: relC 120 -> 60; C licenses
alive so cause -1; attr (C,-1). B untouched at 120, still active.
Follow-up: B, out -1 (still broken). Contrast with D2 is exact: the
only difference is the record, and only D2 revised correctly.

D4 (interference-heavy): 14 episodes incl. two pre-kill B executions
(adversarial: relB 120 -> 140). Record survives byte-identical (seal
ok). Kill F3 at epoch 18. P4: attr (B,F3); relB 140 -> 80 < 110;
follow-up A, out 60.

## Key numbers

- Reliability deltas: D1 +10 (120->130); D2 -60 (120->60); D3 B
  unchanged (120); D4 -60 (140->80).
- Attribution correctness: D2 (1,3) correct; D4 (1,3) correct; D3
  (2,-1) wrong target, unresolved cause.
- sha256 (3/3 identical):
  bf34bd2e03907e07be68ceacf2cb9a9fad4a1a317104acd2a6ced18b8e276cdd
- Cognition lines added: 558 (new .zag file; 0 lines changed
  elsewhere).

## Disclosures

1. PREREG section 5 hand-derived table lists D4 reliabilities
   "C=140 D=130 E=130 B=140". The frozen episode script
   [C,D,E,B,C,D,E,B,C,D,E,C,D,E] gives C/D/E each 4 executions, so
   the correct hand derivation is C=140 D=140 E=140 B=140. The
   implementation follows the frozen script exactly; the slip is in
   the prereg's arithmetic gloss, affects no bar (C/D/E values enter
   no kill bar), and is disclosed here rather than amended.
2. D3 trace lines show COMMIT pred=0 / RECORD id=0 pred=0 epoch=0:
   expected, since the no-record variant writes no record
   (has_rec=0); those fields are zeroed state, never read by the D3
   phase-4 path.
3. znc emitted one E0101 lint warning ("multiplying by 1 has no
   effect", attributed to main) on the standard single raw-syscall
   flush idiom also used by probe_budget; warning only, build
   succeeded, stdout bytes verified against the prereg expectations.
4. Seal threat model: tamper-evidence is against accidental
   corruption of the record region by interference episodes
   (driver-held init constant, re-verified at 4 checkpoints), not
   against an adversarial learner; the learner code is frozen and
   shared across arms.

## Interpretation

Delayed evaluation works when the commitment is reified as
learner-owned state: D2 bound a later failure to the specific
earlier commitment (id, prediction, basis) and revised in the right
direction with the right cause, while D3, identical except for the
missing record, could not attribute and kept preferring the broken
composite. The flaw was genuinely non-trivial at commit time (both
candidates executed correctly; only the recorded-but-discounted
volatility signal distinguished them), so the recovery is credited
to the temporal machinery, not to commit-time detection. No harness
expected answer appears anywhere in the learner path (K6).

Commits: prereg c0cff4c48; implementation f58603a33.
Local only, never pushed.
