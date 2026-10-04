# PREREG AMENDMENT A to PREREG_F3P3: T-NEG world entry point

Date: 2026-09-30. Worker: F3 Phase 3 Amendment Writer.
Parent prereg: `97287f87c` (PREREG_F3P3.md).
Result doc: `57836684b` (RESULT_F3P3.md), verdict BUILD-FAIL,
T-CONJ passes, T-NEG blocked by prereg bug.
Status: AMENDMENT (documentation only). No code is changed by this
commit. No implementation, no build, no test results.
Pure Zag context. No Python. No em dashes.

## 1. The defect (documented, not hidden)

The sealed T-NEG world file `world_tneg.zag`, committed inside prereg
`97287f87c`, contains the full w_* world interface but no `fn main()`
harness entry point. The Zag toolchain requires a `main()` to produce
a native binary. The T-NEG build step

    cat $D/f3_p3.zag $D/world_tneg.zag > $D/run_p3n.zag
    $ZNC $D/run_p3n.zag -o $D/bin_p3n

fails at the compile step with `native: no main function found`
(verified in `build_p3n.err`). T-CONJ works because its world file
`f2_ablation/world_adv1.zag` ends with a `fn main()` that calls the
learner's `L_run()`; that file was written for the older F2 harness,
which required an entry point, so the entry point arrived
incidentally. The T-NEG world was written to the w_* interface list
only, and the prereg never froze the requirement that a sealed world
file supply `main()`. The word "main" does not appear as a
requirement anywhere in PREREG_F3P3.md. The defect is therefore a
prereg omission, not an implementation error and not a learner bug.

The sealed seal statement is preserved verbatim: the original file
committed in `97287f87c` is never modified. This amendment specifies
a successor artifact.

## 2. The amendment (exact specification)

A successor world file SHALL be created as

    docs/lab/research-lead/overnight-20260928/f3_phase3/world_tneg_a.zag

whose content is byte-identical to the sealed `world_tneg.zag`
EXCEPT for the following block appended after the final `w_verify`
function:

```zag

fn main()i32 {
  let m:i32=L_run();
  emit("TNEG DONE mask="); e64(m); emit("\n");
  return 0;
}
```

Rationale for this exact form:

- `L_run()` is the learner entry point defined in `f3_p3.zag`.
  The concatenation order (learner first, world second) is unchanged
  from prereg section 6, so `L_run`, `emit`, and `e64` are all in
  scope, exactly as in the T-CONJ `world_adv1.zag` main.
- The `TNEG DONE mask=` line mirrors the T-CONJ world's
  `ADV1 DONE mask=` line. It is a harness log marker only; it does
  not participate in any verdict. All T-NEG verdicts remain the
  learner-emitted `F3P3 RESULT` lines, which the build script greps.
- The sealed truth (Y(t) = X(t-1) AND NOT Z(t-1)) and every w_*
  function body are untouched. The diff between `world_tneg.zag`
  and `world_tneg_a.zag` SHALL contain only the appended main block
  plus the single blank line that precedes it. Any other diff
  invalidates the amendment.

The prereg section 6 build commands for T-NEG are amended to:

    cat $D/f3_p3.zag $D/world_tneg_a.zag > $D/run_p3n.zag
    $ZNC $D/run_p3n.zag -o $D/bin_p3n
    $D/bin_p3n > $D/raw_p3n_r1.txt 2> $D/raw_p3n_r1.err   (x3)

T-CONJ build commands are unchanged.

## 3. What is NOT changed by this amendment

- No frozen prediction changes. P-PROP-N, P-TRIAL-N, P-FAIL-N,
  P-GROW-N, P-REPLAN-N, P-COST-N, P-DET-N (prereg section 3) apply
  verbatim to the amended build.
- No falsifier changes. F-GROW-N, F-REPLAN-N, F-PROP-N, F-PURITY,
  F-DET, F-SOURCE (prereg section 4) apply verbatim. In particular
  F-PURITY still forbids any Python at any stage, and F-DET still
  requires 3 byte-identical runs.
- No kill-bar changes. K1, K2, K3, K4 (prereg section 5) apply
  verbatim. K4 (no Python anywhere, including byte checks) is
  restated here because the original Phase 3 run violated it with a
  python3 byte check; the amended T-NEG run must be clean.
- No learner changes. `f3_p3.zag` is frozen as implemented; OP-GROW
  and OP-SPLIT code are not touched.
- The original sealed `world_tneg.zag` remains in history,
  unmodified, as evidence of the original defect.

## 4. Re-freeze protocol

The seal is repaired in the open, in this order. No step may be
skipped or reordered.

1. This amendment document is committed (this commit). It changes
   no code and unblocks nothing by itself.
2. A follow-up worker creates `world_tneg_a.zag` exactly per section
   2, then publishes the full unified diff of `world_tneg.zag` vs
   `world_tneg_a.zag` in a short freeze note. The diff must show
   only the appended main block (plus one blank line). If the diff
   shows anything else, the amendment is void and the worker stops.
3. The freeze note and `world_tneg_a.zag` are committed together.
   The commit message cites this amendment document and records the
   sha256 of `world_tneg_a.zag`.
4. The commit from step 3 is the new freeze point. Its hash is
   recorded in the step-3 note. No build or test may run before the
   freeze commit exists.
5. Only then is BUILD.sh (updated per section 2) run: 3 T-NEG runs,
   md5 check, grep of `F3P3 RESULT`, zero stderr, exit code 0.
6. T-NEG results are reported against the unchanged frozen
   predictions and falsifiers. If T-NEG passes its bars while T-CONJ
   still passes, the Phase 3 verdict may be revised from BUILD-FAIL
   to the honest outcome the frozen bars produce. No bar may be
   weakened to force a pass.

## 5. Kill bars for this amendment (met by this document)

- K1 (amendment written, transparent): this file specifies the exact
  main() block, the exact new filename, and the exact amended build
  commands. The original defect is named with its evidence
  (`build_p3n.err`: `native: no main function found`).
- K2 (reason documented): section 1 explains the omission (prereg
  never froze the entry-point requirement; T-CONJ inherited main()
  from the F2-era world file; the w_* interface was complete but the
  harness contract was not).
- K3 (re-freeze specified): section 4 gives the ordered protocol,
  including the diff-only-appended-block gate, the freeze commit,
  and the no-test-before-freeze rule.

Amendment label: AMENDMENT-COMPLETE.
