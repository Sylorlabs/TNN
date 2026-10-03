# REPORT: HOOK-COMPOSITION

## Verdict: MERGE PASS (HK-R1..HK-G8 all green)

Non-ledger task. Branch `tnn-native-lab`, lane
`docs/lab/research-lead/overnight-20260928/hook_composition/`.
All commits local, never pushed.

## What was built

Act 3 (stages S12A-S12J) on top of the INTEGRATION-COMBINED binary,
porting INTEGRATION-HOOK-GENERALIZE's G1/G2/G3 battery into the
combined architecture (self-trigger M1 + B1/B2 contracts M2 + hook
M3). Additive only: hc_base/module/world/learn are byte-copies of
cb_*; hc_main is cb_main plus one additive do_query branch
(okind==4 dispatches the ported oracle_rvr), the ported G-stage
functions (verbatim logic), and the S12 stages.

## Design answers

**Q1: What breaks adding multi-need support to the combined binary?**
Five findings: (a) the hook loop itself does not break (it already
scans all plan positions; bind_fam is read-only so the continued
scan is side-effect-free) but it was never exercised with nn>1 in
the combined binary; Act 3 is its first multi-need exercise.
(b) Telemetry cell collision: hook_gen's L+13288 fire counter vs the
combined binary's L+13288 hook tag; resolved by keeping the combined
layout and translating line formats. (c) Plan-table capacity: 4
slots; post-S11 holds 813/808/818 while Act 3 needs 820+821 (union
needs 5); one disclosed clear_plans at S12A, no table growth.
(d) Binding directory: 8 slots, post-S11 holds 4, Act 3 needs 4
more; disclosed clear_bindings at S12A (stale clause bodies are
fully overwritten by u_induct on reuse). (e) World: S12A re-runs
setup_worldA (byte-identical across lanes, full reset).

**Q2: Does retirement (decline=1) interact with self-trigger?** No.
do_query returns immediately on st==0, before oracle/agree/trigger-B;
the decline path calls no u_invalidate, so no RETRY is emitted.
Proven by HK-G3: decline=1 with zero RETRY lines in Act 3.

**Mechanism delta: none.** The generalized hook was already latent
in the combined binary; hook_gen's three findings transfer as
architectural properties. The merge work is the battery, not the
mechanism. Zero learn-file changes.

## Results

**Regression HK-R1/R2: PASS.** Lines 1-87 byte-identical to
cb_run1.txt (Act 1, hook dormant); lines 88-97 byte-identical (S11).

**HK-G1 multi-need interior: PASS.** Exactly one
`HOOK gtag=820 need=1 tag=804 oldfam=0 newfam=1`; G1Q1 rebuilds with
st=2 agree=1. The inline hook loop handles nn=3 and interior stale
positions.

**HK-G2 coverage needs no hook: PASS.** `S12-NOFIRE hook=0` after the
RET coverage narrowing (602 only); exactly 3 HOOK lines in the whole
run (S11, G1Q1, G2Q1R).

**HK-G3 retirement x self-trigger: PASS.** The G2Q1R block is
exactly `HOOK gtag=821 need=0 tag=806 oldfam=0 newfam=-1` followed by
`Q id=G2Q1R goal=821 decline=1`; zero RETRY lines in Act 3.

**HK-G4 restore: PASS.** G2Q2 st=2 agree=1; final PLAN dump is
exactly `PLAN goal=820 n=3 [2:805:0] [1:804:1] [0:803:0]` and
`PLAN goal=821 n=1 [0:806:0]`.

**HK-G5 lazy: PASS.** Only two clear_plans call sites (S8
pre-existing, S12A disclosed); none in the S12B-S12J path.

**HK-G6 determinism: PASS.** 3/3 byte-identical,
sha256 c7c39f52761015566abffe6b96415ce2d73669615a270e3ac92a45e83eceb62e,
stderr empty, exit 0.

**HK-G7 toolchain: PASS.** Safebin from first command, pure Zag,
pinned znc; prereg committed alone before implementation; amendment
N1 committed alone before the corrected build.

**HK-G8 hygiene: PASS.** Zero em/en dash bytes; no world literals in
executable new code (all tags/rels/objs/goals runtime-derived).

SUMMARY-HOOKGEN (frozen, reproduced exactly):
`agree=13 plans_built=8 plans_loaded=9 trials=21 declines=1 cs=1952
cg=3528 hook=2 covdc=2,0,0`.

## Prereg amendment N1 (transparent)

The first build broke the frozen G2Q0 line: trigger-B fired twice
and the query agreed on generic fallback instead of first-try spec
agree. Root cause was a design miss in the S12A apparatus, not a
mechanism failure: the L-state spec-procedure indexes are
world-relative (fact indices into the live world); S10E built them
on drifted world A2, and S12A restored world A without
re-specializing, so ret_spec read A2 positions against world-A facts
(0 subjects for (601,621)). Self-trigger handled it exactly as
designed (bounded retries, coverage contract retired, generic
fallback, agree). Correction: S12A now re-specializes ret/vfy/cnt on
the restored world A (S10E precedent; u_induct path, no counter
effects, admit sets unchanged). All frozen predictions then held
verbatim. The broken run's artifacts were discarded; the sequence is
recorded in PREREG.md section 8.

## New integration finding

World-relative learner indexes must be re-specialized after a world
restore; the S-contract version routing and the L-index must agree
on the live world. Trigger-B is the safety net when they diverge
(observed live). Follow-ups: (1) 4-slot plan-table eviction policy
(the 5-goal union does not fit; not patched here); (2) trigger-B
attribution (I-4) extended to binding-retirement causes; (3) the
stale-index recovery observed here as a dedicated experiment.

## Commits (local only)

- 8d965446e prereg + namecheck (alone)
- aba2a8f59 prereg amendment N1 (alone)
- (implementation)
- (artifacts)
- (this report)

## Artifacts

- `hc_base/world/module/learn.zag`: sources (base/module/world/learn
  byte-copies of cb_*)
- `hc_main.zag`: cb_main + okind=4 branch, ported G-stage functions,
  S12A-S12J
- `hc_build.sh`: build script
- `hc_full.zag`, `hc_bin` (sha256
  33141bcae85da032ab479375965a8610c6f4abffa0587bc976550a3ebdfcf1b9)
- `hc_run1/2/3.txt`: 3/3 byte-identical (128 lines), stderr empty
- `hc_compile.txt`: clean compile log
