# JUDGE RULINGS: wave-20260928-0221pdt

The advocate argued for the slate; the skeptic attacked it. These
rulings cite evidence, not rhetoric. Where a verdict is amended, the
amendment is stated explicitly and confined to what the cited numbers
support. No verdict is overturned on rhetoric.

## M1: EXP1c attempt 4 coordinator verdict, VOID on K7, nothing adopted

Ruling: AMEND (the VOID stands; the verdict line gains judge
amendments on the K6 operationalization, the C3 ceiling limitation,
and the banked design questions).

The VOID is arithmetic and is confirmed. K7 requires post-enumeration
learned fraction >= 0.50. The Zag-generated evidence note (M1-frozen
emitter, milestone 3 at 25a41e8da) reports I-survive 0/0 and I-invent
0/56 post-enumeration selections. 0/56 is below 0.50. The attempt is
VOID. Under binding precedent e97d1b9c0 a void test cannot kill a
hypothesis; the verdict kills nothing, adopts nothing, and leaves
past VOID attempts as uncertified history. That is the correct
application of the rule, and the advocate's case for it is sound.

Determinism and binding requirements are confirmed from the record:
full-run SHA aa939f9700022cd6a1c2f566fbe1a97843fc16cc056fe53a74709d90f719cb19
byte-identical across two runs; calibration SHA
d54bc389bacef79cf6fd0eb6070c4fabaa46da1eb706a03f7c003054d4661e95
byte-identical across two runs; max enum_tick 1185 >= 1134 minimum,
5 of 5 completed runs at or above the minimum, bound check PASS;
emitter frozen at M1 (f6d0e2084) with the pre-freeze fix disclosed;
M3 verbatim; M4 exhaustive; evidence note Zag-generated. The skeptic
does not dispute these, and neither does the judge.

Amendment 1 (K6 operationalization): The skeptic's confound attack
succeeds on the cited diagnostics. All 5 completed-enumeration runs
are on arm 4 (I-invent) at enum_tick 1152, 1152, 1183, 1185, 1171;
zero completions on arm 3 or the ablation arms; ablation arms show
n_distinct = 258 against the I-invent arm's 399 (258 = 399 minus the
141 COMBINE-containing sketches never tried under selection-side
exclusion). The selection-side exclusion still changes the
exploration-risk profile, so the survival gain (ablation 1200/1068 vs
I 431/282) remains fully explained by reduced exploration risk, per
the binding 2321pdt caveat carried in the Zag-generated evidence
note. REDTEAM_ITER4 section 5's claim that the re-freeze "fixed the
2321pdt confound" is K5-uncertified self-review and cannot amend a
judge's binding caveat. The judge therefore rules: the attempt-4 K6
operationalization is NOT certified a clean confound fix; the binding
2321pdt interpretation caveat stands unamended and travels with the
K6 measurements. This changes nothing about the verdict outcome: the
K1 firing (I-survive 431 <= R 1200) and the K6 firing (ablation
1200/1068 vs I 431/282) remain literal measurements from a voided
run, adopted by no one, killing nothing, per precedent.

Amendment 2 (C3): The skeptic's ceiling attack succeeds on the cited
numbers. f0 = 1200, f1 = 1200, f2 = 1200: all three calibrators sit at
the 1200 ceiling; the vector diffs (d01 = 11, d02 = 12, d12 = 12) are
end-energy-only differences at the ceiling. The distinctness
qualifier was rightly struck per the 2026-09-28 ruling, and C3 PASSES
on its literal frozen gate (three scripted strategies median >= 720),
which the judge confirms as a measurement. But the judge records the
skeptic's point as a measurement limitation: a gate whose every input
is at the ceiling cannot discriminate a broken calibrator, so the
C3-0221 PASS is a record of the measured gate only and must not be
cited by any future wave as substantive evidence of calibration
quality. Under VOID nothing is adopted on C3 either way.

Amendment 3 (the B0 structural finding and the queue items): The
skeptic's instrument-defect attack succeeds. Post-enumeration bonus
always >= 10% of selection weight under the frozen M3, 56
post-enumeration selections, 0 learned. The K7 bar (>= 0.50 learned
fraction within 1200 ticks) was unreachable by construction under
this M3 in attempts 1 through 4. The finding is about the instrument,
not about invention, and it cannot be read as evidence against the
hypothesis. The verdict's "next queue item" (redesign the
exploration/exploitation balance, not another variant-family retune)
is confirmed as a recommendation only, and the judge converts it to
two explicit banked questions to Micah, who owns this frontier-adjacent
design space:

