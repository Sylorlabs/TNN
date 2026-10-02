# PREREG: Forgiveness Clock for Belief Source Reliability (Belief Forgiveness Worker)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

BELIEF-MISINFO (commit 13451a814) proved the fraction reliability rule
(1000*correct/total) has no forgiveness: after M2 degradation, 20 fully
clean rounds only recovered rel(S) to 913, never 1000. The non recovery
is rational given the rule, and that was the finding. UNTESTED: can a
minimal forgiveness mechanism restore gradual recovery while preserving
the M1 correction behavior and the M2 downgrade trajectory?

## Mechanism: streak gated wrong retirement (unfrozen variant)

Same learner machinery as BELIEF-MISINFO (evidence records,
independence discount, event identity register, band derived statuses,
EVN = 64). One addition to learner state per source: a signed streak
counter, consecutive same outcome calibration length (positive for a
correct run, negative for a wrong run). The reliability update rule in
ev_calibrate becomes:

On a correct verification outcome: streak increments (reset to +1 when
the previous outcome was wrong). If the new streak is >= 2 and the
source has historical wrongs (total minus correct > 0), one historical
wrong is retired: total decrements by 1 while the new correct still
increments correct. Net per round at streak >= 2: correct +1, total
unchanged.

On a wrong verification outcome: streak decrements (reset to -1 when
the previous outcome was correct); correct and total update exactly as
the old fraction rule. No forgiveness ever triggers on a wrong outcome.

Ownership accounting (honest): the rule FORM (one wrong retired per
consecutive correct beyond the first) is researcher scaffold, same
category as the independence discount halving in the parent experiment.
Every VALUE the rule operates on (streak, correct, total, wrong count)
is learner owned state, updated only by verification outcomes. There is
no tunable numeric parameter: no decay rate, no window size, no
threshold constant. The recovery rate is fully determined by the
source's own record: a source with W historical wrongs needs a clean
streak of W+1 to retire them all.

## Predicted properties (derived before running)

P0 (downgrade preserved): wrong outcomes never trigger forgiveness, so
the M2 degradation trajectory must match the fraction rule exactly.

P1 (gradual, not instant): recovery is gated by the streak, so one
clean round cannot restore 1000. Full recovery requires wrongs+1
consecutive clean rounds.

P2 (proportional): a single isolated wrong is forgiven after 2 clean
rounds; 4 wrongs need 5 clean rounds. Forgiveness debt scales with
damage, not a fixed clock.

P3 (no immunity): a relapse (a wrong after full recovery) drops
reliability immediately under the same rule; the forgiven record grants
no protection.

## Worlds

M1, M1b, M2, M3: exact reruns of the BELIEF-MISINFO worlds (same
sources, eids, phases) on the new machinery. M3 checkpoints move to
+1..+5 and +20 to resolve the recovery curve.

M4 (adversarial laundering, fresh state): S runs the pattern
correct, correct, wrong repeated for 12 rounds (eids 7401-7412), i.e. a
strategic liar telling truth 2/3 of the time. Measures whether the
forgiveness rule lets a persistent liar keep high reliability.

M4b (alternating control, fresh state): S alternates correct, wrong for
6 rounds (eids 7421-7426). The streak never reaches 2, so no
forgiveness should trigger; reliability must track the fraction rule.

M5 (relapse, continues M3 state): after full recovery, S is wrong once
(eid 7501), then correct twice (eids 7502-7503). Measures whether a
relapse drops reliability immediately and what repair costs.

## Preregistered mechanistic predictions

P4 (M1/M1b/M2 unchanged): every K2/K3 prediction from BELIEF-MISINFO
holds exactly: M1 copy st 11 with s1 3000 s2 0; exposure rel 952 with
stance 11; contradiction st 12 then 22; reassert contrib 1904, s1 4904
s2 4000, st 12; M1b contribs 2000/1000/500 with stances 12, tie, 22;
M2 degrade 952/909/913/875/880/846 with W1 at 1000; downstream 1692,
st 11. Rationale: no world except M3/M4/M5 produces a correct streak
>= 2 while historical wrongs exist, so the rule is inert there.

