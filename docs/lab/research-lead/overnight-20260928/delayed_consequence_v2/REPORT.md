# REPORT: Delayed Consequence V2 (DCE-V2)

Worker: DCE-V2 integration worker (subagent, 2026-10-02).
Prereg: `delayed_consequence_v2/PREREG.md`, frozen at commit
e5e350bb0 (PREREG.md + NAMECHECK.md only; no implementation existed
at that commit).
Implementation: `src/delayed_consequence_v2.zag` (714 lines), built
with the pinned znc to `bin/delayed_consequence_v2`. Runs in
`runs/run1.txt`, `runs/run2.txt`, `runs/run3.txt`.

## What was built

Single-file mechanism per the frozen build plan (PREREG section 5).
Base is the C309 `redteam_guarded.zag` learner plus world structure
(C306 verbatim learner logic with the world selector threaded), with
the GUARD const removed and `learner_phase4_record_checked` called
permanently at the record-P4 entry. `learner_phase4_norecord` added
for the D3 arm (C306 policy, world selector threaded as in the C309
copy). Driver arms: D1(11) D2(12) D3(13) D4(14) A1(1) A2(2) A3(3)
A4(4) A5(5). A5 corruption (new, driver side): after P2 episode 2 the
driver flips bit 0 of the recorded prediction byte (LS_RPRED, offset
76; 50 becomes 51); the id byte and every other record field are
untouched. In-program bars cover every frozen bar except K6, K8,
MACH-0, G-IDENT, COMMIT-ORDER, which are shell and diff audited and
reported here.

## Verdicts per frozen bar

K1 PASS (in-program k1=1): record arms D1/D2/D4 verify the seal at
the commit, post-P2, post-P3, and post-P4 checkpoints; record epoch
equals the driver commit epoch; commit epoch strictly precedes the
kill epoch.

K2 PASS (in-program k2=1): D4 seal verifies after 14 interference
episodes (record bytes unchanged across P2); D4 phase-4 attribution
is (B,F3).

K3 PASS (in-program k3=1): D2 attr_composite == 1, attr_cause == 3.

K4 PASS (in-program k4=1): D1 relA 120 -> 130; D2 relB 120 -> 60,
below relA final 110.

K5 PASS (in-program k5=1): D3 attr names C (attr_c == 2, attr_f ==
-1, not B); B still active (act1 == 1); follow-up choice == B;
evaluator execution of the follow-up choice == FAIL.

K6 PASS (shell audit): grep of the learner functions for EXPECT,
CORRECT_ID, RIGHT_ANSWER, TARGET_ID, ANSWER_KEY returns zero hits.

K7 PASS (shell verified): 3 full binary runs byte identical
(sha256 equal, cmp clean). sha256 of each run:
83ada7719cf793ac32ec8ced78ae0f70881420c27e1c97fba84544480f2f9804

K8 PASS (shell audit): 0 hits for mode/bridge/handler/opcode tokens
in the learner functions; standalone file; TNN core untouched (the
only files added or changed are inside
`delayed_consequence_v2/`; reference dirs read only).

K9 PASS (in-program k9=1): D2 and D4 follow-up queries select A and
executing A does not return FAIL.

K10 PASS (in-program k10=1): all 9 arms show p2_leak == 0 and
kill_epoch strictly after the last P2 epoch; vol ledger and
licensing identical pre/post P2.

A1 PASS, ATTACK-FAILED (in-program a1_succeeds=0): attr (1,3).
Confounded F5 death never entered the attribution path. No
regression in robustness.

A2 PASS, ATTACK-FAILED (in-program a2_succeeds=0): attr (1,3),
observed_kills[F1] == 0. Stale volatility did not hijack
attribution. No regression in robustness.

A3 PASS (two sub-bars, reported separately):
(i) Integrity: seal caught the corruption (seal_ok == 0 at the P4
checkpoint; in-program a3_seal_caught=1), so ATTACK-FAILS on the
integrity claim.
(ii) Sanity: the learner did NOT revise on the corrupted record
(in-program a3_sanity_succeeds=0), so ATTACK-FAILS on the sanity
claim.
Overall A3: ATTACK-FAILED. The C309 genuine break is closed by the
permanent guard.