- Q1: Should the loop pursue a redesign of the exploration/exploitation
  balance (the B0 novelty bonus as specified) as a new design
  direction?
- Q2: Is the K7 bar itself (learned fraction >= 0.50 within 1200
  ticks) attainable under any frozen M3, or does the bar need
  re-specification?

The loop may recommend; it may not decide. No worker is authorized to
implement a redesign on loop authority, and no attempt-5 retune is
authorized by this debate. This matches the 2321pdt EXP2-K4 precedent
(recommendations are not decisions and are not self-executing).

The K4 CANNOT-CONFIRM and K5 INCOMPLETE entries are confirmed as
stated: no audit was attempted, the implementer cannot self-certify,
and the verdict correctly declines to certify.

## M2: fork battery CONFIRM [RE-CERT]

Ruling: CONFIRM.

The numbers are genuine at the task pin: 57 named entries, 55 PASS, 0
FAIL, 2 UNTESTABLE; 45 unique commits recomputed from this wave's own
verdict table; harness rebuilt byte-identical to the frozen a2e6284c;
znc pin 498abcb5 verified before use and uniform across all 55 PASS
entries; task pin 43f339e60 honored by pinned-SHA extraction; the two
UNTESTABLEs are the expected pull-head entries (5802fec8, 4b76bb59)
with the identical content-dependent cause fifteen waves running; the
1721pdt probe-loss stays closed (repair 37d1d3cab is an ancestor of
the pin; the probe compiles and runs at the pin).

The skeptic's scope attack is adopted as a recorded caveat, not as a
defect. The mid-run tip move (43f339e60 to 18c883fec, the design lane
commit 42b3cf492 and the survey commit 18c883fec) was inert under the
pinning discipline, but the CONFIRM line therefore certifies the task
pin 43f339e60, not the wave's closing tip: the wave's two new
docs-only commits were not fork-tested this wave. The judge confirms
the proposed line with its own scope stamp (toolchain stability
only) and records that the two new docs-only commits are testable at
next wave's pin; no re-run is warranted for documentation-only
commits. The repeated HEAD-race pattern is noted: the pinning
discipline continues to work, and the battery's scope stamp continues
to be the honest boundary of its certification.

## M3: design lane [NEW]

Ruling: CONFIRM.

- EXP2-K4 HELD: blocker evidence unchanged in baf48e474..43f339e60;
  the 2321pdt judge amendment struck the 3-wave auto-retire clause and
  converted it to an explicit question to Micah; no answer appears in
  this range; the report does not re-ask him. The judge explicitly
  confirms, per the skeptic's demand: no expiry was set this wave,
  and the expiry question stays on his queue untouched. The
  redesign-or-retire recommendation remains a recommendation, not a
  decision, not self-executing.
- B1 NULL: 0 mechanism hits; 0 new mechanism text in docs/lab/invention/
  across the range; the 11 invention commits since 19f97c6cb each
  verified to predate baf48e474; P9 stays a re-freeze template.
- COMP2-P11 HELD: ruling 6 OPEN; no new ruling-6 text in the range.
- Trades HELD: no new expensive capability with a real mechanism; no
  knob proposed. Correct: a knob without a capability would be
  manufacturing.
- Sensory NULL: standing stand-downs hold (G1, D-VID-1, ST-1 dead;
  E3 rejected by Micah in blind A/B); nothing in the range revives
  any of them.
- Nothing manufactured: explicitly stated with governing commit ids.
  Confirmed.

## M4: interactive survey [NEW]

Ruling: CONFIRM NONE.

1,224 added files swept; 736 text files keyword-searched with a
corrected regex; all 226 added .zag files separately scanned for
stdin/fd-0/readline indicators; 14 hits, all 14 classified as false
positives (n_replans substring matches in EXP1c diagnostics,
self-references to the prior survey, debate records citing the survey
commit, the tnn_chat FIT note, the frozen harness argv spawn helper
that execves canned-argument binaries and is not an interactive input
path). Zero stdin/fd-0/readline indicators in any added .zag file.
The frozen batch probes remain the only loop-owned chat entry points,
batch-only; Micah's frontier REPLs untouched and outside the range.

The skeptic's instrument caveat is recorded: the first keyword run
used a regex with a trailing pipe that matched every file; it was
caught and corrected before classification, and the corrected run
produced the 14 hits. The NONE verdict is confirmed on the corrected
instrument, and this ruling records the correction so no future wave
cites the survey as a clean run without noting it.