P5 (M3 recovery): continuing M2 state (22/26, streak -1), 20 clean
rounds give rel: +1: 851, +2: 888, +3: 925, +4: 962, +5: 1000, +20:
1000. That is 1000*23/27, 1000*24/27, 1000*25/27, 1000*26/27,
1000*27/27. Full recovery at +5, exactly wrongs+1 = 5 consecutive
clean rounds. +1 is 851, not 1000: recovery is gradual, not instant.

P6 (M4 laundering): from fresh state, the R,R,W pattern gives
(correct,total): r3 (2,3) rel 666; r6 (4,5) rel 800; r9 (6,7) rel 857;
r12 (8,9) rel 888. The liar's wrongs are laundered one per cycle while
it keeps lying 1/3 of the time: reliability climbs toward 1000
asymptotically despite persistent lying. This is the documented
vulnerability, predicted in advance.

P7 (M4b alternating): r2 (1,2) rel 500; r4 (2,4) rel 500; r6 (3,6)
rel 500. No forgiveness, exactly the fraction rule.

P8 (M5 relapse): after M3 (27/27, streak +20): one wrong gives
(27,28) rel 964, streak -1: the relapse drops reliability
immediately. Two clean rounds give (28,29) rel 965 then (29,29) rel
1000: repair costs 2 rounds for 1 wrong.

## AMENDMENT 1 (2026-10-02, before REPORT, transparent)

P8 was computed from a wrong mental model of the post M3 record. The
author modeled the record as frozen at (27,27) after the 4 wrongs were
retired at +5. In fact correct outcomes keep incrementing both counters
after wrongs reach 0: rounds +6..+20 add 15 more correct to each, so the
post M3 state is (42,42), streak +20, wrongs 0. Corrected P8: relapse
wrong gives (42,43) rel 976 (1000*42/43); repair round 1 gives (43,44)
rel 977 (1000*43/44), streak +1, no forgiveness yet; repair round 2
gives (44,44) rel 1000, streak +2, the 1 wrong retired. The qualitative
predictions are unchanged (relapse drops reliability immediately; a
single wrong costs 2 clean rounds to repair); only the exact values
move, because a longer clean record cushions a single relapse more.
The implementation's M5 checks were updated to the corrected values
after this amendment was written. Nothing else in this prereg changes:
P4-P7 held exactly as written on the first execution.

## Hypothesis verdict rule (frozen)

BELIEF-FORGIVENESS-COMPLETE iff K1 through K5 all hold. The report must
state: the recovery curve with exact values, the number of clean
observations full recovery required, confirmation that M1/M2 behavior
is unchanged, and the laundering vulnerability with its measured
trajectory.

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: P4 holds exactly (M1/M1b/M2 predictions unchanged from
    BELIEF-MISINFO; forgiveness inert outside recovery streaks).
K3: P5 holds exactly (M3 recovery 851/888/925/962/1000 at +1..+5,
    1000 at +20; nevicted == 0; +1 is not 1000).
K4: P6, P7, P8 hold exactly (laundering trajectory, alternating
    control, relapse cost). The vulnerability analysis is present in
    the report regardless of direction.
K5: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per world: reliability checkpoints with the preregistered exact
values printed alongside every observed value, the streak trace where
it matters, correction counts carried over from the parent, the
recovery curve, the laundering curve, and the relapse cost. Byte verify
stdout of the binary before trusting it (od -c spot check). State
plainly whether each prediction held, with the exact frozen verdict
rule cited. Document the laundering vulnerability as a finding, not a
failure to hide: any forgiveness rule that retires wrongs creates a
rehabilitation channel, and this experiment measures its price.
