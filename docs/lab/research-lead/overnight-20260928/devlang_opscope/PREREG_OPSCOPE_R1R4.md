# PREREG: Operator/Scope R1-R4 Build (devlang_opscope)

## Step 0: standing-rules name-check

The four standing-rules sections at the top of LOOP_STATE.md apply to
this task as follows. (1) PURE ZAG ONLY governs everything here:
implementation, harness, world/battery code, analysis, and byte checks
are Zag and shell only, with zero Python at every step. (2) The
pure-Zag red-line scope ruling confirms fixture provisioning counts as
loop work, so the world and battery generator in this build is Zag-only
as well. (3) The shell-only byte-check rule requires verifying no em or
en dashes with worker_snippets/check_no_dash.sh, never with python3.
(4) The fork-testing rule and the image-judge rule do not directly bind
this builder task, but I will not disturb the shared toolchain or other
workers' files. I honor these by writing all code in pure Zag, running
byte checks through the shell script, staging only my owned path, and
never touching the research paper.

## Ancestry

- Frozen design: commit `71f98aa72` (OP_SCOPE_DESIGN.md, DESIGN-COMPLETE).
  R1 OPREC + interpret routing, R2 DELETION signature + zero-parameter
  gate, R3 scope-conditioned grounding, R4 falsifiers F1-F5.
- Review trigger: SEG_REVIEW2, commit `842638d15`.
- Prior builder: `operator_scope_impl/`, result commit `f01c6b69d`
  (OPSCOPE-FAIL). F3 PASS, F5 PASS (17/20, SIZE 3/3). F1/F2/F4 failed
  solely because K=3 scope diversity is unsatisfiable on the frozen
  battery: the true trigger measured div=2 forever (training NEG
  episodes negate exactly two distinct forms), while the gate correctly
  killed the positional confound. The prior builder's prereg froze K=3
  and reported the fail honestly; that verdict stands and is not
  re-litigated here.
