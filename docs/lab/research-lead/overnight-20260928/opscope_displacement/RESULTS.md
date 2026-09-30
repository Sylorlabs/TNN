# OpScope Tak-Displacement Attack: Sealed Results

Prereg: ae9c3f13e (frozen 2026-09-30 PDT). Sealed seed: 1004, FAM=4.
3 runs, byte-identical sha256:
8c64df7731232e8ffe6713bbc32d178f8726378382755b362fe75a4004dfea98 (x3).
Exit 0, zero stderr on all runs. VERIFY_U_ROUNDTRIP_126: 1.

Learner region verified untouched: diff of displace_all.zag against the
gate-stress sealed fam1 file shows changes only in world generation
(gen_episodes_fam fam==4 branches, probes), FAM/SEED constants, probe
summary labels, and comments. No learner function body changed.

## P1 (white-box): PASS

installed_now=0 at all 9 CHECK lines (seen=20..100). Final OPREC table:
all 8 rows inactive. ANY_OPERATOR_INSTALLED: 0.
TRUE_NOT_INSTALLED_WHITEBOX: 0. No operator with any trigger installed
at any check.

## P2 (DIAG mechanism fingerprint): PASS

seen=30, w=1 (not): epc=6 reclen=1 sup=6 mtch=6 div=3 cs=24 cb=24 gate=0.
seen=40, w=1 (not): epc=12 reclen=1 sup=12 mtch=12 div=3 cs=28 cb=28 gate=0.
The cs == cb equality holds exactly at every check: the empirical
fingerprint of the source-level proof. The zero-parameter gate is blind
to the position-0 negator, exactly as preregistered. (w=0 tak: gate=0 at
every check as well, cs < cb.)

## P3 (behavioral): CALIBRATION MISS, disclosed

Observed TEST_ACC=17/20; T1 (ep 109..111, "tak not grn") 0/3. Per-item:
only ep 109,110,111 fail (pred=17 vs tgt=1); all other 17 pass.

The prereg predicted 16/20, citing a "frozen 16/20 pre-operator baseline".
That citation was wrong: 16/20 was the F5 floor BAR in prereg 51c54e262,
not a measured DEFAULT-only score. The measured no-operator references
on this battery are the F4 ablation (17/20, negdrop=3, observed at
c60bfbe7a) and this displacement run (17/20, T1 0/3). They agree
item-for-item. The prereg's P3 number was miscalibrated; the science is
not: no negation item passes, and the score equals the operator-removed
reference exactly.

## P4 (probes): PASS

PROBE_D1_not_tak_red ("not tak red", trained surface form): 0/3.
PROBE_D2_not_tak_grn ("not tak grn", novel color): 0/3.
The DEFAULT is position-blind: the trained surface form scores no better
than the canonical form, and negation does not generalize to a novel
color without an operator.

## P5 (recovery check): PASS (no recovery)

F1_T1_3x_AND_WHITEBOX: 0 (t1pass=0/3, whitebox=0). F2: 0.
F4_ABLATION: 0 (t1_full=0, t1_abl=0, acc_abl=17/20, negdrop=0): emptying
the operator table changes nothing, because there is nothing to empty.
F5_FLOORS: 1 (acc=17/20 >= 16, SIZE 3/3). VERDICT line: OPSCOPE-R1R4-FAIL
(expected: the battery is attacked).

## Verdict: OPSCOPE-DISPLACEMENT-LOAD-BEARING

No operator installed at any check; the cs==cb proof fingerprint holds;
T1 0/3; both probes 0/3; ablation a no-op. The learner found no other
route to negation. The gate's positional assumption is load-bearing: the
battery's "not"-in-position-1 is a hidden researcher choice, and
negation is learned in this setup only through the DELETION operator,
which the gate can install only when the researcher places the negator
mid-utterance.

This bounds OPSCOPE-R1R4-PASS: it is a position-contingent L2 result
(learner fills a researcher-positioned operator slot), not
position-general negation learning. It does not upgrade or downgrade the
bounded-L2 verdict; it maps its boundary.

## Kill bars

- K1: prereg ae9c3f13e strictly precedes sealed generation and runs.
  Verified: git merge-base --is-ancestor ae9c3f13e <results-commit>.
- K2: 3/3 byte-identical runs; P1, P2, P4, P5 match frozen predictions;
  P3 disclosed as a prereg calibration miss with the corrected reference
  (ablation 17/20, matched item-for-item). No outcome was reinterpreted
  to fit a bar.
- K3: pure Zag + shell only, zero Python; exit 0; zero stderr; no em
  dashes (shell-only check_no_dash.sh); learner region byte-identical to
  the committed mechanism (diff-verified); contaminated paper untouched.

## Recommendation

The developmental-language lane should not try a seventh count bar. The
two attacks together (GATE-STRESS-FAIL, this displacement) show the
discovery gate is a positional template matcher: it installs operators
for words the researcher parks mid-utterance and is provably blind
otherwise. The next step is the redesign the gate-stress red team named:
cross-context behavioral validation (an operator must not degrade
held-out compositions; a candidate must predict correctly from more than
one utterance position) before installation, replacing the
position-sensitive count bars as the admission criterion. Until then,
any "not"-style result must carry the positional scope restriction in
its claim.
