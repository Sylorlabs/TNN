# PREREG: COGOPS-LEARNOSC2 (outcome-record ablation; follow-up to COGOPS-LEARNOSC)

Date: 2026-10-03. Worker: COGOPS-LEARNOSC-FOLLOWUP.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_learnosc2/`
Parent lane: `docs/lab/research-lead/overnight-20260928/cogops_learnosc/`
Status: FROZEN on commit (this file + NAMECHECK.md committed alone
before any implementation file exists). No amendments after
implementation begins.

## 1. Research question

COGOPS-LEARNOSC (BUILD-PASS K1-K9) showed the learner inventing an
oscillation response from its trajectory/outcome record (S3: 4
passes, how=1) and reusing the stored response on re-presentation
(S9: 2 passes, how=2). K5's stated causal claim: "the outcome
record drives behavior; without it the handling would cost the
full invention path." That claim was never tested by lesion:
S9 shows correlation (record present, reuse happens), not
necessity.

This worker runs the missing lesion. After S9, the harness zeroes
the outcome-record entry count (one learner-state word, L+14500)
and re-presents goal 818 under otherwise identical conditions
(S10 ABLATE-818). Prediction: the learner falls back to the full
invention path (how=1, passes=4, confirm pass, src=0), proving the
reuse advantage in S9 was causally downstream of the outcome
record and not an epiphenomenon of specs, index, plans, or world
facts.

## 2. Design

### 2.1 The lesion (researcher intervention, not learner machinery)

`outc_clear(L)` in c8_main.zag (harness): `set32(L,14500,0)`.
This is the ONLY learner-state mutation between S9 and S10. It
zeroes the OUTC entry count word; entry payload bytes remain in
L but are unreachable to `outc_find` (it scans `e < n` with
`n = get32(L,14500)`), so the find-visible state is exactly that
of a fresh run (`z_alloc` zero-initializes). The intervention is
deliberately minimal: specs, index, plans, bindings, and world
facts persist untouched, so any behavioral change is attributable
to the outcome record alone.

### 2.2 The control structure

S10 mirrors S9 exactly (setup_worldD, re-specialize ret/vfy on
the same episodes, same SPEC/LSTATE emission, do_losc on goal
818 with doagree=0). The SPEC/LSTATE lines are a positive
control: they prove the lesion did not damage the rest of
learner state (spec machinery still works, SPECCHK stays 1).
S9 (record intact) is the sham control: identical stage,
record present, reuse expected.

### 2.3 Causal logic and falsification

- If S10 prints how=1 passes=4 with the S3-identical cycle,
  confirm ok=1, src=0: the reuse advantage (2 passes, how=2)
  depended on the record. Necessity established; K5's causal
  story completes.
- If S10 prints how=2 passes=2 (reuse persists without the
  record): the record is NOT the causal driver. K5's story is
  falsified. Report as INFORMATIVE-FAIL with the observed
  bytes; do not salvage.
- If S10 prints how=0 (generic fallback) or phases differing
  from S3's: the invention path is not robust to the lesion
  condition. Report as INFORMATIVE-FAIL.
- The lesion tests NECESSITY, not sufficiency: it does not show
  the record alone would produce handling without trajectory
  machinery (that machinery is generic and held fixed).

### 2.4 What changes vs the parent (additivity)

- c8_base.zag: byte copy of c7_base.zag (cmp-verified).
- c8_world.zag: byte copy of c7_world.zag (cmp-verified).
- c8_learn.zag: byte copy of c7_learn.zag (cmp-verified; ZERO
  changes to learner code: the lesion is a harness operation).
- c8_main.zag: byte copy of c7_main.zag plus exactly two
  additions: the `outc_clear` helper and the S10 stage block
  before SUMMARY (diff-verified).
- No world literals in new code (14500 is a structural L
  offset, same class as 13240/13224 already used by the
  harness; "S10" is a stage label).

### 2.5 The honest boundary (what this does NOT claim)

- Not learner-invented detection: the recurrence scan and the
  lesion are both researcher-side; the learner's detection
  machinery is unchanged and ungeneralized.
- Not L3 representational invention: no new representation,
  primitive, or procedure form; the 12-criterion bar is not
  claimed. Scope is L2 (structural learning) plus a causal
  ablation of L2 state.
- Not a test of sufficiency, lag above 3, multi-node cycles,
  scaling, or cross-goal analogy (open follow-ups 1-3 from the
  parent report).

## 3. Kill bars (frozen)

- K1 (lesion kills the reuse advantage): S10 prints
  `Q id=S10 goal=818 how=1 passes=4`. Falsified by how=2 or
  passes=2 (reuse without the record) or how=0 (fallback).
- K2 (re-invention constructs the identical cycle): S10's
  OSC-CYCLE line is byte-identical to S3/S9's:
  `OSC-CYCLE goal=818 lag=2 nph=2
  ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]`.
- K3 (learner-owned verification and provenance): S10 prints
  `OSC-CONFIRM goal=818 ok=1`, `SPECCHK goal=818 spec=1`,
  `OSC-STATE goal=818 lag=2 nph=2 src=0` (src=0: re-invented,
  not replayed; OSC-REUSE must NOT appear).
- K4 (no regression, exact control): every stdout line from
  `STAGE S1A RET-LEARN` through S9's
  `OSC-STATE goal=818 lag=2 nph=2 src=0` is byte-identical to
  the parent's frozen c7_run1.txt; the full c8 stdout differs
  from c7_run1.txt ONLY in the appended S10 stage and in
  SUMMARY `plans_loaded=3` (was 2: S10's plan_find hits the
  plan built in S3).
- K5 (intervention purity): c8_base.zag cmp-identical to
  c7_base.zag; c8_world.zag cmp-identical to c7_world.zag;
  c8_learn.zag cmp-identical to c7_learn.zag; c8_main.zag
  differs from c7_main.zag only by the `outc_clear` helper
  plus the S10 stage block; zero world literals in new code.
- K6: 3/3 byte-identical stdout across runs, stderr empty.
- K7: safebin active for every command, PATH=$HOME/safebin,
  `which python3` / `which python` empty, all computation
  pure Zag, pinned znc only, new code scanned for the
  `while.*!(` negated-conjunction pattern.
- K8: zero em/en dash bytes in all lane docs.
- K9 (scope honesty): REPORT.md states the L2 scope, the
  necessity-not-sufficiency reading, and the open follow-ups;
  no L3 or detection-invention claim.

Verdict rule: BUILD-PASS requires K1..K9 all PASS. A miss on
K1..K4 is INFORMATIVE-FAIL (mechanism/causality); a miss on
K5..K9 is PROCESS-FAIL.

## 4. Implementation plan (post-freeze)

- cp parent c7_base/c7_world/c7_learn to c8_* (cmp-verified).
- c8_main.zag: parent c7_main.zag + outc_clear fn + S10 stage.
- c8_build.sh: assemble (base+world+learn+main), compile with
  the pinned znc
  `~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
  run 3x, cmp, sha256. Lane path corrected to tnn-rsi-gpi3.
- Verify K1..K9 against Section 7; write REPORT.md.

## 5. Governance notes

- Pure Zag. safebin mandatory from the first command.
- Opaque identifiers throughout; zero world literals in
  c8_learn.zag (inherited by byte copy); zero world literals
  in the c8_main additions.
- Commits local, never pushed, explicit pathspecs only,
  on the current branch; no other lane touched.
- This prereg is adopted as frozen without modification.

## 6. What success would establish (and not)

Would establish: the outcome record is NECESSARY for the reuse
advantage (2 passes, stored-cycle emission). Removing it costs
the full invention path (4 passes, confirm, src=0) with the
identical cycle reconstructed from the trajectory. K5's causal
claim becomes lesion evidence rather than correlation.

Would not establish: sufficiency of the record, learner-invented
detection, L3 invention, lag above 3, multi-node cycles,
scaling, cross-goal analogy.

## 7. Frozen exact predictions

Every stdout line the battery prints, in order. Lines S1A
through S9 are byte-copied from the parent's frozen c7_run1.txt
(the BUILD-PASS run); S10 is hand-traced from the osc_handle
path with OUTC empty (Section 2); SUMMARY is updated for the
one additional plan_find hit (plans_loaded 2 to 3).

```
STAGE S1A RET-LEARN
EP ep=0 ret n=1
EP ep=1 ret n=1
EP ep=2 ret n=1
EP ep=3 ret n=1
SPEC-RET rev=1 nrel=2 ep0=0 ep1=3 nfacts=56
LSTATE-RET nrel=2 ids=601,602 cnts=16,16 prov=0,0,3,56 rev=1
STAGE S1B VFY-LEARN
EP ep=4 vfy v=1
EP ep=5 vfy v=1
EP ep=6 vfy v=1
EP ep=7 vfy v=0
SPEC-VFY rev=1 nrel=3 ep0=4 ep1=7 nfacts=56
LSTATE-VFY nrel=3 ids=601,602,603 cnts=16,16,16 prov=1,4,7,56 rev=1
STAGE S2 OSC-LEARN-D
EP ep=8 ret n=1
EP ep=9 ret n=1
EP ep=10 ret n=1
EP ep=11 ret n=1
SPEC-RET rev=2 nrel=3 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=3 ids=601,602,606 cnts=16,16,3 prov=0,8,11,61 rev=2
EP ep=12 vfy v=1
SPEC-VFY rev=2 nrel=4 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=4 ids=601,602,603,608 cnts=16,16,16,2 prov=1,12,12,61 rev=2
STAGE S3 OSC-D0
Q id=S3 goal=818 how=1 passes=4
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-CONFIRM goal=818 ok=1
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
STAGE S4 OSC-LEARN-E
EP ep=13 ret n=1
EP ep=14 ret n=1
EP ep=15 ret n=1
EP ep=16 ret n=1
EP ep=17 ret n=1
EP ep=18 ret n=1
EP ep=19 ret n=1
EP ep=20 ret n=1
SPEC-RET rev=3 nrel=5 ep0=13 ep1=20 nfacts=68
LSTATE-RET nrel=5 ids=601,602,606,613,615 cnts=16,16,0,3,4 prov=0,13,20,68 rev=3
EP ep=21 vfy v=1
EP ep=22 vfy v=1
SPEC-VFY rev=3 nrel=6 ep0=21 ep1=22 nfacts=68
LSTATE-VFY nrel=6 ids=601,602,603,608,614,616 cnts=16,16,16,0,2,3 prov=1,21,22,68 rev=3
STAGE S5 OSC-E0
Q id=S5 goal=820 how=1 passes=4
OSC-CYCLE goal=820 lag=2 nph=2 ph0=[1,611][1,771][1,771] ph1=[1,611][1,772][1,772]
OSC-CONFIRM goal=820 ok=1
SPECCHK goal=820 spec=1
OSC-STATE goal=820 lag=2 nph=2 src=0
STAGE S6 OSC-E1
Q id=S6 goal=821 how=1 passes=5
OSC-CYCLE goal=821 lag=3 nph=3 ph0=[1,611][1,781][1,781] ph1=[1,611][1,782][1,782] ph2=[1,611][1,783][1,783]
OSC-CONFIRM goal=821 ok=1
SPECCHK goal=821 spec=1
OSC-STATE goal=821 lag=3 nph=3 src=0
STAGE S7 CYCLE-LEARN-C
EP ep=23 ret n=1
EP ep=24 ret n=1
EP ep=25 ret n=1
SPEC-RET rev=4 nrel=6 ep0=23 ep1=25 nfacts=72
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,0,0,0,8 prov=0,23,25,72 rev=4
EP ep=26 vfy v=1
SPEC-VFY rev=4 nrel=7 ep0=26 ep1=26 nfacts=72
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,0,0,0,8 prov=1,26,26,72 rev=4
STAGE S8 CONV-816
Q id=S8 goal=816 how=0 passes=9
AGREE id=S8 a=1
STAGE S9 REUSE-818
SPEC-RET rev=5 nrel=6 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,3,0,0,0 prov=0,8,11,61 rev=5
SPEC-VFY rev=5 nrel=7 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,2,0,0,0 prov=1,12,12,61 rev=5
Q id=S9 goal=818 how=2 passes=2
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-REUSE goal=818 match=2
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
STAGE S10 ABLATE-818
SPEC-RET rev=6 nrel=6 ep0=8 ep1=11 nfacts=61
LSTATE-RET nrel=6 ids=601,602,606,613,615,604 cnts=16,16,3,0,0,0 prov=0,8,11,61 rev=6
SPEC-VFY rev=6 nrel=7 ep0=12 ep1=12 nfacts=61
LSTATE-VFY nrel=7 ids=601,602,603,608,614,616,605 cnts=16,16,16,2,0,0,0 prov=1,12,12,61 rev=6
Q id=S10 goal=818 how=1 passes=4
OSC-CYCLE goal=818 lag=2 nph=2 ph0=[1,611][1,661][1,661] ph1=[1,611][1,662][1,662]
OSC-CONFIRM goal=818 ok=1
SPECCHK goal=818 spec=1
OSC-STATE goal=818 lag=2 nph=2 src=0
SUMMARY-LOSC agree=1 plans_built=4 plans_loaded=3 trials=6 declines=0
```
