# RESULT: Form Invention Test

Worker: Form Invention Worker.
Date: 2026-09-30 UTC.
Verdict: **INVENT-TESTED** (all frozen kill bars pass).

Prereg: `84ddcb57e` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`, see section 6).
Implementation: `finvent.zag` (this directory, pure Zag, pure ASCII).
Learner machinery copied verbatim from learn_scale/lscale.zag
(commit d34e8135c); only true_subj/true_obj extended with families
6, 7, 8 and main() replaced.
Raw: `FINV_RAW_1.txt` (md5 `af471a9120bbe71e150cc2a50ed3d703`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git, cp, mv,
md5sum only; zero Python invocations in source, build, execution,
or analysis); zero em-dash/en-dash bytes in wave files
(byte-checked); prereg strictly precedes implementation; commits
local on `tnn-native-lab`, owned paths only.

## 1. What was tested

Whether the SCALE-TESTED learner invents a fourth schema form when
exposed to families no menu form (F0 CONST, F1 LIN, F2 EXC) can
represent. Three frozen families: G (STEP, threshold in the middle
of the observed range), G2 (STEP, threshold at the edge of the
observed range; near-miss probe), H (TWO-EXC, two exceptions).
Conditions: FRESH (fresh state per family) and RETAINED (after
A,B,C,D,E, which rebuild the 20,11,8,6,5 transfer curve and leave
live F1 with uses[F1]=5).

## 2. Measured behavior

| Run | adopted | cost | refit | strikes[F1] |
|---|---|---|---|---|
| FRESH G | -1 | 40 | -1 | 0 |
| FRESH G2 | 2 | 20 | -1 | 0 |
| FRESH H | -1 | 40 | -1 | 0 |
| RETAINED G | -1 | 40 | 0 | 1 |
| RETAINED H | -1 | 40 | -1 | 1 |
| RETAINED G2 | 2 | 20 | -1 | 1 |

All six adopted/cost pairs match the frozen predictions exactly.

The RETAINED A-E prefix reproduces the lscale curve exactly
(20,11,8,6,5, adopted 1 throughout), confirming the copied
machinery is behavior-equivalent on families 0..5.

One mechanism note deviates from the prereg's non-kill-bar notes
column (disclosed, does not affect K2): the prereg note for
RETAINED G2 said "refit fails (strike)". In the frozen run order
A,B,C,D,E,G,H,G2, H's clean failure had already set live=-1, so
G2 entered discovery directly (refit=-1) and adopted F2 at n=6.
The refit-fail path for G2 would only occur if G2 directly
followed a live-form family. adopted=2 and cost=20 are as
predicted; the strike count stayed at 1 (from G).

## 3. Kill bar evaluation

- K1 (spec): PASS. The run emits all three frozen SPEC lines
  verbatim (grep -Fx verified on the raw log) and executes all
  six predicted runs.
- K2 (behavior): PASS. All six adopted/cost pairs match the
  frozen predictions table exactly (in-code check, K2=1).
- K3 (invention requirements): PASS. Section 5 specifies the
  machinery a learner would need to invent the fourth form.
- K4 (purity): PASS. Pure Zag; zero Python; zero dash bytes;
  3/3 byte-identical; exit 0; zero stderr.

## 4. Interpretation

The learner does not invent the fourth form. Two distinct failure
modes are now measured:

(a) Clean failure (G, H): discovery tries F0, F1, F2 at every
buffer size from 6 to 40, all return 0, and the learner reports
adopted=-1 after burning the full BMAX budget. No diagnosis is
performed, no partial structure is retained, and nothing is
learned from the failure: RETAINED H fails identically right
after RETAINED G failed. The menu is a closed set and the
learner has no machinery for stepping outside it.

(b) Near-miss misapplication (G2): F2 fits the observed buffer
exactly via its nodd==n-1 branch ("default 5, exception at 7000
gives 0") and verifies on 14 further examples drawn from the same
distribution. The learner "succeeds" with a wrong causal story:
the true family is a threshold, and the form is wrong for every
subject below 7000, which verification never samples. This is the
more dangerous failure mode because it is silent: cost 20, no
strikes, full confidence, wrong form. Verification cannot catch
it because verification draws from the same window as discovery.

The sketch control (researcher-authored, never called by the
learner) fits G's buffer in one scan (t=6003), refuses H's buffer
(it needs two thresholds), and refuses A's LIN buffer. The data
are one-scan learnable; the failure implicates the closed menu,
not the data.

## 5. Invention requirements (K3)

For a learner to genuinely invent the STEP form, the following
machinery would be needed. Each item is stated as a falsifiable
requirement.

R1. Failure diagnosis from fit residuals. When discovery exhausts
the menu at BMAX, the learner must retain the failed buffer and
compute per-form failure signatures instead of reporting -1. For
STEP, F0's signature is: two distinct output values, each
occupying a contiguous interval in subject order. Required
primitive: cluster (subj,obj) pairs and test contiguity along the
subject axis. Without diagnosis, invention has no starting point.

R2. A fixed constructive operator vocabulary. Invention needs
building blocks frozen BEFORE the fourth family is designed
(anti-treadmill): terminals {subj, const}, operators {<, ==,
if-then-else}, and the existing forms as composable leaves. New
forms are expression trees in this vocabulary. The vocabulary is
generic machinery; the STEP tree IF(subj<6003, 0, 5) must be
learner-constructed, never a dedicated source case.

R3. Failure-driven candidate generation. From the diagnosis "F0
failed with 2 contiguous clusters", generate the minimal
structural repair: piecewise composition of the failing form,
IF(subj < t, F0(c0), F0(c1)), with t, c0, c1 fitted from the
cluster boundary. This is counterexample-driven structural
growth: extend or split only where the current form fails,
preserve what it explains. Blind enumeration over the
construction vocabulary is the treadmill to avoid.

R4. Promotion protocol with novelty check. The candidate must
pass the same gates as menu forms: exact fit on the discovery
buffer, verification on fresh examples under the standard V
schedule, then persistence with uses/strikes counters subject to
the same retirement policy. Novelty check: reject the candidate
if it reduces to a menu form on the evidence (threshold outside
the observed subject range is just F0; the G2 case shows why this
matters, since F2 already covers that buffer). A tie between a
menu form and an invented form that both fit, as on G2's buffer,
needs a stated tie-break principle (for example, prefer the form
whose predictions diverge less under intervention, or keep both
as competing hypotheses).

R5. Revision. If later evidence contradicts the invented form,
the same machinery must extend it. H is the natural next test:
a one-threshold inventor must grow to two thresholds or fail
honestly. Invention is ongoing, not one-shot.

R6. C0 mapping for a genuine invention claim.
- C0-A: the threshold value, the cluster boundary, and the tree
  structure live in learner-created persistent state with a
  white-box construction trace. Source-audit kill bar: if the
  answer to "where are the semantics?" is a dedicated branch
  written before training, the L3 claim dies.
- C0-B: the form is incrementally constructed
  (diagnosis, candidate, fit, promote), not selected from an
  enumerated list of repairs.
- C0-C: freeze the inventor, then test on adversary-designed
  families (multi-threshold, periodic, nested); at least one
  family designed after the freeze.
- C0-D: the invented form is reused: a later family with the
  same threshold shape but different constants transfers via the
  uses[] discount, and the form composes (a STEP output feeding
  a LIN input).

## 6. Honest scope and limits

- Bounded L1/L2. The learner selects, fits, retains, and rejects
  among researcher-supplied forms; it does not invent forms.
- The sketch is researcher-authored and is not learner machinery;
  it is a control against "the data were unlearnable".
- The G2 misapplication is wrong only with respect to the
  unobserved region; on all observed data the adopted F2 form is
  exactly correct. The finding is about silent wrong-form
  confidence, not predictive error.
- Synthetic workload, exact-match prediction, small scale.
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 7. Commit order verification

Prereg `84ddcb57e` committed alone before `finvent.zag` existed.
`git merge-base --is-ancestor 84ddcb57e HEAD` passes at the result
commit (recorded in the commit message trailer of the result
commit).

## 8. Files

- `PREREG_FORMINVENT.md` (84ddcb57e, frozen before implementation)
- `finvent.zag` (implementation, pure Zag, pure ASCII)
- `FINV_RAW_1.txt` (md5 af471a9120bbe71e150cc2a50ed3d703; runs 2, 3 identical)
- `FINV_RAW_2.txt`, `FINV_RAW_3.txt` (determinism evidence)
- `FINV_ERR_1.txt`, `FINV_ERR_2.txt`, `FINV_ERR_3.txt` (zero bytes each)
- `FORMINVENT_RESULT.md` (this file)
- `finvent_build`, `build.err` (built binary and build log, not committed)
