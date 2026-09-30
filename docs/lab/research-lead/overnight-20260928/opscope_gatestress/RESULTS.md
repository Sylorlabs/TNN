# OpScope Gate-Stress Attack: Sealed Results

Prereg: 37d4212de14b6a51d62312ab7a0d28df741b3ab7 (frozen 2026-09-30 PDT).
Sealed seeds: A=1001, B=1002, C=1003. Each family run 3x on its seed.
Learner: byte-identical to committed c60bfbe7a (git blob
05be258a004ed541e0aff922a3470f00710cc020, verified by git hash-object).

## Determinism (K2)

All three runs per family are byte-identical (sha256):
Fam A: aded96007792a1ea67ee8202b1180ad72dfd4d33b782a58bdab256218402dc55 (x3).
Fam B: dbfaedea1cce352cd3ecfe25b6c7e147346b13e91fc24026a8e8fe029199824f (x3).
Fam C: 1d8df71c583d8f543261887ce89b3012aff3b6a68847b5e56037b26a01979049 (x3).

## Family A: perfect spoof (grn clears all six bars)

Outcome (all 3 runs identical):
- installed_now=2 at seen=30. OPREC: k=0 trig=1 created=30 active=1;
  k=1 trig=4 created=30 active=1. No retire at any later check.
- CONFOUND_GRN_INSTALLED=1. TRUE_NOT_INSTALLED_WHITEBOX=1.
- TEST_ACC=5/20. T1 (ep 109..111) 3/3 via not-op. SYN "tak grn sph" 0/3.
  DIRECT "tak grn cub" (ep 100..102) 0/3. Baseline pollution on tri items.
- PROBE_CONF_NEG ("tak not grn red") 3/3. PROBE_HARM_DIRECT ("tak grn cub") 0/3.
- R1R4 verdict: FAIL (expected; the battery is attacked).

Matches frozen prediction on every line. Verdict: GATE-FAIL,
subtype FAIL-FALSE-INSTALL. The true negator was also installed, so this is
not a miss; it is a false install with severe behavioral harm.

Harm isolation: Family B uses the same battery shape (grn-NEGs in phase 1)
but grn is K=2-killed and never installs; B scores 20/20. The A/B delta
(20/20 vs 5/20) isolates the confound-operator as the cause: the DEFAULT
records are near-identical, the only difference is the installed grn-op,
which fires on any utterance containing grn and mispredicts novel
compositions (its op records only cover trained scope words).

## Family B: K=2 sole discriminator (positive control)

Outcome (all 3 runs identical):
- installed_now=1 at seen=30. OPREC: k=0 trig=1 created=30 active=1 only.
- CONFOUND_GRN_INSTALLED=0. TRUE_NOT_INSTALLED_WHITEBOX=1.
- At seen=30 DIAG, w=4 (grn): epc=6 reclen=1 sup=6 mtch=6 div=1 cs=30
  cb=24 gate=1. Five bars plus the zero-parameter gate clear; K=2 kills it.
- TEST_ACC=20/20. F1=F2=F4=F5=1. R1R4-PASS. Probes 3/3, 3/3.

Matches frozen prediction on every line. Verdict: GATE-PASS. K=2 carries
the discrimination as the sole discriminator (reading (i) of the task).

## Family C: position-0 confound (literal task phrasing)

Outcome (all 3 runs identical):
- installed_now=1 at seen=30. OPREC: k=0 trig=1 created=30 active=1 only.
- At seen=30 DIAG, w=0 (tak): epc=30 reclen=1 sup=16 mtch=16 div=5 cs=0
  cb=24 gate=0. Five count bars clear (including K=2 div=5); cs=0 kills it.
- TEST_ACC=20/20. Probes 3/3, 3/3.

Matches frozen prediction on every line. Verdict: GATE-PASS. The
zero-parameter gate discriminates; the Position-0 Lemma holds empirically.

## Overall attack verdict: GATE-STRESS-FAIL

K2 kill bar: 3/3 families match frozen predictions 3/3 runs each. The gate
discriminates correctly when the confound is K=2-deficient (B) or at
utterance position 0 (C), but it has no defense against a mid-utterance
confound that clears K=2 (A): the confound installs as a DELETION operator
and destroys novel composition (5/20). The K=2-configured discovery gate
does not discriminate correctly in the stress regime.

## Kill bars

K1: prereg commit 37d4212d strictly precedes sealed generation and runs.
Verified by git merge-base --is-ancestor (see below).
K2: three families, 3x runs each, byte-identical; all outcomes match frozen
predictions. No mismatches to report.
K3: pure Zag + shell only; learner byte-identical (git hash-object);
no em dashes (shell checker); no Python authored.

## Recommended next step

The "tak"-displacement family ("not tak <color>"): put the TRUE negator at
utterance position 0, where the Position-0 Lemma proves the zero-parameter
gate is blind (cs=0). If "not" at position 0 can never be installed, the
gate's positional assumption is load-bearing and the battery's "not"-in-
position-1 is a hidden researcher choice. If a gate redesign is attempted,
it must add cross-context behavioral validation (an operator must not
degrade held-out compositions), not a seventh count bar.