- Validated machinery reused by reference: strict-majority binarization
  (cnt*2 > occ, per the prior build's Amendment 1), the (U,T) oracle
  interface, and the R1-R4 algorithms. This is a new build in a new
  owned path with a new prereg, not an amendment to the prior build.

## Mission

Implement R1-R4 in pure Zag against the frozen DEVANG battery and run
the R4 falsifiers F1-F5. Fix the single design parameter the prior
build proved unsatisfiable (K), with written justification below, and
test whether the operator is then discovered and T1 passes. Report
OPSCOPE-R1R4-[PASS/FAIL]. No L3 claim is made; all machinery is
researcher-authored; the learner creates the operator inventory, the
record vectors, and the routing bindings. Bounded L2 direction.

## Frozen constants

| Constant      | Value | Meaning                                    |
|---------------|-------|--------------------------------------------|
| B0 burn-in    | 20    | episodes before residual events start      |
| E interval    | 10    | proposal/retirement check cadence          |
| N_ep recur    | 5     | min episodes containing W                  |
| Fmax elig     | 1     | max features in record(W, DEFAULT)         |
| N support     | 4     | min residual events for W                  |
| C consistency | 0.75  | min signature-match fraction               |
| K diversity   | 2     | min distinct scope unit forms              |
| OPMAX         | 8     | operator table cap                         |

K=2 justification (design section 3.4 permits justified changes; this
is frozen before implementation, not weakened after results): the
design's K rationale is to bar phrase memorization by requiring the
deletion footprint to recur across varied scope content. The frozen
battery's training NEG episodes negate exactly two distinct forms
(red x8, blu x8), so K=3 is unsatisfiable on this battery (measured
div=2 by the prior build). K=2 preserves the anti-memorization intent:
a single fixed collocation yields div=1 and is still barred, while a
genuine operator recurring across two distinct scope forms passes. K=2
is the maximum satisfiable value that keeps the design's stated
property. All other constants adopt the design's proposed values.

Binarization (researcher-chosen, disclosed): bit f set in a record iff
occ > 0 and cnt[f]*2 > occ (strict majority). Adopted from the prior
build's Amendment 1, which showed non-strict majority admits 50%
co-occurrents and collapses the battery.

## Battery (frozen)

The frozen DEVANG battery: `gen_episodes` with seed 123456789, 100
train episodes one-pass online (0..99), 20 test utterances (100..119),
copied from `devang4.zag`. The episode order and RNG stream are
unchanged.

Units: the design (section 6) leaves segmentation orthogonal and
consumes its output through the existing unit-output interface.
SEG_REVIEW2 ruled segmentation non-binding for this failure. This
build uses the true word-id sequence as the unit sequence U (oracle
segmentation interface), identical to the prior build, which factors
out the segmentation confound. Word ids: 0=tak 1=not 2=red 3=blu
4=grn 5=bal 6=sph 7=cub 8=tri 9=big 10=biger 11=smal.

Observed target T (feature set, world side): consequence-feature
vocabulary = the 12 word ids. T = { w in U : the target object
satisfies w }, as a 12-bit mask. Satisfaction: tak always; not never;
red iff color==0; blu iff color==1; grn iff color==2; bal/sph iff
shape==0; cub iff shape==1; tri iff shape==2; big iff size==1; smal
iff size==0; biger iff size==1 and another object shares the target
shape with size 0. Check: DIRECT "tak C S" gives {tak,C,S}; NEG
"tak not C" gives {tak}; REL "tak biger S" gives {tak,biger,S};
SIZE gives {tak,sizeword,S}; 3WAY "tak big grn bal" gives
{tak,big,grn,bal}. The learner never sees objects, target index, or
template; it sees only (U,T) per episode.

### Frozen item ids

- T1 (NEG-novel, F1): episodes 109, 110, 111 ("tak not grn").
- T3 (scope-shift, F2): episodes 109, 110, 111. "grn" is familiar
  affirmatively from phase-2 DIRECT training (episodes 60-79) and is
  never negated in training; T1 and T3 coincide on this battery.
- SIZE group (F5 K6): episodes 115, 116, 117.

## Per-R predictions (frozen before implementation)

- R1: interpret(U) = UNION of DEFAULT records when no operator is
  active; with the discovered operator, rest UNION scope O-records.
  Predicted: after R2 installs the operator, T1 items predict {tak}
  which equals T={tak}.
- R2: the "not" unit (w=1) is the only form passing all bars. At the
  seen=40 check: epcount=16, |record|=0, support=12, consistency 1.0,
  diversity=2, gate strict (correct_sig > correct_base). Predicted:
  OPREC installed with trigger_form=1, scope_rule=REST_OF_UTTERANCE,
  signature=DELETION, support>=4 (expected 12), created_at=40 (>0).
  The positional confound w=0 ("tak") is predicted to keep failing
  the gate at every check.
- R3: routing sends pre-trigger units to DEFAULT and scope units to
  record(u,O) with residual R = T minus rest_pred. For NEG episodes
  R={tak} minus {tak} = {}, so scope O-records converge to empty,
  which is the correct deletion behavior.
- R4: F1-F5 run with per-item results; predictions below.

## R4 falsifiers (frozen bars)

- F1: T1 items 109,110,111 all pass (predicted mask == T mask) AND
  white-box dump shows an OPREC with trigger_form=1,
  signature=DELETION, created_at > 0, support >= N. Predicted PASS
  (T1 3/3 vs frozen 0/3 baseline).
- F2: T3 items 109,110,111 all pass. Predicted PASS (3/3).
- F3: source audit on the committed learner file listed below: grep
  for byte string "not" returns 0 hits; grep -i "negat" 0 hits; grep
  "is_negator" 0 hits; routing predicate references only
  OPREC.trigger_form_id (inspection note in result doc). Predicted
  PASS.
- F4: ablated copy of the trained state with the operator table
  emptied (routing disabled; records intact); re-run frozen T1 with
  no further learning. Pass iff T1_ablated < T1_full (strict).
  Predicted PASS: 0/3 < 3/3. Full 20-item under ablation reported;
  the drop must be localized to the 3 NEG items (predicted 17/20).
- F5: 20-item test accuracy >= 16/20 AND SIZE group (115,116,117)
  == 3/3. Predicted PASS (predicted 20/20 on analysis; bar is the
  frozen floor).

## F3 file paths (frozen)

- Learner (audited):
  `docs/lab/research-lead/overnight-20260928/devlang_opscope/opscope_learner.zag`
- Excluded world:
  `docs/lab/research-lead/overnight-20260928/devlang_opscope/opscope_world.zag`
- Excluded harness:
  `docs/lab/research-lead/overnight-20260928/devlang_opscope/opscope_harness.zag`

The word table lives only in the excluded world file. The learner
operates purely on integer unit ids and contains no word literals.

## Implementation notes (frozen)

- Duplicate-trigger guard: proposal_check skips W when an active
  OPREC already binds trigger_form=W (prevents a second row for the
  same trigger at later checks). Disclosed here; it changes no bar.
- Checks run when (t+1) >= B0 and (t+1) % E == 0 (seen =
  20,30,...,100). Retirement re-runs the gate per installed operator
  at each check (specified; expected no retirement on this battery).
- Determinism: single-threaded, fixed seed 123456789, no randomness
  in the learner. 3/3 byte-identical runs required.

## Kill bars (this build)

- K1: this prereg committed alone before any implementation file
  exists. Verified with `git merge-base --is-ancestor`.
- K2: F1-F5 executed with per-item results reported vs the frozen
  predictions above; T1 vs 0/3 baseline; full battery vs 16/20
  baseline. PASS requires results, not passes.
- K3: pure Zag, zero Python at every step; 3/3 byte-identical runs;
  exit 0; zero stderr; no em dashes (shell-only check_no_dash.sh).

## Governance

- Pure Zag only. No Python anywhere, including scratch and checks.
- No em dashes in source or docs (byte-check with the shell script).
- Owned path only:
  `docs/lab/research-lead/overnight-20260928/devlang_opscope/`.
- Never stage or commit outside the owned path. Never touch
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`.
- If a live `.git/index.lock` is hit, wait and retry; never remove it.
- Verdict: OPSCOPE-R1R4-PASS iff K1+K2+K3 hold and F1-F5 all pass;
  otherwise OPSCOPE-R1R4-FAIL with per-falsifier results.
- No bar is weakened after results are seen.
