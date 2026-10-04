# PREREG_CONTLEARN_LH_AMEND1: event-count arithmetic correction (pre-implementation)

Wave: wave-20261002-0221pdt. Lane: CONTLEARN-LH. Date: 2026-10-02.
Status: transparent amendment, committed BEFORE any implementation file
exists and BEFORE any result is seen. No tuples, phases, bars, or
decision rules change; only the stated total event count is corrected.

## The error

PREREG_CONTLEARN_LH.md states a 358-event script in four places:
section 3 ("Full script (358 events)"), K1a ("one process per full
358-event run"), K1c ("expected audited count 358 per run"), and
NAMECHECK.md Step 3 ("extended 358-event script").

The per-phase event numbers in section 3 sum to 356, not 358:
NOVEL 24 + CONFLICT-1 2 + CORRECTION-1 2 + RETENTION 12 + INTERFERE-A 48
+ DELAYED-A 12 + CONFLICT-2 2 + CORRECTION-2 2 + INTERFERE-B 96 +
DELAYED-B 12 + CONFLICT-3 2 + CORRECTION-3 2 + INTERFERE-C 120 +
LATE-NOVEL 6 + DELAYED-C 12 + LATE-REUSE 2 = 356.

## The correction

Every "358" in the frozen prereg and in NAMECHECK.md Step 3 now reads
356. The driver audit target is hg(W,52)==356 and prints AUDIT_PASS only
at 356. All interference volumes (V_A=52, V_B=152, V_C=276) are
unchanged: they were computed from per-phase numbers and are correct.
The "over 3x the 76-event battery" statement is unchanged (356 > 228).

## What does not change

No phase, tuple, subject id, relation, oracle, kill bar, decision rule,
or claim bound is altered. The script the driver implements is exactly
the per-phase script of PREREG_CONTLEARN_LH.md section 3.