## M5: tnn_chat FIT not re-run

Ruling: CONFIRM as noted.

Staleness 2 of 8 this wave, last fresh re-run at 2021pdt, queued
separately by the parent, not re-run here. The judge confirms the
line and keeps the staleness count visible, per the skeptic's demand,
so the 8-of-8 re-run is not silently dropped.

## M6: commit-order self-check [NEW]

Ruling: CONFIRM.

Strict order verified: 8b456736b < d9e96ad91 < f6d0e2084 <
141584162 < 25a41e8da < 404b639c3, merge-base verified. The verdict's
own caveat is correct and is confirmed with it: commit order evidences
commit order only, never run order or content identity. Nothing is
adopted this wave, so the check is VACUOUS for adoption, as the line
says.

## M7: UNTOUCHED [VOID]

Ruling: CONFIRM recorded, no action.

The six governance rulings remain OPEN (S7 strike, MD-SSD-1 keep-with-
UNVERIFIABLE vs re-freeze and re-run, S11 pull, S11-AUD pull, C12
judge queue, Python-mirror logic). All sealed blind pairs untouched
(R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform).
DP-1 is the parent agent's queue decision. This debate neither
decides, relitigates, nor re-presents any of them.

## Motions table

| Motion | Ruling | Numbers cited |
|--------|--------|---------------|
| M1: EXP1c attempt 4 verdict VOID on K7, nothing adopted | AMEND | K7: 0/0 and 0/56 vs bar >= 0.50. Determinism: run SHA aa939f9700022cd6a1c2f566fbe1a97843fc16cc056fe53a74709d90f719cb19 (x2 byte-identical); calib SHA d54bc389bacef79cf6fd0eb6070c4fabaa46da1eb706a03f7c003054d4661e95 (x2). Bound: max enum_tick 1185 >= 1134 minimum, 5/5 completed at/above. K1: 431 <= 1200; K6: 1200/1068 vs 431/282 (measurements from voided run, binding caveat stands). C3: f0/f1/f2 = 1200/1200/1200, diffs 11/12/12 (ceiling limitation recorded). K6 diagnostics: 5 completions all on arm 4 (enum_tick 1152, 1152, 1183, 1185, 1171); ablation n_distinct = 258 vs 399. Precedent: e97d1b9c0 (void test kills nothing). Milestones: f6d0e2084, 141584162, 25a41e8da, verdict 404b639c3; prereg 8b456736b; addendum d9e96ad91. |
| M2: fork battery CONFIRM [RE-CERT] | CONFIRM | 57 named, 55 PASS, 0 FAIL, 2 UNTESTABLE (rh-pull-1-head 5802fec8, rh-pull-2-head 4b76bb59, expected cause). 45 unique commits. Harness byte-identical to a2e6284c. znc pin 498abcb5 uniform 55/55. Task pin 43f339e60. Mid-run tip move to 18c883fec inert under pin (commits 42b3cf492, 18c883fec docs-only, testable at next pin). 1721pdt probe-loss closed (repair 37d1d3cab ancestor of pin). |
| M3: design lane [NEW] | CONFIRM | EXP2-K4 HELD, no expiry set, no new blocker evidence in baf48e474..43f339e60, expiry question on Micah's queue, not re-asked. B1 NULL: 0 mechanism hits, 11 invention commits all predate baf48e474. COMP2-P11 HELD: ruling 6 OPEN. Trades HELD. Sensory NULL: stand-downs hold. Nothing manufactured. |
| M4: interactive survey [NEW] | CONFIRM | NONE. 1,224 added files swept; 736 text files searched; 226 .zag files scanned; 14 hits, 14 false positives individually classified; 0 stdin/fd-0/readline indicators. Regex correction recorded. |
| M5: tnn_chat FIT not re-run | CONFIRM | Staleness 2 of 8; last fresh re-run 2021pdt; queued separately by the parent. |
| M6: commit-order self-check [NEW] | CONFIRM | VALID: 8b456736b < d9e96ad91 < f6d0e2084 < 141584162 < 25a41e8da < 404b639c3, strict, merge-base verified. VACUOUS for adoption (nothing adopted). Caveat confirmed: commit order evidences commit order only. |
| M7: UNTOUCHED [VOID] | CONFIRM | Six governance rulings OPEN; all sealed blind pairs (R9, C1, C2v3, S11-IMG, C12, S11-AUD, S13, S14, whirlpool-planform) untouched; DP-1 is the parent agent's queue decision. No action. |
