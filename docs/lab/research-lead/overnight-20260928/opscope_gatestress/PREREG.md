# OpScope Gate-Stress Attack: Preregistration

Committed: 2026-09-30 PDT. Worker: OpScope Gate-Stress Attacker.
Target: committed learner at c60bfbe7a (OPSCOPE-R1R4-PASS), K=2 prereg 51c54e262.
Pilot commit (pre-prereg exploratory): 82262d90c901f50dc723b96466b618b6625bca0e.

This preregistration is frozen. Sealed variant generation and sealed runs
happen only after this commit. The learner is never modified (byte-identical
copy, git blob 05be258a004ed541e0aff922a3470f00710cc020, verified by
git hash-object). Only the world (attack instrument) and harness (driver) are
authored; both in pure Zag.

## The K=2 ambiguity (stated explicitly)

The task phrase "K=2-configured discovery gate" admits two readings:
(i) K=2 as the specific diversity bar (popcnt(sforms) >= 2), the one bar
whose threshold was changed from the failed K=3; (ii) the whole discovery
gate as configured with K=2. Family B addresses reading (i) directly: the
confound clears the other five bars and the zero-parameter gate, so K=2 is
the SOLE discriminator. Families A and C address reading (ii): the whole
gate's discrimination behavior. All three readings are reported.

## Position-0 Lemma (proved from committed source, confirmed in pilot)

A word occurring only at utterance position 0 always has cs = 0 in the
zero-parameter gate: gate_pass computes sp = or_default over the prefix
before the FIRST occurrence; at position 0 the prefix is empty, so
sp = 0, while T is never empty (world_T always satisfies wid 0, "tak").
Hence cs = 0 < cb, gate = 0. A literal position-0 "tak" confound is
provably Z-immune and cannot stress the count bars. The strongest
positional confound is therefore a mid-utterance filler. Family A uses
"grn" (wid 4) at position 2 in "tak not grn <color>". Family C tests the
literal task phrasing ("tak" as confound) via doubling: "tak tak not
<color>", and predicts the gate kills it via cs = 0.

## Diversity semantics (corrected in pilot)

sforms[w] is the bitmask of ALL words occurring after w in any sig_match
episode (learn_event ORs 1<<U[j] for all j > i), not the immediate follower.
div[w] = popcnt(sforms[w]). This was verified by hand-reading learn_event
and confirmed by pilot DIAG values.

## Sealed families

All families share: phase-1 DIRECT 0..23, REL 36..47, SIZE 48..59;
phase-2 DIRECT new 60..79, DIRECT old 80..87, REL old 92..95, SIZE new 96..99;
test 100..119 (frozen 20); probes 120..125 (3x "tak not grn red" T={tak},
3x "tak grn cub" T={tak,grn,cub}). Only NEG blocks 24..35 and 88..91 vary.
Seeds: A=1001, B=1002, C=1003. Each family run 3x on its seed;
byte-identical output across the 3 runs is required (determinism check).

### Family A: perfect spoof (mid-utterance confound clears all six bars)

NEG 24..29: 6x "tak not grn <color>", colors 0,1,0,1,0,1.
NEG 30..35: 6x "tak not <color>", colors 0,1,0,1,0,1.
NEG 88..91: "tak not grn red", "tak not grn blu", "tak not red", "tak not blu".
T = {tak} for all NEGs (target avoids the named color; grn unsatisfied).

Static gate math for grn (wid 4) at seen=30: epc=6 (>=5); recmask={tak}
popcnt=1 (<=1); sup=6 (>=4); mtch=6/6 (sp=rec(red/blu)={red}/{blu},
rp={tak}, T={tak}); div={red,blu} popcnt=2 (>=2); gate cs-cb=6>0.
All six bars clear. For not (wid 1): div={grn,red,blu}=3, all six clear.

Pilot-measured (seed 999) at seen=30:
w=1: epc=6 reclen=1 sup=6 mtch=6 div=3 cs=30 cb=24 gate=1.
w=4: epc=6 reclen=1 sup=6 mtch=6 div=2 cs=30 cb=24 gate=1.
installed_now=2. Final OPREC: k=0 trig=1 created=30, k=1 trig=4 created=30,
both active. No retire.

Frozen prediction: grn-op installs (k=1) AND not-op installs (k=0).
CONFOUND_GRN_INSTALLED=1. TRUE_NOT_INSTALLED_WHITEBOX=1 (not-op present).
TEST_ACC collapses (pilot: 5/20): the grn-operator fires on any utterance
containing grn and mispredicts novel compositions (SYN "tak grn sph" 0/3,
DIRECT "tak grn cub" 0/3, baseline pollution on tri items). T1 holds 3/3
(via not-op k=0). PROBE_CONF_NEG ("tak not grn red") 3/3.
PROBE_HARM_DIRECT ("tak grn cub") 0/3. The A/B comparison isolates the
confound-operator harm (B predicts 20/20 on the same battery shape).
Verdict: GATE-FAIL, subtype FAIL-FALSE-INSTALL. K=2 does not discriminate;
no bar does. Behavioral harm: severe (15-point test accuracy drop vs B).