A4 PASS, ATTACK-FAILED (in-program a4_succeeds=0): attr (1,3). The
lookalike L (rel 140, same value 50) did not hijack attribution.
No regression in robustness.

V2-REG PASS (in-program v2reg=1): D1 relA_final == 130 with no
attribution; D2 attr (1,3), relB 120 -> 60, follow-up A with
non-FAIL output; D3 attr (2,-1), relC == 60, relB stays 120 active,
follow-up B with FAIL output; D4 attr (1,3), relB 140 -> 80,
follow-up A with non-FAIL output. The guard is resident but
untriggered on every uncorrupted arm and C306 behavior reproduces
exactly.

A3Q PASS (in-program a3q=1): guarded A3 gives attr (-2,-2), relA ==
110, relB == 120, both active bits still 1, every observed_kill
counter == 0, a3_sanity_succeeds == 0, seal caught at the P4
checkpoint. A3 now fails cleanly with quarantine and zero revision.

A5Q PASS (in-program a5q=1): (i) seal_ok == 0 at the P4 checkpoint,
proving the whole-record tamper evidence catches a non-id
corruption; (ii) attr (-2,-2), relA == 110, relB == 120, both
active bits still 1, every observed_kill counter == 0. No revision
on the corrupted record. The frozen expectation is confirmed
exactly: learner recompute ck = 1*31+51*7+120*13+2*17+3*29 = 2069
vs stored 2062, mismatch, quarantine.

G-IDENT PASS (shell verified): `learner_phase4_record_checked`
extracted from `src/delayed_consequence_v2.zag` (from the `fn` line
through its closing brace) is sha256-identical to the function
extracted from the red-team guarded copy
(`delayed_consequence_redteam/src/redteam_guarded.zag`, verified
byte-identical to commit f58e3eabd). sha256 of both extractions:
a23ad3889c918642c419959c5fcfa2dfa08d1a883231128dbde8d320fe017db8
(diff empty, cmp clean).

MACH-0 PASS (diff plus shell audits): (a) learner-section diff
against the C306 learner functions shows only the 16-line guard
addition plus the world-selector threading already present in the
C309 redteam copy (C309 G2 proved that threading reproduces C306
exactly); (b) token grep audits over the learner functions: 0 hits
for mode/bridge/handler/opcode tokens, 0 hits for expected-answer
tokens, 0 references to the attack selector.

COMMIT-ORDER PASS (self-check, recorded after the commit): the
prereg commit e5e350bb0 (PREREG.md + NAMECHECK.md only, verified via
git show --stat) strictly precedes the implementation commit;
verified with git merge-base --is-ancestor before committing.

In-program summary line from run1: BARS k1=1 k2=1 k3=1 k4=1 k5=1
k9=1 k10=1; a1_succeeds=0 a2_succeeds=0 a3_seal_caught=1
a3_sanity_succeeds=0 a4_succeeds=0; a3q=1 a5q=1 v2reg=1;
IN-PROGRAM-BARS 14/14 PASS.

## Per-arm traces (runs/run1.txt)

D1 (ATK 11): TEACH A,A,B; commit A pred 60; P4 confirm, relA 130,
no attribution; follow-up A out 60.
D2 (ATK 12): TEACH B,B,A; commit B pred 50; P4 attr (1,3), relB 60,
B retired, obs3=1; follow-up A out 60.
D3 (ATK 13): TEACH B,B,A; commit B with NO record (record region
zeroed); P4 norecord path: attr (2,-1), relC 60, B stays 120
active; follow-up B out -1.
D4 (ATK 14): TEACH B,B,A; commit B pred 50; P2 14 episodes, relB
rises to 140; P4 attr (1,3), relB 80, B retired, obs3=1; follow-up
A out 60.
A1 (ATK 1): commit B pred 50; P3 kills F3+F5; P4 attr (1,3), relB
60, B retired, obs3=1; follow-up A out 60.
A2 (ATK 2): commit B pred 90 (A2 world); P3 kills F3; P4 attr
(1,3), relB 60, B retired, obs3=1, obs1=0; follow-up A out 60.
A3 (ATK 3): commit B pred 50 cksum 2062; CORRUPT record-id bit
flipped mid-P2; seal_ok=0 from P2 on; P4 relA 110, relB 120, attr
(-2,-2), act0=1, act1=1, obs all 0; follow-up B out -1.
A4 (ATK 4): commit B pred 50; P2 builds lookalike L (rel 140); P3
kills F3; P4 attr (1,3), relB 60, B retired; follow-up A out 60.
A5 (ATK 5): commit B pred 50 cksum 2062; CORRUPT record-prediction
bit flipped mid-P2 (50 becomes 51); seal_ok=0 from P2 on; P4 relA
110, relB 120, attr (-2,-2), act0=1, act1=1, obs all 0; follow-up
B out -1.

