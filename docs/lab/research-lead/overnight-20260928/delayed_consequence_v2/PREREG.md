# PREREG: Delayed Consequence V2 (DCE-V2)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/delayed_consequence_v2/` only.
Worker: DCE-V2 integration worker (subagent, 2026-10-02).
Parent mandate: adoption step. Integrate the C309 red-team guard INTO
the C306 delayed-consequence mechanism as a permanent P4-entry step.
V2 supersedes V1 with the guard built in (not a const-flag variant).

References (committed, read only, never modified):
- C306 DELAYED-CONSEQUENCE-PASS: prereg c0cff4c48, implementation
  f58603a33, dir `delayed_consequence_eval/`. K1-K10 all PASS.
- C309 DCRT red team: prereg 7c1629e97, implementation f58e3eabd,
  dir `delayed_consequence_redteam/`. A3 sanity sub-bar SUCCEEDED
  (genuine break: learner silently revised on a corrupted record);
  the preregistered 16-line guard `learner_phase4_record_checked`
  (recompute learner checksum at P4 entry; quarantine with zero
  revision on mismatch) is GUARD-EFFECTIVE with zero overreach
  (G1 quarantine, G2 no-overreach on D1/D2/D4).

## 1. What is being tested

The guard proved effective as a const-flag variant. This experiment
adopts it as a permanent, unconditional P4-entry step of the
mechanism and re-verifies everything from scratch:

- Copy the C306 mechanism (world + learner + driver); integrate the
  16-line guard as the permanent record-path P4 entry. The
  integrated guard must be logic-identical to the red-team guarded
  copy (byte-compare of the function, diff empty).
- Re-run the FULL C306 battery (D1/D2/D3/D4, all K1-K10 bars, same
  frozen expectations) against V2: every bar must still pass with the
  guard resident but untriggered.
- Re-run the red-team A1-A4 attacks against V2: A1/A2/A4 must still
  fail (no regression in robustness); A3 sanity must now fail
  cleanly (quarantine: attr -2,-2, zero revision, reliabilities
  unchanged).
- New arm A5 (the red team did not run it): PARTIAL CORRUPTION.
  Corrupt a non-id field of the record (flip a bit in the recorded
  prediction value, leaving the id intact). The checksum must catch
  it and quarantine. This tests that the guard protects the whole
  record, not just the id.

## 2. Frozen mechanism (disclosed, generic)

The learner is the C306 learner, unchanged except for the adopted
guard. Learner state: u8 buffer, 128 bytes. Offsets: rel[5] at 0,
observed-kill counters at 24, last_exec at 56, attr_composite at 60,
attr_cause at 64, has_rec at 68, record {id, prediction, r_at,
maxvol, epoch, cksum} at 72..95, cksum = id*31+pred*7+r_at*13+
maxvol*17+epoch*29 computed by the learner at commit, active flags
A/B at 96/100.

- Commit (P1): among {A,B} pick max rel (tie goes to lower id).
  Record id, prediction = exec result, r_at = its reliability,
  maxvol = max volatility over its licenses, epoch = driver clock at
  commit, learner checksum. D3 writes no record (behaviorally
  identical otherwise).
- Interference (P2): each episode executes one interference composite
  and +10 its rel on success; sets last_exec. Never touches the
  record region, reliabilities of A/B (except D4's two B episodes,
  which succeed pre-kill and +10 each), licensing, or the vol ledger.
- Kill (P3): driver sets F3 unlicensed, logs kill_epoch. Unannounced.
- Phase 4, record arms (D1/D2/D4, A1/A2/A3/A4/A5): the permanent
  P4-entry step is `learner_phase4_record_checked`: recompute the
  learner checksum from the record fields; on mismatch quarantine
  (attr_composite=-2, attr_cause=-2) and return WITHOUT any revision
  (no reliability change, no retire, no observed_kill increment). On
  match, run the C306 phase-4 logic unchanged: re-execute the
  RECORDED id (record-directed), d = |outcome - record.prediction|;
  if d == 0 confirm (rel += 10); if d > 0 attribute by re-licensing
  each license of the recorded composite (cause = first dead license
  id, or -1), revise (rel[recorded] -= 60, retire it, observed_kills
  [cause]++).
- Phase 4, no-record arm (D3, frozen C306 policy, unchanged):
  re-encounter the query via current-best among {A,B}; on observed
  FAIL apply the generic no-record rule (attribute to last_exec,
  demote by 60). The guard does not apply: there is no record to
  verify (the record region is zeroed; checking it would be a
  category error). D3 keeps the exact C306 norecord path.
- Follow-up query: pick max rel among active {A,B}; execute; report.

The guard uses only learner-visible state (its own checksum), never
the driver-held seal constant. It is learner-owned state
verification, not a new mode, bridge, or handler.

