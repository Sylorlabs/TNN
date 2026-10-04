# PREREG: Delayed Consequence Red Team (DCRT)

Status: PREREG-FROZEN. No attack implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/delayed_consequence_redteam/` only.
Worker: Delayed Consequence red team worker (subagent, 2026-10-02).
Parent mandate: red team ledger C306 DELAYED-CONSEQUENCE-PASS
(prereg c0cff4c48, implementation f58603a33). Attack the temporal
credit assignment machinery: tamper-evident commitment record,
delayed consequence, attribution, revision.

## 1. What is being tested

C306 proved the learner commits to a composite, survives
interference, takes a delayed unannounced kill, and revises using
only its recorded prediction as reference. Four preregistered
attacks probe the machinery's failure modes. The learner under test
is the EXACT C306 learner (learner_commit, learner_phase4_record,
learner_phase4_norecord, learner_followup) copied verbatim from
commit f58603a33, sha256
af3915aa66d935f6d848d456e64d25651ed1df9b691e71082b0510a33ff502a9.
The redteam driver supplies new frozen worlds and phase scripts; the
learner code path is unchanged in the unguarded binary.

Verdict per attack against the frozen bars in section 6. No global
claim. A forbidden interpreter invocation at any point is
PROCESS-FAIL and the wave stays exploratory. VOID is terminal.

## 2. Frozen base world (attacks A1, A3, A4 and controls D1/D2/D4)

Facts F0..F7, values 10,20,30,40,50,60,70,80. Public volatility
ledger: F3 vol 2, all others vol 0. All facts licensed (alive) at
start. Composites (id: licenses, execution value):
A=0:{F0,F1,F2}->60 (sound), B=1:{F0,F3}->50 (flawed),
C=2:{F4,F5}->110, D=3:{F6,F7}->150, E=4:{F4,F6}->120.
A4 adds lookalike L=5:{F1,F2}->50 (same prediction value as B,
different provenance). Execution: all licenses alive returns the
value, else FAIL=-1. Current licensing is learner-observable via
lic(); the kill schedule is driver-held and hidden.

## 3. Frozen A2 world (decoy volatility)

Facts F0..F7, values 10,20,30,40,50,60,70,80. Public volatility
ledger: F1 vol 3 (stays live), all others vol 0 (F3 vol 0 but dies
at P3). Composites: A=0:{F0,F1,F2}->60 (sound; carries the
high-volatility fact F1, which stays live), B=1:{F3,F4}->90
(flawed; F3 was historically stable with vol 0 but dies),
C=2:{F5,F6}->130, D=3:{F6,F7}->150, E=4:{F5,F7}->140. The volatility
prior points at the WRONG candidate (A looks risky, B looks safe);
the P3 consequence must dominate the prior.

## 4. Frozen attack designs

Common learner state, record layout, reliability dynamics, seal
function, and epoch discipline are copied from C306 and unchanged.
Teaching: B,B,A gives relB=120 relA=110 and commits B in every
attack arm (D1 control uses A,A,B and commits A). Commit records
{id, prediction, r_at, maxvol, epoch, learner checksum} exactly as
in C306.

A1 CONFOUNDED KILL. World: section 2. Teaching B,B,A, commit B
(pred 50, maxvol 2). P2: [C,D,E,C]. P3: kill F3 AND F5
simultaneously. Only F3 is load-bearing for the committed composite
B (F5 licenses only interference composite C). The correct answer is
determinable from the licensing chain: re-licensing B finds exactly
one dead license, F3; F5 is outside B's chain. Expected honest
outcome: attr (B=1, F3=3), relB 120->60, B retired,
observed_kills[F3]=1.

A2 DECOY VOLATILITY. World: section 3. Teaching B,B,A, commit B
(pred 90, maxvol 0). P2: [C,D,E,C]. P3: kill F3 (vol 0, dies;
F1 vol 3 stays live). Correct behavior: revise against the
actually-dead fact F3, not the stale-volatility fact F1. Expected
honest outcome: attr (B=1, F3=3), relB 120->60, B retired,
observed_kills[F3]=1, observed_kills[F1]=0.

A3 RECORD CORRUPTION. World: section 2. Teaching B,B,A, commit B
(pred 50). P2: [C,D], then the driver flips ONE bit in the record
region (record id byte 1->0, i.e. B becomes A), then [E,C]. P3:
kill F3. The seal threat model under test is exactly the disclosed
one: accidental corruption of the record region by interference, not
an adversarial learner. The driver seal checkpoint at P4 must catch
it (seal_ok=0). The learner under test never verifies its own
checksum in P4. Expected unguarded outcome: the learner re-executes
corrupted id 0 (A)->60 vs recorded pred 50, d=10>0, re-licenses A
(all alive, cause -1), demotes relA 110->50, retires A, attr (0,-1);
broken B stays 120 active; follow-up picks B and fails.

A4 TARGETED INTERFERENCE. World: section 2 plus L=5. Teaching
B,B,A, commit B (pred 50). P2 engineered for lookalikes:
[L,L,C,L,D,L] (L executed 4 times, rel_L boosted to 140; L predicts
50, same value as B's recorded prediction, different provenance
{F1,F2} vs {F0,F3}). P3: kill F3. Expected honest outcome: the
ID-bound record resists the value lookalike; attr (B=1, F3=3),
relB 120->60, B retired.

Controls (guarded binary only, section 7): D1, D2, D4 rerun exactly
as in C306 (same teaching, same P2 scripts, same single F3 kill) to
prove the guard does not overreach.

## 5. The preregistered guard (applies only if an attack succeeds)

If any attack SUCCEEDS, the minimal learner-side guard is:
at the entry of learner_phase4_record, recompute the learner
checksum ck = rid*31+pred*7+r_at*13+maxvol*17+epoch*29 from the
record fields and compare it to the stored LS_RCK. On mismatch,
quarantine: set attr_composite=-2, attr_cause=-2, and return WITHOUT
any revision (no reliability change, no retire, no observed_kill
increment). This uses only learner-visible state (its own checksum),
never the driver-held seal constant. Rationale: the C306 seal is
driver-side and the driver takes no action on seal_ok=0, so a
corrupted record flows silently into revision; the learner's own
checksum already exists but is never verified, so verifying it is
the minimal fix inside the threat model (accidental corruption).

## 6. Frozen bars

Per-attack verdicts. ATTACK-SUCCEEDS means the red team broke the
mechanism on that vector; ATTACK-FAILS means the mechanism resisted.

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

Guard-test bars (evaluated only if A3 sanity succeeds, on the
guarded binary):
G1 (attack now fails): guarded A3 gives attr_composite == -2 AND
attr_cause == -2 AND relA_final == 110 AND relB_final == 120 AND
both active bits still 1 AND every observed_kill counter == 0.
G2 (no overreach): guarded D1 gives relA_final == 130; guarded D2
gives attr == (1,3), relB_final == 60, follow-up selects A with
non-FAIL output; guarded D4 gives attr == (1,3), relB_final == 80,
follow-up selects A with non-FAIL output. These match the C306
frozen expectations exactly.
Guard verdict: GUARD-EFFECTIVE iff G1 and G2 both hold.

## 7. Build and run plan (post prereg)

Two binaries from one source file src/redteam.zag (world variants +
attack arms A1..A4 + controls D1/D2/D4 + in-program bars; learner
functions copied verbatim from C306; the guard gated by
`const GUARD:i32=0`):
- bin/redteam: built as-is (GUARD=0, unguarded). Runs A1..A4.
- bin/redteam_guarded: built from a sed copy with GUARD=1. Runs
  A1..A4 (guard behavior on attacks) and D1/D2/D4 (no-overreach
  controls).
Build: `znc src/redteam.zag -o bin/redteam` (pinned znc via
safebin). Run each binary 3x to runs/ (run1..3.txt,
guarded_run1..3.txt). sha256sum compare per binary; 3/3 byte
identical required. In-program bars print per-attack ATTACK bars
and G1/G2. Write REPORT.md with per-attack verdicts against the
section 6 bars, guard proposal with control results, cognition
lines touched (new .zag lines; guard delta lines). Commit with
explicit pathspecs. Cognition lines added: counted from the new
.zag file; the guard delta counted separately.
