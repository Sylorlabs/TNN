# PREREG: Delayed Consequence Evaluation (DCE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/delayed_consequence_eval/` only.
Worker: Delayed Consequence Evaluation worker (subagent, 2026-10-02).
Parent mandate: Micah priority 5, internal verification. Reduce
dependence on harness-supplied expected answers; prefer learner
commitment, later world consequence, learner-owned evaluation.

## 1. What is being tested

Prior waves proved the learner can choose probe inputs and score its
own predictions at probe time. The untested dimension is TEMPORAL: a
consequence that arrives LATER, after intervening episodes, requiring
credit assignment back to an earlier commitment. Four phases:

- P1 COMMITMENT: the learner answers a query by committing to one of
  two candidate composites and writes a tamper-evident record into
  learner state: composite id, its prediction, its reliability basis.
- P2 INTERFERENCE: unrelated episodes run. They must not corrupt the
  record and must not leak the world's kill schedule.
- P3 CONSEQUENCE: the world kills a load-bearing fact, unannounced.
  The committed composite now fails on re-execution.
- P4 LEARNER-OWNED EVALUATION: the learner compares the outcome
  against its RECORDED prediction, attributes the discrepancy to the
  specific commitment and cause, and revises. All scoring uses the
  learner's own prior prediction as reference, never a researcher
  expected value.

Arms: D1 commit-sound control (consequence confirms, reliability
rises); D2 commit-flawed critical arm (consequence contradicts,
learner must revise correctly); D3 no-attribution control (learner
variant WITHOUT the commitment record must fail to revise correctly,
proving the record did the work); D4 interference-heavy (14
intervening episodes; record must survive and attribution still work).

## 2. Frozen world

Facts F0..F7, values and public volatility ledger (past kill counts,
learner-readable; the FUTURE kill schedule is driver-held and hidden):

F0=10 vol 0, F1=20 vol 0, F2=30 vol 0, F3=40 vol 2,
F4=50 vol 0, F5=60 vol 0, F6=70 vol 0, F7=80 vol 0.

All facts licensed (alive) at start. Kill schedule (frozen, hidden
from the learner): exactly one kill, fact F3, at the P3 boundary. No
kills or re-teaches during P2.

Composites (id: licenses -> execution value):
- A=0: {F0,F1,F2} -> 60. Sound: all licenses stable (vol 0).
- B=1: {F0,F3} -> 50. Flawed: leans on F3 (vol 2, will be killed).
- C=2: {F4,F5} -> 110. D=3: {F6,F7} -> 150. E=4: {F4,F6} -> 120.
  Interference-only composites.

Execution: if every license is alive, return the value; else return
FAIL = -1. Current licensing state is learner-observable via lic();
the future schedule is not.

## 3. Why the flaw is non-trivial (disclosed)

At commit time BOTH candidates execute successfully: A gives 60, B
gives 50, all licenses live. The flaw is NOT detectable from current
licensing state. The only warning is the reliability-relevant signal:
F3 has vol 2 in the public ledger. The frozen commit policy picks the
max experienced reliability among {A,B} and does not penalize
volatility, so in D2/D3/D4 teaching makes B preferred honestly: B
succeeded twice (r 100->110->120), A once (r 100->110). The learner
records the vol signal in its basis field (it noticed) but discounts
it (past success weighs more). A learner that could see the future
would avoid B; the frozen learner cannot. The experiment therefore
tests exactly the delayed-evaluation machinery, not commit-time
detection. If the flaw were trivially detectable at commit time this
design would test nothing; the prereg asserts it is not.

## 4. Frozen learner mechanism (disclosed, generic)

Learner state: u8 buffer. Per-composite reliability rel[5] (init 100,
success +10, confirm +10, demote -60). Active mask (all start
active). Observed-kill counters per fact (init 0). last_exec id.
Attribution fields (attr_composite init -1, attr_cause init -1).
Commitment record region (D1/D2/D4 only): {id, prediction, r_at,
maxvol, epoch, cksum} where cksum = id*31+pred*7+r_at*13+maxvol*17+
epoch*29, computed by the learner at commit.

- Commit (P1): among {A,B} pick max rel (tie -> lower id). Record id,
  prediction = exec result, r_at = its reliability, maxvol = max vol
  over its licenses, epoch = driver clock at commit. D3 writes no
  record (behaviorally identical otherwise).
- Interference (P2): each episode executes one interference composite
  and +10 its rel on success; sets last_exec. Never touches the
  record region, reliabilities of A/B (except D4's two B episodes,
  which succeed pre-kill and +10 each), licensing, or the vol ledger.