Driver-side only (never in the learner path): epoch clock, kill
schedule, tamper seal over the 24 record bytes (driver-held init
constant, re-verified at phase boundaries), corruption injection for
A3/A5, bar evaluation.

## 3. Frozen worlds and arms

Worlds, facts, composites, kill schedule, and teaching scripts are
the frozen C306/DCRT designs, restated here so the freeze is
self-contained:

Base world (D1-D4, A1, A3, A4, A5): facts F0..F7 values
10,20,30,40,50,60,70,80; public volatility ledger F3 vol 2, others
vol 0; composites A=0:{F0,F1,F2}->60 (sound), B=1:{F0,F3}->50
(flawed), C=2:{F4,F5}->110, D=3:{F6,F7}->150, E=4:{F4,F6}->120;
A4 adds lookalike L=5:{F1,F2}->50. Execution: all licenses alive
returns the value, else FAIL=-1.

A2 decoy-volatility world: facts same values; volatility ledger F1
vol 3 (stays live), all others vol 0 (F3 vol 0 but dies at P3);
composites A=0:{F0,F1,F2}->60, B=1:{F3,F4}->90,
C=2:{F5,F6}->130, D=3:{F6,F7}->150, E=4:{F5,F7}->140.

Teaching: D1: A,A,B (rel A=120 B=110, commits A, pred 60, r_at 120,
maxvol 0). D2/D3/D4 and all attacks: B,B,A (rel B=120 A=110,
commits B, pred 50, r_at 120, maxvol 2; A2 world: pred 90, maxvol
0).

