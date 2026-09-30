# ATTACK PLAN: L3C v3 Independent Red Team (SEALED, FROZEN)

Date: 2026-09-30. Status: FROZEN. No attack implementation exists at
commit time. Target: L3C-V3-PASS (commit 3bfa0947c), the claim that the v2
disjunction blind spot is closed by general cover-set composition with no
dedicated OR case and an empty interpreter diff.

## Attack method

The committed binary hardcodes its test worlds, so adversarial worlds
require recompilation. The attack harness rt_worlds.zag is built by
extracting lines 1-1115 of the committed l3c_v3.zag (everything before
`fn main`, i.e. the full mechanism: interpreter, disc2, disc_cover,
build_cover, try_construct_root, try_refine, observe, helpers) VERBATIM,
verified byte-identical to the committed source with cmp, then appending
a new adversarial main() with four attack worlds. The mechanism under
attack is therefore exactly the committed mechanism; only the test worlds
are adversarial. This is the standard form of adversarial probing: same
mechanism, harder worlds.

## Attack A: three-element disjunction (sig 801)

Question: is cover-set composition general beyond the two-element F2
case, or was F2 a lucky fit?

World RT3. Targets: (3,0,0,7)->2 x2, (3,2,2,7)->2 x2.
Contradictions in order R1,R2,R3,R1,R2,R3:
R1 (3,1,0,7)->0 [f1==1], R2 (3,5,0,7)->0 [f1==5], R3 (3,0,9,7)->0 [f2==9].
Ground truth: out=0 iff f1==1 OR f1==5 OR f2==9.

Analysis (frozen): disc2 finds no single atom covering all contradiction
rows and zero target rows ((f2==0) and (f1==0) both hit targets), and no
tightest-bound inequality separates (cmin/cmax interleave with targets on
every feature), so the cover path fires. Candidates at clash_n=6:
A=(f1==1) covers R1x2, B=(f1==5) covers R2x2, C=(f2==9) covers R3x2, each
with 2 rows meeting EVID_MIN=2 and zero target matches. Unique minimal
cover {A,B,C}, ncover=3.

Frozen predictions: trace HONEST_FAIL x4 (clash_n=2,3,4,5),
BUILT_COVER sig=801 ncover=3 (clash_n=6). built_delta=1,
unresolved_delta=4. Truth eval 6/6 on held-out probes:
(3,1,3,7)->0, (3,5,4,7)->0, (3,0,9,7)->0, (3,1,9,7)->0, (3,0,0,7)->2,
(3,7,7,7)->2. Structure: rule(801) is DISP with 3 labeled edges and 1
default edge; rep natoms=3.

Break condition: anything other than BUILT_COVER ncover=3 with 6/6 truth
eval breaks the generality reading of the claim. In particular,
HONEST_FAIL at clash_n=6, a wrong cover, or failed truth eval is a break.

## Attack B: minimality on a genuine cover path (sig 802)

Question: the P4 prereg miss showed size-1 covers are subsumed by the
direct path, so disc_cover minimality has never actually been exercised.
Does minimality really discriminate among multi-atom covers, or does the
first-found cover win regardless of size?

World RTMIN2. Targets: (3,0,0,7)->2 x2, (3,3,3,1)->2 x2 (f3 interleaved
to block the tightest-bound inequality escape, mirroring the P4 miss
mechanism). Contradictions in order R1,R2,R3,R4,R1,R2,R3,R4:
R1 (3,1,0,0)->0, R2 (3,1,2,2)->0, R3 (3,0,9,4)->0, R4 (3,4,9,6)->0.
Ground truth: out=0 iff f1==1 OR f2==9.

