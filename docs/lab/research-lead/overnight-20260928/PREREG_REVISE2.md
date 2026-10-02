# Preregistration: H-REVISE2 (Procedure Revision v2)

**Date:** 2026-09-29
**Researcher:** Procedure Revision v2 Researcher (subagent)
**Status:** FROZEN (commit before any implementation file)
**Branch:** tnn-native-lab

## Hypothesis

H-REVISE2: A self-revising procedure learner with versioned conditional
dispatch can revise a deployed program after a counterexample, sidestepping
the H-REVISE impossibility proof by changing the architecture so the proof's
premise no longer holds.

## Background

H-REVISE (commit c7bfaeba1) proved: no single function P(k,n)->index can
satisfy both training (P(k,3)=2, broadcast-last) and the counterexample
(P(k,3)=0, "xab"->"xxx") for identical (k,n). The tested architecture was
one-shot batch search; revision meant re-search on augmented data. Five
revision capabilities were ABSENT: detection, diagnosis, conditional
representation, revision operators, procedure memory.

H-REVISE2 does not contest the proof. It changes the architecture:

1. **Monitor loop.** The found program stays deployed. Each new observation
   is checked against the program's prediction. Mismatch triggers revision
   autonomously (no human in the loop). This supplies capability 1
   (detection), which H-REVISE lacked.
2. **Diagnosis.** On mismatch, the learner compares the counterexample input
   against training inputs and finds a discriminating content feature
   (pos, val). This supplies capability 2 (diagnosis).
3. **Versioned revision.** The old program P0 is PRESERVED, not discarded. A
   new program P1 is discovered from the counterexample subset. Both are
   stored with a dispatch condition: IF input[pos]==val THEN P1 ELSE P0.
   This supplies capabilities 3, 4, 5 (conditional representation, revision
   operator = version/specialize, procedure memory = version store).
4. **Signature change.** The revised artifact has signature
   (k, n, input)->index, not P(k,n)->index. The impossibility proof's premise
   (one function of (k,n) covering all inputs) is never instantiated.

Difference from the Bridge (H-BRIDGE): the Bridge triggers when direct
discovery FAILS on the full training set at learning time. H-REVISE2
triggers when discovery SUCCEEDED, a program is deployed, and a LATER
counterexample contradicts it at use time. The Bridge is fallback at
learning time; H-REVISE2 is self-correction at use time. This directly
targets L3 criterion 12 (revisable after a counterexample).

## Experiment Design

Implementation: `revise2.zag` (pure Zag), self-contained (includes
extraction, N-first discovery, evaluation, monitor, diagnosis, version
store). Test data is embedded in the source as byte literals for the
inputs/outputs under test (the mechanism under test is the revision
logic; the discovery search space is the standard 1055 programs).

Phase A (learn): training pairs ("abc"->"ccc"), ("def"->"fff"),
("ghi"->"iii"). Run discovery. Expect P0 = [N C1 SUB] (n-1, broadcast-last).

Phase B (deploy and monitor): present new observations one at a time;
learner predicts with P0 and compares.
  B1: ("jkl"->"lll"). P0 predicts "lll". Match. No revision triggered.
  B2: ("xab"->"xxx"). P0 predicts "bbb". MISMATCH. Counterexample detected
      autonomously. Emit DETECT event with the failing pair.

Phase C (diagnose): compare counterexample input "xab" with the four
passing inputs ("abc","def","ghi","jkl"). Search positions 0..2 and the
distinct byte values present in the data for a (pos,val) split where the
counterexample has val at pos and NO passing input has val at pos.
Expect (pos=0, val=120 'x'). Emit DIAGNOSE event. No byte literals for
condition values in the diagnosis code; values come from the data.

Phase D (revise): run discovery on the counterexample subset
{("xab"->"xxx")}. Expect P1 = [C0] (constant 0, broadcast-first).
Store versioned: v0 = (P0, cond input[0] != 120), v1 = (P1, cond
input[0] == 120). Emit REVISE event with both program encodings.

Phase E (verify): apply the versioned dispatch to all five cases:
("abc"->"ccc"), ("def"->"fff"), ("ghi"->"iii"), ("jkl"->"lll"),
("xab"->"xxx"). All five must produce the expected output.

Phase F (honest withhold): present unresolvable counterexample
("abc"->"aaa"): same input as a training pair, different output. No
content feature can discriminate it (input is identical to training).
The mechanism must emit UNRESOLVABLE, must NOT modify P0, and P0 must
still produce "ccc" for "abc" afterward.

## Frozen Kill Bars

K-RV1 (revision works): versioned dispatch produces the expected output on
all five Phase E cases. Each verified by execution in the raw output.
Threshold: 5/5.

K-RV2 (proof sidestepped): the stored revised artifact contains TWO
distinct programs plus a dispatch condition record. It is not a single
affine P(k,n) program. Verified by dumping the version store: two program
slots with different bytes and one condition record (pos, val, slot_true,
slot_false). The H-REVISE impossibility proof cannot apply because no
single P(k,n)->index is claimed.

K-RV3 (white-box trace): the raw output contains, in order: the learned P0
encoding, the B1 pass, the B2 DETECT event with the failing pair, the
DIAGNOSE event with (pos=0, val=120), the learned P1 encoding, the REVISE
event, the version store dump, and the five Phase E results. All
inspectable from the committed raw output.

K-RV4 (determinism): two consecutive runs produce byte-identical raw
output (verified with cmp).

K-RV5 (honest withhold): on the Phase F unresolvable counterexample, the
raw output contains UNRESOLVABLE, the version store is unchanged (same dump
as after Phase D), and P0 still maps "abc"->"ccc".

## Failure Modes (honest)

- If diagnosis finds no discriminating feature for the Phase B2
  counterexample, the mechanism must WITHHOLD (as in Phase F) rather than
  guess. K-RV1 then FAILS honestly and the hypothesis is killed.
- If discovery on the counterexample subset finds no program, K-RV1 FAILS.
- If any bar fails, H-REVISE2 is KILLED or DOWNGRADED per the evidence.
  A killed H-REVISE2 still informs: it would show versioned dispatch is
  insufficient and the revision gap is deeper.

## What This Would Show

If all five bars pass: the core discovery mechanism, extended with a
monitor/diagnose/version loop, revises a deployed program after a
counterexample. L3 criterion 12 would be satisfied for this bounded case
(single binary content condition, affine sub-programs). Classification
would be bounded L2+ revision, not general L3: the condition vocabulary is
(position, equality) only and the sub-program space is unchanged.

## Pure Zag Compliance

Implementation, compilation, and execution in Zag only. No Python anywhere.
Toolchain: znc 2026.07.0-dev (edition 2026).

## Documentation Style

No em dashes in any loop documentation.