- Kill (P3): driver sets F3 unlicensed, logs kill_epoch. Unannounced.
- Phase 4, record arms (D1/D2/D4): re-execute the RECORDED id
  (record-directed, not current-best-directed). d = |outcome -
  record.prediction|. If d == 0: confirm, rel += 10. If d > 0:
  attribute by re-licensing each license of the recorded composite;
  cause = first dead license id (or -1 if none). Revise: rel[recorded]
  -= 60, retire it (clear active bit), observed_kills[cause]++.
- Phase 4, no-record arm (D3, frozen policy): re-encounter the query
  via current-best among {A,B} (B, rel 120). On observed FAIL it has
  no recorded prediction to compare against and no commitment
  binding, so it applies the generic no-record rule: attribute to the
  most recently executed composite (last_exec = C) and demote it by
  60; re-license C's licenses (all alive) so cause = -1 (unresolved).
  B is untouched and stays preferred.
- Follow-up query: pick max rel among active {A,B}; execute; report.

Driver-side only (never in the learner path): epoch clock, kill
schedule, tamper seal = fnv1a(record bytes, driver SECRET const) taken
at commit and re-verified at every phase boundary, bar evaluation.

## 5. Frozen episode scripts and exact arithmetic

Teaching: D1: A,A,B -> rel A=120 B=110. D2/D3/D4: B,B,A -> rel B=120
A=110. Commit: D1 -> A (pred 60, r_at 120, maxvol 0). D2/D3/D4 -> B
(pred 50, r_at 120, maxvol 2).

P2 episodes: D1/D2/D3: [C,D,E,C] -> rel C=120 D=110 E=110,
last_exec=C. D4 (14): [C,D,E,B,C,D,E,B,C,D,E,C,D,E] -> rel C=140 D=130
E=130 B=140, last_exec=E.

P3: kill F3. kill_epoch strictly after last P2 epoch.

P4 expected: D1: exec(A)=60, d=0, rel A=130, no attribution.
D2: exec(B)=-1, d=51, licenses {F0 alive, F3 dead} -> attr (B,F3),
rel B=60, B retired, obs_kills[F3]=1. Follow-up: A (110 > 60),
exec=60 ok.
D3: exec(B)=-1 observed; recency -> demote C: rel C=60; C licenses
alive -> cause -1; attr (C,-1); B stays 120 active; follow-up: B;
evaluator exec(B) = -1 (still broken).
D4: like D2 with rel B 140->80; follow-up A (110 > 80).

## 6. Frozen kill bars

K1 commitment ordering: seal verifies at commit, post-P2, post-P3,
post-P4 checkpoints; record.epoch equals driver commit_epoch; and
commit_epoch < kill_epoch. (D1/D2/D4)
K2 D4 record survival: seal verifies after 14 interference episodes,
record bytes unchanged across P2, and D4 phase-4 attribution is
(B,F3).
K3 correct attribution (D2): attr_composite == B and attr_cause == F3.
K4 reliability direction: D1 rel_A(final)=130 > rel_A(commit)=120;
D2 rel_B(final)=60 < rel_B(commit)=120 and < rel_A(final)=110.
K5 D3 contrast: D3 attr names C (not B); B still active; follow-up
choice == B; evaluator execution of the follow-up choice == FAIL.
K6 researcher-expected-value audit: grep of learner functions for
EXPECT, CORRECT_ID, RIGHT_ANSWER, TARGET_ID, ANSWER_KEY returns zero
hits; learner revision branches only on record fields and observed
licensing.
K7 determinism: 3 full binary runs byte identical (sha256 equal,
shell verified).
K8 architecture: 0 new edge/MAP types, opcodes, modes, bridges,
handlers, semantic cases; standalone file, TNN core untouched
(verified by inspection and token grep).
K9 follow-up preference (D2/D4): post-revision query selects A and
executing it does not return FAIL.
K10 interference non-leakage: driver log shows kill_epoch after the
last P2 epoch; vol ledger and licensing (except the P3 kill) are
identical pre/post P2; no P2 episode touches F0..F3 licensing.

Verdict rule: K1..K10 all pass gives DELAYED-CONSEQUENCE-PASS. Any
bar fails: verdict names the failed bar, no pass claim. A forbidden
interpreter invocation at any point is PROCESS-FAIL and the wave
stays exploratory. VOID is terminal.

## 7. Build and run plan (post prereg)

Single file src/delayed_consequence.zag (world + learner + driver +
single raw-syscall flush; u8 state cells with get32/set32 helpers;
no _zag_print for dynamic output; no `as *i32` slice construction in
functions; if-nesting at most 3; no `!(.. && ..)` in while
conditions). Build: `znc src/delayed_consequence.zag -o
bin/delayed_consequence`. Run 3x to runs/run1.txt, runs/run2.txt,
runs/run3.txt. sha256sum compare. Grep audits K6/K8. Write REPORT.md.
Commit with explicit pathspecs. Cognition lines added: counted from
the new .zag file.