Analysis (frozen): disc2 returns 0 (no single EQ, 2-conjunction, or
inequality atom covers all 8 contradiction rows with zero target rows).
Candidates at clash_n=8: A=(f1==1) covers R1x2,R2x2 (4 rows),
B=(f2==9) covers R3x2,R4x2 (4 rows), C=(f1==4) covers R4x2,
D=(f2==2) covers R2x2, E=(f3==0) covers R1x2, F=(f3==2) covers R2x2,
G=(f3==4) covers R3x2, H=(f3==6) covers R4x2. Each has >= 2 rows and zero
target matches. Unique minimal cover {A,B}, ncover=2. Larger covers
({A,G,H}, {B,E,F}, {E,F,G,H}) must lose to minimality.

Frozen predictions: trace HONEST_FAIL x6 (clash_n=2..7),
BUILT_COVER sig=802 ncover=2 (clash_n=8). built_delta=1,
unresolved_delta=6. Truth eval 4/4: (3,1,5,5)->0, (3,5,9,5)->0,
(3,0,0,7)->2, (3,4,4,4)->2. rep natoms=2 with atoms (1,0,1),(2,0,9).

Break condition: a built cover with ncover != 2 (e.g. ncover=3 or 4,
showing first-found or enumeration-order wins over minimality), or truth
eval < 4/4, breaks the minimality claim. Note the builder's RESULT openly
states this test is untested; a break here narrows but does not by itself
kill L3C-V3-PASS, and will be reported as such.

## Attack C: hidden OR-case source audit (no new world)

Question: does build_cover, disc_cover, or the new control-flow branches
contain a disjunction-specific semantic case (a dedicated OR branch),
which would violate the "no dedicated OR case" core of the claim?

Method (frozen): (1) diff the v3 mechanism against the committed v2
source (20705ab5a, docs/lab/research-lead/overnight-20260928/l3c_v2/
l3c_v2.zag) to isolate exactly the new/changed lines; (2) read every new
line and classify each as generic set-cover machinery or
disjunction-specific; (3) independently re-verify the interpreter-diff
claim by extracting featv, pred_match, select_edge, interp,
trace_last_edge, path_uses from both sources with shell tools and
diffing; (4) grep the new code for any branch conditioned on cover size,
atom count == 2, or disjunction-shaped structure.

Frozen prediction: the new code is generic subset-enumeration set cover
over the existing atom vocabulary; no branch is conditioned on
disjunction; the interpreter diff is empty. Any disjunction-specific
branch found is a break of the central claim.

## Attack D: ambiguity generalization to k=3 (sig 803)

Question: does AMBIGUOUS_COVER honestly count distinct minimal covers
beyond the tested k=2, or is the k=2 result a special case?

World RTAMB3. Targets: (3,0,0,7)->2 x2, (3,2,2,7)->2 x2.
Contradictions in order R1,R2,R3,R1,R2,R3:
R1 (3,1,0,7)->0, R2 (3,0,9,7)->0, R3 (3,5,5,5)->0.
Candidates at clash_n=6: A=(f1==1) covers R1x2, B=(f2==9) covers R2x2,
C=(f1==5) covers R3x2, D=(f2==5) covers R3x2, E=(f3==5) covers R3x2.
Exactly 3 distinct minimal covers: {A,B,C}, {A,B,D}, {A,B,E}.

Frozen predictions: trace HONEST_FAIL x4 (clash_n=2,3,4,5),
AMBIGUOUS_COVER sig=803 k=3 (clash_n=6). built_delta=0, ambig_delta=1.
rule(803) still TERM(2) with ambig field = 3.

Break condition: k != 3 (undercount from the first-recorded logic, or a
spurious build by fiat) breaks the ambiguity-honesty claim.

## Kill bars

K1: this plan commit strictly precedes any attack implementation commit
(merge-base verified). Attack code and results committed only under
docs/lab/research-lead/overnight-20260928/l3c_v3_redteam/ with explicit
pathspecs.
K2: the attack harness mechanism region is byte-identical to committed
l3c_v3.zag lines 1-1115 (cmp-verified); all four attacks execute against
it; results recorded honestly against these frozen predictions.
K3: pure Zag + shell; zero Python; dash-clean per check_no_dash.sh;
contaminated paper untouched.