## Key numbers

- sha256 of the binary (bin/delayed_consequence_v2):
  7dc67ce8b23d57c29d37823c26d305502a1942e61aae6aa5c38002159e9be939
- sha256 of each of the 3 runs (byte identical):
  83ada7719cf793ac32ec8ced78ae0f70881420c27e1c97fba84544480f2f9804
- Guard extraction sha256 (G-IDENT):
  a23ad3889c918642c419959c5fcfa2dfa08d1a883231128dbde8d320fe017db8
- Cognition lines added: 714 (new .zag file; 0 lines changed
  elsewhere). Guard delta: 16 lines (learner_phase4_record_checked),
  byte-identical to the C309 red-team guard.

## Audits

- Learner functions never reference the attack selector (0 hits for
  the `atk` token in the learner section): attack designs do not
  leak into the learner path.
- Researcher-expected-value audit over learner functions: 0 hits.
- Architecture audit for mode/bridge/handler/opcode tokens over
  learner functions: 0 hits. Standalone file; TNN core untouched.
- Learner-section diff vs C306: only the guard addition and the
  world-selector threading (already proven C306-exact by C309 G2).
- Compiler lessons: no `as *i32` slice construction in functions,
  no _zag_print for dynamic output (single raw-syscall flush;
  stdout bytes verified), no `!(.. && ..)` in while conditions
  (grep clean), flat if-nesting with hoisted flags in the new bar
  code.
- Docs: check_no_dash.sh clean on NAMECHECK.md and REPORT.md.

## Disclosures

1. The A5 corruption is a single-bit flip of the recorded prediction
   byte (50 becomes 51) applied by the driver after P2 episode 2.
   This is inside the disclosed threat model (accidental corruption
   of the record region by interference), the same model as A3.
2. The integrated guard is byte-identical to the C309 red-team
   guard (G-IDENT); the comment above it was updated to reflect
   permanent adoption, which is not part of the extracted function.
3. In quarantined arms (A3, A5) the follow-up still selects B
   (120 > 110) and executes to FAIL (-1). This is correct: the
   world is genuinely broken and the learner honestly refuses to
   revise on corrupted data instead of silently condemning the
   wrong composite.
4. During this worker's run the shared /home/hatch filesystem hit
   99 percent full; one file write (NAMECHECK.md edit) failed
   transiently with ENOSPC and truncated the file. The file was
   restored byte-exact from the prereg commit and both edits were
   re-applied and verified. No data was lost; the .zag source, the
   binary, and all three runs were verified intact afterwards
   (sha256 of runs unchanged).
5. znc emitted only the zagd-unavailable notice; no lint warnings.
   The binary ran 3/3 byte identical.

## Interpretation

The adoption holds. The 16-line guard, proven effective as a
const-flag variant in C309, is now a permanent unconditional
P4-entry step with zero behavior change on every uncorrupted arm:
the full C306 battery (D1-D4, K1-K10) reproduces exactly, the three
failed red-team vectors still fail (no robustness regression), A3
now quarantines cleanly instead of silently revising, and the new
A5 arm shows the checksum protects the whole record, not just the
id field. The mechanism adds no modes, bridges, handlers, opcodes,
or semantic cases; the only learner-logic delta vs C306 is the
guard plus its permanent call.

## Verdict: DCE-V2-COMPLETE

Every frozen bar passes: K1-K10, A1/A2/A4 still-fail, A3Q, A5Q,
V2-REG, G-IDENT, MACH-0, K7, COMMIT-ORDER. No bar failed, no
weakening, no reinterpretation. VOID not triggered. No forbidden
interpreter invoked at any point (safebin toolchain guard held).

Commits: prereg e5e350bb0; implementation recorded in NAMECHECK.md
after the commit lands. Local only, never pushed.
