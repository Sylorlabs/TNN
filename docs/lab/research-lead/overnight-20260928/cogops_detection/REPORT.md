# REPORT: COGOPS-DETECTION (learner-invented oscillation detection)

Date: 2026-10-03. Worker: COGOPS-DETECTION.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_detection/`
Prereg: frozen commit ce250a537 (PREREG.md + NAMECHECK.md,
committed alone before any implementation file existed). No
amendments after implementation began; erratum E1 below is a
post-execution correction of a hand-count slip in the K4 prose,
not a prereg change: the frozen Section 7 exact predictions
match the binary byte for byte. Implementation commit follows
this report.

## Verdict: BUILD-PASS (K1..K11 all PASS, with erratum E1)

The learner assembles oscillation detection from the generic
pairwise snapshot-comparison primitive. No researcher scan
runs in this battery: `osc_review` is present in the binary
via the frozen prefix but has zero call sites in the new
code and is never invoked (K8). On goal 818 the learner
proposes its own comparisons (prior=0: fail, hit),
forms a lag-2 hypothesis, verifies it on its own confirm
pass, and stores the constructed checker. On goal 820 the
prior verified on 818 fires first: one comparison, hit,
verified. On goal 821 the learner works through failures
to a lag-3 hypothesis and builds a structurally different
checker. On the convergent goal 816 every proposed
comparison fails and the generic fallback reproduces C6
byte-exact. Lesioning the prior (S10) costs a comparison;
corrupting it (S11) costs a skip plus a comparison:
S5(1) < S10(2) < S11(3), the quantitative signature that
the learner-state prior causally drives detection.

## Kill bar assessment (observed vs frozen prediction)

| Bar | Frozen prediction | Observed | Result |
|-----|-------------------|----------|--------|
| K1 | S3 block of Sec 7: Q how=1 passes=4, DET-PRIOR prior=0, 2 DET-CMP (fail, hit), DET-HYP lag=2 p=2 q=0, DET-PRIOR set=2, LEARNOSC's OSC-CYCLE, confirm ok=1, spec=1, OSC-STATE src=0 | byte-exact | PASS |
| K2 | S5 block: DET-PRIOR prior=2, exactly 1 DET-CMP (the prior pair hits), DET-HYP lag=2, Q how=1 passes=4, OSC-CYCLE phases 771/772, OSC-STATE src=0 | byte-exact | PASS |
| K3 | S6 block: DET-PRIOR prior=2, 5 DET-CMP (2 fails p=2, 2 fails + hit p=3), DET-HYP lag=3 p=3 q=0, DET-PRIOR set=3, Q how=1 passes=5, lag-3 OSC-CYCLE 781/782/783 | byte-exact | PASS |
| K4 | S8 block: DET-PRIOR prior=3, all proposed comparisons fail, no DET-HYP, Q how=0 passes=9, AGREE=1 | byte-exact vs Sec 7 (see E1 on the prose count) | PASS |
| K5 | S9: Q how=2 passes=2, 2 DET-APPLY match=3/3, OSC-CYCLE byte-identical to S3's, OSC-REUSE match=2, OSC-STATE src=0 | byte-exact | PASS |
| K6 | S10: DET-PRIOR prior=0, 2 DET-CMP (vs 1 in S5), re-invented OSC-CYCLE byte-identical to S5's, OSC-STATE src=0, DET-PRIOR set=2 | byte-exact | PASS |
| K7 | S11: DET-PRIOR prior=3, 3 DET-CMP (skip, fail, hit), OSC-CYCLE byte-identical to S5's, DET-PRIOR set=2 | byte-exact | PASS |
| K8 | c9_base cmp-identical to c8_base; c9_learn prefix cmp-identical to c8_learn; zero osc_review call sites in additive section and main; zero world literals in additive section | all verified by cmp/grep | PASS |
| K9 | 3/3 byte-identical stdout, stderr empty | sha256 4d99b0be x3; .err 0 bytes | PASS |
| K10 | safebin, no python, pure Zag, pinned znc, no while-neg-conjunction | verified | PASS |
| K11 | zero em/en dash bytes in lane docs | byte-verified clean | PASS |

Additionally the full 131-line observed stdout is
byte-identical to PREREG Section 7 (mechanical diff, not
eyeballed), including the hand-traced S10 re-specialize
lines (rev=6, union rule).

## Erratum E1 (transparent; prereg NOT silently amended)

The K4 prose said "exactly 13 DET-CMP lines (12 eq=0 plus
the skip)"; observed 12 (11 eq=0 plus the skip). Hand-count
error by the worker: per pass the learner proposes the
prior pair plus up to 3 recency pairs with duplicate
suppression, giving 3+3+3+3 = 12 events at passes 2..5.
The frozen Section 7 block (the exact line-by-line
prediction K4 points to) contains 12 DET-CMP lines and
matches the binary byte for byte, and every substantive
K4 condition holds (all comparisons fail, no DET-HYP in
S8, Q how=0 passes=9, AGREE id=S8 a=1). The binary is
correct; the K4 prose count was wrong. This is the direct
analog of LEARNOSC's erratum E1: a hand-computation gap,
behavior as designed.

## Toolchain disclosure

safebin active for every command (PATH=$HOME/safebin
exported per invocation; `$HOME/safebin` verified
directly: 49 entries, no python3/python; the lane's
safebin_setup script does not exist in this checkout,
same finding as the two predecessor workers).
`which python3` / `which python` return nothing before
and after; pinned znc
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(2026.07.0-dev) for the single build. All computation
pure Zag; shell only for znc/binary/git/assembly/byte
verification. Zero forbidden-executable invocations, no
near-misses. New Zag scanned for the `while.*!(`
negated-conjunction pattern: clean; if-nesting kept at
3 or fewer with hoisted flags per the znc defect notes.
Git writes via /usr/bin/git absolute path, explicit
pathspecs, current branch only, nothing pushed.

## Evidence detail

Invention, not scanning (K1): with no prior, the
learner's first proposal (2,1) fails and its second
(2,0) hits. The ORDER (recency) and the OUTCOME (fail
then hit) are both printed. The learner then forms the
hypothesis itself (DET-HYP), runs its own confirm pass,
and only on verification stores the checker and sets
the prior. No function in the new code iterates lags;
the only comparison primitive invoked is the single-pair
traj_state_eq.

Transfer acceleration, not replay (K2): on goal 820 the
prior=2 (verified on 818's trajectory, a different
relation and different phases) makes the FIRST proposed
pair the hit. One comparison instead of two. The
learner's past detection experience measurably changes
its future detection behavior. A fixed scan cannot do
this; there is no scan here to do it.

Not a filled template (K3): on the period-3 goal the
prior=2 pair fails twice, recency fails twice more, and
the fifth proposal (3,0) hits: lag 3. The constructed
checker has a different structure (3 phases) built from
this trajectory. The source contains no period constant
and no lag-3 special case.

No false positive (K4): on the convergent walk all 12
proposals fail (11 eq=0 plus the inapplicable-prior
skip), no hypothesis forms, the learner invents
nothing, and the generic fallback reproduces C6 exactly
(passes=9, agree=1).

Checker application (K5): on re-presentation the stored
checker is APPLIED (2 DET-APPLY match=3/3), not
re-derived: 2 passes, cycle byte-identical to the
invented one.

Causal lesion (K6/K7): zeroing the prior (S10) forces
the full recency order: 2 comparisons vs 1 with the
prior intact, same checker re-invented from scratch
(src=0). Setting a wrong prior (S11) adds the observable
skip of the inapplicable prior pair: 3 comparisons.
The strict ordering 1 < 2 < 3 is the signature that
the prior is genuinely consulted during detection, not
merely stored. Nothing else in learner state was
touched by the lesions (specs, index, plans, bindings,
world facts persist; the tombstone marks only the
single outcome entry unreachable).

Structural non-use (K8): the additive section was
verified to contain zero `osc_review` references and
zero world/goal/relation literals (comments included);
c9_main.zag calls det_handle exactly once and never
calls osc_handle. The frozen prefix still contains the
old scan (it is part of c8_learn, byte-identical), but
no execution path in this battery reaches it.

## What this establishes (and does not)

Establishes: the learner can assemble an oscillation
detection procedure from a generic comparison primitive
(L2 structural learning). The detection instance (which
pairs proposed, in which order, which hypothesis, which
checker, for which goal) is built from the learner's
trajectory experience and its verification history;
the experience-shaped prior causally modulates future
detection (lesion evidence); the researcher-provided
scan is provably unused. The hypothesis/confirm cycle
is the learner's own epistemic activity, printed in
full including failures.

Does not establish: learner-invented detection STRATEGY
(the pairwise-comparison strategy space, the
prior-then-recency proposal form, the hypothesis rule,
and the confirm protocol remain researcher-provided);
L3 representational invention (no new primitive, no
new representational form, no new procedure class; the
12-criterion bar is not claimed); lag above 3;
divergent trajectories; scaling; behavior under a
different cap. The retract path (falsified hypothesis)
is implemented but not exercised by this battery.

A note on the L2/L3 boundary, stated plainly: what the
learner invents here is the detection procedure
INSTANCE, not the detection problem formulation. The
learner does not decide that pairwise snapshot
comparison is the way to detect oscillation; the
researcher did. What the learner does decide, from
experience, is which pairs to compare (via its prior),
which hypothesis to form, and which checker to keep.
That is structural learning (L2) in the same sense as
LEARNOSC's response invention, extended one step
further down the stack. Anyone claiming more should be
asked to point at the new primitive; there is none.

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/cogops_detection/`:
PREREG.md (frozen, commit ce250a537), NAMECHECK.md
(Step 0), c9_base.zag (cmp-identical to c8_base.zag),
c9_world.zag (cmp-identical to c8_world.zag),
c9_det_additive.zag (the additive section source),
c9_learn.zag (c8 prefix cmp-identical plus the additive
det section), c9_main.zag (S1A..S11 driver; calls
det_handle, never osc_handle), c9_build.sh,
c9_full.zag (assembled; exactly one `fn main`), c9_bin,
c9_compile.txt, c9_run1/2/3.txt (sha256 4d99b0be x3) +
.err (empty), REPORT.md (this file).

## Recommended follow-ups (for the parent, not decided here)

1. Learner-chosen detection STRATEGY: give the learner
   genuinely different detectors (whole-state vs
   per-need vs alternation vs growth) as constructible
   checker forms, with experience (verification
   history) selecting among them. That is the next
   rung toward detection-strategy invention; this
   worker's prior mechanism is the substrate.
2. Exercise the retract path: a world with a
   coincidental early match would test
   hypothesis-falsification-and-continue.
3. Cross-goal analogy: whether a stored checker can
   bootstrap detection on a structurally similar but
   new oscillation (the prior helps only when the lag
   matches; analogy would need more).
4. Lag above 3 and 3+ node cycles: still declined by
   design; the proposal order would need to grow, which
   reopens the strategy question in (1).
5. Sufficiency direction for the prior: the lesion
   shows the prior's causal role in efficiency; whether
   the prior alone (without fresh comparisons) could
   drive application is untested.