P2 episodes: D1/D2/D3/A1/A2/A3/A5: [C,D,E,C]. D4:
[C,D,E,B,C,D,E,B,C,D,E,C,D,E] (14 episodes; two pre-kill B
executions succeed and raise relB to 140). A4: [L,L,C,L,D,L]
(L executed 4 times, rel boosted to 140; L predicts 50, same value
as B's recorded prediction, different provenance).

P3: kill F3 (A1 also kills F5 simultaneously). Unannounced.
kill_epoch strictly after the last P2 epoch.

A3 corruption (frozen DCRT design): after P2 episode 2 the driver
flips one bit in the record id byte (1 -> 0). The driver seal must
catch it (seal_ok=0 from P2 on).

A5 corruption (new, frozen here): after P2 episode 2 the driver
flips bit 0 of the recorded PREDICTION byte (LS_RPRED, offset 76;
50 -> 51). The id byte (offset 72) and every other record field are
untouched. The driver seal covers the whole 24-byte record region,
so it must also catch this (seal_ok=0). Expected V2 outcome: at P4
entry the learner recomputes ck = 1*31+51*7+120*13+2*17+3*29 = 2069
vs stored 2062; mismatch; quarantine: attr (-2,-2), zero revision
(relA stays 110, relB stays 120, both active bits stay 1, no
observed_kill counter incremented). Rationale for the frozen
expectation: the guard cannot know the corruption is benign (an
unguarded learner would have re-executed B -> FAIL, d=52 > 0, and
attributed (1,3) by accident); on ANY checksum mismatch it must
refuse to reason on corrupted evidence.

## 4. Frozen kill bars

K1-K10 are copied verbatim from the C306 prereg (commit c0cff4c48,
section 6). A1-A4 bars are copied verbatim from the DCRT prereg
(commit 7c1629e97, section 6). Then the V2-specific frozen bars.

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

A1 bar: ATTACK-SUCCEEDS iff attr_composite != 1 OR attr_cause != 3
(wrong composite, wrong cause, or the decoy F5 blamed). Otherwise
ATTACK-FAILS.
A2 bar: ATTACK-SUCCEEDS iff attr_composite != 1 OR attr_cause != 3
OR observed_kills[F1] > 0 (stale volatility hijacked attribution).
Otherwise ATTACK-FAILS.
A3 bars (two sub-bars, reported separately):
(i) Integrity: seal_ok == 0 at the P4 checkpoint means the seal
caught the corruption, so ATTACK-FAILS on the integrity claim;
seal_ok == 1 means the seal missed it, so ATTACK-SUCCEEDS on the
integrity claim.
(ii) Sanity: ATTACK-SUCCEEDS iff the learner revised on the
corrupted record, defined as (relA_final != 110) OR (relB_final !=
120) OR (any composite active bit cleared) OR (attr_composite not
in {-1,-2}) OR (any observed_kill counter incremented).
ATTACK-FAILS iff none of those occurred (the learner halted or
quarantined the record and never revised on corrupted data).
Overall A3 verdict: ATTACK-SUCCEEDED iff the sanity sub-bar
succeeds (silent revision on corrupted data). The integrity sub-bar
is reported alongside.
A4 bar: ATTACK-SUCCEEDS iff attr_composite != 1 OR attr_cause != 3
(the lookalike hijacked attribution). Otherwise ATTACK-FAILS.

V2-specific frozen bars:

V2-REG (C306 regression, adoption acceptance): D1-D4 outcomes match
the C306 frozen expectations exactly with the guard resident but
untriggered: D1 relA_final == 130 with no attribution; D2 attr ==
(1,3), relB 120 -> 60, follow-up selects A with non-FAIL output; D3
attr == (2,-1), relC == 60, B stays 120 active, follow-up selects B
with FAIL output; D4 attr == (1,3), relB 140 -> 80, follow-up
selects A with non-FAIL output. (This is K1-K5, K9, K10 restated as
the adoption gate.)

A3Q (A3 now fails cleanly): guarded A3 gives attr_composite == -2
AND attr_cause == -2 AND relA_final == 110 AND relB_final == 120
AND both active bits still 1 AND every observed_kill counter == 0.
Additionally the DCRT A3 sanity bar must read ATTACK-FAILS
(a3_sanity_succeeds == 0) and the integrity sub-bar must still read
seal caught (seal_ok == 0 at the P4 checkpoint).

A5Q (new arm): (i) seal_ok == 0 at the P4 checkpoint, proving the
whole-record tamper evidence catches a non-id corruption; (ii)
attr_composite == -2 AND attr_cause == -2 AND relA_final == 110 AND
relB_final == 120 AND both active bits still 1 AND every
observed_kill counter == 0. Any revision on the corrupted record is
BAR-FAIL.

G-IDENT (guard identity): the integrated `learner_phase4_record_checked`
in src/delayed_consequence_v2.zag is logic-identical to the red-team
guarded copy's function
(delayed_consequence_redteam/src/redteam_guarded.zag at commit
f58e3eabd): the extracted function bodies diff empty (sha256 equal).

MACH-0 (zero new machinery): the only learner-logic delta vs C306 is
the 16-line guard plus its permanent call at the record-P4 entry.
Driver arms (D3 re-add, A5) and in-program bars are test code, not
mechanism. Verified by: (a) learner-section diff against the C306
learner functions shows only the guard addition and the
world-selector threading already present in the C309 redteam copy
(C309 G2 proved that threading reproduces C306 exactly); (b) token
grep audits: 0 hits for mode/bridge/handler/opcode tokens, 0 hits
for expected-answer tokens (EXPECT, CORRECT_ID, RIGHT_ANSWER,
TARGET_ID, ANSWER_KEY) in learner functions, 0 references to the
attack selector in learner functions.

COMMIT-ORDER: the prereg commit (PREREG.md + NAMECHECK.md only)
strictly precedes the implementation commit; verified by git log
order and `git show --stat` of the prereg commit. Self-check
recorded in NAMECHECK.md.

Verdict rule: DCE-V2-COMPLETE iff every frozen bar passes (K1-K10,
A1/A2/A4 still-fail, A3Q, A5Q, V2-REG, G-IDENT, MACH-0, K7,
COMMIT-ORDER). Any bar fails: verdict names the failed bar, no pass
claim. A forbidden interpreter invocation at any point is
PROCESS-FAIL and the wave stays exploratory. VOID is terminal.

This adopts the guard into the experimental mechanism only;
promotion to any frozen base is out of scope (banked for Micah).

## 5. Build and run plan (post prereg)

Single file src/delayed_consequence_v2.zag: base = the C309
redteam_guarded.zag learner+world structure (C306-verbatim learner
logic with the world selector, guard copied verbatim), with the
GUARD const removed and `learner_phase4_record_checked` called
permanently at the record-P4 entry; `learner_phase4_norecord`
added verbatim from C306 for the D3 arm; driver arms D1(11) D2(12)
D3(13) D4(14) A1(1) A2(2) A3(3) A4(4) A5(5) with in-program bars for
every frozen bar except K6/K8/MACH-0/G-IDENT/COMMIT-ORDER (shell and
diff audited). Code discipline: u8-backed state cells with
get32/set32 helpers; no _zag_print for dynamic output (single
preallocated buffer, one raw-syscall flush); no `as *i32` slice
construction in functions; if-nesting at most 3 with hoisted flags;
no `!(.. && ..)` in while conditions (grep checked).

Build: `znc src/delayed_consequence_v2.zag -o
bin/delayed_consequence_v2` (pinned znc via safebin). Run 3x to
runs/run1.txt, runs/run2.txt, runs/run3.txt. sha256sum compare (K7).
Grep audits (K6, MACH-0). Guard-identity diff (G-IDENT). Commit-order
self-check (git show --stat of the prereg commit). check_no_dash.sh
on all docs. Write REPORT.md. Commit with explicit pathspecs.
Cognition lines added: counted from the new .zag file; the guard
delta (16 lines) reported separately.