### Family B: K=2 sole discriminator (positive control)

NEG 24..29: 6x "tak not grn red" (grn always followed by red only).
NEG 30..35: 6x "tak not blu".
NEG 88..91: "tak not grn red" x2, "tak not blu" x2.

Static: grn clears five bars (epc=6, reclen={tak}, sup=6, mtch=6/6,
gate cs-cb>0) but div={red} popcnt=1, so K=2 kills it. not: div={grn,red}
at seen=30 (pilot: div=2), installs.

Pilot-measured (seed 999) at seen=30:
w=1: epc=6 reclen=1 sup=6 mtch=6 div=2 cs=30 cb=24 gate=1 -> installed k=0.
w=4: epc=6 reclen=1 sup=6 mtch=6 div=1 cs=30 cb=24 gate=1 -> KILLED by K=2.
installed_now=1. CONFOUND_GRN_INSTALLED=0.

Frozen prediction: grn never installs at any check (div stays 1; sup grows
from residual phase-2 DIRECTs but mtch does not, so consistency also fails
later). not installs (k=0, created=30). TEST_ACC=20/20. F1=F2=F4=F5=1,
R1R4-PASS. Probes 3/3 and 3/3.
Verdict: GATE-PASS. K=2 carries the discrimination as the sole discriminator.

### Family C: position-0 confound (literal task phrasing)

NEG 24..35: 12x "tak tak not <color>", colors 0,1 alternating.
NEG 88..91: 4x "tak tak not <color>", colors 0,1,0,1.
T = {tak} (target avoids the named color).

Static: tak (wid 0) clears five bars but cs=0 by the Position-0 Lemma, so
the zero-parameter gate kills it. not: div={red,blu}=2, all six clear.

Pilot-measured (seed 999) at seen=30:
w=0: epc=30 reclen=1 sup=16 mtch=16 div=5 cs=0 cb=24 gate=0 -> KILLED.
w=1: epc=6 reclen=1 sup=6 mtch=6 div=2 cs=30 cb=24 gate=1 -> installed k=0.
installed_now=1. CONFOUND_GRN_INSTALLED=0 (no grn-NEGs in this family).

Frozen prediction: tak never installs at any check. not installs (k=0).
TEST_ACC=20/20. Probes 3/3 and 3/3.
Verdict: GATE-PASS. The zero-parameter gate discriminates; Position-0 Lemma
holds empirically.

## Honesty bars

GATE-PASS (family): the true negator "not" is installed as a DELETION
operator (white-box: OPREC row with trig=1, sig=0, created>0, sup>=4,
active=1) AND the confound is NOT installed as an operator.
GATE-FAIL: the confound is installed (subtype FAIL-FALSE-INSTALL) OR the
true negator is never installed (subtype FAIL-MISS). Behavioral harm
(test accuracy, probe results) is reported separately and does not change
the discrimination verdict; a false install that is behaviorally harmless
is still GATE-FAIL.

Overall attack verdict: GATE-STRESS-PASS iff all three families are
GATE-PASS; GATE-STRESS-FAIL iff any family is GATE-FAIL.
Expected: A=FAIL, B=PASS, C=PASS, so overall GATE-STRESS-FAIL: the gate
discriminates correctly when the confound is K=2-deficient (B) or at
position 0 (C), but has no defense against a mid-utterance confound that
clears K=2 (A).

## Kill bars

K1: this prereg commit strictly precedes sealed variant generation and
sealed runs (verify with git merge-base --is-ancestor).
K2: three families, each run 3x on its frozen seed, byte-identical across
runs; outcomes match the frozen predictions above 3/3, OR any mismatch is
reported as a prediction failure (which itself is informative, not hidden).
K3: pure Zag + shell only; learner byte-identical (git hash-object match);
no em dashes in loop docs (shell checker); no Python authored at any step.

## One concrete next step (candidate, not decided)

If Family A fails as predicted, the recommended follow-up is a
"tak"-displacement family ("not tak <color>"): it tests whether the gate's
positional assumption (trigger not at position 0) is load-bearing, by
putting the TRUE negator where the confound was proved Z-immune. If the
gate is redesigned, the redesign must add a behavioral or cross-context
validation (e.g., the operator must not degrade held-out compositions),
not a seventh count bar.
