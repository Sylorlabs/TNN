# ADDENDUM 1 to PREREG_STRESS (pre-implementation, 2026-09-30 PDT)

Status: FROZEN. Dated before any implementation file exists. This addendum
clarifies one bar; it does not soften any bar.

## Correction to K-S4(b) and P6 re-teaching check

The prereg as written says "zero learn() calls on foundation keys between P1
teaching and P6". The three frozen P4 corrections ARE learn() calls on
foundation keys ((2,10) twice, (5,11) once) occurring between P1 and P6, so
the literal reading is unachievable. The intended check is about
RE-TEACHING: the learner must not be re-taught original labels to fake
delayed reuse.

CLARIFIED K-S4(b): structural grep of stress_learn.zag must confirm that
every learn() call with a foundation subject key (subj 1..6) appears ONLY in
the P1 teaching block or the P4 correction block. Equivalently: zero learn()
calls on foundation keys in P2, P3, P5, P6, P7, P8, and zero learn() calls
anywhere that re-assert a pre-correction label ((2,10)->4, (2,10)->6 after
the second correction, (5,11)->2).

All other bars unchanged. This addendum is committed before implementation.
